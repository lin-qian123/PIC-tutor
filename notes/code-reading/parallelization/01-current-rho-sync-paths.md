# Parallelization 01: current / rho 的 coarse-fine 同步路径

绑定源码：

- `../warpx/Source/Parallelization/WarpXComm.cpp`
- `../warpx/Source/Parallelization/WarpXSumGuardCells.H`
- `../warpx/Source/Parallelization/WarpXSumGuardCells.cpp`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Docs/source/developers/fields.rst`

## 1. 这一层要回答什么

上一篇已经把 guard-cell 预算和 `FillBoundary` / `SumBoundary` 的基本语义固定下来了。接下来真正关键的问题是：

1. `SyncCurrent()` / `SyncRho()` 到底按什么顺序处理同层和跨层源项；
2. current/charge 在 coarse patch、buffer patch、fine patch 之间怎样流动；
3. 什么时候先 filter，什么时候先 coarsen，什么时候再 `SumBoundary`；
4. 为什么 WarpX 需要 `OwnerMask`、temporary `MultiFab` 和 `mf_comm` 这样的中间层。

这一篇只做 source 同步主链，不展开 `WarpXRegrid.cpp`。

## 2. 主循环里的位置：deposition 之后、场边界之前

`WarpXEvolve.cpp` 里，沉积后的总入口是：

```cpp
SyncCurrentAndRho();
```

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:559-561`。

它的结构是：

- 先根据 solver 路径调用 `SyncCurrent(...)` / `SyncRho()`；
- 然后才做 PEC 相关的 `ApplyRhofieldBoundary()` / `ApplyJfieldBoundary()`。

```cpp
SyncCurrent("current_fp");
SyncRho();
...
ApplyRhofieldBoundary(...)
ApplyJfieldBoundary(...)
```

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:800-825`。

所以 `SyncCurrentAndRho()` 的真实角色不是 MPI housekeeping，而是 deposition 与物理边界条件之间的源项一致性关口。

## 3. `SyncCurrent()` 的总算法：从 finest 往 coarse 级联

`SyncCurrent()` 的大段注释已经把算法设计讲透了。核心不是一句“同步 current”，而是一整套 finest-to-coarsest 级联流程：

1. 如果需要 current centering，先把 nodal current 转成 staggered current；
2. 从 finest level 往下遍历；
3. 同层对 `J_fp` 做 filter + `SumBoundary`；
4. 若有 finer level，把 finer 的 coarse-patch current（以及可选 buffer）并到当前 level 的 fine patch；
5. 为避免 nodal overlap 双计数，不能直接 `ParallelAdd` 到 `J_fp`，必须借助临时 `fine_lev_cp` 和 `OwnerMask`。

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1174-1342`。

## 4. 第零步：可选的 nodal-to-staggered current centering

若 `do_current_centering` 为真，`SyncCurrent()` 开头先调用：

```cpp
::UpdateCurrentNodalToStag(
    *J_fp[lev][dir], *J_fp_nodal[lev][dir],
    m_current_centering_nox, m_current_centering_noy, m_current_centering_noz,
    ...
);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1188-1195`。

这一步的物理意义是：沉积可能先落在 nodal current 容器上，但后续 FDTD/Yee 路径需要 staggered current，因此同步前先做有限阶 centering。

这也解释了为什么 `SumBoundaryJ()` 在计算 `src_ngrow` 时，若启用了 current centering，还要把 `m_current_centering_no* / 2` 加回去。

## 5. 同层同步：`SumBoundaryJ()` 不是简单 wrapper，而是带 deposition/filter 语义

`SumBoundaryJ()` 先重建“真正可能被源项写到的最大区域”：

```cpp
amrex::IntVect ng_depos_J = get_ng_depos_J();
...
if (do_current_centering) { ... += m_current_centering_no* / 2; }
if (use_filter) {
    ng_depos_J += bilinear_filter.stencil_length_each_dir - amrex::IntVect(1);
}
ng_depos_J.min(ng);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1320-1339`。

然后才调用：

```cpp
WarpXSumGuardCells(J, period, src_ngrow, icomp, ncomp);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1340-1341`。

所以 `SumBoundaryJ()` 不是“把所有 guard cells 都加一遍”，而是只在 deposition + centering + filtering 真正可能影响到的区域里做累加。

## 6. finest level 向下传递：`mf_comm` 是跨层通信载体

`SyncCurrent()` 用：

