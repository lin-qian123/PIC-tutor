# 08 particle class and attribute map：容器层次、编译期 SoA 与运行时属性

绑定源码：

- `../warpx/Source/Particles/WarpXParticleContainer.H`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/PhysicalParticleContainer.cpp`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/Particles/PhotonParticleContainer.H`
- `../warpx/Source/Particles/LaserParticleContainer.H`
- `../warpx/Source/Particles/ParticleCreation/DefaultInitialization.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXImplicitOps.cpp`

前置阅读：

- `../notes/code-reading/initialization/04-particle-creation-kernels.md`
- `../notes/code-reading/particles/00-particle-evolve-callchain.md`
- `../notes/code-reading/particles/04-amr-gather-deposition-buffers.md`

这一篇不再继续往 `gather/deposition` kernel 深钻，而是回到 `Particles/` 顶层，回答三个更基础的问题：

1. WarpX 里到底有哪些粒子容器类，它们之间怎样继承和装配；
2. 哪些属性是编译期固定的，哪些属性是运行时按物理模块动态加上的；
3. `opticalDepthQSR`、`prev_x`、`ionizationLevel`、`x_n/ux_n`、`nsuborbits` 这些名字分别服务哪条算法路径。

## 1. `PIdx` 先定义“每个粒子天生就有的量”

`WarpXParticleContainer.H:55-88` 先定义了 `PIdx`。它不是某个 species 私有的数据表，而是所有粒子容器共享的编译期 SoA 约定：

- 位置：`x/y/z`，不同几何下会变成 `r/z`、`theta`、`phi` 的不同组合；
- 权重：`w`；
- 动量：`ux/uy/uz`，这里存的是 proper velocity `gamma*v`，不是普通速度；
- `nattribs`：当前几何下编译期实数属性个数。

同时 `IntIdx::nattribs` 在 `WarpXParticleContainer.H:92-99` 里是 `0`。这说明 WarpX 的默认设计是：

- 编译期 real SoA 一定存在；
- 编译期 int SoA 默认一个都没有；
- 所有整数标签都走运行时 `AddIntComp()`。

这也是后面 `ionizationLevel`、`nsuborbits` 会显得“后来才长出来”的原因。

## 2. `WarpXParticleContainer` 是统一基类，但不是统一物理模型

`WarpXParticleContainer.H:171-194` 直接把 `WarpXParticleContainer` 定义成所有粒子容器的多态基类。它继承：

`amrex::ParticleContainerPureSoA<PIdx::nattribs, 0, ...>`

含义很明确：

- real SoA 至少有 `PIdx` 这组编译期分量；
- int SoA 初始是 0；
- 允许后续继续添加 runtime real/int comps。

`WarpXParticleContainer.cpp:94-105` 的构造函数又做了三件基础工作：

1. 绑定 AMReX arena；
2. `SetSoACompileTimeNames(...)`，把 `PIdx::names` 真正注册成当前容器的 builtin real names；
3. 调 `ReadParameters()` 读入粒子公共配置。

因此 `WarpXParticleContainer` 提供的是统一的数据骨架和通用操作能力，不是“某种具体粒子”。

## 3. `MultiParticleContainer` 负责装配多 species，而不是把所有粒子都塞进一个大类

`MultiParticleContainer.cpp:96-125` 给出顶层装配逻辑：

- 普通带质量 species 用 `PhysicalParticleContainer`；
- 刚性注入 species 用 `RigidInjectedParticleContainer`；
- 光子 species 用 `PhotonParticleContainer`；
- 激光天线粒子单独用 `LaserParticleContainer`；
- 然后统一保存在 `allcontainers` 里。

这说明 WarpX 的“多 species”不是一个大 switch 到处判断，而是：

- `MultiParticleContainer` 只负责持有和遍历；
- 具体物理差异尽量下推到不同派生容器。

## 4. 四类主要容器的职责边界

按当前源码，顶层可先画成：

