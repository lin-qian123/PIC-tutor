# Boundary 04: Silver-Mueller 内部公式与 stencil

绑定源码：

- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.H`
- `../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp`
- `../warpx/Docs/source/usage/parameters.rst`

## 1. 入口与调用位置

`FiniteDifferenceSolver` 提供的接口是：

```cpp
void ApplySilverMuellerBoundary (
    ablastr::fields::VectorField & Efield,
    ablastr::fields::VectorField & Bfield,
    amrex::Box domain_box,
    amrex::Real dt,
    amrex::Array<FieldBoundaryType,AMREX_SPACEDIM> field_boundary_lo,
    amrex::Array<FieldBoundaryType,AMREX_SPACEDIM> field_boundary_hi);
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.H:87-93`。

它在主循环中的调用位置仍然只有一处：

```cpp
if (lev == 0) {
    if (subcycling_half == SubcyclingHalf::FirstHalf) {
        if(::isAnyBoundary<FieldBoundaryType::Absorbing_SilverMueller>(...)){
            m_fdtd_solver_fp[0]->ApplySilverMuellerBoundary(...);
        }
    }
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp:231-239`。

所以这不是通用边界后处理，而是显式 FDTD/Yee 路径里专门更新 `B` 的边界 guard cell。

## 2. Solver 级约束

函数开头先做硬约束：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    m_fdtd_algo == ElectromagneticSolverAlgo::Yee,
    "The Silver-Mueller boundary conditions can only be used with the Yee solver."
);
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:51-55`。

这和参数文档完全一致：`absorbing_silver_mueller` 只支持 Yee Maxwell solver。见 `../warpx/Docs/source/usage/parameters.rst:779-781`。

## 3. 它更新的不是域内边界 cell，而是“最内侧 guard cell”

函数先把传入 `domain_box` 转成 cell-centered physical domain：

```cpp
domain_box.enclosedCells();
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:57-58`。

随后对 `Bfield` 的 tilebox 全部 `grow(1)`：

```cpp
tbx.grow(1);
tby.grow(1);
tbz.grow(1);
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:270-275`。

源码注释已经写明：

- 要修改的是 first / innermost guard cell
- 不是物理域内最后一个有效 cell

这点很关键。Silver-Mueller 在 WarpX 里的实现不是把边界条件直接写到域内最后一层 `B` 上，而是通过更新边界外第一层 guard cell，让后续 FDTD 更新与 fill boundary 读到“满足吸收关系”的外侧值。

## 4. 系数结构

Cartesian / XZ / 1D 分支里，先为每个方向构造：

```cpp
amrex::Real const cdt_over_dx = PhysConst::c*dt*m_h_stencil_coefs_x[0];
amrex::Real const coef1_x = (1._rt - cdt_over_dx)/(1._rt + cdt_over_dx);
amrex::Real const coef2_x = 2._rt*cdt_over_dx/(1._rt + cdt_over_dx) / PhysConst::c;
```

对应 y、z 方向也有同型系数。源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:218-231`。

这可以直接理解成一维出射波关系离散后的两项结构：

- `coef1_*` 乘边界 guard cell 现有 `B`
- `coef2_*` 乘切向 `E`

因此 Silver-Mueller 在这里不是“纯置值”，而是一步显式递推更新。

## 5. 哪些方向真正应用

每个方向是否应用由 `field_boundary_lo/hi` 逐轴判断：

```cpp
bool const apply_lo_x = (field_boundary_lo[0] == FieldBoundaryType::Absorbing_SilverMueller);
bool const apply_hi_x = (field_boundary_hi[0] == FieldBoundaryType::Absorbing_SilverMueller);
...
bool const apply_lo_z = (field_boundary_lo[WARPX_ZINDEX] == FieldBoundaryType::Absorbing_SilverMueller);
bool const apply_hi_z = (field_boundary_hi[WARPX_ZINDEX] == FieldBoundaryType::Absorbing_SilverMueller);
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:233-242`。

这说明 Silver-Mueller 在 WarpX 中是按“哪一侧边界声明为 `absorbing_silver_mueller`”逐侧生效的，而不是某个 solver 全局开关。

## 6. 3D / XZ / 1D 的 stencil 形态

Cartesian 分支直接对 `Bx / By / Bz` 三个分量逐个更新。

### 6.1 `Bx`

例如 3D 在 `+z` 边界：

```cpp
if ( apply_hi_z && ( k==domain_box.bigEnd(2)+1 ) ) {
    Bx(i,j,k) = coef1_z * Bx(i,j,k) - coef2_z * Ey(i,j,k);
}
```

在 `-z` 边界：

```cpp
if ( apply_lo_z && ( k==domain_box.smallEnd(2)-1 ) ) {
    Bx(i,j,k) = coef1_z * Bx(i,j,k) + coef2_z * Ey(i,j,k+1);
}
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:292-299`。

这体现了两个离散细节：

1. `+`/`-` 边界符号相反；
2. low 边界用域内相邻 `Ey(...,k+1)`，high 边界直接用 `Ey(...,k)`，本质上是按 Yee 交错关系分别取边界内侧切向电场。

### 6.2 `By`

例如 3D 在 `+x` 边界：

```cpp
if ( apply_hi_x && ( i==domain_box.bigEnd(0)+1 ) ) {
    By(i,j,k) = coef1_x * By(i,j,k) - coef2_x * Ez(i,j,k);
}
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:324-332`。

### 6.3 `Bz`

例如 3D 在 `+y` 边界：

```cpp
if ( apply_hi_y && ( j==domain_box.bigEnd(1)+1 ) ) {
    Bz(i,j,k) = coef1_y * Bz(i,j,k) - coef2_y * Ex(i,j,k);
}
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:377-385`。

整体规律很统一：

- 某个法向方向的 Silver-Mueller 条件，更新与该法向正交的两个 `B` 分量；
- 每个 `B_t` 只耦合一个对应切向 `E`；
- 形式都是 `B_t^{guard,new} = coef1 * B_t^{guard,old} +/- coef2 * E_t^{inside}`。

## 7. 圆柱 / RZ / RSPHERE 分支为什么更复杂

圆柱相关分支多出：

```cpp
amrex::Real const coef3_r = cdt/(1._rt + cdt_over_dr) / PhysConst::c;
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:64-66`。

在 `+r` 边界，`Btheta` 更新不仅依赖 `Ez`，还依赖 `Er` 的 `UpwardDz(...)`：

```cpp
Btheta(i,j,0,0) = coef1_r*Btheta(i,j,0,0) - coef2_r*Ez(i,j,0,0)
    + coef3_r*CylindricalYeeAlgorithm::UpwardDz(Er, coefs_z, n_coefs_z, i, j, 0, 0);
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:167-170`。

`Bz` 更新则还出现显式的 `1/r` 项：

```cpp
Bz(i,j,0,0) = coef1_r*Bz(i,j,0,0) + coef2_r*Etheta(i,j,0,0) - coef3_r*Etheta(i,j,0,0)/r;
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:196-199`。

因此，RZ / cylindrical 的 Silver-Mueller 不再是简单的一维切向波阻抗关系，还混入了 cylindrical curl 与几何项。

## 8. 模式展开下的高阶 azimuthal mode

RZ 分支对高阶 mode 不是忽略，而是逐 mode 更新。例如 `Btheta`：

```cpp
for (int m=1; m<nmodes; m++) {
    Btheta(i,j,0,2*m-1) = ...
    Btheta(i,j,0,2*m) = ...
}
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:171-179`。

`Bz` 的高阶 mode 里还会把 `Er` 的实部和虚部按 `m/r` 耦合进去：

```cpp
Bz(...,2*m-1) = ... - coef3_r/r*(Etheta(...,2*m-1) - m*Er(...,2*m));
Bz(...,2*m)   = ... - coef3_r/r*(Etheta(...,2*m)   + m*Er(...,2*m-1));
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/ApplySilverMuellerBoundary.cpp:201-207`。

这说明在模式展开几何里，Silver-Mueller 已经不是单独模式彼此解耦的最简边界，而是受 cylindrical Maxwell 结构影响。

## 9. 这一实现真正保证了什么

从当前代码能稳妥得出的结论是：

1. 它只修改 `B` 的最内侧 guard cell；
2. 使用 Yee stencil 的最前一项系数 `m_h_stencil_coefs_*[0]` 构造离散边界系数；
3. 通过切向 `E` 驱动切向 `B` 的边界递推；
4. 在 cylindrical / RZ 几何中显式保留了额外的 `dz` 导数项和 `1/r` 几何项；
5. 只在被标记为 `absorbing_silver_mueller` 的边界侧启用。

## 10. 与 PML 的本质区别

对比前面的 PML 笔记，可以更清楚地看出两者差别：

- Silver-Mueller：
  - 不生成独立 PML 区域
  - 不维护 split fields
  - 只更新最内侧一层 guard `B`
  - 算法便宜，但吸收能力有限
- PML：
  - 维护独立区域、split fields、`SigmaBox`
  - 支持更复杂的开边界吸收和粒子 / 电流耦合
  - 实现代价更高

这正是参数文档里“Silver-Mueller 更简单、更便宜，但吸收效果不如 PML”的源码基础。

## 11. 当前阶段的稳定结论

1. `ApplySilverMuellerBoundary()` 的核心是基于 Yee 交错的显式边界递推，而不是静态赋值。
2. 它只更新物理域外第一层 `B` guard cell。
3. Cartesian 分支是标准“切向 `E` 驱动切向 `B`”结构；RZ / cylindrical 分支额外带 `dz` 与 `1/r` 项。
4. 这一实现比 PML 轻量得多，因此功能边界也更窄。

## 12. 下一步

- 边界模块若继续推进，下一步应转到 `EmbeddedBoundary/` 与 `Parallelization/`，把边界与 coarse-fine / guard-cell / scraping 的耦合串起来。
- 若继续完善第 7 章，可把本笔记中的“最内侧 guard cell 递推”与 PML 的“独立吸收层”做一节正面对比。
