# `BackgroundMCC`、`PulsedDecay` 与 DSMC `SplitAndScatterFunc`

绑定源码：

- `../warpx/Source/Particles/Collision/BackgroundMCC/BackgroundMCCCollision.H`
- `../warpx/Source/Particles/Collision/BackgroundMCC/BackgroundMCCCollision.cpp`
- `../warpx/Source/Particles/Collision/BackgroundMCC/ImpactIonization.H`
- `../warpx/Source/Particles/Collision/PulsedDecay/PulsedDecay.H`
- `../warpx/Source/Particles/Collision/PulsedDecay/PulsedDecay.cpp`
- `../warpx/Source/Particles/Collision/BinaryCollision/DSMC/DSMCFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/DSMC/DSMCFunc.cpp`
- `../warpx/Source/Particles/Collision/BinaryCollision/DSMC/SplitAndScatterFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/DSMC/SplitAndScatterFunc.cpp`

对应 examples / regressions：

- `../warpx/Examples/Tests/collision/inputs_test_3d_collision_pulsed_decay`
- `../warpx/Examples/Tests/collision/analysis_collision_3d_pulsed_decay.py`
- `../warpx/Examples/Tests/ionization_dsmc/inputs_test_3d_ionization_electron_dsmc`
- `../warpx/Examples/Tests/ionization_dsmc/inputs_test_1d_charge_exchange_dsmc`
- `../warpx/Examples/Tests/ionization_dsmc/inputs_test_1d_two_product_reaction_dsmc`
- `../warpx/Examples/Tests/ionization_dsmc/inputs_test_1d_photoneutralization_dsmc`
- `../warpx/Examples/Tests/ionization_dsmc/analysis_ionization_dsmc_3d.py`
- `../warpx/Examples/Tests/ionization_dsmc/analysis_charge_exchange_dsmc_1d.py`
- `../warpx/Examples/Tests/ionization_dsmc/analysis_two_product_reaction_dsmc_1d.py`
- `../warpx/Examples/Tests/ionization_dsmc/analysis_photoneutralization_dsmc_1d.py`

这一篇解决的不是前面已经讲过的：

- `BinaryCollision -> ParticleCreationFunc`
- 强场 QED `ElementaryProcess`

而是另外三条实现分叉：

1. 单 species 对背景气体的 `BackgroundMCC`
2. 非 pairwise 的 `PulsedDecay`
3. 仍挂在 `BinaryCollision` 体系下，但 product 创建逻辑不同的 DSMC `SplitAndScatterFunc`

---

## 1. `BackgroundMCC`：单 species 对背景介质，不是 pair table

`BackgroundMCCCollision` 继承自 `CollisionBase`，但它和普通 `BinaryCollision<...>` 的第一性差别是：

- 只显式跟踪一个运动 species
- 背景气体不作为完整宏粒子 species 参与配对
- 背景密度和温度由常数或 parser 给定

构造期会强制：

- `species` 只有一个显式 colliding species
- `background_density` 可以是常数，也可以是 `background_density(x,y,z,t)`
- `background_temperature` 可以是常数，也可以是 `background_temperature(x,y,z,t)`
- `max_background_density` 必须可得，因为后面要估算最大碰撞频率

`scattering_processes` 会被解析成多个 `ScatteringProcess`。其中有一个特殊分叉：

- 若 process 是 ionization，则额外读取 `ionization_species`
- 该 species 会追加到 `m_species_names`
- 但源码只允许一个 ionization process

因此 `BackgroundMCC` 的逻辑不是“多 process 的任意自由组合”，而是：

- 若干守恒散射过程
- 加上最多一个 impact-ionization 过程

这也解释了为什么它的 `doCollisions()` 是两段式：

1. 先做 particle-conserving background collisions
2. 再做 `doBackgroundIonization(...)`

### 1.1 `nu_max` 是整个算法的上游稳定性门闩

`get_nu_max(...)` 会在给定能量表范围内扫描碰撞频率峰值，并乘上 `m_max_background_density` 得到最大频率估计。`doCollisions()` 第一次调用时会懒初始化：

- `m_nu_max`
- `m_total_collision_prob`
- 若有 ionization，则还有 `m_nu_max_ioniz`
- `m_total_collision_prob_ioniz`

然后它会显式检查

$$
\nu_{\max}\,\Delta t
$$

若该值过大就给出 warning。也就是说，`BackgroundMCC` 的上游稳定性控制不是 pairwise combinatorics，而是 null-collision 风格的最大频率约束。

### 1.2 `ImpactIonization` 用的是 filter/copy/transform，不是 pair table

`ImpactIonizationFilterFunc` 的逻辑是：

1. 先按总 ionization collision probability 抽一次样
2. 在粒子位置上评估背景密度 parser
3. 由粒子动量算 kinetic energy
4. 插值得到 ionization cross section
5. 再用局域碰撞频率相对 `nu_max` 做第二次 accept/reject

触发后，`ImpactIonizationTransformFunc` 会：

