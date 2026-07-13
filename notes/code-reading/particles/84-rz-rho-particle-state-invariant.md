# RZ rho particle-state invariant

v0.103 对既有 `64/128/256` correction-on/off 初始诊断帧直接比较两组粒子状态。对 `electrons` 和 `ions`，先按 `particle_id` 排序，再逐项比较 `particle_position_x/y`、`particle_theta`、`particle_weight` 和三分量动量；三档 resolution 的粒子数分别为 `58880/235520/944128`（on/off 相同），所有字段最大绝对差均为 `0`。

在相同粒子状态下，species `rho` 仍表现为：

- axis on/off 比值为 `0.85`；
- off-axis 比值最大偏差为 `0`；
- 两个 species、三档 resolution 全部复现。

因此，`0.85` 不能由粒子初始化、粒子位置、权重或动量差异解释。结合 v0.102 的 `GetChargeDensity -> DepositCharge -> ApplyInverseVolumeScalingToChargeDensity` 源码链，当前更窄的边界是 species-rho diagnostic consumer、charge deposition 或负半径 axis wrap/scaling 路径。该合同仍不识别具体 kernel root cause，也不关闭 charge closure。

- 分类：`RZ_RHO_AXIS_DIAGNOSTIC_CONSUMER_BOUNDARY_OPEN`
- 报告：`runs/stage-c-validation/rz-rho-particle-state-invariant-v0.103/contract.{json,md}`
- 脚本：`scripts/audit_rz_rho_particle_state_invariant.py`
