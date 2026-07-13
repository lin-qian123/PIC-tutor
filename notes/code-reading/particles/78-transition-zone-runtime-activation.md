# Transition-zone runtime activation

## 结论

当前 `runs/stage-c-validation/subcycling_2d_mr_mpi2/` 是一条真实的 2-rank、两层 AMR subcycling 运行。它的 `warpx_used_inputs` 同时包含 `amr.max_level = 1`、`warpx.do_subcycling = 1`、`particles.deposit_on_main_grid = plasma_e plasma_p` 以及两项 buffer 参数；`run.log` 中出现了 `PhysicalParticleContainer::PartitionParticlesInBuffers` 和 `OwnerMask()` 的 runtime profiling marker。

因此，本轮可以把结论从“只有源码和整体 workflow”推进为：**transition-zone 的分区/同步代码路径在现有 AMR 运行中被实际调用过**。独立合同为 `RUNTIME_TRANSITION_ZONE_BRANCH_ACTIVATION_OBSERVED_ROUTE_LEDGER_UNPROVEN`。

## 证据边界

这仍然不是 route-count regression。当前日志没有逐粒子 route id、fine/coarse gather/deposit 计数、`current_buf/rho_buf` pre-sync 数值、coarsened-fine 中间账本或 post-sync closure 字段。因此不能据此声称四条 route 已分别命中，也不能声称 coarse-buffer source 与 owner-mask 回灌已经通过同一账本闭合。

合同由 `scripts/audit_transition_zone_runtime_activation.py` 生成，报告位于 `runs/stage-c-validation/transition-zone-runtime-activation-v0.97/contract.{json,md}`。它读取现有 producer log、`warpx_used_inputs`、subcycling workflow contract 和只读 source contract，不修改相邻 `../warpx`。