```text
MultiParticleContainer
  -> WarpXParticleContainer
       -> PhysicalParticleContainer
            -> PhotonParticleContainer
            -> RigidInjectedParticleContainer
       -> LaserParticleContainer
```

职责边界可以直接从类注释和构造逻辑读出来：

- `WarpXParticleContainer`：所有粒子的公共数据骨架和通用接口；
- `PhysicalParticleContainer`：真正带质量、会 gather/push/deposit 的 plasma species；
- `PhotonParticleContainer`：继承 `PhysicalParticleContainer`，但 `DepositCharge()` 和 `DepositCurrent()` 直接空实现，说明它沿用很多粒子基础设施，但不承担带电沉积责任；见 `PhotonParticleContainer.H:25-115`；
- `LaserParticleContainer`：直接继承 `WarpXParticleContainer`，因为它只需要“人工天线粒子沉积电流”，不需要普通 `FieldGather`；见 `LaserParticleContainer.H:30-61`。

这里最值得注意的是：

- photon 不是从零写一套，而是复用 physical container 的很多上层逻辑；
- laser 反而绕开 `PhysicalParticleContainer`，因为它根本不是“真实受 Lorentz 力推进的带质量 species”。

## 5. `PhysicalParticleContainer` 构造函数就是 runtime attribute 的第一层注册中心

`PhysicalParticleContainer::PhysicalParticleContainer()` 的前半段先解决 species 的物理身份：

- `injection_style` / `injection_sources` 决定是否创建 `PlasmaInjector`；
- `species_type`、`charge`、`mass` 共同决定真实物种和荷质参数；
- 然后再打开 splitting、self-fields、ionization、resampling、radiation reaction、QED 等模块。

真正和属性系统直接相关的是后半段，`PhysicalParticleContainer.cpp:255-331` 做了第一轮 runtime attribute 注册：

- `do_qed_quantum_sync` 时加 `opticalDepthQSR`；
- `do_qed_breit_wheeler` 时加 `opticalDepthBW`；
- `addIntegerAttributes` 为用户自定义整数属性逐个 `AddIntComp(...)`；
- `addRealAttributes` 为用户自定义实数属性逐个 `AddRealComp(...)`；
- `save_previous_position` 时加 `prev_x/prev_y/prev_z`。

也就是说，species 构造期加进去的 runtime attribute 基本都属于“长期存在的物理属性”，而不是一步临时缓存。

## 6. `opticalDepthQSR` 和 `opticalDepthBW` 是 QED 过程状态，不是普通诊断量

`PhysicalParticleContainer.cpp:255-264` 表明：

- `opticalDepthQSR` 跟着 quantum synchrotron 开关走；
- `opticalDepthBW` 跟着 Breit-Wheeler 开关走。

它们的默认初始化不在 species 构造函数里手写，而是交给
`PhysicalParticleContainer::DefaultInitializeRuntimeAttributes()`，再转给
`ParticleCreation::DefaultInitializeRuntimeAttributes()`；见 `PhysicalParticleContainer.cpp:436-449`。

`DefaultInitialization.H:152-209` 里对这两个量的处理是：

- 运行时逐分量检查名字；
- 若命中 `opticalDepthQSR` 或 `opticalDepthBW`；
- 就调用对应 QED engine 的 `build_optical_depth_functor()`；
- 用 RNG 从指数分布抽样初值。

因此这两项不是“默认零值标签”，而是新粒子生成时就有物理概率意义的随机状态量。

## 7. `prev_x/prev_y/prev_z` 是历史位置缓存，用于“保存上一位置”路径

`PhysicalParticleContainer.cpp:316-331` 表明：

- `save_previous_position` 开启后才会加 `prev_*`；
- 这组属性在 3D/XZ/1D 风格几何下按已有坐标维度加入；
- RZ/RCYLINDER/RSPHERE 目前直接 abort，说明这条路径还没做完非笛卡尔支持。

