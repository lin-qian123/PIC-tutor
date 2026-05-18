# FDTD 差分算子精读：Yee、Nodal 与 CKC

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

上一节已经把 `WarpX::EvolveE/B/F/G()` 追到 `FiniteDifferenceSolver::EvolveE/B/F/G()`。本节继续回答：`T_Algo::UpwardDx()`、`T_Algo::DownwardDz()` 这些模板差分算子到底是什么。核心源码在：

- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianNodalAlgorithm.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianCKCAlgorithm.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.cpp`

## 1. 参数层：WarpX Maxwell solver 选项

官方参数文档位置：`../warpx/Docs/source/usage/parameters.rst:3329-3353`。

```rst
Maxwell solver
^^^^^^^^^^^^^^

Two families of Maxwell solvers are implemented in WarpX, based on the Finite-Difference Time-Domain method (FDTD) or the Pseudo-Spectral Analytical Time-Domain method (PSATD), respectively.

.. pp:param:: algo.maxwell_solver
    :type: ``string``
    :optional:

    The algorithm for the Maxwell field solver.
    Available options are:

     - ``yee``: Yee FDTD solver.
     - ``ckc``: (not available in ``RZ``, ``RCYLINDER``, and ``RSPHERE`` geometries) Cole-Karkkainen solver with Cowan
       coefficients (see :cite:t:`param-CowanPRSTAB13`).
     - ``psatd``: Pseudo-spectral solver (see :ref:`theory <theory-mwsolve-psatd>`).
     - ``ect``: Enlarged cell technique (conformal finite difference solver. See :cite:t:`param-XiaoIEEE2005`).
     - ``hybrid``: The E-field will be solved using Ohm's law and a kinetic-fluid hybrid model (see :ref:`theory <theory-kinetic-fluid-hybrid-model>`).
     - ``none``: No field solve will be performed.
```

本节只处理 Cartesian FDTD 族中的三个算法：

- Yee：staggered Yee grid 的标准二阶 FDTD。
- Nodal：collocated/nodal grid 上的中心差分。
- CKC：Cole-Karkkainen-Cowan 扩展 stencil，用于改善数值色散。

RZ、RCYLINDER、RSPHERE 和 ECT 会在后续单独展开。

## 2. `FiniteDifferenceSolver` 构造函数：差分系数从哪里来

`FiniteDifferenceSolver` 对象构造时，会按 solver 和 grid type 初始化 stencil coefficients，并复制到 GPU device vector。源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.cpp:29-128`。

```cpp
FiniteDifferenceSolver::FiniteDifferenceSolver (
    ElectromagneticSolverAlgo const fdtd_algo,
    std::array<amrex::Real,3> cell_size,
    ablastr::utils::enums::GridType grid_type):
    // Register the type of finite-difference algorithm
    m_fdtd_algo{fdtd_algo},
    m_grid_type{grid_type}
{
    // return if not FDTD
    if (fdtd_algo == ElectromagneticSolverAlgo::None || fdtd_algo == ElectromagneticSolverAlgo::PSATD) {
        return;
    }
```

Cartesian 分支：

```cpp
#else
    if (grid_type == ablastr::utils::enums::GridType::Collocated) {

        CartesianNodalAlgorithm::InitializeStencilCoefficients( cell_size,
            m_h_stencil_coefs_x, m_h_stencil_coefs_y, m_h_stencil_coefs_z );

    } else if (fdtd_algo == ElectromagneticSolverAlgo::Yee ||
               fdtd_algo == ElectromagneticSolverAlgo::ECT ||
               fdtd_algo == ElectromagneticSolverAlgo::HybridPIC) {

        CartesianYeeAlgorithm::InitializeStencilCoefficients( cell_size,
            m_h_stencil_coefs_x, m_h_stencil_coefs_y, m_h_stencil_coefs_z );

    } else if (fdtd_algo == ElectromagneticSolverAlgo::CKC) {

        CartesianCKCAlgorithm::InitializeStencilCoefficients( cell_size,
            m_h_stencil_coefs_x, m_h_stencil_coefs_y, m_h_stencil_coefs_z );

    } else {
        WARPX_ABORT_WITH_MESSAGE(
            "FiniteDifferenceSolver: Unknown algorithm");
    }
```

然后复制到 device：

