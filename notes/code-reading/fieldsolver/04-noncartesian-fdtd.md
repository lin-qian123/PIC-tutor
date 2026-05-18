# 非 Cartesian FDTD：RZ、RCYLINDER 与 RSPHERE 精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 FieldSolver 中非 Cartesian FDTD 的第一轮源码阅读：

- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CylindricalYeeAlgorithm.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/SphericalYeeAlgorithm.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveF.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/ComputeDivE.cpp`
- 官方参数文档 `../warpx/Docs/source/usage/parameters.rst:622-639,3342`

## 1. 参数与编译几何边界

官方参数文档说明 `geometry.dims` 支持 `RZ`、`RCYLINDER`、`RSPHERE`：

```rst
Supported values are ``1``, ``2``, ``3``, ``RZ``, ``RCYLINDER``, and ``RSPHERE``.

* For ``RZ``, a cylindrical geometry with the axis ``r`` and ``z``, with an azimuthal mode decomposition, with :pp:param:`warpx.n_rz_azimuthal_modes` providing further control.
* For ``RCYLINDER``, a cylindrical geometry with the axis ``r``, invariant in ``theta`` and ``z``.
* For ``RSPHERE``, a spherical geometry with the axis ``r``, invariant in ``theta`` and ``phi``.
```

同一参数文档还说明 CKC 不支持这些几何：

```rst
``ckc``: (not available in ``RZ``, ``RCYLINDER``, and ``RSPHERE`` geometries)
```

源码中，非 Cartesian FDTD 在编译期选择专用 algorithm。`FiniteDifferenceSolver.cpp:46-76`：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
    m_dr = cell_size[0];
    m_nmodes = WarpX::n_rz_azimuthal_modes;
    m_rmin = WarpX::GetInstance().Geom(0).ProbLo(0);
    if (fdtd_algo == ElectromagneticSolverAlgo::Yee ||
        fdtd_algo == ElectromagneticSolverAlgo::HybridPIC ) {
        CylindricalYeeAlgorithm::InitializeStencilCoefficients( cell_size,
            m_h_stencil_coefs_r, m_h_stencil_coefs_z );
```

```cpp
#elif defined(WARPX_DIM_RSPHERE)
    m_dr = cell_size[0];
    m_rmin = WarpX::GetInstance().Geom(0).ProbLo(0);
    if (fdtd_algo == ElectromagneticSolverAlgo::Yee ||
        fdtd_algo == ElectromagneticSolverAlgo::HybridPIC ) {
        SphericalYeeAlgorithm::InitializeStencilCoefficients(cell_size, m_h_stencil_coefs_r);
```

结论：

- RZ/RCYLINDER 只初始化 `r,z` 两个方向的 cylindrical Yee 系数。
- RSPHERE 只初始化 `r` 方向的 spherical Yee 系数。
- 这些编译几何下，当前源码只接受 `Yee` 或 `HybridPIC` 的 finite-difference algorithm；不是 Cartesian 中的 CKC/Nodal 分支。

## 2. CylindricalYeeAlgorithm：`1/r d(rF)/dr` 是核心算子

`CylindricalYeeAlgorithm.H` 初始化系数：

```cpp
stencil_coefs_r.resize(1);
stencil_coefs_r[0] = 1._rt/cell_size[0];  // 1./dr
stencil_coefs_z.resize(1);
stencil_coefs_z[0] = 1._rt/cell_size[2];  // 1./dz
```

RZ 的 CFL 不是简单 Cartesian CFL，而是含 azimuthal modes 的经验/半解析限制：

```cpp
std::array< amrex::Real, 6 > const multimode_coeffs = {{ 0.2105_rt, 1.0_rt, 3.5234_rt, 8.5104_rt, 15.5059_rt, 24.5037_rt }};
const amrex::Real multimode_alpha = (n_rz_azimuthal_modes < 7)?
    multimode_coeffs[n_rz_azimuthal_modes-1]:
    (n_rz_azimuthal_modes - 1._rt)*(n_rz_azimuthal_modes - 1._rt) - 0.4_rt;
const amrex::Real delta_t = 1._rt / ( std::sqrt(
                             (1._rt + multimode_alpha) / (dx[0]*dx[0])
                            + 1._rt / (dx[1]*dx[1])
                      ) * PhysConst::c );
```

