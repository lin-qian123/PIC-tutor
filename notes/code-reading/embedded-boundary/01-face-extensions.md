# EmbeddedBoundary 01: face extension、借用关系与 BCK fallback

绑定源码：

- `../warpx/Source/EmbeddedBoundary/WarpXFaceInfoBox.H`
- `../warpx/Source/EmbeddedBoundary/WarpXFaceInfoBox_fwd.H`
- `../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp`
- `../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp`
- `../warpx/Source/Initialization/WarpXInitData.cpp`
- `../warpx/Source/WarpX.H`
- `../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp`

## 1. 这一层要回答什么

在 EB + ECT 路径里，`MarkExtensionCells()` 已经把 cut face 分成了：

- 需要扩展的 face
- 可以借出面积的 face

但这还不是最终可用于场更新的数据。接下来还必须回答三件事：

1. 一个不稳定 face 需要补多少面积才稳定；
2. 这些面积从哪些邻居借，按什么规则分配；
3. 借用关系如何传给 ECT `B` 更新 kernel。

`WarpXFaceExtensions.cpp` 就是在做这三件事。

## 2. face extension 只服务 ECT solver

`WarpX.H` 里对三类成员写得很直接：

```cpp
/** EB: for every mesh face flag_info_face contains a:
 *          * 0 if the face needs to be extended
 *          * 1 if the face is large enough to lend area to other faces
 *          * 2 if the face is actually intruded by other face
 * This is only used for the ECT solver.*/
amrex::Vector<std::array< std::unique_ptr<amrex::iMultiFab>, 3 > > m_flag_info_face;

/** EB: for every mesh face face flag_ext_face contains a:
 *          * 1 if the face needs to be extended
 *          * 0 otherwise
 * This is only used for the ECT solver.*/
amrex::Vector<std::array< std::unique_ptr<amrex::iMultiFab>, 3 > > m_flag_ext_face;

/** EB: m_borrowing contains the info about the enlarged cells, i.e. for every enlarged cell it
 * contains the info of which neighbors are being intruded (and the amount of borrowed area).
 * This is only used for the ECT solver.*/
amrex::Vector<std::array< std::unique_ptr<amrex::LayoutData<FaceInfoBox> >, 3 > > m_borrowing;
```

源码位置：`../warpx/Source/WarpX.H:1220-1238`。

所以这一整套 face extension 机制并不是 EB 通用层，而是 ECT solver 为 cut face 稳定化额外维护的数据结构。

## 3. 初始化时机：在 `InitData()` 里，先算几何量，再算 extension

调用顺序在 `WarpXInitData.cpp`：

```cpp
auto edge_lengths_lev = m_fields.get_alldirs(FieldType::edge_lengths, lev);
warpx::embedded_boundary::ComputeEdgeLengths(edge_lengths_lev, eb_fact);
warpx::embedded_boundary::ScaleEdges(edge_lengths_lev, CellSize(lev));

auto face_areas_lev = m_fields.get_alldirs(FieldType::face_areas, lev);
warpx::embedded_boundary::ComputeFaceAreas(face_areas_lev, eb_fact);
warpx::embedded_boundary::ScaleAreas(face_areas_lev, CellSize(lev));

const auto& area_mod = m_fields.get_alldirs(FieldType::area_mod, maxLevel());
warpx::embedded_boundary::MarkExtensionCells(
    CellSize(maxLevel()), m_flag_info_face[maxLevel()], m_flag_ext_face[maxLevel()],
    m_fields.get_alldirs(FieldType::Bfield_fp, maxLevel()),
    face_areas_lev,
    edge_lengths_lev, area_mod);
ComputeFaceExtensions();
```

源码位置：`../warpx/Source/Initialization/WarpXInitData.cpp:1595-1610`。

这说明 extension 不是运行中动态重算，而是在初始化阶段基于：

- `edge_lengths`
- `face_areas`
- `area_mod`
- `m_flag_info_face`
- `m_flag_ext_face`

一次性准备好。

## 4. 稳定性阈值：`S_stab` 是 cut face 至少要长到多大

`MarkExtensionCells()` 对每个面先算最小稳定面积 `S_stab`：

