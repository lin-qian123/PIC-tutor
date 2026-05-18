# QED 多物理入口：runtime attributes、product species 与三条事件主链

绑定源码：

- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/PhotonParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/ElementaryProcess/QEDPhotonEmission.{H,cpp}`
- `../warpx/Source/Particles/ElementaryProcess/QEDPairGeneration.{H,cpp}`
- `../warpx/Source/Particles/ElementaryProcess/QEDSchwingerProcess.H`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`

关联 regression：

- `../warpx/Examples/Tests/qed/analysis_quantum_sync.py`
- `../warpx/Examples/Tests/qed/analysis_breit_wheeler_core.py`
- `../warpx/Examples/Tests/qed/analysis_schwinger.py`

## 1. 第一入口不在单个 kernel，而在 species 构造期

QED 不是运行到一半才“顺手开一下”的开关。`PhysicalParticleContainer` 和 `PhotonParticleContainer` 构造期就先决定：

1. 该 species 是否启用 quantum synchrotron
2. 是否启用 Breit-Wheeler
3. 需要给 SoA 额外加哪些 runtime attributes
4. 产物 species 的名字是什么

`PhysicalParticleContainer.cpp` 里最关键的三段是：

```cpp
pp_species_name.query("do_qed_quantum_sync", m_do_qed_quantum_sync);
if (m_do_qed_quantum_sync) {
    AddRealComp("opticalDepthQSR");
}

pp_species_name.query("do_qed_breit_wheeler", m_do_qed_breit_wheeler);
if (m_do_qed_breit_wheeler) {
    AddRealComp("opticalDepthBW");
}

if(m_do_qed_quantum_sync){
    pp_species_name.get("qed_quantum_sync_phot_product_species",
        m_qed_quantum_sync_phot_product_name);
}
```

这里的语义有三层：

- `opticalDepthQSR` 是 lepton species 的持久 runtime attribute；
- `opticalDepthBW` 是 photon species 的持久 runtime attribute；
- 产品 species 名字先存成字符串，真正变成容器索引要等 `MultiParticleContainer::mapSpeciesProduct()`。

`PhotonParticleContainer.cpp` 里又补了一条硬约束：

```cpp
pp_species_name.query("do_qed_breit_wheeler", m_do_qed_breit_wheeler);
if(m_do_qed_breit_wheeler){
    pp_species_name.get("qed_breit_wheeler_ele_product_species",
        m_qed_breit_wheeler_ele_product_name);
    pp_species_name.get("qed_breit_wheeler_pos_product_species",
        m_qed_breit_wheeler_pos_product_name);
}

bool test_quantum_sync = false;
pp_species_name.query("do_qed_quantum_sync", test_quantum_sync);
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    test_quantum_sync == 0,
    "ERROR: do_qed_quantum_sync can't be enabled for photon particles!");
```

也就是说：

- lepton species 可以开 `do_qed_quantum_sync`；
- photon species 可以开 `do_qed_breit_wheeler`；
- photon species 不能反过来再开 quantum synchrotron。

## 2. `InitQED()` 的职责不是做事件，而是装配 engine 和表

QED 真正的模块初始化不在 species 构造函数里，而在：

```cpp
MultiParticleContainer::InitMultiPhysicsModules()
```

这条链里：

```cpp
for (auto& pc : allcontainers) {
    pc->InitIonizationModule();
}
mapSpeciesProduct();
CheckIonizationProductSpecies();
#ifdef WARPX_QED
CheckQEDProductSpecies();
InitQED();
#endif
```

这里要分清三层职责：

1. `mapSpeciesProduct()`：把字符串 species 名字变成容器索引；
2. `CheckQEDProductSpecies()`：检查产品 species 类型是否正确；
3. `InitQED()`：创建 QED engine，并初始化 lookup tables。

`mapSpeciesProduct()` 对 QED 的部分是：

```cpp
if (pc->has_breit_wheeler()){
    pc->m_qed_breit_wheeler_ele_product =
        getSpeciesID(pc->m_qed_breit_wheeler_ele_product_name);
    pc->m_qed_breit_wheeler_pos_product =
        getSpeciesID(pc->m_qed_breit_wheeler_pos_product_name);
}

if(pc->has_quantum_sync()){
    pc->m_qed_quantum_sync_phot_product =
        getSpeciesID(pc->m_qed_quantum_sync_phot_product_name);
}
```

`CheckQEDProductSpecies()` 又把类型合同写死：

- Breit-Wheeler 的两个 product 必须分别是 electron 和 positron；
- Quantum Synchrotron 的 product 必须是 photon；
- product 不能和 source species 是同一个容器。

`InitQED()` 本体则只做 engine 和 lookup-table 初始化：