cylindrical divergence/curl 中反复出现的算子是

$$
\frac{1}{r}\frac{\partial(rF)}{\partial r}.
$$

源码实现为 `UpwardDrr_over_r()`：

```cpp
Real const inv_dr = coefs_r[0];
return 1._rt/r * inv_dr*( (r+0.5_rt*dr)*F(i+1,j,k,comp) - (r-0.5_rt*dr)*F(i,j,k,comp) );
```

以及 `DownwardDrr_over_r()`：

```cpp
Real const inv_dr = coefs_r[0];
return 1._rt/r * inv_dr*( (r+0.5_rt*dr)*F(i,j,k,comp) - (r-0.5_rt*dr)*F(i-1,j,k,comp) );
```

这就是 cylindrical Yee 和 Cartesian Yee 的主要差异：不是简单 $\partial_rF$，而是带 metric factor 的保守形式。

`RCYLINDER` 代表只随 r 变化，z derivative 直接为零：

```cpp
#elif defined(WARPX_DIM_RCYLINDER)
    using namespace amrex::literals;
    amrex::ignore_unused(F, coefs_z, i, j, k, comp);
    return 0._rt;
```

## 3. RZ mode decomposition：实部/虚部组件

RZ 使用 azimuthal mode 展开。对于 $m\ge 1$，每个 mode 存实部和虚部。源码中 component 编号是：

- `0`：m=0。
- `2*m-1`：第 m 个 mode 的实部。
- `2*m`：第 m 个 mode 的虚部。

例如 `EvolveBCylindrical()` 更新 `Br` 时：

```cpp
Br(i, j, 0, 0) += dt * T_Algo::UpwardDz(Etheta, coefs_z, n_coefs_z, i, j, 0, 0); // Mode m=0
for (int m=1; m<nmodes; m++) { // Higher-order modes
    Br(i, j, 0, 2*m-1) += dt*(
        T_Algo::UpwardDz(Etheta, coefs_z, n_coefs_z, i, j, 0, 2*m-1)
        - m * Ez(i, j, 0, 2*m  )/r );  // Real part
    Br(i, j, 0, 2*m  ) += dt*(
        T_Algo::UpwardDz(Etheta, coefs_z, n_coefs_z, i, j, 0, 2*m  )
        + m * Ez(i, j, 0, 2*m-1)/r ); // Imaginary part
}
```

连续形式上，$\partial_\theta$ 在 Fourier mode 中变成 $im$。把复场拆成实部/虚部后，$im$ 会把实部和虚部耦合，并引入符号相反的 $m/r$ 项。这正是上面两行中 `- m * Ez_imag/r` 和 `+ m * Ez_real/r` 的来源。

## 4. 轴上正则化：不能直接除以 r

RZ 的 `r=0` 是坐标奇点。源码不在轴上硬算 `m/r`，而是按 mode 的正则性条件处理。

`EvolveBCylindrical()` 中 `Br` 轴上处理：

```cpp
if (r != 0) {
    // Off-axis, regular Maxwell equations
    // ...
} else { // r==0: On-axis corrections
    // Ensure that Br remains 0 on axis (except for m=1)
    Br(i, j, 0, 0) = 0.; // Mode m=0
    for (int m=1; m<nmodes; m++) {
        if (m == 1){
            Br(i, j, 0, 2*m-1) += dt*(
                T_Algo::UpwardDz(Etheta, coefs_z, n_coefs_z, i, j, 0, 2*m-1)
                - m * Ez(i+1, j, 0, 2*m  )/dr );
```

`EvolveECylindrical()` 中 `Etheta` 轴上处理更明显：

