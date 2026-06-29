# PSATD comoving coefficient boundary

绑定源码：

- `../warpx/Source/FieldSolver/SpectralSolver/SpectralSolver.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmComoving.H`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmComoving.cpp`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Examples/Tests/nci_psatd_stability/`

## 结论

`PsatdAlgorithmComoving` 是 regular-domain Cartesian/2D/3D PSATD 的单独 algorithm class。它和 Galilean PSATD 一样使用复相位系数，但源码分派、速度语义、current correction 和验证边界都不同。

本文件只讨论 comoving PSATD 的源码实现边界，不把它并入下面几类同名系数：

- Cartesian Galilean `PsatdAlgorithmGalilean.cpp` 的 `X1-X4/T2`。
- Galilean average-field 的 `Psi1/Psi2/Y1-Y4`。
- JRhom second-order 的 `Y1-Y8`。
- RZ/Galilean RZ 的 `Ep/Em` layout 与 `Theta2/T_rho`。
- PML PSATD 的 `C1-C25`。

## 分派边界

`SpectralSolver.cpp` 中，regular-domain PSATD 的 algorithm 选择顺序是：

```cpp
if (v_comoving[0] != 0. || v_comoving[1] != 0. || v_comoving[2] != 0.)
{
    algorithm = std::make_unique<PsatdAlgorithmComoving>(...);
}
else if (v_galilean[0] != 0. || v_galilean[1] != 0. || v_galilean[2] != 0.)
{
    algorithm = std::make_unique<PsatdAlgorithmGalilean>(...);
}
else if (psatd_solution_type == PSATDSolutionType::FirstOrder)
{
    algorithm = std::make_unique<PsatdAlgorithmJRhomFirstOrder>(...);
}
else if (psatd_solution_type == PSATDSolutionType::SecondOrder)
{
    algorithm = std::make_unique<PsatdAlgorithmJRhomSecondOrder>(...);
}
```

这说明 `v_comoving` 是 regular-domain PSATD algorithm dispatch 的第一优先级。WarpX 解析阶段又强制 `v_galilean` 和 `v_comoving` 不能同时非零：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    v_galilean_is_zero || v_comoving_is_zero,
    "Galilean and comoving algorithms should not be used together"
);
```

因此正文中不能写成“Galilean/comoving 共享同一条分派后再选系数”。更准确的说法是：二者共享 boosted-frame 默认速度入口和 direct deposition 约束，但最终落到两个不同 `PsatdAlgorithm*` class。

## 参数和约束

WarpX 的参数文档把 `psatd.v_comoving` 定义为单位为光速的三分量速度。非零 `v_comoving` 会选择 comoving PSATD，用于在一定假设下抑制 boosted-frame NCI；它要求 spectral solver/FFT，并要求 direct current deposition。

源码侧还有几个更硬的约束：

1. `psatd.use_default_v_comoving = 1` 只能在设置 `warpx.gamma_boost` 后使用。
2. 默认 comoving 速度只填 `z` 分量：

```cpp
m_v_comoving[2] = -std::sqrt(1._rt - 1._rt / (gamma_boost * gamma_boost));
```

随后 `m_v_comoving` 会乘上 `PhysConst::c`，从 normalized velocity 变成 SI 速度。

3. charge-conserving current deposition 不能和 comoving PSATD 搭配：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(v_comoving_is_zero,
    "charge-conserving current depositions (Esirkepov and Villasenor) cannot be used with the comoving PSATD algorithm");
```

4. comoving PSATD 强制 `psatd.update_with_rho = 1`：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    v_comoving_is_zero || update_with_rho,
    "psatd.update_with_rho must be equal to 1 for comoving PSATD"
);
```

5. 非默认时间依赖只允许在非 comoving/Galilean 路径继续：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    v_comoving_is_zero,
    "Time dependencies other than J constant and Rho linear not implemented with comoving PSATD");
```

6. `PsatdAlgorithmComoving::VayDeposition()` 直接 abort：

```cpp
WARPX_ABORT_WITH_MESSAGE(
    "Vay deposition not implemented for comoving PSATD");
```

这些约束把 comoving PSATD 压成一个很窄的组合：regular-domain PSATD、nonzero `v_comoving`、direct deposition、`update_with_rho=1`、默认 `J constant / rho linear` 时间依赖。

