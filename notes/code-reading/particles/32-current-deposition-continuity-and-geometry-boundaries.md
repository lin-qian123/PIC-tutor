# 32 current deposition continuity and geometry boundaries：离散连续性合同、implicit 时间层恢复与几何实现边界

绑定源码：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`

前置阅读：

- `../notes/code-reading/particles/05-current-deposition-algorithms-near-amr-buffer.md`
- `../notes/code-reading/particles/06-charge-conserving-current-kernel-structures.md`
- `../notes/code-reading/particles/07-vay-deposition-d-field-structure.md`

上一轮已经把：

- Esirkepov 的 old/new shape-difference
- Villasenor 的 segment loop
- Vay deposition 的 `D`-field 两阶段重组

分别拆开了。这里继续压另一层边界：这些 kernel 到底怎样共同服务于离散连续性方程，以及它们在 `implicit / 1D / RZ / RCYLINDER / RSPHERE` 下的真实实现边界是什么。

## 1. 第 5 章里真正要保住的不是“有几种 deposition”，而是离散连续性合同

WarpX 的电荷和电流沉积不是并列的两个小工具。源码真正要保住的合同是

$$
\frac{\rho^{n+1}_i-\rho^n_i}{\Delta t}
+(\nabla_h\cdot \mathbf{J}^{n+1/2})_i=0.
$$

如果把单个宏粒子的 nodal/cell shape 记成 `S_i(x)`，则电荷沉积是

$$
\rho_i^n=\frac{1}{\Delta V_i}\sum_p q_p w_p\,S_i(x_p^n).
$$

因此单个粒子在一步中的净电荷变化就是

$$
\rho_i^{n+1}-\rho_i^n
=
\frac{q_p w_p}{\Delta V_i}\bigl(S_i(x_p^{n+1})-S_i(x_p^n)\bigr).
$$

charge-conserving current deposition 要做的，不是“再估一个差不多的 `\mathbf J`”，而是构造某个离散电流，使得它的 divergence 恰好等于这个 shape difference 除以 `-\Delta t`。

这也是为什么 Esirkepov 和 Villasenor 的实现虽然形式差很大，但第一性目标相同：

- Esirkepov：直接在 old/new shape 差上做离散构造；
- Villasenor：先把轨迹按 crossing 切 segment，再让每段的局部电荷输运满足同一个离散守恒。

反过来说，Direct deposition 之所以不自动保证离散连续性，就是因为它直接写的是

$$
\mathbf J \sim q w \frac{\mathbf v}{\Delta V},
$$

而不是先从 `S(x^{n+1})-S(x^n)` 反推一个严格 compatible 的 divergence。

## 2. implicit charge-conserving 路径的关键不是名字，而是时间层恢复方式

`CurrentDeposition.H` 的 implicit charge-conserving 入口是：

```cpp
template <int depos_order>
void doChargeConservingDepositionShapeNImplicit (
    const amrex::ParticleReal * const xp_n,
    const amrex::ParticleReal * const yp_n,
    const amrex::ParticleReal * const zp_n,
    const GetParticlePosition<PIdx>& GetPosition,
    const amrex::ParticleReal * const wp,
    const amrex::ParticleReal * const uxp_n,
    const amrex::ParticleReal * const uyp_n,
    const amrex::ParticleReal * const uzp_n,
    const amrex::ParticleReal * const uxp_nph,
    const amrex::ParticleReal * const uyp_nph,
    const amrex::ParticleReal * const uzp_nph,
    ...
)
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1117-1140`。

这里和显式路径最根本的差别不是“implicit 更复杂”，而是沉积所需的时间层信息已经换了：

- 不再靠 `relative_time`
- 直接读 `x_n`
- 再从 `GetPosition()` 读当前的 `x_{n+1/2}`
- 同时用 `u_n` 与 `u_{n+1/2}` 恢复隐式平均的 `\gamma^{-1}`

源码里这条恢复链是：

```cpp
const amrex::ParticleReal gaminv = GetImplicitGammaInverse(uxp_n[ip], uyp_n[ip], uzp_n[ip],
                                                           uxp_nph[ip], uyp_nph[ip], uzp_nph[ip]);