```cpp
if (idim == 0){
    S_stab = 0.5 * std::max({ly(i, j, k) * dz, ly(i, j, k + 1) * dz,
                                    lz(i, j, k) * dy, lz(i, j + 1, k) * dy});
} else if (idim == 1){
    ...
} else {
    S_stab = 0.5 * std::max({lx(i, j, k) * dy, lx(i, j + 1, k) * dy,
                             ly(i, j, k) * dx, ly(i + 1, j, k) * dx});
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:388-410`。

这里的意思不是“把 cut face 修回原来完整网格面”，而是只要求它达到 ECT 稳定性所需的最小面积。

随后按这个阈值初始化两类标志：

```cpp
flag_ext_face_data(i, j, k) = int(S(i, j, k) < S_stab && S(i, j, k) > 0);
if(flag_ext_face_data(i, j, k)){
    flag_info_face_data(i, j, k) = 0;
}
if(int(S(i, j, k) > 0 && !flag_ext_face_data(i, j, k))) {
    flag_info_face_data(i, j, k) = 1;
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/EmbeddedBoundaryInit.cpp:426-433`。

因此：

- `flag_ext_face = 1` 表示这个 face 面积不足，必须扩展；
- `flag_info_face = 0` 表示“我是借方面”；
- `flag_info_face = 1` 表示“我是可出借方”；
- 后续真正被侵入的 lender 会改成 `2`。

## 5. `FaceInfoBox`：记录“从谁借了多少”

`FaceInfoBox` 是 extension 结果的核心容器：

```cpp
struct FaceInfoBox {
    enum Neighbours : uint8_t {n, s, e, w, nw, ne, sw, se};

    amrex::Gpu::DeviceVector<Neighbours> neigh_faces;
    amrex::Gpu::DeviceVector<amrex::Real> area;
    amrex::Gpu::DeviceVector<int> inds;
    amrex::BaseFab<int> size;
    amrex::BaseFab<int*> inds_pointer;
    int vecs_size;
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceInfoBox.H:15-29`。

它不是每个 face 固定存一个结构体，而是：

- 用 `size(i,j,k)` 记录这个 face 借了几个邻居；
- 用 `inds_pointer(i,j,k)` 指向全局压缩向量中的起点；
- `neigh_faces` 存邻居方位；
- `area` 存每个邻居贡献的借出面积。

也就是说，`FaceInfoBox` 本质上是一个压缩邻接表，而不是规则的 `3x3` 邻域数组。

辅助函数 `addConnectedNeighbor()` / `uint8_to_inds()` 只负责在：

- 枚举邻居方向
- `(i_n, j_n)` 偏移

之间来回转换。

## 6. `ComputeFaceExtensions()`：三段式稳定化流程

顶层入口是：

```cpp
::init_borrowing(m_borrowing[maxLevel()], Bfield);
ComputeOneWayExtensions();
...
ComputeEightWaysExtensions();
::shrink_borrowing(m_borrowing[maxLevel()], Bfield);
...
if (N_ext_faces_after_eight_ways(1) > 0) {
    ::ApplyBCKCorrection<1>(...);
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:514-565`。

因此整个流程是三段式：

1. 先尝试 one-way extension；
2. 剩下的再尝试 eight-ways extension；
3. 再剩下的用 BCK correction 兜底。

前后还会用 `CountExtFaces()` 统计每一步剩余多少未稳定 face，并通过 warning 输出。

## 7. one-way extension：只找一个正交邻居借满

`ComputeNBorrowOneFaceExtension()` 的判据是：

```cpp
if (GetNeigh(S_red, i, j, k, i_n, j_n, idim) > S_ext
    && (GetNeigh(flag_info_face, i, j, k, i_n, j_n, idim) == 1
    || GetNeigh(flag_info_face, i, j, k, i_n, j_n, idim) == 2)
    && flag_ext_face(i, j, k) && ! stop) {
    n_borrow += 1;
    stop = true;
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:398-404`。

这里有三个关键点：

