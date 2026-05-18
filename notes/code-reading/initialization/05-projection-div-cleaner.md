# ProjectionDivCleaner 精读：外部场初始散度清理

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.H/.cpp`，并对照 `WarpXInitData.cpp`、`ExternalVectorPotential.cpp` 和官方参数文档中相关入口。

先区分两个容易混淆的概念：

- `warpx.do_dive_cleaning` / `warpx.do_divb_cleaning`：演化阶段的 Maxwell 方程扩展或 PSATD `F/G` 清理变量。
- `warpx.do_initial_div_cleaning` 对应的 projection cleaner：初始化阶段对外部加载的 `B` 或时间变化矢势 `A` 做投影清理。

本篇只讲第二类：`ProjectionDivCleaner`。

## 1. 官方参数边界

源码位置：`../warpx/Docs/source/usage/parameters.rst:3792-3811`。

```rst
.. pp:param:: warpx.do_initial_div_cleaning
    :type: ``0`` or ``1``
    :default: 0

    Whether to use projection method to scrub A/B field divergence in externally
    loaded fields. This is automatically turned on if external/initial B or time varying A fields are loaded.

.. pp:param:: warpx.projection_div_cleaner.rtol
    :type: ``float``
    :default: ``5e-12`` when double precision and ``5e-5`` for single precision
    :optional:

    Controls the relative tolerance when solving for the projected divergence of the field in the MLMG AMReX solver.

.. pp:param:: warpx.projection_div_cleaner.atol
    :type: ``float``
    :default: ``0``
    :optional:

    Controls the absolute tolerance when solving for the projected divergence of the field in the MLMG AMReX solver.
```

文档明确了适用对象：外部加载的 `A/B` 场。它不是每一步都执行的场演化修正，而是初始化或外部矢势构造后的投影。

数学上，给定一个离散向量场 `F`，目标是去掉其纵向分量：

$$
\mathbf{F}' = \mathbf{F} + \nabla \phi,
$$

要求

$$
\nabla \cdot \mathbf{F}' = 0.
$$

于是需要解

$$
\nabla^2 \phi = -\nabla \cdot \mathbf{F}.
$$

代码中的 `m_source = -div(F)`、`MLMG solve`、`F += grad(phi)` 正是这个 projection。

## 2. 类状态：solution/source 与 stencil 系数

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.H:45-124`。

```cpp
namespace warpx::initialization {

class ProjectionDivCleaner
{
protected:
    int m_levels = 1; // Hard coded to 1 for now, will only clean first level

    int m_ref_ratio = 1;

    // For MLMG solver
    int m_verbose = 2;
    int m_bottom_verbose = 0;
    int m_max_iter = 5000;
    int m_max_fmg_iter = 1000;
    int m_linop_maxorder = 3;
    bool m_agglomeration = false;
    bool m_consolidation = false;
    bool m_semicoarsening = true;
    int m_max_coarsening_level = 10;
    int m_max_semicoarsening_level = 10;
    amrex::BottomSolver m_bottom_solver = amrex::BottomSolver::bicgstab;
```

当前实现只清理 level 0，`m_levels = 1` 是硬编码。AMR 多层存在时会给 warning，而不是跨 coarse-fine 统一投影。

关键数据成员：

```cpp
public:
    amrex::Vector< std::unique_ptr<amrex::MultiFab> > m_solution;
    amrex::Vector< std::unique_ptr<amrex::MultiFab> > m_source;

    amrex::Vector<amrex::Real> m_h_stencil_coefs_x;
    amrex::Vector<amrex::Real> m_h_stencil_coefs_y;
    amrex::Vector<amrex::Real> m_h_stencil_coefs_z;

    amrex::Gpu::DeviceVector<amrex::Real> m_stencil_coefs_x;
    amrex::Gpu::DeviceVector<amrex::Real> m_stencil_coefs_y;
    amrex::Gpu::DeviceVector<amrex::Real> m_stencil_coefs_z;

    explicit ProjectionDivCleaner (std::string const& a_field_name, bool a_vector_potential=false);

    void ReadParameters ();
    void solve ();
    void setSourceFromField ();
    void correctField ();
```

`m_solution` 存的是投影势 `phi`，`m_source` 存的是 `-div(F)`。stencil 系数必须和 WarpX 当前 grid type 及几何一致，否则“清理出来的 divergence”和后续场 solver 的离散 divergence 不是同一个算子。

