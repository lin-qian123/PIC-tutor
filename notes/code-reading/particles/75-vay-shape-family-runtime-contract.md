# Vay deposition 2D/3D shape-family runtime contract

本轮在不修改 `../warpx` 的前提下，复制官方 `Examples/Tests/vay_deposition/` 的 2D/3D 输入，只替换 `algo.particle_shape`，分别运行 shape=1、2、3、4。每个 case 都由当前 `build_full` binary 生成官方最终 plotfile，再由上游 `analysis.py` 消费 `divE-rho/epsilon_0`。

## 结果

| case | shape=1 | shape=2 | shape=3 | shape=4 |
|---|---:|---:|---:|---:|
| 2D `error_rel` | `1.4634713308363294e-4` | `1.4688955667848161e-4` | `1.5542590389041434e-4` | `1.647286594131451e-4` |
| 3D `error_rel` | `2.8823750115376914e-4` | `2.7647274952842705e-4` | `2.9007226763170857e-4` | `3.0592307138679957e-4` |
| tolerance | `1e-3` | `1e-3` | `1e-3` | `1e-3` |

八个 case（其中六个是本轮新增 sibling，另两个复用上一轮 shape=3 producer）均生成最终 plotfile，均为单进程，并通过官方 `analysis.py` 的 `1e-3` gate。可重放 contract 为：

```bash
python scripts/analyze_vay_shape_family_runtime.py \
  --case-root-2d runs/stage-c-validation/vay-runtime/shape-family-2d \
  --case-root-3d runs/stage-c-validation/vay-runtime/shape-family-3d \
  --output-json runs/stage-c-validation/vay-shape-family/contract.json \
  --output-md runs/stage-c-validation/vay-shape-family/contract.md
```

## 证据边界

该 contract 分类为 `RUNTIME_SINGLE_RANK_VAY_SHAPE_FAMILY_PASS_2D_3D`。它关闭的是支持的 Cartesian shape=1..4 单进程 runtime family 缺口；不能替代官方 CMake 要求的 2-rank 回归，也不外推到 RZ/1D source guard、AMR/边界裁剪或正式收敛阶。原始日志和 plotfile 保留在 `runs/`，不进入 public release。
