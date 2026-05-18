# 3A. WarpX 初始化链：从 `InitData()` 到初始粒子和外部场

本章把 `WarpX::InitData()` 展开成一条完整的初始化链。它补足第 3 章中“初始化”只作为主循环前置步骤的不足：这里开始逐块解释 fresh run / restart、AMR level 初始化、外部场、species 注入器、粒子创建 kernel、Gaussian beam、openPMD 文件注入和 projection divergence cleaning。

本章绑定本地源码 `../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。详细源码笔记见：

- `notes/code-reading/initialization/08-initialization-bootstrap.md`
- `notes/code-reading/initialization/09-preconstruct-parameter-locking.md`
- `notes/code-reading/initialization/10-readparameters-runtime-landing.md`
- `notes/code-reading/initialization/11-readparameters-combination-constraints.md`
- `notes/code-reading/initialization/12-alloclevelmfs-specialized-branches.md`
- `notes/code-reading/initialization/13-initdata-postallocation-consumption.md`
- `notes/code-reading/initialization/14-initialization-validation-map.md`
- `notes/code-reading/initialization/15-initialization-validation-map-external-relativistic-openbc.md`
- `notes/code-reading/initialization/16-initialization-validation-map-density-magnetostatic-nodal.md`
- `notes/code-reading/initialization/00-init-callgraph.md`
- `notes/code-reading/initialization/01-external-fields.md`
- `notes/code-reading/initialization/02-plasma-injector.md`
- `notes/code-reading/initialization/03-density-momentum-dispatch.md`
- `notes/code-reading/initialization/04-particle-creation-kernels.md`
- `notes/code-reading/initialization/05-projection-div-cleaner.md`
- `notes/code-reading/initialization/06-gaussian-beam-openpmd-injection.md`

## 3A.1 初始化链为什么值得单独成章

PIC 程序的时间推进方程通常写成：

$$
f^n,\mathbf{E}^n,\mathbf{B}^n
\longrightarrow
f^{n+1},\mathbf{E}^{n+1},\mathbf{B}^{n+1}.
$$

但第一个时间步之前必须先构造一个满足几何、边界、粒子权重、外部场、离散约束和并行布局的初态。WarpX 的初始化不是“读入参数然后开始跑”，而是完成以下任务：

1. 选择 fresh run 或 checkpoint restart。
2. 建立 AMReX level、field MultiFab、PML、EB 和 solver 数据结构。
3. 初始化 diagnostics 和 reduced diagnostics。
4. 创建 species、解析密度/动量/位置分布，并生成宏粒子。
5. 读入或解析外部场，并把外部场叠加到 self field 或 particle external field。
6. 对外部 `A/B` 场做 projection divergence cleaning。
7. 输出第 0 步 diagnostics，并检查 guard cell、solver 配置和 known issue。

这一章先给出正式书稿版的主干，后续章节会继续把每个子函数扩成更细的逐行讲解。

## 3A.2 启动层先于 `InitData()`：MPI、AMReX、FFT、PETSc 与运行时契约

前面的初始化笔记大多从 `WarpX::InitData()` 往后讲，但 WarpX 真正的初始化链更早就开始了。`main.cpp` 最外层先做的是：

```cpp
int
main (int argc, char* argv[]) {
    warpx::initialization::initialize_external_libraries(argc, argv);
    {
        auto& warpx = WarpX::GetInstance();
        warpx.InitData();
        warpx.Evolve();
        WarpX::Finalize();
    }
    warpx::initialization::finalize_external_libraries();
}
```

这说明 `InitData()` 之前还有一层独立的 bootstrap 逻辑，负责：

1. 初始化 MPI、AMReX、FFT，以及可选 PETSc。
2. 覆盖一批 AMReX 默认 parser 行为。
3. 解析 geometry、periodicity 和整数数组表达式。
4. 锁定 `geometry.dims`、moving window 和 warning policy 这类全局运行时契约。

这一层主要分布在：

- `Initialization/WarpXAMReXInit.*`
- `Initialization/WarpXInit.*`
- `WarpX::MakeWarpX()`

### 3A.2.1 参数系统先分命名空间，再分读取语义

WarpX 的参数不是“一个大表一次性读完”。它先按 `ParmParse` 前缀拆成局部命名空间，然后再决定是：

- 立即求值成数值；
- 保留 parser 字符串，稍后编译；
- 解释成 interval 切片；
- 还是先解析成枚举型算法选择。

最上游的运行控制参数就是无前缀直接读取：

```cpp
const ParmParse pp;// Traditionally, max_step and stop_time do not have prefix.
utils::parser::queryWithParser(pp, "max_step", max_step);
utils::parser::queryWithParser(pp, "stop_time", stop_time);
```

而大部分初始化参数则先按前缀取视图：

```cpp
const ParmParse pp_amr("amr");
const ParmParse pp_algo("algo");
ParmParse const pp_warpx("warpx");
const ParmParse pp_geometry("geometry");
const ParmParse pp_boundary("boundary");
const ParmParse pp_psatd("psatd");
```

接下来又会分成几种读取壳：

1. `queryWithParser/queryArrWithParser`
   - 适合 `warpx.cfl`、`const_dt`、`amr.n_cell` 这类“读入就该变成数值”的参数；
2. `Store_parserString + makeParser`
   - 适合 `ref_patch_function(x,y,z)`、外场 parser、diagnostics 过滤函数这类“先保留表达式，再在别处编译执行”的参数；
3. `IntervalsParser`
   - 适合 `sort_intervals`、`dt_update_interval`、diagnostics `intervals` 这类切片语法，不应误看成普通整数；
4. `query_enum_sloppy + AMREX_ENUM`
   - 适合 `algo.evolve_scheme`、`warpx.do_electrostatic`、`algo.current_deposition` 这类算法枚举入口。

这层结构解释了为什么同样都出现在 `parameters.rst` 里，`max_step`、`ref_patch_function(x,y,z)` 和 `algo.evolve_scheme` 在源码中会走三种完全不同的消费链。后续参数索引如果想真正有用，就必须至少区分：

- 参数前缀；
- 第一次被哪个 `ParmParse` 命名空间读取；
- 它属于数值参数、parser 字符串、interval 还是枚举型算法选择。

例如 `WarpXAMReXInit.cpp` 并不是简单调用 `amrex::Initialize()`，而是把一个缺省值覆盖回调一起传进去：

```cpp
amrex::Initialize(
    argc,
    argv,
    build_parm_parse,
    MPI_COMM_WORLD,
    ::overwrite_amrex_parser_defaults
);
```

这个回调会统一注入常量、改写 `amrex.abort_on_out_of_gpu_memory`、`amrex.the_arena_is_managed`、`amrex.omp_threads`、粒子 tiling 缺省值，以及由 `boundary.field_*` / `boundary.particle_*` 反推 `geometry.is_periodic`。换句话说，WarpX 从程序一启动就已经不是“AMReX 原生默认设置”。

同一个文件还会在 AMReX 初始化后立即把 `geometry.prob_lo/prob_hi`、`amr.n_cell`、`max_grid_size*`、`blocking_factor*` 这类可能带表达式的输入预解析并写回 parser，保证后面的 `Geometry`、`warpx_job_info` 和 `yt` 读到的是数值结果，而不是未展开的表达式字符串。

### 3A.2.2 文档 alias、AMReX-owned 参数与 WarpX 本地 parser 不是一回事

参数索引继续往下清理后，会发现还有一类参数不能简单用“有没有 grep 到同名字符串”来理解。典型例子是：

- `geometry.prob_lo/hi`
- `boundary.field_lo/hi`
- `boundary.potential_lo/hi_x/y/z`
- `psatd.nox/noy/noz`
- `qed_schwinger.xmin/ymin/zmin/xmax/ymax/zmax`

这些名字在文档里是 grouped alias，但源码里真实读取的仍然是拆开的 key。以 `geometry.prob_lo/hi` 为例，WarpX 真正做的是：

```cpp
utils::parser::getArrWithParser(
    pp_geometry, "prob_lo", prob_lo, 0, AMREX_SPACEDIM);
utils::parser::getArrWithParser(
    pp_geometry, "prob_hi", prob_hi, 0, AMREX_SPACEDIM);

pp_geometry.addarr("prob_lo", prob_lo);
pp_geometry.addarr("prob_hi", prob_hi);
```

所以 `geometry.prob_lo/hi` 只是文档层“成对参数”的写法，真正 parser key 仍然是 `prob_lo` 和 `prob_hi`。`boundary.field_lo/hi`、`boundary.particle_lo/hi`、`boundary.potential_lo/hi_x/y/z`、`psatd.nox/noy/noz` 和 Schwinger 区域边界框也都属于这一类。

还要再区分另一类：参数确实出现在 WarpX 手册里，但本地 WarpX 并不直接读取，而是由 AMReX 自己消费，WarpX 只消费结果。例如 `amr.ref_ratio` / `amr.ref_ratio_vect` 和 `amrex.async_out` / `amrex.async_out_nfiles`。当前本地 WarpX 源码没有独立的：

```cpp
ParmParse("amr").query("ref_ratio", ...)
ParmParse("amrex").query("async_out", ...)
```

但后续代码会直接消费已经构造好的 `ref_ratios`，或者在 plotfile I/O 邻近层继续设置 WarpX 自己的 `field_io_nfiles` / `particle_io_nfiles`。因此，参数索引如果要稳定，至少要区分三类：

1. WarpX 本地直接 parse；
2. WarpX 子对象 parse；
3. AMReX-owned 输入，WarpX 只消费 materialized 结果。

另一条关键链在 `WarpX::MakeWarpX()`：

```cpp
warpx::initialization::check_dims();
warpx::initialization::read_moving_window_parameters(...);
ConvertLabParamsToBoost();
parse_field_boundaries();
parse_particle_boundaries(...);
CheckGriddingForRZSpectral();
m_instance = new WarpX();
```

因此单例构造前就已经锁定了四类全局事实：

- 当前可执行文件与 `geometry.dims` 是否匹配；
- moving window 是否开启、方向和速度是什么；
- field / particle boundary 类型是什么；
- RZ spectral 的 gridding 约束是否满足。

例如 `check_dims()` 直接把编译维度和 `geometry.dims` 做强一致断言，而 `read_moving_window_parameters()` 会把输入文件里的 `moving_window_v` 从“以光速为单位的无量纲参数”转换成真正的物理速度 `v = (\cdots)c`，再写进 `WarpX` 的全局静态状态。

这里还要补一层工程来源。`check_dims()` 能做这种强断言，前提不是“WarpX 在运行时随意切换几何”，而是构建系统已经先把几何变体锁死了。当前主构建链在顶层 `CMakeLists.txt` 中通过 `WarpX_DIMS` 生成一组按维度后缀分裂的 `lib_${SD}` / `pyWarpX_${SD}` target；旧 GNUmake 链则通过 `DIM`、`USE_RZ` 以及 `-DWARPX_DIM_3D`、`-DWARPX_DIM_XZ`、`-DWARPX_DIM_RZ` 这组宏编码几何变体。因此初始化阶段读到的 `geometry.dims` 实际是在和“当前可执行文件已经按哪一种几何编译出来”做一致性检查，而不是在决定后面要不要临时切换到另一种维度。

再往下，`WarpX` 构造函数开头还会调用：

```cpp
warpx::initialization::initialize_warning_manager();
```

也就是在任何 `ReadParameters()` 和 `InitData()` 之前，先读入：

- `warpx.always_warn_immediately`
- `warpx.abort_on_warning_threshold`

这说明 warning manager 在 WarpX 里也是初始化启动层的一部分，而不是后面运行时再临时决定的日志选项。

这一层再往下细分，还要注意 `MakeWarpX()` 和构造期 `ReadParameters()` 之间并不是简单前后顺序，而是“前者已经开始改写后者将要读取的参数”。例如 `ConvertLabParamsToBoost()` 不只是保存 `gamma_boost`，而是会先把：

- `geometry.prob_lo/prob_hi`
- `warpx.fine_tag_lo/fine_tag_hi`
- `slice.dom_lo/dom_hi`

按 boosted-frame 规则直接回写进 parser。若同时启用 moving window，它计算的转换系数还会显式依赖 `moving_window_v/c`。因此 boosted-frame 与 moving-window 的第一次耦合，其实发生在 `ReadParameters()` 之前，而不是发生在后面的 `Evolve()`。

同样，`CheckGriddingForRZSpectral()` 也不是单纯做断言。对 `WARPX_DIM_RZ + algo.maxwell_solver = psatd` 这条组合，它会在构造 `WarpX` 对象之前直接改写：

- `amr.blocking_factor_x/y`
- `amr.max_grid_size_x/y`

并要求 longitudinal 方向至少满足“每个 MPI rank 至少有一个 block，且每个 rank 至少有 8 个 z cells”的约束。也就是说，构造函数里的 `ReadParameters()` 读到的并不总是用户输入文件里的原始 AMR 分块值，而往往已经是启动层重写过的 spectral-compatible 版本。

把这一点看清之后，初始化启动层就能更准确地拆成两段：

1. 预初始化与 parser 改写段：
   - `initialize_external_libraries()`
   - `amrex_init()`
   - `parse_geometry_input()`
   - `read_moving_window_parameters()`
   - `ConvertLabParamsToBoost()`
   - `CheckGriddingForRZSpectral()`
2. 构造与运行态落地段：
   - `initialize_warning_manager()`
   - `ReadParameters()`
   - `BackwardCompatibility()`
   - `InitEB()`
   - `MultiParticleContainer` / `ParticleBoundaryBuffer` / solver objects` 的真正创建

