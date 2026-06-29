# PSATD-JRhom second-order Y coefficient atlas

绑定源码：`../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmJRhomSecondOrder.cpp`。

本笔记只覆盖 Cartesian `PsatdAlgorithmJRhomSecondOrder` 的 `Y1-Y8`。这些系数属于 JRhom second-order 的多项式源项积分：`Y1-Y5` 总是分配，参与普通 `E/B/F` 谱推进；`Y6-Y8` 只在 `psatd.do_time_averaging=1` 时分配，用于累计 average-field 输出。它们不是 `PsatdAlgorithmGalilean.cpp` average-field 分支里的 complex `Y1-Y4`，也不是 RZ/Galilean RZ 或 PML PSATD 的系数。

## 分配边界

`PsatdAlgorithmJRhomSecondOrder` 构造函数总是分配实系数 `C/S_ck/Y1-Y5`：

```cpp
C_coef = SpectralRealCoefficients(ba, dm, 1, 0);
S_ck_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y1_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y2_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y3_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y4_coef = SpectralRealCoefficients(ba, dm, 1, 0);
Y5_coef = SpectralRealCoefficients(ba, dm, 1, 0);
```

只有 time averaging 打开时才分配 `Y6-Y8`：

```cpp
if (time_averaging)
{
    Y6_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    Y7_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    Y8_coef = SpectralRealCoefficients(ba, dm, 1, 0);
    InitializeSpectralCoefficientsAveraging(spectral_kspace, dm, dt);
}
```

源码还要求 time averaging 必须配合 `update_with_rho`：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    !time_averaging || update_with_rho,
    "psatd.time_averaging=1 implemented only with psatd.update_with_rho=1"
);
```

## 多项式源项坐标

JRhom second-order 支持常量、线性、二次 `J/rho` 时间依赖。源码先把 `old/mid/new` 时间层组合成局部多项式系数：

```cpp
const Complex a_jx = (J_quadratic) ? (Jx_new - 2._rt * Jx_mid + Jx_old) : 0._rt;
const Complex b_jx = (J_linear || J_quadratic) ? (Jx_new - Jx_old) : 0._rt;
const Complex c_jx = (J_linear) ? (Jx_new + Jx_old)/2._rt : Jx_mid;

const Complex a_rho = (rho_quadratic) ? (rho_new - 2._rt * rho_mid + rho_old) : 0._rt;
const Complex b_rho = (rho_linear || rho_quadratic) ? (rho_new - rho_old) : 0._rt;
const Complex c_rho = (rho_linear) ? (rho_new + rho_old)/2._rt : rho_mid;
```

可以把它读作每个 JRhom 子区间内的源项表示：

$$
\mathbf{J}(\tau)=\mathbf{a}_J\tau^2+\mathbf{b}_J\tau+\mathbf{c}_J,
\qquad
\rho(\tau)=a_\rho\tau^2+b_\rho\tau+c_\rho.
$$

其中 $\tau$ 是源码隐含的子区间局部时间坐标。`SpectralSolver.cpp` 在 JRhom 打开时先把 solver 内部步长缩成外层 PIC 大步长的 $1/m$，因此本文件公式里的 $\Delta t$ 是子区间步长。

## 共享谱量

JRhom second-order 使用 staggered modified k 的频率：

$$
\omega_s=c|\mathbf{k}_s|,
\qquad
C=\cos(\omega_s\Delta t),
\qquad
S_{ck}=\frac{\sin(\omega_s\Delta t)}{\omega_s}.
$$

零模分支取 `S_ck = dt`。

## Y1-Y5 公式和作用面

源码中的 `Y1-Y5` 全部是实系数。非零模公式为：

$$
Y_1=
\frac{
(1-C)(8-\omega_s^2\Delta t^2)-4S_{ck}\omega_s^2\Delta t
}{
2\epsilon_0\Delta t^2\omega_s^4
},
$$

$$
Y_2=
\frac{
2(C-1)+S_{ck}\omega_s^2\Delta t
}{
2\epsilon_0\Delta t\,\omega_s^2
},
$$

$$
Y_3=
\frac{
S_{ck}\omega_s(8-\omega_s^2\Delta t^2)-4(1+C)\omega_s\Delta t
}{
2\epsilon_0\Delta t^2\omega_s^3
},
$$

$$
Y_4=
\frac{1-C}{\epsilon_0\omega_s^2},
\qquad
Y_5=
\frac{(1+C)\Delta t-2S_{ck}}
{2\epsilon_0\Delta t\,\omega_s^2}.
$$

零模分支为：

$$
Y_1=-\frac{\Delta t^2}{12\epsilon_0},\quad
Y_2=0,\quad
Y_3=-\frac{\Delta t}{6\epsilon_0},\quad
Y_4=\frac{\Delta t^2}{2\epsilon_0},\quad
Y_5=-\frac{\Delta t^2}{12\epsilon_0}.
$$

这些系数在更新式中的角色不是按编号递增的简单顺序，而是按源项多项式分工：

| 系数 | 普通推进中的主要位置 | 物理/数值角色 |
|---|---|---|
| `Y1` | `sum_rho = Y1*a_rho - Y5*b_rho - Y4*c_rho`；`B` 中 `-i*Y1*(k x a_J)`；`F` 中 `i*Y1*k dot ddJ` | 二次源项的电荷纵向项和电流旋度项 |
| `Y2` | `E` 中 `Y2*b_J`；`F` 中 `Y2*b_rho` | 一次源项对电场/cleaning 标量的贡献 |
| `Y3` | `E` 中 `Y3*a_J`；`F` 中 `Y3*a_rho` | 二次源项对电场/cleaning 标量的贡献 |
| `Y4` | `sum_rho` 中 `-Y4*c_rho`；`B` 中 `+i*Y4*(k x c_J)`；`F` 中 `-i*Y4*k dot J_mid` | 常量源项的电荷纵向项和电流旋度项 |
| `Y5` | `sum_rho` 中 `-Y5*b_rho`；`B` 中 `+i*Y5*(k x b_J)`；`F` 中 `-i*Y5*k dot dJ` | 一次源项的电荷纵向项和电流旋度项 |

电场更新式以 `Ex` 为例：

```cpp
fields(i,j,k,Idx.Ex) = C * Ex_old
    + I * c2 * S_ck * (ky * Bz_old - kz * By_old)
    + Y3 * a_jx + Y2 * b_jx - S_ck/ep0 * c_jx
    + I * c2 * kx * sum_rho;
