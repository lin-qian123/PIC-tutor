# Vay deposition 2D/3D 2-rank shape-family contract

本轮将官方 shape=3 2-rank case 与六个 case-local shape=1/2/4 sibling 合并复核，形成 2D/3D Cartesian 的 `particle_shape=1/2/3/4` 两进程 runtime family。所有输入保持官方 Vay、PSATD、collocated 和最终 `divE-rho/epsilon_0` analysis；shape=1/2/4 只改变 shape 和对应 `warpx.numprocs`，不修改 WarpX 源码。

## 结果

| case | shape=1 | shape=2 | shape=3 | shape=4 |
|---|---:|---:|---:|---:|
| 2D `error_rel` | `4.671739425626634e-4` | `3.81912847363086e-4` | `4.0410735061469414e-4` | `4.2829451447370665e-4` |
| 3D `error_rel` | `5.97920560804836e-4` | `5.744068540430952e-4` | `6.026615606043056e-4` | `6.355935958035336e-4` |
| tolerance | `1e-3` | `1e-3` | `1e-3` | `1e-3` |

八个 case 均由 2 个 MPI processes 运行并通过官方 `analysis.py`。可重放 contract：

```bash
python scripts/analyze_vay_mpi2_shape_family_contract.py \
  --warpx-root ../warpx \
  --case-root-2d runs/stage-c-validation/vay-runtime/shape-family-2d-mpi2 \
  --case-root-3d runs/stage-c-validation/vay-runtime/shape-family-3d-mpi2 \
  --official-case-2d runs/stage-c-validation/vay-runtime/official-2d-mpi2 \
  --official-case-3d runs/stage-c-validation/vay-runtime/official-3d-mpi2 \
  --output-json runs/stage-c-validation/vay-mpi2-shape-family/contract.json \
  --output-md runs/stage-c-validation/vay-mpi2-shape-family/contract.md
```

## 证据边界

分类为 `RUNTIME_2RANK_VAY_SHAPE_FAMILY_PASS_2D_3D_CASE_LOCAL`。它关闭的是 Cartesian shape=1..4 的两进程 runtime family 缺口；shape=1/2/4 不是上游 CMake 注册的新测试，不能外推到 AMR、边界裁剪、RZ/1D、非 Cartesian geometry 或正式 convergence order。原始日志和 plotfile 保留在 `runs/`，不进入 public release。
