# Parallelization 00: guard cell 配额模型、FillBoundary 与 J/rho 同步语义

绑定源码：

- `../warpx/Source/Parallelization/GuardCellManager.H`
- `../warpx/Source/Parallelization/GuardCellManager.cpp`
- `../warpx/Source/Parallelization/WarpXComm.cpp`
- `../warpx/Source/Parallelization/WarpXSumGuardCells.H`
- `../warpx/Source/Parallelization/WarpXSumGuardCells.cpp`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Docs/source/developers/fields.rst`

## 1. 这一层要回答什么

边界与 AMR 一旦进入多 box / 多 level，就不能只说“场有 guard cells”。在 WarpX 里，真正决定通信量、局部 stencil 可用范围和 coarse-fine 同步节奏的是一整套 guard-cell 配额模型：

1. 每类 MultiFab 一开始分配多少 guard cells；
2. PIC 循环的不同阶段实际交换多少；
3. E/B 这类场为什么用 `FillBoundary`，而 J/rho 为什么必须用 `SumBoundary` 风格的累加；
4. mesh refinement 时 coarse/fine current 与 charge 怎样并入同一层。

`GuardCellManager` 和 `WarpXComm.cpp` 就是在定义这套模型。

## 2. `guardCellManager`：先区分“分配多少”和“每阶段用多少”

`GuardCellManager.H` 先把两类量分开了。

### 2.1 分配量

- `ng_alloc_EB`
- `ng_alloc_J`
- `ng_alloc_Rho`
- `ng_alloc_F`
- `ng_alloc_G`

它们表示 MultiFab 实际分配的 guard-cell 厚度。

### 2.2 使用量

- `ng_FieldSolver`
- `ng_FieldSolverF`
- `ng_FieldSolverG`
- `ng_FieldGather`
- `ng_UpdateAux`
- `ng_MovingWindow`
- `ng_afterPushPSATD`
- `ng_depos_J`
- `ng_depos_rho`

源码位置：`../warpx/Source/Parallelization/GuardCellManager.H:78-114`。

因此 WarpX 不是“每次都把所有 guard cells 全交换”，而是先分配上限，再按 PIC 循环阶段申请较小子集。

## 3. guard-cell 初值首先由粒子形函数、subcycling 和运动范围决定

`GuardCellManager::Init()` 一上来不是先看 field solver，而是先看粒子。

### 3.1 subcycling 会多要一层

```cpp
int ngx_tmp = (max_level > 0 && do_subcycling) ? nox+1 : nox;
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:58-61`。

注释说明原因是：细层 subcycling 时，粒子在两次重分布前会连续推两步，所以局部沉积/访问范围更大。

### 3.2 Galilean / comoving 再多加一层

```cpp
if (galilean || comoving)
{
  ngx_tmp += 1;
  ngy_tmp += 1;
  ngz_tmp += 1;
}
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:68-74`。

### 3.3 E/B 的 guard cell 强制取偶数

```cpp
int ngx = (ngx_tmp % 2) ? ngx_tmp+1 : ngx_tmp;
...
const int ngz_nonci = (ngz_tmp % 2) ? ngz_tmp+1 : ngz_tmp;
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:81-84`。

注释给出的理由是 coarse-to-fine 插值更方便。相比之下，J 只需要 fine-to-coarse，因此不强制偶数：

```cpp
int ngJx = ngx_tmp;
int ngJy = ngy_tmp;
int ngJz = ngz_tmp;
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:91-94`。

所以 WarpX 在 guard-cell 设计上已经把“场插值约束”和“源项 restriction 约束”区分开了。

## 4. moving window、NCI、滤波和 solver stencil 会继续推高配额

### 4.1 moving window

```cpp
if (do_moving_window) {
    ...
    ngx = std::max(ngx,max_r);
    ...
    ngJz = std::max(ngJz,max_r);
}
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:98-112`。

含义是：只要窗口会整体平移，guard-cell 配额至少得容纳一次窗口位移。

### 4.2 电磁显式推进再叠加粒子传播距离

```cpp
ng_alloc_Rho[i] += static_cast<int>(std::ceil(PhysConst::c * dt_Rho / dx[i]));
ng_alloc_J[i]   += static_cast<int>(std::ceil(PhysConst::c * dt_J / dx[i]));
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:156-157`。

这里把“粒子在一个或半个时间步里能跨过多少 cell”直接转成 guard-cell 需求。

### 4.3 bilinear current filter 会额外扩 J

```cpp
if (use_filter)
{
    ng_alloc_J += bilinear_filter_stencil_length - amrex::IntVect(1);
}
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:187-190`。

### 4.4 PSATD 会按 FFT stencil 重新统一所有配额

PSATD 分支里，`nx_guard/ny_guard/nz_guard` 默认依据谱阶和 grid type 估计，随后取各类字段需求的最大值：

```cpp
ng_required = std::max(ng_required, ng_alloc_EB[i_dim]);
ng_required = std::max(ng_required, ng_alloc_J[i_dim]);
ng_required = std::max(ng_required, ng_alloc_Rho[i_dim]);
ng_required = std::max(ng_required, ng_alloc_F[i_dim]);
...
ng_alloc_EB[i_dim] = ng_required;
ng_alloc_J[i_dim] = ng_required;
ng_alloc_F[i_dim] = ng_required;
ng_alloc_Rho[i_dim] = ng_required;
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:252-261`。

这一步很关键。它意味着在 PSATD 下，guard-cell 配额不再主要由粒子 shape 或 Yee stencil 决定，而要服从局部 FFT stencil 截断误差模型。

## 5. 分配完上限后，再生成“阶段性需求”

这一段最重要的不是数值，而是思路：

### 5.1 `ng_FieldSolver`

- PSATD：直接等于分配上限；
- FDTD：来自 `CartesianYee/Nodal/CKC` 或 cylindrical/spherical algorithm 的 `GetMaxGuardCell()`。

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:265-303`。

