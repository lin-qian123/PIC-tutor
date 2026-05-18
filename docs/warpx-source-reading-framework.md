# WarpX Source 全源码精读框架

记录日期：2026-05-14

绑定源码：

- 路径：`../warpx/Source`
- 分支：`pkuHEDPbranch`
- commit：`063f8b586f04321e13150ae3e730e0794ca75cb1`
- 统计口径：只读本地源码；`.H/.cpp` 为主要精读对象，`CMakeLists.txt`、`Make.package` 用于确认模块边界和编译开关。

## 1. 为什么需要重排精读顺序

前几轮已经深入了主循环、粒子推进、field gather、shape factor 和部分沉积 kernel，但这仍然只是 WarpX `Source` 的局部路径。WarpX 的真实源码结构不是“一个 PIC loop 加几个函数”，而是由以下几类系统交织组成：

1. 执行骨架：`main.cpp`、`WarpX` 主类、初始化、时间推进、AMR/并行、诊断。
2. PIC 核心：粒子容器、gather、pusher、deposition、场求解、同步、边界。
3. 场求解族：FDTD、PSATD、electrostatic、magnetostatic、implicit、hybrid PIC、macroscopic media。
4. 多物理：碰撞、MCC、stopping、电离、QED、Schwinger、流体、加速器晶格。
5. 工程支撑：`ablastr`、parser、utility、Python binding、I/O、filter、load balance、restart。

因此后续不能按“某个感兴趣模块”继续写，而应先建立覆盖全部 `Source` 的精读框架，再逐个任务完成。

## 2. 全局模块盘点

当前 `../warpx/Source` 约 712 个文件，其中 `.H/.cpp` 主体约 562 个文件。按顶层目录统计：

| 顶层模块 | 文件数 | `.H/.cpp` 行数级别 | 主要职责 | 精读优先级 |
|---|---:|---:|---|---|
| 根层 `main/WarpX/Fields` | 6 | 5k+ | 程序入口、主类、全局状态、field registry 入口 | P0 |
| `Evolve` | 4 | 1.6k | 全局时间推进、`OneStep` 分派、dt 计算 | P0 |
| `Initialization` | 32 | 6k+ | AMReX/WarpX 初始化、参数、注入器、外场、温度/速度分布、div cleaner | P0 |
| `Particles` | 173 | 33k+ | 粒子容器、gather、push、deposition、collision、QED、边界、初始化、排序、重采样 | P0 |
| `FieldSolver` | 132 | 23k+ | FDTD、PSATD、electrostatic、implicit、hybrid、magnetostatic、QED field push | P0 |
| `BoundaryConditions` | 20 | 6k+ | 场边界、PML、PEC、insulator、PML current | P1 |
| `Parallelization` | 9 | 3k+ | guard cells、通信、regrid、sum guard cells | P1 |
| `Diagnostics` | 133 | 22k+ | full/reduced diagnostics、openPMD、plotfile、checkpoint、BTD、functors | P1 |
| `EmbeddedBoundary` | 13 | 2k+ | EB 初始化、face extension、particle scraping、distance | P1 |
| `Filter` | 9 | 700+ | bilinear/current filter、NCI Godfrey filter | P1 |
| `Laser` | 8 | 1.3k | laser profiles、from file、Gaussian、field function | P1 |
| `Fluids` | 9 | 2.4k | cold fluid、MUSCL-Hancock、fluid current deposition | P2 |
| `NonlinearSolvers` | 20 | 4.7k | Newton/Picard/KSP/SNES/PC 抽象和 PETSc wrapper | P2 |
| `AcceleratorLattice` | 18 | 1.2k | drift、quadrupole、plasma lens、lattice element finder | P2 |
| `Python` | 12 | 1.1k | pyWarpX binding、callbacks、particle/field Python access | P2 |
| `Utils` | 36 | 5k+ | algorithm selection、parser、moving window、species utils、constants、ionization table | P1 |
| `ablastr` | 78 | 8k+ | MultiFabRegister、Poisson solvers、coarsen、FFT、logging、communication | P1 |

