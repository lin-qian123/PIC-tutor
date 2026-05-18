# QED kernels 与 wrapper 合同：optical depth 演化、source/product 更新、table 边界

绑定源码：

- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/PhotonParticleContainer.cpp`
- `../warpx/Source/Particles/ElementaryProcess/QEDPhotonEmission.H`
- `../warpx/Source/Particles/ElementaryProcess/QEDPairGeneration.H`
- `../warpx/Source/Particles/ElementaryProcess/QEDInternals/QuantumSyncEngineWrapper.H`
- `../warpx/Source/Particles/ElementaryProcess/QEDInternals/BreitWheelerEngineWrapper.H`

关联 regression：

- `../warpx/Examples/Tests/qed/inputs_test_2d_qed_quantum_sync`
- `../warpx/Examples/Tests/qed/inputs_base_2d_breit_wheeler`
- `../warpx/Examples/Tests/qed/inputs_base_3d_schwinger`
- `../warpx/Examples/Tests/qed/analysis_quantum_sync.py`
- `../warpx/Examples/Tests/qed/analysis_breit_wheeler_core.py`
- `../warpx/Examples/Tests/qed/analysis_schwinger.py`

## 1. QED 事件触发不是“概率函数直接返回 true”，而是 optical depth 先在 push 中被推进

上一轮只把 QED 入口层打到了：

- species 构造期加入 `opticalDepthQSR/BW`
- `InitQED()` 装配 engine 与 tables
- `doQedQuantumSync()` / `doQedBreitWheeler()` / `doQEDSchwinger()` 插入主循环

继续往下读会发现，真正决定某个粒子在这一轮是否发生事件的，不是某个独立的 `rate > rand` 判断函数，而是：

1. 在日常 push 阶段先连续推进 optical depth；
2. 只有当 optical depth 被推进到负值时，后续 `FilterFunc` 才返回 `true`。

这在 `QEDPhotonEmission.H` 和 `QEDPairGeneration.H` 里写得非常直接：

```cpp
bool operator() (const PData& ptd, int const i, amrex::RandomEngine const&) const noexcept
{
    const amrex::ParticleReal opt_depth =
        ptd.m_runtime_rdata[m_opt_depth_runtime_comp][i];
    return (opt_depth < 0.0_rt);
}
```

也就是说：

- `PhotonEmissionFilterFunc` 看的是 `opticalDepthQSR < 0`
- `PairGenerationFilterFunc` 看的是 `opticalDepthBW < 0`

这两个 filter 自己不做任何物理采样。真正的统计演化已经在 push 阶段先发生了。

## 2. Quantum Synchrotron：source lepton 在 `PushPX()` 里先演化 optical depth

`PhysicalParticleContainer::PushPX()` 在 QED 打开时会提前准备：

```cpp
const auto do_sync = m_do_qed_quantum_sync;
if (do_sync) { t_chi_max = m_shr_p_qs_engine->get_minimum_chi_part(); }

