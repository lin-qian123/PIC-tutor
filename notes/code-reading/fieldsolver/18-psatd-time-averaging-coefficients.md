# PSATD time-averaging coefficient atlas

绑定源码：`../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp`。

本笔记只覆盖 Cartesian standard/Galilean PSATD 中的 time-averaged field 输出，也就是 `PsatdAlgorithmGalilean.cpp` 里 `time_averaging` 打开后分配的 `Psi1/Psi2/Y1/Y2/Y3/Y4`。它不覆盖 `PsatdAlgorithmJRhomSecondOrder.cpp` 中的 JRhom `Y1-Y8`，也不覆盖 RZ/Galilean RZ 或 PML PSATD 的系数表。

## 入口和前置条件

构造函数在 `time_averaging` 为真时才分配平均场系数：

```cpp
if (time_averaging)
{
    Psi1_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
    Psi2_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
    Y1_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
    Y3_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
    Y2_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
    Y4_coef = SpectralComplexCoefficients(ba, dm, 1, 0);
    InitializeSpectralCoefficientsAveraging(spectral_kspace, dm, dt);
}
```

同一构造函数还约束 `time_averaging` 必须配合 `update_with_rho`：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    !time_averaging || update_with_rho,
    "PSATD: psatd.time_averaging=1 implemented only with psatd.update_with_rho=1"
);
```

因此平均场公式不是一个只依赖 `J` 的附加输出。它必须同时保留 `rho_old/rho_new`，否则 `Y2/Y3` 没有输入。

## 共享谱量

`InitializeSpectralCoefficientsAveraging()` 使用 staggered modified k 的模长和 centered modified k 的 Galilean 频率：

$$
\omega_s=c|\mathbf{k}_s|,\qquad
\omega_c=\mathbf{k}_c\cdot\mathbf{v}_{gal}.
$$

源码中的相位和半步/三半步三角量为：

$$
\theta_c=e^{i\omega_c\Delta t/2},\quad
\theta_c^2=e^{i\omega_c\Delta t},\quad
\theta_c^3=e^{i3\omega_c\Delta t/2},\quad
\theta_c^5=e^{i5\omega_c\Delta t/2},
$$

$$
C_1=\cos(\omega_s\Delta t/2),\qquad
C_3=\cos(3\omega_s\Delta t/2),
$$

$$
S_1=\frac{\sin(\omega_s\Delta t/2)}{\omega_s},\qquad
S_3=\frac{\sin(3\omega_s\Delta t/2)}{\omega_s}.
$$

当 $\omega_s=0$ 时，源码分别取 `S1_om = 0.5*dt`、`S3_om = 1.5*dt`。

## 平均场更新式中的位置

`pushSpectralFields()` 在普通 `E/B` 更新之后，额外写入 `Ex_avg...Bz_avg`：

$$
\langle\mathbf{E}\rangle
=\Psi_1\mathbf{E}^n
-ic^2\Psi_2(\mathbf{k}\times\mathbf{B}^n)
+Y_4\mathbf{J}
+(Y_2\rho^{n+1}+Y_3\rho^n)\mathbf{k},
$$

$$
\langle\mathbf{B}\rangle
=\Psi_1\mathbf{B}^n
+i\Psi_2(\mathbf{k}\times\mathbf{E}^n)
+iY_1(\mathbf{k}\times\mathbf{J}).
$$

这里的 `avg` 是谱空间平均场分量。主循环随后在 `WarpXEvolve.cpp` 中调用 `PSATDScaleAverageFields(1/(2*dt))`，再调用 `PSATDBackwardTransformEBavg(...)` 把它们变回实空间 `Efield_avg/Bfield_avg`。所以 `Psi/Y` 系数负责的是粒子 gather 前的时间平均场，而不是替代普通 `E/B` 更新。

## Psi 系数

`Psi1` 同时乘在 `<E>` 和 `<B>` 的旧场项上：

$$
\Psi_1
=
\frac{
\theta_c^3(\omega_s^2S_3+i\omega_cC_3)
-\theta_c(\omega_s^2S_1+i\omega_cC_1)
}{
\Delta t(\omega_s^2-\omega_c^2)
}.
$$

源码在 $\omega_s=0$ 且 $\omega_c=0$ 时取 `Psi1 = 1`。

`Psi2` 乘在平均电场中的 `-i*c^2*(k x B)` 和平均磁场中的 `+i*(k x E)`：

$$
\Psi_2
=
\frac{
\theta_c^3(C_3-i\omega_cS_3)
-\theta_c(C_1-i\omega_cS_1)
}{
\Delta t(\omega_s^2-\omega_c^2)
}.
$$

源码在 $\omega_s=0$ 且 $\omega_c=0$ 时取 `Psi2 = -dt`。符号要和更新式一起读：平均电场里实际出现的是 `-i*c2*Psi2*(k x B)`。

## Y 系数

源码先定义一个内部辅助量 `Psi3`：

$$
\Psi_3=
\begin{cases}
-i(\theta_c^3-\theta_c)/(\Delta t\,\omega_c), & \omega_c\ne0,\\
1, & \omega_c=0.
\end{cases}
$$

`Y1` 只进入平均磁场的电流旋度项：

$$
Y_1=
\frac{1-\Psi_1-i\omega_c\Psi_2}{\epsilon_0(\omega_s^2-\omega_c^2)}.
$$

零模标准分支为：

$$
Y_1=\frac{13\Delta t^2}{24\epsilon_0}.
$$

`Y2` 乘 `rho_new`，`Y3` 乘 `rho_old`。在 $\omega_s\ne0$ 且 $\omega_c\ne0$ 的通用分支中：

$$
Y_2=
\frac{
ic^2(\epsilon_0\omega_s^2Y_1-\Psi_3+\Psi_1)
}{
\epsilon_0\omega_s^2(\theta_c^2-1)
},
$$

$$
Y_3=
\frac{
ic^2(\Psi_3-\Psi_1-\epsilon_0\theta_c^2\omega_s^2Y_1)
}{
\epsilon_0\omega_s^2(\theta_c^2-1)
}.
$$

标准 PSATD 非零模分支，即 $\omega_s\ne0$ 且 $\omega_c=0$，源码写成：

$$
Y_2=
\frac{ic^2(C_1-C_3-\Delta t^2\omega_s^2)}
{\epsilon_0\Delta t^2\omega_s^4},
\qquad
Y_3=
\frac{ic^2(C_3-C_1+\Delta t\omega_s^2(S_3-S_1))}
{\epsilon_0\Delta t^2\omega_s^4}.
$$

完全零模分支为：

$$
Y_2=-\frac{5ic^2\Delta t^2}{24\epsilon_0},
\qquad
Y_3=-\frac{ic^2\Delta t^2}{3\epsilon_0}.
$$

`Y4` 是平均电场中的直接电流项：

$$
Y_4=\frac{\Psi_2+i\epsilon_0\omega_cY_1}{\epsilon_0}.
$$

因此 `Y1` 和 `Y4` 都和电流有关，但作用面不同：`Y1` 进入 $\mathbf{k}\times\mathbf{J}$ 的平均磁场项，`Y4` 直接进入平均电场的 $\mathbf{J}$ 项。`Y2/Y3` 则是 charge-density 端点项，不应该和 JRhom 二阶算法里的 `Y2/Y3` 多项式电流系数混写。

## 写作边界

- `Psi/Y` 系数描述 average-field 输出；`X1-X4` 描述普通 `E/B` 推进中的源项积分。
- 这里的 `Y1-Y4` 只属于 Cartesian `PsatdAlgorithmGalilean.cpp` average-field branch。
- JRhom second-order 的 `Y1-Y8` 对应多项式 `J/rho` 源项积分，应在独立笔记中处理。
- RZ/Galilean RZ 的 time averaging 和 mode coupling 使用另一套字段结构，不能直接套用本页公式。
