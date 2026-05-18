# 6. 电磁场求解器

电磁 PIC 的场求解器离散 Maxwell 方程。显式 FDTD 的经典代表是 Yee 算法：电场和磁场在空间上交错，在时间上也交错。抽象地写，

$$
\mathbf{B}^{n+1/2}=\mathbf{B}^{n}-\frac{\Delta t}{2}\nabla_h\times\mathbf{E}^{n},
$$

$$
\mathbf{E}^{n+1}=\mathbf{E}^{n}+c^2\Delta t\nabla_h\times\mathbf{B}^{n+1/2}
-\frac{\Delta t}{\epsilon_0}\mathbf{J}^{n+1/2},
$$

$$
\mathbf{B}^{n+1}=\mathbf{B}^{n+1/2}-\frac{\Delta t}{2}\nabla_h\times\mathbf{E}^{n+1}.
$$

这正对应 `WarpX::OneStep_nosub` 中的 FDTD 路径：`EvolveB(dt/2)`、`EvolveE(dt)`、`EvolveB(dt/2)`。本机源码位置是 `../warpx/Source/Evolve/WarpXEvolve.cpp` 行 603-640。

WarpX 的场推进封装在 `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp`。其中：

- `WarpX::EvolveB` 行 946 起：按 level 和 patch type 调用 FDTD solver 或 PML solver 的 B 更新。
- `WarpX::EvolveE` 行 1000 起：按 level 和 patch type 调用 E 更新，并处理 PML 和电荷守恒相关字段。
- 文件前部包含 PSATD current correction、Vay deposition 和谱空间 transform 辅助函数。

真正的 FDTD stencil 在 `Source/FieldSolver/FiniteDifferenceSolver/` 中，例如 `EvolveB.cpp`、`EvolveE.cpp`、`EvolveBPML.cpp`、`EvolveEPML.cpp`。当前已新增第一篇源码精读 `notes/code-reading/fieldsolver/00-fieldsolver-dispatch.md`，开始逐块展开这些文件。

`WarpX::EvolveB()` 的顶层路由在 `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:946-990`：

```cpp
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

`FiniteDifferenceSolver::EvolveB()` 的 Cartesian 主 kernel 在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp:130-211`：

```cpp
Bx(i, j, k) += dt * T_Algo::UpwardDz(Ey, coefs_z, n_coefs_z, i, j, k)
             - dt * T_Algo::UpwardDy(Ez, coefs_y, n_coefs_y, i, j, k);

By(i, j, k) += dt * T_Algo::UpwardDx(Ez, coefs_x, n_coefs_x, i, j, k)
             - dt * T_Algo::UpwardDz(Ex, coefs_z, n_coefs_z, i, j, k);

Bz(i, j, k) += dt * T_Algo::UpwardDy(Ex, coefs_y, n_coefs_y, i, j, k)
             - dt * T_Algo::UpwardDx(Ey, coefs_x, n_coefs_x, i, j, k);
```

这就是

$$
\partial_t\mathbf{B}=-\nabla_h\times\mathbf{E}.
$$

`FiniteDifferenceSolver::EvolveE()` 的 Cartesian 主 kernel 在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp:119-228`：

```cpp
Ex(i, j, k) += c2 * dt * (
    - T_Algo::DownwardDz(By, coefs_z, n_coefs_z, i, j, k)
    + T_Algo::DownwardDy(Bz, coefs_y, n_coefs_y, i, j, k)
    - PhysConst::mu0 * jx(i, j, k) );
```

它对应

$$
\partial_t\mathbf{E}=c^2(\nabla_h\times\mathbf{B}-\mu_0\mathbf{J}).
$$

如果开启 `do_dive_cleaning`，`EvolveE()` 还会加入 `grad(F)`；`EvolveF.cpp` 更新

$$
\partial_tF=\nabla_h\cdot\mathbf{E}-\rho/\epsilon_0.
$$

如果开启 `do_divb_cleaning`，`EvolveG.cpp` 更新

$$
\partial_tG=c^2\nabla_h\cdot\mathbf{B},
$$

并由 `EvolveB.cpp` 中的 `+grad(G)` 反馈到磁场。

PSATD 的思路不同：在 Fourier 空间中，Maxwell 方程的线性部分可以在一个时间步内解析积分。这样可以显著降低数值色散，尤其适合激光等离子体加速、boosted frame 和长距离传播问题。代价是并行分解、边界、PML、current correction 和多层 AMR 的实现更复杂。WarpX 的 `OneStep_nosub` 对 PSATD 单独分支：行 575-602 调用 `PushPSATD`、PML damping 和谱场回填。

电磁求解器的稳定性首先受 CFL 条件约束。对标准 Yee 网格，时间步必须小于电磁波跨越网格的稳定上限。WarpX 输入中可通过 `warpx.cfl` 控制 CFL 系数；Langmuir 示例使用 `warpx.cfl = 0.8`，uniform plasma 示例使用 `warpx.cfl = 1.0`。

一个常见误区是只把 field solver 当作 Maxwell 方程更新器。真实代码还必须处理：

- guard cell 填充；
- nodal point 同步；
- PML 阻尼；
- current filtering；
- divergence cleaning；
- embedded boundary；
- macroscopic medium；
- PSATD 的谱空间电流校正。

因此，写“场求解器正确”不能只看 `EvolveE.cpp` 和 `EvolveB.cpp`。必须同时检查它们在主循环中的调用时间、输入的 `J` 是否已同步、边界和 guard cells 是否处在正确状态。

## 6.1 FDTD 差分算子：Yee、Nodal 与 CKC

`notes/code-reading/fieldsolver/01-fdtd-evolve-e-b.md` 已经把 `T_Algo::Upward/Downward` 展开到算法头文件。Yee 的 `UpwardDx` 和 `DownwardDx` 分别是 staggered forward/backward difference：

```cpp
return inv_dx*( F(i+1,j,k,ncomp) - F(i,j,k,ncomp) );

return inv_dx*( F(i,j,k,ncomp) - F(i-1,j,k,ncomp) );
```

Nodal grid 没有 Yee 那种 E/B 空间交错，所以 `UpwardDx` 是中心差分，`DownwardDx` 直接调用同一个函数：

```cpp
return 0.5_rt*inv_dx*( F(i+1,j,k,ncomp) - F(i-1,j,k,ncomp) );
```

CKC 的关键差异是 `Upward` 使用横向邻点加权扩展 stencil，而 `Downward` 保持局部 backward difference。这对应理论文档中的

$$
D_t\mathbf B=-\nabla^*\times\mathbf E,\qquad
D_t\mathbf E=\nabla\times\mathbf B-\mathbf J.
$$

因此同一个 `EvolveB.cpp` 模板 kernel 在传入 `CartesianYeeAlgorithm`、`CartesianNodalAlgorithm` 或 `CartesianCKCAlgorithm` 时，会得到不同的离散 curl。

本章当前引用的核心文献线索是 `Yee`、`GodfreyJCP2014_PSATD`、`Lehe2016`、`VayJCP2013`。后续需要将 PSATD 相关论文用 MinerU 转换成 Markdown，并补一节 Galilean PSATD 与数值 Cherenkov 不稳定性的推导。

## 6.2 FDTD PML split-field 更新

PML 的目标是在计算区域边缘吸收入射电磁波。Berenger PML 的基本做法不是简单给整个场乘阻尼，而是把场分量拆成不同方向的 split components，并对这些分量施加匹配吸收。WarpX 的 FDTD PML 第一层实现见 `notes/code-reading/fieldsolver/02-fdtd-pml.md`。

PML split components 的 component 编号定义在 `../warpx/Source/BoundaryConditions/PMLComponent.H:8-18`：

```cpp
/* In WarpX, the split fields of the PML (e.g. Eyx, Eyz) are stored as
 * components of a MultiFab (e.g. component 0 and 1 of the MultiFab for Ey)
 * The correspondence between the component index (0,1) and its meaning
 * (yx, yz, etc.) is defined in the present file */

 struct PMLComp {
   enum { xy=0, xz=1, xx=2,
          yz=0, yx=1, yy=2,
          zx=0, zy=1, zz=2,
          x=0, y=1, z=2 }; // Used for the PML components of F
 };
```

因此，`Ex(i,j,k,PMLComp::xy)` 不是另一个物理电场分量，而是 `E_x` 中由 y 方向 curl 项驱动的 split component。这个存储约定贯穿 `EvolveBPML.cpp`、`EvolveEPML.cpp` 和 `EvolveFPML.cpp`。

`EvolveBPML()` 明确把非 Cartesian FDTD PML 排除掉：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    amrex::ignore_unused(fields, patch_type, level, dt, dive_cleaning);
    WARPX_ABORT_WITH_MESSAGE(
        "PML only implemented in Cartesian geometry.");
#else
```

这是一条功能边界：当前读到的 FDTD PML kernel 不能拿来解释 RZ 或 spherical 几何的 PML。进入 Cartesian 后，B 的 split update 仍然复用 Yee/Nodal/CKC 的 `T_Algo::UpwardD*` 差分模板。例如 `Bx` 的更新为：

```cpp
Bx(i, j, k, PMLComp::xz) += dt * (
    T_Algo::UpwardDz(Ey, coefs_z, n_coefs_z, i, j, k, PMLComp::yx)
  + T_Algo::UpwardDz(Ey, coefs_z, n_coefs_z, i, j, k, PMLComp::yz)
  + UpwardDz_Ey_yy);

Bx(i, j, k, PMLComp::xy) -= dt * (
    T_Algo::UpwardDy(Ez, coefs_y, n_coefs_y, i, j, k, PMLComp::zx)
  + T_Algo::UpwardDy(Ez, coefs_y, n_coefs_y, i, j, k, PMLComp::zy)
  + UpwardDy_Ez_zz);
```

它仍对应普通 Maxwell 方程中的

$$
\partial_tB_x=\partial_zE_y-\partial_yE_z,
$$

但 `E_y` 和 `E_z` 已经被拆成 PML components，所以源码必须把相关 components 求和。`UpwardDz_Ey_yy` 和 `UpwardDy_Ez_zz` 只在开启 PML divergence cleaning 时加入。

`EvolveEPML()` 做相反的 curl(B) 更新，并在 PML 中可选加入 `F` 修正和粒子电流项：

```cpp
Ex(i, j, k, PMLComp::xz) -= c2 * dt * (
    T_Algo::DownwardDz(By, coefs_z, n_coefs_z, i, j, k, PMLComp::yx)
  + T_Algo::DownwardDz(By, coefs_z, n_coefs_z, i, j, k, PMLComp::yz) );
Ex(i, j, k, PMLComp::xy) += c2 * dt * (
    T_Algo::DownwardDy(Bz, coefs_y, n_coefs_y, i, j, k, PMLComp::zx)
  + T_Algo::DownwardDy(Bz, coefs_y, n_coefs_y, i, j, k, PMLComp::zy) );
```

这对应

$$
\partial_tE_x=c^2(\partial_yB_z-\partial_zB_y),
$$

只是每个参与 curl 的磁场分量也以 split components 形式存储。若 `pml_has_particles` 为真，`EvolveEPML.cpp` 还会读取 `pml_j_fp/cp` 并调用 `push_ex_pml_current` 等 helper，使 PML 中传播的粒子电流进入电场更新。

最后，`EvolveFPML()` 更新 PML divergence-cleaning 标量：

```cpp
F(i, j, k, PMLComp::x) += dt * (
      T_Algo::DownwardDx(Ex, coefs_x, n_coefs_x, i, j, k, PMLComp::xx)
    + T_Algo::DownwardDx(Ex, coefs_x, n_coefs_x, i, j, k, PMLComp::xy)
    + T_Algo::DownwardDx(Ex, coefs_x, n_coefs_x, i, j, k, PMLComp::xz) );
```

普通区域的 `F` 方程含有 `-\rho/\epsilon_0` 项；当前 PML `F` kernel 只读到 split E 的 divergence 累积。PML 中吸收系数、sigma profile、damping 因子和 current damping 的细节不在这三个 field update 文件中，下一步要继续进入 `BoundaryConditions/PML.cpp` 和 `BoundaryConditions/PML_current.H`。

## 6.3 PML sigma profile、damping 与电流源项

`notes/code-reading/fieldsolver/03-pml-damping-current.md` 已经继续展开 `BoundaryConditions/PML.cpp` 和 `WarpXEvolvePML.cpp`。PML 的吸收 profile 由 `FillLo()` / `FillHi()` 生成：

```cpp
Real offset = static_cast<Real>(glo-i);
p_sigma[i-slo] = fac*(offset*offset);
p_sigma_cumsum[i-slo] = (fac*(offset*offset*offset)/3._rt)/v_sigma;
if (i <= ohi+1) {
    offset = static_cast<Real>(glo-i) - 0.5_rt;
    p_sigma_star[i-sslo] = fac*(offset*offset);
    p_sigma_star_cumsum[i-sslo] = (fac*(offset*offset*offset)/3._rt)/v_sigma;
}
```

对应的 profile 是

