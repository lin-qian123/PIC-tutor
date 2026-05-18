# Collision 主链入口：`CollisionHandler` 分派、步进模式与 `split_momentum_push` 验证层

绑定源码：

- `../warpx/Source/Particles/Collision/CollisionHandler.H`
- `../warpx/Source/Particles/Collision/CollisionHandler.cpp`
- `../warpx/Source/Particles/Collision/CollisionBase.H`
- `../warpx/Source/Particles/Collision/CollisionBase.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/WarpX.cpp`

代表性 examples / regressions：

- `../warpx/Examples/Tests/collision/inputs_base_2d_collisions_split_momentum_push`
- `../warpx/Examples/Tests/collision/analysis_test_2d_collisions_split_momentum_push.py`
- `../warpx/Examples/Tests/collision/inputs_test_2d_collisions_split_momentum_push_electrostatic`
- `../warpx/Examples/Tests/collision/inputs_test_2d_collisions_split_momentum_push_electromagnetic`
- `../warpx/Examples/Tests/collision/inputs_test_2d_collisions_split_momentum_push_electromagnetic_vay`
- `../warpx/Examples/Tests/collision/inputs_test_2d_charge_exchange_dsmc`
- `../warpx/Examples/Tests/collision/inputs_test_3d_collision_pulsed_decay`

## 1. Collision 在 WarpX 里不是一个 species 小插件

与 field ionization 不同，collision 的第一入口不在 `PhysicalParticleContainer` 里，而在 `MultiParticleContainer` 层：

```cpp
collisionhandler = std::make_unique<CollisionHandler>(this);
```

运行时调用则是：

```cpp
collisionhandler->doCollisions(step, cur_time, dt, this);
```

因此 collision 模块的设计出发点不是“某个 species 自己决定怎么碰撞”，而是：

- 先在全局参数里声明一组 collision objects
- 再由统一 handler 在每个 PIC step 或若干步里调度它们

这和 field ionization 的“每个源 species 自己携带 product species 逻辑”是不同的抽象层级。

## 2. `CollisionHandler` 的职责就是“名字到对象”的总分派

`CollisionHandler` 构造期会先读取：

```cpp
pp_collisions.queryarr("collision_names", collision_names);
```

然后对每个 collision name 查它自己的：

```cpp
<collision_name>.type
```

默认值是：

```cpp
std::string type = "pairwisecoulomb";
```

也就是说，在 legacy 输入里如果没显式写 `type`，WarpX 会把它解释成 pairwise Coulomb collision。

## 3. 当前支持的类型不是一条线，而是一张分派表

`CollisionHandler.cpp` 当前显式分派到：

- `pairwisecoulomb`
- `background_mcc`
- `pulsed_decay`
- `background_stopping`
- `dsmc`
- `nuclearfusion`
- `bremsstrahlung`
- `linear_breit_wheeler`
- `linear_compton`

它们背后的对象模型也分成几类：

1. 直接继承 `CollisionBase` 的整块模块：
   - `BackgroundMCCCollision`
   - `PulsedDecay`
   - `BackgroundStopping`
2. 模板化的 `BinaryCollision<CollisionFunc, CreationFunc>`：
   - Coulomb
   - DSMC
   - nuclear fusion
   - bremsstrahlung
   - linear Breit-Wheeler
   - linear Compton

因此，WarpX 的 collision 入口其实已经把“只改动动量”和“会生成新粒子”的两类过程放在同一套 handler 下面统一调度了。

## 4. `CollisionBase` 给的不是物理公式，而是时间调度合同

`CollisionBase` 最核心的公共状态只有三件事：

- `m_species_names`
- `m_ndt`
- `m_collision_stepping_mode`

其中 `m_collision_stepping_mode` 只有两种：

- `Supercycle`
- `Subcycle`

对应输入是互斥的：

- `<collision_name>.ndt_supercycle`
- `<collision_name>.ndt_subcycle`

旧参数 `<collision_name>.ndt` 已经被废弃，源码会直接报错。

这说明 `CollisionBase` 的真正合同不是“提供一个碰撞算子”，而是“给出一个碰撞算子在 PIC 时间步里以什么节奏调用”。

## 5. `Subcycle` 和 `Supercycle` 的真实语义

`CollisionHandler::doCollisions()` 对每个 collision object 的逻辑是：

### 5.1 `Subcycle`

如果：

```cpp
collision_stepping_mode == CollisionSteppingMode::Subcycle
```

则会在一个 PIC step 内运行 `ndt` 次，每次：

```cpp
dt_sub = dt / ndt
sub_time = cur_time + i_sub * dt_sub
collision->doCollisions(sub_time, dt_sub, mypc);
```

这适用于碰撞频率比主场推进更快、需要更细 collision time resolution 的情形。

### 5.2 `Supercycle`

如果是 `Supercycle`，则只在：

```cpp
step % ndt == 0
```

时运行一次，并把单次碰撞步长放大到：

```cpp
dt_collision = dt * ndt
```

这适用于碰撞过程比 PIC 主步慢得多的场景。

所以，这里的 `ndt` 不是统一意义的“碰撞子步数”，而是要和 stepping mode 一起解释。

