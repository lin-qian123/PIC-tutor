# 3. WarpX 主演化路径：生命周期、初始化与 `Evolve()`

本章开始进入 WarpX 源码。目标不是概括“WarpX 有一个 Evolve 函数”，而是建立一个可复查的调用图：程序从 `main.cpp` 进入，如何构造 `WarpX` 对象，如何读取参数和初始化数据，如何计算步长，最后如何在 `WarpXEvolve.cpp` 中把一个个 PIC step 推进下去。

本章的任务是让读者能从一个输入出发，追踪它何时变成网格、场、粒子和诊断，再进入一个物理时间步。使用任何 WarpX 源树时，都应优先按 `main.cpp`、`InitData()`、`ComputeDt()`、`Evolve()` 和 `OneStep()` 的职责与调用关系检索，而不要把固定行号或某个分支名称当作算法语义。

`main.cpp` 负责生命周期，`WarpX` 类建立模拟状态，`WarpXEvolve.cpp` 组织时间推进，`WarpXInitData.cpp` 则准备首个时间步之前的状态。`OneStep_sub1()`、PSATD-JRhom 和 implicit solver 的入口会在本章中定位；场算法的离散公式、粒子的 nonlinear solve 参数和 mass-matrix kernel 分别在后续相关章节展开，避免在调用图中打断物理主线。

### 源码定位约定

WarpX 的实现会继续演进，固定行号只能说明某一次快照的位置，不能说明算法语义。本章因此把 **文件路径和函数/类符号** 作为可迁移的定位锚点：例如，读者在 `Source/Evolve/WarpXEvolve.cpp` 中搜索 `WarpX::OneStep_nosub`，而不是依赖某个行号。引用小段源码时，重点是观察其输入、输出和先后关系；阅读自己的 WarpX 版本时，应先重新搜索同名符号，再比较实现是否改变。

## 3.1 顶层入口：`main.cpp`

WarpX 的可执行入口在 `Source/main.cpp`。主函数的控制流非常短：

```text
initialize_external_libraries(argc, argv)
warpx = WarpX::GetInstance()
warpx.InitData()
warpx.Evolve()
is_warpx_verbose = warpx.Verbose()
WarpX::Finalize()
print timer if verbose
finalize_external_libraries()
```

核心调用的职责如下：

| 源码锚点 | 代码含义 |
|---|---|
| `Source/main.cpp`：`initialize_external_libraries` | 初始化 AMReX/MPI/GPU runtime 等 WarpX 依赖的底层运行环境。 |
| `Source/main.cpp`：`WarpX::GetInstance()` | 取得全局 `WarpX` 单例。 |
| `Source/main.cpp`：`warpx.InitData()` | 把参数、网格、场、粒子、诊断和边界准备好。 |
| `Source/main.cpp`：`warpx.Evolve()` | 进入时间推进主循环。 |
| `Source/main.cpp`：`WarpX::Finalize()` | 释放 `WarpX` 单例。 |
| `Source/main.cpp`：`finalize_external_libraries` | 结束外部库。 |

主函数中的核心段落如下：

```cpp
warpx::initialization::initialize_external_libraries(argc, argv);

auto timer = ablastr::utils::timer::Timer{};
timer.record_start_time();

auto& warpx = WarpX::GetInstance();
warpx.InitData();
warpx.Evolve();
const auto is_warpx_verbose = warpx.Verbose();
WarpX::Finalize();

timer.record_stop_time();
if (is_warpx_verbose) {
    amrex::Print() << "Total Time                     : "
                   << timer.get_global_duration() << '\n';
}

warpx::initialization::finalize_external_libraries();
```

逐块看，这段代码只有一个物理模拟对象 `warpx`。`InitData()` 之前还没有进入时间推进；`Evolve()` 返回之后模拟已经结束，后续只做计时、profiling 和库资源释放。这里没有任何粒子或场循环，因为 WarpX 把模拟状态封装在 `WarpX` 单例内部。

这个入口说明：WarpX 的主程序不直接管理粒子数组或场数组；它只管理生命周期。真正的模拟状态集中在 `WarpX` 对象及其持有的 `MultiParticleContainer`、field register、diagnostics、solver、PML 等成员中。

## 3.2 `WarpX` 类与单例构造

`WarpX` 类定义在 `Source/WarpX.H`。关键声明包括：

| 源码锚点 | 声明 | 作用 |
|---|---|---|
| `Source/WarpX.H` | `class WarpX : public amrex::AmrCore` | WarpX 以 AMReX 的 AMR 基类为基础。 |
| `WarpX::GetInstance()` | `static WarpX& GetInstance();` | 全局单例入口。 |
| `WarpX::Finalize()` | `static void Finalize();` | 删除单例。 |
| `WarpX::InitData()` | `void InitData();` | 初始化模拟数据。 |
| `WarpX::Evolve()` | `void Evolve(int numsteps=-1);` | 外层时间推进。 |
| `WarpX::OneStep*()` | `OneStep`、`OneStep_nosub`、`OneStep_sub1`、`OneStep_JRhom` | 主循环内部的单步推进路径。 |

单例实现位于 `Source/WarpX.cpp`：

- `WarpX::GetInstance()` 检查 `m_instance`，为空则调用 `MakeWarpX()`。
- `WarpX::Finalize()` 调 `ResetInstance()` 删除对象。
- `WarpX::WarpX()` 设置 `m_instance=this`，初始化 warning manager，调用 `ReadParameters()`，做向后兼容处理，初始化 EB，建立 `istep/nsubsteps/t_new/t_old/dt` 数组，并创建 `MultiParticleContainer`。

构造函数中最重要的调用是 `ReadParameters()`。这意味着 solver 类型、边界、步长策略、滤波、静电/电磁模式等会在 `InitData()` 前决定。

## 3.3 `ReadParameters()`：主循环分支的来源

`WarpX::ReadParameters()` 定义在 `Source/WarpX.cpp`。完整参数系统很大，本章只列出直接影响主循环的部分。

| 参数或逻辑 | 读取位置 | 对主循环的影响 |
|---|---|---|
| `max_step`、`stop_time` | `WarpX::ReadParameters()` | `Evolve()` 用它们限制循环终点。 |
| `algo.maxwell_solver` | `WarpX::ReadParameters()` | 选择 PSATD、Yee、CKC、ECT、HybridPIC、None 等路径。 |
| PSATD 不支持 PEC/PMC 的断言 | `WarpX::ReadParameters()` | solver 选择会反过来限制边界条件。 |
| `algo.evolve_scheme` | `WarpX::ReadParameters()` | 决定 explicit、theta implicit 等演化框架。 |
| `warpx.cfl`、`verbose`、`regrid_int`、`do_subcycling` | `WarpX::ReadParameters()` | 控制步长、输出、重网格和 AMR 子循环。 |
| `warpx.do_electrostatic` | `WarpX::ReadParameters()` | 静电 solver 非空时把 electromagnetic solver 设为 `None`。 |
| `const_dt`、`max_dt`、`dt_update_interval` | `WarpX::ReadParameters()` | 控制固定步长和运行中步长更新。 |
| filter 默认开关 | `WarpX::ReadParameters()` | 显式 scheme 默认滤波，隐式 scheme 默认关闭滤波。 |