这个分层很有用，因为后面再读 boosted-frame 例子、RZ spectral gridding、moving window 连续注入或 warning manager，就不会再把“参数在哪一步被锁定”与“对象在哪一步消费这些参数”混在一起。

再往前走一步，`ReadParameters()` 还不只是“把输入存进成员”。它已经在替后面的对象图做分叉。例如：

- `do_fluid_species` 先通过 `fluids.species_names` 决定，随后直接控制是否创建 `MultiFluidContainer`；
- `electrostatic_solver_id` 与 `electromagnetic_solver_id` 先在 `ReadParameters()` 中互相覆盖和约束，随后决定静电 solver 具体实例化成 `LabFrameExplicitES`、`EffectivePotentialES` 还是 `RelativisticExplicitES`；
- `electromagnetic_solver_id == HybridPIC` 时，构造函数后半段才真正创建 `HybridPICModel`；
- `grid_type`、`do_current_centering`、`n_rz_azimuthal_modes` 等参数先在 `ReadParameters()` 中完成默认值推导和合法组合检查，后面再影响 nodal flags、centering coefficients、fluid 兼容性与容器初始化。

同样，`ReadParameters()` 里还有一类“源码先推导默认，再由用户输入覆盖”的派生状态。最典型的是：

```cpp
if (!do_divb_cleaning
    && m_p_ext_field_params->B_ext_grid_type != ExternalFieldType::default_zero
    && m_p_ext_field_params->B_ext_grid_type != ExternalFieldType::constant
    ...
    && (electromagnetic_solver_id == Yee
        || electromagnetic_solver_id == HybridPIC
        || ...))
{
    m_do_initial_div_cleaning = true;
}
pp_warpx.query("do_initial_div_cleaning", m_do_initial_div_cleaning);
```

这里 `do_initial_div_cleaning` 不是单纯从输入文件机械读取，而是先根据外部场类型、grid type 和 solver 组合推导一个默认值，再允许用户显式覆盖。也就是说，后面 `ProjectionDivCleaner` 是否参与初态构造，不是孤立地由一个布尔开关决定，而是由初始化启动层和 `ReadParameters()` 主体共同塑造的。

到这一层为止，初始化阶段已经可以更清楚地压成一条完整链：

1. 启动层先改 parser、锁定全局静态状态。
2. `ReadParameters()` 再把这些值落到 `WarpX` 成员，并决定对象图分叉。
3. 构造函数后半段据此创建 `MultiParticleContainer`、`ParticleBoundaryBuffer`、`MultiFluidContainer` 和 solver objects。
4. 最后 `InitData()` 才真正开始分配 level data、生成粒子和构造初态。

但这里还差最后一层经常被误读的东西：`ReadParameters()` 里那些看上去分散的算法检查，其实会继续决定后面到底分配哪类 `MultiFab`、是否创建 implicit solver 额外状态，以及 `ProjectionDivCleaner` 是否在初态构造中插队。

最紧的一组约束是：

- `grid_type=hybrid` 会把 `do_current_centering` 推成默认真值，并要求 `algo.field_gathering=momentum-conserving`；
- 这又会让 `AllocLevelData()` 中的 `aux_is_nodal=true`，从而把 `Efield_aux/Bfield_aux`、后续 coarse-aux `cax` 和 gather buffer 路径切到 nodal 版本；
- 如果同时显式要求 `do_current_centering=1`，源码只允许 `grid_type=hybrid`，并且在 level 分配时额外分配 `current_fp_nodal`。

换句话说，`grid_type`、`field_gathering_algo`、`do_current_centering` 在这里并不是三个平行开关，而是一组会继续改写场 index type 和附加存储布局的上游选择器。

同样，`current_deposition_algo` 也不是只影响某个沉积 kernel。源码先把 `PSATD`、`HybridPIC` 和 electrostatic 的默认 deposition 拉回 `Direct`，再对 `Vay` 加上三重限制：

- 只能配 `PSATD`
- 不能配 mesh refinement
- 不能配 `do_current_centering`

这条限制后面会直接落成额外字段分配：如果真的选了 `Vay`，`AllocLevelMFs()` 会专门分配 `current_fp_vay`。所以它已经是初始化对象图的一部分，而不只是运行时算法分派。

implicit 系列更明显。`ReadParameters()` 一旦看到

- `semi_implicit_em`
- `theta_implicit_em`
- `strang_implicit_spectral_em`

就会立即构造 `m_implicit_solver`，并同时要求：

- current deposition 只能是 `Esirkepov` / `Villasenor` / `Direct`
- EM solver 只能是 `Yee` / `CKC` / `PSATD`
- particle pusher 只能是 `Boris` / `HigueraCary`
- field gather 不能是 momentum-conserving

然后这条链会继续穿到 `InitFromScratch()` 和 `AllocLevelMFs()`：

- `InitFromScratch()` 在 `mypc->InitData()` 之前调用 `m_implicit_solver->Define()` 和 `CreateParticleAttributes()`；
- `AllocLevelMFs()` 在 fine patch 上额外分配 `current_fp_non_suborbit` 与 `E_old`。

因此 implicit 不是“场求解器章节内部的一个局部话题”，而是在初始化阶段就已经改变粒子属性表和字段分配合同。

`particle_shape`、filter 和 projection div cleaning 也属于同一种“前置组合约束”。只要存在 particles 或 lasers，`algo.particle_shape` 就变成强制参数，并直接设定 `nox=noy=noz`；这反过来继续影响 guard-cell 配额、沉积 stencil 和排序默认值。`use_filter` 也不是后面可有可无的一步卷积，因为 `AllocLevelData()` 会先 `InitFilter()`，再把 filter stencil 长度交给 `guard_cells.Init(...)`，于是它会继续改写 guard-cell 和 buffer 需求。

最后，`m_do_initial_div_cleaning` 也不是孤立的布尔开关。源码先根据外部 `B` 场类型、EM solver 组合和是否已经启用 `do_divb_cleaning` 推导默认值，再允许用户覆盖；而它的下游消费点就在初始化主链里，直接决定 `ProjectionDivCleaner` 是否参与初始场构造。所以到这一步为止，`ReadParameters()` 的真实地位可以概括成一句话：

它不是单纯读参数，而是在 `AllocLevelData()` 和 `InitFromScratch()` 之前，先把“允许哪种物理-算法-存储组合存在”这件事裁成一个可执行的对象图。

接下来再往下走一步，就会看到 `AllocLevelMFs()` 真正把这张对象图摊成一组具体字段。这里最容易误判的是 `rho`、aux、外场、HybridPIC/fluid/macroscopic/EB 这些分支。

先看 `rho_fp`。它并不是总存在的基础字段，而是只在几类路径下显式分配：

- electrostatic / electromagnetostatic / effective-potential
- `HybridPIC`
- `do_dive_cleaning`
- PSATD 且启用了 `update_with_rho` 或 `current_correction`

而且它的分量数也不是固定值：普通 electrostatic 或 `HybridPIC` 只需要 `ncomps`，`do_dive_cleaning` 一般把它升到 `2*ncomps`，PSATD 又会根据 `JRhom` 是否开启在 `ncomps` 和 `2*ncomps` 之间切换。也就是说，WarpX 初始化阶段持不持有一份“可演化的 rho 状态”，本身就是 solver contract 的一部分。

与此平行的还有三类不同的辅助标量/约束场：

- `phi_fp`：只属于 electrostatic 系列；
- `F_fp`：只属于 `div(E)` cleaning；
- `G_fp`：只属于 `div(B)` cleaning。

不要把它们混成“又分配了几个标量场”。它们分别服务于 Poisson 势解、电场散度清理和磁场散度清理，而且 `G` 的 coarse-patch index type 还会继续受 `grid_type` 控制。

再看外场分支。源码实际上维护了两套完全不同的合同：

1. grid external fields  
   它们分配成 `Efield_fp_external/Bfield_fp_external`，index type 必须匹配 `fp`，后面由 `AddExternalFields()` 加到主网格场上。
2. particle external fields  
   它们分配成 `E_external_particle_field/B_external_particle_field`，index type 必须匹配 `aux`，而且分量数直接来自外部粒子场元数据。

所以 particle external field 不是 grid external field 的别名；它跟粒子 gather 所看的 `aux` 路径绑定得更紧。这也解释了为什么只要 `mypc->m_E_ext_particle_s` 或 `m_B_ext_particle_s` 是 `read_from_file`，最常见的 `aux -> fp` alias 优化就会被打断，`Efield_aux/Bfield_aux` 必须改成单独分配。

剩下几条看似“模块化”的分支，其实也都在 `AllocLevelMFs()` 里继续扩展 field registry：

- `electromagnetic_solver_id == HybridPIC` 时，`m_hybrid_pic_model->AllocateLevelMFs(...)` 会追加 hybrid 自己的 level 字段；
- `do_fluid_species` 时，`myfl->AllocateLevelMFs(...)` 之后立刻 `InitData(...)`，说明 fluid 已经进入初始化主链，而不是仅仅挂了个容器；
- `m_em_solver_medium == Macroscopic` 时，`m_macroscopic_properties->AllocateLevelMFs(...)` 只允许 `lev==0`，直接把 mesh refinement 排除在外；
- `EB::enabled()` 时，所有 level 至少都会有 `distance_to_eb` 与 `m_eb_reduce_particle_shape`，而 finest level 上又会继续长出 `m_eb_update_E/B`；如果 solver 还是 `ECT`，则再额外长出 `edge_lengths`、`face_areas`、`area_mod`、`Venl`、`ECTRhofield` 和 `FaceInfoBox` 借用关系。

因此 `AllocLevelMFs()` 的真实角色不是“机械把 `MultiFab` 开出来”，而是把前面 `ReadParameters()` 裁出来的对象图真正展开成可执行状态。

更关键的是，这些特例字段不会等到 `Evolve()` 才第一次使用。在 `InitData()` 后半段，源码会立刻：

- `BuildBufferMasks()`
- `m_macroscopic_properties->InitData(...)`
- `m_electrostatic_solver->InitData()`
- `m_hybrid_pic_model->InitData(m_fields)`
- `ProjectionCleanDivB()`

这就说明初始化链的最后三步其实是：

1. `ReadParameters()` 决定哪些组合允许存在；
2. `AllocLevelMFs()` 把这些组合摊成真实字段和对象；
3. `InitData()` 后半段立刻消费这些字段，把它们变成一份可跑的初态。

再往后一步，`InitData()` 后半真正把这条合同闭合掉。它的顺序不是“初始化完就直接写 diagnostics”，而是先做一轮收尾和首次消费：

- `ComputeMaxStep()`
- `ComputePMLFactors()`
- 可选 `InitNCICorrector()`
- `BuildBufferMasks()`
- `m_macroscopic_properties->InitData(...)`
- `m_electrostatic_solver->InitData()`
- `m_hybrid_pic_model->InitData(m_fields)`
- `CheckGuardCells()`
- `ProjectionCleanDivB()`

这一步说明前面 `AllocLevelMFs()` 分配出来的对象并不是先放着，很多都会在这里立刻进入第一次初始化消费。

尤其要区分两步经常被混在一起的电场初始化动作：

