# 09 radiation reaction, implicit and photon pushers：属性缓存如何进入非标准推进路径

绑定源码：

- `../warpx/Source/Particles/Pusher/PushSelector.H`
- `../warpx/Source/Particles/Pusher/UpdateMomentumBorisWithRadiationReaction.H`
- `../warpx/Source/Particles/Pusher/ImplicitPushPX.cpp`
- `../warpx/Source/Particles/PhotonParticleContainer.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXImplicitOps.cpp`

前置阅读：

- `../notes/code-reading/particles/03-vay-higuera-cary-pushers.md`
- `../notes/code-reading/particles/08-particle-class-and-attribute-map.md`

上一篇已经把 `x_n/ux_n/nsuborbits`、`opticalDepthQSR/BW`、`ionizationLevel` 这些属性的注册语义理清了。这一篇继续回答：这些属性在非标准粒子推进路径里究竟怎么被消费。

这里把三条容易被混在一起的支线拆开：

1. classical radiation reaction 只是 Boris 的一个修正尾项；
2. implicit push 不是普通 `PushPX()` 的小改版，而是整个时间层和收敛逻辑都变了；
3. photon push 复用 `PhysicalParticleContainer::Evolve()` 的大框架，但 deliberately 不做带电沉积。

## 1. `PushSelector` 先定义了三条动量推进分支的总分派

`PushSelector.H:39-104` 的 `doParticleMomentumPush()` 是所有单粒子 momentum update 的统一分派点：

- 先把 species charge 乘 `ion_lev`，得到粒子的有效电荷 `qp`；
- 如果 `do_crr` 为真，优先走 classical radiation reaction 分支；
- 否则才按 `ParticlePusherAlgo` 分到 Boris、Vay、Higuera-Cary。

也就是说，在 WarpX 当前结构里：

- radiation reaction 不是第四种独立 pusher；
- 它是“Boris + RR correction”；
- 一旦打开 `do_crr`，Vay 和 Higuera-Cary 这两条路径都不会再被使用。

这和 `PhysicalParticleContainer` 构造函数中的约束是一致的：`do_classical_radiation_reaction` 只允许 lepton species，并且只允许 Boris pusher。

## 2. classical radiation reaction 路径本质是“先 Boris，再加 Landau-Lifshitz 型阻尼力”

`UpdateMomentumBorisWithRadiationReaction.H:21-90` 的结构非常直接：

1. 保存旧动量 `ux_old/uy_old/uz_old`；
2. 先调用普通 `UpdateMomentumBoris(...)`；
3. 再用新旧半步动量的平均构造中间时刻量；
4. 计算 RR force；
5. 最后再把这股附加力乘 `dt` 加到动量上。

核心源码骨架是：

```cpp
UpdateMomentumBoris(...);

const amrex::ParticleReal ux_n = (ux+ux_old)*0.5_prt;
...
const amrex::ParticleReal gamma_n = std::sqrt(1._prt + (ux_n*ux_n + ...)*inv_c2);
...
const amrex::ParticleReal flx_q = (Ex + vy_n*Bz - vz_n*By);
...
const amrex::ParticleReal RRcoeff = (2.0_prt/3.0_prt)*PhysConst::r_e*q_over_mc*q_over_mc;
...
ux += frx*dt_multiplier*dt;
uy += fry*dt_multiplier*dt;
uz += frz*dt_multiplier*dt;
```

这里最关键的实现判断是：

- RR 并不替换 Boris 旋转；
- 它把 Boris 产生的动量当作主更新；
- 再用中间时刻的 \(\gamma_n\)、\(\mathbf{v}_n\)、Lorentz force 和 \( \mathbf{\beta}\cdot\mathbf{E} \) 构造阻尼修正。

因此从代码结构看，WarpX 的 classical radiation reaction 路径是“operator correction”风格，而不是从头重写一套相对论推进器。

## 3. QED quantum synchrotron 打开时，RR 还会先看 `chi`

`PushSelector.H:64-88` 还有一层只有在 `WARPX_QED` 下才出现的逻辑：

- 如果模板参数 `do_sync` 为真；
- 就先用 `QedUtils::chi_ele_pos(...)` 算粒子当前 `chi`；
- 若 `chi < t_chi_max`，才走 classical RR；
- 否则退回普通 Boris。

这意味着 WarpX 在“同时启用 QED synchrotron 和 classical RR”时，不是简单叠加两套辐射模型，而是：

- 低 `chi` 区域用 classical RR 近似；
- 高 `chi` 区域交给 QED 路径处理。

所以 `do_crr` 在这里只是一种带阈值切换的近经典近似，不是对所有粒子无条件生效。

## 4. 显式 `PushPX()` 里的 RR 路径只是就地替换动量更新器

`PhysicalParticleContainer.cpp:1288-1313` 给出显式 `PushPX()` 中 RR 的真正落点：

