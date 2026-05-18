# PSATD-JRhom 源码精读：任意 J/rho 时间依赖、多次沉积与谱更新

绑定源码：

- `../warpx/Source/Evolve/WarpXEvolve.cpp:430-466,840-1042`
- `../warpx/Source/WarpX.cpp:1584-1655,1799-1811,3079-3159`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralSolver.cpp:76-112`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralFieldData.cpp:30-103`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomFirstOrder.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomSecondOrder.cpp`
- `../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:286-360`

本节阅读的是 PSATD-JRhom，而不是普通 `PushPSATD()`。普通 PSATD 在一个 PIC 步内假设电流 `J` 近似常量、`rho` 线性变化；PSATD-JRhom 把一个大时间步 `dt` 拆成 `m` 个子区间，并允许 `J` 和 `rho` 在每个子区间内为常量、线性或二次多项式。WarpX 的源码实现把这个思想拆成四层：

1. 输入参数 `psatd.JRhom` 解析出 `J/rho` 的时间依赖类型和子区间数 `m`。
2. 主循环 `OneStep_JRhom()` 在每个子区间按需要重复沉积 `J` 和 `rho`。
3. `SpectralFieldIndex` 根据时间依赖类型分配 `J_old/J_mid/J_new` 和 `rho_old/rho_mid/rho_new`。
4. `PsatdAlgorithmJRhomFirstOrder` 或 `PsatdAlgorithmJRhomSecondOrder` 在谱空间解析推进 `E/B/F/G`。

## 1. 物理模型：把源项写成子区间多项式

官方文档给出的 modified Maxwell system 是：

$$
\frac{\partial\widetilde{\mathbf E}}{\partial t}
=i\mathbf k\times\widetilde{\mathbf B}-\widetilde{\mathbf J}
+i\mathbf k\widetilde F,
$$

$$
\frac{\partial\widetilde{\mathbf B}}{\partial t}
=-i\mathbf k\times\widetilde{\mathbf E},
$$

$$
\frac{\partial\widetilde F}{\partial t}
=i\mathbf k\cdot\widetilde{\mathbf E}-\widetilde\rho.
$$

这里 `F` 是 Gauss law divergence cleaning 标量。若数值解始终满足 Gauss law，则 `F=0`，方程退回普通 Maxwell 方程。JRhom 的关键是：在一个 PIC 步 `dt` 内，把源项写成每个子区间上的多项式。

设子步长

$$
\delta t=\frac{\Delta t}{m}.
$$

对某个子区间，可以把电流写成

$$
\widetilde{\mathbf J}(t)
=\mathbf a_J \tau^2+\mathbf b_J\tau+\mathbf c_J,
\qquad 0\le \tau\le \delta t,
$$

电荷密度写成

$$
\widetilde\rho(t)
=a_\rho\tau^2+b_\rho\tau+c_\rho.
$$

其中常量、线性、二次依赖分别由中点、端点、端点加中点沉积值构造。源码中的 `a_j/b_j/c_j` 和 `a_rho/b_rho/c_rho` 就是这些多项式系数的离散表达。

## 2. 参数入口：`psatd.JRhom`

`WarpX.cpp` 中的解析规则非常直接：字符串第一个字符控制 `J`，第二个字符控制 `rho`，后面的数字控制子区间数 `m`。

```cpp
std::string JRhom_input;
pp_psatd.query("JRhom", JRhom_input);
if (!JRhom_input.empty()) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        JRhom_input.length() >= 3,
        "psatd.JRhom = '" + JRhom_input + "' input string is too short to parse."
    );
    m_JRhom = true;
    // parse time dependency of J from first character
    if (JRhom_input[0] == 'C') {
        time_dependency_J = TimeDependencyJ::Constant;
    }
    else if (JRhom_input[0] == 'L') {
        time_dependency_J = TimeDependencyJ::Linear;
    }
    else if (JRhom_input[0] == 'Q') {
        time_dependency_J = TimeDependencyJ::Quadratic;
    }
