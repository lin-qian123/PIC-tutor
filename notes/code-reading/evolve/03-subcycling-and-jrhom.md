# `OneStep_sub1()` 与 `OneStep_JRhom()` 精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `../warpx/Source/Evolve/WarpXEvolve.cpp` 中两个非标准主循环分支：

- `OneStep_sub1()`：两层 AMR 的 time subcycling。
- `OneStep_JRhom()`：PSATD-JRhom 多次 `J/rho` 沉积与谱空间场推进。

这两个函数都不是独立物理模型，而是对标准 explicit electromagnetic PIC loop 的时间组织方式重排。理解它们的关键是先抓住时间层：粒子推进、场推进、沉积、fine/coarse 同步、FFT 谱空间更新分别发生在什么相对时间。

## 1. 从 `OneStep()` 分派进入两个分支

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:389-496`。

```cpp
void WarpX::OneStep (
    amrex::Real a_cur_time,
    amrex::Real a_dt,
    int a_step
)
{
    ABLASTR_PROFILE("WarpX::OneStep()");

    // implicit solver
    if (m_implicit_solver) {
        // advance fields and particles by one time step
        m_implicit_solver->OneStep(a_cur_time, a_dt, a_step);
    }
    // explicit solver
    else {
        // electrostatic solver or hybrid solver
        if (electromagnetic_solver_id == ElectromagneticSolverAlgo::None ||
            electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC) {
            // ...
        }
        // electromagnetic solver
        else {
            // without mesh refinement
            if (finest_level == 0) {
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
            }
            // with mesh refinement
            else {
                // without subcycling
                if (!m_do_subcycling) {
                    OneStep_nosub(a_cur_time, a_dt, a_step);
                }
                // with subcycling
                else {
                    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
                        finest_level == 1,
                        "Subcycling not implemented with more than 1 mesh refinement level"
                    );
                    AMREX_ALWAYS_ASSERT_WITH_MESSAGE(
                        m_collisions_split_momentum_push == 0,
                        "Collisions with split momentum push not yet implemented with subcycling."
                        "Set `collisions.split_momentum_push=0` to use subcycling with standard (pre-v-push collisions placement) collisions model."
                    );
                    // perform particle collisions
                    ExecutePythonCallback("beforecollisions");
                    mypc->doCollisions(a_step, a_cur_time, a_dt);
                    ExecutePythonCallback("aftercollisions");

                    OneStep_sub1(a_cur_time);
                }
            }
        }
    }
}
```

这个分派给出三个功能边界：

- `OneStep_JRhom()` 只在 `finest_level == 0` 的无 mesh refinement 路径进入。
- `OneStep_sub1()` 只在 `finest_level == 1` 且 `m_do_subcycling` 为真时进入。
- JRhom 和 subcycling 都暂不支持 `collisions.split_momentum_push=1`，因为 split momentum push 会把碰撞放进动量半步中间，而这两个特殊循环已经有自己的时间层结构。

## 2. `warpx.do_subcycling` 参数与时间步

官方文档位置：`../warpx/Docs/source/usage/parameters.rst:3813-3828`。

```rst
.. pp:param:: warpx.do_subcycling
    :type: ``0`` or ``1``
    :default: 0

    Whether or not to use sub-cycling. Different refinement levels have a
    different cell size, which results in different Courant–Friedrichs–Lewy
    (CFL) limits for the time step. By default, when using mesh refinement,
    the same time step is used for all levels. This time step is
    taken as the CFL limit of the finest level. Hence, for coarser
    levels, the timestep is only a fraction of the CFL limit for this
    level, which may lead to numerical artifacts. With sub-cycling, each level
    evolves with its own time step, set to its own CFL limit. In practice, it
    means that when level 0 performs one iteration, level 1 performs two
    iterations. Currently, this option is only supported when
    :pp:param:`amr.max_level = 1`.
```

`ComputeDt()` 中，subcycling 会让粗层时间步比细层大。源码位置：`../warpx/Source/Evolve/WarpXComputeDt.cpp:100-108`，前一篇笔记已展开：

```cpp
dt.resize(0);
dt.resize(max_level+1,deltat);

if (m_do_subcycling) {
    for (int lev = max_level-1; lev >= 0; --lev) {
        dt[lev] = dt[lev+1] * refRatio(lev)[0];
    }
}
```

若 `refRatio(0)=2`，则

$$
\Delta t_0 = 2\Delta t_1.
$$

`OneStep_sub1()` 的注释也明确当前版本只支持两层、refinement ratio 2。源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:1043-1064`。

