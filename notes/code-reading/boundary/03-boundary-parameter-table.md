# Boundary 03: field / particle / PML 参数总表

绑定文档与源码：

- `../warpx/Docs/source/usage/parameters.rst:763-950`
- `../warpx/Source/BoundaryConditions/FieldBoundaries.cpp`
- `../warpx/Source/Particles/ParticleBoundaries.cpp`
- `../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp`
- `../warpx/Source/BoundaryConditions/PML.cpp`
- `../warpx/Source/BoundaryConditions/PEC_Insulator.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`

## 1. 这张表的作用

前面三篇边界笔记已经解释了：

- 参数解析与 periodic 一致性
- PML 数据结构和 split-field 更新
- PEC / PMC / PECInsulator / Silver-Mueller 的边界语义

这一篇不再展开源码机制，而是把“输入参数名 -> 作用对象 -> 关键限制 -> 主要实现入口”压缩成可检索总表，方便后续书稿正文和章节索引引用。

## 2. 场边界主参数

### 2.1 `boundary.field_lo/hi`

默认值：`pml`

源码入口：

- `../warpx/Source/BoundaryConditions/FieldBoundaries.cpp`
- `../warpx/Source/BoundaryConditions/WarpXFieldBoundaries.cpp`

核心约束：

- 某方向只要 `lo` 是 periodic，则 `hi` 也必须 periodic
- field periodic 会强制 particle periodic 一致

各选项总览：

| 选项 | 主要物理语义 | 关键限制 | 主要实现入口 |
|---|---|---|---|
| `periodic` | 整轴周期闭合 | `lo/hi` 必须成对 periodic；particle 若显式设置也必须成对 periodic | `FieldBoundaries.cpp` + `ParticleBoundaries.cpp` |
| `pml` | 开放边界吸收层 | 可与 `warpx.do_pml_in_domain`、`warpx.pml_has_particles`、`warpx.do_pml_j_damping` 联动 | `PML.H/.cpp`、`WarpXEvolvePML.cpp` |
| `absorbing_silver_mueller` | 较轻量的吸收边界 | 只适用于 Yee Maxwell solver | `WarpXFieldBoundaries.cpp` 调 `ApplySilverMuellerBoundary()` |
| `damped` | moving-window 谱求解中的 guard-cell 阻尼 | 当前文档只推荐 spectral solver 且 moving direction 使用 | 相关分支不在本批精读重点内 |
| `pec` | 完美电导体边界 | 对 spectral solver 无效；RZ/RCYLINDER/RSPHERE 的 `r=0` 不可用 | `WarpX_PEC.cpp` |
| `pmc` | 完美磁导体边界 | 对 spectral solver 无效；实现上复用 PEC helper 并交换 E/B 角色 | `WarpXFieldBoundaries.cpp` + `WarpX_PEC.cpp` |
| `pec_insulator` | 部分 PEC、部分 insulator 的混合边界 | 需配合 `insulator.area_*` 和可选切向场 parser | `PEC_Insulator.cpp` |
| `none` | Maxwell solve 不施加场边界 | RZ/RCYLINDER/RSPHERE 的 lower radial boundary 必须用它 | solver 分支自行跳过 |
| `neumann` | 静电 multigrid 的零法向导数边界 | 只对 electrostatic multigrid 有意义 | electrostatic solver 分支 |
| `open` | 静电 Poisson open boundary | 只对 integrated Green function Poisson solver 有意义 | electrostatic open solver 分支 |

## 3. 静电边界电势参数

### 3.1 `boundary.potential_lo/hi_x/y/z`

默认值：`0`

文档含义：

- 对 electrostatic solver：给定边界电势，参与每个时间步的势求解
- 对非 electrostatic Maxwell 模式：若设置该参数，会在 `t=0` 触发一次 electrostatic solve，用边界电势初始化自场

书稿里应把它视为“边界值驱动的初始自场工具”，而不是仅限静电模式的参数。

