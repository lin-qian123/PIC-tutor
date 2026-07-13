# RZ axis correction non-neutral shape family

v0.106 将非中性 `64x128` RZ correction-on/off 控制扩展到 `particle_shape=1/2/3/4`。每个 shape 的 on/off 输入只在 `boundary.verboncoeur_axis_correction` 上不同；电子/离子 particle ID、位置、角度、权重和动量逐项一致，off-axis rho 比值全部为 `1`。

总 `rho` 的 axis on/off 比值随 shape 单调变化：shape 1/2/3/4 分别为 `0.850000000`、`0.843478261`、`0.836500221`、`0.831672744`。每个 shape 都满足 `delta(rho) = delta(rho_electrons) + delta(rho_ions)`（最大误差不超过 `1.17e-10`），初始 `Er/Ez/divE` 仍为零差异。

源码分层显示 `ChargeDeposition.H` 负责 RZ 半径 `sqrt(xp*xp + yp*yp)` 和 shape weights `sx[ix]*sz[iz]*wq`，不读取 `verboncoeur_axis_correction`；该 toggle 只在后续 `ApplyInverseVolumeScalingToChargeDensity` 中参与轴向体积因子。跨 shape 的单调比值因此排除了单一统一体积比例，当前边界进一步收窄到 RZ shape deposition 与 axis wrap/scaling 的耦合，但仍不识别具体 kernel root cause、不关闭 charge closure 或正式收敛阶。合同见 `runs/stage-c-validation/rz-axis-correction-nonneutral-shape-family-v0.106/contract.{json,md}`，脚本为 `scripts/audit_rz_axis_correction_nonneutral_shape_family.py`。