- 用背景温度给 ion velocity 加 Maxwellian 展宽
- 先扣掉 ionization energy
- 再把剩余能量在原电子和新电子之间平分
- 把两只电子都随机化为各向同性出射

因此这条链本质上更接近：

```text
source electron
-> probability filter
-> transform source momentum
-> create product electron and ion
```

而不是：

```text
pair reactants
-> event table
-> ParticleCreationFunc
```

---

## 2. `PulsedDecay`：不是碰撞配对，而是 cell 内权重衰变与再生

`PulsedDecay` 也是 `CollisionBase` 子类，但语义完全不同。它要求：

- 恰好一个 parent species
- 两个 product species
- 产品总电荷守恒
- 产品总质量守恒

用户输入的真正物理驱动量不是 cross section，而是：

- `decay_rate(x,y,z,t)`
- `fixed_product_weight`
- `productA_temperature_eV`
- `productB_temperature_eV`

因此它描述的不是“两个宏粒子相遇后散射”，而是：

$$
\frac{dn_1}{dt} = -\nu(x,y,z,t)\,n_1,
\qquad
\frac{dn_A}{dt} = \nu n_1,
\qquad
\frac{dn_B}{dt} = \nu n_1.
$$

### 2.1 算法结构：先按 cell 统计，再按固定宏粒子权重生 products

`PulsedDecay::doCollisions()` 的 tile 级主链是：

1. 用 `findParticlesInEachCell()` 找每个 cell 内的 parent particles
2. 统计每个 cell 的总宏粒子权重 `wtot1`
3. 在 cell center 上评估 `decay_rate(x,y,z,t)`
4. 计算该 cell 本步应衰变掉的总权重
5. 用
   $$
   N_{\text{macro}} \approx \frac{W_{\text{products}}}{w_{\text{fixed}}}
   $$
   决定要生成多少 product 宏粒子
6. 对 productA / productB tile 做 resize
7. 在每个 cell 内随机挑 parent particle 作为新 products 的位置与基底速度来源
8. 给 A/B 分别叠加用户指定的方向相关 thermal speed
9. 再从 parent cell 内的真实粒子权重里扣掉对应 `fixed_product_weight`

这里最关键的是：`PulsedDecay` 不是对某个 parent 粒子“一对一衰变”。它先在 cell 级确定总衰变权重，再通过固定 product 权重离散化成宏粒子数，最后从该 cell 的有效粒子集合里扣权重。

### 2.2 parent 不是立刻删掉，而是按统一 invalid/weight 语义逐步耗尽

扣权重使用的仍然是 `BinaryCollisionUtils::remove_weight_from_colliding_particle(...)`。因此 parent species 的消失方式仍遵守 WarpX 粒子通用合同：

- 权重可能被逐渐减小
- 权重扣空后粒子才会变 invalid
- 真正删除仍由后续统一清理阶段完成

这一点把 `PulsedDecay` 和前面讲过的 absorbing boundaries、BinaryCollision、QED source invalidation 接回了同一种容器语义。

---

## 3. DSMC：事件筛选仍在 `BinaryCollision` 前半段，product 生成改走 `SplitAndScatterFunc`

DSMC 依然属于 `BinaryCollision` 家族，但它在后半段没有继续复用上一节讲过的 `ParticleCreationFunc`。真正负责它的两段对象是：

- `DSMCFunc`
- `SplitAndScatterFunc`

### 3.1 `DSMCFunc`：先做 pair sampling 和权重扣除

`DSMCFunc::Executor` 在 cell 内：

- 把两组粒子做配对
- 针对每对调用 `CollisionPairFilter<...>`
- 按 `ScatteringProcess` 决定是否发生
  - elastic
  - back
  - ionization
  - charge_exchange
  - two_product_reaction
- 若事件发生，先从两个 reactant 权重里扣掉 `p_pair_reaction_weight`

输出仍是前面熟悉的 event table：

- `p_mask`
- `p_pair_indices_1`
- `p_pair_indices_2`
- `p_pair_reaction_weight`

所以 DSMC 前半段和 `LinearCompton` / `LinearBreitWheeler` 的共同点是：

- 先筛事件
- 再做后半段 product / child 生成

但它的后半段不是 `ParticleCreationFunc`。

### 3.2 `SplitAndScatterFunc`：slot 语义固定，兼顾“保留 reactants”与“新增 true products”

`SplitAndScatterFunc` 用四个固定 slot 组织 product tiles：

- slot 0：第一 reactant species 的 child copy
- slot 1：第二 reactant species 的 child copy
- slot 2：第一 true product
- slot 3：第二 true product

这和 `ParticleCreationFunc` 的核心差异在于：

- DSMC 的非产物散射也会显式创建 child copies
- 不是简单地“事件发生就只给新 species 加粒子”

对不同 process：

- elastic / back：
  - 只在 slot 0/1 生成 weight-split child
  - 在 center-of-momentum frame 随机旋转或反转速度