## 4. 粒子边界主参数

### 4.1 `boundary.particle_lo/hi`

默认值：`absorbing`

源码入口：

- `../warpx/Source/Particles/ParticleBoundaries.cpp`

关键限制：

- 只要 field periodic，则 particle 必须周期一致
- RZ / RCYLINDER / RSPHERE 的 lower radial boundary 必须用 `none`

各选项总览：

| 选项 | 行为 | 关键限制 / 伴随参数 | 主要实现入口 |
|---|---|---|---|
| `absorbing` | 越界粒子删除 | 非 periodic 默认行为 | `ParticleBoundaries.cpp` + particle container 边界处理 |
| `periodic` | 从对侧重新进入 | field boundary 必须整轴 periodic | `ParticleBoundaries.cpp` |
| `reflecting` | 反射回域内 | `boundary.reflect_all_velocities` 控制只翻法向还是全速度翻号 | particle boundary apply path |
| `thermal` | 反射并热化速度 | 需为每个 species 提供 `boundary.<species>.u_th` | particle boundary apply path |
| `none` | 不处理粒子边界 | 只建议用于 RZ/RCYLINDER/RSPHERE 的 lower radial boundary | `ParticleBoundaries.cpp` |

### 4.2 `boundary.reflect_all_velocities`

默认值：`false`

作用：

- `reflecting` 边界下，只翻法向速度还是所有速度分量一起翻号

它只影响粒子反射模型，不改变场边界语义。

### 4.3 `boundary.<species_name>.u_th`

文档位置没有单独列在这段里，但被 `thermal` 选项显式引用。

作用：

- 为 thermal particle boundary 提供高斯 / 高斯通量分布的热速度宽度

后续若写粒子边界细节，应把它与 species 参数章节联动，而不是只留在边界章。

## 5. 轴上修正参数

### 5.1 `boundary.verboncoeur_axis_correction`

默认值：`true`

作用：

- 在 RZ / RCYLINDER / RSPHERE 几何中，对轴上 nodal `rho` / `Jz` 的有效体积做 Verboncoeur 修正

这不是“域边界条件”，但它属于 boundary 参数组，并直接影响轴上沉积的数值一致性。后续写 RZ 边界或粒子沉积时，应把它和 axis regularization 一起讲。

## 6. PEC / PECInsulator 相关粒子裁剪参数

### 6.1 `particles.crop_on_PEC_boundary`

默认值：`false`

源码入口：

- `../warpx/Source/Particles/WarpXParticleContainer.cpp`

作用：

- 当粒子穿过 `pec` 或 `pec_insulator` 边界时，是否裁剪其轨迹

关键点：

- 它作用于粒子几何处理
- 不改变场边界更新公式

因此书稿里应把它归到“粒子与固体边界的几何处理选项”，而不是误归为场边界参数。

## 7. PECInsulator 专属 parser 参数

### 7.1 区域判定

这些参数决定边界上哪一部分是 insulator：

- `insulator.area_x_lo(y,z)`
- `insulator.area_x_hi(y,z)`
- `insulator.area_y_lo(x,z)`
- `insulator.area_y_hi(x,z)`
- `insulator.area_z_lo(x,y)`
- `insulator.area_z_hi(x,y)`

源码入口：

- `PEC_Insulator.cpp` 中 `m_insulator_area_lo/hi`
- `ApplyPEC_InsulatortoField()` 中 `area_parser(...) > 0`

规则：

- parser 值大于 0 的横向位置被视为 insulator
- 否则按 PEC 处理

### 7.2 切向场赋值

这些参数可显式指定 insulator 部分的切向 E/B：

- x 边界：`Ey_x_*`、`Ez_x_*`、`By_x_*`、`Bz_x_*`
- y 边界：`Ex_y_*`、`Ez_y_*`、`Bx_y_*`、`Bz_y_*`
- z 边界：`Ex_z_*`、`Ey_z_*`、`Bx_z_*`、`By_z_*`