这里有一个阅读原则：输入文件里的参数名只是表层。要理解参数的真实含义，必须追到 `ReadParameters()` 中它如何被读入、被断言约束、被改写，并进一步影响 `Evolve()`、`ComputeDt()` 或 solver 对象。

## 3.3.1 构造函数只建“跨 level 外壳”，不直接建完整网格数据

仅从 `ReadParameters()` 还看不出一个常见实现边界：`WarpX::WarpX()` 构造函数里虽然已经决定了 solver 路线，但此时还没有有效的 `BoxArray` 和 `DistributionMapping`。构造函数中的注释明确说明：

```cpp
// Geometry on all levels has been defined already.
// No valid BoxArray and DistributionMapping have been defined.
// But the arrays for them have been resized.
```

所以构造函数能做的是：

- 创建不依赖具体网格盒划分的跨 level 对象：
  - `MultiParticleContainer`
  - `m_electrostatic_solver`
  - `m_hybrid_pic_model`
  - solver 指针数组外壳
- 按 `maxLevel()+1` 先 `resize` 各种 level 容器：
  - `istep`
  - `nsubsteps`
  - `t_old/t_new`
  - `dt`

但它不能在这里直接分配真正的 `Efield_fp/Bfield_fp/current_fp/rho_fp`。这些字段必须等到 `MakeNewLevelFromScratch() -> AllocLevelData() -> AllocLevelMFs()`，拿到真实的 `ba/dm`、index type 和 guard cell 之后才创建。

这也是为什么：

- `effective potential` 在构造期只创建 `EffectivePotentialES` 对象；
- `hybrid PIC` 在构造期只创建 `HybridPICModel` 对象；
- `implicit solver` 即使已经存在，也还没分配 mass matrices。

真正的 level 级附加字段要到后面才各自落地。

## 3.3.2 `AllocLevelData()` / `AllocLevelMFs()` 里，四条 solver 分支的落点不同

`AllocLevelData()` 定义在 `Source/WarpX.cpp`。它先调用 `guard_cells.Init(...)`，再进入 `AllocLevelMFs(...)`。这一层真正决定的是：哪些 `MultiFab` 需要随着 level 一起出生。

先看隐式分支。`AllocLevelMFs()` 并不会一次性把全部隐式字段都分好，它只先放两类最基础的 level 数据：

```cpp
if (m_implicit_solver) {
    m_fields.alloc_init(FieldType::current_fp_non_suborbit, Direction{0}, lev,
                        amrex::convert(ba, jx_nodal_flag), dm, ncomps, ngJ, 0.0_rt);
    ...
    m_fields.alloc_init(FieldType::E_old, Direction{2}, lev,
                        amrex::convert(ba, Ez_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
}
```

也就是说，隐式路线在 level 分配期先保存：

- 非 suborbit 粒子的独立电流容器 `current_fp_non_suborbit`
- 旧电场时间层 `E_old`

而更重的 `MassMatrices_X/Y/Z`、`MassMatrices_PC` 不是在这里分配，而是在后续 `ImplicitSolver::InitializeMassMatrices()` 里，等标准 `current_fp/Efield_fp` 的 index type、guard cells 和 deposition 算法都稳定后再决定组件数。

再看 `hybrid PIC`。它在构造期只有一个模型对象，真正的 level 字段由 `HybridPICModel::AllocateLevelMFs(...)` 填入共享的 `m_fields` register：

```cpp
if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC)
{
    m_hybrid_pic_model->AllocateLevelMFs(
        m_fields,
        lev, ba, dm, ncomps, ngJ, ngRho, ngEB, jx_nodal_flag, jy_nodal_flag,
        jz_nodal_flag, rho_nodal_flag, Ex_nodal_flag, Ey_nodal_flag, Ez_nodal_flag,
        Bx_nodal_flag, By_nodal_flag, Bz_nodal_flag
    );
}
```

这一调用会分配：

- `hybrid_electron_pressure_fp`
- `hybrid_rho_fp_temp`
- `hybrid_current_fp_temp`
- `hybrid_current_fp_plasma`
- 可选的 `hybrid_current_fp_external`

若启用 `add_external_fields`，还会进一步分配 external vector potential 相关字段。也就是说，hybrid 不是在 `WarpX` 根层自己持有一套独立网格，而是把专用状态嵌进统一的 field register。

再看 `effective potential electrostatic solver`。这条线在构造期创建了 `EffectivePotentialES` 对象，但 level 分配期没有额外的 `effective_potential_*` 专用字段。它复用的是静电共享合同：

```cpp
if( (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrame) ||
    (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic) ||
    (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameEffectivePotential) ||
    (electromagnetic_solver_id == ElectromagneticSolverAlgo::HybridPIC) ) {
    rho_ncomps = ncomps;
}

if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrame ||
    electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic ||
    electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameEffectivePotential )
{
    m_fields.alloc_init(FieldType::phi_fp, lev, amrex::convert(ba, phi_nodal_flag), dm,
                         ncomps, ngPhi, 0.0_rt );
}
```

所以 `effective potential` 在根层最关键的差异不是“多了什么字段”，而是后续 solver 如何解释和消费 `rho_fp/phi_fp`。

最后是 `PML`。它同样不是在 `AllocLevelMFs()` 里出生。真正创建 `PML` 对象是在 `InitFromScratch()` 的最后一步：

```cpp
AmrCore::InitFromScratch(time);  // This will call MakeNewLevelFromScratch
...
mypc->AllocData();
mypc->InitData();

InitPML();
```

这条顺序说明：

- 先有普通 level 的 fields / particles
- 后有作为边界子系统的 `PML`

因此 `PML` 是初始化末段附加上的 patch 级边界对象，而不是和 `Efield_fp/Bfield_fp` 同时由 `AllocLevelMFs()` 常规分配的主网格字段。

把对象落点按路径分开读，会比把构造、分配和初始化末段塞进同一张宽表更清楚：

- **标准场**：构造期只准备容器外壳；`AllocLevelMFs()` 分配 `Efield_fp`、`Bfield_fp`、`current_fp`、`rho_fp` 和 `phi_fp`；`InitLevelData()` 再填入物理初值。
- **effective potential**：构造期创建 `EffectivePotentialES`；level 分配期不另建专用字段，而是复用 `rho_fp/phi_fp`；静电求解器随后按 effective-potential 语义消费这些字段。
- **hybrid PIC**：构造期创建 `HybridPICModel`；level 分配期把 `hybrid_*` 字段放入共享 `m_fields`；`HybridPICModel::InitData()` 再编译 parser 并准备外加电流和矢势。
- **implicit**：solver 对象在构造期已存在；level 分配期先分配 `current_fp_non_suborbit` 与 `E_old`；随后 `Define()`、`CreateParticleAttributes()` 和 `InitializeMassMatrices()` 逐步补齐隐式响应数据。
- **PML**：构造期只知道参数和开关，`AllocLevelMFs()` 也不创建 PML patch；`InitPML()` 在获得真实 `boxArray`、`DistributionMapping`、`dt` 和 `m_fields` 后再创建边界对象。

## 3.4 `InitData()`：把状态准备到可推进

