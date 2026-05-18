# Electrostatic / Magnetostatic 源码精读

绑定源码与文档：

- `../warpx/Source/FieldSolver/WarpXSolveFieldsES.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.H`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.H`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/LabFrameExplicitES.H`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/LabFrameExplicitES.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/RelativisticExplicitES.H`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/RelativisticExplicitES.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.H`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.cpp`
- `../warpx/Source/FieldSolver/MagnetostaticSolver/MagnetostaticSolver.H`
- `../warpx/Source/FieldSolver/MagnetostaticSolver/MagnetostaticSolver.cpp`
- `../warpx/Source/WarpX.cpp:399-410,729-781,2409-2524`
- `../warpx/Docs/source/theory/models_algorithms/electrostatic_pic.rst`
- `../warpx/Docs/source/usage/parameters.rst:360-510`

这一组代码不是 Maxwell push 的另一个时间推进器，而是把每步的场重新投影到椭圆方程解上。显式电磁 PIC 用

$$
\partial_t \mathbf B=-\nabla\times\mathbf E,\qquad
\partial_t \mathbf E=c^2\nabla\times\mathbf B-\mathbf J/\epsilon_0
$$

沿时间推进；静电 PIC 则把场看成瞬时满足

$$
\nabla^2\phi=-\rho/\epsilon_0,\qquad \mathbf E=-\nabla\phi.
$$

这会去掉光波传播和辐射自由度，因此没有 Maxwell CFL 的同一类限制；代价是每一步要解 Poisson 方程，并且只能描述静电或准静磁自场。WarpX 还实现了三个扩展：

1. `labframe-electromagnetostatic`：在 lab frame 解标量势和矢势
   $$
   \nabla^2\phi=-\rho/\epsilon_0,\qquad
   \nabla^2\mathbf A=-\mu_0\mathbf J,\qquad
   \mathbf B=\nabla\times\mathbf A.
   $$
2. `relativistic`：对每个 species 用平均速度 $\boldsymbol\beta=\langle\mathbf v\rangle/c$ 修正 Poisson 算子和场重建
   $$
   \left[\nabla^2-(\boldsymbol\beta\cdot\nabla)^2\right]\phi=-\rho/\epsilon_0,
   $$
   $$
   \mathbf E=-\nabla\phi+\boldsymbol\beta(\boldsymbol\beta\cdot\nabla\phi),\qquad
   \mathbf B=-\frac{1}{c}\boldsymbol\beta\times\nabla\phi.
   $$
3. `labframe-effective-potential`：把 Poisson 方程改写成带有效介电函数的半隐式形式
   $$
   \nabla\cdot\left[\left(1+\frac{C_{EP}}{4}\sum_s(\omega_{ps}\Delta t)^2\right)\nabla\phi\right]=-\rho/\epsilon_0.
   $$

## 1. 参数入口和 solver 对象选择

`warpx.do_electrostatic` 一旦不是 `none`，WarpX 会关闭电磁 Maxwell solver。源码在 `WarpX::ReadParameters()` 中这样处理：

```cpp
pp_warpx.query_enum_sloppy("do_electrostatic", electrostatic_solver_id, "-_");
// if an electrostatic solver is used, set the Maxwell solver to None
if (electrostatic_solver_id != ElectrostaticSolverAlgo::None) {
    electromagnetic_solver_id = ElectromagneticSolverAlgo::None;
}
```

这句话的物理含义很直接：静电模式不再用 `EvolveE/B` 推 Maxwell 方程。每步的电场来自 Poisson 解，电磁波、激光传播和辐射传播不在这个模型内。

Poisson solver 有 `multigrid` 和 `fft` 两类。源码限制 FFT/IGF 只能用于 3D，且 open field boundary 只能由 FFT Poisson solver 处理：

```cpp
pp_warpx.query_enum_sloppy("poisson_solver", poisson_solver_id, "-_");
#ifndef WARPX_DIM_3D
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    poisson_solver_id!=PoissonSolverAlgo::IntegratedGreenFunction,
    "The FFT Poisson solver only works in 3D.");
#endif

const bool is_any_boundary_open =
    std::any_of(field_boundary_lo.begin(), field_boundary_lo.end(), [](auto fb){return (fb == FieldBoundaryType::Open ); }) ||
    std::any_of(field_boundary_hi.begin(), field_boundary_hi.end(), [](auto fb){return (fb == FieldBoundaryType::Open ); }) ;

if(is_any_boundary_open){
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        poisson_solver_id == PoissonSolverAlgo::IntegratedGreenFunction,
        "Field open boundary conditions are only implemented for the FFT-based Poisson solver");
}
```

`labframe-electromagnetostatic` 还会读取磁静态 vector Poisson 的收敛参数。它先继承 `self_fields_*`，再允许 `magnetostatic_solver_*` 覆盖：

```cpp
// Read magnetostatic solver parameters
// First use self_fields_* as defaults for backward compatibility,
// then allow explicit magnetostatic_solver_* parameters to override
utils::parser::queryWithParser(pp_warpx, "self_fields_required_precision", magnetostatic_solver_required_precision);
utils::parser::queryWithParser(pp_warpx, "magnetostatic_solver_required_precision", magnetostatic_solver_required_precision);
utils::parser::queryWithParser(pp_warpx, "self_fields_absolute_tolerance", magnetostatic_solver_absolute_tolerance);
utils::parser::queryWithParser(pp_warpx, "magnetostatic_solver_absolute_tolerance", magnetostatic_solver_absolute_tolerance);
utils::parser::queryWithParser(pp_warpx, "self_fields_max_iters", magnetostatic_solver_max_iters);
utils::parser::queryWithParser(pp_warpx, "magnetostatic_solver_max_iters", magnetostatic_solver_max_iters);
utils::parser::queryWithParser(pp_warpx, "self_fields_verbosity", magnetostatic_solver_verbosity);
utils::parser::queryWithParser(pp_warpx, "magnetostatic_solver_verbosity", magnetostatic_solver_verbosity);
```

对象选择在 `WarpX::WarpX()` 构造期完成：

```cpp
// Create Electrostatic Solver object if needed
if ((WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrame)
    || (WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic))
{
    m_electrostatic_solver = std::make_unique<LabFrameExplicitES>(nlevs_max);
}
// Initialize the effective potential electrostatic solver if required
else if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameEffectivePotential)
{
    m_electrostatic_solver = std::make_unique<EffectivePotentialES>(nlevs_max);
}
else
{
    m_electrostatic_solver = std::make_unique<RelativisticExplicitES>(nlevs_max);
}
```

这里有一个容易误读的点：`else` 会创建 `RelativisticExplicitES`，并不意味着用户一定启用了 relativistic electrostatic mode。这个对象也负责 electromagnetic 模式下 `species.initialize_self_fields=1` 的初始自场计算，以及边界电势触发的初始 Poisson 解。

## 2. 每步静电场入口

主入口是 `WarpX::ComputeSpaceChargeField(reset_fields)`：

```cpp
void WarpX::ComputeSpaceChargeField (bool const reset_fields)
{
    ABLASTR_PROFILE("WarpX::ComputeSpaceChargeField");
    using ablastr::fields::Direction;
    using warpx::fields::FieldType;

    if (reset_fields) {
        // Reset all E and B fields to 0, before calculating space-charge fields
        ABLASTR_PROFILE("WarpX::ComputeSpaceChargeField::reset_fields");
        for (int lev = 0; lev <= max_level; lev++) {
            for (int comp=0; comp<3; comp++) {
                m_fields.get(FieldType::Efield_fp, Direction{comp}, lev)->setVal(0);
                m_fields.get(FieldType::Bfield_fp, Direction{comp}, lev)->setVal(0);
            }
        }
    }

    m_electrostatic_solver->ComputeSpaceChargeField(
        m_fields, *mypc, myfl.get(), max_level );
}
```

`reset_fields` 为真时，E/B 先被清零，然后 solver 把静电或静磁自场加回 `Efield_fp/Bfield_fp`。这和 Maxwell push 的“在旧场基础上推进半步/整步”不同；静电场是重新由当前粒子电荷密度解出来的。`ComputeSpaceChargeField()` 并不关心具体算法，它只把 field registry、粒子容器、流体容器和 level 数传给多态 solver。

## 3. Poisson 边界条件和边界电势 parser

`PoissonBoundaryHandler` 构造时读取 `boundary.potential_*` 和 `warpx.eb_potential(x,y,z,t)`：

```cpp
PoissonBoundaryHandler::PoissonBoundaryHandler ()
{
    ReadParameters();
    BuildParsers();
}