```

逐块解释：

- `psatd.JRhom = CL1` 表示 `J` 常量、`rho` 线性、`m=1`，这对应普通 PSATD 的源项时间依赖。
- `LQ4` 表示 `J` 分段线性、`rho` 分段二次，一个 PIC 步拆成 4 个谱推进子区间。
- 字符只允许 `C/L/Q`，源码对非法字符立即 abort。

第二个字符用同样方式解析 `rho`：

```cpp
// parse time dependency of rho from second character
if (JRhom_input[1] == 'C') {
    time_dependency_rho = TimeDependencyRho::Constant;
}
else if (JRhom_input[1] == 'L') {
    time_dependency_rho = TimeDependencyRho::Linear;
}
else if (JRhom_input[1] == 'Q') {
    time_dependency_rho = TimeDependencyRho::Quadratic;
}
else {
    WARPX_ABORT_WITH_MESSAGE(
        "Time dependency '" + std::string(1, JRhom_input[1]) + "' of rho set by psatd.JRhom = '" + JRhom_input + "' not valid."
        " Valid options are 'C' (constant), 'L' (linear), 'Q' (quadratic)."
    );
}
```

尾部数字必须全是 digit，然后转成整数：

```cpp
for (const char m : JRhom_input.substr(2)) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        std::isdigit(m),
        "psatd.JRhom = '" + JRhom_input + "' input string must include integer 'm' after the first two characters (e.g., 'CL1')."
    );
}
m_JRhom_subintervals = std::stoi(JRhom_input.substr(2));
```

这里源码目前只检查是否为数字，没有在这一段显式检查 `m>0`。从数值意义上 `m=0` 不成立，因为后面会执行

```cpp
const amrex::Real sub_dt = dt[0] / static_cast<amrex::Real>(n_deposit);
```

所以书稿中不能把 `m` 解释为任意非负整数；物理和算法上它必须是正整数。

## 3. 约束：不能随意组合 JRhom、Vay、Galilean 和 current correction

JRhom 不是一个可以和所有 PSATD 选项自由叠加的开关。源码中首先禁止 Vay deposition：

```cpp
if (current_deposition_algo == CurrentDepositionAlgo::Vay) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        m_JRhom == false,
        "Vay deposition not implemented with JRhom algorithm");
}
```

随后把 current correction 默认关掉：

```cpp
// TODO Remove this default when current correction will
// be implemented for the PSATD-JRhom algorithm as well
if (m_JRhom) { current_correction = false; }
```

更后面还禁止 Galilean PSATD：

```cpp
if (m_JRhom)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        v_galilean_is_zero,
        "PSATD-JRhom algorithm not implemented with Galilean PSATD"
    );
}
```

对 `update_with_rho` 也有一条重要限制：

```cpp
if (time_dependency_J != TimeDependencyJ::Constant || time_dependency_rho != TimeDependencyRho::Linear)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        update_with_rho,
        "psatd.update_with_rho must be set to 1 unless J is constant in time and Rho is linear in time");
```

这表示只有标准 `J=constant, rho=linear` 情况可以不显式用 `rho` 更新；一旦采用更一般的时间依赖，谱推进需要真实的 `rho_old/mid/new` 数据来闭合。

## 4. 外层 PIC 调度：进入 `OneStep_JRhom`

JRhom 的 PIC loop 在 `WarpXEvolve.cpp` 的电磁 solver 路径中分叉。普通路径调用 `OneStep_nosub()`，JRhom 路径先做碰撞，再调用 `OneStep_JRhom()`：

```cpp
// standard PIC loop
if (!m_JRhom) {
    OneStep_nosub(a_cur_time, a_dt, a_step);
}
// JRhom PIC loop
else {
    AMREX_ALWAYS_ASSERT_WITH_MESSAGE(
        m_collisions_split_momentum_push == 0,
        "Collisions with split momentum push not yet implemented for JRhom PIC loop."
        "Set `collisions.split_momentum_push=0` to use JRhom with standard (pre-v-push collisions placement) collisions model."
    );
    // perform particle collisions
    ExecutePythonCallback("beforecollisions");
    mypc->doCollisions(a_step, a_cur_time, a_dt);
    ExecutePythonCallback("aftercollisions");

    OneStep_JRhom(a_cur_time);
}
```

两个结论：

- JRhom 当前只走无 mesh refinement 的分支；源码片段所在上下文是 `finest_level == 0`。
- `collisions.split_momentum_push` 不能与 JRhom 组合，因为 split momentum push 的碰撞位置尚未实现。

## 5. `OneStep_JRhom()` 第一段：先推进粒子，不沉积

JRhom 的粒子推进和普通 PIC loop 不一样：先把粒子从 `x^n,p^{n-1/2}` 推到 `x^{n+1},p^{n+1/2}`，但跳过普通的一次性沉积。

```cpp
// Push particle from x^{n} to x^{n+1}
//               from p^{n-1/2} to p^{n+1/2}
const bool skip_deposition = true;
PushParticlesandDeposit(cur_time, skip_deposition);
```

为什么要跳过沉积？因为 JRhom 要在一个步长内的多个相对时刻沉积 `J/rho`。如果这里执行普通沉积，就会把 `J^{n+1/2}` 和 `rho^n/rho^{n+1}` 的普通 PSATD 逻辑混进 JRhom 的多项式源项构造。

随后进入谱空间：

```cpp
// 1) Prepare E,B,F,G fields in spectral space
PSATDForwardTransformEB();
if (WarpX::do_dive_cleaning) { PSATDForwardTransformF(); }
if (WarpX::do_divb_cleaning) { PSATDForwardTransformG(); }

