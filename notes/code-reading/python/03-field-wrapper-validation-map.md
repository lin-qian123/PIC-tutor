# `python_wrappers`：field wrapper、PML split fields 与 script-local assert 的验证边界

绑定源码与测试：

- `../warpx/Examples/Tests/python_wrappers/CMakeLists.txt`
- `../warpx/Examples/Tests/python_wrappers/inputs_test_2d_python_wrappers_picmi.py`
- `../warpx/Examples/Tests/python_wrappers/analysis_default_regression.py`
- `../warpx/Python/pywarpx/fields.py`
- `../warpx/Python/pywarpx/extensions/MultiFabRegister.py`
- `../warpx/Source/Python/MultiFabRegister.cpp`

这组 regression 不验证粒子物理，也不是单纯 writer smoke test。它真正验证的是：

1. PICMI `Simulation` 初始化后，Python 侧能否通过 `sim.fields.get(...)` 稳定拿到 WarpX 注册表里的 `MultiFab`。
2. 这些 `MultiFab` 是否同时覆盖 valid domain、PML split fields 和 divergence-cleaning 标量。
3. Python 返回的数组视图在推进后是否还能保留正确的形状、分量和数值内容。

当前目录下的 `analysis_default_regression.py` 只是本地 checksum helper 副本；真正的强断言全部写在 input 脚本本身。

## 1. CMake 注册：只有 checksum，没有独立 analysis 脚本

`CMakeLists.txt` 里这组只有一个测试：

```cmake
if(WarpX_FFT)
    add_warpx_test(
        test_2d_python_wrappers_picmi  # name
        2  # dims
        2  # nprocs
        inputs_test_2d_python_wrappers_picmi.py  # inputs
        OFF  # analysis
        "analysis_default_regression.py --path diags/diag1000100"  # checksum
        OFF  # dependency
    )
endif()
```

所以如果只看 CMake，很容易误判成“纯 checksum-only”。但这条测试的强断言不在独立 `analysis.py`，而是直接内嵌在 PICMI input 脚本末尾。

## 2. 脚本真正验证的是 `sim.fields.get(...)`

input 先构造一个 2D PICMI 最小骨架：

- `ElectromagneticSolver(method="PSATD")`
- `divE_cleaning=1`
- `divB_cleaning=1`
- `pml_divE_cleaning=1`
- `pml_divB_cleaning=1`
- `warpx_psatd_update_with_rho=True`
- x/z 两侧 open boundary + PML

然后在 `sim.initialize_inputs(); sim.initialize_warpx()` 之后，直接通过 Python wrapper 抓取字段寄存器：

```python
Ex = sim.fields.get("Efield_fp", dir="x", level=0)
Ey = sim.fields.get("Efield_fp", dir="y", level=0)
Ez = sim.fields.get("Efield_fp", dir="z", level=0)
Bx = sim.fields.get("Bfield_fp", dir="x", level=0)
By = sim.fields.get("Bfield_fp", dir="y", level=0)
Bz = sim.fields.get("Bfield_fp", dir="z", level=0)
F = sim.fields.get("F_fp", level=0)
G = sim.fields.get("G_fp", level=0)
Expml = sim.fields.get("pml_E_fp", dir="x", level=0)
Eypml = sim.fields.get("pml_E_fp", dir="y", level=0)
Ezpml = sim.fields.get("pml_E_fp", dir="z", level=0)
Bxpml = sim.fields.get("pml_B_fp", dir="x", level=0)
Bypml = sim.fields.get("pml_B_fp", dir="y", level=0)
Bzpml = sim.fields.get("pml_B_fp", dir="z", level=0)
Fpml = sim.fields.get("pml_F_fp", level=0)
Gpml = sim.fields.get("pml_G_fp", level=0)
```

这条链直接覆盖了：

- 主寄存器 `Efield_fp/Bfield_fp`
- divergence-cleaning 标量 `F_fp/G_fp`
- PML split-field `pml_E_fp/pml_B_fp`
- PML cleaning 标量 `pml_F_fp/pml_G_fp`

因此它验证的是 Python field-wrapper 覆盖面，而不是某一个孤立字段。

## 3. 断言结构：不是图像，而是逐分量 benchmark 求和

