# PML damping、sigma profile 与 PML 电流精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记接在 `02-fdtd-pml.md` 之后。`02` 只解释了 PML 中的 split-field curl 更新；本笔记解释这些 split fields 如何被真正“吸收”：

- `../warpx/Source/BoundaryConditions/PML.cpp`
- `../warpx/Source/BoundaryConditions/PML.H`
- `../warpx/Source/BoundaryConditions/WarpXEvolvePML.cpp`
- `../warpx/Source/BoundaryConditions/WarpX_PML_kernels.H`
- `../warpx/Source/BoundaryConditions/PML_current.H`
- `../warpx/Source/Initialization/WarpXInitData.cpp`

## 1. 源码层面的 PML 分成三件事

在 FDTD 路径中，PML 不是一个单独的 Maxwell solver，而是三层逻辑叠加：

1. `EvolveBPML/EPML/FPML`：在 split components 上做 curl/div 更新。
2. `DampPML()`：对 PML split components 乘指数阻尼因子。
3. `Exchange()`：在常规场和 PML split fields 的总和之间交换边界/guard 数据。

如果 PML 中允许粒子传播，还有：

1. `CopyJPML()`：把常规区域电流拷到 PML 电流场。
2. `DampJPML()`：对 `pml_j` 乘累积阻尼因子。
3. `push_*_pml_current()`：把 `pml_j` 的电流源项按 sigma 权重分配到 E 的 split components。

因此，PML 的物理效果不在 `EvolveEPML.cpp` 的 curl 一行里，而在 `PML.cpp + WarpXEvolvePML.cpp + PML_current.H` 共同形成的闭环里。

## 2. sigma profile：二次吸收函数与半格点版本

`PML.cpp` 中 `FillLo()` 和 `FillHi()` 生成吸收层两端的 sigma profile。源码位置：`../warpx/Source/BoundaryConditions/PML.cpp:67-118`。

```cpp
void FillLo (Sigma& sigma, Sigma& sigma_cumsum,
                    Sigma& sigma_star, Sigma& sigma_star_cumsum,
                    const int olo, const int ohi, const int glo, Real fac,
                    const amrex::Real v_sigma)
{
    const int slo = sigma.m_lo;
    const int sslo = sigma_star.m_lo;

    const int N = ohi+1-olo+1;
    Real* p_sigma = sigma.data();
    Real* p_sigma_cumsum = sigma_cumsum.data();
    Real* p_sigma_star = sigma_star.data();
    Real* p_sigma_star_cumsum = sigma_star_cumsum.data();
    amrex::ParallelFor(N, [=] AMREX_GPU_DEVICE (int i) noexcept
    {
        i += olo;
        Real offset = static_cast<Real>(glo-i);
        p_sigma[i-slo] = fac*(offset*offset);
        p_sigma_cumsum[i-slo] = (fac*(offset*offset*offset)/3._rt)/v_sigma;
        if (i <= ohi+1) {
            offset = static_cast<Real>(glo-i) - 0.5_rt;
            p_sigma_star[i-sslo] = fac*(offset*offset);
            p_sigma_star_cumsum[i-sslo] = (fac*(offset*offset*offset)/3._rt)/v_sigma;
        }
    });
}
```

```cpp
void FillHi (Sigma& sigma, Sigma& sigma_cumsum,
                    Sigma& sigma_star, Sigma& sigma_star_cumsum,
                    const int olo, const int ohi, const int ghi, Real fac,
                    const amrex::Real v_sigma)
{
    // ...
    amrex::ParallelFor(N, [=] AMREX_GPU_DEVICE (int i) noexcept
    {
        i += olo;
        Real offset = static_cast<Real>(i-ghi-1);
        p_sigma[i-slo] = fac*(offset*offset);
        p_sigma_cumsum[i-slo] = (fac*(offset*offset*offset)/3._rt)/v_sigma;
        if (i <= ohi+1) {
            offset = static_cast<Real>(i-ghi) - 0.5_rt;
            p_sigma_star[i-sslo] = fac*(offset*offset);
            p_sigma_star_cumsum[i-sslo] = (fac*(offset*offset*offset)/3._rt)/v_sigma;
        }
    });
}
```

