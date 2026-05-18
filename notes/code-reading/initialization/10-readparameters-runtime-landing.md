# `ReadParameters()`：从输入参数到运行态对象

绑定源码：

- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/WarpX.H`
- `../warpx/Source/Initialization/WarpXInit.cpp`

这一篇继续沿启动层往下，不再只问“哪些参数在构造前被锁定”，而是直接回答构造函数里的另一个核心问题：

1. `ReadParameters()` 读到的参数，哪些会直接改写 `WarpX` 成员状态。
2. 哪些成员状态会立刻决定后面创建什么容器、solver 对象或默认约束。
3. 哪些参数其实不是“普通配置”，而是对象存在性或兼容性条件。

## 1. 构造函数的主骨架

`WarpX::WarpX()` 的开头顺序是：

```cpp
warpx::initialization::initialize_warning_manager();

ReadParameters();

BackwardCompatibility();

if (EB::enabled()) { InitEB(); }

ablastr::utils::SignalHandling::InitSignalHandling();
...
mypc = std::make_unique<MultiParticleContainer>(this);
...
m_particle_boundary_buffer = std::make_unique<ParticleBoundaryBuffer>();
...
if (do_fluid_species) {
    myfl = std::make_unique<MultiFluidContainer>();
}
...
if ((electrostatic_solver_id == LabFrame) || ...) {
    m_electrostatic_solver = ...
}
...
if (electromagnetic_solver_id == HybridPIC) {
    m_hybrid_pic_model = std::make_unique<HybridPICModel>();
}
```

所以这条链的真实结构是：

1. 先读参数并做兼容性断言。
2. 再根据已经落到成员里的状态决定要不要创建：
   - 粒子容器
   - 粒子边界 buffer
   - 流体容器
   - 静电 solver
   - hybrid PIC model

这意味着 `ReadParameters()` 不只是“保存配置”，而是在为后半段构造函数决定对象图。

## 2. boosted-frame 与 moving window 在 `ReadParameters()` 里第一次落到真正成员

前一篇已经说明：

- `read_moving_window_parameters()` 在构造前先锁定了 `do_moving_window`、`moving_window_dir`、`moving_window_v`
- `ConvertLabParamsToBoost()` 在构造前先改写了 geometry/tagging 输入

到了 `ReadParameters()`，boost 参数又被正式读进 `WarpX` 运行态成员：

```cpp
ReadBoostedFrameParameters(gamma_boost, beta_boost, boost_direction);
```

然后立刻和运行时 geometry 发生真实兼容性检查：

```cpp
if (do_moving_window)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        Geom(0).isPeriodic(moving_window_dir) == 0,
        "The problem must be non-periodic in the moving window direction");
    moving_window_x = geom[0].ProbLo(moving_window_dir);
}
```

这一步之后，moving window 不再只是“全局开关”，而是已经多了一个和当前 `Geometry` 绑定的运行时位置锚点 `moving_window_x`。

再到构造函数后半段，它才真正落到粒子容器：

```cpp
if (do_moving_window){
    ...
    if (moving_window_v > 0._rt)
        pc.m_current_injection_position = geom[0].ProbHi(moving_window_dir);
    else if (moving_window_v < 0._rt)
        pc.m_current_injection_position = geom[0].ProbLo(moving_window_dir);
}
```

所以这一条链可以明确拆成三层：

1. 启动层先解析 moving-window 参数。
2. `ReadParameters()` 再检查它和 geometry 是否兼容，并落到 `moving_window_x`。
3. 构造函数后半段再把它写进每个粒子容器的连续注入位置。

## 3. solver 选择不是平行配置项，而是带覆盖关系的状态机

`ReadParameters()` 里先读：

```cpp
pp_warpx.query_enum_sloppy("do_electrostatic", electrostatic_solver_id, "-_");
```

然后立即有一条覆盖规则：

```cpp
if (electrostatic_solver_id != ElectrostaticSolverAlgo::None) {
    electromagnetic_solver_id = ElectromagneticSolverAlgo::None;
}
```

因此，electrostatic 并不是和 EM solver 并列可并存的一个标签，而是会主动把 Maxwell solver 置空。

后面构造函数再根据 `electrostatic_solver_id` 的最终值决定真正创建哪个对象：

```cpp
if ((electrostatic_solver_id == LabFrame)
    || (electrostatic_solver_id == LabFrameElectroMagnetostatic))
{
    m_electrostatic_solver = std::make_unique<LabFrameExplicitES>(nlevs_max);
}
else if (electrostatic_solver_id == LabFrameEffectivePotential)
{
    m_electrostatic_solver = std::make_unique<EffectivePotentialES>(nlevs_max);
}
else
{
    m_electrostatic_solver = std::make_unique<RelativisticExplicitES>(nlevs_max);
}
```

也就是说，哪怕用户最后没有走 electrostatic 主线，这里仍然会创建一个 electrostatic solver 对象，只是具体类型不同；真正的区别是：

- `electrostatic_solver_id`
- `poisson_solver_id`
- `electromagnetic_solver_id`

这三者在 `ReadParameters()` 里怎样彼此覆盖和约束。

## 4. `do_fluid_species` 不是后面看到 species 才随手生成，而是在 `ReadParameters()` 里先决定对象存在性

`ReadParameters()` 会先查：

```cpp
const ParmParse pp_fluids("fluids");
std::vector<std::string> fluid_species_names = {};
pp_fluids.queryarr("species_names", fluid_species_names);
do_fluid_species = !fluid_species_names.empty();
```

同时立刻施加兼容性约束：

- 不能和 mesh refinement 共存
- 不能和 relativistic electrostatic solver 共存
- RZ 下不能和 `n_rz_azimuthal_modes > 1` 共存

然后构造函数后半段才根据这个布尔值决定：

```cpp
if (do_fluid_species) {
    myfl = std::make_unique<MultiFluidContainer>();
}
```

所以 `do_fluid_species` 的语义不是“有没有流体物理”，而是“是否允许创建整个 `MultiFluidContainer` 子系统”。

## 5. `electromagnetic_solver_id` 也不仅影响算法路径，还直接控制额外对象图

一个最明显的例子是 Hybrid PIC：

在 `ReadParameters()` 中，`algo.maxwell_solver`、`algo.current_deposition`、`grid_type`、filter、gather、implicit 兼容性等逻辑会共同把 `electromagnetic_solver_id` 定到最终值。

然后构造函数里直接按这个值决定：

```cpp
if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC)
{
    m_hybrid_pic_model = std::make_unique<HybridPICModel>();
}
```

这说明 `electromagnetic_solver_id` 不是“后面 field push 时再 if 一下”的标签，而是对象图级别的分叉条件。

同理，`m_em_solver_medium == Macroscopic` 也会直接触发：

```cpp
m_macroscopic_properties = std::make_unique<MacroscopicProperties>();
```

## 6. `grid_type` 在这里是真正的几何/离散结构选择器

`ReadParameters()` 先读：

```cpp
pp_warpx.query_enum_sloppy("grid_type", grid_type, "-_");
```

然后它不只是影响后面某个 kernel，而是立刻改变多个默认和约束：

1. `grid_type == Collocated` 时，`galerkin_interpolation = false`
2. `grid_type == Hybrid` 时，默认打开：
   - 高阶 field centering
   - `do_current_centering = true`
   - 对应 centering order
3. cylindrical/spherical geometry 下禁止 `grid_type = hybrid`
4. RZ + PSATD 时强制：
   - `grid_type = collocated`
   - `galerkin_interpolation = false`

因此 `grid_type` 在 WarpX 里并不是“数值细节调味参数”，而是后续：

- nodal flags
- centering coefficients
- current/gather compatibility
- implicit / PSATD / HybridPIC 合法组合

这些状态的上游选择器。

## 7. `m_do_initial_div_cleaning` 的默认值其实是一个派生条件，不是简单布尔输入

`ReadParameters()` 里有一段特别值得单独拿出来：

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

这说明 `do_initial_div_cleaning` 的真实语义是：

1. 先根据外部 `B` 场读入类型、grid type、solver 组合自动推导一个“建议默认值”；
2. 再允许用户输入显式覆盖。

所以它不是像 `verbose` 那样直接 `query` 进来，而是一个“源码先推导默认，再由输入决定是否覆盖”的派生参数。

这也解释了为什么 `ProjectionDivCleaner` 那条初始化链必须和外部场类型、grid type、solver 选择一起看，而不能单看 `do_initial_div_cleaning` 一个开关。

## 8. `ParticleBoundaryBuffer` 的创建不依赖 diagnostics，但依赖整个粒子子系统存在

构造函数中：

```cpp
mypc = std::make_unique<MultiParticleContainer>(this);
...
m_particle_boundary_buffer = std::make_unique<ParticleBoundaryBuffer>();
```

这条顺序说明两件事：

1. boundary buffer 是 WarpX 粒子基础设施的一部分，不是 diagnostics 才临时创建的对象。
2. 它创建在 `MultiParticleContainer` 之后，因此默认就假设粒子 species / lasers 子系统已经存在，后面 `BoundaryScrapingDiagnostics` 和 Python wrapper 只是消费它。

这和之前 diagnostics 笔记里“writer 与 Python 共用同一份 buffer”是完全一致的。

## 9. `ReadParameters()` 的一部分工作，其实是在决定后面 sanity checks 会检查什么

构造函数源码里在 `MultiParticleContainer` 创建后还有一句注释：

```cpp
// Sanity checks. Must be done after calling the MultiParticleContainer
```

这说明 `ReadParameters()` 前半段虽然已经做了大量 compatibility assert，但还没结束。它先把：

- solver 选择
- species / laser 名称
- particle shape
- sorting
- grid type
- current centering
- fluid species

这些状态落到成员里，再由后面的容器构造和 sanity checks 继续验证“参数和真实 species/container 结构是否一致”。

因此，`ReadParameters()` 不能孤立看成“完整的参数验证器”，它只是构造期验证链的第一阶段。

## 10. 当前启动层到构造期可以压成一条更清楚的总链

到这里，这一整段源码可以总结成：

### 10.1 构造前锁定

- `check_dims()`
- `read_moving_window_parameters()`
- `ConvertLabParamsToBoost()`
- boundary parsing
- `CheckGriddingForRZSpectral()`

它们主要负责：

- 改 parser
- 锁全局静态状态
- 提前消化 boosted/RZ spectral/moving-window 这类会改输入语义的逻辑

### 10.2 构造期落地

- `initialize_warning_manager()`
- `ReadParameters()`
- `BackwardCompatibility()`
- `InitEB()`
- `MultiParticleContainer`
- `ParticleBoundaryBuffer`
- `MultiFluidContainer`
- electrostatic solver
- hybrid PIC model

它们主要负责：

- 把参数落成真正的 `WarpX` 成员
- 对象级分叉
- 容器/solver 实例化

这样分层之后，后面再看：

- `InitData()`
- species initialization
- field allocation
- diagnostics

就能更清楚地区分：

- 哪些条件是“对象都还没创建之前”就决定好的；
- 哪些条件是“构造对象时”才第一次真正生效的。
