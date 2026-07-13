# RZ non-neutral shape family across ion density

## 问题

v0.107 在 `128x256`、`ions.density = 0.5*n0` 的 shape family 中发现：species rho 的 axis 比值仍随 shape 单调下降，但 shape=2/3/4 的 total-rho 因电子/离子贡献抵消而接近 `1`。本轮保持网格、粒子、shape 和 on/off 控制不变，只把离子密度改为 `0.25*n0`，检查 total-rho 的可见性是否随物种配比变化。

## Runtime 证据

两组 `128x256` family 都由真实 2-rank WarpX 运行生成。每个 on/off sibling 只差 `boundary.verboncoeur_axis_correction`；初始化帧的粒子 ID、位置、角度、权重和动量逐项一致，off-axis rho 比值为 `1`，初始 `Er/Ez/divE` 不变，`delta(rho)` 与 species delta 逐数组相符。

species rho axis on/off 比值在两种离子密度上完全相同：`0.850000000/0.843478261/0.836500221/0.831672744`。但 total-rho 的可见性不同：

| `ions.density` | total-rho shape=1/2/3/4 |
|---:|---:|
| `0.25*n0` | `0.850000000/0.843478261/0.836500221/0.831672744` |
| `0.5*n0` | `0.850000000/1/1/1` |

因此 v0.107 的现象不是“128x256 网格必然失去 shape 依赖”，而是 total-rho 这个合成 observable 对 species cancellation 和离子密度敏感。该结果不能反向证明具体 kernel root cause，也不能关闭 charge closure 或正式收敛阶。

## 源码边界

`ChargeDeposition.H` 仍负责 RZ 半径和 shape 权重，且不读取 `verboncoeur_axis_correction`；axis toggle 仍出现在后续 `ApplyInverseVolumeScalingToChargeDensity` 路径。当前最窄分类为 `RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_CANCELLATION_DENSITY_SENSITIVE_BOUNDARY_OPEN`。审计脚本为 `scripts/audit_rz_axis_correction_nonneutral_density_family.py`，报告为 `runs/stage-c-validation/rz-axis-correction-nonneutral-density-family-v0.108/contract.{json,md}`。