$$
\sigma(s)=C s^2,\qquad \int_0^s\sigma(s')\,ds'=\frac{C s^3}{3}.
$$

`SigmaBox::ComputePMLFactorsE/B()` 再把它转成指数阻尼：

```cpp
p_sigma_star_fac[idim][i] = std::exp(-p_sigma_star[idim][i]*dt);
p_sigma_fac[idim][i] = std::exp(-p_sigma[idim][i]*dt);
```

`DampPML_Cartesian()` 在每个 PML tile 上调用 `warpx_damp_pml_ex/ey/ez` 和 `warpx_damp_pml_bx/by/bz`。这些 kernel 根据场的 staggered 位置选择 `sigma_fac` 或 `sigma_star_fac`，对 split components 逐方向相乘。例如 `Exy` 乘 y 方向阻尼，`Exz` 乘 z 方向阻尼；若开启 `do_pml_dive_cleaning`，`Exx` 也乘 x 方向阻尼。

若 PML 中有粒子电流，`push_ex_pml_current()` 会把 `J_x` 按横向 sigma 比例分给 `Exy` 和 `Exz`：

```cpp
alpha_xy = sigjy[k-ylo]/(sigjy[k-ylo]+sigjz[l-zlo]);
alpha_xz = sigjz[l-zlo]/(sigjy[k-ylo]+sigjz[l-zlo]);
Ex(j,k,l,PMLComp::xy) = Ex(j,k,l,PMLComp::xy) - mu_c2_dt  * alpha_xy * jx(j,k,l);
Ex(j,k,l,PMLComp::xz) = Ex(j,k,l,PMLComp::xz) - mu_c2_dt  * alpha_xz * jx(j,k,l);
```

而 `DampJPML()` 使用的是 `sigma_cumsum_fac`，不是场 damping 的 `sigma_fac`：

```cpp
damp_jx_pml(i, j, k, pml_jxfab, sigma_star_cumsum_fac_j_x,
            sigma_cumsum_fac_j_y, sigma_cumsum_fac_j_z,
            xs_lo,y_lo, z_lo);
```

这说明 WarpX 对 PML 电流采用沿吸收层积分后的 damping，而不是简单的局部 `e^{-\sigma\Delta t}`。

最后，`PML::Exchange()` 把 split fields 求和再与常规场交换：

```cpp
MultiFab totpmlmf(pml.boxArray(), pml.DistributionMap(), 1, 0);
MultiFab::LinComb(totpmlmf, 1.0, pml, 0, 1.0, pml, 1, 0, 1, 0);
if (ncp == 3) {
    MultiFab::Add(totpmlmf,pml,2,0,1,0);
}
```

所以 PML 的完整链条是：常规场进入 PML split component，PML 内 curl 更新，乘 sigma damping，split components 求和回填常规边界。只看 `EvolveEPML.cpp` 或只看 `DampPML()` 都不足以说明 PML 的实际边界条件。

## 6.4 非 Cartesian FDTD：RZ、RCYLINDER 与 RSPHERE

`notes/code-reading/fieldsolver/04-noncartesian-fdtd.md` 继续把 FDTD 从 Cartesian 推到 WarpX 的编译几何分支。`FiniteDifferenceSolver.cpp` 中，RZ/RCYLINDER 和 RSPHERE 不走 Cartesian CKC/Nodal 分支，而是只接受 Yee/HybridPIC：

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

cylindrical Yee 的核心算子不是 $\partial_rF$，而是

$$
\frac{1}{r}\frac{\partial(rF)}{\partial r}.
$$

源码中对应：

```cpp
return 1._rt/r * inv_dr*( (r+0.5_rt*dr)*F(i+1,j,k,comp) - (r-0.5_rt*dr)*F(i,j,k,comp) );
```

RZ 的 azimuthal mode 展开使 $\partial_\theta$ 变成 $im$，所以实部/虚部会互相耦合。`EvolveBCylindrical()` 中 `Br` 的高阶 mode 更新为：

```cpp
Br(i, j, 0, 2*m-1) += dt*(
    T_Algo::UpwardDz(Etheta, coefs_z, n_coefs_z, i, j, 0, 2*m-1)
    - m * Ez(i, j, 0, 2*m  )/r );
Br(i, j, 0, 2*m  ) += dt*(
    T_Algo::UpwardDz(Etheta, coefs_z, n_coefs_z, i, j, 0, 2*m  )
    + m * Ez(i, j, 0, 2*m-1)/r );
```

轴上 $r=0$ 不能直接除以 r，源码显式使用正则化条件。例如 `Etheta(r=0,m=1)=-i Er(r=0,m=1)`：

```cpp
Etheta(i,j,0,2*m-1) =  Er(i,j,0,2*m  );
Etheta(i,j,0,2*m  ) = -Er(i,j,0,2*m-1);
```

这类条件是 RZ FDTD 的物理核心：轴上的场必须满足坐标正则性，而不是普通网格差分的延伸。

RSPHERE 使用 spherical operator：

$$
\frac{1}{r^2}\frac{\partial(r^2F)}{\partial r}.
$$

源码为：

```cpp
return 1._rt/(r*r) * inv_dr*( rph*rph*F(i,j,k,comp) - rmh*rmh*F(i-1,j,k,comp) );
```

对应的 `EvolveFSpherical()` 在轴上用 `6*Er/dr` 正则化：

```cpp
F(i, j, 0, 0) += dt * (
    - rho(i, j, 0, rho_shift) * inv_epsilon0
     + 6._rt*Er(i, j, 0, 0)/dr);
```

这说明非 Cartesian FDTD 不能作为 Cartesian FDTD 的坐标名替换来讲；必须把 metric factors、mode coupling 和 axis regularization 都写入公式和源码解读。

## 6.5 PSATD 谱求解主流程

`notes/code-reading/fieldsolver/05-psatd-spectral-flow.md` 开始进入 PSATD。理论上，PSATD 把 Maxwell 方程写到 Fourier 空间：

$$
\frac{\partial\widetilde{\mathbf E}}{\partial t}
=i\mathbf k\times\widetilde{\mathbf B}-\widetilde{\mathbf J},
\qquad
\frac{\partial\widetilde{\mathbf B}}{\partial t}
=-i\mathbf k\times\widetilde{\mathbf E}.
$$

在一个时间步内对线性部分解析积分，得到含

$$
C=\cos(k\Delta t),\qquad S=\sin(k\Delta t)
$$

的更新式。源码入口是 `WarpX::PushPSATD()`：

```cpp
// FFT of E and B
PSATDForwardTransformEB();

// FFT of F and G
if (WarpX::do_dive_cleaning) { PSATDForwardTransformF(); }
if (WarpX::do_divb_cleaning) { PSATDForwardTransformG(); }

// Update E, B, F, and G in k-space
PSATDPushSpectralFields();

// Inverse FFT of E, B, F, and G
PSATDBackwardTransformEB();
```

在此之前，`PushPSATD()` 会根据 `current_correction`、Vay deposition、periodic single box 和 mesh refinement 分支处理 `J/rho`：

```cpp
PSATDForwardTransformJ(current_fp_string, current_cp_string);
PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 0, rho_old);
PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 1, rho_new);

::PSATDCurrentCorrection(finest_level, spectral_solver_fp, spectral_solver_cp);

PSATDBackwardTransformJ(current_fp_string, current_cp_string);
```

`SpectralSolver` 本身只负责建立 k-space、spectral field storage 和选择具体算法：

```cpp
const SpectralKSpace k_space= SpectralKSpace(realspace_ba, dm, dx);

m_spectral_index = SpectralFieldIndex(
    update_with_rho, fft_do_time_averaging, time_dependency_J, time_dependency_rho,
    dive_cleaning, divb_cleaning, pml);
```

```cpp
void SpectralSolver::pushSpectralFields(){
    algorithm->pushSpectralFields( field_data );
}
```

所以真正的 PSATD 更新在 `PsatdAlgorithm*` 子类中。以 `PsatdAlgorithmGalilean.cpp` 为例，标准 PSATD 也通过 `v_galilean=0` 的情形进入同一套形式：

```cpp
fields(i,j,k,Idx.Ex) = T2 * C * Ex_old
                       + I * c2 * T2 * S_ck * (ky * Bz_old - kz * By_old)
                       + X4 * Jx - I * (X2 * rho_new - T2 * X3 * rho_old) * kx;
```

`(ky*Bz-kz*By)` 是谱空间 curl 的 x 分量。`X1/X2/X3/X4/T2` 是下一节需要展开的系数，它们把标准 PSATD、Galilean PSATD、是否使用 rho、是否时间平均等分支折叠成统一更新式。

PSATD 还必须处理 staggered 网格位置。`SpectralFieldData::ForwardTransform()` 在实空间场不是 nodal 时乘相位因子：

```cpp
if (!is_nodal_0) { spectral_field_value *= shift0_arr[i]; }
if (!is_nodal_1) { spectral_field_value *= shift1_arr[j]; }
if (!is_nodal_2) { spectral_field_value *= shift2_arr[k]; }
```

相位因子来自

```cpp
pshift[i] = amrex::exp( I*sign*pk[i]*0.5_rt*t_dx_idim);
```

即 $e^{\pm ik\Delta x/2}$。这一步是把 Yee staggered 数据映射到谱算法假定的位置；没有这一步，谱空间 curl 与实空间场的位置会错半格。

## 6.6 标准/Galilean PSATD 系数和 current correction

`notes/code-reading/fieldsolver/06-psatd-galilean-current-correction.md` 继续展开 `PsatdAlgorithmGalilean.cpp`。标准 PSATD 是 Galilean 实现的 $v_G=0$ 极限；源码中

$$
w_c=\mathbf k_c\cdot\mathbf v_G,\qquad T_2=e^{iw_c\Delta t}.
$$

`w_c` 必须使用 centered modified k：

```cpp
const amrex::Real w_c = kx_c[i]*vg_x +
#if defined(WARPX_DIM_3D)
    ky_c[j]*vg_y + kz_c[k]*vg_z;
#else
    kz_c[j]*vg_z;
#endif
```

基础振荡系数是：

```cpp
C(i,j,k) = std::cos(om_s * dt);

if (om_s != 0.)
{
    S_ck(i,j,k) = std::sin(om_s * dt) / om_s;
}
else
{
    S_ck(i,j,k) = dt;
}

T2(i,j,k) = theta_c * theta_c;
```

其中 `om_s = c*|k_s|`。`X1-X4` 把电流和电荷项折叠进统一更新式；源码显式处理 $k=0$ 和 $w_c=0$ 极限，避免除零。

current correction 的源码与官方参数文档逐项对应。标准分支为：

```cpp
fields(i,j,k,Idx.Jx_mid) = Jx - (k_dot_J - I * (rho_new - rho_old) / dt)
    * kx / (k_norm * k_norm);
```

这正是

$$
\widehat{\mathbf J}_{corr}
=\widehat{\mathbf J}
-\left(\mathbf k\cdot\widehat{\mathbf J}
-i\frac{\widehat\rho^{n+1}-\widehat\rho^n}{\Delta t}\right)\frac{\mathbf k}{k^2}.
$$

Galilean 分支为：

```cpp
const Complex rho_old_mod = rho_old * amrex::exp(I * k_dot_vg * dt);
const Complex den = 1._rt - amrex::exp(I * k_dot_vg * dt);

fields(i,j,k,Idx.Jx_mid) = Jx - (k_dot_J - k_dot_vg * (rho_new - rho_old_mod) / den)
    * kx / (k_norm * k_norm);
```

这里 `rho_old_mod` 是 $\rho^n\theta^2$，`den` 是 $1-\theta^2$。因此 current correction 的目的不是平滑电流，而是投影掉违反谱空间连续性方程的纵向误差，使修正后的电流与 `rho_old/rho_new` 相容。

## 6.7 PSATD-JRhom：多次源项沉积与一阶/二阶谱更新

`notes/code-reading/fieldsolver/07-psatd-jrhom.md` 把 PSATD-JRhom 从主循环到谱算法做了第一轮完整精读。物理上，JRhom 处理的是一个 PIC 时间步内 `J` 和 `rho` 不一定满足“电流常量、电荷线性”的假设。WarpX 使用 `psatd.JRhom` 字符串指定时间依赖：

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

第一个字符控制 `J`，第二个字符控制 `rho`，后续数字控制子区间数 `m`。例如 `CL1` 是标准 PSATD 源项假设，`LQ4` 表示 `J` 分段线性、`rho` 分段二次，并把大时间步拆成 4 个子区间。谱求解器分配时会把内部时间步改成

```cpp
amrex::Real solver_dt = dt[lev];
if (WarpX::m_JRhom) { solver_dt /= static_cast<amrex::Real>(WarpX::m_JRhom_subintervals); }
```

因此 `PsatdAlgorithmJRhom*` 内部看到的是 $\delta t=\Delta t/m$。

JRhom 的外层 PIC loop 不走普通 `PushPSATD()`。它先推进粒子，但跳过普通沉积：

```cpp
// Push particle from x^{n} to x^{n+1}
//               from p^{n-1/2} to p^{n+1/2}
const bool skip_deposition = true;
PushParticlesandDeposit(cur_time, skip_deposition);
```

随后在每个子区间按时间依赖类型重新沉积 `J/rho`：

```cpp
const int n_deposit = WarpX::m_JRhom_subintervals;
const amrex::Real sub_dt = dt[0] / static_cast<amrex::Real>(n_deposit);
const int n_loop = (WarpX::fft_do_time_averaging) ? 2*n_deposit : n_deposit;

for (int i_deposit = 0; i_deposit < n_loop; i_deposit++)
{
    if (time_dependency_J != TimeDependencyJ::Constant) { PSATDMoveJNewToJOld(); }

    const amrex::Real t_deposit_current = (time_dependency_J == TimeDependencyJ::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;

    const amrex::Real t_deposit_charge = (time_dependency_rho == TimeDependencyRho::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;
```

线性依赖使用子区间端点，常量和二次依赖使用中点；二次依赖还会额外沉积一次，形成 `old/mid/new` 三个时间层：

```cpp
if (time_dependency_J == TimeDependencyJ::Quadratic)
{
    PSATDMoveJNewToJMid();
    mypc->DepositCurrent( m_fields.get_mr_levels_alldirs(current_string, finest_level),  dt[0], t_deposit_current + 0.5_rt*sub_dt);
    SyncCurrent("current_fp");
    PSATDForwardTransformJ("current_fp", "current_cp");
}
```

谱数组的 `old/mid/new` component 由 `SpectralFieldIndex` 分配：

```cpp
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

二阶 JRhom kernel 把这些时间层组合成多项式系数：

```cpp
const Complex a_jx = (J_quadratic) ? (Jx_new - 2._rt * Jx_mid + Jx_old) : 0._rt;
const Complex b_jx = (J_linear || J_quadratic) ? (Jx_new - Jx_old) : 0._rt;
const Complex c_jx = (J_linear) ? (Jx_new + Jx_old)/2._rt : Jx_mid;

const Complex a_rho = (rho_quadratic) ? (rho_new - 2._rt * rho_mid + rho_old) : 0._rt;
const Complex b_rho = (rho_linear || rho_quadratic) ? (rho_new - rho_old) : 0._rt;
const Complex c_rho = (rho_linear) ? (rho_new + rho_old)/2._rt : rho_mid;
```

这对应每个子区间内

$$
\widetilde{\mathbf J}(t)=\mathbf a_J\tau^2+\mathbf b_J\tau+\mathbf c_J,
\qquad
\widetilde\rho(t)=a_\rho\tau^2+b_\rho\tau+c_\rho.
$$

电场更新式以 `Ex` 为例：

```cpp
fields(i,j,k,Idx.Ex) = C * Ex_old
    + I * c2 * S_ck * (ky * Bz_old - kz * By_old)
    + Y3 * a_jx + Y2 * b_jx - S_ck/ep0 * c_jx
    + I * c2 * kx * sum_rho;
```

这里 `(ky*Bz-kz*By)` 是谱空间 curl(B)，`Y3/Y2/S_ck` 分别积分二次、一次和常量电流源项，`sum_rho` 则是电荷密度多项式带来的纵向修正。

磁场更新式同样含有 `k x J` 的多项式积分：

```cpp
fields(i,j,k,Idx.Bx) = C * Bx_old
    - I * S_ck * (ky * Ez_old - kz * Ey_old)
    - I * Y1 * (ky * a_jz - kz * a_jy)
    + I * Y5 * (ky * b_jz - kz * b_jy)
    + I * Y4 * (ky * c_jz - kz * c_jy );
```

JRhom 的支持边界也必须写清楚：源码禁止 Vay deposition 与 JRhom 组合，默认关闭 JRhom current correction，并禁止 Galilean PSATD：

```cpp
if (current_deposition_algo == CurrentDepositionAlgo::Vay) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        m_JRhom == false,
        "Vay deposition not implemented with JRhom algorithm");
}