1. `m_electrostatic_solver->InitData()`  
   这是 solver 对象自身的初始化，fresh run 和 restart 都会走。
2. `ComputeSpaceChargeField(reset_fields=false)`  
   这是 fresh-run 下的初始 self-field / electrostatic solve，只在需要时触发，而且还明确保留网格上已有的用户指定值，不会先把字段清空。

它的触发条件也不是“只有 electrostatic solver 才会跑”，而是三选一：

- 开启 electrostatic solver
- 任意 species 打开 `initialize_self_fields`
- 指定了 boundary potential

但如果当前走的是 `HybridPIC`，源码又会显式跳过这条初始 field-solve 路径。

在这之前，若 `m_do_initial_div_cleaning` 成立，还会先执行 `ProjectionCleanDivB()`。因此初始 `B` 场的散度修正顺序其实非常明确：先完成外场读入与对象初始化，再做 `div B` cleaning，随后才进入初始 self-field / electrostatic solve。

Python callback 也不是一个统一“初始化结束后调用”的事件，而是被拆成了三类窗口：

- `beforeInitEsolve`：只在 fresh run，发生在初始场求解前；
- `afterInitEsolve`：只在 fresh run，发生在初始场求解后、外加场提交前；
- `afterInitatRestart`：只在 restart，表示恢复态后处理，而不是 fresh-run 初始求解窗口的一部分。

外加场这里也有两步，不能混读：

1. `LoadExternalFields()`  
   先把 external grid fields 装到 `Efield_fp_external/Bfield_fp_external`，把 particle-only external fields 装到 `E_external_particle_field/B_external_particle_field`，并在 finest level 给 Python `loadExternalFields` callback 一个写这些 buffer 的机会。
2. `AddExternalFields()`  
   再把 grid external fields 统一加回 `Efield_fp/Bfield_fp` 主场。

所以第 0 步最终主场不是“纯 self-field 结果”，而是“初始 self-field / electrostatic solve 结果，再叠加 grid external fields”。

这之后才进入第 0 步 diagnostics：

- `multi_diags->FilterComputePackFlush(istep[0]-1)`
- `reduced_diags->ComputeDiags(...)`
- `reduced_diags->WriteToFile(...)`

因此第 0 步输出的并不是“原始输入快照”，而是“初始化主链已经全部完成后的第一份可运行状态快照”。对于 restart，这一步则取决于 `write_diagnostics_on_restart`，表示是否要把恢复态也立刻写成一份 diagnostics。

## 3A.3 顶层入口：fresh run 与 restart 分叉

`WarpX::InitData()` 位于 `../warpx/Source/Initialization/WarpXInitData.cpp`。第 3 章已经给过总表，这里看核心源码原文。

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:824-837`。

```cpp
if (!restart_chkfile.empty())
{
    InitFromCheckpoint(restart_chkfile);
    PrintDtDxDyDz();
    PostRestart();
}
else
{
    ComputeDt();
    PrintDtDxDyDz();
    InitFromScratch();
    InitDiagnostics();
}
```

这段分支决定初始化数据来源：

- restart：从 checkpoint 恢复 mesh、field、particles 和时间层，再做 restart 后处理；
- fresh run：先由 CFL、网格和 solver 计算 `dt`，再从零建立 AMR level、field、particles 和 diagnostics。

物理上，restart 应该恢复一个已经离散一致的状态；fresh run 则必须从输入参数构造这种一致状态。后面讲的外部场、初始粒子、Gaussian beam、openPMD 注入和 projection cleaning，主要属于 fresh run 路径。

## 3A.4 `InitFromScratch()`：AMReX level 与粒子初始化

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:993-1009`。

```cpp
void
WarpX::InitFromScratch ()
{
    BL_PROFILE("WarpX::InitFromScratch()");

    const amrex::Real time = 0.0;
    amrex::AmrCore::InitFromScratch(time);

    AllocLevelData();

    mypc->AllocData();
    mypc->InitData();

    InitPML();
}
```

这里的顺序很重要：

1. `AmrCore::InitFromScratch(time)` 创建 AMR level。
2. `AllocLevelData()` 分配 WarpX 自己管理的场、solver、buffer 和 level 数据。
3. `mypc->AllocData()` 为粒子容器准备数据结构。
4. `mypc->InitData()` 创建初始粒子。
5. `InitPML()` 初始化吸收边界数据结构。

因此，species 初始化发生在 field/level 数据结构已经存在之后，但在正式时间推进之前。

粒子容器入口源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:429-433`。

```cpp
void PhysicalParticleContainer::InitData ()
{
    AddParticles(0); // Note - add on level 0
    Redistribute();  // We then redistribute
}
```

这两行是后续所有粒子创建逻辑的入口。`AddParticles(0)` 负责生成初始粒子，`Redistribute()` 负责把粒子分配到正确 tile，并清理 invalid 粒子。

## 3A.5 外部场初始化：grid field 与 particle external field

WarpX 支持两类外部场：

- grid external field：外部场先放在网格 MultiFab 上，可参与 field solve 或作为背景场；
- particle external field：外部场在 particle gather 时参与粒子受力。

外部场初始化的关键是：外部场可以是常量、parser 函数、openPMD 文件或 Python 回调。读者应避免把“外部场”理解成单一数组。

以 projection cleaner 前的 external grid field 判断为例，源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:1658-1664`。

```cpp
if ( (m_p_ext_field_params->B_ext_grid_type == ExternalFieldType::read_from_file) ||
     (m_p_ext_field_params->E_ext_grid_type == ExternalFieldType::read_from_file) ||
     (mypc->m_B_ext_particle_s == "read_from_file") ||
     (mypc->m_E_ext_particle_s == "read_from_file") ) {
    ReadExternalFieldFromFile();
}
```

这段代码把 grid external field 与 particle external field 放在同一个文件读取入口下处理。真正写入哪一类 MultiFab，取决于前面解析出的 `B_ext_grid_type/E_ext_grid_type` 和 `m_B_ext_particle_s/m_E_ext_particle_s`。

外部场的物理约束是：如果读入的是 `B` 或矢势 `A`，数值上还需要检查离散散度误差；这就是后面 projection divergence cleaner 的用途。

## 3A.6 species 初始化：`PlasmaInjector` 是参数总容器

`PlasmaInjector` 的职责不是推进粒子，而是把输入文件中一个 species 的初始化规则收集成一组可供 kernel 调用的对象。

源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:126-153`。

```cpp
std::string injection_style = "none";
utils::parser::query(pp_species, source_name, "injection_style", injection_style);
std::transform(injection_style.begin(),
               injection_style.end(),
               injection_style.begin(),
               ::tolower);

num_particles_per_cell_each_dim.assign(3, 0);

if (injection_style == "singleparticle") {
    setupSingleParticle(pp_species);
    return;
} else if (injection_style == "multipleparticles") {
    setupMultipleParticles(pp_species);
    return;
} else if (injection_style == "gaussian_beam") {
    setupGaussianBeam(pp_species);
} else if (injection_style == "nrandompercell") {
    setupNRandomPerCell(pp_species);
} else if (injection_style == "nfluxpercell") {
    setupNFluxPerCell(pp_species);
} else if (injection_style == "nuniformpercell") {
    setupNuniformPerCell(pp_species);
} else if (injection_style == "external_file") {
    setupExternalFile(pp_species);
} else if (injection_style != "none") {
    SpeciesUtils::StringParseAbortMessage("Injection style", injection_style);
}
```

这个分支定义了初始粒子创建的第一层分类：

| `injection_style` | 含义 | 后续创建路径 |
|---|---|---|
| `singleparticle` | 单个手工粒子 | `AddNParticles()` |
| `multipleparticles` | 手工粒子列表 | `AddNParticles()` |
| `gaussian_beam` | 空间高斯束流 | `AddGaussianBeam()` |
| `external_file` | openPMD 粒子文件 | `AddPlasmaFromFile()` |
| `nrandompercell` / `nuniformpercell` | 体密度注入 | `AddPlasma()` |
| `nfluxpercell` | 面通量注入 | `AddPlasmaFlux()` |

在这一步之后，`PlasmaInjector` 还会把 host 侧 functor 拷贝到 device 侧，保证后续 GPU kernel 可以调用。

## 3A.7 密度和动量分布：从文本参数到 functor

密度解析由 `SpeciesUtils::parseDensity()` 完成。源码位置：`../warpx/Source/Utils/SpeciesUtils.cpp:80-114`。

```cpp
if ( profile == "constant" ){
    pp_species_name.query("density", plasma_injector.density);
    plasma_injector.m_inj_rho =
        std::make_unique<InjectorDensity>(InjectorDensityConstant{
            plasma_injector.density});
} else if (profile == "parse_density_function") {
    std::string str_density_function;
    utils::parser::queryWithParser(pp_species_name, "density_function(x,y,z)", str_density_function);
    auto density_parser =
        std::make_unique<amrex::Parser>(
            utils::parser::makeParser(str_density_function,{"x","y","z"}));
    plasma_injector.m_inj_rho =
        std::make_unique<InjectorDensity>(InjectorDensityParser{
            std::move(density_parser)});
} else if (profile == "read_from_file") {
    std::string read_density_from_path;
    pp_species_name.query("read_density_from_path", read_density_from_path);
    bool read_density_distributed = false;
    pp_species_name.query("read_density_distributed", read_density_distributed);
    plasma_injector.m_inj_rho =
        std::make_unique<InjectorDensity>(InjectorDensityFromFile{
            read_density_from_path, read_density_distributed});
}
```

体注入中的宏粒子权重由密度决定：

$$
w_p \approx n(\mathbf{x})\frac{\Delta V}{N_{ppc}}.
$$

动量解析由 `SpeciesUtils::parseMomentum()` 完成。常见分支包括：

- `at_rest`：`u=0`；
- `constant`：固定 `ux/uy/uz`；
- `gaussian`：每个方向正态采样；
- `gaussianflux`：通量注入专用，法向速度按 `v_n f(v)` 加权；
- `uniform`：每个方向均匀采样；
- `maxwell_boltzmann`：非相对论 Maxwellian；
- `maxwell_juttner`：相对论热平衡分布；
- `parse_momentum_function`：空间解析函数。

`InjectorMomentum` 的关键工程实现是手写 tagged union。源码位置：`../warpx/Source/Initialization/InjectorMomentum.H:459-719`。

```cpp
struct InjectorMomentum
{
    enum struct Type {
        constant,
        gaussian,
        gaussianflux,
        uniform,
        boltzmann,
        juttner,
        parser,
        gaussianparser
    };

    Type type;

