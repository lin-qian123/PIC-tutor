# 42 Villasenor segment loop and Esirkepov contrast：两条 charge-conserving 路径的守恒合同相同，但组织方式完全不同

绑定源码：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`

前置阅读：

- `../notes/code-reading/particles/06-charge-conserving-current-kernel-structures.md`
- `../notes/code-reading/particles/37-direct-vs-villasenor-boundary-cropping-and-suborbit.md`
- `../notes/code-reading/particles/38-shape-factor-indexing-and-implicit-geometry-contracts.md`

第 5 章前面已经说明：

- Esirkepov 走 old/new shape difference；
- Villasenor 走 cell-crossing segmentation。

但如果正文只停在这个层级，读者仍然很难真正看懂两者的实现差异。更精确的说法应该是：它们追求的是同一条离散连续性合同，但把这条合同压进源码的方式完全不同。

## 1. Villasenor kernel 的第一动作不是构造 shape difference，而是把整条轨迹切成 segment

`VillasenorDepositionShapeNKernel(...)` 在几何恢复和 boundary crop 之后，立即写明：

```cpp
// 1) Determine the number of segments.
// 2) Loop over segments and deposit current.
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1590-1592`。

随后的第一批计算就是：

- 统计 `cell_crossings_x/y/z`
- `num_segments += cell_crossings_*`
- 根据 `dxp/dyp/dzp` 的符号初始化 `Xcell/Ycell/Zcell`

源码位置：

- 3D：`CurrentDeposition.H:1599-1636`
- XZ/RZ：`CurrentDeposition.H:1778-1804`
- 1D_Z：`CurrentDeposition.H:1902-1914`
- RCYLINDER/RSPHERE：`CurrentDeposition.H:1959-1971`

因此 Villasenor 的第一性对象不是“一对 old/new shape 数组”，而是：

- 一条从 old endpoint 到 new endpoint 的轨迹；
- 以及这条轨迹真实穿过了哪些 cell crossing。

## 2. 每个 segment 的终点是动态决定的，不是预先均匀切步长

3D 情况下，源码不会把轨迹平均切成 `num_segments` 份，而是每轮比较哪个方向先撞到下一条 crossing：

```cpp
if ( (dyp == 0. || std::abs(dxp_seg) < std::abs(dxp/dyp*dyp_seg))
  && (dzp == 0. || std::abs(dxp_seg) < std::abs(dxp/dzp*dzp_seg)) ) {
    ...
}
else if (dzp == 0. || std::abs(dyp_seg) < std::abs(dyp/dzp*dzp_seg)) {
    ...
}
else {
    ...
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1660-1678`。

这段逻辑的含义很直接：

1. 先为 x/y/z 三个方向都假设一个“下一个 crossing”；
2. 比较哪一个方向最先发生；
3. 用最早发生的 crossing 定义当前 segment 的终点；
4. 剩余轨迹再交给下一轮 segment。

所以 Villasenor 的 segment loop 不是形式化分段，而是一个真正的 crossing-driven 几何算法。

## 3. Villasenor 在每个 segment 内同时构造 cell-based 和 node-based 权重

每个 segment 都会先构造：

1. **cell-based weights**
   - 用段中心 `x0_bar/y0_bar/z0_bar` 计算；
   - 由 `Compute_shape_factor<depos_order-1>` 给出；
2. **node-based old/new weights**
   - 用段两端 `x0_old -> x0_new`、`y0_old -> y0_new`、`z0_old -> z0_new` 计算；
   - 由 `Compute_shape_factor_pair<depos_order>` 给出。

3D 主干源码：

```cpp
const Compute_shape_factor< depos_order-1 > compute_shape_factor_cell;
const Compute_shape_factor_pair< depos_order > compute_shape_factors_node;
...
const int i0_cell = compute_shape_factor_cell( sx_cell, x0_bar-0.5 );
...
const int i0_node = compute_shape_factors_node( sx_old_node, sx_new_node, x0_old, x0_new );
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1639-1708`。

也就是说，Villasenor 并不是“把 segment 长度乘一个平均速度再抹到网格上”。它对每个 segment 同时保留了：

- 主输运方向的 cell-based 支撑；
- 横向方向 old/new node 权重的对称平均。

## 4. `depos_order >= 3` 时，Villasenor 仍有 higher-order 修正，但修正在 segment 内完成

一个容易误读的地方是：Villasenor stencil 更紧，不等于它是低阶近似。源码在 `depos_order >= 3` 时还会对 cell-based weights 做更高阶修正：

```cpp
sx_cell[m] = (4.0*sx_cell[m] + sx_old_cell[m] + sx_new_cell[m])/6.0;
sy_cell[m] = (4.0*sy_cell[m] + sy_old_cell[m] + sy_new_cell[m])/6.0;
sz_cell[m] = (4.0*sz_cell[m] + sz_old_cell[m] + sz_new_cell[m])/6.0;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1689-1693`。

因此 tighter stencil 的真正来源不是“放弃高阶”，而是：

- 先按 crossing 把轨迹分段；
- 再把 higher-order 修正局部化到每个 segment 内。

## 5. Villasenor 的 `Jx/Jy/Jz` 是一组段局部写回，不是 Esirkepov 那种方向前缀累加

3D 段内沉积的代码是：

```cpp
this_Jx = wqx*sx_cell[i]*( ... )*seg_factor_x;
...
this_Jy = wqy*sy_cell[j]*( ... )*seg_factor_y;
...
this_Jz = wqz*sz_cell[k]*( ... )*seg_factor_z;
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1710-1744`。

这里每个 `this_J*` 都是：

- 当前 segment 的局部输运量；
- 乘上该段在对应方向的 `seg_factor = dt_seg/dt`；
- 再按 segment-local 的 cell/node 权重组合直接原子加回去。

这和 Esirkepov 的结构差异非常大。Esirkepov 在 3D 中写的是：

```cpp
sdxi += wq*invdtd.x*(sx_old[i] - sx_new[i])*(...)
```

也就是沿沉积方向不断累加 old/new shape difference。Villasenor 则没有 `sdxi/sdyj/sdzk` 这种“方向前缀累加变量”，它只在每个 segment 内生成局部 `this_Jx/this_Jy/this_Jz`。

## 6. 用一句话区分两条 charge-conserving 路径

如果只保留最小实现差异，可以这样概括：

1. **Esirkepov**
   - 先把整条轨迹压成 old/new shape arrays；
   - 再在统一索引框架内对 shape difference 做方向前缀累加；
   - 守恒来自差分望远镜求和。

2. **Villasenor**
   - 先把整条轨迹按真实 cell crossing 切成多个 segment；
   - 再对每个 segment 单独构造 cell/node 权重并写回局部 `this_J*`；
   - 守恒来自每一段局部输运量的逐段闭合。

两者都满足同一条离散连续性方程，但一条是“整轨迹差分累加”，另一条是“分段局部输运求和”。

## 7. 对第 5 章最值得带走的结论

第 5 章如果要把 Villasenor 讲到真正可用的程度，至少要明确下面三点：

1. 它的 tighter stencil 来自真实 crossing-driven segmentation，而不是“更粗糙的近似”。
2. 它在每个 segment 内仍保留了 higher-order cell/node 权重结构，不是只靠段长比例沉积。
3. 它和 Esirkepov 的差异不只是“一个叫 segment，一个叫 shape difference”，而是：
   - Esirkepov 把守恒压进整条轨迹的差分前缀累加；
   - Villasenor 把守恒压进每个 crossing segment 的局部输运闭合。
