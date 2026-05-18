# Fluids 源码精读入口

绑定源码：`../warpx/Source/Fluids`。

## 模块边界

- 构建入口：`Fluids/CMakeLists.txt`、`Fluids/Make.package`。
- 主要文件：`MultiFluidContainer.*`、`WarpXFluidContainer.*`、`MusclHancockUtils.H`。
- 关联模块：hybrid PIC field solve、electron pressure、source deposition。

## 核心问题

- fluid species 如何初始化、推进和沉积 current。
- MUSCL-Hancock 更新如何实现。
- fluid 与 PIC 粒子、hybrid solver 和 fields 如何耦合。

## 精读顺序

1. `MultiFluidContainer.*`。
2. `WarpXFluidContainer.*` 参数和数据结构。
3. `WarpXFluidContainer::Evolve`。
4. `MusclHancockUtils.H`。
5. `WarpXFluidContainer::DepositCurrent`。

## 输出目标

- `00-fluid-container-map.md`
- `01-muscl-hancock-update.md`
- `02-fluid-pic-coupling.md`

## 验证线索

- hybrid / Ohm solver examples。
- `Examples/Tests/langmuir_fluids/`

## 当前状态

- 已完成 `00-fluid-container-map.md`：把 `fluids.species_names -> MultiFluidContainer -> WarpXFluidContainer` 这条对象图、启动期约束、`N/NU` level data、shared injector 初始化和 moving-window 连续再注入主链压实。
- 已完成 `01-muscl-hancock-update.md`：解释 cold relativistic fluid 的 `N/NU` 守恒变量、`ave` limiter、Rusanov flux、positivity limiter、RZ/RCYLINDER/RSPHERE 几何修正和 `centrifugal_source_rz()` 的 SSP-RK3 曲率源项。
- 已完成 `02-fluid-pic-coupling.md`：解释 fluid species 如何 gather `Efield_aux/Bfield_aux`、复用 Higuera-Cary source-step、把 nodal `N/NU` 转成 `rho/J` 沉积回普通场寄存器，以及它与 `HybridPICModel` 电子闭合的真实边界。
