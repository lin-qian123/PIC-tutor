# WarpX 全源码精读书写作计划

> **For agentic workers:** REQUIRED: 后续执行本计划时，先按章节建立源码证据表，再写正文。每个任务使用 checkbox 跟踪；若需要并行执行，按模块切分，不能让不同 worker 同时改同一章节文件。

**Goal:** 写出一本从物理过程、数学推导、数值算法到 WarpX 真实源码逐行解读的完整中文书稿，覆盖本地 `../warpx` 的所有主要模块、物理模型、算法路径、示例、测试和文献证据。

**Architecture:** 书稿采用“物理模型 -> 离散算法 -> WarpX 调用链 -> 源码原文摘录 -> 文件级/函数级/关键内核逐行解读 -> 输入参数 -> 示例验证 -> 文献闭环”的固定结构。全书不是按源码目录机械翻译，而是先建立物理和算法主线，再把每个源码模块嵌入对应章节；同时保留一个完整源码索引附录，保证没有模块被遗漏。

**Tech Stack:** Markdown-first 书稿、`../warpx` 本地源码、WarpX 官方文档、WarpX `refs.bib`、`references/` PDF 文献库、MinerU 论文转换、WarpX Examples/Regression、本地运行验证。

---

## 0. 当前绑定的源码状态

- WarpX 路径：`../warpx`
- 分支：`pkuHEDPbranch`
- commit：`063f8b586f04321e13150ae3e730e0794ca75cb1`
- 计划创建日期：2026-05-14
- 只读约束：本项目默认不修改 `../warpx`。

每次正式写入源码解释前，必须重新记录当日分支和 commit。如果 commit 变化，章节开头必须注明“本章依据的源码版本”。

## 1. 对前一版草稿的修正

前一版 `manuscript/` 只能作为目录草稿，不能作为正式书稿。它的问题是：

- 物理推导停留在概述，没有从连续方程逐步推到离散式。
- 代码解释只引用少数函数，没有逐行讲清调用关系、数据结构、时间层和边界状态。
- 覆盖范围过窄，只碰到 `Evolve`、少量 `Particles`、少量 `FieldSolver`。
- 文献没有真正进入推导和代码判断。
- 示例验证没有形成“运行 -> 输出 -> 物理量 -> 源码路径”的闭环。

后续写作以本文档为准。旧 `docs/master-plan.md` 保留为早期思路，不再作为深度要求的唯一依据。

## 2. “讲透”的验收标准

每个章节、每个源码模块都要满足以下标准：

1. **物理过程清楚**：说明模拟的物理对象、方程、近似、守恒律、适用条件和失效条件。
2. **数学推导完整**：从连续方程推到离散变量、时间层、网格位置、粒子权重、形函数和更新公式。
3. **算法边界明确**：说明算法保证什么，不保证什么；稳定性、精度、噪声、守恒误差来自哪里。
4. **源码路径准确**：记录文件、类、函数、行号范围、调用者、被调用者、输入参数和输出状态。
5. **源码原文必须出现**：讲解源码时必须先放对应真实源码块，标注路径、函数和行号范围，再解释；不能只写路径和行号。
6. **关键代码逐行解释**：物理内核、算法分支、数据交换、边界处理、参数解析必须逐行或逐块解释；纯 boilerplate 可以文件级解释，但不能跳过其职责。
7. **示例验证闭环**：至少给出一个官方 Example 或 Regression 对应关系；能本地跑的要记录命令、环境变量、输出目录和检查脚本。
8. **文献闭环**：每个核心算法都要有原始论文或权威教材；论文需要深入使用时按 MinerU 转 Markdown 并写中文讲解笔记。

## 3. 总产物

- `docs/warpx-full-code-reading-book-plan.md`：本文档，作为最高优先级写作计划。
- `docs/source-map.md`：动态更新的源码-章节映射表。
- `docs/literature-map.md`：文献-章节-算法映射表。
- `docs/module-inventory.md`：每个源码目录和文件的阅读状态。
- `docs/parameter-map.md`：输入参数、官方文档、源码解析位置、章节位置。
- `docs/example-regression-map.md`：Examples / Regression 到章节的验证映射。
- `manuscript/chapters/`：正式章节。
- `manuscript/appendices/`：源码索引、参数索引、符号表、公式推导全集、运行脚本说明。
- `notes/code-reading/`：逐文件源码阅读笔记，写正文前先在这里沉淀。
- `notes/papers/` 或各 `references/<paper>/`：MinerU 转换和中文论文笔记。

