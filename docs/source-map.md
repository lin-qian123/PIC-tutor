# PIC-tutor 源码与资料映射

记录日期：2026-05-14

本书当前绑定的 WarpX 本地源码状态：

- 路径：`../warpx`
- 分支：`pkuHEDPbranch`
- commit：`063f8b586f04321e13150ae3e730e0794ca75cb1`
- 使用原则：`../warpx` 只读；书稿引用源码时以本地文件、官方文档和可检索文献为准。

## 总入口

| 主题 | 官方文档 | 源码入口 | 示例/测试 | 主要文献线索 |
|---|---|---|---|---|
| WarpX 仓库组织 | `Docs/source/developers/repo_organization.rst` | `Source/` | `Examples/`, `Regression/` | WarpX 论文、AMReX/PICSAR/openPMD/PICMI |
| PIC 总循环 | `Docs/source/glossary.rst`, `Docs/source/developers/repo_organization.rst` | `Source/Evolve/WarpXEvolve.cpp` | `Examples/Tests/langmuir/`, `Examples/Physics_applications/uniform_plasma/` | `Birdsalllangdon`, `HockneyEastwoodBook`, `DawsonRMP83` |
| 显式电磁 PIC | `Docs/source/theory/models_algorithms/electromagnetic_pic.rst`, `explicit_em_pic.rst` | `Source/Evolve/`, `Source/Particles/`, `Source/FieldSolver/` | `Examples/Tests/langmuir/inputs_test_1d_langmuir_multi` | `Yee`, `Villasenorcpc92`, `Esirkepovcpc01` |
| 粒子推进 | `Docs/source/developers/particles.rst` | `Source/Particles/Pusher/`, `Source/Particles/PhysicalParticleContainer.cpp` | pusher 相关 regression 测试需要后续细查 | `HigueraPOP2017`, Vay pusher 相关条目 |
| 沉积 | `Docs/source/theory/models_algorithms/explicit_em_pic.rst`, `Docs/source/developers/fields.rst` | `Source/Particles/Deposition/`, `Source/Particles/WarpXParticleContainer.cpp` | Langmuir、uniform plasma、current correction / PSATD 测试 | `Villasenorcpc92`, `Esirkepovcpc01`, `VayJCP2013` |
| 场求解 FDTD/PSATD | `Docs/source/developers/fields.rst`, `Docs/source/theory/models_algorithms/explicit_em_pic.rst` | `Source/FieldSolver/FiniteDifferenceSolver/`, `Source/FieldSolver/SpectralSolver/` | Gaussian beam、Langmuir、laser acceleration | `Yee`, `Lehe2016`, `GodfreyJCP2014_PSATD` |
| 边界与 PML | `Docs/source/theory/boundary_conditions.rst`, `Docs/source/usage/parameters.rst` | `Source/BoundaryConditions/`, `Source/Particles/ParticleBoundaries.cpp` | `Examples/Tests/boundaries/` | `Berengerjcp94`, `Berengerjcp96` |
| AMR 与 guard cells | `Docs/source/theory/amr.rst` | `Source/Parallelization/`, `Source/Evolve/WarpXEvolve.cpp` | mesh-refinement examples/tests | `Vayjcp01`, `Vaylpb2002`, `Vaycpc04` |
| 诊断与验证 | `Docs/source/usage/parameters.rst`, `Docs/source/dataanalysis/` | `Source/Diagnostics/`, `Regression/Checksum/` | `Examples/analysis_default_regression.py` | openPMD 条目、WarpX 论文 |

## 第一轮源码证据

### `Source/Evolve/WarpXEvolve.cpp`

- `WarpX::Evolve`，行 146-387：外层时间步循环，包含 Python callback、负载均衡、Ionization/QED、多物理、`OneStep`、边界处理、诊断和停止条件。
- `WarpX::OneStep`，行 389-496：按 implicit / explicit、电磁 / 静电 / hybrid、是否 mesh refinement、是否 subcycling 分派到具体推进路径。
- `WarpX::OneStep_nosub`，行 503-643：无 subcycling 的显式电磁 PIC 核心循环。先粒子推进和沉积，再同步 `J`/`rho`，再推进场。
- `WarpX::ExplicitFillBoundaryEBUpdateAux`，行 652-711：维护显式 leapfrog 中粒子动量和场时间层的关系。
- `WarpX::HandleParticlesAtBoundaries`，行 713-766：连续注入、粒子边界、重分布、嵌入边界刮擦和排序。
- `WarpX::SyncCurrentAndRho`，行 768-837：电流/电荷同步、滤波、guard cell 交换、AMR 插值和边界处理。
- `WarpX::OneStep_sub1`，行 1060 起：两级 refinement、refinement ratio = 2 的 subcycling 路径。

### `Source/Particles/MultiParticleContainer.cpp`

- `MultiParticleContainer::Evolve`，行 471-516：清零当前步沉积场，遍历全部 species，调用每个 `PhysicalParticleContainer::Evolve`。
- `MultiParticleContainer::DepositCurrent`，行 580-605：清零多层电流场并逐 species 沉积。
- `MultiParticleContainer::DepositCharge`，行 608 起：清零电荷场，必要时临时移动粒子位置后沉积。

### `Source/Particles/PhysicalParticleContainer.cpp`

- `PhysicalParticleContainer::Evolve`，行 452-825：单 species 的 gather-push-deposit 主体。先决定是否沉积 `rho`/`J`，按 tile 遍历粒子，必要时区分 fine patch 与 buffer。
- 行 579-592：粒子推进前把电荷密度沉积到 `rho` component 0。
- 行 613-617、671-676：调用 `PushPX`，完成场 gather、动量推进和位置推进。
- 行 697-733：在显式推进后按 `relative_time = -0.5*dt` 沉积当前 `J`。
- 行 785-803：电磁模式下在推进后把电荷密度沉积到 `rho` component 1。
- `PhysicalParticleContainer::PushPX`，行 1324 起；行 1502-1508 gather，行 1523-1547 动量推进，行 1549-1552 位置推进。

### `Source/Particles/Pusher/`

- `PushSelector.H`，行 39-104：按 `ParticlePusherAlgo` 选择 Boris、Vay、Higuera-Cary；若启用 classical radiation reaction 则转入辐射反作用版本。
- `UpdateMomentumBoris.H`，行 20-62：Boris 推进的电半步、磁旋转、电半步结构；`FirstHalf`/`SecondHalf` 与 `Full` 的分裂设计在注释行 13-18 中说明。
- `UpdateMomentumVay.H`，行 17-77：Vay pusher；文件注释引用 Vay 2008 公式 (9)-(13)，源码通过 `u'`、`sigma`、`gisq` 解析构造新的相对论旋转。
- `UpdateMomentumHigueraCary.H`，行 16-65：Higuera-Cary pusher；从 `u_minus`、`beta`、`sigma`、`u*` 构造 `u_plus`，最后加电半步和 `u_plus x t` 修正项。

### `Source/Particles/Gather/`

- `Gather/FieldGather.H`，行 2119-2192：`doGatherShapeN()` 运行时 wrapper，把 `nox` 与 `galerkin_interpolation` 分派为 `doGatherShapeN<depos_order, galerkin_interpolation>()` 模板实例。
- `Gather/FieldGather.H`，行 348-439：gather 模板主体开头，按场分量的 node/cell centering 和 Galerkin 降阶生成 x 方向 shape 数组与左端索引。
- `Gather/FieldGather.H`，行 547-581：XZ 维度下按 `sx*sz` 权重把 `ex/ey/ez/bx/by/bz` gather 到粒子场。
- `Gather/FieldGather.H`，行 583-686：RZ 维度下先 gather `Er/Etheta/Br/Btheta` 和 Fourier mode，再转回 Cartesian `Ex/Ey/Bx/By`。

### `Source/Particles/ShapeFactors.H`