```cpp
/**
 *  \brief Perform one PIC iteration, with subcycling
 *  i.e. The fine patch uses a smaller timestep (and steps more often)
 *  than the coarse patch, for the field advance and particle pusher.
 *
 * This version of subcycling only works for 2 levels and with a refinement
 * ratio of 2.
 * The particles and fields of the fine patch are pushed twice
 * (with dt[coarse]/2) in this routine.
 * The particles of the coarse patch and mother grid are pushed only once
 * (with dt[coarse]). The fields on the coarse patch and mother grid
 * are pushed in a way which is equivalent to pushing once only, with
 * a current which is the average of the coarse + fine current at the 2
 * steps of the fine grid.
 *
 */
```

物理/数值意义：

- 细网格 cell 更小，CFL 限制更严格，因此细层用更小时间步。
- 粗层如果也用最细层时间步，会浪费粗层 CFL 余量，并可能引入不必要的多层同步误差。
- subcycling 让 level 1 走两次小步，level 0 走一次大步；关键难点在于两次 fine current/rho 如何等效反馈到 coarse patch 和 mother grid。

## 3. `OneStep_sub1()` 的总流程

`OneStep_sub1()` 开头先断言功能边界。源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:1065-1080`。

```cpp
void
WarpX::OneStep_sub1 (Real cur_time)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        electrostatic_solver_id == ElectrostaticSolverAlgo::None,
        "Electrostatic solver cannot be used with sub-cycling."
    );

    // TODO: we could save some charge depositions

    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(finest_level == 1, "Must have exactly two levels");
    const int fine_lev = 1;
    const int coarse_lev = 0;

    using warpx::fields::FieldType;

    bool const skip_lev0_coarse_patch = true;
```

主流程可以压缩成：

```text
fine step 1:
  PushParticlesandDeposit(fine_lev, cur_time, FirstHalf)
  restrict fine current/rho to coarse patch
  fine E/B/F advance over dt[1]

coarse first half:
  PushParticlesandDeposit(coarse_lev, cur_time, None)
  store coarse current
  add fine-level current/rho contribution
  evolve fine-level coarse patch over dt[1]
  evolve level-0 fine patch over 0.5 dt[0]
  update auxiliary fields

fine step 2:
  PushParticlesandDeposit(fine_lev, cur_time+dt[1], SecondHalf)
  restrict fine current/rho again
  fine E/B/F advance over dt[1]

coarse second half:
  restore stored coarse current
  add second fine-level current/rho contribution
  evolve fine-level coarse patch over dt[1]
  evolve level-0 fine patch over 0.5 dt[0]
  PML damping and guard exchange
```

其中 `PatchType::fine` 和 `PatchType::coarse` 不是 AMR level 的同义词。对 `lev=1`：

- `PatchType::fine` 是 fine level 的真实 fine patch。
- `PatchType::coarse` 是 fine level 对应的 coarse patch，用于粗细交界同步。

## 4. Fine step 1：细层粒子/场推进与 restriction

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:1080-1120`。

```cpp
// i) Push particles and fields on the fine patch (first fine step)
PushParticlesandDeposit(fine_lev, cur_time, SubcyclingHalf::FirstHalf);
RestrictCurrentFromFineToCoarsePatch(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::current_cp, finest_level, skip_lev0_coarse_patch), fine_lev);
RestrictRhoFromFineToCoarsePatch(fine_lev);
if (use_filter) {
    ApplyFilterMF( m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level), fine_lev);
}
SumBoundaryJ(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    fine_lev, Geom(fine_lev).periodicity());

if (m_fields.has(FieldType::rho_fp, finest_level) &&
    m_fields.has(FieldType::rho_cp, finest_level)) {
    ApplyFilterandSumBoundaryRho(
        m_fields.get_mr_levels(FieldType::rho_fp, finest_level),
        m_fields.get_mr_levels(FieldType::rho_cp, finest_level, skip_lev0_coarse_patch),
        fine_lev, PatchType::fine, 0, 2*ncomps);
}

EvolveB(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], SubcyclingHalf::FirstHalf, cur_time);
EvolveF(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], /*rho_comp=*/0);
FillBoundaryB(fine_lev, PatchType::fine, guard_cells.ng_FieldSolver,
              WarpX::sync_nodal_points);
FillBoundaryF(fine_lev, PatchType::fine, guard_cells.ng_alloc_F,
              WarpX::sync_nodal_points);

EvolveE(fine_lev, PatchType::fine, dt[fine_lev], cur_time);
FillBoundaryE(fine_lev, PatchType::fine, guard_cells.ng_FieldGather);

EvolveB(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], SubcyclingHalf::SecondHalf, cur_time + 0.5_rt * dt[fine_lev]);
EvolveF(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], /*rho_comp=*/1);
```