## 4. 全书结构

正式书稿建议分为 12 个部分、约 70-90 章。每一章都要嵌入源码解释，而不是另开“源码手册”。

### Part I：等离子体动理学与 PIC 基础

1. 等离子体多尺度问题：为什么流体模型不够，为什么需要动理学。
2. Vlasov 方程：Liouville 图像、相空间守恒、碰撞项何时能忽略。
3. Maxwell 方程与源项：电荷、电流、约束方程和演化方程。
4. Vlasov-Maxwell 系统：能量守恒、动量守恒、规范和约束传播。
5. Vlasov-Poisson / electrostatic 极限：何时能忽略电磁波。
6. 宏粒子近似：权重、形函数、采样噪声、有限粒子效应。
7. 网格、时间步和分辨率：Debye 长度、等离子体频率、CFL、数值色散。
8. 单位制与 WarpX 常数：SI 常数、归一化动量、源码中的 `WarpXConst.H`。

### Part II：PIC 主循环与 WarpX 程序骨架

9. PIC loop 总览：gather、push、deposit、solve、boundary、diagnostics。
10. WarpX 程序入口：`Source/main.cpp`、AMReX 初始化、`WarpX` 单例和运行生命周期。
11. `WarpX` 主类：`Source/WarpX.H`、`Source/WarpX.cpp` 的成员组织、全局状态和模块所有权。
12. 时间推进外层：`Source/Evolve/WarpXEvolve.cpp::WarpX::Evolve` 逐行讲解。
13. 单步分派：`WarpX::OneStep`、implicit / explicit / ES / EM / hybrid / subcycling 分支。
14. 无 subcycling 显式 EM 主循环：`WarpX::OneStep_nosub` 逐行讲解。
15. subcycling 主循环：`WarpX::OneStep_sub1`、两层 AMR、fine/coarse 时间层。
16. 时间步计算：`Source/Evolve/WarpXComputeDt.cpp`，CFL、粒子速度、自适应时间步。

### Part III：粒子系统

17. 粒子数据结构：AMReX particle tile、AoS/SoA、runtime attributes。
18. 多 species 容器：`MultiParticleContainer` 的职责和生命周期。
19. 物理粒子容器：`PhysicalParticleContainer` 的 gather-push-deposit 主体。
20. `WarpXParticleContainer` 基类：沉积、访问、粒子属性、共同工具。
21. 粒子初始化：`ParticleCreation/`、`PlasmaInjector`、密度/动量/温度分布。
22. 粒子位置推进：`Pusher/UpdatePosition.H`、相对论速度与坐标更新。
23. Boris 推进器：完整推导和 `UpdateMomentumBoris.H` 逐行解释。
24. Vay 推进器：相对论漂移问题、推导和 `UpdateMomentumVay.H` 逐行解释。
25. Higuera-Cary 推进器：结构保持性质、推导和 `UpdateMomentumHigueraCary.H`。
26. 辐射反作用推进：`UpdateMomentumBorisWithRadiationReaction.H`、适用条件和 QED 关系。
27. field gather：`Particles/Gather/`，shape factor、grid staggering、Galerkin interpolation。
28. external particle fields：`ExternalParticleFields.*`，外加场如何进入粒子推进。
29. particle boundaries：`ParticleBoundaries.*`、吸收/反射/周期/thermal/reemission。
30. particle boundary buffer：边界刮擦、诊断和 domain boundary 数据。
31. photon 与 laser particle container：`PhotonParticleContainer`、`LaserParticleContainer`。
32. rigid injection：`RigidInjectedParticleContainer` 和 boosted-frame/beam 注入。
33. 粒子排序与重分布：`Sorting/`、`Redistribute`、load balance 关系。
34. 粒子重采样：`Resampling/`，thinning、leveling、权重守恒风险。
35. particle filter 与 thermalizer：`Particles/Filter/`、`ParticleThermalizer/`。

### Part IV：沉积、形函数与守恒

36. shape factor 数学：B-spline 形函数、阶数、support、噪声和 guard cells。
37. charge deposition：`Particles/Deposition/ChargeDeposition.H`，`rho^n` 和 `rho^{n+1}`。
38. current deposition 总览：连续性方程、轨迹积分和离散守恒。
39. direct deposition：算法、误差和适用边界。
40. Villasenor-Buneman deposition：轨迹切分与守恒思想。
41. Esirkepov deposition：离散连续性方程推导和代码路径。
42. Vay deposition：PSATD 谱空间沉积、current partial sums 和限制条件。
43. mass matrices deposition：implicit solver 中的质量矩阵物理意义和代码。
44. temperature deposition 与 reduced moments：诊断、流体耦合和统计误差。
45. `SyncCurrentAndRho`：滤波、guard cell、AMR interpolation、PEC 边界处理。