- 行 27-84：`Compute_shape_factor<depos_order>` 实现 0 到 4 阶 shape factor，并返回粒子 stencil 的最左网格点。
- 行 93-156：`Compute_shifted_shape_factor<depos_order>` 为 Esirkepov old/new shape 差分提供与新位置对齐的旧位置 shape 数组。
- 行 158-240：`Compute_shape_factor_pair<depos_order>` 为 Villasenor 等 segment 相关算法提供 old/new 成对 shape；尚需后续逐行展开。

### `Source/Particles/Deposition/`

- `Deposition/ChargeDeposition.H`，行 36-172：`doChargeDepositionShapeN<depos_order>()`；计算 `wq=q*wp*invvol`，按 rho staggering 计算 shape，原子加 `sx*sy*sz*wq` 到 `rho_arr`。
- `Deposition/CurrentDeposition.H`，行 47-274：direct current deposition kernel；用 `relative_time` 取半步沉积位置，并按 `q*w*v/vol` 乘 shape 原子加到 `jx/jy/jz`。
- `Deposition/CurrentDeposition.H`，行 675-723：Esirkepov kernel 入口；定义 `invdtd`、电离权重和 reduced-shape 分派。
- `Deposition/CurrentDeposition.H`，行 724-935：Esirkepov 对每个粒子反推 old/new 网格坐标并生成对齐的 old/new shape factor。
- `Deposition/CurrentDeposition.H`，行 955-989：3D Esirkepov 电流公式，用 `sx_old-sx_new`、`sy_old-sy_new`、`sz_old-sz_new` 的累积差构造 charge-conserving current。

### `Source/FieldSolver/WarpXPushFieldsEM.cpp`

- `WarpX::EvolveB`，行 946 起：按 level / patch type 调用 FDTD 或 PML 的 B 更新。
- `WarpX::EvolveE`，行 1000 起：按 level / patch type 调用 E 更新，并处理 PML 与电荷守恒相关场。
- 文件前部的 PSATD 辅助函数包含 current correction、Vay deposition 和谱空间变换入口。

## 当前样章使用的示例

- `../warpx/Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`
  - `max_step = 80`
  - `geometry.dims = 1`
  - 周期场边界：`boundary.field_lo/hi = periodic`
  - `algo.field_gathering = energy-conserving`
  - `algo.current_deposition = esirkepov`
  - 电子和正电子双 species，密度 `n0 = 2.e24 m^-3`
- `../warpx/Examples/Physics_applications/uniform_plasma/inputs_test_2d_uniform_plasma`
  - `max_step = 10`
  - `geometry.dims = 2`
  - 周期场边界
  - 单电子 species，常密度，热动量分布

## 后续待补证据

- 用 `rg` 精确定位每个 `algo.*` 参数的解析位置和默认值。
- 对 `Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp`、`EvolveB.cpp` 做逐行公式对照。
- 继续补齐 `Source/Particles/Deposition/CurrentDeposition.H` 中 Villasenor、Vay、implicit charge-conserving、shared-memory direct 和非 3D 维度分支。
- 对 `Source/BoundaryConditions/` 和 `Source/Particles/ParticleBoundaries*` 建立场边界与粒子边界的匹配规则表。

## 阶段 A 索引产物

2026-05-14 已生成第一批全局索引，作为后续精读的导航层。它们是自动生成的初筛结果，不替代正式章节中的人工源码阅读。

| 文件 | 覆盖范围 | 当前用途 |
|---|---|---|
| `docs/module-inventory.md` | `../warpx/Source` 下 707 个目标源码/构建文件 | 给每个文件标注模块、物理主题、计划章节和讲解深度 |
| `docs/parameter-map.md` | `Docs/source/usage/parameters.rst` 中 352 个 `pp:param` 参数 | 建立参数、文档行号、初步源码命中和章节的映射 |
| `docs/parameter-chapter-index.md` | `parameters.rst`、`WarpX.cpp`、`WarpXInit.cpp`、`Utils/Parser/*` | 对高频参数做人工章节校正，并按 `species / laser / diagnostics / collision` 建立对象前缀导航，同时把 `boundary / solver / psatd / implicit` 的入口接回源码图 |
| `notes/code-reading/utils/02-parameter-family-entrypoints.md` | `WarpX.cpp`、`Initialization/WarpXAMReXInit.cpp`、`BoundaryConditions/FieldBoundaries.cpp`、`Particles/MultiParticleContainer.cpp`、`Particles/WarpXParticleContainer.cpp`、`Diagnostics/MultiDiagnostics.cpp`、`Diagnostics/ReducedDiags/MultiReducedDiags.cpp`、`Particles/Collision/CollisionHandler.cpp`、`FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp` | 把高频参数族的真实读取入口压成源码图，区分 `global gate / factory dispatch / instance-local parse` 三层壳，并补 `boundary / solver / psatd / implicit` 四组入口 |
| `notes/code-reading/utils/05-deep-solver-object-parameter-families.md` | `WarpX.cpp`、`Fluids/MultiFluidContainer.cpp`、`Fluids/WarpXFluidContainer.cpp`、`FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp`、`FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/MacroscopicProperties.cpp`、`FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp`、`FieldSolver/ElectrostaticSolvers/EffectivePotentialES.*` | 把 `fluids / hybrid_pic_model / macroscopic / effective potential` 四组更深的 solver-object 参数入口压成源码图，区分 existence gate、object creation、instance-local parse 和 runtime materialization |
| `notes/code-reading/utils/06-external-vector-potential-and-poisson-boundary-parameters.md` | `WarpX.cpp`、`FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.*`、`FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.*`、`FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp`、`Initialization/WarpXInitData.cpp`、`Python/WarpX.cpp` | 把 `external_vector_potential.*`、`boundary.potential_*` 与 `warpx.eb_potential(x,y,z,t)` 的真实入口压成源码图，区分 parent gate、subobject parse、parser build 和 runtime apply |
| `notes/code-reading/accelerator-lattice/00-lattice-data-model.md` | `Source/AcceleratorLattice/AcceleratorLattice.*`、`Source/AcceleratorLattice/LatticeElements/LatticeElementBase.*`、`Source/AcceleratorLattice/README.rst` | 解释递归 `lattice.elements/line/reverse` 输入树、`z_location -> zs/ze` 几何账本，以及 host/device 双层对象图 |
| `notes/code-reading/accelerator-lattice/01-lattice-elements.md` | `Source/AcceleratorLattice/LatticeElements/Drift.*`、`HardEdgedQuadrupole.*`、`HardEdgedPlasmaLens.*`、`HardEdged_K.H` | 解释 `drift` 只贡献几何、`quad/plasmalens` 的 `dEdx/dBdx` 读取与场对称性，以及 hard-edged residence correction |
| `notes/code-reading/accelerator-lattice/02-element-finder-device-path.md` | `Source/AcceleratorLattice/LatticeElementFinder.*`、`Source/AcceleratorLattice/AcceleratorLattice.cpp` | 解释 per-tile nearest-element lookup table、boosted-frame 反变换、`zpvdt` residence 查询和粒子侧 `E/B` 外场累加路径 |
| `notes/code-reading/accelerator-lattice/03-validation-map.md` | `Source/AcceleratorLattice/AcceleratorLattice.*`、`Source/AcceleratorLattice/LatticeElements/HardEdgedQuadrupole.*`、`Source/AcceleratorLattice/LatticeElementFinder.*`、`Examples/Tests/accelerator_lattice/*` | 把 hard-edged quadrupole 的 lab-frame / boosted-frame / moving-window 三条解析轨道对照 regression 接回 accelerator lattice 主链 |
| `notes/code-reading/utils/07-parameter-validation-links-for-boundary-and-external-fields.md` | `FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.*`、`FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.*`、`FieldSolver/ElectrostaticSolvers/EffectivePotentialES.*`、`Examples/Tests/electrostatic_dirichlet_bc/*`、`Examples/Tests/open_bc_poisson_solver/*`、`Examples/Tests/effective_potential_electrostatic/*`、`Examples/Physics_applications/ion_beam_extraction/*` | 把 `boundary.potential_*`、open-boundary Poisson、effective-potential 和 `warpx.eb_potential(x,y,z,t)` 从参数入口图接到 examples / analysis 验证链，并记录 `external_vector_potential.*` 当前缺独立强 regression 的边界 |
| `notes/code-reading/utils/08-low-frequency-parameter-families-and-pass-throughs.md` | `Initialization/WarpXAMReXInit.cpp`、`WarpX.cpp`、`BoundaryConditions/FieldBoundaries.cpp`、`Particles/ParticleBoundaries.cpp`、`Initialization/ExternalField.cpp`、`Fluids/WarpXFluidContainer.cpp`、`Particles/MultiParticleContainer.cpp`、`Particles/Gather/GetExternalFields.cpp`、`Parallelization/GuardCellManager.cpp`、`FieldSolver/FiniteDifferenceSolver/MacroscopicProperties/MacroscopicProperties.cpp`、`FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp`、`Particles/ElementaryProcess/QEDSchwingerProcess.H` | 解释 `parameter-map` 最后那批低频空项为什么常常检索不到：文档 grouped alias、AMReX-owned pass-through 输入、外场聚合开关、PSATD/centering grouped key、macroscopic/hybrid parser 参数和 Schwinger 区域边界框的真实读取层次 |
| `docs/example-regression-map.md` | 657 个 Examples 输入/脚本和 356 个 checksum benchmark | 把测试/案例映射到物理模型、算法章节和验证用途 |
| `docs/literature-map.md` | 251 条 WarpX BibTeX 和 41 个本地 PDF | 把文献初步映射到算法/物理章节和 MinerU 状态 |
| `scripts/generate_stage_a_maps.py` | 阶段 A 索引生成脚本 | 后续 WarpX 源码或参考库变化时可重新生成索引 |

