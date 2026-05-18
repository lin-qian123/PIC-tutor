# FieldSolver 顶层分派与 `EvolveE/B/F/G` 第一轮精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记进入 `../warpx/Source/FieldSolver`，先回答一个结构问题：`Evolve/WarpXEvolve.cpp` 中的 `EvolveB()`、`EvolveE()`、`EvolveF()`、`EvolveG()` 到底调用了哪些 field solver 对象，`fp/cp/PML` 如何分派，FDTD kernel 如何对应 Maxwell 方程。

本轮覆盖：

- `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveF.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveG.cpp`
- 官方理论文档 `../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst`

## 1. 连续方程与 WarpX 的单位写法

官方理论文档给出的 FDTD 方程位置：`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:31-80`。

```rst
.. math::
   D_{t}\mathbf{B} = -\nabla\times\mathbf{E}
   :label: Faraday-2

.. math::
   D_{t}\mathbf{E} = \nabla\times\mathbf{B}-\mathbf{J}
   :label: Ampere-2

.. math::
   \left[\nabla\cdot\mathbf{E} = \rho\right]
   :label: Gauss-2

.. math::
   \left[\nabla\cdot\mathbf{B} = 0\right].
   :label: divb-2
```

文档这里采用归一化写法；源码中 `EvolveE.cpp` 使用 SI 常数：

$$
\frac{\partial \mathbf B}{\partial t}=-\nabla\times\mathbf E,
$$

$$
\frac{\partial \mathbf E}{\partial t}
=c^2\nabla\times\mathbf B-\frac{\mathbf J}{\epsilon_0}
=c^2\left(\nabla\times\mathbf B-\mu_0\mathbf J\right),
$$

因为

$$
c^2\mu_0=\frac{1}{\epsilon_0}.
$$

WarpX 的显式 leapfrog 时间层在 `OneStep_nosub()` 中体现为：

```text
B: n     -> n+1/2
E: n     -> n+1
B: n+1/2 -> n+1
```

`F` 和 `G` 是 hyperbolic divergence-cleaning 标量：

$$
\frac{\partial F}{\partial t}=\nabla\cdot\mathbf E-\rho/\epsilon_0,
$$

$$
\frac{\partial \mathbf E}{\partial t}
=c^2(\nabla\times\mathbf B-\mu_0\mathbf J+\nabla F),
$$

$$
\frac{\partial G}{\partial t}=c^2\nabla\cdot\mathbf B,
$$

$$
\frac{\partial \mathbf B}{\partial t}
=-\nabla\times\mathbf E+\nabla G.
$$

这些式子分别对应 `EvolveF.cpp`、`EvolveE.cpp` 中的 `grad(F)` 修正、`EvolveG.cpp` 和 `EvolveB.cpp` 中的 `grad(G)` 修正。

## 2. `WarpXPushFieldsEM.cpp`：field push 的顶层路由

`EvolveB()` 的三层重载位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:946-990`。

```cpp
void
WarpX::EvolveB (amrex::Real a_dt, SubcyclingHalf subcycling_half, amrex::Real start_time)
{
    for (int lev = 0; lev <= finest_level; ++lev) {
        EvolveB(lev, a_dt, subcycling_half, start_time);
    }

    // Allow execution of Python callback after B-field push
    ExecutePythonCallback("afterBpush");
}

void
WarpX::EvolveB (int lev, amrex::Real a_dt, SubcyclingHalf subcycling_half, amrex::Real start_time)
{
    ABLASTR_PROFILE("WarpX::EvolveB()");
    EvolveB(lev, PatchType::fine, a_dt, subcycling_half, start_time);
    if (lev > 0)
    {
        EvolveB(lev, PatchType::coarse, a_dt, subcycling_half, start_time);
    }
}

