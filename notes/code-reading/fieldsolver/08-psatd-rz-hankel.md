# RZ PSATD 与 Hankel transform 源码精读

绑定源码：

- `../warpx/Source/WarpX.cpp:572,1093-1095,2457,3070-3121`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralSolverRZ.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralFieldDataRZ.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralKSpaceRZ.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralHankelTransform/SpectralHankelTransformer.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralHankelTransform/HankelTransform.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmRZ.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalileanRZ.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPmlRZ.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/SpectralBaseAlgorithmRZ.cpp`
- `../warpx/Docs/source/usage/parameters.rst:622-639,3216`

RZ PSATD 和 Cartesian PSATD 的最大区别不是把 `y` 方向删掉，而是谱基完全不同。`z` 方向仍然做 Fourier transform；径向 `r` 方向做离散 Hankel transform；横向矢量分量还要先转换成适合 Bessel 基的 `p/m` 组合。源码中的核心对象是：

- `SpectralSolverRZ`：RZ 谱求解器门面，选择标准/Galilean/PML 算法。
- `SpectralFieldDataRZ`：负责 Hankel transform、z FFT、谱字段存储、滤波和反变换。
- `SpectralHankelTransformer` / `HankelTransform`：构造 Bessel 根、离散 Hankel 矩阵和正/反变换。
- `PsatdAlgorithmRZ`：RZ 标准 PSATD 更新、RZ current correction 和 time averaging。

## 1. RZ 模式数和场 component 数

RZ 采用 azimuthal mode decomposition。一个实物理场写成

$$
F(r,z,\theta)=\sum_m \Re\left(F_m(r,z)e^{im\theta}\right).
$$

实空间 `MultiFab` 中每个 mode 用实部/虚部分量存储，但 `m=0` 没有虚部。因此总 component 数是

$$
n_\mathrm{comps}=2n_\mathrm{modes}-1.
$$

源码在 `WarpX.cpp` 中设置：

```cpp
utils::parser::queryWithParser(pp_warpx, "n_rz_azimuthal_modes", n_rz_azimuthal_modes);
WARPX_ALWAYS_ASSERT_WITH_MESSAGE( n_rz_azimuthal_modes > 0,
    "The number of azimuthal modes (n_rz_azimuthal_modes) must be at least 1");
```

```cpp
ncomps = n_rz_azimuthal_modes*2 - 1;
```

这解释了为什么 RZ 源码中经常出现 `2*n_rz_azimuthal_modes` 的临时数组：Hankel transform 中需要显式保留 `m=0` 的虚部槽，虽然它为零。

RZ PSATD 还要求径向下边界在轴上：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    Geom(0).ProbLo(0) == 0.,
    "Lower bound of radial coordinate (prob_lo[0]) with RZ PSATD solver must be zero");
```

这不是格式限制，而是 Hankel/Bessel 模式基建立在 `r=0` 到 `rmax` 的径向区间上。

## 2. `SpectralSolverRZ`：选择 RZ 谱算法

RZ spectral solver 在 `WarpX::AllocLevelSpectralSolverRZ()` 中创建，并传入 `n_rz_azimuthal_modes`、`norder_z`、`v_galilean`、`update_with_rho`、time averaging 和 cleaning 选项。

```cpp
auto pss = std::make_unique<SpectralSolverRZ>(lev,
                                              realspace_ba,
                                              dm,
                                              n_rz_azimuthal_modes,
                                              noz_fft,
                                              grid_type,
                                              m_v_galilean,
                                              dx_vect,
                                              solver_dt,
                                              ::isAnyBoundaryPML(field_boundary_lo, field_boundary_hi),
                                              update_with_rho,
                                              fft_do_time_averaging,
                                              time_dependency_J,
                                              time_dependency_rho,
                                              do_dive_cleaning,
                                              do_divb_cleaning);
```

`SpectralSolverRZ` 构造函数先建立 `SpectralKSpaceRZ`，再建立 `SpectralFieldIndex`。和 Cartesian 不同，最后一个参数 `with_pml` 会让 `SpectralFieldIndex` 额外分配 RZ PML component：

