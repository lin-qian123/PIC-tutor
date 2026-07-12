# Transition-zone route-count implementation packet

## 目标

关闭 2D MR Esirkepov 当前 `BOUNDARY` 的最小 WarpX-side change surface：记录粒子在 fine interior 与 transition buffer 之间的路由、`rho/J` 中间场账本和同步后的 coarse closure。该 packet 只描述目标 checkout 的精确插入点，不修改当前 `../warpx`。

## 当前 checkout anchors

| 层 | 文件与位置 | 现有语义 | 建议 hook |
|---|---|---|---|
| buffer controls | `Source/WarpX.H:341,345,913` | gather/current buffer width 与 mask builder | reduced diagnostic 参数和 runtime enable |
| mask construction | `Source/WarpX.cpp:3471,3496` | 生成 `gather_buffer_masks/current_buffer_masks` | 可选 mask summary，不输出整张 mask |
| stable partition | `Source/Particles/Sorting/Partition.cpp:53,81` | `PartitionParticlesInBuffers` / `stablePartition` | 返回或累计 route counters |
| route inputs | `Source/Particles/PhysicalParticleContainer.cpp:567-595,712-730` | `nfine_gather/nfine_deposit`，`rho_fp/rho_buf`，`current_fp/current_buf` | 每 tile/species/level 计数与权重账本 |
| current sync | `Source/Parallelization/WarpXComm.cpp:1170,1319` | `SyncCurrent` 与 `current_buf` coarse merge | sync 前后 source norm |
| rho sync | `Source/Parallelization/WarpXComm.cpp:1364,1372` | `SyncRho` 与 `rho_buf` merge | rho sync 前后 closure |

## 最小 reduced diagnostic schema

每个 iteration、level 和 species 写一行，避免导出完整 MultiFab：

```text
level, species, nfine_gather, nbuffer_gather,
nfine_deposit, nbuffer_deposit,
weight_fine, weight_buffer, weight_total,
rho_fp_l1, rho_buf_l1, current_fp_l1, current_buf_l1,
coarsened_fine_l1, merged_coarse_l1,
owner_mask_removed_l1, post_sync_l1,
route_partition_pass, source_merge_pass
```

定义边界：

- `nfine_*` 是 partition 后粒子数，不是最终 plotfile 粒子数；
- `weight_*` 只统计实际参与该次 deposition 的粒子；
- `coarsened_fine_l1` 是 fine source 按真实 refinement ratio coarsen 后的账本；
- `merged_coarse_l1` 必须在 `current_buf/rho_buf` 合并、owner-mask 去重之后读取；
- `owner_mask_removed_l1` 不能用“总量差”猜，必须由 merge 前后同一 coarse surface 直接计算。

## 推荐执行顺序

1. 在 `PartitionParticlesInBuffers()` 返回后记录 route counts/weights。
2. 在 `PhysicalParticleContainer::Evolve()` 两组 `DepositCharge/DepositCurrent` 完成后记录 `fp/buf` source norms。
3. 在 `SyncCurrent()` / `SyncRho()` 的 fine-to-coarse merge 前记录 coarsened fine、buffer 和 owner-mask 输入。
4. 在 `SyncCurrentAndRho()` 完成后记录 post-sync source，并写出 `route_partition_pass/source_merge_pass`。
5. 在 CMake 中新增一个 MR-specific analysis consumer；普通 Langmuir analysis 不应承担这条中间账本职责。

## 最小 gates

- `nfine + nbuffer == np_before_partition`，按 species/level 分别成立；
- `weight_fine + weight_buffer == weight_deposited`，允许明确记录的 filtered/scraped 分支；
- coarsened fine、buffer、owner-mask 去重和 merged coarse 的账本可回代；
- post-sync 的 `rho/J` closure 与同一时间层的 field-level `divE-rho/epsilon0` 分开报告；
- 任一 gate 缺少中间字段时，状态保持 `BOUNDARY`，不退化成 checksum-only PASS。

## 当前证据边界

当前 checkout 没有 `TransitionZoneRoutes`、`amr_transition_zone` 或上述中间字段输出。现有 2D MR overlay 的理论场通过，但 level-0/level-1 charge reader residual 为 `0.8828/1.2005`；因此 packet 是可执行的后续修改入口，不是已经完成的 runtime regression。
