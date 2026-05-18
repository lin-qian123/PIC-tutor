# `pairwise Coulomb`、`bremsstrahlung`、`background_stopping` 与 `nuclearfusion`

绑定源码：

- `../warpx/Source/Particles/Collision/BinaryCollision/Coulomb/PairWiseCoulombCollisionFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/Coulomb/ElasticCollisionPerez.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/Bremsstrahlung/BremsstrahlungFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/Bremsstrahlung/PhotonCreationFunc.H`
- `../warpx/Source/Particles/Collision/BackgroundStopping/BackgroundStopping.H`
- `../warpx/Source/Particles/Collision/BackgroundStopping/BackgroundStopping.cpp`
- `../warpx/Source/Particles/Collision/BinaryCollision/NuclearFusion/NuclearFusionFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/NuclearFusion/SingleNuclearFusionEvent.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/NuclearFusion/BoschHaleFusionCrossSection.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/NuclearFusion/ProtonBoronFusionCrossSection.H`

对应 examples / regressions：

- `../warpx/Examples/Tests/collision/analysis_collision_1d.py`
- `../warpx/Examples/Tests/collision/analysis_collision_1d_correct_conservation.py`
- `../warpx/Examples/Tests/collision/analysis_collision_1d_Bremsstrahlung.py`
- `../warpx/Examples/Tests/ion_stopping/analysis.py`
- `../warpx/Examples/Tests/nuclear_fusion/analysis_two_product_fusion.py`
- `../warpx/Examples/Tests/nuclear_fusion/analysis_proton_boron_fusion.py`

这一篇补的是 `Particles/Collision` 当前剩余的四类主分叉：

1. `pairwisecoulomb`
2. `bremsstrahlung`
3. `background_stopping`
4. `nuclearfusion`

它们都已经在 `CollisionHandler` 调度表里出现，但物理语义和后半段 product 行为互不相同，不能再统一写成“碰撞模块”。

---

## 1. `pairwisecoulomb`：没有 products，只有 cell 内配对后的动量散射

`PairWiseCoulombCollisionFunc` 是最接近“纯碰撞而不产物化”的分支。它构造期只真正读取两类东西：

- `CoulombLog`
- `use_global_debye_length`

若：

- `CoulombLog >= 0`

则直接用用户给定的 Coulomb logarithm；若：

- `CoulombLog < 0`
- 且 `use_global_debye_length = 0`

则要求运行时再计算 species 温度，因此 `Executor` 会打开：

- `m_computeSpeciesTemperatures = true`

它的 `Executor::operator()` 几乎没有任何 product 逻辑，核心就是把 cell 内配对后的粒子交给：

```cpp
ElasticCollisionPerez(...)
```

所以这条分支的最重要边界是：

- 它仍然走 `BinaryCollision` 的 cell 内 pairing 外壳
- 但不会填 `p_mask/p_product_data` 去触发 product creation
- 后半段只有 reactant 动量更新，没有新 species

### 1.1 这类 regression 看的是 relaxation 和守恒，不是粒子数

`analysis_collision_1d.py` 对的是 Higginson 2020 的 Coulomb relaxation benchmark：

- 低密度流动组注入高密度静止组
- 通过宏粒子权重分组
- 最后检查某个平行温度分量是否回到参考值

因此它验证的是：

- `ElasticCollisionPerez` 的 relaxation rate
- intra-species pairing 统计

`analysis_collision_1d_correct_conservation.py` 则换成更硬的守恒口径：

- 显式比较 step 0 和 step 1 的总动量
- 显式比较总动能
- 重点验证 collision 后应用的守恒修正是否生效

所以 pairwise Coulomb 的 strongest evidence 不是“有没有新粒子”，而是：

- relaxation benchmark
- energy/momentum conservation

---

## 2. `bremsstrahlung`：pair event 先产 photon 能量，再由专门 `PhotonCreationFunc` 落地

`BremsstrahlungFunc` 也挂在 `BinaryCollision` 框架下，但它和前面 `LinearCompton` / DSMC 的区别在于：

- 前半段 pair event 只针对 photon 产额和 photon 能量
- 后半段 product 创建不走通用 `ParticleCreationFunc`
- 而是走专门的 `Bremsstrahlung/PhotonCreationFunc`