脚本会在 valid domain 里给 `E/B/F/G` 填一个平滑 unit pulse，然后推进 `100` 步。之后虽然会画很多 `figure_*.png`，但这些图不是 regression 本体。本体是后面的 `check_values(...)`：

```python
def check_values(benchmark, data, comp, rtol, atol):
    passed = np.allclose(
        benchmark, np.sum(np.abs(data[(), (), comp])), rtol=rtol, atol=atol
    )
    assert passed
```

其中 `data[(), (), comp]` 这一写法也有特殊含义：

- `()` 表示取出 valid + ghost 全部索引范围；
- `comp` 用来访问 split-field 的不同 component；
- 最终比较的是整个数组绝对值求和后的标量 benchmark。

脚本按同一套 `rtol = 5e-08`、`atol = 1e-12`，依次断言：

- `Ex/Ey/Ez`
- `Bx/By/Bz`
- `F/G`
- `Expml/Eypml/Ezpml` 的各 split component
- `Bxpml/Bypml/Bzpml` 的各 split component
- `Fpml/Gpml` 的各 component

其中还显式验证若干理论上应为零的分量，例如：

```python
check_values(0.0, Eypml, 2, rtol, atol)
check_values(0.0, Ezpml, 1, rtol, atol)
check_values(0.0, Bypml, 2, rtol, atol)
check_values(0.0, Bzpml, 1, rtol, atol)
check_values(0.0, Fpml, 1, rtol, atol)
check_values(0.0, Gpml, 1, rtol, atol)
```

所以它真正验证的是：

- Python wrapper 返回的数组 shape / component 解释没有错；
- PML split-field component 的排列没有错；
- valid domain 和 PML 区里的 `E/B/F/G` 在推进后数值与 benchmark 一致。

## 4. 为什么这条测试不该只记成 “Python API / callbacks”

当前 `example-regression-map.md` 里把它粗写成 `Python API / callbacks` 容易误导，因为这条测试：

- 没有粒子 callback；
- 没有 boundary-buffer callback；
- 重点也不是 runtime particle attributes。

它更准确的定位应当是：

- `Python field wrapper / MultiFabRegister / PML and cleaning fields`

也就是：

1. PICMI 前端把 solver/PML/cleaning 对象图接起来；
2. `pywarpx` 把 C++ `MultiFabRegister` 暴露到 Python；
3. Python 侧通过 `sim.fields.get(...)` 拿到非 owning `MultiFab` 视图；
4. 这些视图在 valid/PML/ghost/component 维度上都能被正确消费。

## 5. 和 `fields.py` / `MultiFabRegister` 的源码边界

`pywarpx/fields.py` 顶部已经明确提示老的 `MultiFabWrapper` 正在退场：

```python
warnings.warn(
    """The fields wrapper is now obsolete ...
    recommended way ... is the 'sim.fields.get' routine ...""",
    UserWarning,
)
```

当前推荐路径是 `sim.fields.get(...)`，它真正绑定到：

- `pywarpx/extensions/MultiFabRegister.py`
- `Source/Python/MultiFabRegister.cpp`

Python 扩展层只是薄封装：

```python
if dir is None:
    mf = self._get(name=name, level=level)
else:
    mf = self._get(name=name, dir=dir, level=level)
```

而 C++ binding 真正暴露的是：

```cpp
.def("_get",
     py::overload_cast<
         std::string,
         ablastr::fields::Direction,
         int
     >(&MultiFabRegister::get<std::string>),
     py::return_value_policy::reference_internal,
     py::arg("name"),
     py::arg("dir"),
     py::arg("level")
)
```

因此这条 regression 本质上是在验证：

- `MultiFabRegister::get(...)`
- Python `Direction`
- 非 owning `MultiFab` 视图
- 以及 field registry 里的命名约定

这些 Python binding 合同没有被 PML/split-field/component 复杂度搞坏。

## 6. 当前最准确的记录口径

这组测试当前应记成：

- `field solver / Python field wrapper / PML split-field access`

并补一句边界：

- 活跃强断言写在 input 脚本内部，不在独立 `analysis.py`
- 目录下 `analysis_default_regression.py` 只提供 checksum 比较

这样才不会把它误降成纯 checksum，也不会误写成粒子 callback regression。