细层第一小步仍是 Yee/leapfrog 风格：

$$
B^{n}\rightarrow B^{n+1/2},\qquad
E^{n}\rightarrow E^{n+1},\qquad
B^{n+1/2}\rightarrow B^{n+1}.
$$

这里 `rho_comp=0` 和 `rho_comp=1` 对应不同时间层的电荷密度分量；subcycling 会在一个粗步中保存两次 fine 层沉积，所以后面 `AddRhoFromFineLevelandSumBoundary(..., 0, ncomps)` 和 `(..., ncomps, ncomps)` 分别取两段。

restriction helper 在 `../warpx/Source/Parallelization/WarpXComm.cpp:1457-1477`：

```cpp
void WarpX::RestrictCurrentFromFineToCoarsePatch (
    const ablastr::fields::MultiLevelVectorField& J_fp,
    const ablastr::fields::MultiLevelVectorField& J_cp,
    const int lev)
{
    J_cp[lev][0]->setVal(0.0);
    J_cp[lev][1]->setVal(0.0);
    J_cp[lev][2]->setVal(0.0);

    const IntVect& refinement_ratio = refRatio(lev-1);

    std::array<const MultiFab*,3> fine { J_fp[lev][0],
                                         J_fp[lev][1],
                                         J_fp[lev][2] };
    std::array<      MultiFab*,3> crse { J_cp[lev][0],
                                         J_cp[lev][1],
                                         J_cp[lev][2] };
    ablastr::coarsen::average::Coarsen(*crse[0], *fine[0], refinement_ratio );
    ablastr::coarsen::average::Coarsen(*crse[1], *fine[1], refinement_ratio );
    ablastr::coarsen::average::Coarsen(*crse[2], *fine[2], refinement_ratio );
}
```

它做的是体平均 coarsening：

$$
\mathbf{J}_{\mathrm{cp}}(I)
=\frac{1}{r_xr_yr_z}
\sum_{\mathbf{i}\in I}\mathbf{J}_{\mathrm{fp}}(\mathbf{i}),
$$

其中 $I$ 是一个 coarse cell 对应的 fine cells 集合。

`RestrictRhoFromFineToCoarsePatch()` 同理，位置 `../warpx/Source/Parallelization/WarpXComm.cpp:1652-1660`：

```cpp
void WarpX::RestrictRhoFromFineToCoarsePatch ( const int lev )
{
    if (m_fields.has(FieldType::rho_fp, lev)) {
        m_fields.get(FieldType::rho_cp, lev)->setVal(0.0);
        const IntVect& refinement_ratio = refRatio(lev-1);
        ablastr::coarsen::average::Coarsen(*m_fields.get(FieldType::rho_cp, lev), *m_fields.get(FieldType::rho_fp, lev), refinement_ratio );
    }
}
```

## 5. Coarse first half：保存 coarse current 并叠加 fine contribution

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:1120-1158`。

```cpp
// ii) Push particles on the coarse patch and mother grid.
// Push the fields on the coarse patch and mother grid
// by only half a coarse step (first half)
PushParticlesandDeposit(coarse_lev, cur_time, SubcyclingHalf::None);
::StoreCurrent(coarse_lev, m_fields);
AddCurrentFromFineLevelandSumBoundary(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::current_cp, finest_level, skip_lev0_coarse_patch),
    m_fields.get_mr_levels_alldirs(FieldType::current_buf, finest_level, skip_lev0_coarse_patch), coarse_lev);

if (m_fields.has(FieldType::rho_fp, finest_level) &&
    m_fields.has(FieldType::rho_cp, finest_level) &&
    m_fields.has(FieldType::rho_buf, finest_level)) {
    AddRhoFromFineLevelandSumBoundary(
        m_fields.get_mr_levels(FieldType::rho_fp, finest_level),
        m_fields.get_mr_levels(FieldType::rho_cp, finest_level, skip_lev0_coarse_patch),
        m_fields.get_mr_levels(FieldType::rho_buf, finest_level, skip_lev0_coarse_patch),
        coarse_lev, 0, ncomps);
}

EvolveB(fine_lev, PatchType::coarse, dt[fine_lev], SubcyclingHalf::FirstHalf, cur_time);
EvolveF(fine_lev, PatchType::coarse, dt[fine_lev], /*rho_comp=*/0);
FillBoundaryB(fine_lev, PatchType::coarse, guard_cells.ng_FieldGather);
FillBoundaryF(fine_lev, PatchType::coarse, guard_cells.ng_FieldSolverF);

