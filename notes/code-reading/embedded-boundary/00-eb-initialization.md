# EmbeddedBoundary 00: 初始化、distance field 与更新标记

绑定源码：

- `../warpx/Source/EmbeddedBoundary/Enabled.H`
- `../warpx/Source/EmbeddedBoundary/Enabled.cpp`
- `../warpx/Source/WarpXInitEB.cpp`
- `../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.H`
- `../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp`
- `../warpx/Docs/source/usage/parameters.rst`

## 1. 这一层要回答什么

边界条件章节里，embedded boundary（EB）不能只理解成“又一种边界类型”。在 WarpX 里，它实际上先做三件事：

1. 判定运行时是否真的启用 EB。
2. 把解析函数或 STL 几何交给 AMReX EB2，构建 cut-cell 几何。
3. 基于 cut-cell 信息生成后续 solver、deposition 和 particle scraping 需要的辅助标记。

因此，`EmbeddedBoundary/` 的第一篇笔记不该直接从粒子刮擦或 face extension 开始，而应先把“几何是怎么进入 WarpX 的”讲清楚。

## 2. 运行时 EB 开关：编译支持不等于实际启用

最外层开关在 `Enabled.cpp`：

```cpp
bool enabled ()
{
#ifndef AMREX_USE_EB
    return false;
#else
    amrex::ParmParse const pp_warpx("warpx");
    amrex::ParmParse const pp_eb2("eb2");

    std::string eb_implicit_function;
    bool eb_enabled = pp_warpx.query("eb_implicit_function", eb_implicit_function);

    std::string eb_stl;
    eb_enabled |= pp_eb2.query("geom_type", eb_stl);

    return eb_enabled;
#endif
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/Enabled.cpp:18-34`。

这里有两个关键结论：

1. 编译时必须打开 `AMREX_USE_EB`，否则 `EB::enabled()` 永远返回 `false`。
2. 即便编译支持 EB，运行时也只有在输入文件里出现 `warpx.eb_implicit_function` 或 `eb2.geom_type` 时才真正启用。

所以 WarpX 对 EB 的判断是“编译能力 + 运行时参数”双门槛，而不是只看编译选项。

## 3. 官方参数入口：解析函数、STL 和边界电势

官方文档 `Docs/source/usage/parameters.rst` 给出 EB 的两种几何定义方式：

- `warpx.eb_implicit_function`
- `eb2.stl_file` 且配合 `eb2.geom_type = stl`

文档明确规定：

- 隐式函数值为 `0` 的地方是 EB 表面；
- 函数值为负的区域是物理模拟区域；
- 函数值为正的区域是 embedded boundary 内部。

此外还定义了：

- `warpx.eb_potential(x,y,z,t)`

它的意义不是“给边界再加一个标签”，而是直接提供 EB 表面的电势：

- 对 electrostatic solver，每个时间步都参与求势；
- 对 Maxwell solver，若设置该参数，会在 `t = 0` 触发一次 electrostatic solve，用来构造初始边界电场；
- 该函数在 EB 内部也会被计算，因此文档要求它在 EB 内部保持常数。

源码/文档位置：`../warpx/Docs/source/usage/parameters.rst:954-995`。

## 4. `WarpX::InitEB()`：把输入几何交给 AMReX EB2

真正的初始化入口在 `WarpXInitEB.cpp`：

```cpp
void
WarpX::InitEB ()
{
    if (!EB::enabled()) {
        throw std::runtime_error("InitEB only works when EBs are enabled at runtime");
    }

#if !defined(WARPX_DIM_3D) && !defined(WARPX_DIM_XZ) && !defined(WARPX_DIM_RZ)
    WARPX_ABORT_WITH_MESSAGE("EBs only implemented in 2D and 3D");
#endif
```

源码位置：`../warpx/Source/WarpXInitEB.cpp:63-72`。

这里先做了两个硬约束检查：

1. 运行时必须真的启用 EB；
2. 维度只支持 `3D`、`XZ`、`RZ`，也就是 2D/3D 类几何。

随后，如果用户提供了 `warpx.eb_implicit_function`，WarpX 会先把字符串 parser 编译成三变量函数，再交给 AMReX `GeometryShop`：

```cpp
const amrex::ParmParse pp_warpx("warpx");
std::string impf;
pp_warpx.query("eb_implicit_function", impf);
if (! impf.empty()) {
    auto eb_if_parser = utils::parser::makeParser(impf, {"x", "y", "z"});
    ParserIF const pif(eb_if_parser.compile<3>());
    auto gshop = amrex::EB2::makeShop(pif, eb_if_parser);
    amrex::EB2::Build(gshop, Geom(maxLevel()), maxLevel(), maxLevel()+20);
}
```