优先级含义：

- P0：必须先读。没有它们无法解释 WarpX 如何执行 PIC。
- P1：必须早读。它们决定物理正确性、边界、同步、I/O 和验证。
- P2：按应用章推进。它们是重要扩展，但依赖 P0/P1 的执行框架。

## 3. 编译边界和模块依赖

根层 `Source/Make.package` 只显式加入：

- `main.cpp`，当 `USE_PYTHON_MAIN != TRUE`；
- `WarpX.cpp`；
- `Source` include path。

CMake 模块边界由各子目录 `CMakeLists.txt` 决定。关键入口：

| 构建入口 | 直接加入文件 | 子目录 |
|---|---|---|
| `Particles/CMakeLists.txt` | `MultiParticleContainer.cpp`、`ParticleBoundaries.cpp`、`PhotonParticleContainer.cpp`、`PhysicalParticleContainer.cpp`、`RigidInjectedParticleContainer.cpp`、`WarpXParticleContainer.cpp`、`LaserParticleContainer.cpp`、`ParticleBoundaryBuffer.cpp`、`SpeciesPhysicalProperties.cpp`、`ExternalParticleFields.cpp` | `Collision`、`Deposition`、`ElementaryProcess`、`Gather`、`ParticleCreation`、`ParticleThermalizer`、`Pusher`、`Resampling`、`Sorting` |
| `FieldSolver/CMakeLists.txt` | `WarpXPushFieldsEM.cpp`、`WarpXPushFieldsHybridPIC.cpp`、`WarpX_QED_Field_Pushers.cpp`、`WarpXSolveFieldsES.cpp` | `ElectrostaticSolvers`、`FiniteDifferenceSolver`、`MagnetostaticSolver`、`ImplicitSolvers`、`SpectralSolver` when `WarpX_FFT` |

这说明源码精读需要同时看目录结构和构建文件。某些算法不是在顶层显式出现，而是通过子目录条件加入，例如 PSATD 依赖 `WarpX_FFT`，QED internals 位于 `Particles/ElementaryProcess/QEDInternals`。

## 4. 精读输出规范

每个模块完成时必须产生四类产物：

| 产物 | 位置 | 要求 |
|---|---|---|
| 源码笔记 | `notes/code-reading/<module>/NN-*.md` | 记录读取日期、commit、源码路径、函数/类、行号、调用关系、未解决问题 |
| 正文草稿 | `manuscript/chapters/*.md` | 先物理/算法推导，再源码原文块，再逐行/逐块解释 |
| 映射更新 | `docs/source-map.md` | 新增源码路径、行号、主题、对应章节、验证例子 |
| TODO 状态 | `TODO.md` | 标记已读、已入正文、待验证、阻塞点 |

关键函数或 kernel 的讲解必须包含真实源码原文块，不能只给路径和行号。大型文件允许按功能块拆分，但每个被解释的代码结论都必须能回到源码块。

## 5. 精读任务模板

每个任务按以下顺序执行：

1. 读构建边界：`CMakeLists.txt`、`Make.package`。
2. 读公开接口：`.H` 中 class、struct、enum、public methods。
3. 读执行入口：被 `WarpX::Evolve()`、初始化、参数解析或 Python/API 调用的函数。
4. 读内层 kernel：`ParallelFor`、GPU device function、模板分派、维度宏分支。
5. 写物理/算法推导：连续方程、离散化、时间层、守恒量、边界条件。
6. 写源码块解释：路径、行号、源码原文、逐行/逐块解释。
7. 关联参数：`docs/parameter-map.md` 和源码 `ParmParse`。
8. 关联示例/测试：`docs/example-regression-map.md`。
9. 关联文献：`docs/literature-map.md`，必要时 MinerU 处理。
10. 更新 `README.md`、`TODO.md`、`docs/source-map.md`。