EvolveE(fine_lev, PatchType::coarse, dt[fine_lev], cur_time);
FillBoundaryE(fine_lev, PatchType::coarse, guard_cells.ng_FieldGather);

EvolveB(coarse_lev, PatchType::fine, 0.5_rt*dt[coarse_lev], SubcyclingHalf::FirstHalf, cur_time);
EvolveF(coarse_lev, PatchType::fine, 0.5_rt*dt[coarse_lev], /*rho_comp=*/0);
```

`StoreCurrent()` 和 `RestoreCurrent()` 是 subcycling 的关键。源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:80-105`。

```cpp
void StoreCurrent (int lev, ablastr::fields::MultiFabRegister& fields)
{
    using ablastr::fields::Direction;
    using warpx::fields::FieldType;

    for (int idim = 0; idim < 3; ++idim) {
        const auto dir = Direction{idim};
        if (fields.has(FieldType::current_store, dir,lev)) {
            MultiFab::Copy(*fields.get(FieldType::current_store, dir, lev),
                           *fields.get(FieldType::current_fp, dir, lev),
                           0, 0, 1, fields.get(FieldType::current_store, dir, lev)->nGrowVect());
        }
    }
}

void RestoreCurrent (int lev, ablastr::fields::MultiFabRegister& fields)
{
    using ablastr::fields::Direction;
    using warpx::fields::FieldType;

    for (int idim = 0; idim < 3; ++idim) {
        const auto dir = Direction{idim};
        if (fields.has(FieldType::current_store, dir, lev)) {
            std::swap(
                *fields.get(FieldType::current_fp, dir, lev),
                *fields.get(FieldType::current_store, dir, lev)
            );
        }
    }
}
```

为什么要存 current？因为 coarse 粒子只推进一次，但 coarse field 被拆成两个半粗步推进。每个半步都要叠加对应 fine substep 的 coarse-patch current；第二半步前必须恢复 coarse 粒子自身沉积出来的原始 current，再叠加第二次 fine contribution。

`AddCurrentFromFineLevelandSumBoundary()` 在 `../warpx/Source/Parallelization/WarpXComm.cpp:1575-1648`，核心是把 fine level 的 coarse patch 和 buffer patch contribution 累加回 coarse level。

```cpp
void WarpX::AddCurrentFromFineLevelandSumBoundary (
    const ablastr::fields::MultiLevelVectorField& J_fp,
    const ablastr::fields::MultiLevelVectorField& J_cp,
    const ablastr::fields::MultiLevelVectorField& J_buffer,
    const int lev)
{
    const amrex::Periodicity& period = Geom(lev).periodicity();

    if (use_filter)
    {
        ApplyFilterMF(J_fp, lev);
    }
    SumBoundaryJ(J_fp, lev, period);

    if (lev < finest_level)
    {
        // When there are current buffers, unlike coarse patch,
        // we don't care about the final state of them.

        for (int idim=0; idim<3; ++idim)
        {
            MultiFab mf(J_fp[lev][idim]->boxArray(),
                        J_fp[lev][idim]->DistributionMap(), J_fp[lev][idim]->nComp(), 0);
            mf.setVal(0.0);

            const IntVect ng = J_cp[lev+1][idim]->nGrowVect();
            // ...
            SumBoundaryJ(J_cp, lev+1, idim, period);
            MultiFab::Add(*J_fp[lev][idim], mf, 0, 0, J_fp[lev+1][idim]->nComp(), 0);
        }
    }
}
```

这段中的 `mf` 是临时 coarse-level `MultiFab`，通过 `ParallelAdd` 把 fine level coarse/buffer patch 的数据投到 coarse layout，再加到 `J_fp[lev]`。

## 6. Fine step 2 与 coarse second half

第二个 fine substep 的源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:1159-1199`。

```cpp
// iv) Push particles and fields on the fine patch (second fine step)
PushParticlesandDeposit(fine_lev, cur_time + dt[fine_lev], SubcyclingHalf::SecondHalf);
RestrictCurrentFromFineToCoarsePatch(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::current_cp, finest_level, skip_lev0_coarse_patch), fine_lev);
RestrictRhoFromFineToCoarsePatch(fine_lev);
if (use_filter) {
    ApplyFilterMF( m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level), fine_lev);
}
SumBoundaryJ( m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level), fine_lev, Geom(fine_lev).periodicity());

