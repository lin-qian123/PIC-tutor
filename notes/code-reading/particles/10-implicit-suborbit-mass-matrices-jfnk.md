# 10 implicit suborbit mass matrices and JFNK：`current_fp_non_suborbit`、`MassMatrices_PC` 与两阶段重沉积

绑定源码：

- `../warpx/Source/Particles/Pusher/ImplicitPushPX.cpp`
- `../warpx/Source/Particles/WarpXParticleContainer.cpp`
- `../warpx/Source/Particles/Deposition/MassMatricesDeposition.H`
- `../warpx/Source/Particles/MultiParticleContainer.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`

前置阅读：

- `../notes/code-reading/particles/08-particle-class-and-attribute-map.md`
- `../notes/code-reading/particles/09-radiation-reaction-implicit-photon-pushers.md`

上一篇已经把 implicit push 的主流程、`x_n/ux_n/nsuborbits` 的角色，以及 suborbit fallback 的基本结构讲清了。这一篇继续往下补两个更深的数值层面：

1. mass matrices、`current_fp_non_suborbit` 和 JFNK linear stage 之间到底怎样分工；
2. suborbit 粒子为什么要单独存索引、清权重、重跑沉积，以及它和 preconditioner 用的 `MassMatrices_PC` 有什么关系。

## 1. `MultiParticleContainer::Evolve()` 先决定本步到底要清哪些 implicit 辅助场

`MultiParticleContainer.cpp:479-516` 在进入各 species 之前，不只是清零普通 `current_fp/current_buf/rho_fp/rho_buf`，还按 `implicit_options` 的状态决定另外两组量：

- `current_fp_non_suborbit`
- `MassMatrices_PC`

源码里的两个布尔量很关键：

```cpp
const bool zero_current_fp_non_suborbit =
    !(implicit_options->use_mass_matrices_jacobian &&
      implicit_options->linear_stage_of_jfnk);

const bool zero_mass_matrices_pc =
    implicit_options->use_mass_matrices_pc &&
    !implicit_options->linear_stage_of_jfnk;
```

这里已经暴露出 WarpX 对 implicit 电流的分拆思路：

- 非 suborbit 粒子的“基准电流”单独放在 `current_fp_non_suborbit`；
- suborbit 粒子在某些阶段不会重新贡献这部分；
- preconditioner 专用的质量矩阵 `MassMatrices_PC` 也不是每次都重置。

也就是说，implicit 粒子推进并不是“把所有电流都重新沉一遍”那么简单，而是把不同来源的响应分拆保存。

## 2. `ImplicitSolver::CumulateJ()` 给出了这组分拆的物理含义

`ImplicitSolver.cpp:108-125` 直接写明了：

```cpp
J(E=E0+dE) = J_suborbit + J0 + MM*(E - E0)
```

这里三个量分别对应：

- `J_suborbit`：需要 suborbit 的粒子贡献；
- `J0`：包含在 mass matrices 近似里的普通粒子在 `E0` 上的基准电流；
- `MM*(E-E0)`：质量矩阵给出的线性化电流修正。

对应的场容器也很清楚：

- `J_suborbit` 走 `current_fp`；
- `J0` 走 `current_fp_non_suborbit`；
- `MM` 走 `MassMatrices_X/Y/Z` 或 `MassMatrices_PC`。

`CumulateJ()` 做的事情就是把 `J0` 加回 `current_fp`。因此：

- `current_fp` 并不总是“所有粒子一步直接沉出来的完整电流”；
- 在 implicit / JFNK 路径里，它更像是一个最终拼装容器。

## 3. 普通质量矩阵沉积默认跳过 suborbit 粒子

`MassMatricesDeposition.H:486-576` 的 `doDirectSigmaDeposition()` 和
`MassMatricesDeposition.H:1603+` 的 `doVillasenorSigmaDeposition()` 都有同一个保护：

```cpp
if (nsuborbits && nsuborbits[ip] > 1) { return; }
```

这条规则非常关键。它说明普通的 mass matrix deposition 假设：

- 粒子本步可以用一条正常 implicit 轨道近似；
- 这些粒子的线性响应能安全进入 `MM`。

一旦粒子被标成 suborbit，WarpX 就不再把它视为“可以被这套线性近似覆盖的普通粒子”，而是把它从 mass matrices 近似里剔除出来。

因此 `nsuborbits` 不只改变 push 和 current deposition，还会改变粒子是否属于 `MM` 近似的建模对象。