## 6. 全源码精读阶段

### 阶段 0：全局结构和阅读基础

目标：建立后续所有模块的导航。

- [x] 生成 `docs/module-inventory.md`。
- [x] 生成 `docs/parameter-map.md`。
- [x] 生成 `docs/example-regression-map.md`。
- [x] 生成 `docs/literature-map.md`。
- [x] 建立本框架文档。
- [ ] 人工复核每个模块的实际构建边界和条件编译开关。
- [ ] 为每个顶层模块建立 `notes/code-reading/<module>/README.md`。

### 阶段 1：根层主类和全局状态

模块：

- `main.cpp`
- `WarpX.H`
- `WarpX.cpp`
- `Fields.H`
- `WarpXVersion.cpp`

必须回答：

- 程序如何从 `main()` 进入 AMReX 和 WarpX 单例？
- `WarpX` 主类持有哪些全局状态？
- `Fields` / `MultiFabRegister` 如何抽象字段所有权？
- 哪些成员决定 geometry、AMR、solver、particles、diagnostics？

输出：

- `notes/code-reading/root/00-main-and-warpx-singleton.md`
- `notes/code-reading/root/01-warpx-state-map.md`
- `manuscript/chapters/03-warpx-evolve.md` 继续补全主类成员图。

当前状态：已部分完成，需要补 `WarpX.H/WarpX.cpp/Fields.H` 的类成员分区表。

### 阶段 2：初始化和参数系统

模块：

- `Initialization/WarpXAMReXInit.*`
- `Initialization/WarpXInit.*`
- `Initialization/WarpXInitData.cpp`
- `Initialization/PlasmaInjector.*`
- `Initialization/InjectorDensity.H`
- `Initialization/InjectorMomentum.H`
- `Initialization/InjectorPosition.H`
- `Initialization/InjectorFlux.H`
- `Initialization/GetTemperature.*`
- `Initialization/GetVelocity.*`
- `Initialization/ExternalField.*`
- `Initialization/DivCleaner/ProjectionDivCleaner.*`
- `Utils/Parser/*`
- `Utils/WarpXAlgorithmSelection.H`

必须回答：

- 参数如何从 inputs 文件进入 `WarpX`、species、laser、solver、diagnostics？
- species density、momentum、temperature、position 分布如何被 parser / table / file 控制？
- 外场是 grid field 还是 particle field？何时叠加？
- divergence cleaner 初始化解决哪个约束？

输出：

- 参数解析源码地图。
- species 初始化正文小节。
- 外场与 moving window 正文小节。

### 阶段 3：全局时间推进

模块：

- `Evolve/WarpXEvolve.cpp`
- `Evolve/WarpXComputeDt.cpp`
- `Utils/WarpXMovingWindow.cpp`

必须回答：

- `Evolve()`、`OneStep()`、`OneStep_nosub()`、`OneStep_sub1()`、`OneStep_JRhom()` 的区别是什么？
- 显式、隐式、静电、hybrid、subcycling、moving window 如何分派？
- `ComputeDt()` 如何结合 CFL、粒子速度、boosted frame 和 solver 限制？

当前状态：已完成 `Evolve/OneStep/OneStep_nosub` 第一轮；仍需补 `OneStep_sub1`、`OneStep_JRhom`、moving window 和 `ComputeDt` 细节。

### 阶段 4：粒子系统主干

模块：

- `Particles/MultiParticleContainer.*`
- `Particles/WarpXParticleContainer.*`
- `Particles/PhysicalParticleContainer.*`
- `Particles/PhotonParticleContainer.*`
- `Particles/LaserParticleContainer.*`
- `Particles/RigidInjectedParticleContainer.*`
- `Particles/SpeciesPhysicalProperties.*`
- `Particles/ExternalParticleFields.*`
- `Particles/ParticleIO.H`

