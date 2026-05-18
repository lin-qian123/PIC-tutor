# `QedChiFunctions`、virtual photons 与 `linear_breit_wheeler` 的分叉关系

绑定源码：

- `../warpx/Source/Particles/ElementaryProcess/QEDInternals/QedChiFunctions.H`
- `../warpx/Source/Particles/Collision/CollisionHandler.cpp`
- `../warpx/Source/Particles/Collision/BinaryCollision/VirtualPhotonCreation.cpp`
- `../warpx/Source/Particles/Collision/BinaryCollision/LinearBreitWheeler/LinearBreitWheelerCollisionFunc.H`
- `../warpx/Source/Particles/Collision/BinaryCollision/LinearCompton/LinearComptonCollisionFunc.H`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Examples/Tests/virtual_photons/*`
- `../warpx/Examples/Tests/linear_breit_wheeler/*`
- `../warpx/Examples/Tests/linear_compton/*`

这篇笔记回答一个容易混淆的问题：WarpX 里名字都带 QED / photons / Breit-Wheeler 的几条路径，到底哪些属于前面已经梳理过的 `ElementaryProcess` 强场 QED 主链，哪些其实属于 `CollisionHandler -> BinaryCollision` 的另一棵树。

## 1. `QedChiFunctions.H` 只负责算 `chi`

`QedChiFunctions.H` 只有两个 GPU 包装函数：

- `QedUtils::chi_photon(...)`
- `QedUtils::chi_ele_pos(...)`

它们只做一件事：把 SI 单位下的：

- 粒子动量
- `E/B` 场

转交给 PICSAR 的：

- `picsar::multi_physics::phys::chi_photon`
- `picsar::multi_physics::phys::chi_ele_pos`

因此它不是：

- 事件调度器
- table 管理器
- product-species 组织层

而只是强场 QED 所依赖的基础数学包装。

## 2. 当前强场 QED 主链怎样消费 `chi`

源码检索显示，`QedUtils::chi_*` 当前直接进入三类位置：

1. `PushSelector.H`
   - classical radiation reaction 与 QED 联动时，用 `chi_ele_pos(...)` 做阈值判断
2. `QuantumSyncEngineWrapper.H`
   - `chi_ele_pos(...)` 进入 Quantum Synchrotron optical-depth 演化和 photon emission 采样
3. `BreitWheelerEngineWrapper.H`
   - `chi_photon(...)` 进入 Breit-Wheeler optical-depth 演化和 pair-generation 采样

所以 `QedChiFunctions` 服务的是上一组笔记已经打通的这条强场 QED 树：

```text
gather E/B
-> compute chi
-> evolve optical depth
-> lookup-table sampling
-> update source and create products
```

## 3. virtual photons 不走 `chi -> optical depth -> lookup table`

另一个分叉在 `PhysicalParticleContainer.cpp` 里先出现。

species 构造期除了：

- `do_qed_quantum_sync`
- `do_qed_breit_wheeler`

之外，还支持：

- `do_qed_virtual_photons`
- `qed_virtual_photon_species_name`
- `qed_virtual_photons_do_beam_size_effect`

并且源码强制只有：

- electron
- positron

可以开启 virtual photons。

`MultiParticleContainer::mapSpeciesProduct()` 后续只是把：

- source lepton species
- virtual photon species

做容器层映射，并检查 product species 的类型必须是 photon。

这一步最关键的结论是：virtual photons 虽然在 `WARPX_QED` 宏下，但它不走：

- `InitQED()`
- `qed_qs.*` / `qed_bw.*`
- `opticalDepthQSR/BW`
- lookup tables

## 4. virtual photons 的运行时入口在 `CollisionHandler::doCollisions()`

`CollisionHandler::doCollisions()` 一开始先做：

```cpp
// The virtual photons are newly generated here and participate in the collisions.
// Here, the virtual photons are regenerated from scratch, i.e. they are overwritten by new ones at each time step.
collision::binarycollision::virtualphotons::GenerateVirtualPhotons(mypc);
```

这说明 virtual photons 的运行时位置在碰撞调度层，而不是：

- `doQedEvents()`
- `QEDPhotonEmission.H`
- `QEDPairGeneration.H`

它属于另一条主链：

```text
CollisionHandler
-> GenerateVirtualPhotons()
-> BinaryCollision functors
```

## 5. `GenerateVirtualPhotons()` 的真实语义是“每步重建辅助 photon species”

`VirtualPhotonCreation.cpp` 的算法结构是：

1. 遍历所有开启 `do_qed_virtual_photons` 的 lepton species
2. 读取 virtual photon species 上的：
   - `qed_virtual_photons_min_energy`
   - `qed_virtual_photons_multiplier`
3. 第一遍 kernel：
   - 按 Berestetskii 公式决定每个主粒子要采样多少 virtual photons
4. `ExclusiveSum` 得到 offsets 与 tile 内总 photon 数
5. 直接 `resize` 对应的 photon species tile
6. 第二遍 kernel：
   - 写出 virtual photon 的 `ux,uy,uz,x,y,z,w,idcpu`

源码注释还明确写了：

- 旧 virtual photons 会在下一步被覆盖

所以这不是普通会继续 push 的 product photons，而是碰撞模块每步现造的一份辅助 photon 分布。

## 6. beam-size effect 是 virtual photons 专有的几何分支

`VirtualPhotonCreation.cpp` 在 3D 下支持：

- `qed_virtual_photons_do_beam_size_effect`

打开后，虚光子位置不再与源 lepton 完全重合，而是按：

- reduced Compton wavelength
- fractional energy
- 横向随机方向

在垂直于主粒子动量的平面内做有限半径位移。

这层几何逻辑只存在于 virtual photons 分叉，不属于：

- Quantum Synchrotron
- Breit-Wheeler table sampling
- Schwinger

也不复用 `QedChiFunctions`。

## 7. `linear_breit_wheeler` 不是 `doQedBreitWheeler()` 的别名

`CollisionHandler.cpp` 对 `type = linear_breit_wheeler` 的分派是：

```cpp
std::make_unique<
    BinaryCollision<LinearBreitWheelerCollisionFunc, ParticleCreationFunc>
>(...)
```

因此它不走：

- `MultiParticleContainer::doQedBreitWheeler()`
- `PairGenerationFilterFunc`
- `BreitWheelerEngineWrapper`
- `opticalDepthBW`
- lookup tables

而是走 `BinaryCollision` 的另一套骨架：

1. 在 cell 内把两类 photon 宏粒子配对
2. `LinearBreitWheelerCollisionFunc` 判断这一对是否发生反应
3. 把结果写进：
   - `p_mask`
   - `p_pair_indices_*`
   - `p_pair_reaction_weight`
4. 再由 `ParticleCreationFunc` 真正创建 electron / positron products

这和强场 Breit-Wheeler 最大的不同不是某个公式系数，而是整个调度结构都不一样。

## 8. `linear_breit_wheeler` / `linear_compton` 属于 Higginson 风格的 binary-collision 路径

`LinearBreitWheelerCollisionFunc.H` 和 `LinearComptonCollisionFunc.H` 都明确说明：

- 在 cell 内进行宏粒子对碰撞
- 算法来自 Higginson et al. 2019
- 当前实现相对原论文还做了：
  - 质心系变换的相对论推广
  - `probability_threshold / probability_target_value` 的高概率修正
  - 按配对次数重新分配权重

这两条路径控制的运行时参数是：

- `event_multiplier`
- `probability_threshold`
- `probability_target_value`

而不是强场 QED 那套：

- `chi_min`
- `lookup_table_mode`
- `photon_creation_energy_threshold`

## 9. virtual photons 正是把 lepton species 与 collision-QED 分叉接起来的桥

现在就能把三层关系压实：

1. `QedChiFunctions`
   - 只服务强场 QED 主链
2. virtual photons
   - 在碰撞前把 lepton species 每步转成辅助 photon species
3. `linear_breit_wheeler` / `linear_compton`
   - 再把这些 photon 或 real photon 拿去做 `BinaryCollision`

因此 WarpX 里至少有两棵名字都带 QED / photons 的树：

### 强场 QED / `ElementaryProcess`

```text
QedChiFunctions
-> QuantumSync/BreitWheeler wrappers
-> optical depth
-> lookup tables
-> filterCopyTransformParticles
```

### 碰撞 QED / `BinaryCollision`

```text
optional GenerateVirtualPhotons()
-> BinaryCollision<LinearBreitWheeler or LinearCompton>
-> p_mask / reaction weights
-> ParticleCreationFunc
```

这两棵树都依赖 `WARPX_QED`，但不共享同一套事件骨架。

## 10. regression 证据也对应两棵不同的树

### virtual photons

`Examples/Tests/virtual_photons/analysis_virtual_photons.py` 检查：

- 每个电子平均生成的 virtual photon 数
- `dN/dy` 能谱
- virtual photons 与源电子位置一致

`analysis_beamsize_effect.py` 进一步检查：

- beam-size effect 关闭时坐标不变
- 打开后位移半径在理论上限内

这两组 tests 验证的是：

- `GenerateVirtualPhotons()` 的采样和几何写入

而不是强场 QED tables。

其中 `inputs_test_3d_beamsize_effect` 的结构也很说明问题：两束高能轻子都开启 `do_qed_virtual_photons = 1`，但分别把

- `qed_virtual_photons_do_beam_size_effect = 0`
- `qed_virtual_photons_do_beam_size_effect = 1`

放在并列 species 上，同时把 Maxwell solver 关掉，并令主束 `do_not_deposit = 1`、`do_not_push = 1`。这使得 `analysis_beamsize_effect.py` 检查到的差异几乎完全来自 virtual-photon 生成本身，而不是后续场推进或粒子动力学。

### linear Breit-Wheeler

`Examples/Tests/linear_breit_wheeler/analysis_base.py` 与 `analysis_many_photons.py` 检查：

- 电荷守恒
- 能量守恒
- 动量守恒
- pair yield 时间演化与理论公式一致

这验证的是：

- binary-collision pairing
- 事件概率
- reaction weight
- product creation

也不是 `doQedBreitWheeler()` 的强场 event pass。

## 11. 当前源码边界

这一轮源码阅读后，可以把边界压成三句：

1. `QedChiFunctions` 是强场 QED 的基础数学包装层，不是所有 QED-like 过程的统一入口。
2. virtual photons 属于 `CollisionHandler` 前置辅助 species 生成器，每步重建，不进入 `InitQED()` / lookup-table / optical-depth 主链。
3. `linear_breit_wheeler` 和 `linear_compton` 属于 `BinaryCollision` 家族，只和碰撞调度、mask、reaction weight、product creation 共享骨架，而不是 `ElementaryProcess` 的 QED event kernels。

有了这层分叉图，后面继续：

- 下钻 `BinaryCollision`
- 读 `BackgroundMCC/PulsedDecay`
- 或再追 `QedChiFunctions` 更深数学角色

都不会再把两套不同的多物理主链混写。
