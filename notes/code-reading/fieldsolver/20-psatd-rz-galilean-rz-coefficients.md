# RZ and Galilean RZ PSATD coefficient boundary atlas

绑定源码：

- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmRZ.cpp`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalileanRZ.cpp`

本笔记只覆盖 RZ 标准 PSATD 与 RZ Galilean PSATD 的系数边界。它的目的不是重新推导完整 cylindrical vector harmonic theory，而是把 RZ 里的 `X*` 与 Cartesian `X*`、JRhom `Y*`、PML `C*` 明确拆开，避免同名系数跨算法误读。

## RZ 谱基和字段布局

RZ PSATD 不是 Cartesian PSATD 删掉一个方向。它在 $z$ 方向做 Fourier transform，在径向做 Hankel transform，并把横向矢量分量写成 `p/m` 组合：

```cpp
int const Ep_m = Idx.Ex + Idx.n_fields*mode;
int const Em_m = Idx.Ey + Idx.n_fields*mode;
int const Ez_m = Idx.Ez + Idx.n_fields*mode;
int const Bp_m = Idx.Bx + Idx.n_fields*mode;
int const Bm_m = Idx.By + Idx.n_fields*mode;
int const Bz_m = Idx.Bz + Idx.n_fields*mode;
```

RZ 谱导数的基础量是 Hankel radial wavenumber `kr` 和 modified Fourier `kz`：

$$
k=\sqrt{k_r^2+k_z^2}.
$$

因此 `Ep/Em` 不是 Cartesian `Ex/Ey`，更新式里的 `kr/2` 和 `Ep-Em`、`Ep+Em` 结构来自 cylindrical vector harmonics。

## Standard RZ coefficient set

`PsatdAlgorithmRZ` 总是分配实系数：

```cpp
C_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
S_ck_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
X1_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
X2_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
X3_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
```

非零模公式为：

$$
C=\cos(ck\Delta t),\qquad
S_{ck}=\frac{\sin(ck\Delta t)}{ck},
$$

$$
X_1=\frac{1-C}{\epsilon_0c^2k^2},
\qquad
X_2=\frac{1-S_{ck}/\Delta t}{\epsilon_0k^2},
\qquad
X_3=\frac{C-S_{ck}/\Delta t}{\epsilon_0k^2}.
$$

零模分支为：

$$
C=1,\quad
S_{ck}=\Delta t,\quad
X_1=\frac{\Delta t^2}{2\epsilon_0},\quad
X_2=\frac{c^2\Delta t^2}{6\epsilon_0},\quad
X_3=-\frac{c^2\Delta t^2}{3\epsilon_0}.
$$

`X1` 只进入 RZ 磁场更新中的 current-curl 项。`X2/X3` 只组合 `rho_new/rho_old`：

```cpp
if (update_with_rho) {
    rho_diff = X2*rho_new - X3*rho_old;
} else {
    Complex const divE = kr*(Ep_old - Em_old) + I*kz*Ez_old;
    Complex const divJ = kr*(Jp - Jm) + I*kz*Jz;

    rho_diff = (X2 - X3)*PhysConst::epsilon_0*divE - X2*dt*divJ;
}
```

电场更新式以 `Ep/Em/Ez` 显示 RZ 的符号结构：

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

磁场更新式同样使用 `Ep/Em` 组合：

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

这就是 RZ 系数不能直接套 Cartesian `kx/ky/kz` 向量式的原因：系数标量看起来相近，但作用在 `Ep/Em/Bp/Bm` 的谱算子结构不同。

## RZ time averaging: X5 and X6

标准 RZ time averaging 只在 `time_averaging && time_dependency_J == Linear` 下支持。源码若发现 time averaging 配合非线性 `J`，会直接 abort：

```cpp
if (time_averaging && time_dependency_J != TimeDependencyJ::Linear)
{
    WARPX_ABORT_WITH_MESSAGE(
        "RZ PSATD: psatd.do_time_averaging=1 implemented only with psatd.time_dependency_J=linear");
}
```

线性 `J` 时额外分配 `X5/X6`：

```cpp
if (time_averaging && time_dependency_J == TimeDependencyJ::Linear)
{
    X5_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
    X6_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
}
```

令 $\omega=ck$，非零模公式为：

$$
X_5=\frac{c^2}{\epsilon_0}
\left[
\frac{S_{ck}}{\omega^2}
-\frac{1-C}{\omega^4\Delta t}
-\frac{\Delta t}{2\omega^2}
\right],
$$

$$
X_6=\frac{c^2}{\epsilon_0}
\left[
\frac{1-C}{\omega^4\Delta t}
-\frac{\Delta t}{2\omega^2}
\right].
$$

零模分支为：

$$
X_5=-\frac{c^2\Delta t^3}{8\epsilon_0},
\qquad
X_6=-\frac{c^2\Delta t^3}{24\epsilon_0}.
$$

average-field 更新中，`X5` 乘 old `rho/J`，`X6` 乘 new `rho/J`：

```cpp
fields(i,j,k,Ep_avg_m) += S_ck * Ep_old
    + c2 * ep0 * X1 * (kz * Bp_old - I * kr * 0.5_rt * Bz_old)
    - kr * 0.5_rt * (X5 * rho_old + X6 * rho_new) + X3/c2 * Jp - X2/c2 * Jp_new;
```