if (m_JRhom) { current_correction = false; }
```

```cpp
if (m_JRhom)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        v_galilean_is_zero,
        "PSATD-JRhom algorithm not implemented with Galilean PSATD"
    );
}
```

所以 JRhom 不是“普通 PSATD 上再加一个系数表”，而是重排了源项采样和谱推进：粒子先完整推进，源项在多个相对时刻沉积，谱场按 `old/mid/new` 保存源项时间层，最后在每个子区间用解析积分推进 `E/B/F/G`。

## 6.8 RZ PSATD：Hankel transform、azimuthal modes 与 `Ep/Em`

`notes/code-reading/fieldsolver/08-psatd-rz-hankel.md` 进入 RZ spectral solver。RZ PSATD 不能理解成“二维 PSATD”。它使用 azimuthal mode decomposition：

$$
F(r,z,\theta)=\sum_m \Re\left(F_m(r,z)e^{im\theta}\right),
$$

并且每个实空间 MultiFab 的 component 数为

$$
n_\mathrm{comps}=2n_\mathrm{modes}-1.
$$

源码中：

```cpp
utils::parser::queryWithParser(pp_warpx, "n_rz_azimuthal_modes", n_rz_azimuthal_modes);
WARPX_ALWAYS_ASSERT_WITH_MESSAGE( n_rz_azimuthal_modes > 0,
    "The number of azimuthal modes (n_rz_azimuthal_modes) must be at least 1");
```

```cpp
ncomps = n_rz_azimuthal_modes*2 - 1;
```

RZ spectral solver 入口选择标准、Galilean 或 PML 算法：

```cpp
if (with_pml) {
        PML_algorithm = std::make_unique<PsatdAlgorithmPmlRZ>(
            k_space, dm, m_spectral_index, n_rz_azimuthal_modes, norder_z, grid_type, dt);
}
if (v_galilean[2] == 0) {
    algorithm = std::make_unique<PsatdAlgorithmRZ>(
        k_space, dm, m_spectral_index, n_rz_azimuthal_modes, norder_z, grid_type, dt,
        update_with_rho, fft_do_time_averaging, time_dependency_J, time_dependency_rho, dive_cleaning, divb_cleaning);
} else {
    algorithm = std::make_unique<PsatdAlgorithmGalileanRZ>(
        k_space, dm, m_spectral_index, n_rz_azimuthal_modes, norder_z, grid_type, v_galilean, dt, update_with_rho);
}
```

RZ 的 `kz` 来自 z 向 FFT，而 `kr` 来自径向 Hankel transform 的 Bessel roots。`SpectralKSpaceRZ` 只构造 z 向 k：

```cpp
const int i_dim = 1;
const bool only_positive_k = false;
k_vec[i_dim] = getKComponent(dm, realspace_ba, i_dim, only_positive_k);
```

Hankel transformer 为每个 mode 建立三套 transform：

```cpp
for (int mode=0 ; mode < m_n_rz_azimuthal_modes ; mode++) {
    dht0[mode] = std::make_unique<HankelTransform>(mode  , mode, m_nr, rmax);
    dhtp[mode] = std::make_unique<HankelTransform>(mode+1, mode, m_nr, rmax);
    dhtm[mode] = std::make_unique<HankelTransform>(mode-1, mode, m_nr, rmax);
}
```

标量用 `dht0`。横向矢量场先组合为

$$
F_p=\frac{F_r-iF_\theta}{2},\qquad
F_m=\frac{F_r+iF_\theta}{2},
$$

源码中对应：

```cpp
// temp_p = (F_r - I*F_t)/2
// temp_m = (F_r + I*F_t)/2
F_r_physical_array(i,j,k,mode_r) = 0.5_rt*(r_real + t_imag);
F_r_physical_array(i,j,k,mode_i) = 0.5_rt*(r_imag - t_real);
F_t_physical_array(i,j,k,mode_r) = 0.5_rt*(r_real - t_imag);
F_t_physical_array(i,j,k,mode_i) = 0.5_rt*(r_imag + t_real);
```

然后分别做 `dhtp/dhtm`：

```cpp
dhtp[mode]->HankelForwardTransform(F_r_physical, mode_r, G_p_spectral, mode_r);
dhtm[mode]->HankelForwardTransform(F_t_physical, mode_r, G_m_spectral, mode_r);
```

所以 `PsatdAlgorithmRZ` 中的 `Ep/Em` 不是 `Ex/Ey`，而是由 `E_r/E_theta` 组合出的谱分量：

```cpp
int const Ep_m = Idx.Ex + Idx.n_fields*mode;
int const Em_m = Idx.Ey + Idx.n_fields*mode;
int const Ez_m = Idx.Ez + Idx.n_fields*mode;
int const Bp_m = Idx.Bx + Idx.n_fields*mode;
int const Bm_m = Idx.By + Idx.n_fields*mode;
int const Bz_m = Idx.Bz + Idx.n_fields*mode;
```

RZ PSATD 的电场更新以 `Ep/Em/Ez` 为变量：

```cpp
fields(i,j,k,Ep_m) = C*Ep_old
            + S_ck*(-c2*I*kr/2._rt*Bz_old + c2*kz*Bp_old - inv_ep0*Jp)
            + 0.5_rt*kr*rho_diff;
fields(i,j,k,Em_m) = C*Em_old
            + S_ck*(-c2*I*kr/2._rt*Bz_old - c2*kz*Bm_old - inv_ep0*Jm)
            - 0.5_rt*kr*rho_diff;
fields(i,j,k,Ez_m) = C*Ez_old
            + S_ck*(c2*I*kr*Bp_old + c2*I*kr*Bm_old - inv_ep0*Jz)
            - I*kz*rho_diff;
```

RZ 的谱散度写成

$$
\nabla\cdot\mathbf E
\rightarrow k_r(E_p-E_m)+ik_zE_z.
$$

源码中 `update_with_rho=0` 时用它重构电荷项：

```cpp
Complex const divE = kr*(Ep_old - Em_old) + I*kz*Ez_old;
Complex const divJ = kr*(Jp - Jm) + I*kz*Jz;

rho_diff = (X2 - X3)*PhysConst::epsilon_0*divE - X2*dt*divJ;
```

RZ current correction 也沿这个谱散度结构投影：

```cpp
Complex const F = - ((rho_new - rho_old)/dt + I*kz*Jz + kr*(Jp - Jm))/k_norm2;

fields(i,j,k,Jp_m) += +0.5_rt*kr*F;
fields(i,j,k,Jm_m) += -0.5_rt*kr*F;
fields(i,j,k,Jz_m) += -I*kz*F;
```

反变换后，RZ 还要按 mode 对称性填充轴下 guard cells：

```cpp
if (i < 0) {
    ii = -i - 1;
    if (icomp == 0) {
        // Mode zero is symmetric
        sign = +1._rt;
    } else {
        // Odd modes are anti-symmetric
        const auto imode = (icomp + 1)/2;
        sign = static_cast<amrex::Real>(std::pow(-1._rt, imode));
    }
}
```

这说明 RZ PSATD 的“正确性”同时依赖三件事：Hankel/Bessel 谱基、`Ep/Em` 横向矢量代数、以及轴上/轴下 mode 对称性。把 Cartesian PSATD 的 `kx,ky,kz` 公式机械删去一个方向，得不到 WarpX 的 RZ 实现。

## 6.9 静电与静磁求解器

绑定精读笔记：`notes/code-reading/fieldsolver/09-electrostatic-magnetostatic.md`。

WarpX 的 electrostatic 路径不再用 Maxwell curl 方程推进场，而是在每一步从当前粒子/流体源项重新解椭圆方程。最基本的 lab-frame 静电模式是

$$
\nabla^2\phi=-\rho/\epsilon_0,\qquad \mathbf E=-\nabla\phi.
$$

如果启用 `labframe-electromagnetostatic`，还会解磁矢势：

$$
\nabla^2\mathbf A=-\mu_0\mathbf J,\qquad \mathbf B=\nabla\times\mathbf A.
$$

如果启用 `relativistic`，WarpX 对每个 species 用平均速度 $\boldsymbol\beta=\langle\mathbf v\rangle/c$ 解修正 Poisson 方程：

$$
\left[\nabla^2-(\boldsymbol\beta\cdot\nabla)^2\right]\phi=-\rho/\epsilon_0,
$$

并按

$$
\mathbf E=-\nabla\phi+\boldsymbol\beta(\boldsymbol\beta\cdot\nabla\phi),
\qquad
\mathbf B=-\frac{1}{c}\boldsymbol\beta\times\nabla\phi
$$

重建场。这个模式不能把所有 species 的电荷先相加，因为不同 species 的平均速度不同。

参数入口在 `WarpX::ReadParameters()`。一旦 `warpx.do_electrostatic` 不是 `none`，Maxwell solver 会被关闭：

```cpp
pp_warpx.query_enum_sloppy("do_electrostatic", electrostatic_solver_id, "-_");
// if an electrostatic solver is used, set the Maxwell solver to None
if (electrostatic_solver_id != ElectrostaticSolverAlgo::None) {
    electromagnetic_solver_id = ElectromagneticSolverAlgo::None;
}
```

这句代码是模型边界：静电 PIC 不传播光波，也不描述激光/辐射传播。它用瞬时 Poisson 解代替全 Maxwell 更新。

solver 对象在 `WarpX::WarpX()` 构造期选择：

```cpp
if ((WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrame)
    || (WarpX::electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic))
{
    m_electrostatic_solver = std::make_unique<LabFrameExplicitES>(nlevs_max);
}
else if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameEffectivePotential)
{
    m_electrostatic_solver = std::make_unique<EffectivePotentialES>(nlevs_max);
}
else
{
    m_electrostatic_solver = std::make_unique<RelativisticExplicitES>(nlevs_max);
}
```

每步入口是 `WarpX::ComputeSpaceChargeField()`。如果 `reset_fields=true`，E/B 先被清零，再由静电/静磁求解器把自洽场加回：

```cpp
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
```

### 6.9.1 Poisson 边界条件

`PoissonBoundaryHandler` 读取 `boundary.potential_lo_x/hi_x/...` 和 `warpx.eb_potential(x,y,z,t)`，再把 field boundary 转成 AMReX linear operator boundary。Multigrid 支持 periodic、PEC/Dirichlet、Neumann；open/PML 会被拒绝：

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

Dirichlet 电势由 `setPhiBC()` 写入 nodal `phi` 的物理边界：

```cpp
if (dirichlet_flag[2*idim] && iv[idim] == domain.smallEnd(idim)){
    phi_arr(i,j,k) = phi_bc_values_lo[idim];
}
if (dirichlet_flag[2*idim+1] && iv[idim] == domain.bigEnd(idim)) {
    phi_arr(i,j,k) = phi_bc_values_hi[idim];
}
```

因此边界电势是解空间上的约束，而不是加到 $\rho$ 的体源项。

### 6.9.2 Lab-frame 静电

`LabFrameExplicitES::ComputeSpaceChargeField()` 先取出 `rho_fp/rho_cp/phi_fp/Efield_fp`，把所有粒子电荷和流体电荷沉积到总 `rho`：

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

随后同步电荷密度：

```cpp
const Vector<std::unique_ptr<MultiFab> > rho_buf(num_levels);
auto & warpx = WarpX::GetInstance();
warpx.SyncRho( rho_fp, rho_cp, amrex::GetVecOfPtrs(rho_buf) );
```

lab-frame 中 `beta=0`，所以 `computeE()` 退化为普通的 `E=-grad(phi)`：

```cpp
const std::array<Real, 3> beta = {0._rt};