数学上，这里使用的离散 profile 是

$$
\sigma(s)=C s^2,
$$

其中 $s$ 是离常规区域边界的网格距离。`sigma_star` 是半格点偏移版本，对应 Yee 网格中位于半整数位置的量。`sigma_cumsum` 和 `sigma_star_cumsum` 是解析积分：

$$
\int_0^s C s'^2\,ds'=\frac{C s^3}{3}.
$$

源码中还除以 `v_sigma`，表示电流 damping 使用的坐标/速度尺度归一化。

## 3. `SigmaBox` 保存每个方向的 sigma 与阻尼因子

`SigmaBox` 的构造函数为每个空间方向分配八组数组。源码位置：`PML.cpp:298-330`。

```cpp
for (int idim = 0; idim < AMREX_SPACEDIM; ++idim)
{
    sigma                [idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
    sigma_cumsum         [idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
    sigma_star           [idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
    sigma_star_cumsum    [idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
    sigma_fac            [idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
    sigma_cumsum_fac     [idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
    sigma_star_fac       [idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
    sigma_star_cumsum_fac[idim].resize(sz[idim]+1,std::numeric_limits<Real>::quiet_NaN());
}

Array<Real,AMREX_SPACEDIM> fac;
for (int idim = 0; idim < AMREX_SPACEDIM; ++idim) {
    fac[idim] = 4.0_rt*PhysConst::c/(dx[idim]*static_cast<Real>(delta[idim]*delta[idim]));
}
```

这里的 `fac` 给出

$$
C_i=\frac{4c}{\Delta x_i\,\delta_i^2}.
$$

其中 `delta` 来自输入参数 `warpx.pml_delta`，控制吸收系数增加的特征深度。因为 $s$ 是格点计数，`dx` 把它转换到物理尺度；前面的 $4c$ 是 WarpX 当前采用的经验幅度。

八组数组的用途是：

- `sigma`：整数/节点位置的 $\sigma$。
- `sigma_star`：半格点 staggered 位置的 $\sigma^\*$。
- `sigma_cumsum`：$\sigma$ 的解析积分。
- `sigma_star_cumsum`：$\sigma^\*$ 的解析积分。
- `*_fac`：这些量转换出的指数阻尼因子。

## 4. `ComputePMLFactors*()`：把 sigma 转成指数 damping factor

`ComputePMLFactorsB()` 和 `ComputePMLFactorsE()` 把 profile 转成每个时间步要乘的指数因子。源码位置：`PML.cpp:582-646`。

```cpp
p_sigma_star_fac[idim][i] = std::exp(-p_sigma_star[idim][i]*dt);
p_sigma_star_cumsum_fac[idim][i] = std::exp(-p_sigma_star_cumsum[idim][i]*dx[idim]);
```

```cpp
p_sigma_fac[idim][i] = std::exp(-p_sigma[idim][i]*dt);
p_sigma_cumsum_fac[idim][i] = std::exp(-p_sigma_cumsum[idim][i]*dx[idim]);
```

第一类因子用于场：

$$
F \leftarrow e^{-\sigma\Delta t}F.
$$

第二类 `cumsum_fac` 用于电流 damping：

$$
J \leftarrow e^{-\left(\int\sigma\,ds\right)\Delta x}J.
$$

注意 `MultiSigmaBox::ComputePMLFactorsE/B()` 会缓存 `dt_E` 和 `dt_B`，如果时间步没有变化就直接返回。这避免每步重复生成相同的 GPU 数组。

## 5. `PML::PML()`：PML box 与 MultiFab 分配

PML 构造函数位置：`PML.cpp:689-1053`。其中 `do_pml_in_domain` 决定 PML 是在计算域外扩展，还是占据物理区域边缘的最后 `ncell` 个网格。

