# 39 current deposition writeback rules in 1D_Z, RCYLINDER, RSPHERE：几何分支不只决定坐标恢复，还决定 `J` 三分量的写回规则

绑定源码：

- `../warpx/Source/Particles/Deposition/CurrentDeposition.H`

前置阅读：

- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`
- `../notes/code-reading/particles/38-shape-factor-indexing-and-implicit-geometry-contracts.md`

第 5 章前面已经说明：`1D_Z / RCYLINDER / RSPHERE` 的 current deposition 不是统一模板自动适配，而是 kernel 内部显式分支。但如果只写到“有几何分支”，还不够。真正影响读者理解的是：这些分支不只决定如何恢复 `x_old/x_new` 或 `r_old/r_new`，还直接决定 `Jx/Jy/Jz` 三个分量分别按什么离散形式写回网格。

## 1. implicit Esirkepov：`1D_Z` 下 `Jx/Jy` 是横向平均，`Jz` 才是守恒差分累加

`doChargeConservingDepositionShapeNImplicit(...)` 的 `1D_Z` 写回分支是：

```cpp
for (int k=dkl; k<=depos_order+2-dku; k++) {
    amrex::Real const sdxi = wq*vx*invvol*0.5_rt*(sz_old[k] + sz_new[k]);
    ... Jx_arr(...)
}
for (int k=dkl; k<=depos_order+2-dku; k++) {
    amrex::Real const sdyj = wq*vy*invvol*0.5_rt*(sz_old[k] + sz_new[k]);
    ... Jy_arr(...)
}
amrex::Real sdzk = 0._rt;
for (int k=dkl; k<=depos_order+1-dku; k++) {
    sdzk += wq*invdtd.z*(sz_old[k] - sz_new[k]);
    ... Jz_arr(...)
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1439-1453`。

所以 `1D_Z` 的真正语义不是“空间一维，因此只剩 `Jz`”，而是：

- `Jx/Jy`
  - 仍然可以非零
  - 但它们不承担一维连续性方程里的 divergence difference
  - 写回时只用 old/new node weight 的平均 `0.5*(sz_old+sz_new)`
- `Jz`
  - 才是沿唯一空间方向承担守恒合同的分量
  - 因而走 `sz_old - sz_new` 的前缀累加结构

也就是说，`1D_Z` 是“空间网格一维”，不是“速度和电流物理上只剩一个分量”。

## 2. Villasenor `1D_Z`：同样是 `Jx/Jy` 平均、`Jz` 沿 segment cell weights 写回

Villasenor 的 `1D_Z` segment kernel 则写成：

```cpp
for (int k=0; k<=depos_order; k++) {
    const amrex::Real weight = 0.5_rt*(sz_old_node[k] + sz_new_node[k])*seg_factor;
    ... Jx_arr(..., wqx*weight);
    ... Jy_arr(..., wqy*weight);
}

for (int k=0; k<=depos_order-1; k++) {
    const amrex::Real this_Jz = wqz*sz_cell[k]*seg_factor;
    ... Jz_arr(..., this_Jz);
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2030-2059`。

这和 Esirkepov 在物理语义上是对齐的：

- `Jx/Jy` 都是 out-of-plane current，走横向平均 node weights
- `Jz` 才是 segment-local 的主输运方向，走 cell-based weights

区别只是：

- Esirkepov 用 old/new difference 的守恒累加
- Villasenor 用 segment decomposition 后的局部 `sz_cell` 写回

## 3. implicit Esirkepov：`RCYLINDER/RSPHERE` 下只有径向分量走守恒差分

`RCYLINDER / RSPHERE` 分支的 implicit Esirkepov 写回是：

```cpp
amrex::Real sdri = 0._rt;
for (int i=dil; i<=depos_order+1-diu; i++) {
    sdri += wq*invdtd.x*(sx_old[i] - sx_new[i]);
    ... Jx_arr(...)
}
for (int i=dil; i<=depos_order+2-diu; i++) {
    amrex::Real const sdyj = wq*vy*invvol*0.5_rt*(sx_old[i] + sx_new[i]);
    ... Jy_arr(...)
}
for (int i=dil; i<=depos_order+2-diu; i++) {
    amrex::Real const sdzk = wq*vz*invvol*0.5_rt*(sx_old[i] + sx_new[i]);
    ... Jz_arr(...)
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:1455-1469`。

这里的分工非常清楚：

- `Jx`
  - 在这两个几何分支里实际上是径向 `J_r`
  - 因为唯一空间支撑方向是径向，所以它承担守恒差分，走 `sx_old - sx_new`
- `Jy/Jz`
  - 分别对应角向/切向分量
  - 不承担径向 divergence 的主差分
  - 因而走 `0.5*(sx_old + sx_new)` 的平均写回

因此第 5 章不能把这两条分支粗写成“球/柱坐标下也一样沉 `Jx/Jy/Jz`”。更准确的说法应是：

- 变量名仍叫 `Jx/Jy/Jz`
- 但在 `RCYLINDER / RSPHERE` 里它们的物理角色已经变成 `J_r` 与两个切向分量

## 4. Villasenor `RCYLINDER/RSPHERE`：同样是“径向 cell weight，切向 node-average”

Villasenor 对应分支写成：

```cpp
for (int i=0; i<=depos_order; i++) {
    const amrex::Real weight = 0.5_rt*(sx_old_node[i] + sx_new_node[i])*seg_factor;
    ... Jy_arr(..., wqy*weight);
    ... Jz_arr(..., wqz*weight);
}

for (int i=0; i<=depos_order-1; i++) {
    const amrex::Real this_Jx = wqx*sx_cell[i]*seg_factor;
    ... Jx_arr(..., this_Jx);
}
```

源码位置：`../warpx/Source/Particles/Deposition/CurrentDeposition.H:2126-2145`。

所以它和 Esirkepov 保持了同一层物理分工：

- 径向主输运分量 `Jx/J_r`
  - 走沿轨迹段的 cell-based deposition
- 两个切向分量 `Jy/Jz`
  - 走 node-average 的横向权重

不同点仍是：

- Esirkepov：用 old/new difference 累加出守恒主分量
- Villasenor：先把径向轨迹切段，再对每段用 `sx_cell` 局部写回

## 5. 对第 5 章最值得带走的结论

第 5 章如果要把几何分支讲到真正可用的粒度，至少要明确下面两条：

1. `1D_Z`
   - 不是只剩 `Jz`
   - `Jx/Jy` 仍存在，但作为 out-of-plane 分量只走 old/new 平均
   - `Jz` 才承担一维守恒输运

2. `RCYLINDER / RSPHERE`
   - 变量名虽然还是 `Jx/Jy/Jz`
   - 但 `Jx` 已经承担径向主输运角色
   - `Jy/Jz` 是切向分量，写回规则与径向分量不同

因此这些几何分支真正改变的不是“先恢复什么坐标”这么简单，而是：

- 哪个分量承担连续性方程的主差分；
- 哪些分量只沿横向平均写回；
- Villasenor segment kernel 里的 cell/node 权重该分派给哪一组物理分量。
