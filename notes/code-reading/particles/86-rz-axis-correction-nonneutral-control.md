# RZ axis correction non-neutral control

v0.105 新增一个真实 2-rank、`64x128` RZ 非中性 sibling：保持几何、粒子形状、沉积算法和初始电子分布不变，只把 `ions.density` 改为 `0.5*n0`，并运行 correction-on/default 与显式 `false` 两个 case。两份 `warpx_used_inputs` 除 axis correction toggle 外一致，电子/离子 particle ID、位置、角度、权重和动量逐项一致。

species rho 的 axis on/off 比值仍为 `0.85`，off-axis 比值仍为 `1`；非中性 case 中总 `rho` 的 axis 比值也为 `0.85`，最大 axis 差为 `30040.81188750008`。`delta(rho)` 与 `delta(rho_electrons)+delta(rho_ions)` 的最大误差为 `0`，说明中性 case 中总 rho 未变化是电子/离子贡献抵消的结果，而不是 species-rho 差异消失。初始帧的 `Er/Ez/divE` 在 on/off 间仍为零差异。

该合同把当前解释推进为：axis correction 参与的 species-rho deposition/diagnostic consumer 差异是真实的，并且在非中性电荷中会进入 total-rho；中性设置只能掩盖其 total-rho 可见性。它仍不识别具体 kernel root cause，不关闭 charge closure，也不证明正式收敛阶。合同见 `runs/stage-c-validation/rz-axis-correction-nonneutral-control-v0.105/contract.{json,md}`，脚本为 `scripts/audit_rz_axis_correction_nonneutral_control.py`。