void
WarpX::EvolveB (int lev, PatchType patch_type, amrex::Real a_dt, SubcyclingHalf subcycling_half, amrex::Real start_time)
{
    // Evolve B field in regular cells
    if (patch_type == PatchType::fine) {
        m_fdtd_solver_fp[lev]->EvolveB( m_fields,
                                        lev,
                                        patch_type,
                                        m_flag_info_face[lev], m_borrowing[lev], a_dt );
    } else {
        m_fdtd_solver_cp[lev]->EvolveB( m_fields,
                                        lev,
                                        patch_type,
                                        m_flag_info_face[lev], m_borrowing[lev], a_dt );
    }
```

逐层解释：

- 第一层遍历所有 AMR level，并在所有 level 的 B push 后触发 Python callback `afterBpush`。
- 第二层对一个 AMR level 分派 `PatchType::fine`，如果 `lev>0`，再分派 `PatchType::coarse`。
- 第三层选择 `m_fdtd_solver_fp[lev]` 或 `m_fdtd_solver_cp[lev]`。`fp` 是 fine patch 数据，`cp` 是 refined level 的 coarse patch 数据。

PML 和边界条件紧跟 regular-cell 更新：

```cpp
    // Evolve B field in PML cells
    if (do_pml && pml[lev]->ok()) {
        if (patch_type == PatchType::fine) {
            m_fdtd_solver_fp[lev]->EvolveBPML(
                m_fields, patch_type, lev, a_dt, WarpX::do_dive_cleaning);
        } else {
            m_fdtd_solver_cp[lev]->EvolveBPML(
                m_fields, patch_type, lev, a_dt, WarpX::do_dive_cleaning);
        }
    }

    amrex::Real const new_time = start_time + a_dt;
    ApplyBfieldBoundary(lev, patch_type, subcycling_half, new_time);
}
```

因此 `EvolveB()` 的真实含义不是“只改 B 数组”，而是：

```text
regular B update
-> optional PML B update
-> physical boundary application
-> optional Python callback at outer level
```

## 3. `EvolveE()`：regular E、PML、边界与 ECT rho

`EvolveE()` 结构和 `EvolveB()` 平行。源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:1000-1086`。

```cpp
void
WarpX::EvolveE (amrex::Real a_dt, amrex::Real start_time)
{
    for (int lev = 0; lev <= finest_level; ++lev)
    {
        EvolveE(lev, a_dt, start_time);
    }

    // Allow execution of Python callback after E-field push
    ExecutePythonCallback("afterEpush");
}

void
WarpX::EvolveE (int lev, PatchType patch_type, amrex::Real a_dt, amrex::Real start_time)
{
    // Evolve E field in regular cells
    if (patch_type == PatchType::fine) {
        m_fdtd_solver_fp[lev]->EvolveE( m_fields,
                                        lev,
                                        patch_type,
                                        m_fields.get_alldirs(FieldType::Efield_fp, lev),
                                        m_eb_update_E[lev],
                                        a_dt );
    } else {
        m_fdtd_solver_cp[lev]->EvolveE( m_fields,
                                        lev,
                                        patch_type,
                                        m_fields.get_alldirs(FieldType::Efield_cp, lev),
                                        m_eb_update_E[lev],
                                        a_dt );
    }
```

注意 `EvolveE()` 显式传入 `Efield_fp` 或 `Efield_cp`，同时传入 `m_eb_update_E[lev]`。后者用于 embedded boundary 下跳过某些 E field 位置。

PML 更新和边界条件：

```cpp
    // Evolve E field in PML cells
    if (do_pml && pml[lev]->ok()) {
        if (patch_type == PatchType::fine) {
            m_fdtd_solver_fp[lev]->EvolveEPML(
                m_fields,
                patch_type,
                lev,
                pml[lev]->GetMultiSigmaBox_fp(),
                a_dt, pml_has_particles );
        } else {
            m_fdtd_solver_cp[lev]->EvolveEPML(
                m_fields,
                patch_type,
                lev,
                pml[lev]->GetMultiSigmaBox_cp(),
                a_dt, pml_has_particles );
        }
    }

    amrex::Real const new_time = start_time + a_dt;
    ApplyEfieldBoundary(lev, patch_type, new_time);
```

若使用 ECT embedded-boundary solver，E 更新之后还要重算 `ECTRhofield`：

