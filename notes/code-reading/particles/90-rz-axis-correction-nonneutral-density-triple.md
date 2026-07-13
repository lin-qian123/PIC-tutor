# RZ axis correction non-neutral density triple

## Scope

本记录对应 `128x256`、2-rank RZ 初始化帧，对 `ions.density=0.25*n0/0.5*n0/0.75*n0` 和 `particle_shape=1/2/3/4` 的 correction-on/off sibling 做 reader-side 对照。相邻 `../warpx` 只读使用，未修改上游源码。

## Result

三种密度的 species `rho_ions` axis on/off 比值完全一致：

`shape=1/2/3/4 -> 0.850000000/0.843478261/0.836500221/0.831672744`

`0.25*n0` 与 `0.75*n0` 的 total-rho 复现同一序列；`0.5*n0` 的 total-rho 为 `0.850000000/1/1/1`，其中 shape=2/3/4 在 sampled axis cells 出现 species contribution cancellation。由此可见，现象不是任意密度变化都会触发的普遍失效，而是特定物种配比与 shape 组合下的合成 observable cancellation。

所有 on/off sibling 均通过粒子状态、off-axis rho、初始 field、MPI decomposition 和 `delta(rho)` species-sum 检查。源码交叉检查仍显示 `ChargeDeposition.H` 的 RZ shape path 不读取 `boundary.verboncoeur_axis_correction`，axis correction 由后续 axis wrap/scaling consumer 处理。

## Classification and limits

分类：`RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_SAMPLED_AXIS_CANCELLATION_SPECIAL_RATIO_BOUNDARY_OPEN`

该结果收窄的是 total-rho sampled-axis observable 的边界，不是 kernel root cause、charge closure 或正式收敛阶证明。原始合同：`runs/stage-c-validation/rz-axis-correction-nonneutral-density-triple-v0.109/contract.{json,md}`；复现实验脚本：`scripts/audit_rz_axis_correction_nonneutral_density_triple.py`。
