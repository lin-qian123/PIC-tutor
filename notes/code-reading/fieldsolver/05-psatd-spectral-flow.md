# PSATD 谱求解主流程精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 PSATD 的第一轮源码主链，不在本篇完整推导所有 Galilean/JRhom 系数：

- `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralSolver.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralFieldData.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralKSpace.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/SpectralBaseAlgorithm.H`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp`
- 官方理论文档 `../warpx/Docs/source/theory/models_algorithms/explicit_em_pic.rst:165-286`
- 官方参数文档 `../warpx/Docs/source/usage/parameters.rst:3362-3538`

## 1. 物理主线：Maxwell 方程在 Fourier 空间解析积分

官方理论文档给出 Fourier 空间 Maxwell 方程：

```rst
.. math:: \frac{\partial\mathbf{\tilde{E}}}{\partial t} = i\mathbf{k}\times\mathbf{\tilde{B}}-\mathbf{\tilde{J}}
.. math:: \frac{\partial\mathbf{\tilde{B}}}{\partial t} = -i\mathbf{k}\times\mathbf{\tilde{E}}
.. math:: {}[i\mathbf{k}\cdot\mathbf{\tilde{E}} = \tilde{\rho}]
.. math:: {}[i\mathbf{k}\cdot\mathbf{\tilde{B}} = 0]
```

若一个时间步内电流近似为常量，横向电磁波部分可解析积分：

$$
\widetilde{\mathbf E}^{n+1}
=C\widetilde{\mathbf E}^{n}
iS\hat{\mathbf k}\times\widetilde{\mathbf B}^{n}
-\frac{S}{k}\widetilde{\mathbf J}^{n+1/2}
+(1-C)\hat{\mathbf k}(\hat{\mathbf k}\cdot\widetilde{\mathbf E}^{n})
+\hat{\mathbf k}(\hat{\mathbf k}\cdot\widetilde{\mathbf J}^{n+1/2})\left(\frac{S}{k}-\Delta t\right),
$$

$$
\widetilde{\mathbf B}^{n+1}
=C\widetilde{\mathbf B}^{n}
-iS\hat{\mathbf k}\times\widetilde{\mathbf E}^{n}
+i\frac{1-C}{k}\hat{\mathbf k}\times\widetilde{\mathbf J}^{n+1/2},
$$

其中

$$
C=\cos(k\Delta t),\qquad S=\sin(k\Delta t).
$$

这解释了 PSATD 与 FDTD 的根本差异：FDTD 用局部差分近似 curl 并受 CFL 稳定性约束；PSATD 在谱空间对线性 Maxwell 部分解析推进，代价是 FFT、谱空间 guard/分解和边界处理复杂。

## 2. `WarpX::PushPSATD()`：实空间到谱空间再返回

PSATD 顶层入口在 `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:771-935`。

```cpp
WarpX::PushPSATD (amrex::Real start_time)
{
#ifndef WARPX_USE_FFT
    amrex::ignore_unused(start_time);
    WARPX_ABORT_WITH_MESSAGE(
        "PushFieldsEM: PSATD solver selected but not built");
#else

    bool const skip_lev0_coarse_patch = true;

    const int rho_old = spectral_solver_fp[0]->m_spectral_index.rho_old;
    const int rho_new = spectral_solver_fp[0]->m_spectral_index.rho_new;
```

第一个边界：没有编译 `WARPX_USE_FFT` 时，PSATD 直接 abort。谱求解器不是运行时纯参数开关，必须有 FFT 构建支持。

`PushPSATD()` 的主流程是：

1. 根据 `current_correction`、Vay deposition、periodic single box 等分支，把 `J/rho` 变换到谱空间。
2. 必要时在谱空间做 current correction 或 Vay deposition。
3. 把 `E/B` 变换到谱空间。
4. 可选变换 `F/G`。
5. 调用 `PSATDPushSpectralFields()`。
6. 把 `E/B/F/G` 逆变换回实空间。
7. 若有 PML，调用 PML 的 PSATD 推进。

源码中的主线：

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

如果开启时间平均，随后还会 inverse transform 平均场：

```cpp
if (WarpX::fft_do_time_averaging) {
    auto Efield_avg_fp = m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_fp, finest_level);
    auto Bfield_avg_fp = m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_fp, finest_level);
    auto Efield_avg_cp = m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_cp, finest_level, skip_lev0_coarse_patch);
    auto Bfield_avg_cp = m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_cp, finest_level, skip_lev0_coarse_patch);
    PSATDBackwardTransformEBavg(Efield_avg_fp, Bfield_avg_fp, Efield_avg_cp, Bfield_avg_cp);
}
```

这说明 PSATD 的 averaged fields 是谱算法直接产生的独立输出，不是事后对实空间 E/B 做简单平均。

## 3. current correction 与 Vay deposition 分支

`PushPSATD()` 在场推进前处理 current 和 rho。periodic single box 分支中 current correction 路径为：

```cpp
if (current_correction)
{
    // FFT of J and rho
    PSATDForwardTransformJ(current_fp_string, current_cp_string);
    PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 0, rho_old);
    PSATDForwardTransformRho(rho_fp_string, rho_cp_string, 1, rho_new);

    // Correct J in k-space
    ::PSATDCurrentCorrection(finest_level, spectral_solver_fp, spectral_solver_cp);

    // Inverse FFT of J
    PSATDBackwardTransformJ(current_fp_string, current_cp_string);
}
```

非 single-box 分支中，current correction 后还要 `SyncCurrent()` 和 `SyncRho()`：

```cpp
// Correct J in k-space
::PSATDCurrentCorrection(finest_level, spectral_solver_fp, spectral_solver_cp);