```cpp
#ifdef AMREX_USE_EB
    if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::ECT) {
        if (patch_type == PatchType::fine) {
            m_fdtd_solver_fp[lev]->EvolveECTRho( m_fields.get_alldirs(FieldType::Efield_fp, lev),
                                                 m_fields.get_alldirs(FieldType::edge_lengths, lev),
                                                 m_fields.get_alldirs(FieldType::face_areas, lev),
                                                 m_fields.get_alldirs(FieldType::ECTRhofield, lev),
                                                 lev );
        } else {
            m_fdtd_solver_cp[lev]->EvolveECTRho( m_fields.get_alldirs(FieldType::Efield_cp, lev),
                                                 m_fields.get_alldirs(FieldType::edge_lengths, lev),
                                                 m_fields.get_alldirs(FieldType::face_areas, lev),
                                                 m_fields.get_alldirs(FieldType::ECTRhofield, lev),
                                                 lev);
        }
    }
#endif
```

这说明 ECT 的 charge-like auxiliary field 必须和新 E 保持一致，不能在 E push 前或 PML 前更新。

## 4. `EvolveF()` 和 `EvolveG()`：divergence-cleaning 标量

`EvolveF()` 顶层先检查 `do_dive_cleaning`。源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:1090-1139`。

```cpp
void
WarpX::EvolveF (amrex::Real a_dt, int const rho_comp)
{
    if (!do_dive_cleaning) { return; }

    for (int lev = 0; lev <= finest_level; ++lev)
    {
        EvolveF(lev, a_dt, rho_comp);
    }
}

void
WarpX::EvolveF (int lev, PatchType patch_type, amrex::Real a_dt, int const rho_comp)
{
    if (!do_dive_cleaning) { return; }

    ABLASTR_PROFILE("WarpX::EvolveF()");

    // Evolve F field in regular cells
    if (patch_type == PatchType::fine) {
        m_fdtd_solver_fp[lev]->EvolveF( m_fields.get(FieldType::F_fp, lev),
                                        m_fields.get_alldirs(FieldType::Efield_fp, lev),
                                        m_fields.get(FieldType::rho_fp,lev), rho_comp, a_dt );
    } else {
        m_fdtd_solver_cp[lev]->EvolveF( m_fields.get(FieldType::F_cp, lev),
                                        m_fields.get_alldirs(FieldType::Efield_cp, lev),
                                        m_fields.get(FieldType::rho_cp,lev), rho_comp, a_dt );
    }
```

`rho_comp` 来自主循环中的 `rho` 时间层，例如 `OneStep_nosub()` 里先用 `rho_comp=0`，后用 `rho_comp=1`。它决定 `rho(i,j,k,rho_comp)` 中取哪一组电荷密度。

PML 中也有 `F`：

```cpp
    // Evolve F field in PML cells
    if (do_pml && pml[lev]->ok()) {
        if (patch_type == PatchType::fine) {
            m_fdtd_solver_fp[lev]->EvolveFPML(
                m_fields.get(FieldType::pml_F_fp, lev),
                m_fields.get_alldirs(FieldType::pml_E_fp, lev),
                a_dt );
        } else {
            m_fdtd_solver_cp[lev]->EvolveFPML(
                m_fields.get(FieldType::pml_F_cp, lev),
                m_fields.get_alldirs(FieldType::pml_E_cp, lev),
                a_dt );
        }
    }
}
```

`EvolveG()` 只在 `do_divb_cleaning` 开启时执行。源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:1142-1190`。

```cpp
void
WarpX::EvolveG (amrex::Real a_dt)
{
    if (!do_divb_cleaning) { return; }

    for (int lev = 0; lev <= finest_level; ++lev)
    {
        EvolveG(lev, a_dt);
    }
}

void
WarpX::EvolveG (int lev, PatchType patch_type, amrex::Real a_dt)
{
    if (!do_divb_cleaning) { return; }

    ABLASTR_PROFILE("WarpX::EvolveG()");

    bool const skip_lev0_coarse_patch = true;

    // Evolve G field in regular cells
    if (patch_type == PatchType::fine)
    {
        ablastr::fields::MultiLevelVectorField const& Bfield_fp = m_fields.get_mr_levels_alldirs(FieldType::Bfield_fp, finest_level);
        m_fdtd_solver_fp[lev]->EvolveG(
            m_fields.get(FieldType::G_fp, lev),
            Bfield_fp[lev], a_dt);
    }
    else // coarse patch
    {
        ablastr::fields::MultiLevelVectorField const& Bfield_cp_new = m_fields.get_mr_levels_alldirs(FieldType::Bfield_cp, finest_level, skip_lev0_coarse_patch);
        m_fdtd_solver_cp[lev]->EvolveG(
            m_fields.get(FieldType::G_cp, lev),
            Bfield_cp_new[lev], a_dt);
    }

    // TODO Evolution in PML cells will go here
}
```

