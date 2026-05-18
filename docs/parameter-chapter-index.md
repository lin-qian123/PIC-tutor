# 参数到章节索引（第一版人工校正）

本文件是对 [parameter-map.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/parameter-map.md) 的人工补层。

当前原则：

- `parameter-map.md` 继续保留自动抽取的文档行号和初步源码命中。
- 本文件只做“参数族到底应回哪一章”的人工校正。
- 正式结论仍以本地 WarpX 源码、官方文档和对应章节正文为准。

绑定源码与文档：

- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Initialization/WarpXInit.cpp`
- `../warpx/Source/Utils/Parser/*`
- 已有书稿章节 `03/03A/04/05/06/07/08`

## 1. 映射规则

第一层看“第一次在哪里被 `ParmParse` 读取”，第二层看“真正在哪一章解释其物理或数值语义”。

| 参数族 | 第一解析层 | 主要书稿章节 |
|---|---|---|
| 无前缀参数：`max_step`、`stop_time` | `WarpX.cpp::ReadParameters()` 与 `Evolve()` | 第 3 章 |
| `geometry.*`、`amr.*`、moving window / boost / startup 运行契约 | `WarpXAMReXInit.*`、`WarpXInit.*`、`WarpX.cpp` | 第 3A 章 |
| `algo.*`、`interpolation.*`、`psatd.*`、`warpx.cfl/max_dt/...` | `WarpX.cpp::ReadParameters()` | 第 3/4/5/6 章 |
| `boundary.*`、PML、EB、AMR 通信 | `WarpX.cpp`、Boundary/AMR 模块 | 第 7 章 |
| species、external field、`particles.*` | Initialization / Particles | 第 3A、4 章 |
| `lasers.*` | Laser / Initialization | 第 3A 章加 Laser 笔记 |
| `diagnostics.*`、`<diag>.*`、`warpx.reduced_diags_names`、`reduced_diags.*` | Diagnostics | 第 8 章 |
| `collisions.*`、`<collision>.*`、QED 相关 | Collision / QED | 第 4 章 |

## 2. 代表性参数的人工章节归属

| 参数 | 第一次解析位置 | 章节归属 | 说明 |
|---|---|---|---|
| `max_step` | `WarpX.cpp::ReadParameters()` | 第 3 章 | 无前缀运行控制；决定外层时间推进终止条件 |
| `stop_time` | `WarpX.cpp::ReadParameters()` | 第 3 章 | 无前缀物理时间终止条件 |
| `authors` | diagnostics writer | 第 8 章 | openPMD 元数据，不属于物理解算参数 |
| `warpx.gamma_boost` | `ConvertLabParamsToBoost()` / `ReadBoostedFrameParameters()` | 第 3A 章 | 启动层先改 parser，构造期再落到运行态 |
| `warpx.boost_direction` | 同上 | 第 3A 章 | 与 boosted-frame 几何改写绑定 |
| `geometry.dims` | `check_dims()` | 第 3A 章 | 编译维度契约，不只是几何装饰字符串 |
| `amr.n_cell` | `parse_geometry_input()` | 第 3A 章 | geometry / level 布局前就被求值 |
| `amr.max_level` | `ReadParameters()` | 第 3A、7 章 | 初始化对象图先读，AMR 真正语义在第 7 章 |
| `warpx.do_moving_window` | `read_moving_window_parameters()` | 第 3A 章 | 启动层锁定，演化期消费 |
| `warpx.moving_window_dir` | 同上 | 第 3A 章 | moving window 几何契约 |
| `warpx.moving_window_v` | 同上 | 第 3A 章 | 启动层从 `c` 单位换到物理速度 |
| `algo.evolve_scheme` | `WarpX.cpp::ReadParameters()` | 第 3、6 章 | 决定 `OneStep` 分派，隐式部分回第 6 章 |
| `warpx.do_electrostatic` | `WarpX.cpp::ReadParameters()` | 第 3A、6 章 | 初始化时决定 solver 对象图，物理语义在第 6 章 |
| `warpx.poisson_solver` | `WarpX.cpp::ReadParameters()` | 第 6 章 | Poisson 解法分支 |
| `warpx.const_dt` | `WarpX.cpp::ReadParameters()` / `ComputeDt()` | 第 3 章 | 时间步控制 |
| `warpx.dt_update_interval` | `IntervalsParser` | 第 3 章 | 不是普通整数，而是 interval 语法 |
| `warpx.cfl` | `WarpX.cpp::ReadParameters()` | 第 3、6 章 | 步长入口在第 3 章，CFL 物理解释回第 6 章 |
| `warpx.use_filter` | `WarpX.cpp::ReadParameters()` | 第 3A、5 章 | 初始化里决定 guard/filter 资源，沉积/噪声语义回第 5 章 |
| `boundary.field_lo/hi` | field boundary parser | 第 7 章 | 场边界条件 |
| `boundary.particle_lo/hi` | particle boundary parser | 第 7、4 章 | 输入在第 7 章，粒子后续行为在第 4 章 |
| `lasers.names` | `LaserParticleContainer` 构造期 | 第 3A 章 | 激光注入对象图入口 |
| `diagnostics.diags_names` | `MultiDiagnostics` | 第 8 章 | diagnostics 顶层注册 |
| `warpx.reduced_diags_names` | `MultiReducedDiags` | 第 8 章 | reduced diagnostics 顶层注册 |
| `collisions.collision_names` | `CollisionHandler` | 第 4 章 | 碰撞总调度入口 |

## 3. 第二批已校正高频参数

| 参数 | 第一次解析位置 | 章节归属 | 说明 |
|---|---|---|---|
| `warpx.used_inputs_file` | `InitData()` 后写出 used-inputs 文件 | 第 3A 章 | 启动/初始化产物，不是演化期控制量 |
| `warpx.break_signals` | `WarpX.cpp::ReadParameters()` | 第 3 章 | 外层运行控制；决定优雅退出条件 |
| `warpx.checkpoint_signals` | `WarpX.cpp::ReadParameters()` | 第 3、8 章 | 先是运行控制，再落到 checkpoint 输出链 |
| `warpx.verbose` | `WarpX.cpp::ReadParameters()` | 第 3 章 | 全局运行期打印级别；diagnostics 只是局部继承或覆盖 |
| `warpx.limit_verbose_step` | `WarpX.cpp::ReadParameters()` | 第 3 章 | 只影响主循环打印节奏 |
| `warpx.serialize_initial_conditions` | `WarpX.cpp::ReadParameters()` | 第 3A 章 | 初始化阶段的可复现实验开关 |
| `warpx.safe_guard_cells` | `WarpX.cpp::ReadParameters()` | 第 7 章 | guard-cell / moving-window / coarse-fine 通信的 debug-safe 模式 |
| `amrex.abort_on_unused_inputs` | AMReX startup 参数 | 第 3A 章 | 启动层/CI 契约，不属于某个物理模块 |
| `amrex.use_profiler_syncs` | AMReX runtime/profiling 参数 | 第 7 章 | 直接服务并行通信计时与负载观测 |
| `ablastr.fillboundary_always_sync` | `ablastr::utils::Communication` | 第 7 章 | 强制 nodal `FillBoundary` 同步，属于通信/调试开关 |
| `algo.maxwell_solver` | `WarpX.cpp::ReadParameters()` | 第 3、6 章 | 构造期决定 field solver 分派，物理/数值语义在第 6 章 |
| `algo.evolve_scheme` | `WarpX.cpp::ReadParameters()` | 第 3、6 章 | 决定 `OneStep` 主分支，implicit/JFNK 解释回第 6 章 |
| `algo.current_deposition` | `WarpX.cpp::ReadParameters()` | 第 3、5 章 | 运行期总开关在第 3 章，沉积算法细节在第 5 章 |
| `algo.charge_deposition` | `WarpX.cpp::ReadParameters()` | 第 3、5 章 | 同上 |
| `algo.field_gathering` | `WarpX.cpp::ReadParameters()` | 第 3、4 章 | 运行期总开关在第 3 章，gather kernel 在第 4 章 |
| `algo.particle_pusher` | `WarpX.cpp::ReadParameters()` | 第 3、4 章 | 运行期总开关在第 3 章，粒子推进器细节在第 4 章 |
| `algo.load_balance_intervals` | `IntervalsParser` + `WarpX.cpp` | 第 7 章 | AMR / load-balance 时序入口 |
| `algo.load_balance_with_sfc` | `WarpX.cpp::ReadParameters()` | 第 7 章 | SFC vs knapsack 的负载均衡策略选择 |
| `algo.load_balance_costs_update` | `query_enum_sloppy(...)` | 第 7 章 | `heuristic/timers` 两类 costs 更新模型 |
| `diagnostics.diags_names` | `MultiDiagnostics::ReadParameters()` | 第 8 章 | top-level diagnostics 注册 |
| `<diag_name>.intervals` | `Diagnostics` | 第 8 章 | full / BTD diagnostics 的时间切片入口 |
| `<diag_name>.dt_snapshots_lab` | `BTDiagnostics` | 第 8 章 | BTD lab-frame 快照间隔 |
| `<diag_name>.buffer_size` | `BTDiagnostics` | 第 8 章 | BTD buffer 容量控制 |
| `warpx.reduced_diags_names` | `MultiReducedDiags` | 第 8 章 | top-level reduced diagnostics 注册 |
| `<reduced_diags_name>.type` | `ReducedDiags` | 第 8 章 | reduced diagnostics 工厂分派 |
| `reduced_diags.intervals` | `ReducedDiags` | 第 8 章 | reduced diagnostics 时间切片入口 |
| `reduced_diags.path` | `ReducedDiags` | 第 8 章 | reduced diagnostics 输出路径 |
| `reduced_diags.extension` | `ReducedDiags` | 第 8 章 | reduced diagnostics 文件后缀 |
| `reduced_diags.separator` | `ReducedDiags` | 第 8 章 | reduced diagnostics 文本列分隔符 |
| `reduced_diags.precision` | `ReducedDiags` | 第 8 章 | reduced diagnostics 文本精度 |

## 4. 第三批已校正参数族

| 参数族 | 第一次解析位置 | 章节归属 | 说明 |
|---|---|---|---|
| `warpx.self_fields_*`、`warpx.magnetostatic_solver_*` | `WarpX.cpp`、electrostatic / magnetostatic solver 构造与调用链 | 第 3A、6 章 | 构造期决定 solver 容差与迭代预算，物理/数值语义属于静电静磁求解 |
| `boundary.*`、`warpx.pml_*`、`do_similar_dm_pml`、`warpx.eb_potential(...)` | `WarpX.cpp`、PML / EB 初始化与边界模块 | 第 7 章；其中 `boundary.particle_*`、`pml_has_particles` 兼接第 4 章 | 这批参数控制 boundary、PML、EB 和粒子边界/PML 行为，不应再挂旧的 boundary 计划编号 |
| `warpx.num_mirrors`、`warpx.mirror_z*` | `WarpX.cpp` | 第 7 章；boosted 相关约束兼接第 3A 章 | 本质上是域内 perfect-mirror 边界合同，而不是一般启动参数 |
| `lattice.*`、`<element_name>.type` | `AcceleratorLattice::ReadLattice()` | 第 4 章 | 这些参数直接定义粒子推进时消费的 accelerator lattice 元素 |
| `collisions.*`、`<collision_name>.*` | `CollisionHandler` / `CollisionBase` / 各具体 collision 分支 | 第 4 章 | 已把 pairwise Coulomb、DSMC、BackgroundMCC、PulsedDecay、Bremsstrahlung、Fusion、Linear Breit-Wheeler/Compton 的参数统一拉回粒子多物理章节 |
| `qed_qs.*`、`qed_bw.*`、`qed_schwinger.*`、species QED 开关 | `MultiParticleContainer::ReadParameters()` / `InitQED()` | 第 4 章 | 已与 collision 分支区分：强场 QED、lookup table、Schwinger、RR 都属于粒子/QED 章节 |
| `warpx.use_hybrid_QED`、`warpx.quantum_xi` | `WarpX.cpp::ReadParameters()` | 第 6 章 | 这是场求解器级 QED Maxwell 修正，不属于粒子 QED 输入 |
| `warpx.cfl`、`warpx.const_dt`、`warpx.max_dt`、`warpx.dt_update_interval` | `WarpX.cpp::ReadParameters()` / `ComputeDt()` | 第 3 章；电磁/静电解释兼接第 6 章 | 已从旧 `ComputeDt` 计划编号迁到真实时间推进与 solver 章节 |
| `psatd.*` | `WarpX.cpp::ReadParameters()` / PSATD solver | 第 6 章 | 已把 `nox/noy/noz`、guard、Galilean/comoving、`current_correction`、`JRhom` 全部拉回场求解器章节 |
| `warpx.sort_*`、shared-memory deposition | `WarpX.cpp::ReadParameters()` | 第 4、5 章 | sorting 属于粒子执行层；shared-memory charge/current deposition 属于沉积实现与性能路径 |
| `diagnostics.enable`、`warpx.synchronize_velocity_for_diagnostics`、`<diag_name>.*` writer / BTD / particle-output / raw-fields / async-I/O 参数 | `MultiDiagnostics`、`Diagnostics`、`BTDiagnostics`、writer | 第 8 章 | 已把 full diagnostics、BTD、time-average、plotfile/openPMD/back-transformed/async-I/O 参数统一拉回 diagnostics 章节 |
| `amr.restart`、`warpx.write_diagnostics_on_restart` | `WarpX.cpp` / diagnostics restart 路径 | 第 8 章 | checkpoint/restart 与 restart 时 diagnostics 写出属于 diagnostics / restart 合同 |

## 5. 对象前缀子族导航（第一版）

这一层不再按“第几批修了什么”组织，而是直接回答：

- 某类参数第一次在哪里被读；
- 应优先去哪章看正文；
- 若需要源码精读，先看哪组笔记。

### 5.1 Species / Particle Initialization

| 参数族 | 第一次解析位置 | 主要章节 | 先看笔记 |
|---|---|---|---|
| `particles.species_names`、`particles.rigid_injected_species`、`particles.do_tiling` | `MultiParticleContainer` / startup | 第 3A、4 章 | `initialization/02-04`、`laser/06`、`particles/README` |
| `<species_name>.species_type`、`charge`、`mass` | `SpeciesUtils` / `WarpXParticleContainer` | 第 3A、4 章 | `initialization/02-plasma-injector.md`、`03-density-momentum-dispatch.md` |
| `<species_name>.injection_style`、`num_particles_per_cell_each_dim`、`random_theta` | `PlasmaInjector` / particle creation | 第 3A、4 章 | `initialization/02-plasma-injector.md`、`04-particle-creation-kernels.md` |
| `<species_name>.do_continuous_injection`、`zinject_plane`、`rigid_advance`、`do_backward_propagation` | initialization + runtime injection | 第 3A、4 章 | `evolve/05-moving-window.md`、`laser/06-rigid-injection-btd-and-undulator-coupling.md` |
| `<species_name>.profile`、`flux_profile`、`density_min/max`、`radial_numpercell_power` | `InjectorDensity` / `SpeciesUtils` | 第 3A、4 章 | `initialization/02-plasma-injector.md`、`03-density-momentum-dispatch.md` |
| `<species_name>.momentum_distribution_type`、`theta_distribution_type`、`beta_distribution_type` | `InjectorMomentum` / temperature / velocity helpers | 第 3A、4 章 | `initialization/03-density-momentum-dispatch.md`、`07-temperature-velocity-properties.md` |
| `<species_name>.initialize_self_fields`、`self_fields_*` | electrostatic self-field initialization | 第 3A、6 章 | `initialization/05-projection-div-cleaner.md`、`14-19` 验证地图 |
| `<species_name>.do_not_deposit/gather/push`、`save_particles_at_*`、自定义 attributes | particle container runtime gates | 第 4 章；buffer / scraping 兼接第 8 章 | `particles/11`、`28`、`29` |
| `<species_name>.do_field_ionization`、`physical_element`、`ionization_*` | `InitIonizationModule()` | 第 4 章 | `particles/12-field-ionization-adk-pipeline.md` |
| `<species_name>.do_resampling`、`resampling_*`、`do_temperature_deposition` | particle runtime services | 第 4、5 章 | `particles/23-resampling-thermalizer-and-sorting.md` |
| `<species>.do_qed_*`、virtual photons | `MultiParticleContainer::ReadParameters()` / `InitQED()` | 第 4 章 | `particles/14-17` |

### 5.2 Lasers / Antenna Injection

| 参数族 | 第一次解析位置 | 主要章节 | 先看笔记 |
|---|---|---|---|
| `lasers.names` | `LaserParticleContainer` 构造期 | 第 3A 章 | `laser/00-laser-profile-dispatch.md` |
| `<laser_name>.position`、`direction`、`polarization` | 天线几何构造 | 第 3A 章 | `laser/00`、`01` |
| `<laser_name>.e_max`、`a0`、`wavelength` | 公共 profile 参数 | 第 3A 章 | `laser/00`、`01` |
| `<laser_name>.profile` | profile 工厂分派 | 第 3A 章 | `laser/00-laser-profile-dispatch.md` |
| `<laser_name>.field_function(X,Y,t)` | `FieldFunctionLaserProfile` | 第 3A 章；粒子更新核兼接第 4 章 | `laser/02-field-function-and-particle-update-kernel.md` |
| `<laser_name>.binary_file_name`、`lasy_file_name`、`time_chunk_size`、`delay` | `FromFileLaserProfile` | 第 3A 章 | `laser/01-gaussian-from-file-and-runtime.md` |
| `<laser_name>.profile_*`、`phi0`、`stc_direction`、`zeta/beta/phi2` | `GaussianLaserProfile` | 第 3A 章 | `laser/01-gaussian-from-file-and-runtime.md` |
| `<laser_name>.do_continuous_injection`、`lasers.deposit_on_main_grid` | laser runtime injection / AMR | 第 3A、7 章 | `laser/04-moving-window-external-field-coupling.md` |
| `warpx.num_mirrors`、`mirror_z*` | laser-adjacent in-domain mirror setup | 第 7 章；boosted 边界兼接第 3A 章 | `laser/04-moving-window-external-field-coupling.md` |

### 5.3 Diagnostics / Output / Restart

| 参数族 | 第一次解析位置 | 主要章节 | 先看笔记 |
|---|---|---|---|
| `diagnostics.enable`、`diagnostics.diags_names` | `MultiDiagnostics` | 第 8 章 | `diagnostics/01-diagnostics-dispatch.md` |
| `<diag_name>.intervals`、`dump_last_timestep`、`diag_type`、`format` | `Diagnostics` / `BTDiagnostics` / `BoundaryScrapingDiagnostics` | 第 8 章 | `diagnostics/01`、`06` |
| `<diag_name>.openpmd_*`、`adios2_*`、`sensei_*` | writer backend selection | 第 8 章 | `diagnostics/06-writer-comparison-and-minimal-cases.md` |
| `<diag_name>.fields_to_plot`、`particle_fields_*`、`plot_raw_fields*`、`coarsening_ratio` | full diagnostics field packing | 第 8 章 | `diagnostics/02-field-and-particle-functors.md` |
| `<diag_name>.file_prefix`、`file_min_digits`、`diag_lo/hi` | writer output layout | 第 8 章 | `diagnostics/06`、`07` |
| `<diag_name>.species`、`variables`、`additional_variables`、`random_fraction`、`uniform_stride`、`plot_filter_function(...)` | particle output filter/staging | 第 8 章 | `diagnostics/02`、`08`、`09` |
| `amrex.async_out`、`amrex.async_out_nfiles`、`warpx.field/particle_io_nfiles`、`warpx.mffile_nstreams` | AMReX / writer I/O throttling | 第 8 章 | `diagnostics/06-writer-comparison-and-minimal-cases.md` |
| `<diag_name>.time_average_mode`、`average_*` | time-averaged diagnostics | 第 8 章 | `diagnostics/01`、`05` |
| `<diag_name>.num_snapshots_lab`、`dt/dz_snapshots_lab`、`buffer_size`、`do_back_transformed_*` | back-transformed diagnostics | 第 8 章 | `diagnostics/01`、`06` |
| `warpx.reduced_diags_names`、`reduced_diags.*`、`<reduced_diags_name>.type` | `MultiReducedDiags` / `ReducedDiags` | 第 8 章 | `diagnostics/05-reduced-diagnostic-case-studies.md` |
| `amr.restart`、`warpx.write_diagnostics_on_restart` | checkpoint / restart | 第 8 章 | `diagnostics/06-writer-comparison-and-minimal-cases.md` |

### 5.4 Collisions / QED

| 参数族 | 第一次解析位置 | 主要章节 | 先看笔记 |
|---|---|---|---|
| `collisions.collision_names`、`<collision_name>.type` | `CollisionHandler` | 第 4 章 | `particles/13-collision-handler-stepping-and-regression-map.md` |
| `<collision_name>.species`、`product_species`、`ndt_supercycle/subcycle` | `CollisionBase` / concrete collision classes | 第 4 章 | `particles/13`、`18` |
| pairwise Coulomb：`CoulombLog`、`use_global_debye_length`、energy correction flags | `BinaryCollision` / Coulomb kernels | 第 4 章 | `particles/20-22` |
| DSMC / MCC：`background_*`、`scattering_processes`、cross-section / energy / ionization target | `BackgroundMCC` / DSMC branches | 第 4 章 | `particles/19-backgroundmcc-pulseddecay-and-dsmc-branches.md` |
| `event_multiplier`、`probability_threshold`、`probability_target_value`、fusion / linear BW / Compton specifics | binary-collision event controls | 第 4 章 | `particles/17`、`18`、`20-22` |
| `decay_rate(...)`、`fixed_product_weight`、`productA/B_temperature_eV` | `PulsedDecay` | 第 4 章 | `particles/19-backgroundmcc-pulseddecay-and-dsmc-branches.md` |
| Bremsstrahlung：`Z`、`multiplier`、`create_photons`、`koT1_cut` | bremsstrahlung branch | 第 4 章 | `particles/20`、`21`、`22` |
| `qed_qs.*`、`qed_bw.*`、`qed_schwinger.*`、species QED flags | `InitQED()` / QED wrappers | 第 4 章 | `particles/14-17` |
| `warpx.use_hybrid_QED`、`warpx.quantum_xi` | field-solver side hybrid-QED | 第 6 章 | `fieldsolver/10-implicit-and-hybrid.md` |

#### 5.4.1 Collision / QED 子族导航

1. 调度层与时间门闩：
   - `collisions.collision_names`
   - `<collision_name>.type`
   - `<collision_name>.ndt_subcycle`
   - `<collision_name>.ndt_supercycle`
   先看：
   - [13-collision-handler-stepping-and-regression-map.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/13-collision-handler-stepping-and-regression-map.md)
2. BinaryCollision event table 与 product species：
   - `<collision_name>.species`
   - `<collision_name>.product_species`
   - `event_multiplier`
   - `probability_threshold`
   - `probability_target_value`
   先看：
   - [18-binary-collision-product-creation-and-linear-compton.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/18-binary-collision-product-creation-and-linear-compton.md)
   - [22-perez-bremsstrahlungevent-and-fusion-probability-control.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/22-perez-bremsstrahlungevent-and-fusion-probability-control.md)
3. MCC / DSMC / decay 子族：
   - `background_*`
   - `scattering_processes`
   - `decay_rate(...)`
   - `fixed_product_weight`
   先看：
   - [19-backgroundmcc-pulseddecay-and-dsmc-branches.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/19-backgroundmcc-pulseddecay-and-dsmc-branches.md)
4. 强场 QED 子族：
   - `<species_name>.do_qed_quantum_sync`
   - `<species_name>.do_qed_breit_wheeler`
   - `qed_qs.*`
   - `qed_bw.*`
   - `qed_schwinger.*`
   先看：
   - [14-qed-entrypoints.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/14-qed-entrypoints.md)
   - [15-qed-kernels-and-wrapper-contracts.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/15-qed-kernels-and-wrapper-contracts.md)
   - [16-qed-table-generation-and-serialization.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/16-qed-table-generation-and-serialization.md)
5. collision-side QED / virtual photons 子族：
   - `linear_breit_wheeler`
   - `linear_compton`
   - virtual photon helper species
   先看：
   - [17-qed-chi-virtual-photons-and-linear-breit-wheeler.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/17-qed-chi-virtual-photons-and-linear-breit-wheeler.md)

### 5.5 Boundary / Solver / PSATD / Implicit

| 参数族 | 第一次解析位置 | 主要章节 | 先看笔记 |
|---|---|---|---|
| `boundary.field_*`、`boundary.particle_*`、`boundary.reflect_all_velocities` | `WarpX.cpp` + `FieldBoundaries.cpp` | 第 7 章；粒子行为兼接第 4 章 | `boundary/00-04`、`particles/11` |
| `boundary.potential_*`、`warpx.eb_potential(x,y,z,t)` | `PoissonBoundaryHandler` | 第 7 章；静电求解兼接第 6 章 | `utils/06`、`utils/07`、`initialization/18-19` |
| `warpx.pml_*`、`do_similar_dm_pml`、`do_pml_div*cleaning` | `WarpX.cpp` / PML init | 第 7 章 | `boundary/01`、`fieldsolver/02-03` |
| `warpx.do_electrostatic`、`warpx.poisson_solver`、`self_fields_*`、`magnetostatic_solver_*` | `WarpX.cpp` / electrostatic solver construction | 第 3A、6 章 | `fieldsolver/09-electrostatic-magnetostatic.md`、`initialization/10-13` |
| `warpx.cfl`、`const_dt`、`max_dt`、`dt_update_interval`、`compute_max_step_from_btd` | `WarpX.cpp` / `ComputeDt()` | 第 3 章；BTD 联动兼接第 8 章 | `evolve/04-compute-dt-and-adaptive-timestep.md`、`diagnostics/06` |
| `warpx.use_filter`、`use_kspace_filter`、`num_filter_passes` | `WarpX.cpp` / filter setup | 第 5、7 章 | `fieldsolver/03`、`parallelization/00` |
| `psatd.*`、`warpx.n_rz_azimuthal_modes`、`warpx.grid_type`、`interpolation.galerkin_scheme` | `WarpX.cpp` / PSATD solver block | 第 4、6 章 | `fieldsolver/05-08`、`particles/25` |
| `implicit_evolve.*`、`algo.evolve_scheme=implicit` | `WarpX.cpp` + `ThetaImplicitEM.cpp` | 第 3、6 章 | `fieldsolver/10`、`nonlinear-solvers/00-06`、`particles/09-10` |

补充边界：

- 如果参数在文档里是 grouped alias，但本地源码总搜不到同名 key，先看：
  - [08-low-frequency-parameter-families-and-pass-throughs.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/08-low-frequency-parameter-families-and-pass-throughs.md)
- 这一层专门处理：
  - `geometry.prob_lo/hi`
  - `boundary.field_lo/hi`
  - `boundary.potential_lo/hi_x/y/z`
  - `psatd.nox/noy/noz`
  - `qed_schwinger.xmin/.../zmax`
  - 以及 `amr.ref_ratio`、`amrex.async_out` 这类 AMReX-owned pass-through 输入

#### 5.5.1 Boundary / Solver 子族导航

1. boundary / PML：
   - `boundary.field_*`
   - `boundary.particle_*`
   - `warpx.pml_*`
   - `warpx.pml_has_particles`
   先看：
   - [00-field-boundary-parameters.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/boundary/00-field-boundary-parameters.md)
   - [01-pml-data-and-update.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/boundary/01-pml-data-and-update.md)
   - [11-particle-boundaries-buffer-sorting.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/11-particle-boundaries-buffer-sorting.md)
2. electrostatic / Poisson / boundary potentials：
   - `warpx.do_electrostatic`
   - `warpx.poisson_solver`
   - `boundary.potential_*`
   - `warpx.eb_potential(...)`
   先看：
   - [09-electrostatic-magnetostatic.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/fieldsolver/09-electrostatic-magnetostatic.md)
   - [06-external-vector-potential-and-poisson-boundary-parameters.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/06-external-vector-potential-and-poisson-boundary-parameters.md)
   - [07-parameter-validation-links-for-boundary-and-external-fields.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/07-parameter-validation-links-for-boundary-and-external-fields.md)
3. timestep / filter：
   - `warpx.cfl`
   - `warpx.const_dt`
   - `warpx.max_dt`
   - `warpx.dt_update_interval`
   - `warpx.use_filter`
   先看：
   - [04-compute-dt-and-adaptive-timestep.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/evolve/04-compute-dt-and-adaptive-timestep.md)
   - `filter/README.md`
4. PSATD / grid / gather coupling：
   - `psatd.*`
   - `warpx.grid_type`
   - `interpolation.galerkin_scheme`
   先看：
   - [05-psatd-spectral-flow.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/fieldsolver/05-psatd-spectral-flow.md)
   - [06-psatd-galilean-current-correction.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/fieldsolver/06-psatd-galilean-current-correction.md)
   - [25-gather-variants-and-external-particle-fields.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/25-gather-variants-and-external-particle-fields.md)

### 5.6 Deep Solver Objects / Subobjects

| 参数族 | 第一次解析位置 | 主要章节 | 先看笔记 |
|---|---|---|---|
| `fluids.species_names`、`<fluid_name>.*` | `WarpX.cpp` + `MultiFluidContainer` | 第 3A、6 章 | `utils/05-deep-solver-object-parameter-families.md` |
| `hybrid_pic_model.*`、`external_vector_potential.*` | `HybridPICModel` / `ExternalVectorPotential` | 第 6 章 | `fieldsolver/12`、`utils/05`、`utils/06`、`utils/07` |
| `macroscopic.*` | `MacroscopicProperties` | 第 6 章 | `utils/05-deep-solver-object-parameter-families.md` |
| `warpx.effective_potential_*` | `EffectivePotentialES::ComputeSigma()` | 第 3A、6 章 | `utils/05`、`utils/07`、`initialization/18` |

#### 5.6.1 Deep Solver 子族导航

1. fluids：
   - `fluids.species_names`
   - `<fluid_name>.charge/mass`
   - fluid closure / initialization 参数
   先看：
   - [05-deep-solver-object-parameter-families.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/05-deep-solver-object-parameter-families.md)
2. hybrid + external vector potential：
   - `algo.maxwell_solver = hybrid`
   - `hybrid_pic_model.add_external_fields`
   - `external_vector_potential.fields`
   - `<field_name>.A*_external_grid_function(...)`
   先看：
   - [12-hybrid-pic-model-deep-dive.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/fieldsolver/12-hybrid-pic-model-deep-dive.md)
   - [06-external-vector-potential-and-poisson-boundary-parameters.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/06-external-vector-potential-and-poisson-boundary-parameters.md)
3. macroscopic medium：
   - `algo.em_solver_medium = macroscopic`
   - `macroscopic.sigma/epsilon/mu`
   - `*_function(x,y,z)`
   先看：
   - [05-deep-solver-object-parameter-families.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/05-deep-solver-object-parameter-families.md)
4. effective potential：
   - `warpx.do_electrostatic = labframe-effective-potential`
   - `warpx.effective_potential_factor`
   - `warpx.effective_potential_time_filter`
   - `warpx.effective_potential_density_floor`
   先看：
   - [05-deep-solver-object-parameter-families.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/05-deep-solver-object-parameter-families.md)
   - [18-initialization-validation-map-dirichlet-and-effective-potential.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/initialization/18-initialization-validation-map-dirichlet-and-effective-potential.md)

## 6. 当前最应该优先人工纠正的 `parameter-map` 区域

优先级最高的不是所有 352 个条目一起改，而是先纠正这些最容易误导读者的高频入口：

1. 无前缀运行控制：
   - `max_step`
   - `stop_time`
2. startup / AMReX 契约：
   - `amrex.abort_on_out_of_gpu_memory`
   - `amrex.the_arena_is_managed`
   - `amrex.omp_threads`
3. `WarpX.cpp::ReadParameters()` 主分派：
   - `algo.evolve_scheme`
   - `warpx.do_electrostatic`
   - `warpx.poisson_solver`
   - `warpx.cfl`
   - `warpx.const_dt`
4. diagnostics 元数据：
   - `authors`
5. 前三批已清理的高频族：
   - 无前缀运行控制和 startup debug 参数
   - `algo.*` 主算法入口
   - `diagnostics.*` / `reduced_diags.*`
   - `boundary/PML/EB`、`collisions/QED`、`psatd.*`

## 7. 当前阶段性边界

本文件还不是“全部 352 个参数逐项落章”的最终版。

它当前完成的是：

- 给 `parameter-map.md` 提供第一层人工章节语义；
- 把最上游高频参数从 `待定` 或旧计划编号里拉回当前书稿结构；
- 为后续按 `species / lasers / diagnostics / collisions` 继续展开提供稳定骨架；
- 并已通过 [utils/02-parameter-family-entrypoints.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/02-parameter-family-entrypoints.md) 把 `species / laser / diagnostics / reduced diagnostics / collision / boundary / solver / psatd / implicit` 这几组参数的 `global gate / factory dispatch / instance-local parse` 入口接回真实源码。
- 对更深的 solver-object 参数，又已通过 [utils/05-deep-solver-object-parameter-families.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/05-deep-solver-object-parameter-families.md) 把 `fluids / hybrid_pic_model / macroscopic / effective potential` 这四组参数继续拆到 `object creation / instance-local parse / runtime materialization`。
- 对更细的边界/子对象 parser 参数，又已通过 [utils/06-external-vector-potential-and-poisson-boundary-parameters.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/06-external-vector-potential-and-poisson-boundary-parameters.md) 把 `external_vector_potential.*`、`boundary.potential_*` 和 `warpx.eb_potential(x,y,z,t)` 继续拆到 `parent gate / subobject parse / parser build / runtime apply`。
- 对这些边界/子对象参数的 example-level 闭环，又已通过 [utils/07-parameter-validation-links-for-boundary-and-external-fields.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/07-parameter-validation-links-for-boundary-and-external-fields.md) 接到 `electrostatic_dirichlet_bc`、`open_bc_poisson_solver`、`effective_potential_electrostatic` 和 `ion_beam_extraction` 四条最稳定 validation 链。

下一步自然动作：

1. 继续人工修正 `parameter-map.md` 中剩余仍保留旧计划编号的尾项，优先清理：
   `load_balance` 零散项、个别 `species/laser` 残留、以及仍未逐项回填的辅助 writer 参数；
2. 在现有对象前缀导航基础上，继续把 `species`、`laser`、`diagnostics`、`collision` 细化成更稳定的子族索引，并补 `boundary / solver / psatd / implicit`、`hybrid / macroscopic / effective potential / fluids`、`external_vector_potential / Poisson boundary` 的子族导航；
3. 最后把参数索引与书稿正文里的参数表做双向链接，减少“参数在 map 里已校正，但章节正文仍未显式表格化”的脱节。