必须回答：

- 多 species、物理粒子、光子、激光粒子、刚性注入粒子的类层次是什么？
- SoA/AoS 属性如何组织？`PIdx`、`DiagIdx`、runtime component 如何映射物理量？
- 粒子数据如何初始化、推进、重分布、restart、diagnostics 输出？

当前状态：已读显式主链；仍需补类层次、属性系统、photon/laser/rigid containers、I/O。

### 阶段 5：粒子 gather / pusher / position update

模块：

- `Particles/Gather/FieldGather.H`
- `Particles/Gather/GetExternalFields.*`
- `Particles/Gather/ScaleFields.H`
- `Particles/Pusher/*`
- `Particles/ShapeFactors.H`
- `Particles/Algorithms/KineticEnergy.H`

必须回答：

- field gather 的 momentum-conserving / energy-conserving / Galerkin 路径如何对应公式？
- Boris、Vay、Higuera-Cary、radiation reaction、implicit pusher、photon pusher 的差别是什么？
- 位置推进如何处理 massive/massless 粒子？

当前状态：已入正文的有 Boris、Vay、Higuera-Cary、`doGatherShapeN()` 主路径、shape factor 主路径。待补 radiation reaction、implicit pusher、external gather、所有维度分支。

### 阶段 6：沉积、形函数和源项同步

模块：

- `Particles/Deposition/ChargeDeposition.H`
- `Particles/Deposition/CurrentDeposition.H`
- `Particles/Deposition/MassMatricesDeposition.H`
- `Particles/Deposition/TemperatureDeposition.H`
- `Particles/Deposition/VarianceAccumulationBuffer.*`
- `Particles/Deposition/SharedDepositionUtils.H`
- `Particles/Filter/FilterFunctors.H`
- `Parallelization/WarpXSumGuardCells.*`
- `Parallelization/GuardCellManager.*`
- `Evolve/WarpXEvolve.cpp::SyncCurrentAndRho`

必须回答：

- charge、current、mass matrix、temperature、variance 的沉积对象分别是什么？
- Direct、Esirkepov、Villasenor、Vay、implicit charge-conserving、shared-memory deposition 的适用条件是什么？
- 源项如何在 tile、species、level、AMR、guard cells、PML/buffer 之间同步？

当前状态：已入正文的有 charge deposition、direct current、Esirkepov 3D 主路径。待补 Villasenor、Vay、implicit、shared memory、mass/temperature/variance。

### 阶段 7：场求解器总入口

模块：

- `FieldSolver/WarpXPushFieldsEM.cpp`
- `FieldSolver/WarpXPushFieldsEM_K.H`
- `FieldSolver/WarpXSolveFieldsES.cpp`
- `FieldSolver/WarpXPushFieldsHybridPIC.cpp`
- `FieldSolver/WarpX_QED_Field_Pushers.cpp`
- `FieldSolver/WarpX_QED_K.H`

必须回答：

- `EvolveE/B/F/G` 如何从 `WarpX::OneStep*` 调到具体 solver？
- FDTD、PSATD、PML、QED、hybrid、electrostatic 的 field push 入口如何分派？
- field data 在 `Efield_fp/aux/cp`、`Bfield_fp/aux/cp`、`current_fp/buf`、`rho_fp/buf` 之间如何流动？

输出：第 6 章重写入口。

### 阶段 8：FDTD、PML、宏观介质和 filter

模块：

- `FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.*`
- `FieldSolver/FiniteDifferenceSolver/EvolveE.cpp`
- `FieldSolver/FiniteDifferenceSolver/EvolveB.cpp`
- `FieldSolver/FiniteDifferenceSolver/EvolveF.cpp`
- `FieldSolver/FiniteDifferenceSolver/EvolveG.cpp`
- `FieldSolver/FiniteDifferenceSolver/EvolveEPML.cpp`
- `FieldSolver/FiniteDifferenceSolver/EvolveBPML.cpp`
- `FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/*`
- `FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/*`
- `FieldSolver/FiniteDifferenceSolver/MacroscopicEvolveE.cpp`
- `Filter/*`
- `BoundaryConditions/PML*`

