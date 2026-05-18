# 34 sync current rho and source synchronization：`SyncCurrentAndRho()` 如何把局部沉积变成场求解器可消费的全局源项

绑定源码：

- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Source/Parallelization/WarpXComm.cpp`

前置阅读：

- `../notes/code-reading/particles/04-amr-gather-deposition-buffers.md`
- `../notes/code-reading/particles/32-current-deposition-continuity-and-geometry-boundaries.md`
- `../notes/code-reading/particles/33-mass-matrix-and-temperature-variance-deposition.md`

前几轮已经把粒子沉积主线压成了：

- `rho/J` 的离散连续性合同；
- `Direct / Esirkepov / Villasenor / Vay` 的算法分叉；
- `MassMatrices_*` 与 `temperature/variance` 这种非 Maxwell 源项的沉积支线。

但只看到 deposition kernel 还不够。粒子刚沉完时，`rho/J` 还只是：

- 本 tile 的局部贡献；
- 本 level 的局部 box 数据；
- 或 coarse-fine buffer / coarse patch 上的中间容器。

真正给 field solver 用的源项，要经过 `SyncCurrentAndRho()` 这条同步链。

## 1. 顶层时序：主循环先沉积，再统一做 source synchronization

主循环在 `WarpXEvolve.cpp` 里先 `PushParticlesandDeposit(...)`，随后立即调用：

```cpp
// Synchronize J and rho:
// filter (if used), exchange guard cells, interpolate across MR levels
// and apply boundary conditions
SyncCurrentAndRho();
```

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:555-561`。

这一步的职责不是“顺手通信一下”，而是把粒子侧局部沉积升级为：

1. same-level box 间一致；
2. fine/coarse 间一致；
3. filter 和 current-centering 后一致；
4. boundary 条件后可直接被 field solver 消费。

## 2. `SyncCurrentAndRho()` 的第一层分叉：`PSATD` 与 `FDTD` 不同

顶层分派在 `../warpx/Source/Evolve/WarpXEvolve.cpp:768-837`。

### 2.1 `PSATD + periodic single box`

这时即使启用了：

- `current correction`
- `Vay deposition`

也立即同步：

```cpp
std::string const current_fp_string = (current_deposition_algo == CurrentDepositionAlgo::Vay)
    ? "current_fp_vay" : "current_fp";
SyncCurrent(current_fp_string);
SyncRho();
```

源码位置：`WarpXEvolve.cpp:777-784`。

这说明 periodic single-box 下，source synchronization 可以在这里一次性收口。

### 2.2 `PSATD + 非 periodic single box`

这时只有在

- 没开 `current_correction`
- 且不是 `Vay deposition`

的情况下，才立刻做：

```cpp
SyncCurrent("current_fp");
SyncRho();
```

源码位置：`WarpXEvolve.cpp:789-796`。

如果：

- `current_correction == true`
- 或 `current_deposition_algo == Vay`

则同步推迟到 `PushPSATD` 里更晚的阶段。这说明对 PSATD 来说，source synchronization 时序本身就是算法合同的一部分，不是沉积之后永远立刻做。

### 2.3 `PSATD + Vay deposition` 的特殊处理

在非 periodic single-box 分支下，Vay 还有一条额外逻辑：

```cpp
if (current_deposition_algo == CurrentDepositionAlgo::Vay)
{
    // TODO This works only without mesh refinement
    const int lev = 0;
    if (use_filter) {
        ApplyFilterMF(m_fields.get_mr_levels_alldirs(FieldType::current_fp_vay, finest_level), lev);
    }
}
```

源码位置：`WarpXEvolve.cpp:798-806`。

这说明当前 worktree 里：

- `current_fp_vay` 是单独的 source family；
- 它在这里最多只先做 filter；
- 而且这条逻辑当前只假定 **无 mesh refinement**。

### 2.4 `FDTD`

FDTD 路径最直接：

```cpp
SyncCurrent("current_fp");
SyncRho();
```

源码位置：`WarpXEvolve.cpp:809-813`。

