# 01. Pusher 与沉积源码证据表

## 1. Momentum pusher 分派

`Source/Particles/Pusher/PushSelector.H:39-104` 定义 `doParticleMomentumPush()`。

| 行号 | 操作 |
|---|---|
| `:61-62` | species 电荷乘 ionization level，得到粒子有效电荷。 |
| `:64-88` | 如果启用 classical radiation reaction，使用 `UpdateMomentumBorisWithRadiationReaction()`，QED 同步情况下可按 `chi` 截断。 |
| `:89-92` | `ParticlePusherAlgo::Boris` 分派到 `UpdateMomentumBoris()`。 |
| `:93-96` | `ParticlePusherAlgo::Vay` 分派到 `UpdateMomentumVay()`。 |
| `:97-100` | `ParticlePusherAlgo::HigueraCary` 分派到 `UpdateMomentumHigueraCary()`。 |

这说明输入参数选择 pusher 后，真正被每个粒子调用的是单粒子 device 函数。

## 2. Boris pusher

`Source/Particles/Pusher/UpdateMomentumBoris.H:20-62` 是 Boris 动量更新。

| 行号 | 数学动作 |
|---|---|
| `:28` | `econst = 0.5*q*dt/m`，电半步系数。 |
| `:30-35` | FirstHalf 或 Full 时执行第一段电场半步。 |
| `:37-45` | 计算相对论 `inv_gamma`、磁旋转向量 `t` 和 `s`。 |
| `:49-55` | Boris 磁旋转。 |
| `:56-61` | SecondHalf 或 Full 时执行第二段电场半步。 |

文件注释 `:13-18` 明确说明 `FirstHalf` 和 `SecondHalf` 连续执行应与一次 `Full` 更新等价。这与碰撞 split momentum push 的源码路径对应。

## 3. Position update

`Source/Particles/Pusher/UpdatePosition.H:19-70` 是显式位置推进：

$$
\mathbf{x}^{n+1}=\mathbf{x}^{n}+\mathbf{v}^{n+1/2}\Delta t,
\qquad
\mathbf{v}^{n+1/2}=\frac{\mathbf{u}^{n+1/2}}{\gamma}.
$$

| 行号 | 操作 |
|---|---|
| `:33-39` | 对有质量粒子计算 \(u^2\) 和 `inv_gamma`。 |
| `:41-50` | 按编译维度更新 \(x,y,z\)。 |
| `:52-69` | 对 massless particles 使用 \(c\mathbf{u}/|\mathbf{u}|\) 更新位置。 |
| `:98-127` | 隐式 Crank-Nicolson 位置推进，使用 \(n\) 与 \(n+1\) 的平均 gamma。 |

## 4. Current deposition 分派

`Source/Particles/WarpXParticleContainer.cpp:392-900` 是 tile 级 current deposition 入口的前半部分。

| 行号 | 操作 |
|---|---|
| `:401-409` | 检查 deposition level，只处理非空粒子且 `do_not_deposit` 为假。 |
| `:411-446` | 取得 `ng_J`，检查粒子 shape 是否能放入 guard cells。 |
| `:448-520` | 准备沉积 level 的 cell size、tilebox、场数组、边界 cropping。 |
| `:546-550` | Esirkepov/Villasenor charge-conserving deposition 不允许 collocated grid。 |
| `:556-650` | shared-memory current deposition 只支持 direct，Esirkepov/Villasenor/Vay 会 abort。 |
| `:654-695` | explicit Esirkepov 分派 `doEsirkepovDepositionShapeN<N>()`。 |
| `:696-751` | implicit charge-conserving deposition 分派。 |
| `:752-835` | Villasenor explicit/implicit 分派。 |
| `:836-864` | Vay deposition 分派；隐式路径会 abort。 |
| `:865-900` | Direct deposition explicit/implicit 分派开头。 |

current deposition 是本书后续需要逐算法推导的重点。当前笔记只确认分派结构。

## 5. Charge deposition 入口

`Source/Particles/WarpXParticleContainer.cpp:1479-1585` 是 tile 级 charge deposition 的入口部分。

| 行号 | 操作 |
|---|---|
| `:1485-1489` | 检查 `rho` component 数量是否足够。 |
| `:1491` | 当前片段进入 shared-memory charge deposition 分支。 |
| `:1497-1503` | 非空粒子检查并取得 `ng_rho`。 |
| `:1504-1533` | 检查粒子 shape 与 guard cells。 |
| `:1535-1539` | 取得 species 电荷并建立 profiling scope。 |
| `:1541-1558` | 构造沉积 tilebox，并按 level/coarse buffer 处理。 |
| `:1560-1577` | GPU 使用 `rho` alias，CPU 使用 thread-local `local_rho`。 |
| `:1579-1585` | 计算 `time_shift_delta`：`icomp==0` 为旧时间层，`icomp==1` 为新时间层。 |

`PhysicalParticleContainer::Evolve()` 中 `rho` component 0 在 push 前沉积，component 1 在 push 后沉积；这里的 `time_shift_delta` 解释了这两个 component 的时间含义。

