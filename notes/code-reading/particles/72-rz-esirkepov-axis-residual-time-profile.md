# RZ Esirkepov evolved-time axis residual profile

## 目的

v0.90 将 v0.89 的单一末帧径向 profile 扩展到现有 8 个 `256x512`、2-rank RZ sibling 的全部数值 plotfile。每个 case 都有 `diag1000000` 初始化帧、`diag1000040` 中间帧和 `diag1000080` 末帧。

## 归一化与初始化帧边界

每个 plotfile 独立读取 `rho` 和 `divE`，计算

$$
R_{i,j} = \frac{|(\nabla\cdot E)_{i,j} - \rho_{i,j}/\epsilon_0|}{\max_{i,j}|\rho_{i,j}/\epsilon_0|}.
$$

`diag1000000` 保留在原始表中，但不参加 evolved-time 分类。它是 `t=0` 初始化基线；在尚未形成演化场的情况下，使用同一归一化会使 off-axis 的零场/零差结构主导最大值，不能与粒子推进后的残差混写。

## 结果

- 8 个 case、24 个保存帧全部成功读取。
- 排除初始化帧后，16 个 evolved frames 的 profile maximum 全部位于 `r=0`。
- `diag1000040` 与 `diag1000080` 均保持 axis dominance；correction-on/default 的末帧 `r=0` 最大值为 `7.554e-4/8.990e-4/9.289e-4/9.729e-4`，correction-off 为 `1.639e-11/1.020e-11/8.399e-12/6.669e-12`。

原始合同：`runs/stage-c-validation/esirkepov_langmuir_rz_axis-residual-time-profile/contract.{json,md}`。分类为 `POST_INITIAL_AXIS_DOMINATED_READER_SIDE_RESIDUAL_TIME_PROFILE`。

## 结论边界

这条时间证据说明 axis dominance 不是只在末帧偶然出现，并支持优先检查 axis volume scaling、staggering/interpolation 和 mode handling 的耦合。它仍是 reader-side same-surface profile：不能区分这些候选的根因，不能证明 current closure，也不能关闭正式收敛或默认 correction-on 的 `divE-rho` boundary。