这组 `X5/X6` 是 RZ linear-J time averaging 系数，不是 Cartesian `X5/X6`，也不是 JRhom `Y6/Y8`。

## Galilean RZ coefficient set

`PsatdAlgorithmGalileanRZ` 只使用轴向 Galilean velocity：

```cpp
const amrex::Real vz = m_v_galilean[2];
amrex::Real const kv = kz*vz;
```

它分配两类系数：

```cpp
C_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
S_ck_coef = SpectralRealCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
X1_coef = SpectralComplexCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
X2_coef = SpectralComplexCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
X3_coef = SpectralComplexCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
X4_coef = SpectralComplexCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
Theta2_coef = SpectralComplexCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
T_rho_coef = SpectralComplexCoefficients(ba, dm, n_rz_azimuthal_modes, 0);
```

`C/S_ck` 仍按 $k=\sqrt{k_r^2+k_z^2}$ 计算。Galilean 特有量为：

$$
k_v=k_zv_z,\qquad
\nu=\frac{k_v}{ck},\qquad
\theta=e^{ik_v\Delta t/2}.
$$

源码存储：

$$
\Theta_2=\theta^2.
$$

`T_rho` 是 charge-continuity 相位因子：

$$
T_\rho=
\begin{cases}
-\Delta t, & k_z=0,\\
\dfrac{1-\theta^2}{ik_zv_z}, & k_z\ne0.
\end{cases}
$$

一般分支 `nu != 1 && nu != 0` 中，源码先构造

$$
x_1=\frac{\theta^\ast-C\theta+ik_vS_{ck}\theta}{1-\nu^2},
$$

再定义

$$
X_1=\frac{\theta x_1}{\epsilon_0c^2k^2},
$$

$$
X_2=\frac{x_1-\theta(1-C)}{(\theta^\ast-\theta)\epsilon_0k^2},
\qquad
X_3=\frac{x_1-\theta^\ast(1-C)}{(\theta^\ast-\theta)\epsilon_0k^2},
$$

$$
X_4=ik_vX_1-\frac{\theta^2S_{ck}}{\epsilon_0}.
$$

当 `nu == 0`，它回到标准 RZ 系数：

$$
X_1=\frac{1-C}{\epsilon_0c^2k^2},\quad
X_2=\frac{1-S_{ck}/\Delta t}{\epsilon_0k^2},\quad
X_3=\frac{C-S_{ck}/\Delta t}{\epsilon_0k^2},\quad
X_4=-\frac{S_{ck}}{\epsilon_0}.
$$

当 `nu == 1`，源码使用专门极限分支，避免 $\theta^\ast-\theta$ 或 $1-\nu^2$ 分母退化。零模分支则取：

$$
C=1,\quad S_{ck}=\Delta t,\quad
X_1=\frac{\Delta t^2}{2\epsilon_0},\quad
X_2=\frac{c^2\Delta t^2}{6\epsilon_0},\quad
X_3=-\frac{c^2\Delta t^2}{3\epsilon_0},\quad
X_4=-\frac{\Delta t}{\epsilon_0},\quad
\Theta_2=1.
$$

Galilean RZ 更新式和 standard RZ 的字段布局相同，但旧场和 curl 项乘 `T2=Theta2`，电流直接项用 `X4`：

```cpp
fields(i,j,k,Ep_m) = T2*C*Ep_old
            + T2*S_ck*(-c2*I*kr/2._rt*Bz_old + c2*kz*Bp_old)
            + X4*Jp + 0.5_rt*kr*rho_diff;
```

电荷项也携带 Galilean 相位：

```cpp
if (update_with_rho) {
    rho_diff = X2*rho_new - T2*X3*rho_old;
} else {
    rho_diff = T2*(X2 - X3)*myeps0*divE + T_rho*X2*divJ;
}
```

## Current correction and unsupported combinations

RZ current correction 沿 RZ 谱梯度方向修正 `Jp/Jm/Jz`：

```cpp
Complex const F = - ((rho_new - rho_old)/dt + I*kz*Jz + kr*(Jp - Jm))/k_norm2;

fields(i,j,k,Jp_m) += +0.5_rt*kr*F;
fields(i,j,k,Jm_m) += -0.5_rt*kr*F;
fields(i,j,k,Jz_m) += -I*kz*F;
```

Galilean RZ current correction 把 `rho_old` 乘 `theta2`，并用

```cpp
Complex const j_corr_coef = (kz == 0._rt ? 1._rt/dt : -I*kz*vz/(1._rt - theta2));
```

替换标准连续性残差中的时间差分。RZ Vay deposition 当前显式不可用：

```cpp
WARPX_ABORT_WITH_MESSAGE(
    "Vay deposition not implemented in RZ geometry");
```

## 防混写规则

- Standard RZ `X1-X3` 是实系数，作用在 `Ep/Em/Ez/Bp/Bm/Bz` 和 RZ 谱算子上。
- Standard RZ `X5/X6` 只属于 linear-J time averaging。
- Galilean RZ `X1-X4` 是 complex 系数，并额外有 `Theta2/T_rho`。
- Cartesian Galilean `X1-X4` 的向量形式不能直接搬到 RZ，因为 RZ 的横向分量是 `Ep/Em`，径向谱量来自 Hankel transform。
- JRhom `Y1-Y8` 与 RZ `X*` 属于不同 algorithm class，不能合并成同一张 PSATD 系数表。