...
GetPosition(ip, xp_nph, yp_nph, zp_nph);
...
const xp_np1 = 2._prt*xp_nph - xp_n[ip];
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1158-1186`。

因此，这条 implicit charge-conserving 路径的数学意义很明确：

1. 先恢复一步完整轨迹 `x_n -> x_{n+1} `
2. 再把这个完整轨迹喂给 charge-conserving deposition

也就是说，implicit 不是改变了守恒合同本身，而是改变了“如何重建满足该合同的轨迹端点”。

## 3. Villasenor explicit/implicit 的第一层差异，也是在时间层恢复，而不是在 segment 数学

显式 Villasenor 的入口：

```cpp
template <int depos_order>
void doVillasenorDepositionShapeNExplicit (...,
                                           const amrex::Real dt,
                                           const amrex::Real relative_time,
                                           ...)
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2189-2209`。

它的 old/new 端点是从当前位置和 `relative_time` 回推：

```cpp
amrex::Real const xp_new = xp + (relative_time + 0.5_rt*dt)*uxp[ip]*gaminv;
amrex::Real const xp_old = xp_new - dt*uxp[ip]*gaminv;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2236-2241`。

隐式 Villasenor 则完全换成了 `x_n + x_{n+1/2} + u_n/u_{n+1/2}` 的恢复链：

```cpp
template <int depos_order>
void doVillasenorDepositionShapeNImplicit (
    const amrex::ParticleReal * const xp_n_data,
    ...
    const amrex::ParticleReal * const uxp_n,
    ...
    const amrex::ParticleReal * const uxp_nph,
    ...)
```

以及

```cpp
const amrex::ParticleReal gaminv = GetImplicitGammaInverse(...);
...
const amrex::ParticleReal xp_np1 = 2._prt*xp_nph - xp_n;
```

源码位置：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H:2281-2306`
- `../warpx/Source/Particles/Deposition/CurrentDeposition.H:2327-2350`

所以，对 Villasenor 来说：

- `explicit/implicit` 的第一层分界是“如何恢复轨迹端点”
- 不是“segment-by-segment 数学被改写了”

segment decomposition 本身在两条线上都保留。

## 4. 几何边界不是隐藏在上层；`CurrentDeposition.H` 里直接写死了哪些维度能用

这部分最容易被忽略，因为上层 `DepositCurrent()` 的算法分派看起来是通用模板。但在 kernel 里，维度边界是直接 `abort` 或 `#if` 切掉的。

### 4.1 Vay deposition 的几何边界最硬

Vay 的入口内部直接写：

```cpp
#if defined(WARPX_DIM_RZ)
    WARPX_ABORT_WITH_MESSAGE("Vay deposition not implemented in RZ geometry");
#endif

#if defined(WARPX_DIM_1D_Z) || defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    WARPX_ABORT_WITH_MESSAGE("Vay deposition not implemented in 1D geometry");
#endif
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2406-2417`。

因此当前 worktree 下，Vay deposition 的真实实现边界是：

- 支持：
  - `3D`
  - `XZ`
- 不支持：
  - `RZ`
  - `1D_Z`
  - `RCYLINDER`
  - `RSPHERE`

这不是文档级建议，而是源码级 `abort`。

### 4.2 implicit charge-conserving 与 Villasenor 反而把这些几何显式展开了

`doChargeConservingDepositionShapeNImplicit()` 里直接把各几何分开处理：

- `RZ / RCYLINDER`
  - 先从 `(x,y)` 恢复半径 `r`
  - 再用 `costheta/sintheta` 重建分量
- `RSPHERE`
  - 再进一步从 `(x,y,z)` 恢复 `r,\theta,\phi`
