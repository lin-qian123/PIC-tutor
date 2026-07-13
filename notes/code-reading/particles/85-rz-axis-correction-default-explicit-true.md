# RZ axis correction default versus explicit true

v0.104 新增一个真实 2-rank、64x128 RZ sibling：原 on case 使用默认值（省略 `boundary.verboncoeur_axis_correction`），新 case 显式写入 `boundary.verboncoeur_axis_correction = true`，并与既有显式 false case 对照。

default-true 与 explicit-true 的 `rho_electrons`、`rho_ions`、`rho`、`Er`、`Ez`、`divE` 数组最大绝对差均为 `0`；电子和离子的 particle ID、位置、角度、权重和动量也逐项一致。相对地，explicit false sibling 的 species axis rho 与 default-true 相差 `60081.62377500016`，而总 `rho`、`Er`、`Ez`、`divE` 仍为零差异或数值相同。

因此，默认值解析、显式 true 分支和输入 parser 选择均被排除为 axis species-rho 差异的来源。当前边界进一步收窄到 axis correction 参与的 species-rho diagnostic/deposition/wrap/scaling consumer；该结果仍不等于已识别具体 kernel root cause，也不关闭 charge closure。

- 分类：`RZ_AXIS_CORRECTION_DEFAULT_EXPLICIT_TRUE_EQUIVALENT_FALSE_BOUNDARY_OPEN`
- 报告：`runs/stage-c-validation/rz-axis-correction-default-explicit-true-v0.104/contract.{json,md}`
- 脚本：`scripts/audit_rz_axis_correction_default_explicit_true.py`