// 2) Set the averaged fields to zero
if (WarpX::fft_do_time_averaging) { PSATDEraseAverageFields(); }
```

这一段和普通 `PushPSATD()` 类似：先把场从实空间 FFT 到谱空间；如果需要时间平均场，就清零 accumulator。

## 6. 初始旧端点沉积：为线性/二次源项准备 old 值

如果 `rho` 不是常量，源码先在相对时间 `-dt` 沉积一次 charge，并放入 `rho_new` slot。这个名字容易误导：此处的 `rho_new` 是一个临时容器，后续循环中会通过 `PSATDMoveRhoNewToRhoOld()` 滚动到 old。

```cpp
// 3) Deposit rho (in rho_new, since it will be moved during the loop)
//    (after checking that pointer to rho_fp on MR level 0 is not null)
if (m_fields.has(FieldType::rho_fp, 0) && time_dependency_rho != TimeDependencyRho::Constant)
{
    ablastr::fields::MultiLevelScalarField const rho_fp = m_fields.get_mr_levels(FieldType::rho_fp, finest_level);

    std::string const rho_fp_string = "rho_fp";
    std::string const rho_cp_string = "rho_cp";

    // Deposit rho at relative time -dt
    // (dt[0] denotes the time step on mesh refinement level 0)
    mypc->DepositCharge(rho_fp, -dt[0]);
    // Filter, exchange boundary, and interpolate across levels
    SyncRho();
    // Forward FFT of rho
    PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 0, rho_new);
}
```

电流同理：如果 `J` 不是常量，先在相对时间 `-dt` 沉积一次 `J`，进入谱空间，作为之后滚动的旧端点。

```cpp
// 4) Deposit J at relative time -dt with time step dt
//    (dt[0] denotes the time step on mesh refinement level 0)
if (time_dependency_J != TimeDependencyJ::Constant)
{
    std::string const current_string = (do_current_centering) ? "current_fp_nodal" : "current_fp";
    mypc->DepositCurrent( m_fields.get_mr_levels_alldirs(current_string, finest_level), dt[0], -dt[0]);
    // Synchronize J: filter, exchange boundary, and interpolate across levels.
    SyncCurrent("current_fp");
    // Forward FFT of J
    PSATDForwardTransformJ("current_fp", "current_cp");
}
```

这里 `DepositCurrent(..., dt[0], -dt[0])` 的第二个时间参数是相对沉积时间，说明 JRhom 不是在粒子推进半步位置一次取源项，而是在多个源项采样时刻重算沉积。

## 7. 子区间循环：`m` 次沉积与谱推进

子区间数来自 `psatd.JRhom`：

```cpp
// Number of depositions for multi-J scheme
const int n_deposit = WarpX::m_JRhom_subintervals;
// Time sub-step for each multi-J deposition
const amrex::Real sub_dt = dt[0] / static_cast<amrex::Real>(n_deposit);
// Whether to perform PSATD-JRhom depositions on a time interval that spans
// one or two full time steps (from n*dt to (n+1)*dt, or from n*dt to (n+2)*dt)
const int n_loop = (WarpX::fft_do_time_averaging) ? 2*n_deposit : n_deposit;
```

若开启 `fft_do_time_averaging`，循环长度变成 `2*m`，因为平均场要跨 `2*dt` 积分，后面再除以 `2*dt`。

每个子区间开始时，线性或二次 `J` 先滚动谱数组：

```cpp
// Loop over PSATD-JRhom depositions
for (int i_deposit = 0; i_deposit < n_loop; i_deposit++)
{
    // Move J from new to old if J is linear or quadratic in time
    if (time_dependency_J != TimeDependencyJ::Constant) { PSATDMoveJNewToJOld(); }

    const amrex::Real t_deposit_current = (time_dependency_J == TimeDependencyJ::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;

    const amrex::Real t_deposit_charge = (time_dependency_rho == TimeDependencyRho::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;
```

这段是 JRhom 时间几何的核心：

- 线性源项使用子区间端点，所以时间为 `(i-m+1)*sub_dt`。
- 常量或二次源项需要中点采样，先用 `(i-m+0.5)*sub_dt`。
- 二次情形还会再沉积一次 `+0.5*sub_dt`，形成 old/mid/new 三点。

## 8. 子区间内的 J 沉积

每个子区间都沉积新电流，做 `SyncCurrent()`，再 FFT 到谱空间：

```cpp
// Deposit new J at relative time t_deposit_current with time step dt
// (dt[0] denotes the time step on mesh refinement level 0)
std::string const current_string = (do_current_centering) ? "current_fp_nodal" : "current_fp";
mypc->DepositCurrent( m_fields.get_mr_levels_alldirs(current_string, finest_level), dt[0], t_deposit_current);
// Synchronize J: filter, exchange boundary, and interpolate across levels.
SyncCurrent("current_fp");
// Forward FFT of J
PSATDForwardTransformJ("current_fp", "current_cp");
```

如果 `J` 是二次时间依赖，源码把当前 new 移到 mid，然后在中点偏移处再沉积一次：

```cpp
if (time_dependency_J == TimeDependencyJ::Quadratic)
{
    PSATDMoveJNewToJMid();
    mypc->DepositCurrent( m_fields.get_mr_levels_alldirs(current_string, finest_level),  dt[0], t_deposit_current + 0.5_rt*sub_dt);
    SyncCurrent("current_fp");
    PSATDForwardTransformJ("current_fp", "current_cp");
}
```

因此二次 `J` 的谱数组语义是：

- `J_old`：子区间左端；
- `J_mid`：子区间中点；
- `J_new`：子区间右端。

这些名字由 `SpectralFieldIndex` 决定，而不是由 `MultiFab` 字段名决定。

## 9. 子区间内的 rho 沉积

`rho` 的逻辑与 `J` 平行。非常量 `rho` 会先把 `rho_new` 滚到 `rho_old`：

```cpp
// Move rho from new to old if rho is linear in time
if (time_dependency_rho != TimeDependencyRho::Constant) { PSATDMoveRhoNewToRhoOld(); }

// Deposit rho at relative time t_deposit_charge
mypc->DepositCharge(rho_fp, t_deposit_charge);
// Filter, exchange boundary, and interpolate across levels
SyncRho();
// Forward FFT of rho
const int rho_idx = (time_dependency_rho != TimeDependencyRho::Constant) ? rho_new : rho_mid;
PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 0, rho_idx);
```

常量 `rho` 存到 `rho_mid`；线性/二次 `rho` 的新端点存到 `rho_new`。二次 `rho` 再补一次中点：

```cpp
if (time_dependency_rho == TimeDependencyRho::Quadratic)
{
    PSATDMoveRhoNewToRhoMid();
    mypc->DepositCharge(rho_fp, t_deposit_charge + 0.5_rt*sub_dt);
    SyncRho();
    PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 0, rho_new);
}
```

这里的操作顺序说明：`rho_mid` 存的是前一次 `rho_new` 通过 move 得来的中点，而最后一次 FFT 写入新的右端点。

## 10. 谱推进、回填和边界

每个子区间沉积完成后推进谱场：

```cpp
if (WarpX::current_correction)
{
    WARPX_ABORT_WITH_MESSAGE(
        "Current correction not implemented for PSATD-JRhom algorithm.");
}

// Advance E,B,F,G fields in time and update the average fields
PSATDPushSpectralFields();
```

虽然 `WarpX.cpp` 默认把 JRhom 的 `current_correction` 关掉，这里仍保留运行时保护。走到 `PSATDPushSpectralFields()` 时，具体算法由 `SpectralSolver` 选择。

在走完 `m` 个子区间，也就是回到一个完整 PIC 时间步末端时，非平均场逆 FFT 回实空间：

```cpp
// Transform non-average fields E,B,F,G after n_deposit pushes
// (the relative time reached here coincides with an integer full time step)
if (i_deposit == n_deposit-1)
{
    PSATDBackwardTransformEB();
    if (WarpX::do_dive_cleaning) { PSATDBackwardTransformF(); }
    if (WarpX::do_divb_cleaning) { PSATDBackwardTransformG(); }
}
```

如果有时间平均场，最后缩放并逆变换平均场：

```cpp
// We summed the integral of the field over 2*dt
PSATDScaleAverageFields(1._rt / (2._rt*dt[0]));
PSATDBackwardTransformEBavg(
    m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_cp, finest_level, skip_lev0_coarse_patch),
    m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_cp, finest_level, skip_lev0_coarse_patch)
);
```

最后仍然要处理 PML、边界和 guard cells：

```cpp
if (do_pml && pml[lev]->ok())
{
    pml[lev]->PushPSATD(m_fields, lev);
}
ApplyEfieldBoundary(lev, PatchType::fine, cur_time + dt[0]);
ApplyBfieldBoundary(lev, PatchType::fine, SubcyclingHalf::FirstHalf, cur_time + dt[0]);
```

这说明 JRhom 只改变源项采样和谱推进节奏，不取消 WarpX 的 PML、边界和 guard-cell 同步义务。

## 11. 谱场数组布局：`SpectralFieldIndex`

JRhom 需要根据时间依赖分配不同数量的谱字段。源码在 `SpectralFieldIndex` 中按顺序设置 component index：

```cpp
if (time_dependency_J == TimeDependencyJ::Constant)
{
    Jx_mid = c++; Jy_mid = c++; Jz_mid = c++;
}
if (time_dependency_J == TimeDependencyJ::Quadratic)
{
    Jx_old = c++; Jy_old = c++; Jz_old = c++;
    Jx_new = c++; Jy_new = c++; Jz_new = c++;
    Jx_mid = c++; Jy_mid = c++; Jz_mid = c++;
}
else if (time_dependency_J == TimeDependencyJ::Linear)
{
    Jx_old = c++; Jy_old = c++; Jz_old = c++;
    Jx_new = c++; Jy_new = c++; Jz_new = c++;
}
```

`J` 常量只需要 `mid`。线性需要 `old/new`。二次需要 `old/mid/new`。`rho` 同理：

```cpp
if (time_dependency_rho == TimeDependencyRho::Constant)
{
    rho_mid = c++;
}
if (time_dependency_rho == TimeDependencyRho::Quadratic)
{
    rho_old = c++;
    rho_mid = c++;
    rho_new = c++;
}
else if (time_dependency_rho == TimeDependencyRho::Linear)
{
    rho_old = c++;
    rho_new = c++;
}
```

这解释了为什么 `OneStep_JRhom()` 中有那么多 `MoveJNewToJOld()`、`MoveJNewToJMid()`、`MoveRhoNewToRhoOld()`、`MoveRhoNewToRhoMid()`：这些函数不是移动实空间 `MultiFab`，而是在谱空间 field component 之间滚动时间层。

## 12. 谱求解器选择：一阶或二阶 JRhom

`SpectralSolver.cpp` 中，JRhom 算法不是单独在 `m_JRhom` 下选择，而是由 `psatd.solution_type` 选择 first-order 或 second-order。因为这两个类也覆盖标准 PSATD 的 `CL1` 情形。

```cpp
else if (psatd_solution_type == PSATDSolutionType::FirstOrder)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        !fft_do_time_averaging,
        "psatd.do_time_averaging=1 not supported when psatd.solution_type=first-order");

    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        (!dive_cleaning && !divb_cleaning) || (dive_cleaning && divb_cleaning),
        "warpx.do_dive_cleaning and warpx.do_divb_cleaning must be equal when psatd.solution_type=first-order");

    const bool div_cleaning = (dive_cleaning && divb_cleaning);

    // First-order PSATD equations with variable time dependency of J and rho
    // (valid also for standard PSATD, where J is constant and rho is linear)
    algorithm = std::make_unique<PsatdAlgorithmJRhomFirstOrder>(
        k_space, dm, m_spectral_index, norder_x, norder_y, norder_z, grid_type,
        dt, div_cleaning, time_dependency_J, time_dependency_rho);
}
```

一阶形式不能做时间平均；若使用 divergence cleaning，`do_dive_cleaning` 和 `do_divb_cleaning` 必须同时开。

二阶形式是默认更一般的实现：

```cpp
else if (psatd_solution_type == PSATDSolutionType::SecondOrder)
{
    // Second-order PSATD equations with variable time dependency of J and rho
    // (valid also for standard PSATD, where J is constant and rho is linear)
    algorithm = std::make_unique<PsatdAlgorithmJRhomSecondOrder>(
      k_space, dm, m_spectral_index, norder_x, norder_y, norder_z, grid_type,
      dt, update_with_rho, fft_do_time_averaging, dive_cleaning, divb_cleaning, time_dependency_J, time_dependency_rho);
}
```

注意：这里传入的 `dt` 已在分配 spectral solver 时被缩小为 `dt/m`。

```cpp
amrex::Real solver_dt = dt[lev];
if (WarpX::m_JRhom) { solver_dt /= static_cast<amrex::Real>(WarpX::m_JRhom_subintervals); }
```

这保证 `PsatdAlgorithmJRhom*` 内部的 `m_dt` 就是子区间长度 `delta t`，而不是外层 PIC 大步长。

## 13. 一阶 JRhom：直接构造 `c0/c1` 并展开更新式

一阶实现支持 `J/rho` 的常量和线性依赖。开头先根据枚举设置布尔量：

```cpp
const bool J_constant = (m_time_dependency_J == TimeDependencyJ::Constant);
const bool J_linear   = (m_time_dependency_J == TimeDependencyJ::Linear);
const bool rho_constant = (m_time_dependency_rho == TimeDependencyRho::Constant);
const bool rho_linear   = (m_time_dependency_rho == TimeDependencyRho::Linear);
```

随后从谱 field array 中取出所需时间层，并构造

$$
\mathbf J(t)=\mathbf J_{c0}+\mathbf J_{c1}t.
$$

```cpp
const Complex Jx_mid = (J_constant) ? fields(i,j,k,Idx.Jx_mid) : 0._rt;
const Complex Jy_mid = (J_constant) ? fields(i,j,k,Idx.Jy_mid) : 0._rt;
const Complex Jz_mid = (J_constant) ? fields(i,j,k,Idx.Jz_mid) : 0._rt;
const Complex Jx_old = (J_linear  ) ? fields(i,j,k,Idx.Jx_old) : 0._rt;
const Complex Jy_old = (J_linear  ) ? fields(i,j,k,Idx.Jy_old) : 0._rt;
const Complex Jz_old = (J_linear  ) ? fields(i,j,k,Idx.Jz_old) : 0._rt;
const Complex Jx_new = (J_linear  ) ? fields(i,j,k,Idx.Jx_new) : 0._rt;
const Complex Jy_new = (J_linear  ) ? fields(i,j,k,Idx.Jy_new) : 0._rt;
const Complex Jz_new = (J_linear  ) ? fields(i,j,k,Idx.Jz_new) : 0._rt;