必须回答：

- Yee/CKC/nodal/RZ/spherical FDTD 的离散 curl 如何实现？
- PML split-field / damping / current damping 如何实现？
- filter 在 current、rho、fields 上何时作用？
- macroscopic media 如何改写 Maxwell update？

### 阶段 9：谱求解器 PSATD

模块：

- `FieldSolver/SpectralSolver/SpectralSolver.*`
- `FieldSolver/SpectralSolver/SpectralFieldData*`
- `FieldSolver/SpectralSolver/SpectralKSpace*`
- `FieldSolver/SpectralSolver/SpectralAlgorithms/*`
- `FieldSolver/SpectralSolver/SpectralHankelTransform/*`

必须回答：

- FFT/Hankel 数据结构如何组织？
- PSATD、Galilean、Comoving、JRhom、averaged Galilean、PML spectral algorithms 的公式如何映射到代码？
- current correction、Vay deposition、charge conservation 在谱空间如何实现？

### 阶段 10：静电、磁静态、隐式和非线性求解器

模块：

- `FieldSolver/ElectrostaticSolvers/*`
- `FieldSolver/MagnetostaticSolver/*`
- `FieldSolver/ImplicitSolvers/*`
- `NonlinearSolvers/*`
- `ablastr/fields/*`

必须回答：

- Poisson/effective potential/relativistic electrostatic 的方程是什么？
- magnetostatic solver 解什么变量？
- semi-implicit、theta-implicit、Strang implicit spectral 的未知量和残差如何定义？
- Newton/Picard/GMRES/PETSc wrapper 如何接入 WarpX field/particle 数据？

### 阶段 11：边界、嵌入边界、AMR 和通信

模块：

- `BoundaryConditions/*`
- `EmbeddedBoundary/*`
- `Particles/ParticleBoundaries.*`
- `Particles/ParticleBoundaryBuffer.*`
- `Particles/Sorting/*`
- `Parallelization/WarpXComm.*`
- `Parallelization/WarpXRegrid.cpp`
- `ablastr/coarsen/*`
- `ablastr/utils/Communication.*`

必须回答：

- field boundary 和 particle boundary 如何分别解析、检查、执行？
- PML、PEC、insulator、Silver-Mueller、periodic 的边界条件如何进入 field/particle 更新？
- EB 如何初始化、扩展 face、刮擦粒子和处理沉积附近 shape？
- AMR regrid、guard cells、buffer、coarse/fine 同步如何构成完整路径？

### 阶段 12：碰撞、电离、QED 和多物理

模块：

- `Particles/Collision/*`
- `Particles/ElementaryProcess/Ionization.*`
- `Particles/ElementaryProcess/QEDPhotonEmission.*`
- `Particles/ElementaryProcess/QEDPairGeneration.*`
- `Particles/ElementaryProcess/QEDSchwingerProcess.H`
- `Particles/ElementaryProcess/QEDInternals/*`
- `Utils/Physics/IonizationEnergiesTable.H`

必须回答：

- Binary collision、DSMC、MCC、stopping、bremsstrahlung、nuclear fusion、linear Compton、linear Breit-Wheeler 的事件抽样和权重处理是什么？
- ADK/OTB ionization 如何读取能级、改变 ionization level、创建电子？
- Quantum synchrotron、Breit-Wheeler、Schwinger 的光学深度、查表和粒子创建如何实现？

### 阶段 13：流体、hybrid PIC、激光和加速器晶格

模块：

- `Fluids/*`
- `FieldSolver/FiniteDifferenceSolver/HybridPICModel/*`
- `FieldSolver/FiniteDifferenceSolver/HybridPICSolveE.cpp`
- `Laser/*`
- `AcceleratorLattice/*`

