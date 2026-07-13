# RZ rho axis pre-scaling boundary

v0.101 已确认既有 `64/128/256` correction-on/off 初始帧的最终 species-rho axis 比值稳定为 `0.85`，off-axis 比值为 `1`。本轮把 WarpX 当前 checkout 的调用链继续展开：`RhoFunctor` 的 species 分支请求 `WarpXParticleContainer::GetChargeDensity`，该路径调用 `DepositCharge(... apply_boundary_and_scale_volume=true, ...)`；`ApplyInverseVolumeScalingToChargeDensity` 在轴上先做负半径 guard-cell wrap，再按 `pi*dr*axis_volume_factor` 归一化。

如果最终输出比值写作

$$
R_{\mathrm{final}} = R_{\mathrm{pre}} \times \frac{1/3}{1/4},
$$

则现有 `R_final=0.85` 反推出 scaling 前 axis 输入比值

$$
R_{\mathrm{pre}} = 0.85 \times \frac{1/3}{1/4} = 1.133333\ldots.
$$

合同在三档 resolution 和 `rho_electrons/rho_ions` 两个字段上全部复现这一数值，且只差显式 `boundary.verboncoeur_axis_correction = false` 的 on/off 输入对照通过。因此，`0.85` 不能由外层 `1/3` 与 `1/4` 因子单独解释；当前更窄的边界是 scaling 前 axis deposit、负半径 wrap 或其输入状态。该结果仍不是 deposition kernel root-cause 证明、charge closure 或正式收敛阶。

- 分类：`RZ_RHO_AXIS_PRESCALE_INPUT_BOUNDARY_OPEN`
- 报告：`runs/stage-c-validation/rz-rho-axis-prescale-boundary-v0.102/contract.{json,md}`
- 脚本：`scripts/audit_rz_rho_axis_prescale_boundary.py`