```cpp
if (do_crr) {
    amrex::ParticleReal qp = q;
    if (ion_lev) { qp *= ion_lev[ip]; }
    UpdateMomentumBorisWithRadiationReaction(...);
} else if (pusher_algo == ParticlePusherAlgo::Boris) {
    UpdateMomentumBoris(...);
} else if (pusher_algo == ParticlePusherAlgo::Vay) {
    UpdateMomentumVay(...);
} else if (pusher_algo == ParticlePusherAlgo::HigueraCary) {
    UpdateMomentumHigueraCary(...);
}
```

这说明在显式主线里：

- gather、外场叠加、QED optical depth 更新、位置推进这些外壳都不变；
- RR 只是在“单粒子 momentum push 这一小块”替换具体 kernel。

所以从软件结构看，RR 是 `PushPX()` 内部最局部的一层变体。

## 5. implicit push 的第一性变化不在 pusher 公式，而在时间层和收敛循环

`ImplicitPushPX.cpp:369-378` 的注释已经把它和普通 `PushPX()` 的差异点说得很清楚：

- 先 position push 半步；
- 再 gather fields；
- 再 velocity push 一整步；
- 再把 old/new velocity 平均成 time-centered 量；
- 最终位置和速度都停在 half time level；
- 位置和速度互相依赖，因此要做迭代直到一致。

这不是把显式 `PushPX()` 换成另一个 `UpdateMomentum*()` 就能得到的；implicit 路径从时间层定义开始就不同。

## 6. `x_n/ux_n` 在 implicit 路径里不是辅助记录，而是主未知量的锚点

`ImplicitPushXP()` 在 `ImplicitPushPX.cpp:495-507` 先把：

- `x_n/y_n/z_n`
- `ux_n/uy_n/uz_n`

取出来，并直接注释为“the positions and velocities saved at the start of the step”。

随后粒子初值不是从当前 `xp`、`ux` 推进，而是明确从：

```cpp
amrex::ParticleReal xp = x_n[ip];
const amrex::ParticleReal xp_n = x_n[ip];
...
ux[ip] = uxp_n;
```

开始。也就是说，implicit kernel 真正把 `*_n` 看成当前 nonlinear solve 的参考态，而不是普通历史诊断量。

## 7. `PushXPSingleStep()` 是 implicit 单 substep 的核心 fixed-point kernel

`PushXPSingleStep()` 在 `ImplicitPushPX.cpp:53-258` 里实现的其实就是单个粒子的一次 Picard 固定点迭代：

1. 用旧的 time-centered velocity 先给位置一个初猜；
2. 在新位置 gather 场；
3. 把动量先重置回 step start 的 `uxp_n/uyp_n/uzp_n`；
4. 调 `doParticleMomentumPush(...)` 做 full momentum push；
5. 再把 old/new velocity 取平均，得到 time-centered velocity；
6. 用它更新位置；
7. 比较前后两次位置改变量的 step norm，决定是否收敛。

这段代码最关键的实现事实是：

- implicit 路径仍然复用了 `doParticleMomentumPush()`；
- 也就是说 Boris / RR / QED 等单粒子动量物理仍然在里面；
- 但它们被放进了“位置和速度自洽求解”的外循环中。

因此 implicit 粒子推进不是另一个完全独立的物理模型，而是把现有 momentum pusher 嵌入自洽 fixed-point 框架。

## 8. `nsuborbits` 是 implicit 不收敛时的 fallback 机制，而不是一开始就固定分裂

`ImplicitPushXP()` 在 `ImplicitPushPX.cpp:555-667` 中的主循环里，如果某个粒子没收敛：

```cpp
if (nsuborbits) {
    nsuborbits[ip] = 2;
}
...
SetupSuborbitParticles(...)
```

前面 `FindSuborbitParticles()` / `SetupSuborbitParticles()` 又会：

- 找出 `nsuborbits > 1` 的粒子；
- 保存它们的 index；
- 暂存它们的权重；
- 把原权重设成 0，避免它们当前轮错误贡献电流。

所以 `nsuborbits` 的真实语义不是“这类粒子天然要分裂成若干轨道”，而是：

- 默认每个粒子都是 1 条完整轨道；
- 只有 Picard 不收敛，才临时升级为 suborbit 粒子；
- 然后进入专门的补救推进和沉积路径。

## 9. suborbit 路径不是简单重复推进，而是强制切到 Villasenor current deposition

`ImplicitPushXPSubOrbits()` 在 `ImplicitPushPX.cpp:734-738` 明确写了：

```cpp
const auto depos_type = CurrentDepositionAlgo::Villasenor;
```

注释直接解释原因：

- suborbit 只支持 Villasenor current deposition；
- 为了保持能量守恒，gather 也必须匹配这个沉积方式。

因此这里不是“保留用户原来选的 deposition algo 再拆分轨道”，而是：

- 一旦进入 suborbit fallback；
- current deposition 算法就被强制替换成 Villasenor。

这说明 `nsuborbits` 背后不仅是时间步细分，还连带改变了当前粒子的沉积数学。

## 10. suborbit 路径对收敛与沉积做了两阶段处理