### Part V：电磁、静电和谱场求解器

46. Maxwell 离散基础：Yee staggered grid、约束方程和数值色散。
47. FDTD solver 架构：`FieldSolver/FiniteDifferenceSolver/` 总览。
48. `EvolveB.cpp`：Faraday 方程离散和逐行代码。
49. `EvolveE.cpp`：Ampere-Maxwell 方程、current source、div cleaning 和逐行代码。
50. Yee、CKC、nodal、cylindrical、spherical algorithms：`FiniteDifferenceAlgorithms/`。
51. macroscopic medium：`MacroscopicProperties/`、介质响应、Lax-Wendroff/Backward Euler。
52. PML 场推进：`EvolveBPML.cpp`、`EvolveEPML.cpp`、`PMLComponent`。
53. PSATD 理论：谱空间 Maxwell 解析积分、time staggering、current correction。
54. Spectral solver 架构：`SpectralSolver/`、spectral fields、FFT、parallel stencil。
55. Galilean / comoving PSATD：数值 Cherenkov 抑制、boosted-frame 应用。
56. PSATD PML 与 Hankel transform：RZ 谱方法和 `SpectralHankelTransform/`。
57. electrostatic solvers：`ElectrostaticSolvers/`、Poisson、lab-frame / relativistic。
58. magnetostatic solver：`MagnetostaticSolver/`、vector potential 和适用范围。
59. implicit EM solver：theta implicit、semi-implicit、JFNK/Picard/Newton 路径。
60. nonlinear/linear solver 库：`NonlinearSolvers/`、PETSc/AMReX wrappers、preconditioners。
61. hybrid PIC field solver：Ohm 定律、ion kinetic + electron fluid、`HybridPICModel/`。
62. QED field pushers：`WarpX_QED_Field_Pushers.cpp` 和 hybrid QED field path。

### Part VI：边界、嵌入边界、PML 与几何

63. 场边界条件总论：periodic、PEC、PMC、Silver-Mueller、open、Dirichlet。
64. `BoundaryConditions/FieldBoundaries.*`：参数解析、边界类型和调度。
65. PML 实现：`PML.*`、`PML_RZ.*`、`WarpXEvolvePML.cpp`、`WarpX_PML_kernels.H`。
66. PEC/insulator：`WarpX_PEC.*`、`PEC_Insulator.*` 和 embedded conductor 关系。
67. 粒子边界与场边界一致性：periodic 特例、非周期可分离规则、测试案例。
68. Embedded boundary 几何：`EmbeddedBoundaryInit.*`、STL/implicit function、distance field。
69. EB 粒子刮擦和吸收：`ParticleScraper.H`、`ParticleBoundaryProcess.H`。
70. EB field extension：`WarpXFaceExtensions.cpp`、small-cell 稳定性问题。

### Part VII：AMR、并行与性能工程

71. AMReX 基础：BoxArray、DistributionMapping、MultiFab、FabArray、MFIter。
72. WarpX AMR 物理问题：self-force、coarse-fine interface、patch PML、subcycling。
73. guard cell 管理：`Parallelization/GuardCellManager.*`。
74. 通信与同步：`WarpXComm.cpp`、`WarpXComm_K.H`、periodic 和 nodal sync。
75. regrid：`WarpXRegrid.cpp`、refinement criteria、particle redistribution。
76. sum guard cells：`WarpXSumGuardCells.*`、电流/电荷守恒和并行边界。
77. load balancing：cost model、粒子排序、diagnostic timing、`amr.max_grid_size`。
78. GPU portability：AMReX GPU launch、lambda capture、compile-time options、memory layout。
79. build variants：维度宏、RZ/RCYLINDER/RSPHERE、single/double precision、MPI/OpenMP/GPU。

### Part VIII：初始化、输入参数、激光和外场