## 全源码精读框架

2026-05-14 根据反馈新增 `docs/warpx-source-reading-framework.md`，把 `../warpx/Source` 的约 712 个文件重排为可执行的 15 个精读阶段。

该框架覆盖：

- 根层 `main/WarpX/Fields`、`Evolve`、`Initialization`；
- `Particles` 的 container、gather、pusher、deposition、collision、QED、初始化、边界、重采样；
- `FieldSolver` 的 FDTD、PSATD、electrostatic、magnetostatic、implicit、hybrid；
- `BoundaryConditions`、`EmbeddedBoundary`、`Parallelization`、`Filter`；
- `Diagnostics`、`Python`、`Utils`、`ablastr`；
- `Laser`、`Fluids`、`AcceleratorLattice`、`NonlinearSolvers`。

后续 `source-map` 的扩展应按该框架的阶段顺序记录，避免只围绕当前已经熟悉的粒子/沉积路径继续局部扩写。

## 阶段 0 模块入口产物

2026-05-14 已建立 `notes/code-reading/README.md` 总索引，并为所有 Source 顶层模块建立精读入口：

| 模块入口 | 对应源码 | 当前用途 |
|---|---|---|
| `notes/code-reading/root/README.md` | 根层 `main.cpp`、`WarpX.*`、`Fields.H` | 阶段 1 主类状态精读入口 |
| `notes/code-reading/initialization/README.md` | `Initialization/` | 参数、初始化、注入器入口 |
| `notes/code-reading/evolve/README.md` | `Evolve/` | 时间推进入口 |
| `notes/code-reading/particles/README.md` | `Particles/` | 粒子系统入口 |
| `notes/code-reading/fieldsolver/README.md` | `FieldSolver/` | 场求解入口 |
| `notes/code-reading/boundary/README.md` | `BoundaryConditions/` | 场边界和 PML 入口 |
| `notes/code-reading/parallelization/README.md` | `Parallelization/` | guard cell、通信、AMR 入口 |
| `notes/code-reading/embedded-boundary/README.md` | `EmbeddedBoundary/` | EB 入口 |
| `notes/code-reading/filter/README.md` | `Filter/` | 滤波器入口 |
| `notes/code-reading/diagnostics/README.md` | `Diagnostics/` | 诊断和 I/O 入口 |
| `notes/code-reading/diagnostics/00-boundary-scraping-diagnostics-python.md` | `Diagnostics/BoundaryScrapingDiagnostics.*`, `Diagnostics/ParticleBoundaryBuffer.*`, `Python/ParticleBoundaryBufferWrapper.*`, `PICMI` scraping diagnostic glue | `BoundaryScraping` 如何绑定 scraped-particle buffer、flush 后何时清空，以及 Python/PICMI 如何零拷贝消费同一份边界事件流 |
| `notes/code-reading/diagnostics/01-diagnostics-dispatch.md` | `Diagnostics/MultiDiagnostics.*`, `Diagnostics/Diagnostics.*`, `Diagnostics/FullDiagnostics.*`, `Diagnostics/ParticleDiag.*` | diagnostics 工厂分派、`Diagnostics` 基类模板骨架、`FullDiagnostics` 主链与 `ParticleDiag` 作为 species 输出配置对象的真实角色 |
| `notes/code-reading/diagnostics/02-field-and-particle-functors.md` | `Diagnostics/ComputeDiagFunctors/*`, `Diagnostics/WarpXOpenPMD.*`, `Diagnostics/FlushFormats/FlushFormatPlotfile.*` | 字段 functor、`ParticleReductionFunctor`、writer 阶段粒子过滤/附加粒子场，以及 `phi` / `E/B` on particles 的真实边界 |
| `notes/code-reading/diagnostics/03-reduced-diagnostics.md` | `Diagnostics/ReducedDiags/*` | `MultiReducedDiags` 工厂、`ReducedDiags` 表格输出协议，以及 `FieldPoyntingFlux` 这类带 checkpoint 状态的 reduced diagnostics |
| `notes/code-reading/diagnostics/04-io-formats-and-restart.md` | `Diagnostics/FlushFormats/*`, `Diagnostics/BTDiagnostics.*`, `Diagnostics/WarpXIO.cpp` | checkpoint/restart、BTD 状态机、writer 分叉，以及 diagnostics 在恢复态中的延续边界 |
| `notes/code-reading/diagnostics/05-reduced-diagnostic-case-studies.md` | `Examples/Tests/reduced_diags/*`, `Diagnostics/ReducedDiags/*` | `FieldProbe`、`ParticleHistogram*`、`LoadBalanceCosts/Efficiency` 的最小实现骨架与 regression 断言 |
| `notes/code-reading/diagnostics/06-writer-comparison-and-minimal-cases.md` | `Diagnostics/FlushFormats/*`, `Examples/Tests/reduced_diags/*`, `Examples/Physics_applications/uniform_plasma/*` | plotfile/openPMD/checkpoint 三类 writer 的真实边界，以及最小输入骨架和 restart / writer 角色差异 |
| `notes/code-reading/diagnostics/07-output-layouts-and-reading-tools.md` | `plotfile/openPMD/checkpoint` 典型输出树、`Tools/PostProcessing/read_raw_data.py`, `yt`, `openPMD-viewer/api` | 三类输出布局、读者侧工具链与适用场景 |
| `notes/code-reading/diagnostics/08-template-cases-and-boundaryscraping-example.md` | `Examples/Physics_applications/thomson_parabola_spectrometer/*`, `point_of_contact_eb/*`, `scraping/*` | `plotfile/openPMD/checkpoint/BoundaryScraping` 四类模板与 `BoundaryScraping` 的真实读取入口 |
| `notes/code-reading/diagnostics/09-python-boundary-buffer-callback-case.md` | `Examples/Tests/particle_boundary_scrape/*`, `Examples/Physics_applications/spacecraft_charging/*` | `ParticleBoundaryBufferWrapper` 的离线检查与 callback 在线消费两种最小模式 |
| `notes/code-reading/laser/README.md` | `Laser/` | 激光模块入口 |
| `notes/code-reading/laser/00-laser-profile-dispatch.md` | `Laser/`, `Particles/LaserParticleContainer.*` | laser profile 字典、公共参数和人工天线粒子分派 |
| `notes/code-reading/laser/01-gaussian-from-file-and-runtime.md` | `Laser/LaserProfilesImpl/LaserProfileGaussian.cpp`, `LaserProfileFromFile.cpp`, `Particles/LaserParticleContainer.cpp` | Gaussian / from-file profile、lasy/binary 时间块读取、天线粒子运行时沉积链 |
| `notes/code-reading/laser/02-field-function-and-particle-update-kernel.md` | `Laser/LaserProfilesImpl/LaserProfileFieldFunction.cpp`, `Particles/LaserParticleContainer.cpp` | parser laser profile、平面坐标回投、mobility/weight 设定与人工天线粒子更新 kernel |
| `notes/code-reading/laser/03-laser-validation-map.md` | `Examples/Tests/laser_injection/`, `Examples/Tests/laser_injection_from_file/`, `Examples/Physics_applications/laser_acceleration/`, `Examples/Tests/boosted_diags/` | laser 注入、LWFA 场景、RZ openPMD、BTD 与 callback smoke test 的验证边界 |
| `notes/code-reading/laser/04-moving-window-external-field-coupling.md` | `Utils/WarpXMovingWindow.cpp`, `Initialization/ExternalField.*`, `Particles/LaserParticleContainer.cpp` | moving window 与 laser continuous injection、AMR finest spacing、parser/constant 外场重建和 file-driven 外场禁用的耦合边界 |
| `notes/code-reading/laser/05-application-and-diagnostic-cases.md` | `Examples/Physics_applications/laser_ion/`, `free_electron_laser/`, `laser_on_fine/`, `laser_acceleration/` | laser 应用层主线、diagnostics 组合、LWFA/PWFA runtime matrix 与 AMR placement/checksum 边界 |
| `notes/code-reading/laser/06-rigid-injection-btd-and-undulator-coupling.md` | `Examples/Physics_applications/free_electron_laser/`, `Examples/Tests/rigid_injection/`, `Examples/Tests/boosted_diags/` | rigid bunch、external particle-field undulator、BTD plotfile/openPMD 一致性与 FEL gain-length/wavelength 断言分层 |
| `notes/code-reading/laser/07-laser-ion-multiphysics-switches.md` | `Examples/Physics_applications/laser_ion/`, `Particles/Collision/CollisionHandler.*`, `Particles/ElementaryProcess/*`, `Particles/QED*` | laser 驱动 target 场景下 field ionization、collisions、QED 的开关边界与真实接入链 |
| `notes/code-reading/fluids/README.md` | `Fluids/` | 流体模块入口 |
| `notes/code-reading/fluids/00-fluid-container-map.md` | `Fluids/MultiFluidContainer.*`, `Fluids/WarpXFluidContainer.*`, `WarpX.cpp`, `WarpXEvolve.cpp`, `Utils/WarpXMovingWindow.cpp` | `fluids.species_names` 的对象图、`N/NU` level data、shared injector 初始化和 moving-window 连续再注入 |
| `notes/code-reading/fluids/01-muscl-hancock-update.md` | `Fluids/WarpXFluidContainer.cpp`, `Fluids/MusclHancockUtils.H` | cold relativistic fluid 的 `N/NU` 守恒更新、`ave` limiter、Rusanov flux、positivity limiter 和 RZ/spherical 几何修正 |
| `notes/code-reading/fluids/02-fluid-pic-coupling.md` | `Fluids/WarpXFluidContainer.cpp`, `FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp`, `WarpXEvolve.cpp`, `WarpXMovingWindow.cpp` | fluid species 的 `E/B` gather、Higuera-Cary source-step、`rho/J` 沉积，以及与 `HybridPICModel` 电子闭合的边界 |
| `notes/code-reading/nonlinear-solvers/README.md` | `NonlinearSolvers/` | 非线性/线性求解器入口 |
| `notes/code-reading/accelerator-lattice/README.md` | `AcceleratorLattice/` | 加速器晶格入口 |
| `notes/code-reading/accelerator-lattice/00-lattice-data-model.md` | `AcceleratorLattice/AcceleratorLattice.*`, `AcceleratorLattice/LatticeElements/LatticeElementBase.*` | 递归 beamline 输入树、`z_location` 几何账本和 host/device 对象图 |
| `notes/code-reading/accelerator-lattice/01-lattice-elements.md` | `AcceleratorLattice/LatticeElements/Drift.*`, `HardEdgedQuadrupole.*`, `HardEdgedPlasmaLens.*`, `HardEdged_K.H` | `drift`、`quad`、`plasmalens` 的参数/场语义与 residence correction |
| `notes/code-reading/accelerator-lattice/02-element-finder-device-path.md` | `AcceleratorLattice/LatticeElementFinder.*`, `AcceleratorLattice/AcceleratorLattice.cpp` | per-tile lookup table、boosted-frame 反变换与粒子侧外场累加 |
| `notes/code-reading/python/README.md` | `Python/` | Python binding 入口 |
| `notes/code-reading/python/00-python-module-init.md` | `Source/Python/pyWarpX.*`, `Source/Python/WarpX.cpp`, `Python/pywarpx/_libwarpx.py`, `Python/pywarpx/picmi.py` | 维度专用 pybind module、geometry-aware lazy load、WarpX singleton 暴露，以及 PICMI `Simulation.step()` 到 `WarpX::InitData/Evolve` 的主链 |
| `notes/code-reading/python/01-callbacks.md` | `Source/Python/callbacks.*`, `Source/Python/pyWarpX.cpp`, `Python/pywarpx/callbacks.py`, `Python/pywarpx/_libwarpx.py` | C++ 最小 callback 表、Python `CallbackFunctions` 聚合桥、固定 callback 名集合与 `exit(3)` 异常边界 |
| `notes/code-reading/python/02-field-particle-access.md` | `Source/Python/WarpX.cpp`, `Source/Python/MultiFabRegister.cpp`, `Source/Python/Particles/*.cpp`, `Python/pywarpx/fields.py`, `Python/pywarpx/picmi.py` | `multifab_register`、`multi_particle_container`、`particle_boundary_buffer` 三条数据访问面，以及 `sim.fields` / `sim.particles` 的真实指向 |
| `notes/code-reading/python/03-field-wrapper-validation-map.md` | `Examples/Tests/python_wrappers/`, `Python/pywarpx/fields.py`, `Python/pywarpx/extensions/MultiFabRegister.py`, `Source/Python/MultiFabRegister.cpp` | 把 `sim.fields.get(...)`、PML split fields、`F/G` cleaning 标量和 Python `MultiFabRegister` 绑定到一条最小强 regression |
| `notes/code-reading/utils/README.md` | `Utils/` | 工具、parser、moving window 入口 |
| `notes/code-reading/tools/README.md` | `Tools/` | top-level 工具目录入口 |
| `notes/code-reading/tools/00-parser-postprocessing-algorithms-boundary.md` | `Tools/Parser/input_file_parser.py`, `Tools/PostProcessing/read_raw_data.py`, `Tools/PostProcessing/plot_timestep_duration.py`, `Tools/Algorithms/stencil.py`, `psatd.ipynb`, `psatd_pml.ipynb` | 解释 top-level Parser 是轻量脚本、PostProcessing 是 reader/log helper、Algorithms 是推导/估计工具，不是 runtime 模块 |
| `notes/code-reading/tools/01-qed-tables-utils.md` | `Tools/QedTablesUtils/CMakeLists.txt`, `Tools/QedTablesUtils/Source/QedTableGenerator.cpp`, `QedTableReader.cpp`, `ArgParser/QedTablesArgParser.*` | 解释 `qed_table_generator` / `qed_table_reader` 的命令行分派、BW/QS 二进制布局和离线表工具链边界 |
| `notes/code-reading/build/README.md` | `CMakeLists.txt`, `Source/Make.WarpX`, `Source/*/CMakeLists.txt`, `Source/*/Make.package`, `Tools/machines/*` | 构建系统、维度变体和机器脚本入口 |
| `notes/code-reading/build/00-cmake-superbuild-and-module-aggregation.md` | `CMakeLists.txt`, `Source/FieldSolver/CMakeLists.txt`, `Source/Python/CMakeLists.txt`, `Docs/source/developers/repo_organization.rst`, `Docs/source/install/cmake.rst` | 顶层 option/variant 矩阵、依赖 superbuild、`lib_${SD}` / `pyWarpX_${SD}` target 聚合 |
| `notes/code-reading/build/01-gnu-make-and-dimension-variants.md` | `Source/Make.WarpX`, `Source/Make.package`, `Docs/source/developers/gnumake.rst`, `Docs/source/developers/dimensionality.rst` | GNUmake 旧构建链、`DIM/USE_RZ` 维度宏、`USERSuffix` feature 编码与 Python shared-lib 路径 |
| `notes/code-reading/build/02-hpc-machine-profiles.md` | `Tools/machines/desktop/spack-macos-openmp.yaml`, `Tools/machines/frontier-olcf/*`, `Docs/source/install/hpc.rst`, `Docs/source/install/hpc/frontier.rst` | `warpx.profile` / `install_dependencies.sh` / `submit.sh` 三件套与 machine-specialized build/deploy workflow |
| `notes/code-reading/applications/README.md` | `Examples/Tests/langmuir/*`, `Examples/Tests/langmuir_fluids/*`, 以及后续应用综合章条目 | 把底层模块笔记重新收束成应用级案例入口 |
| `notes/code-reading/applications/00-langmuir-wave.md` | `Examples/Tests/langmuir/*`, `Examples/Tests/langmuir_fluids/*`, `analysis_1d/2d/3d/rz/r1d.py`, `analysis_utils.py` | 从冷等离子体解析振荡、输入骨架、源码路径到 analysis/checksum/PICMI/fluids 分层，形成应用综合章第一条正式主线 |
| `notes/code-reading/applications/01-uniform-plasma.md` | `Examples/Physics_applications/uniform_plasma/*`, `Examples/Tests/energy_conserving_thermal_plasma/*`, `Examples/Tests/nci_psatd_stability/*` | 从均匀热等离子体背景、噪声/性能/workflow 基线，到 writer/checkpoint/restart 与相邻能量/NCI 强断言测试的边界，形成应用综合章第二条正式主线 |
| `notes/code-reading/applications/02-lwfa-pwfa.md` | `Examples/Physics_applications/laser_acceleration/*`, `Examples/Physics_applications/plasma_acceleration/*` | 把 `laser_acceleration` 的 `LWFA runtime matrix` 与 `plasma_acceleration` 的 `PWFA workflow matrix` 重新收束成共享 moving window、boosted frame、diagnostics、MR 和 PICMI/native front端分裂的第三条正式应用主线 |
| `notes/code-reading/applications/03-laser-targets-rpa-tnsa.md` | `Examples/Physics_applications/laser_ion/*`, `Examples/Physics_applications/plasma_mirror/*`, `Docs/source/glossary.rst` | 把 `laser_ion` 的强场靶 + diagnostics 组合、`plasma_mirror` 的 laser-solid workflow baseline，以及 `RPA/TNSA` 当前仅作为机制标签而非独立本地应用树的边界重新收束成第四条正式应用主线 |
| `notes/code-reading/applications/04-capacitive-discharge.md` | `Examples/Physics_applications/capacitive_discharge/*`, `analysis_1d.py`, `analysis_dsmc.py` | 把 1D Turner benchmark、Python callback Poisson solver、DSMC 分支和 2D native/PICMI workflow baseline 收束成第五条正式应用主线 |
| `notes/code-reading/ablastr/README.md` | `ablastr/` | 支撑库入口 |