```cpp
    m_stencil_coefs_x.resize(m_h_stencil_coefs_x.size());
    m_stencil_coefs_y.resize(m_h_stencil_coefs_y.size());
    m_stencil_coefs_z.resize(m_h_stencil_coefs_z.size());

    amrex::Gpu::copyAsync(amrex::Gpu::hostToDevice,
                          m_h_stencil_coefs_x.begin(), m_h_stencil_coefs_x.end(),
                          m_stencil_coefs_x.begin());
    amrex::Gpu::copyAsync(amrex::Gpu::hostToDevice,
                          m_h_stencil_coefs_y.begin(), m_h_stencil_coefs_y.end(),
                          m_stencil_coefs_y.begin());
    amrex::Gpu::copyAsync(amrex::Gpu::hostToDevice,
                          m_h_stencil_coefs_z.begin(), m_h_stencil_coefs_z.end(),
                          m_stencil_coefs_z.begin());
    amrex::Gpu::synchronize();
```

这解释了 `EvolveE.cpp` 和 `EvolveB.cpp` 中这类代码的来源：

```cpp
Real const * const AMREX_RESTRICT coefs_x = m_stencil_coefs_x.dataPtr();
auto const n_coefs_x = static_cast<int>(m_stencil_coefs_x.size());
```

内核里不再判断用户参数，而是只使用已经构造好的 device-side coefficients。

## 3. Yee stencil：`Upward` 与 `Downward` 的 staggered 差分