void PoissonBoundaryHandler::ReadParameters()
{
    // Parse the input file for domain boundary potentials
    const ParmParse pp_boundary("boundary");

    // Read potentials from input file
    m_boundary_potential_specified |= pp_boundary.query("potential_lo_x", potential_xlo_str);
    m_boundary_potential_specified |= pp_boundary.query("potential_hi_x", potential_xhi_str);
    m_boundary_potential_specified |= pp_boundary.query("potential_lo_y", potential_ylo_str);
    m_boundary_potential_specified |= pp_boundary.query("potential_hi_y", potential_yhi_str);
    m_boundary_potential_specified |= pp_boundary.query("potential_lo_z", potential_zlo_str);
    m_boundary_potential_specified |= pp_boundary.query("potential_hi_z", potential_zhi_str);

    const ParmParse pp_warpx("warpx");
    m_boundary_potential_specified |= pp_warpx.query("eb_potential(x,y,z,t)", potential_eb_str);
```

随后 `DefinePhiBCs()` 把 WarpX 的 field boundary 映射为 AMReX linear operator boundary：

```cpp
if (WarpX::poisson_solver_id == PoissonSolverAlgo::Multigrid){
    if ( WarpX::field_boundary_lo[idim] == FieldBoundaryType::Periodic
            && WarpX::field_boundary_hi[idim] == FieldBoundaryType::Periodic ) {
        lobc[idim] = LinOpBCType::Periodic;
        hibc[idim] = LinOpBCType::Periodic;
        dirichlet_flag[idim*2] = false;
        dirichlet_flag[idim*2+1] = false;
    }
    else {
        has_non_periodic = true;
        if ( WarpX::field_boundary_lo[idim] == FieldBoundaryType::PEC ) {
            lobc[idim] = LinOpBCType::Dirichlet;
            dirichlet_flag[idim*2] = true;
        }
        else if ( WarpX::field_boundary_lo[idim] == FieldBoundaryType::Neumann ) {
            lobc[idim] = LinOpBCType::Neumann;
            dirichlet_flag[idim*2] = false;
        }
```

Multigrid 支持 periodic、PEC/Dirichlet、Neumann；open/PML 被拒绝：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    (WarpX::field_boundary_lo[idim] != FieldBoundaryType::Open &&
    WarpX::field_boundary_hi[idim] != FieldBoundaryType::Open &&
    WarpX::field_boundary_lo[idim] != FieldBoundaryType::PML &&
    WarpX::field_boundary_hi[idim] != FieldBoundaryType::PML) ,
    "Open and PML field boundary conditions only work with "
    "warpx.poisson_solver = fft."
);
```

FFT/Integrated Green Function 分支则要求 electrostatic mode 下边界为 open；如果只是 electromagnetic mode 中初始化 species self fields，则要求 PML：

```cpp
else if (WarpX::poisson_solver_id == PoissonSolverAlgo::IntegratedGreenFunction){
    if (WarpX::electrostatic_solver_id != ElectrostaticSolverAlgo::None){
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            (WarpX::field_boundary_lo[idim] == FieldBoundaryType::Open &&
            WarpX::field_boundary_hi[idim] == FieldBoundaryType::Open),
            "The FFT Poisson solver only works with field open boundary conditions "
            "in electrostatic mode."
        );
    }
    else{ // if electromagnetic mode on with species.initialize_self_fields = 1
        WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
            (WarpX::field_boundary_lo[idim] == FieldBoundaryType::PML &&
            WarpX::field_boundary_hi[idim] == FieldBoundaryType::PML),
            "The FFT Poisson solver only works with field PML boundary conditions "
            "to initialize the self-fields of the species in electromagnetic mode."
        );
    }
}
```

实际写入 Dirichlet 边界值的是 `ElectrostaticSolver::setPhiBC()`。它把每个非周期方向的 boundary parser 在当前时间 `t` 处求值，再把 domain 边界节点上的 `phi` 设为该值：

```cpp
if (!m_poisson_boundary_handler->has_non_periodic) { return; }

// get the boundary potentials at the current time
amrex::Array<amrex::Real,AMREX_SPACEDIM> phi_bc_values_lo;
amrex::Array<amrex::Real,AMREX_SPACEDIM> phi_bc_values_hi;
#ifdef WARPX_ZINDEX
    phi_bc_values_lo[WARPX_ZINDEX] = m_poisson_boundary_handler->potential_zlo(t);
    phi_bc_values_hi[WARPX_ZINDEX] = m_poisson_boundary_handler->potential_zhi(t);
#endif
```

```cpp
if (dirichlet_flag[2*idim] && iv[idim] == domain.smallEnd(idim)){
    phi_arr(i,j,k) = phi_bc_values_lo[idim];
}
if (dirichlet_flag[2*idim+1] && iv[idim] == domain.bigEnd(idim)) {
    phi_arr(i,j,k) = phi_bc_values_hi[idim];
}
```

所以边界电势不是 Poisson RHS 的源项，而是解空间上的 Dirichlet 约束；Neumann 边界不会在这里写 `phi` 值。

## 4. `ElectrostaticSolver::computePhi()`：调用 ABLASTR Poisson solver

静电 solver 基类统一读取 MLMG/FFT 收敛参数：

```cpp
void ElectrostaticSolver::ReadParameters () {

    ParmParse const pp_warpx("warpx");

    // Note that with the relativistic version, these parameters would be
    // input for each species.
    utils::parser::queryWithParser(
        pp_warpx, "self_fields_required_precision", self_fields_required_precision);
    utils::parser::queryWithParser(
        pp_warpx, "self_fields_absolute_tolerance", self_fields_absolute_tolerance);
    utils::parser::queryWithParser(
        pp_warpx, "self_fields_max_iters", self_fields_max_iters);
   utils::parser::queryWithParser(
        pp_warpx, "self_fields_verbosity", self_fields_verbosity);

    // FFT solver flags
   utils::parser::queryWithParser(
        pp_warpx, "use_2d_slices_fft_solver", is_igf_2d_slices);
}
```

`computePhi()` 负责把多层 `rho/phi` 整理成 ABLASTR solver 接口需要的按 level 排列的 vector：

```cpp
amrex::Vector<amrex::MultiFab *> sorted_rho;
amrex::Vector<amrex::MultiFab *> sorted_phi;
for (int lev = 0; lev < num_levels; ++lev) {
    sorted_rho.emplace_back(rho[lev]);
    sorted_phi.emplace_back(phi[lev]);
}
```

如果启用了 embedded boundary，并且调用方传入了 `Efield`，WarpX 不再用简单有限差分计算 EB 附近的 `E=-grad(phi)`，而是注册一个 post callback 让 AMReX/ABLASTR 在 Poisson solve 后计算电场：

```cpp
if (EB::enabled() && efield.has_value())
{
    // EB: use AMReX to directly calculate the electric field since with EB's the
    // simple finite difference scheme in WarpX::computeE sometimes fails

    amrex::Vector<amrex::Array<amrex::MultiFab *, AMREX_SPACEDIM>> e_field;
    for (int lev = 0; lev < num_levels; ++lev) {
        e_field.push_back(
#if defined(WARPX_DIM_1D_Z)
            amrex::Array<amrex::MultiFab*, 1>{
                efield.value()[lev][2]
            }
#elif defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
            amrex::Array<amrex::MultiFab*, 1>{
                efield.value()[lev][0]
            }
#elif defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
            amrex::Array<amrex::MultiFab*, 2>{
                efield.value()[lev][0], efield.value()[lev][2]
            }
#elif defined(WARPX_DIM_3D)
            amrex::Array<amrex::MultiFab *, 3>{
                efield.value()[lev][0], efield.value()[lev][1], efield.value()[lev][2]
            }
#endif
        );
    }
    post_phi_calculation = EBCalcEfromPhiPerLevel(e_field);
}
```

最终进入 `ablastr::fields::computePhi(...)`：

```cpp
ablastr::fields::computePhi(
    sorted_rho,
    sorted_phi,
    beta,
    required_precision,
    absolute_tolerance,
    max_iters,
    verbosity,
    warpx.Geom(),
    warpx.DistributionMap(),
    warpx.boxArray(),
    WarpX::grid_type,
    is_solver_igf_on_lev0,
    is_igf_2d,
    EB::enabled(),
    WarpX::do_single_precision_comms,
    warpx.refRatio(),
    post_phi_calculation,
    *m_poisson_boundary_handler,
    warpx.gett_new(0),
    eb_farray_box_factory
);
```

这里的 `beta` 是 relativistic solver 的关键参数。`beta=0` 时就是普通 Poisson；`beta!=0` 时 ABLASTR solve 的算子对应官方文档里的

$$
\nabla^2-(\boldsymbol\beta\cdot\nabla)^2.
$$

## 5. 从 `phi` 重建 `E` 和 `B`

`computeE()` 实现的是

$$
\mathbf E=-\nabla\phi+\boldsymbol\beta(\boldsymbol\beta\cdot\nabla\phi).
$$

以 3D nodal grid 为例，`Ex` 的代码是：

```cpp
Ex_arr(i,j,k) +=
    +(beta_x*beta_x-1._rt)*0.5_rt*inv_dx*(phi_arr(i+1,j  ,k  )-phi_arr(i-1,j  ,k  ))
    + beta_x*beta_y       *0.5_rt*inv_dy*(phi_arr(i  ,j+1,k  )-phi_arr(i  ,j-1,k  ))
    + beta_x*beta_z       *0.5_rt*inv_dz*(phi_arr(i  ,j  ,k+1)-phi_arr(i  ,j  ,k-1));
```

这一行可直接读成矩阵形式：

$$
E_i=(\beta_i\beta_j-\delta_{ij})\partial_j\phi.
$$

当 `beta=0`，只有对角项留下，得到普通静电场 `E_i=-partial_i phi`。如果 field 是 Yee staggered，源码不用中心差分到节点，而是按目标场分量的 staggering 取单边差分和横向平均。例如 3D staggered `Ex`：

```cpp
Ex_arr(i,j,k) +=
    +(beta_x*beta_x-1._rt) *inv_dx*(phi_arr(i+1,j  ,k  )-phi_arr(i  ,j  ,k  ))
    + beta_x*beta_y*0.25_rt*inv_dy*(phi_arr(i  ,j+1,k  )-phi_arr(i  ,j-1,k  )
                                + phi_arr(i+1,j+1,k  )-phi_arr(i+1,j-1,k  ))
    + beta_x*beta_z*0.25_rt*inv_dz*(phi_arr(i  ,j  ,k+1)-phi_arr(i  ,j  ,k-1)
                                + phi_arr(i+1,j  ,k+1)-phi_arr(i+1,j  ,k-1));
```

这说明静电场并不是简单写到 nodal grid 后再随便插值，而是直接按 `Efield_fp` 的 index type 重建，以保持和后续 gather/deposition 所期望的 staggering 一致。

`computeB()` 实现

$$
\mathbf B=-\frac{1}{c}\boldsymbol\beta\times\nabla\phi.
$$

如果 `beta=0` 立即返回：

```cpp
// return early if beta is 0 since there will be no B-field
if ((beta[0] == 0._rt) && (beta[1] == 0._rt) && (beta[2] == 0._rt)) { return; }
```

3D nodal grid 下的 curl-like 结构是：

```cpp
Bx_arr(i,j,k) += PhysConst::inv_c * (
    -beta_y*inv_dz*0.5_rt*(phi_arr(i,j  ,k+1)-phi_arr(i,j  ,k-1))
    +beta_z*inv_dy*0.5_rt*(phi_arr(i,j+1,k  )-phi_arr(i,j-1,k  )));
```

把括号整理成

$$
B_x=\frac{1}{c}(-\beta_y\partial_z\phi+\beta_z\partial_y\phi),
$$

正是 $-(\boldsymbol\beta\times\nabla\phi)_x/c$。

## 6. Lab-frame explicit electrostatic solver

`LabFrameExplicitES` 是 `warpx.do_electrostatic=labframe` 和 `labframe-electromagnetostatic` 共用的静电部分。初始化只做 Poisson 边界条件定义：

```cpp
void LabFrameExplicitES::InitData() {
    auto & warpx = WarpX::GetInstance();
    m_poisson_boundary_handler->DefinePhiBCs(warpx.Geom(0));
}
```

每步流程如下：

```cpp
const MultiLevelScalarField rho_fp = fields.get_mr_levels(FieldType::rho_fp, max_level);
const MultiLevelScalarField rho_cp = fields.get_mr_levels(FieldType::rho_cp, max_level, skip_lev0_coarse_patch);
const MultiLevelScalarField phi_fp = fields.get_mr_levels(FieldType::phi_fp, max_level);
const MultiLevelVectorField Efield_fp = fields.get_mr_levels_alldirs(FieldType::Efield_fp, max_level);

mpc.DepositCharge(rho_fp, 0.0_rt);
if (mfl) {
    const int lev = 0;
    mfl->DepositCharge(fields, *rho_fp[lev], lev);
}
```

先把所有 particle species 的电荷沉积到总 `rho_fp`；如果有流体 species，也把流体电荷加进去。因此 labframe solver 解的是总电荷密度

$$
\rho=\sum_s\rho_s+\rho_\mathrm{fluid}.
$$

随后同步多层电荷密度：

```cpp
// Apply filter, perform MPI exchange, interpolate across levels
const Vector<std::unique_ptr<MultiFab> > rho_buf(num_levels);
auto & warpx = WarpX::GetInstance();
warpx.SyncRho( rho_fp, rho_cp, amrex::GetVecOfPtrs(rho_buf) );

#ifndef WARPX_DIM_RZ
for (int lev = 0; lev < num_levels; lev++) {
    // Reflect density over PEC boundaries, if needed.
    warpx.ApplyRhofieldBoundary(lev, rho_fp[lev], PatchType::fine);
}
#endif
```

`SyncRho` 是并行/AMR 层面的守恒处理：guard cell 归并、MPI 交换、过滤和 coarse/fine 插值都在这里闭合。静电 solver 不应该在未同步的局部 `rho` 上解全局 Poisson。

Lab-frame 的 `beta=0`：

```cpp
// beta is zero in lab frame
// Todo: use simpler finite difference form with beta=0
const std::array<Real, 3> beta = {0._rt};
```

然后设置边界势并求 `phi`：

```cpp
// set the boundary potentials appropriately
setPhiBC(phi_fp, warpx.gett_new(0));

// Compute the potential phi, by solving the Poisson equation
if (IsPythonCallbackInstalled("poissonsolver")) {

    // Use the Python level solver (user specified)
    ExecutePythonCallback("poissonsolver");

} else {

#if defined(WARPX_DIM_1D_Z)
    // Use the tridiag solver with 1D
    computePhiTriDiagonal(rho_fp, phi_fp);
#else
    // Use the AMREX MLMG or the FFT (IGF) solver otherwise
    computePhi(rho_fp, phi_fp, beta, self_fields_required_precision,
               self_fields_absolute_tolerance, self_fields_max_iters,
               self_fields_verbosity, is_igf_2d_slices, Efield_fp);
#endif

}
```

1D Z 编译下使用 tridiagonal solver；其他维度使用 ABLASTR/AMReX MLMG 或 FFT/IGF。最后从 `phi` 得到 `E`：

```cpp
// Compute the electric field. Note that if an EB is used the electric
// field will be calculated in the computePhi call.
if (!EB::enabled()) { computeE( Efield_fp, phi_fp, beta ); }
else {
    if (IsPythonCallbackInstalled("poissonsolver")) { computeE(Efield_fp, phi_fp, beta); }
}
```

注意 EB 分支：如果不是 Python Poisson callback，`computePhi()` 中的 EB post callback 已经计算过电场；这里不再重复 `computeE()`。

### 6.1 1D tridiagonal Poisson

1D solver 解离散方程

$$
\phi_{i+1}-2\phi_i+\phi_{i-1}=-\rho_i\Delta x^2/\epsilon_0.
$$

源码先决定未知量区间：PEC 边界给定 `phi`，Neumann 边界则边界点也参与求解。

```cpp
int nx_solve_min = 1;
int nx_solve_max = nx_full_domain - 1;

if (field_boundary_lo0 == FieldBoundaryType::Neumann) {
    // Solve for the point on the lower boundary
    nx_solve_min = 0;
}
if (field_boundary_hi0 == FieldBoundaryType::Neumann) {
    // Solve for the point on the upper boundary
    nx_solve_max = nx_full_domain;
}
```

RHS 预乘 $\Delta x^2/\epsilon_0$：

```cpp
// Multiplier on the charge density
const amrex::Real norm = dx[0]*dx[0]/PhysConst::epsilon_0;
rho1d_mf.mult(norm);
```

PEC 下边界第一点使用边界值：

```cpp
if (field_boundary_lo0 == FieldBoundaryType::PEC) {

    phi1d_arr(1,0,0) = (phi1d_arr(0,0,0) + rho1d_arr(1,0,0))/diag;

} else if (field_boundary_lo0 == FieldBoundaryType::Neumann) {
```

Neumann 下边界则改写第一行，相当于使用 ghost point 消去法：

```cpp
// Neumann boundary condition
phi1d_arr(0,0,0) = rho1d_arr(0,0,0)/diag;

zwork1d_arr(1,0,0) = 2._rt/diag;
diag = 2._rt - zwork1d_arr(1,0,0);
phi1d_arr(1,0,0) = (rho1d_arr(1,0,0) - (-1._rt)*phi1d_arr(1-1,0,0))/diag;
```

中间点是标准 Thomas elimination：

```cpp
for (int i_up = 2 ; i_up < nx_solve_max ; i_up++) {

    zwork1d_arr(i_up,0,0) = 1._rt/diag;
    diag = 2._rt - zwork1d_arr(i_up,0,0);
    phi1d_arr(i_up,0,0) = (rho1d_arr(i_up,0,0) - (-1._rt)*phi1d_arr(i_up-1,0,0))/diag;

}
```

如果两端都是 Neumann，Poisson 方程只确定到任意常数，源码在上边界把一个值固定为零：

```cpp
if (diag == 0._rt) {
    // This happens if the lower boundary is also Neumann.
    // It this case, the potential is relative to an arbitrary constant,
    // so set the upper boundary to zero to force a value.
    phi1d_arr(nx_full_domain,0,0) = 0.;
} else {
    phi1d_arr(nx_full_domain,0,0) = (rho1d_arr(nx_full_domain,0,0) - (-1._rt)*phi1d_arr(nx_full_domain-1,0,0))/diag;
}
```

这正是 Neumann-Poisson 零模不唯一性的离散处理。

## 7. Relativistic explicit electrostatic solver

Relativistic solver 的初始化条件比 labframe 更宽。只要当前是 relativistic electrostatic，或某个 species 要初始化 self fields，或输入指定了边界电势，就需要准备 Poisson BC：

```cpp
void RelativisticExplicitES::InitData () {
    auto & warpx = WarpX::GetInstance();
    bool prepare_field_solve = (WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::Relativistic);
    // check if any of the particle containers have initialize_self_fields = True
    for (auto const& species : warpx.GetPartContainer()) {
        prepare_field_solve |= species->initialize_self_fields;
    }
    prepare_field_solve |= m_poisson_boundary_handler->m_boundary_potential_specified;

    if (prepare_field_solve) {
        m_poisson_boundary_handler->DefinePhiBCs(warpx.Geom(0));
    }
}
```

每步 `ComputeSpaceChargeField()` 遍历 species，而不是把所有 species 加成总电荷：

```cpp
const bool always_run_solve = (WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::Relativistic);

MultiLevelVectorField Efield_fp = fields.get_mr_levels_alldirs(FieldType::Efield_fp, max_level);
MultiLevelVectorField Bfield_fp = fields.get_mr_levels_alldirs(FieldType::Bfield_fp, max_level);

// Loop over the species and add their space-charge contribution to E and B.
// Note that the fields calculated here does not include the E field
// due to simulation boundary potentials
for (auto const& species : mpc) {
    if (always_run_solve || (species->initialize_self_fields)) {
        AddSpaceChargeField(*species, Efield_fp, Bfield_fp);
    }
}
```

这是因为每个 species 的平均速度不同，对应的 $\boldsymbol\beta$ 和 Lorentz-transformed field 不同。把不同 species 的 `rho` 先相加再用一个 beta 解方程，在物理上是不对的。

`AddSpaceChargeField()` 先为单个 species 分配局部 `rho/phi`：

```cpp
Vector<std::unique_ptr<MultiFab>> rho(num_levels);
Vector<std::unique_ptr<MultiFab>> rho_coarse(num_levels); // Used in order to interpolate between levels
Vector<std::unique_ptr<MultiFab>> phi(num_levels);
// Use number of guard cells used for local deposition of rho
const amrex::IntVect ng = warpx.get_ng_depos_rho();
for (int lev = 0; lev < num_levels; lev++) {
    BoxArray nba = warpx.boxArray(lev);
    nba.surroundingNodes();
    rho[lev] = std::make_unique<MultiFab>(nba, warpx.DistributionMap(lev), 1, ng);
    rho[lev]->setVal(0.);
    phi[lev] = std::make_unique<MultiFab>(nba, warpx.DistributionMap(lev), 1, 1);
    phi[lev]->setVal(0.);
```

然后只沉积该 species 的电荷，并同步：

```cpp
if ( !pc.do_not_deposit) {
    pc.DepositCharge(amrex::GetVecOfPtrs(rho),
        local, reset, apply_boundary_and_scale_volume,
        interpolate_across_levels);
}

// Apply filter, perform MPI exchange, interpolate across levels
const Vector<std::unique_ptr<MultiFab>> rho_buf(num_levels);
warpx.SyncRho(
    amrex::GetVecOfPtrs(rho),
    amrex::GetVecOfPtrs(rho_coarse),
    amrex::GetVecOfPtrs(rho_buf));
```

平均速度来自全部 MPI rank：

```cpp
// Get the particle beta vector
bool const local_average = false; // Average across all MPI ranks
std::array<ParticleReal, 3> beta_pr = pc.meanParticleVelocity(local_average);
std::array<Real, 3> beta;
for (int i=0 ; i < static_cast<int>(beta.size()) ; i++) {
    beta[i] = beta_pr[i]/PhysConst::c; // Normalize
}
```

最后用 species 自己的 self-field 收敛参数求 `phi`，并把 `E` 和 `B` 加到全局 field 上：

```cpp
computePhi( amrex::GetVecOfPtrs(rho), amrex::GetVecOfPtrs(phi),
            beta, pc.self_fields_required_precision,
            pc.self_fields_absolute_tolerance, pc.self_fields_max_iters,
            pc.self_fields_verbosity, is_igf_2d_slices);

// Compute the corresponding electric and magnetic field, from the potential phi
computeE( Efield_fp, amrex::GetVecOfPtrs(phi), beta );
computeB( Bfield_fp, amrex::GetVecOfPtrs(phi), beta );
```

边界电势另走 `AddBoundaryField()`：它设 `rho=0`、`beta=0`，只给 `E` 加边界电势的解，不给 `B` 加场：

```cpp
// Set the boundary potentials appropriately
setPhiBC( amrex::GetVecOfPtrs(phi), warpx.gett_new(0));

// beta is zero for boundaries
const std::array<Real, 3> beta = {0._rt};

// Compute the potential phi, by solving the Poisson equation
computePhi( amrex::GetVecOfPtrs(rho), amrex::GetVecOfPtrs(phi),
            beta, self_fields_required_precision,
            self_fields_absolute_tolerance, self_fields_max_iters,
            self_fields_verbosity, is_igf_2d_slices);

// Compute the corresponding electric field, from the potential phi.
computeE( Efield_fp, amrex::GetVecOfPtrs(phi), beta );
```

## 8. Effective potential electrostatic solver

Effective potential solver 是单层算法，初始化时为有效介电函数 `sigma` 分配 cell-centered MultiFab：

```cpp
void EffectivePotentialES::InitData() {
    auto & warpx = WarpX::GetInstance();
    m_poisson_boundary_handler->DefinePhiBCs(warpx.Geom(0));

    // Initialize "sigma" MF which stores the dressing of the Poisson equation.
    // It is a cell-centered multifab.
    auto& fields = warpx.GetMultiFabRegister();
    auto* rho = fields.get(warpx::fields::FieldType::rho_fp, 0);
    fields.alloc_init(
        warpx::fields::FieldType::effective_potential_sigma, /*level=*/ 0,
        convert(rho->boxArray(), IntVect(AMREX_D_DECL(0,0,0))),
        rho->DistributionMap(), 1, IntVect(AMREX_D_DECL(0,0,0)), 1.0_rt
    );
    m_overwrite_sigma = true;
}
```

每步先设置边界势，再计算 `sigma` 和总 `rho`：

```cpp
// set the boundary potentials appropriately
setPhiBC(phi_fp, warpx.gett_new(0));

// Calculate the mass enhancement factor - see  Appendix A of
// Barnes, Journal of Comp. Phys., 424 (2021), 109852.
// Also accumulate the total charge density.
ComputeSigma(rho_fp);

// perform phi calculation
computePhi(rho_fp, phi_fp, Efield_fp);
```

`ComputeSigma()` 的核心参数是 `C_SI`、时间滤波参数和 density floor：

```cpp
// Get the user set value for C_SI (defaults to 4)
amrex::Real C_SI = 4.0;
const ParmParse pp_warpx("warpx");
utils::parser::queryWithParser(pp_warpx, "effective_potential_factor", C_SI);

// Get the user set value for the time filtering parameter (defaults to 0.1)
amrex::Real time_filter_param = 0.1;
utils::parser::queryWithParser(pp_warpx, "effective_potential_time_filter_param", time_filter_param);

// Get the user set value for the density floor in m^-3 (defaults to 0.0)
amrex::Real density_floor = 0.0;
utils::parser::queryWithParser(pp_warpx, "effective_potential_density_floor", density_floor);
```

代码注释给出了有效介电函数：

```cpp
// The effective potential dielectric function is given by
// \varepsilon_{SI} = \varepsilon * (1 + \sum_{i in species} C_{SI}*(w_pi * dt)^2/4)
// Note the use of the plasma frequency in rad/s (not Hz) and the factor of 1/4,
// these choices make it so that C_SI = 1 is the marginal stability threshold.
auto mult_factor = (
    C_SI * warpx.getdt(lev) * warpx.getdt(lev) / (4._rt * PhysConst::epsilon_0)
);
```

对每个 species，先取单 species 电荷密度并加到总 `rho_fp`：

```cpp
auto rho = pc->GetChargeDensity(lev, true);

// Handle the parallel transfer of guard cells and apply filtering
warpx.ApplyFilterandSumBoundaryRho(lev, lev, *rho, 0, rho->nComp());

// Add rho for this species to the total charge density MF
amrex::MultiFab::Add(*rho_fp[lev], *rho, 0, 0, 1, rho_fp[lev]->nGrowVect());
```

再把 nodal `rho` 插值到 cell center，用绝对值和 floor 计算该 species 的 $\omega_{ps}^2$ 项：

```cpp
auto const q = std::abs(pc->getCharge());
auto const mult_factor_pc = mult_factor * q / pc->getMass();

// update sigma
for ( MFIter mfi(*sigma, TilingIfNotGPU()); mfi.isValid(); ++mfi ) {
    Array4<Real> const& sigma_arr = sigma->array(mfi);
    Array4<Real const> const& rho_arr = rho->const_array(mfi);

    amrex::ParallelFor(mfi.tilebox(), [=] AMREX_GPU_DEVICE (int i, int j, int k){
        // Interpolate rho to cell-centered value, applying a floor
        // on the density
        auto const rho_cc = std::max(
            density_floor*q,
            std::abs(ablastr::coarsen::sample::Interp(
                rho_arr, nodal, cell_centered, coarsen, i, j, k, 0
            ))
        );
        // add species term to sigma:
        // C_SI * w_p^2 * dt^2 / 4 = C_SI / 4 * q*rho/(m*eps0) * dt^2
        sigma_arr(i, j, k, 0) += time_filter_param * mult_factor_pc * rho_cc;
    });
}
```

最后加上基底 1：

```cpp
sigma->plus(time_filter_param, 0);
```

`sigma` 带时间滤波，因此实际更新是

$$
\sigma^{n+1}=(1-\alpha)\sigma^n+\alpha\left[1+\sum_s\frac{C_{EP}}{4}\omega_{ps}^2\Delta t^2\right].
$$

解方程时进入专用的 `computeEffectivePotentialPhi(...)`：

```cpp
ablastr::fields::computeEffectivePotentialPhi(
    sorted_rho,
    sorted_phi,
    *sigma,
    required_precision,
    absolute_tolerance,
    max_iters,
    verbosity,
    warpx.Geom(),
    warpx.DistributionMap(),
    warpx.boxArray(),
    WarpX::grid_type,
    false,
    EB::enabled(),
    WarpX::do_single_precision_comms,
    warpx.refRatio(),
    post_phi_calculation,
    *m_poisson_boundary_handler,
    warpx.gett_new(0),
    eb_farray_box_factory
);
```

所以 effective-potential 的差异不在 `E=-grad(phi)`，而在椭圆算子的系数 `sigma`：它解的是 variable-coefficient Poisson。

## 9. Magnetostatic solver：从电流到矢势再到 `B`

`labframe-electromagnetostatic` 静电部分仍由 `LabFrameExplicitES` 完成；磁静态部分由 `WarpX::ComputeMagnetostaticField()` 接着把 `B` 加回来：

```cpp
void
WarpX::ComputeMagnetostaticField()
{
    ABLASTR_PROFILE("WarpX::ComputeMagnetostaticField");
    // Fields have been reset in Electrostatic solver for this time step, these fields
    // are added into the B fields after electrostatic solve

    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(this->max_level == 0,
        "Magnetostatic solver not implemented with mesh refinement.");

    AddMagnetostaticFieldLabFrame();
}
```

当前实现明确不支持 mesh refinement。`AddMagnetostaticFieldLabFrame()` 先定义 vector potential 边界，再清零并沉积总电流：

```cpp
// Store the boundary conditions for the field solver if they haven't been
// stored yet
if (!m_vector_poisson_boundary_handler.bcs_set) {
    m_vector_poisson_boundary_handler.defineVectorPotentialBCs();
}

// reset current_fp before depositing current density for this step
for (int lev = 0; lev <= max_level; lev++) {
    for (int dim=0; dim < 3; dim++) {
        m_fields.get(FieldType::current_fp, Direction{dim}, lev)->setVal(0.);
    }
}

// Deposit current density (source of Poisson solver)
for (int ispecies=0; ispecies<mypc->nSpecies(); ispecies++){
    WarpXParticleContainer& species = mypc->GetParticleContainer(ispecies);
    if (!species.do_not_deposit) {
        species.DepositCurrent(
            m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
            dt[0], 0.);
    }
}
```

RZ/1D cylindrical/spherical 几何下还要做体积因子修正：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    for (int lev = 0; lev <= max_level; lev++) {
        ApplyInverseVolumeScalingToCurrentDensity(
            m_fields.get(FieldType::current_fp, Direction{0}, lev),
            m_fields.get(FieldType::current_fp, Direction{1}, lev),
            m_fields.get(FieldType::current_fp, Direction{2}, lev),
            lev );
    }
#endif

SyncCurrent("current_fp");
```

然后给 vector potential 设置边界值，并调用 vector Poisson solver：

```cpp
// set the boundary and current density potentials
setVectorPotentialBC(m_fields.get_mr_levels_alldirs(FieldType::vector_potential_fp_nodal, finest_level));

// Compute the vector potential A, by solving the Poisson equation
WARPX_ALWAYS_ASSERT_WITH_MESSAGE( !IsPythonCallbackInstalled("poissonsolver"),
    "Python Level Poisson Solve not supported for Magnetostatic implementation.");

computeVectorPotential(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::vector_potential_fp_nodal, finest_level),
    magnetostatic_solver_required_precision, magnetostatic_solver_absolute_tolerance,
    magnetostatic_solver_max_iters, magnetostatic_solver_verbosity
);
```

物理上是在 Coulomb gauge 下解

$$
\nabla^2\mathbf A=-\mu_0\mathbf J,\qquad \mathbf B=\nabla\times\mathbf A.
$$

源码注释在 curvilinear 情况写作 `nabla^2 r A = - r mu0 J`，反映了 metric/volume-weighted 的离散形式：

```cpp
/* Compute the vector potential `A` by solving the Poisson equation with `J` as
   a source.
   This uses the amrex solver.

    More specifically, this solves the equation
    \f[
        \vec{\nabla}^2 r \vec{A} = - r \mu_0 \vec{J}
 \f]
```

`computeVectorPotential()` 把三分量电流和三分量矢势整理成 vector Poisson 接口：

```cpp
amrex::Vector<amrex::Array<amrex::MultiFab*,3>> sorted_curr;
amrex::Vector<amrex::Array<amrex::MultiFab*,3>> sorted_A;
for (int lev = 0; lev <= finest_level; ++lev) {
    sorted_curr.emplace_back(amrex::Array<amrex::MultiFab*,3> ({curr[lev][0],
                                                                curr[lev][1],
                                                                curr[lev][2]}));
    sorted_A.emplace_back(amrex::Array<amrex::MultiFab*,3> ({A[lev][0],
                                                             A[lev][1],
                                                             A[lev][2]}));
}
```

它还注册 `post_A_calculation`，使 vector Poisson solve 后立刻从 `A` 计算 `B`：

```cpp
const ablastr::fields::MultiLevelVectorField Bfield_fp = m_fields.get_mr_levels_alldirs(FieldType::Bfield_fp, finest_level);
const std::optional<MagnetostaticSolver::EBCalcBfromVectorPotentialPerLevel> post_A_calculation(
{
    Bfield_fp,
    m_fields.get_mr_levels_alldirs(FieldType::vector_potential_grad_buf_e_stag, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::vector_potential_grad_buf_b_stag, finest_level)
});
```

最终调用 ABLASTR vector Poisson solver：

```cpp
ablastr::fields::computeVectorPotential(
    sorted_curr,
    sorted_A,
    required_precision,
    absolute_tolerance,
    max_iters,
    verbosity,
    this->geom,
    this->dmap,
    this->grids,
    this->m_vector_poisson_boundary_handler,
    EB::enabled(),
    WarpX::do_single_precision_comms,
    this->ref_ratio,
    post_A_calculation,
    gett_new(0),
    eb_farray_box_factory
);
```

## 10. 矢势边界条件和 `B=curl A`

Vector potential 的边界条件与 scalar potential 不同。PEC 边界上，法向分量 `A_n` 使用 Neumann，切向分量使用 Dirichlet：

```cpp
if ( WarpX::field_boundary_lo[idim] == FieldBoundaryType::PEC ) {
    if (ndotA) {
        lobc[adim][idim] = LinOpBCType::Neumann;
        dirichlet_flag[adim][idim*2] = false;
    } else {
        lobc[adim][idim] = LinOpBCType::Dirichlet;
        dirichlet_flag[adim][idim*2] = true;
    }
}
```

`setVectorPotentialBC()` 对 Dirichlet 标记处直接设置 `A=0`：

```cpp
if (dirichlet_flag[adim][2*idim] && iv[idim] == domain.smallEnd(idim)) {
    A_arr(i,j,k) = 0.;
}

if (dirichlet_flag[adim][2*idim+1] && iv[idim] == domain.bigEnd(idim)) {
    A_arr(i,j,k) = 0.;
}
```

从 `A` 到 `B` 的 post callback 用 MLMG 给出的梯度解，再插值到 `B` 的 staggering。`doInterp()` 先填 guard cell，然后调用 WarpX 的 finite-order centering stencil：

```cpp
ablastr::utils::communication::FillBoundary(src,
                                            src.nGrowVect(),
                                            WarpX::do_single_precision_comms);

for (MFIter mfi(dst, TilingIfNotGPU()); mfi.isValid(); ++mfi)
{
    IntVect const src_stag = src.ixType().toIntVect();
    IntVect const dst_stag = dst.ixType().toIntVect();

    Array4<amrex::Real const> const& src_arr = src.const_array(mfi);
    Array4<amrex::Real> const& dst_arr = dst.array(mfi);

    const Box bx = mfi.tilebox();

    ParallelFor(bx, [=] AMREX_GPU_DEVICE (int j, int k, int l) noexcept
    {
        warpx_interp(j, k, l, dst_arr, src_arr, dst_stag, src_stag, fg_nox, fg_noy, fg_noz,
            stencil_coeffs_x, stencil_coeffs_y, stencil_coeffs_z);
    });
}
```

`operator()` 按照

$$
\nabla\times\mathbf A
=
(\partial_y A_z-\partial_z A_y,\,
 \partial_z A_x-\partial_x A_z,\,
 \partial_x A_y-\partial_y A_x)
$$

逐项累加：

```cpp
// This will grab the gradient values for Ax
mlmg[0]->getGradSolution({buf_ptr});

// Interpolate dAx/dz to By grid buffer, then add to By
this->doInterp(*m_grad_buf_e_stag[lev][2],
               *m_grad_buf_b_stag[lev][1]);
MultiFab::Add(*(m_b_field[lev][1]), *(m_grad_buf_b_stag[lev][1]), 0, 0, 1, 0 );

// Interpolate dAx/dy to Bz grid buffer, then subtract from Bz
this->doInterp(*m_grad_buf_e_stag[lev][1],
               *m_grad_buf_b_stag[lev][2]);
m_grad_buf_b_stag[lev][2]->mult(-1._rt);
MultiFab::Add(*(m_b_field[lev][2]), *(m_grad_buf_b_stag[lev][2]), 0, 0, 1, 0 );
```

```cpp
// This will grab the gradient values for Ay
mlmg[1]->getGradSolution({buf_ptr});

// Interpolate dAy/dx to Bz grid buffer, then add to Bz
this->doInterp(*m_grad_buf_e_stag[lev][0],
               *m_grad_buf_b_stag[lev][2]);
MultiFab::Add(*(m_b_field[lev][2]), *(m_grad_buf_b_stag[lev][2]), 0, 0, 1, 0 );

// Interpolate dAy/dz to Bx grid buffer, then subtract from Bx
this->doInterp(*m_grad_buf_e_stag[lev][2],
               *m_grad_buf_b_stag[lev][0]);
m_grad_buf_b_stag[lev][0]->mult(-1._rt);
MultiFab::Add(*(m_b_field[lev][0]), *(m_grad_buf_b_stag[lev][0]), 0, 0, 1, 0 );
```

```cpp
// This will grab the gradient values for Az
mlmg[2]->getGradSolution({buf_ptr});

// Interpolate dAz/dy to Bx grid buffer, then add to Bx
this->doInterp(*m_grad_buf_e_stag[lev][1],
               *m_grad_buf_b_stag[lev][0]);
MultiFab::Add(*(m_b_field[lev][0]), *(m_grad_buf_b_stag[lev][0]), 0, 0, 1, 0 );

// Interpolate dAz/dx to By grid buffer, then subtract from By
this->doInterp(*m_grad_buf_e_stag[lev][0],
               *m_grad_buf_b_stag[lev][1]);
m_grad_buf_b_stag[lev][1]->mult(-1._rt);
MultiFab::Add(*(m_b_field[lev][1]), *(m_grad_buf_b_stag[lev][1]), 0, 0, 1, 0 );
```

逐项对应关系是：

- `+dAx/dz -> By`，`-dAx/dy -> Bz`
- `+dAy/dx -> Bz`，`-dAy/dz -> Bx`
- `+dAz/dy -> Bx`，`-dAz/dx -> By`

因此 magnetostatic solver 的 `B` 不是另一个 Maxwell 更新的结果，而是 vector Poisson 后的 `curl A`。

## 11. 场和电流的 staggering 分配

`labframe-electromagnetostatic` 要求电流和矢势使用 nodal 布局。`WarpX.cpp` 分配 field 时做了专门覆盖：

```cpp
if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic)
{
    jx_nodal_flag  = IntVect::TheNodeVector();
    jy_nodal_flag  = IntVect::TheNodeVector();
    jz_nodal_flag  = IntVect::TheNodeVector();
    ngJ = ngRho;
}
rho_nodal_flag = IntVect( AMREX_D_DECL(1,1,1) );
phi_nodal_flag = IntVect::TheNodeVector();
```

随后分配 vector potential 和 `curl A` 用的梯度缓冲：

```cpp
if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic)
{
    m_fields.alloc_init(FieldType::vector_potential_fp_nodal, Direction{0}, lev, amrex::convert(ba, rho_nodal_flag), dm, ncomps, ngRho, 0.0_rt);
    m_fields.alloc_init(FieldType::vector_potential_fp_nodal, Direction{1}, lev, amrex::convert(ba, rho_nodal_flag), dm, ncomps, ngRho, 0.0_rt);
    m_fields.alloc_init(FieldType::vector_potential_fp_nodal, Direction{2}, lev, amrex::convert(ba, rho_nodal_flag), dm, ncomps, ngRho, 0.0_rt);

    // Memory buffers for computing magnetostatic fields
    // Vector Potential A and previous step.  Time buffer needed for computing dA/dt to first order
    m_fields.alloc_init(FieldType::vector_potential_grad_buf_e_stag, Direction{0}, lev, amrex::convert(ba, Ex_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::vector_potential_grad_buf_e_stag, Direction{1}, lev, amrex::convert(ba, Ey_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::vector_potential_grad_buf_e_stag, Direction{2}, lev, amrex::convert(ba, Ez_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
```

这解释了 magnetostatic solver 中为什么有两个梯度缓冲：MLMG gradient 的自然位置更接近 E-stagger，需要再插值到 B-stagger 才能加到 `Bfield_fp`。

## 12. 小结：静电/静磁源码闭环

完整调用链可以压缩为：

1. `WarpX::ReadParameters()` 读取 `warpx.do_electrostatic`、`warpx.poisson_solver`、`self_fields_*` 和 `magnetostatic_solver_*`，并在 electrostatic mode 下关闭 Maxwell solver。
2. `WarpX::WarpX()` 按模式创建 `LabFrameExplicitES`、`EffectivePotentialES` 或 `RelativisticExplicitES`。
3. `PoissonBoundaryHandler` 读取边界电势 parser，并把 field boundary 映射成 AMReX linear-operator BC。
4. `WarpX::ComputeSpaceChargeField()` 可选择先清零 E/B，再调用具体 electrostatic solver。
5. `LabFrameExplicitES` 沉积总电荷，`SyncRho` 后解普通 Poisson，并用 `E=-grad(phi)` 重建电场。
6. `RelativisticExplicitES` 对每个 species 分开沉积电荷、计算平均 beta，解修正 Poisson，并加上 `E` 与 `B`。
7. `EffectivePotentialES` 构造 cell-centered `sigma`，解 variable-coefficient Poisson，提升大 `omega_pe dt` 下的稳定性。
8. `labframe-electromagnetostatic` 额外沉积总电流，解 vector Poisson 得到 `A`，再用 `B=curl A` 加回磁场。

从物理模型角度看，WarpX 这组代码覆盖了四个层级：纯 Vlasov-Poisson、准静态自磁场、平均速度相对论 self-field 初始化/推进、以及 effective-potential 半隐式稳定化。它们共享 field registry、rho/current 沉积和 AMReX/ABLASTR 椭圆求解器接口，但在 source 聚合方式、Poisson 算子、边界条件和 `phi/A -> E/B` 重建上有本质差异。