if (m_fields.has(FieldType::rho_fp, finest_level) &&
    m_fields.has(FieldType::rho_cp, finest_level)) {
    ApplyFilterandSumBoundaryRho(
        m_fields.get_mr_levels(FieldType::rho_fp, finest_level),
        m_fields.get_mr_levels(FieldType::rho_cp, finest_level, skip_lev0_coarse_patch),
        fine_lev, PatchType::fine, 0, ncomps);
}

EvolveB(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], SubcyclingHalf::FirstHalf, cur_time + dt[fine_lev]);
EvolveF(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], /*rho_comp=*/0);
```

注意第二次 fine 粒子推进的 `cur_time + dt[fine_lev]`。这使 fine substeps 覆盖

$$
[t^n,t^n+\Delta t_1],\qquad
[t^n+\Delta t_1,t^n+2\Delta t_1]=[t^n+\Delta t_1,t^n+\Delta t_0].
$$

coarse second half 源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:1203-1269`。

```cpp
// v) Push the fields on the coarse patch and mother grid
// by only half a coarse step (second half)
::RestoreCurrent(coarse_lev, m_fields);
AddCurrentFromFineLevelandSumBoundary(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::current_cp, finest_level, skip_lev0_coarse_patch),
    m_fields.get_mr_levels_alldirs(FieldType::current_buf, finest_level, skip_lev0_coarse_patch),
    coarse_lev);

if (m_fields.has(FieldType::rho_fp, finest_level) &&
    m_fields.has(FieldType::rho_cp, finest_level) &&
    m_fields.has(FieldType::rho_buf, finest_level)) {
    AddRhoFromFineLevelandSumBoundary(
        m_fields.get_mr_levels(FieldType::rho_fp, finest_level),
        m_fields.get_mr_levels(FieldType::rho_cp, finest_level, skip_lev0_coarse_patch),
        m_fields.get_mr_levels(FieldType::rho_buf, finest_level, skip_lev0_coarse_patch),
        coarse_lev, ncomps, ncomps);
}

EvolveE(fine_lev, PatchType::coarse, dt[fine_lev], cur_time + 0.5_rt * dt[fine_lev]);
FillBoundaryE(fine_lev, PatchType::coarse, guard_cells.ng_FieldSolver,
              WarpX::sync_nodal_points);

EvolveB(fine_lev, PatchType::coarse, dt[fine_lev], SubcyclingHalf::SecondHalf, cur_time + 0.5_rt * dt[fine_lev]);
EvolveF(fine_lev, PatchType::coarse, dt[fine_lev], /*rho_comp=*/1);
```

这里 `AddRhoFromFineLevelandSumBoundary(..., ncomps, ncomps)` 取第二组 rho 分量，配合 fine step 1 中的 `(..., 0, ncomps)`。这就是注释中“coarse field 使用两次 fine current 的平均效果”的实现结构：每个 half coarse step 使用对应 fine substep 的沉积贡献。

## 7. `psatd.JRhom` 参数和理论入口

官方参数文档位置：`../warpx/Docs/source/usage/parameters.rst:3528-3540`。

```rst
.. pp:param:: psatd.JRhom
    :type: ``string``

    This determines whether the PSATD JRhom algorithm is used, where current deposition and field update are performed multiple times within one time step, while field gathering is performed only once.
    For simulations with strong numerical Cherenkov instability (NCI), the PSATD JRhom algorithm is recommended in combination with :pp:param:`psatd.do_time_averaging = 1`.
    The input parameter is a string composed by two characters and one digit.
    The first character represents the time dependency of J within the time step over which the electromagnetic fields are evolved, e.g., "C" for constant in time, "L" for linear in time, "Q" for quadratic in time.
    The second character represents the time dependency of rho within the time step over which the electromagnetic fields are evolved, following the same naming convention as for J.
    The last digit is an integer that represents the number of subintervals used in the JRhom algorithm.
    Examples: "CL1" (equivalent to the standard PSATD PIC algorithm), "CL2", "LL4", etc.
```

理论文档位置：`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:286-306`。其中给出 modified Maxwell equations 的谱空间形式：

```rst
   \begin{align}
   \frac{\partial\boldsymbol{\widetilde{E}}}{\partial t} & = i\boldsymbol{k}\times\boldsymbol{\widetilde{B}}-\boldsymbol{\widetilde{J}} + i\boldsymbol{k}{\widetilde{F}} \,, \\
   \frac{\partial\boldsymbol{\widetilde{B}}}{\partial t} & = -i\boldsymbol{k}\times\boldsymbol{\widetilde{E}} \,, \\
   \frac{\partial{\widetilde{F}}}{\partial t} & = i\boldsymbol{k}\cdot\boldsymbol{\widetilde{E}} - \widetilde{\rho} \,.
   \end{align}
```