`G` 当前没有 PML evolution，实现里留下 TODO。这和 `F` 的 PML 更新不同。

## 5. PSATD 顶层：不同于 FDTD 的谱空间路由

标准 PSATD push 的主体也在 `WarpXPushFieldsEM.cpp`。源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:900-937`。

```cpp
// FFT of E and B
PSATDForwardTransformEB();

#ifdef WARPX_DIM_RZ
constexpr auto lev0 = 0;
if (pml_rz[lev0]) { pml_rz[lev0]->PushPSATD(lev0, m_fields, get_spectral_solver_fp(lev0)); }
#endif

// FFT of F and G
if (WarpX::do_dive_cleaning) { PSATDForwardTransformF(); }
if (WarpX::do_divb_cleaning) { PSATDForwardTransformG(); }

// Update E, B, F, and G in k-space
PSATDPushSpectralFields();

// Inverse FFT of E, B, F, and G
PSATDBackwardTransformEB();
if (WarpX::fft_do_time_averaging) {
    auto Efield_avg_fp = m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_fp, finest_level);
    auto Bfield_avg_fp = m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_fp, finest_level);
    auto Efield_avg_cp = m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_cp, finest_level, skip_lev0_coarse_patch);
    auto Bfield_avg_cp = m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_cp, finest_level, skip_lev0_coarse_patch);
    PSATDBackwardTransformEBavg(Efield_avg_fp, Bfield_avg_fp, Efield_avg_cp, Bfield_avg_cp);
}
if (WarpX::do_dive_cleaning) { PSATDBackwardTransformF(); }
if (WarpX::do_divb_cleaning) { PSATDBackwardTransformG(); }
```

`PSATDPushSpectralFields()` 很短，但它是谱 solver 的关键分派。源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:632-645`。

```cpp
WarpX::PSATDPushSpectralFields ()
{
    for (int lev = 0; lev <= finest_level; ++lev)
    {
        spectral_solver_fp[lev]->pushSpectralFields();

        if (spectral_solver_cp[lev])
        {
            spectral_solver_cp[lev]->pushSpectralFields();
        }
    }
}
```

和 FDTD 不同，PSATD 的实际 Maxwell update 不在 `EvolveE/B` 的 stencil 中，而是在 `SpectralSolver` 的 spectral field data 上进行。`WarpXPushFieldsEM.cpp` 负责 real-space field register 与 spectral solver 之间的 FFT 往返、PML、boundary 和 average field 回填。

## 6. `FiniteDifferenceSolver::EvolveB()`：算法选择和 B 更新

