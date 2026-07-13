# Explicit leapfrog position update: source crosswalk

## 目的

本笔记固定第 4 章里容易混写的三件事：momentum half-push、显式位置更新，以及 plotfile 中可见的粒子属性。它只读当前 WarpX checkout，不把相邻 plotfile 重建的速度 proxy 当成直接 half-step diagnostic。

## 源码链

1. `PhysicalParticleContainer.cpp` 的显式主循环先调用 `doParticleMomentumPush(...)`。
2. 当 `position_push_type == PositionPushType::Full` 时，紧接着调用 `UpdatePosition(...)`，再写回粒子位置。
3. `UpdatePosition.H` 对有质量粒子计算

   $$
   \gamma^{-1}=\left(1+|\mathbf u|^2/c^2\right)^{-1/2},
   \qquad
   \mathbf x^{n+1}=\mathbf x^n+\mathbf u^{n+1/2}\gamma^{-1}\Delta t.
   $$

   因而这里的 `ux/uy/uz` 不是任意整数时刻速度，而是显式 leapfrog 位置推进所消费的时间中心动量。

4. `PushSelector.H` 保留 Boris 的 `FirstHalf/SecondHalf/Full` 分派参数；当前 `UpdateMomentumHigueraCary(...)` 的接口没有 `momentum_push_type`，因此不能把 Higuera-Cary 直接描述成与 Boris 相同的 split-half runtime surface。

## 诊断边界

当前公共 Full plotfile 可以输出位置和机械动量。用相邻帧位置差除以物理时间步，可以构造 position-update velocity proxy；这对 uniform-`B` 对照已经通过，但它不是直接读取的半步速度属性，也不证明论文 Appendix B 的专门圆轨道输出已经接入 WarpX regression。

## 验收

`scripts/audit_position_leapfrog_source_crosswalk.py` 对上述调用顺序、公式锚点、维度条件、selector split surface 和 Higuera-Cary 接口边界执行只读检查。报告写入 `runs/stage-c-validation/position-leapfrog-source-crosswalk/contract.{json,md}`。