```cpp
m_shr_p_qs_engine = std::make_shared<QuantumSynchrotronEngine>();
m_shr_p_bw_engine = std::make_shared<BreitWheelerEngine>();
...
if(m_nspecies_quantum_sync != 0) {
    InitQuantumSync();
}
if(m_nspecies_breit_wheeler !=0) {
    InitBreitWheeler();
}
```

`InitQuantumSync()` 和 `InitBreitWheeler()` 都遵循同一套模式：

- 读 `qed_qs.*` 或 `qed_bw.*`
- 读 `chi_min`
- 决定 `lookup_table_mode = builtin / load / generate`
- 初始化或生成 tables

所以 `InitQED()` 的核心语义是：

- 它不产生任何粒子；
- 它只是把“哪些 species 会参与哪些 QED 过程”以及“这些过程用哪张表”装配完成。

## 3. 主循环里的插入顺序：field ionization 之后，particle injection 之前

QED 事件不是在 `PushPX()` 里偷偷发生的。顶层主循环在 `WarpXEvolve.cpp` 里先明确插入：

```cpp
doFieldIonization();

#ifdef WARPX_QED
doQEDEvents();
mypc->doQEDSchwinger();
#endif

ExecutePythonCallback("particleinjection");
OneStep(cur_time, dt[0], step);
```

这说明当前主循环的多物理顺序是：

1. 先做 field ionization
2. 再做 QED photon emission / pair generation
3. 再做 Schwinger
4. 然后才进入用户 particle injection 和正常 PIC step

这里有两个重要结论：

- QED 事件发生在 `OneStep()` 之前，不是碰撞那样嵌在 split-momentum push 的组织里；
- 它直接消费 `Efield_aux/Bfield_aux`，所以它看到的是进入本步前已经准备好的辅助场。

## 4. `doQEDEvents()` 实际上又分成两条：BW 先，QS 后

`WarpX::doQEDEvents()` 只是逐 level 转发到 `MultiParticleContainer::doQedEvents()`：

```cpp
mypc->doQedEvents(
    lev,
    *m_fields.get(FieldType::Efield_aux, Direction{0}, lev),
    ...
    *m_fields.get(FieldType::Bfield_aux, Direction{2}, lev)
);
```

而 `MultiParticleContainer::doQedEvents()` 的真实顺序是：

```cpp
doQedBreitWheeler(...);
doQedQuantumSync(...);
```

也就是：

- photon 的 pair generation 先做；
- lepton 的 photon emission 后做。

这个顺序不是对称随便写的，它隐含了一条实现假设：同一步里先处理已有 photon species 的衰变，再处理 lepton 的新 photon 产生。

## 5. Quantum Synchrotron：`filterCopyTransformParticles` 同时改 source 和 product

`doQedQuantumSync()` 的骨架是：

```cpp
auto& pc_product_phot =
    allcontainers[pc_source->m_qed_quantum_sync_phot_product];

const auto Filter   = phys_pc_ptr->getPhotonEmissionFilterFunc();
const auto CopyPhot = copy_factory_phot.getSmartCopy();

auto Transform = PhotonEmissionTransformFunc(
      m_shr_p_qs_engine->build_optical_depth_functor(),
      pc_source->GetRealCompIndex("opticalDepthQSR") - pc_source->NArrayReal,
      m_shr_p_qs_engine->build_phot_em_functor(),
      pti, lev, Ex.nGrowVect(), ...);

filterCopyTransformParticles<1>(
    *pc_product_phot, dst_tile, src_tile, np_dst,
    Filter, CopyPhot, Transform);
```

这条链的物理语义不是“只新建 photon”：

1. `Filter` 用 `opticalDepthQSR` 判断 source lepton 是否发生事件；
2. `Transform` 需要场 gather、external particle fields、QED table；
3. `Transform` 既会更新 source 粒子的 optical depth / momentum，也会生成 product photon；
4. 生成后的低能 photon 还会被 `cleanLowEnergyPhotons(...)` 再筛一次。

所以 quantum synchrotron 真正是：

- 对 source lepton 做事件判定和状态更新；
- 对 product photon 做复制-变换-落盘前初始化；
- 这不是简单的“在旁边 append 一批 photon”。

## 6. Breit-Wheeler：source 是 photon，两个 product 是 electron/positron

`doQedBreitWheeler()` 结构和上面平行，但它是双 product：

```cpp
auto& pc_product_ele =
    allcontainers[pc_source->m_qed_breit_wheeler_ele_product];
auto& pc_product_pos =
    allcontainers[pc_source->m_qed_breit_wheeler_pos_product];

const auto Filter  = phys_pc_ptr->getPairGenerationFilterFunc();
const auto pair_gen_functor = m_shr_p_bw_engine->build_pair_functor();

auto Transform = PairGenerationTransformFunc(pair_gen_functor,
                                             pti, lev, Ex.nGrowVect(), ...);

filterCopyTransformParticles<1>(
    *pc_product_ele, *pc_product_pos,
    dst_ele_tile, dst_pos_tile, src_tile,
    np_dst_ele, np_dst_pos,
    Filter, CopyEle, CopyPos, Transform);
```

