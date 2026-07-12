# Comoving first-stage target-checkout preflight

审计日期：2026-07-12

## 当前事实

对相邻目标 WarpX checkout `/Volumes/PHILIPS/programs/PIC/warpx` 做了只读 `audit`、`report`、`preview` 和 `stage --dry-run`：

- `Examples/Tests/nci_psatd_stability/analysis_comoving.py` 当前不存在；
- `nci_psatd_stability/CMakeLists.txt` 中 `test_2d_comoving_psatd_hybrid` 的 analysis 仍为 `OFF`；
- 目标树状态为 `unstaged`，不是已经接入或部分接入；
- unified diff 只计划两项改动：新增第一阶段 helper，并把对应 CMake analysis 行改成 `analysis_comoving.py diags/diag1000400`；
- `stage --dry-run` 与 preview 的计划完全一致；本轮没有向 sibling WarpX 写入文件。

## 证据边界

本地 `finite + spike` 正/负 contract 已证明 helper 具有最小判别力，但当前没有可靠的 comoving unstable-energy oracle，因此第一阶段草案不带 energy gate。目标 checkout 仍需维护者明确允许后，才能执行真实 staging；在此之前，本项目只能声称 handoff 和 staging workflow 已准备好，不能声称 upstream regression 已接入。

## 可重放命令

```bash
python scripts/audit_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --json
python scripts/report_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx
python scripts/preview_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx
python scripts/stage_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --dry-run
```