因此 source synchronization 的复杂时序主要来自 PSATD，而不是 FDTD。

## 3. `SyncCurrentAndRho()` 的最后一步不是通信，而是边界条件

顶层同步做完后，`SyncCurrentAndRho()` 还会对每个 level 调：

- `ApplyRhofieldBoundary(...)`
- `ApplyJfieldBoundary(...)`

分别作用于：

- fine patch 的 `rho_fp/current_fp`
- coarse patch 的 `rho_cp/current_cp`

源码位置：`WarpXEvolve.cpp:815-836`。

所以这条函数的完整职责是：

1. 同步；
2. 过滤；
3. fine/coarse 汇总；
4. 最后再施加 PEC/PMC/PECInsulator 等边界镜像或反射规则。

它不是单纯 MPI/guard-cell helper。

## 4. `SyncCurrent()` 的第一层真实工作：同层 box 间求和、fine-to-coarse 合并、去重、过滤

`SyncCurrent()` 位于 `../warpx/Source/Parallelization/WarpXComm.cpp:1170-1370`。

它的结构可以压成四步。

### 4.1 可选 current centering：先把 nodal current 变回 staggered current

如果打开 `do_current_centering`，会先从 `current_fp_nodal` 生成 `current_fp`：

```cpp
UpdateCurrentNodalToStag(
    *J_fp[lev][dir], *J_fp_nodal[lev][dir], ...);
```

源码位置：`WarpXComm.cpp:1180-1196`。

因此 `SyncCurrent()` 不是只处理通信，它还可能先做一个 nodal-to-staggered 的源项重排。

### 4.2 finest-to-coarsest 迭代：先 coarsen 未过滤、未求和的 fine current

对 `lev > 0`，它先把当前 fine level 的 `J_fp` coarsen 到同 level 的 `J_cp`：

```cpp
ablastr::coarsen::average::Coarsen(*J_cp[lev][Direction{idim}],
                                   *J_fp[lev][Direction{idim}],
                                   refRatio(lev-1));
```

源码位置：`WarpXComm.cpp:1310-1313`。

这一步刻意发生在 filter 和 same-level SumBoundary 之前。也就是说，fine-to-coarse 传下去的是 **未过滤、未求和** 的 fine source。

### 4.3 current buffer 会先和 `J_cp` 合并，再统一作为跨 level 通信源

如果存在 `current_buf`，源码会先：

```cpp
MultiFab::Add(*J_buffer[lev][Direction{idim}], *J_cp[lev][Direction{idim}], ...)
mf_comm = alias(J_buffer[lev][Direction{idim}])
```

否则直接拿 `J_cp` 做 `mf_comm`。

源码位置：`WarpXComm.cpp:1314-1328`。

这说明 coarse-fine buffer 不是同步后的附属容器，而是跨 level 源项通信链的一部分。

### 4.4 coarse level 接收时要用 owner mask 去掉 nodal overlap double counting

`lev < finest_level` 时，fine level 传下来的 `mf_comm` 先 `ParallelAdd` 到一个临时 `fine_lev_cp`，然后再用 `OwnerMask(...)` 选出单一 owner：

```cpp
if (mma[bno](i,j,k) && sma[bno](i,j,k,n) != 0.0_rt) {
    dma[bno](i,j,k,n) += sma[bno](i,j,k,n);
}
```

源码位置：`WarpXComm.cpp:1260-1294`。

这是一个很关键的实现点：如果直接把 fine-coarse 通信结果并进当前 level 的 `J_fp`，在 nodal overlap 或 periodic overlap 处会 double count。

因此 `SyncCurrent()` 的本质不是简单 `ParallelAdd + SumBoundary`，而是：

1. 临时接收；
2. owner-mask 去重；
3. 再并到真正的 `J_fp`。

## 5. `SyncCurrent()` 的 filter / SumBoundary 顺序也是合同的一部分

在每个 level 的当前方向上，源码最后总是：

1. 如需要，先 `ApplyFilterMF(J_fp, lev, idim)`；
2. 再 `SumBoundaryJ(J_fp, lev, idim, period)`。

