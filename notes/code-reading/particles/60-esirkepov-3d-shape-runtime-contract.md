# 3D Esirkepov Langmuir shape=2/3/4 runtime contract

在 v0.51 覆盖矩阵中，3D Esirkepov 只有 shape=1 的运行证据。本轮以官方 3D Langmuir 输入为基础，在 `runs/` 下建立 case-local shape=2/3/4 sibling，只覆盖 `algo.particle_shape`，保持 `64^3`、周期 Yee、2 MPI ranks、40 steps 和其他输入不变；未修改 `../warpx`。

## 结果

| particle shape | 官方 field relative error | 官方 field gate | 独立 `divE-rho` residual | 独立 charge gate | 分类 |
|---:|---:|:---:|---:|:---:|:---:|
| 2 | `3.5970e-2` | PASS (`<5e-2`) | `1.3914e-12` | PASS (`<1e-11`) | PASS |
| 3 | `6.7792e-2` | BOUNDARY (`>5e-2`) | `9.2043e-13` | PASS (`<1e-11`) | field boundary |
| 4 | `8.7344e-2` | BOUNDARY (`>5e-2`) | `7.2393e-13` | PASS (`<1e-11`) | field boundary |

官方 `analysis_3d.py` 与独立 `scripts/analyze_esirkepov_langmuir_contract.py` 均在正确的 `Tools/Parser` Python path 下运行。汇总脚本为 `scripts/summarize_esirkepov_3d_shape_contract.py`，报告为 `runs/stage-c-validation/esirkepov_langmuir_3d_shape-matrix/contract.{json,md}`。

## 解释边界

这三档结果关闭了“3D 高阶 shape 完全没有 runtime evidence”的缺口，但没有关闭所有 geometry/order 组合：

- shape=2 在当前 `64^3` case 同时通过 field/charge；
- shape=3/4 的 charge deposition 仍通过独立 gate，field error 则超过官方 5% 阈值，保留为 resolution-sensitive field boundary；
- 这不是 3D refined-resolution 收敛阶，也不外推到 AMR、RZ、RCYLINDER/RSPHERE、implicit 或边界裁剪路径；
- 不修改全局 `particle_shape` 默认值。