## 系数数组

`PsatdAlgorithmComoving` 分配两个实系数和五个复系数：

```cpp
C_coef    = SpectralRealCoefficients(ba, dm, 1, 0);
S_ck_coef = SpectralRealCoefficients(ba, dm, 1, 0);

X1_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
X2_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
X3_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
X4_coef     = SpectralComplexCoefficients(ba, dm, 1, 0);
Theta2_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
```

其中 `C/S_ck` 使用 finite-order modified wave number 的模：

$$
\omega_\mathrm{mod}=c|\mathbf k_\mathrm{mod}|,\qquad
C=\cos(\omega_\mathrm{mod}\Delta t),\qquad
S_{ck}=\frac{\sin(\omega_\mathrm{mod}\Delta t)}{\omega_\mathrm{mod}}.
$$

comoving 相位使用 infinite-order $\mathbf k$ 与 comoving velocity 的点积：

$$
k_v=\mathbf k\cdot\mathbf v_c,\qquad
\omega=c|\mathbf k|,\qquad
\nu=-\frac{k_v}{\omega},
$$

$$
\theta=e^{i\nu\omega\Delta t/2},\qquad
\theta^\ast=e^{-i\nu\omega\Delta t/2},\qquad
\Theta_2=\theta^2.
$$

这就是 comoving 与普通 Galilean、RZ Galilean 的第一个差异：comoving 同时保留 modified $\mathbf k_\mathrm{mod}$ 和 infinite-order $\mathbf k$，并用二者的比例处理特殊极限。

## 一般分支

当 `knorm_mod != 0`、`knorm != 0`，且

```cpp
nu != om_mod/om && nu != -om_mod/om && nu != 0.
```

源码先构造：

$$
x_1=\frac{\omega^2}{\omega_\mathrm{mod}^2-\nu^2\omega^2}
\left[
\theta^\ast-\theta C+i\nu\omega\theta S_{ck}
\right].
$$

随后：

$$
X_1=\frac{x_1}{\epsilon_0\omega^2},
$$

$$
X_2=\frac{c^2\left(x_1\omega_\mathrm{mod}^2-\theta(1-C)\omega^2\right)}
{(\theta^\ast-\theta)\epsilon_0\omega^2\omega_\mathrm{mod}^2},
$$

$$
X_3=\frac{c^2\left(x_1\omega_\mathrm{mod}^2-\theta^\ast(1-C)\omega^2\right)}
{(\theta^\ast-\theta)\epsilon_0\omega^2\omega_\mathrm{mod}^2},
$$

$$
X_4=i\nu\omega X_1-\frac{\theta S_{ck}}{\epsilon_0}.
$$

从更新式看：

- `X1` 乘 `i*(k_mod x J)`，进入 `B` 更新。
- `X2` 乘 `rho_new`，进入 `E` 更新。
- `X3` 乘 `rho_old`，进入 `E` 更新。
- `X4` 直接乘 `J`，进入 `E` 更新。
- `Theta2` 在 coefficient initialization 的特殊极限公式中参与 `X2/X3` 构造；ordinary field push 中并不把旧场整体乘 `Theta2`，这点和 Galilean RZ 更新式不同。

## 特殊分支

源码显式拆出四类极限：

1. `nu == 0`：回到 standard PSATD 的 `X1-X4` 形式。

$$
X_1=\frac{1-C}{\epsilon_0\omega_\mathrm{mod}^2},
\qquad
X_2=\frac{c^2(1-S_{ck}/\Delta t)}{\epsilon_0\omega_\mathrm{mod}^2},
\qquad
X_3=\frac{c^2(C-S_{ck}/\Delta t)}{\epsilon_0\omega_\mathrm{mod}^2},
\qquad
X_4=-\frac{S_{ck}}{\epsilon_0}.
$$

2. `nu == om_mod/om` 和 `nu == -om_mod/om`：源码用 `tmp1/tmp2` 和半步相位 `tmp1_sqrt/tmp2_sqrt` 写出专门极限，避免分母 $\omega_\mathrm{mod}^2-\nu^2\omega^2$ 退化。

3. `knorm_mod != 0 && knorm == 0`：没有 comoving 相位，使用 standard PSATD 的 `X1-X4`。