## 阶段 1 Root / WarpX 主类状态产物

2026-05-14 已开始把 root 模块从入口索引推进到人工源码精读。第一篇笔记聚焦 `WarpX` 根对象、全局算法状态和 `m_fields` 场注册表。

| 文件 | 源码范围 | 当前用途 |
|---|---|---|
| `notes/code-reading/root/01-warpx-state-map.md` | `../warpx/Source/WarpX.H`、`../warpx/Source/WarpX.cpp`、`../warpx/Source/Fields.H` | 建立 `WarpX : amrex::AmrCore`、参数解析、主类成员状态、`FieldType` 和 `AllocLevelData()` 场分配的第一轮精读图谱 |
| `notes/code-reading/root/02-construction-and-level-allocation.md` | `../warpx/Source/WarpX.cpp:274-536`、`2271-3056`、`3058-3164` | 解释 `MakeWarpX()`、`WarpX::WarpX()`、`AllocLevelData()`、`AllocLevelMFs()` 和 spectral/FDTD solver 分配之间的生命周期边界 |

## 阶段 2 Initialization 产物

2026-05-14 已开始 `Initialization/` 模块的人工源码精读，先建立 fresh run / restart / level 初始化总调用图。

| 文件 | 源码范围 | 当前用途 |
|---|---|---|
| `notes/code-reading/initialization/00-init-callgraph.md` | `../warpx/Source/Initialization/WarpXInitData.cpp`、`../warpx/Source/Diagnostics/WarpXIO.cpp:94-180` | 解释 `InitData()` fresh/restart 分叉、`InitFromScratch()`、`InitPML()`、`InitLevelData()`、外场 parser 初始化、`PostRestart()` 和 `CheckGuardCells()` |
| `notes/code-reading/initialization/01-external-fields.md` | `../warpx/Source/Initialization/ExternalField.H`、`ExternalField.cpp`、`WarpXInitData.cpp:1642-1844` | 区分 grid external field 与 particle external field，解释 constant/parser/openPMD/Python 外场路径和 staggered 坐标插值 |
| `notes/code-reading/initialization/02-plasma-injector.md` | `../warpx/Source/Initialization/PlasmaInjector.H/.cpp`、`InjectorPosition.H`、`InjectorDensity.H`、`Particles/ParticleCreation/DefaultInitialization.H` | 建立 species 初始化、位置/密度/动量/flux functor、openPMD 粒子文件和 runtime attribute 默认初始化总图 |
| `notes/code-reading/initialization/03-density-momentum-dispatch.md` | `../warpx/Source/Utils/SpeciesUtils.H/.cpp`、`../warpx/Source/Initialization/InjectorMomentum.H` | 解释 species 质量/电荷优先级、密度 profile、动量分布参数、Boltzmann/Juttner 采样、parser 动量和 GPU 可用 tagged union |
| `notes/code-reading/initialization/04-particle-creation-kernels.md` | `../warpx/Source/Particles/PhysicalParticleContainer.cpp:429-449`、`ParticleCreation/AddParticles.cpp`、`AddPlasmaUtilities.H/.cpp`、`SmartCreate.H`、`DefaultInitialization.H`、`WarpXParticleContainer.cpp:183-354` | 解释初始化入口、`AddParticles()` 分发、`AddPlasma()` 体注入、`AddPlasmaFlux()` 面通量注入、权重公式、boosted-frame 修正、RZ/RSPHERE 几何权重和 runtime 属性写入 |
| `notes/code-reading/initialization/05-projection-div-cleaner.md` | `../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.H/.cpp`、`../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.cpp:209-217`、`../warpx/Docs/source/usage/parameters.rst:3792-3811` | 解释外部 `A/B` 场 projection divergence cleaning，推导 `∇²φ=-∇·F` 与 `F<-F+∇φ`，并区分初始化 projection cleaner 和演化阶段 div cleaning |
| `notes/code-reading/initialization/06-gaussian-beam-openpmd-injection.md` | `../warpx/Source/Initialization/PlasmaInjector.cpp:229-299`、`483-584`、`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:340-743`、`../warpx/Docs/source/usage/parameters.rst:1418-1494` | 解释 `gaussian_beam` 与 `external_file` 两条显式粒子列表注入路径，包括束流权重、cut、focusing、rotation、symmetrization、openPMD position/momentum/weighting 读取和单位换算 |
| `manuscript/chapters/03a-warpx-initialization.md` | 汇总 `Initialization/WarpXInitData.cpp`、`PlasmaInjector.cpp`、`SpeciesUtils.cpp`、`InjectorMomentum.H`、`ParticleCreation/AddParticles.cpp`、`ProjectionDivCleaner.*` | 正式书稿初始化章节入口，把 `00-06` 初始化 notes 的主链回填到正文 |
| `notes/code-reading/initialization/07-temperature-velocity-properties.md` | `../warpx/Source/Initialization/TemperatureProperties.H/.cpp`、`GetTemperature.H/.cpp`、`VelocityProperties.H/.cpp`、`GetVelocity.H/.cpp`、`../warpx/Docs/source/usage/parameters.rst:1701-1787` | 解释 Maxwell-Boltzmann/Juttner 初始化中的 `theta`、`beta`、`bulk_vel_dir`、parser 编译和漂移方向 functor |
| `notes/code-reading/utils/01-parser-system.md` | `../warpx/Source/Utils/Parser/ParserUtils.H/.cpp`、`IntervalsParser.H/.cpp`、`WarpXAlgorithmSelection.H`、`../warpx/Source/WarpX.cpp`、`../warpx/Source/Initialization/WarpXInit.cpp` | 解释 `ParmParse` 前缀命名空间、数值参数/表达式字符串/interval/枚举四类读取壳，以及参数到书稿章节的两级映射规则 |

