# PSATD Galilean 系数、current correction 与 Vay spectral deposition 精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记接在 `05-psatd-spectral-flow.md` 之后，聚焦标准/Galilean PSATD 的统一实现：

- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.H`
- `../warpx/Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmGalilean.cpp`
- `../warpx/Docs/source/usage/parameters.rst:3400-3538`

本篇暂不展开 JRhom first/second order，也不展开 RZ Hankel transform。

## 1. 类边界：标准 PSATD 也走 Galilean 类

`PsatdAlgorithmGalilean.H` 说明这个类负责在谱空间更新场并保存更新系数：

```cpp
class PsatdAlgorithmGalilean : public SpectralBaseAlgorithm
{
    public:
        void pushSpectralFields (SpectralFieldData& f) const final;
        void InitializeSpectralCoefficients (
            const SpectralKSpace& spectral_kspace,
            const amrex::DistributionMapping& dm,
            amrex::Real dt);
        void InitializeSpectralCoefficientsAveraging (
            const SpectralKSpace& spectral_kspace,
            const amrex::DistributionMapping& dm,
            amrex::Real dt);
        void CurrentCorrection (SpectralFieldData& field_data) final;
        void VayDeposition (SpectralFieldData& field_data) final;
```

成员系数分为两组：

```cpp
// These real and complex coefficients are always allocated
SpectralRealCoefficients C_coef, S_ck_coef;
SpectralComplexCoefficients T2_coef, X1_coef, X2_coef, X3_coef, X4_coef;

// These real and complex coefficients are allocated only with averaged Galilean PSATD
SpectralComplexCoefficients Psi1_coef, Psi2_coef, Y1_coef, Y2_coef, Y3_coef, Y4_coef;
```

这解释了 `05` 中看到的更新式：普通推进用 `C/S_ck/T2/X1-X4`，时间平均输出 `<E>/<B>` 还需要 `Psi/Y` 系数。

标准 PSATD 是这个类的特例：当 `psatd.v_galilean = 0`，源码中 `w_c = k_c\cdot v_G = 0`，`T2=1`，Galilean 相位因子退化。

## 2. `w_c` 必须用 centered modified k

`InitializeSpectralCoefficients()` 的第一件事是同时取 staggered 和 centered modified k：

```cpp
const amrex::Real* kx_s = modified_kx_vec[mfi].dataPtr();
const amrex::Real* kx_c = modified_kx_vec_centered[mfi].dataPtr();
#if defined(WARPX_DIM_3D)
const amrex::Real* ky_s = modified_ky_vec[mfi].dataPtr();
const amrex::Real* ky_c = modified_ky_vec_centered[mfi].dataPtr();
#endif
const amrex::Real* kz_s = modified_kz_vec[mfi].dataPtr();
const amrex::Real* kz_c = modified_kz_vec_centered[mfi].dataPtr();
```

然后用 centered modified k 计算 Galilean 频率：

```cpp
const amrex::Real w_c = kx_c[i]*vg_x +
#if defined(WARPX_DIM_3D)
    ky_c[j]*vg_y + kz_c[k]*vg_z;
#else
    kz_c[j]*vg_z;
#endif
```

源码注释说明原因：

```cpp
// This has to be computed always with the centered (collocated) finite-order
// modified k vectors, to work correctly for both collocated and staggered grids.
// w_c = 0 always with standard PSATD (zero Galilean velocity).
```

物理上，$w_c=\mathbf k_c\cdot\mathbf v_G$ 是 Galilean 坐标中网格相对等离子体漂移带来的相位频率。即使 E/B 存在 staggered modified k，Galilean 平移相位也必须用 collocated 位置的 k 表示。

## 3. 基础系数：`C`、`S_ck`、`T2`

谱空间波数模长：

```cpp
const amrex::Real knorm_s = std::sqrt(
    amrex::Math::powi<2>(kx_s[i]) +
#if defined(WARPX_DIM_3D)
    amrex::Math::powi<2>(ky_s[j]) + amrex::Math::powi<2>(kz_s[k]));
#else
    amrex::Math::powi<2>(kz_s[j]));
#endif
```

然后：

```cpp
const amrex::Real om_s = c * knorm_s;
const amrex::Real om2_s = amrex::Math::powi<2>(om_s);

const Complex theta_c      = amrex::exp( I * w_c * dt * 0.5_rt);
const Complex theta2_c     = amrex::exp( I * w_c * dt);
const Complex theta_c_star = amrex::exp(-I * w_c * dt * 0.5_rt);