```cpp
if (m == 1){
    // Etheta(r=0,m=1) should equal -iEr(r=0,m=1), for the fields Er and Etheta to be
    // independent of theta at r=0.
    Etheta(i,j,0,2*m-1) =  Er(i,j,0,2*m  );
    Etheta(i,j,0,2*m  ) = -Er(i,j,0,2*m-1);
} else {
    Etheta(i, j, 0, 2*m-1) = 0.;
    Etheta(i, j, 0, 2*m  ) = 0.;
}
```

这段代码把坐标奇点处的物理正则性条件直接写进 field update。对书稿来说，这是 RZ field solver 不能被简化成“把 x 改成 r”的关键证据。

## 5. `EvolveECylindrical()`：curl(B)、电流和 F 修正

`EvolveECylindrical()` 的 `Er` 更新：

```cpp
Er(i, j, 0, 0) +=  c2 * dt*(
    - T_Algo::DownwardDz(Btheta, coefs_z, n_coefs_z, i, j, 0, 0)
    - PhysConst::mu0 * jr(i, j, 0, 0) ); // Mode m=0
for (int m=1; m<nmodes; m++) {
    Er(i, j, 0, 2*m-1) += c2 * dt*(
        - T_Algo::DownwardDz(Btheta, coefs_z, n_coefs_z, i, j, 0, 2*m-1)
        + m * Bz(i, j, 0, 2*m  )/r
        - PhysConst::mu0 * jr(i, j, 0, 2*m-1) );
```

它对应 Ampere 方程

$$
\partial_t\mathbf E=c^2(\nabla\times\mathbf B-\mu_0\mathbf J),
$$

但 cylindrical curl 中含 $m/r$ mode coupling。若 `Ffield` 存在，RZ 还会加入 hyperbolic divergence cleaning 的 `grad(F)`。例如：

```cpp
Er(i, j, 0, 0) += c2 * dt * T_Algo::UpwardDr(F, coefs_r, n_coefs_r, i, j, 0, 0);
```

`Etheta` 的 `grad(F)` 对 m=0 无更新，对高阶 mode 有 $mF/r$ 项：

```cpp
Etheta(i, j, 0, 2*m-1) += c2 * dt *  m * F(i, j, 0, 2*m  )/r;
Etheta(i, j, 0, 2*m  ) += c2 * dt * -m * F(i, j, 0, 2*m-1)/r;
```

## 6. `EvolveF` 与 `ComputeDivE`：cylindrical divergence

`EvolveFCylindrical()` 更新

$$
\partial_tF=\nabla\cdot\mathbf E-\rho/\epsilon_0.
$$

off-axis 的 m=0 更新为：

```cpp
F(i, j, 0, 0) += dt * (
    - rho(i, j, 0, rho_shift) * inv_epsilon0
    + T_Algo::DownwardDrr_over_r(Er, r, dr, coefs_r, n_coefs_r, i, j, 0, 0)
    + T_Algo::DownwardDz(Ez, coefs_z, n_coefs_z, i, j, 0, 0) );
```

这就是

$$
\nabla\cdot\mathbf E
=\frac{1}{r}\frac{\partial(rE_r)}{\partial r}
+\frac{1}{r}\frac{\partial E_\theta}{\partial\theta}
+\frac{\partial E_z}{\partial z}.
$$

对高阶 modes，源码再加入 `m*Et/r` 的实虚耦合项。`ComputeDivECylindrical()` 使用同样结构，但只输出 divE，不减 $\rho/\epsilon_0$。

轴上 m=0 的 cylindrical divergence 使用正则化：

```cpp
divE(i, j, 0, 0) =
       4._rt*Er(i, j, 0, 0)/dr // regularization
     + T_Algo::DownwardDz(Ez, coefs_z, n_coefs_z, i, j, 0, 0);
```

这里的 `4*Er/dr` 来自 Yee staggered 网格下轴附近 $E_r\propto r$ 的离散极限。

