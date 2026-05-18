# `MakeWarpX()` 与构造期 `ReadParameters()` 的交界

绑定源码：

- `../warpx/Source/WarpX.cpp`
- `../warpx/Source/Utils/WarpXUtil.cpp`
- `../warpx/Source/Utils/WarpXUtil.H`
- `../warpx/Source/Initialization/WarpXInit.cpp`

这一篇接着上一篇 `08-initialization-bootstrap.md` 往下走，但不再停留在“外部库和 AMReX 怎样启动”，而是专门回答一个更容易混淆的问题：

1. 哪些全局参数在 `WarpX::ReadParameters()` 之前就已经被锁定。
2. 哪些参数虽然在启动层先读了一遍，但还要到构造期再做物理/算法一致性约束。
3. `MakeWarpX()`、`ConvertLabParamsToBoost()`、`CheckGriddingForRZSpectral()` 和 `ReadParameters()` 之间到底是谁先改 parser、谁后消费结果。

## 1. `GetInstance()` 不是“读完参数再创建对象”，而是先做一层前置参数锁定

真正的创建顺序是：

```cpp
WarpX::GetInstance()
    -> WarpX::MakeWarpX()
        -> check_dims()
        -> read_moving_window_parameters(...)
        -> ConvertLabParamsToBoost()
        -> parse_field_boundaries()
        -> parse_particle_boundaries(...)
        -> CheckGriddingForRZSpectral()
        -> new WarpX()
            -> initialize_warning_manager()
            -> ReadParameters()
```

这意味着 WarpX 的参数语义不是“一切都在 `ReadParameters()` 里第一次出现”。恰恰相反，在对象真正构造前，已经有一批全局状态被读出、转换、甚至直接回写进 `ParmParse`。

## 2. `read_moving_window_parameters()` 先锁定 moving window，再由 `ReadParameters()` 检查几何兼容性

在 `MakeWarpX()` 里，moving window 相关量已经先读出来：

```cpp
warpx::initialization::read_moving_window_parameters(
    do_moving_window, start_moving_window_step, end_moving_window_step,
    moving_window_dir, moving_window_v);
```

这里完成了两件事：

1. 把 `moving_window_dir = x/y/z` 先映射成内部整数方向。
2. 把 `moving_window_v` 从“以 `c` 为单位的输入值”直接乘成物理速度。

因此进入 `WarpX` 构造函数时：

- `do_moving_window`
- `moving_window_dir`
- `moving_window_v`

都已经是全局静态状态，不再是原始 parser 字符串。

但 moving window 还没有在这一层完成全部一致性检查。真正的几何兼容性约束出现在后面的 `ReadParameters()`：

```cpp
if (do_moving_window)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        Geom(0).isPeriodic(moving_window_dir) == 0,
        "The problem must be non-periodic in the moving window direction");
    moving_window_x = geom[0].ProbLo(moving_window_dir);
}
```

也就是说：

- 启动层负责“把参数变成内部状态”；
- 构造期负责“检查这些状态和当前 geometry/solver 是否兼容”。

## 3. `ConvertLabParamsToBoost()` 不是只读 boosted-frame 参数，而是会直接改写 geometry 和 tagging 输入

这个函数最容易被误解成“只是把 `gamma_boost` 存起来”。实际它做得更重：

1. 先调用 `ReadBoostedFrameParameters(gamma_boost, beta_boost, boost_direction)`。
2. 如果 `gamma_boost <= 1` 就直接返回。
3. 如果真的启用 boosted frame，就读取并重写：
   - `geometry.prob_lo`
   - `geometry.prob_hi`
   - `warpx.fine_tag_lo`
   - `warpx.fine_tag_hi`
   - `slice.dom_lo`
   - `slice.dom_hi`

核心更新结构是：

```cpp
convert_factor = 1._rt/( gamma_boost * ( 1 - beta_boost * beta_window ) );
prob_lo[idim] *= convert_factor;
prob_hi[idim] *= convert_factor;
...
pp_geometry.addarr("prob_lo", prob_lo);
pp_geometry.addarr("prob_hi", prob_hi);
pp_warpx.addarr("fine_tag_lo", fine_tag_lo);
pp_warpx.addarr("fine_tag_hi", fine_tag_hi);
pp_slice.addarr("dom_lo",slice_lo);
pp_slice.addarr("dom_hi",slice_hi);
```

所以它不是“记住 boost 参数，稍后再用”，而是直接把 parser 中的实验室系输入坐标区间提前改写成 boosted-frame 下要用的值。

## 4. moving window 和 boosted frame 在这里已经发生第一次耦合

`ConvertLabParamsToBoost()` 计算转换系数时并不总是只看 `beta_boost`。如果开启 moving window，并且当前 boost 方向正好是 moving-window 方向，它会用：

```cpp
beta_window = WarpX::moving_window_v / PhysConst::c;
convert_factor = 1._rt/( gamma_boost * ( 1 - beta_boost * beta_window ) );
```

这说明两个重要事实：

1. `read_moving_window_parameters()` 必须先于 `ConvertLabParamsToBoost()`。
2. boosted-frame 的坐标缩放已经把 moving-window 速度耦合进去了，不是后面 `Evolve()` 时才第一次相遇。

也就是说，WarpX 启动层里已经存在“moving window 影响几何参数预处理”这一层，不只是推进阶段才有 moving window 逻辑。

## 5. `ReadParameters()` 会再次调用 `ReadBoostedFrameParameters()`，但这次消费目标变了

在 `ReadParameters()` 里，boosted-frame 参数又被读了一遍：

