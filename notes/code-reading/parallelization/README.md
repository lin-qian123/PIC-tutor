# Parallelization / AMR 通信源码精读入口

绑定源码：`../warpx/Source/Parallelization`。

## 模块边界

- 构建入口：`Parallelization/CMakeLists.txt`、`Parallelization/Make.package`。
- 主要文件：`WarpXComm.cpp`、`WarpXComm_K.H`、`WarpXRegrid.cpp`、`GuardCellManager.*`、`WarpXSumGuardCells.*`。
- 关联模块：`ablastr/coarsen`、`BoundaryConditions`、`Particles/Sorting`。

## 核心问题

- guard cell fill、sum、copy、AMR interpolation 和 restriction 如何分层执行。
- regrid 如何影响粒子、fields、diagnostics 和 load balance。
- fine/coarse/current/rho/buffer fields 的同步路径是什么。

## 精读顺序

1. `GuardCellManager.*`。
2. `WarpXComm.cpp` 的 fill/sync/copy 入口。
3. `WarpXSumGuardCells.*`。
4. `WarpXRegrid.cpp`。
5. `WarpXComm_K.H` device kernels。

## 输出目标

- `00-guard-cell-model.md`
- `01-current-rho-sync-paths.md`
- `02-regrid-and-load-balance.md`
- `03-amr-coarse-fine-substitution.md`
- `04-warpxcomm-kernel-execution-model.md`

## 当前进度

- 已完成 `00-guard-cell-model.md`：梳理 `GuardCellManager` 中 guard-cell 的分配上限与阶段性需求、`FillBoundaryE/B/F/G/Aux` 的 copy/sync 语义、`WarpXSumGuardCells` 的 source accumulation 语义，以及 `SyncCurrent()` / `SyncRho()` 中 coarse-fine / owner-mask 去重的基本结构。
- 已完成 `01-current-rho-sync-paths.md`：梳理 `SyncCurrent()` / `SyncRho()` 的 finest-to-coarsest 级联、`mf_comm`、`OwnerMask` 去重、`RestrictCurrentFromFineToCoarsePatch` / `AddCurrentFromFineLevelandSumBoundary` 与对应 rho 路径。
- 已完成 `02-regrid-and-load-balance.md`：梳理 `CheckLoadBalance()` 的触发条件、SFC/knapsack 候选映射比较、`load_balance_efficiency_ratio_threshold` 的采纳逻辑、`RemakeLevel()` 的同 `BoxArray` 重映射边界、fields/EB/PSATD/buffer masks/particle boundary buffer/diagnostics 的整体重建，以及 heuristic / timer 两类 costs 更新模型。
- 已完成 `03-amr-coarse-fine-substitution.md`：梳理 `amr.rst` 的 substitution 公式、`UpdateAuxilaryData*()` 的 `aux = fp + I(parent_aux-cp)` 主链、`E/Bfield_cax` 的 coarse-aux 副本角色、`gather/current buffer masks` 的 transition-zone 语义，以及 `PartitionParticlesInBuffers()` 如何把粒子按 fine / lower-level gather-deposit 路径稳定分区。
- 已完成 `04-warpxcomm-kernel-execution-model.md`：梳理 `WarpXComm_K.H` 中 coarse-fine / centering kernel 的分层、`MFIter + Array4 + ParallelFor` 的统一执行壳、`TilingIfNotGPU()` / `Gpu::notInLaunchRegion()` / OpenMP 条件并行的 CPU-GPU 双栈写法，以及 `FillBoundary` 的 `do_single_precision_comms` / `nodal_sync` / `m_safe_guard_cells` 通信策略分支。
- 下一步更适合回到 `Particles/Gather` 与 `Particles/Deposition`，把 `aux` / buffer masks / partition 如何进入具体粒子 kernel 再向下打穿；若暂不回粒子层，则转去 `Diagnostics/` 查看 multi-level container 如何被诊断消费。

## 验证线索

- `Examples/Tests/subcycling/`
- mesh-refinement Langmuir tests。