## 阶段 C 主循环阅读产物

2026-05-14 已开始把自动索引转化为人工源码精读笔记和正式样章。

| 文件 | 内容 | 当前用途 |
|---|---|---|
| `notes/code-reading/evolve/00-lifecycle-and-callgraph.md` | 从 `main.cpp` 到 `WarpX::Evolve` 的对象生命周期、初始化顺序和 Mermaid 调用图 | 支撑 `manuscript/chapters/03-warpx-evolve.md` |
| `notes/code-reading/evolve/01-pic-time-layers.md` | 从 Vlasov-Maxwell 到 leapfrog PIC 时间层，再映射 `OneStep_nosub` | 支撑 `manuscript/chapters/02-pic-loop.md` |
| `notes/code-reading/evolve/02-evolve-source-evidence.md` | `WarpXEvolve.cpp`、`WarpXComputeDt.cpp`、`WarpXInitData.cpp` 的源码证据表 | 后续继续追踪粒子、场求解、同步、PSATD 和 subcycling |
| `notes/code-reading/evolve/03-subcycling-and-jrhom.md` | `../warpx/Source/Evolve/WarpXEvolve.cpp:389-496,839-1042,1043-1269`、`../warpx/Source/Parallelization/WarpXComm.cpp:1457-1788`、`../warpx/Source/WarpX.cpp:1584-1655`、`../warpx/Docs/source/usage/parameters.rst:3528-3540,3813-3828`、`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:286-306` | 解释 `OneStep_sub1()` 的两层 AMR subcycling、fine-to-coarse current/rho 同步，以及 `OneStep_JRhom()` 的 PSATD 多次源项沉积和谱推进 |
| `notes/code-reading/evolve/04-compute-dt-and-adaptive-timestep.md` | `../warpx/Source/Evolve/WarpXComputeDt.cpp`、`../warpx/Source/WarpX.cpp:679,797-810`、`../warpx/Docs/source/usage/parameters.rst:3169-3197` | 解释初始 `dt` 的 solver/CFL/`const_dt`/`max_dt` 分支、自适应粒子速度时间步、AMR subcycling 的 level dt 缩放 |
| `notes/code-reading/evolve/05-moving-window.md` | `../warpx/Source/Utils/WarpXMovingWindow.cpp`、`../warpx/Source/Initialization/WarpXInit.cpp:116-154`、`../warpx/Source/WarpX.cpp:354-372,705-717`、`../warpx/Source/Evolve/WarpXEvolve.cpp:240-270,1248-1256`、`../warpx/Docs/source/usage/parameters.rst:653-676` | 解释 moving window 参数读取、连续窗口位置、整数 cell 平移、`shiftMF()`、连续粒子/流体注入、PML 交换和 boosted-frame 速度变换 |

