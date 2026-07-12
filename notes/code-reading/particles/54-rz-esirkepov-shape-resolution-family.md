# 54 RZ Esirkepov：shape=2/3/4 correction-off 的分辨率族对照

绑定证据：

- `runs/stage-c-validation/esirkepov_langmuir_rz_shape2_axis-resolution-comparison/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape3_no_verboncoeur_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape3_resolution128_no_verboncoeur_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape4_no_verboncoeur_mpi2/contract.json`
- `runs/stage-c-validation/esirkepov_langmuir_rz_shape4_resolution128_no_verboncoeur_mpi2/contract.json`
- `scripts/summarize_rz_esirkepov_shape_resolution_family.py`

## 1. correction-off 族结果

| shape | coarse `Er` error | refined `Er` error | coarse charge | refined charge | coarse | refined |
|---:|---:|---:|---:|---:|:---:|:---:|
| 2 | `1.323e-1` | `9.318e-3` | `2.202e-12` | `9.644e-12` | BOUNDARY | PASS |
| 3 | `1.734e-1` | `1.113e-2` | `2.103e-12` | `6.086e-12` | BOUNDARY | PASS |
| 4 | `2.134e-1` | `1.365e-2` | `2.063e-12` | `6.724e-12` | BOUNDARY | PASS |

三档 coarse case 都只在 `Er` field gate 失败，charge gate 已通过；三档 `128x256` refined case 的 field/charge 双 gate 全部通过。这里的共同变量是 correction-off、RZ、单层和固定 Langmuir 初始化，不能外推到 AMR、RCYLINDER、RSPHERE 或 implicit 路径。

## 2. 证据边界

这组族对照把 shape=2/3/4 的 coarse `Er` 失败从“shape 越高越不稳定”的直觉说法收窄为：在当前输入和轴修正关闭的条件下，粗网格 field error 随 shape 增大，网格加密后均回到 `0.12` gate 内。

它仍然不能证明：

- correction-on 的 axis charge residual 已经闭合；
- correction-off 应成为 WarpX 全局默认；
- 其他几何、AMR、时间推进或 particle shape 组合都具有同样收敛行为。

因此第 5 章应把它写成“高阶 shape 的 resolution-sensitive boundary”，而不是把 refined sibling 写成上游 active regression 已通过。

## 3. 可重复命令

```bash
python scripts/summarize_rz_esirkepov_shape_resolution_family.py \
  --case 2=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_no_verboncoeur_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape2_resolution128_no_verboncoeur_mpi2/contract.json \
  --case 3=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_no_verboncoeur_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape3_resolution128_no_verboncoeur_mpi2/contract.json \
  --case 4=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_no_verboncoeur_mpi2/contract.json=runs/stage-c-validation/esirkepov_langmuir_rz_shape4_resolution128_no_verboncoeur_mpi2/contract.json \
  --output-dir runs/stage-c-validation/esirkepov_langmuir_rz_shape-resolution-family
```
