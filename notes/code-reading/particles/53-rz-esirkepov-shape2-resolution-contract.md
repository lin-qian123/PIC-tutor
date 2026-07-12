# 53 RZ Esirkepov shape=2：高分辨率消除 correction-off 的 field 边界

绑定证据：

- `runs/stage-c-validation/esirkepov_langmuir_rz_shape2_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape2_no_verboncoeur_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_no_verboncoeur_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape2_axis-resolution-comparison/contract.json`
- `scripts/summarize_rz_esirkepov_axis_resolution_contract.py --particle-shape 2`

## 1. 四格结果

| 网格 | 修正 | `Er/Ez` field error | charge residual | 结论 |
|---|---|---:|---:|---|
| `64x128` | on | `5.703e-2/1.280e-2` | `4.306e-3` | field PASS，charge BOUNDARY |
| `64x128` | off | `1.323e-1/1.445e-2` | `2.202e-12` | field BOUNDARY，charge PASS |
| `128x256` | on | `9.321e-3/5.154e-3` | `2.177e-3` | field PASS，charge BOUNDARY |
| `128x256` | off | `9.318e-3/7.775e-3` | `9.644e-12` | field/charge 全部 PASS |

field gate 为 `max(Er_error, Ez_error) < 0.12`，charge gate 为同面 `divE-rho/epsilon0 <= 1e-11`。shape=2 的 correction-off `Er` 误差从 `0.1323` 降至 `0.0093`，因此低分辨率 field 失败是可被加密消除的离散边界；correction-on 的 axis charge residual 虽下降，仍没有接近强 charge gate。

## 2. 证据边界

这组结果不能推出关闭 `boundary.verboncoeur_axis_correction` 是全局修复：

- 它只覆盖 RZ、shape=2、单层、周期轴向和固定 Langmuir 初始化；
- shape=1 的两档 correction-off 也通过，但 shape=3/4 的既有 coarse correction-off controls 仍有 `Er=0.173/0.213` 的 field 边界；
- 因而当前最稳妥的结论是：RZ axis treatment 的 field/charge 表现同时依赖 shape 与分辨率，不能以单个 coarse failure 或 refined pass 外推所有 geometry/order。

## 3. 可重复命令

```bash
python scripts/summarize_rz_esirkepov_axis_resolution_contract.py \
  --particle-shape 2 \
  --baseline-on runs/stage-c-validation/esirkepov_langmuir_rz_shape2_mpi2/contract.json \
  --baseline-off runs/stage-c-validation/esirkepov_langmuir_rz_shape2_no_verboncoeur_mpi2/contract.json \
  --refined-on runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_mpi2/contract.json \
  --refined-off runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_no_verboncoeur_mpi2/contract.json \
  --output-dir runs/stage-c-validation/esirkepov_langmuir_rz_shape2_axis-resolution-comparison
```
