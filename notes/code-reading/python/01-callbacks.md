# Python 01: callback registry, C++ bridge, and execution boundary

绑定源码：

- `../warpx/Source/Python/callbacks.H`
- `../warpx/Source/Python/callbacks.cpp`
- `../warpx/Source/Python/pyWarpX.cpp`
- `../warpx/Python/pywarpx/callbacks.py`
- `../warpx/Python/pywarpx/_libwarpx.py`

这篇只回答 callback 这条线：

1. Python callback 是怎么注册到 C++ 的。
2. 真正执行 callback 的对象是谁。
3. 当前错误处理和运行边界是什么。

## 1. C++ 侧只有一个最小名字到函数映射表

`Source/Python/callbacks.cpp` 当前核心状态只有：

```text
std::map<std::string, std::function<void()> > warpx_callback_py_map;
```

C++ 层提供的接口也非常薄：

- `InstallPythonCallback(name, callback)`
- `IsPythonCallbackInstalled(name)`
- `ExecutePythonCallback(name)`
- `ClearPythonCallback(name)`

所以 C++ 并不维护 callback 列表、装饰器语法、方法对象生命周期这些复杂逻辑。它只认：

- 一个名字
- 一个可调用 `std::function<void()>`

## 2. Python 侧真正的 callback manager 是 `CallbackFunctions`

`pywarpx/callbacks.py` 里的 `CallbackFunctions` 才是完整注册表。

它负责：

- 保存多个函数
- 支持普通函数、实例方法、字符串名
- 管理 timer
- 支持 `singlefunconly`
- 支持 `lcallonce`

也就是说，用户以为在“向 WarpX 注册很多 callback”，实际发生的是：

1. Python 侧先自己维护一整组函数列表
2. 只有当某个 callback 名下第一次有函数时
3. 才把 `CallbackFunctions` 这个聚合对象本身注册给 C++

## 3. C++ 看见的不是用户函数，而是 Python 聚合对象

`CallbackFunctions.installfuncinlist()` 里最关键的一步是：

```text
if len(self.funcs) == 0:
    libwarpx.libwarpx_so.add_python_callback(self.name, self)
```

所以 C++ 层真正持有的是：

- 某个 callback name
- 对应的 `CallbackFunctions.__call__`

后续当 C++ 执行：

```text
ExecutePythonCallback(name)
```

实际进入的是 Python 侧：

```text
CallbackFunctions.__call__()
-> callfuncsinlist()
-> 逐个执行用户函数
```

这解释了为什么 Python 侧可以支持：

- 多个函数
- decorator
- 实例方法弱/强引用处理
- 计时统计

而 C++ 仍然保持极简。

## 4. callback 名字集合是 Python 侧显式定义的合同

`pywarpx/callbacks.py` 的文档字符串已经把当前支持的 callback 点列得很清楚，包括：

- `loadExternalFields`
- `beforeInitEsolve`
- `afterInitEsolve`
- `afterinit`
- `beforeEsolve`
- `poissonsolver`
- `afterEsolve`
- `afterBpush`
- `afterEpush`
- `beforedeposition`
- `afterdeposition`
- `beforestep`
- `afterstep`
- `afterdiagnostics`
- `oncheckpointsignal`
- `onbreaksignal`
- `particlescraper`
- `particleloader`
- `particleinjection`

这组名字本身就是 Python/C++ 的共享协议。

## 5. callback 触发时机仍然由 C++ 主循环决定

Python 可以安装函数，但不能重新定义 callback 时机。

真正何时调用：

- `afterinit`
- `particleloader`
- `beforestep`
- `afterstep`
- `afterdiagnostics`

仍然是 C++ 主循环、初始化链、外场加载链里显式调用 `ExecutePythonCallback(name)` 决定的。

因此当前 callback 体系更准确的描述是：

- Python 决定“在某个命名槽位里放哪些函数”
- C++ 决定“这些槽位什么时候被执行”

## 6. `_libwarpx.initialize()` 里已经硬编码了两次早期 callback

`_libwarpx.py` 在：

```text
self.warpx.initialize_data()
self.libwarpx_so.execute_python_callback("afterinit")
self.libwarpx_so.execute_python_callback("particleloader")
```

这说明 Python 初始化路径里有两个非常关键的事实：

1. `afterinit`
   - 是在 `WarpX::InitData()` 完成后立即执行
2. `particleloader`
   - 是 Python 层显式在初始化完成后触发
   - 不是用户想象中的“完全由 C++ 粒子装载器内部回调”

这也是 `particleloader` / `beforeInitEsolve` / `loadExternalFields` 这些 hooks 在项目文档里需要和主循环 callback 分开描述的原因。

## 7. 错误处理边界很硬：callback 异常直接 `exit(3)`

`ExecutePythonCallback(name)` 里的异常处理当前是：

```text
catch (std::exception &e) {
    std::cerr << ...
    std::exit(3);
}
```

源码注释还明确解释：

- 不用 `amrex::Abort()`
- 是为了避免 MPI runs hang

因此当前 callback 合同不是“异常能被优雅回抛到用户 Python 层”，而是：

- callback 一旦在 C++ 触发点抛异常
- 当前进程直接终止

这条边界必须写清，否则用户很容易误判 debug 行为。

## 8. `clear_all()` 和 finalize 的责任划分

`_libwarpx.finalize()` 在 `amrex_finalize()` 后会：

```text
from pywarpx import callbacks
callbacks.clear_all()
```

而 `CallbackFunctions.clearlist()` 又会：

- 清空 Python 函数表
- 调 `remove_python_callback(self.name)`

所以 callback 生命周期的当前责任链是：

- Python finalize 负责清场
- C++ 只负责把 name->callable 的入口删掉

## 9. 对项目最重要的结论

这条主线最值得固定下来的不是 callback 名单本身，而是这个三层结构：

```text
user function / decorator
-> Python CallbackFunctions registry
-> one aggregate callable per callback name registered to C++
-> C++ ExecutePythonCallback(name) at fixed lifecycle points
```

以及一个必须明确的运行边界：

- callback 异常当前不会优雅回到 Python REPL
- 会直接 `exit(3)` 以避免 MPI hang

这也是后面读 `particle_boundary_scrape`、`spacecraft_charging`、`loadExternalFields`、外部 Poisson solver callback 时的共同底层合同。