这组量的角色和 `x_n` 不同：

- `prev_*` 是某些显式粒子路径要额外保留的历史位置；
- `x_n` 是 implicit solver 专门在时间步开始时快照下来的“本步起点位置”。

两者都像“旧位置”，但属于不同算法层。

## 8. `ionizationLevel` 不是默认属性，而是在启用电离模块时补注册

`PhysicalParticleContainer::InitIonizationModule()` 在 `PhysicalParticleContainer.cpp:1592-1595` 里明确写了：

```cpp
if (!HasiAttrib("ionizationLevel")) {
    AddIntComp("ionizationLevel");
}
```

所以 `ionizationLevel` 的语义是：

- 只有源 species 真正走 field ionization 时才需要；
- 它是 runtime int attribute，不是 builtin；
- 注册时机会比构造函数更晚，在 ionization module 初始化阶段。

`DefaultInitialization.H:244-260` 又说明它的默认值不是任意整数，而是统一初始化为
`ionization_initial_level`。

因此这项不是“诊断性标签”，而是后续 effective charge、ADK/OTB 电离状态演化的核心状态量。

## 9. `AddNParticles()` 只填用户显式给出的属性，其余交给统一默认初始化

`WarpXParticleContainer.cpp:262-330` 给了 runtime attribute 落地的关键接口：

1. 先把 builtin `x/y/z/w/ux/uy/uz/...` 推进 `pinned_tile`；
2. 再把 `attr_real` 里用户显式提供的 `nattr_real-1` 个 runtime real 填进去；
3. 再把 `attr_int` 里用户显式提供的 runtime int 填进去；
4. 最后调用 `DefaultInitializeRuntimeAttributes(...)` 补其余还没给值的 runtime attrs。

这意味着 WarpX 的策略不是“所有属性都要求调用者显式给全”，而是：

- 外部输入只负责自己知道的那部分；
- 其余由容器根据属性名和当前物理模块自动补默认值。

这也是为什么同一个 `AddParticles()` 路径能同时兼容：

- 普通 species；
- 带 QED optical depth 的 species；
- 带 ionizationLevel 的 species；
- 带用户 parser attribute 的 species。

## 10. 用户自定义 runtime attributes 是 parser 驱动的，而不是硬编码扩展

`PhysicalParticleContainer.cpp:286-314` 和 `DefaultInitialization.H:212-241` 给出用户属性的完整机制：

- 输入文件用 `addRealAttributes` / `addIntegerAttributes` 列出名字；
- 每个属性都可以绑定 `attribute.<name>(x,y,z,ux,uy,uz,t)` parser；
- 初始化时按粒子当前位置、动量和当前时间执行 parser；
- 结果写入对应 runtime attr。

所以 WarpX 这里提供的不是“几个固定扩展槽位”，而是一套：

- 名字注册；
- parser 编译；
- GPU/CPU 双栈执行；
- 初始化自动落盘

的通用运行时属性机制。

## 11. `x_n/ux_n` 与 `nsuborbits` 是 implicit solver 运行时临时属性

这组属性不在 `PhysicalParticleContainer` 构造函数里注册，而是在
`ImplicitSolver::CreateParticleAttributes()` 里统一加入；见 `ImplicitSolver.cpp:10-34`。

规则是：

- `x_n/y_n/z_n`：保存时间步开始时的粒子位置；
- `ux_n/uy_n/uz_n`：保存时间步开始时的动量；
- `nsuborbits`：只有开启 particle suborbits 时才加；
- 所有这些属性都用 `comm = 0` 注册，所以不会参与通信，也不会写入 checkpoint。

`WarpX::SaveParticlesAtImplicitStepStart()` 在 `WarpXImplicitOps.cpp:133-207` 里把这组量真正填值：

- 逐粒子把当前位置写进 `x_n/y_n/z_n`；
- 把当前动量写进 `ux_n/uy_n/uz_n`；
- 若存在 `nsuborbits`，就先设成 `1`。