C(i,j,k) = std::cos(om_s * dt);
```

`S_ck` 是 $\sin(\omega\Delta t)/\omega$，但零模时取极限 $\Delta t$：

```cpp
if (om_s != 0.)
{
    S_ck(i,j,k) = std::sin(om_s * dt) / om_s;
}
else // om_s = 0
{
    S_ck(i,j,k) = dt;
}
```

`T2` 是 Galilean 相位：

```cpp
T2(i,j,k) = theta_c * theta_c;
```

即

$$
T_2=e^{i(\mathbf k_c\cdot\mathbf v_G)\Delta t}.
$$

标准 PSATD 中 $v_G=0$，所以 $T_2=1$。

## 4. `X1-X4`：把 J/rho 项折叠进 E/B 更新

源码中的辅助变量：

```cpp
const amrex::Real tmp = (om_s != 0.)?
    ((1._rt - C(i,j,k)) / (ep0 * om2_s)):(0.5_rt * dt2 / ep0);
```

`X1` 乘在 B 更新中的 $i(\mathbf k\times\mathbf J)$ 项上：

```cpp
if ((om_s != 0.) || (w_c != 0.))
{
    X1(i,j,k) = (1._rt - theta2_c * C(i,j,k) + I * w_c * theta2_c * S_ck(i,j,k))
                / (ep0 * (om2_s - w2_c));
}
else
{
    X1(i,j,k) = 0.5_rt * dt2 / ep0;
}
```

`X2` 和 `X3` 分别乘在 E 更新中的 `rho_new` 和 `rho_old` 上：

```cpp
if (w_c != 0.)
{
    X2(i,j,k) = c2 * (theta_c_star * X1(i,j,k) - theta_c * tmp)
                / (theta_c_star - theta_c);
}
else
{
    if (om_s != 0.)
    {
        X2(i,j,k) = c2 * (dt - S_ck(i,j,k)) / (ep0 * dt * om2_s);
    }
    else
    {
        X2(i,j,k) = c2 * dt2 / (6._rt * ep0);
    }
}
```

```cpp
if (w_c != 0.)
{
    X3(i,j,k) = c2 * (theta_c_star * X1(i,j,k) - theta_c_star * tmp)
                / (theta_c_star - theta_c);
}
else
{
    if (om_s != 0.)
    {
        X3(i,j,k) = c2 * (dt * C(i,j,k) - S_ck(i,j,k)) / (ep0 * dt * om2_s);
    }
    else
    {
        X3(i,j,k) = - c2 * dt2 / (3._rt * ep0);
    }
}
```

`X4` 乘在 E 更新中的 J 项：

```cpp
X4(i,j,k) = I * w_c * X1(i,j,k) - theta2_c * S_ck(i,j,k) / ep0;
```

这些分支都在处理两个奇异极限：

- $k\to0$，即 $\omega_s=ck_s\to0$。
- $\omega_s^2-w_c^2\to0$ 或 $w_c\to0$。

源码没有用单一公式硬算，而是给零模/标准 PSATD 极限单独表达式，避免除零和数值不稳定。

## 5. 更新式中的系数位置

`pushSpectralFields()` 中 E 的 x 分量更新为：

```cpp
fields(i,j,k,Idx.Ex) = T2 * C * Ex_old
                       + I * c2 * T2 * S_ck * (ky * Bz_old - kz * By_old)
                       + X4 * Jx - I * (X2 * rho_new - T2 * X3 * rho_old) * kx;
```

B 的 x 分量更新为：

```cpp
fields(i,j,k,Idx.Bx) = T2 * C * Bx_old
                       - I * T2 * S_ck * (ky * Ez_old - kz * Ey_old)
                       + I * X1 * (ky * Jz - kz * Jy);
```

逐项对应：

- `T2*C*E_old/B_old`：Galilean 相位加电磁自由振荡。
- `I*c2*T2*S_ck*(k cross B)`：Ampere 方程的 curl(B) 解析积分。
- `-I*T2*S_ck*(k cross E)`：Faraday 方程的 curl(E) 解析积分。
- `X4*J`：电流横向/源项贡献。
- `X2/X3*rho*k`：用 `rho_new/rho_old` 写出的纵向场贡献。
- `I*X1*(k cross J)`：电流对磁场的贡献。

当 `update_with_rho=false`，源码先从 Gauss 定律与连续性重构 rho：

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

所以 `psatd.update_with_rho=0` 并不是忽略电荷密度，而是把电荷密度作为谱空间约束量重构。

## 6. current correction：文档公式与源码逐项对应

官方参数文档给出标准 PSATD current correction：

```rst
\widehat{\boldsymbol{J}}^{\,n+1/2}_{\mathrm{correct}} = \widehat{\boldsymbol{J}}^{\,n+1/2}
- \bigg(\boldsymbol{k}\cdot\widehat{\boldsymbol{J}}^{\,n+1/2}
- i \frac{\widehat{\rho}^{n+1} - \widehat{\rho}^{n}}{\Delta{t}}\bigg) \frac{\boldsymbol{k}}{k^2}
```

Galilean 版本：

```rst
\widehat{\boldsymbol{J}}^{\,n+1/2}_{\mathrm{correct}} = \widehat{\boldsymbol{J}}^{\,n+1/2}
- \bigg(\boldsymbol{k}\cdot\widehat{\boldsymbol{J}}^{\,n+1/2} - (\boldsymbol{k}\cdot\boldsymbol{v}_G)
\,\frac{\widehat\rho^{n+1} - \widehat\rho^{n}\theta^2}{1 - \theta^2}\bigg) \frac{\boldsymbol{k}}{k^2}
```

源码位置：`PsatdAlgorithmGalilean.cpp:634-730`。

```cpp
const Complex k_dot_J = kx * Jx + ky * Jy + kz * Jz;
const amrex::Real k_dot_vg = kx_c * vgx + ky_c * vgy + kz_c * vgz;