### 2.1 前半段：`BremsstrahlungFunc` 只给出事件、权重和 photon 能量

`BremsstrahlungFunc::Executor` 在 cell 内：

- 只按第一 reactant species 的粒子数循环，默认这一侧是 electrons
- 调 `BremsstrahlungEvent(...)`
- 填：
  - `p_mask`
  - `p_pair_indices_1`
  - `p_pair_indices_2`
  - `p_pair_reaction_weight`
  - `p_product_data`

其中：

- `p_product_data` 存的是 photon energy

源码里还专门处理了低能 cutoff：

- 低于由 plasma frequency 给出的 photon cutoff，不再计入

这意味着前半段真正决定的是：

- 是否发生 bremsstrahlung
- 发生后 photon 带走多少能量

### 2.2 后半段：`PhotonCreationFunc` 同时改 electron/ion 动量并创建 photon

`PhotonCreationFunc` 的 product 语义也和通用 `ParticleCreationFunc` 不同：

- 新 photon 创建在第一 reactant 粒子位置上
- photon 权重来自 `p_pair_reaction_weight`
- photon 动量不需要表驱动采样，而是由守恒关系直接补出

更关键的是，它不会只创建 photon 然后结束。它还会：

1. 把电子和离子先变到离子静止系
2. 用给定的 photon energy 解新的 electron / ion / photon 动量守恒
3. 再把 electron、ion、photon 一起 Lorentz 变回 lab frame
4. 最后原地改写 parent electron/ion 的动量

所以这条分支的真实结构是：

```text
pairing
-> event + photon energy
-> parent electron/ion momentum update
-> photon creation
```

而不是：

```text
pairing
-> create product
```

### 2.3 regression 的 strongest evidence

`analysis_collision_1d_Bremsstrahlung.py` 明确验证三件事：

1. 总能量守恒
2. 总动量守恒
3. `dE/dx` 与解析 stopping estimate、以及每步新 photon 数与解析截面估计一致

因此这条 regression 同时锁定了：

- event rate
- photon creation count
- parent 粒子失能
- 能量动量守恒

---

## 3. `background_stopping`：不是二体散射，而是解析 slowing-down law

`BackgroundStopping` 连 `BinaryCollision` 外壳都不再走。它是 `CollisionBase` 的独立分支，并要求：

- 恰好一个 active species
- `background_type = electrons` 或 `ions`
- `background_density`
- `background_temperature`
- 若 `background_type = ions`，还要给：
  - `background_mass`
  - `background_charge_state`

### 3.1 electrons 和 ions 走两套不同公式

`doCollisions()` 只做分派：

- `doBackgroundStoppingOnElectronsWithinTile(...)`
- `doBackgroundStoppingOnIonsWithinTile(...)`

对电子背景，源码实现的是 Goldston & Rutherford 的电子 stopping 公式，写成：

$$
\frac{d\mathbf{u}}{dt} = -\alpha \mathbf{u}
$$

并在单步内积分成

$$
\mathbf{u}^{n+1} = \mathbf{u}^{n} e^{-\alpha \Delta t}.
$$

对离子背景，源码实现的是另一条能量形式：

$$
\frac{dW}{dt} = -\frac{\alpha}{\sqrt{W}},
$$

离散成

$$
W^{n+1} = \left[\left(W^n\right)^{3/2} - \frac{3}{2}\alpha \Delta t\right]^{2/3},
$$

再回推出速度缩放 `vscale`。

也就是说，`background_stopping` 根本不是“碰撞后随机散射”，而是解析 slowing-down 更新。

### 3.2 regression 的 strongest evidence

`ion_stopping/analysis.py` 直接在 Python 里重写同一组 stopping 公式：

- constant electron background
- parsed electron background
- constant ion background
- parsed ion background

然后逐步推进同样的 step 数，再和最终粒子能量逐点对比。它验证的是：

- parser 驱动的 `background_density/background_temperature`
- `background_type = electrons/ions`
- 电子 / 离子两套 slowing-down 公式

这类测试的口径和前面 pairwise scattering 完全不同：它不是统计意义上的 relaxation，而是点对点解析积分对照。

---

## 4. `nuclearfusion`：还是 pair-event 框架，但概率控制和截面模型更复杂