```cpp
const bool is_pml = false;
m_spectral_index = SpectralFieldIndex(
    update_with_rho, fft_do_time_averaging, time_dependency_J, time_dependency_rho,
    dive_cleaning, divb_cleaning, is_pml, with_pml);
```

算法选择逻辑是：

```cpp
if (with_pml) {
        PML_algorithm = std::make_unique<PsatdAlgorithmPmlRZ>(
            k_space, dm, m_spectral_index, n_rz_azimuthal_modes, norder_z, grid_type, dt);
}
if (v_galilean[2] == 0) {
     // v_galilean is 0: use standard PSATD algorithm
    algorithm = std::make_unique<PsatdAlgorithmRZ>(
        k_space, dm, m_spectral_index, n_rz_azimuthal_modes, norder_z, grid_type, dt,
        update_with_rho, fft_do_time_averaging, time_dependency_J, time_dependency_rho, dive_cleaning, divb_cleaning);
} else {
    // Otherwise: use the Galilean algorithm
    algorithm = std::make_unique<PsatdAlgorithmGalileanRZ>(
        k_space, dm, m_spectral_index, n_rz_azimuthal_modes, norder_z, grid_type, v_galilean, dt, update_with_rho);
}
```

RZ Galilean 只检查 `v_galilean[2]`，即沿 `z` 的 Galilean 速度。RZ 几何中没有 Cartesian 的任意三维 Galilean drift。

`pushSpectralFields()` 根据 `doing_pml` 分派：

```cpp
void
SpectralSolverRZ::pushSpectralFields (const bool doing_pml) {
    ABLASTR_PROFILE("SpectralSolverRZ::pushSpectralFields");
    if (doing_pml) {
        PML_algorithm->pushSpectralFields(field_data);
    } else {
        algorithm->pushSpectralFields(field_data);
    }
}
```

## 3. RZ k-space：只有 z 方向 Fourier k，径向 k 来自 Hankel

`SpectralKSpaceRZ` 的构造只为 z 方向创建 Fourier k：

```cpp
// Allocate the components of the kz vector
const int i_dim = 1;
const bool only_positive_k = false;
k_vec[i_dim] = getKComponent(dm, realspace_ba, i_dim, only_positive_k);
```

径向 `kr` 不在这里生成，而是在 `SpectralHankelTransformer` 中从 Bessel roots 生成。这个分工很重要：

- `kz`：由 z 向 FFT 网格给出；
- `kr`：由每个 azimuthal mode 的离散 Hankel 基给出；
- 谱算法中使用

$$
k=\sqrt{k_r^2+k_z^2}.
$$

`PsatdAlgorithmRZ` 初始化系数时就这么写：

```cpp
int const ir = i + nr*mode;
amrex::Real const kr = kr_arr[ir];
amrex::Real const kz = modified_kz[j];
amrex::Real const k_norm = std::sqrt(kr*kr + kz*kz);
```

## 4. `SpectralFieldDataRZ`：先 Hankel，再 z FFT

RZ 谱 field storage 的 component 排布为“每个 mode 的所有 field 挤在一起”：

```cpp
fields = SpectralField(spectralspace_ba, dm, n_rz_azimuthal_modes*n_field_required, 0);
```

注释明确说明：

```cpp
// The fields of each mode are grouped together, so that the index of a
// field for a specific mode is given by field_index + mode*n_fields.
```

所以 `PsatdAlgorithmRZ` 里大量索引都形如：

```cpp
int const Ep_m = Idx.Ex + Idx.n_fields*mode;
int const Em_m = Idx.Ey + Idx.n_fields*mode;
int const Ez_m = Idx.Ez + Idx.n_fields*mode;
```

正变换中，标量字段先 copy 到临时 MultiFab，再做 Hankel transform：

