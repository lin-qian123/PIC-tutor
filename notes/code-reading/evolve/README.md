# Evolve 源码精读入口

绑定源码：`../warpx/Source/Evolve`。

本目录记录 WarpX 主生命周期与时间推进路径的逐段源码阅读。所有源码路径默认相对于同级只读仓库 `../warpx`，当前源码基线见 `TODO.md`。

## 模块边界

- 构建入口：`Evolve/CMakeLists.txt`、`Evolve/Make.package`。
- 主要文件：`WarpXEvolve.cpp`、`WarpXComputeDt.cpp`。
- 关联模块：`Utils/WarpXMovingWindow.cpp`、`Particles`、`FieldSolver`、`Diagnostics`、`Parallelization`。

## 核心问题

- `Evolve()`、`OneStep()`、`OneStep_nosub()`、`OneStep_sub1()`、`OneStep_JRhom()` 的物理和算法差别。
- 显式/隐式、电磁/静电/hybrid、AMR/subcycling/moving window 如何分派。
- `ComputeDt()` 如何结合 CFL、solver、boosted frame、粒子速度和用户限制。

## 阅读顺序

1. `00-lifecycle-and-callgraph.md`：从 `main.cpp` 到 `WarpX::Evolve` 的对象生命周期、初始化顺序和总调用图。
2. `01-pic-time-layers.md`：从 Vlasov-Maxwell 方程到 leapfrog PIC 时间层，再映射到 `OneStep_nosub`。
3. `02-evolve-source-evidence.md`：`WarpXEvolve.cpp`、`WarpXComputeDt.cpp`、`WarpXInitData.cpp` 的行号证据表。
4. `03-subcycling-and-jrhom.md`：`OneStep_sub1()` 两层 AMR subcycling 与 `OneStep_JRhom()` PSATD 多源项时间依赖循环。
5. `04-compute-dt-and-adaptive-timestep.md`：`ComputeDt()`、`UpdateDtFromParticleSpeeds()` 与自适应时间步。
6. `05-moving-window.md`：moving window 的连续窗口坐标、整数 cell 平移、连续注入和 boosted-frame 速度变换。

## 输出目标

- 继续扩写 `manuscript/chapters/03-warpx-evolve.md`。
- 为场求解、粒子系统、诊断和 AMR 章节提供调用链入口。

## 本轮已确认的核心事实

- 可执行入口是 `Source/main.cpp`，主序列是初始化外部库、取得 `WarpX` 单例、`InitData()`、`Evolve()`、`Finalize()`、结束外部库。
- `WarpX` 构造函数会调用 `ReadParameters()`，随后建立时间步数组、粒子容器、边界缓冲和可选的流体容器。
- `InitData()` 负责诊断对象、`ComputeDt()`、从头初始化或 checkpoint 恢复、PML/宏观介质/静电与 hybrid 初始化、初始自洽场和初始诊断。
- `Evolve()` 是外层时间步循环；`OneStep()` 是求解器和 AMR/subcycling 分派；`OneStep_nosub()` 是显式电磁无 subcycling 的第一个精读样板。
- `PushParticlesandDeposit()` 不是实际粒子核函数，而是选择沉积目标字段名后转入 `MultiParticleContainer::Evolve()`。
- `OneStep_sub1()` 把 fine level 推进两次小步、coarse level 推进一次大步，并通过 fine-to-coarse current/rho contribution 保持 coarse patch 同步。
- `OneStep_JRhom()` 是 PSATD 专用循环，粒子 push/gather 一次，但在多个相对时间重复沉积 `J/rho` 并在谱空间推进场。
- moving window 在每步末尾先更新连续窗口位置，再按整数 cell 平移 `MultiFab` 数据，并在新露出的整数 cell 层做连续粒子/流体注入。