80. 参数系统总论：`Docs/source/usage/parameters.rst` 到源码 `ParmParse`。
81. WarpX 初始化总路径：`Initialization/WarpXInit.*`、`WarpXInitData.cpp`。
82. AMReX 初始化：`WarpXAMReXInit.*`、运行参数、geometry 和 domain。
83. species 初始化：`PlasmaInjector.*`、`InjectorDensity.*`、`InjectorMomentum.*`、`InjectorPosition.*`。
84. 温度与速度分布：`TemperatureProperties.*`、`VelocityProperties.*`、`GetTemperature.*`、`GetVelocity.*`。
85. external fields：`Initialization/ExternalField.*`、网格外场和粒子外场区别。
86. div cleaner 初始化：`Initialization/DivCleaner/`。
87. laser profiles：`Laser/LaserProfiles.H`、`LaserProfilesImpl/`。
88. laser injection：antenna、Gaussian、Laguerre-Gaussian、from file、lasy 输入。
89. moving window：`Utils/WarpXMovingWindow.cpp`、boosted frame 和粒子重分布。

### Part IX：多物理扩展

90. collision 架构：`Particles/Collision/CollisionHandler.*`、`CollisionBase.*`。
91. binary Coulomb collision：`BinaryCollision/`、pairing、scattering、conservation。
92. Background MCC：`BackgroundMCC/`、低温等离子体、neutral background 和反应表。
93. Background stopping：阻止功、适用模型和代码。
94. pulsed decay：`PulsedDecay/`。
95. ionization：ADK/OTB、`ElementaryProcess/Ionization.*`、能量处理限制。
96. QED photon emission：`QEDPhotonEmission.*`、quantum synchrotron、optical depth。
97. Breit-Wheeler pair generation：`QEDPairGeneration.*`、photon -> pair。
98. QED internals：`QEDInternals/` wrappers、chi 函数、PICSAR-QED tables。
99. Schwinger process：`QEDSchwingerProcess.H` 和场强极限。
100. nuclear fusion / virtual photons / linear BW / Compton：对应 Examples 与 collision/QED 路径。

### Part X：流体、混合模型与加速器元件

101. cold fluid model：连续方程、pressure closure、和 PIC loop 的耦合。
102. fluid container：`Fluids/MultiFluidContainer.*`、`WarpXFluidContainer.*`。
103. MUSCL-Hancock：`MusclHancockUtils.H`、重构、Riemann flux、稳定性。
104. kinetic-fluid hybrid model：质量为零电子流体、Ohm 定律、magnetic reconnection。
105. accelerator lattice：`AcceleratorLattice/`、lattice elements、external beamline fields。
106. lattice element finder：moving window / boosted lattice 位置更新。

### Part XI：诊断、I/O、Python 接口和工具

107. diagnostics 架构：`Diagnostics/Diagnostics.*`、`MultiDiagnostics.*`、`FullDiagnostics.*`。
108. field diagnostics：`FieldIO.*`、field selection、derived fields、plotfile。
109. particle diagnostics：`ParticleDiag/`、species variables、scraping diagnostics。
110. reduced diagnostics：`ReducedDiags/`，能量、动量、field probe、luminosity、custom reductions。
111. openPMD：`WarpXOpenPMD.*`、`OpenPMDHelpFunction.*`、metadata 标准。
112. plotfile / checkpoint / restart：`WarpXIO.cpp`、BTD、restart tests。
113. insitu diagnostics：Ascent、Catalyst、SENSEI 相关文档与 Tools。
114. Python callbacks：`Python/callbacks.*`、beforestep/afterstep/particleinjection 等。
115. pyWarpX bindings：`Python/WarpX.cpp`、`pyWarpX.*`、`Python/Particles/`。
116. PICMI：官方 Python 文档、examples、参数翻译层。
117. Tools/Parser：输入文件解析器，用于书稿参数索引自动化。
118. Tools/PostProcessing：NCI growth、particle path、distribution mapping、timing plot。
119. Tools/Algorithms：PSATD notebook、stencil 工具，作为推导辅助。
120. QED table tools：`Tools/QedTablesUtils/`。

### Part XII：构建、测试、案例和工程生态

121. CMake / GNUmake 构建系统：`CMakeLists.txt`、`Source/Make.*`、维度和依赖选项。
122. 机器配置和 HPC 脚本：`Tools/machines/`、install docs、batch docs。
123. Regression framework：`Regression/Checksum/`、benchmark json、checksum API。
124. Examples/Tests 全覆盖路线：每个测试对应哪个物理/算法章节。
125. Physics_applications 全覆盖路线：beam-beam、laser acceleration、plasma acceleration、laser ion、plasma mirror、capacitive discharge、FEL、ion extraction。
126. 与其他 PIC 程序比较：EPOCH、OSIRIS、VPIC、PIConGPU、FBPIC、Smilei、HiPACE++。
127. 如何给 WarpX 添加新模块：从论文公式到参数、源码、测试、文档、benchmark。
128. 全书总结：从 Vlasov 方程到 exascale PIC 程序。

