# RZ Esirkepov rho/species decomposition time profile

## 目的

v0.91 把 v0.88 的末帧 `rho` species decomposition 扩展到 v0.90 同一批 8 个 `256x512`、2-rank RZ sibling 的全部数值 plotfile，验证 `rho` 组装链是否在时间上独立于 `divE-rho` axis boundary。

## 合同

- 脚本：`scripts/analyze_rz_esirkepov_rho_species_time_profile.py`
- 读取：`rho`、`rho_electrons`、`rho_ions`
- family：correction-on/default 与 correction-off，各含 shape=1/2/3/4
- 帧：每个 case 的 `diag1000000`、`diag1000040`、`diag1000080`，共 24 帧
- evolved gate：`max(abs(rho-(rho_electrons+rho_ions))) / max(abs(rho)) <= 1e-12`
- 原始报告：`runs/stage-c-validation/esirkepov_langmuir_rz_rho-species-time-profile/contract.{json,md}`

## 结果

| case | 初始化帧相对差 | evolved frames 最大相对差 |
|---|---:|---:|
| correction-on shape=1 | `1.369863e-2` | `1.853601e-14` |
| correction-on shape=2 | `1.927711e-2` | `1.635856e-14` |
| correction-on shape=3 | `1.960784e-2` | `1.590772e-14` |
| correction-on shape=4 | `2.279202e-2` | `1.435273e-14` |
| correction-off shape=1 | `1.369863e-2` | `1.599320e-14` |
| correction-off shape=2 | `1.927711e-2` | `1.389006e-14` |
| correction-off shape=3 | `1.960784e-2` | `1.340970e-14` |
| correction-off shape=4 | `2.279202e-2` | `1.346772e-14` |

24 帧均成功读取；排除 `diag1000000` 初始化基线后，16 个 evolved frames 全部通过 `1e-12` gate，分类为 `EVOLVED_TIME_RHO_SPECIES_DECOMPOSITION_PASS_AXIS_CHARGE_SEPARATE`。

## 结论边界

初始化帧的约 `1e-2` 差异属于 pre-evolution baseline，不能和推进后的 species decomposition 混写。evolved-time 结果支持 `rho` 与物种分解在 reader-side 达到机器精度，但不证明 `divE-rho`、current closure、axis volume scaling 或 formal convergence；因此它强化了“rho-side assembly 已分离、axis charge boundary 仍独立”的表述，而不是关闭 RZ physics gap。