Yee 算法初始化系数。源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H:23-37`。

```cpp
static void InitializeStencilCoefficients (
    std::array<amrex::Real,3>& cell_size,
    amrex::Vector<amrex::Real>& stencil_coefs_x,
    amrex::Vector<amrex::Real>& stencil_coefs_y,
    amrex::Vector<amrex::Real>& stencil_coefs_z ) {

    using namespace amrex;
    // Store the inverse cell size along each direction in the coefficients
    stencil_coefs_x.resize(1);
    stencil_coefs_x[0] = 1._rt/cell_size[0];
    stencil_coefs_y.resize(1);
    stencil_coefs_y[0] = 1._rt/cell_size[1];
    stencil_coefs_z.resize(1);
    stencil_coefs_z[0] = 1._rt/cell_size[2];
}
```

所以 Yee 的每个方向只有一个系数：

$$
c_x=\frac{1}{\Delta x},\quad c_y=\frac{1}{\Delta y},\quad c_z=\frac{1}{\Delta z}.
$$

`UpwardDx()` 与 `DownwardDx()` 的源码位置：`CartesianYeeAlgorithm.H:56-93`。

```cpp
static amrex::Real UpwardDx (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {

    using namespace amrex;
#if (defined WARPX_DIM_1D_Z)
    amrex::ignore_unused(F, coefs_x, i, j, k, ncomp);
    return 0._rt; // 1D Cartesian: derivative along x is 0
#else
    amrex::Real const inv_dx = coefs_x[0];
    return inv_dx*( F(i+1,j,k,ncomp) - F(i,j,k,ncomp) );
#endif
}
```

```cpp
template< typename T_Field>
static amrex::Real DownwardDx (
    T_Field const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {

    using namespace amrex;
#if (defined WARPX_DIM_1D_Z)
    amrex::ignore_unused(F, coefs_x, i, j, k, ncomp);
    return 0._rt; // 1D Cartesian: derivative along x is 0
#else
    amrex::Real const inv_dx = coefs_x[0];
    return inv_dx*( F(i,j,k,ncomp) - F(i-1,j,k,ncomp) );
#endif
}
```

数学上：

$$
D_x^+F_i=\frac{F_{i+1}-F_i}{\Delta x},
\qquad
D_x^-F_i=\frac{F_i-F_{i-1}}{\Delta x}.
$$

为什么一个叫 upward，一个叫 downward？因为在 staggered Yee grid 上，导数的输入和输出并不位于同一类格点。源码注释写得很直白：

```cpp
/**
 * Perform derivative along x on a cell-centered grid, from a nodal field `F`*/
```

和

```cpp
/**
 * Perform derivative along x on a nodal grid, from a cell-centered field `F`*/
```

也就是说 `Upward` 和 `Downward` 不只是左右差分符号，而是把 staggered 位置从 nodal 到 cell-centered、或从 cell-centered 到 nodal 的离散导数。

z 方向在不同编译维度下映射到不同数组 index。源码位置：`CartesianYeeAlgorithm.H:196-225`。

```cpp
static amrex::Real UpwardDz (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_z, int const /*n_coefs_z*/,
    int const i, int const j, int const k, int const ncomp=0 ) {

    using namespace amrex;
    Real const inv_dz = coefs_z[0];
#if defined WARPX_DIM_3D
    return inv_dz*( F(i,j,k+1,ncomp) - F(i,j,k,ncomp) );
#elif (defined WARPX_DIM_XZ)
    return inv_dz*( F(i,j+1,k,ncomp) - F(i,j,k,ncomp) );
#elif (defined WARPX_DIM_1D_Z)
    return inv_dz*( F(i+1,j,k,ncomp) - F(i,j,k,ncomp) );
#endif
}
```

这说明在 XZ 编译维度中，物理 z 方向对应数组第二个空间 index `j`；在 1D_Z 中，物理 z 对应数组 `i`。书稿里讲源码时不能把 `i,j,k` 机械等同于 `x,y,z`。

## 4. Yee CFL 与 guard cell

Yee 的 CFL 上限源码位置：`CartesianYeeAlgorithm.H:39-49`。

```cpp
static amrex::Real ComputeMaxDt ( amrex::Real const * const dx ) {
    using namespace amrex::literals;
    amrex::Real const delta_t  = 1._rt / ( std::sqrt( AMREX_D_TERM(
                                       1._rt / (dx[0]*dx[0]),
                                     + 1._rt / (dx[1]*dx[1]),
                                     + 1._rt / (dx[2]*dx[2])
                                 ) ) * PhysConst::c );
    return delta_t;
}
```

即

$$
\Delta t_{\max}
=\frac{1}{c\sqrt{\sum_d \Delta x_d^{-2}}}.
$$

Yee field solve 需要每个方向一个 guard cell：

```cpp
static amrex::IntVect GetMaxGuardCell () {
    // The yee solver requires one guard cell in each dimension
    return amrex::IntVect{AMREX_D_DECL(1,1,1)};
}
```

这个 guard cell 需求会影响 `GuardCellManager` 和 `FillBoundaryE/B` 的配置；场求解器正确不只取决于 stencil 公式，还取决于 stencil 读到的 neighbor 数据是否已同步。

## 5. Nodal algorithm：中心差分，Upward 与 Downward 等价

Nodal 算法的系数也只是反网格间距。源码位置：`CartesianNodalAlgorithm.H:24-38`。

```cpp
stencil_coefs_x.resize(1);
stencil_coefs_x[0] = 1._rt/cell_size[0];
stencil_coefs_y.resize(1);
stencil_coefs_y[0] = 1._rt/cell_size[1];
stencil_coefs_z.resize(1);
stencil_coefs_z[0] = 1._rt/cell_size[2];
```

但它的导数不是 forward/backward staggered difference，而是中心差分。源码位置：`CartesianNodalAlgorithm.H:59-97`。

```cpp
static amrex::Real UpwardDx (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {

    using namespace amrex;
#if (defined WARPX_DIM_1D_Z)
    ignore_unused(i, j, k, coefs_x, ncomp, F);
    return 0._rt; // 1D Cartesian: derivative along x is 0
#else
    Real const inv_dx = coefs_x[0];
    return 0.5_rt*inv_dx*( F(i+1,j,k,ncomp) - F(i-1,j,k,ncomp) );
#endif
}
```

`DownwardDx()` 直接调用 `UpwardDx()`：

```cpp
static amrex::Real DownwardDx (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_x, int const n_coefs_x,
    int const i, int const j, int const k, int const ncomp=0 ) {

    using namespace amrex;
#if (defined WARPX_DIM_1D_Z)
    ignore_unused(i, j, k, coefs_x, n_coefs_x, ncomp, F);
    return 0._rt; // 1D Cartesian: derivative along x is 0
#else
    return UpwardDx( F, coefs_x, n_coefs_x, i, j, k ,ncomp);
    // For CartesianNodalAlgorithm, UpwardDx and DownwardDx are equivalent
#endif
}
```

数学上：

$$
D_xF_i=\frac{F_{i+1}-F_{i-1}}{2\Delta x}.
$$

Nodal grid 没有 Yee 那种 E/B 空间 stagger，所以 `Upward` 和 `Downward` 在实现上等价。这个差异会影响数值色散和场/粒子插值策略，后续要和 `algo.field_gathering`、current centering 一起讲。

Nodal 的 CFL 公式和 Yee 相同：

```cpp
amrex::Real const delta_t  = 1._rt / ( std::sqrt( AMREX_D_TERM(
                                   1._rt/(dx[0]*dx[0]),
                                 + 1._rt/(dx[1]*dx[1]),
                                 + 1._rt/(dx[2]*dx[2])
                             ) ) * PhysConst::c );
```

## 6. CKC：扩展 stencil 与 Cowan 系数

官方理论文档把 CKC 放在 NSFDTD 一节。位置：`../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:81-160`。其中核心形式是

$$
D_t\mathbf B=-\nabla^*\times\mathbf E,
\qquad
D_t\mathbf E=\nabla\times\mathbf B-\mathbf J.
$$

也就是说 CKC 的非标准差分主要改 Faraday 方程中的 curl(E)，也就是 WarpX `EvolveB()` 中使用的 `Upward` 导数；Ampere 方程中的 `Downward` 导数保持标准形式。

源码也体现了这一点。`CartesianCKCAlgorithm::InitializeStencilCoefficients()` 位置：`CartesianCKCAlgorithm.H:25-112`。

```cpp
// Compute Cole-Karkkainen-Cowan coefficients according
// to Cowan - PRST-AB 16, 041303 (2013)
Real const inv_dx = 1._rt/cell_size[0];
Real const inv_dy = 1._rt/cell_size[1];
Real const inv_dz = 1._rt/cell_size[2];
#if defined WARPX_DIM_3D
Real const delta = std::max( { inv_dx,inv_dy,inv_dz } );
Real const rx = (inv_dx/delta)*(inv_dx/delta);
Real const ry = (inv_dy/delta)*(inv_dy/delta);
Real const rz = (inv_dz/delta)*(inv_dz/delta);
Real const beta = 0.125_rt*(1._rt - rx*ry*rz/(ry*rz + rz*rx + rx*ry));
Real const betaxy = ry*beta*inv_dx;
Real const betaxz = rz*beta*inv_dx;
Real const betayx = rx*beta*inv_dy;
Real const betayz = rz*beta*inv_dy;
Real const betazx = rx*beta*inv_dz;
Real const betazy = ry*beta*inv_dz;
Real const inv_r_fac = (1._rt/(ry*rz + rz*rx + rx*ry));
Real const gammax = ry*rz*(0.0625_rt - 0.125_rt*ry*rz*inv_r_fac);
Real const gammay = rx*rz*(0.0625_rt - 0.125_rt*rx*rz*inv_r_fac);
Real const gammaz = rx*ry*(0.0625_rt - 0.125_rt*rx*ry*inv_r_fac);
Real const alphax = (1._rt - 2._rt*ry*beta - 2._rt*rz*beta - 4._rt*gammax)*inv_dx;
Real const alphay = (1._rt - 2._rt*rx*beta - 2._rt*rz*beta - 4._rt*gammay)*inv_dy;
Real const alphaz = (1._rt - 2._rt*rx*beta - 2._rt*ry*beta - 4._rt*gammaz)*inv_dz;
```

系数存储顺序：

```cpp
stencil_coefs_x.resize(6);
stencil_coefs_x[0] = inv_dx;
stencil_coefs_x[1] = alphax;
stencil_coefs_x[2] = betaxy;
stencil_coefs_x[3] = betaxz;
stencil_coefs_x[4] = gammax*inv_dx;
```

`coefs_x[0]` 仍是标准 `1/dx`，给 `DownwardDx()` 使用；`coefs_x[1..4]` 是 CKC 扩展 stencil 给 `UpwardDx()` 使用。

## 7. CKC `UpwardDx()`：横向邻点加权的扩展导数

源码位置：`CartesianCKCAlgorithm.H:143-185`。

```cpp
static amrex::Real UpwardDx (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {

    using namespace amrex;
#if (defined WARPX_DIM_3D || WARPX_DIM_XZ)
    amrex::Real const alphax = coefs_x[1];
    amrex::Real const betaxz = coefs_x[3];
#endif
#if defined WARPX_DIM_3D
    amrex::Real const betaxy = coefs_x[2];
    amrex::Real const gammax = coefs_x[4];
#endif
```

3D 返回式：

```cpp
#if defined WARPX_DIM_3D
    return alphax * (F(i+1,j  ,k  ,ncomp) - F(i,  j,  k  ,ncomp))
         + betaxy * (F(i+1,j+1,k  ,ncomp) - F(i  ,j+1,k  ,ncomp)
                  +  F(i+1,j-1,k  ,ncomp) - F(i  ,j-1,k  ,ncomp))
         + betaxz * (F(i+1,j  ,k+1,ncomp) - F(i  ,j  ,k+1,ncomp)
                  +  F(i+1,j  ,k-1,ncomp) - F(i  ,j  ,k-1,ncomp))
         + gammax * (F(i+1,j+1,k+1,ncomp) - F(i  ,j+1,k+1,ncomp)
                  +  F(i+1,j-1,k+1,ncomp) - F(i  ,j-1,k+1,ncomp)
                  +  F(i+1,j+1,k-1,ncomp) - F(i  ,j+1,k-1,ncomp)
                  +  F(i+1,j-1,k-1,ncomp) - F(i  ,j-1,k-1,ncomp));
```

可读成

$$
D_x^*F =
\alpha_x(F_{i+1,j,k}-F_{i,j,k})
\beta_{xy}\sum_{\pm}(F_{i+1,j\pm1,k}-F_{i,j\pm1,k})
\beta_{xz}\sum_{\pm}(F_{i+1,j,k\pm1}-F_{i,j,k\pm1})
\gamma_x\sum_{\pm,\pm}(F_{i+1,j\pm1,k\pm1}-F_{i,j\pm1,k\pm1}).
$$

这就是文档中

$$
D_x^*=(\alpha+\beta S_x^1+\xi S_x^2)D_x
$$

在源码中的显式展开。区别是 Cowan 系数对非立方网格分方向计算，源码中写成 `alphax/betaxy/betaxz/gammax`。

2D XZ 分支去掉 y 方向横向项：

```cpp
#elif (defined WARPX_DIM_XZ)
    return alphax * (F(i+1,j  ,k  ,ncomp) - F(i,  j,  k  ,ncomp))
         + betaxz * (F(i+1,j+1,k  ,ncomp) - F(i  ,j+1,k  ,ncomp)
                  +  F(i+1,j-1,k  ,ncomp) - F(i  ,j-1,k  ,ncomp));
```

## 8. CKC `Downward` 保持局部差分

`CartesianCKCAlgorithm::DownwardDx()` 位置：`CartesianCKCAlgorithm.H:187-207`。

```cpp
template< typename T_Field>
static amrex::Real DownwardDx (
    T_Field const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {

    using namespace amrex;
#if (defined WARPX_DIM_1D_Z)
    amrex::ignore_unused(F, coefs_x, i, j, k, ncomp);
    return 0._rt; // 1D Cartesian: derivative along x is 0
#else
    amrex::Real const inv_dx = coefs_x[0];
    return inv_dx*( F(i,j,k,ncomp) - F(i-1,j,k,ncomp) );
#endif
}
```

z 方向 `DownwardDz()` 也一样，位置：`CartesianCKCAlgorithm.H:296-313`。

```cpp
template< typename T_Field>
static amrex::Real DownwardDz (
    T_Field const& F,
    amrex::Real const * const coefs_z, int const /*n_coefs_z*/,
    int const i, int const j, int const k, int const ncomp=0) {

    amrex::Real const inv_dz = coefs_z[0];
#if defined WARPX_DIM_3D
    return inv_dz*( F(i,j,k,ncomp) - F(i,j,k-1,ncomp) );
#elif (defined WARPX_DIM_XZ)
    return inv_dz*( F(i,j,k,ncomp) - F(i,j-1,k,ncomp) );
#elif (defined WARPX_DIM_1D_Z)
    return inv_dz*( F(i,j,k,ncomp) - F(i-1,j,k,ncomp) );
#endif
}
```

这和理论文档完全一致：

- Faraday: $D_t\mathbf B=-\nabla^*\times\mathbf E$
- Ampere: $D_t\mathbf E=\nabla\times\mathbf B-\mathbf J$

在 `EvolveB.cpp` 中，curl(E) 用的是 `T_Algo::UpwardD*`，所以 CKC 修改 B 更新中的 curl(E)。在 `EvolveE.cpp` 中，curl(B) 用的是 `T_Algo::DownwardD*`，所以 CKC 的 E 更新仍是局部 Yee-style 差分。

## 9. CKC CFL 与 guard cell

CKC 的 `ComputeMaxDt()` 源码位置：`CartesianCKCAlgorithm.H:114-126`。

```cpp
static amrex::Real ComputeMaxDt ( amrex::Real const * const dx ) {
#if (defined WARPX_DIM_1D_Z)
        amrex::Real const delta_t = dx[0]/PhysConst::c;
#elif (defined WARPX_DIM_XZ)
        // - In Cartesian 2D geometry: determined by the minimum cell size in all direction
        amrex::Real const delta_t = std::min( dx[0], dx[1] )/PhysConst::c;
#else
        // - In Cartesian 3D geometry: determined by the minimum cell size in all direction
        amrex::Real const delta_t = std::min( dx[0], std::min( dx[1], dx[2] ) ) / PhysConst::c;
#endif
    return delta_t;
}
```

这比 Yee 的

$$
\Delta t_{\max}
=\frac{1}{c\sqrt{\sum_d\Delta x_d^{-2}}}
$$

更接近“光每步走过最小 cell 尺寸”的上限。文档说明 CKC/NSFDTD 的目标之一就是改善数值色散，并允许在特定条件下更接近 $\Delta t=\Delta x/c$。

尽管 CKC stencil 看起来更宽，源码中 `GetMaxGuardCell()` 仍返回 1：

```cpp
static amrex::IntVect GetMaxGuardCell () {
    // The ckc solver requires one guard cell in each dimension
    return amrex::IntVect{AMREX_D_DECL(1,1,1)};
}
```

原因是 CKC 扩展项只访问相邻横向 offsets `j±1`、`k±1`，没有超过一层 guard cell。

## 10. 维度宏对数组索引的影响

三个 Cartesian 算法都大量使用维度宏：

- `WARPX_DIM_3D`：物理 `(x,y,z)` 对应数组 `(i,j,k)`。
- `WARPX_DIM_XZ`：物理 x 对应 `i`，物理 z 对应 `j`，物理 y 不存在。
- `WARPX_DIM_1D_Z`：物理 z 对应 `i`，x/y 导数为零。

例如 Yee 的 `UpwardDz()`：

```cpp
#if defined WARPX_DIM_3D
    return inv_dz*( F(i,j,k+1,ncomp) - F(i,j,k,ncomp) );
#elif (defined WARPX_DIM_XZ)
    return inv_dz*( F(i,j+1,k,ncomp) - F(i,j,k,ncomp) );
#elif (defined WARPX_DIM_1D_Z)
    return inv_dz*( F(i+1,j,k,ncomp) - F(i,j,k,ncomp) );
#endif
```

因此讲 WarpX 源码时必须区分“物理方向”和“AMReX Array4 index”。在 XZ/1D 编译下，源码里的 `j` 或 `i` 可能代表物理 z。

## 11. 本节总结

`EvolveB.cpp` 与 `EvolveE.cpp` 中的模板参数 `T_Algo` 具体含义如下：

| 算法 | `UpwardD*` | `DownwardD*` | CFL 上限 | 典型用途 |
|---|---|---|---|---|
| `CartesianYeeAlgorithm` | staggered forward difference | staggered backward difference | $1/[c\sqrt{\sum_d\Delta x_d^{-2}}]$ | 标准 Yee FDTD |
| `CartesianNodalAlgorithm` | centered difference | 与 `Upward` 等价 | 同 Yee 形式 | collocated/nodal grid |
| `CartesianCKCAlgorithm` | CKC/Cowan extended stencil | 标准 backward difference | $\min(\Delta x_d)/c$ | 降低数值色散的 NSFDTD |

这也解释了为什么 `FiniteDifferenceSolver::EvolveB()` 和 `EvolveE()` 只写一份模板 kernel，却能支持多种 Maxwell FDTD 算法。真正差异不在主 kernel 的 Maxwell 方程结构，而在 `T_Algo` 提供的离散导数。

下一步应继续两个方向：

- 读 `CylindricalYeeAlgorithm.H` 和 `SphericalYeeAlgorithm.H`，补齐 RZ/RCYLINDER/RSPHERE 几何项和轴处理。
- 读 `EvolveBPML.cpp`、`EvolveEPML.cpp`、`EvolveFPML.cpp`，解释 PML split-field 更新与 damping 参数。

