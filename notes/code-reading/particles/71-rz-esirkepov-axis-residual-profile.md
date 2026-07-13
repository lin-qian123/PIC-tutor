# RZ Esirkepov axis residual radial profile

## 目的

v0.89 对现有 `256x512`、2-rank RZ Esirkepov 高分辨率 sibling 做 reader-side 径向剖面，区分 `r=0`、`r=1` 和 `r>=2` 的同面 `abs(divE-rho/epsilon_0)`。这一步只定位观测残差的空间分布，不把诊断结果外推成 deposition kernel 的根因。

## 运行合同

- 脚本：`scripts/analyze_rz_esirkepov_axis_residual_profile.py`
- 输入：`diags/diag1000080`、`rho`、`divE`，归一化分母为同一 plotfile 的 `max(abs(rho/epsilon_0))`
- family：correction-on/default 与 correction-off，各包含 shape=1/2/3/4，共 8 个 case
- 原始报告：`runs/stage-c-validation/esirkepov_langmuir_rz_axis-residual-profile/contract.{json,md}`
- 结论范围：reader-side same-surface radial profile；不是 kernel root-cause proof、current closure 或 formal convergence study

## 结果

| family | shape | `r=0` 最大值 | `r=1` 最大值 | `r>=2` 最大值 | 最大位置 |
|---|---:|---:|---:|---:|---|
| correction-off | 1 | `1.639115e-11` | `7.152343e-12` | `8.458668e-12` | `r=0` |
| correction-off | 2 | `1.019519e-11` | `4.310026e-12` | `4.036116e-12` | `r=0` |
| correction-off | 3 | `8.399090e-12` | `3.313056e-12` | `2.963069e-12` | `r=0` |
| correction-off | 4 | `6.668825e-12` | `3.928485e-12` | `2.572233e-12` | `r=0` |
| correction-on/default | 1 | `7.553707e-4` | `1.720181e-4` | `5.713737e-5` | `r=0` |
| correction-on/default | 2 | `8.989555e-4` | `2.232327e-4` | `6.934285e-5` | `r=0` |
| correction-on/default | 3 | `9.288744e-4` | `2.336470e-4` | `7.187007e-5` | `r=0` |
| correction-on/default | 4 | `9.728866e-4` | `2.466515e-4` | `7.541276e-5` | `r=0` |

8/8 case 的 profile maximum 都位于 `r=0`，因此 v0.89 将其分类为 `AXIS_DOMINATED_READER_SIDE_RESIDUAL_PROFILE`。该结果支持优先检查 axis volume scaling、staggering/interpolation 和 mode handling 的耦合，但单凭这个 profile 不能在这些候选之间定根因，也不能关闭默认 correction-on 的 `divE-rho` boundary。
