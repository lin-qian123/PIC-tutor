# `ReadParameters()` 组合约束：grid、gather、deposition、filter、implicit 如何塑造后续初始化

绑定源码：

- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Initialization/WarpXInitData.cpp`

这篇笔记只处理一个问题：`ReadParameters()` 里看似分散的算法开关，怎样在构造期就决定后面会不会分配某些 `MultiFab`、会不会创建 implicit solver、以及 `ProjectionDivCleaner` 和粒子容器要不要准备额外状态。

## 1. `grid_type` 不是局部参数，而是后续 index type 的上游总开关

`ReadParameters()` 先把 `grid_type`、`field_gathering_algo`、`do_current_centering` 串成一组硬约束。

源码位置：`../warpx/Source/WarpX.cpp:1118-1186, 1296-1346`。

```cpp
if (grid_type == GridType::Hybrid)
{
    do_current_centering = true;
}

pp_warpx.query("do_current_centering", do_current_centering);
if (do_current_centering)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        grid_type == GridType::Hybrid,
        "warpx.do_current_centering=1 can be used only with warpx.grid_type=hybrid");
}

if (!pp_algo.query("field_gathering", tmp_algo))
{
    if (grid_type == GridType::Hybrid)
    {
        field_gathering_algo = GatheringAlgo::MomentumConserving;
    }
}
else
{
    if (grid_type == GridType::Hybrid)
    {
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            field_gathering_algo == GatheringAlgo::MomentumConserving,
            "Hybrid grid ... should be used only with momentum-conserving field gathering");
    }
}
```

这里的真实语义不是“hybrid grid 推荐配 momentum-conserving gather”，而是：

1. `grid_type=Hybrid` 会先把 `do_current_centering` 推成默认真值。
2. 用户若显式要求 `do_current_centering=1`，源码反过来要求 grid 必须是 `Hybrid`。
3. `Hybrid` 又反过来强制 field gather 必须是 `MomentumConserving`。

所以这三者构成的是一组单向收紧的组合约束，不是彼此独立的选项。

这组约束在 level 分配阶段会直接落成：

源码位置：`../warpx/Source/WarpX.cpp:2271-2342, 2480-2513, 2784-2830`。

```cpp
const bool aux_is_nodal = (field_gathering_algo == GatheringAlgo::MomentumConserving);

AllocLevelMFs(..., aux_is_nodal);

if (do_current_centering)
{
    amrex::BoxArray const& nodal_ba = amrex::convert(ba, amrex::IntVect::TheNodeVector());
    m_fields.alloc_init(FieldType::current_fp_nodal, Direction{0}, lev, nodal_ba, dm, ncomps, ngJ, 0.0_rt);
    ...
}

if (aux_is_nodal and grid_type != GridType::Collocated)
{
    BoxArray const nba = amrex::convert(ba,IntVect::TheNodeVector());
    m_fields.alloc_init(FieldType::Bfield_aux, Direction{0}, lev, nba, dm, ncomps, ngEB, 0.0_rt);
    ...
}
```

也就是说，`ReadParameters()` 这一组选择后面至少控制三件事：

- 是否额外分配 `current_fp_nodal`
- `aux` 场是否变成真正的 nodal `MultiFab`
- 后续 coarse-fine `cax`、buffer gather 和 field centering 是否走 nodal 路径

## 2. `field_centering_nox/noy/noz` 只在特定组合下才有意义

源码位置：`../warpx/Source/WarpX.cpp:1511-1538`。

```cpp
if ((WarpX::field_gathering_algo == GatheringAlgo::MomentumConserving
    && WarpX::grid_type != GridType::Collocated)
    || WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic)
{
    utils::parser::queryWithParser(pp_warpx, "field_centering_nox", field_centering_nox);
    ...
    ::AllocateCenteringCoefficients(...);
}
```

这意味着高阶 field centering 并不是所有模拟都在用。只有两类路径真正消费它：

- staggered/hybrid grid 上的 momentum-conserving gather
- `LabFrameElectroMagnetostatic`

如果后面 `maxLevel()>0`，源码还会进一步卡死：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    field_centering_nox == 2 && field_centering_noy == 2 && field_centering_noz == 2,
    "High-order centering of fields ... is not implemented with mesh refinement");
```

所以这组参数不是“想升几阶就升几阶”，而是会直接改变：

- 是否分配 centering stencil 系数
- AMR 是否允许当前组合继续运行

## 3. current deposition 不是独立于 solver 的

源码位置：`../warpx/Source/WarpX.cpp:1218-1293, 1636-1689`。

```cpp
if (electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD ||
    electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC ||
    electrostatic_solver_id != ElectrostaticSolverAlgo::None) {
    current_deposition_algo = CurrentDepositionAlgo::Direct;
}

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    WarpX::current_deposition_algo != CurrentDepositionAlgo::Vay ||
    !do_current_centering,
    "Vay deposition not implemented with current centering");

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    WarpX::current_deposition_algo != CurrentDepositionAlgo::Vay ||
    maxLevel() <= 0,
    "Vay deposition not implemented with mesh refinement");

if (WarpX::current_deposition_algo == CurrentDepositionAlgo::Vay) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD,
        "Vay deposition is implemented only for PSATD");
}
```