- charge exchange / two-product reaction：
  - 在 slot 2/3 生成 true products
  - `charge_exchange` 还会交换 product 生成位置，以维持局域电荷守恒
  - 动量由 `TwoProductComputeProductMomenta(...)` 统一处理
- ionization：
  - slot 0 保留 incident/reactant copy
  - slot 2/3 分别生成 ejected electron 与 ion
  - 再用专门的三体能量分配近似更新动量

因此 DSMC 的后半段更接近“反应网络中的 child-species 重建”，而不是前一篇 `ParticleCreationFunc` 那种“把 pair event 直接落地成标准 products”。

### 3.3 `linear_compton` 与 DSMC 后半段的根本差异

前一篇已经解释过 `LinearCompton` 走的是：

- `BinaryCollision`
- `ParticleCreationFunc`
- type-specific momentum initializer

而 DSMC 这里不是。它自己在 `SplitAndScatterFunc` 里直接处理：

- reactant copy 是否保留
- true products 应该写进哪些 slot
- 是否交换 products 的生成位置
- 非相对论 COM frame 动量重排

所以这两条虽然都挂在 `BinaryCollision` 下，但后半段的 product 语义已经完全不同。

---

## 4. regression 证据层：`PulsedDecay`、DSMC ionization、charge exchange、two-product、photoneutralization 各看不同物理量

### 4.1 `analysis_collision_3d_pulsed_decay.py`

`pulsed_decay` 的 analysis 不是查单粒子速度，而是：

- 先用高斯时间依赖 `decay_rate` 积分出 0D 模型
- 再从 `particle_number.txt` 取 product ion 的总权重
- 比较最终 ion weight 是否与 0D 衰变模型一致

因此它验证的是：

- `decay_rate(x,y,z,t)`
- `fixed_product_weight`
- cell 级总权重转化
- parent 权重扣减

这整条 `PulsedDecay` 合同。

### 4.2 `analysis_ionization_dsmc_3d.py`

3D DSMC ionization regression 做的是全局模型对照：

- 由截面表积分出 Maxwellian rate coefficient
- 建立 `n_e`、`n_n`、`n_e T_e` 的 ODE
- 用 openPMD diagnostics 反算 WarpX 的
  - plasma density
  - neutral density
  - electron energy density
- 再逐项比较 relative error

因此它验证的是：

- DSMC ionization cross section 使用
- source/neutral 数守恒
- 电离能损失进入电子能量方程

而不是只验证“是否多出了一个电子 species”。

### 4.3 `analysis_charge_exchange_dsmc_1d.py`

这条 regression 读取 `H` 和 `Hplus` 的粒子通量，和

$$
\Phi(z)=\Phi_0 e^{-n \sigma z}
$$

型理论衰减做比较。它主要锁定的是：

- `charge_exchange` 反应率
- product species 顺序
- position swap 之后的局域通量保真

### 4.4 `analysis_two_product_reaction_dsmc_1d.py`

这条 regression 不看通量，而是直接比较两只 product species 的速度。它验证的是：

- `two_product_reaction_energy`
- `TwoProductComputeProductMomenta(...)`
- 反应前后 COM frame 能量分配

### 4.5 `analysis_photoneutralization_dsmc_1d.py`

这条 regression 有一处实现边界很重要：

- 电子飞得太快，会立刻离开 box
- 所以 analysis 不是从普通 diagnostics 取电子
- 而是从 `BoundaryScraping` 的 `particles_at_zlo` 读电子

它因此同时验证：

- photoneutralization 反应的 product 动量
- `BoundaryScraping` 对快电子的抓取

这条链把 collision / DSMC 与 diagnostics buffer 明确接了起来。

### 4.6 `analysis_default_regression.py`

`ionization_dsmc/analysis_default_regression.py` 只是通用 checksum helper：

- 自动识别 plotfile 或 openPMD
- 再调 `evaluate_checksum(...)`

它本身不提供额外物理断言，作用只是兜底保证 baseline 不漂。

---

## 5. 这一轮得到的结构结论

到这里，`Particles/Collision` 至少已经能分成四簇清楚的实现结构：

1. `BackgroundMCC`
   - 单显式 species 对背景介质
   - null-collision 风格 `nu_max`
   - ionization 走 filter/copy/transform
2. `PulsedDecay`
   - 非 pairwise
   - cell 内总权重衰变再离散成固定 product weight
3. `BinaryCollision + ParticleCreationFunc`
   - `linear_breit_wheeler`
   - `linear_compton`
4. `BinaryCollision + SplitAndScatterFunc`
   - DSMC elastic/back
   - DSMC ionization
   - DSMC charge exchange
   - DSMC two-product reaction

也就是说，“collision” 在 WarpX 里不是一个统一 product-creation 机制，而是至少三种不同的后半段实现：

- transform-only
- fixed-weight decay
- pair-event tables + custom child creation

这也是为什么不能再用一套简化说法把 `BackgroundMCC`、`PulsedDecay`、DSMC、`LinearCompton`、QED 全混成“碰撞会产生新粒子”。