## 3. 构造函数：选择 nodal/cell-centered solve，并初始化离散 stencil

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp:36-123`。

```cpp
ProjectionDivCleaner::ProjectionDivCleaner(std::string const& a_field_name, bool a_vector_potential) :
    m_field_name{a_field_name},
    m_grid_type{WarpX::grid_type},
    m_vector_potential{a_vector_potential}
{
    using ablastr::fields::Direction;
    ReadParameters();

    auto& warpx = WarpX::GetInstance();

    // Only div clean level 0
    if (warpx.finestLevel() > 0) {
        ablastr::warn_manager::WMRecordWarning("Projection Div Cleaner",
            "Multiple AMR levels detected, only first level has been cleaned.",
            ablastr::warn_manager::WarnPriority::low);
    }
```

这里绑定待清理的 field name，例如 `Bfield_fp_external` 或外部矢势 field name。`a_vector_potential=true` 时会改变 solution/source 的 nodality。

网格类型选择：

```cpp
    IntVect nodal_flag{};
    if (m_grid_type == GridType::Collocated || m_vector_potential) {
        nodal_flag = IntVect::TheNodeVector();
    } else {
        nodal_flag = IntVect::TheCellVector();
    }
```

含义：

- collocated 网格或 vector potential 清理：`phi` 放在节点；
- Yee/staggered B 场清理：`phi` 放在 cell center，然后用 downward derivative 修正 face/edge field。

MultiFab 分配：

```cpp
        const auto tag1 = amrex::MFInfo().SetTag("div_cleaner_solution");
        m_solution[lev] = std::make_unique<MultiFab>(amrex::convert(ba, nodal_flag),
            dmap, ncomps, ng, tag1);
        const auto tag2 = amrex::MFInfo().SetTag("div_cleaner_source");
        m_source[lev] = std::make_unique<MultiFab>(amrex::convert(ba, nodal_flag),
            dmap, ncomps, ng, tag2);

        m_solution[lev]->setVal(0.0, ng);
        m_source[lev]->setVal(0.0, ng);
```

随后初始化与当前几何一致的差分系数：

```cpp
    auto cell_size = WarpX::CellSize(0);
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
    CylindricalYeeAlgorithm::InitializeStencilCoefficients( cell_size,
        m_h_stencil_coefs_x, m_h_stencil_coefs_z );
#elif defined(WARPX_DIM_RSPHERE)
    SphericalYeeAlgorithm::InitializeStencilCoefficients( cell_size,
        m_h_stencil_coefs_x );
#else
    if (m_grid_type == GridType::Collocated) {
        CartesianNodalAlgorithm::InitializeStencilCoefficients( cell_size,
            m_h_stencil_coefs_x, m_h_stencil_coefs_y, m_h_stencil_coefs_z );
    } else {
        CartesianYeeAlgorithm::InitializeStencilCoefficients( cell_size,
            m_h_stencil_coefs_x, m_h_stencil_coefs_y, m_h_stencil_coefs_z );
    }
#endif
```

这一步决定后面 `correctField()` 用哪一种离散梯度。

## 4. 参数读取：只暴露 solver tolerance

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp:125-143`。

```cpp
void
ProjectionDivCleaner::ReadParameters ()
{
    // Initialize tolerance based on field precision
    if constexpr (std::is_same_v<Real, float>) {
        m_rtol = 5e-5;
        m_atol = 0.0;
    }
    else {
        m_rtol = 5e-12;
        m_atol = 0.0;
    }

    const ParmParse pp_div_cleaner("warpx.projection_div_cleaner");

    // Defaults to rtol 5e-12 for double fields and 5e-5 for single
    utils::parser::queryWithParser(pp_div_cleaner, "atol", m_atol);
    utils::parser::queryWithParser(pp_div_cleaner, "rtol", m_rtol);
}
```

当前用户可调参数只有 `atol` 和 `rtol`。多重网格迭代次数、底层 solver、coarsening 等参数在类内固定，不通过输入文件暴露。

## 5. `setSourceFromField()`：计算 Poisson 右端项 `-div(F)`

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp:218-272`。

```cpp
void
ProjectionDivCleaner::setSourceFromField ()
{
    using ablastr::fields::Direction;

    // Get WarpX object
    auto & warpx = WarpX::GetInstance();
    const auto& geom = warpx.Geom();

    // This function will compute -divB and store it in the source multifab
    for (int ilev = 0; ilev < m_levels; ++ilev)
    {
        // Grab B-field multifabs at this level
        amrex::MultiFab* Bx = warpx.m_fields.get(m_field_name, Direction{0}, ilev);
        amrex::MultiFab* By = warpx.m_fields.get(m_field_name, Direction{1}, ilev);
        amrex::MultiFab* Bz = warpx.m_fields.get(m_field_name, Direction{2}, ilev);
```

变量名仍写成 `Bx/By/Bz`，但 `m_field_name` 可以是 B field，也可以是 vector potential field。代码把三方向分量视为待投影清理的向量场。

计算前先填 ghost：

```cpp
        ablastr::utils::communication::FillBoundary(*Bx,
                Bx->nGrowVect(),
                WarpX::do_single_precision_comms,
                geom[ilev].periodicity(),
                true);
        ablastr::utils::communication::FillBoundary(*By,
                By->nGrowVect(),
                WarpX::do_single_precision_comms,
                geom[ilev].periodicity(),
                true);
        ablastr::utils::communication::FillBoundary(*Bz,
                Bz->nGrowVect(),
                WarpX::do_single_precision_comms,
                geom[ilev].periodicity(),
                true);
```

然后调用 WarpX 的离散 divergence：

```cpp
        WarpX::ComputeDivB(
            *m_source[ilev],
            0,
            {Bx, By, Bz},
            WarpX::CellSize(0)
            );

        m_source[ilev]->mult(-1._rt);
```

这正是

$$
source = -\nabla_h \cdot \mathbf{F}.
$$

## 6. `solve()`：用 AMReX MLMG 解 Poisson 方程

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp:145-216`。

```cpp
void
ProjectionDivCleaner::solve ()
{
    auto & warpx = WarpX::GetInstance();

    const auto& ba = warpx.boxArray();
    const auto& dmap = warpx.DistributionMap();
    const auto& geom = warpx.Geom();

    amrex::Array<LinOpBCType,AMREX_SPACEDIM> lobc({AMREX_D_DECL(LinOpBCType::bogus,
                                                                LinOpBCType::bogus,
                                                                LinOpBCType::bogus)});
    amrex::Array<LinOpBCType,AMREX_SPACEDIM> hibc({AMREX_D_DECL(LinOpBCType::bogus,
                                                                LinOpBCType::bogus,
                                                                LinOpBCType::bogus)});
```

field boundary 被映射成线性算子的边界条件：

```cpp
    std::map<FieldBoundaryType, LinOpBCType> bcmap{
        {FieldBoundaryType::PEC, LinOpBCType::Dirichlet},
        {FieldBoundaryType::Neumann, LinOpBCType::Neumann}, // Note that PMC is the same as Neumann
        {FieldBoundaryType::Periodic, LinOpBCType::Periodic},
        {FieldBoundaryType::None, LinOpBCType::Neumann}
    };

    for (int idim=0; idim<AMREX_SPACEDIM; idim++){
        auto itlo = bcmap.find(WarpX::field_boundary_lo[idim]);
        auto ithi = bcmap.find(WarpX::field_boundary_hi[idim]);
        if (itlo == bcmap.end() || ithi == bcmap.end()) {
            WARPX_ABORT_WITH_MESSAGE(
                "Field boundary conditions have to be either periodic, PEC, PMC, or neumann "
                "when using the MLMG projection based divergence cleaner solver."
            );
        }

        lobc[idim] = bcmap[WarpX::field_boundary_lo[idim]];
        hibc[idim] = bcmap[WarpX::field_boundary_hi[idim]];
    }
```

对于 RZ/球几何，Poisson operator 开启 metric term：

```cpp
    LPInfo info;
    info.setAgglomeration(m_agglomeration);
    info.setConsolidation(m_consolidation);
    info.setMaxCoarseningLevel(m_max_coarsening_level);
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    info.setMetricTerm(true);
#endif
```

根据 field 的中心位置选择不同 Laplacian：

```cpp
        if (m_grid_type == GridType::Collocated || m_vector_potential) {
            MLNodeLaplacian linop({geom[ilev]}, {ba[ilev]}, {dmap[ilev]}, info, eb_farray_box_factory, 1.0_rt);
            runMLMG<MLNodeLaplacian>(linop, lobc, hibc, ilev);
        } else {
            MLPoisson linop({geom[ilev]}, {ba[ilev]}, {dmap[ilev]}, info);
            runMLMG<MLPoisson>(linop, lobc, hibc, ilev);
        }
```

`runMLMG()` 里真正调用 solver：

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

因此 `m_solution` 满足离散方程：

$$
\nabla_h^2 \phi = -\nabla_h \cdot \mathbf{F}.
$$

## 7. `correctField()`：用 `grad(phi)` 修正原场

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp:274-392`。

Cartesian 主 kernel：

```cpp
template <typename T>
AMREX_FORCE_INLINE
void correctFieldCartesian_kernel (
    const Box & tbx, const Box & tby, const Box & tbz,
    Real const * const AMREX_RESTRICT coefs_x,
    Real const * const AMREX_RESTRICT coefs_y,
    Real const * const AMREX_RESTRICT coefs_z,
    const int n_coefs_x, const int n_coefs_y, const int n_coefs_z,
    amrex::Array4<Real> const& Bx_arr,
    amrex::Array4<Real> const& By_arr,
    amrex::Array4<Real> const& Bz_arr,
    amrex::Array4<Real> const& sol_arr
    )
{
    amrex::ParallelFor(tbx, tby, tbz,
        [=] AMREX_GPU_DEVICE (int i, int j, int k)
        {
            Bx_arr(i,j,k) += T::DownwardDx(sol_arr, coefs_x, n_coefs_x, i, j, k);
        },
        [=] AMREX_GPU_DEVICE (int i, int j, int k)
        {
            By_arr(i,j,k) += T::DownwardDy(sol_arr, coefs_y, n_coefs_y, i, j, k);
        },
        [=] AMREX_GPU_DEVICE (int i, int j, int k)
        {
            Bz_arr(i,j,k) += T::DownwardDz(sol_arr, coefs_z, n_coefs_z, i, j, k);
        });
}
```

`DownwardD*` 是和场网格 staggering 匹配的离散梯度。注意这里是 `+= grad(phi)`，因为 `phi` 的方程右端已经是 `-div(F)`。

维度/几何分支：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
            amrex::ParallelFor(tbx, tbz,
            [=] AMREX_GPU_DEVICE (int i, int j, int /*k*/)
            {
                Bx_arr(i,j,0) += CylindricalYeeAlgorithm::DownwardDr(sol_arr, coefs_x, n_coefs_x, i, j, 0, 0);
            },
            [=] AMREX_GPU_DEVICE (int i, int j, int /*k*/)
            {
                Bz_arr(i,j,0) += CylindricalYeeAlgorithm::DownwardDz(sol_arr, coefs_z, n_coefs_z, i, j, 0, 0);
            });
#elif defined(WARPX_DIM_RSPHERE)
            amrex::ParallelFor(tbx,
            [=] AMREX_GPU_DEVICE (int i, int /*j*/, int /*k*/)
            {
                Bx_arr(i,0,0) += SphericalYeeAlgorithm::DownwardDr(sol_arr, coefs_x, n_coefs_x, i, 0, 0, 0);
            });
#else
            if (m_grid_type == GridType::Collocated)
            {
                correctFieldCartesian_kernel<CartesianNodalAlgorithm>(tbx, tby, tbz, coefs_x, coefs_y, coefs_z,
                    n_coefs_x, n_coefs_y, n_coefs_z, Bx_arr, By_arr, Bz_arr, sol_arr);
            } else {
                correctFieldCartesian_kernel<CartesianYeeAlgorithm>(tbx, tby, tbz, coefs_x, coefs_y, coefs_z,
                    n_coefs_x, n_coefs_y, n_coefs_z, Bx_arr, By_arr, Bz_arr, sol_arr);
            }
#endif
```

这段说明 projection cleaner 不是抽象连续公式的简单套用，而是严格使用当前几何和 grid type 的离散导数。

## 8. B 场清理入口：`WarpX::ProjectionCleanDivB()`

源码位置：`../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp:396-433`。

```cpp
void
WarpX::ProjectionCleanDivB() {
    ABLASTR_PROFILE("WarpX::ProjectionDivCleanB()");

    if ( (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee
            ||  WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC
            ||  ( (WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrame
                || WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic)
                && WarpX::poisson_solver_id == PoissonSolverAlgo::Multigrid))
#if defined(WARPX_DIM_RZ)
                && WarpX::grid_type == GridType::Staggered
#endif
            )
    {
        amrex::Print() << Utils::TextMsg::Info( "Starting Projection B-Field divergence cleaner.");
```

支持范围：

- Yee；
- HybridPIC；
- LabFrame / LabFrameElectroMagnetostatic 且 Poisson solver 是 Multigrid；
- RZ 下要求 staggered grid。

调用顺序：

```cpp
        warpx::initialization::ProjectionDivCleaner dc("Bfield_fp_external");

        dc.setSourceFromField();
        dc.solve();
        dc.correctField();

        amrex::Print() << Utils::TextMsg::Info( "Finished Projection B-Field divergence cleaner.");
    } else {
        ablastr::warn_manager::WMRecordWarning("Projection Div Cleaner",
            "Only Yee, HybridPIC, and MLMG based static Labframe solvers are currently supported, so divB not cleaned. "
            "Interpolation may lead to non-zero B field divergence.",
            ablastr::warn_manager::WarnPriority::low);
    }
}
```

这说明 projection cleaner 当前不是所有 solver 都可用；如果 solver 不在支持范围内，WarpX 给 warning 并跳过。

## 9. 外部矢势 A 的清理入口

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.cpp:209-217`。

```cpp
        amrex::Gpu::streamSynchronize();

        if (m_do_clean_divA) {
            warpx::initialization::ProjectionDivCleaner dc(Aext_field, true);
            dc.setSourceFromField();
            dc.solve();
            dc.correctField();
            amrex::Print() << Utils::TextMsg::Info( "Finished Projection A-Field divergence cleaner.");
        }
```

这里第二个参数是 `true`，即 `a_vector_potential=true`。构造函数因此会使用 nodal solution/source。虽然函数名和局部变量仍沿用 `B`，数学操作实际上是对外部矢势 `A` 做同样投影：

$$
\mathbf{A}' = \mathbf{A} + \nabla \phi,\qquad
\nabla_h \cdot \mathbf{A}' = 0.
$$

这等价于在离散层面选择一个更接近 Coulomb gauge 的外部矢势初态。

## 10. 与演化阶段 div cleaning 的关系

`WarpXInitData.cpp` 在打印 PSATD 配置时会显示演化阶段的清理变量：

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:671-675`。

```cpp
    if (WarpX::do_dive_cleaning) {
      amrex::Print() << "                      | - div(E) cleaning is ON \n";
      }
    if (WarpX::do_divb_cleaning) {
      amrex::Print() << "                      | - div(B) cleaning is ON \n";
      }
```

这不是 `ProjectionDivCleaner` 的调用点。演化阶段的 `do_dive_cleaning/do_divb_cleaning` 会在 PSATD/FDTD 推进路径中引入附加变量或额外变换；projection cleaner 则是外部初始场上的一次 Poisson 投影。

可以把二者分成：

| 机制 | 发生时间 | 典型对象 | 核心方程 |
|---|---|---|---|
| projection cleaner | 初始化/外部场加载后 | 外部 `B` 或外部 `A` | `∇²φ = -∇·F`, `F <- F + ∇φ` |
| `do_dive_cleaning/do_divb_cleaning` | 时间推进中 | Maxwell solver 的 `E/B` 约束误差 | 修改 Maxwell 方程或 PSATD 清理变量 |

## 11. 初始化阶段当前闭环

到目前为止，阶段 2 的初始化链已经覆盖：

```text
WarpX::InitData()
  -> fresh run / restart
  -> InitFromScratch()
  -> InitLevelData()
  -> external grid/particle fields
  -> species PlasmaInjector
  -> density/momentum functor dispatch
  -> AddParticles/AddPlasma particle creation kernels
  -> projection div cleaner for externally loaded A/B fields
```

下一步应做两件事：

1. 把 `AddGaussianBeam()` 和 `AddPlasmaFromFile()` 的边缘路径补成逐块精读，因为当前 `04-particle-creation-kernels.md` 主要讲体注入和 flux 注入主链。
2. 开始把 `00-05` 六篇 initialization notes 合并进正式书稿中的初始化章节，避免精读笔记长期只停留在 notes 层。
