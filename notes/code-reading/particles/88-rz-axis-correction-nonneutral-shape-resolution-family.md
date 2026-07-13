# RZ non-neutral shape family across resolution

## 问题

v0.106 在 `64x128`、`ions.density = 0.5*n0` 的 RZ sibling 上观察到 shape=1/2/3/4 的 total-rho axis on/off 比值严格下降。本轮将同一控制扩展到 `128x256`，检查该结论是否可以直接跨分辨率复用。

## Runtime 证据

两套分辨率都使用真实 2-rank WarpX 运行，on/off sibling 只差 `boundary.verboncoeur_axis_correction`。初始化帧的电子/离子 particle ID、位置、角度、权重和动量逐项一致，off-axis rho 比值为 `1`，初始 `Er/Ez/divE` 不变，且 `delta(rho)` 与两 species delta 逐数组相符。

species rho 的 axis on/off 比值在两套网格上完全相同：

| shape | `64x128` | `128x256` |
|---:|---:|---:|
| 1 | 0.850000000 | 0.850000000 |
| 2 | 0.843478261 | 0.843478261 |
| 3 | 0.836500221 | 0.836500221 |
| 4 | 0.831672744 | 0.831672744 |

但 total rho 不是分辨率稳定的 observable：`64x128` 保持同一组单调比值，而 `128x256` 的 shape=2/3/4 因电子与离子贡献在 sampled axis cells 近乎抵消，total-rho axis 比值为 `1/1/1`。最大跨分辨率差为 `0.168327256`。

## 源码边界

`ChargeDeposition.H` 仍负责 RZ 半径 `sqrt(xp*xp + yp*yp)` 和 shape 权重 `sx[ix]*sz[iz]*wq`，不读取 `verboncoeur_axis_correction`；axis toggle 只在 `ApplyInverseVolumeScalingToChargeDensity` 的后续路径出现。因此当前最窄结论是：species-level shape behavior 可跨分辨率复现，但 total-rho 的可见性受 species cancellation 与网格共同影响。

分类：`RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_CROSS_RESOLUTION_BOUNDARY_OPEN`。这不是 charge closure、正式收敛阶或具体 kernel root cause 证明。审计脚本为 `scripts/audit_rz_axis_correction_nonneutral_resolution_family.py`，报告为 `runs/stage-c-validation/rz-axis-correction-nonneutral-shape-resolution-family-v0.107/contract.{json,md}`。