## 5. 源码模块覆盖矩阵

以下矩阵用于检查“是否覆盖整个 WarpX 代码”。状态列后续在 `docs/module-inventory.md` 中维护。

| 源码目录 | 主要内容 | 计划章节 |
|---|---|---|
| `Source/main.cpp` | 程序入口、初始化、运行生命周期 | 10 |
| `Source/WarpX.H`, `Source/WarpX.cpp` | 主类、全局状态、模块所有权 | 11 |
| `Source/Evolve/` | 时间步、主循环、subcycling、dt | 12-16 |
| `Source/Particles/` | species、粒子容器、边界、I/O、属性 | 17-35 |
| `Source/Particles/Pusher/` | Boris/Vay/Higuera-Cary/位置推进 | 22-26 |
| `Source/Particles/Gather/` | 场插值、外场、shape | 27 |
| `Source/Particles/Deposition/` | charge/current/mass/temperature deposition | 36-45 |
| `Source/Particles/Collision/` | MCC、binary collision、stopping、decay | 90-94 |
| `Source/Particles/ElementaryProcess/` | ionization、QED emission、pair generation | 95-99 |
| `Source/FieldSolver/` | EM/ES/hybrid/implicit/spectral field solve | 46-62 |
| `Source/FieldSolver/FiniteDifferenceSolver/` | Yee/CKC/nodal/RZ/spherical FDTD | 47-52 |
| `Source/FieldSolver/SpectralSolver/` | PSATD、Galilean、Hankel、FFT | 53-56 |
| `Source/FieldSolver/ElectrostaticSolvers/` | Poisson/electrostatic PIC | 57 |
| `Source/FieldSolver/ImplicitSolvers/` | theta/semi implicit/JFNK | 59 |
| `Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/` | Ohm solver/hybrid PIC | 61, 104 |
| `Source/BoundaryConditions/` | field boundary、PML、PEC、insulator | 63-67 |
| `Source/EmbeddedBoundary/` | EB 初始化、distance、scraping、face info | 68-70 |
| `Source/Parallelization/` | guard cells、communication、regrid | 71-77 |
| `Source/Filter/` | bilinear filter、Godfrey NCI filter | 45, 53-56 |
| `Source/Initialization/` | 参数解析、species/profile/temperature/velocity | 80-86 |
| `Source/Laser/` | 激光轮廓、注入模型 | 87-88 |
| `Source/Fluids/` | cold fluid、MUSCL、hybrid model coupling | 101-104 |
| `Source/Diagnostics/` | full/reduced/openPMD/BTD/scraping I/O | 107-113 |
| `Source/AcceleratorLattice/` | lattice 元件和查找 | 105-106 |
| `Source/NonlinearSolvers/` | Newton/Picard/GMRES/PETSc/preconditioner | 59-60 |
| `Source/Python/` | callbacks、pybind、Python API | 114-116 |
| `Source/Utils/` | 常数、算法选择、移动窗口、插值、parser helpers | 8, 80, 89 |
| `Source/ablastr/` | fields、particles、math、parallelization、profiler 工具层 | 71, 78, 107 |
| `CMakeLists.txt`, `Source/Make.*` | 构建系统 | 121 |
| `Examples/` | 用户案例和算法测试输入 | 123-125 |
| `Regression/` | checksum、benchmark、CI 验证 | 123-124 |
| `Tools/` | 推导、后处理、QED table、HPC 脚本 | 117-122 |

## 6. 物理模型覆盖清单

- 无碰撞 Vlasov-Maxwell。
- Vlasov-Poisson / electrostatic PIC。
- 相对论动理学粒子。
- 显式电磁 PIC。
- theta implicit EM PIC。
- semi-implicit EM PIC。
- kinetic-fluid hybrid model。
- cold relativistic fluid。
- macroscopic media EM response。
- laser injection and laser-plasma interaction。
- boosted-frame and moving-window physics。
- AMR electromagnetic/electrostatic refinement physics。
- PML/open boundary wave absorption。
- PEC/PMC/Silver-Mueller/conductor/insulator boundary physics。
- embedded boundary plasma-material interaction。
- Coulomb / binary collisions。
- Monte Carlo collision with background neutrals。
- stopping power / ion stopping。
- field ionization: ADK/OTB/corrections。
- QED quantum synchrotron photon emission。
- Breit-Wheeler pair production。
- Schwinger-like strong-field process。
- nuclear fusion reactions in examples。
- beam-beam collision, luminosity diagnostics。
- accelerator lattice and external focusing elements。
- FEL, LWFA/PWFA, laser ion acceleration, plasma mirror, capacitive discharge, magnetic reconnection。

