# `laser_ion` 的可选多物理开关：field ionization、collisions 与 QED 的真实接入边界

绑定源码：

- `../warpx/Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc`
- `../warpx/Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc_picmi.py`
- `../warpx/Examples/Physics_applications/laser_ion/analysis_test_laser_ion.py`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/WarpX.cpp`

支撑性 regression：

- `../warpx/Examples/Tests/field_ionization/analysis.py`
- `../warpx/Examples/Tests/collision/analysis_test_2d_collisions_split_momentum_push.py`
- `../warpx/Examples/Tests/qed/analysis_quantum_sync.py`

## 1. `laser_ion` 当前真正激活了什么，没激活什么

`laser_ion` 输入当前真正激活的是：

1. Gaussian laser antenna
2. 预电离的 `electrons + hydrogen` target
3. full diagnostics
4. time-averaged diagnostics
5. reduced diagnostics

而下面两组多物理只是预留开关，并没有在当前 regression 中打开。

### 1.1 field ionization 只是注释掉的替代分支

输入里当前启用的是：

```text
electrons.profile = parse_density_function
```

也就是把电子直接当作“fully ionized reference density”初始化出来。

可切换的另一支是：

```text
hydrogen.do_field_ionization = 1
hydrogen.physical_element = H
hydrogen.ionization_initial_level = 0
hydrogen.ionization_product_species = electrons
electrons.profile = constant
electrons.density = 0.0
```

这会把 `laser_ion` 从“预电离靶”改成“中性氢靶 + ADK 场电离 + 电离电子产物 species”。

### 1.2 collisions 也是预留开关

输入里给了：

```text
collisions.collision_names = c_eH c_ee c_HH
```

以及各组 `species` / `CoulombLog`，但当前都是注释状态。因此当前 `laser_ion` regression 并不在验证 binary collisions。

### 1.3 QED 在这个应用里当前没有入口

当前 `laser_ion` 输入里没有：

- `do_qed_quantum_sync`
- `do_qed_breit_wheeler`
- `photon` species
- `qed_*_product_species`

所以它不是 QED regression，也不应被写成“已经在 laser-target 场景中连到了 QED”。

## 2. field ionization 真正在哪一层接进 `laser_ion`

### 2.1 species 构造期只是记住 `do_field_ionization`

`PhysicalParticleContainer` 构造阶段只做最早的开关读取：

```cpp
pp_species_name.query("do_field_ionization", do_field_ionization);
```

此时还没有真正初始化 ionization module，因为 ADK 预因子依赖 `dt`。

### 2.2 真正初始化发生在 `MultiParticleContainer::InitMultiPhysicsModules()`

初始化主线是：

```cpp
for (auto& pc : allcontainers) {
    pc->InitIonizationModule();
}
mapSpeciesProduct();
CheckIonizationProductSpecies();
```

也就是说，field ionization 的接入点不是 laser profile、也不是 diagnostics，而是在 `MultiParticleContainer::InitData()` 之前统一挂上去的多物理初始化阶段。

### 2.3 `InitIonizationModule()` 做了哪些不可省的事

`PhysicalParticleContainer::InitIonizationModule()` 会：

1. 把 ionizable species 的电荷强制改回单电子电荷 `q_e`
2. 读取：
   - `ionization_initial_level`
   - `ionization_product_species`
   - `physical_element`
   - `do_adk_correction`
3. 若需要，动态加上 runtime integer attribute：
   - `ionizationLevel`
4. 从原子数据表装入 ionization energies
5. 计算 ADK 相关 prefactors

因此，在 `laser_ion` 里打开 `hydrogen.do_field_ionization = 1` 不只是多了一条开关，而是会改写：

- species 的有效电荷语义
- runtime attribute 图
- 产物 species 映射

## 3. ionization product 是怎样真正生成的

`mapSpeciesProduct()` 会先把字符串 species 名映射成整数 ID：

```cpp
if (pc->do_field_ionization){
    const int i_product = getSpeciesID(pc->ionization_product_name);
    pc->ionization_product = i_product;
}
```

之后 `doFieldIonization()` 才会在推进循环中真正创建电离产物：

```cpp
auto& pc_product = allcontainers[pc_source->ionization_product];
const SmartCopyFactory copy_factory(*pc_source, *pc_product);
auto Filter = phys_pc_ptr->getIonizationFunc(...);
filterCopyTransformParticles<1>(...)
```

也就是说，这条链的真实语义不是“把同一个 species 的电荷加 1”，而是：

1. 源离子保留并更新 `ionizationLevel`
2. 电子产物写入另一个 product species
3. 新粒子再走普通 particle push / diagnostics / filtering

## 4. `ionizationLevel` 还会继续进入电流和电荷沉积

`WarpXParticleContainer` 在沉积阶段会专门取出：

```cpp
int* ion_lev = nullptr;
if (do_field_ionization) {
    ion_lev = pti.GetiAttribs("ionizationLevel").dataPtr();
}
```

然后把它传进 `DepositCurrent(...)` 和 `DepositCharge(...)`。

因此 `ionizationLevel` 不只是给 diagnostics 看的标签，而是直接影响每个宏粒子的有效电荷，从而进入：

- `J`
- `rho`
- 后续 field solve / diagnostics

这也是为什么 `laser_ion` 一旦切到 ADK 分支，不只是粒子数会变，整条 `rho_electrons / rho_hydrogen / Ez` 诊断链都会被重写。

## 5. collisions 在源码里怎样插到主循环

与 ionization 不同，collisions 不是 species 内部模块，而是 `MultiParticleContainer` 级的统一 handler。

构造阶段就会创建：

```cpp
collisionhandler = std::make_unique<CollisionHandler>(this);
```

运行时调用入口是：

```cpp
collisionhandler->doCollisions(step, cur_time, dt, this);
```

因此在 `laser_ion` 里打开：

```text
collisions.collision_names = c_eH c_ee c_HH
```

真正改变的是主循环里是否在粒子推进流程中插入一段 cell-local binary interaction，而不是改 laser 注入本身。

## 6. `split_momentum_push` 才是 laser-target 场景里 collisions 更敏感的地方

`WarpX.cpp` 在全局参数读取阶段会根据：

```cpp
collisions.collision_names
```

决定 `m_collisions_split_momentum_push` 的默认值，并允许用户再用：

```text
collisions.split_momentum_push
```

覆盖。

它的物理含义不是“是否打开 collisions”，而是 collisions 放在 momentum push 的哪个阶段。这对高场 laser-plasma 场景更关键，因为场加速和粒子散射的 operator ordering 会直接影响：

- 总能量守恒误差
- equipartition 收敛

所以如果以后把 `laser_ion` 从 collision-free 版本推进到带 Coulomb collisions 的 target heating / stopping 版本，更敏感的参数往往不是 `collision_names` 本身，而是 `split_momentum_push` 与 pusher 组合。

## 7. QED 在这条链上的真实边界

当前 `laser_ion` 没开 QED，但源码里入口很清楚。

### 7.1 species 构造期的 QED runtime attributes

如果 species 打开：

- `do_qed_quantum_sync`
- `do_qed_breit_wheeler`

则 `PhysicalParticleContainer` 会动态加：

- `opticalDepthQSR`
- `opticalDepthBW`

并记录 product species 名称。

### 7.2 `InitMultiPhysicsModules()` 会继续做 product species 检查和 QED engine 初始化

```cpp
CheckQEDProductSpecies();
InitQED();
```

但这些逻辑都被包在 `#ifdef WARPX_QED` 里，所以它不仅是输入层开关，还依赖编译时启用 QED 支持。