```cpp
// When `do_pml_in_domain` is true, the PML overlap with the last `ncell` of the physical domain or fine patch(es)
// (instead of extending `ncell` outside of the physical domain or fine patch(es))
// In order to implement this, we define a new reduced Box Array ensuring that it does not
// include ncells from the edges of the physical domain or fine patch.
// (thus creating the PML boxes at the right position, where they overlap with the original domain or fine patch(es))

BoxArray grid_ba_reduced = grid_ba;
if (do_pml_in_domain) {
    BoxList bl = grid_ba.boxList();
    for (auto& b : bl) {
        for (int idim = 0; idim < AMREX_SPACEDIM; ++idim) {
            if (do_pml_Lo[idim]) {
                Box const& bb = amrex::adjCellLo(b, idim);
                if ( ! grid_ba.intersects(bb) ) {
                    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(b.length(idim) > ncell, " box length must be greater that pml size");
                    b.growLo(idim, -ncell);
                }
            }
```

这一段的意思是：如果 PML 在 domain 内部，那么常规 grid 的边缘 box 先被缩小，再由 `MakeBoxArray()` 根据缩小后的常规域构造 PML box。这样 PML 与原物理域边缘重叠，而不是在外部 ghost 区域另建一层。

场的 component 数由 divergence cleaning 决定：

```cpp
const int ncompe = (m_dive_cleaning) ? 3 : 2;
const int ncompb = (m_divb_cleaning) ? 3 : 2;
```

这与 `PMLComponent.H` 的 `xx/yy/zz` 对应。不开启 PML divergence cleaning 时，只分配两个 curl split components；开启时才有 diagonal components。

## 6. `DampPML()`：场 damping 的调用层

`WarpXEvolvePML.cpp` 中的顶层 damping 入口位置：`../warpx/Source/BoundaryConditions/WarpXEvolvePML.cpp:46-80`。

```cpp
void
WarpX::DampPML ()
{
    for (int lev = 0; lev <= finest_level; ++lev) {
        DampPML(lev);
    }
}

void
WarpX::DampPML (const int lev)
{
    DampPML(lev, PatchType::fine);
    if (lev > 0) { DampPML(lev, PatchType::coarse); }
}

void
WarpX::DampPML (const int lev, PatchType patch_type)
{
    if (!do_pml) { return; }

    ABLASTR_PROFILE("WarpX::DampPML()");
#if (defined WARPX_DIM_RZ) && (defined WARPX_USE_FFT)
    if (pml_rz[lev]) {
        // ...
        pml_rz[lev]->ApplyDamping(...);
    }
#endif
    if (pml[lev]) {
        DampPML_Cartesian (lev, patch_type);
    }
}
```

这里有两个重要边界：

- RZ PSATD PML 有单独的 `pml_rz` damping 路径。
- 常规 Cartesian PML 进入 `DampPML_Cartesian()`。

`DampPML_Cartesian()` 取出 `pml_E/pml_B` 和 `sigba`，然后对 E、B、可选 F/G 分别调用 kernel。源码位置：`WarpXEvolvePML.cpp:92-228`。

```cpp
const auto& pml_E = (patch_type == PatchType::fine) ? m_fields.get_alldirs(FieldType::pml_E_fp, lev) : m_fields.get_alldirs(FieldType::pml_E_cp, lev);
const auto& pml_B = (patch_type == PatchType::fine) ? m_fields.get_alldirs(FieldType::pml_B_fp, lev) : m_fields.get_alldirs(FieldType::pml_B_cp, lev);
const auto& sigba = (patch_type == PatchType::fine) ? pml[lev]->GetMultiSigmaBox_fp() : pml[lev]->GetMultiSigmaBox_cp();
```

```cpp
amrex::ParallelFor(tex, tey, tez,
[=] AMREX_GPU_DEVICE (int i, int j, int k) {
    warpx_damp_pml_ex(i, j, k, pml_Exfab, Ex_stag, sigma_fac_x, sigma_fac_y, sigma_fac_z,
                      sigma_star_fac_x, sigma_star_fac_y, sigma_star_fac_z, x_lo, y_lo, z_lo,
                      dive_cleaning);
},
[=] AMREX_GPU_DEVICE (int i, int j, int k) {
    warpx_damp_pml_ey(i, j, k, pml_Eyfab, Ey_stag, sigma_fac_x, sigma_fac_y, sigma_fac_z,
                      sigma_star_fac_x, sigma_star_fac_y, sigma_star_fac_z, x_lo, y_lo, z_lo,
                      dive_cleaning);
},
[=] AMREX_GPU_DEVICE (int i, int j, int k) {
    warpx_damp_pml_ez(i, j, k, pml_Ezfab, Ez_stag, sigma_fac_x, sigma_fac_y, sigma_fac_z,
                      sigma_star_fac_x, sigma_star_fac_y, sigma_star_fac_z, x_lo, y_lo, z_lo,
                      dive_cleaning);
});
```