```

磁场更新式以 `Bx` 为例：

```cpp
fields(i,j,k,Idx.Bx) = C * Bx_old
    - I * S_ck * (ky * Ez_old - kz * Ey_old)
    - I * Y1 * (ky * a_jz - kz * a_jy)
    + I * Y5 * (ky * b_jz - kz * b_jy)
    + I * Y4 * (ky * c_jz - kz * c_jy );
```

因此 JRhom `Y1-Y5` 不是 average-field 系数。它们首先服务普通 field push 中的多项式源项积分，并同时被 divergence-cleaning 标量 `F` 复用。

## Y6-Y8 和平均场累计

`Y6-Y8` 只在 time averaging 打开时存在。非零模公式为：

$$
Y_6=
\frac{
\Delta t^3\omega_s^3
-3\Delta t^2\omega_s^3S_{ck}
-12\Delta t\omega_s(1+C)
+24\omega_sS_{ck}
}{
6\epsilon_0\Delta t^2\omega_s^5
},
$$

$$
Y_7=
\frac{
\Delta t\omega_s^2S_{ck}+2C-2
}{
2\epsilon_0\Delta t\omega_s^4
},
\qquad
Y_8=
\frac{\Delta t-S_{ck}}{\epsilon_0\omega_s^2}.
$$

零模分支为：

$$
Y_6=\frac{\Delta t^3}{30\epsilon_0},\quad
Y_7=-\frac{\Delta t^3}{24\epsilon_0},\quad
Y_8=\frac{\Delta t^3}{6\epsilon_0}.
$$

平均场更新使用累加形式：

```cpp
fields(i,j,k,Idx.Ex_avg) += S_ck * Ex_old
    + I * c2 * ep0 * Y4 * (ky * Bz_old - kz * By_old)
    - I * c2 * kx * (Y6 * a_rho + Y7 * b_rho + Y8 * c_rho)
    + ( Y1 * a_jx - Y5 * b_jx - Y4 * c_jx);
```

平均磁场也用 `Y6/Y7/Y8` 对电流多项式求时间积分：

```cpp
fields(i,j,k,Idx.Bx_avg) += S_ck * Bx_old
    - I * ep0 * Y4 * (ky * Ez_old - kz * Ey_old)
    + I * (ky * (Y6 * a_jz + Y7 * b_jz + Y8 * c_jz) - kz * (Y6 * a_jy + Y7 * b_jy + Y8 * c_jy));
```

源码注释明确说这里是在 accumulating average，因为 JRhom 可配合 sub-cycling。外层 `OneStep_JRhom()` 在循环结束后调用 `PSATDScaleAverageFields(1/(2*dt[0]))`，再反变换平均场。因此 `Y6-Y8` 应读作平均场累计积分系数，而不是普通 `E/B` 更新的新源项。

## 防混写规则

- Cartesian Galilean/standard PSATD 的 `X1-X4`：普通 `E/B` 源项积分。
- Cartesian Galilean/standard PSATD 的 `Psi1/Psi2/Y1-Y4`：average-field 输出。
- JRhom second-order 的 `Y1-Y5`：多项式 `J/rho` 对普通 `E/B/F` 的解析积分。
- JRhom second-order 的 `Y6-Y8`：time-averaged field 的累计积分。
- RZ/Galilean RZ/PML PSATD 的系数属于各自算法类，不能按名字和这里的 `Y*` 直接合并。
