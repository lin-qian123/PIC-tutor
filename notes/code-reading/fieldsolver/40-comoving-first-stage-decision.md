# Comoving first-stage decision

审计日期：2026-07-13

## 决策

comoving PSATD first-stage patch 的本地证据边界已经足够明确：第一阶段按 `finite + spike` 收敛，不加入 energy gate；实际写入 WarpX checkout 则另列为需要维护者许可的 staging 动作。

### 支持该决策的证据

- 1-rank stable baseline 通过 finite/spike，zero-comoving sibling 被当前 stable-derived spike ceiling 拒绝；
- velocity scan 中显式 `-beta` 与默认 selector 的 energy/spike 相对差约 `1e-14`，反号 sibling 的 spike ratio 为 stable 的 `1.0622` 倍；
- 真实 MPI=2 中默认 selector、显式 `-beta` 和反号 sibling 的 plotfile 均完整且 fields finite；显式/default 的 energy/spike 相对差约 `1.20e-14/4.03e-14`，反号 sibling 的 spike ratio 为 stable 的 `1.0637` 倍；
- zero-comoving 和反号 sibling 都没有形成高于 stable 的 electric-energy ordering，因此没有可审查的 `energy_ref_unstable` 常量。

## 交接状态

当前 handoff bundle、provenance、submission packet、PR draft 和 target-checkout workflow 已由 MPI=2 contract 自动生成。对相邻 `/Volumes/PHILIPS/programs/PIC/warpx` 的只读 audit、report、preview、stage dry-run 均通过，目标仍为 `unstaged`，本项目没有写入上游源码。

因此当前可以准确声称：

- first-stage gate decision：`finite + spike`，已收敛；
- upstream staging：尚未执行；
- energy-gate follow-up：未完成，需新的更强 unstable-energy oracle；
- 现有结果：project-level local calibration/handoff，不是 upstream CI 结果。

## 可重放命令

```bash
python scripts/build_comoving_first_stage_patch.py
python scripts/audit_comoving_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --json
python scripts/report_comoving_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx
python scripts/preview_comoving_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx
python scripts/stage_comoving_first_stage_patch.py \
  --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --dry-run
```