- `1D_Z`
  - 只保留 `z` 方向位置，但仍允许横向动量分量参与 `vx,vy`

例如：

```cpp
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
    ...
    const amrex::Real costheta_mid = (rp_mid > 0._rt ? xp_mid/rp_mid : 1._rt);
    const amrex::Real sintheta_mid = (rp_mid > 0._rt ? yp_mid/rp_mid : 0._rt);
```

以及：

```cpp
#elif defined(WARPX_DIM_RSPHERE)
    ...
    const amrex::Real cosphi_mid = (rp_mid > 0. ? rpxy_mid/rp_mid : 1._rt);
    const amrex::Real sinphi_mid = (rp_mid > 0. ? zp_mid/rp_mid : 0._rt);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1191-1237`。

同样，Villasenor 的 segment kernel 也明确区分：

- `XZ / RZ`
- `1D_Z`
- `RCYLINDER / RSPHERE`

源码位置可从：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H:1578-1624`
- `../warpx/Source/Particles/Deposition/CurrentDeposition.H:2000-2079`

直接看出。

因此，几何差异不是“调用层统一、底层自然适配”这么简单，而是 deposition kernel 内部就已经把不同几何的坐标重建和支撑域组织写死了。

## 5. `1D_Z` 的一个容易误解的点：位置是一维，电流合同不只剩 `J_z`

源码里多处出现：

```cpp
#elif defined(WARPX_DIM_1D_Z)
    amrex::Real const vx = uxp_nph[ip]*gaminv;
    amrex::Real const vy = uyp_nph[ip]*gaminv;
```

源码位置：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H:1260-1261`
- 类似逻辑在显式路径也有

这说明 `1D_Z` 的限制是空间网格只剩 `z` 方向，不等于粒子速度空间只剩一个分量。对 deposition 来说：

- 轨迹支撑域只在 `z` 方向展开；
- 但横向速度分量仍可能进入某些 current 分量的几何解释。

这和 Birdsall 里 `1d2v/1d3v` 的边界是一致的：低空间维度不等于低速度维度。

## 6. 这几条实现边界和离散连续性合同怎样接起来

现在可以把这条主线压成一句更准确的话：

- **离散连续性合同** 决定了为什么必须有 charge-conserving deposition；
- **时间层恢复方式** 决定了显式/隐式路径怎样重建 `x_n -> x_{n+1}`；
- **几何编译分支** 决定了这些合同在哪些维度上有实现、以哪种坐标重建方式实现。

所以第 5 章后面讲 `CurrentDeposition.H` 时，不能只按算法名字排目录。更稳定的组织方式是：

1. 先讲离散连续性合同
2. 再讲：
   - Direct
   - Esirkepov
   - Villasenor
   - Vay
3. 最后再单独讲：
   - implicit 时间层恢复
   - `RZ/RCYLINDER/RSPHERE/1D_Z` 的几何实现边界

## 7. 当前最小结论

这轮补完后，第 5 章里关于 current deposition 的剩余 hard boundary 已经能压成：

1. Direct 不自动保证离散连续性。
2. Esirkepov / Villasenor 的第一性目标相同，都是让 `(\rho^{n+1}-\rho^n)/\Delta t + \nabla_h\cdot J = 0` 成立。
3. implicit 路线没有改写这个守恒目标，只是改写了轨迹端点恢复方式。
4. Vay deposition 是显式-only 且只在 `3D/XZ` 有实现的两阶段 `D`-field 重组算法。
5. `RZ/1D/RCYLINDER/RSPHERE` 的 current deposition 不是统一模板自动适配，而是 kernel 内部显式几何分支。

## 8. 下一步入口

最自然的下一步有两条：

1. 把这条“离散连续性合同 + 时间层恢复 + 几何边界”回填到 `manuscript/chapters/05-deposition-shapes.md`。
2. 然后继续下钻：
   - `MassMatricesDeposition.H`
   - temperature deposition
   - variance accumulation