const Complex Jx_c0 = (J_constant) ? Jx_mid : Jx_old;
const Complex Jy_c0 = (J_constant) ? Jy_mid : Jy_old;
const Complex Jz_c0 = (J_constant) ? Jz_mid : Jz_old;
const Complex Jx_c1 = (J_linear  ) ? (Jx_new-Jx_old)/dt : 0._rt;
const Complex Jy_c1 = (J_linear  ) ? (Jy_new-Jy_old)/dt : 0._rt;
const Complex Jz_c1 = (J_linear  ) ? (Jz_new-Jz_old)/dt : 0._rt;
```

`rho` 只在 divergence cleaning 分支中显式出现：

```cpp
if (div_cleaning)
{
    rho_mid = (rho_constant) ? fields(i,j,k,Idx.rho_mid) : 0._rt;
    rho_old = (rho_linear  ) ? fields(i,j,k,Idx.rho_old) : 0._rt;
    rho_new = (rho_linear  ) ? fields(i,j,k,Idx.rho_new) : 0._rt;

    F_old = fields(i,j,k,Idx.F);
    G_old = fields(i,j,k,Idx.G);

    rho_c0 = (rho_constant) ? rho_mid : rho_old;
    rho_c1 = (rho_linear  ) ? (rho_new-rho_old)/dt : 0._rt;
}
```

零模 `k=0` 单独处理：

```cpp
if (knorm == 0._rt)
{
    fields(i,j,k,Idx.Ex) = Ex_old - mu0*c2*dt*Jx_c0 - 0.5_rt*mu0*c2*dt2*Jx_c1;
    fields(i,j,k,Idx.Ey) = Ey_old - mu0*c2*dt*Jy_c0 - 0.5_rt*mu0*c2*dt2*Jy_c1;
    fields(i,j,k,Idx.Ez) = Ez_old - mu0*c2*dt*Jz_c0 - 0.5_rt*mu0*c2*dt2*Jz_c1;

    if (div_cleaning)
    {
        fields(i,j,k,Idx.F) = F_old - mu0*c2*dt*rho_c0 - 0.5_rt*mu0*c2*dt2*rho_c1;
    }
}
```

这是 Ampere 方程在没有空间 curl 时对源项的时间积分。若 `J=J_c0+J_c1 t`，则

$$
\int_0^{\Delta t}J(t)\,dt
=J_{c0}\Delta t+\frac{1}{2}J_{c1}\Delta t^2.
$$

源码中电场更新前的负号来自

$$
\partial_t\mathbf E=-\frac{\mathbf J}{\epsilon_0}
=-\mu_0c^2\mathbf J.
$$

非零模则展开大量 `C01-C16` 系数。以 `Ex` 为例：

```cpp
fields(i,j,k,Idx.Ex) = C01*Ex_old + C02*Ey_old + C03*Ez_old
                     + C04*Bx_old + C05*By_old + C06*Bz_old
                     + C07*F_old // only with div cleaning
                     + C09*Jx_c0 + C10*Jy_c0 + C11*Jz_c0
                     + C12*Jx_c1 + C13*Jy_c1 + C14*Jz_c1 // only with J linear in time
                     + C15*rho_c0  // only with div cleaning
                     + C16*rho_c1; // only with div cleaning and rho linear in time
