# Python 接口源码精读入口

绑定源码：`../warpx/Source/Python`。

## 模块边界

- 构建入口：`Python/CMakeLists.txt`、`Python/Make.package`。
- 主要文件：`pyWarpX.*`、`WarpX.cpp`、`callbacks.*`、`MultiFabRegister.cpp`、`Particles/*.cpp`。

## 核心问题

- pybind11 模块如何暴露 WarpX 主类、fields、particles 和 boundary buffer。
- Python callbacks 在时间推进中何时触发。
- Python main 与 C++ main 的边界是什么。

## 精读顺序

1. `pyWarpX.*`。
2. `WarpX.cpp` binding。
3. `callbacks.*`。
4. `MultiFabRegister.cpp`。
5. `Particles/*.cpp`。

## 输出目标

- `00-python-module-init.md`
- `01-callbacks.md`
- `02-field-particle-access.md`
- `03-field-wrapper-validation-map.md`

## 当前进度

- 已完成 `00-python-module-init.md`：梳理维度专用 pybind shared object 的编译期分裂、`_libwarpx.py` 的 geometry-aware lazy load、`pyWarpX.cpp` 的模块组装，以及 PICMI `Simulation.step()` 如何最终落回 `WarpX::InitData/Evolve`。
- 已完成 `01-callbacks.md`：梳理 C++ 侧名字到 `std::function<void()>` 的最小 callback 表、Python `CallbackFunctions` 聚合对象如何桥接到 C++、固定 callback 名集合、以及 callback 异常当前直接 `exit(3)` 的运行边界。
- 已完成 `02-field-particle-access.md`：梳理 `multifab_register`、`multi_particle_container`、`particle_boundary_buffer` 三条 pybind 访问面、PICMI `sim.fields` / `sim.particles` convenience property 的真实指向，以及 `particle_data_python` / `particle_boundary_scrape` / `python_wrappers` 这三条 active contract 如何分别验证 field、particle 和 boundary-buffer 访问层。
- 已完成 `03-field-wrapper-validation-map.md`：把 `sim.fields.get(...)`、PML split fields、`F/G` cleaning 标量与 `MultiFabRegister` 接到最小强 regression。

## 验证线索

- `Examples/Tests/python_wrappers/`
- `Examples/Tests/particle_data_python/`
- `Examples/Tests/projection_div_cleaner/`
