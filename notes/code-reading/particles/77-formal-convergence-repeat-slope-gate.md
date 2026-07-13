# Formal convergence repeat-slope gate

## 结论

v0.95 把两组 RZ/RSPHERE family 的 slope 一致性从开放文字变成可执行 gate。预注册的比较量是同一 geometry、同一 correction-on 控制、同一 observable 和同一相邻 refinement interval 的 pairwise log2 slope 绝对差；容差固定为 `1e-8`。

当前 14 个 correction-on comparisons 全部通过，最大绝对 slope 差为 `2.587e-11`。RZ 与 RSPHERE 分开比较，覆盖 field、axis charge 和 off-axis charge observable 的全部声明区间，没有 pooled fit，也没有事后删除异常区间。

## correction-off 负对照

`correction=off` 仍被读取和报告，但不进入 slope gate。它的 axis/off-axis residual 接近 numerical/reader floor，导致 log-slope 对末位误差敏感；本轮负对照的最大绝对 slope 差为 `1.996e-3`。把这个差异当作 formal-order failure 会把 reader floor 误写成物理不一致，因此只保留为 descriptive negative control。

## 结论边界

该 gate 只证明两个独立 family 对 correction-on slope 的重复一致性，不证明某个唯一的 formal numerical order。更不关闭 correction-on axis charge correctness：RZ/RSPHERE axis residual 仍然高于强 charge gate，且 v0.94 的 source-diagnostic crosswalk 仍将它分类为 `SOURCE_DIAGNOSTIC_DISCRETIZATION_BOUNDARY`。

合同由 `scripts/audit_formal_convergence_repeat_slope_gate.py` 生成，产物位于 `runs/stage-c-validation/formal-convergence-repeat-slope-gate-v0.95/contract.{json,md}`。下一步仍需把 slope comparison、独立 charge gate 和更强的离散算子中间量分开收口，不能把本 gate 的 PASS 写成整项 formal convergence closure。
