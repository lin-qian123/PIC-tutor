# 02. 主演化源码证据表

## 1. 顶层文件

| 主题 | 源码位置 | 读法 |
|---|---|---|
| 程序入口 | `Source/main.cpp:20-41` | 外部库初始化、单例、`InitData()`、`Evolve()`、释放单例、外部库结束。 |
| `WarpX` 类定义 | `Source/WarpX.H:85-132` | `WarpX` 继承 `amrex::AmrCore`，暴露 `GetInstance()`、`Finalize()`、`InitData()`、`Evolve()`。 |
| 私有 one-step 声明 | `Source/WarpX.H:1038-1055` | `OneStep`、`OneStep_nosub`、`OneStep_sub1`、`OneStep_JRhom` 都是类内部实现细节。 |
| 单例与构造 | `Source/WarpX.cpp:298-350` | `GetInstance()` 延迟构造；构造函数读参数、建时间数组、建粒子容器。 |
| 参数读取入口 | `Source/WarpX.cpp:547-860` | 本轮已读主循环相关的 solver、scheme、dt、filter、electrostatic、subcycling 分支。 |
| 初始化主函数 | `Source/Initialization/WarpXInitData.cpp:793-949` | 诊断、步长、scratch/restart、PML、初始场、初始诊断、性能提示。 |
| 步长计算 | `Source/Evolve/WarpXComputeDt.cpp:45-108` | 根据 hybrid、electrostatic、PSATD、FDTD、subcycling 计算 `dt`。 |
| 自适应步长 | `Source/Evolve/WarpXComputeDt.cpp:115-142` | 由最大粒子速度更新 `dt`，用于 electrostatic / theta implicit 等可支持路径。 |

## 2. `Evolve()` 外层循环

`Source/Evolve/WarpXEvolve.cpp:146-387` 是主循环。

| 行号 | 代码事件 | 物理/算法含义 |
|---|---|---|
| `154-165` | 取 `cur_time`，确定 `numsteps_max`，进入 `for` | 顶层循环受 `max_step/numsteps` 和 `stop_time` 双重约束。 |
| `170-173` | 信号检查，诊断新迭代 | 支持运行时中断/checkpoint，诊断状态进入新步。 |
| `191-203` | `beforestep`、负载均衡、自适应步长 | 步长更新前需要 `SynchronizeVelocityWithPosition()`，因为最大粒子速度要有一致时间层。 |
| `205-209` | `ExplicitFillBoundaryEBUpdateAux()` | 显式路径在粒子推进前准备 field gather 所需的 auxiliary fields。 |
| `211-217` | HybridPIC 初始 \(\rho,J,B\) | hybrid 模型在第一步前需要初始离子源项和磁场。 |
| `219-229` | 场电离、QED、粒子注入 | 多物理事件发生在 `OneStep()` 前。 |
| `231-233` | `OneStep(cur_time, dt[0], step)` | 真正推进粒子/场一个时间步的分派入口。 |
| `234-243` | resampling 与 mirror | `OneStep()` 后处理粒子重采样和镜面条件。 |
| `245-257` | `istep++`、更新时间 | 更新全局步数和 `t_old/t_new`。 |
| `258-273` | 诊断预打包、moving window、粒子边界 | window 移动会影响粒子重分布和 lattice finder。 |
| `280-321` | 隐式碰撞、静电/hybrid 场解 | 静电与 hybrid 的场更新放在 `OneStep()` 之后。 |
| `323-331` | 诊断需要时同步速度 | 为输出把 \(\mathbf{p}\) 推到与 \(\mathbf{x}\) 同步的时间层。 |
| `333-347` | `afterstep`、reduced/full diagnostics、`afterdiagnostics` | 用户 callback 与诊断写出。 |
| `349-371` | 输入 typo 检查、计时、信号和停止条件 | 第一步后检查未使用输入，循环尾部处理停止。 |
| `374-386` | 终步诊断与全局 warning | PICMI 多次调用 `Evolve()` 时也要避免重复写终步诊断。 |

## 3. `OneStep()` 分派

`Source/Evolve/WarpXEvolve.cpp:389-496` 的分派结构：