```cpp
// Perform the Hankel transform first.
// tempHTransformedSplit includes the imaginary component of mode 0.
// field_mf does not.
amrex::Box const& realspace_bx = tempHTransformed[mfi].box();

field_mf_copy[mfi].copy<amrex::RunOn::Device>(field_mf[mfi], i_comp*m_ncomps, 0, m_ncomps);
multi_spectral_hankel_transformer[mfi].PhysicalToSpectral_Scalar(field_mf_copy[mfi], tempHTransformedSplit[mfi]);

FABZForwardTransform(mfi, realspace_bx, tempHTransformedSplit, field_index, is_nodal_z);
```

`FABZForwardTransform()` 再把 split complex 转成 interleaved complex，并执行 z FFT：

```cpp
ParallelFor(realspace_bx, modes,
[=] AMREX_GPU_DEVICE(int i, int j, int k, int mode) noexcept {
    int const mode_r = 2*mode;
    int const mode_i = 2*mode + 1;
    complex_arr(i,j,k,mode) = Complex{split_arr(i,j,k,mode_r), split_arr(i,j,k,mode_i)};
});
```

FFT 后写入谱 field，并在 cell-centered z 网格上乘 shift：

```cpp
Complex spectral_field_value = tmp_arr(i,j,k,mode);
// Apply proper shift.
if (!is_nodal_z) { spectral_field_value *= zshift_arr[j]; }
// Copy field into the correct index.
int const ic = field_index + mode*n_fields;
fields_arr(i,j,k,ic) = spectral_field_value*inv_nz;
```

因此 RZ 正变换顺序是：

$$
\text{real }(r,z,\theta)\quad
\xrightarrow{\text{Hankel in }r}
\quad (k_r,z,m)\quad
\xrightarrow{\text{FFT in }z}
\quad (k_r,k_z,m).
$$

## 5. 横向矢量场：`r/theta` 组合成 `p/m`

标量 Hankel transform 使用 `dht0`。矢量横向分量不能直接分别做同阶 Hankel transform，而要先组合为

$$
F_p=\frac{F_r-iF_\theta}{2},\qquad
F_m=\frac{F_r+iF_\theta}{2}.
$$

源码中实部/虚部展开为：

```cpp
// Combine the values
// temp_p = (F_r - I*F_t)/2
// temp_m = (F_r + I*F_t)/2
F_r_physical_array(i,j,k,mode_r) = 0.5_rt*(r_real + t_imag);
F_r_physical_array(i,j,k,mode_i) = 0.5_rt*(r_imag - t_real);
F_t_physical_array(i,j,k,mode_r) = 0.5_rt*(r_real - t_imag);
F_t_physical_array(i,j,k,mode_i) = 0.5_rt*(r_imag + t_real);
```

然后对 `p/m` 分别使用不同阶数的 Hankel transform：

```cpp
dhtp[mode]->HankelForwardTransform(F_r_physical, mode_r, G_p_spectral, mode_r);
dhtp[mode]->HankelForwardTransform(F_r_physical, mode_i, G_p_spectral, mode_i);
dhtm[mode]->HankelForwardTransform(F_t_physical, mode_r, G_m_spectral, mode_r);
dhtm[mode]->HankelForwardTransform(F_t_physical, mode_i, G_m_spectral, mode_i);
```

这些 transform 对象在构造函数中建立：

```cpp
for (int mode=0 ; mode < m_n_rz_azimuthal_modes ; mode++) {
    dht0[mode] = std::make_unique<HankelTransform>(mode  , mode, m_nr, rmax);
    dhtp[mode] = std::make_unique<HankelTransform>(mode+1, mode, m_nr, rmax);
    dhtm[mode] = std::make_unique<HankelTransform>(mode-1, mode, m_nr, rmax);
}
```

所以 RZ 谱算法里的 `Ep/Em` 不是 Cartesian 的 `Ex/Ey`，而是由 `E_r/E_theta` 组合出的正负螺旋分量。curl、div、grad 的谱表达都围绕 `Ep-Em`、`Ep+Em` 展开。

## 6. Hankel transform 矩阵：Bessel roots、伪逆与 GEMM

`HankelTransform` 构造时先取 Bessel roots：

