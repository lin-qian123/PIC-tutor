# BoundaryConditions 源码精读入口

绑定源码：`../warpx/Source/BoundaryConditions`。

## 模块边界

- 构建入口：`BoundaryConditions/CMakeLists.txt`、`BoundaryConditions/Make.package`。
- 主要文件：`FieldBoundaries.*`、`PML.*`、`PML_RZ.*`、`WarpXFieldBoundaries.cpp`、`WarpXEvolvePML.cpp`、`WarpX_PEC.*`、`PEC_Insulator.*`。

## 核心问题

- field boundary 参数如何解析、检查和应用。
- PML boxes、sigma、split fields、current damping 如何组织。
- PEC、insulator、Silver-Mueller 和 periodic 与粒子边界如何匹配。
- RZ PML 与 Cartesian PML 的差异。

## 精读顺序

1. `FieldBoundaries.*` 参数解析。
2. `WarpXFieldBoundaries.cpp` 应用入口。
3. `PML.*` 与 `WarpXEvolvePML.cpp`。
4. `WarpX_PEC.*`。
5. `PEC_Insulator.*`。
6. `PML_RZ.*`。

## 输出目标

- `00-field-boundary-parameters.md`
- `01-pml-data-and-update.md`
- `02-pec-insulator-silver-mueller.md`
- `03-boundary-parameter-table.md`
- `04-silver-mueller-internal-stencil.md`
- 更新边界/AMR 章节。

## 当前进展

- `00-field-boundary-parameters.md`：已建立，覆盖 `FieldBoundaries.*`、`ParticleBoundaries.cpp`、`WarpX.cpp` 中 field/particle 边界解析顺序、periodic 一致性约束和 `WarpXFieldBoundaries.cpp` 的第一层分派。
- `01-pml-data-and-update.md`：已建立，覆盖 `PML.H`、`PML.cpp`、`WarpXEvolvePML.cpp`、`PML_current.H`、`WarpX_PML_kernels.H` 的 PML 几何、`SigmaBox`、split-field 阻尼和 PML 电流更新。
- `02-pec-insulator-silver-mueller.md`：已建立，覆盖 `WarpX_PEC.cpp`、`PEC_Insulator.cpp`、`WarpXFieldBoundaries.cpp` 中 PEC/PMC 的 E/B 奇偶规则、rho/J 镜像沉积、PECInsulator parser 边界和值以及 `crop_on_PEC_boundary` / Silver-Mueller 的实现边界。
- `03-boundary-parameter-table.md`：已建立，汇总 `boundary.field_*`、`boundary.particle_*`、`boundary.potential_*`、PECInsulator parser、`particles.crop_on_PEC_boundary` 与 PML 参数的适用范围、联动关系和源码入口。
- `04-silver-mueller-internal-stencil.md`：已建立，覆盖 `ApplySilverMuellerBoundary.cpp` 中的 Yee-only 限制、最内侧 guard cell 更新、Cartesian 边界递推系数，以及 RZ / cylindrical 分支的 `dz` 与 `1/r` 几何项。

## 验证线索

- `Examples/Tests/boundaries/`
- `Examples/Tests/particles_in_pml/`
- 既有本地经验：field/particle periodic 边界匹配规则需回到源码验证。