源码位置：`../warpx/Source/WarpXInitEB.cpp:78-87`。

这里的 `ParserIF` 做了一件容易忽略的事：在 `XZ` / `RZ` 维度下，它把三变量接口映射成 `(x, 0, z)` 风格调用，因此输入层仍然维持统一的 `x, y, z` 语法。

如果用户没有提供隐式函数，WarpX 则退回 AMReX EB2 的标准参数路径：

```cpp
amrex::ParmParse pp_eb2("eb2");
if (!pp_eb2.contains("geom_type")) {
    std::string const geom_type = "all_regular";
    pp_eb2.add("geom_type", geom_type);
}
amrex::EB2::Build(Geom(maxLevel()), maxLevel(), maxLevel()+20);
```

源码位置：`../warpx/Source/WarpXInitEB.cpp:88-95`。

这段的真实语义是：

- 若已指定 `eb2.geom_type = stl` 或其他 AMReX EB2 几何，WarpX 直接沿用；
- 若什么都没写，就强制退回 `all_regular`；
- `maxLevel()+20` 不是物理参数，而是允许 EB2 为 multigrid 尽量向粗层 coarsen 的硬编码上限。

因此，`InitEB()` 的职责不是自己构造几何细节，而是把 WarpX 参数翻译成 AMReX EB2 的构建请求。

## 5. `ComputeDistanceToEB()`：生成 signed distance 场

EB 几何建好之后，WarpX 还会生成 `distance_to_eb` 场：

```cpp
void
WarpX::ComputeDistanceToEB ()
{
    if (!EB::enabled()) {
        throw std::runtime_error("ComputeDistanceToEB only works when EBs are enabled at runtime");
    }
    const amrex::EB2::IndexSpace& eb_is = amrex::EB2::IndexSpace::top();
    for (int lev=0; lev<=maxLevel(); lev++) {
        const amrex::EB2::Level& eb_level = eb_is.getLevel(Geom(lev));
        auto const eb_fact = fieldEBFactory(lev);
        amrex::FillSignedDistance(*m_fields.get(FieldType::distance_to_eb, lev), eb_level, eb_fact, 1);
    }
}
```

源码位置：`../warpx/Source/WarpXInitEB.cpp:100-112`。

这里要抓住两个数据结构：

- `amrex::EB2::IndexSpace::top()`：AMReX 保存的全局 EB 几何层级；
- `FieldType::distance_to_eb`：WarpX field registry 中存放 signed distance 的场。

因此，distance field 不是独立几何求解器重新算出来的，而是从 EB2 已有几何层直接填充到 WarpX MultiFab。

这也解释了为什么后续粒子 scraping、reduced diagnostics 或近壁沉积修正可以直接依赖 EB 几何辅助场，而不必重新解析 STL 或隐式函数。

## 6. `EmbeddedBoundaryInit.H`：初始化阶段真正要产出的辅助量

`EmbeddedBoundaryInit.H` 把初始化阶段要准备的 EB 辅助量列得很清楚：