```cpp
std::unique_ptr<MultiFab> mf_comm;
for (int lev = finest_level; lev >= 0; --lev)
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1271-1274`。

其含义是：

- 当前 level 处理完后，把“需传给更粗层的信息”打包进 `mf_comm`；
- 下一轮循环（更粗 level）把它并入当前 fine patch。

这比在每层直接互相操作 `fp/cp/buffer` 清晰得多，也减少了通信分支爆炸。

## 7. 从 fine patch 到同层 coarse patch：先 coarsen，再决定是否并入 buffer

在 `lev > 0` 的 fine level 上，`SyncCurrent()` 先把当前 fine patch restriction 到 coarse patch：

```cpp
J_cp[lev][Direction{idim}]->setVal(0.0);
ablastr::coarsen::average::Coarsen(*J_cp[lev][Direction{idim}],
                                   *J_fp[lev][Direction{idim}],
                                   refRatio(lev-1));
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1314-1318`。

若存在 current buffer，则：

```cpp
MultiFab::Add(*J_buffer[lev][Direction{idim}], *J_cp[lev][Direction{idim}], 0, 0, ncomp, ng);
mf_comm = std::make_unique<MultiFab>(*J_buffer[lev][Direction{idim}], amrex::make_alias, 0, ncomp);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1321-1328`。

否则 `mf_comm` 直接 alias 到 `J_cp[lev]`。

这一步的设计非常实用：

- coarse patch 仍保留原始意义；
- 但如果 buffer 存在，就把要跨层发送的量合并到 buffer 容器里，减少额外通信对象。

## 8. finer level 回灌到当前 fine patch：为什么需要 `OwnerMask`

当 `lev < finest_level` 时，当前层要接收 finer level 传来的 coarse-patch 信息：

```cpp
MultiFab fine_lev_cp(J_fp[lev][Direction{idim}]->boxArray(),
                     J_fp[lev][Direction{idim}]->DistributionMap(),
                     ncomp, 0);
fine_lev_cp.setVal(0.0);
fine_lev_cp.ParallelAdd(*mf_comm, 0, 0, ncomp, mf_comm->nGrowVect(),
                        IntVect(0), period);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1280-1285`。

问题在于：对于 nodal 数据，同一个物理点可能在多个 box 中都存在。若直接把 `fine_lev_cp` 加回 `J_fp[lev]`，后续同层 `SumBoundary` 时就会双计数。

因此 WarpX 立刻构造：

```cpp
auto owner_mask = amrex::OwnerMask(fine_lev_cp, period);
...
if (mma[bno](i,j,k) && sma[bno](i,j,k,n) != 0.0_rt) {
    dma[bno](i,j,k,n) += sma[bno](i,j,k,n);
}
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1287-1300`。

这意味着 coarse-fine 回灌不是“让所有 overlap 都收一次”，而是“只让 owner box 真正接管这份数据，再交给后续 SumBoundary 扩散”。

这就是 WarpX 解决 nodal coarse-fine 双计数的核心机制。

## 9. `J_cp` / `J_fp` 的 filter 和 `SumBoundary` 顺序并不相同

`SyncCurrent()` 的细节里最容易搞混的是顺序。

### 9.1 当前层的 `J_fp`

在每层循环末尾：

```cpp
if (use_filter)
{
    ApplyFilterMF(J_fp, lev, idim);
}
SumBoundaryJ(J_fp, lev, idim, period);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1335-1341`。

即：先 filter，再同层 accumulate。

### 9.2 finer level 的 `J_cp`

只有在更粗层接收完 finer contribution 后，才：

```cpp
if (use_filter)
{
    ApplyFilterMF(J_cp, lev+1, idim);
}
SumBoundaryJ(J_cp, lev+1, idim, period);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1302-1304`。

这说明 WarpX 刻意把 `J_cp` 的处理延后到它真正完成 coarse-fine 回灌职责之后，避免把“尚未发给更粗层的数据”提前变形。

## 10. `SyncRho()`：结构几乎平行，但 filter 入口不同

`SyncRho()` 的主体与 `SyncCurrent()` 是平行结构：