### 5.2 `ng_FieldGather`

```cpp
int const FGcell = (nox + 1) / 2;
auto ng_FieldGather_noNCI = IntVect(...);
...
ng_FieldGather = ng_FieldGather_noNCI + ng_NCIFilter;
...
ng_FieldGather = ng_FieldGather.max(ng_FieldSolver);
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:333-366`。

也就是说，field gather 的 guard cells 首先由粒子 shape 决定，但最终不能小于下一次 field solve 需要的 stencil 宽度。

### 5.3 `ng_UpdateAux`

```cpp
ng_UpdateAux = 2*ng_FieldGather_noNCI + ng_NCIFilter;
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:357-358`。

这反映了 aux 网格不是单纯复制主场，而是还要支持 staggered-to-nodal 转换和 particle gather，所以需求更大。

### 5.4 safe mode

```cpp
if (safe_guard_cells){
    ng_FieldSolver = ng_alloc_EB;
    ...
    ng_FieldGather = ng_alloc_EB;
    ng_UpdateAux = ng_alloc_EB;
}
```

源码位置：`../warpx/Source/Parallelization/GuardCellManager.cpp:322-332`。

safe mode 的真实意义不是“更保守一点”，而是完全放弃阶段性压缩策略，每次通信都直接交换分配上限，用于调试。

## 6. `FillBoundaryE/B/F/G/Aux`：场通信的基本语义是 copy，不是 add

开发者文档 `fields.rst` 直接点明：

- E/B guard cells 用 `FillBoundary`
- J/rho guard cells 用 `SumBoundary`

文档位置：`../warpx/Docs/source/developers/fields.rst:95-104`。

`WarpXComm.cpp` 里 `FillBoundaryE()` / `FillBoundaryB()` 也体现了这一点。

以 `FillBoundaryE()` 为例：

1. 先处理 PML 与 valid domain 的数据交换；
2. 再对 valid domain 做普通 guard-cell 填充。

```cpp
if (do_pml)
{
    ...
    pml[lev]->Exchange(mf_pml, mf, patch_type, do_pml_in_domain);
    pml[lev]->FillBoundary(mf_pml, patch_type, nodal_sync);
}
...
ablastr::utils::communication::FillBoundary(*mf[i], nghost, do_single_precision_comms, period, nodal_sync);
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:780-821`。

这里的语义就是复制/同步邻居有效区数据到 guard cells，而不是把重叠区域相加。

## 7. 为什么 J/rho 不能只用 `FillBoundary`

因为粒子沉积的几何语义不同。

`SyncCurrent()` 的注释写得很明确：

- 粒子靠近 box 边界时，可能把同一个 `(i,j,k)` 同时沉积到一个 box 的 guard/edge 区和另一个 box 的 valid 区；
- 因此 after-deposition 必须把重叠区域的贡献累加，结果才等价于“全域只有一个大 box”。

源码注释位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1198-1215`。

因此，源项同步需要的是 **sum over overlaps**，不是 **copy from neighbors**。

## 8. `WarpXSumGuardCells`：J/rho 的同层同步是加法语义

`WarpXSumGuardCells.H` 的接口文档已经说明：

```cpp
/** Sum the values of `mf`, where the different boxes overlap
 * (i.e. in the guard cells)
 *
 * This is typically called for the sources of the Maxwell equations (J/rho)
 * after deposition from the macroparticles.
 */