对应数学形式是

$$
\frac{\partial\widetilde{\mathbf E}}{\partial t}
=i\mathbf{k}\times\widetilde{\mathbf B}-\widetilde{\mathbf J}
+i\mathbf{k}\widetilde F,
$$

$$
\frac{\partial\widetilde{\mathbf B}}{\partial t}
=-i\mathbf{k}\times\widetilde{\mathbf E},
$$

$$
\frac{\partial\widetilde F}{\partial t}
=i\mathbf{k}\cdot\widetilde{\mathbf E}-\widetilde{\rho}.
$$

JRhom 的核心不是改变粒子 push，而是在一个 PIC step 内把源项 $\widetilde{\mathbf J}(t)$ 和 $\widetilde\rho(t)$ 允许为分段常数、线性或二次函数，并把一个大步分为

$$
\delta t=\frac{\Delta t}{m}
$$

的多个 subinterval。文档引用 `pt-shapovalPRE2024`，并指出标准 PSATD 相当于 $\mathbf J$ 常数、$\rho$ 线性。

## 8. `psatd.JRhom` 源码解析

源码位置：`../warpx/Source/WarpX.cpp:1584-1634`。

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
    else {
        WARPX_ABORT_WITH_MESSAGE(
            "Time dependency '" + std::string(1, JRhom_input[0]) + "' of J set by psatd.JRhom = '" + JRhom_input + "' not valid."
            " Valid options are 'C' (constant), 'L' (linear), 'Q' (quadratic)."
        );
    }
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
```

后半段解析 subinterval 数并排除 Vay deposition：

```cpp
    // parse number of subintervals from last digit
    for (const char m : JRhom_input.substr(2)) {
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            std::isdigit(m),
            "psatd.JRhom = '" + JRhom_input + "' input string must include integer 'm' after the first two characters (e.g., 'CL1')."
        );
    }
    m_JRhom_subintervals = std::stoi(JRhom_input.substr(2));
}

if (current_deposition_algo == CurrentDepositionAlgo::Vay) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        m_JRhom == false,
        "Vay deposition not implemented with JRhom algorithm");
}
```

因此 `"LL4"` 表示：

- `J` 在每个 step 内按 linear time dependency 处理；
- `rho` 也按 linear time dependency 处理；
- 一个 PIC step 分为 4 个 JRhom subinterval。

源码还强制 JRhom 下关闭 current correction 默认值，因为该功能尚未实现。位置：`../warpx/Source/WarpX.cpp:1651-1655`。

```cpp
// TODO Remove this default when current correction will
// be implemented for the PSATD-JRhom algorithm as well
if (m_JRhom) { current_correction = false; }
```

官方参数文档也说明 current correction 不适用于 PSATD JRhom，位置 `../warpx/Docs/source/usage/parameters.rst:3405-3422`。

## 9. `OneStep_JRhom()` 第一段：粒子只 push/gather 一次

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:839-869`。

```cpp
void
WarpX::OneStep_JRhom (const amrex::Real cur_time)
{
#ifdef WARPX_USE_FFT

    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD,
        "JRhom algorithm not implemented with the FDTD solver"
    );

    using warpx::fields::FieldType;

    bool const skip_lev0_coarse_patch = true;

    const int rho_mid = spectral_solver_fp[0]->m_spectral_index.rho_mid;
    const int rho_new = spectral_solver_fp[0]->m_spectral_index.rho_new;

    // Push particle from x^{n} to x^{n+1}
    //               from p^{n-1/2} to p^{n+1/2}
    const bool skip_deposition = true;
    PushParticlesandDeposit(cur_time, skip_deposition);

    // Initialize PSATD-JRhom loop:

    // 1) Prepare E,B,F,G fields in spectral space
    PSATDForwardTransformEB();
    if (WarpX::do_dive_cleaning) { PSATDForwardTransformF(); }
    if (WarpX::do_divb_cleaning) { PSATDForwardTransformG(); }
```

这里粒子推进只做一次，而且 `skip_deposition=true`。这与官方文档一致：field gathering 只发生一次，之后在不同相对时间重复沉积 `J/rho`。粒子轨道信息已经在容器中可用于 `DepositCurrent(..., relative_time)` 和 `DepositCharge(..., relative_time)`。

## 10. JRhom 初始化沉积：旧时间源项

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:870-904`。

```cpp
// 2) Set the averaged fields to zero
if (WarpX::fft_do_time_averaging) { PSATDEraseAverageFields(); }

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

