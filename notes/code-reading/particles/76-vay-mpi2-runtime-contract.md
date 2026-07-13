# Official Vay deposition 2D/3D 2-rank runtime contract

本轮找到本机 Conda 环境中的 MPICH 5.0.1 launcher，并按 `Examples/Tests/vay_deposition/CMakeLists.txt` 的 2-rank 规模运行官方 2D/3D 输入。2D 使用 `warpx.numprocs = 2 1`，3D 使用 `warpx.numprocs = 2 1 1`；两条路径都由官方 `analysis.py` 消费最终 plotfile。

## 结果

| case | MPI ranks | final plotfile | `error_rel` | tolerance |
|---|---:|---|---:|---:|
| 2D | `2` | `diags/diag1000050` | `4.0410735061469414e-4` | `1e-3` |
| 3D | `2` | `diags/diag1000025` | `6.026615606043056e-4` | `1e-3` |

两条官方 CMake 注册路径均完成 producer、plotfile、`warpx_used_inputs`、2-rank provenance 和 analysis consumer 检查。可重放 contract：

```bash
python scripts/analyze_vay_mpi2_runtime_contract.py \
  --warpx-root ../warpx \
  --case-2d runs/stage-c-validation/vay-runtime/official-2d-mpi2 \
  --case-3d runs/stage-c-validation/vay-runtime/official-3d-mpi2 \
  --output-json runs/stage-c-validation/vay-mpi2/contract.json \
  --output-md runs/stage-c-validation/vay-mpi2/contract.md
```

## 证据边界

分类为 `RUNTIME_OFFICIAL_CMAKE_SCALE_2RANK_ANALYSIS_PASS_2D_3D`。这关闭了已注册 2D/3D shape=3 Cartesian case 的 2-rank runtime consumer 缺口，但不外推到 shape family 的 2-rank 全组合、AMR、边界裁剪、RZ/1D 或正式收敛阶。原始 MPI 日志和 plotfile 保留在 `runs/`，不进入 public release。