```cpp
amrex::Vector<amrex::Real> alphas;
amrex::Vector<int> alpha_errors;

GetBesselRoots(azimuthal_mode, m_nk, alphas, alpha_errors);
AMREX_ALWAYS_ASSERT(std::all_of(alpha_errors.begin(), alpha_errors.end(), [](int i) { return i == 0; }));

amrex::Vector<amrex::Real> kr(m_nk);
for (int ik=0 ; ik < m_nk ; ik++) {
    kr[ik] = alphas[ik]/rmax;
}
```

径向网格用半格偏移：

```cpp
const amrex::Real dr = rmax/m_nr;
for (int ir=0 ; ir < m_nr ; ir++) {
    rmesh[ir] = dr*(ir + 0.5_rt);
}
```

随后构造离散 Hankel transform 的矩阵。某些 mode 下矩阵奇异，需要 Moore-Penrose 伪逆：

```cpp
if (azimuthal_mode !=0 && hankel_order != azimuthal_mode-1) {
    // In this case, invM is singular, thus we calculate the pseudo-inverse.
    // The Moore-Penrose pseudo-inverse is calculated using the SVD method.
```

正变换和反变换最终都落到 BLAS GEMM：

```cpp
// Note that M is flagged to be transposed since it has dimensions (m_nr, m_nk)
blas::gemm(blas::Layout::ColMajor, blas::Op::Trans, blas::Op::NoTrans,
           m_nk, nz, m_nr, 1._rt,
           m_M.dataPtr(), m_nk,
           F.dataPtr(F_icomp)+ngr, nrF, 0._rt,
           G.dataPtr(G_icomp), m_nk
#ifdef AMREX_USE_GPU
           , *m_queue
#endif
       );
```

反变换用 `m_invM`：

```cpp
blas::gemm(blas::Layout::ColMajor, blas::Op::Trans, blas::Op::NoTrans,
           m_nr, nz, m_nk, 1._rt,
           m_invM.dataPtr(), m_nr,
           G.dataPtr(G_icomp), m_nk, 0._rt,
           F.dataPtr(F_icomp)+ngr, nrF
#ifdef AMREX_USE_GPU
           , *m_queue
#endif
       );
```

这说明 RZ PSATD 的径向谱变换不是 FFT，而是 dense matrix transform。它的计算和内存特征与 Cartesian FFT 路径完全不同。

## 7. RZ PSATD 更新式：`Ep/Em/Ez` 与 `Bp/Bm/Bz`

`PsatdAlgorithmRZ` 对每个 `(kr,kz,mode)` 解析推进。它先取 `Ep/Em/Ez` 和 `Bp/Bm/Bz`：

```cpp
Complex const Ep_old = fields(i,j,k,Ep_m);
Complex const Em_old = fields(i,j,k,Em_m);
Complex const Ez_old = fields(i,j,k,Ez_m);
Complex const Bp_old = fields(i,j,k,Bp_m);
Complex const Bm_old = fields(i,j,k,Bm_m);
Complex const Bz_old = fields(i,j,k,Bz_m);
```

如果 `update_with_rho` 打开，纵向电荷修正为：

```cpp
if (update_with_rho) {
    rho_diff = X2*rho_new - X3*rho_old;
} else {
    Complex const divE = kr*(Ep_old - Em_old) + I*kz*Ez_old;
    Complex const divJ = kr*(Jp - Jm) + I*kz*Jz;

    rho_diff = (X2 - X3)*PhysConst::epsilon_0*divE - X2*dt*divJ;
}
```

这里 RZ 谱散度是：

$$
\nabla\cdot\mathbf E
\rightarrow k_r(E_p-E_m)+ik_zE_z.
$$

电场更新为：

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

磁场更新为：

```cpp
fields(i,j,k,Bp_m) = C*Bp_old
            - S_ck*(-I*kr/2._rt*Ez_old + kz*Ep_old)
            + X1*(-I*kr/2._rt*Jz + kz*Jp);
fields(i,j,k,Bm_m) = C*Bm_old
            - S_ck*(-I*kr/2._rt*Ez_old - kz*Em_old)
            + X1*(-I*kr/2._rt*Jz - kz*Jm);
fields(i,j,k,Bz_m) = C*Bz_old
            - S_ck*I*(kr*Ep_old + kr*Em_old)
            + X1*I*(kr*Jp + kr*Jm);
```

