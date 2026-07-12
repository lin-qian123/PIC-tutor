# RZ JRhom first-stage decision

审计日期：2026-07-13

## 决策

RZ `test_rz_psatd_JRhom_LL2` 第一阶段按 `finite + energy` 收敛，不加入 spike gate；实际写入 WarpX checkout 和运行官方 regression 另列为待许可的 staging/validation 动作。

### 证据链

- MPI=2 baseline 与 `ll2-no-timeavg-cleaning` reference 的所有目标字段均 finite；
- baseline helper 直接执行返回码 `0`，reference 返回码 `1`，且 reference 失败明确来自 `err_energy=1.0 > TOL_ENERGY=0.9780664916317521`；
- MPI=2 ledger 中 baseline/reference energy ratio 为 `0.9770894022295227/1.0`，energy ceiling 能稳定区分两者；
- spike ratio 虽然也分离，但当前第一阶段选择更窄、更易审查的 energy gate，不把 spike 追加为强断言。

## 交接状态

bundle、provenance、submission packet、PR draft、helper execution contract 和 target-checkout workflow 均已存在。对 `/Volumes/PHILIPS/programs/PIC/warpx` 的 audit/report/preview/stage dry-run 全部成功，目标仍为 `unstaged`，本项目没有写入上游源码。

因此当前可以准确声称：

- first-stage gate decision：`finite + energy`，已收敛；
- helper 正负行为：已在 MPI=2 plotfile 上直接验证；
- upstream staging/official test：尚未执行；
- spike gate、`divE` widening 和更长时间窗口：后续项；
- 当前证据：project-level handoff，不是 upstream CI 结果。

## 可重放命令

```bash
python scripts/build_rz_jrhom_first_stage_patch.py
python scripts/verify_rz_jrhom_first_stage_helper.py \
  --helper notes/code-reading/fieldsolver/analysis_rz_jrhom_first_stage_draft.py \
  --baseline-plotfile runs/fieldsolver-validation/rz-jrhom-reference-scan-mpi2/baseline-jrhom-ll2-timeavg-cleaning/diags/diag1000025 \
  --reference-plotfile runs/fieldsolver-validation/rz-jrhom-reference-scan-mpi2/ll2-no-timeavg-cleaning/diags/diag1000025 \
  --output-dir runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-helper-execution-contract
python scripts/stage_rz_jrhom_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --dry-run
```