`NuclearFusionFunc` 重新回到 `BinaryCollision` 风格：

- cell 内 pairing
- `p_mask`
- `p_pair_indices_*`
- `p_pair_reaction_weight`

但它的事件概率计算和后处理比一般 pair reaction 更复杂。

构造期最关键的输入是：

- `event_multiplier`
- `probability_threshold`
- `probability_target_value`

以及由 `BinaryCollisionUtils::get_nuclear_fusion_type(...)` 识别出来的 fusion type。

### 4.1 `event_multiplier` 不是数值小技巧，而是显式控制宏粒子统计

源码注释已经说明：

- `event_multiplier` 用来提高 fusion 事件统计量
- 对应做法是增加 fusion occurrence，同时减小 product 权重

但如果 multiplier 开得过大，就会把单 pair 的 fusion probability 推到接近 1。这时 WarpX 不直接接受，而是用：

- `probability_threshold`
- `probability_target_value`

把本次 collision 的有效 multiplier 降下来，避免系统性低估总 yield。

这条语义在 `analysis_proton_boron_fusion.py` 的 test 4 / test 5 里直接有验证：

- 一个 test 会把 boron 几乎完全烧完
- 另一个故意把 `probability_threshold` 设得极不合理，从而观察 fusion yield 被明显低估

### 4.2 截面模型分成 Bosch-Hale 和 Tentori-Belloni 两族

源码上至少有两套主要截面路径：

- `BoschHaleFusionCrossSection.H`
  - D-D / D-T 这类经典两产物 fusion
- `ProtonBoronFusionCrossSection.H`
  - p-B11，采用 Tentori & Belloni 2023 的解析拟合

因此 `nuclearfusion` 不是“一个 cross section 文件换参数”这么简单，而是按 fusion type 切到不同物理模型。

### 4.3 regression 的 strongest evidence

`analysis_two_product_fusion.py` 主要覆盖：

- D-D / D-T 两产物 fusion
- reactant 消耗、product 数、能量守恒、动量守恒、产品各向同性
- 与 Bosch-Hale 对应的理论 fusion yield / product energy 对照

`analysis_proton_boron_fusion.py` 则覆盖更特殊的 p-B11 场景：

- 三 alpha products
- Maxwellian plasma yield 与 Tentori-Belloni 热率拟合对照
- 低 boron density 极限
- `probability_threshold` 过大时的故意失真场景

因此 `nuclearfusion` 的验证不只是“是否创建了 products”，而是：

- event probability control
- cross-section model choice
- 高能 product kinematics
- yield scaling

一起被锁定。

---

## 5. 到这里，`Collision` 主分叉已经能按后半段和物理合同分成八类

如果把前几篇一起合并，WarpX 当前已经成文的 collision / reaction 主分叉至少可以这样分：

1. `pairwisecoulomb`
   - 无 products
   - 只做动量散射与 relaxation
2. `BackgroundMCC`
   - 单 species 对背景气体
   - ionization 走 filter/copy/transform
3. `PulsedDecay`
   - cell 内总权重衰变
4. DSMC + `SplitAndScatterFunc`
   - elastic / back / ionization / charge exchange / two-product reaction
5. `linear_compton`
   - `BinaryCollision + ParticleCreationFunc`
6. `linear_breit_wheeler`
   - `BinaryCollision + ParticleCreationFunc`
7. `bremsstrahlung`
   - `BinaryCollision + PhotonCreationFunc`
8. `nuclearfusion`
   - `BinaryCollision` 事件概率 + specialized fusion cross sections / kinematics

再加上前面已经单独成文的强场 QED `ElementaryProcess`，现在就能明确看出：

- “碰撞模块”在 WarpX 里并不是一个统一产品创建器
- 后半段至少已经分裂成：
  - no-product momentum scattering
  - filter/transform
  - fixed-weight decay
  - generic `ParticleCreationFunc`
  - DSMC `SplitAndScatterFunc`
  - bremsstrahlung `PhotonCreationFunc`
  - fusion-specific event-probability control

这也是后面如果还要继续扩写 `bremsstrahlung` 的光子动量初始化、`pairwise Coulomb` 的 Perez 算法细节、或 `nuclearfusion` 的 product momentum initializer，最自然的源码入口。