`ImplicitPushXPSubOrbits()` 的主 while-loop 在 `ImplicitPushPX.cpp:988-1170` 里还有一个容易忽视的结构：

- nonlinear stage 先只做 push，不立即沉积；
- 如果所有 suborbits 都收敛，再把 `doing_deposition` 切成 true；
- 然后从 `xp_n0/uxp_n0` 再跑一遍，把沉积真正做出来。

也就是说，这里不是“边试收敛边顺手沉积”，而是：

1. 先确认本次 suborbit 划分能否收敛；
2. 收敛后再从 step start 重新执行一次、得到一致的沉积。

这是为了避免不收敛试探轨道污染当前步源项。

## 11. photon push 复用了物理粒子的外壳，但去掉了带电沉积

`PhotonParticleContainer::Evolve()` 在 `PhotonParticleContainer.cpp:242-255` 并没有重写整个 species 循环，而是直接调用：

```cpp
PhysicalParticleContainer::Evolve(..., nullptr);
```

因此 photon container 仍然复用了：

- 多 tile 循环；
- gather / push 的大框架；
- AMR buffer 分区等外层机制。

但它通过两个地方改变物理语义：

1. `PhotonParticleContainer.H` 中 `DepositCharge()` 和 `DepositCurrent()` 都是空实现；
2. `PhotonParticleContainer::PushPX()` 重写了单粒子推进逻辑。

所以 photon path 的关键不是“自己再写一套 Evolve”，而是“只替换内层 push 和沉积语义”。

## 12. photon `PushPX()` 仍然 gather `E/B`，但不做带质量 momentum push

`PhotonParticleContainer.cpp:83-239` 的 `PushPX()` 结构是：

- 先 gather `E/B`；
- 可选叠加 external EB fields；
- 若启用 Breit-Wheeler，就先更新 `opticalDepthBW`；
- 然后只在 `position_push_type == Full` 时调用 `UpdatePosition(x,y,z,ux,uy,uz,dt,mass)`。

最关键的是，这里根本没有 `UpdateMomentumBoris/Vay/HigueraCary` 这一层。

也就是说 photon 当前实现假定：

- `ux/uy/uz` 表示光子传播方向和频率相关的无质量动量状态；
- 场不会像带电粒子那样直接推动其动量；
- photon 的主要多物理演化体现在 QED optical depth，而不是 Lorentz-force momentum rotation。

所以 photon path 和普通 charged species 的本质区别，不只是“不沉积 charge/current”，而是连 momentum update 的物理机制都不同。

## 13. photon path 也消费 runtime attributes，但消费的是另一组

在这一条线上真正重要的属性是：

- `opticalDepthBW`：Breit-Wheeler 过程状态；
- `*_btd`：若启用 back-transformed particles，则也会复制旧态；
- builtin `ux/uy/uz`：用于无质量位置推进。

而 photon path 不会用到：

- `ionizationLevel`
- `opticalDepthQSR`
- `x_n/ux_n/nsuborbits`

这正好说明上一篇属性地图的意义：同样叫 `PushPX()`，不同派生容器消费的 runtime attrs 完全不同。

## 14. 这一层和后续任务的关系

现在粒子推进这条线已经分成三层：

1. 显式标准路径：Boris / Vay / Higuera-Cary；
2. 显式变体：classical radiation reaction，是 Boris 后附加阻尼力；
3. 非标准路径：implicit fixed-point / suborbit fallback / photon push。

这三层共用的基础设施是：

- `doParticleMomentumPush()` 分派；
- gather 外壳；
- `PhysicalParticleContainer::Evolve()` 的 tile loop；
- 上一篇整理过的 runtime attributes。

而真正分叉的地方是：

- 是否需要 `x_n/ux_n/nsuborbits`；
- 是否需要 `opticalDepthQSR/BW`；
- 是否保留 charged current deposition；
- 是否必须强制切换 deposition algo。

因此下一步继续读 collision、ionization、QED internals 时，应该始终先问一句：当前路径到底在消费哪一组粒子属性，以及它是否还沿用普通 charged-species 的 push/deposition 假设。

## 15. `radiation_reaction` regression：当前本地对 classical RR 最直接的强基准

`Examples/Tests/radiation_reaction/` 不应再留在 `general / to classify`。它正好对应这一篇讨论的 RR 分支：

- `do_classical_radiation_reaction = 1`
- 常量外磁场
- `SingleParticle`

analysis 脚本把 5 个 lepton case 分成两类：

1. 初始动量平行于磁场：
   - 末态 `gamma` 应保持不变；
2. 初始动量垂直于磁场：
   - 末态 `gamma(t)` 应满足解析 Landau-Lifshitz 衰减公式；

并统一要求相对误差低于 `5%`。

因此这组 regression 的真实意义是：

1. 它直接验证 `UpdateMomentumBorisWithRadiationReaction()` 这条 Boris+RR 修正路径；
2. 它同时覆盖 electron 和 positron，不把电荷符号差异留给隐式假设；
3. 它是当前本地 checkout 中 classical radiation reaction 最直接的 example-level 强 analysis。