setPhiBC(phi_fp, warpx.gett_new(0));

computePhi(rho_fp, phi_fp, beta, self_fields_required_precision,
           self_fields_absolute_tolerance, self_fields_max_iters,
           self_fields_verbosity, is_igf_2d_slices, Efield_fp);
```

### 6.9.3 Relativistic self fields

Relativistic solver 对每个 species 分别求自场。核心差异是先沉积单 species 电荷，再用该 species 的全局平均速度设置 `beta`：

```cpp
bool const local_average = false; // Average across all MPI ranks
std::array<ParticleReal, 3> beta_pr = pc.meanParticleVelocity(local_average);
std::array<Real, 3> beta;
for (int i=0 ; i < static_cast<int>(beta.size()) ; i++) {
    beta[i] = beta_pr[i]/PhysConst::c; // Normalize
}
```

然后用 species 自己的 self-field solver 参数求势并加场：

```cpp
computePhi( amrex::GetVecOfPtrs(rho), amrex::GetVecOfPtrs(phi),
            beta, pc.self_fields_required_precision,
            pc.self_fields_absolute_tolerance, pc.self_fields_max_iters,
            pc.self_fields_verbosity, is_igf_2d_slices);

computeE( Efield_fp, amrex::GetVecOfPtrs(phi), beta );
computeB( Bfield_fp, amrex::GetVecOfPtrs(phi), beta );
```

`computeE()` 的 nodal 3D `Ex` 代码正是 $(\beta_i\beta_j-\delta_{ij})\partial_j\phi$：

```cpp
Ex_arr(i,j,k) +=
    +(beta_x*beta_x-1._rt)*0.5_rt*inv_dx*(phi_arr(i+1,j  ,k  )-phi_arr(i-1,j  ,k  ))
    + beta_x*beta_y       *0.5_rt*inv_dy*(phi_arr(i  ,j+1,k  )-phi_arr(i  ,j-1,k  ))
    + beta_x*beta_z       *0.5_rt*inv_dz*(phi_arr(i  ,j  ,k+1)-phi_arr(i  ,j  ,k-1));
```

`computeB()` 在 `beta=0` 时立即返回；否则按 $-\boldsymbol\beta\times\nabla\phi/c$ 生成磁场：

```cpp
if ((beta[0] == 0._rt) && (beta[1] == 0._rt) && (beta[2] == 0._rt)) { return; }
```

```cpp
Bx_arr(i,j,k) += PhysConst::inv_c * (
    -beta_y*inv_dz*0.5_rt*(phi_arr(i,j  ,k+1)-phi_arr(i,j  ,k-1))
    +beta_z*inv_dy*0.5_rt*(phi_arr(i,j+1,k  )-phi_arr(i,j-1,k  )));
```

### 6.9.4 Effective potential

Effective potential solver 把 Poisson 方程改为 variable-coefficient elliptic solve。它先分配 cell-centered `effective_potential_sigma`：

```cpp
fields.alloc_init(
    warpx::fields::FieldType::effective_potential_sigma, /*level=*/ 0,
    convert(rho->boxArray(), IntVect(AMREX_D_DECL(0,0,0))),
    rho->DistributionMap(), 1, IntVect(AMREX_D_DECL(0,0,0)), 1.0_rt
);
```

`ComputeSigma()` 中的核心因子是

$$
\frac{C_{EP}}{4}\omega_{ps}^2\Delta t^2
=\frac{C_{EP}}{4}\frac{q_s n_s}{m_s\epsilon_0}\Delta t^2.
$$

源码写作：

```cpp
auto mult_factor = (
    C_SI * warpx.getdt(lev) * warpx.getdt(lev) / (4._rt * PhysConst::epsilon_0)
);
```

每个 species 对 `sigma` 的贡献为：

```cpp
auto const q = std::abs(pc->getCharge());
auto const mult_factor_pc = mult_factor * q / pc->getMass();

sigma_arr(i, j, k, 0) += time_filter_param * mult_factor_pc * rho_cc;
```

最后调用专门的 variable-coefficient solver：

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

### 6.9.5 Magnetostatic vector Poisson

`labframe-electromagnetostatic` 的磁场不是 Maxwell curl 更新，而是解 vector Poisson 后取 curl。入口明确要求无 mesh refinement：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(this->max_level == 0,
    "Magnetostatic solver not implemented with mesh refinement.");

AddMagnetostaticFieldLabFrame();
```

它先清零并沉积所有 species 的电流：

```cpp
for (int lev = 0; lev <= max_level; lev++) {
    for (int dim=0; dim < 3; dim++) {
        m_fields.get(FieldType::current_fp, Direction{dim}, lev)->setVal(0.);
    }
}

for (int ispecies=0; ispecies<mypc->nSpecies(); ispecies++){
    WarpXParticleContainer& species = mypc->GetParticleContainer(ispecies);
    if (!species.do_not_deposit) {
        species.DepositCurrent(
            m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
            dt[0], 0.);
    }
}
```

再同步电流，设置矢势边界，调用 vector Poisson solver：

```cpp
SyncCurrent("current_fp");

setVectorPotentialBC(m_fields.get_mr_levels_alldirs(FieldType::vector_potential_fp_nodal, finest_level));

computeVectorPotential(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    m_fields.get_mr_levels_alldirs(FieldType::vector_potential_fp_nodal, finest_level),
    magnetostatic_solver_required_precision, magnetostatic_solver_absolute_tolerance,
    magnetostatic_solver_max_iters, magnetostatic_solver_verbosity
);
```

矢势的 PEC 边界条件按分量区分：法向 `A_n` 用 Neumann，切向 `A_t` 用 Dirichlet：

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

Poisson solve 后，`EBCalcBfromVectorPotentialPerLevel::operator()` 从 MLMG 取每个 `A` 分量的梯度，再按 curl 组合成 `B`。例如 `Ax` 对 `By/Bz` 的贡献：

