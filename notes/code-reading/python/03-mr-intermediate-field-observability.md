# MR intermediate-field observability boundary

## 审计结果

`scripts/audit_python_mr_observability.py` 对当前 WarpX checkout 的 Python/field-register 入口和 MR field allocation 做了 7 个锚点检查，全部通过：

- `MultiFabRegister` 暴露 `list`、`has` 和 `_get`；
- PICMI `Simulation.fields` 指向底层 field register；
- 现有 Python regression 已验证 `deposit_current("current_fp", ...)`；
- WarpX 初始化确实分配 `current_buf` 和 `rho_buf`。

报告归档于 `runs/stage-c-validation/python-mr-observability/contract.{json,md}`。

## 不能推出的结论

这些源码/API 锚点不能证明 Python callback 在 MR native producer 中已经读到了 `current_buf/rho_buf`，也不能证明 `current_fp`、`current_buf`、coarsened fine source 和 owner-mask 去重结果能被同一时间层完整导出。当前 `particle_data_python` regression 只验证 `current_fp`，而现有 PICMI 示例没有直接 materialize 2D MR `max_level/fine_tag` + intermediate-field ledger 的完整路径。

因此，2D MR Esirkepov runtime 继续保持 `BOUNDARY`。真正关闭它需要 dedicated diagnostic/API wiring 或 WarpX 侧 route-count reduced diagnostic，不能只靠最终 `rho/divE` plotfile 或 generic field-register source audit。