这里要注意三点：

1. source species 仍然是 photon 容器；
2. 事件后会同时生成 electron 和 positron 两个 product；
3. `PairGenerationTransformFunc` 也要 gather 主网格场和 external particle fields。

这说明 WarpX 当前的 QED 事件模型非常一致：

- source 粒子上的 optical depth 决定是否触发；
- 事件 functor 从 PICSAR-QED wrapper 来；
- `filterCopyTransformParticles` 负责把 event decision、source 更新和 product 创建绑在一起。

## 7. Schwinger 是第三条完全不同的路径

Schwinger 不属于“source species 复制到 product species”的模型，它直接从场创建粒子：

```cpp
void MultiParticleContainer::doQEDSchwinger ()
```

它的边界非常硬：

- 只支持 `warpx.grid_type=collocated` 或 momentum-conserving gather；
- 不支持 mesh refinement；
- 不支持 RZ；
- 不支持 1D。

它直接用：

- `Efield_aux/Bfield_aux`
- 全局几何窗口 `qed_schwinger_{xmin,...,zmax}`
- `filterCreateTransformFromFAB<1>(...)`

在网格上按 cell/node 创建 `ele_schwinger` 和 `pos_schwinger`。

所以 Schwinger 不是 quantum synchrotron / Breit-Wheeler 的再包装，而是第三条独立的“场到粒子”创建路径。

## 8. regression 证据：三类 analysis 对应三条 QED 主链

### 8.1 `analysis_quantum_sync.py`

这组脚本不是只看“有没有 photon”。

它明确检查：

1. photon 数目是否符合理论率
2. photon 权重是否正确
3. photon 发射方向是否和初始粒子方向一致
4. photon 能谱是否符合理论分布
5. source lepton 和 product photon 的 optical depth 分布是否仍是指数分布

因此它直接验证的是：

- `opticalDepthQSR`
- quantum synchrotron engine
- product photon 初始化
- source/product optical-depth 合同

### 8.2 `analysis_breit_wheeler_core.py`

这组脚本检查：

1. 产生的 pair 数是否符合理论率
2. electron/positron 权重是否继承 photon 权重
3. residual photons 是否保持原始动量
4. pairs 是否沿原 photon 方向发射
5. 单事件能量守恒
6. 电子/正电子能谱是否符合理论分布
7. photon / electron / positron 的 optical depth 分布是否仍为指数分布

因此它是 product-species 合同最强的回归证据之一。

### 8.3 `analysis_schwinger.py`

Schwinger 的断言口径完全不同：

1. 若理论期望对数极小，则应完全不产对；
2. 若理论期望显著非零，则 `ele_schwinger` 与 `pos_schwinger` 的总物理权重和必须落在理论率的 `5 sigma` 窗口内；
3. 电子和正电子的权重数组必须逐项一致。

所以它验证的是：

- 强场率标度
- 生成对数目
- 成对权重一致性

而不是 quantum synchrotron / Breit-Wheeler 那种 optical-depth 继承合同。

## 9. 当前最关键的实现边界

当前入口层已经能明确看到几条后续必须继续下钻的边界：

1. `QuantumSyncEngineWrapper` / `BreitWheelerEngineWrapper` 只是 wrapper，本体物理采样在 PICSAR-QED；
2. `PhotonEmissionTransformFunc` / `PairGenerationTransformFunc` 里真正怎样同时更新 source 和 product，还值得再单开一篇；
3. `doQEDSchwinger()` 和普通 species/QED species 的 product 创建机制并不一样，不能混写成一条链；
4. `CollisionHandler` 下的 `linear_breit_wheeler` / `linear_compton` 是另一套 collision-style QED 接口，和这里的 `ElementaryProcess/QED*` 入口要分开讲。

## 10. 本轮结论

QED 在 WarpX 里不是“一个统一的 qed 开关”，而是三条不同的多物理入口：

1. quantum synchrotron：lepton source -> photon product
2. Breit-Wheeler：photon source -> electron/positron products
3. Schwinger：field -> electron/positron creation

它们共享的上游是：

- species 构造期 runtime attributes
- `mapSpeciesProduct()` 的产品容器映射
- `InitQED()` 的 engine/table 初始化

但它们进入主循环后的事件组织和 regression 断言并不相同。下一层更合理的工作，不是再泛讲“QED 支持哪些过程”，而是继续下钻：

- `QEDPhotonEmission.H`
- `QEDPairGeneration.H`
- `QEDInternals/*`

把 optical depth 演化、源粒子更新和 product 粒子创建的 kernel 级细节再打穿。*** End Patch
