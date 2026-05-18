# Particles 源码精读入口

绑定源码：`../warpx/Source/Particles`。

本目录记录从 `WarpX::PushParticlesandDeposit()` 继续进入粒子模块后的源码阅读。当前已有内容已经覆盖显式电磁路径下的多物种循环、单物种 tile loop、field gather、momentum push、position push、charge/current deposition、粒子容器层次与 runtime attribute 系统、AMR coarse-fine interface 附近粒子的 gather/deposition buffer 路径，以及 `FieldGather.H` 的主要几何分支、implicit/deposition-coupled gather、external particle fields、field ionization、collision、QED、virtual photons、binary-collision products、background gas、pulsed decay、DSMC、resampling、thermalizer、sorting、`particle_pusher / single_particle / larmor / photon_pusher` 这组验证入口、`particle_fields_diags / plasma_lens / pass_mpi_communicator` 这组 diagnostics/外场/Python-MPI 接口验证入口、`particle_boundary_scrape / particle_data_python / particle_fields_diags` single-precision 这组 diagnostics/Python-wrapper validation、`particle_boundary_interaction / particle_boundary_process / particle_thermal_boundary / plasma_lens_python` 这组粒子边界与 Python front-end validation、`point_of_contact_eb / particles_in_pml / subcycling_mr / Langmuir multi_mr` 这组 EB 接触几何、带粒子 PML 与 MR validation 的真实断言边界，以及余下 `embedded_boundary_* / electrostatic_sphere_eb / scraping / particle_absorbing_boundary` helper 的验证清理；后续主要剩下更深的 collision/QED 实现细节与少量 validation 尾项。

## 模块边界

- 构建入口：`Particles/CMakeLists.txt`、`Particles/Make.package`。
- 直接加入的主体文件：`MultiParticleContainer.cpp`、`WarpXParticleContainer.cpp`、`PhysicalParticleContainer.cpp`、`PhotonParticleContainer.cpp`、`LaserParticleContainer.cpp`、`RigidInjectedParticleContainer.cpp`、`ParticleBoundaries.cpp`、`ParticleBoundaryBuffer.cpp`、`SpeciesPhysicalProperties.cpp`、`ExternalParticleFields.cpp`。
- 子模块：`Collision/`、`Deposition/`、`ElementaryProcess/`、`Gather/`、`ParticleCreation/`、`ParticleThermalizer/`、`Pusher/`、`Resampling/`、`Sorting/`。

## 核心问题

- 多 species、物理粒子、光子、激光粒子、刚性注入粒子的类层次和数据属性。
- gather、pusher、position update、deposition 如何在 tile kernel 中组合。
- 粒子边界、buffer、sorting、resampling、thermalizer 如何影响物理和性能。
- collision、电离、QED、virtual photons、background gas、DSMC 与 binary-collision products 如何插入主循环并分叉。

## 阅读顺序

