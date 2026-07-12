# 55 RZ Esirkepov：高阶 shape 的 correction-on/off 完整矩阵

绑定证据：

- `runs/stage-c-validation/esirkepov_langmuir_rz_shape2_axis-resolution-comparison/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape3_resolution128_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape4_resolution128_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape-resolution-family/contract.json`
- `scripts/summarize_rz_esirkepov_axis_correction_family.py`

## 1. refined `128x256` correction-on/off 结果

| shape | correction-on `Er` | correction-on charge | correction-off `Er` | correction-off charge |
|---:|---:|---:|---:|---:|
| 2 | `9.321e-3` | `2.177e-3` | `9.318e-3` | `9.644e-12` |
| 3 | `9.342e-3` | `2.353e-3` | `1.113e-2` | `6.086e-12` |
| 4 | `1.079e-2` | `2.552e-3` | `1.365e-2` | `6.724e-12` |

三档 correction-on 的 `Er/Ez` field gate 均通过，但 charge residual 仍由 axis cell 主导、保持在 `O(1e-3)`；三档 correction-off 的 field/charge 双 gate 均通过。该结果把当前证据分成两个独立问题：粗网格 correction-off 的 field boundary 已由分辨率解释，高分辨率 correction-on 的 axis charge boundary 仍未解释或闭合。

## 2. 不应过度外推

这里的 correction-off refined pass 不是全局默认参数建议，因为它只覆盖 RZ 单层 Langmuir、固定时间步和 shape=2/3/4。correction-on charge residual 也不能直接等同于 kernel 错误：现有诊断链仍包含 axis volume correction、`divE`/`rho` 的不同构造路径和同面采样语义。

更准确的正文结论是：

- field accuracy 对高阶 shape 的 coarse-resolution 敏感性已经被 refined siblings 复现；
- correction-off 在当前 refined sibling 上恢复了 charge gate；
- correction-on 仍保留 axis-dominated charge boundary，需要继续沿诊断语义、轴体积离散和更直接的 charge observable 推进。

## 3. 可重复命令

```bash
python scripts/summarize_rz_esirkepov_axis_correction_family.py \
  --case 2=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_no_verboncoeur_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_no_verboncoeur_mpi2/contract.json \
  --case 3=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_no_verboncoeur_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_resolution128_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_resolution128_no_verboncoeur_mpi2/contract.json \
  --case 4=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_no_verboncoeur_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_resolution128_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_resolution128_no_verboncoeur_mpi2/contract.json \
  --output-dir runs/stage-c-validation/esirkepov_langmuir_rz_axis-correction-family
```
