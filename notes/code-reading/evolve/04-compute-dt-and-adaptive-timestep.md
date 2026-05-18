# ComputeDt 与自适应时间步精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `../warpx/Source/Evolve/WarpXComputeDt.cpp`，并对照 `WarpX.cpp` 中参数读取和官方参数文档。它回答阶段 3 的第一个问题：WarpX 初始时间步 `dt` 怎样由 solver、CFL、用户参数、粒子速度和 AMR subcycling 决定。

## 1. 参数入口：`cfl`、`const_dt`、`max_dt`、`dt_update_interval`

`WarpX::ReadParameters()` 中读取时间步相关参数。源码位置：`../warpx/Source/WarpX.cpp:679, 797-810`。

```cpp
utils::parser::queryWithParser(pp_warpx, "cfl", cfl);

utils::parser::queryWithParser(pp_warpx, "const_dt", m_const_dt);
utils::parser::queryWithParser(pp_warpx, "max_dt", m_max_dt);
amrex::Vector<int> dt_interval_vec;
pp_warpx.queryarr("dt_update_interval", dt_interval_vec);
m_dt_update_interval = utils::parser::IntervalsParser(dt_interval_vec);
if (m_dt_update_interval.isActivated()) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        !m_const_dt.has_value(),
        "warpx.const_dt and warpx.dt_update_interval cannot be defined simultaneously."
    );
```

逻辑边界：

- `warpx.cfl` 是无量纲安全系数。
- `warpx.const_dt` 直接覆盖 CFL 计算。
- `warpx.max_dt` 是自适应 dt 或静电 dt 的上限。
- `warpx.dt_update_interval` 和 `warpx.const_dt` 互斥。

官方文档位置：`../warpx/Docs/source/usage/parameters.rst:3169-3197`。

```rst
.. pp:param:: warpx.cfl

    and the Courant-Friedrichs-Lewy (CFL) limit. (e.g. for ``warpx.cfl=1``,
    the timestep will be exactly equal to the CFL limit.)
    For some speed v and grid spacing dx, this limits the timestep to ``warpx.cfl * dx / v``.

.. pp:param:: warpx.const_dt

    This can be used with the electromagnetic solver, overriding :pp:param:`warpx.cfl`, but
    it is up to the user to ensure that the CFL condition is met.

.. pp:param:: warpx.dt_update_interval

    Must be greater than ``0`` to use adaptive timestepping, or else :pp:param:`warpx.const_dt` must be specified.
```

## 2. `ComputeDt()` 的特殊 solver 约束

源码位置：`../warpx/Source/Evolve/WarpXComputeDt.cpp:43-57`。

```cpp
void
WarpX::ComputeDt ()
{
    // Handle cases where the timestep is not limited by the speed of light
    // and no constant timestep is provided
    if (electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC) {
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(m_const_dt.has_value(), "warpx.const_dt must be specified with the hybrid-PIC solver.");
    } else if (electromagnetic_solver_id == ElectromagneticSolverAlgo::None) {
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            m_const_dt.has_value() || m_dt_update_interval.isActivated(),
            "warpx.const_dt must be specified with the electrostatic solver, or warpx.dt_update_interval must be > 0."
        );
    }
```

这段是 solver 级约束：

- HybridPIC 必须指定 `warpx.const_dt`。
- electrostatic solver 下 electromagnetic solver 为 `None`，此时必须指定 `const_dt` 或打开自适应更新。

原因是这些路径不一定由光速 CFL 直接限制；用户或粒子速度更新机制必须给出时间步尺度。

## 3. 初始 `dt` 的 solver 分支

源码位置：`../warpx/Source/Evolve/WarpXComputeDt.cpp:58-99`。

```cpp
// Determine the appropriate timestep as limited by the speed of light
const amrex::Real* dx = geom[max_level].CellSize();
amrex::Real deltat = 0.;

if (m_const_dt.has_value()) {
    deltat = m_const_dt.value();
} else if (electrostatic_solver_id  != ElectrostaticSolverAlgo::None) {
    // Set dt for electrostatic algorithm
    if (m_max_dt.has_value()) {
        deltat = m_max_dt.value();
    } else {
        deltat = cfl * minDim(dx) / PhysConst::c;
    }
} else if (electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD) {
    // Computation of dt for spectral algorithm
    // (determined by the minimum cell size in all directions)
    deltat = cfl * minDim(dx) / PhysConst::c;
} else {
```

前半段可以概括为：

$$
\Delta t =
\begin{cases}
\Delta t_{\mathrm{const}}, & \text{if const\_dt is set},\\
\Delta t_{\max}, & \text{electrostatic and max\_dt is set},\\
\mathrm{CFL}\,\min(\Delta x_i)/c, & \text{electrostatic fallback or PSATD}.
\end{cases}
$$