## 4. `WarpXParticleContainer::DepositMassMatrices()` 还限制了可用沉积算法和网格类型

`WarpXParticleContainer.cpp:1133-1141` 直接 abort 的几种组合是：

- 质量矩阵不能和 Esirkepov 一起用；
- 质量矩阵不能和 Vay deposition 一起用；
- 质量矩阵不能和 collocated grid 一起用；
- implicit 路径也不能用 shared-memory current deposition。

这几条限制说明 WarpX 当前 mass-matrix 线性化是围绕：

- Direct / Villasenor 风格沉积；
- staggered current grids；
- 非 shared-memory kernel

这组实现假设写出来的，而不是所有 deposition/grid 组合的通用层。

## 5. `DepositMassMatrices()` 对 Villasenor 和 Direct 分别走不同 kernel

`WarpXParticleContainer.cpp:1183-1365` 的分派把质量矩阵沉积分成两大类：

- Villasenor：调用 `doVillasenorSigmaDeposition<order, full_mass_matrices>`；
- Direct：调用 `doDirectSigmaDeposition<order, full_mass_matrices>`。

这和普通 current deposition 的思路一致，但这里真正输出的不是 `J` 本身，而是：

- `Sxx/Sxy/Sxz`
- `Syx/Syy/Syz`
- `Szx/Szy/Szz`

这些是 \(dJ/dE\) 的离散近似容器。

所以从软件结构看，WarpX 把质量矩阵沉积也当成了“与 current deposition 并行的一套粒子到网格映射”，只是输出量从 `J` 换成了线性响应核。

## 6. `ImplicitPushXPSubOrbits()` 里 `deposit_mass_matrices` 只服务 preconditioner，不服务 Jacobian

`ImplicitPushPX.cpp:816-839` 定义了：

```cpp
const bool use_mass_matrices_pc = implicit_options->use_mass_matrices_pc;
const bool linear_stage_of_jfnk = implicit_options->linear_stage_of_jfnk;
const bool deposit_mass_matrices = use_mass_matrices_pc && !linear_stage_of_jfnk;
```

随后的注释也说得很直白：

- suborbit 粒子的 mass matrices deposit 只给 preconditioner 用；
- 不是给 Jacobian calculation 用。

这意味着 WarpX 在这里做了一个很务实的切分：

- 对普通粒子，Jacobain 可用 `MM` 线性化；
- 对麻烦的 suborbit 粒子，不把它们并进 Jacobian 的 `MM` 里；
- 但如果 preconditioner 需要，也允许把 suborbit 粒子的某种近似响应沉到 `MassMatrices_PC`。

所以 `MassMatrices_PC` 和主 Jacobian 用的 `MassMatrices_X/Y/Z` 在语义上并不完全等价。

## 7. suborbit 粒子在 nonlinear stage 和 linear stage 的策略不同

`ImplicitPushXPSubOrbits()` 里有一句非常关键：

```cpp
bool doing_deposition = linear_stage_of_jfnk;
```

这意味着：

- nonlinear stage：先只验证各 suborbit 是否收敛，不立刻沉积；
- linear stage of JFNK：一开始就处在 deposition 模式，因为 suborbit 数不能再改。

随后又有：

```cpp
if (linear_stage_of_jfnk) { convergence = true; }
```

再配合上面的 `iter_buffer = linear_stage_of_jfnk ? 10 : 0`，就能看出两阶段的数值哲学：

- nonlinear stage 允许动态增加 `nsuborbits`，追求“真收敛”；
- linear stage 不允许改变轨道划分，否则 GMRES/JFNK 线性化会失去一致性；
- 为了降低线性阶段失败概率，只能多给一点迭代余量。

所以 `linear_stage_of_jfnk` 不是一个普通日志标志，而是直接改写了粒子推进算法的容错策略。

## 8. suborbit 重跑沉积的真正原因是“先找稳定轨道，再产出可信源项”

在 `ImplicitPushXPSubOrbits()` 主循环里，如果还没开始沉积，且本轮所有 suborbits 都收敛，就会：

```cpp
doing_deposition = true;
isuborbit = 0;
xp_n = xp_n0; ... uxp_n = uxp_n0; ...
```

也就是把整个粒子状态重置回 full-step 起点，然后再跑一遍。

这个结构说明 WarpX 显式区分了两类任务：

1. 寻找一个足够稳定的 suborbit 划分和轨道推进结果；
2. 在该划分固定后，重新生成 current / mass-matrix 源项。