`WarpX::InitData()` 定义在 `Source/Initialization/WarpXInitData.cpp`。它不是简单分配内存，而是把一个模拟从“参数已读”变成“可以推进第一步”。

核心顺序如下：

| 源码动作 | 解释 |
|---|---|
| 进入 `InitData()`，检查 MPI thread level | 并行运行前的运行环境检查。 |
| 创建 `MultiDiagnostics` 和 `MultiReducedDiags` | 诊断系统在初始化早期建立。 |
| 非 restart：`ComputeDt()`、打印步长网格、`InitFromScratch()`、`InitDiagnostics()` | 从头运行时先确定步长，再建立网格/粒子/诊断。 |
| restart：`InitFromCheckpoint()`、打印步长网格、`PostRestart()` | checkpoint 恢复不走完全相同的初始化路径。 |
| `ComputeMaxStep()`、PML factors、NCI corrector、buffer masks | 准备停止步数、吸收边界和数值不稳定修正。 |
| 宏观介质、静电 solver、HybridPIC 初始化 | solver 相关对象拿到场布局和参数。 |
| 网格摘要、guard cell 检查、打印 PIC 参数、写 used inputs | 把运行状态和输入记录下来。 |
| 初始 div cleaning、自洽静电/磁静场、外场叠加 | 从头运行时在第一个 step 前建立初始场。 |
| 初始 full/reduced diagnostics | 允许输出第 0 步或 restart 后诊断。 |
| 性能提示和 solver issue 检查 | 给出已知风险提示。 |

`InitFromScratch()` 调用 `AmrCore::InitFromScratch(time)` 建立 AMR level，然后让 `mypc->AllocData()` 和 `mypc->InitData()` 初始化粒子，最后初始化 PML。

## 3.5 `ComputeDt()`：步长不是一个固定常数

`WarpX::ComputeDt()` 定义在 `Source/Evolve/WarpXComputeDt.cpp`。

逻辑可以分成四类：

1. HybridPIC 必须显式给出 `warpx.const_dt`。
2. 纯静电或无 Maxwell solver 时，必须给出 `const_dt` 或激活 `dt_update_interval`。
3. 若用户给了 `const_dt`，直接使用。
4. 否则按 solver 计算 CFL 限制：静电/PSATD 用最小 cell size 与 \(c\)，FDTD 调用具体几何和算法的 `ComputeMaxDt()`。

最终 `dt` 被 resize 到 `max_level+1`。若启用 subcycling，粗层步长由细层步长乘 refinement ratio 得到。

把它写成决策顺序会比宽表更容易在阅读和排版中保持清楚：

1. **用户固定步长优先。** 设置 `warpx.const_dt` 后，`ComputeDt()` 直接采用它，所有 CFL 估计都不再决定步长；稳定性责任也随之转给用户。
2. **特殊模型先检查强制条件。** HybridPIC 必须给出 `const_dt`。静电路径若未使用固定步长，则以 `max_dt` 为初值；若也未给出，则退回到 $\mathrm{CFL}\,\Delta x_{\min}/c$。
3. **PSATD 使用最小网格尺度的光速尺度。** 在没有固定步长时，初值为 $\mathrm{CFL}\,\Delta x_{\min}/c$。这只是本函数的初始选择，不能替代该配置的物理分辨率判断。
4. **FDTD 按几何和网格布置选择稳定上限。** Cartesian collocated grid 调用 `CartesianNodalAlgorithm::ComputeMaxDt`；Yee/ECT 调用 `CartesianYeeAlgorithm::ComputeMaxDt`；CKC 调用 `CartesianCKCAlgorithm::ComputeMaxDt`。RZ/RCYLINDER 的 Yee 路径还使用 azimuthal mode 数，RSPHERE 则走 `SphericalYeeAlgorithm::ComputeMaxDt`。这些函数名比展开成长公式更适合作为源码阅读入口。

因此，`ComputeDt()` 不只是“取最小网格长度除以光速”，而是在参数层先决定有没有用户强制时间步，再按 solver 家族和几何去选真正的稳定上限公式。

运行中自适应步长由 `WarpX::ApplyDtLimiters()` 处理。它首先经 `ParticleGridSpeedMax()` 从 `mypc->maxParticleVelocity()` 计算最大粒子跨网格速度，再与可选的等离子体频率、回旋频率和 `max_dt` 限制一起取最严格的步长。仅考虑粒子跨网格限制时，公式是

$$
\Delta t_{\mathrm{new}}=\mathrm{CFL}\frac{\Delta x_{\min}}{v_{\max}}
$$

`ApplyDtLimiters()` 更新 finest level 的 `dt`，再向粗层回推。因此它并不等同于一个只看粒子速度的旧接口：开启 `max_omegap_dt`、`max_omegac_dt` 或 `max_dt` 时，任何一个限制都可以成为最终瓶颈。

这里还要补一条参数层边界：`warpx.const_dt` 与 `warpx.dt_update_interval` 在 `ReadParameters()` 中就是互斥的。也就是说，运行时 adaptive timestep 不是“在固定步长上再做微调”，而是一条和 `const_dt` 完全不同的时间组织路线。`Evolve()` 里只有当 `m_dt_update_interval.contains(step+1)` 为真，或首步需要应用 `max_dt` 时，才会在步首调用 `ApplyDtLimiters()`。

## 3.6 `Evolve()` 外层时间步

`WarpX::Evolve()` 定义在 `Source/Evolve/WarpXEvolve.cpp`。它不是单纯调用 `OneStep()`，而是在每个 step 前后管理大量状态。

外层结构是：

```text
cur_time = t_new[0]
numsteps_max = max_step or istep[0] + numsteps
for step in range while cur_time < stop_time:
    check signals
    multi_diags->NewIteration()
    run beforestep callback
    CheckLoadBalance(step)
    maybe update dt from particle speeds
    ExplicitFillBoundaryEBUpdateAux()
    hybrid initialization if first step
    field ionization / QED / particle injection
    OneStep(cur_time, dt[0], step)
    resampling / mirrors
    increment istep and time
    diagnostics prepack, moving window, particle boundary handling
    electrostatic or hybrid field solve if selected
    optional velocity synchronization for diagnostics
    afterstep callback, diagnostics, warnings, signals, stop check
```

关键动作：

| 源码动作 | 读法 |
|---|---|
| 初始化 `cur_time` 和循环边界 | `numsteps=-1` 时使用全局 `max_step`。 |
| 信号检查、诊断新迭代 | 支持运行中断、checkpoint 和诊断状态更新。 |
| callback、负载均衡、可选步长更新 | 更新步长前需要同步粒子速度时间层。 |
| `ExplicitFillBoundaryEBUpdateAux()` | 显式 scheme 为后续 field gather 准备场。 |
| field ionization、QED、particle injection | 多物理事件在 `OneStep()` 前改变粒子集合。 |
| `OneStep(cur_time, dt[0], step)` | 进入单步推进分派。 |
| 更新 `istep` 和 `t_old/t_new` | 单步推进后更新时间状态。 |
| 诊断预处理、moving window、粒子边界 | `OneStep()` 后的工程处理同样影响物理结果。 |
| 静电或 HybridPIC 的场解 | 非标准电磁路径的场更新位置不同。 |
| 诊断需要时同步粒子速度 | 为输出把 \(\mathbf{p}\) 与 \(\mathbf{x}\) 放到同步时间层。 |
| reduced/full diagnostics 和 callback | 诊断写出发生在本步状态更新之后。 |
| 未使用输入检查、计时、信号、停止 | 第一步后检查输入 typo，最后判断是否退出。 |

