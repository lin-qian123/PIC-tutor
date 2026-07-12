# Comoving real MPI=2 stable/sign pair contract

审计日期：2026-07-13

## 运行结果

在真实 MPICH 2-rank launcher 下，固定 `inputs_test_2d_comoving_psatd_hybrid`，分别运行默认 comoving selector 与反号 `v_comoving=+beta` sibling。两个 `diag1000400` plotfile 均完整落盘，所有字段有限；MPI 进程只在 AMReX finalize 后出现已知尾部挂起/OFI finalize 噪声，未影响 plotfile 读取。

- MPI=2 stable：electric energy `8.166055351004438e14`，spike ratio `1.111713589404735`；相对既有 1-rank stable 的 energy/spike 差分别约 `1.72e-3/1.21e-3`，均低于 1%。
- MPI=2 positive-sign：electric energy `6.536505608465998e14`，spike ratio `1.1824991395788464`。
- positive/stable spike ratio 为约 `1.0637`，满足 sign-sensitivity screen；但 positive sibling 的 energy 更低，因此不能作为 unstable-energy oracle。

该 pair contract 把 comoving 证据从单进程 scan 推进到真实 MPI 形状，同时保留“不启用 energy gate、不声称 upstream CI 已接入”的边界。

## 可重放命令

分析已落盘的 pair：

```bash
python scripts/analyze_comoving_mpi2_pair.py \
  --stable-plotfile runs/fieldsolver-validation/comoving-mpi2/stable-default-selector/diags/diag1000400 \
  --positive-plotfile runs/fieldsolver-validation/comoving-mpi2/positive-default-beta/diags/diag1000400 \
  --one-rank-ledger runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan.json \
  --output-dir runs/fieldsolver-validation/comoving-reference-ledgers/comoving-mpi2-pair-contract
```

原始 MPI 运行目录留在 `runs/fieldsolver-validation/comoving-mpi2/`，不进入 public release。
