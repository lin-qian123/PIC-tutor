# 06 charge-conserving current kernel structures：Esirkepov 的 shape-difference 与 Villasenor 的 segment loop

绑定源码：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`

前置阅读：

- `../notes/code-reading/particles/05-current-deposition-algorithms-near-amr-buffer.md`

上一轮已经把 AMR buffer 下不同 current deposition 算法的接口差异梳理清楚了。本文继续向下走一层：不再只看“入口传了什么参数”，而是直接看 kernel 本体里 charge-conserving 电流是怎样组织的。

本文只比较两条主线：

1. Esirkepov：old/new shape arrays 差分累加。
2. Villasenor-Buneman：按 cell crossing 切 segment，再对每段沉积。

## 1. Esirkepov 的结构核心：把 old/new shape 放到同一索引框架里做差

Esirkepov 相关 kernel 在 `CurrentDeposition.H` 里首先会同时构造新旧 shape，并让旧 shape 对齐到以 `*_new` 为参考的索引框架：

```cpp
double sx_new[depos_order + 3] = {0.};
double sx_old[depos_order + 3] = {0.};
const int i_new = compute_shape_factor(sx_new+1, x_new );
const int i_old = compute_shifted_shape_factor(sx_old, x_old, i_new);
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:881-884`。

这里的关键不是 `sx_new` 本身，而是 `compute_shifted_shape_factor`。它保证：

- `sx_new` 按新位置 `x_new` 的左端索引展开；
- `sx_old` 不再按自己的 `i_old` 独立展开；
- 而是被平移到与 `i_new` 兼容的数组框架里。

这样后面才能直接写：

```cpp
sx_old[i] - sx_new[i]
```

而不需要在 kernel 内部再做复杂的 old/new stencil 对齐。

这就是 Esirkepov 的第一个结构特征：它先把 old/new shape 写到同一离散索引语境，再用差分直接构造守恒电流。

## 2. `dil/diu`、`djl/dju`、`dkl/dku` 不是小优化，而是在裁掉不可能有贡献的边界

在 old/new shape 对齐之后，源码立刻计算：

```cpp
int dil = 1, diu = 1;
if (i_old < i_new) { dil = 0; }
if (i_old > i_new) { diu = 0; }
```

以及 `y/z` 方向对应的 `djl/dju`、`dkl/dku`。

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:939-948` 与 `1324-1333`。

这一步的作用是限定 current contribution 的最小/最大索引范围。直观上说：

- 如果 old/new stencil 向右移动了，就要把左端边界放开；
- 如果向左移动了，就要把右端边界放开；
- 如果没移动，两端都可以各收缩一个单位。

因此 `dil/diu` 不是性能微调，而是 old/new difference stencil 的真实边界控制量。

## 3. Esirkepov 的 `Jx/Jy/Jz` 都是“差分累加”而不是一次性局部写入

3D `Jx` 的主结构是：

```cpp
for (int k=dkl; k<=depos_order+2-dku; k++) {
    for (int j=djl; j<=depos_order+2-dju; j++) {
        amrex::Real sdxi = 0._rt;
        for (int i=dil; i<=depos_order+1-diu; i++) {
            sdxi += wq*invdtd.x*(sx_old[i] - sx_new[i])*(
                one_third*(sy_new[j]*sz_new[k] + sy_old[j]*sz_old[k])
               +one_sixth*(sy_new[j]*sz_old[k] + sy_old[j]*sz_new[k]));
            amrex::Gpu::Atomic::AddNoRet(&Jx_arr(...), sdxi);
        }
    }
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:951-965`。

这里最重要的是 `sdxi += ...` 这一层累加。也就是说：

- Esirkepov 不直接把每个 `i` 点的局部贡献单独写成 `this_Jx`；
- 它先沿沉积方向做前缀式累加；
- 再把这个累加结果写到 `Jx_arr`。

`Jy` 和 `Jz` 的结构完全平行，只是把差分方向换成 `y` 或 `z`。

这正是 Esirkepov “从 old/new shape 差构造满足离散连续性方程的电流”的实现痕迹。

## 4. Esirkepov 的 higher-order 支撑宽度来自 `depos_order + 3` 与 node/cell 混合平均