必须回答：

- cold fluid 与 PIC 粒子如何共享 field/source？
- hybrid PIC 的 Ohm law、electron pressure、external vector potential 如何进入 E update？
- laser profiles 和 laser particle container 的关系是什么？
- lattice elements 如何给粒子施加束线力？

### 阶段 14：诊断、I/O、Python 和工具层

模块：

- `Diagnostics/*`
- `Python/*`
- `Utils/*`
- `ablastr/*`

必须回答：

- diagnostics 如何选择 field/particle/reduced/BTD/checkpoint 输出？
- openPMD、plotfile、checkpoint 的数据布局和重启语义是什么？
- Python callbacks 和 pyWarpX 如何访问 WarpX 主对象、fields、particles？
- `ablastr` 的 MultiFabRegister、Poisson solvers、logging、FFT、communication 为 WarpX 提供了什么公共层？

## 7. 建议的书稿章节重排

当前 `manuscript/chapters/00-09` 可以保留，但后续应扩展为下列长书结构：

| 卷/章 | 内容 | 主要源码 |
|---|---|---|
| 卷 I：PIC 物理基础 | Vlasov-Maxwell、宏粒子、shape、leapfrog、守恒、稳定性 | 理论和文献为主 |
| 卷 II：WarpX 执行骨架 | main、WarpX 主类、初始化、时间推进、参数系统 | 根层、`Initialization`、`Evolve`、`Utils/Parser` |
| 卷 III：粒子核心 | container、属性、gather、pusher、deposition、源项同步 | `Particles`、`Parallelization` |
| 卷 IV：场求解 | FDTD、PSATD、electrostatic、implicit、hybrid、filter | `FieldSolver`、`Filter`、`NonlinearSolvers` |
| 卷 V：边界和 AMR | PML、PEC、particle boundaries、EB、AMR、guard cells | `BoundaryConditions`、`EmbeddedBoundary`、`Parallelization` |
| 卷 VI：多物理 | collisions、ionization、QED、fluids、laser、lattice | `Particles/Collision`、`ElementaryProcess`、`Fluids`、`Laser`、`AcceleratorLattice` |
| 卷 VII：诊断和工程系统 | diagnostics、openPMD、checkpoint、Python、ablastr、构建 | `Diagnostics`、`Python`、`ablastr` |
| 卷 VIII：案例验证 | Langmuir、uniform plasma、LWFA、RPA、MCC、QED、hybrid、EB | `Examples`、`Regression`、本地运行记录 |

## 8. 下一步执行队列

为了避免继续局部漂移，后续任务按如下队列推进：

1. 补全阶段 0：为每个模块建立 `notes/code-reading/<module>/README.md`，并在 `source-map` 中加入全模块框架入口。
2. 回到阶段 1：精读 `WarpX.H/WarpX.cpp/Fields.H`，画出主类状态和 field registry。
3. 阶段 2：精读初始化和参数系统，修正 `parameter-map` 中自动命中的不准确项。
4. 阶段 3：补完 `OneStep_sub1`、`OneStep_JRhom`、`ComputeDt`、moving window。
5. 阶段 4-6：在已有粒子章节基础上补齐属性系统、photon/laser/rigid、Villasenor/Vay/implicit deposition、mass/temperature deposition。
6. 阶段 7-10：开始场求解卷，先 FDTD，再 PSATD，再 electrostatic/implicit/hybrid。
7. 阶段 11-14：边界/AMR、多物理、诊断/Python/ablastr。

每完成一个阶段，都必须运行一次文档一致性检查：

```text
README.md 是否反映当前状态
TODO.md 是否标记完成/待做
docs/source-map.md 是否新增源码证据
notes/code-reading/<module>/ 是否有 README 和笔记
正文是否有源码原文块
未解决问题是否显式保留
```
