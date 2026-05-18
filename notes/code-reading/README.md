# WarpX Source 代码精读总索引

绑定源码：`../warpx/Source`，`pkuHEDPbranch / 063f8b586f04321e13150ae3e730e0794ca75cb1`。

本目录按 `docs/warpx-source-reading-framework.md` 组织。每个子目录是一个源码模块入口，后续详细笔记都挂在对应模块下。

## 阶段 0 模块入口

| 模块入口 | 对应 `Source` 路径 | 当前职责 |
|---|---|---|
| `root/` | 根层 `main.cpp`、`WarpX.*`、`Fields.H` | 程序入口、主类、全局状态 |
| `initialization/` | `Initialization/` | 初始化、参数、注入器、外场、div cleaner |
| `evolve/` | `Evolve/` | 时间推进、`OneStep` 分派、dt |
| `particles/` | `Particles/` | 粒子容器、gather、push、deposition、多物理粒子 |
| `fieldsolver/` | `FieldSolver/` | FDTD、PSATD、electrostatic、implicit、hybrid |
| `boundary/` | `BoundaryConditions/` | PML、PEC、field boundary |
| `parallelization/` | `Parallelization/` | guard cells、通信、regrid、AMR 同步 |
| `diagnostics/` | `Diagnostics/` | full/reduced diagnostics、I/O、restart |
| `embedded-boundary/` | `EmbeddedBoundary/` | EB 初始化、face extension、particle scraping |
| `filter/` | `Filter/` | bilinear filter、NCI Godfrey filter |
| `laser/` | `Laser/` | laser profile 和 laser 注入 |
| `fluids/` | `Fluids/` | fluid species、MUSCL-Hancock、fluid current |
| `nonlinear-solvers/` | `NonlinearSolvers/` | Newton/Picard/KSP/SNES/PC |
| `accelerator-lattice/` | `AcceleratorLattice/` | beamline elements 和 lattice finder |
| `python/` | `Python/` | pyWarpX、callbacks、field/particle access |
| `utils/` | `Utils/` | parser、algorithm selection、moving window、常量 |
| `ablastr/` | `ablastr/` | MultiFabRegister、Poisson、communication、logging |

## 执行规则

每个模块推进时必须同步四类产物：

1. `notes/code-reading/<module>/NN-*.md`：源码证据和调用链。
2. `manuscript/chapters/*.md`：正文源码块和物理/算法解释。
3. `docs/source-map.md`：源码路径、函数、行号、章节映射。
4. `TODO.md`：完成状态、阻塞点和下一步。

关键函数、类和 kernel 的正文讲解必须包含真实源码原文块。
