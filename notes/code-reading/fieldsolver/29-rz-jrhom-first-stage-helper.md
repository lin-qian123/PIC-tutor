# RZ JRhom LL2 第一阶段 helper 原型

绑定对象：

- `scripts/analysis_rz_jrhom.py`
- `scripts/scan_rz_jrhom_reference_candidates.py`
- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-mpi2.json`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_psatd_CC1.py`

## 目标

前一轮 sibling 扫描已经把方向收窄到一个很具体的问题：

**如果 `test_rz_psatd_JRhom_LL2` 要补第一阶段独立 analysis，当前最小、最诚实、最接近 `nci_psatd_stability` 口径的 helper 应该长什么样？**

这份笔记记录当前给出的原型答案。

## 当前 helper 形态

新增脚本：

- `scripts/analysis_rz_jrhom.py`

它保持和本地 `scripts/analysis_comoving.py` 同一类接口风格，但换成 RZ 字段口径：

- 始终检查 `Er/Ez/Bt/jr/jz/rho` 的 finite 性；
- 主判据默认启用 `energy gate`；
- `spike gate` 保留为可选增强项，而不是第一阶段必带项。

这里的取舍是刻意的。当前 sibling 扫描已经证明 `ll2-no-timeavg-cleaning` 同时给出最高 `electric_energy` 与最高 `spike_ratio`，因此第一阶段最稳定的主线应该先收成：

- `finite + energy`

而不是继续停留在“也许要 energy，也许要 spike”的模糊状态。

## 阈值如何从 ledger 导出

脚本默认读取：

- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-mpi2.json`

并默认绑定两条 label：

- baseline: `baseline-jrhom-ll2-timeavg-cleaning`
- reference: `ll2-no-timeavg-cleaning`

从当前更接近 upstream regression 形状的 2-rank ledger 可直接读出：

- baseline energy = `2.7378937095024567e+10`
- reference energy = `2.8020912961036427e+10`
- baseline spike = `2.1161359692328046`
- reference spike = `2.2339009047374176`

因此当前默认导出的第一阶段 energy 口径是：

$$
\mathrm{err\_energy} = \frac{E_{\mathrm{plotfile}}}{E_{\mathrm{ref}}}
$$

并把 stable/reference 比值

$$
\frac{E_{\mathrm{baseline}}}{E_{\mathrm{ref}}}
$$

乘一个很小的 safety factor 作为 `tol_energy`。默认值现在是：

- `energy_safety_factor = 1.001`

对应当前 2-rank ledger，会得到大约：

- `tol_energy ≈ 9.779e-1`

这保证：

1. baseline 当前样本能通过；
2. `ll2-no-timeavg-cleaning` 这条 reference sibling 自身会失败；
3. 阈值来源仍然是 ledger 可追溯值，而不是手工抄常数。

同理，如果显式打开 `--enable-spike-gate`，脚本会把

$$
\frac{\mathrm{spike}_{\mathrm{baseline}}}{\mathrm{spike}_{\mathrm{ref}}}
$$

乘 safety factor 作为 `spike_ratio_max`。

## 为什么默认不开 spike gate

不是因为 spike 没价值，而是因为第一阶段先要把主合同收窄。

当前 sibling 扫描已经说明：

- `energy` 和 `spike` 在这条 RZ 线里同向变化；
- 但最核心的读者/评审问题仍是“有没有一条像 `analysis_psatd_CC1.py` 那样的稳定性 gate”。

所以默认行为应先回答这个问题：

- **有，并且当前已经可以写成 `finite + energy`。**

`spike` 更适合保留为第二层增强项，用来帮助后续判断局部尖峰是否值得单独约束，而不是在第一阶段把主线又拉回到多重 gate 的不确定状态。

## 2-rank 复核后的变化

这份 helper 最初是基于本机 `warpx.numprocs=1 1` 的快速样本长出来的，但现在已经补做过更贴近 upstream regression 的 repeated/MPI 复核，记录在：

- `notes/code-reading/fieldsolver/30-rz-jrhom-input-numprocs-audit.md`
- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-mpi2.{md,json}`

关键结论有两条：

1. 输入卡原生 `warpx.numprocs = 1 2` 在真正的 `mpiexec -n 2` 运行下可以稳定落出 baseline / `ll2-no-timeavg-cleaning` / `ll2-timeavg-no-cleaning` / `cl1-no-timeavg-no-cleaning` 的 `diag1000025`；
2. repeated/MPI 下的 energy 排序与本机 `1 1` 样本一致：
   - `ll2-no-timeavg-cleaning`
   - `baseline-jrhom-ll2-timeavg-cleaning`
   - `cl1-no-timeavg-no-cleaning`
   - `ll2-timeavg-no-cleaning`

因此，当前 helper 的默认 ledger 已经切到 `mpi2` 版本，而不再继续依赖较弱的 `1 1` 样本。

## 当前用法

对当前 stable baseline 运行：

```bash
python scripts/analysis_rz_jrhom.py \
  runs/fieldsolver-validation/rz-jrhom-reference-scan/baseline-jrhom-ll2-timeavg-cleaning/diags/diag1000025 \
  --label baseline
```

若要额外打开 spike gate：

```bash
python scripts/analysis_rz_jrhom.py \
  runs/fieldsolver-validation/rz-jrhom-reference-scan/baseline-jrhom-ll2-timeavg-cleaning/diags/diag1000025 \
  --label baseline \
  --enable-spike-gate
```

若直接分析 reference sibling：

```bash
python scripts/analysis_rz_jrhom.py \
  runs/fieldsolver-validation/rz-jrhom-reference-scan/ll2-no-timeavg-cleaning/diags/diag1000025 \
  --label ll2-no-timeavg-cleaning
```

它应在默认 energy gate 下失败，这正是当前原型需要的分辨力。

## 当前边界

这份 helper 仍然只是 `PIC-tutor` 内的原型，不是已经提交到 `../warpx` 的正式 regression helper。当前还保留三条边界：

1. 阈值虽然已切到 2-rank ledger，但仍然来自当前本机 repeated/MPI 样本，还不是 upstream CI 或多机复核后的最终常数；
2. 当前 gate 只基于 `diag1000025`，还没有证明更长时间窗是否会给出更稳的 separation；
3. repeated/MPI 运行当前仍带已知 `MPI_Finalize / OFI poll failed` 尾噪声，虽然 plotfile 已完整落盘，但后续若要正式上提，仍应把这条环境噪声和 helper 逻辑区分开；
4. 这条 helper 还没有落到 WarpX `CMakeLists.txt` wiring，只是先把 helper 形态和阈值来源收口。

## 当前结论

**RZ JRhom LL2 这条线现在已经不再只停留在“reference sibling 已找到”，而是具备了一个经过 2-rank repeated/MPI 排序复核的第一阶段 helper 原型：默认 `finite + energy`，可选 `spike`。**
