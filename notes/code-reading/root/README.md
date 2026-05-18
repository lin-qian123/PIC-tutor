# Root / WarpX 主类源码精读入口

绑定源码：`../warpx/Source`，`pkuHEDPbranch / 063f8b586f04321e13150ae3e730e0794ca75cb1`。

## 模块边界

- 根层文件：`main.cpp`、`WarpX.H`、`WarpX.cpp`、`Fields.H`、`WarpXVersion.cpp`。
- 构建入口：`Source/Make.package` 加入 `main.cpp` 和 `WarpX.cpp`；CMake 顶层由上级工程组织。

## 核心问题

- `main()` 如何进入 AMReX 初始化、Python callback 和 `WarpX::Evolve()`。
- `WarpX` 主类持有哪些全局状态：geometry、AMR、fields、particles、solvers、diagnostics、参数选项。
- `Fields.H` 与 `ablastr::fields::MultiFabRegister` 如何承载场数据命名和所有权。

## 精读顺序

1. `main.cpp`：程序入口与异常/并行初始化。
2. `WarpX.H`：主类成员按物理和工程职责分区。
3. `WarpX.cpp`：构造、析构、单例、参数读取入口和辅助函数。
4. `Fields.H`：field key、MultiFab registry、field ownership。
5. `WarpXVersion.cpp`：版本和构建信息。

## 输出目标

- `00-main-and-warpx-singleton.md`
- `01-warpx-state-map.md`
- 更新 `manuscript/chapters/03-warpx-evolve.md` 的主类状态图。

## 验证线索

- 最小运行案例：`Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`。
- 对照文档：`Docs/source/developers/repo_organization.rst`。