每个 kernel 内部只做乘法。以 `warpx_damp_pml_ex()` 为例，`Exy` 乘 y 方向阻尼，`Exz` 乘 z 方向阻尼；如果开启 `dive_cleaning`，`Exx` 乘 x 方向阻尼。staggered 位置使用 `sigma_star_fac`，nodal/cell-centered 位置使用 `sigma_fac`。

## 7. PML 电流源项：按 sigma 比例拆到 E 的 split components

`PML_current.H` 中 `push_ex_pml_current()` 把 `J_x` 加入 `E_x` 的 split components。源码位置：`../warpx/Source/BoundaryConditions/PML_current.H:17-40`。

```cpp
void push_ex_pml_current (int j, int k, int l,
                          amrex::Array4<amrex::Real> const& Ex,
                          amrex::Array4<amrex::Real const> const& jx,
                          amrex::Real const * const sigjy,
                          amrex::Real const * const sigjz,
                          int ylo, int zlo,
                          amrex::Real mu_c2_dt)
{
#if defined(WARPX_DIM_3D)
    amrex::Real alpha_xy, alpha_xz;
    if (sigjy[k-ylo]+sigjz[l-zlo] == 0){
        alpha_xy = 0.5;
        alpha_xz = 0.5;
    }
    else {
        alpha_xy = sigjy[k-ylo]/(sigjy[k-ylo]+sigjz[l-zlo]);
        alpha_xz = sigjz[l-zlo]/(sigjy[k-ylo]+sigjz[l-zlo]);
    }
    Ex(j,k,l,PMLComp::xy) = Ex(j,k,l,PMLComp::xy) - mu_c2_dt  * alpha_xy * jx(j,k,l);
    Ex(j,k,l,PMLComp::xz) = Ex(j,k,l,PMLComp::xz) - mu_c2_dt  * alpha_xz * jx(j,k,l);
#else
```

普通 Ampere 方程中的电流源项是

$$
\partial_t\mathbf E=-c^2\mu_0\mathbf J+\cdots .
$$

PML 中的区别是：`J_x` 不直接加到一个单 component `E_x` 上，而是按横向吸收系数比例分到 `Exy` 和 `Exz`。当两个方向 sigma 都为零时，源码用 0.5/0.5 平分，避免除零。

## 8. `DampJPML()`：PML 电流的累积阻尼

若 `warpx.do_pml_j_damping = 1`，主循环在沉积后会调用 `DampJPML()`。源码入口位置：`WarpXEvolvePML.cpp:249-348`。

```cpp
void
WarpX::DampJPML (int lev, PatchType patch_type)
{
    if (!do_pml) { return; }
    if (!do_pml_j_damping) { return; }
    if (!pml[lev]) { return; }

    ABLASTR_PROFILE("WarpX::DampJPML()");

    if (pml[lev]->ok())
    {
        using warpx::fields::FieldType;

        const auto& pml_j = (patch_type == PatchType::fine) ? m_fields.get_alldirs(FieldType::pml_j_fp, lev) : m_fields.get_alldirs(FieldType::pml_j_cp, lev);
        const auto& sigba = (patch_type == PatchType::fine) ? pml[lev]->GetMultiSigmaBox_fp()
                                                            : pml[lev]->GetMultiSigmaBox_cp();
```

核心调用是：

