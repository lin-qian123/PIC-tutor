# Boundary 00: field / particle 边界参数解析与一致性约束

绑定源码：

- `../warpx/Source/BoundaryConditions/FieldBoundaries.H`
- `../warpx/Source/BoundaryConditions/FieldBoundaries.cpp`
- `../warpx/Source/Particles/ParticleBoundaries.cpp`
- `../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/theory/boundary_conditions.rst`

## 1. 这一层解决什么问题

边界条件在 WarpX 里分成两套：

1. `boundary.field_lo/hi` 决定 Maxwell/Poisson 求解器在域边界如何闭合；
2. `boundary.particle_lo/hi` 决定宏粒子越界后是吸收、反射、周期穿越还是不处理。

这两套参数不是独立的。对 periodic 方向，场和粒子必须一起 periodic；对非 periodic 方向，则允许 field 和 particle 采用不同语义，例如 field 用 PEC/PML，particle 用 absorbing/reflecting。

## 2. 主调用链

`WarpX::MakeWarpX()` 在真正构造 `WarpX` 单例前先解析边界：

```cpp
std::tie(field_boundary_lo, field_boundary_hi) =
    warpx::boundary_conditions::parse_field_boundaries();

const auto is_field_boundary_periodic =
    warpx::boundary_conditions::get_periodicity_array(field_boundary_lo, field_boundary_hi);

std::tie(particle_boundary_lo, particle_boundary_hi) =
    warpx::particles::parse_particle_boundaries(is_field_boundary_periodic);
```

源码位置：`../warpx/Source/WarpX.cpp:284-291`。

这个顺序很关键：

1. 先读 field boundary；
2. 再把 field 是否 periodic 压缩成布尔数组；
3. 最后在 particle boundary 解析时强制 periodic 一致性。

## 3. field boundary 的最小约束

`parse_field_boundaries()` 的主体非常短：

```cpp
for (int idim = 0; idim < AMREX_SPACEDIM; ++idim) {
    pp_boundary.query_enum_sloppy("field_lo",
        field_boundary_lo[idim], "-_", idim);
    pp_boundary.query_enum_sloppy("field_hi",
        field_boundary_hi[idim], "-_", idim);
}

detail::check_periodicity_consistency(field_boundary_lo, field_boundary_hi);
```

源码位置：`../warpx/Source/BoundaryConditions/FieldBoundaries.cpp:54-63`。

真正的约束写在 `check_periodicity_consistency()`：

```cpp
const bool is_lo_periodic =
    (field_boundary_lo[idim]  == FieldBoundaryType::Periodic);
const bool is_hi_periodic =
    (field_boundary_hi[idim]  == FieldBoundaryType::Periodic);
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    (is_lo_periodic == is_hi_periodic),
    "field boundary must be consistenly periodic in both lo and hi");
```

源码位置：`../warpx/Source/BoundaryConditions/FieldBoundaries.cpp:26-34`。

结论：

- WarpX 不允许某个方向只在 `lo` 或只在 `hi` 一侧设 periodic。
- periodic 在这里不是“单边通量条件”，而是“这一整根轴是否拓扑闭合”的开关。

## 4. particle boundary 的默认值不是简单的 “absorbing everywhere”

文档里写 `boundary.particle_lo/hi` 默认是 `absorbing`，但源码层面还要区分“用户有没有显式写 particle 边界”。

`parse_particle_boundaries()` 先判断：

```cpp
const bool particle_boundary_specified =
    pp_boundary.contains("particle_lo") ||
    pp_boundary.contains("particle_hi");
```

源码位置：`../warpx/Source/Particles/ParticleBoundaries.cpp:69-71`。

如果用户根本没写 particle 边界，就执行：

```cpp
detail::set_to_periodic_if_field_boundary_is_periodic(
    particle_boundary_lo, particle_boundary_hi,
    is_field_boundary_periodic);
```

源码位置：`../warpx/Source/Particles/ParticleBoundaries.cpp:73-77`。

这个 helper 的逻辑是：