1. one-way 只看非对角邻居，条件是 `i_n != j_n && i_n != -j_n`；
2. 借出方不仅可以是 `flag_info_face == 1`，也可以是已经被别人侵入过的 `2`；
3. 借出方必须还能一次性拿出 `S_ext` 这么多剩余面积。

真正写入 extension 结果时：

```cpp
::SetNeigh(S_mod,
         ::GetNeigh(S_mod, i, j, k, i_n, j_n, idim) - S_ext,
         i, j, k, i_n, j_n, idim);
...
FaceInfoBox::addConnectedNeighbor(i_n, j_n, ps, borrowing_neigh_faces);
borrowing_area[ps] = S_ext;
...
::SetNeigh(flag_info_face, 2, i, j, k, i_n, j_n, idim);
S_mod(i, j, k) = S(i, j, k) + S_ext;
flag_ext_face(i, j, k) = false;
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:681-697`。

所以 one-way 的效果是：

- lender 的 `S_mod` 减少 `S_ext`；
- borrower 的 `S_mod` 增加 `S_ext`；
- lender 标志改成 `2`；
- borrower 的 `flag_ext_face` 置零，表示已稳定；
- 借用关系写进 `m_borrowing`。

## 8. eight-ways extension：按所有可用邻居面积比例分摊

如果 one-way 找不到能一次借满的正交邻居，就进入 eight-ways extension。

它先把 `3x3` 邻域中可用 lender 筛出来：

```cpp
const int flag = GetNeigh(flag_info_face, i, j, k, i_loc - 1, j_loc - 1, idim);
local_avail(i_loc, j_loc) = flag == 1 || flag == 2;
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:438-440`。

然后按每个邻居的原始面面积 `S` 形成总权重：

```cpp
amrex::Real denom = local_avail(0, 1) * GetNeigh(S, i, j, k, -1, 0, idim) +
                    ...
                    local_avail(2, 2) * GetNeigh(S, i, j, k, 1, 1, idim);
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:443-450`。

每个邻居应借出的 patch 是：

```cpp
const amrex::Real patch = S_ext * GetNeigh(S, i, j, k, i_n, j_n, idim) / denom;
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:454-455` 及 `830-831`。

但 WarpX 不会盲目按这个比例分摊。它先循环剔除那些一旦按比例借出就会把自己 `S_mod` 减到非正的邻居：

```cpp
if(::GetNeigh(S_mod, i, j, k, i_n, j_n, idim) - patch <= 0) {
    neg_face = true;
    local_avail(i_n + 1, j_n + 1) = false;
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:832-835`。

只有剔除后仍满足 `denom >= S_ext`，才真正提交这次扩展：

```cpp
if(denom >= S_ext){
    ...
    borrowing_area[ps + count] = patch;
    ::SetNeigh(flag_info_face, 2, i, j, k, i_n, j_n, idim);
    S_mod(i, j, k) += patch;
    ::SetNeigh(S_mod,
             ::GetNeigh(S_mod, i, j, k, i_n, j_n, idim) - patch,
             i, j, k, i_n, j_n, idim);
    ...
    flag_ext_face(i, j, k) = false;
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:849-869`。

因此 eight-ways 的本质是“保正性的按面积加权分摊借用”。

## 9. `init_borrowing()` / `shrink_borrowing()`：先粗分配，再压缩

`init_borrowing()` 一开始给每个 tile 都按最大可能值分配：

```cpp
borrowing_dir.inds.resize(8*ncells);
borrowing_dir.neigh_faces.resize(8*ncells);
borrowing_dir.area.resize(8*ncells);
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:223-230`。

原因很直接：一个 face 最多可能向 8 个邻居建立借用关系。

等 two-pass `PrefixSum` 把真实条目数 `vecs_size` 算出来后，再通过 `shrink_borrowing()` 缩容到实际大小。

所以 `FaceInfoBox` 的内存策略是“先按最坏情况申请，再按实际借用图压缩”。

## 10. BCK correction：ECT 扩展失败时的兜底

如果 eight-ways 之后还有未稳定 face，WarpX 会改走 BCK correction：

```cpp
if (flag_ext_face_max_lev_idim(i, j, k)) {
    S(i, j, k) = ::ComputeSStab<idim>(i, j, k, lx, ly, lz, dx, dy, dz);
    flag_info_face_max_lev_idim(i, j, k) = -1;
}
```