```cpp
damp_jx_pml(i, j, k, pml_jxfab, sigma_star_cumsum_fac_j_x,
            sigma_cumsum_fac_j_y, sigma_cumsum_fac_j_z,
            xs_lo,y_lo, z_lo);

damp_jy_pml(i, j, k, pml_jyfab, sigma_cumsum_fac_j_x,
            sigma_star_cumsum_fac_j_y, sigma_cumsum_fac_j_z,
            x_lo,ys_lo, z_lo);

damp_jz_pml(i, j, k, pml_jzfab, sigma_cumsum_fac_j_x,
            sigma_cumsum_fac_j_y, sigma_star_cumsum_fac_j_z,
            x_lo,y_lo, zs_lo);
```

`damp_jx_pml()` 的定义为：

```cpp
void damp_jx_pml (int j, int k, int l,
                  amrex::Array4<amrex::Real> const& jx,
                  amrex::Real const* const sigsjx,
                  amrex::Real const* const sigjy,
                  amrex::Real const* const sigjz,
                  int xlo, int ylo, int zlo)
{
#if defined(WARPX_DIM_3D)
    jx(j,k,l) = jx(j,k,l) * sigsjx[j-xlo] * sigjy[k-ylo] * sigjz[l-zlo];
#else
    jx(j,k,l) = jx(j,k,l) * sigsjx[j-xlo] * sigjz[k-zlo];
    amrex::ignore_unused(sigjy, ylo);
#endif
}
```

因此，PML 电流阻尼不是 `exp(-sigma dt)`，而是沿各方向乘 `sigma_cumsum_fac` 或 `sigma_star_cumsum_fac`。`J_x` 在 x 方向使用 star 版本，在横向使用非 star 版本；`J_y/J_z` 类似。这与电流分量的 staggered 位置对应。

## 9. `Exchange()`：split field 总和与常规场交换

PML field 在内部以 split components 存储，但常规区域只知道总场。`PML::Exchange()` 先把 split components 求和，再复制回常规场。源码位置：`PML.cpp:1130-1205`。

```cpp
// Create the sum of the split fields, in the PML
MultiFab totpmlmf(pml.boxArray(), pml.DistributionMap(), 1, 0); // Allocate
MultiFab::LinComb(totpmlmf, 1.0, pml, 0, 1.0, pml, 1, 0, 1, 0); // Sum
if (ncp == 3) {
    MultiFab::Add(totpmlmf,pml,2,0,1,0); // Sum the third split component
}
```

随后：

- 若 `do_pml_in_domain = 1`，PML valid cells 与常规 valid cells 重叠，直接把 `totpmlmf` 拷到常规场。
- 若 PML 在 domain 外，PML valid cells 只与常规 guard cells 或 nodal 外边界接触，源码通过临时 `tmpregmf` 只更新 guard 区域，并避免覆盖常规区最外层 valid cell。
- 常规场再拷回 PML 的第一个 component，第二/第三 component 清零，作为下一轮 split update 的边界输入。

这一步解释了为什么 `DampPML()` 不能孤立理解。PML 的吸收效果要经过 `DampPML()` 和 `Exchange()` 反馈到常规域边界，才会改变实际模拟区域中的出射波边界条件。

## 10. 当前边界和下一步

已确认：

- FDTD PML 场更新只读到 Cartesian kernel；RZ PSATD PML damping 有独立 `pml_rz` 路径。
- PML 的 sigma profile 是二次函数，场 damping 使用 `exp(-sigma dt)`。
- 电流 damping 使用 sigma 的解析积分因子，并按 staggered 位置选择 `sigma_cumsum_fac` 或 `sigma_star_cumsum_fac`。
- `PML::Exchange()` 是 split PML 与常规场之间的连接点。
- `do_pml_in_domain` 会改变 PML box 构造和常规/PML valid cell 的交换方式。

后续应继续：

- 把 `WarpXEvolve.cpp` 中 `DampPML()`、`CopyJPML()`、`DampJPML()` 的时间顺序回填到第 3 章。
- 进入 RZ/RCYLINDER/RSPHERE 几何下的场算法文件，区分 FDTD PML 不支持和 RZ PSATD PML 支持的边界。
- 进入 `SpectralSolver/`，解释 PSATD PML 的 spectral path。