规则：

- 若给定 parser，则 insulator 边界值直接取 parser
- 若未给定，则用代码里的镜像 / 外推逻辑维持该边界段的场

因此 PECInsulator 不是简单的“绝缘体开关”，而是“区域判定 + 可选边界值表达式”的组合。

## 8. PML 相关参数

这些参数控制 `pml` 选项的具体实现：

| 参数 | 默认值 | 作用 | 关键限制 / 依赖 |
|---|---|---|---|
| `warpx.pml_ncell` | `10` | PML 总厚度 | 决定 PML box 厚度 |
| `do_similar_dm_pml` | `1` | PML grid 是否使用与母网格相近的 `DistributionMapping` | 影响通信开销 |
| `warpx.pml_delta` | `10` | 阻尼增长特征深度 | 进入 `sigma` profile 构造 |
| `warpx.do_pml_in_domain` | `0` | PML 放在域内还是域外 | 域内时才能让粒子进入 PML |
| `warpx.pml_has_particles` | `0` | 是否在 PML 内推进粒子 | 需要 `warpx.do_pml_in_domain = 1` |
| `warpx.do_pml_j_damping` | `0` | 是否阻尼 PML 电流 | 需要 `warpx.pml_has_particles = 1` |
| `warpx.v_particle_pml` | `1` | PML 吸收粒子的速度假设（单位 `c`） | 与 `do_pml_j_damping` 联动 |
| `warpx.do_pml_dive_cleaning` | solver-dependent | 是否对 PML 中 `E` 清理场启用 divergence cleaning | 必须与 `do_pml_divb_cleaning` 配对 |
| `warpx.do_pml_divb_cleaning` | solver-dependent | 是否对 PML 中 `B` 清理场启用 divergence cleaning | 必须与 `do_pml_dive_cleaning` 配对 |

## 9. 参数之间最重要的联动关系

后续写正文时，最容易漏掉的不是参数定义本身，而是它们之间的组合约束：

1. `field periodic` -> `particle periodic`
2. `warpx.do_pml_in_domain = 1` -> 才允许 `warpx.pml_has_particles = 1`
3. `warpx.pml_has_particles = 1` -> 才允许 `warpx.do_pml_j_damping = 1`
4. `warpx.do_pml_dive_cleaning` 和 `warpx.do_pml_divb_cleaning` 必须成对一致
5. `pec` / `pec_insulator` 经常与 `particles.crop_on_PEC_boundary` 一起讨论
6. RZ / RCYLINDER / RSPHERE 的 lower radial boundary：
   - field 要用 `none`
   - particle 要用 `none`

## 10. 建议在书稿中的引用方式

这张表更适合作为：

- 第 7 章的参数速查小节
- 后续附录中的 boundary parameter index

不适合直接把整张表原样复制到正文主线，因为正文仍应按物理边界类型分段讲解：

- periodic / open
- PML / Silver-Mueller / damped
- PEC / PMC / PECInsulator
- particle reflecting / thermal / none

## 11. 当前阶段的稳定结论

1. `boundary.field_lo/hi` 其实混合了承担 Maxwell、electrostatic multigrid 和 open Poisson 的不同语义。
2. `boundary.particle_lo/hi` 的“默认 absorbing”只对非 periodic 方向成立。
3. `particles.crop_on_PEC_boundary`、`boundary.reflect_all_velocities`、`boundary.<species>.u_th` 这些辅助参数必须和主边界参数一起讲，否则读者容易误解真实行为。
4. PML 参数之间存在明显依赖链，不能孤立解释单个参数。

## 12. 下一步

- 若继续推进边界模块，下一优先项应是 `ApplySilverMuellerBoundary()` 内部公式与理论文档的逐项对齐。
- 若切换到 AMR / Parallelization，则本表已可作为后续章节的 boundary 参数附录基础。