为什么有 `-dt`？因为线性或二次时间依赖需要旧端点或旧区间源项作为多项式构造的一部分。常数源项不需要 old/new 区分，所以 `time_dependency_* == Constant` 时跳过这一步。

## 11. JRhom 主循环：多次沉积、多次谱推进

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:906-986`。

```cpp
// Number of depositions for multi-J scheme
const int n_deposit = WarpX::m_JRhom_subintervals;
// Time sub-step for each multi-J deposition
const amrex::Real sub_dt = dt[0] / static_cast<amrex::Real>(n_deposit);
// Whether to perform PSATD-JRhom depositions on a time interval that spans
// one or two full time steps (from n*dt to (n+1)*dt, or from n*dt to (n+2)*dt)
const int n_loop = (WarpX::fft_do_time_averaging) ? 2*n_deposit : n_deposit;

// Loop over PSATD-JRhom depositions
for (int i_deposit = 0; i_deposit < n_loop; i_deposit++)
{
    // Move J from new to old if J is linear or quadratic in time
    if (time_dependency_J != TimeDependencyJ::Constant) { PSATDMoveJNewToJOld(); }

    const amrex::Real t_deposit_current = (time_dependency_J == TimeDependencyJ::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;

    const amrex::Real t_deposit_charge = (time_dependency_rho == TimeDependencyRho::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;

    // Deposit new J at relative time t_deposit_current with time step dt
    std::string const current_string = (do_current_centering) ? "current_fp_nodal" : "current_fp";
    mypc->DepositCurrent( m_fields.get_mr_levels_alldirs(current_string, finest_level), dt[0], t_deposit_current);
    SyncCurrent("current_fp");
    PSATDForwardTransformJ("current_fp", "current_cp");
```

沉积时间的规则是：

$$
t_J =
\begin{cases}
(i-m+1)\delta t, & J\ \text{linear},\\
(i-m+\frac12)\delta t, & J\ \text{constant or quadratic midpoint stage},
\end{cases}
$$

其中 $m=n_{\mathrm{deposit}}$。循环从相对时间负区间开始，是为了构造跨越当前 step 的源项历史。若开启 time averaging，`n_loop=2m`，会覆盖两个完整时间步区间，用于场平均。

二次时间依赖会额外沉积 midpoint：

```cpp
    if (time_dependency_J == TimeDependencyJ::Quadratic)
    {
        PSATDMoveJNewToJMid();
        mypc->DepositCurrent( m_fields.get_mr_levels_alldirs(current_string, finest_level),  dt[0], t_deposit_current + 0.5_rt*sub_dt);
        SyncCurrent("current_fp");
        PSATDForwardTransformJ("current_fp", "current_cp");
    }
```

rho 的结构类似：

```cpp
    // Deposit new rho
    if (m_fields.has(FieldType::rho_fp, 0))
    {
        ablastr::fields::MultiLevelScalarField const rho_fp = m_fields.get_mr_levels(FieldType::rho_fp, finest_level);

        std::string const rho_fp_string = "rho_fp";
        std::string const rho_cp_string = "rho_cp";

        // Move rho from new to old if rho is linear in time
        if (time_dependency_rho != TimeDependencyRho::Constant) { PSATDMoveRhoNewToRhoOld(); }

        // Deposit rho at relative time t_deposit_charge
        mypc->DepositCharge(rho_fp, t_deposit_charge);
        SyncRho();
        const int rho_idx = (time_dependency_rho != TimeDependencyRho::Constant) ? rho_new : rho_mid;
        PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 0, rho_idx);

        if (time_dependency_rho == TimeDependencyRho::Quadratic)
        {
            PSATDMoveRhoNewToRhoMid();
            mypc->DepositCharge(rho_fp, t_deposit_charge + 0.5_rt*sub_dt);
            SyncRho();
            PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 0, rho_new);
        }
    }
```

随后检查 current correction 并推进谱场：

```cpp
    if (WarpX::current_correction)
    {
        WARPX_ABORT_WITH_MESSAGE(
            "Current correction not implemented for PSATD-JRhom algorithm.");
    }

    // Advance E,B,F,G fields in time and update the average fields
    PSATDPushSpectralFields();

    // Transform non-average fields E,B,F,G after n_deposit pushes
    // (the relative time reached here coincides with an integer full time step)
    if (i_deposit == n_deposit-1)
    {
        PSATDBackwardTransformEB();
        if (WarpX::do_dive_cleaning) { PSATDBackwardTransformF(); }
        if (WarpX::do_divb_cleaning) { PSATDBackwardTransformG(); }
    }
}
```

`i_deposit == n_deposit-1` 时，谱场已经从当前 step 推到下一个整数时间层，才把非平均的 `E/B/F/G` 变换回实空间。若 time averaging 开启，循环还会继续第二个 step 的积分，用于平均场。

## 12. JRhom 收尾：平均场、PML、边界和 guard cells

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:988-1038`。