```

这段不是经验公式，而是把 modified Maxwell system 对线性源项解析积分后的矩阵指数写成逐分量系数。`C01-C03` 乘旧电场，`C04-C06` 乘旧磁场，`C09-C14` 是电流源项，`C15-C16` 是 divergence cleaning 下的电荷源项。

一阶实现明确不支持 current correction 和 Vay：

```cpp
void PsatdAlgorithmJRhomFirstOrder::CurrentCorrection (SpectralFieldData& field_data)
{
    BL_PROFILE("PsatdAlgorithmJRhomFirstOrder::CurrentCorrection");

    amrex::ignore_unused(field_data);
    WARPX_ABORT_WITH_MESSAGE(
        "Current correction not implemented for first-order PSATD equations");
}
```

## 14. 二阶 JRhom：`a/b/c` 多项式系数与 `Y1-Y5`

二阶实现支持 `C/L/Q` 三种时间依赖，构造二次多项式系数：

```cpp
const Complex a_jx = (J_quadratic) ? (Jx_new - 2._rt * Jx_mid + Jx_old) : 0._rt;
const Complex a_jy = (J_quadratic) ? (Jy_new - 2._rt * Jy_mid + Jy_old) : 0._rt;
const Complex a_jz = (J_quadratic) ? (Jz_new - 2._rt * Jz_mid + Jz_old) : 0._rt;