// Inverse FFT of J
PSATDBackwardTransformJ(current_fp_string, current_cp_string);

// Synchronize J and rho
SyncCurrent("current_fp");
SyncRho();
```

这个顺序很重要：PSATD current correction 在 local spectral boxes 内完成，回到实空间后还需要多层/guard 同步，才能保证后续再 forward transform 的 `J/rho` 是一致的。

Vay deposition 路径不是直接修正 `J`，而是先把 `current_fp_vay` 变换到谱空间，再由 `VayDeposition()` 生成 `J`，回实空间后减掉 cumulative sums：

```cpp
current_fp_string = "current_fp_vay";
PSATDForwardTransformJ(current_fp_string, current_cp_string);

// Compute J from D in k-space
::PSATDVayDeposition(finest_level, spectral_solver_fp, spectral_solver_cp);

// Inverse FFT of J, subtract cumulative sums of D
current_fp_string = "current_fp";
PSATDBackwardTransformJ(current_fp_string, current_cp_string);
```

后续要在沉积章节单独回读 Vay spectral deposition 的细节。

## 4. `SpectralSolver`：选择具体谱算法

`SpectralSolver.cpp` 构造函数中先建立 k 空间和 spectral field index：

```cpp
const SpectralKSpace k_space= SpectralKSpace(realspace_ba, dm, dx);

m_spectral_index = SpectralFieldIndex(
    update_with_rho, fft_do_time_averaging, time_dependency_J, time_dependency_rho,
    dive_cleaning, divb_cleaning, pml);