    union {
        InjectorMomentumConstant constant;
        InjectorMomentumGaussian gaussian;
        InjectorMomentumGaussianFlux gaussianflux;
        InjectorMomentumUniform uniform;
        InjectorMomentumBoltzmann boltzmann;
        InjectorMomentumJuttner juttner;
        InjectorMomentumParser parser;
        InjectorMomentumGaussianParser gaussianparser;
    };
```

这不是普通虚函数多态，而是 GPU kernel 友好的平铺对象。后续 `AddPlasma()` 可以在 device 上用 `getMomentum()` 采样单粒子动量，用 `getBulkMomentum()` 得到平均漂移速度。

## 3A.7 `AddParticles()`：按注入类型进入创建函数

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:194-260`。

```cpp
void
PhysicalParticleContainer::AddParticles (int lev)
{
    ABLASTR_PROFILE("PhysicalParticleContainer::AddParticles()");

    for (auto const& plasma_injector : plasma_injectors) {

        if (plasma_injector->add_single_particle) {
            if (WarpX::gamma_boost > 1.) {
                MapParticletoBoostedFrame(plasma_injector->single_particle_pos[0],
                                          plasma_injector->single_particle_pos[1],
                                          plasma_injector->single_particle_pos[2],
                                          plasma_injector->single_particle_u[0],
                                          plasma_injector->single_particle_u[1],
                                          plasma_injector->single_particle_u[2]);
            }
            const amrex::Vector<ParticleReal> xp = {plasma_injector->single_particle_pos[0]};
            const amrex::Vector<ParticleReal> yp = {plasma_injector->single_particle_pos[1]};
            const amrex::Vector<ParticleReal> zp = {plasma_injector->single_particle_pos[2]};
            const amrex::Vector<ParticleReal> uxp = {plasma_injector->single_particle_u[0]};
            const amrex::Vector<ParticleReal> uyp = {plasma_injector->single_particle_u[1]};
            const amrex::Vector<ParticleReal> uzp = {plasma_injector->single_particle_u[2]};
            const amrex::Vector<amrex::Vector<ParticleReal>> attr = {{plasma_injector->single_particle_weight}};
            const amrex::Vector<amrex::Vector<int>> attr_int;
            AddNParticles(lev, 1, xp, yp, zp, uxp, uyp, uzp,
                          1, attr, 0, attr_int, 0);
            return;
        }
```

后半段分派如下：

```cpp
        if (plasma_injector->gaussian_beam) {
            AddGaussianBeam(*plasma_injector);
        }

        if (plasma_injector->external_file) {
            AddPlasmaFromFile(*plasma_injector,
                              plasma_injector->q_tot,
                              plasma_injector->z_shift);
        }

        if ( plasma_injector->doInjection() ) {
            AddPlasma(*plasma_injector, lev);
        }
    }
}
```

这个函数说明：`PlasmaInjector` 中可能同时保存多种初始化信息，但最终创建时按 flag 调用不同路径。

## 3A.8 体注入 `AddPlasma()`：候选粒子、密度、动量和权重

体注入的核心思想是：先按 cell 和 `num_particles_per_cell` 创建候选粒子，然后用真实 density/bounds 筛掉无效粒子，并把有效粒子写入 SoA。

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:854-912`。

```cpp
// count the number of particles that each cell in overlap_box could add
amrex::Gpu::DeviceVector<amrex::Long> counts(overlap_box.numPts(), 0);
amrex::Gpu::DeviceVector<amrex::Long> offset(overlap_box.numPts());
auto *pcounts = counts.data();
amrex::Box fine_overlap_box; // default Box is NOT ok().
if (refine_injection) {
    fine_overlap_box = overlap_box & amrex::shift(fine_injection_box, -shifted);
}
amrex::ParallelFor(overlap_box, [=] AMREX_GPU_DEVICE (int i, int j, int k) noexcept
{
    const amrex::IntVect iv(AMREX_D_DECL(i, j, k));
    auto lo = getCellCoords(overlap_corner, dx, {0._rt, 0._rt, 0._rt}, iv);
    auto hi = getCellCoords(overlap_corner, dx, {1._rt, 1._rt, 1._rt}, iv);

    lo.z = applyBallisticCorrection(lo, inj_mom, gamma_boost, beta_boost, t);
    hi.z = applyBallisticCorrection(hi, inj_mom, gamma_boost, beta_boost, t);

    if (inj_pos->overlapsWith(lo, hi))
    {
        auto index = overlap_box.index(iv);
        const amrex::Long r = (fine_overlap_box.ok() && fine_overlap_box.contains(iv))?
            (AMREX_D_TERM(rrfac[0],*rrfac[1],*rrfac[2])) : (1);
        pcounts[index] = num_ppc*r;
```

`applyBallisticCorrection()` 用 bulk velocity 把 boosted-frame 位置反推到 lab-frame 初始面。其公式是：

$$
z_{0,lab}=\gamma_b\left[z_{boost}(1-\beta_b\beta_z)-ct_{boost}(\beta_z-\beta_b)\right].
$$

随后用 prefix scan 得到写入 offset：

```cpp
const amrex::Long max_new_particles = amrex::Scan::ExclusiveSum(counts.size(), counts.data(), offset.data());

amrex::Long pid;
{
    pid = ParticleType::NextID();
    ParticleType::NextID(pid+max_new_particles);
}
```

这种“两遍法”避免在 GPU kernel 中动态 push 粒子。

真正填充粒子时，体注入权重系数为：

```cpp
AMREX_GPU_HOST_DEVICE AMREX_FORCE_INLINE
amrex::Real compute_scale_fac_volume (const amrex::GpuArray<amrex::Real, AMREX_SPACEDIM>& dx,
                                      const amrex::Long pcount) {
    using namespace amrex::literals;
    return (pcount != 0) ? AMREX_D_TERM(dx[0],*dx[1],*dx[2])/pcount : 0.0_rt;
}
```

即

$$
w_p = n(\mathbf{x})\frac{\Delta V}{N_{ppc}}.
$$

在 boosted-frame 分支中，密度和纵向动量做 Lorentz 变换：

```cpp
dens = gamma_boost * dens * ( 1.0_rt - beta_boost*betaz_lab );
u.z = gamma_boost * ( u.z -beta_boost*gamma_lab );
```

对应：

$$
n'=\gamma_b n(1-\beta_b\beta_z),\qquad
u_z'=\gamma_b(u_z-\beta_b\gamma).
$$

最后写入粒子 SoA：

```cpp
u.x *= PhysConst::c;
u.y *= PhysConst::c;
u.z *= PhysConst::c;

amrex::Real weight = dens;
weight *= scale_fac;

pa[PIdx::w ][ip] = weight;
pa[PIdx::ux][ip] = u.x;
pa[PIdx::uy][ip] = u.y;
pa[PIdx::uz][ip] = u.z;
```

因此 `InjectorMomentum` 返回的 `u` 是无量纲 `\gamma\beta`，粒子数组中存的是 `\gamma v`。

## 3A.9 Gaussian beam：显式束流列表注入

Gaussian beam 不使用 `InjectorDensity`，而是在 IO rank 上显式随机生成粒子列表。

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:396-407`。

```cpp
if (ParallelDescriptor::IOProcessor()) {
    // If do_symmetrize, create either 4x or 8x fewer particles, and
    // Replicate each particle either 4 times (x,y) (-x,y) (x,-y) (-x,-y)
    // or 8 times, additionally (y,x), (-y,x), (y,-x), (-y,-x)
    if (do_symmetrize){
        npart /= symmetrization_order;
    }
    // compute the weight from N_tot if the user specified npart_real = N_tot
    // compute the weight from q_tot if the user specified q_tot
    // note that npart is the number of macroparticles
    const amrex::Real weight_3d = (N_tot > 0._rt) ? (N_tot / npart) : (q_tot / (npart*charge));
```

权重来自总真实粒子数或总电荷：

$$
w_{3d} =
\begin{cases}
N_{\mathrm{tot}}/N_p,\\
Q_{\mathrm{tot}}/(N_p q).
\end{cases}
$$

随后按高斯分布采样空间位置：

```cpp
#if defined(WARPX_DIM_3D) || defined(WARPX_DIM_RZ)
    const amrex::Real weight = weight_3d;
    amrex::Real x = amrex::RandomNormal(x_m, x_rms);
    amrex::Real y = amrex::RandomNormal(y_m, y_rms);
    amrex::Real z = amrex::RandomNormal(z_m, z_rms);
#elif defined(WARPX_DIM_XZ)
    const amrex::Real weight = weight_3d/y_rms;
    amrex::Real x = amrex::RandomNormal(x_m, x_rms);
    constexpr amrex::Real y = 0._prt;
    amrex::Real z = amrex::RandomNormal(z_m, z_rms);
```

如果设置 `focal_distance`，代码用弹道近似从焦平面束斑反推出初始位置。核心公式是：

$$
t = \frac{(\mathbf{x}_f-\mathbf{x})\cdot\mathbf{n}}{\mathbf{v}\cdot\mathbf{n}},
\qquad
\mathbf{x}\leftarrow \mathbf{x}-\mathbf{v}_\perp t.
$$

源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:453-462`。

```cpp
// Compute the time at which the particle will cross the focal plane
const amrex::Real v_dot_n = v_x * n_x + v_y * n_y + v_z * n_z;
const amrex::Real t = ((x_f-x)*n_x + (y_f-y)*n_y + (z_f-z)*n_z) / v_dot_n;

// Displace particles in the direction orthogonal to the beam bulk momentum
// i.e. orthogonal to (n_x, n_y, n_z)
#if defined(WARPX_DIM_3D) || defined(WARPX_DIM_RZ)
x = x - (v_x - v_dot_n*n_x) * t;
y = y - (v_y - v_dot_n*n_y) * t;
z = z - (v_z - v_dot_n*n_z) * t;
```

如果设置 symmetrization，代码为每个样本生成 4 或 8 个镜像粒子，并把权重除以阶数。这降低横向低阶统计噪声。

## 3A.10 openPMD 粒子文件：文件粒子列表注入

`external_file` 路径在构造期先打开 openPMD 文件，读取可选 `charge/mass`。源码位置：`../warpx/Source/Initialization/PlasmaInjector.cpp:483-584`。

```cpp
void PlasmaInjector::setupExternalFile (amrex::ParmParse const& pp_species)
{
#ifndef WARPX_USE_OPENPMD
    WARPX_ABORT_WITH_MESSAGE(
        "WarpX has to be compiled with USE_OPENPMD=TRUE to be able"
        " to read the external openPMD file with species data");
#endif
    external_file = true;
    std::string str_injection_file;
    utils::parser::get(pp_species, source_name, "injection_file", str_injection_file);
    // optional parameters
    utils::parser::queryWithParser(pp_species, source_name, "q_tot", q_tot);
    utils::parser::queryWithParser(pp_species, source_name, "z_shift",z_shift);
```

质量和电荷优先级是：

```text
input charge/mass > input species_type > openPMD charge/mass record
```

真正读入粒子时，源码位置：`../warpx/Source/Particles/ParticleCreation/AddParticles.cpp:680-715`。

```cpp
for (auto i = decltype(npart){0}; i<npart; ++i){

    amrex::ParticleReal const weight = ptr_w.get()[i]*w_unit;

#if !defined(WARPX_DIM_1D_Z)
    amrex::ParticleReal const x = ptr_x.get()[i]*position_unit_x + ptr_offset_x.get()[i]*position_offset_unit_x;
#else
    amrex::ParticleReal const x = 0.0_prt;
#endif
#if defined(WARPX_DIM_3D) || defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    amrex::ParticleReal const y = ptr_y.get()[i]*position_unit_y + ptr_offset_y.get()[i]*position_offset_unit_y;
#else
    amrex::ParticleReal const y = 0.0_prt;
#endif
#if !defined(WARPX_DIM_RCYLINDER)
    amrex::ParticleReal const z = ptr_z.get()[i]*position_unit_z + ptr_offset_z.get()[i]*position_offset_unit_z + z_shift;
#else
    amrex::ParticleReal const z = 0.0_prt;
#endif
```

openPMD 的 `position` 和 `positionOffset` 都乘以各自 `unitSI`，`z_shift` 是 WarpX 额外偏移。

动量换算：

```cpp
if (plasma_injector.insideBounds(x, y, z)) {

    // The normalized momentum is u = p / m = gamma beta c
    // with m = m_e for photons, m the particle mass otherwise.
    amrex::ParticleReal const mass_eff = (m_mass > 0.0_prt) ? m_mass : PhysConst::m_e;
    amrex::ParticleReal const ux = ptr_ux.get()[i]*momentum_unit_x/mass_eff;
    amrex::ParticleReal const uz = ptr_uz.get()[i]*momentum_unit_z/mass_eff;
    amrex::ParticleReal uy = 0.0_prt;
    if (ps["momentum"].contains("y")) {
        uy = ptr_uy.get()[i]*momentum_unit_y/mass_eff;
    }
```

openPMD 文件中的 momentum 是物理动量 `p`。除以质量得到 `p/m=\gamma v`，这正是 WarpX 粒子数组的 `ux/uy/uz` 量纲。文件中的 `weighting` 直接成为宏粒子权重；`q_tot` 只产生 warning，不会重标定权重。

## 3A.11 Projection divergence cleaning：外部 `A/B` 场的初始约束修正

如果外部加载的 `B` 或矢势 `A` 在离散网格上不满足散度约束，WarpX 可用 projection 方法清理。

数学上，给定向量场 `F`，构造：

$$
\mathbf{F}'=\mathbf{F}+\nabla_h\phi,
\qquad
\nabla_h\cdot\mathbf{F}'=0.
$$

于是

$$
\nabla_h^2\phi=-\nabla_h\cdot\mathbf{F}.
$$

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp:256-264`。

```cpp
WarpX::ComputeDivB(
    *m_source[ilev],
    0,
    {Bx, By, Bz},
    WarpX::CellSize(0)
    );

m_source[ilev]->mult(-1._rt);
```

然后用 AMReX MLMG 解 Poisson 方程。源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.H:93-100`。

```cpp
amrex::MLMG mlmg(linop);
mlmg.setMaxIter(m_max_iter);
mlmg.setMaxFmgIter(m_max_fmg_iter);
mlmg.setBottomSolver(m_bottom_solver);
mlmg.setVerbose(m_verbose);
mlmg.setBottomVerbose(m_bottom_verbose);
mlmg.setConvergenceNormType(amrex::MLMGNormType::greater);
mlmg.solve({m_solution[lev].get()}, {m_source[lev].get()}, m_rtol, m_atol);
```

最后修正场：

```cpp
Bx_arr(i,j,k) += T::DownwardDx(sol_arr, coefs_x, n_coefs_x, i, j, k);
By_arr(i,j,k) += T::DownwardDy(sol_arr, coefs_y, n_coefs_y, i, j, k);
Bz_arr(i,j,k) += T::DownwardDz(sol_arr, coefs_z, n_coefs_z, i, j, k);
```

这不是演化阶段的 `warpx.do_dive_cleaning/do_divb_cleaning`。后者是 Maxwell solver 时间推进中的清理变量或修正方程；本节讲的是初始化或外部场加载后的 Poisson projection。

### Laser antenna 与 profile 分派：laser 初始化并不走 `PlasmaInjector`

species 初始化走的是 `PlasmaInjector -> AddPlasma/AddGaussianBeam/AddPlasmaFromFile` 这一条链；laser 初始化则完全不同。它的入口是：

- `lasers.names`
- `LaserParticleContainer`
- `Laser/LaserProfiles.*`

`LaserParticleContainer` 构造函数先统一读取天线几何和公共物理参数：

```cpp
utils::parser::getArrWithParser(pp_laser_name, "position", m_position);
utils::parser::getArrWithParser(pp_laser_name, "direction", m_nvec);
utils::parser::getArrWithParser(pp_laser_name, "polarization", m_p_X);
utils::parser::getWithParser(pp_laser_name, "wavelength", m_wavelength);
```

然后要求 `e_max` 和 `a0` 二选一：

```cpp
const bool e_max_is_specified =
    utils::parser::queryWithParser(pp_laser_name, "e_max", m_e_max);
Real a0;
const bool a0_is_specified =
    utils::parser::queryWithParser(pp_laser_name, "a0", a0);
...
AMREX_ALWAYS_ASSERT_WITH_MESSAGE(
    e_max_is_specified ^ a0_is_specified,
    "Exactly one of e_max or a0 must be specified for the laser.\n");
```

如果给的是 `a0`，WarpX 会立即按

$$
E_{\max}=\frac{m_e \omega c}{q_e}a_0
$$

换算成真实场强 `e_max`。这说明在 profile 实现层，`a0` 已经不再存在，剩下的只是规范化后的公共参数。

profile 类型分派也不是一串手写 `if-else`，而是 `LaserProfiles.H` 中的工厂字典：

```cpp
laser_profiles_dictionary =
{
    {"gaussian",
        [] () {return std::make_unique<GaussianLaserProfile>();} },
    {"parse_field_function",
        [] () {return std::make_unique<FieldFunctionLaserProfile>();} },
    {"from_file",
        [] () {return std::make_unique<FromFileLaserProfile>();} }
};
```

构造函数把 `profile` 字符串转成小写后直接做字典查找，再调用统一接口：

```cpp
m_up_laser_profile = laser_profiles_dictionary.at(laser_type_s)();
...
m_up_laser_profile->init(pp_laser_name, common_params);
```

所以：

1. `gaussian` 走解析包络与聚焦/STC/chirp 公式；
2. `parse_field_function` 直接把 `field_function(X,Y,t)` 编译成 parser；
3. `from_file` 则走 `lasy_file_name` 或 `binary_file_name`，并用 `time_chunk_size` / `delay` 做时间分块读入。

更重要的是，laser pulse 不是直接“写入一个初始场数组”，而是通过人工天线粒子实现。`LaserParticleContainer.H` 的类注释写得很明确：这些粒子均匀分布在一个平面上，按预设位移沉积电流 `J`，再由 Maxwell solver 在网格上生成真正的激光场。因此 `LaserParticleContainer` 需要 current deposition，但不走普通 `FieldGather`，它也正因如此直接继承 `WarpXParticleContainer`，而不是 `PhysicalParticleContainer`。

continuous injection 对 laser 还有额外几何约束：

```cpp
AMREX_ALWAYS_ASSERT_WITH_MESSAGE(
    ...,
    "do_continous_injection for laser particle only works"
    " if moving window direction and laser propagation direction are the same");
```

如果叠加 boosted frame，目前还进一步要求 boost 方向是 `z`。因此 laser 的 `do_continuous_injection` 虽然和普通 species 同名，但它的可用组合更窄，实际上是“moving-window / boosted-frame 下天线何时进入域内”的控制开关。

这还只是 laser 初始化链的入口。真正运行起来后，WarpX 并不会把解析式或文件 profile 直接写进 `E/Bfield_fp`。它先把 profile 解释成“天线平面上每个人工粒子的目标发射振幅”，再通过标准 `J/rho` 沉积把激光交给 Maxwell solver。

`GaussianLaserProfile::init()` 继续在公共参数外读取：

```cpp
utils::parser::getWithParser(ppl, "profile_waist", m_params.waist);
utils::parser::getWithParser(ppl, "profile_duration", m_params.duration);
utils::parser::getWithParser(ppl, "profile_t_peak", m_params.t_peak);
utils::parser::getWithParser(ppl, "profile_focal_distance", m_params.focal_distance);
utils::parser::queryWithParser(ppl, "zeta", m_params.zeta);
utils::parser::queryWithParser(ppl, "beta", m_params.beta);
utils::parser::queryWithParser(ppl, "phi2", m_params.phi2);
utils::parser::queryWithParser(ppl, "phi0", m_params.phi0);
```

因此当前 `gaussian` profile 并不是“只有纵向和横向高斯包络”的最简形式，而是已经直接包含：

- 聚焦距离 `profile_focal_distance`
- carrier-envelope phase `phi0`
- spatial chirp `zeta`
- angular dispersion `beta`
- temporal chirp `phi2`

WarpX 随后还会把 `stc_direction` 归一化，并强制要求它与天线法向 `nvec` 正交：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(std::abs(dp2) < 1.0e-14,
    "stc_direction is not perpendicular to the laser plane vector");
```

这说明 `stc_direction` 的真实语义是“STC 在激光平面内的作用方向”，不是随手附带的一个参考向量。到了 `fill_amplitude()`，WarpX 再显式构造：

- `diffract_factor`
- `inv_complex_waist_2`
- `stretch_factor`

并按 3D/RZ、XZ、1D 分别选不同 prefactor。也就是说，当前 Gaussian 实现已经把 diffraction、Gouy phase、wavefront curvature、spatial chirp、angular dispersion 和 temporal chirp 全都折叠进同一个复 envelope 公式里，而不是后面再给场求解器额外修正。

`from_file` profile 的合同也比“读一个文件”更具体。源码强制要求：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE (
    lasy_file_name.empty() != binary_file_name.empty(),
    "Exactly one of 'binary_file_name' and 'lasy_file_name' has to be specified");
```

因此 `from_file` 不是同时混用两种后端，而是在：

- `lasy_file_name`
- `binary_file_name`

之间二选一。并且它不是一次性把整份文件全读进来，而是先把 `time_chunk_size` 设成默认全时域，再允许用户把它改小，随后只预读第一块；真正运行时由 `m_up_laser_profile->update(t_lab)` 按需换块。`delay` 也不是写文件时的预处理，而是在 `update()` / `fill_amplitude()` 内统一平移 profile 时间轴。

更关键的是，`LaserParticleContainer::InitData()` 的产物不是“初始化场”，而是人工天线粒子。它先按 finest cell 和天线平面方向计算平面 spacing `S_X/S_Y`，再建立实验室坐标与激光平面坐标之间的 `Transform/InverseTransform`，最后只在注入盒覆盖的区域生成粒子：

- Cartesian / XZ / 1D：每个平面位置生成一对 `+w/-w` 粒子
- RZ：围绕轴向展开成 spokes，并用 `2πr/n_spokes` 修正权重

到了 `LaserParticleContainer::Evolve()`，运行时主链是：

1. 若在 boosted frame，先把数值时间 `t` 转回实验室系 `t_lab`
2. `m_up_laser_profile->update(t_lab)`，必要时推进 `from_file` 的时间块缓存
3. `calculate_laser_plane_coordinates(...)`，把真实粒子位置映回激光平面坐标
4. `fill_amplitude(...)`，为每个天线粒子求目标 `E` 振幅
5. `update_laser_particle(...)`，把振幅变成粒子动量和位置
6. `DepositCurrent()` / `DepositCharge()`，把人工天线粒子写入 `current_fp/rho_fp`，必要时也写入 coarse-fine `current_buf/rho_buf`

所以 WarpX 的 laser antenna 不是“边界直接给定场”，而是“人为构造一层发射粒子，通过普通沉积链把 profile 写成 `J`，再让 Maxwell solver 自己生成传播场”。这也解释了为什么 laser 在 mesh refinement 下照样要走 `fp / buf` 分流，以及为什么 `lasers.deposit_on_main_grid` 其实属于 AMR/沉积合同，而不只是一个 laser 小选项。

最后，laser 的 continuous injection 也应理解得更准确一点。`ContinuousInjection()` 检查的是更新后的 `m_updated_position` 是否第一次进入当前 `injection_box`；一旦进入，就调用一次 `InitData()` 生成那片天线粒子，之后再由普通 `Evolve()` 周期性更新它们的发射振幅。它不是每步“重新生成整束激光”，而是在 moving-window / boosted-frame 下决定“天线什么时候进入域内并开始工作”。

`parse_field_function` 这条分支也需要单独说明，因为它和前两类 profile 的数学合同并不一样。官方参数文档把它定义成：

```text
<laser_name>.field_function(X,Y,t)
```

这里给出的不是包络，而是完整电场本身；`X/Y` 是垂直于激光传播方向的平面坐标，而不是固定的仿真坐标轴。`FieldFunctionLaserProfile::init()` 在源码里只做两件事：

```cpp
utils::parser::Store_parserString(
        ppl, "field_function(X,Y,t)", m_params.field_function);
m_parser = utils::parser::makeParser(m_params.field_function,{"X","Y","t"});
```

随后 `fill_amplitude()` 也没有再加任何 envelope、phase 或 geometry 修正，而是直接逐粒子求值：

```cpp
auto parser = m_parser.compile<3>();
amrex::ParallelFor(np, [=] AMREX_GPU_DEVICE (int i) noexcept
{
    amplitude[i] = parser(Xp[i], Yp[i], t);
});
```

这说明 `parse_field_function` 的 profile 层是三类实现里最薄的一层：用户写什么场函数，天线平面上就得到什么目标场值；后续所有“把目标场值变成可沉积粒子运动”的责任，都落在 `LaserParticleContainer` 的更新 kernel 上。

这几个 kernel 里，`calculate_laser_plane_coordinates(...)` 负责把真实粒子位置减去天线参考点后，投影回 `m_u_X/m_u_Y` 基底，因此 profile 接口始终统一在激光平面坐标上。`ComputeWeightMobility()` 则先用固定的峰值速度上限 `eps = 0.05` 设定：

```cpp
m_mobility = eps/m_e_max;
m_weight = PhysConst::epsilon_0 / m_mobility;
m_weight *= AMREX_D_TERM(1._rt, * Sx, * Sy);
```

也就是说，WarpX 不是先任意给天线粒子权重，再让速度自己长出来；而是先要求峰值场下粒子速度不超过 `0.05c`，再反推单粒子权重。到了 `update_laser_particle()`，WarpX 再把 `amplitude[i]` 变成：

1. 沿主偏振方向 `p_X` 的速度
2. boosted-frame 下额外减去沿传播方向 `nvec` 的平移速度
3. 相应的 relativistic momentum `ux/uy/uz`
4. 显式路径的整步位置推进，或 implicit 路径基于 `x_n/y_n/z_n` 的半步 time-centered 位置推进

因此 laser 的人工天线粒子并不是一个只服务显式 solver 的简单边界 hack。它同样要遵守 implicit particle-centering 合同，并继续进入普通 `DepositCurrent()/DepositCharge()` 主链。

当前本地 checkout 里，`parse_field_function` 的最明确真实用例是 `Examples/Tests/particle_absorbing_boundary/inputs_test_1d_particle_absorbing_boundary`。这个输入把：

- `laser1.profile = parse_field_function`
- `laser1.field_function(X,Y,t) = ...`

嵌进了吸收边界测试里。但对应 `analysis.py` 检查的是边界附近的负向高速电子是否被抑制，而不是直接检查激光场本身。这意味着 `parse_field_function` 目前是“有真实 regression 入口，但没有独立 field-level 解析断言”的状态，书稿里应把这个验证边界明确写出来。

把 laser 模块整体放回 regression 版图后，还能看到另一个重要事实：不同 laser tests 的证据强度差别很大。`Examples/Tests/laser_injection/` 的 1D/2D analysis 会直接比较 Gaussian 注入场的包络和主频；implicit 1D/2D 变体也继续复用同一组 analysis，因此并不只是“implicit 能跑通”的 checksum test。`Examples/Tests/laser_injection_from_file/` 则继续给 `lasy`、legacy binary、boosted-frame 和 RZ `thetaMode` 文件提供 envelope/frequency 双断言。

但这一组还必须再分出一层 helper / prepare 边界。两个目录里的 `analysis_default_regression.py` 都只是本地 checksum helper 副本：职责是自动识别 plotfile/openPMD 并按测试目录名调用 `evaluate_checksum(...)`，给 active tests 提供历史输出基线，而不是新增 laser 物理断言。更重要的是，`laser_injection_from_file/` 里那批 `inputs_test_*_prepare.py` 并不是“待分析输入”，而是被 `CMakeLists.txt` 先行注册成 dependency 的外部文件生成阶段：

- 普通 1D/2D/3D/RZ lasy 变体统一先写 `gaussian_laser_3d`
- legacy binary 变体先手工写 `gauss_2d`
- RZ `thetaMode` 变体先写 `laguerre_laser_RZ`

因此这组 regression 的正确结构不是单段输入，而是：

1. `prepare`
   - 生成外部 laser 文件
2. `inject`
   - WarpX 按 `from_file` / `binary_file_name` / RZ 路径消费这些文件
3. `analysis`
   - 再对最终包络和主频做强断言

这条边界对后面精读 `Laser/` 很关键，因为它说明“外部 laser 文件格式合同”本身已经是 active regression 的一部分，而不只是示例配套脚本。

但到了 `Examples/Physics_applications/laser_acceleration/`，情况就不一样了。这个目录本质上不是一组 laser-injection 单元测试，而是一套 LWFA runtime matrix。`README.rst` 自己都把 `Analyze` 章节留成了 `TODO`，而当前大多数 active tests 在 `CMakeLists.txt` 中也都配置成 `analysis = OFF`，只保留 checksum；只有少数变体有明确 analysis：

- `analysis_1d_fluid_boosted.py`：把 laser 驱动的 1D boosted fluid WFA 结果与理论 ODE 解对照，检查 `Ez/Jz/rho/Vz`
- `analysis_refined_injection.py`：检查 `warpx.refine_plasma = 1` 场景下的总粒子数和 refinement edge 前方 `rho` 切片均匀性
- `analysis_openpmd_rz.py`：检查 RZ openPMD diagnostics 的 mesh shape、species ordering 和 `rho_<species>` 物理中心位置

更进一步，`inputs_base_1d/2d/3d/rz` 四个基础输入也说明了这组 family 先定义的是不同维度下的运行骨架：

- 1D：moving window + 连续电子注入 + Gaussian laser antenna + `FieldProbe`
- 2D：PML + moving window + refined patch + 连续背景电子 + Gaussian `beam`
- 3D：moving window + openPMD Full diagnostics + 自定义粒子属性
- RZ：`n_rz_azimuthal_modes = 2` + beam/plasma 共存 + species 变量输出

因此 `laser_acceleration` 目录里的大多数条目当前更准确的定位应该是：

- LWFA application/runtime checksum baseline
- 以及 boosted / MR / PICMI / Python callback / RZ / openPMD 的路径覆盖

而不是统一的 wake amplitude 或 laser envelope 解析 benchmark。

此外，`Examples/Tests/boosted_diags/analysis.py` 对 `test_3d_laser_acceleration_btd` 的验证重点也不是 laser 包络本身，而是：

1. BTD plotfile 与 BTD openPMD 的 `Ez` 是否逐点一致
2. `random_fraction` 粒子子采样是否真的生效

所以当前本地 WarpX checkout 对 laser 的回归支持应这样理解：

- 注入本体：1D/2D 强，3D 较弱
- `from_file`：强
- `parse_field_function`：有真实入口，但主要是间接覆盖
- `laser_acceleration`：多数是下游 LWFA/LPI 工作流回归，不应误写成 laser 注入公式的直接解析验证
- BTD / openPMD / Python callback：更偏 diagnostics 和 workflow 合同

这组边界在书稿中必须显式写出，否则很容易把“有 analysis.py”误判成“已经有强物理断言”，或者把 `laser_acceleration` 目录整体误判成 laser injection 的单元测试集合。

再往运行态交界看一层，laser 初始化还必须和 moving window、boosted frame、continuous injection、external fields 的更新合同一起理解。`WarpX::MoveWindow()` 在真正平移网格前，会先做三件互不等价的更新：

```cpp
moving_window_x += ...;
::UpdateInjectionPosition(*mypc, gamma_boost, beta_boost, boost_direction, moving_window_dir, dt[0]);
mypc->UpdateAntennaPosition(dt[0]);
```

这里：

1. `moving_window_x` 是窗口几何本身的位置；
2. `UpdateInjectionPosition(...)` 更新普通 species 的 `m_current_injection_position`；
3. `UpdateAntennaPosition(dt)` 更新 laser antenna 的 `m_updated_position`。

普通 species 的连续注入位置来自 `PlasmaInjector` 的 bulk momentum，再换成速度并在 boosted frame 下做洛伦兹变换；laser 则完全不走 `PlasmaInjector`，只在 `do_continuous_injection=1` 且 `gamma_boost>1` 时按 boost velocity 平移天线平面。因此两者虽然都叫 continuous injection，但运行态位置更新机制不同。

两者的 `ContinuousInjection()` 语义也不同。普通物理粒子是在 moving window 新扫进来的 level-0 `particleBox` 中反复调用 `AddPlasma(...)`；laser 则只在 `m_updated_position` 第一次进入当前 `injection_box` 时调用一次 `InitData()`，之后靠已有人工天线粒子在 `Evolve()` 中持续更新并沉积 `J/rho`。AMR 下这两个尺度也不同：species 的 runtime 注入盒按 level-0 cell 对齐，而 `LaserParticleContainer::InitData()` 仍然按 `maxLevel()` 的 finest spacing 建立天线粒子。

external field 的 moving-window 合同也在这里锁死。`LoadExternalFields()` 对 `B/E_ext_grid_type == read_from_file` 以及 particle external field 的 `read_from_file` 都直接断言：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    WarpX::do_moving_window == 0,
    "External fields from file are not compatible with the moving window." );
```

原因不是 openPMD 不能读，而是 `MoveWindow()` 在新进入的 cells 上只能通过 `shiftMF(...)` 用 constant 或 parser 两种方式重建主场背景：

```cpp
srcfab(i,j,k,n) = external_field;
srcfab(i,j,k,n) = field_parser(x,y,z);
```

因此 constant/parser 外场可以跟着 moving window 继续生成，而 `read_from_file` 缺少“窗口每推进一次就按新的 physical coordinates 增量重读”的实现，所以被源码显式禁止。这也解释了为什么当前 `load_external_field*` regressions 都天然是静态窗口场景，而 `laser_acceleration_boosted`、`refined_injection`、`subcycling_mr` 这些例子才更贴近 laser 与 moving-window 交界的真实运行态合同。

再往应用层走，laser 在本地 WarpX 里已经分叉成三种不同角色。`laser_ion` 是最典型的“laser 作为驱动器”的场景：输入里同时绑了 Gaussian laser、solid-density target、full diagnostics、time-averaged diagnostics、`ParticleHistogram`、`FieldProbe` 和 `ParticleHistogram2D`。但它最硬的 regression 断言并不是离子能量标度，而是 `analysis_test_laser_ion.py` 对 `diagInst` 最后 5 个 snapshot 的瞬时 `Ez` 平均值与 `diagTimeAvg` 原位 time-averaged `Ez` 的逐点比较。因此它在书稿里最适合承担“laser 主链怎样进入复杂 diagnostics 组合场景”的角色。

`free_electron_laser` 则正好是反例：它没有 `lasers.names = ...`，而是通过刚性注入电子/正电子束、boosted frame、moving window 和外加 undulator `B_y(z)` 让辐射在束流中自发增长。`analysis_fel.py` 在 lab-frame 与 boosted-frame diagnostics 上分别拟合 gain length，并通过 FFT 反推出 radiation wavelength。这说明这里的“laser/辐射”不是天线输入，而是束流和 external particle field 共同产生的结果量，所以它更像 laser 相关应用，而不是 Laser 模块本身的 injection regression。

再往实现层拆，`free_electron_laser` 真正依赖的三块基础设施是：

1. `RigidInjectedParticleContainer`
2. `particles.B_ext_particle_init_style = parse_B_ext_particle_function`
3. `BackTransformed` diagnostics

它的 species 不会实例化普通 `PhysicalParticleContainer`，而是被 `MultiParticleContainer` 切到 `RigidInjectedParticleContainer`。`zinject_plane` 和 `rigid_advance` 决定束团在注入面之前是按各自 `v_z` 还是按平均束流速度作刚体传播；boosted-frame 下 `zinject_plane_levels` 还会继续按 `beta_boost c` 平移。与此同时，undulator 场也不是写入主场 `Bfield_fp`，而是通过 particle external field parser 直接在 gather 侧提供 `B_y(z)`。因此这里的主链其实是“刚性束流 + 粒子背景场 + BTD 恢复 lab-frame 物理”，而不是 laser antenna 本体。

`rigid_injection` 和 `boosted_diags` 两组 tests 则给这条链提供了更基础的硬断言。前者分别在 lab frame 和 BTD 下检查：刚性传播是否真的把束宽保持到 `zinject_plane`、以及 plotfile/openPMD 回写的束团位置与动量是否一致；后者额外验证 BTD 两种 writer 的场数据一致性与 `random_fraction` 粒子子采样合同。也就是说，`analysis_fel.py` 负责最终 FEL 标度，`rigid_injection*` 负责 rigid propagation 本身，`boosted_diags` 负责 BTD 基础设施，而这三层不应再被混写成一个笼统的“laser regression”。

`laser_on_fine` 则又是第三类。它确实使用真正的 Gaussian laser antenna，但 `CMakeLists.txt` 里没有独立 analysis，主要依赖 checksum；输入重点在 `max_level = 1`、`fine_tag_lo/hi`、`laser1.prob_lo/prob_hi` 和 PML。也就是说它更像一个 AMR placement/solver 稳定性测试，而不是下游应用 physics 场景。

因此，后续书稿中的 laser 应用层不应只按 profile 分类，而应按三种角色拆分：

1. laser 作为驱动器并配套 diagnostics 组合：`laser_ion`
2. 辐射/laser 作为输出结果量：`free_electron_laser`
3. laser 作为 AMR/placement 测试对象：`laser_on_fine`

还需要再补一个当前证据层更弱、但应用语义很典型的角色：`plasma_mirror`。它的输入已经把 Gaussian laser、solid-density target、前后指数梯度、PML、field filter 和双 species 固体靶骨架接在一起，因此在应用语义上非常像“laser-solid surface-plasma 最小样板”；但当前 active regression 只有 checksum helper，没有独立 analysis，也没有 PICMI 版输入。所以它更适合在书稿里承担“过密靶/表面等离子体应用骨架已经存在，但强物理断言仍未单独压实”的角色，而不应被写成 plasma-mirror 反射率或高次谐波 benchmark。

还需要再补一句边界：`laser_ion` 当前并不是“多物理全开”的综合 benchmark。它的输入确实给了三条可切换分叉：

- `hydrogen.do_field_ionization = 1`
- `collisions.collision_names = ...`
- 将来再接 `do_qed_*`

但在当前 regression 版本里，这些开关都没有同时启用。它真正激活的是“Gaussian laser + 预电离 target + full/time-averaged/reduced diagnostics”。因此更准确的写法应该是：`laser_ion` 提供了一个 laser-target 骨架，field ionization、collisions 和 QED 都可以从这个骨架分叉出去，但它们各自的物理正确性仍然主要由 `field_ionization/`、`collision/`、`qed/` 这些独立 regression 目录兜底，而不是由 `analysis_test_laser_ion.py` 一次性证明。

从源码链看，这三条分叉接入的位置也不同。field ionization 在 species 构造期只先记住 `do_field_ionization`，真正的 `InitIonizationModule()`、`mapSpeciesProduct()` 和 `doFieldIonization()` 要到 `MultiParticleContainer::InitMultiPhysicsModules()` 与推进循环里才发生；collisions 则走 `CollisionHandler` 和 `collision_names`，并额外受 `collisions.split_momentum_push` 的 operator ordering 影响；QED 又只在 `#ifdef WARPX_QED` 编译路径下才会继续增加 `opticalDepthQSR/BW`、product species 映射和 `InitQED()`。所以，`laser_ion` 更适合承担“应用输入如何把这些模块挂到同一目标骨架上”的说明，而不应把不同层级的验证合同混写成一条单一主链。

## 3A.12 初始化验证入口：哪些 regressions 真正在兜底

前面的 3A.1-3A.11 讲的是“源码如何初始化”；但如果没有本地 regressions 对照，这些讲解很容易停留在静态阅读层。当前 WarpX 对 `Initialization` 的验证并没有集中在一个目录里，而是分散在几组物理 test 中。

第一组是 `Langmuir`。它通常被当成 evolve 基准，但对初始化同样关键，因为它直接覆盖：

- `NUniformPerCell`
- `profile=constant`
- `parse_momentum_function`
- 周期边界下的初始粒子/场一致性

例如 `analysis_1d.py` 的主断言不是 checksum，而是把输出 `Ez` 与理论 Langmuir 波逐点比较：

```python
E_sim = data[("mesh", field)].to_ndarray()[:, 0, 0]
E_th = get_theoretical_field(field, t0)
max_error = abs(E_sim - E_th).max() / abs(E_th).max()
assert error_rel < tolerance_rel
check_charge_conservation(data)
```

这意味着 `Langmuir` 不只是“时间推进跑通”，而是在验证 parser 形式的初始扰动确实经过 `PlasmaInjector`、`SpeciesUtils` 和 `AddPlasma()` 正确落到了粒子和场上。

第二组是 `space_charge_initialization`。它最直接对应 `species.initialize_self_fields = 1` 这条初始化支线。输入文件显式打开：

```text
beam.injection_style = "gaussian_beam"
beam.initialize_self_fields = 1
beam.momentum_distribution_type = "at_rest"
```

而 analysis 脚本把输出 `Ex/Ey/Ez` 与高斯电荷团理论场直接比较。因此这组 test 实际上在硬验证：

1. `gaussian_beam` 初始粒子云生成正确；
2. `InitData()` 检测到 `has_initialize_self_fields`；
3. `ComputeSpaceChargeField(reset_fields=false)` 在第一个时间步前给出了正确的 Coulomb 场。

第三组是 `dive_cleaning`。它验证的不是 projection cleaner，而是：

- 初始 Gaussian beam 状态进入演化后，
- `warpx.do_dive_cleaning = 1` 与 PML 能否把 `div(E)-rho/\epsilon_0` 误差传播并吸收掉，
- 最终场是否回到理论 Gaussian beam 电场。

第四组是 `gaussian_beam` / `external_file`。这里要分两半看：

1. `analysis_focusing_beam.py` 和 `analysis_rotated_beam.py` 分别验证 `focal_distance`、束斑统计、旋转位置和旋转动量；
2. `inputs_test_3d_focusing_gaussian_beam_from_openpmd_prepare.py` + `inputs_test_3d_focusing_gaussian_beam_from_openpmd` 则覆盖 `external_file` openPMD 粒子注入合同，包括 `weighting`、`mass`、`charge`、`positionOffset` 和 `momentum.unit_SI = m_e c`。

这一组现在还能再细一层：

- `inputs_test_3d_focusing_gaussian_beam_photons` 不是新物理 benchmark，而是把同一聚焦束斑统计合同重复到 `species_type = photon` 路径；
- `inputs_test_3d_gaussian_beam_picmi.py` 则主要覆盖 PICMI `GaussianBunchDistribution` 前端到 runtime attributes 的接线，当前主要依赖 checksum，而不是独立理论断言。

这里还要诚实记录一个当前本地 checkout 的边界：`gaussian_beam/CMakeLists.txt` 给 `test_3d_focusing_gaussian_beam_from_openpmd` 指定了 `analysis.py`，但 `Examples/Tests/gaussian_beam/` 目录下当前没有这个文件。因此对这条回归，最稳妥的说法是：

- openPMD 输入路径以及 `prepare -> inject -> checksum` workflow coverage 明确存在；
- PICMI 版本有显式 `analysis_focusing_beam.py` 物理断言；
- 原生 inputs 版本的 analysis 脚本在当前 checkout 中仍需额外核对。

第五组是 electrostatic / EB 初始化：

- `effective_potential_electrostatic` 用电子径向密度和解析 adiabatic expansion 基准比较，验证 effective-potential electrostatic solver；
- `electrostatic_sphere_eb` 则用 `ChargeOnEB` reduced diag 和 `eb_covered` 场，验证 `InitEB()`、Poisson 边界条件和带导体球的初始势问题。

最后一组是 `projection_div_cleaner`，它对应 3A.11 的 Poisson projection，而不是演化阶段的 `do_dive_cleaning`。当前本地 tests 已覆盖：

1. RZ openPMD 文件外场版本；
2. 3D PICMI 文件外场版本；
3. Python callback 版本；
4. 2D 解析外场版本。

这些脚本的共同断言都是：初始化完成后，从 `raw` staggered `Bx_aux/By_aux/Bz_aux` 重建的离散 `divB` 必须足够接近零。

这里也要区分强断言的位置：

- `test_rz_projection_div_cleaner` 的强断言在独立 `analysis.py` 里；
- `test_3d_projection_div_cleaner_picmi`、`test_3d_projection_div_cleaner_callback_picmi` 和 `test_2d_projection_div_cleaner_initial_analytical_field_picmi` 则都把 `divB` 断言直接写在输入脚本尾部，所以 `CMakeLists.txt` 里虽然 `analysis=OFF`，但并不等于这些条目只是 checksum-only。

再往 species 入口侧补一组，本地还有一个直接锚定 `setupNFluxPerCell()` 的 regression 家族：`Examples/Tests/flux_injection/`。这组 tests 分三条：

1. `analysis_flux_injection_3d.py`
   - 对 3D `NFluxPerCell` 场景同时检查总发射量、法向 Gaussian-flux 分布和切向 Gaussian 分布；
2. `analysis_flux_injection_rz.py`
   - 对 `flux_normal_axis = t` 的 RZ 连续注入检查粒子始终停留在预期 Larmor 半径带，并保持正确总通量；
3. `analysis_flux_injection_from_eb.py`
   - 对 `inject_from_embedded_boundary = 1` 的 2D/3D/RZ 变体检查发射总数、法向/切向速度统计，以及粒子不会落入 EB 内部。

因此 `flux_injection` 的意义不是普通 emitter 示例，而是 `NFluxPerCell`、Gaussian-flux rejection sampling 和 embedded-boundary surface emission 这三条运行态合同的直接验证入口。

因此，把本章和 regression 对上之后，`Initialization` 目前可以压成这样一张验证图：

- parser 初始化与常规粒子装填：`Langmuir`
- `gaussian_beam` 与束流几何：`focusing_gaussian_beam`、`rotated_gaussian_beam`
- openPMD 粒子文件注入：`focusing_gaussian_beam_from_openpmd*`
- 初始 self-field：`space_charge_initialization`
- electrostatic / effective potential / EB：`effective_potential_electrostatic`、`electrostatic_sphere_eb*`
- projection cleaner：`projection_div_cleaner*`
- `NFluxPerCell` / flux injection：`flux_injection*`
- 演化态 `div(E)` cleaning：`dive_cleaning`

这张图的意义不在于宣称“初始化层已经被完全证明”，而在于把三类情况分清：

1. 已有显式物理量 hard assert 的路径；
2. 当前主要靠 checksum regression 的路径；
3. 像 `gaussian_beam` 原生 openPMD variant 这样，在本地 checkout 里还存在脚本缺口、需要后续单独核对的路径。

再补两组之后，这张验证图就不再只覆盖“场和束流自场”，也开始覆盖初始化分布 API 本身。

第一组是 `initial_distribution`。它不是普通 smoke test，而是一组多 species、多分布的综合强基准：同一输入里同时覆盖

- `gaussian`
- `maxwell_boltzmann`
- `maxwell_juttner`
- `gaussian_beam`
- parser 温度
- parser bulk velocity
- `uniform`
- parser-Gaussian 动量统计

analysis 脚本把 reduced histogram、束斑统计和解析分布逐条对照。这意味着它真正验证的是 `PlasmaInjector`、`SpeciesUtils` 和 momentum-dispatch 层的 built-in / parser 初始化合同，而不只是“粒子能被建出来”。

第二组是 `initial_plasma_profile`。这组当前没有独立 `analysis.py`，只有 checksum helper，但输入本身非常明确：

- `injection_style = NUniformPerCell`
- `profile = parse_density_function`

并把横向 parabolic channel 与纵向 ramp / plateau / ramp 组合成二维电子密度。所以它更准确地是：

- `parse_density_function` 抛物型通道初始化的 checksum-only 基线

而不是应继续留在 `general / to classify` 的未知条目。

再往 `initialize_self_fields` 这一支补一组，本地还有一个更小但更干净的两体基准：`repelling_particles`。它只放两个同号 `SingleParticle` species，却同时打开：

- `electron1.initialize_self_fields = 1`
- `electron2.initialize_self_fields = 1`

analysis 随后从连续 plotfiles 读取两粒子的间距和速度，并用两体排斥的非相对论能量守恒关系构造理论 `\beta(d)`。因此这组 regression 的真实意义不是“一对粒子大概会分开”，而是：

1. 初始 electrostatic self-field 确实被建立起来；
2. 后续 pusher 对这份初始场的消费是对的；
3. 两者联立后能回到解析两体减速关系。

接着把另外三组容易落单的入口也补上之后，初始化验证图还能再细一层。

第一组是 `load_external_field`。它不是普通粒子轨道测试，而是在验证两套初始化合同：

1. grid external field：
   - `LoadExternalFields()`
   - `ReadExternalFieldFromFile()`
   - `Bfield_fp_external/Efield_fp_external`
   - `AddExternalFields()`
2. particle external field：
   - `Particles/ExternalParticleFields.cpp`
   - `m_B_ext_particle_s / m_E_ext_particle_s`
   - `B_external_particle_field/E_external_particle_field`
   - `GetExternalFields.cpp`

`analysis_3d.py` / `analysis_rz.py` 通过磁镜中的单粒子最终位置做硬断言，说明这组 regression 同时验证了“初始化写场”和“后续 gather 消费场”的接口契合。时间依赖变体 `analysis_time_scaling.py` 则不看粒子，而是直接比较两个时刻 plotfile 上 `B` 分量的缩放比，从而验证 `read_fields_*_dependency(t)` parser 和多 field map 的时间缩放合同。

这组 family 里还要再区分一层 restart 保真。当前活跃的三条最小入口是：

- `test_3d_load_external_field_particle_time_restart`
- `test_rz_load_external_field_grid_restart`
- `test_rz_load_external_field_particles_restart`

它们都只是：

- 先继承对应非 restart 输入
- 再通过 `amr.restart = ../.../chk000150` 从中间 checkpoint 恢复
- 然后复用 `analysis_default_restart.py` 逐字段比较 restart 与非 restart 输出

因此这三条 regression 验证的不是新的外场 physics，而是：

1. `read_from_file` 的 grid external field 状态能否在 restart 后保持一致；
2. `read_from_file` / dependency parser 的 particle external field 状态能否在 restart 后保持一致；
3. 初始化阶段构造出的 external-field 寄存器，不会在 checkpoint/restart 边界上丢失或漂移。

第二组是 `relativistic_space_charge_initialization`。它的输入和普通 `space_charge_initialization` 一样也打开了：

```text
beam.initialize_self_fields = 1
beam.injection_style = "gaussian_beam"
```

但束流动量改成了 relativistic：

```text
beam.uz = 100.0
```

因此这组 regression 实际验证的是 `RelativisticExplicitES::ComputeSpaceChargeField()`，而不再只是静止高斯电荷团的 Coulomb 场。analysis 脚本把 `Ex` 与理论值比较，并检查 `By` 是否满足相对论束流自场的 `By \approx Ex/c` 结构。这说明 `initialize_self_fields` 在 relativistic solver 分支下对应的是另一份初始化合同。

第三组是 `open_bc_poisson_solver`。它把四个条件绑在一起：

```text
boundary.field_lo = open open open
boundary.field_hi = open open open
warpx.do_electrostatic = relativistic
warpx.poisson_solver = fft
electron.initialize_self_fields = 1
```

同时粒子不是 `gaussian_beam`，而是 `parse_density_function + NUniformPerCell`。analysis 脚本用 Basseti-Erskine 公式逐个 `z` 截面比较 `Ex/Ey`，因此它验证的不是一般的 electrostatic 初始化，而是：

- open boundary
- relativistic bunch
- FFT Poisson
- 以及可选 `warpx.use_2d_slices_fft_solver = 1`

共同定义的初始 Poisson 解是否正确。

把这些补进去以后，初始化章节的本地回归证据就可以更完整地压成：

1. parser 初始化与常规宏粒子装填：`Langmuir`
2. `gaussian_beam` 注入几何：`focusing_gaussian_beam`、`rotated_gaussian_beam`
3. openPMD 粒子文件注入：`focusing_gaussian_beam_from_openpmd*`
4. lab-frame 初始 self-field：`space_charge_initialization`
5. relativistic 初始 self-field：`relativistic_space_charge_initialization`
6. electrostatic / effective potential / EB：`effective_potential_electrostatic`、`electrostatic_sphere_eb*`
7. 外部 grid / particle fields：`load_external_field*`
8. projection cleaner：`projection_div_cleaner*`
9. 开放边界 relativistic Poisson 初始化：`open_bc_poisson_solver*`
10. 演化态 `div(E)` cleaning：`dive_cleaning`

这样第 3A 章就不再只是“源码怎么走”，而是已经能回答“这些初始化合同在本地 WarpX 里分别由哪组 regression 兜底”。

继续补入 `load_density`、`magnetostatic_eb` 和 `nodal_electrostatic` 之后，这张验证地图还要再加三层。

第一层是 `load_density`。这组 regression 的输入明确使用：

```text
electrons.profile = "read_from_file"
electrons.read_density_from_path = "../test_*_load_density_prepare/example-density.h5"
electrons.do_continuous_injection = 1
warpx.do_moving_window = 1
```

源码上它直接对应 `SpeciesUtils::parseDensity()` 里 `profile = read_from_file` 分支，把 openPMD density mesh 装进 `InjectorDensityFromFile`，然后交给 `PlasmaInjector` 和连续注入主链消费。analysis 脚本则逐个 iteration 读取 diagnostics 中的 `rho`，与 prepare 脚本定义的 ramp / parabolic channel profile 比较。因此 `load_density` 验证的不是一般 I/O，而是“file-driven density profile + moving-window 连续注入”这条初始化合同。

第二层是 `magnetostatic_eb`。原生 inputs 文件把：

```text
warpx.do_electrostatic = labframe-electromagnetostatic
beam.initialize_self_fields = 1
warpx.eb_implicit_function = "(x**2+y**2-radius**2)"
warpx.eb_potential(x,y,z,t) = "1."
```

绑在一起，而 `WarpXInitData.cpp` 的 fresh-run 分支会在 `ComputeSpaceChargeField(reset_fields)` 之后继续调用 `ComputeMagnetostaticField()`。所以这组 test 验证的是 embedded boundary、边界 potential、初始 self-field 和 magnetostatic solve 在初始化阶段的联动。这里还必须区分两层证据：原生 `inputs_test_3d_magnetostatic_eb` 目前主要由 checksum 兜底；两个 PICMI 输入文件则在 `sim.step()` 之后内嵌了解析 `E_r/B_\theta` 误差断言，因此它们不是简单的 checksum-only regression。

第三层是 `nodal_electrostatic`。这组输入把：

```text
warpx.do_electrostatic = relativistic
warpx.grid_type = collocated
beam_p.initialize_self_fields = 1
beam_p.do_qed_quantum_sync = 1
```

放在同一条链上。它的 analysis 不直接比较 `E/B`，而是用 reduced diagnostics 断言 `ParticleExtrema_beam_p` 给出的最大 `chi` 极小，且 `ParticleNumber` 中 photon 数始终为零。也就是说，这组 regression 验证的是 collocated relativistic electrostatic 初始 self-field 没有制造出会假触发 QED 的非物理场，它更准确地是一个“零触发基准”。

把这三组再并进来以后，初始化章节的本地回归证据可以进一步压成：

1. parser 初始化与常规宏粒子装填：`Langmuir`
2. `gaussian_beam` 注入几何：`focusing_gaussian_beam`、`rotated_gaussian_beam`
3. openPMD 粒子文件注入：`focusing_gaussian_beam_from_openpmd*`
4. file-driven density profile 与连续注入：`load_density*`
5. lab-frame 初始 self-field：`space_charge_initialization`
6. relativistic 初始 self-field：`relativistic_space_charge_initialization`
7. effective-potential electrostatic：`effective_potential_electrostatic`
8. electrostatic / magnetostatic / EB 联合初始化：`magnetostatic_eb*`
9. electrostatic / EB Poisson：`electrostatic_sphere_eb*`
10. 外部 grid / particle fields：`load_external_field*`
11. projection cleaner：`projection_div_cleaner*`
12. collocated relativistic electrostatic 零触发基准：`nodal_electrostatic`
13. 开放边界 relativistic FFT Poisson 初始化：`open_bc_poisson_solver*`
14. 演化态 `div(E)` cleaning：`dive_cleaning`

这样 `nodal_electrostatic`、`open_bc_poisson_solver` 和 `relativistic_space_charge_initialization` 就不再需要继续共用一个过粗的 `electrostatic / Poisson` 桶。它们分别对应的是：

- collocated relativistic electrostatic 零触发基准
- open boundary + FFT/sliced FFT 的 relativistic Poisson 初始化
- relativistic Gaussian beam 的初始 self-field

不过还有一组此前仍容易被写得过粗：`electrostatic_sphere`。它不该和一般 `Poisson` 条目混成一桶，因为它真正验证的是“一个静止均匀电子球在自身 Coulomb 场下膨胀”这条自场初始化主链。`analysis_electrostatic_sphere.py` 的第一层断言是解析电场对照：脚本用最终输出时间 `t_max` 反解球半径 `r_end`，再构造内外球解析 `E(r)`，沿坐标轴比较 `Ex/Ey/Ez` 或 RZ 下的 `Er/Ez` 的相对 `L2` 误差。这意味着它验证的不只是 solver 跑通，而是：

1. 初始电子球几何是否被正确装填；
2. 初始自场是否正确建立；
3. 后续 electrostatic 演化是否仍与解析膨胀解一致。

这组 test 的第二层断言只在 lab-frame 变体上才打开。只有当输入显式要求：

```text
warpx.do_electrostatic = labframe
diag2.electron.variables = x y z ux uy uz w phi
```

analysis 才会利用粒子 `phi` 重建：

- 动能
- 自场势能 `0.5 \sum w q \phi`

并检查初末总能量。也就是说：

- 所有 `electrostatic_sphere` 变体都做解析电场对照；
- 只有写出 `phi` 的 lab-frame 版本额外验证能量账本。

各输入变体的角色也不同：

- `inputs_test_3d_electrostatic_sphere`
  - 3D relativistic electrostatic 自场膨胀基线
- `inputs_test_3d_electrostatic_sphere_lab_frame`
  - lab-frame 自场膨胀 + 能量守恒
- `inputs_test_3d_electrostatic_sphere_lab_frame_mr_emass_10`
  - lab-frame + MR；`electron.mass = 10` 主要是减慢膨胀，便于短步数比较
- `inputs_test_3d_electrostatic_sphere_rel_nodal`
  - `warpx.grid_type = collocated`，验证 collocated electrostatic 布局
- `inputs_test_3d_electrostatic_sphere_adaptive`
  - adaptive-dt 变体；analysis 仍用实际 `t_max` 做强对照
- `inputs_test_rz_electrostatic_sphere`
  - RZ 自场膨胀 + 能量守恒
- `inputs_test_rz_electrostatic_sphere_uniform_weighting`
  - 再额外覆盖 `radial_numpercell_power = 1.` 的 uniform-weighting 粒子装填

另外，这组目录下还有两个容易误读的文件：

- `analysis_default_regression.py` 只是通用 checksum helper；
- `catalyst_pipeline.py` 只是 ParaView Catalyst 的可视化脚本。

因此，`electrostatic_sphere` 在初始化验证图里更准确的位置应单独写成：

14. electrostatic self-field expansion：`electrostatic_sphere*`

还剩另外两组此前也容易被写得过粗，但它们和 `electrostatic_sphere` 不是一类问题。

第一组是 `electrostatic_dirichlet_bc`。这组不是带电粒子自场 benchmark，而是纯粹在验证时变边界势是否真正进入 electrostatic 解。输入直接设置：

```text
warpx.do_electrostatic = labframe
boundary.potential_lo_x = 150.0*sin(2*pi*6.78e+06*t)
boundary.potential_hi_x = 450.0*sin(2*pi*13.56e+06*t)
diag1.fields_to_plot = phi
```

analysis 并不读取内部粒子量，而是逐个输出时刻取两侧边界上的平均 `phi`，然后与理论正弦函数比较。因此它测的不是一般 `Poisson` 正确性，而是：

- `boundary.potential_lo_x / potential_hi_x`
- time-dependent parser
- electrostatic Dirichlet boundary condition
- diagnostics 中 `phi` 的边界保真

PICMI 变体只是在 `Cartesian2DGrid(..., lower_boundary_conditions=["dirichlet", ...])`、`warpx_potential_lo_x`、`warpx_potential_hi_x` 这一层重复同一件事，所以它更准确的归类是：

15. time-dependent electrostatic boundary driving：`electrostatic_dirichlet_bc*`

第二组是 `effective_potential_electrostatic`。这组当前只有一个 PICMI test，而且它验证的也不是一般意义上的 electrostatic `phi` 场，而是 `warpx_effective_potential=True` 这条 solver 分叉是否能在导体球约束下复现绝热膨胀 benchmark。PICMI 输入脚本同时做了三件关键事：

1. 用 `GaussianBunchDistribution` 初始化电子和离子球团；
2. 加入导体球 embedded boundary；
3. 选择：

```python
picmi.ElectrostaticSolver(
    method="Multigrid",
    warpx_effective_potential=True,
    warpx_effective_potential_factor=C_EP,
)
```

analysis 则从 `sim_parameters.dpkl` 读回参数，构造 Connor et al. 风格的绝热膨胀近似电子密度，再把 openPMD 中的 `rho_electrons` 变成径向密度曲线，与理论值逐个输出时刻比较 RMS 误差。因此它的真实验证对象是：

- effective-potential electrostatic solver
- PICMI front-end
- 导体球约束下的电子密度膨胀近似

更准确的归类应是：

16. effective-potential electrostatic：`effective_potential_electrostatic`

## 3A.13 本章小结：初始化状态怎样进入第一步推进

到 `InitData()` 结束时，WarpX 已经完成：

```text
inputs
  -> WarpX::ReadParameters()
  -> WarpX::InitData()
  -> InitFromScratch or InitFromCheckpoint
  -> AMReX levels and WarpX field data
  -> external fields
  -> species PlasmaInjector
  -> AddParticles / AddPlasma / AddGaussianBeam / AddPlasmaFromFile
  -> projection div cleaner if needed
  -> initial diagnostics
  -> Evolve()
```

这个状态才是 PIC 时间推进的初始条件。后续 `Evolve()`、`OneStep()`、`PushParticlesandDeposit()`、field solver 和 diagnostics 都在这个已经离散化、分布式、带权重和边界条件的状态上工作。

后续扩写方向：

- 把 `InitLevelData()` 中每一类 field allocation 展开到 root/fieldsolver 章节；
- 把 Gaussian beam 的 emittance/focal distance 公式结合 accelerator beam optics 文献继续推导；
- 把 openPMD 文件格式与 WarpX 单位约定加入诊断/I/O 章节；
- 判断 initialization 验证层是否已经阶段性收口，并切回下一未完成模块。
