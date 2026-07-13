# 75. RZ axis charge 跨 family repeat stability

## 目的

v0.92 已完成两组独立 RZ/RSPHERE 2-rank refinement family，但 correction-on `divE-rho` 仍只是稳定趋势。v0.93 不再新增 producer，而是把两组末帧的 axis/off-axis residual 做成独立 repeat stability contract，判断“axis-dominated”是否依赖某一次运行。

## 判据

对每个 geometry、correction 和 `64/128/256` level，比较第一、第二 family 的 axis residual：

$$
\delta_{repeat} = \frac{|R_{axis}^{(1)}-R_{axis}^{(2)}|}{\max(|R_{axis}^{(1)}|,|R_{axis}^{(2)}|)}
$$

`correction=on` 使用 `delta_repeat <= 1e-10` 作为 reader-side 重复稳定性 gate；同时要求两组 family 都满足 `R_axis > R_off-axis`。`correction=off` 只作 negative control，因为其绝对 residual 已接近 reader/numerical floor，不能用相对差直接套同一 gate。

## 结果

RZ 与 RSPHERE 的 6 个 correction-on level 全部通过 `1e-10` gate，且 axis residual 在两组 family 中均高于 off-axis。RZ correction-off 的相对末位差在低残差下被放大，但绝对差仍处于数值地板量级。合同见 `runs/stage-c-validation/rz-axis-charge-repeat-stability-v0.93/contract.{json,md}`，公开摘要见 `docs/rz-axis-charge-repeat-stability-v0.93.{json,md}`。

## 边界

该证据把 correction-on axis charge 定位为跨 family 稳定的 reader-side boundary，增强了正文中“不能把单次 profile 当偶然噪声”的论证；它仍不能区分 axis-volume scaling、staggering/interpolation、mode handling、diagnostic discretization 与 deposition kernel，也不证明 current closure 或正式 convergence order。