## 7. SphericalYeeAlgorithm：`1/r^2 d(r^2F)/dr`

RSPHERE 只保留径向依赖。`SphericalYeeAlgorithm.H` 中除了 `1/r d(rF)/dr`，还定义了 spherical divergence 的核心算子：

```cpp
amrex::Real const inv_dr = coefs_r[0];
amrex::Real const rph = r + 0.5_rt*dr;
amrex::Real const rmh = r - 0.5_rt*dr;
return 1._rt/(r*r) * inv_dr*( rph*rph*F(i,j,k,comp) - rmh*rmh*F(i-1,j,k,comp) );
```

它对应

$$
\frac{1}{r^2}\frac{\partial(r^2F)}{\partial r}.
$$

RSPHERE 的 CFL 在当前源码中是经验值：

```cpp
const amrex::Real delta_t = 0.78_rt * dx[0] / PhysConst::c;
```

## 8. `EvolveBSpherical()` 和 `EvolveESpherical()`

RSPHERE 的 B 更新非常短：

```cpp
Br(i, 0, 0, 0) = 0.;
```

```cpp
Real const r = rmin + (i + 0.5_rt)*dr;
Btheta(i, 0, 0, 0) += dt*( + T_Algo::UpwardDrr_over_r(Ephi, r, dr, coefs_r, n_coefs_r, i, 0, 0, 0));
```

```cpp
Bphi(i, 0, 0, 0) += dt*( - T_Algo::UpwardDrr_over_r(Etheta, r, dr, coefs_r, n_coefs_r, i, 0, 0, 0));
```

E 更新则是：

```cpp
Er(i, 0, 0, 0) += c2 * dt*(
    - PhysConst::mu0 * jr(i, 0, 0, 0) );
```

```cpp
Etheta(i, 0, 0, 0) += c2 * dt*(
    - T_Algo::DownwardDrr_over_r(Bphi, r, dr, coefs_r, n_coefs_r, i, 0, 0, 0)
    - PhysConst::mu0 * jtheta(i, 0, 0, 0 ) );
```

```cpp
Ephi(i, 0, 0, 0) += c2 * dt*(
    + T_Algo::DownwardDrr_over_r(Btheta, r, dr, coefs_r, n_coefs_r, i, 0, 0, 0)
    - PhysConst::mu0 * jphi(i, 0, 0, 0  ) );
```

`Er` 没有 curl(B) 项，只响应径向电流；横向分量通过径向 curl 更新。

`EvolveFSpherical()` 和 `ComputeDivESpherical()` 使用

$$
\nabla\cdot\mathbf E=\frac{1}{r^2}\frac{\partial(r^2E_r)}{\partial r}.
$$

轴上正则化为：

```cpp
F(i, j, 0, 0) += dt * (
    - rho(i, j, 0, rho_shift) * inv_epsilon0
     + 6._rt*Er(i, j, 0, 0)/dr);
```

对应 `ComputeDivESpherical()` 中的 `6*Er/dr`。

## 9. 与 PML 和其他功能的边界

本轮源码阅读给出几个边界：

- `EvolveBPML/EPML/FPML` 对 RZ/RCYLINDER/RSPHERE 会 abort；FDTD split-field PML 只支持 Cartesian。
- `DampPML()` 对 RZ PSATD PML 有单独 `pml_rz` 路径，但这不是上述 FDTD PML field update。
- `MacroscopicEvolveE.cpp` 明确写着宏观介质 E push 当前不支持 RZ。
- `ComputeGradient`、`ComputeLaplacian`、`ComputeVectorLaplian` 的 cylindrical/spherical 版本当前多处直接 abort，后续 electrostatic/implicit/hybrid 章节必须逐项核对，不能假设所有算子都实现。

后续应继续进入：

- `ApplySilverMuellerBoundary.cpp` 中非 Cartesian 辐射边界。
- `HybridPICSolveE.cpp` 的 cylindrical/spherical 分支。
- `SpectralSolver/` 的 RZ PSATD 路径。
