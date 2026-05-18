# Python 00: pybind module init, geometry dispatch, and PICMI bootstrap

绑定源码：

- `../warpx/Source/Python/pyWarpX.cpp`
- `../warpx/Source/Python/pyWarpX.H`
- `../warpx/Source/Python/WarpX.cpp`
- `../warpx/Python/pywarpx/_libwarpx.py`
- `../warpx/Python/pywarpx/picmi.py`

这篇先回答三个问题：

1. Python 入口是怎么按维度选到正确的 pybind 模块的。
2. pybind 暴露的最低层对象是什么。
3. PICMI `Simulation.step()` 最后怎样落到 C++ `WarpX::InitData/Evolve`。

## 1. pybind 模块名在编译期就按维度分裂

`Source/Python/pyWarpX.cpp` 里，`PYBIND11_MODULE(...)` 的名字不是固定的 `warpx_pybind`，而是按编译维度展开：

- `warpx_pybind_1d`
- `warpx_pybind_2d`
- `warpx_pybind_rz`
- `warpx_pybind_rcylinder`
- `warpx_pybind_rsphere`
- `warpx_pybind_3d`

这意味着 Python 端并不是运行时再切 geometry kernel，而是：

- 先编译出维度专用 shared object
- 再在 Python 里按 `geometry.dims` 选择加载哪个模块

## 2. `_libwarpx.py` 才是 Python 侧真正的 loader

`pywarpx/_libwarpx.py` 的 `LibWarpX` 用惰性加载方式管理 pybind shared object。

只有当代码第一次访问：

- `libwarpx.libwarpx_so`

时，`load_library()` 才会触发。

它会先检查：

- `pywarpx.Geometry.geometry.dims`

然后选择：

- `amrex.space1d`
- `amrex.space2d`
- `amrex.space3d`

以及对应的：

- `warpx_pybind_1d`
- `warpx_pybind_2d`
- `warpx_pybind_rz`
- `warpx_pybind_3d`

所以当前 Python 入口的真实合同是：

- geometry 必须先定义
- shared object 才能被正确选择并导入

## 3. `LibWarpX` 不是仅读库，还负责扩展 pybind 类型

`load_library()` 在导入 pybind 模块后，还会做第二层拼装：

- `register_warpx_MultiFab_extension`
- `register_warpx_MultiFabRegister_extension`
- `register_warpx_MultiParticleContainer_extension`
- `register_warpx_WarpXParticleContainer_extension`

这说明当前 Python API 不是纯 C++ pybind 表面，而是：

1. C++ 暴露基础对象
2. Python 再给这些对象挂更多便捷方法

也就是说，读 `Source/Python/*.cpp` 只看到了一半接口，另一半在 `pywarpx/extensions/*.py`。

## 4. `pyWarpX.cpp` 负责组装 pybind 模块骨架

`PYBIND11_MODULE(...)` 里当前初始化顺序是：

1. `init_MultiFabRegister`
2. `init_WarpXParticleContainer`
3. `init_WarpXParIter`
4. `init_BoundaryBufferParIter`
5. `init_ParticleBoundaryBuffer`
6. `init_MultiParticleContainer`
7. `init_WarpX`

然后再额外挂：

- `amr`
- `__version__`
- `__author__`
- `__license__`

以及几类模块级函数：

- `amrex_init`
- `amrex_finalize`
- `getNProcs`
- `getMyProc`
- `add_python_callback`
- `remove_python_callback`
- `execute_python_callback`

所以当前 pybind 模块的最低层职责是：

- 暴露 WarpX singleton
- 暴露 MultiFab / particle / boundary buffer 这些运行态对象
- 暴露 AMReX 初始化与 callback 注册壳

## 5. `WarpX.cpp` binding 不是另起一个 Python 仿真器

`Source/Python/WarpX.cpp` 里 `init_WarpX()` 最核心的绑定只有三类：

### 5.1 lifecycle

- `get_instance`
- `finalize`
- `initialize_data`
- `evolve`

这说明 Python 并没有一个和 C++ 并列的新时间推进器。它最终还是直接调用：

- `WarpX::InitData`
- `WarpX::Evolve`

### 5.2 state accessors

- `max_level`
- `finest_level`
- `Geom`
- `DistributionMap`
- `boxArray`
- `multifab_register`
- `multi_particle_container`
- `get_particle_boundary_buffer`

这组接口的角色是把当前 C++ 运行态对象借给 Python，而不是复制一份镜像状态。

### 5.3 runtime controls

例如：

- `sync_rho`
- `getistep`
- `gett_new`
- `getdt`
- `set_potential_on_domain_boundary`
- `set_potential_on_eb`
- `run_div_cleaner`
- `synchronize_velocity_with_position`

因此 `WarpX.cpp` binding 的真实定位是：

- 一个“把现有 C++ runtime 管理对象和少量控制旋钮暴露给 Python”的薄桥

## 6. PICMI bootstrap 的真实终点

`pywarpx/picmi.py` 里真正把用户级 `Simulation` 落到 WarpX runtime 的地方很短：

```text
initialize_inputs()
initialize_warpx()
pywarpx.warpx.step(nsteps)
```

其中：

- `initialize_warpx(mpi_comm=None)`
  - 会调用 `pywarpx.warpx.init(...)`
- `step(...)`
  - 若未初始化，先 `initialize_inputs()`
  - 再 `initialize_warpx()`
  - 最后 `pywarpx.warpx.step(nsteps)`

所以 PICMI `Simulation.step()` 的真实链是：

```text
PICMI Simulation
-> pywarpx high-level object graph
-> _libwarpx lazy-load and init
-> pybind WarpX singleton
-> WarpX::InitData()
-> WarpX::Evolve()
```

## 7. `mpi_comm` 当前仍是明确未完成边界

`_libwarpx.py` 的：

- `amrex_init(argv, mpi_comm=None)`

当前如果 `mpi_comm is not None`，直接：

```text
raise Exception("mpi_comm argument not yet supported")
```

因此当前 Python/PICMI 侧关于 MPI communicator handoff 的真实状态是：

- 参数口已经在高层 API 上存在
- 但底层 runtime 初始化仍未支持非空 communicator 传入

这和 `pass_mpi_communicator` 那类 regression 当前停在 scaffold 状态是一致的。

## 8. 当前最适合给书稿的总括

Python 这条线当前最准确的三层描述是：

1. 编译层  
   维度专用 pybind module 在编译期分裂。
2. 绑定层  
   `pyWarpX.cpp` 和 `WarpX.cpp` 暴露 singleton、fields、particles、boundary buffer 与少量 runtime controls。
3. 高层装配层  
   `_libwarpx.py` 和 `picmi.py` 负责 geometry-aware lazy load、类型扩展、PICMI 输入拼装，以及把 `Simulation.step()` 最终落回 `WarpX::InitData/Evolve`。

这也是后面分别看 callbacks 和 field/particle access 时必须先固定住的总骨架。
