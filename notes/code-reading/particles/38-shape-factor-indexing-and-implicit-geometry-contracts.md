# 38 shape factor indexing and implicit geometry contracts：`Compute_shape_factor` 三兄弟怎样真正进入 current deposition

绑定源码：

- `../warpx/Source/Particles/ShapeFactors.H`
- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`

前置阅读：

- `../notes/code-reading/particles/02-gather-shape-deposition-kernels.md`
- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`

第 5 章已经把 `Compute_shape_factor`、`Compute_shifted_shape_factor` 和 `Compute_shape_factor_pair` 介绍成 shape helper，但如果只停在“它们给权重数组”，还是不够。对 current deposition 来说，这三个 functor 实际上对应三种不同的离散合同：

1. 单时间层 shape 的左端定位；
2. Esirkepov old/new shape 的同框对齐；
3. Villasenor 单段横向 old/new 权重的共同支撑。

## 1. `Compute_shape_factor` 的真正输出不是只有权重，还有 “leftmost grid point”

`ShapeFactors.H` 开头的注释已经把 contract 说得很明确：

- compute shape factor
- return index of leftmost cell where particle writes

源码位置：`../warpx/Source/Particles/ShapeFactors.H:14-24`。

这意味着每个 specialization 都同时返回两样东西：

1. `sx[...]`
2. 该 stencil 的左端索引

例如：

- order 1 返回 `j`
- order 2 返回 `j-1`
- order 4 返回 `j-2`

current deposition 里出现的

```cpp
Jx_arr(lo.x+i_new-1+i, ...)
```

之类下标，真正的参考点就是这些 leftmost-index contract。

## 2. `Compute_shifted_shape_factor` 不是普通 old-shape helper，而是 Esirkepov 的 “同框对齐器”

`Compute_shifted_shape_factor` 的区别不在公式本身，而在它接收：

```cpp
const T x_old,
const int i_new
```

源码位置：`../warpx/Source/Particles/ShapeFactors.H:99-156`。

其核心量是：

```cpp
const int i_shift = i - i_new;
```

或高阶对应的 `i - (i_new + 1/2...)` 变体。

也就是说，它不会把 old shape 独立排到自己的左端，而是把它平移进“以 new shape 为参考”的数组坐标。对 Esirkepov 来说，这层合同比具体的 B-spline 多项式更关键，因为后面要直接做：

```cpp
sx_old[i] - sx_new[i]
```

如果 old/new 不先放到同一索引框架里，这个差分就没有离散意义。

## 3. `Compute_shape_factor_pair` 服务的是 Villasenor segment 的共同横向支撑

`Compute_shape_factor_pair` 的注释写得也很精确：

- two positions within half a grid cell of the same cell interface
- return the common index of the leftmost cell
- used transverse to the current density direction in Villasenor deposition

源码位置：`../warpx/Source/Particles/ShapeFactors.H:158-240`。

这里的关键不是“同时算 old/new 两份权重”，而是：

1. 用 `xmid = 0.5*(xnew + xold)` 决定共同参考单元；
2. 保证同一 segment 横向 old/new 权重写在同一个 local stencil 上。

这正好匹配 Villasenor 的 segment-local 电流公式：沿沉积方向看轨迹被切段；横向则必须让同一段 old/new 支撑共用一个局部坐标系。

## 4. 为什么 current deposition 里特意把这些 shape 数组声明成 `double`

`ShapeFactors.H` 文件头已经解释过一次：

- current deposition 中可用 double 参数求值；
- 这样小位移粒子的 current 仍能被稳定解析；
- 否则单精度与双精度会在某些 setup 上给出不同时间演化。

源码位置：`../warpx/Source/Particles/ShapeFactors.H:18-24`。

这条注释在 `CurrentDeposition.H` 里被真正兑现了。implicit Esirkepov 那段直接写：

```cpp
// Keep these double to avoid bug in single precision
double sx_new[depos_order + 3] = {0.};
double sx_old[depos_order + 3] = {0.};
```

以及对应的 `x_new/x_old`、`y_new/y_old`、`z_new/z_old` 也先转成 `double` 网格坐标。源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1198-1321`。

这说明 double 在这里不是“为了更高精度更好看”，而是 current deposition contract 的一部分：如果粒子一步只走很短距离，old/new shape difference 很容易变成小数减小数；不用 double，就可能把该守住的差分结构数值磨掉。

## 5. implicit Esirkepov 的几何恢复和 shape 对齐是同一条链

`doChargeConservingDepositionShapeNImplicit(...)` 的前半段不是先恢复几何、后面“顺便”算 shape，而是一条连续合同：

1. 从 `x_n` 与 `x_{n+1/2}` 恢复 `x_{n+1}`；
2. 按几何分支把 Cartesian 位置转成 `r` 或 `r,\theta,\phi`；
3. 必要时先做 `crop_at_boundary(...)`；
4. 再用 `Compute_shape_factor` / `Compute_shifted_shape_factor` 生成对齐后的 old/new stencil。

例如：

- `RZ / RCYLINDER` 先恢复 `rp_new/rp_old/rp_mid`
- `RSPHERE` 再恢复 `rpxy_mid/cosphi_mid/sinphi_mid`
- `1D_Z` 则只剩 `z` 位置，但横向速度分量仍保留在 `vx,vy`

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1191-1290`。

因此对 implicit Esirkepov 来说，shape factor functor 不是几何之后的附属工具，而是几何恢复链的最后离散化步骤。

## 6. 对第 5 章可直接带走的最小结论

第 5 章后续若再提 `ShapeFactors.H`，最有价值的不是重复 0-4 阶多项式，而是明确这三件事：

1. `Compute_shape_factor`
   - 定义单时间层权重
   - 同时返回 stencil 左端

2. `Compute_shifted_shape_factor`
   - 把 old shape 平移到以 new shape 为参考的索引框架
   - 服务 Esirkepov 的 old/new difference current

3. `Compute_shape_factor_pair`
   - 为同一 Villasenor segment 的横向 old/new 权重提供共同 leftmost index
   - 服务 tighter-stencil 的 segment-local 支撑

再加上一条数值实现边界：

- current deposition 里这些 old/new shape 和坐标经常特意升到 `double`
- 这是为了在小位移粒子上保住离散差分结构，而不是一般性的“更高精度更好”

这样，`ShapeFactors.H` 在第 5 章中的角色就不再只是“列几个 shape 公式”，而是 current deposition 真正的 indexing 和 alignment contract。
