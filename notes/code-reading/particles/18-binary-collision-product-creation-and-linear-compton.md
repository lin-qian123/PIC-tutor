# `BinaryCollision`、`ParticleCreationFunc` 与 `linear_compton` / `linear_breit_wheeler` 的 product 创建合同

绑定源码：

- `../warpx/Source/Particles/Collision/BinaryCollision/BinaryCollision.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/ParticleCreationFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/ParticleCreationFunc.cpp`
- `../warpx/Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/LinearBreitWheelerInitializeMomentum.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/LinearCompton/LinearComptonInitializeMomentum.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/LinearBreitWheelerCollisionFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/LinearCompton/LinearComptonCollisionFunc.H`
- `../warpx/Examples/Tests/linear_breit_wheeler/*`
- `../warpx/Examples/Tests/linear_compton/*`

上一篇笔记已经把：

- 强场 QED / `ElementaryProcess`
- 碰撞 QED / `BinaryCollision + virtual photons`

两棵树分开了。这一篇继续往碰撞树里走，专门回答一个更具体的问题：

- `BinaryCollision` 在 tile 内做完 pairing 和事件判断之后，product particles 到底怎样被创建？

## 1. `BinaryCollision` 真正输出给下游的不是“新粒子”，而是事件表

`BinaryCollision<CollisionFunctor, CopyTransformFunctor>` 的 cell 级碰撞 functor 先做的不是直接 `push_back` product particles，而是先在 tile 内构造几组事件表：

- `p_mask`
- `p_pair_indices_1`
- `p_pair_indices_2`
- `p_pair_reaction_weight`
- 可选 `p_product_data`

含义分别是：

- 哪一对真的发生了反应
- 这对反应来自哪两个 parent 粒子
- 这次反应要抽走多少权重并交给 products
- 某些 collision type 额外需要的中间数据

也就是说，`BinaryCollision` 的前半段更像一个“事件压缩器”，先把 tile 内所有可能配对压缩成一张可供创建函数消费的事件清单。

## 2. 真正的 product 创建统一交给 `ParticleCreationFunc`

如果该 collision type 有 `product_species`，`BinaryCollision` 会在 tile 内进一步调用：

- `ParticleCreationFunc`

这一步才真正：

1. 给 product species tile 分配空间
2. 决定每个事件在每个 product species 里增加多少宏粒子
3. 把 parent 粒子的位置信息和默认属性复制过去
4. 设置 product 权重
5. 再按具体 collision type 初始化 product 动量

因此碰撞树当前的清晰分层是：

```text
CollisionFunc
-> p_mask / pair indices / reaction weights
-> ParticleCreationFunc
-> type-specific momentum initialization
```

## 3. `ParticleCreationFunc` 先决定“每个事件要生几个不同 species、每种生几个”

`ParticleCreationFunc.cpp` 的构造函数先根据 collision type 决定：

- `m_num_product_species`
- `m_num_products_host/device`

当前几类典型情况是：

- Proton-Boron fusion：
  - 1 个 product species
  - 每次反应生 3 个 alpha
- two-product fusion / `LinearBreitWheeler` / `LinearCompton`：
  - 2 个 product species
  - 每个 species 每次反应先定义为 1 个“物理 product”

但这还不是最终加到 tile 里的宏粒子数，因为后面还要乘上一个很关键的几何因子。

## 4. `LinearCompton` 和其他 binary creation 路径的最大不同：`products_per_reactant_factor`

`ParticleCreationFunc.H` 在真正分配产品粒子前先决定：

```cpp
const int products_per_reactant_factor =
    (m_collision_type == CollisionType::LinearCompton) ? 1 : 2;
```

这意味着：

- `LinearCompton`：每个 product species 每个事件只创建 1 个宏粒子
- 几乎所有其他 binary creation 过程：
  - 包括 `LinearBreitWheeler`
  - 每个事件都按两个 reactants 的位置各创建一份 product

源码注释把原因写得很直白：

- `LinearCompton`：一个散射 photon 放在入射 photon 位置，一个散射 lepton 放在入射 lepton 位置
- 其他过程：在两个 parent 位置各复制一套 product，以保持严格电荷守恒

这是 WarpX 当前 `BinaryCollision` product 创建里最重要的非对称点。

## 5. 为什么 `LinearBreitWheeler` 会变成“4 个宏粒子”

`LinearBreitWheelerInitializeMomentum.H` 里已经把这个语义写死了：

- 物理上每次事件只有一对 `electron + positron`
- 但实现上会在两个入射 photon 的位置各复制一套

因此最终宏粒子数是：

- 2 个电子宏粒子
- 2 个正电子宏粒子

并且四个宏粒子里：

- 两个电子动量相同
- 两个正电子动量相同

只是空间位置分别继承自两个不同的 parent photons。

再配合 `ParticleCreationFunc` 里：

- 每个 product 宏粒子只拿 `p_pair_reaction_weight / 2`

就能看出 WarpX 的策略是：

- 用“复制到两个 parent 位置”换取局域电荷守恒
- 再用“每份减半权重”保持总产额正确

## 6. `LinearCompton` 则故意不复制两份

`ParticleCreationFunc` 对 `LinearCompton` 的 special case 是：