```cpp
ReadBoostedFrameParameters(gamma_boost, beta_boost, boost_direction);
```

这不是和 `ConvertLabParamsToBoost()` 重复，而是两次消费目标不同：

- `ConvertLabParamsToBoost()` 用 boost 参数去改写 parser 里的几何和 tagging 区间；
- `ReadParameters()` 用同一组 boost 参数去初始化真正的 `WarpX` 运行态成员，例如：
  - `gamma_boost`
  - `beta_boost`
  - `boost_direction`
  - 以及后面默认 `v_galilean` / `v_comoving` 等 solver 相关状态

因此，这里不是“重复读取无意义”，而是“先改输入，再建状态”。

## 6. `CheckGriddingForRZSpectral()` 也是启动层预写回，不是构造期检查器

`CheckGriddingForRZSpectral()` 的调用点也在 `new WarpX()` 之前：

```cpp
CheckGriddingForRZSpectral();
```

它只在 `WARPX_DIM_RZ + algo.maxwell_solver = psatd` 这条组合下生效；否则直接返回。

一旦进入这条路径，它会直接改写 `amr` parser 里的分块参数，而不是仅仅做断言：

### 径向方向

- `blocking_factor_x` 会被改成“不小于径向总网格数的 2 的幂”
- `max_grid_size_x` 会被改成当前 level 的完整径向网格数

并且 refinement level 上继续按 2 倍递推。

### 纵向方向

它还要求：

```cpp
n_cell[1] >= 8*nprocs
```

否则直接 abort，原因是 RZ spectral 至少要保证每个 processor 有足够的 longitudinal blocks，并给 shape/filter 留余量。

接着它会根据：

- 用户给的 `blocking_factor` 或 `blocking_factor_y`
- 用户给的 `max_grid_size` 或 `max_grid_size_y`

做二次缩减，直到 coarse level 至少还能提供“每个 processor 至少一个 block”。

因此，`CheckGriddingForRZSpectral()` 的本质不是“检查用户输入是否合法”，而是“为了 RZ spectral decomposition 主动覆盖 AMR 分块参数”。

## 7. 这解释了为什么 `ReadParameters()` 之后看到的并不总是用户原始输入

把这一篇和上一篇合起来，会发现启动层至少有三类“先改 parser，再让构造期消费”的行为：

1. `WarpXAMReXInit.cpp`
   - 常量注入
   - `geometry.is_periodic` 回写
   - `prob_lo/prob_hi/n_cell` 预解析
2. `ConvertLabParamsToBoost()`
   - `prob_lo/prob_hi`
   - `fine_tag_lo/fine_tag_hi`
   - `slice.dom_lo/dom_hi` 改写
3. `CheckGriddingForRZSpectral()`
   - `blocking_factor_x/y`
   - `max_grid_size_x/y` 改写

所以 `WarpX::ReadParameters()` 读到的很多值，已经不再是用户输入文件里的“原始字面量”，而是启动层处理过的运行时版本。

这对源码精读很重要，因为否则很容易误以为：

- `ReadParameters()` 自己决定了一切；
- 或者误把某些 AMR / boost / geometry 行为理解成“后来才出现的副作用”。

实际上，这些副作用很多在构造函数进入前就已经发生了。

## 8. 构造函数开始时，真正新加入的是 warning policy、solver compatibility 和容器初始化

当 `new WarpX()` 终于发生时，构造函数开头主要做三件新事情：

1. `initialize_warning_manager()`：把 warning policy 接进运行时。
2. `ReadParameters()`：读取 solver、grid、species、diagnostics 等主体参数，并做大量 compatibility 断言。
3. 基于前面已经锁定的全局状态创建容器：
   - `MultiParticleContainer`
   - `ParticleBoundaryBuffer`
   - `MultiFluidContainer`
   - electrostatic / hybrid solver objects

例如 moving window 对粒子连续注入位置的影响，直到这时才第一次落到真实容器成员：

```cpp
if (do_moving_window){
    ...
    if (moving_window_v > 0._rt)
        pc.m_current_injection_position = geom[0].ProbHi(moving_window_dir);
    else if (moving_window_v < 0._rt)
        pc.m_current_injection_position = geom[0].ProbLo(moving_window_dir);
}
```

这说明构造期不是在“首次知道 moving window”，而是在“首次把已锁定的 moving-window 语义写进具体对象”。

## 9. 当前 `Initialization` 启动层可以再细分成两段

到这里，启动层其实已经能更细地分成：

### 9.1 预初始化与 parser 改写段

- `initialize_external_libraries()`
- `amrex_init()`
- `overwrite_amrex_parser_defaults()`
- `parse_geometry_input()`
- `read_moving_window_parameters()`
- `ConvertLabParamsToBoost()`
- `CheckGriddingForRZSpectral()`

这一段的共同点是：

- 还没有真正构造 `WarpX` 对象；
- 但已经在不断改写 parser 和全局静态状态。

### 9.2 构造与运行态落地段

- `initialize_warning_manager()`
- `ReadParameters()`
- `BackwardCompatibility()`
- `InitEB()`
- `MultiParticleContainer` / `ParticleBoundaryBuffer` / solver objects 初始化

这一段的共同点是：

- 终于有了 `WarpX` 实例；
- 之前锁定的状态开始落到真实运行态对象里。

这两段分开之后，后面再读：

- boosted-frame 例子
- RZ spectral gridding
- moving window 连续注入
- warning manager / known-issue 机制

就不会再把“参数锁定时机”和“对象消费时机”混在一起了。