下一步应把 `OneStep_sub1()`、`OneStep_JRhom()`、AMR subcycling、PSATD-JRhom 和 moving window 的主循环细节继续回填到正式第 3 章，并转入 `FieldSolver` 的 `EvolveE/B/F/G` 实现。

## 阶段 4 FieldSolver 产物

2026-05-14 已开始 `FieldSolver/` 模块的人工源码精读，先从主循环 field push 分派进入 FDTD 与 PSATD 的顶层路由。

| 文件 | 源码范围 | 当前用途 |
|---|---|---|
| `notes/code-reading/fieldsolver/00-fieldsolver-dispatch.md` | `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:632-720,900-1086,1090-1190`、`../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp:48-220`、`EvolveE.cpp:50-228`、`EvolveF.cpp:48-138`、`EvolveG.cpp:36-111`、`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:31-160` | 解释 `WarpX::EvolveE/B/F/G` 的 level/patch/PML/boundary 分派，FDTD Cartesian 主 kernel，`F/G` divergence cleaning 和 PSATD spectral push 顶层流程 |
| `notes/code-reading/fieldsolver/01-fdtd-evolve-e-b.md` | `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.cpp:29-128`、`FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H`、`CartesianNodalAlgorithm.H`、`CartesianCKCAlgorithm.H`、`../warpx/Docs/source/usage/parameters.rst:3329-3353`、`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:81-160` | 解释 FDTD 差分系数初始化、Yee staggered forward/backward 差分、Nodal 中心差分、CKC/Cowan 扩展 stencil、CFL 与 guard cell |
| `notes/code-reading/fieldsolver/02-fdtd-pml.md` | `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveBPML.cpp`、`EvolveEPML.cpp`、`EvolveFPML.cpp`、`../warpx/Source/BoundaryConditions/PMLComponent.H:8-18`、`../warpx/Docs/source/theory/boundary_conditions.rst:8-60,174-210`、`../warpx/Docs/source/usage/parameters.rst:888-952` | 解释 Cartesian FDTD PML 的 split-field E/B/F 更新、PML component 存储、`pml_has_particles` 电流项、divergence cleaning components 和 RZ/spherical unsupported 边界 |
| `notes/code-reading/fieldsolver/03-pml-damping-current.md` | `../warpx/Source/BoundaryConditions/PML.cpp:67-146,290-335,582-646,689-1055,1130-1205`、`../warpx/Source/BoundaryConditions/WarpXEvolvePML.cpp:46-230,249-348`、`../warpx/Source/BoundaryConditions/WarpX_PML_kernels.H`、`../warpx/Source/BoundaryConditions/PML_current.H:17-144`、`../warpx/Source/Initialization/WarpXInitData.cpp:1095-1105` | 解释 PML box 构造、二次 sigma profile、`exp(-sigma dt)` 场阻尼、`sigma_cumsum_fac` 电流阻尼、PML current split source 和 regular/PML exchange |
| `notes/code-reading/fieldsolver/04-noncartesian-fdtd.md` | `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.cpp:46-76`、`FiniteDifferenceAlgorithms/CylindricalYeeAlgorithm.H`、`SphericalYeeAlgorithm.H`、`EvolveB.cpp:391-620`、`EvolveE.cpp:237-570`、`EvolveF.cpp:141-320`、`ComputeDivE.cpp:133-257`、`../warpx/Docs/source/usage/parameters.rst:622-639,3342` | 解释 RZ/RCYLINDER/RSPHERE 编译几何的 Yee-only 路径、cylindrical/spherical metric operators、RZ mode 实虚部耦合、轴上正则化、F/divE 非 Cartesian 更新 |
| `notes/code-reading/fieldsolver/05-psatd-spectral-flow.md` | `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:771-935`、`../warpx/Source/FieldSolver/SpectralSolver/SpectralSolver.cpp`、`SpectralFieldData.cpp`、`SpectralKSpace.cpp`、`SpectralAlgorithms/SpectralBaseAlgorithm.H`、`SpectralAlgorithms/PsatdAlgorithmGalilean.cpp:105-286`、`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:165-286`、`../warpx/Docs/source/usage/parameters.rst:3362-3538` | 解释 PSATD 从实空间 FFT 到谱空间推进再逆变换的主流程、current correction/Vay 分支、谱空间字段索引、local k-space、staggered shift 和 algorithm 虚分派 |
| `notes/code-reading/fieldsolver/06-psatd-galilean-current-correction.md` | `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.H`、`PsatdAlgorithmGalilean.cpp:105-286,302-460,451-633,634-860`、`../warpx/Docs/source/usage/parameters.rst:3400-3538` | 解释标准/Galilean PSATD 的 `C/S_ck/T2/X1-X4` 系数、零模极限、`update_with_rho` 重构、current correction 文档公式与源码对应、Vay spectral deposition 转换 |
| `notes/code-reading/fieldsolver/07-psatd-jrhom.md` | `../warpx/Source/Evolve/WarpXEvolve.cpp:430-466,840-1042`、`../warpx/Source/WarpX.cpp:1584-1655,1799-1811,3079-3159`、`../warpx/Source/FieldSolver/SpectralSolver/SpectralFieldData.cpp:30-103`、`PsatdAlgorithmJRhomFirstOrder.cpp`、`PsatdAlgorithmJRhomSecondOrder.cpp`、`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:286-360` | 解释 `psatd.JRhom` 字符串参数、多次 `J/rho` 沉积时刻、谱数组 `old/mid/new` 时间层、一阶/二阶 JRhom 源项多项式更新、`Y1-Y8` 系数和 current correction/Vay/Galilean 限制 |
| `notes/code-reading/fieldsolver/08-psatd-rz-hankel.md` | `../warpx/Source/FieldSolver/SpectralSolver/SpectralSolverRZ.cpp`、`SpectralFieldDataRZ.cpp`、`SpectralKSpaceRZ.cpp`、`SpectralHankelTransformer.cpp`、`HankelTransform.cpp`、`PsatdAlgorithmRZ.cpp`、`PsatdAlgorithmGalileanRZ.cpp`、`PsatdAlgorithmPmlRZ.cpp`、`../warpx/Source/WarpX.cpp:572,1093-1095,2457,3070-3121` | 解释 RZ PSATD 的 azimuthal mode component 布局、Hankel+FFT 变换链、`Ep/Em` 横向分量、Bessel roots 与 DHT 矩阵、RZ current correction、Galilean RZ 和 RZ PML |
| `notes/code-reading/fieldsolver/09-electrostatic-magnetostatic.md` | `../warpx/Source/FieldSolver/WarpXSolveFieldsES.cpp`、`../warpx/Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp`、`PoissonBoundaryHandler.cpp`、`LabFrameExplicitES.cpp`、`RelativisticExplicitES.cpp`、`EffectivePotentialES.cpp`、`../warpx/Source/FieldSolver/MagnetostaticSolver/MagnetostaticSolver.cpp`、`../warpx/Source/WarpX.cpp:399-410,729-781,2409-2524`、`../warpx/Docs/source/theory/models_algorithms/electrostatic_pic.rst`、`../warpx/Docs/source/usage/parameters.rst:360-510` | 解释 electrostatic 参数入口、solver 对象选择、Poisson 边界条件、labframe 总电荷 Poisson、relativistic species-by-species self fields、effective-potential variable-coefficient Poisson、magnetostatic vector Poisson 和 `B=curl A` |
| `notes/code-reading/fieldsolver/10-implicit-and-hybrid.md` | `../warpx/Source/WarpX.cpp:1248-1266,2480-2533`、`../warpx/Source/FieldSolver/WarpXPushFieldsHybridPIC.cpp`、`../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.*`、`ThetaImplicitEM.*`、`SemiImplicitEM.*`、`StrangImplicitSpectralEM.*`、`WarpXSolverVec.H`、`WarpXSolverDOF.H`、`../warpx/Source/NonlinearSolvers/*`、`../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.*`、`../warpx/Docs/source/usage/parameters.rst:240-320` | 解释 implicit evolve scheme 选择、非线性 solver 抽象、theta/semi/Strang implicit EM stencil、mass matrices、hybrid PIC 的 Ohm 定律闭合、外电流/外场分裂和 RK4 B-field push |
| `notes/code-reading/fieldsolver/11-psatd-coefficient-derivation.md` | `../warpx/Tools/Algorithms/psatd.ipynb`、`../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp`、`PsatdAlgorithmJRhomFirstOrder.cpp`、`PsatdAlgorithmJRhomSecondOrder.cpp`、`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:165-360` | 解释 PSATD notebook 的线性系统构造、齐次/非齐次解分解、`J/rho` 多项式源项、`exp(MΔt)` 对角化和系数表抽取，与运行时 `C/S_ck/T2/X1-X4`、`Y1-Y8` 和 `update_with_rho` 相互对照 |
| `notes/code-reading/fieldsolver/12-hybrid-pic-model-deep-dive.md` | `../warpx/Source/FieldSolver/WarpXPushFieldsHybridPIC.cpp`、`../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.H`、`HybridPICModel.cpp`、`ExternalVectorPotential.H`、`ExternalVectorPotential.cpp`、`../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICSolveE.cpp`、`../warpx/Docs/source/theory/models_algorithms/kinetic_fluid_hybrid_model.rst`、`../warpx/Docs/source/usage/parameters.rst:3578-3713` | 解释 kinetic-fluid hybrid 的广义 Ohm 定律、`rho/J_i/J_e/J_ext` 分裂、electron pressure closure、B 场 RK4 子步、`solve_for_Faraday` 分支、resistivity/hyper-resistivity、Holmstrom vacuum handling 和外部矢势 split-field |
| `notes/code-reading/fieldsolver/13-fieldsolver-verification-map.md` | `../warpx/Examples/Tests/CMakeLists.txt`、`../warpx/Examples/Tests/nci_fdtd_stability/CMakeLists.txt`、`nci_psatd_stability/CMakeLists.txt`、`electrostatic_sphere/CMakeLists.txt`、`implicit/CMakeLists.txt`、`ohm_solver_*/CMakeLists.txt` | 索引 FieldSolver 相关 regression tests 的输入文件、analysis 脚本、checksum 路径和源码章节覆盖关系；明确当前只完成定位，尚未运行本地测试 |
| `notes/code-reading/fieldsolver/14-fieldsolver-analysis-criteria.md` | `../warpx/Examples/Tests/nci_fdtd_stability/analysis_ncicorr.py`、`../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py`、`../warpx/Examples/Tests/electrostatic_sphere/analysis_electrostatic_sphere.py`、`../warpx/Examples/Tests/implicit/analysis_*.py`、`../warpx/Examples/Tests/ohm_solver_*/analysis*.py` | 精读 FieldSolver regression analysis 的实际物理判据、容差和 assert/checksum/可视化分层，覆盖 NCI 场能、PSATD Gauss law、静电球解析场、隐式能量/Gauss/迭代数和 hybrid Ohm 谱/增长率/阻尼率/重联率 |
| `notes/code-reading/applications/00-langmuir-wave.md` | `../warpx/Examples/Tests/langmuir/*`、`../warpx/Examples/Tests/langmuir_fluids/*`、`notes/code-reading/initialization/*`、`notes/code-reading/particles/*`、`notes/code-reading/fieldsolver/*`、`notes/code-reading/diagnostics/*` | 把 Langmuir wave 从冷等离子体解析振荡、输入骨架、源码调用链、analysis/checksum/PICMI 分层一路收束成应用级主线，并明确 `langmuir_fluids` 是 `Fluids/` 的直接应用级验证入口 |
| `notes/code-reading/applications/01-uniform-plasma.md` | `../warpx/Examples/Physics_applications/uniform_plasma/*`、`../warpx/Examples/Tests/energy_conserving_thermal_plasma/*`、`../warpx/Examples/Tests/nci_psatd_stability/*` | 把均匀热等离子体背景、full diagnostics、checkpoint/restart 最小工作流与相邻能量守恒、PSATD 稳定性强断言的边界收束成应用级主线 |
| `notes/code-reading/applications/02-lwfa-pwfa.md` | `../warpx/Examples/Physics_applications/laser_acceleration/*`、`../warpx/Examples/Physics_applications/plasma_acceleration/*`、`notes/code-reading/laser/05-application-and-diagnostic-cases.md` | 把 `laser_acceleration` 与 `plasma_acceleration` 从 moving window、boosted frame、diagnostics、MR 和 PICMI/native 前端分裂的角度收束成 wakefield acceleration 应用主线，并保留 `LWFA runtime matrix` / `PWFA workflow matrix` 的真实边界 |
| `notes/code-reading/applications/03-laser-targets-rpa-tnsa.md` | `../warpx/Examples/Physics_applications/laser_ion/*`、`../warpx/Examples/Physics_applications/plasma_mirror/*`、`../warpx/Docs/source/glossary.rst` | 把 `laser_ion` 的强场靶 + diagnostics 组合、`plasma_mirror` 的 laser-solid workflow baseline，以及 `RPA/TNSA` 当前仅作为机制标签的边界收束成应用级主线 |
| `notes/code-reading/applications/04-capacitive-discharge.md` | `../warpx/Examples/Physics_applications/capacitive_discharge/*`、`notes/code-reading/particles/19-backgroundmcc-pulseddecay-and-dsmc-branches.md`、`notes/code-reading/particles/22-perez-bremsstrahlungevent-and-fusion-probability-control.md` | 把 1D Turner benchmark、Python callback Poisson solver、DSMC 分支和 2D native/PICMI workflow baseline 收束成 PIC-MCC 低温等离子体应用主线 |
| `notes/code-reading/applications/05-magnetic-reconnection.md` | `../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/*`、`notes/code-reading/fieldsolver/10-implicit-and-hybrid.md`、`notes/code-reading/fieldsolver/12-hybrid-pic-model-deep-dive.md`、`notes/code-reading/fieldsolver/13-fieldsolver-verification-map.md`、`notes/code-reading/fieldsolver/14-fieldsolver-analysis-criteria.md`、`notes/code-reading/fluids/02-fluid-pic-coupling.md` | 把 `HybridPICModel`、force-free-sheet 初场、reduced `FieldProbe`、重联率提取与 checksum 分层收束成 hybrid-PIC space-plasma 应用主线，并明确它不是 `Fluids/` runtime layer 的应用页 |
| `notes/code-reading/applications/06-beam-collider-fel-extraction.md` | `../warpx/Examples/Tests/diff_lumi_diag/*`、`../warpx/Examples/Physics_applications/beam_beam_collision/*`、`../warpx/Examples/Physics_applications/free_electron_laser/*`、`../warpx/Examples/Physics_applications/ion_beam_extraction/*`、`../warpx/Examples/Tests/accelerator_lattice/*`、`notes/code-reading/diagnostics/05-reduced-diagnostic-case-studies.md`、`notes/code-reading/laser/06-rigid-injection-btd-and-undulator-coupling.md`、`notes/code-reading/utils/07-parameter-validation-links-for-boundary-and-external-fields.md`、`notes/code-reading/accelerator-lattice/03-validation-map.md` | 把 luminosity 强谱基准、collider-QED 应用骨架、boosted FEL 强 benchmark、EB electrostatic extraction 与 beamline optics 强回归收束成一条束流与加速器应用主线 |
| `notes/code-reading/nonlinear-solvers/00-solver-abstractions.md` | `../warpx/Source/NonlinearSolvers/NonlinearSolver.H`、`LinearSolver.H`、`Preconditioner.H`、`PicardSolver.H`、`NewtonSolver.H`、`WarpX_PETSc.cpp`、`MatrixPC.H`、`CurlCurlMLMGPC.H`、`../warpx/Docs/source/usage/parameters.rst:252-320` | 解释 Picard / Newton / SNES 抽象、线性 solver 接口、预条件器接口、PS-JFNK 残差组织和 curl-curl preconditioner |
| `notes/code-reading/nonlinear-solvers/01-newton-picard.md` | `../warpx/Source/NonlinearSolvers/NewtonSolver.H`、`PicardSolver.H`、`NonlinearSolver.H`、`../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.H`、`ThetaImplicitEM.cpp`、`SemiImplicitEM.cpp`、`StrangImplicitSpectralEM.cpp`、`WarpX_PETSc.cpp`、`../warpx/Docs/source/usage/parameters.rst:252-320` | 解释 Picard 固定点迭代、Newton 残差线性化、`Ops::ComputeRHS()` 契约、PETSc SNES / KSP 残差与 Jacobian 回调、线性求解参数和收敛判据 |
| `notes/code-reading/nonlinear-solvers/02-preconditioners-and-petsc.md` | `../warpx/Source/NonlinearSolvers/Preconditioner.H`、`MatrixPC.H`、`CurlCurlMLMGPC.H`、`WarpX_PETSc.cpp`、`../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverVec.H`、`WarpXSolverDOF.H`、`../warpx/Docs/source/usage/parameters.rst:252-320` | 解释 `MatrixPC`、`CurlCurlMLMGPC`、PETSc 向量/矩阵桥接、SNES/KSP wrapper 和隐式电磁预条件器结构 |