FDTD 分支调用具体算法的 `ComputeMaxDt()`：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
    // - In RZ geometry
    if (electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee) {
        deltat = cfl * CylindricalYeeAlgorithm::ComputeMaxDt(dx,  n_rz_azimuthal_modes);
#elif defined(WARPX_DIM_RSPHERE)
    // - In RZ geometry
    if (electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee) {
        deltat = cfl * SphericalYeeAlgorithm::ComputeMaxDt(dx);
#else
    // - In Cartesian geometry
    if (grid_type == GridType::Collocated) {
        deltat = cfl * CartesianNodalAlgorithm::ComputeMaxDt(dx);
    } else if (electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee
                || electromagnetic_solver_id == ElectromagneticSolverAlgo::ECT) {
        deltat = cfl * CartesianYeeAlgorithm::ComputeMaxDt(dx);
    } else if (electromagnetic_solver_id == ElectromagneticSolverAlgo::CKC) {
        deltat = cfl * CartesianCKCAlgorithm::ComputeMaxDt(dx);
```

因此，FDTD 的稳定时间步不是统一写死为 `min(dx)/c`，而是由 Yee、CKC、collocated/nodal、RZ、spherical 等具体离散 Maxwell 算法提供。

## 4. AMR subcycling 下不同 level 的 `dt`

源码位置：`../warpx/Source/Evolve/WarpXComputeDt.cpp:100-108`。

```cpp
dt.resize(0);
dt.resize(max_level+1,deltat);

if (m_do_subcycling) {
    for (int lev = max_level-1; lev >= 0; --lev) {
        dt[lev] = dt[lev+1] * refRatio(lev)[0];
    }
}
```

没有 subcycling 时，每个 level 使用相同 `dt`。开启 subcycling 后，最细 level 的 `dt[max_level]` 是基准，粗 level 时间步按 refinement ratio 放大：

$$
\Delta t_\ell = r_\ell \Delta t_{\ell+1}.
$$

这和 AMR 的空间 refinement 相匹配：细网格空间步小，时间步也小；粗网格可以用更大的时间步。

## 5. 自适应时间步：由最大粒子速度限制

源码位置：`../warpx/Source/Evolve/WarpXComputeDt.cpp:110-142`。

```cpp
void
WarpX::UpdateDtFromParticleSpeeds ()
{
    const amrex::Real* dx = geom[max_level].CellSize();
    const amrex::Real dx_min = minDim(dx);

    const amrex::ParticleReal max_v = mypc->maxParticleVelocity();
    amrex::Real deltat_new = 0.;

    // Protections from overly-large timesteps
    if (max_v == 0) {
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(m_max_dt.has_value(), "Particles at rest and no constant or maximum timestep specified. Aborting.");
        deltat_new = m_max_dt.value();
    } else {
        deltat_new = cfl * dx_min / max_v;
    }
```

自适应时间步的目标是让最快粒子每步最多跨过 `cfl` 个最小网格间距：

$$
\Delta t = \mathrm{CFL}\frac{\min_i \Delta x_i}{v_{\max}}.
$$

如果所有粒子静止，`v_max=0`，代码要求用户提供 `max_dt`，否则没有自然速度尺度可以限制时间步。

然后应用 `max_dt` 上限，并更新 AMR level：

```cpp
// Restrict to be less than user-specified maximum timestep, if present
if (m_max_dt.has_value()) {
    deltat_new = std::min(deltat_new, m_max_dt.value());
}

// Update dt
dt[max_level] = deltat_new;

for (int lev = max_level-1; lev >= 0; --lev) {
    dt[lev] = dt[lev+1] * refRatio(lev)[0];
}
```

## 6. 在 `Evolve()` 中何时更新

`UpdateDtFromParticleSpeeds()` 不是每步无条件调用，而是由 `m_dt_update_interval` 控制。源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:196-199`。

```cpp
// Update timestep based on particle speeds for solvers with adaptive timesteps
// (electrostatic and theta-implicit EM), provided const_dt is not specified.
if (m_dt_update_interval.contains(step+1)) {
    UpdateDtFromParticleSpeeds();
}
```

因此自适应 dt 的工作流是：

```text
ReadParameters()
  -> parse dt_update_interval
InitData()
  -> ComputeDt()
Evolve loop
  -> if interval contains step+1
       UpdateDtFromParticleSpeeds()
```

## 7. 当前结论

`ComputeDt()` 的逻辑可以压缩成一张决策表：

| 条件 | 初始 `dt` 来源 |
|---|---|
| `warpx.const_dt` 设置 | 直接使用 `const_dt` |
| HybridPIC | 必须设置 `const_dt` |
| electrostatic solver | `max_dt` 或 `cfl*min(dx)/c`，也可运行中自适应 |
| PSATD | `cfl*min(dx)/c` |
| Cartesian Yee/ECT | `cfl*CartesianYeeAlgorithm::ComputeMaxDt(dx)` |
| Cartesian CKC | `cfl*CartesianCKCAlgorithm::ComputeMaxDt(dx)` |
| collocated grid | `cfl*CartesianNodalAlgorithm::ComputeMaxDt(dx)` |
| RZ/RCYLINDER Yee | `cfl*CylindricalYeeAlgorithm::ComputeMaxDt(dx,n_modes)` |
| RSPHERE Yee | `cfl*SphericalYeeAlgorithm::ComputeMaxDt(dx)` |
| subcycling | 粗 level `dt` 按 refinement ratio 放大 |
| adaptive interval | 运行中由 `maxParticleVelocity()` 更新 |

下一篇阶段 3 笔记应进入 `Utils/WarpXMovingWindow.cpp`：moving window 如何更新位置、触发连续注入，以及 boosted-frame 下窗口速度如何变换。