const Complex b_jx = (J_linear || J_quadratic) ? (Jx_new - Jx_old) : 0._rt;
const Complex b_jy = (J_linear || J_quadratic) ? (Jy_new - Jy_old) : 0._rt;
const Complex b_jz = (J_linear || J_quadratic) ? (Jz_new - Jz_old) : 0._rt;

const Complex c_jx = (J_linear) ? (Jx_new + Jx_old)/2._rt : Jx_mid;
const Complex c_jy = (J_linear) ? (Jy_new + Jy_old)/2._rt : Jy_mid;
const Complex c_jz = (J_linear) ? (Jz_new + Jz_old)/2._rt : Jz_mid;
```

这与数学表述中的 `a_J,b_J,c_J` 对应。线性时 `a=0`，`c` 取端点平均；常量或二次时 `c` 取中点值。

在标准 `J` 常量、`rho` 线性、且 `update_with_rho=0` 的特殊情形，源码从 Gauss law 和连续性方程重构 `rho_old/rho_new`：

```cpp
if (J_constant && rho_linear && !update_with_rho)
{
    const Complex k_dot_E_old = kx*Ex_old + ky*Ey_old + kz*Ez_old;
    const Complex k_dot_J_mid = kx*Jx_mid + ky*Jy_mid + kz*Jz_mid;

    rho_old = I*ep0*k_dot_E_old;
    rho_new = rho_old - I*k_dot_J_mid*dt;
}
```

这两行对应谱空间 Gauss law 和连续性方程：

$$
i\mathbf k\cdot\mathbf E=\rho/\epsilon_0,
$$

$$
\rho^{n+1}=\rho^n-i\Delta t\,\mathbf k\cdot\mathbf J^{n+1/2}.
$$

随后构造 `rho` 的多项式系数：

```cpp
const Complex a_rho = (rho_quadratic) ? (rho_new - 2._rt * rho_mid + rho_old) : 0._rt;
const Complex b_rho = (rho_linear || rho_quadratic) ? (rho_new - rho_old) : 0._rt;
const Complex c_rho = (rho_linear) ? (rho_new + rho_old)/2._rt : rho_mid;