## 7. 算法覆盖清单

- leapfrog time staggering。
- Boris, Vay, Higuera-Cary, radiation-reaction pushers。
- field gather: momentum-conserving / energy-conserving / Galerkin interpolation。
- B-spline particle shapes 0-4 阶。
- charge deposition and rho time components。
- direct, Villasenor-Buneman, Esirkepov, Vay current deposition。
- current correction, charge conservation correction。
- filtering: bilinear, NCI Godfrey, PSATD-specific current filtering。
- Yee FDTD, CKC, nodal FDTD。
- cylindrical / spherical / RZ field algorithms。
- PSATD, Galilean PSATD, averaged fields, JRhom。
- Hankel transform for RZ spectral solver。
- PML for FDTD and PSATD。
- divergence cleaning for E/B。
- electrostatic Poisson solve, open BC Poisson, effective potential。
- magnetostatic vector potential solve。
- implicit theta, semi-implicit, Strang implicit spectral。
- Newton, Picard, JFNK, GMRES, PETSc KSP/SNES, preconditioners。
- MUSCL-Hancock fluid update。
- AMR synchronization, restriction/prolongation, coarse-fine patch substitution。
- guard cell exchange, nodal synchronization, periodic communication。
- particle sorting, redistribution, load-balance cost update。
- particle resampling and thinning。
- diagnostic packing, output flushing, checkpoint/restart。
- Python callbacks and runtime data access。

## 8. 写作执行阶段

### 阶段 A：建立全源码索引

- [ ] 生成 `docs/module-inventory.md`，列出 `Source/` 下每个 `.H/.cpp/.py/CMakeLists.txt/Make.package` 文件。
- [ ] 为每个文件标注：所属模块、物理主题、关键类/函数、是否需要逐行解读、对应章节。
- [ ] 生成 `docs/parameter-map.md` 初版，从 `Docs/source/usage/parameters.rst` 抽取参数名、说明、源码解析位置。
- [ ] 生成 `docs/example-regression-map.md`，把 `Examples/` 和 `Regression/Checksum/benchmarks_json/` 映射到章节。
- [ ] 更新 `docs/source-map.md`，从当前少量函数扩展到全模块索引。

### 阶段 B：先写物理和数学基础，不碰复杂实现细节

- [ ] 完成 Vlasov-Maxwell 推导章节。
- [ ] 完成 Vlasov-Poisson / electrostatic 极限章节。
- [ ] 完成宏粒子、shape、噪声和采样误差章节。
- [ ] 完成 leapfrog、稳定性、CFL、数值色散基础章节。
- [ ] 为每章建立文献清单，优先处理 Birdsall-Langdon、Hockney-Eastwood、Dawson、Yee。

### 阶段 C：主循环精读样章重写

- [ ] 重新读取 `main.cpp`、`WarpX.H`、`WarpX.cpp`、`Evolve/WarpXEvolve.cpp`。
- [ ] 画出完整调用图：`main -> WarpX::GetInstance -> InitData -> Evolve -> OneStep -> Particles/Fields/Diagnostics`。
- [ ] 写 `WarpX::Evolve` 逐行讲解，说明每个 callback、多物理插入点和状态变量。
- [ ] 写 `OneStep` 分支表，列出所有 solver/evolve scheme 组合。
- [ ] 写 `OneStep_nosub` 逐行讲解，重点解释时间层、J/rho 同步、PSATD/FDTD 分支。
- [ ] 写 `OneStep_sub1` 逐块讲解，解释 coarse/fine 时间推进和限制条件。
- [ ] 用 Langmuir 和 uniform plasma 做最小验证记录。

### 阶段 D：粒子模块精读