如果不这样做，试探性的不收敛轨道就会把污染过的源项写进网格。

## 9. suborbit 的 current deposition 和 mass-matrix deposition共享同一个几何外壳

`ImplicitPushXPSubOrbits()` 在真正沉积时先统一构造：

- `xp_np1 = 2*xp - xp_n`
- `gaminv = GetImplicitGammaInverse(...)`
- `wq_invvol` 或 `wq_n`
- `dt_suborbit`
- `dinv`、`xyzmin`、`domain_double`、`do_cropping`

然后根据 `deposit_mass_matrices` 分叉：

- 若为真：调用 `doVillasenorJandSigmaDepositionKernel<..., deposit_J=true>`；
- 若为假：调用 `VillasenorDepositionShapeNKernel<...>`。

这说明 suborbit 路径不是把 current 和 mass matrices 完全分开算两次几何，而是复用同一条：

- suborbit 轨道
- Villasenor crossing 几何
- 中点速度 / `gaminv`

只是在输出层选择：

- `J` only
- `J + S`

## 10. `MassMatrices_PC` 当前只真正使用对角部分

`ImplicitPushPX.cpp:821-839` 的注释指出：

- suborbit 粒子的 mass matrices deposit 目前只给 preconditioner 用；
- preconditioner 当前只成熟支持 diagonal elements；
- 其它 off-diagonal 容器虽然还要传入接口，但并不会成为 PC 的真正最终依赖。

这说明当前 `MassMatrices_PC` 不是“完整三维耦合电流响应矩阵”的最终实现，而更像是：

- 先把接口和部分存储对齐好；
- 当前只稳定消费 diagonal preconditioner 所需的那部分。

因此书稿里不能把它表述成“WarpX 已经完全实现了 full suborbit mass-matrix PC”。

## 11. unconverged 粒子的权重清零，不只是避免双计数，也是为了隔离 Jacobian/PC 语义

`SetupSuborbitParticles()` 在 `ImplicitPushPX.cpp:343-361` 做的动作是：

- 记录 `unconverged_i[x] = ip + offset`
- 保存 `saved_w[x] = w[ip]`
- 然后 `w[ip] = 0`

这当然能避免这些粒子在普通 current deposition 路径里继续贡献电流，但更深一层的意义是：

- 它把“普通可线性化粒子”和“需要特殊 suborbit 处理的粒子”在源项层彻底隔离；
- 这样 `current_fp_non_suborbit`、`MM`、`MassMatrices_PC`、suborbit `J` 才能各司其职。

所以这里不是简单的去重技巧，而是 implicit 源项分拆的关键数据隔离步骤。

## 12. linear stage of JFNK 下，suborbit 电流是唯一直接推进得到的那部分

把前面的逻辑拼起来，JFNK linear stage 的图像就清晰了：

- 普通粒子不重新做完整 nonlinear 推进；
- 它们的基准电流存在 `current_fp_non_suborbit = J0`；
- 它们的线性响应通过 `MM*(E-E0)` 提供；
- 只有 suborbit 粒子继续显式推进，并把结果直接沉到 `current_fp`。

这正是 `ImplicitSolver::CumulateJ()` 里

$$
J(E)=J_{\text{suborbit}} + J_0 + MM(E-E_0)
$$

在代码中的真正分工落点。

## 13. 对后续阅读的直接影响

这篇补完之后，implicit 粒子推进这条线已经可以拆成四层：

1. 属性层：`x_n/ux_n/nsuborbits`
2. nonlinear fixed-point 层：`PushXPSingleStep()`
3. fallback 层：suborbit 粒子筛选、清权重、单独推进
4. 线性化层：`current_fp_non_suborbit`、`MM`、`MassMatrices_PC`、JFNK / PC 分工

因此后面再读：

- `ImplicitSolver::ComputeJfromMassMatrices()`
- `PrepareForLinearSolve()`
- `ScaleMassMatricesForPC()`
- `ThetaImplicitEM` / `SemiImplicitEM`

时，必须始终分清当前看到的是：

- 真正推进出来的粒子电流；
- 基准电流 `J0`；
- Jacobian 的线性响应；
- 还是 preconditioner 的近似响应。

不把这四层拆开，`current_fp`、`current_fp_non_suborbit`、`MassMatrices_X/Y/Z`、`MassMatrices_PC` 这些名字会很容易被误读成“同一类场”。