### 7.3 因此 `laser_ion` 当前最多只能说“QED-ready boundary exists”

更准确的表述是：

- `laser_ion` 当前没有使用 QED
- 但它所在的 `PhysicalParticleContainer -> MultiParticleContainer` 主链已经为 QED runtime attributes、product mapping 和 engine 初始化预留了位置

## 8. 这条分叉该怎样接回 regression 证据

### 8.1 `laser_ion` 自己的 analysis 只验证 diagnostics 合同

`analysis_test_laser_ion.py` 当前只做一件硬断言：

- 把 `diagInst` 最后 5 个 snapshot 的瞬时 `Ez` 做时间平均
- 与 `diagTimeAvg` 的原位平均 `Ez` 逐点比较

因此它验证的是：

- TimeAveraged diagnostics
- openPMD field output

不是：

- ADK ionization fraction
- collision heating
- QED photon yield

### 8.2 field ionization 的直接证据来自 `Examples/Tests/field_ionization`

`analysis.py` 复现 Chen 2013 的平面波电离问题，并检查：

- 最终约 `32%` 的离子处于 `N5+`
- 若有 runtime attribute，也检查其取值合理

这才是 `laser_ion` 注释块里 `do_field_ionization` 最直接的物理验证来源。

### 8.3 collisions 的直接证据来自 `analysis_test_2d_collisions_split_momentum_push.py`

这个 analysis 关注的是：

- 总能量守恒误差
- 场能量向 equipartition 值的收敛

因此它验证的是 collision operator 在 momentum push 中的位置与能量账本，而不是 laser target 的离子加速图像。

### 8.4 QED 的直接证据来自 `analysis_quantum_sync.py` 等专门 tests

`analysis_quantum_sync.py` 检查：

- 生成 photon 数目
- photon 权重
- 发射方向
- 能量分布
- product species optical depth 初始化

所以如果将来要把 `laser_ion` 推进到超强场 QED 版本，当前最可靠的一手验证证据仍然不在 `laser_ion` 目录，而在专门的 `qed/` tests。

## 9. 这条链在书稿里的更准确定位

`laser_ion` 当前更像一个“laser 驱动 target + diagnostics 组合样板”，而不是“多物理已经全开”的一体化 benchmark。

更准确的分层应该是：

1. `laser_ion` 负责说明：
   - laser 如何驱动靶
   - diagnostics 如何组织
   - 输入层给哪些多物理留了切换位
2. `field_ionization` tests 负责证明 ADK 分支
3. `collision` tests 负责证明 binary collision 与 split-momentum ordering
4. `qed` tests 负责证明量子发光 / 对产生 / Schwinger 等高场过程

也就是说，从 `laser_ion` 切向多物理时，真正要展开的是“同一个 laser-target 输入骨架怎样挂接这些模块”，而不是把这些专门 regression 误说成已经在 `laser_ion` 当前输入里同时激活。