注意 `Evolve()` 中多物理和诊断并不都在 `OneStep()` 内部。比如 field ionization、QED 和 particle injection 在 `OneStep()` 之前，resampling、moving window、粒子边界和某些 electrostatic/hybrid 场解在 `OneStep()` 之后。

### 3.6.1 步末 moving window：连续坐标与整数网格平移

要理解 moving window，先把它放回 `Evolve()` 主循环中：`MoveWindow(step+1, move_j)` 发生在 `OneStep()` 完成、`cur_time` 和 `t_new` 更新之后，粒子边界处理之前。对应逻辑位于 `WarpX::Evolve()`：

```cpp
cur_time += dt[0];

ShiftGalileanBoundary();

// sync up time
for (int i = 0; i <= max_level; ++i) {
    t_old[i] = t_new[i];
    t_new[i] = cur_time;
}
multi_diags->FilterComputePackFlush( step, false, true );

const bool move_j = m_is_synchronized;
// If m_is_synchronized we need to shift j too so that next step we can evolve E by dt/2.
// We might need to move j because we are going to make a plotfile.
const int num_moved = MoveWindow(step+1, move_j);
```

`MoveWindow()` 的第一层逻辑是维护一个连续窗口位置 `moving_window_x`，但只有当它相对当前几何左边界跨过整数个 cell 时才真正平移网格数据。实现位于 `Source/Utils/WarpXMovingWindow.cpp`：

```cpp
if (!moving_window_active(step)) { return 0; }

// Update the continuous position of the moving window,
// and of the plasma injection
moving_window_x += (moving_window_v - WarpX::beta_boost * PhysConst::c)
                   / (1 - moving_window_v * WarpX::beta_boost / PhysConst::c) * dt[0];
const int dir = moving_window_dir;

// Update current injection position for all containers
::UpdateInjectionPosition(*mypc, gamma_boost, beta_boost, boost_direction, moving_window_dir, dt[0]);

// Update antenna position for all lasers
// TODO Make this specific to lasers only
mypc->UpdateAntennaPosition(dt[0]);

// compute the number of cells to shift on the base level
amrex::Real new_lo[AMREX_SPACEDIM];
amrex::Real new_hi[AMREX_SPACEDIM];
const amrex::Real* current_lo = geom[0].ProbLo();
const amrex::Real* current_hi = geom[0].ProbHi();
const amrex::Real* cdx = geom[0].CellSize();
const int num_shift_base = static_cast<int>((moving_window_x - current_lo[dir]) / cdx[dir]);

if (num_shift_base == 0) { return 0; }
```

这段代码中的速度变换是相对论速度合成公式：

$$
v'_w=\frac{v_w-\beta_b c}{1-v_w\beta_b/c}.
$$

因此 boosted-frame 模拟中窗口速度不是简单使用输入的 `moving_window_v`。输入参数在 `read_moving_window_parameters()` 中先由以 \(c\) 为单位的无量纲数转成 SI 速度；运行时再按 boost 速度变换到模拟坐标系。

active 判定本身也不是模糊的“某个阶段窗口有效”，而是源码里一个明确的闭开区间：

$$
\texttt{start\_moving\_window\_step}\le n < \texttt{end\_moving\_window\_step},
$$

若 `end_moving_window_step < 0` 则表示没有终止步。这也是为什么 `Evolve()` 调的是 `MoveWindow(step+1, ...)`：窗口平移是本步结束后、下一步开始前的状态更新。

当 `num_shift_base != 0` 时，`MoveWindow()` 调用 `ResetProbDomain()` 更新几何域，随后由 `shiftMF()` 平移场、source、PML、\(F/G\)、\(\rho\) 与 fluid 的 `MultiFab`。核心赋值为：

```cpp
amrex::Box dstBox = mf[mfi].box();
if (num_shift > 0) {
    dstBox.growHi(dir, -num_shift);
} else {
    dstBox.growLo(dir,  num_shift);
}
AMREX_PARALLEL_FOR_4D ( dstBox, nc, i, j, k, n,
{
    dstfab(i,j,k,n) = srcfab(i+shift.x,j+shift.y,k+shift.z,n);
})
```

即

$$
F_{\mathrm{new}}(\mathbf{i})=F_{\mathrm{old}}(\mathbf{i}+N_{\mathrm{shift}}\hat e_{\mathrm{dir}}).
$$

新露出的边界层不是随便置零。对外部场，`shiftMF()` 可以用常量外场或 parser 外场重新初始化；对背景粒子，`MoveWindow()` 构造整数 cell 宽度的 `particleBox` 并调用 `pc.ContinuousInjection(particleBox)`。这解释了 moving window 的数值设计：连续窗口位置负责物理速度，整数 cell 平移负责保持网格离散结构和宏粒子 spacing。

这里还要和步末的 `ContinuousFluxInjection(cur_time, dt[0])` 分开。二者不是同一件事：

- moving-window continuous injection：在新露出的体网格区域里补背景体分布；
- continuous flux injection：从定义好的注入面持续打入粒子通量。

前者是“窗口移动后补齐新计算域”，后者是“边界源项继续往域内送粒子”。

## 3.7 `OneStep()`：求解器分派器

`WarpX::OneStep()` 定义在 `Source/Evolve/WarpXEvolve.cpp`。它按 solver 和 AMR 情况分派：

```text
if m_implicit_solver:
    m_implicit_solver->OneStep(...)
else:
    if electromagnetic_solver_id is None or HybridPIC:
        push particles, optionally split collisions, skip deposition
    else:
        if finest_level == 0:
            OneStep_nosub or OneStep_JRhom
        else:
            OneStep_nosub or OneStep_sub1
```

这段代码体现了 WarpX 的设计：`OneStep()` 不直接写某一种 PIC 算法的全部细节，而是先把路径分开。

**读者的生命周期检查卡。** 从一个输入追到可比较的输出时，不要把函数名称当成时间层。先确认输入参数如何决定求解器、几何和 AMR 分支；再确认 `InitData()` 已创建可被第一步消费的离散状态；随后把 `Evolve()` 视为提交一个外层区间 $t^n\to t^{n+1}$ 的边界；最后才由 `OneStep()` 判断这个区间实际采用哪一条时间合同。每次读到一次循环、一次沉积或一次 RHS 评估，都要回问：它是在推进物理时间，还是在为同一外层步重建 source？输出文件出现后，还必须接回独立 reference 和 observable，不能把控制流命中当作物理验证。

可将这条检查卡压成五个连续问题：

1. 输入参数先决定求解器、几何和 AMR 分支；
2. 初始化负责创建可被第一步消费的离散状态；
3. 外层步只定义 $t^n\to t^{n+1}$ 的提交边界；
4. 单步分派才决定实际进入哪条时间合同；
5. 可观察输出必须与独立 reference 一起判断。