QuantumSynchrotronEvolveOpticalDepth evolve_opt;
amrex::ParticleReal* p_optical_depth_QSR = nullptr;
const bool local_has_quantum_sync = has_quantum_sync();
if (local_has_quantum_sync) {
    evolve_opt = m_shr_p_qs_engine->build_evolve_functor();
    p_optical_depth_QSR = pti.GetAttribs("opticalDepthQSR").dataPtr() + offset;
}
```

因此 lepton species 的日常推进里，QED 不是完全独立于 pusher 的后处理。它至少已经和下面几件事绑在了一起：

- `PushPX()` 的 tile loop
- field gather
- external particle fields
- `chi_min`
- optical-depth 存储

这意味着 `opticalDepthQSR` 的演化时刻和 momentum push 是紧耦合的，而不是 diagnostics 或 post-step 再计算。

## 3. Photon path 也一样：Breit-Wheeler 的 optical depth 在光子推进时先演化

`PhotonParticleContainer::PushPX()` 里对 photon species 做的是平行结构：

```cpp
BreitWheelerEvolveOpticalDepth evolve_opt;
amrex::ParticleReal* p_optical_depth_BW = nullptr;
const bool local_has_breit_wheeler = has_breit_wheeler();
if (local_has_breit_wheeler) {
    evolve_opt = m_shr_p_bw_engine->build_evolve_functor();
    p_optical_depth_BW = pti.GetAttribs("opticalDepthBW").dataPtr() + offset;
}
```

所以 current WarpX 里：

- lepton 的 QED 统计量在 `PhysicalParticleContainer::PushPX()` 内推进；
- photon 的 QED 统计量在 `PhotonParticleContainer::PushPX()` 内推进。

这就解释了为什么上一轮入口笔记里说：

- Quantum Synchrotron 是 `lepton source -> photon product`
- Breit-Wheeler 是 `photon source -> electron/positron products`

因为 source species 自己在日常 push 阶段就已经持有并推进了各自的 optical depth。

## 4. Wrapper 的真正职责：把 PICSAR-QED core 包成 GPU functor，而不是重写物理

`QuantumSyncEngineWrapper.H` 和 `BreitWheelerEngineWrapper.H` 最容易被误解成“WarpX 自己又实现了一遍 QED 公式”。实际上它们的职责更窄：

1. 保存 lookup tables
2. 保存 `chi_min`
3. 把 PICSAR-QED core 包成 WarpX/AMReX 可在 GPU kernel 里调用的 functor

例如 `QuantumSynchrotronEvolveOpticalDepth` 最终调用的是：

```cpp
pxr_qs::evolve_optical_depth(...)
```

`QuantumSynchrotronPhotonEmission` 最终调用的是：

```cpp
pxr_qs::generate_photon_update_momentum(...)
```

`BreitWheelerEvolveOpticalDepth` 最终调用的是：

```cpp
pxr_bw::evolve_optical_depth(...)
```

`BreitWheelerGeneratePairs` 最终调用的是：

```cpp
pxr_bw::generate_breit_wheeler_pairs(...)
```

因此 wrapper 的真实定位是：

- WarpX 负责 gather 场、拿粒子属性、管理 `MultiFab`/SoA/runtime attributes；
- PICSAR-QED core 负责 QED rate / emission / pair generation 的物理采样；
- wrapper 只做中间胶水层。

## 5. Quantum Synchrotron kernel：先 gather 场，再同时改写 source momentum 和 product photon

`PhotonEmissionTransformFunc::operator()` 的结构很干净：

1. 用 `GetParticlePosition` 取 source lepton 位置
2. 先加载 constant external fields
3. 用 `GetExternalEBField` 叠加 embedded-boundary / 粒子侧附加场
4. 用 `doGatherShapeN(...)` 从主网格 gather `E/B`
5. 调用 `m_emission_functor(...)`
6. 把 source optical depth 重新随机初始化

核心代码是：

```cpp
m_emission_functor(
    ux, uy, uz,
    ex, ey, ez,
    bx, by, bz,
    g_ux, g_uy, g_uz,
    engine);

src.m_runtime_rdata[m_opt_depth_runtime_comp][i_src] =
    m_opt_depth_functor(engine);
```

这段有两个关键结论：

1. Quantum Synchrotron 事件发生时，source lepton 的动量会被原地改写；
2. product photon 不是“复制 source 再改字段”，而是直接由 emission functor 写出 `g_ux/g_uy/g_uz`。

所以 Quantum Synchrotron 的一次事件，本质上是：

- source 粒子损失一部分动量；
- photon product 得到对应动量；
- source 的 optical depth 被抽一份新的指数随机数重新开始累计。

## 6. `cleanLowEnergyPhotons()` 说明 Quantum Synchrotron 还有一道后置筛选

`doQedQuantumSync()` 在 `filterCopyTransformParticles` 之后还会调用：

```cpp
cleanLowEnergyPhotons(dst_tile, np_dst, num_added,
                      m_quantum_sync_photon_creation_energy_threshold);
```

`QEDPhotonEmission.H` 里这段逻辑的语义是：

- photon 即便被创建出来，也可能因为能量太低被立即标 invalid；
- 阈值来自 `qed_qs.photon_creation_energy_threshold`；
- 同时还会强制删除极低能 photon，避免数值垃圾。

这意味着 `analysis_quantum_sync.py` 里的最终 photon 数，并不是“所有抽样事件数”，而是“通过能量阈值筛选后留下的 photon 数”。

这也解释了为什么：

- `inputs_test_2d_qed_quantum_sync` 把 `qed_qs.photon_creation_energy_threshold = 0.0`
- 而 `inputs_base_2d_breit_wheeler` 把它设成 `2`

它们想覆盖的是不同的 product-photon 保留边界。

## 7. Breit-Wheeler kernel：source photon 被标 invalid，而不是保留 residual 后再复制

`PairGenerationTransformFunc::operator()` 和 Quantum Synchrotron 的最大区别在 source 处理方式：

```cpp
m_generate_functor(
    ux, uy, uz,
    ex, ey, ez,
    bx, by, bz,
    e_ux, e_uy, e_uz,
    p_ux, p_uy, p_uz,
    engine);