```cpp
if (is_field_boundary_periodic[idim]){
    particle_boundary_lo[idim] = ParticleBoundaryType::Periodic;
    particle_boundary_hi[idim] = ParticleBoundaryType::Periodic;
}
```

源码位置：`../warpx/Source/Particles/ParticleBoundaries.cpp:24-29`。

所以更准确的结论是：

- 如果用户没有写 `boundary.particle_lo/hi`，非 periodic 方向保留类默认值 absorbing；
- 但 periodic 方向会被自动改写成 periodic，而不是 absorbing。

## 5. field / particle periodic 耦合规则

如果用户显式写了 particle 边界，源码会做更严格检查：

```cpp
if (is_field_boundary_periodic[idim] ||
    particle_boundary_lo[idim] == ParticleBoundaryType::Periodic ||
    particle_boundary_hi[idim] == ParticleBoundaryType::Periodic ) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        (particle_boundary_lo[idim] == ParticleBoundaryType::Periodic) &&
        (particle_boundary_hi[idim] == ParticleBoundaryType::Periodic),
        "field and particle boundary must be periodic in both lo and hi");
}
```

源码位置：`../warpx/Source/Particles/ParticleBoundaries.cpp:38-47`。

因此，periodic 在 WarpX 中总是“整轴成对出现”的约束，而不是单边选项。

## 6. 文档参数表与源码能力的对应关系

`boundary.field_lo/hi` 文档列出的主要选项见 `../warpx/Docs/source/usage/parameters.rst:763-825`：

- `Periodic`
- `pml`
- `absorbing_silver_mueller`
- `damped`
- `pec`
- `pmc`
- `pec_insulator`
- `none`
- `neumann`
- `open`

这里要区分三类求解器语义：

1. 电磁 Maxwell 边界；
2. 静电 multigrid 边界；
3. 静电 open Poisson 边界。

## 7. 解析后的边界如何落到真实场数组

真正把边界施加到场数组的入口在 `WarpXFieldBoundaries.cpp`。`ApplyEfieldBoundary()` 顶层先按边界类型分派：

```cpp
if (::isAnyBoundary<FieldBoundaryType::PEC>(field_boundary_lo, field_boundary_hi)) {
    PEC::ApplyPECtoEfield(...);
}

if (::isAnyBoundary<FieldBoundaryType::PMC>(field_boundary_lo, field_boundary_hi)) {
    PEC::ApplyPECtoBfield(...);
}

if (::isAnyBoundary<FieldBoundaryType::PECInsulator>(field_boundary_lo, field_boundary_hi)) {
    pec_insulator_boundary->ApplyPEC_InsulatortoEfield(...);
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp:55-161`。

对应的 `ApplyBfieldBoundary()` 则额外处理 Silver-Mueller：

```cpp
if (lev == 0) {
    if (subcycling_half == SubcyclingHalf::FirstHalf) {
        if(::isAnyBoundary<FieldBoundaryType::Absorbing_SilverMueller>(field_boundary_lo, field_boundary_hi)){
            m_fdtd_solver_fp[0]->ApplySilverMuellerBoundary(...);
        }
    }
}
```

源码位置：`../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp:228-242`。

## 8. 当前阶段的稳定结论

1. boundary 参数解析的核心不是枚举表，而是 periodic 一致性约束。
2. field boundary 先解析，particle boundary 后解析，后者依赖前者生成的 periodic 掩码。
3. “particle 默认是 absorbing” 只对非 periodic 方向成立；若 field 是 periodic，particle 在未显式指定时会自动变成 periodic。
4. Silver-Mueller 不是通用 field boundary post-process，而是挂在 FDTD B 半步上的特定算法边界。

## 9. 下一步

- 继续精读 `PML.H`、`PML.cpp`、`WarpXEvolvePML.cpp`，补 `01-pml-data-and-update.md`。
- 继续精读 `WarpX_PEC.cpp` 与 `PEC_Insulator.cpp`，补 PEC/PMC/PECInsulator 的场与沉积镜像规则。