源码位置：`WarpXComm.cpp:1331-1338`。

对 finer level 传下来的 `J_cp` 也是：

1. 先按该 level 的 filter 规则处理；
2. 再做 `SumBoundaryJ(...)`。

源码位置：`WarpXComm.cpp:1295-1303`。

所以这里 filter 不是同步后附加的 cosmetic smoothing，而是 source synchronization chain 的正式一环。

## 6. `SumBoundaryJ()` 不是无脑求和，它只汇总足够覆盖 deposition 和 filter stencil 的 guard 区

`SumBoundaryJ()` 位于 `WarpXComm.cpp:1516-1557`。

它先从：

- `get_ng_depos_J()`

出发，再根据：

- current centering stencil
- bilinear filter stencil

扩展出实际要汇总的 `ng_depos_J`，最后才做：

```cpp
WarpXSumGuardCells(J, period, src_ngrow, icomp, ncomp);
```

因此这里的 same-level 同步范围不是整个 ghost region，而是“沉积和后续 filter 真正需要的那一部分 guard cells”。

## 7. `SyncRho()` 与 `SyncCurrent()` 结构平行，但对象更简单

`SyncRho()` 位于 `WarpXComm.cpp:1379-1451`，整体逻辑和 `SyncCurrent()` 平行：

1. finest-to-coarsest 迭代；
2. `rho_fp -> rho_cp` coarsen；
3. 若存在 `rho_buf`，先和 `rho_cp` 合并；
4. coarse level 用临时 `fine_lev_cp + OwnerMask` 去重后再并入 `rho_fp`；
5. 最后对每个 level 调 `ApplyFilterandSumBoundaryRho(...)`。

它比 current 少一层：

- 没有 `do_current_centering`
- 没有方向分量循环

但 fine/coarse + buffer + owner-mask 去重的骨架相同。

## 8. `ApplyFilterandSumBoundaryRho()` 暴露了 rho 同步和 current 同步的一个差别

`ApplyFilterandSumBoundaryRho()` 位于 `WarpXComm.cpp:1677-1692`。

如果 `use_filter`：

1. 先构造临时 `rf`
2. `bilinear_filter.ApplyStencil(rf, rho, ...)`
3. 再 `WarpXSumGuardCells(rho, rf, period, ng_depos_rho, ...)`

否则直接：

```cpp
WarpXSumGuardCells(rho, period, ng_depos_rho, icomp, ncomp);
```

和 current 相比，这里最显著的差别是：

- current 用 `ApplyFilterMF` 先改写原 `J`
- rho 这边 filter 后再通过 `WarpXSumGuardCells(rho, rf, ...)` 把 filtered 数据并回

所以 `SyncCurrent()` 和 `SyncRho()` 结构平行，但具体 filter/sum 实现并不完全一样。

## 9. 这条线回到第 5 章后，更稳定的结论是什么

`SyncCurrentAndRho()` 不该再被概括成一句：

- “filter、exchange guard cells、interpolate across MR levels、apply boundary conditions”

更稳定的分层应该是：

1. 顶层时序分叉
   - `PSATD periodic single box`
   - `PSATD non-single-box`
   - `current correction`
   - `Vay deposition`
   - `FDTD`
2. current 同步主链
   - current centering
   - fine-to-coarse coarsen
   - buffer 合并
   - owner-mask 去重
   - filter
   - SumBoundary
3. rho 同步主链
   - fine-to-coarse coarsen
   - buffer 合并
   - owner-mask 去重
   - `ApplyFilterandSumBoundaryRho`
4. 最后边界条件
   - `ApplyRhofieldBoundary`
   - `ApplyJfieldBoundary`

## 10. 当前前沿

最自然的下一步有两条：

1. 把这条 source-synchronization 分层回填到 `manuscript/chapters/05-deposition-shapes.md`。
2. 然后转去验证层，把
   - Langmuir PSATD current correction
   - `vay_deposition`
   这两组 regression 更明确挂到本地 source-synchronization 边界上。