这些式子是 RZ 版 PSATD 的核心：`kr/2` 和 `Ep/Em` 的正负号来自 cylindrical vector harmonics 的 curl/div 代数，而不是任意系数调参。

## 8. RZ 系数与零模极限

RZ 标准 PSATD 系数是：

```cpp
if (k_norm != 0){
    C(i,j,k,mode) = std::cos(c*k_norm*dt);
    S_ck(i,j,k,mode) = std::sin(c*k_norm*dt)/(c*k_norm);
    X1(i,j,k,mode) = (1._rt - C(i,j,k,mode))/(ep0 * c*c * k_norm*k_norm);
    X2(i,j,k,mode) = (1._rt - S_ck(i,j,k,mode)/dt)/(ep0 * k_norm*k_norm);
    X3(i,j,k,mode) = (C(i,j,k,mode) - S_ck(i,j,k,mode)/dt)/(ep0 * k_norm*k_norm);
} else {
    C(i,j,k,mode) = 1._rt;
    S_ck(i,j,k,mode) = dt;
    X1(i,j,k,mode) = 0.5_rt * dt*dt / ep0;
    X2(i,j,k,mode) = c*c * dt*dt / (6._rt*ep0);
    X3(i,j,k,mode) = - c*c * dt*dt / (3._rt*ep0);
}
```

零模极限在 RZ 中同样必须显式处理；否则 `k_norm=0` 会导致除零。这里的 `k_norm` 是 `sqrt(kr^2+kz^2)`，所以零模只发生在径向 Hankel 零模和 z 向零频同时出现的模式上。

## 9. RZ current correction

RZ current correction 修正的是 `Jp/Jm/Jz`：

```cpp
Complex const F = - ((rho_new - rho_old)/dt + I*kz*Jz + kr*(Jp - Jm))/k_norm2;

fields(i,j,k,Jp_m) += +0.5_rt*kr*F;
fields(i,j,k,Jm_m) += -0.5_rt*kr*F;
fields(i,j,k,Jz_m) += -I*kz*F;
```

它对应把电流投影到满足谱空间连续性方程的子空间。RZ 的散度形式是

$$
\nabla\cdot\mathbf J
\rightarrow k_r(J_p-J_m)+ik_zJ_z.
$$

所以修正量沿 RZ 谱梯度方向分配到 `Jp/Jm/Jz`，而不是 Cartesian 中的 `Jx/Jy/Jz`。

RZ Vay deposition 当前不可用：

```cpp
void
PsatdAlgorithmRZ::VayDeposition (SpectralFieldDataRZ& /*field_data*/)
{
    WARPX_ABORT_WITH_MESSAGE(
        "Vay deposition not implemented in RZ geometry");
}
```

## 10. RZ Galilean PSATD

`PsatdAlgorithmGalileanRZ` 只支持 `v_galilean[2]`。它在标准 RZ 更新式上加入

$$
T_2=e^{ik_zv_G\Delta t}
$$

和复数 `X1-X4` 系数。源码中：

```cpp
amrex::Real const kv = kz*vz;

amrex::Real const nu = kv/(k_norm*c);
Complex const theta = amrex::exp( 0.5_rt*I*kv*dt );
Complex const theta_star = amrex::exp( -0.5_rt*I*kv*dt );
Complex const e_theta = amrex::exp( I*c*k_norm*dt );

Theta2(i,j,k,mode) = theta*theta;
```

更新式以 `Ep` 为例：

```cpp
fields(i,j,k,Ep_m) = T2*C*Ep_old
            + T2*S_ck*(-c2*I*kr/2._rt*Bz_old + c2*kz*Bp_old)
            + X4*Jp + 0.5_rt*kr*rho_diff;
```