- [ ] 从 `MultiParticleContainer` 和 `PhysicalParticleContainer` 建立 species 生命周期。
- [ ] 逐行解释 `PhysicalParticleContainer::Evolve` 和 `PushPX`。
- [ ] 分别写 Boris、Vay、Higuera-Cary 的完整推导和源码行注。
- [ ] 逐文件解释 `Gather/`、`ShapeFactors.H`、external fields。
- [ ] 逐文件解释 particle boundary、boundary buffer、scraping。
- [ ] 解释 photon/laser/rigid injected particle containers。
- [ ] 用 `Examples/Tests/particle_pusher`、`single_particle`、`larmor`、`photon_pusher` 验证。

### 阶段 E：沉积和守恒模块精读

- [ ] 推导 charge/current deposition 的离散连续性方程。
- [ ] 逐行解释 `ChargeDeposition.H`。
- [ ] 逐行解释 `CurrentDeposition.H` 的 direct / Esirkepov / Vay 路径。
- [ ] 逐块解释 mass matrices deposition 和 implicit 耦合。
- [ ] 解释 `SyncCurrentAndRho` 和所有 guard/current/rho 同步路径。
- [ ] 用 Langmuir PSATD current correction、Vay deposition tests 验证。

### 阶段 F：场求解器精读

- [ ] 完整推导 Yee/FDTD/CKC/nodal/RZ/spherical 更新。
- [ ] 逐行解释 `FiniteDifferenceSolver/EvolveB.cpp`。
- [ ] 逐行解释 `FiniteDifferenceSolver/EvolveE.cpp`。
- [ ] 逐行解释 PML E/B 更新。
- [ ] 推导 PSATD 和 Galilean PSATD，读取 `Tools/Algorithms/psatd.ipynb`。
- [ ] 逐文件解释 `SpectralSolver/` 和 `SpectralAlgorithms/`。
- [ ] 解释 electrostatic、magnetostatic、implicit solver、hybrid solver。
- [ ] 用 `nci_fdtd_stability`、`nci_psatd_stability`、`electrostatic_sphere`、`implicit`、`ohm_solver_*` 验证。

### 阶段 G：边界、AMR、并行精读

- [ ] 完成 field boundary / particle boundary 全参数表。
- [ ] 逐文件解释 `BoundaryConditions/` 和 `EmbeddedBoundary/`。
- [ ] 推导 AMR coarse-fine interface 问题和 WarpX substitution strategy。
- [ ] 逐文件解释 `Parallelization/`。
- [ ] 解释 GPU portability、MFIter、ParallelFor、compile-time options。
- [ ] 用 boundaries、PML、particles_in_pml、embedded_boundary、subcycling、MR Langmuir tests 验证。

### 阶段 H：初始化、参数、激光、多物理精读

- [ ] 逐文件解释 `Initialization/`。
- [ ] 建立所有 `ParmParse` 参数到章节的索引。
- [ ] 逐文件解释 `Laser/`。
- [ ] 逐文件解释 collisions、ionization、QED、fluids、accelerator lattice。
- [ ] 用 laser injection、field ionization、qed、collision、capacitive discharge、hybrid reconnection、accelerator lattice tests 验证。

### 阶段 I：诊断、Python、工具、构建和生态

- [ ] 逐文件解释 `Diagnostics/` 和 `ReducedDiags/`。
- [ ] 解释 plotfile、openPMD、checkpoint/restart、BTD。
- [ ] 逐文件解释 `Python/` 和 PICMI 工作流。
- [ ] 解释 Tools/Parser、PostProcessing、Algorithms、QedTablesUtils。
- [ ] 解释 CMake/GNUmake/build variants。
- [ ] 用 restart、reduced_diags、particle_data_python、python_wrappers、openPMD examples 验证。

### 阶段 J：应用案例综合章

- [ ] Langmuir wave：从解析色散关系到源码路径。
- [ ] Uniform plasma：噪声、能量、性能和诊断。
- [ ] LWFA/PWFA：laser、plasma, moving window, boosted frame, diagnostics。
- [ ] Laser ion / plasma mirror / RPA/TNSA：边界、靶、强场、多物理。
- [ ] Capacitive discharge：PIC-MCC 低温等离子体。
- [ ] Magnetic reconnection：hybrid model 和 fluid/PIC 耦合。
- [ ] Beam-beam / luminosity / FEL / ion extraction：束流和加速器模块。

## 9. 每章固定工作流

每章开始前：

- [ ] 记录 WarpX commit。
- [ ] 列出本章物理问题和连续方程。
- [ ] 列出本章涉及的源码文件。
- [ ] 列出本章涉及的参数和示例。
- [ ] 列出本章必须处理的文献。

写作顺序：