src.m_idcpu[i_src] = amrex::ParticleIdCpus::Invalid;
```

也就是说，事件触发后：

- electron/positron 两个 product 都会被填充动量；
- source photon 不是继续带着“剩余能量”留在容器里；
- 而是直接标记成 invalid，后续由常规清理流程删除。

这就是为什么 `analysis_breit_wheeler_core.py` 里要显式检查：

- 剩余 photons 数量
- 丢失 photons 数量
- generated pairs 数量

因为 current 实现语义是“被触发的 source photon 消失，转化成一对新粒子”。

## 8. 两种 optical-depth functor 的边界不同

虽然两套 wrapper 长得很像，但它们的 cutoff 逻辑并不完全相同。

### 8.1 Quantum Synchrotron

`QuantumSynchrotronEvolveOpticalDepth` 的早退条件只有：

- `chi_part < qs_minimum_chi_part`

### 8.2 Breit-Wheeler

`BreitWheelerEvolveOpticalDepth` 的早退条件有两条：

- `gamma_photon < 2`
- `chi_phot < bw_minimum_chi_phot`

也就是 photon 能量不够生成一对时，WarpX 连 optical depth 都不会继续推进。

这和 Quantum Synchrotron 很不一样，因为后者并不存在“低于对产生阈值就根本不演化”的能量门槛。

## 9. regression 证据和 kernel 细节是如何一一对应的

### 9.1 `analysis_quantum_sync.py`

它检查：

- photon 数
- photon 权重
- photon 发射方向
- photon 能谱
- source/product optical-depth 仍服从指数分布

这正好对应 kernel/wrapper 层的五个点：

1. `evolve_optical_depth` 先把 optical depth 推到触发
2. `PhotonEmissionFilterFunc` 只在 `opticalDepthQSR < 0` 时放行
3. `m_emission_functor` 同时更新 source momentum 和 photon momentum
4. `m_opt_depth_functor(engine)` 重置 source optical depth
5. `cleanLowEnergyPhotons()` 再做 product photon 阈值筛选

### 9.2 `analysis_breit_wheeler_core.py`

它检查：

- pair 数
- 权重继承
- residual photon 动量
- 单事件能量守恒
- 电子/正电子能谱
- photon / electron / positron optical-depth 分布

这对应 kernel 层的关键语义是：

- `PairGenerationFilterFunc` 由 `opticalDepthBW < 0` 触发
- `m_generate_functor` 同时给 electron/positron 生成动量
- source photon 被 `idcpu = Invalid` 删除
- product electron/positron 若再启 QSR，会重新持有 `opticalDepthQSR`

### 9.3 `analysis_schwinger.py`

它不关心上面这些 source/product optical-depth 细节，而是直接对强场率公式做总数窗口验证。说明 Schwinger 的 regression 口径从一开始就是另一类，不应和前两条混写。

## 10. 当前更深一层的边界

读到这里，QED 还剩下几条清晰的下一层工作：

1. `QEDInternals/*.cpp` 里 builtin/load/generate table 的具体参数与序列化边界；
2. `QedChiFunctions.H` 如何定义 lepton/photon 的 `chi`；
3. `PhotonParticleContainer::PushPX()` 与 `PhysicalParticleContainer::PushPX()` 内 `evolve_optical_depth` 的完整 device-lambda 细节；
4. `linear_breit_wheeler` / `linear_compton` 为什么被放进 `CollisionHandler`，以及它和这里的 `ElementaryProcess/QED*` 到底如何分工。

## 11. 本轮结论

QED 的真正 kernel 级合同可以压缩成一句话：

- 平时在 push 中推进 optical depth；
- optical depth 变负时，在单独的 QED event pass 里触发 filter-copy-transform；
- wrapper 只负责把 PICSAR-QED core 包成 WarpX/AMReX GPU functor；
- Quantum Synchrotron 会保留 source lepton 并重置 optical depth；
- Breit-Wheeler 会删除 source photon 并创建一对 product；
- Schwinger 则根本不依赖 source species。

所以下一轮最合理的工作，要么继续下钻 `QEDInternals/*.cpp` 的 table 生成与序列化，要么切回 `BinaryCollision` / `BackgroundMCC` / `PulsedDecay`，把多物理的另一支实现层也补齐。*** End Patch