`manuscript/chapters/06-field-solvers.md` 已回填 6.10 Hybrid PIC 小节，`notes/code-reading/fieldsolver/13-fieldsolver-verification-map.md` 已建立验证样例索引，`14-fieldsolver-analysis-criteria.md` 已完成 analysis 判据精读。下一步应把这些判据回填到第 6 章验证小节，继续转入后续模块源码精读。

## 粒子推进与沉积阅读产物

2026-05-14 已完成粒子主链的第一轮人工精读，并据此重写第 4/5 章。

| 文件 | 内容 | 当前用途 |
|---|---|---|
| `notes/code-reading/particles/00-particle-evolve-callchain.md` | `WarpX::PushParticlesandDeposit -> MultiParticleContainer::Evolve -> PhysicalParticleContainer::Evolve -> PushPX` 调用链。 | 支撑 `manuscript/chapters/04-particle-pushers.md`。 |
| `notes/code-reading/particles/01-pusher-and-deposition-evidence.md` | Boris pusher、position update、current/charge deposition 分派证据表。 | 支撑 `manuscript/chapters/04-particle-pushers.md` 和 `05-deposition-shapes.md`。 |
| `notes/code-reading/particles/02-gather-shape-deposition-kernels.md` | Field gather、shape factor、charge deposition、direct current 和 Esirkepov current 的 kernel 级证据表。 | 支撑 `manuscript/chapters/04-particle-pushers.md` 和 `05-deposition-shapes.md` 的源码原文扩写。 |
| `notes/code-reading/particles/03-vay-higuera-cary-pushers.md` | Vay 与 Higuera-Cary pusher 的源码证据表。 | 支撑 `manuscript/chapters/04-particle-pushers.md` 的剩余 pusher 源码扩写。 |

下一步应继续进入 `Particles/Deposition/CurrentDeposition.H` 的 Villasenor、Vay、implicit charge-conserving 和 shared-memory direct 路径，并补齐 pusher 的 radiation reaction 与 implicit pusher。