```

然后根据参数选择算法：

```cpp
if (pml)
{
    algorithm = std::make_unique<PsatdAlgorithmPml>(
        k_space, dm, m_spectral_index, norder_x, norder_y, norder_z, grid_type,
        v_galilean, dt, dive_cleaning, divb_cleaning);
}
else
{
    if (v_comoving[0] != 0. || v_comoving[1] != 0. || v_comoving[2] != 0.)
    {
        algorithm = std::make_unique<PsatdAlgorithmComoving>(...);
    }
    else if (v_galilean[0] != 0. || v_galilean[1] != 0. || v_galilean[2] != 0.)
    {
        algorithm = std::make_unique<PsatdAlgorithmGalilean>(...);
    }
```

标准 PSATD/JRhom 进入 first-order 或 second-order 算法：

```cpp
else if (psatd_solution_type == PSATDSolutionType::FirstOrder)
{
    algorithm = std::make_unique<PsatdAlgorithmJRhomFirstOrder>(...);
}
else if (psatd_solution_type == PSATDSolutionType::SecondOrder)
{
    algorithm = std::make_unique<PsatdAlgorithmJRhomSecondOrder>(...);
}
```

因此，`SpectralSolver` 自身不是具体算法，它是：

- k-space 几何容器；
- spectral field container；
- algorithm dispatch wrapper；
- FFT forward/backward wrapper。

实际 `pushSpectralFields()` 是虚函数分派：

```cpp
void SpectralSolver::pushSpectralFields(){
    ABLASTR_PROFILE("SpectralSolver::pushSpectralFields");
    algorithm->pushSpectralFields( field_data );
}
```

## 5. `SpectralFieldIndex`：谱空间字段布局

`SpectralFieldData.cpp` 中 `SpectralFieldIndex` 决定每个谱空间 component 对应什么物理量。

普通区域：

```cpp
if (!pml)
{
    Ex = c++; Ey = c++; Ez = c++;
    Bx = c++; By = c++; Bz = c++;

    divE = 3;

    if (time_averaging)
    {
        Ex_avg = c++; Ey_avg = c++; Ez_avg = c++;
        Bx_avg = c++; By_avg = c++; Bz_avg = c++;
    }

    if (dive_cleaning) { F = c++; }
    if (divb_cleaning) { G = c++; }
```

`divE = 3` 复用 `Bx` 的 component index，这是一个内存复用细节，后续解释 spectral divE 时必须小心，不能把它理解为物理上 `divE` 等于 `Bx`。

PML 区域的谱空间布局完全不同：

```cpp
else // PML
{
    Exy = c++; Exz = c++; Eyx = c++; Eyz = c++; Ezx = c++; Ezy = c++;
    Bxy = c++; Bxz = c++; Byx = c++; Byz = c++; Bzx = c++; Bzy = c++;

    if (dive_cleaning)
    {
        Exx = c++; Eyy = c++; Ezz = c++;
        Fx  = c++; Fy  = c++; Fz  = c++;
    }
```

这与 FDTD PML 中的 split component 存储一致，只是现在存放在谱空间 `SpectralFieldData::fields` 中。

## 6. `SpectralKSpace`：local FFT 的 spectral boxes 和 k 向量

`SpectralKSpace.cpp` 对每个 real-space box 建立 local spectral box：

```cpp
IntVect fft_size = realspace_bx.length();
IntVect spectral_bx_size = fft_size;
spectral_bx_size[0] = fft_size[0]/2 + 1;
const Box spectral_bx = Box( IntVect::TheZeroVector(),
                       spectral_bx_size - IntVect::TheUnitVector() );
```

因为 WarpX 使用 real-to-complex FFT，最快轴只保留非负 k，长度变成 `N/2+1`。其他轴保留正负频率：

```cpp
if (only_positive_k){
    pk[i] = i*dk;
} else {
    const int mid_point = (N+1)/2;
    if (i < mid_point) {
        pk[i] = i*dk;
    } else {
        pk[i] = (i-N)*dk;
    }
}
```

有限阶 PSATD 的“谱导数”不是一定用精确 k，而是可以用 modified k vector。`SpectralKSpace::getModifiedKComponent()` 后续需要结合 `SpectralBaseAlgorithm` 继续展开。

## 7. staggered 网格的 spectral shift

PSATD 理论文档中的公式常写在 collocated/nodal 网格上，但 WarpX 也支持 staggered grid。`SpectralFieldData::ForwardTransform()` 会检测 real-space `MultiFab` 是否 nodal；若不是 nodal，就在谱空间乘 shift factor：

```cpp
Complex spectral_field_value = tmp_arr(i,j,k);
if (!is_nodal_0) { spectral_field_value *= shift0_arr[i]; }
#if AMREX_SPACEDIM > 1
if (!is_nodal_1) { spectral_field_value *= shift1_arr[j]; }
#if AMREX_SPACEDIM > 2
if (!is_nodal_2) { spectral_field_value *= shift2_arr[k]; }
#endif
#endif
fields_arr(i,j,k,field_index) = spectral_field_value;
```

shift factor 在 `SpectralKSpace.cpp` 中定义为

```cpp
pshift[i] = amrex::exp( I*sign*pk[i]*0.5_rt*t_dx_idim);
```

这就是把 cell-centered/staggered 位置的场移动到谱算法期望位置的相位因子：

$$
e^{\pm i k\Delta x/2}.
$$

逆变换时用相反方向的 shift，把谱空间结果放回原来的 staggered 网格。

## 8. 谱空间更新 kernel：以 Galilean/standard 统一实现为例

`PsatdAlgorithmGalilean.cpp` 中 `pushSpectralFields()` 把标准 PSATD 和 Galilean PSATD 统一在一套系数里。`v_galilean=0` 时注释写明 `T2=1`，退回标准 PSATD。

源码核心更新：

```cpp
fields(i,j,k,Idx.Ex) = T2 * C * Ex_old
                       + I * c2 * T2 * S_ck * (ky * Bz_old - kz * By_old)
                       + X4 * Jx - I * (X2 * rho_new - T2 * X3 * rho_old) * kx;
```

```cpp
fields(i,j,k,Idx.Bx) = T2 * C * Bx_old
                       - I * T2 * S_ck * (ky * Ez_old - kz * Ey_old)
                       + I * X1 * (ky * Jz - kz * Jy);
```

这里的 `(ky*Bz-kz*By)` 是 Fourier 空间 curl 的 x 分量；`I*c2*S_ck` 对应解析积分中的 $i c^2 S/k$ 类系数；`X1/X2/X3/X4/T2` 是 Galilean/standard/J-rho 假设折叠后的系数。

若 `update_with_rho=false`，算法会从 Gauss 定律和连续性方程重构 `rho_old/rho_new`：

```cpp
const Complex k_dot_E = kx*Ex_old + ky*Ey_old + kz*Ez_old;
const Complex k_dot_J = kx*Jx + ky*Jy + kz*Jz;

rho_old = I*ep0*k_dot_E;

if (kc_dot_vg == 0._rt)
{
    rho_new = rho_old - I*k_dot_J*dt;
}
else
{
    rho_new = T2*rho_old + (1._rt-T2)*k_dot_J/kc_dot_vg;
}
```

这一点和输入参数 `psatd.update_with_rho` 直接相关：源码并不是总从实空间 rho 读 `rho_old/rho_new`，可以用谱空间约束关系重构。

## 9. 下一步边界

本篇只建立 PSATD 主流程。下一批需要逐块展开：

- `PsatdAlgorithmGalilean::InitializeSpectralCoefficients()` 中 `C/S_ck/X1/X2/X3/X4/T2` 的公式。
- `CurrentCorrection()` 对应参数文档中的标准/ Galilean current correction 公式。
- `PsatdAlgorithmJRhomFirstOrder/SecondOrder` 与 `OneStep_JRhom()` 的对应关系。
- `SpectralSolverRZ`、Hankel transform 与 RZ PSATD。
- `PsatdAlgorithmPml` 与 `PML::PushPSATD()`。