FDTD B push 的入口在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp:48-124`。

```cpp
void FiniteDifferenceSolver::EvolveB (
    ablastr::fields::MultiFabRegister& fields,
    int lev,
    PatchType patch_type,
    [[maybe_unused]] std::array< std::unique_ptr<amrex::iMultiFab>, 3 >& flag_info_cell,
    [[maybe_unused]] std::array< std::unique_ptr<amrex::LayoutData<FaceInfoBox> >, 3 >& borrowing,
    [[maybe_unused]] amrex::Real const dt )
{
    using ablastr::fields::Direction;
    using warpx::fields::FieldType;

    const ablastr::fields::VectorField Bfield = patch_type == PatchType::fine ?
        fields.get_alldirs(FieldType::Bfield_fp, lev) : fields.get_alldirs(FieldType::Bfield_cp, lev);
    const ablastr::fields::VectorField Efield = patch_type == PatchType::fine ?
        fields.get_alldirs(FieldType::Efield_fp, lev) : fields.get_alldirs(FieldType::Efield_cp, lev);
```

算法分派：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
    if ((m_fdtd_algo == ElectromagneticSolverAlgo::Yee)||
        (m_fdtd_algo == ElectromagneticSolverAlgo::HybridPIC)){
        EvolveBCylindrical <CylindricalYeeAlgorithm> ( Bfield, Efield, lev, dt );
#elif defined(WARPX_DIM_RSPHERE)
    if ((m_fdtd_algo == ElectromagneticSolverAlgo::Yee)||
        (m_fdtd_algo == ElectromagneticSolverAlgo::HybridPIC)){
        EvolveBSpherical <SphericalYeeAlgorithm> ( Bfield, Efield, lev, dt );
#else
    if (m_grid_type == GridType::Collocated) {
        EvolveBCartesian <CartesianNodalAlgorithm> ( Bfield, Efield, Gfield, lev, dt );
    } else if ((m_fdtd_algo == ElectromagneticSolverAlgo::Yee) ||
               (m_fdtd_algo == ElectromagneticSolverAlgo::HybridPIC)) {
        EvolveBCartesian <CartesianYeeAlgorithm> ( Bfield, Efield, Gfield, lev, dt );
    } else if (m_fdtd_algo == ElectromagneticSolverAlgo::CKC) {
        EvolveBCartesian <CartesianCKCAlgorithm> ( Bfield, Efield, Gfield, lev, dt );
    } else if (m_fdtd_algo == ElectromagneticSolverAlgo::ECT) {
        EvolveBCartesianECT(Bfield, face_areas, area_mod, ECTRhofield, Venl, flag_info_cell,
                            borrowing, lev, dt);
#endif
    } else {
        WARPX_ABORT_WITH_MESSAGE("EvolveB: Unknown algorithm");
    }
}
```

这说明 `FiniteDifferenceSolver` 本身是运行时选择、编译期模板实例化的混合结构：

- 运行时：`m_fdtd_algo` 和 `m_grid_type` 决定走哪条分支。
- 编译期：`CartesianYeeAlgorithm`、`CartesianCKCAlgorithm`、`CartesianNodalAlgorithm` 等通过模板内联具体差分算子。

Cartesian B kernel 位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp:130-211`。

```cpp
amrex::ParallelFor(tbx, tby, tbz,

    [=] AMREX_GPU_DEVICE (int i, int j, int k){

        Bx(i, j, k) += dt * T_Algo::UpwardDz(Ey, coefs_z, n_coefs_z, i, j, k)
                     - dt * T_Algo::UpwardDy(Ez, coefs_y, n_coefs_y, i, j, k);

    },

    [=] AMREX_GPU_DEVICE (int i, int j, int k){

        By(i, j, k) += dt * T_Algo::UpwardDx(Ez, coefs_x, n_coefs_x, i, j, k)
                     - dt * T_Algo::UpwardDz(Ex, coefs_z, n_coefs_z, i, j, k);

    },

    [=] AMREX_GPU_DEVICE (int i, int j, int k){

        Bz(i, j, k) += dt * T_Algo::UpwardDy(Ex, coefs_y, n_coefs_y, i, j, k)
                     - dt * T_Algo::UpwardDx(Ey, coefs_x, n_coefs_x, i, j, k);

    }
);
```

这对应

$$
B_x^{n+1}=B_x^n+\Delta t(\partial_z E_y-\partial_y E_z),
$$

$$
B_y^{n+1}=B_y^n+\Delta t(\partial_x E_z-\partial_z E_x),
$$

$$
B_z^{n+1}=B_z^n+\Delta t(\partial_y E_x-\partial_x E_y).
$$

也就是

$$
\partial_t\mathbf B=-\nabla\times\mathbf E.
$$

`Gfield` 若存在，则加上 div(B) cleaning 的梯度修正：

```cpp
if (Gfield)
{
    Array4<Real const> const G = Gfield->array(mfi);

    amrex::ParallelFor(tbx, tby, tbz,
        [=] AMREX_GPU_DEVICE (int i, int j, int k)
        {
            Bx(i,j,k) += dt * T_Algo::DownwardDx(G, coefs_x, n_coefs_x, i, j, k);
        },
        [=] AMREX_GPU_DEVICE (int i, int j, int k)
        {
            By(i,j,k) += dt * T_Algo::DownwardDy(G, coefs_y, n_coefs_y, i, j, k);
        },
        [=] AMREX_GPU_DEVICE (int i, int j, int k)
        {
            Bz(i,j,k) += dt * T_Algo::DownwardDz(G, coefs_z, n_coefs_z, i, j, k);
        }
    );
}
```

因此 WarpX 中的 `EvolveB` 实现的是

$$
\partial_t\mathbf B=-\nabla\times\mathbf E+\nabla G.
$$

## 7. `FiniteDifferenceSolver::EvolveE()`：curl(B)、current 和 grad(F)

FDTD E push 的入口在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp:50-113`。它先取出 B、J 和可选 F：

```cpp
const ablastr::fields::VectorField Bfield = patch_type == PatchType::fine ?
    fields.get_alldirs(FieldType::Bfield_fp, lev) : fields.get_alldirs(FieldType::Bfield_cp, lev);
const ablastr::fields::VectorField Jfield = patch_type == PatchType::fine ?
    fields.get_alldirs(FieldType::current_fp, lev) : fields.get_alldirs(FieldType::current_cp, lev);

amrex::MultiFab* Ffield = nullptr;
if (fields.has(FieldType::F_fp, lev)) {
    Ffield = patch_type == PatchType::fine ?
             fields.get(FieldType::F_fp, lev) : fields.get(FieldType::F_cp, lev);
}
```

Cartesian kernel 位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp:119-228`。

```cpp
Real constexpr c2 = PhysConst::c2;
```

每个 E 分量按 `c2 * dt` 更新：

```cpp
Ex(i, j, k) += c2 * dt * (
    - T_Algo::DownwardDz(By, coefs_z, n_coefs_z, i, j, k)
    + T_Algo::DownwardDy(Bz, coefs_y, n_coefs_y, i, j, k)
    - PhysConst::mu0 * jx(i, j, k) );
```

```cpp
Ey(i, j, k) += c2 * dt * (
    - T_Algo::DownwardDx(Bz, coefs_x, n_coefs_x, i, j, k)
    + T_Algo::DownwardDz(Bx, coefs_z, n_coefs_z, i, j, k)
    - PhysConst::mu0 * jy(i, j, k) );
```

```cpp
Ez(i, j, k) += c2 * dt * (
    - T_Algo::DownwardDy(Bx, coefs_y, n_coefs_y, i, j, k)
    + T_Algo::DownwardDx(By, coefs_x, n_coefs_x, i, j, k)
    - PhysConst::mu0 * jz(i, j, k) );
```

以 `Ex` 为例，括号前两项是

$$
(\nabla\times\mathbf B)_x=\partial_yB_z-\partial_zB_y,
$$

所以源码是

$$
E_x^{n+1}=E_x^n+c^2\Delta t
\left[(\nabla\times\mathbf B)_x-\mu_0J_x\right].
$$

由于 $c^2\mu_0=1/\epsilon_0$，这正是 Maxwell-Ampere 方程。

embedded boundary 会跳过不应更新的 E 位置：

```cpp
// Skip field push in the embedded boundaries
if (update_Ex_arr && update_Ex_arr(i, j, k) == 0) { return; }
```

若 `Ffield` 存在，E 还会加 divergence-cleaning 梯度修正：

```cpp
if (Ffield) {
    const Array4<Real const> F = Ffield->array(mfi);

    amrex::ParallelFor(tex, tey, tez,
        [=] AMREX_GPU_DEVICE (int i, int j, int k){
            Ex(i, j, k) += c2 * dt * T_Algo::UpwardDx(F, coefs_x, n_coefs_x, i, j, k);
        },
        [=] AMREX_GPU_DEVICE (int i, int j, int k){
            Ey(i, j, k) += c2 * dt * T_Algo::UpwardDy(F, coefs_y, n_coefs_y, i, j, k);
        },
        [=] AMREX_GPU_DEVICE (int i, int j, int k){
            Ez(i, j, k) += c2 * dt * T_Algo::UpwardDz(F, coefs_z, n_coefs_z, i, j, k);
        }
    );
}
```

因此 `EvolveE` 的完整 Cartesian 方程是

$$
\partial_t\mathbf E
=c^2(\nabla\times\mathbf B-\mu_0\mathbf J+\nabla F).
$$

## 8. `FiniteDifferenceSolver::EvolveF()`：Gauss law error propagation

`EvolveF()` 的 Cartesian kernel 位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveF.cpp:88-138`。

```cpp
Real constexpr inv_epsilon0 = 1._rt/PhysConst::epsilon_0;

amrex::ParallelFor(tf,

    [=] AMREX_GPU_DEVICE (int i, int j, int k){
        F(i, j, k) += dt * (
            - rho(i, j, k, rho_comp) * inv_epsilon0
            + T_Algo::DownwardDx(Ex, coefs_x, n_coefs_x, i, j, k)
            + T_Algo::DownwardDy(Ey, coefs_y, n_coefs_y, i, j, k)
            + T_Algo::DownwardDz(Ez, coefs_z, n_coefs_z, i, j, k) );
    }

);
```

这就是

$$
F^{n+1}=F^n+\Delta t\left(\nabla\cdot\mathbf E-\frac{\rho}{\epsilon_0}\right).
$$

如果 Gauss law 完全满足，即

$$
\nabla\cdot\mathbf E=\rho/\epsilon_0,
$$

则 $F$ 不增长。若沉积、边界或 AMR 同步产生局部 Gauss law 误差，`F` 会作为传播型清理变量参与下一次 `EvolveE`。

## 9. `FiniteDifferenceSolver::EvolveG()`：magnetic Gauss law cleaning

`EvolveG()` 的 Cartesian kernel 位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveG.cpp:65-111`。

```cpp
amrex::Real constexpr c2 = PhysConst::c2;

amrex::ParallelFor(tf, [=] AMREX_GPU_DEVICE (int i, int j, int k)
{
    G(i,j,k) += c2 * dt * (T_Algo::UpwardDx(Bx, coefs_x, n_coefs_x, i, j, k)
                         + T_Algo::UpwardDy(By, coefs_y, n_coefs_y, i, j, k)
                         + T_Algo::UpwardDz(Bz, coefs_z, n_coefs_z, i, j, k));
});
```

对应

$$
G^{n+1}=G^n+c^2\Delta t\,\nabla\cdot\mathbf B.
$$

再由 `EvolveB()` 中的 `+grad(G)` 修正回馈到磁场，形成 magnetic divergence cleaning。源码中 RZ/RCYLINDER/RSPHERE 分支尚未实现 `G` 更新：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    // TODO Implement G update equation in RZ geometry
    amrex::ignore_unused(Gfield, Bfield, dt);
```

这个 TODO 是正式书稿中必须记录的功能边界：不能把 Cartesian `do_divb_cleaning` 解释直接推广到 RZ 或 spherical。

## 10. 本节调用链总结

当前已经确认的 field solver 分派链是：

```text
Evolve/WarpXEvolve.cpp
  OneStep_nosub / OneStep_sub1
    -> WarpX::EvolveB/E/F/G(...)

FieldSolver/WarpXPushFieldsEM.cpp
  WarpX::EvolveB
    -> m_fdtd_solver_fp/cp[lev]->EvolveB(...)
    -> EvolveBPML(...)
    -> ApplyBfieldBoundary(...)
  WarpX::EvolveE
    -> m_fdtd_solver_fp/cp[lev]->EvolveE(...)
    -> EvolveEPML(...)
    -> ApplyEfieldBoundary(...)
    -> optional EvolveECTRho(...)
  WarpX::EvolveF
    -> m_fdtd_solver_fp/cp[lev]->EvolveF(...)
    -> EvolveFPML(...)
  WarpX::EvolveG
    -> m_fdtd_solver_fp/cp[lev]->EvolveG(...)

FieldSolver/FiniteDifferenceSolver
  EvolveB.cpp
    -> CartesianYee/CKC/Nodal/Cylindrical/Spherical/ECT B kernels
  EvolveE.cpp
    -> CartesianYee/CKC/Nodal/Cylindrical/Spherical E kernels
  EvolveF.cpp
    -> div(E)-rho/epsilon0 cleaning scalar
  EvolveG.cpp
    -> c^2 div(B) cleaning scalar for Cartesian

Spectral path
  PSATDForwardTransform*
  -> spectral_solver_fp/cp[lev]->pushSpectralFields()
  -> PSATDBackwardTransform*
```

后续继续精读应分两路：

- `01-fdtd-evolve-e-b.md`：进入 `FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H`、`CartesianCKCAlgorithm.H`、`CartesianNodalAlgorithm.H`，把 `Upward/Downward` 差分算子和 staggered index type 讲透。
- `02-psatd-spectral-flow.md`：进入 `SpectralSolver/` 和 `SpectralAlgorithms/`，解释 `pushSpectralFields()` 如何解析积分 Maxwell 方程。

