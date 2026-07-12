# RZ JRhom first-stage handoff decision

审计日期：2026-07-13

## 当前结论

RZ `test_rz_psatd_JRhom_LL2` 的第一阶段 patch 已达到 `handoff-ready`，但本轮不直接写入相邻 `../warpx` checkout。

只读审计结果：

- target checkout 状态为 `unstaged`；`analysis_rz_jrhom.py` 尚不存在，CMake 中该测试的 analysis 仍为 `OFF`。
- `preview` 与 `stage --dry-run` 均成功，计划写入面只有两处：新增 `analysis_rz_jrhom.py`，以及将 `test_rz_psatd_JRhom_LL2` 的 analysis 接到 `diags/diag1000025`。
- MPI=2 repeated ledger 中，baseline 与 `ll2-no-timeavg-cleaning` 均为有限场；baseline 通过 energy ceiling，reference 被拒绝，contract 为 `passed=true`。
- 第一阶段只启用 `finite + energy`；spike ratio 继续报告但不进入 gate，避免把当前证据外推成更强的 upstream 断言。

## 可执行交接命令

```bash
python scripts/audit_rz_jrhom_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --json
python scripts/report_rz_jrhom_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx
python scripts/preview_rz_jrhom_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx
python scripts/stage_rz_jrhom_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --dry-run
```

只有在 WarpX 维护者明确允许后，才执行不带 `--dry-run` 的 staging，并在目标 checkout 内重新运行官方 test、analysis 和 checksum。`PIC-tutor` 当前不声称 upstream 已接入，也不把本地 handoff 资产当作 upstream CI 结果。

## 对 comoving 线的处理

comoving patch 同样保持 `unstaged`，且当前只具备 `finite + spike` 合同；energy gate 仍未取得可靠 unstable-energy oracle。因此本轮不将它提升为正式上提项，下一步应优先寻找更接近 upstream regression 的 sibling 或 repeated/MPI contrast。
