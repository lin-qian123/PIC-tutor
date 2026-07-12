# RZ JRhom LL2 输入卡原生 `numprocs` 审计

绑定对象：

- `scripts/scan_rz_jrhom_reference_candidates.py`
- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-input-numprocs.json`
- `../warpx/Examples/Tests/nci_psatd_stability/inputs_test_rz_psatd_JRhom_LL2`
- `../warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`

## 目标

`29-rz-jrhom-first-stage-helper.md` 已经把当前本机 `warpx.numprocs=1 1` 样本收成了第一阶段 `finite + energy` helper 原型。

但如果这条 helper 真要继续往 upstream regression 方向推进，下一步不能只看 `1 1` 本地样本，还必须先回答一个更基础的问题：

**当我们把输入卡原本写着的 `warpx.numprocs = 1 2` 保留下来时，当前本机到底发生了什么？**

这份笔记记录这次审计结论。

## 当前事实

WarpX 当前测试入口里，`test_rz_psatd_JRhom_LL2` 在 `CMakeLists.txt` 中注册为：

- dims: `RZ`
- nprocs: `2`
- input: `inputs_test_rz_psatd_JRhom_LL2`
- analysis: `OFF`
- checksum: `analysis_default_regression.py --path diags/diag1000025`

而对应输入卡里显式写着：

```text
warpx.numprocs = 1 2
```

也就是说，这条测试本来就不是单进程 `1 1` 设计。

## 本轮新增能力

为了审计这件事，当前仓库先扩展了：

- `scripts/scan_rz_jrhom_reference_candidates.py`

新增两类接口：

1. `--numprocs-override`
   - 默认仍是 `1 1`，保持旧扫描可复现；
   - 传 `none` 时，不再覆盖输入卡里的 `warpx.numprocs`。

2. `--command-prefix`
   - 允许后续在环境具备 launcher 时直接写：
   - `--command-prefix mpiexec -n 2`

这样同一份扫描脚本就能覆盖：

- 本机单进程快速样本；
- 输入卡原生 `1 2` 审计；
- 未来真正的 2-rank 重跑。

## 当前审计命令

这轮实际执行的是：

```bash
python scripts/scan_rz_jrhom_reference_candidates.py \
  --numprocs-override none \
  --output-root runs/fieldsolver-validation/rz-jrhom-reference-scan-input-numprocs \
  --ledger-stem runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-input-numprocs \
  --force-rerun
```

生成：

- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-input-numprocs.md`
- `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-input-numprocs.json`

## 审计结果

这轮结果最重要的结论不是“排序变了”，而是：

- 当前五条候选都没有跑到 `diag1000025`；
- 它们在 producer 启动阶段就统一失败；
- 失败原因不是物理参数组合本身，而是进程数合同不满足。

baseline 的核心报错是：

```text
warpx.numprocs, if specified, its product must be equal to the
number of processes
```

stdout 同时表明当前实际只启动了：

```text
MPI initialized with 1 MPI processes
```

因此，当前 `1 2` 审计得到的不是 “energy ordering 消失”，而是更严格也更有用的一条边界：

- **如果不通过 MPI launcher 真的起到 2 个 processes，输入卡原生 `warpx.numprocs = 1 2` 连 producer 都不会通过。**

## 这说明什么

这条结论会直接改变后续判断顺序。

当前真正缺的首先不是再去讨论：

- `tol_energy` 要不要微调；
- `spike` 要不要升级成默认 gate。

而是先解决更前面的执行条件：

- 要想验证更贴近 upstream regression 的 `1 2` 形状，必须先用真正的 2-process 启动方式。

如果只用当前这种 plain single-process 调用方式，那么：

1. `warpx.numprocs = 1 2` 一定会触发 AMReX 断言；
2. 这类失败不能被解释成 physical ordering drift；
3. 当前 `1 1` helper 原型仍然是唯一已被本机 plotfile 证实的 gate 形态。

## 当前阻塞点

随后这条 blocker 已经在本机被部分打通：当前机器虽然默认 `PATH` 下没有 `mpiexec/mpirun`，但另一个 Conda 环境里存在：

- `/Users/yuxiangzhang/anaconda3/envs/warpx-cpu-mpich-dev/bin/mpiexec`
- `/Users/yuxiangzhang/anaconda3/envs/warpx-cpu-mpich-dev/bin/mpirun`

并且当前 WarpX binary 也明确链接到 `libmpi.12.dylib`。因此，同一份扫描脚本后来已经能用：

```bash
python scripts/scan_rz_jrhom_reference_candidates.py \
  --numprocs-override none \
  --command-prefix-str '/Users/yuxiangzhang/anaconda3/envs/warpx-cpu-mpich-dev/bin/mpiexec -n 2' \
  --output-root runs/fieldsolver-validation/rz-jrhom-reference-scan-mpi2 \
  --ledger-stem runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-mpi2
```

真正完成 2-rank 复核。

这轮 repeated/MPI 结果最关键的结论是：

1. baseline、`ll2-no-timeavg-cleaning`、`ll2-timeavg-no-cleaning`、`cl1-no-timeavg-no-cleaning` 都能在 `mpiexec -n 2` 下落出 `diag1000025`；
2. `cl1-timeavg-cleaning` 仍然是源码级非法组合；
3. repeated/MPI 下的 energy 排序与本机 `1 1` 快速样本一致，`ll2-no-timeavg-cleaning` 仍是最强 unstable reference。

也就是说，这份审计的最终结论已经从“缺 launcher，因此只能止步于 process-count mismatch”推进成：

- **launcher 路径已找到并完成 2-rank 复核；process-count mismatch 只是在 plain single-process 调用方式下成立的边界，而不是这台机器无法进行 MPI 复核的最终结论。**

## 当前结论

**输入卡原生 `warpx.numprocs = 1 2` 现在已经完成了真实的 2-process 复核：plain invocation 下的失败说明的是 launcher 合同不满足，而在 `mpiexec -n 2` 下，当前 `finite + energy` ordering 依然成立。**