```cpp
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

逐项合起来就是

$$
B_x=\partial_y A_z-\partial_z A_y,\qquad
B_y=\partial_z A_x-\partial_x A_z,\qquad
B_z=\partial_x A_y-\partial_y A_x.
$$

因此这一路径的正确性依赖三个环节同时一致：电流沉积/同步给出正确 `J`，vector Poisson 解出符合边界条件的 `A`，post callback 再把 `curl A` 插值到 `Bfield_fp` 的实际 staggering。

## 6.10 Hybrid PIC：广义 Ohm 定律与 B 场 RK 子步

`notes/code-reading/fieldsolver/12-hybrid-pic-model-deep-dive.md` 把 WarpX 的 kinetic-fluid hybrid solver 从模型参数到 kernel 做了第一轮深拆。这个路径不使用 Maxwell-Ampere 方程推进电场，而是把电子视为流体、离子仍作为 kinetic particles，用广义 Ohm 定律求电场：

$$
\mathbf E =
-\frac{1}{e n_e}\left(\mathbf J_e\times\mathbf B+\nabla P_e\right)
+\eta\mathbf J-\eta_h\nabla^2\mathbf J.
$$

其中准中性假设给出 `rho = e n_e`，总电流由忽略位移电流后的 Ampere 定律给出：

$$
\mu_0\mathbf J=\nabla\times\mathbf B.
$$

电子电流不直接沉积，而是由

$$
\mathbf J_e=\mathbf J-\mathbf J_i-\mathbf J_{\rm ext}
$$

得到。源码里的 `Jfield` 已经在 `CalculatePlasmaCurrent()` 阶段扣除了外部电流，所以 Ohm kernel 中只显式出现 `J - Ji`。

### 6.10.1 参数与辅助场

`HybridPICModel` 保存 hybrid solver 的所有模型参数和辅助场接口：

```cpp
class HybridPICModel
{
public:
    HybridPICModel ();
    void ReadParameters ();
    void AllocateLevelMFs (... ) const;
    void InitData (const ablastr::fields::MultiFabRegister& fields);
    void GetCurrentExternal ();
    void CalculatePlasmaCurrent (... ) const;
    void HybridPICSolveE (... ) const;
    void BfieldEvolveRK (... );
    void FieldPush (... );
    void CalculateElectronPressure () const;
```

它要求用户指定电子温度，并在非等温多方闭合时要求 `n0_ref`：

```cpp
utils::parser::queryWithParser(pp_hybrid, "gamma", m_gamma);
if (!utils::parser::queryWithParser(pp_hybrid, "elec_temp", m_elec_temp)) {
    Abort("hybrid_pic_model.elec_temp must be specified when using the hybrid solver");
}
const bool n0_ref_given = utils::parser::queryWithParser(pp_hybrid, "n0_ref", m_n0_ref);
if (m_gamma != 1.0 && !n0_ref_given) {
    Abort("hybrid_pic_model.n0_ref should be specified if hybrid_pic_model.gamma != 1");
}
```

电子温度从 eV 转成 J 后参与压力计算：

```cpp
// convert electron temperature from eV to J
m_elec_temp *= PhysConst::q_e;
```

Hybrid PIC 需要额外场来存储电子压强、时间插值用的 `rho/J_i`、Ampere 电流和外部电流：

```cpp
fields.alloc_init(FieldType::hybrid_electron_pressure_fp,
    lev, amrex::convert(ba, rho_nodal_flag),
    dm, ncomps, ngRho, 0.0_rt);

fields.alloc_init(FieldType::hybrid_rho_fp_temp,
    lev, amrex::convert(ba, rho_nodal_flag),
    dm, ncomps, ngRho, 0.0_rt);

fields.alloc_init(FieldType::hybrid_current_fp_plasma, Direction{0},
    lev, amrex::convert(ba, jx_nodal_flag),
    dm, ncomps, ngJ, 0.0_rt);
```

`InitData()` 还会记录 `J/B/E` 的 index type。这个细节决定 `HybridPICSolveE.cpp` 里每个物理量如何从自身 staggering 插值到 `Ex/Ey/Ez` 的位置：

```cpp
amrex::IntVect Jx_stag = fields.get(FieldType::current_fp, Direction{0}, 0)->ixType().toIntVect();
amrex::IntVect Bx_stag = fields.get(FieldType::Bfield_fp, Direction{0}, 0)->ixType().toIntVect();
amrex::IntVect Ex_stag = fields.get(FieldType::Efield_fp, Direction{0}, 0)->ixType().toIntVect();

Jx_IndexType[idim] = Jx_stag[idim];
Bx_IndexType[idim] = Bx_stag[idim];
Ex_IndexType[idim] = Ex_stag[idim];
```

### 6.10.2 顶层 field update

Hybrid field update 的主入口是 `WarpX::HybridPICEvolveFields()`。它目前硬性限制为单 level：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    finest_level == 0,
    "Ohm's law E-solve only works with a single level.");
```

进入这个函数时，粒子已经被推到 `x^{n+1}`。接着沉积 `rho^{n+1}` 和 `J_i^{n+1/2}`：

```cpp
// The particles have now been pushed to their t_{n+1} positions.
// Perform charge deposition at t_{n+1} and current deposition at t_{n+1/2}.
HybridPICDepositRhoAndJ();

// Get the external current
m_hybrid_pic_model->GetCurrentExternal();
```

因为上一步末尾保存了 `rho^n` 和 `J_i^{n-1/2}`，源码可以构造中间时间层。`J_i^n` 由两侧半步平均得到：

```cpp
MultiFab::LinComb(
    *current_fp_temp[lev][idim],
    0.5_rt, *current_fp_temp[lev][idim], 0,
    0.5_rt, *m_fields.get(FieldType::current_fp, Direction{idim}, lev), 0,
    0, 1, current_fp_temp[lev][idim]->nGrowVect()
);
```

`rho^{n+1/2}` 同样由 `rho^n` 和 `rho^{n+1}` 平均：

```cpp
MultiFab::LinComb(
    *rho_fp_temp[lev], 0.5_rt, *rho_fp_temp[lev], 0,
    0.5_rt, *m_fields.get(FieldType::rho_fp, lev), 0, 0, 1,
    rho_fp_temp[lev]->nGrowVect()
);
```

第一个半步用 `E^n` 推 `B^n -> B^{n+1/2}`，第二个半步用 `E^{n+1/2}` 推 `B^{n+1/2} -> B^{n+1}`。最后，为了得到 `E^{n+1}`，代码把 ion current 外推到 `n+1`：

```cpp
MultiFab::LinComb(
    *current_fp_temp[lev][idim],
    -1._rt, *current_fp_temp[lev][idim], 0,
    2._rt, *m_fields.get(FieldType::current_fp, Direction{idim}, lev), 0,
    0, 1, current_fp_temp[lev][idim]->nGrowVect()
);
```

由于此时 `current_fp_temp = J_i^n = 0.5(J_i^{n-1/2}+J_i^{n+1/2})`，上式就是

$$
J_i^{n+1}=\frac32J_i^{n+1/2}-\frac12J_i^{n-1/2}.
$$

### 6.10.3 Ampere 电流与 Ohm kernel

每个 B 场 RK stage 都通过 `FieldPush()` 闭合一次 `B -> J -> E -> B`：

```cpp
// Calculate J = curl x B / mu0 - J_ext
CalculatePlasmaCurrent(Bfield, eb_update_E);
// Calculate the E-field from Ohm's law
HybridPICSolveE(Efield, Jfield, Bfield, rhofield, eb_update_E, true);

// Push forward the B-field using Faraday's law
warpx.EvolveB(dt, subcycling_half, t_old);
warpx.FillBoundaryB(ng, nodal_sync);
```

`CalculatePlasmaCurrent()` 先用 finite-difference solver 从 B 计算 Ampere 电流，再减去外部电流：

```cpp
warpx.get_pointer_fdtd_solver_fp(lev)->CalculateCurrentAmpere(
    current_fp_plasma, Bfield, eb_update_E, lev
);

if (m_has_external_current) {
    ablastr::fields::VectorField current_fp_external =
        warpx.m_fields.get_alldirs(FieldType::hybrid_current_fp_external, lev);
    for (int i=0; i<3; i++) {
        current_fp_plasma[i]->minus(*current_fp_external[i], 0, 1, 1);
    }
}
```

`HybridPICSolveECartesian()` 先把 `J`、`J_i` 和 `B` 插值到 nodal grid，并计算 Hall 项：

```cpp
// calculate enE = (J - Ji) x B
enE_nodal(i, j, k, 0) = (
    (jy_interp - jiy_interp) * Bz_interp
    - (jz_interp - jiz_interp) * By_interp
);
enE_nodal(i, j, k, 1) = (
    (jz_interp - jiz_interp) * Bx_interp
    - (jx_interp - jix_interp) * Bz_interp
);
enE_nodal(i, j, k, 2) = (
    (jx_interp - jix_interp) * By_interp
    - (jy_interp - jiy_interp) * Bx_interp
);
```

随后在每个 E 分量所在的 grid staggering 上除以 `rho`，加入压力梯度、阻性和超阻性项。以 `Ex` 为例：

```cpp
const Real rho_val = Interp(rho, nodal, Ex_stag, coarsen, i, j, k, 0);

if (rho_val < rho_floor && holmstrom_vacuum_region) {
    Ex(i, j, k) = 0._rt;
} else {
    const Real grad_Pe = (!solve_for_Faraday) ?
        T_Algo::UpwardDx(Pe, coefs_x, n_coefs_x, i, j, k)
        : 0._rt;

    const auto enE_x = Interp(enE, nodal, Ex_stag, coarsen, i, j, k, 0);
    const auto rho_val_limited = std::max(rho_val, rho_floor);

    Ex(i, j, k) = (enE_x - grad_Pe) / rho_val_limited;
}
```

`solve_for_Faraday` 是一个重要分支：如果这个 E 只用于更新 B，则 `curl(grad Pe)=0`，压力梯度对 Faraday 更新没有贡献，所以源码跳过它；如果最终要求输出 `E^{n+1}`，才把纵向压力项加回。

阻性和超阻性只在 `solve_for_Faraday=true` 时加入：

```cpp
Ex(i, j, k) += eta(rho_val, jtot_val) * Jx(i, j, k);

auto nabla2Jx = T_Algo::Dxx(Jx, coefs_x, n_coefs_x, i, j, k)
    + T_Algo::Dyy(Jx, coefs_y, n_coefs_y, i, j, k)
    + T_Algo::Dzz(Jx, coefs_z, n_coefs_z, i, j, k);

Ex(i, j, k) -= eta_h(rho_val, btot_val) * nabla2Jx;
```

因此源码完整对应

$$
\eta\mathbf J-\eta_h\nabla^2\mathbf J.
$$

### 6.10.4 电子压力与外部矢势 split field

电子压力闭合是多方形式：

```cpp
static amrex::Real get_pressure (amrex::Real const n0,
                                 amrex::Real const T0,
                                 amrex::Real const gamma,
                                 amrex::Real const rho) {
    return n0 * T0 * std::pow((rho/PhysConst::q_e)/n0, gamma);
}
```

也就是

$$
P_e=n_0T_{e0}\left(\frac{n_e}{n_0}\right)^\gamma.
$$

外部矢势由 `ExternalVectorPotential` 管理。用户提供空间矢势 `A(x,y,z)` 和时间函数 `s(t)`，代码从中构造

$$
\mathbf B_{\rm ext}=s(t)\nabla\times\mathbf A,
\qquad
\mathbf E_{\rm ext}=-\frac{d s}{dt}\mathbf A.
$$

源码用中心差分计算时间因子：

```cpp
const amrex::Real scale_factor_B = m_A_time_scale[i](t);

const amrex::Real sf_l = m_A_time_scale[i](t-0.5_rt*dt);
const amrex::Real sf_r = m_A_time_scale[i](t+0.5_rt*dt);
const amrex::Real scale_factor_E = -(sf_r - sf_l)/dt;
```

然后累加到 hybrid 外部场：

```cpp
AddExternalFieldFromVectorPotential(E_ext[lev], scale_factor_E, A_ext[lev],
    warpx.GetEBUpdateEFlag()[lev]);
AddExternalFieldFromVectorPotential(B_ext[lev], scale_factor_B, curlA_ext[lev],
    warpx.GetEBUpdateBFlag()[lev]);
```

在 `HybridPICEvolveFields()` 中，若启用 split external fields，推进前先从总 B 中减去外部 B，结束时再把外部 E/B 加回。这一点防止 Ohm solver 把外部驱动场误当成自洽 plasma response。

这一路径的实现边界也很明确：目前 field solve 只支持单 level；RZ Ohm solver 只支持 `m=0`；`n_floor` 是除以密度时的硬下限；`holmstrom_vacuum_region` 会在低密度区置零 E 以抑制真空区波动。Hybrid PIC 的正确性不能只检查 `HybridPICSolveE.cpp`，还必须同时检查沉积时间层、Ampere current、RK 子步、外部场分裂和边界填充是否一致。

### 6.10.5 `Fluids/` 与 `HybridPICModel` 不是同一条流体链

这里有一个很容易混淆的边界：WarpX 当前 worktree 里同时存在

- `Source/Fluids/*`
- `FieldSolver/FiniteDifferenceSolver/HybridPICModel/*`

它们都带有“fluid”语义，但职责完全不同。

`HybridPICModel` 是 field solver 内部的电子流体闭合。它不维护一套独立的 species state，也不通过 `WarpXFluidContainer` 推进电子。它做的是：

1. 从 `curl B / \mu_0` 得到总 plasma current；
2. 扣掉外部电流和 kinetic ion current；
3. 用剩下的电子流体电流加上电子压强闭合广义 Ohm 定律，求出 `E`；
4. 再用 Faraday 定律和 RK 子步推进 `B`。

而 `Fluids/` 里的 `MultiFluidContainer -> WarpXFluidContainer` 则是另一条 runtime layer。它真正维护的是每个 fluid species 的 nodal

$$
(N,\; N U_x,\; N U_y,\; N U_z),
$$

并在每个 PIC step 里执行：

1. 从 `Efield_aux/Bfield_aux` gather 主场；
2. 复用粒子侧 `UpdateMomentumHigueraCary(...)` 加 Lorentz source；
3. 用 `AdvectivePush_Muscl()` 做 cold-fluid 守恒更新；
4. 把 `qN` 和 `qNU/\gamma` 再沉积回普通 `rho_fp/current_fp`。

所以 `Fluids/` 更像“额外 cold-fluid species 参与普通场沉积”，而不是“hybrid solver 的电子闭合实现”。这也是为什么：

- `WarpX.cpp` 里 `do_fluid_species` 和 `electromagnetic_solver_id == HybridPIC` 是两套独立 existence gate；
- `Fluids/` 会在 moving window 下整体平移并对新暴露 nodal box 重新 `InitData()`；
- 最直接的 validation 入口是 `langmuir_fluids` 这类 cold-fluid regression，而不是 `ohm_solver_*`。

## 6.11 FieldSolver regression 判据：从 analysis 脚本反读物理检查量

前面各节解释了场求解器的离散方程和源码路径。还需要回答一个实际问题：WarpX 自己怎样判断这些 solver 没有坏掉？答案不只在 `CMakeLists.txt` 里。`Examples/Tests/*/CMakeLists.txt` 告诉我们跑哪些输入文件和 checksum；真正带物理含义的判据在 `analysis*.py` 中。

因此本节只讨论源码/脚本判据，不把本地运行结果混入结论。FieldSolver 相关测试大致分三类：

- 明确 `assert` 物理量：NCI 场能、PSATD Gauss law、静电球 L2 误差、隐式能量守恒、Newton/GMRES 迭代数。
- 半物理半回归：Hybrid Ohm solver 的 RZ normal modes 和 ion beam instability 会比较谱采样或增长率 RMS 的历史值。
- 可视化加 checksum：Landau damping、magnetic reconnection、Cartesian Ohm EM modes、cylinder compression 主要生成物理图像并依靠 checksum 自动发现输出漂移。

### 6.11.1 NCI FDTD：场能增长是否被 corrector 压住

`../warpx/Examples/Tests/nci_fdtd_stability/analysis_ncicorr.py` 的核心检查是读 plotfile 中的 `Ex`、`Ez`、`By`，计算

$$
\mathcal E_{\rm NCI}=\sum_{\rm grid}\left(E_x^2+E_z^2+c^2B_y^2\right).
$$

源码判据是：

```python
use_MR = re.search("nci_correctorMR", fn) is not None

if use_MR:
    energy_corrector_off = 5.0e32
    energy_threshold = 1.0e28
else:
    energy_corrector_off = 1.5e26
    energy_threshold = 1.0e24

ex = ad0["boxlib", "Ex"].v
ez = ad0["boxlib", "Ez"].v
by = ad0["boxlib", "By"].v
energy = np.sum(ex**2 + ez**2 + scc.c**2 * by**2)

assert energy < energy_threshold
```

这条 regression 的输入骨架也值得写清。`inputs_base_2d` 不是空白模板，而是已经固定了：

- 2D periodic drifting plasma；
- `algo.current_deposition = esirkepov`；
- `algo.particle_shape = 3`；
- `warpx.use_filter = 1`；
- `warpx.cfl = 1`；
- `warpx.do_subcycling = 1`；
- 电子和离子都沿漂移方向取无量纲动量 `u_z = 1000`；
- base 层已经打开 `particles.use_fdtd_nci_corr = 1`。

`inputs_test_2d_nci_corrector` 只是把它固定为单层 `amr.max_level = 0`，而 `inputs_test_2d_nci_corrector_mr` 则切到 `amr.max_level = 1` 并用 `warpx.fine_tag_lo/hi` 把整个域提升到 refined level。也就是说，这两条并不是“是否开 corrector”的 AB 对照，而是“同一 corrected drifting-plasma 骨架”在 non-MR 与 MR 配置下的稳定性检查。

还要明确一个当前源码树边界：`analysis_ncicorr.py` 试图用

```python
use_MR = re.search("nci_correctorMR", fn) is not None
```

来切换 non-MR 的 `1e24` 阈值与 MR 的 `1e28` 阈值，但当前 `CMakeLists.txt` 给两条活跃测试传入的参数都写成 `diags/diag1000600`。因此，从可见注册层看，MR 分支并没有被单独显式选通。保守的结论应是：

- non-MR 强断言是直接可见并可证实的；
- MR 变体的验证目标明确是“mesh refinement 下也要压制 NCI”，但 `1e28` 那条阈值分支目前更像 analysis 脚本中的预留区分逻辑，而不是注册参数层已直接证明的独立入口。

这个量不是严格写成 SI 形式的电磁能，而是 NCI 增长指示量。脚本把 corrector 关闭时的 benchmark 能量量级也打印出来，说明测试要捕捉的是“数值 Cherenkov 不稳定性是否被压低很多个数量级”。它对应前面 FDTD `EvolveE/B`、NCI corrector/filter 和边界/同步状态的组合效果，而不是单独验证某一行 curl stencil。

### 6.11.2 NCI PSATD：电场能量比与 Gauss law

PSATD 的 NCI 稳定性测试在 `../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py`。脚本先从 `warpx_used_inputs` 判断维度、current correction、time averaging 和 single-box FFT，然后设置不同 reference energy 与容差。

核心源码是：

```python
energy = np.sum(scc.epsilon_0 / 2 * (Ex**2 + Ey**2 + Ez**2))
err_energy = energy / energy_ref
assert err_energy < tol_energy

if current_correction:
    divE = all_data["boxlib", "divE"].squeeze().v
    rho = all_data["boxlib", "rho"].squeeze().v / scc.epsilon_0
    err_charge = np.amax(np.abs(divE - rho)) / max(np.amax(divE), np.amax(rho))
    assert err_charge < tol_charge
```

这里 `energy_ref` 不是解析电磁能，而是同一测试在不稳定设置下的参考能量。例如 Galilean PSATD case 的参考来自 `psatd.v_galilean=(0,0,0)`，averaged Galilean case 的参考来自关闭 time averaging。判据是

$$
\frac{\sum \epsilon_0|\mathbf E|^2/2}{\mathcal E_{\rm unstable,ref}}
<{\tt tol\_energy}.
$$

如果打开 `psatd.current_correction`，脚本还检查离散 Gauss law：

$$
\epsilon_\rho=
\frac{\|\nabla_h\cdot\mathbf E-\rho/\epsilon_0\|_\infty}
{\max(\|\nabla_h\cdot\mathbf E\|_\infty,\|\rho/\epsilon_0\|_\infty)}
<{\tt tol\_charge}.
$$

这正对应前面 PSATD 章节中的两件事：`PsatdAlgorithmGalilean` 通过移动坐标系降低 NCI；current correction 通过谱空间投影修正 `J`，使更新后的 `E` 与 `rho` 满足 Gauss law。

### 6.11.3 Maxwell hybrid QED：真空修正后的相速度偏移

`../warpx/Examples/Tests/maxwell_hybrid_qed/analysis.py` 不是在检查辐射反作用、光子发射或 Breit-Wheeler 产额，而是在检查 hybrid-QED 修正后的 Maxwell 色散关系。输入文件固定了：

- `warpx.grid_type = collocated`
- `algo.maxwell_solver = psatd`
- `warpx.use_hybrid_QED = 1`
- `warpx.quantum_xi = 1.e-23`

并直接用 parser 外场构造一个叠加在静态背景场 `E_s` 上的高斯包络平面波：

```ini
warpx.Ey_external_grid_function(x,y,z) = "exp(-z**2/L**2)*cos(2*pi*z/wavelength) + Es"
warpx.Bx_external_grid_function(x,y,z)= "-sqrt((1+(12*xi*Es**2)/epsilon0)/(1+(4*xi*Es**2)/epsilon0))*exp(-z**2/L**2)*cos(2*pi*z/wavelength)/clight"
```

analysis 从最终 `Ey(x_mid,z)` 线抽取脉冲峰值位置，进而计算模拟相速度：

```python
EyQED = EyQED_2d[EyQED_2d.shape[0] // 2, :]
z_end = dsQED.domain_left_edge[1].v + np.argmax(EyQED) * dz
phase_velocity_pic = (z_end - z_start) / dsQED.current_time.v
```

然后与输入里同一组 `Es`、`xi` 对应的理论相速度比较：

```python
phase_velocity_theory = scc.c / np.sqrt(
    (1.0 + 12.0 * xi * Es**2 / scc.epsilon_0) / (1.0 + 4.0 * xi * Es**2 / scc.epsilon_0)
)
error_percent = (
    100.0 * np.abs(phase_velocity_pic - phase_velocity_theory) / phase_velocity_theory
)
assert error_percent < 1.25
```

因此它验证的是：

$$
v_\phi^{\rm PIC}
\approx
v_\phi^{\rm hybrid\ QED}
=
\frac{c}{\sqrt{(1+12\xi E_s^2/\epsilon_0)/(1+4\xi E_s^2/\epsilon_0)}}.
$$

这条 test 的定位应当是“field solver / Maxwell hybrid QED / vacuum-dispersion benchmark”，而不是宽泛的“QED processes”。它和第 4 章那类粒子 QED regression 的差别很大：这里没有粒子事件统计，只有带 vacuum-polarization 修正的场传播速度。

### 6.11.4 静电球：解析场 L2 误差与能量守恒

`../warpx/Examples/Tests/electrostatic_sphere/analysis_electrostatic_sphere.py` 检查均匀带电电子球的库仑展开。球半径满足

$$
\ddot r=\frac{a}{r^2},
\qquad
a=\frac{q_eq_{\rm tot}}{4\pi\epsilon_0m_e}.
$$

脚本把解析反函数写成：

```python
def v_exact(r):
    return np.sqrt(q_e * q_tot / (2 * pi * e_mass * epsilon_0) * (1 / r_0 - 1 / r))

def t_exact(r):
    return np.sqrt(r_0**3 * 2 * pi * e_mass * epsilon_0 / (q_e * q_tot)) * (
        np.sqrt(r / r_0 - 1) * np.sqrt(r / r_0)
        + np.log(np.sqrt(r / r_0 - 1) + np.sqrt(r / r_0))
    )

r_end = fsolve(func, r_0)[0]

def E_exact(r):
    return np.sign(r) * (
        q_tot / (4 * pi * epsilon_0 * r**2) * (abs(r) >= r_end)
        + q_tot * abs(r) / (4 * pi * epsilon_0 * r_end**3) * (abs(r) < r_end)
    )
```

然后沿三条坐标轴抽取 WarpX 电场，避开靠近边界的区域，计算相对 L2 误差：

```python
L2_error = np.sqrt(sum((E_exact_grid - E_grid) ** 2)) / np.sqrt(
    sum((E_exact_grid) ** 2)
)

assert L2_error_x < l2_tolerance
assert L2_error_y < l2_tolerance
assert L2_error_z < l2_tolerance
```

普通 case 的 `l2_tolerance=0.05`，`emass_10` case 放宽到 `0.096`。如果粒子 openPMD 诊断里有 `phi`，脚本还检查势能释放和总能量守恒：

```python
assert Ep_f < 0.7 * Ep_i
assert abs((Ek_i + Ep_i) - (Ek_f + Ep_f)) < energy_fraction * (
    Ek_i + Ep_i
)
```

这组判据直接覆盖 `ElectrostaticSolvers` 的 Poisson solve、边界处理、粒子 `phi` 诊断和粒子-场能量一致性。与 NCI 测试不同，它有明确解析解，因此最适合作为静电求解器章节的物理闭环例子。

这里正好可以接回 Birdsall-Langdon 第一分卷 `4-9` 到 `4-10` 的两个老判断。第一，Poisson stencil 的“局部更高阶”不自动意味着整套 PIC 离散系统更准确，因为真正决定误差的是 mover、shape、field differencing 和 solver 合起来的系统合同，而不是某一个局部公式单独最优。第二，在已经用 finite-size particles 和网格差分改写了短程库仑作用之后，场能量更基础的记账式是

$$
\mathrm{ESE} \propto \sum_k \rho_k \phi_k^*
$$

而不是简单把

$$
\sum_k |E_k|^2
$$

当成无条件等价的替代。因为一旦离散系统把 `\rho -> \phi -> E` 的合同改成了 `K^2`、`\kappa`、smoothing 和 staggered differencing 的版本，`|E_k|^2` 与 `\rho_k \phi_k^*` 的比值就会带上额外的离散因子。第 6 章后面遇到 electrostatic sphere、Pierce diode 和其它静电 benchmark 时，应优先把 `rho`、`phi`、field solve 和总能量账本放在同一个检查框架里，而不是只看场图像。

Chapter 8 则把这条判断推进成更系统的 finite-grid 理论：`K(k)`、`\kappa(k)`、`S(k)` 和 alias sum 不是分散在不同实现角落里的“修正项”，而是直接一起进入 grid-modified dielectric function。换句话说，field solver 在 PIC 里不是单独决定色散的；它总是和 particle shape、sampled density、force interpolation 共同定义一条离散色散关系。所以本章讨论 Poisson、spectral solve、smoothing 和 field differencing 时，不能只按“求解器精度”排序，而必须同时追问这些算子会怎样改写 alias branches、Langmuir dispersion 和 warm-plasma damping 的数值边界。

Chapter 9/10 进一步把这条判断分成两半。第一，finite `\Delta t` 也会制造自己的 time aliases，因此 numerical heating 不一定只是 spatial-grid aliases 的副产品；当某条 plasma branch 靠近 `\pi/\Delta t` 一带的时间 alias 时，branch-coupling 本身就能触发高噪声和非物理增热。第二，若想得到 exact energy conservation，关键不是“把 `E` 算得更准”，而是让离散 Poisson 解、`\sum_j \rho_j\phi_j` 场能量账本和粒子受力共享同一套 reciprocity 合同。也正因为如此，energy-conserving 路线和 momentum-conserving 路线不是同一求解器上可自由互换的小选项，而是两套不同的离散系统组织方式：前者优先保证总能量账本，后者更自然地保留零总力/动量结构，而 long-wavelength dispersion、self-force 与 alias errors 则必须另行逐项审查。

Chapter 12 再把这件事推进到统计层。Birdsall 在 `12-3` 到 `12-7` 里说明：PIC 里的 thermal noise、Debye shielding、field correlation 和 numerical heating 不能只被看成“粒子数有限导致的随机噪声”，而应写成带有 `S(k_p)`、`\epsilon(k,\omega)` 和时间 alias comb `\omega_g` 的 fluctuation spectrum。此时 `1/2\,\rho\phi` 又一次成为更基础的能量变量，因为它直接把 `(\rho^2)_{k,\omega}` 通过 `K^2` 接到 field-energy density 上。更关键的是，Birdsall 进一步把 grid effects 写成 effective kinetic collision operator，并用 `H`-theorem 说明：space-time grid 可以在 Maxwellian 本应最大熵的情形下继续制造 entropy，这正是 nonphysical heating、drift drag 和 velocity diffusion 的统一统计图像。因此本章后面凡是谈 Poisson、PSATD、smoothing、Langmuir damping、uniform-plasma noise floor 或 NCI/stability 时，都不该只问“色散关系对不对”，还要追问这套离散合同在 `(\rho^2)_{k,\omega}`、`1/2\,\rho\phi`、drift / diffusion 和 entropy production 这几类观测量上会留下什么数值病灶。

Chapter 13 则把这条统计图像压成了更直接的工程尺度。第一，thermal plasma 的 heating/cooling 不能只按 `N_D` 或 CFL 粗略估；它还显式依赖 `\lambda_D/\Delta x`、`v_t\Delta t/\Delta x`、shape order，以及 mover 自身的 phase error。第二，damped equations of motion 既可能抑制某些高频 branch，也可能通过 nonresonant drag term 制造 nonphysical cooling，所以“总能量下降”并不自动代表数值健康。第三，Hockney 的 2d2v 长时间实验说明：真正有设计价值的量往往不是单独的 collision time `\tau_s` 或 heating time `\tau_H`，而是二者的比值 `\tau_H/\tau_s`，以及它如何沿着 `v_t\Delta t \approx \Delta x/2` 这类 optimum path 随 `\lambda_D/\Delta x` 和 particle shape 改变。也就是说，本章后面只写“某求解器稳定”还不够；更严谨的说法应当是，它把 thermal-plasma 观测窗口放在了多少个 collision times 之前，或者把 nonphysical heating / cooling 推迟到了多久之后。

`Dawson 1983` 对本章的补充则更偏“为什么 electrostatic solver 会自然长成这个样子”。这篇综述不是从 Poisson 方程本身出发，而是先从 finite-size particles 与 coarse-grained density 讲起，然后把 `shape factor -> charge sharing / multipole expansion -> uniform-grid FFT -> Fourier-space Poisson solve -> inverse FFT -> gather back to particle` 写成标准 electrostatic particle-model contract。这样一来，本章讨论 electrostatic / spectral 路线时就不该把 FFT-Poisson 看成孤立求解器技巧，而应把它视为和 particle shape、source representation、field interpolation 同时定义的一整条离散系统。

同一篇综述对 electromagnetic / Darwin 路线也给出了一条很适合保留的高层边界。对 full electromagnetic model，时间步首先受最高频 light mode 与 CFL 限制；主动截断高频 `k` modes 的理由，不只是“算得更快”，而是把弱耦合短波 branch 从建模目标里剔除，从而把时间分辨率留给真正关心的大尺度 collective physics。与此同时，Dawson 还明确批评了 space/time filtering 的根本不对称：空间方向早已有 particle size、`k`-mode truncation 与 Fourier solve 这类成熟手段，但时间方向并没有真正等价的 `\omega`-space filtering，因此 large-time-step / time-averaged routes 仍然只是不同程度的时间滤波妥协。

对 Darwin model，他的判断更直接：这条路线的目标不是更完整地逼近 Maxwell，而是主动删去 displacement current 和不关心的 radiation branch，以便在 Alfvén waves、pinches、ion-cyclotron 这类低频磁化问题上摆脱 light-wave time-step 限制。但它也不能靠“把 Maxwell 少一项再原样 leapfrog”获得，因为直接这样做会因 different-current mutual inductance 而数值不稳定，必须重新组织 transverse-field 方程。这正好说明本章后面遇到的 electrostatic、full EM、implicit、hybrid 或 Darwin-like low-frequency routes，并不是同一个 solver 家族上的小微调，而是针对不同 branch-retention 目标做出的不同模型组织。

`Dawson 1983` 在 numerical stability 小节里又给了一个比 Birdsall 更概括的总结：particle simulation 里的两类典型数值不稳定，本质上都来自 stroboscopic sampling。空间离散会把连续 density spectrum 投影到有限 field Fourier modes 上，从而制造 spatial aliasing；有限 `\Delta t` 则会把高频 branch 重新折叠成低频有效 branch，形成 time aliasing。这样看，finite-size particles、short-wavelength cutoff 和足够小的 time step 并不只是零散经验，而是在分别压制这两类 alias resonance。这个高层说法对本章很有用，因为它把 electrostatic、full EM、PSATD、implicit 和后面所有 time-filtering / space-filtering 取舍都放回了同一组数值病灶。

同一篇综述在 `Tests of the statistical theory of plasmas` 的入口又补了一条很有用的校验边界：对一维 electrostatic sheet model，因其力律简单、无需 grid，可以直接跟踪 point-particle dynamics 到接近 machine accuracy，文中甚至给出长时间能量守恒到 `10^{-12}` 量级的代表性代码。这意味着后面凡是讨论 gridded electrostatic model 的 drag、diffusion、field fluctuations 或 transport coefficients，都不该只拿解析理论作唯一标尺；更基础的比较对象还包括这类无 grid、近 exact 的 particle benchmark。换句话说，Poisson solver、particle shape 和 field interpolation 的数值副作用，很多时候应被理解成“相对于更 fundamental particle model 多引入了多少统计输运偏差”，而不只是“场图看起来是否平滑”。

这条统计理论主线再往下走，还有两个对本章特别实用的测量合同。第一，velocity diffusion 不是一条单斜率直线：`Dawson 1983` 明确把它分成 short-time 的 `\langle \Delta v^2\rangle \propto \tau^2` 阶段和 decorrelation 之后的近线性增长阶段。这意味着 diffusion coefficient 只有在进入 random-impulse regime 后才有稳定解释。第二，thermal field fluctuation 的第一层合同不是整张场图，而是每个 Fourier mode 的 time-averaged modal energy；对 point particles，它满足 `KT/2` 型 equipartition，而 finite-size particle shape 会系统改写这一 fluctuation level。于是本章后面不论讨论 electrostatic noise floor、shape order，还是 smoothing / spectral filtering，都应追问它们怎样改写 modal fluctuation spectrum，而不是只看总场能量是否变小。

再进一步，`Dawson 1983` 还明确说明：thermal-plasma wave diagnostics 至少要分成 power spectrum、time correlation 和 magnetized peak taxonomy 三层。power spectrum 的第一价值是把 Debye-cloud random continuum 和 collective plasma spike 分开，而不是单纯“看哪里有峰”；同时 `\Delta\omega \simeq 1/T` 又说明有限 run length 会直接限制谱结构的可解释性。对有外磁场的体系，谱图里还会出现 Bernstein harmonics、upper-hybrid peak、可动离子时的 ion-cyclotron / lower-hybrid peaks，以及 `\omega=0` 的 convective-cell / charged-flux-tube 结构。于是本章后面讨论噪声底、shape order、smoothing、spectral filtering 或 magnetized fluctuation 时，都不应只写“能量更小/更稳定”，而应继续问：谱是在 continuum 还是 discrete spike 上被改写、相关时间有多长、以及被改写的是哪一类 mode family。

除了均匀带电球，当前本地 examples 里还有一个更偏工程器件侧、但同样有理论对照的静电强基准：`Examples/Physics_applications/pierce_diode/`。它把两平行板间的 1D Pierce diode 直接设到 Child-Langmuir 极限，输入里：

- `warpx.do_electrostatic = labframe`
- `boundary.potential_lo_z = 0`
- `boundary.potential_hi_z = extractor_voltage`
- `ions.flux = J_CL/q_e`

也就是把注入通量直接固定成理论空间电荷限制电流。analysis 随后读取 openPMD 中的 `phi`、`E_z`、`rho`、`j_z` 和离子 `z/u_z`，并把 `phi(z)` 与 `J(z)` 和 Child-Langmuir 理论解比较，要求相对误差都低于 `20%`。

所以 `pierce_diode` 的意义不是泛泛的“静电应用案例”，而是：

- Poisson solver
- fixed-potential conducting boundaries
- 连续粒子注入通量
- space-charge-limited diode steady profile

这四层在同一个 1D 理论基准下被同时闭合。

### 6.11.5 隐式 EM：能量、Gauss law 与求解器迭代数

隐式 solver 的 regression 不是只看场图像，而是直接读 reduced diagnostics。`../warpx/Examples/Tests/implicit/analysis_1d.py` 对 1D Picard case 做总能量漂移检查：

```python
field_energy = np.loadtxt("diags/reducedfiles/field_energy.txt", skiprows=1)
particle_energy = np.loadtxt("diags/reducedfiles/particle_energy.txt", skiprows=1)

total_energy = field_energy[:, 2] + particle_energy[:, 2]
delta_E = (total_energy - total_energy[0]) / total_energy[0]
max_delta_E = np.abs(delta_E).max()

if re.match("test_1d_semi_implicit_picard", test_name):
    tolerance_rel = 2.5e-5
elif re.match("test_1d_theta_implicit_picard", test_name):
    tolerance_rel = 1.0e-14

assert max_delta_E < tolerance_rel
```

`theta_implicit_picard` 要求接近机器精度，`semi_implicit_picard` 允许更大的能量误差。对 exactly energy-conserving implicit EM，`analysis_implicit.py` 还检查 Gauss law RMS：

```python
drho = (rho - epsilon_0 * divE) / e / ne0
drho2_avg = (drho**2).sum() / (nX * nY * nZ)
drho_rms = np.sqrt(drho2_avg)

assert drho_rms < tolerance_rel_charge
```

归一化形式是

$$
\epsilon_{\rm Gauss,rms}=
\left[
\frac{1}{N}\sum_{\mathbf i}
\left(
\frac{\rho_{\mathbf i}-\epsilon_0(\nabla_h\cdot\mathbf E)_{\mathbf i}}
{e n_{e0}}
\right)^2
\right]^{1/2}.
$$

如果只看这些 diagnostics，很容易把 implicit case 误解成“普通场推进外加一个 nonlinear solver 黑箱”。实际上源码里，Gauss law 和能量误差背后还隐含着一条更具体的线性化装配链。`../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp:771-788` 的 `PreLinearSolve()` 在线性求解前会：

```cpp
m_WarpX->DepositMassMatrices();

if (m_use_mass_matrices_jacobian) {
    FinishMassMatrices();
    SaveE();
}

if (m_use_mass_matrices_pc) {
    SyncMassMatricesPCAndApplyBCs();
    const amrex::Real theta_dt = m_theta*m_dt;
    SetMassMatricesForPC( theta_dt );
}
```

这几步不是普通缓存刷新，而是在把粒子响应拆成两套不同对象：

- `current_fp_non_suborbit = J_0`；
- `MassMatrices_X/Y/Z = dJ/dE` 的完整局域响应；
- `MassMatrices_PC` 是从主质量矩阵裁剪、通信、施边界、再乘上 $c^2\mu_0\theta\Delta t$ 后供 preconditioner 使用的近似系数场。

随后 `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp:105-125` 和 `:144-356` 把 linear stage 的电流明确写成

$$
J(E)=J_{\rm suborbit}+J_0+MM\,(E-E_0),
$$

其中 `E_0` 由 `Efield_fp_save` 保存。`ComputeJfromMassMatrices()` 不是抽象矩阵乘法，而是在每个 `Jx/Jy/Jz` 分量的真实 staggered grid 上，对 `Ex/Ey/Ez-E0` 做局域 stencil 卷积。再往下，`../warpx/Source/NonlinearSolvers/MatrixPC.H:300-318`、`JacobiPC.H:286-317` 和 `CurlCurlMLMGPC.H:275-308` 分别把 `MassMatrices_PC` 当成稀疏矩阵条目、局域 Jacobi 权重或 MLMG 的 `beta` 系数来消费。

因此这些 implicit regression 实际同时在检查三层东西：

1. 粒子推进和 `J_0/MM/J_{\rm suborbit}` 分拆是否一致；
2. Jacobian 近似是否真的围绕同一个 `E_0` 线性化；
3. preconditioner 拿到的 `MassMatrices_PC` 是否已经是边界、通信和物理系数都正确处理过的线性算子系数。

再往下一层，Newton 真正送进 GMRES / PETSc 的也不是 `R(U)` 本身，而是

$$
F(U)=U-b-R(U).
$$

`../warpx/Source/NonlinearSolvers/NewtonSolver.H:454-468` 的 `EvalResidual()` 明确写成：

```cpp
m_ops->ComputeRHS( m_R, a_U, a_time, a_iter, false );

// Compute residual: F(U) = U - b - R(U)
a_F.Copy(a_U);
a_F -= m_R;
a_F -= a_b;
```

而 matrix-free Jacobian `../warpx/Source/NonlinearSolvers/JacobianFunctionMF.H:198-234` 再用有限差分构造方向作用：

```cpp
m_Z.linComb( 1.0, m_Y0, eps, a_dU ); // Z = Y0 + eps*dU
m_ops->ComputeRHS(m_R, m_Z, m_cur_time, -1, true );

// dF = dU - (R(Z)-R(Y0))/eps
a_dF.linComb( 1.0, a_dU, eps_inv, m_R0 );
a_dF.increment(m_R,-eps_inv);
```

因此 WarpX 的 JFNK 线性 solve 实际是在做

$$
J_F(U_0)\,\delta U
\approx
\delta U-\frac{R(U_0+\epsilon\delta U)-R(U_0)}{\epsilon},
$$

而不是手工显式装配整块 Jacobian。接着 `WarpX_PETSc.cpp:174-190,300-318` 只把这两个本地回调接进 PETSc：

- `applyMatOp` 调 `a_linop->apply(...)`
- `applyNativePC` 调 `a_linop->precond(...)`

也就是说，PETSc 在这里不是重新定义物理，而只是消费 WarpX 本地已经定义好的 residual、Jacobian 方向作用和 preconditioner apply。

若再切到 `pc_petsc` 这条支线，结构还要再分一次：`../warpx/Source/FieldSolver/ImplicitSolvers/StrangImplicitSpectralEM.cpp:106-123` 里，Strang split implicit spectral EM 的 nonlinear 右端不是 curl-curl 场更新，而是直接

$$
R(U)=-\frac{\Delta t}{2}\mu_0 c^2 J^{n+1/2},
$$

因为 source-free Maxwell 部分已经由前后两次 spectral advance 吃掉。对应源码是：

```cpp
a_RHS.Copy(FieldType::current_fp, warpx::fields::FieldType::None, allow_type_mismatch);
amrex::Real constexpr coeff = PhysConst::c2 * PhysConst::mu0;
a_RHS.scale(-coeff * 0.5_rt*m_dt);
```

而当 PETSc 不走 `PCSHELL`，`WarpX_PETSc.cpp:115-140,342-391` 会在 SNES Jacobian callback 里触发一次 `assemblePCMatrix()`，把 WarpX 本地 preconditioner 近似搬进显式 `Mat P`。这条链的关键不是 Jacobian `A` 被显式装配，而是：

- `A` 仍然是 shell matrix，继续通过 `apply()` 做 matrix-free Jacobian；
- 只有 `P` 被单独装配成 sparse matrix 给 PETSc PC 使用。

对应初始化代码是：

```cpp
KSPSetOperators( m_ksp->obj, this->m_A->obj, this->m_P->obj );
```

`MatrixPC::Assemble()` 则把这块 `P` 写成

$$
P \approx I + \nabla\times(\alpha\nabla\times \cdot) + M_{\rm PC},
$$

其中单位阵、curl-curl stencil 和 `MassMatrices_PC` 都通过 `insertOrAdd()` 累加到同一行的列条目里。也就是说，`pc_petsc` 路径不是“把整个 implicit 求解显式矩阵化”，而只是把 preconditioner 近似显式矩阵化，再交给 PETSc 处理。

若再往下追一层，`../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverDOF.cpp:19-207` 说明 `MatrixPC` 的每一行并不是抽象的 “`Ex/Ey/Ez` 某个分量块”，而是先由 `WarpXSolverDOF` 给 staggered `Efield_fp` 的每个有效点分配一对 `{local,global}` 自由度编号。这个编号还不是对整个 `MultiFab` 无差别铺开，而是先经过 `getFieldDotMaskPointer(...)` 取回的 dot-mask 裁剪：只有 mask 为真的位置才进入线性系统，其他位置的 local/global 槽都保留为 invalid。于是 `MatrixPC::Assemble()` 里的

```cpp
const int ridx_l = dof_arr(i,j,k,0);
const int ridx_g = dof_arr(i,j,k,1);
if (ridx_l < 0) { return; }
```

实际意思就是：这一条矩阵行只对应一个被 dot-mask 接受的 staggered 电场自由度，而 `ridx_l` 决定它在本 rank 的行号，`ridx_g` 决定它在全局稀疏矩阵里的真实列号。

在此基础上，`../warpx/Source/NonlinearSolvers/MatrixPC.H:319-809` 再按几何把这一行写成局域 stencil。共有三层叠加：

1. 先无条件写单位对角 `I`；
2. 若 `thetaDt>0`，再写 `curl(alpha curl .)` 的离散条目；
3. 若 `m_include_mass_matrices=true`，最后再把 `MassMatrices_PC` 的同分量局域窗口写进去。

不同几何的差异主要体现在第二层。1D `Z` 几何下只有横向 `Ex/Ey` 行带三点二阶差分，`Ez` 不带 curl-curl；XZ / RZ 下 `dir=0,2` 不只是本分量三点模板，还会额外跨到横向分量写四个 mixed-derivative 角点条目，对应二维的 $\partial_x\partial_z$ 交叉导数；3D 下每个分量行都会同时耦合到另外两个分量，在两个横向方向上写二阶项和 mixed-derivative 项；RCYLINDER 则没有这类跨分量 mixed derivative，但径向二阶项都显式带有 `1 \pm 0.5/i` 这类圆柱几何因子。所有这些条目都通过 `insertOrAdd()` 合并到同一行里，并逐项乘上 `BC_mask_Edir_arr(...)`，所以边界条件不是事后再修，而是在矩阵条目生成时就已经嵌入 stencil。

而 `BC_mask_Edir_arr(...)` 本身也不是临时判断得到的布尔开关，而是 `../warpx/Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp:190-417` 在 `pc_petsc` 模式下预先分配并写好的系数场。`InitializeCurlCurlBCMasks()` 会根据几何维度先决定每个 `E` 分量需要多少类 mask，然后再把 PEC、PMC、Silver-Mueller、PECInsulator 甚至轴线 `None` 的边界重构系数直接写进这些分量里。所以 `MatrixPC::Assemble()` 在边界上不是“先写标准 stencil，再删条目”，而是直接把已经改写好的离散系数乘进对角项、邻点项和 mixed-derivative 项。

`MassMatrices_PC` 这边也有类似的“前处理后消费”结构。`../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp:470-765` 先按 deposition 算法、shape 和 `mass_matrices_pc_width` 得到完整的 Jacobian mass-matrix 窗口 `m_ncomp_xx/yy/zz`，再裁出只供 preconditioner 使用的 `m_ncomp_pc_xx/yy/zz`。当前这一步只保留 `xx/yy/zz` 三个同分量块，不显式保留 `xy/xz/...` 交叉块；随后 `PreLinearSolve()` 再对 `MassMatrices_PC` 做同步、`J` 边界处理和 `c^2\mu_0\theta\Delta t` 缩放。因此 `MatrixPC::Assemble()` 读到的 `sigma_ii_arr` 已经不是原始粒子沉积结果，而是一个经过窗口裁剪、通信和边界条件处理的 diagonal-block 近似。

最后一步 `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp:342-389,468-490` 说明 `pc_petsc` 的矩阵提交流程是：WarpX 先按本 rank 的 `m_ndofs_l` 创建 `Mat P` 的 local 行块，再由 `assemblePCMatrix()` 从 `MatrixPC` 取回 device 端的行存数组，拷回 host，逐行调用 `MatSetValues()`，最后统一 `MatAssemblyBegin/End`。所以这条链的并行 ownership 仍然完全跟着 `WarpXSolverDOF` 的 local/global 编号走，PETSc 只负责把这些本地行提交拼成全局 sparse matrix，而不重新定义行列的物理含义。

这些实现细节之所以值得追到测试层，是因为 `Examples/Tests/implicit/analysis_petsc_matrix.py` 给了它们一个非常强的硬断言：`inputs_test_2d_curl_curl_petsc_pc`、`inputs_test_rz_curl_curl_petsc_pc` 和 `inputs_test_rcylinder_curl_curl_petsc_pc` 都把 `jacobian.pc_type = pc_petsc` 和 `pc_petsc.type = lu` 放在一起，然后直接要求

```python
assert total_gmres_iters == num_steps
assert total_newton_iters == num_steps
```

也就是每个时间步恰好只需要 1 次 Newton 和 1 次 GMRES。由于 LU 在这里是精确线性求解器，这组 regression 实际不是在检验长期物理解，而是在把 `WarpXSolverDOF` 编号、`MatrixPC::Assemble()` 几何条目、`curl2_BC_mask`、`MassMatrices_PC` 和 `assemblePCMatrix()` 提交链整体当成一个“应当等价于精确 PC”的矩阵装配系统来验收。只要这条断言失败，就更应该先怀疑矩阵条目生成或提交，而不是先怀疑 Maxwell 方程本身。

同一条结构判据现在应明确绑定到三条 benchmark 名，而不该再混成一个笼统的 implicit checksum 桶：

- `test_2d_curl_curl_petsc_pc`
- `test_rz_curl_curl_petsc_pc`
- `test_rcylinder_curl_curl_petsc_pc`

它们共享同一个 `analysis_petsc_matrix.py`，区别只在几何维度和 `MatrixPC` 的装配分支。

相比之下，`Examples/Tests/implicit/analysis_planar_pinch.py` 的验证口径更综合。它一边读取 `newton_solver.txt` 约束平均 `GMRES/Newton` 和 `Newton/step` 迭代数，一边把 `field_energy.txt`、`particle_energy.txt` 和 `poynting_flux.txt` 合成完整能量账本，再用 plotfile 里的 `divE` 与 `rho` 做 Gauss 定律 RMS 误差检查。因此 planar pinch 这一组 regression 不只是 solver smoke test，而是在同时检验：implicit 粒子-场耦合是否保持能量守恒，边界 Poynting flux 是否正确计入能量账本，preconditioner 是否维持可接受效率，以及最终的电荷约束是否仍在机器精度附近。

另外一组经常被忽略但同样关键的 regression 是 `analysis_vandb_jfnk_2d.py` 与 `analysis_vandb_jfnk_2d_cropping.py`。前者把 `theta_implicit_em + newton + Villasenor` 放在 2D periodic thermal plasma 下，只检查两件事：总能量机器精度守恒，以及

$$
\rho-\epsilon_0\nabla\cdot E
$$

的 RMS 误差仍在机器精度附近。它因此更像是对 `ImplicitPushPX.cpp`、`CurrentDeposition.H` 中 Villasenor 路径、以及 `SyncCurrentAndRho()` 后续消费链的专项守恒验收，而不是对 `pc_petsc` 的矩阵装配验收。`inputs_test_2d_theta_implicit_jfnk_vandb_filtered` 只是把 `warpx.use_filter = 1` 打开，然后继续用同一个 analysis，这等价于给 filter 路径加了一条“不能破坏能量守恒和 Gauss 定律”的强回归约束。

`analysis_vandb_jfnk_2d_cropping.py` 则更偏向边界和粒子轨道纠正路径。对应输入把 PEC 场边界、absorbing 粒子边界、`particles.crop_on_PEC_boundary = 1`、`implicit_evolve.particle_suborbits = 1` 和 `algo.current_deposition = villasenor` 同时打开，但 analysis 只保留一个最大局部误差断言：

```python
assert drho_max < tolerance_max_charge
```

这表明它关心的不是闭域总能量，而是：当 particle cropping、PEC 边界、suborbit fallback 和 Villasenor charge-conserving deposition 一起出现时，局部 Gauss 定律还能不能被守住。换句话说，这个 regression 实际把第 5 章的 charge-conserving deposition、第 4 章的 implicit suborbit fallback，以及第 7 章的 PEC/cropping 边界语义绑成了一条共同的验证链。

因此 `Examples/Tests/implicit/` 现在至少应分成五条不同验证线，而不应继续被写成一个统一的 implicit checksum 桶：

1. `analysis_1d.py`
   验证 1D Picard 周期热等离子体的总能量漂移，其中 `semi_implicit_picard` 容差较宽，`theta_implicit_picard` 要求机器精度；
2. `analysis_implicit.py`
   验证周期/对称边界下 exactly energy-conserving implicit EM 的总能量和 Gauss-law RMS 同时达到机器精度；
3. `analysis_2d_psatd.py`
   验证 `strang_implicit_spectral_em + psatd` 的 spectral split 没有破坏总能量守恒；
4. `analysis_planar_pinch.py`
   验证 planar pinch 的能量账本、边界 Poynting flux、平均 Newton/GMRES 迭代数和 Gauss 定律；
5. `analysis_vandb_jfnk_2d.py` 与 `analysis_vandb_jfnk_2d_cropping.py`
   分别验证 JFNK + Villasenor 周期热等离子体守恒，以及 PEC cropping / suborbit fallback 组合下的局部 Gauss-law 约束。

这样看，`inputs_test_2d_theta_implicit_jfnk_vandb_filtered` 和 `inputs_test_2d_theta_implicit_jfnk_vandb_picmi.py` 也都不再是“新的 implicit 物理 benchmark”，而只是把同一条 JFNK/Villasenor 守恒合同分别延伸到 filter 路径和 PICMI front-end 映射路径。

PSATD 这边的验证树也应采用同样的分层，而不是把所有 `nci_psatd_stability` tests 都写成一个统一的 “PSATD / spectral solver” 桶。当前至少应分成三类：

1. `analysis_galilean.py` 族：
   2D/3D/RZ 的普通 Galilean、`current_correction`、`current_correction + periodic_single_box_fft`，以及 averaged Galilean 与其 hybrid-grid 版本。共同判据是把最终电场能量与一个已知不稳定参考值比较，并在 `current_correction=1` 时额外检查 `divE-rho/\epsilon_0` 的相对误差。
2. `analysis_psatd_CC1.py`：
   单独覆盖 `test_3d_uniform_plasma_psatd_JRhom_CC1`，验证 `JRhom = CC1` 配合 `do_divb_cleaning/do_dive_cleaning` 后的 NCI 抑制。
3. checksum-only 基线：
   `test_2d_comoving_psatd_hybrid`、`test_2d_galilean_psatd_hybrid` 和 `test_rz_psatd_JRhom_LL2` 当前都没有独立 analysis，应诚实记录为工作流/输出基线，而不是强稳定性断言。

Planar pinch case 还必须把边界 Poynting flux 纳入能量账本：

```python
dE = Efields + Eplasma + dE_poynting
rel_net_energy = np.abs(dE - dE[0]) / Eplasma
assert max_rel_net_energy < rel_net_energy_tol

assert total_gmres_iters / total_newton_iters < gmres_iters_tol
assert total_newton_iters / num_steps < newton_iters_tol
```

这说明隐式 field solver 的正确性至少有三层：离散能量守恒、Gauss law 约束、非线性/线性求解器效率。PETSc matrix 测试进一步把求解器结构变成硬断言：

```python
assert total_gmres_iters == num_steps
assert total_newton_iters == num_steps
```

当 LU 作为精确求解器或预条件器时，每个时间步只需要 1 次 Newton 和 1 次 GMRES；如果这个断言失败，问题更可能出在矩阵装配、DOF 映射、PETSc bridge 或预条件器，而不是 Maxwell 方程本身。

### 6.11.6 Hybrid Ohm solver：哪些是强判据，哪些只是输出回归

Hybrid Ohm solver 的测试更接近物理 benchmark。`ohm_solver_em_modes/analysis_rz.py` 先对 $E_\theta(r,z,t)$ 做径向 Hankel 投影、轴向 Fourier transform 和时间 Fourier transform：

```python
def transform_spatially(data_for_transform):
    interp = RegularGridInterpolator(
        (info.z, info.r), data_for_transform, method="linear"
    )
    data_interp = interp((zg, rg))

    Fmz = np.einsum("ijkl,kl->ij", proj, data_interp)
    Fmn = fft.fftshift(fft.fft(Fmz, axis=1), axes=1)
    return Fmn

F_kw = fft.fftshift(fft.fft(results, axis=0), axes=0)
```

它会画出 fast/slow branch 和热共振线。显式 assert 只比较谱上固定采样点：

```python
amps = np.abs(F_kw[2, 1, len(kz) // 2 - 2 : len(kz) // 2 + 2])
assert np.allclose(
    amps, np.array([55.65891974, 31.29213566, 70.13683876, 15.395433])
)
```

所以这不是完整色散关系拟合，而是谱结构回归。Ion beam R instability 更接近增长率 benchmark：对 `B_y(z,t)` 做空间 FFT，追踪 `m=4,5,6` 模，并用 Munoz et al. 2018 Fig. 12a 的增长率在 $10<t\Omega_i<40$ 内拟合：

```python
gamma4 = 0.1915611861780133
gamma5 = 0.20087036355662818
gamma6 = 0.17123024228396777
idx = np.where((t_grid > 10) & (t_grid < 40))

A4 = np.exp(np.mean(np.log(np.abs(field_kt[idx, 4] / sim.B0)) - t_points * gamma4))
m4_rms_error = np.sqrt(
    np.mean(
        (np.abs(field_kt[idx, 4] / sim.B0) - A4 * np.exp(t_points * gamma4)) ** 2
    )
)

assert np.isclose(m4_rms_error, 1.546, atol=0.01)
```

脚本注释说明这些容差来自测试创建时的误差，不是从理论直接推导出的严格误差上界。因此失败时不能只看 assert，需要重跑 full benchmark 并人工比较增长到饱和前的理论趋势。

另外几类 Hybrid Ohm 测试没有显式 assert：

- `ohm_solver_ion_Landau_damping/analysis.py` 画出 $|E_z(k_m,t)|/|E_z(k_m,0)|$ 与 $\exp(-\gamma t)$ 的比较，$\gamma$ 来自 Munoz et al. 2018 Fig. 14b 插值。
- `ohm_solver_magnetic_reconnection/analysis.py` 输出重联率

$$
R(t)=\frac{\langle E_y\rangle}{v_A B_0}.
$$

- `ohm_solver_em_modes/analysis.py` 对 Cartesian parallel/perpendicular EM modes 做二维 FFT 谱图。
- `ohm_solver_cylinder_compression` 在 CMake 中 `analysis=OFF`，只有 checksum。

这给本章一个重要限制：Hybrid PIC 章节不能把所有 regression 都写成“物理判据已严格验证”。更准确的说法是：RZ normal modes 和 ion beam instability 有脚本级硬断言；Landau damping、magnetic reconnection、Cartesian EM modes 和 cylinder compression 主要提供物理图像与输出回归线索。

### 6.11.7 本章验证链的结论

综合这些脚本，FieldSolver 的验证链可以这样归纳：

| 求解器路径 | analysis 量 | 主要检查 |
|---|---|---|
| FDTD + NCI corrector | $\sum(E_x^2+E_z^2+c^2B_y^2)$ | 数值 Cherenkov 是否被抑制 |
| PSATD Galilean/current correction | 电场能量比、$\nabla\cdot E-\rho/\epsilon_0$ | NCI 抑制和 Gauss law |
| Electrostatic Poisson | 均匀球解析 $E_r$ 的三轴 L2、粒子势能/动能 | Poisson 场、边界和能量一致性 |
| Implicit EM | 总能量漂移、Gauss RMS、Newton/GMRES 迭代数 | 隐式离散守恒和求解器结构 |
| Hybrid Ohm | 谱采样、增长率 RMS、阻尼/重联图像、checksum | Ohm solver 的物理 benchmark 和输出回归 |

这也决定后续写作方式：场求解器的“正确性”不能只靠某一个 `assert`，而要把连续方程、离散公式、源码时间层、边界/同步和 regression analysis 合起来看。否则，单独贴 `EvolveE.cpp` 的 curl 更新式，仍然无法证明真实 WarpX field solver 在完整 PIC loop 中保持物理一致。