## 6. `split_momentum_push` 是 collision 和 pusher 之间最关键的耦合点

`WarpX.cpp` 在全局参数读取阶段会先看：

```cpp
collisions.collision_names
```

只要非空，默认就把：

```cpp
m_collisions_split_momentum_push = true;
```

然后允许用户再用：

```text
collisions.split_momentum_push
```

覆盖。

这一步很重要，因为它说明 collision 不只是“主循环里多跑一个模块”，而是默认要插到 momentum push 的中间。

源码还明确给出当前边界：

- implicit evolve scheme 下不支持真正的 split momentum push，会忽略该选项并告警
- Higuera-Cary pusher 当前也不支持

因此，collision 模块从入口层开始就已经和 pusher choice、evolve scheme 强耦合，而不是独立正交选项。

## 7. `analysis_test_2d_collisions_split_momentum_push.py` 为什么重要

这个 regression 的价值不在于覆盖最多 collision type，而在于它直接验证了 `split_momentum_push` 这一调度合同。

它做两类断言：

1. 总能量守恒误差必须足够小
2. 场能量涨落的长期平均必须接近 equipartition 参考值

更关键的是，它会根据输入里：

```text
warpx.do_electrostatic
```

自动切换 electrostatic / electromagnetic 的 equipartition 公式和容差。

因此它不是单纯的“跑出一条曲线看看”，而是在用 reduced diagnostics 的：

- `field_energy`
- `particle_energy`

直接给 collision insertion ordering 做数值稳定性断言。

## 8. `inputs_base_2d_collisions_split_momentum_push` 覆盖了什么

这个 base input 有几个关键特征：

- 周期边界
- 双 species：electrons / protons
- `pairwisecoulomb` 默认 type
- full particle + field diagnostics
- reduced diagnostics：`FieldEnergy` 和 `ParticleEnergy`

它覆盖的是最小的“可验证碰撞热化”框架，而不是现实应用几何。

随后三个具体 tests 只是换外层求解环境：

- electrostatic
- electromagnetic
- electromagnetic + Vay

所以这里的变量不是碰撞模型本体，而是 collision 与 field/pusher 组合的耦合边界。

## 9. `CollisionHandler` 的另外几条重要分叉

虽然这轮不下钻每个实现，但从入口层已经能看出后续阅读应该怎么分块。

### 9.1 `background_mcc`

它不是 binary collision 模板实例，而是独立的 `BackgroundMCCCollision`。这说明带背景中性气体的 MCC 路径，在抽象上和 pairwise binary collisions 已经分家。

### 9.2 `dsmc`

它仍复用 `BinaryCollision<DSMCFunc, SplitAndScatterFunc>`，说明 DSMC 在 WarpX 里被看作：

- pair selection / probability 在 `DSMCFunc`
- 产物与权重/动量更新在 `SplitAndScatterFunc`

这条线和 field ionization 的 `filter + transform` 结构有某种相似性，但发生在 collision 模板体系内。

### 9.3 `bremsstrahlung`、`linear_breit_wheeler`、`linear_compton`

这三条都已经在 collision handler 入口里，而不是放在纯 QED 独立入口里。也就是说，WarpX 当前把若干“会生成新粒子”的高能过程也视作 collision family 的一部分。

## 10. virtual photons 是 QED 与 collision 的交界点

`CollisionHandler::doCollisions()` 一开始有一段只在 `WARPX_QED` 下启用的逻辑：

```cpp
collision::binarycollision::virtualphotons::GenerateVirtualPhotons(mypc);
```

注释明确说，这是给 incoherent QED processes 使用的中介虚光子。

这说明从体系结构上看：

- `QED` 并不完全平行于 `Collision/`
- 至少一部分高能过程是“QED 物理 + collision 调度壳”

这也是为什么下一阶段进入 QED 时，不能把它完全和 collision 子树割裂开读。

## 11. 这轮能给回归索引压实哪些条目

从当前入口层，可以把原先还偏粗的几类条目进一步明确成：

1. `analysis_test_2d_collisions_split_momentum_push.py`
   - 断言的是能量守恒和 equipartition
   - 不是一般的散射截面正确性
2. `inputs_base_2d_collisions_split_momentum_push`
   - 是 pairwise Coulomb 最小验证骨架
3. `inputs_test_2d_collisions_split_momentum_push_{electrostatic,electromagnetic,electromagnetic_vay}`
   - 重点在 field solver / pusher 组合边界
4. `test_2d_collisions_split_momentum_push_*.json`
   - checksum 基线之外，还有 analysis 的显式物理断言

## 12. 这条链在书稿里的更合理归位

collision 这一层不该继续混在 `laser_ion` 多物理开关里讲完。更合理的归位是：

1. `Laser/` 只说 `laser_ion` 给了一个应用入口
2. `Particles/` 负责说明 collision 如何插入粒子推进主循环
3. 后续再分别下钻：
   - `BinaryCollision`
   - `BackgroundMCC`
   - `BackgroundStopping`
   - `PulsedDecay`

当前这一篇的作用，就是先把“collision 在主循环哪里、按什么步频、如何和 pusher/solver 耦合、哪些 regression 真正在兜底”这四件事压实。