| 分支 | 源码锚点 | 含义 |
|---|---|---|
| implicit solver | `m_implicit_solver->OneStep(...)` | 交给隐式 solver 自己推进一整步。 |
| electrostatic / HybridPIC | `electromagnetic_solver_id == None/HybridPIC` | 粒子推进但跳过标准电磁沉积路径，场解在外层后处理。 |
| 标准电磁无 MR | `finest_level == 0` | 进入 `OneStep_nosub()` 或 PSATD-JRhom。 |
| 有 MR 无 subcycling | `!m_do_subcycling` | 仍进入 `OneStep_nosub()`，所有 level 使用同一步长推进。 |
| 有 MR 且 subcycling | `m_do_subcycling` | 进入 `OneStep_sub1()`；该函数拒绝超过两个 level，且要求 2:1 refinement ratio。 |

几个断言值得后续单独讲：

- JRhom 与 split momentum collision 不能组合。
- subcycling 要求 `finest_level == 1`。
- subcycling 与 split momentum collision 也不能组合。

这些不是文档层面的“建议”，而是源码级功能边界。

还应补一条输入层边界：`psatd.JRhom` 不是布尔开关，而是一个编码了源项时间模型的字符串。`ReadParameters()` 里它会同时决定：

- `J` 的时间依赖是 constant / linear / quadratic；
- `rho` 的时间依赖是 constant / linear / quadratic；
- 一个 PIC step 里切成多少个 JRhom subinterval。

因此 `JRhom` 开启后，后续变的不是“另一个小优化开关”，而是 `OneStep()` 内部的时间组织、`rho_fp` 的组件语义和谱空间源项更新公式。

## 3.8 `OneStep_nosub()`：显式电磁标准路径

`WarpX::OneStep_nosub()` 定义在 `Source/Evolve/WarpXEvolve.cpp`。这是本书第一个需要逐行读懂的核心函数。

它的结构分为四段。

第一段：粒子推进、碰撞与沉积。

源码原文：

```cpp
// Push particle from x^{n} to x^{n+1}
//               from p^{n-1/2} to p^{n+1/2}
// Deposit current j^{n+1/2}
// Deposit charge density rho^{n}

ExecutePythonCallback("beforedeposition");

// with collisions placed in the middle of the momentum push
if (m_collisions_split_momentum_push) {
    // push particles (half momentum)
    PushParticlesandDeposit(
        a_cur_time,
        /*skip_deposition=*/true,
        PositionPushType::None,
        MomentumPushType::FirstHalf
    );
    // perform particle collisions
    ExecutePythonCallback("beforecollisions");
    mypc->doCollisions(a_step, a_cur_time, a_dt);
    ExecutePythonCallback("aftercollisions");

    // push particles (full position and half momentum)
    PushParticlesandDeposit(
        a_cur_time,
        /*skip_deposition=*/false,
        PositionPushType::Full,
        MomentumPushType::SecondHalf
    );
}
else {
    ExecutePythonCallback("beforecollisions");
    mypc->doCollisions(a_step, a_cur_time, a_dt);
    ExecutePythonCallback("aftercollisions");

    PushParticlesandDeposit(
        a_cur_time,
        /*skip_deposition=*/false,
        PositionPushType::Full,
        MomentumPushType::Full
    );
}

ExecutePythonCallback("afterdeposition");
```

- 注释明确时间层：\(\mathbf{x}^{n}\to\mathbf{x}^{n+1}\)，\(\mathbf{p}^{n-1/2}\to\mathbf{p}^{n+1/2}\)，沉积 \(\mathbf{J}^{n+1/2}\) 和 \(\rho^n\)。
- 如果 `m_collisions_split_momentum_push` 为真，先做半个动量 push，再碰撞，再做位置 push 和后半动量 push。
- 否则先做碰撞，再调用 `PushParticlesandDeposit()` 完整推进粒子并沉积。

第二段：源项同步。

源码原文：

```cpp
// Synchronize J and rho:
// filter (if used), exchange guard cells, interpolate across MR levels
// and apply boundary conditions
SyncCurrentAndRho();

// At this point, J is up-to-date inside the domain, and E and B are
// up-to-date including enough guard cells for first step of the field
// solve.

// For extended PML: copy J from regular grid to PML, and damp J in PML
if (do_pml && pml_has_particles) { CopyJPML(); }
if (do_pml && do_pml_j_damping) { DampJPML(); }
```

- `SyncCurrentAndRho()` 会处理滤波、guard cells、AMR 跨层插值/加和和边界。
- PML 若含粒子或需要电流阻尼，会复制和阻尼 PML 中的电流。

第三段：PSATD 或 FDTD 场推进。

FDTD 分支的核心源码如下：

```cpp
} else {
    EvolveF(0.5_rt * dt[0], /*rho_comp=*/0);
    EvolveG(0.5_rt * dt[0]);
    FillBoundaryF(guard_cells.ng_FieldSolverF);
    FillBoundaryG(guard_cells.ng_FieldSolverG);

    EvolveB(0.5_rt * dt[0], SubcyclingHalf::FirstHalf, a_cur_time); // We now have B^{n+1/2}
    FillBoundaryB(guard_cells.ng_FieldSolver, WarpX::sync_nodal_points);

    if (m_em_solver_medium == MediumForEM::Vacuum) {
        EvolveE(dt[0], a_cur_time); // We now have E^{n+1}
    } else if (m_em_solver_medium == MediumForEM::Macroscopic) {
        MacroscopicEvolveE(dt[0], a_cur_time); // We now have E^{n+1}
    } else {
        WARPX_ABORT_WITH_MESSAGE("Medium for EM is unknown");
    }
    FillBoundaryE(guard_cells.ng_FieldSolver, WarpX::sync_nodal_points);

    EvolveF(0.5_rt * dt[0], /*rho_comp=*/1);
    EvolveG(0.5_rt * dt[0]);
    EvolveB(0.5_rt * dt[0], SubcyclingHalf::SecondHalf,
            a_cur_time + 0.5_rt * dt[0]); // We now have B^{n+1}
```

- PSATD 走 `PushPSATD(a_cur_time)`，并处理 hybrid QED、PML、平均场、\(F/G\) guard cells。
- FDTD 走 `EvolveF/G` 半步、`EvolveB(dt/2)`、`EvolveE(dt)`、`EvolveF/G` 半步、`EvolveB(dt/2)`。

第四段：回调。

- `afterEsolve` callback 在场更新后执行。

从物理角度看，`OneStep_nosub()` 做的事情是：用旧场 gather 推粒子，得到新位置和半步电流；把源项修整到网格和边界一致；再用这些源项推进电磁场。

## 3.9 `SyncCurrentAndRho()`：源项不是沉积完就可用

`SyncCurrentAndRho()` 定义在 `Source/Evolve/WarpXEvolve.cpp`。

它的分支很重要：

- PSATD 且 periodic single box 时，会立即同步 \(J\) 和 \(\rho\)。
- PSATD 非 periodic single box 时，若没有 current correction 且不是 Vay deposition，才在这里同步。
- Vay deposition 在特定情况下先只做 filter。
- FDTD 路径总是 `SyncCurrent("current_fp")` 和 `SyncRho()`。
- 最后对 \(\rho\) 和 \(J\) 施加 PEC 等边界处理。

