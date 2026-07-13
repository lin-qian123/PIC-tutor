# Higuera-Cary Poincare evidence boundary

当前 Poincare 相关运行证据应分成三层，而不能压成一个“拓扑通过”结论：

1. 短轨道 family 只有 8 个截面点/轨道，分类器明确返回 `INSUFFICIENT_SAMPLING`。
2. 长轨道 family 达到最少 16 个截面点；invariant order 和 quartic reference curve 通过，时间顺序折线产生的交叉候选在 angular ordering 后消失，但 topology gate 仍保持 `REVIEW_REQUIRED`。
3. 密集 `p_y` family 的 resonance-sensitive screen 和 coarse/fine resolution screen 通过，支持 Vay 在约 `p_y=1.7` 窗口的局部漂移候选；但 dense family 的解析 reference curve 和 cross-pusher candidate signature 不一致，因此不能升级成 paper-equivalent island/trajectory-crossing 证明。

`scripts/summarize_higuera_poincare_evidence.py` 将这三层与现有 5 个合同统一验收。当前分类为 `HIGUERA_POINCARE_INVARIANT_AND_RESONANCE_SCREEN_VERIFIED_TOPOLOGY_REMAINS_UNPROMOTED`。后续若要关闭 topology 缺口，仍需论文一致的截面构造、足够密的参考轨道以及明确的 two-fold island/trajectory-crossing gate。