这和 Cartesian Galilean PSATD 的结构平行：旧场和 curl 项乘 `T2`，电流和电荷项使用 Galilean 系数。

## 11. RZ PML PSATD

RZ PML 谱算法只推进 PML 的横向 split components：

```cpp
int const Ep_m_pml = Idx.Er_pml + Idx.n_fields*mode;
int const Em_m_pml = Idx.Et_pml + Idx.n_fields*mode;
int const Bp_m_pml = Idx.Br_pml + Idx.n_fields*mode;
int const Bm_m_pml = Idx.Bt_pml + Idx.n_fields*mode;
int const Ez_m = Idx.Ez + Idx.n_fields*mode;
int const Bz_m = Idx.Bz + Idx.n_fields*mode;
```

更新式为：

```cpp
fields(i,j,k,Ep_m_pml) = C*Ep_old_pml
            + S_ck*(-c2*I*kr/2._rt*Bz_old);
fields(i,j,k,Em_m_pml) = C*Em_old_pml
            + S_ck*(-c2*I*kr/2._rt*Bz_old);
// Update B
fields(i,j,k,Bp_m_pml) = C*Bp_old_pml
            - S_ck*(-I*kr/2._rt*Ez_old);
fields(i,j,k,Bm_m_pml) = C*Bm_old_pml
            - S_ck*(-I*kr/2._rt*Ez_old);
```

RZ PML current correction 和 Vay 都显式 abort：

```cpp
WARPX_ABORT_WITH_MESSAGE(
    "Current correction not implemented in RZ geometry PML");
```

```cpp
WARPX_ABORT_WITH_MESSAGE(
    "Vay deposition not implemented in RZ geometry PML");
```

## 12. 反变换和轴下 guard cells

RZ 反变换时，先做 z inverse FFT，再做 inverse Hankel transform。随后填充轴下 guard cells，并根据 mode 奇偶设置符号。标量反变换中：

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

矢量反变换中，mode zero 的径向/方位分量是反对称的：

```cpp
if (i < 0) {
    ii = -i - 1;
    if (icomp == 0) {
        // Mode zero is anti-symmetric
        sign = -1._rt;
    } else {
        // Even modes are anti-symmetric
        const int imode = (icomp + 1)/2;
        sign = static_cast<amrex::Real>(std::pow(-1._rt, imode+1));
    }
}
```

这和 FDTD RZ 中的轴上正则化是同一类物理约束：`r=0` 附近的场不能按普通 Cartesian guard cell 镜像处理，而必须按 azimuthal mode 的对称性处理。

## 13. 小结：RZ PSATD 的源码闭环

RZ PSATD 的完整路径是：

1. `WarpX.cpp` 读取 `warpx.n_rz_azimuthal_modes`，设置 RZ field component 数 `2*modes-1`，并要求 RZ PSATD 的 `prob_lo[0]=0`。
2. `AllocLevelSpectralSolverRZ()` 创建 `SpectralSolverRZ`。
3. `SpectralSolverRZ` 根据 PML 和 `v_galilean[2]` 选择 `PsatdAlgorithmRZ`、`PsatdAlgorithmGalileanRZ` 或 `PsatdAlgorithmPmlRZ`。
4. `SpectralFieldDataRZ` 先做径向 Hankel transform，再做 z FFT，并以 `field_index + mode*n_fields` 存储谱字段。
5. `SpectralHankelTransformer` 对 scalar 使用 `dht0`，对 vector 使用 `dhtp/dhtm` 和 `p/m` 组合。
6. `HankelTransform` 用 Bessel roots 构造 `kr` 和离散 Hankel 变换矩阵，必要时用 SVD 伪逆。
7. `PsatdAlgorithmRZ` 在 `(kr,kz,mode)` 空间更新 `Ep/Em/Ez/Bp/Bm/Bz`。
8. 反变换时按 mode 对称性填充轴下 guard cells。

因此，RZ PSATD 不是 Cartesian PSATD 的二维简化版。它的数学基、数据布局、横向分量定义、current correction 和 guard-cell 对称性都不同。