这说明“沉积”与“可用于场解”之间有一段不可忽略的工程层：滤波、guard cell、AMR 和边界会改变源项数组的可用状态。

## 3.10 `PushParticlesandDeposit()`：进入粒子容器

`PushParticlesandDeposit()` 的两个重载定义在 `Source/Evolve/WarpXEvolve.cpp`。

第一层重载遍历所有 AMR level。第二层重载做三件事：

1. 根据 `do_current_centering` 和 `current_deposition_algo == Vay` 选择当前沉积字段名。
2. 调用 `mypc->Evolve(...)`，把 field register、level、字段名、时间、`dt[lev]`、subcycling half、是否跳过沉积、位置/动量 push 类型传入粒子容器。
3. 对 RZ/柱/球几何做逆体积缩放，并在有流体物种时调用流体容器演化。

因此，下一阶段逐行阅读必须从 `mypc->Evolve()` 继续进入 `Source/Particles`。`PushParticlesandDeposit()` 是主循环到粒子模块的接口，不是粒子 pusher 本身。

## 3.11 `OneStep_sub1()` 与 JRhom 的位置

理解这两个特殊分支时，先把它们放回主循环时间层。

`OneStep_sub1()` 定义在 `Source/Evolve/WarpXEvolve.cpp`。这条 subcycling 路径要求两个 level 和 2:1 refinement ratio：fine patch 用小步长推两次，coarse patch 和 mother grid 推一次，coarse 场使用两次 fine current 的平均效果。入口断言与函数注释共同限定了这个适用范围：

```cpp
 * This version of subcycling only works for 2 levels and with a refinement
 * ratio of 2.
 * The particles and fields of the fine patch are pushed twice
 * (with dt[coarse]/2) in this routine.
 * The particles of the coarse patch and mother grid are pushed only once
 * (with dt[coarse]). The fields on the coarse patch and mother grid
 * are pushed in a way which is equivalent to pushing once only, with
 * a current which is the average of the coarse + fine current at the 2
 * steps of the fine grid.
```

第一段 fine step 的核心源码如下：

```cpp
PushParticlesandDeposit(fine_lev, cur_time, SubcyclingHalf::FirstHalf);
RestrictCurrentFromFineToCoarsePatch(
    m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level),
    m_fields.get_mr_levels_alldirs(
        FieldType::current_cp, finest_level, skip_lev0_coarse_patch),
    fine_lev);
RestrictRhoFromFineToCoarsePatch(fine_lev);

EvolveB(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], SubcyclingHalf::FirstHalf, cur_time);
EvolveF(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], /*rho_comp=*/0);
EvolveE(fine_lev, PatchType::fine, dt[fine_lev], cur_time);
EvolveB(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev],
        SubcyclingHalf::SecondHalf,
        cur_time + 0.5_rt * dt[fine_lev]);
EvolveF(fine_lev, PatchType::fine, 0.5_rt*dt[fine_lev], /*rho_comp=*/1);
```

因此 subcycling 的物理时间层是

$$
\Delta t_0=2\Delta t_1.
$$

fine level 在一个 coarse step 内走两个完整 leapfrog 小步。随后对 current 和 \(\rho\) 做 restriction 到 coarse patch；`StoreCurrent()`/`RestoreCurrent()` 保证 coarse 粒子自身 current 能在两个 half coarse step 中分别叠加对应的 fine contribution。

这里 `StoreCurrent()`/`RestoreCurrent()` 的角色需要说得更硬一点：subcycling 不是简单把 fine current 直接覆写 coarse current，而是要先保留 coarse 粒子本身在大步时间层上的电流，再把两次 fine-step 的 restriction 结果分别叠回 coarse half-step。否则 coarse mother grid 看到的就不是“一个 coarse 大步上等效的平均源项”，而会把 coarse 自身电流和 fine 补偿混在一起。

`OneStep_JRhom()` 定义在 `Source/Evolve/WarpXEvolve.cpp`。它是 PSATD-JRhom 专用路径，会多次沉积 \(J\) 和 \(\rho\)，在谱空间推进字段，并支持时间平均场。入口先断言 solver 必须是 PSATD，并且粒子 push 时跳过标准沉积：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD,
    "JRhom algorithm not implemented with the FDTD solver"
);

// Push particle from x^{n} to x^{n+1}
//               from p^{n-1/2} to p^{n+1/2}
const bool skip_deposition = true;
PushParticlesandDeposit(cur_time, skip_deposition);

// Initialize PSATD-JRhom loop:

// 1) Prepare E,B,F,G fields in spectral space
PSATDForwardTransformEB();
if (WarpX::do_dive_cleaning) { PSATDForwardTransformF(); }
if (WarpX::do_divb_cleaning) { PSATDForwardTransformG(); }
```

随后 JRhom 以

$$
\delta t=\frac{\Delta t}{m}
$$

为子区间，多次在相对时间 `t_deposit_current` 和 `t_deposit_charge` 沉积源项：

```cpp
const int n_deposit = WarpX::m_JRhom_subintervals;
const amrex::Real sub_dt = dt[0] / static_cast<amrex::Real>(n_deposit);
const int n_loop = (WarpX::fft_do_time_averaging) ? 2*n_deposit : n_deposit;