1. `00-particle-evolve-callchain.md`：`WarpX::PushParticlesandDeposit -> MultiParticleContainer::Evolve -> PhysicalParticleContainer::Evolve -> PushPX`。
2. `01-pusher-and-deposition-evidence.md`：Boris pusher、position update、charge/current deposition 的源码证据表。
3. `02-gather-shape-deposition-kernels.md`：`FieldGather.H`、`ShapeFactors.H`、`ChargeDeposition.H`、`CurrentDeposition.H` 的 kernel 级证据表。
4. `03-vay-higuera-cary-pushers.md`：Vay 与 Higuera-Cary pusher 的源码证据表。
5. `04-amr-gather-deposition-buffers.md`：`aux`、`cax`、buffer masks、`PartitionParticlesInBuffers()` 如何进入 `PushPX`、`DepositCurrent()`、`DepositCharge()`。
6. `05-current-deposition-algorithms-near-amr-buffer.md`：Villasenor、Vay、Esirkepov implicit、Direct implicit 在 coarse-fine buffer 几何上的共同点与差异。
7. `06-charge-conserving-current-kernel-structures.md`：Esirkepov 的 old/new shape-difference 累加与 Villasenor 的 cell-crossing / segment-loop / tighter stencil。
8. `07-vay-deposition-d-field-structure.md`：Vay deposition 的 `D`-field / temporary-array / 二阶段重组结构与适用边界。
9. `32-current-deposition-continuity-and-geometry-boundaries.md`：把第 5 章里真正要保住的离散连续性合同、implicit 时间层恢复，以及 `RZ / 1D_Z / RCYLINDER / RSPHERE / 3D / XZ` 的 current deposition 实现边界压成一条独立主线。
10. `33-mass-matrix-and-temperature-variance-deposition.md`：把 `MassMatricesDeposition.H`、`TemperatureDeposition.H` 和 `VarianceAccumulationBuffer` 压成一条“线性响应矩阵与统计矩沉积”主线，区分它们和普通 `rho/J` 源项沉积的物理语义。
11. `34-sync-current-rho-and-source-synchronization.md`：把 `SyncCurrentAndRho()`、`SyncCurrent()`、`SyncRho()`、owner-mask 去重、buffer 合并、filter、PEC 边界反射压成一条“源项同步”主线。
12. `35-current-correction-and-vay-validation-map.md`：把 `Langmuir + current_correction` 与 `vay_deposition` 的真实断言边界压成一条“source-synchronization validation” 主线，区分解析场解对照与纯 `divE-rho/\epsilon_0` 断言。
13. `08-particle-class-and-attribute-map.md`：粒子容器类层次、编译期 SoA、runtime attributes、`x_n/ux_n`、`opticalDepthQSR`、`ionizationLevel`、`*_btd`。
14. `09-radiation-reaction-implicit-photon-pushers.md`：classical radiation reaction、implicit fixed-point / suborbits、photon `PushPX()`。
15. `10-implicit-suborbit-mass-matrices-jfnk.md`：`current_fp_non_suborbit`、`MassMatrices_PC`、JFNK linear stage、suborbit 重沉积。
16. `11-particle-boundaries-buffer-sorting.md`：已建立，覆盖 `boundary.particle_*`、`particles.crop_on_PEC_boundary`、absorbing/reflecting/thermal 边界、scraped particle buffer、invalid 删除与 sorting 在 Villasenor / suborbit 路径中的交界。
17. `12-field-ionization-adk-pipeline.md`：ADK filter、`InitIonizationModule()`、product species、`ionizationLevel` 与 `rho/J` 沉积闭环。
18. `13-collision-handler-stepping-and-regression-map.md`：`CollisionHandler` 分派、`CollisionBase` 的 subcycle/supercycle 合同、`split_momentum_push` 与 regression 验证层。
19. `14-qed-entrypoints.md`：QED runtime attributes、`InitQED()`、Quantum Synchrotron / Breit-Wheeler / Schwinger 三条主链，以及对应 regression。
20. `15-qed-kernels-and-wrapper-contracts.md`：optical depth 在 push 中的演化、`filterCopyTransformParticles` 触发条件、source/product 更新语义、PICSAR-QED wrapper 的职责边界。
21. `16-qed-table-generation-and-serialization.md`：`builtin / load / generate` 三条 QED table 生命周期、raw binary 序列化格式、IOProcessor 生成与 MPI 广播合同。
22. `17-qed-chi-virtual-photons-and-linear-breit-wheeler.md`：`QedChiFunctions` 的 `chi` 包装角色、virtual photons 的 collision 前置辅助 species 生成、以及 `linear_breit_wheeler` / `linear_compton` 与 `ElementaryProcess` 强场 QED 主链的分叉关系。
23. `18-binary-collision-product-creation-and-linear-compton.md`：`BinaryCollision` 的事件表输出、`ParticleCreationFunc` 的统一 product 落地、`LinearBreitWheeler` 的四宏粒子实现与 `LinearCompton` 的单-product-per-species 特例。
24. `19-backgroundmcc-pulseddecay-and-dsmc-branches.md`：`BackgroundMCC` 的背景气体 null-collision 风格频率上界、`PulsedDecay` 的 cell 内 fixed-weight 衰变，以及 DSMC `SplitAndScatterFunc` 与 `ParticleCreationFunc` 的后半段分叉。
25. `20-coulomb-bremsstrahlung-stopping-and-fusion.md`：`pairwisecoulomb` 的 Perez 弹性散射、`bremsstrahlung` 的专门 photon-creation 分支、`background_stopping` 的解析 slowing-down 公式，以及 `nuclearfusion` 的 event-multiplier / probability-threshold / cross-section 分叉。
26. `21-collision-kernel-details-and-product-initializers.md`：`ElasticCollisionPerez` 的 Debye/atomic 尺度与加权 `n12`、Bremsstrahlung photon `ux/uy/uz` 写回尾部、两产物 fusion 的 4 宏粒子复制，以及 p-B11 两步反应的 6 alpha 初始化。
27. `22-perez-bremsstrahlungevent-and-fusion-probability-control.md`：Perez kernel 的 `s12` 四段式散射角抽样与 weighted rejection、`BremsstrahlungEvent(...)` 的 plasma-frequency cutoff 与表驱动 photon-energy 反演、`SingleNuclearFusionEvent.H` 的 `probability_threshold / probability_target_value` 有效倍率回退，以及 2D/3D/isotropization/RZ collision regressions 与 `background_mcc` 应用级 checksum 的真实边界。
24. `23-resampling-thermalizer-and-sorting.md`：`ResamplingTrigger` 的 intervals / global-average-ppc 触发合同、`LevelingThinning` 与 `VelocityCoincidenceThinning` 两条重采样算法、`ParticleThermalizer` 在 boundary 之后 collisions 之前的局部热化路径，以及 `sort_intervals` / deposition sort / generic bin sort 的全局性能排序语义。
25. `24-thermalizer-validation-and-checksum-boundaries.md`：`particle_absorbing_boundary` 如何作为 `ParticleThermalizer` 的耦合式 regression 入口，以及 `analysis_default_regression.py` 在 `particle_absorbing_boundary`、`resampling`、`capacitive_discharge` 中作为通用 checksum helper 的真实边界。
26. `25-gather-variants-and-external-particle-fields.md`：`FieldGather.H` 在 `1D_Z / RCYLINDER / RSPHERE / 3D` 下的剩余 gather 分支、energy-conserving 与 momentum-conserving 的真实代码差异、implicit gather 对沉积算法的 stencil 耦合，以及 external particle fields 在 parser / repeated-lens / read-from-file 三条路径下怎样进入 `PushPX()`。
27. `26-pusher-single-particle-and-photon-validation-map.md`：`particle_pusher`、`single_particle`、`larmor`、`photon_pusher` 四组 regression 分别在验证 Higuera-Cary pusher、bilinear current filter、diagnostics 半步速度同步、massless photon transport，还是仅作为应用级 checksum 基线。
28. `27-particle-fields-plasma-lens-and-mpi-validation-map.md`：`particle_fields_diags` 如何验证 `particle_fields_to_plot` 的 reduction/writer 合同，`plasma_lens` 如何验证 repeated-plasma-lens 与 hard-edged lattice lens 两条 external particle field 路径，以及 `pass_mpi_communicator` 为什么当前仍是未启用的 Python/MPI communicator handoff 脚手架。
29. `28-particle-diagnostics-python-interface-validation-map.md`：`particle_boundary_scrape` 如何同时验证 EB scraping 删除和 Python boundary-buffer wrapper，`particle_data_python` 如何验证 runtime attributes / 手动沉积 / 旧位置缓存这条 Python 接口链，以及 `particle_fields_diags` single-precision 为何当前仍停在“脚本已存在但 CMake 未启用”的保留状态。
30. `29-boundary-and-python-front-end-validation-map.md`：`particle_boundary_interaction` 如何通过 scraped-buffer 几何与 Python callback 实现自定义镜面反射，`particle_boundary_process` 如何分别验证 absorbing boundary 的随机反射模型与粒子吸收删除，`particle_thermal_boundary` 如何用 reduced-diag 能量账本约束 thermal particle boundary，以及 `plasma_lens_python` 如何把同一 repeated-plasma-lens 物理 analysis 扩展到纯 Python 参数前端。
31. `30-pml-eb-contact-and-mr-validation-map.md`：`point_of_contact_eb` 如何验证 `BoundaryScraping/openPMD` 里的接触点、时间戳和法向，`particles_in_pml` 如何验证带粒子 PML 后残余场是否足够小，`subcycling_mr` 为什么当前仍只是 AMR+subcycling 组合稳定性的 checksum 基线，以及 `Langmuir multi_mr` 如何继续用解析场解与 charge conservation 做 MR 强基准。
32. `31-embedded-boundary-and-helper-validation-cleanup.md`：`particle_absorbing_boundary/plot_*.py` 为什么只是可视化 helper，`embedded_boundary_cube/rotated_cube/diffraction/em_particle_absorption` 各自在验证哪类解析场解或 scraped-particle 合同，`embedded_boundary_python_api` 怎样在 PICMI 输入脚本内部断言 `edge_lengths/face_areas` wrapper，以及 `electrostatic_sphere_eb`、`scraping` 这两组 EB 条目应该如何从粗分类改写成具体验证语义。