- finest-to-coarsest 遍历
- `mf_comm`
- `fine_lev_cp`
- `OwnerMask`
- coarse patch restriction
- 可选 buffer 合并

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1385-1455`。

但 rho 有一个差异：filter/sum 被合并成 `ApplyFilterandSumBoundaryRho(...)`，而不是分开写。

### 10.1 无 filter

```cpp
WarpXSumGuardCells(rho, period, ng_depos_rho, icomp, ncomp);
```

### 10.2 有 bilinear filter

```cpp
MultiFab rf(rho.boxArray(), rho.DistributionMap(), ncomp, ng);
bilinear_filter.ApplyStencil(rf, rho, glev, icomp, 0, ncomp);
WarpXSumGuardCells(rho, rf, period, ng_depos_rho, icomp, ncomp );
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1685-1696`。

这意味着：

- current 的 filter 通常先写回原 `J` MultiFab 再 sum；
- rho 的 filter 常常先写到临时 `rf`，再把 filtered result accumulate 回目标 `rho`。

## 11. 显式 coarse-patch 更新函数：`Restrict*` 与 `Add*`

除了统一的 `SyncCurrent()` / `SyncRho()`，`WarpXComm.cpp` 还把 coarse-fine 源项路径拆成更显式的辅助函数。

### 11.1 `RestrictCurrentFromFineToCoarsePatch`

只做一件事：

```cpp
ablastr::coarsen::average::Coarsen(*crse[0], *fine[0], refinement_ratio );
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1457-1475`。

它不管 filter，不管同层通信，不管 buffer。

### 11.2 `AddCurrentFromFineLevelandSumBoundary`

这个函数更贴近“边界与 AMR”的语义。它会：

1. 先对当前 level `J_fp` 做 filter + `SumBoundary`；
2. 再根据 finer `J_cp` 和 `J_buffer` 的存在与否，分别处理四种组合；
3. 通过 `ablastr::utils::communication::ParallelAdd` 把 finer current 投到临时 `mf`；
4. 再把 `mf` 加回当前 `J_fp[lev]`。

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1575-1651`。

它比 `SyncCurrent()` 更显式地暴露出：

- coarse patch
- buffer patch
- current buffer
- filter
- same-level accumulation

之间的组合逻辑。

### 11.3 `RestrictRhoFromFineToCoarsePatch` / `AddRhoFromFineLevelandSumBoundary`

rho 侧与 current 完全对称，只是调用的是 `ApplyFilterandSumBoundaryRho()`。

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1653-1782`。

## 12. `WarpXComm_K.H` 在这一层的角色

本轮只需要用到一个判断：`WarpXComm_K.H` 里的 `warpx_interp(...)` 系列 kernel 主要服务 `UpdateAuxilaryDataSameType/StagToNodal`，即 field gather 所用 aux 网格的 coarse/fine 插值。

它不是这篇笔记里 current/rho 同步链条的主体，但说明了同一个 `Parallelization` 模块同时负责：

- 源项同步
- aux field coarse/fine 插值

这也是为什么第 7 章里 guard-cell、source synchronization、aux communication 不应被拆成彼此无关的小节。

## 13. 当前可以得到的结构性结论

到这一层为止，WarpX 的 current / rho coarse-fine 同步路径可以归纳成：

1. 先在各自 level 上沉积；
2. 同层 overlap 用 `SumBoundary` 语义累加，而不是 copy；
3. finer level 先 restriction 到 coarse patch；
4. 若存在 buffer，则 coarse patch 先并入 buffer，再作为跨层通信源；
5. 更粗层接收 finer 数据时，先进入临时 `fine_lev_cp`；
6. 对 nodal overlap，用 `OwnerMask` 只让 owner box 接管这些数据；
7. 之后再对当前层做本层 filter / sum；
8. `SyncCurrentAndRho()` 完成后，才进入 PEC rho/J 反射与后续 field solve。

因此，WarpX 的 coarse-fine source 同步不是单纯“restriction + prolongation”，而是：

`restriction -> optional buffer merge -> coarse-level injection with owner-mask de-dup -> same-level accumulation`

的组合。

## 14. 这篇笔记的边界

这篇已经把 current/rho 主同步链讲清了，但还没展开：

- `WarpXRegrid.cpp`
- `LoadBalance()`
- `RemakeLevel()`
- EB 数据和 particle boundary buffer 在 regrid / remake 后怎样重建

这些应进入下一篇 `02-regrid-and-load-balance.md`。

## 15. 验证入口

这一层最直接相关的验证入口包括：

- `../warpx/Examples/Tests/subcycling/`
- mesh-refinement Langmuir tests

开发者文档中与这条链直接对应的索引是：

- `../warpx/Docs/source/developers/fields.rst`

本轮没有运行案例，只把源码同步链与文档索引补齐。