for (int i_deposit = 0; i_deposit < n_loop; i_deposit++)
{
    if (time_dependency_J != TimeDependencyJ::Constant) { PSATDMoveJNewToJOld(); }

    const amrex::Real t_deposit_current = (time_dependency_J == TimeDependencyJ::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;

    const amrex::Real t_deposit_charge = (time_dependency_rho == TimeDependencyRho::Linear) ?
        (i_deposit-n_deposit+1)*sub_dt : (i_deposit-n_deposit+0.5_rt)*sub_dt;

    mypc->DepositCurrent(
        m_fields.get_mr_levels_alldirs(current_string, finest_level),
        dt[0], t_deposit_current);
    SyncCurrent("current_fp");
    PSATDForwardTransformJ("current_fp", "current_cp");
```

所以 JRhom 的核心不是多次 gather，也不是多次粒子 push，而是用同一次粒子轨道在多个相对时间沉积源项，让 PSATD 在一个 step 内看到更高阶的 \(\widetilde{\mathbf J}(t)\) 和 \(\widetilde\rho(t)\)。

这条线路还有两条必须写清的功能限制：

1. `JRhom` 不支持 FDTD，只能走 PSATD。
2. `JRhom` 和 `current_correction`、`Vay deposition` 都不兼容；源码层会把 `current_correction` 关掉，并显式禁止 `Vay deposition` 和 JRhom 组合。

所以这一支的真实定位是：它不是“PSATD 上再附加一个任意可叠加的小修正”，而是 PSATD 自身的一种替代性时间积分组织方式。

### 3.11.1 implicit 分支：一次物理步包含多次试探性 source 重建

在 `WarpX::OneStep()` 中，只要 `m_implicit_solver` 非空，程序就不会进入 `OneStep_nosub()`、`OneStep_sub1()` 或 `OneStep_JRhom()`，而是把整步交给 `m_implicit_solver->OneStep(...)`。

以 `SemiImplicitEM::OneStep()` 为代表，隐式电磁步的控制流是：

| 顺序 | 源码动作 | 时间层/物理含义 |
| --- | --- | --- |
| 1 | `SaveParticlesAtImplicitStepStart()` | 保存 $x^n,p^n$，供非线性迭代和最终提交使用 |
| 2 | 初始化 $E^{n+θ}$ 猜测、保存 `E_old` | 构造 solver 的中间场未知量，而不是直接写最终 $E^{n+1}$ |
| 3 | `EvolveB(Δt/2)` | 先把 WarpX 所有的磁场推进到半步 |
| 4 | `m_nlsolver->Solve(...)` | 反复调用 `ComputeRHS()`，求粒子和中间电场自洽的离散方程 |
| 5 | `SetElectricFieldAndApplyBCs()`、`FinishImplicitParticleUpdate()` | 将收敛的中间场写回，并把粒子从半步状态完成到 $t^{n+1}$ |
| 6 | 第二个 `EvolveB(Δt/2)` | 完成磁场后半步，物理时间步才真正结束 |

因此 `m_nlsolver->Solve()` 不是一个普通的函数调用包装，而是这条路径的核心时间组织。`SemiImplicitEM::ComputeRHS()` 会先用当前猜测的 $E^{n+1/2}$ 更新 WarpX 持有的电场，然后调用 `PreRHSOp()`；后者定义在 `Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`，完成：

1. 以当前中间场推进粒子位置和速度；
2. 形成 $J^{n+1/2}$；
3. 按需要合并 `current_fp_non_suborbit`、mass-matrix 或 JFNK 线性阶段贡献；
4. 做 RZ/柱/球几何的逆体积缩放；
5. 调用 `SyncCurrentAndRho()`，把源项整理后交给隐式 RHS 或 Jacobian。

这条链中的 `PushParticlesandDeposit()` 可能在多个 nonlinear iteration、Jacobian evaluation 和 particle Picard iteration 中重复出现，但这些重复并不代表多个物理时间步。它们是在同一个 $t^n -> t^{n+1}$ 问题上，对不同中间场猜测重新计算离散残差。

implicit 还有两个容易误读的实现边界：

- `CumulateJ()` 必须在 `SyncCurrentAndRho()` 之前，把 mass-matrix 路径之外的 `J` 贡献合入 `current_fp`；否则同步的是不完整源项。
- `m_use_mass_matrices_jacobian` 和 `m_particle_suborbits` 会让 Jacobian 阶段只推进 suborbit 粒子或直接用 `ComputeJfromMassMatrices()` 构造电流，因而不能假定每次 RHS 都走同一个粒子 kernel。

这也解释了为什么 implicit 的验证不能只复制显式 Langmuir 的“单步场误差”判据。至少要分别检查：非线性求解是否收敛、粒子最终状态是否只提交一次、RHS 期间的 source synchronization 是否完整，以及最终 $E/B$ 时间层是否与 `FinishImplicitParticleUpdate()` 一致。

### 3.11.2 nonlinear solver、JFNK 与 mass-matrix：`J` 的三种构造层

`ImplicitSolver::parseNonlinearSolverParams()` 定义在 `Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`。它首先读取 `nonlinear_solver`，再决定后续 `J` 是通过完整粒子响应、Newton/JFNK 近似，还是 PETSc SNES 的线性阶段构造：

| 配置 | solver 对象 | 粒子/电流路径 | 关键边界 |
| --- | --- | --- | --- |
| `picard` | `PicardSolver` | 每次 RHS 直接用当前场推进粒子并沉积 `J` | `parseNonlinearSolverParams()` 将 `max_particle_iterations=1`、`particle_tolerance=0` 设为最小 Picard 路径 |
| `newton` | `NewtonSolver` | 非线性外层配合 JFNK；可选 particle suborbits 与 mass-matrix Jacobian | `use_mass_matrices_jacobian` 和 `use_mass_matrices_pc` 只能在该类 solver 中启用 |
| `petsc_snes` | `PETScSNES` | 由 PETSc 管理 nonlinear/linear solve，仍复用 `PreRHSOp()` 构造源项 | 必须以 `AMREX_USE_PETSC` 编译，否则源码直接 abort |

在普通 nonlinear RHS 阶段，`PreRHSOp()` 的电流来源可以概括为完整粒子响应：

$$
J = J_{\mathrm{particle}} + J_{\mathrm{non\text{-}suborbit}}.
$$

但在使用 mass matrices 的 Jacobian 阶段，源码采用的是线性化响应：

$$
J(E_0+\delta E)
=J_{\mathrm{suborbit}}+J_0+M\,\delta E,
$$

其中 $E_0$ 是 Newton step 开始时由 `SaveE()` 保存的电场，$J_0$ 是以 $E_0$ 推进的非 mass-matrix 粒子电流，$M$ 是 `MassMatrices_X/Y/Z` 表示的离散响应算子。这个式子正是 `CumulateJ()` 和 `ComputeJfromMassMatrices()` 之间的职责分界：

- `CumulateJ()` 把 `current_fp_non_suborbit` 加回当前 `current_fp`，补上不在 mass matrices 中的粒子贡献；
- `ComputeJfromMassMatrices()` 根据当前 `E-E0`、`J0` 和各方向交叉响应，把 $M\,\delta E$ 写入 `current_fp`；
- `SyncCurrentAndRho()` 只负责之后的滤波、边界、guard/level 通信，不负责判断 `J` 应该由完整粒子还是线性响应产生。

`ComputeJfromMassMatrices()` 还必须处理 Yee/nodal staggering。源码先根据 `Jx/Jy/Jz` 的 `ixType()` 计算 `offset_xx ... offset_zz`，再用 `Sxx/Sxy/.../Szz` 的多分量 stencil 访问邻近电场。因此 mass matrix 不是一个可以在任意 centering 上直接相乘的标量系数；它同时编码了方向耦合、空间 support 和网格位置偏移。把它简写成 $M=\partial J/\partial E$ 只足以说明物理意图，不足以替代对 index type 和 component offset 的源码核对。

配置层也有明确的几何限制：参数检查拒绝在 3D 启用 `use_mass_matrices_jacobian`，拒绝在 RSPHERE 使用 mass matrices；`mass_matrices_pc_width` 只在非 3D 情况下读取。因而这条路径不能被描述成所有 implicit geometry 的通用加速开关。

最后，`particle_suborbits` 改变的是粒子响应如何被拆分，而不是外层物理时间步。在线性 Jacobian 阶段，若启用 suborbit，`PreRHSOp()` 可以只推进 suborbit 粒子并用 `ComputeJfromMassMatrices(J_from_MM_only)` 补齐响应；若未启用，则由 mass matrices 直接构造线性阶段的 `J`。这正是 implicit 验证必须同时记录 solver 类型、particle suborbit、mass-matrix 开关和最终 source gate 的原因。

## 3.12 参数示例与最小运行闭环

如果把本章压成一个最小、可执行、可回查的演化入口，可从下面的官方回归案例开始：

- `Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`

输入文件直接消费了本章讲到的一组顶层参数：

- `max_step = 80`
- `algo.current_deposition = esirkepov`
- `algo.field_gathering = energy-conserving`
- `warpx.cfl = 0.8`
- 周期场边界

这里需要避免一个常见误读：这个输入 **没有** 显式设置 `algo.maxwell_solver`。因此它不能用于证明某个 solver 参数由该输入给出；实际采用的默认 solver 必须回到所用版本的 `ReadParameters()` 与官方文档确认。

它成为可执行案例，是因为 `Examples/Tests/langmuir/CMakeLists.txt` 把它注册为 `test_1d_langmuir_multi`：一维、2 个 MPI rank，分析命令为 `analysis_1d.py diags/diag1000080`。也就是说，`max_step = 80` 只规定步数；最终 plotfile 名称和分析入口来自 CMake 注册，不能单凭步数猜出。

对本章来说，这个案例最重要的意义不是“Langmuir 物理本身”，而是它把主循环连接到明确的消费端。对于这个显式电磁、无 AMR 的输入，主路径是：

```text
main.cpp
-> WarpX::GetInstance()
-> InitData()
-> ComputeDt()
-> Evolve()
-> OneStep()
-> PushParticlesandDeposit()
-> SyncCurrentAndRho()
-> EvolveB/EvolveE/EvolveB
-> diagnostics
```

分析脚本 `analysis_1d.py` 读取最终 plotfile，按解析的 Langmuir 波重建 $E_z$，并要求最大相对误差满足

$$
\max\left|E_{z,\mathrm{sim}}-E_{z,\mathrm{theory}}\right|/
\max\left|E_{z,\mathrm{theory}}\right| < 0.05.
$$

随后它还调用 `check_charge_conservation(data)`。对这个 Esirkepov、非 PSATD、非 RZ 的案例，辅助分析会检查离散 Gauss-law 残差；这补充了场形状的比较，但不等同于证明所有几何、所有 solver 或 AMR 分支的守恒性。

这样，`inputs_test_1d_langmuir_multi` 把本章的“主循环入口”压成一个可复现的闭环：

- 有参数入口：输入文件
- 有测试编排：`test_1d_langmuir_multi` 的 CMake 注册与 2-rank 规模
- 有明确消费端：`analysis_1d.py diags/diag1000080`
- 有两类检查：$E_z$ 解析误差阈值和离散 Gauss-law 残差

这条路线把 `WarpX` 主类生命周期和 `Evolve()` 主链从静态调用图连接到输入、输出和可检查的物理量。它只覆盖这个 Langmuir 配置，不能据此推出所有 solver、几何或 AMR 分支都已验证。

## 3.13 进一步阅读与练习

进一步阅读：

1. [第 4 章：粒子推进器](04-particle-pushers.md)：继续从 `PushParticlesandDeposit()` 进入 `mypc->Evolve()` 和粒子推进器。
2. [第 5 章：沉积与形函数](05-deposition-shapes.md)：继续展开 `SyncCurrentAndRho()`、沉积、guard/source synchronization。
3. 对 lifecycle、subcycling/JRhom 与 moving window 三条分支，继续分别追问：状态在哪个时间层更新、哪些网格层参与、以及结果应通过哪个 observable 判断。

练习题：

1. 说明为什么 `WarpX::WarpX()` 里只能创建跨-level 外壳，而不能直接分配完整 `MultiFab` 主字段。
2. 用本章的 `StoreCurrent()/RestoreCurrent()` 解释：为什么 subcycling 不能简单拿 fine current 覆盖 coarse current。
3. 结合本章的 Langmuir 案例，指出 `inputs_test_1d_langmuir_multi` 中哪些参数分别进入 `ReadParameters()`、`ComputeDt()` 和 `OneStep_nosub()` 的不同层次。
4. **案例闭环题。** 阅读该输入、`Examples/Tests/langmuir/CMakeLists.txt` 和 `analysis_1d.py`，写出四行表格：输入参数、测试规模、分析命令、通过条件。解释为什么 `max_step = 80` 不能单独推出输出目录或通过阈值，并说明两类检查各自能与不能支持什么结论。

## 3.14 本章小结

本章建立的主演化路线可压缩为五个读者检查点。它们按一个输入从启动到一次时间步的顺序排列，而不是按源码文件的出现顺序排列：

1. **启动与构造：** 从 `main.cpp` 进入 `GetInstance()`、`WarpX::WarpX()` 和 `ReadParameters()`。先问哪些参数与 solver 分支在建立网格前已经确定。
2. **初始化：** 依次检查 `InitData()`、`ComputeDt()`、`InitFromScratch()` 或 `InitFromCheckpoint()`。确认初始 level、粒子、场、PML 和 diagnostics 在第一步前已就绪。
3. **外层推进：** 在 `Evolve()` 中核对 callback、负载均衡、注入、边界与诊断分别发生在单步前还是单步后。
4. **单步分派：** 在 `OneStep()` 中判断该输入实际走 implicit、electrostatic/HybridPIC、`OneStep_nosub()`、subcycling 还是 JRhom。
5. **显式主链：** 从 `PushParticlesandDeposit()` 到 `SyncCurrentAndRho()`，再到 `PushPSATD()` 或 `EvolveB/EvolveE/EvolveB`，确认粒子输运、源项同步和场推进的时间层相容。

### 跨章交接卡：从调用图保留到可验证的状态

第 3 章的调用图只说明控制流进入了哪些阶段；它不能替代后续章节对变量、时间层和 observable 的定义。读者从本章进入初始化、推进、沉积和诊断时，至少应保留下面四项信息：

| 交接问题 | 本章已经定位的入口 | 下一章必须继续确认的内容 | 不能直接推出的结论 |
|---|---|---|---|
| 输入动量在什么单位下被解释？ | `ReadParameters()`、species/injector 配置 | 输入中的 `gamma*beta`、容器中的 `gamma*v` 与 diagnostics metadata 的差异，见附录 A | 同一个 `ux/uy/uz` 数值在输入、粒子数组和输出中可直接互换 |
| 第一个物理时间步前有哪些状态？ | `InitData()`、`InitFromScratch()` / `InitFromCheckpoint()` | 第 3A 章中的 level、field、PML、external field、species 与 diagnostics 初始化顺序 | 一次对象分配或 writer 创建就证明初态的物理约束已满足 |
| 显式粒子轨迹怎样变成 solver source？ | `PushParticlesandDeposit()`、`mypc->Evolve()`、`SyncCurrentAndRho()` | 第 4、5 章中的 \(\mathbf{x}^n\)、\(\mathbf{u}^{n-1/2}\)、\(\mathbf{J}^{n+1/2}\)、old/new \(\rho\) 以及 AMR/边界同步 | 任意 `rho` 或 `current_*` 数组都已经是场求解器消费的最终源项 |
| 怎样判断这条路径可信？ | `Evolve()`、`OneStep()` 与 diagnostics 调度 | 第 6--8 章中的 solver 前提、边界条件、producer/consumer、reference 和 observable | 程序完成、文件写出或 checksum 一致就证明物理结论 |

因此，跨章阅读时可把一条输入压缩成下列核查链：

```text
输入量纲与配置
-> InitData 创建的离散初态
-> 一个时间步内的粒子/源项/场时间层
-> 同步后由 solver 消费的状态
-> 有独立 reference 的 observable
```

这张交接卡的用途是防止两类常见跳步：把输入参数的语义直接当成内部数组语义，或把控制流命中和输出文件存在直接当成物理验证。后续章节必须分别补全这条链上的离散公式、实现分派和可检验的证据。