if ( k_dot_vg != 0._rt )
{
    const Complex rho_old_mod = rho_old * amrex::exp(I * k_dot_vg * dt);
    const Complex den = 1._rt - amrex::exp(I * k_dot_vg * dt);

    fields(i,j,k,Idx.Jx_mid) = Jx - (k_dot_J - k_dot_vg * (rho_new - rho_old_mod) / den)
        * kx / (k_norm * k_norm);
```

标准分支：

```cpp
else
{
    fields(i,j,k,Idx.Jx_mid) = Jx - (k_dot_J - I * (rho_new - rho_old) / dt)
        * kx / (k_norm * k_norm);
```

对应关系：

- `k_dot_J` 是 $\mathbf k\cdot\widehat{\mathbf J}$。
- `rho_old_mod = rho_old * exp(i k_dot_vg dt)` 是文档里的 $\rho^n\theta^2$。
- `den = 1 - exp(i k_dot_vg dt)` 是 $1-\theta^2$。
- `* kx / (k_norm*k_norm)` 是投影到 $\mathbf k/k^2$。

`k_norm==0` 时源码不修正，这避免零模除以 $k^2$。

## 7. Vay spectral deposition：从 cumulative D 到 J

`VayDeposition()` 在 `PushPSATD()` 的 Vay 分支中被调用。这里输入到 `Idx.J*_mid` 的不是普通电流，而是 spectral D/cumulative quantity。源码把它除以 modified k 并乘 $i$：

```cpp
const Complex Dx = fields(i,j,k,Idx.Jx_mid);
#if defined(WARPX_DIM_3D)
const Complex Dy = fields(i,j,k,Idx.Jy_mid);
#endif
const Complex Dz = fields(i,j,k,Idx.Jz_mid);
```

```cpp
if (kx_mod != 0._rt) { fields(i,j,k,Idx.Jx_mid) = I * Dx / kx_mod; }
else                 { fields(i,j,k,Idx.Jx_mid) = 0._rt; }
```

这不是完整的 Vay deposition 物理推导，只是谱求解器侧的转换步骤。真实的 particle-side cumulative deposition 和 `PSATDSubtractCurrentPartialSumsAvg()` 还需要回到粒子沉积章节继续追。

## 8. 时间平均系数的边界

`InitializeSpectralCoefficientsAveraging()` 只在 `psatd.do_time_averaging=1` 时分配并使用 `Psi1/Psi2/Y1-Y4`。这些系数对应 `<E>/<B>` 的时间平均输出：

```cpp
fields(i,j,k,Idx.Ex_avg) = Psi1 * Ex_old
                           - I * c2 * Psi2 * (ky * Bz_old - kz * By_old)
                           + Y4 * Jx + (Y2 * rho_new + Y3 * rho_old) * kx;
```

系数初始化中同样存在多种零模/极限分支：

```cpp
if ((om_s != 0.) || (w_c != 0.))
{
    Psi1(i,j,k) = (theta3_c * (om2_s * S3_om + I * w_c * C3)
                  - theta_c * (om2_s * S1_om + I * w_c * C1)) / (dt * (om2_s - w2_c));
}
else
{
    Psi1(i,j,k) = 1._rt;
}
```

本笔记只记录时间平均的入口和边界；完整系数推导需要对照 Lehe 2016 / WarpX 文档中的 averaged Galilean PSATD 公式继续展开。

## 9. 已确认边界

- `current_correction` 文档明确说尚未用于 PSATD JRhom；源码中 JRhom 是独立算法类。
- `psatd.update_with_rho=0` 与 comoving、time averaging、divE cleaning、JRhom 不兼容，文档中已有约束。
- `v_galilean` 非零要求 direct current deposition；这个约束来自参数文档，后续要回到 `WarpX.cpp` 参数检查确认。
- `VayDeposition()` 的谱侧只做 `J=iD/k` 转换，粒子侧和 cumulative sums 需单独读。

下一步应进入：

- `PsatdAlgorithmJRhomFirstOrder.cpp` / `SecondOrder.cpp`，把 `OneStep_JRhom()` 的多次沉积与谱系数对应起来。
- `SpectralSolverRZ.cpp`、`SpectralKSpaceRZ.cpp` 和 Hankel transform。