与直觉不同，Esirkepov 这里并不是只拿两个 `depos_order+1` 的 nodal arrays 就结束了。实际代码里：

- old/new nodal arrays 用 `depos_order + 3`
- 计算区间也走到 `depos_order + 2`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:881-883,951-986`。

这背后反映的是：

- old/new stencil 可能相对错开一个网格单位；
- mixed old-new averaging 还要在另外两个方向上组合；
- 所以最终 current support 比单次 nodal shape 的裸宽度更大。

也正因为这样，Esirkepov 的 stencil 一般会比 Villasenor 的 segment version 更“厚”。

## 5. Embedded boundary reduced shape 会直接改写 Esirkepov 的 old/new shape arrays

在 Esirkepov kernel 上游，若粒子靠近 embedded boundary，源码会把高阶 shape 擦掉，重新按一阶 shape 写入：

```cpp
if (reduce_shape_new) {
    for (int i=0; i<depos_order+3; i++) {sx_new[i] = 0.;}
    compute_shifted_shape_factor_order1( sx_new+depos_order/2, x_new, i_new+depos_order/2 );
}
if (reduce_shape_old) {
    for (int i=0; i<depos_order+3; i++) {sx_old[i] = 0.;}
    compute_shifted_shape_factor_order1( sx_old+depos_order/2, x_old, i_new+depos_order/2 );
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:885-895`。

这说明 embedded boundary 与 charge-conserving deposition 的耦合点，不是在最终 `Jx/Jy/Jz` 累加公式，而是在 old/new shape arrays 构造阶段。

因此，如果后面要同时理解：

- EB reduced shape
- AMR buffer
- Esirkepov current deposition

它们的交点首先就在这里。

## 6. Villasenor 的结构核心：先数 crossing，再按 segment 沉积

Villasenor kernel 一开头就直接声明策略：

```cpp
// 1) Determine the number of segments.
// 2) Loop over segments and deposit current.
// cell crossings are defined at cell edges if depos_order is odd
// cell crossings are defined at cell centers if depos_order is even
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1633-1637`。

随后它先计算：

```cpp
const auto i_old = static_cast<int>(x_old-shift);
const auto i_new = static_cast<int>(x_new-shift);
const int cell_crossings_x = std::abs(i_new-i_old);
num_segments += cell_crossings_x;
```

再对 `y/z` 做同样处理。

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1645-1661`。

这说明 Villasenor 的第一步不是构造 old/new shape 差，而是先明确粒子轨迹穿过了多少 cell 界面。

## 7. `shift = 0` 或 `0.5` 决定 crossing 是按 edge 还是 center 定义

源码里有一条很关键的规则：

```cpp
double shift = 0.0;
if ( (depos_order % 2) == 0 ) { shift = 0.5; }
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1640-1641`。

因此：

- 奇数阶 deposition：crossing 按 cell edge 定义；
- 偶数阶 deposition：crossing 按 cell center 定义。

这不是书写习惯，而是和奇偶阶 shape 的自然支撑中心直接对应。它决定了 Villasenor 如何把一条粒子轨迹切分成多个 segment。

## 8. Villasenor 的 segment loop 会动态决定下一个 crossing 发生在哪个方向

3D 情况下，每个 segment 并不是预先均匀切好，而是动态比较哪一个方向先撞到下一个 crossing：

```cpp
if ( (dyp == 0. || std::abs(dxp_seg) < std::abs(dxp/dyp*dyp_seg))
  && (dzp == 0. || std::abs(dxp_seg) < std::abs(dxp/dzp*dzp_seg)) ) {
    Xcell = x0_new;
    dyp_seg = dyp/dxp*dxp_seg;
    dzp_seg = dzp/dxp*dxp_seg;
    y0_new = y0_old + dyp_seg;
    z0_new = z0_old + dzp_seg;
}
else if (...) {
    ...
}
else {
    ...
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1701-1729`。

这段代码真正干的是：

- 预测沿 `x/y/z` 三个方向，哪一个界面最先被撞到；
- 用最早发生的 crossing 定义当前 segment 的终点；
- 然后把剩余轨迹继续交给下一轮 segment。

因此 Villasenor 的“按 crossing 分段”不是概念描述，而是实打实的几何分段算法。

## 9. Villasenor 为每个 segment 同时构造 cell-based 和 node-based 权重

每个 segment 内部先构造 cell-based 权重：

```cpp
const Compute_shape_factor< depos_order-1 > compute_shape_factor_cell;
...
const int i0_cell = compute_shape_factor_cell( sx_cell, x0_bar-0.5 );
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1679,1744-1748`。

然后再构造 node-based old/new 权重：

```cpp
const Compute_shape_factor_pair< depos_order > compute_shape_factors_node;
...
const int i0_node = compute_shape_factors_node( sx_old_node, sx_new_node, x0_old, x0_new );
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1680,1769-1775`。

所以 Villasenor 并不是“只用 segment 长度乘一个平均速度”。它对每个 segment 也会同时使用：

- cell-centered 权重，给沿该方向的 current 分量；
- node-centered old/new 权重，给横向混合平均。

这解释了为什么它仍然是 charge-conserving deposition，而不是简单的几何分段近似。

## 10. `depos_order >= 3` 时，Villasenor 还会对 cell-based 权重做更高阶修正

源码中有一段明确的 higher-order correction：

```cpp
if constexpr (depos_order >= 3) {
    ...
    sx_cell[m] = (4.0*sx_cell[m] + sx_old_cell[m] + sx_new_cell[m])/6.0;
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1750-1763`，以及 XZ/1D/RCYLINDER 分支对应位置。

这说明 Villasenor 的 tighter stencil 不是“低阶近似换来的更窄 stencil”。它依然保留 higher-order 修正，只是把这些修正组织在每个 segment 内，而不是像 Esirkepov 那样全程围绕 old/new shape difference 展开。

## 11. 为什么说 Villasenor 的 stencil 更紧

源码注释直接说：

- `segments are determined by cell crossings`
- `this results in a tighter stencil`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2164-2166`。

从实现上看，更紧的原因主要有两个：

1. Villasenor 只在每个真实 crossing segment 上沉积，而不是一次性把整条轨迹映射成全局 old/new difference support。
2. 每个 segment 的 cell-based 权重只围绕该段的平均位置 `x0_bar`、`y0_bar`、`z0_bar` 构造。

所以它的支持域往往比 Esirkepov 那种“old/new shape 整体差分后再累加”的方式更局部。

## 12. Esirkepov 与 Villasenor 的最小结构对照

可以把两者压缩成下面这张表：

| 维度 | Esirkepov | Villasenor |
|---|---|---|
| 第一动作 | 构造 old/new shape arrays 并对齐 | 统计 cell crossings，切分 segments |
| 主组织方式 | 沿沉积方向做差分前缀累加 | 逐 segment 沉积 |
| 关键数组 | `sx_old/sx_new`、`sy_old/sy_new`、`sz_old/sz_new` | `sx_cell`、`sx_old_node/sx_new_node` 等 |
| 边界宽度控制 | `dil/diu`、`djl/dju`、`dkl/dku` | `num_segments` 与 segment endpoint |
| EB reduced shape 耦合点 | old/new shape arrays 构造时 | 当前阅读范围内未见同等级直接改写点 |

## 13. 与 AMR buffer 的关系

这些 kernel 本体在 AMR coarse-fine buffer 下并没有换算法。变化仍然只有：

- `depos_lev`
- coarse 化后的 `tilebox`
- coarse `xyzmin/dinv`
- coarse `domain_double/do_cropping`

但一旦进入 kernel：

- Esirkepov 仍然按 old/new shape difference 累加；
- Villasenor 仍然按 crossing 切段再沉积。

因此，AMR buffer 只是改变几何解释，不改变 charge-conserving 电流的内部数学结构。

## 14. 下一步入口

这一层之后，最合理的两条接续是：

1. 继续精读 `CurrentDeposition.H` 里 Vay deposition 的 `D`-field / temporary-array 路径，解释它与 Direct / Esirkepov / Villasenor 的根本区别。
2. 转去 `Diagnostics/`，看 `current_fp/current_buf/rho_fp/rho_buf` 合并后怎样进入 multi-level diagnostics。