1. 物理过程叙述。
2. 连续方程和假设。
3. 离散推导。
4. 伪代码。
5. WarpX 调用链。
6. 源码原文摘录。
7. 逐行或逐块源码解读。
8. 输入参数解释。
9. 示例/测试验证。
10. 文献和进一步阅读。
11. 未解决问题和下一轮检查项。

完成前检查：

- [ ] 公式变量均已定义。
- [ ] 所有源码路径真实存在。
- [ ] 所有行号来自当日重新读取。
- [ ] 所有被讲解的源码段已经把源码原文放入正文。
- [ ] 参数说明回到官方文档或源码解析。
- [ ] 至少一个示例或 regression 对应本章。
- [ ] 关键物理结论有文献或可运行验证。

## 10. 文献处理计划

优先级 1：基础和核心算法。

- Birdsall & Langdon: PIC 基础、shape、noise。
- Hockney & Eastwood: particle-mesh 方法。
- Dawson review: PIC 历史和物理直觉。
- Yee 1966: FDTD。
- Boris pusher 原始资料和标准教材。
- Vay pusher。
- Higuera-Cary pusher。
- Villasenor-Buneman deposition。
- Esirkepov deposition。
- Berenger PML。

优先级 2：WarpX 特有和高阶算法。

- WarpX 论文。
- AMReX 论文。
- PICSAR / PICSAR-QED。
- openPMD / PICMI。
- PSATD / Galilean PSATD / NCI suppression。
- AMR for electromagnetic PIC。
- boosted-frame papers。
- implicit PIC papers。
- hybrid PIC / Ohm solver papers。

优先级 3：应用和比较。

- LWFA/PWFA。
- laser ion acceleration。
- plasma mirror。
- capacitive discharge PIC-MCC。
- magnetic reconnection。
- beam-beam collision。
- EPOCH / OSIRIS / VPIC / PIConGPU / Smilei / FBPIC / HiPACE++。

所有深入使用的 PDF 都必须按 `docs/paper-reading-workflow.md` 执行：论文专属目录、MinerU Markdown、`images/`、中文讲解笔记、章节用途标注。

## 11. 验证和运行计划

本机短 WarpX 运行若遇到 MPI/OFI 问题，优先使用：

```bash
FI_PROVIDER=tcp
```

每个案例记录：

- binary 路径。
- 输入文件路径。
- 运行命令。
- 环境变量。
- 输出目录。
- 关键日志。
- 后处理脚本。
- 物理检查量。
- 对应源码路径。

最低验证矩阵：

| 章节群 | 验证案例 |
|---|---|
| 主循环/沉积/场求解 | `Examples/Tests/langmuir` |
| 粒子推进 | `Examples/Tests/particle_pusher`, `larmor`, `single_particle` |
| FDTD/PML/边界 | `pml`, `silver_mueller`, `pec`, `boundaries` |
| PSATD/NCI | `nci_psatd_stability`, `Langmuir_multi_*_psatd*` |
| AMR/subcycling | `langmuir_multi_mr`, `subcycling` |
| electrostatic | `electrostatic_sphere`, `open_bc_poisson_solver` |
| implicit | `Examples/Tests/implicit` |
| hybrid/fluid | `ohm_solver_*`, `langmuir_fluids` |
| collisions/MCC | `collision`, `ionization_dsmc`, `capacitive_discharge` |
| ionization/QED | `field_ionization`, `qed`, `linear_breit_wheeler`, `linear_compton` |
| EB | `embedded_boundary_*`, `particle_boundary_process` |
| diagnostics/Python | `reduced_diags`, `particle_data_python`, `python_wrappers`, `restart` |
| applications | `laser_acceleration`, `plasma_acceleration`, `laser_ion`, `plasma_mirror`, `beam_beam_collision` |

## 12. 近期执行顺序

下一步不直接继续写正文，而是先建立索引和样章重写基础：

- [ ] 创建 `docs/module-inventory.md`。
- [ ] 创建 `docs/parameter-map.md`。
- [ ] 创建 `docs/example-regression-map.md`。
- [ ] 创建 `docs/literature-map.md`。
- [ ] 重写 `manuscript/chapters/02-pic-loop.md` 和 `03-warpx-evolve.md`，达到第一章样章标准。
- [ ] 严格审查样章：物理推导、源码行号、参数、示例、文献是否闭环。

只有样章达到“讲透”标准后，再批量推进其他模块，避免全书铺开但每章仍然空泛。
