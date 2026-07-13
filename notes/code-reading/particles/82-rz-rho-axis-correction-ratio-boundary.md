# RZ rho axis correction ratio boundary

v0.101 将 rho-side 的轴修正从源码静态合同推进到现有 correction-on/off 初始帧的独立比值合同。对 `64x128`、`128x256`、`256x512` 三档 family，输入卡除 `boundary.verboncoeur_axis_correction` 外相同；off-axis `rho_electrons`/`rho_ions` 比值严格为 `1`，说明该对照没有把全域场值整体重标定。

但 axis 两个 species 的 `rho(on)/rho(off)` 都稳定为 `0.85`。源码 `ApplyInverseVolumeScalingToChargeDensity` 在 RZ axis 使用 `1/3`（correction-on）和 `1/4`（correction-off），若只考虑这两个外层体积因子，纯比例应为

$$
\frac{1/4}{1/3}=0.75.
$$

因此当前可复核结论是：axis rho 输出存在一个稳定的、跨分辨率的比例边界，不能由源码轴体积因子单独解释。合同分类为 `RZ_RHO_AXIS_CORRECTION_RATIO_MISMATCH_BOUNDARY_OPEN`。这不是 charge PASS，也不能单独把根因归给 deposition kernel；候选剩余层包括轴向粒子沉积/镜像、`RhoFunctor` 重建、mode/位置处理和输出时序。报告见 `runs/stage-c-validation/rz-rho-axis-correction-ratio-v0.101/contract.{json,md}`。