```text
if implicit solver:
    m_implicit_solver->OneStep(...)
else:
    if electrostatic or HybridPIC:
        collision placement
        PushParticlesandDeposit(skip_deposition=true)
    else electromagnetic:
        if finest_level == 0:
            OneStep_nosub or OneStep_JRhom
        else:
            OneStep_nosub or OneStep_sub1
```

关键限制：

- JRhom 当前只进入 PSATD 专用路径，见 `OneStep_JRhom()` 的断言 `Source/Evolve/WarpXEvolve.cpp:844-847`。
- subcycling 当前要求 `finest_level == 1`，见 `Source/Evolve/WarpXEvolve.cpp:477-480` 和 `1069`。
- split momentum push 与 JRhom/subcycling 的组合当前有断言限制，见 `Source/Evolve/WarpXEvolve.cpp:456-459`、`481-484`。

## 4. `OneStep_nosub()` 逐段结构

| 行号 | 操作 | 解释 |
|---|---|---|
| `512-515` | 注释给出时间层 | \(\mathbf{x}^n\to\mathbf{x}^{n+1}\)、\(\mathbf{p}^{n-1/2}\to\mathbf{p}^{n+1/2}\)、沉积 \(J^{n+1/2}\) 与 \(\rho^n\)。 |
| `517-556` | `beforedeposition`、碰撞、`PushParticlesandDeposit()`、`afterdeposition` | 根据 `m_collisions_split_momentum_push` 决定碰撞位于动量 push 中间还是 push 前。 |
| `558-561` | `SyncCurrentAndRho()` | 对沉积源项执行滤波、guard cell、AMR 跨层和边界同步。 |
| `567-569` | PML 粒子源项处理 | extended PML 可复制和阻尼 \(J\)。 |
| `571-603` | PSATD 路径 | hybrid QED、`PushPSATD()`、PML、平均场和 divergence cleaning 的 guard cell 更新。 |
| `604-625` | FDTD 路径 | \(F/G\) 半步、\(B\) 半步、\(E\) 一步、\(F/G\) 半步、\(B\) 半步。 |
| `627-640` | PML 和 safe guard cells | 场已更新，但 guard cells 需要按后续操作补齐。 |

## 5. `PushParticlesandDeposit()` 入口

`Source/Evolve/WarpXEvolve.cpp:1311-1415` 是从 WarpX 主循环进入粒子容器的最后一层包装：

- `:1320-1333` 的重载遍历所有 AMR level。
- `:1349-1362` 根据 `do_current_centering` 和 `current_deposition_algo == Vay` 选择沉积目标字段名。
- `:1364-1375` 调用 `mypc->Evolve(...)`，把字段注册器、level、当前字段名、时间、`dt[lev]`、subcycling half、是否跳过沉积、位置/动量 push 类型传入粒子容器。
- `:1377-1405` 在 RZ/柱/球几何中对电流和电荷做逆体积缩放。
- `:1406-1413` 如果有流体物种，则同步推进流体容器。

因此，`PushParticlesandDeposit()` 这个名字不能误读为单个 kernel。它是主循环到物种/粒子模块的接口，真正的粒子循环和沉积分支在 `Particles/MultiParticleContainer*` 与各物种容器中，后续章节需要从这里继续追踪。

## 6. 本轮未完成但已定位的下一级阅读点

| 下一层问题 | 入口线索 |
|---|---|
| `mypc->Evolve()` 如何遍历物种、gather field、调用 pusher、沉积电流/电荷 | 从 `Source/Particles/MultiParticleContainer*` 搜 `void MultiParticleContainer::Evolve`。 |
| `EvolveE/B/F/G` 的有限差分 stencil 和边界应用 | `Source/FieldSolver/FiniteDifferenceSolver` 与 `Source/BoundaryConditions`。 |
| `SyncCurrent()`、`SyncRho()` 的滤波、AMR 加和、guard cell 顺序 | `Source/Evolve` 和 `Source/FieldSolver/Filter` 中对应定义。 |
| PSATD 的 `PushPSATD()`、current correction、JRhom 子沉积 | `Source/FieldSolver/SpectralSolver` 与 `Source/Evolve/WarpXEvolve.cpp:839-1041`。 |
| subcycling 中 fine/coarse current averaging 的守恒解释 | `Source/Evolve/WarpXEvolve.cpp:1043-1269`。 |