```cpp
// Transform fields back to real space
if (WarpX::fft_do_time_averaging)
{
    // We summed the integral of the field over 2*dt
    PSATDScaleAverageFields(1._rt / (2._rt*dt[0]));
    PSATDBackwardTransformEBavg(
        m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_fp, finest_level),
        m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_fp, finest_level),
        m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_cp, finest_level, skip_lev0_coarse_patch),
        m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_cp, finest_level, skip_lev0_coarse_patch)
    );
}

// Evolve fields in PML
for (int lev = 0; lev <= finest_level; ++lev)
{
    if (do_pml && pml[lev]->ok())
    {
        pml[lev]->PushPSATD(m_fields, lev);
    }
    ApplyEfieldBoundary(lev, PatchType::fine, cur_time + dt[0]);
    if (lev > 0) { ApplyEfieldBoundary(lev, PatchType::coarse, cur_time + dt[0]); }
    ApplyBfieldBoundary(lev, PatchType::fine, SubcyclingHalf::FirstHalf, cur_time + dt[0]);
    if (lev > 0) { ApplyBfieldBoundary(lev, PatchType::coarse, SubcyclingHalf::FirstHalf, cur_time + dt[0]); }
}

// Damp fields in PML before exchanging guard cells
if (do_pml)
{
    DampPML();
}

// Exchange guard cells and synchronize nodal points
FillBoundaryE(guard_cells.ng_alloc_EB, WarpX::sync_nodal_points);
FillBoundaryB(guard_cells.ng_alloc_EB, WarpX::sync_nodal_points);
if (WarpX::do_dive_cleaning || WarpX::do_pml_dive_cleaning) {
    FillBoundaryF(guard_cells.ng_alloc_F, WarpX::sync_nodal_points);
}
if (WarpX::do_divb_cleaning || WarpX::do_pml_divb_cleaning) {
    FillBoundaryG(guard_cells.ng_alloc_G, WarpX::sync_nodal_points);
}
```

这段说明 JRhom 虽然主体在谱空间，但最终仍要回到 WarpX 的实空间 field register，并走 PML、边界条件和 guard cell exchange。它不是独立于 WarpX 场系统之外的特殊 solver，而是 PSATD solver 的一个时间积分组织方式。

## 13. 两个分支的本质差异

`OneStep_sub1()` 解决的是 AMR 多层 CFL 问题：

$$
\Delta t_\ell \propto \Delta x_\ell,\qquad
\Delta t_0=2\Delta t_1.
$$

它的难点是 coarse/fine 电流和电荷守恒同步。

`OneStep_JRhom()` 解决的是 PSATD 中源项时间依赖的高阶表示问题：

$$
\widetilde{\mathbf J}(t),\ \widetilde{\rho}(t)
\quad\text{在一个 PIC step 内按 C/L/Q 分段近似。}
$$

它的难点是粒子只推进一次，但要在多个相对时间沉积源项，并在谱空间多次推进场。

二者共同点是：都没有改变 PIC 的基本闭环

```text
gather -> push particles -> deposit sources -> push fields -> synchronize boundaries
```

但它们改变了这个闭环在一个 coarse/global step 内的拆分方式。

## 14. 后续需要继续追踪的源码

本笔记已经把两个入口函数和直接同步 helper 固定下来，但完整逐行讲透还需要后续进入：

- `FieldSolver/WarpXPushFieldsEM.cpp`：`EvolveE/B/F/G` 在 `PatchType::fine/coarse` 与 `SubcyclingHalf` 下的真实 stencil。
- `FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomFirstOrder.cpp` 与 `PsatdAlgorithmJRhomSecondOrder.cpp`：`PSATDPushSpectralFields()` 内部如何使用 `J_old/J_mid/J_new` 与 `rho_old/rho_mid/rho_new`。
- `Parallelization/WarpXComm.cpp`：`SyncCurrent()`、`SyncRho()`、`ParallelAdd()`、`WarpXSumGuardCells()` 的通信边界。
- `Particles/WarpXParticleContainer.cpp`：`DepositCurrent(..., relative_time)` 和 `DepositCharge(..., relative_time)` 如何从粒子 old/new 位置构造相对时间沉积。