这里最重要的不是 `Vay` 自己的限制，而是源码把 deposition 和 solver、AMR、current centering 连成了一个组合空间：

- `PSATD / HybridPIC / electrostatic` 默认把 deposition 拉回 `Direct`
- `Vay` 只能配 `PSATD`
- `Vay` 不能配 mesh refinement
- `Vay` 不能配 `do_current_centering`

这条链随后会直达字段分配：

源码位置：`../warpx/Source/WarpX.cpp:2505-2513`。

```cpp
if (WarpX::current_deposition_algo == CurrentDepositionAlgo::Vay)
{
    m_fields.alloc_init(FieldType::current_fp_vay, Direction{0}, lev, amrex::convert(ba, rho_nodal_flag), dm, ncomps, ngJ, 0.0_rt);
    ...
}
```

所以 `algo.current_deposition=vay` 不只是切换一个 kernel，而是让初始化阶段多出一套 `current_fp_vay` 存储契约。

## 4. implicit evolve scheme 会提前改写粒子与场的初始化前置条件

源码位置：`../warpx/Source/WarpX.cpp:1247-1364`。

```cpp
if (evolve_scheme == EvolveScheme::SemiImplicitEM) {
    m_implicit_solver = std::make_unique<SemiImplicitEM>();
}
else if (evolve_scheme == EvolveScheme::ThetaImplicitEM) {
    m_implicit_solver = std::make_unique<ThetaImplicitEM>();
}
else if (evolve_scheme == EvolveScheme::StrangImplicitSpectralEM) {
    m_implicit_solver = std::make_unique<StrangImplicitSpectralEM>();
}

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    current_deposition_algo == CurrentDepositionAlgo::Esirkepov ||
    current_deposition_algo == CurrentDepositionAlgo::Villasenor ||
    current_deposition_algo == CurrentDepositionAlgo::Direct,
    "Only Esirkepov, Villasenor, or Direct current deposition supported ...");

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee ||
    electromagnetic_solver_id == ElectromagneticSolverAlgo::CKC ||
    electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD,
    "Only the Yee, CKC, and PSATD EM solvers are supported ...");

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    particle_pusher_algo == ParticlePusherAlgo::Boris ||
    particle_pusher_algo == ParticlePusherAlgo::HigueraCary,
    "Only the Boris and Higuera particle pushers are supported ...");

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    field_gathering_algo != GatheringAlgo::MomentumConserving,
    "With implicit and semi-implicit schemes, the momentum conserving field gather is not supported ...");
```

所以 implicit 这里已经不是一个“后面场求解器内部再决定”的局部选项。`ReadParameters()` 直接把：

- current deposition
- EM solver
- particle pusher
- field gather

全部压成了一个可行组合。

这条组合随后在 `InitFromScratch()` 前就开始落地：

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:999-1003`。

```cpp
if (m_implicit_solver) {
    m_implicit_solver->Define(this,/*from_restart=*/false);
    m_implicit_solver->CreateParticleAttributes();
}
```

而在 `AllocLevelMFs()` 里又继续落成额外字段：

源码位置：`../warpx/Source/WarpX.cpp:2480-2497`。

```cpp
if (m_implicit_solver) {
    m_fields.alloc_init(FieldType::current_fp_non_suborbit, Direction{0}, lev, ...);
    ...
    m_fields.alloc_init(FieldType::E_old, Direction{0}, lev, ...);
    ...
}
```

因此 implicit 的真实初始化影响至少包括：

- 构造期就实例化 `m_implicit_solver`
- `InitFromScratch()` 之前就向粒子容器注册额外 runtime attributes
- level 分配时额外分配 `current_fp_non_suborbit` 和 `E_old`

## 5. particle shape、species/lasers 存在性和排序策略是绑在一起的

源码位置：`../warpx/Source/WarpX.cpp:1404-1499`。

```cpp
if (!species_names.empty() || !lasers_names.empty()) {
    if (utils::parser::queryWithParser(pp_algo, "particle_shape", particle_shape)){
        ...
        nox = particle_shape;
        noy = particle_shape;
        noz = particle_shape;
    }
    else{
        WARPX_ABORT_WITH_MESSAGE(
            "algo.particle_shape must be set in the input file:");
    }

    if (evolve_scheme == EvolveScheme::ThetaImplicitEM ||
        evolve_scheme == EvolveScheme::StrangImplicitSpectralEM) {
        pp_particles.query("max_grid_crossings", particle_max_grid_crossings);
    }

#ifdef AMREX_USE_GPU
    sort_intervals_string_vec = {"4"};
#else
    sort_intervals_string_vec = {"-1"};
#endif
}
```

这里可以看出三件事：

1. 只要存在粒子 species 或 laser species，`algo.particle_shape` 就从“普通参数”升级成强制参数。
2. `particle_shape` 直接决定 `nox/noy/noz`，因此会继续影响 guard cells、deposition stencil、filter 需求和 load-balance 成本模型。
3. 默认排序间隔不是固定值，而是“只有存在粒子/laser 时才启用按平台区分的默认策略”。

换句话说，species 是否存在本身就在改写初始化默认值，而不是只影响后面的 `mypc->InitData()`。

## 6. `use_filter` 和 PSATD 不是两个平行开关

源码位置：`../warpx/Source/WarpX.cpp:684-741, 1636-1857, 2277-2299`。

```cpp
if (evolve_scheme != EvolveScheme::Explicit) {
    use_filter = false;
}

