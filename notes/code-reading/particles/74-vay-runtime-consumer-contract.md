# Vay deposition 2D/3D runtime consumer contract

本轮使用当前 `../warpx/build_full/bin/warpx.2d` 和 `warpx.3d`，在项目 `runs/stage-c-validation/vay-runtime/` 的 case-local 目录中重放官方 Vay 输入。没有修改 WarpX 原仓库。

## 结果

| case | producer | final plotfile | `error_rel` | tolerance |
|---|---|---|---:|---:|
| 2D | `inputs_test_2d_vay_deposition`, `warpx.numprocs='1 1'` | `diags/diag1000050` | `1.5542590389041434e-4` | `1e-3` |
| 3D | `inputs_test_3d_vay_deposition`, `warpx.numprocs='1 1 1'` | `diags/diag1000025` | `2.9007226763170857e-4` | `1e-3` |

两条路径均由官方 `Examples/Tests/vay_deposition/analysis.py` 读取最终 plotfile 的 `rho` 与 `divE`，对

$$
\frac{\max |\nabla_h\cdot\mathbf{E}-\rho/\epsilon_0|}{\max |\rho/\epsilon_0|}
$$

施加 `1e-3` gate。contract 还核对了 `warpx_used_inputs` 中的 geometry、Vay、PSATD、collocated 和 shape=3 参数，以及最终 `Header` 的存在。

## 证据边界

该结果分类为 `RUNTIME_SINGLE_RANK_OFFICIAL_ANALYSIS_PASS_2D_3D`：

- 它把前一轮的 source/regression wiring 推进到真实 producer、plotfile 和 analysis consumer；
- 它是单进程复现，官方 `vay_deposition/CMakeLists.txt` 的 active entries 要求 2 MPI ranks，因此不能写成官方 2-rank regression 已重跑；
- 它覆盖 shape=3 的 2D/3D sibling，不关闭 shape=1/2/4 的完整 runtime family、AMR、边界或正式收敛阶缺口；
- 结果日志和 plotfile 保留在 `runs/`，不进入 public release；可重放 contract 见 `runs/stage-c-validation/vay-runtime/contract.{json,md}`。

## 可重放命令

```bash
python scripts/analyze_vay_runtime_contract.py \
  --case-2d runs/stage-c-validation/vay-runtime/official-2d \
  --case-3d runs/stage-c-validation/vay-runtime/official-3d \
  --output-json runs/stage-c-validation/vay-runtime/contract.json \
  --output-md runs/stage-c-validation/vay-runtime/contract.md
```