因此这组量的本质不是“species 的持久物理属性”，而是 implicit 时间推进器为当前 step 临时开的一组状态快照。

## 12. `nsuborbits` 不是单纯计数器，而是 implicit fallback 的轨道细分状态

虽然本篇不展开 `ImplicitPushPX.cpp` 的全部细节，但从属性注册和保存入口已经能看出：

- 它只在 implicit + particle suborbits 路径出现；
- 初值统一设成 `1`；
- 后续 implicit push 失败或需要更细子步时再逐粒子增大。

所以 `nsuborbits` 不是普通 diagnostics 整数，而是 implicit solver 的局部自适应轨道分裂状态。

## 13. `*_btd` 是另一组“只在特定后处理打开时才出现”的临时属性

`MultiParticleContainer::SetDoBackTransformedParticles(...)` 在
`MultiParticleContainer.cpp:1018-1045` 里，如果某个 species 首次启用 back-transformed particles，就会加：

- `x_n_btd/y_n_btd/z_n_btd`
- `ux_n_btd/uy_n_btd/uz_n_btd`

而且同样是 `comm = 0`。

这说明 WarpX 里至少有三类 runtime attribute：

1. species 长期物理属性：如 `opticalDepthQSR`、`opticalDepthBW`、`ionizationLevel`；
2. 用户自定义属性：parser 驱动；
3. 算法临时缓存：如 `x_n/ux_n/nsuborbits`、`*_btd`。

## 14. Laser 容器故意不走这套默认初始化

`LaserParticleContainer.H:55-61` 直接把 `DefaultInitializeRuntimeAttributes()` 写成空实现。

这很关键，因为它说明：

- runtime attribute 初始化框架并不是强制所有派生类都一样；
- laser 天线粒子的状态由其专门初始化逻辑控制；
- 它不需要像 plasma species 那样自动补 QED、ionization、用户 parser 这类属性。

换句话说，`PhysicalParticleContainer` 的属性语义和 `LaserParticleContainer` 的属性语义并不相同。

## 15. 当前可以把粒子属性系统总结成一张表

| 类别 | 例子 | 注册时机 | 是否持久物理状态 |
|---|---|---|---|
| 编译期 builtin real | `x,y,z,w,ux,uy,uz,theta,phi` | `PIdx` 编译期定义 | 是 |
| 构造期 runtime real | `opticalDepthQSR`, `opticalDepthBW`, `prev_x` | `PhysicalParticleContainer` 构造函数 | 通常是 |
| 构造期 runtime int | 用户 `addIntegerAttributes` | `PhysicalParticleContainer` 构造函数 | 取决于用户 |
| 模块初始化期 runtime int | `ionizationLevel` | `InitIonizationModule()` | 是 |
| implicit 临时 real | `x_n`, `ux_n` 等 | `ImplicitSolver::CreateParticleAttributes()` | 否 |
| implicit 临时 int | `nsuborbits` | `ImplicitSolver::CreateParticleAttributes()` | 否 |
| back-transform 临时 real | `x_n_btd`, `ux_n_btd` 等 | `SetDoBackTransformedParticles()` | 否 |

## 16. 对后续阅读的直接影响

这张属性图会直接决定后面几条源码主线该怎么看：

- 读 `PushPX()`、`DepositCurrent()`、`ImplicitPushPX.cpp` 时，必须先分清 `ux` 和 `ux_n`；
- 读 ionization、电离产物复制和 effective charge 时，必须盯住 `ionizationLevel`；
- 读 QED photon emission / pair generation 时，必须盯住 `opticalDepthQSR/BW`；
- 读 particle boundary buffer、sorting、checkpoint/restart 时，必须分清哪些 runtime attrs 会通信/写盘，哪些只是 `comm = 0` 的局部临时缓存。

所以这一层虽然不像 deposition kernel 那样“算公式”，但它决定了后续所有粒子算法到底在读写哪一类状态。