- product photon 用 `copy_species1`，继承入射 photon 的位置
- product electron 用 `copy_species2`，继承入射 electron 的位置
- 两个 products 都拿完整的 `p_pair_reaction_weight`

所以 `LinearCompton` 的一个事件最终只会新增：

- 1 个散射 photon 宏粒子
- 1 个散射 electron 宏粒子

这和 `LinearBreitWheeler` 的“4 宏粒子实现”形成鲜明对比。

## 7. `SmartCopy` 先复制 parent 结构，真正的动量由 type-specific initializer 覆盖

`ParticleCreationFunc` 里 product 粒子的创建顺序是：

1. 先用 `SmartCopy` 把 parent 粒子的基本结构复制到 product tile
2. 写 product 权重
3. 再按 collision type 调：
   - `ProtonBoronFusionInitializeMomentum`
   - `TwoProductFusionInitializeMomentum`
   - `LinearBreitWheelerInitializeMomentum`
   - `LinearComptonInitializeMomentum`
4. 最后 `DefaultInitializeRuntimeAttributes(...)`

这说明 product 创建不是“一步到位算完所有属性”，而是：

- 先复制容器/结构层默认状态
- 再覆盖动量
- 再补 runtime attributes 的默认初始化

## 8. `LinearComptonInitializeMomentum` 的物理结构

`LinearComptonInitializeMomentum.H` 的流程很完整：

1. 取入射 photon 和 lepton 的动量
2. 先把入射 photon 四动量 Lorentz 变换到 lepton 静止系
3. 在静止系里按 Klein-Nishina 分布抽样散射角
4. 得到散射后的 photon 动量
5. 再反变换回 lab frame
6. 最后用总动量守恒直接给出散射后 lepton 动量

因此 `LinearCompton` 的 product 初始化不是简单的“沿入射方向随机抖一下”，而是完整的：

```text
lab frame
-> lepton rest frame
-> sample Klein-Nishina angle
-> back to lab frame
-> enforce momentum conservation on scattered lepton
```

## 9. `LinearBreitWheelerInitializeMomentum` 则复用中心动量系下的 pair 生成

`LinearBreitWheelerInitializeMomentum.H` 更短，因为真正的物理核心已经放在：

- `LinearBreitWheelerComputeProductMomenta(...)`

里了。这个 helper 会根据两束 photon 的入射动量，给出：

- 一份 electron 动量
- 一份 positron 动量

然后初始化函数再把这两份动量各复制两次，填给四个宏粒子。

所以：

- `LinearCompton` 的复杂性在静止系散射角采样
- `LinearBreitWheeler` 的复杂性在事件是否发生与 pair 动量求解
- `ParticleCreationFunc` 只负责把这些结果落到 tile 内的实际 product 宏粒子布局上

## 10. 创建完 products 后，parent species 的无效粒子才会被统一清掉

`BinaryCollision::doCollisions()` 在每个 level 完成后，如果有 product species，会统一做：

- `species1.deleteInvalidParticles()`
- `species2.deleteInvalidParticles()`

这说明 product creation 和 invalid parent 删除是两步：

1. 先通过 collision functor 和 creation functor 改权重、建新粒子
2. 再在 level 末尾统一清理由权重耗尽或显式标 invalid 的 parent 粒子

这和前面 particle boundaries / EB scraping / QED pair generation 里的“先标 invalid，后统一删”语义是同一类容器合同。

## 11. regression 证据怎样对应这层 product 创建语义

### linear Breit-Wheeler

`Examples/Tests/linear_breit_wheeler/analysis_base.py` 和 `analysis_many_photons.py` 检查：

- 总能量守恒
- 总动量守恒
- 电荷守恒
- pair yield 时间演化

这些检查共同验证的其实就是：

- cell-local pairing
- reaction weight
- product creation
- 以及 `LinearBreitWheelerInitializeMomentum` 的结果能否和全局守恒兼容

### linear Compton

`Examples/Tests/linear_compton/analysis_base.py` 检查：

- 总能量守恒
- 总动量守恒
- 电荷守恒

`analysis_bunch_laser.py` 进一步检查：

- 散射后总纵向动量守恒
- 横向总动量仍为 0
- 最终散射 photon fraction 与 Klein-Nishina 估计相近

这组回归正好对应了：

- `LinearComptonCollisionFunc`
- `ParticleCreationFunc` 的 1-product-per-species special case
- `LinearComptonInitializeMomentum` 的 rest-frame 采样与回变换

## 12. 当前源码边界

这一轮源码阅读后，`BinaryCollision` 这一支当前已经能压实成四句：

1. collision functor 先输出事件表，而不是直接创建 products。
2. `ParticleCreationFunc` 才是统一的 product 容器落地层。
3. `LinearBreitWheeler` 为保持局域电荷守恒，会把一对物理 products 复制成四个宏粒子。
4. `LinearCompton` 是当前最明显的特例，它每个事件只给每个 product species 创建一个宏粒子，并通过 rest-frame Klein-Nishina 抽样初始化散射动量。

有了这层以后，后面再去读：

- `BackgroundMCC`
- `PulsedDecay`
- DSMC 的 `SplitAndScatterFunc`

就不会再把“事件判断”和“product species 真正落地”的职责混在一起。