if (WarpX::current_deposition_algo == CurrentDepositionAlgo::Esirkepov ||
    WarpX::current_deposition_algo == CurrentDepositionAlgo::Villasenor ||
    WarpX::current_deposition_algo == CurrentDepositionAlgo::Vay ||
    WarpX::do_dive_cleaning)
{
    current_correction = false;
}

if (m_JRhom) { current_correction = false; }
```

PSATD 路径里真正被同时耦合的是：

- `use_filter`
- `current_correction`
- `update_with_rho`
- `m_JRhom`
- `v_galilean`
- `v_comoving`
- `current_deposition_algo`

例如：

- `Vay` 不能和 `JRhom` 共存
- `Vay` 不能和 `current_correction` 共存
- `Esirkepov/Villasenor` 不能和 Galilean / comoving PSATD 共存
- implicit scheme 默认先把 `use_filter` 关掉

这组约束最后还会反射到分配层，因为 `AllocLevelData()` 会先 `InitFilter()`，再让 `guard_cells.Init(...)` 把 filter stencil 长度也纳入 guard-cell 配额模型：

```cpp
if (use_filter)
{
    InitFilter();
}

guard_cells.Init(
    ...,
    use_filter,
    bilinear_filter.stencil_length_each_dir);
```

所以 filter 不是“后面再额外卷积一次”的小功能，而是会改写 guard-cell、buffer 和场分配半径。

## 7. `m_do_initial_div_cleaning` 是 `ProjectionDivCleaner` 的上游门闩

源码位置：`../warpx/Source/WarpX.cpp:1130-1154`。

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

这说明初始化阶段的 `ProjectionDivCleaner` 不是“用户手动开一个布尔值就完了”。源码会先看：

- 外部 `B` 场是不是文件/parser 型
- 当前 EM solver 是不是支持这条清理路径
- `do_divb_cleaning` 是否已经承担了演化期散度控制

然后才派生出 `m_do_initial_div_cleaning`。

它的消费点在 `InitData()`：

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:875-883`。

```cpp
if (m_implicit_solver) {
    m_implicit_solver->PrintParameters();
}

if (m_do_initial_div_cleaning) {
    InitLevelData();
}
```

这里的重点不是具体函数名，而是初始化主链在真正生成初态前就已经要知道：

- 是不是需要为外部场准备额外读入和修正路径
- `ProjectionDivCleaner` 是否会参与初始场构造

因此 `m_do_initial_div_cleaning` 属于“启动层和参数层共同决定的初始化拓扑”，不是后处理选项。

## 8. 这组组合约束最后怎样汇总成对象和字段分配前提

把上面几条放在一起，`ReadParameters()` 到 `AllocLevelData()/InitFromScratch()` 的真实作用可以压成下面这张表：

| 上游组合 | 直接结果 | 后续初始化消费点 |
| --- | --- | --- |
| `grid_type=Hybrid` + momentum-conserving gather | `do_current_centering=true`、`aux_is_nodal=true` | `current_fp_nodal`、nodal `E/Bfield_aux`、后续 `cax`/buffer gather |
| `current_deposition_algo=Vay` | 只能配 `PSATD`、无 AMR、无 current centering | 额外分配 `current_fp_vay` |
| `evolve_scheme` 为 implicit 系列 | 构造 `m_implicit_solver`，限制 gather/pusher/deposition/solver | `Define()`、`CreateParticleAttributes()`、`current_fp_non_suborbit`、`E_old` |
| 存在 particle/laser species | 强制要求 `algo.particle_shape` | `nox/noy/noz`、guard cells、排序默认值、部分 implicit `max_grid_crossings` |
| `use_filter` 与 PSATD/JRhom/Galilean/comoving 组合 | 改写 current correction / guard-cell 需求 | `InitFilter()`、`guard_cells.Init(...)` |
| `m_do_initial_div_cleaning=true` | 初始散度清理路径启用 | `InitData()` 中进入 `ProjectionDivCleaner` 相关初态构造 |

结论很直接：`ReadParameters()` 并不是“把字符串参数翻译成成员变量”的轻量阶段。它已经在决定：

- 后面哪些对象会被创建
- 哪些 `MultiFab` 会被额外分配
- 粒子容器会不会提前注册 implicit/runtime attributes
- 初态场构造会不会插入 projection cleaning

所以从源码阅读顺序上，`ReadParameters()` 必须和 `AllocLevelData()`、`AllocLevelMFs()`、`InitFromScratch()` 连着看；只读前者而不追后续分配，容易把这些组合约束误读成普通输入检查。