4. `knorm_mod == 0 && knorm != 0`：`C=1`、`S_ck=dt`，但仍保留 $\theta$。若 `nu != 0`，源码使用一组含 `T2` 的极限公式；若 `nu == 0`，退到零模多项式极限。

5. `knorm_mod == 0 && knorm == 0`：完全零模：

$$
C=1,\qquad S_{ck}=\Delta t,\qquad \Theta_2=1,
$$

$$
X_1=\frac{\Delta t^2}{2\epsilon_0},\qquad
X_2=\frac{c^2\Delta t^2}{6\epsilon_0},\qquad
X_3=-\frac{c^2\Delta t^2}{3\epsilon_0},\qquad
X_4=-\frac{\Delta t}{\epsilon_0}.
$$

## Ordinary field push

comoving `pushSpectralFields()` 使用 Cartesian `Ex/Ey/Ez/Bx/By/Bz` layout：

```cpp
fields(i,j,k,Idx.Ex) = C*Ex_old + S_ck*c2*I*(ky_mod*Bz_old - kz_mod*By_old)
    + X4*Jx - I*(X2*rho_new - X3*rho_old)*kx_mod;
```

磁场更新：

```cpp
fields(i,j,k,Idx.Bx) = C*Bx_old - S_ck*I*(ky_mod*Ez_old - kz_mod*Ey_old)
    + X1*I*(ky_mod*Jz - kz_mod*Jy);
```

这里的 curl 全部使用 `modified_k*_vec`，而 `nu/theta` 的相位来自 infinite-order `k*_vec` 与 `v_comoving`。正文要把“curl 用 modified k”和“相位用 physical/infinite-order k”分开写，不能只写一个抽象 $\mathbf k$。

## Current correction

comoving current correction 先取

$$
\mathbf k_\mathrm{mod}\cdot \mathbf J
$$

和

$$
\mathbf k\cdot \mathbf v_c.
$$

若 $\mathbf k\cdot\mathbf v_c\ne0$，源码使用：

```cpp
const Complex theta = amrex::exp(- I * k_dot_v * dt * 0.5_rt);
const Complex den = 1._rt - theta * theta;

fields(i,j,k,Idx.Jx_mid) = Jx
    - (kmod_dot_J + k_dot_v * theta * (rho_new - rho_old) / den)
    * kx_mod / (knorm_mod * knorm_mod);
```

若 $\mathbf k\cdot\mathbf v_c=0$，退到普通 continuity correction：

```cpp
fields(i,j,k,Idx.Jx_mid) = Jx
    - (kmod_dot_J - I * (rho_new - rho_old) / dt)
    * kx_mod / (knorm_mod * knorm_mod);
```

这条 current correction 不是 Galilean RZ 的 `T_rho` 形式，也不是 standard RZ 的 `Ep/Em` 梯度修正。

## Regression 边界

`Examples/Tests/nci_psatd_stability/CMakeLists.txt` 注册了：

```cmake
add_warpx_test(
    test_2d_comoving_psatd_hybrid
    2
    2
    inputs_test_2d_comoving_psatd_hybrid
    OFF
    "analysis_default_regression.py --path diags/diag1000400"
    OFF
)
```

输入卡设置：

```ini
algo.maxwell_solver = psatd
algo.current_deposition = direct
psatd.use_default_v_comoving = 1
psatd.current_correction = 0
warpx.gamma_boost = 13.
warpx.grid_type = hybrid
```

这说明当前 comoving NCI regression 至少证明了 boosted-frame hybrid PSATD 配置可运行并有 checksum baseline；但它没有绑定 `analysis_galilean.py` 那样的物理增长率/稳定性判据。因此正文应把它标成 checksum regression，不应声称已经有强 NCI analysis gate。

## 防混写规则

- `v_comoving` 非零时，regular-domain `SpectralSolver` 先选 `PsatdAlgorithmComoving`，不会继续落入 Galilean 或 JRhom class。
- `v_comoving` 与 `v_galilean` 解析阶段互斥。
- comoving 的 `X1-X4` 是 complex 系数，和 Cartesian Galilean 的同名 `X1-X4` 相似但不相同。
- comoving current correction 使用 `k_dot_v` 与 `theta` 的 continuity 修正，不是 RZ `T_rho`，也不是 PML split-field 系数。
- comoving regression 当前是 checksum-only 边界，正文应继续要求后续补强 analysis。