- `MarkReducedShapeCells`
- `MarkUpdateCellsStairCase`
- `MarkUpdateECellsECT`
- `MarkUpdateBCellsECT`
- `MarkExtensionCells`
- `ComputeEdgeLengths`
- `ComputeFaceAreas`
- `ScaleEdges`
- `ScaleAreas`

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.H:22-128`。

这份声明本身就说明一件事：WarpX 处理 EB 时不是只维护“哪一格被切到”，而是至少同时维护三层信息：

1. 粒子沉积是否要降阶；
2. 场更新是否允许进行；
3. cut edge / cut face 的几何长度和面积，以及后续 face extension 所需的稳定性标志。

## 7. `MarkReducedShapeCells()`：EB 附近强制把沉积降成一阶

这个函数的目标是：如果某个粒子所在单元附近，shape 可能跨到部分覆盖或完全覆盖的 cut cell，就强制该单元内粒子使用一阶 shape 沉积。

核心逻辑：

```cpp
if (fab_type == amrex::FabType::regular) {
    eb_reduce_particle_shape_arr(i, j, k) = 0;
} else if (fab_type == amrex::FabType::covered) {
    eb_reduce_particle_shape_arr(i, j, k) = 1;
} else {
    ...
    if ( !flag(i_cell, j_cell, k_cell).isRegular() ) {
        reduce_shape = 1;
    }
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:44-107`。

这里的物理/算法含义是：

- `regular`：附近没有 cut cell，保持原来的高阶 shape；
- `covered`：整个 tile 都被覆盖，直接标记降阶；
- `mixed`：只要 shape 可能伸到任意非 regular cell，就降成一阶。

这一设计的核心目的不是“让沉积更便宜”，而是避免高阶 shape 把电荷/电流沉积到部分覆盖或完全覆盖的 cell 中。

函数末尾还会执行：

```cpp
eb_reduce_particle_shape->FillBoundary(periodicity);
```

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:114`。

说明该标记也要同步到 guard cells，后续 tile kernel 才能无条件读取。

## 8. `MarkUpdateCellsStairCase()`：非 ECT solver 的 stair-case 更新屏蔽

对于普通 finite-difference solver，WarpX 不是在 cut face 上做连续几何更新，而是采用 stair-case 近似：只要某个 field grid point 邻接到非 regular cell，就不更新它。

核心判断：

```cpp
if (fab_type == amrex::FabType::regular) {
    eb_update_arr(i, j, k) = 1;
} else if (fab_type == amrex::FabType::covered) {
    eb_update_arr(i, j, k) = 0;
} else {
    ...
    if ( !flag(i_cell, j_cell, k_cell).isRegular() ) {
        eb_update_flag = 0;
    }
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:137-214`。

更关键的是它如何定义“邻接”：

- 若该 field 分量在某个方向是 nodal，就检查该节点左右两侧单元；
- 若该方向是 cell-centered，就只检查同位置单元。

所以 `MarkUpdateCellsStairCase()` 的本质不是单纯复制 cell flag，而是把 cut-cell 拓扑投影到具体的 Yee / nodal 场自由度上。

## 9. `MarkUpdateECellsECT()` 与 `MarkUpdateBCellsECT()`：ECT 直接看 edge/face 是否被切断

ECT solver 不走 stair-case，而是直接依据 cut edge / cut face 的几何量判定是否更新。

对 `E`：

```cpp
eb_update_Ex_arr(i, j, k) = (lx_arr(i, j, k) == 0)? 0 : 1;
...
eb_update_Ez_arr(i, j, k) = (lz_arr(i, j, k) == 0)? 0 : 1;
```

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:242-268`。

在 `XZ` / `RZ` 中，`Ey` 是 node-centered，自身不对应单根 edge，因此要检查周围几条 edge 是否有任意一条长度为零：

```cpp
if((lx_arr(...)==0)
 ||(lx_arr(...)==0)
 ||(lz_arr(...)==0)
 ||(lz_arr(...)==0)) {
    eb_update_Ey_arr(i, j, k) = 0;
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:250-262`。

对 `B`：

- 3D 下 `Bx/By/Bz` 看对应 face area 是否为零；
- `XZ` / `RZ` 下 `Bx/Bz` 改看对应 edge length 是否为零，`By` 仍看 face area。

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:289-334`。

因此，ECT 的 EB 判据比 stair-case 更几何化：它不是“附近有 cut cell 就停更”，而是“该离散自由度对应的 edge/face 是否已经被 EB 完全截断”。

## 10. `MarkExtensionCells()` 说明下一层要进入 face extension

虽然本篇不展开 `MarkExtensionCells()` 细节，但声明和开头实现已经给出了后续方向：

- `flag_info_face`
- `flag_ext_face`
- 稳定 / 未侵入 / 已侵入三态标志

对应注释为：

- `0` unstable
- `1` stable and not intruded
- `2` stable and intruded

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.H:80-97`。

这说明 WarpX 在 cut-face 更新之外，还要为 face extension 维护额外拓扑状态。下一篇 `01-face-extensions.md` 应该直接从这里继续。

## 11. 当前可以得到的结构性结论

到这一层为止，WarpX 的 EB 初始化链可以概括为：

1. `Enabled.*` 判断编译与运行时双条件是否满足；
2. `InitEB()` 把隐式函数或 `eb2` 几何交给 AMReX EB2；
3. `ComputeDistanceToEB()` 从 EB2 几何填充 signed distance 场；
4. `EmbeddedBoundaryInit.*` 基于 EB cell flag / edge length / face area 生成：
   - 沉积降阶标志；
   - 场更新允许标志；
   - face extension 预备标志。

所以 EB 在 WarpX 中首先是“几何驱动的辅助场与标记系统”，然后才进入边界物理、粒子 scraping 和 cut-cell field update。

## 12. 下一步

这一篇之后，最自然的顺序是：

1. `WarpXFaceExtensions.cpp` 与 `WarpXFaceInfoBox.H`
2. `ParticleScraper.H` 与 `ParticleBoundaryProcess.H`
3. `Examples/Tests/embedded_boundary/` 的验证入口

这样才能把 EB 从“初始化几何”推进到“它如何真实改变场更新和粒子命运”。