const Complex sum_rho = Y1 * a_rho - Y5 * b_rho - Y4 * c_rho;
```

`sum_rho` 是电场纵向项的源项积分组合。

## 15. 二阶 `E/B/F/G` 更新式

`E` 的更新式以 `Ex` 为例：

```cpp
fields(i,j,k,Idx.Ex) = C * Ex_old
    + I * c2 * S_ck * (ky * Bz_old - kz * By_old)
    + Y3 * a_jx + Y2 * b_jx - S_ck/ep0 * c_jx
    + I * c2 * kx * sum_rho;
```

逐项对应：

- `C * Ex_old`：解析振荡中的旧电场保留项；
- `I*c2*S_ck*(ky*Bz-kz*By)`：谱空间 curl(B)；
- `Y3*a_j + Y2*b_j - S_ck/ep0*c_j`：电流多项式源项的解析积分；
- `I*c2*kx*sum_rho`：由电荷密度约束和 divergence cleaning 形式引入的纵向修正。

`B` 的更新式以 `Bx` 为例：

```cpp
fields(i,j,k,Idx.Bx) = C * Bx_old
    - I * S_ck * (ky * Ez_old - kz * Ey_old)
    - I * Y1 * (ky * a_jz - kz * a_jy)
    + I * Y5 * (ky * b_jz - kz * b_jy)
    + I * Y4 * (ky * c_jz - kz * c_jy );
```

这里 `ky*Ez-kz*Ey` 是 `(k x E)_x`。后面三项是 `k x J` 的二次、一次、常量源项积分。

如果开 `dive_cleaning`，`F` 也按同样源项积分推进：

```cpp
fields(i,j,k,Idx.F) = C * F_old + S_ck * I * k_dot_E
    + I * ( Y1 * k_dot_ddJ - Y5 * k_dot_dJ - Y4 * k_dot_J_mid )
    +  Y3 * a_rho + Y2 * b_rho - S_ck/ep0 * c_rho;
```

如果开 `divb_cleaning`，`G` 用 `k dot B` 推进：

```cpp
fields(i,j,k,Idx.G) = C * G_old + I * c2 * S_ck * k_dot_B;
```

因此二阶 JRhom 不只是更新 `E/B`；它同时把 Gauss law 和 `div B` cleaning 标量纳入同一个谱空间解析推进。

## 16. `Y1-Y5` 系数和零模极限

二阶实现先为每个谱 mode 预计算 `C/S_ck/Y1-Y5`：

```cpp
// C
C(i,j,k) = std::cos(om_s * dt);

