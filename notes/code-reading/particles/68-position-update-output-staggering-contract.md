# Full plotfile position-update output staggering contract

## 结论

当前 `UpdatePosition.H` 明确实现

$$
\Delta \mathbf{x}=\mathbf{u}\,\gamma^{-1}\Delta t,
\qquad
\gamma^{-1}=\left(1+|\mathbf{u}|^2/c^2\right)^{-1/2}.
$$

`PhysicalParticleContainer.cpp` 也确认在 `position_push_type == PositionPushType::Full` 时，先完成 `doParticleMomentumPush(...)`，再调用 `UpdatePosition(...)` 并写回位置。

但现有三条 uniform-`B` case 的 81 个 Full plotfile 不能把上一帧或下一帧保存的机械动量直接当成该次位移的独立 half-step 输出：逐步比较的最大相对向量误差为约 `6.242e-2`。相邻两帧动量的中点 proxy 将误差压到约 `1.609e-3`，说明输出 cadence 与 leapfrog 时间层之间存在可观测的 stagger，而不是一个可以被单帧字段名自动消除的问题。

## 验收

`python scripts/audit_position_update_runtime_contract.py ...` 对 `UpdatePosition.H`、`PhysicalParticleContainer.cpp` 和 Boris/Vay/Higuera-Cary 三组 case-local 运行产物执行合同检查。当前分类为：

`POSITION_UPDATE_SOURCE_CONFIRMED_OUTPUT_STAGGERING_BOUNDARY_DIRECT_HALF_STEP_ATTRIBUTE_REMAINS`

这条合同关闭了“源码公式是否接到运行输出”的时间层歧义，但不宣称 WarpX 暴露了独立命名的 half-step velocity attribute，也不替代 Vay Appendix B 论文图形逐点复现。后续若要关闭该边界，需要在 diagnostics producer 侧显式输出正确时间层的速度，而不是继续从 Full plotfile 的相邻帧猜测。
