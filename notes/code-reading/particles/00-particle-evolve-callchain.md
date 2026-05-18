# 00. 粒子推进主链

## 1. 从 WarpX 主循环进入粒子容器

主循环中的入口仍然是 `Source/Evolve/WarpXEvolve.cpp:1311-1415` 的 `WarpX::PushParticlesandDeposit()`。它本身不执行粒子 kernel，而是：

1. 遍历 AMR level 或处理指定 level。
2. 根据 `do_current_centering` 和 `current_deposition_algo == Vay` 选择沉积目标字段名。
3. 调用 `mypc->Evolve(...)`，即 `MultiParticleContainer::Evolve()`。
4. 在 RZ/柱/球几何下做逆体积缩放，并在需要时推进流体容器。

因此，真正的粒子循环从 `Source/Particles/MultiParticleContainer.cpp:471-516` 开始。

## 2. `MultiParticleContainer::Evolve()`

| 行号 | 操作 | 解释 |
|---|---|---|
| `Source/Particles/MultiParticleContainer.cpp:471-477` | 函数签名 | 接收 field register、level、current 字段名、时间、步长、subcycling half、是否跳过沉积、位置/动量 push 类型和隐式选项。 |
| `:479-489` | 若不跳过沉积，清零 `current_fp/current_buf/rho_fp/rho_buf` | 一个 step 的源项不能累加上一步残留。 |
| `:490-510` | 隐式 solver 的额外源项和 mass-matrix 清零逻辑 | JFNK/质量矩阵路径需要更细的重置规则。 |
| `:513-515` | 遍历 `allcontainers` | 每个 species 调自己的 `pc->Evolve(...)`。 |

多物种层只管理“所有 species 都要参与本步”。物种内部是否 push、是否 deposit、如何 gather、如何处理 buffer 由 `PhysicalParticleContainer::Evolve()` 决定。

## 3. `PhysicalParticleContainer::Evolve()`

`Source/Particles/PhysicalParticleContainer.cpp:452-825` 是显式粒子章节的主函数。

| 行号 | 操作 | 解释 |
|---|---|---|
| `:468` | `push_type = Explicit/Implicit` | 是否进入隐式粒子推进路径。 |
| `:472-478` | 取 current/gather masks 和 buffer 相关字段是否存在 | AMR fine/coarse buffer 决定哪些粒子在 fine patch 或 coarse patch gather/deposit。 |
| `:480-485` | 取得 `Efield_aux` 和 `Bfield_aux` | 粒子 gather 使用 auxiliary fields，而不是直接任意场数组。 |
| `:487-497` | 计算 `deposit_charge`、`deposit_current` | `skip_deposition`、`do_not_deposit`、隐式 suborbit 都会改变沉积行为。 |
| `:517-575` | 遍历 tile，抽取粒子数据，必要时按 buffer 分区 | `WarpXParIter` 是 tile 级并行入口。 |
| `:579-592` | 推进前沉积 `rho` component 0 | 代表本步旧时间层电荷，常对应 \(\rho^n\)。 |
| `:595-617` | fine patch 粒子 `PushPX()` | 对非 buffer 粒子 gather fine fields 并推进。 |
| `:635-692` | buffer/coarse gather 粒子 `PushPX()` | 对 AMR 边界附近粒子从 coarse auxiliary fields gather。 |
| `:697-733` | 显式路径沉积 current | `relative_time = -0.5*dt`，使电流对应半步时间中心。 |
| `:785-803` | 电磁模式下推进后沉积 `rho` component 1 | 代表新时间层电荷，常对应 \(\rho^{n+1}\)。 |
| `:816-824` | 可选 particle splitting | subcycling 时只在大步末尾 split，避免 coarse level 重复沉积。 |

这段函数把教科书的 “gather-push-deposit” 拆成了实际生产代码顺序：先处理旧电荷、再 gather/push、再 current、再新电荷，并穿插 AMR buffer、隐式路径、load balance cost 和 particle splitting。

## 4. `PushPX()` 融合 kernel

`Source/Particles/PhysicalParticleContainer.cpp:1324-1565` 是显式粒子推进的单粒子融合 kernel。

| 行号 | 操作 | 解释 |
|---|---|---|
| `:1340-1344` | 检查 gather level 并处理空粒子 | gather buffer 只允许从本层或 `lev-1` gather。 |
| `:1346-1360` | 根据 gather level 构造 gather box 并加 guard cells | 形函数 stencil 需要 guard cells 支持。 |
| `:1362-1371` | `gather_fields` 和 BTD copy 逻辑 | 可通过 `do_not_gather` 跳过 field gather。 |
| `:1373-1421` | 准备位置访问器、外场、粒子属性指针、ionization level | device lambda 捕获前的局部数据准备。 |
| `:1440-1468` | species 电荷/质量、pusher 算法、radiation/QED flags | momentum push 分派依赖这些局部变量。 |
| `:1474-1479` | `amrex::ParallelFor` | 真正的 GPU/CPU 并行粒子循环。 |
| `:1480-1508` | 读取粒子位置并调用 `doGatherShapeN` | 网格场通过形函数 gather 到粒子位置。 |
| `:1511-1516` | 叠加外部粒子场和用户缩放 | gather 后还可能有 external field contribution。 |
| `:1523-1547` | 调用 `doParticleMomentumPush` | 分派 Boris/Vay/Higuera-Cary/辐射反作用。 |
| `:1549-1552` | `UpdatePosition` | 若位置 push 类型为 Full，则用更新后的动量推进位置。 |

源码顺序表明 WarpX 在 `PushPX()` 内先 gather，再 momentum push，再 position push。这与 `OneStep_nosub()` 的注释时间层一致：从 \(\mathbf{x}^n,\mathbf{p}^{n-1/2}\) 推到 \(\mathbf{x}^{n+1},\mathbf{p}^{n+1/2}\)。