```

源码位置：`../warpx/Source/Parallelization/WarpXSumGuardCells.H:11-22`。

实现也很薄：

```cpp
ablastr::utils::communication::SumBoundary(mf, ...);
```

或：

```cpp
dst.setVal(0., ...);
dst.ParallelAdd(src, ...);
```

源码位置：`../warpx/Source/Parallelization/WarpXSumGuardCells.cpp:15-36`。

这说明 WarpX 在同层 source 同步上的核心语义就是：

- 允许不同 box 在 guard/valid overlap 里各自先沉积；
- 之后再做 overlap accumulation。

## 9. `SyncCurrent()`：多层 AMR 下不是“先 sum 再 restriction”，而是 finest-to-coarsest 级联

`SyncCurrent()` 的大注释是并行/AMR 模块里最关键的说明之一。它明确指出：

1. finest level 先处理自己；
2. 若有 finer level，则其 coarse patch 数据会并到当前 level 的 fine patch；
3. 但不能直接 `ParallelAdd` 到当前 level 的 `fp`，因为 nodal overlap 会双计数；
4. 因此需要：
   - 临时 `fine_lev_cp`
   - `OwnerMask`
   - 只让拥有者把 coarse-patch 数据加到当前 `fp`

关键代码：

```cpp
fine_lev_cp.ParallelAdd(*mf_comm, 0, 0, ncomp, mf_comm->nGrowVect(),
                        IntVect(0), period);
auto owner_mask = amrex::OwnerMask(fine_lev_cp, period);
...
if (mma[bno](i,j,k) && sma[bno](i,j,k,n) != 0.0_rt) {
    dma[bno](i,j,k,n) += sma[bno](i,j,k,n);
}
```

源码位置：`../warpx/Source/Parallelization/WarpXComm.cpp:1284-1302`。

所以 WarpX 对 nodal coarse-fine current 同步的真实处理不是 naïve `ParallelAdd`，而是“先接收、再 owner-mask 去重、最后并入”。

## 10. `SyncCurrentAndRho()`：主循环里这一切在哪发生

在 `WarpXEvolve.cpp`，所有这些 guard-cell / source 通信被总装到：

```cpp
SyncCurrentAndRho();
```

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:559-561`。

其 FDTD 路径很简单：

```cpp
SyncCurrent("current_fp");
SyncRho();
```

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:800-804`。

PSATD 则根据 `periodic_single_box`、`current_correction`、`Vay deposition` 是否启用，决定是现在同步还是推迟到谱推进路径里。

同步后还会立刻施加 PEC 相关的 rho/J 边界反射：

```cpp
ApplyRhofieldBoundary(...)
ApplyJfieldBoundary(...)
```

源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:807-825`。

因此，从主循环视角看，`SyncCurrentAndRho()` 不是一个“可有可无的并行后处理”，而是 deposition 与后续 field solve 之间的物理一致性关口。

## 11. 当前可以得到的结构性结论

到这一层为止，WarpX 并行/AMR 通信模型可以先归纳成四条：

1. guard cells 先由 `GuardCellManager` 统一预算，预算来源同时包含：
   - particle shape
   - subcycling
   - moving window
   - NCI / filter
   - field solver stencil
   - PSATD FFT stencil
2. E/B/F/G/Aux 的同层 guard-cell 通信语义是 `FillBoundary` 式复制/同步。
3. J/rho 的同层 guard-cell 通信语义是 `SumBoundary` / `ParallelAdd` 式累加，因为 deposition 可在重叠区域重复发生。
4. mesh refinement 下 coarse/fine source 同步还要再额外解决 nodal overlap 双计数问题，所以 `SyncCurrent()` / `SyncRho()` 不是简单 restriction，而是带 `OwnerMask` 的 finest-to-coarsest 级联。

## 12. 这篇笔记的边界

这篇只把并行层的 guard-cell 模型和通信语义固定下来，还没有展开：

- `RestrictCurrentFromFineToCoarsePatch`
- `AddCurrentFromFineLevelandSumBoundary`
- `WarpXRegrid.cpp`

这些应放到后续两篇：

1. `01-current-rho-sync-paths.md`
2. `02-regrid-and-load-balance.md`

## 13. 验证入口

当前最直接的验证入口仍是：

- `../warpx/Examples/Tests/subcycling/`
- mesh-refinement Langmuir tests

另外，PSATD guard-cell 经验模型还与官方工作流文档直接对应：

- `../warpx/Docs/source/usage/workflows/psatd_stencil.rst`

本轮没有运行这些案例，只先把源码与文档链条补齐。