## 输出目标

- 继续扩写 `manuscript/chapters/04-particle-pushers.md` 和 `05-deposition-shapes.md`。
- 为多物理卷建立 collision、ionization、QED、virtual photons、background gas、pulsed decay、pairwise Coulomb、bremsstrahlung、background stopping、fusion 与 binary-collision/DSMC product 创建语义的源码入口。

## 本轮已确认的核心事实

- `MultiParticleContainer::Evolve()` 在不跳过沉积时先清零当前步的 `current_fp/current_buf/rho_fp/rho_buf`，然后遍历所有 species。
- `PhysicalParticleContainer::Evolve()` 在每个 tile 内按顺序处理旧电荷沉积、field gather 和粒子推进、电流沉积、新电荷沉积。
- `PhysicalParticleContainer::PushPX()` 是 field gather、外场叠加、momentum pusher 和 position update 的融合 kernel。
- `PushSelector.H` 负责按 `ParticlePusherAlgo` 分派 Boris、Vay、Higuera-Cary 或带 classical radiation reaction 的 Boris。
- `WarpXParticleContainer::DepositCurrent()` 根据 `current_deposition_algo` 分派 Esirkepov、Villasenor、Vay、Direct 和隐式/共享内存变体。
- `doGatherShapeN()` 先把运行时 `nox` 和 `galerkin_interpolation` 转成模板参数，再按场分量 staggering 选择 node/cell 与 Galerkin 降阶 shape。
- `doChargeDepositionShapeN()` 把 `q*wp*invvol` 乘 shape 权重原子加到 `rho_arr`，电离 species 再乘 `ion_lev`。
- Direct current deposition 使用半步位置和 \(q w_p \mathbf{v}/\Delta V\) 沉积；Esirkepov deposition 使用 old/new shape 差构造守恒电流。
- `UpdateMomentumVay.H` 通过解析新 \(\gamma\) 构造相对论 Vay pusher；`UpdateMomentumHigueraCary.H` 在 Boris-like 结构上加入 Higuera-Cary 的修正旋转项。
- AMR coarse-fine interface 处，粒子并不是在 gather/deposition kernel 内临时查 mask；`PartitionParticlesInBuffers()` 会先重排粒子数组，再分别把前半段送进 `E/Bfield_aux + current_fp/rho_fp`，后半段送进 `E/Bfield_cax + current_buf/rho_buf`。
- 粒子属性系统分成三层：`PIdx` 编译期 builtin real、`PhysicalParticleContainer`/ionization/QED 在运行时补加的持久属性，以及 implicit / back-transformed particles 路径按 `comm=0` 动态加入的临时缓存属性。
- field ionization 的主链不是“额外 source term”，而是 `InitIonizationModule() -> IonizationFilterFunc -> filterCopyTransformParticles -> ionizationLevel 进入 rho/J 沉积` 这一整条 species/runtime-attribute/deposition 闭环。
- collision 的第一入口不在单 species，而在 `MultiParticleContainer -> CollisionHandler -> CollisionBase` 这条调度链；真正的公共合同首先是步频和插入位置，而不是某个具体散射公式。
- QED 的第一入口也不在单个 kernel，而在 species 构造期 runtime attributes、`mapSpeciesProduct()`、`CheckQEDProductSpecies()` 和 `InitQED()` 这套对象图装配；真正运行时又分成 Quantum Synchrotron、Breit-Wheeler 和 Schwinger 三条不同事件链。
- QED 更深一层的 kernel 合同是：optical depth 平时在 `PushPX()` 中先演化，只有变成负值后，后续 `PhotonEmissionFilterFunc` / `PairGenerationFilterFunc` 才会触发 `filterCopyTransformParticles`；wrapper 本身不重写物理，只桥接 PICSAR-QED core。
- RR、implicit 和 photon path 并不是三套完全独立容器；它们共享 `PhysicalParticleContainer::Evolve()` 或 `doParticleMomentumPush()` 的外壳，但分别在单粒子 momentum 修正、`x_n/ux_n/nsuborbits` 收敛循环、以及“无 charge/current 沉积的光子 push”这三处显著分叉。
- implicit 粒子推进还要继续分成两层看：粒子 fixed-point / suborbit 轨道本身，以及 `current_fp_non_suborbit + MM*(E-E0) + J_suborbit` 这套 JFNK 线性化源项拼装。