源码位置：`../warpx/Source/EmbeddedBoundary/WarpXFaceExtensions.cpp:196-200`。

源码注释已经明确说明：

- 这是 Benkler-Chavannes-Kuster 方法；
- 它比常规 ECT 精度差；
- 但仍优于纯 staircasing。

所以 BCK 不是和 one-way / eight-ways 并列的主方案，而是“扩展拓扑已经找不到合法借法时的稳定化兜底”。

同时 `flag_info_face = -1` 的意义是：后续 solver 不再把这个 face 当成仍在 extension 图里的节点。

## 11. 最终怎样进入场更新

`WarpX::EvolveB()` 把 `m_flag_info_face` 和 `m_borrowing` 直接传给 FDTD solver：

```cpp
m_fdtd_solver_fp[lev]->EvolveB( m_fields,
                                lev,
                                patch_type,
                                m_flag_info_face[lev], m_borrowing[lev], a_dt );
```

源码位置：`../warpx/Source/FieldSolver/WarpXPushFieldsEM.cpp:971-980`。

在 `FiniteDifferenceSolver::EvolveBCartesianECT()` 里，ECT `B` 更新遇到 `flag_info_cell_dim(i, j, k) == 0` 的不稳定 face，会先聚合 enlarged face 的有效电荷：

```cpp
Venl_dim(i, j, k) = Rho(i, j, k) * S(i, j, k);
...
Venl_dim(i, j, k) += Rho(ip, jp, kp) * borrowing_dim_area[ind];
...
rho_enl = Venl_dim(i, j, k) / S_mod(i, j, k);
```

源码位置：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp:283-339`。

所以 `FaceInfoBox` 记录的不是装饰性元数据，而是 solver 真正用来构造 enlarged face 有效 `rho` 的借用图。

## 12. 当前可以得到的结构性结论

到这一层为止，WarpX 的 EB face extension 机制可以概括为：

1. `MarkExtensionCells()` 用 `S_stab` 判定哪些 face 天生不稳定；
2. `ComputeOneWayExtensions()` 先尝试“单邻居一次借满”；
3. `ComputeEightWaysExtensions()` 再尝试“多邻居按面积比例分摊，但必须保持每个 lender 仍为正面积”；
4. 若还失败，`ApplyBCKCorrection()` 直接把面积抬到稳定阈值；
5. 所有借用关系通过 `FaceInfoBox` 压缩存储，并在 `EvolveBCartesianECT()` 中转化为 enlarged-face `rho`。

因此，ECT + EB 的核心并不是“某些 cut face 不能更新”，而是“WarpX 尝试把不稳定 cut face 重新解释成由周围面拼接出的 enlarged face，再把这个 enlarged topology 传进 `B` 更新”。

## 13. 验证入口

当前最直接的本地验证入口不是一个总目录，而是下面这些测试族：

- `../warpx/Examples/Tests/embedded_boundary_cube/`
- `../warpx/Examples/Tests/embedded_boundary_rotated_cube/`
- `../warpx/Examples/Tests/embedded_boundary_em_particle_absorption/`
- `../warpx/Examples/Tests/embedded_boundary_diffraction/`
- `../warpx/Examples/Tests/embedded_circle/`

对应 checksum 线索包括：

- `../warpx/Regression/Checksum/benchmarks_json/test_2d_embedded_boundary_cube.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_3d_embedded_boundary_cube.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_2d_pml_x_yee_eb.json`
- `../warpx/Regression/Checksum/benchmarks_json/test_rz_embedded_boundary_diffraction.json`

本轮没有运行这些 case；这里只把后续验证入口补齐。

## 14. 下一步

`face extension` 已经把 EB + ECT 的 cut-face 稳定化链条补上。下一篇最自然的顺序是：

1. `ParticleScraper.H`
2. `ParticleBoundaryProcess.H`
3. `DistanceToEB.H`

这样就能把 embedded boundary 从“场更新侧的 cut-face 修正”继续推进到“粒子如何被吸收、裁切和近壁处理”。