// S_ck
if (om_s != 0.)
{
    S_ck(i,j,k) = std::sin(om_s * dt) / om_s;
}
else // om_s = 0
{
    S_ck(i,j,k) = dt;
}
```

这里

$$
\omega_s=c|\mathbf k_s|.
$$

`S_ck` 的零模极限是

$$
\lim_{\omega\to0}\frac{\sin(\omega\Delta t)}{\omega}=\Delta t.
$$

`Y1-Y5` 也都有显式零模极限。例如：

```cpp
// Y1
if (om_s != 0.)
{
    Y1(i,j,k) = ( (1._rt - C(i,j,k)) * (8._rt - om2_s*dt2) - 4._rt * S_ck(i,j,k) * om2_s * dt) / (2._rt * ep0 * dt2 * om2_s * om2_s);
}
else // om_s = 0
{
    Y1(i,j,k) = - dt2 / (12._rt * ep0);
}
```

这些分支不是优化，而是数值正确性所需。若直接用非零模公式，`om_s=0` 时会除以 `om_s^4`，并在低频 mode 造成严重 cancellation。

## 17. 时间平均：`Y6-Y8`

如果 `fft_do_time_averaging` 打开，二阶 JRhom 额外分配 `Y6/Y7/Y8`：

```cpp
if (time_averaging)
{
    Y6_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    Y7_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    Y8_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    InitializeSpectralCoefficientsAveraging(spectral_kspace, dm, dt);
}
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    !time_averaging || update_with_rho,
    "psatd.time_averaging=1 implemented only with psatd.update_with_rho=1"
);
```

平均场更新是累加形式，不是覆盖形式：

```cpp
// Here the code is *accumulating* the average,
// because it is meant to be used with sub-cycling.
// Maybe this should be made more generic?
fields(i,j,k,Idx.Ex_avg) += S_ck * Ex_old
    + I * c2 * ep0 * Y4 * (ky * Bz_old - kz * By_old)
    - I * c2 * kx * (Y6 * a_rho + Y7 * b_rho + Y8 * c_rho)
    + ( Y1 * a_jx - Y5 * b_jx - Y4 * c_jx);
```

这和 `OneStep_JRhom()` 末尾的

```cpp
PSATDScaleAverageFields(1._rt / (2._rt*dt[0]));
```

配套：前者在每个子区间累加积分量，后者在外层除以总时间长度。

## 18. 二阶类里仍有 current correction/Vay，但主 JRhom 路径禁用

`PsatdAlgorithmJRhomSecondOrder` 中保留了 current correction 和 Vay spectral deposition，但只允许 `J_constant && rho_linear`：

```cpp
const bool J_constant = (m_time_dependency_J   == TimeDependencyJ::Constant);
const bool rho_linear = (m_time_dependency_rho == TimeDependencyRho::Linear);

WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    J_constant && rho_linear,
    "Current correction implemented only with J constant in time and rho linear in time");
```

修正公式是标准谱连续性投影：

```cpp
fields(i,j,k,Idx.Jx_mid) = Jx - (k_dot_J-I*(rho_new-rho_old)/dt)*kx/(knorm2);
fields(i,j,k,Idx.Jy_mid) = Jy - (k_dot_J-I*(rho_new-rho_old)/dt)*ky/(knorm2);
fields(i,j,k,Idx.Jz_mid) = Jz - (k_dot_J-I*(rho_new-rho_old)/dt)*kz/(knorm2);
```

但 `OneStep_JRhom()` 中仍然 abort `current_correction`，`WarpX.cpp` 也默认关掉 JRhom current correction。因此书稿应区分：

- 类本身实现了 `CL` 情形的 correction helper；
- 当前 JRhom PIC loop 不把 current correction 作为可用组合暴露。

## 19. 小结：JRhom 的源码逻辑闭环

PSATD-JRhom 的完整闭环是：

1. `WarpX.cpp` 解析 `psatd.JRhom`，得到 `time_dependency_J`、`time_dependency_rho` 和 `m_JRhom_subintervals`。
2. `AllocLevelSpectralSolver()` 把谱求解器内部 `dt` 缩小为 `dt/m`。
3. `OneStep()` 在无 MR 电磁路径中分派到 `OneStep_JRhom()`。
4. `OneStep_JRhom()` 先推进粒子但跳过普通沉积。
5. 每个子区间按 `C/L/Q` 类型在不同相对时刻沉积 `J/rho`。
6. `SpectralFieldIndex` 提供 `old/mid/new` 谱数组槽。
7. `PsatdAlgorithmJRhomFirstOrder` 或 `SecondOrder` 把源项多项式解析积分进 `E/B/F/G`。
8. 完整 `m` 个子区间后回填实空间场，再做 PML、边界和 guard-cell 同步。

物理上，它解决的是“粒子源项在一个 PIC 时间步内并不真的常量”的问题。代码上，它不是在普通 PSATD 上加一个更复杂的系数，而是重排了 PIC loop：把源项沉积从一次变成多次，把谱推进从一次变成 `m` 次，并让谱场数组显式保存源项时间层。
