# RZ JRhom first-stage helper execution contract

审计日期：2026-07-13

## 本轮验证

新增 `scripts/verify_rz_jrhom_first_stage_helper.py`，直接执行生成的 `analysis_rz_jrhom_first_stage_draft.py`：

- MPI=2 baseline plotfile 返回码 `0`，finite check 和 energy ceiling 均通过；
- `ll2-no-timeavg-cleaning` reference 返回码 `1`，字段 finite，但 `err_energy=1.0` 超过 `TOL_ENERGY=0.9780664916317521`，按预期被拒绝。

这一步验证的是“交接包中的 helper 本身可运行且正负行为与 ledger 一致”，不是新的物理运行，也不是 upstream CI 结果。reference 的 stdout/stderr 会保存在机器可读 contract 中，便于接续者区分预期 gate rejection 和 Python/runtime failure。

## 可重放命令

```bash
python scripts/verify_rz_jrhom_first_stage_helper.py \
  --helper notes/code-reading/fieldsolver/analysis_rz_jrhom_first_stage_draft.py \
  --baseline-plotfile runs/fieldsolver-validation/rz-jrhom-reference-scan-mpi2/baseline-jrhom-ll2-timeavg-cleaning/diags/diag1000025 \
  --reference-plotfile runs/fieldsolver-validation/rz-jrhom-reference-scan-mpi2/ll2-no-timeavg-cleaning/diags/diag1000025 \
  --output-dir runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-helper-execution-contract
```
