# Esirkepov MR source-sync boundary

## 当前 source contract

`scripts/audit_esirkepov_mr_source_contract.py` 对当前 `../warpx` checkout 做了 15 个源码锚点检查，全部覆盖以下链路：

1. `MultiParticleContainer::Evolve()` 清零并传递 `current_fp_string`，同时存在 `current_buf`；
2. `WarpXParticleContainer::DepositCurrent()` 允许 `depos_lev=lev-1`，并用 coarse `tilebox`、`dinv`、`xyzmin`、`domain_double` 和 `do_cropping` 解释 buffer 粒子；
3. `WarpX` 为 `current_buf` 和 `current_buffer_masks` 分配多层数据结构；
4. `WarpXEvolve.cpp` 通过 `SyncCurrent()` 和 `AddCurrentFromFineLevelandSumBoundary()` 把 fine/coarse source 合并。

报告归档于 `runs/stage-c-validation/esirkepov_mr_source-contract/contract.{json,md}`。

## 与 MR runtime boundary 的关系

2D MR Esirkepov overlay 的理论场 gate 通过，但逐层 `divE-rho/epsilon0` reader contract 为 L0 `0.8828041`、L1 `1.2005240`。source audit 证明“路由和合并骨架存在”，不能证明实际粒子 route count、`current_buf` 与 fine `current_fp` 的贡献去重、或最终同步后离散连续性已经闭合。

当前 plotfile 只暴露最终字段，不直接暴露 `current_fp/current_buf/rho_fp/rho_buf` 中间场。因此下一条强验证需要 dedicated diagnostic surface，至少输出：

- fine-interior 与 transition-zone 粒子 route counts/weights；
- `current_fp`、`current_buf` 和 coarsened fine contribution 的分量账本；
- owner-mask 去重前后的 coarse source；
- 同一时间层的 `rho_fp/rho_buf` 对照。

在这些中间量可观测之前，MR overlay 继续保持 `BOUNDARY`，不升级为 Esirkepov AMR physics pass。
