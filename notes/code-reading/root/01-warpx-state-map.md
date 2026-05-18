# WarpX 主类状态图谱第一轮精读

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `Source/WarpX.H`、`Source/WarpX.cpp` 和 `Source/Fields.H`。目标不是一次性替代正式章节，而是建立后续逐行精读的总索引：`WarpX` 对象如何成为 AMReX 层级模拟的根对象，哪些物理和算法选择被保存为全局状态，哪些状态进入 `m_fields` 场寄存器，以及这些状态怎样控制初始化、演化和诊断。

## 1. `WarpX` 是 AMR 根对象和全局单例

源码位置：`../warpx/Source/WarpX.H:85-132`。

```cpp
class WARPX_EXPORT WarpX
    : public amrex::AmrCore
{
public:
    static WarpX& GetInstance ();

    static void ResetInstance ();

    /**
     * \brief
     * This method has to be called at the end of the simulation. It deletes the WarpX instance.
     */
    static void Finalize();

    /** Destructor */
    ~WarpX () override;

    /** Copy constructor */
    WarpX ( WarpX const &) = delete;
    /** Copy operator */
    WarpX& operator= ( WarpX const & ) = delete;

    /** Move constructor */
    WarpX ( WarpX && ) = delete;
    /** Move operator */
    WarpX& operator= ( WarpX && ) = delete;

    static std::string Version (); //!< Version of WarpX executable
    static std::string PicsarVersion (); //!< Version of PICSAR dependency

    [[nodiscard]] int Verbose () const { return verbose; }

    void InitData ();

    void Evolve (int numsteps = -1);
```

这段代码给出三个关键事实。

第一，`WarpX` 继承 `amrex::AmrCore`。因此网格层级、level 生命周期、regrid、DistributionMapping、`MakeNewLevelFromScratch()` 这类 AMR 入口，不是 WarpX 自己从零发明的框架，而是挂在 AMReX 的 `AmrCore` 生命周期上。

第二，`WarpX` 是单例。外部主程序不会到处创建多个 `WarpX` 实例，而是通过 `GetInstance()` 拿到全局模拟对象；复制和移动构造被删除，说明这个对象不是普通值对象，而是拥有场、粒子、诊断、PML、solver、EB 等大量全局资源的根控制器。

第三，面向外部的核心执行接口非常少：`InitData()` 负责把输入、网格、场、粒子和诊断初始化到一致状态；`Evolve()` 负责进入时间推进。这解释了为什么后续真正的代码阅读应围绕“构造/读参数/初始化 level/演化 step”四条路径展开。

## 2. 算法选择首先作为 `WarpX` 状态存在

源码位置：`../warpx/Source/WarpX.H:182-238`。

```cpp
// Algorithms
//! Integer that corresponds to the current deposition algorithm (Esirkepov, direct, Vay, Villasenor)
static inline auto current_deposition_algo = CurrentDepositionAlgo::Default;
//! Integer that corresponds to the charge deposition algorithm (only standard deposition)
static inline auto charge_deposition_algo = ChargeDepositionAlgo::Default;
//! Integer that corresponds to the field gathering algorithm (energy-conserving, momentum-conserving)
static inline auto field_gathering_algo = GatheringAlgo::Default;
//! Integer that corresponds to the particle push algorithm (Boris, Vay, Higuera-Cary)
static inline auto particle_pusher_algo = ParticlePusherAlgo::Default;
//! Integer that corresponds to the type of Maxwell solver (Yee, CKC, PSATD, ECT)
static inline auto electromagnetic_solver_id = ElectromagneticSolverAlgo::Default;
//! Integer that corresponds to the evolve scheme (explicit, semi_implicit_em, theta_implicit_em)
EvolveScheme evolve_scheme = EvolveScheme::Default;
```

PIC 程序的“算法组合”在 WarpX 中不是散落在各个 kernel 里的字符串判断，而是先被解析成枚举状态：电流沉积、电荷沉积、场 gather、粒子 pusher、Maxwell solver、时间推进 scheme。这样做的直接后果是：后续粒子、场求解、同步和诊断模块都读取同一组状态，保证同一个输入文件不会在不同模块中被解释成不同算法。

这些状态的物理含义可以按 PIC loop 对应起来：

| 状态 | 对应物理/算法步骤 | 后续精读入口 |
|---|---|---|
| `particle_pusher_algo` | 从 Lorentz 方程离散推进粒子动量 | `Particles/Pusher/` |
| `field_gathering_algo` | 把网格场插值到粒子位置 | `Particles/Gather/` |
| `current_deposition_algo` | 把粒子运动沉积成电流源项 | `Particles/Deposition/` |
| `charge_deposition_algo` | 把粒子权重沉积成电荷密度 | `Particles/Deposition/` |
| `electromagnetic_solver_id` | 推进 Maxwell 方程 | `FieldSolver/` |
| `evolve_scheme` | 显式、半隐式、theta 隐式或谱隐式时间层 | `Evolve/`, `NonlinearSolvers/` |

边界条件也被保存为全局状态：

```cpp
static inline amrex::Array<FieldBoundaryType,AMREX_SPACEDIM> field_boundary_lo;
static inline amrex::Array<FieldBoundaryType,AMREX_SPACEDIM> field_boundary_hi;

static inline amrex::Array<ParticleBoundaryType,AMREX_SPACEDIM> particle_boundary_lo;
static inline amrex::Array<ParticleBoundaryType,AMREX_SPACEDIM> particle_boundary_hi;
```

这里要特别注意：场边界和粒子边界不是同一个物理对象。场边界约束 Maxwell/Poisson 更新和 guard cell 填充；粒子边界约束宏粒子越过物理边界后的吸收、反射、热发射或周期处理。正式正文中不能把 `boundary.field_*` 和 `boundary.particle_*` 混成一类。

## 3. `ReadParameters()` 同时完成参数读取和算法合法性约束

源码位置：`../warpx/Source/WarpX.cpp:547-1660`。

`WarpX::ReadParameters()` 的作用远超过“把输入文件读进变量”。第一轮阅读可把它分成八类：

| 代码区域 | 主要工作 |
|---|---|
| `547-733` | 主步数、停止时间、restart、Maxwell/electrostatic solver、boosted frame、moving window、external field |
| `740-781` | Poisson/magnetostatic solver 选择和 FFT/open-boundary 约束 |
| `796-865` | 时间步、滤波器、非笛卡尔几何下的 filter/PSATD 约束 |
| `891-912` | shared-memory deposition 和 GPU/维度限制 |
| `934-1035` | PML、Silver-Mueller、PML 内 divergence cleaning 约束 |
| `1055-1187` | refinement patch、grid type、hybrid grid、current centering |
| `1190-1387` | Maxwell solver、deposition、field gathering、implicit scheme 组合合法性 |
| `1389-1660` | load balance、particle shape、sorting、PSATD 阶数、JRhom、current correction |

一个典型例子是 electrostatic 模式会关闭 Maxwell solver：

```cpp
pp_warpx.query_enum_sloppy("do_electrostatic", electrostatic_solver_id, "-_");
// if an electrostatic solver is used, set the Maxwell solver to None
if (electrostatic_solver_id != ElectrostaticSolverAlgo::None) {
    electromagnetic_solver_id = ElectromagneticSolverAlgo::None;
}
```

这不是语法糖，而是物理模型选择：静电模式解的是 Poisson 或静电近似下的场，不再推进全套电磁 Maxwell 方程。因此后续章节讲 `algo.maxwell_solver` 时必须说明它可能被 `warpx.do_electrostatic` 这类更高层模型选择覆盖。

另一个关键例子是 current centering：

```cpp
pp_warpx.query("do_current_centering", do_current_centering);
if (do_current_centering)
{
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        grid_type == GridType::Hybrid,
        "warpx.do_current_centering=1 can be used only with warpx.grid_type=hybrid");

    utils::parser::queryWithParser(
        pp_warpx, "current_centering_nox", m_current_centering_nox);
    utils::parser::queryWithParser(
        pp_warpx, "current_centering_noy", m_current_centering_noy);
    utils::parser::queryWithParser(
        pp_warpx, "current_centering_noz", m_current_centering_noz);
```

这里的物理/数值含义是：hybrid grid 允许电流先沉积到 nodal 网格，再有限阶中心化到 staggered 网格。它不是一般网格都能打开的选项，因为电流所在位置必须和 Maxwell solver 使用的离散 curl 结构一致，否则离散连续性和场更新源项会失配。

PSATD/JRhom 相关解析说明 `ReadParameters()` 也负责谱算法的时间模型：

```cpp
std::string JRhom_input;
pp_psatd.query("JRhom", JRhom_input);
if (!JRhom_input.empty()) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        JRhom_input.length() >= 3,
        "psatd.JRhom = '" + JRhom_input + "' input string is too short to parse."
    );
    m_JRhom = true;
    // parse time dependency of J from first character
    if (JRhom_input[0] == 'C') {
        time_dependency_J = TimeDependencyJ::Constant;
    }
    else if (JRhom_input[0] == 'L') {
        time_dependency_J = TimeDependencyJ::Linear;
    }
    else if (JRhom_input[0] == 'Q') {
        time_dependency_J = TimeDependencyJ::Quadratic;
    }
```

`JRhom` 不是一个普通开关，而是同时编码 `J` 的时间依赖、`rho` 的时间依赖和子区间数 `m`。这会改变后续 `OneStep_JRhom()`、电流/电荷沉积次数、谱空间源项更新和 `rho_fp` 组件数。后续正式章节要把这个输入字符串拆成时间积分公式，而不能只翻译参数说明。

## 4. 成员状态按物理职责分组

源码位置：`../warpx/Source/WarpX.H:1157-1614`。

```cpp
//! Author of an input file / simulation setup
std::string m_authors;

amrex::Vector<int> istep;      // which step?
amrex::Vector<int> nsubsteps;  // how many substeps on each level?

amrex::Vector<amrex::Real> t_new;
amrex::Vector<amrex::Real> t_old;
amrex::Vector<amrex::Real> dt;
utils::parser::IntervalsParser m_dt_update_interval = utils::parser::IntervalsParser{}; // How often to update the timestep when using adaptive timestepping

bool m_safe_guard_cells = false;

// Particle container
std::unique_ptr<MultiParticleContainer> mypc;
std::unique_ptr<MultiDiagnostics> multi_diags;
```

这段状态把“时间层”和“子系统对象”放在同一个根对象中。`istep/t_old/t_new/dt` 是 AMR 多层时间推进的全局时钟；`mypc` 是所有粒子 species 的容器；`multi_diags` 管理诊断输出。也就是说，`WarpX` 不是某个物理求解器本身，而是一个调度器和状态总线：它让粒子、场、边界、诊断在同一套时间层和网格层级上工作。

可把 `WarpX` 成员状态先归为以下类别：

| 类别 | 代表成员 | 解释 |
|---|---|---|
| 时间与 AMR 层级 | `istep`, `nsubsteps`, `t_new`, `t_old`, `dt` | 每个 refinement level 的步数、旧/新时间和时间步长 |
| 粒子和诊断 | `mypc`, `multi_diags`, `m_particle_thermalizer` | species、碰撞/热化、输出诊断 |
| 流体和介质 | `do_fluid_species`, `myfl`, `m_em_solver_medium`, `m_macroscopic_solver_algo` | fluid species 和 macroscopic Maxwell 介质 |
| EB 和边界掩码 | `m_eb_update_E/B`, `m_eb_reduce_particle_shape`, `m_flag_info_face` | 嵌入边界对场更新、粒子 shape、ECT solver 的影响 |
| AMR buffer | `current_buffer_masks`, `gather_buffer_masks` | refinement patch 附近的沉积/gather buffer 区域 |
| PML | `pml_ncell`, `do_pml_in_domain`, `pml`, `pml_rz` | 吸收层厚度、位置、PML 对象 |
| 外场/移动窗口 | `m_p_ext_field_params`, `moving_window_x`, `m_mirror_z` | 外部场、移动窗口、反射镜 |
| 场求解器 | `spectral_solver_fp/cp`, `m_fdtd_solver_fp/cp`, `m_electrostatic_solver` | 细 patch/粗 patch 的具体 field solver |
| 隐式/矩阵状态 | `m_implicit_solver`, `m_JRhom`, mass matrix 相关字段 | 隐式 EM 或谱源项时间模型 |

这张表是后续精读 `WarpX.H` 私有成员的路线图。每个成员都应最终回到“谁分配它、谁写它、谁读它、它对应哪个物理量或数值约束”四个问题。

## 5. `m_fields` 是场数据的总注册表

源码位置：`../warpx/Source/WarpX.H:934-942`，`../warpx/Source/Fields.H:20-155`。

```cpp
#ifdef WARPX_USE_FFT
    auto&  get_spectral_solver_fp (int lev) {return *spectral_solver_fp[lev];}
#endif

    FiniteDifferenceSolver * get_pointer_fdtd_solver_fp (int lev) { return m_fdtd_solver_fp[lev].get(); }

    // Field container
    ablastr::fields::MultiFabRegister m_fields;
    ablastr::fields::MultiFabRegister& GetMultiFabRegister() {return m_fields;}
```

`m_fields` 是理解 WarpX 场数据的核心。早期代码常用很多成员数组直接保存 `Efield_fp`、`Bfield_fp` 等；当前源码把标量场和矢量场统一放进 `ablastr::fields::MultiFabRegister`，再用 `FieldType` 枚举索引。

`Fields.H` 中的注释已经给出第一层语义：

```cpp
AMREX_ENUM(FieldType,
    None,
    Efield_aux, /**< Field that the particles gather from. Obtained from Efield_fp (and Efield_cp when using MR); see UpdateAuxilaryData */
    Bfield_aux, /**< Field that the particles gather from. Obtained from Bfield_fp (and Bfield_cp when using MR); see UpdateAuxilaryData */
    Efield_fp,  /**< The field that is updated by the field solver at each timestep */
    Bfield_fp,  /**< The field that is updated by the field solver at each timestep */
    Efield_fp_external, /**< Stores grid particle fields provided by the user as  through an openPMD file */
    Bfield_fp_external, /**< Stores grid particle fields provided by the user as  through an openPMD file */
    current_fp, /**< The current that is used as a source for the field solver */
    current_fp_nodal, /**< Only used when using nodal current deposition */
    current_fp_vay,   /**< Only used when using Vay current deposition */
    current_buf, /**< Particles that are close to the edge of the MR patch (i.e. in the deposition buffer) deposit to this field. */
```

最重要的命名规律：

| 后缀/字段 | 含义 |
|---|---|
| `_fp` | fine patch，即当前 level 的主网格数据 |
| `_cp` | coarse patch，即 refinement level 内用于 AMR 接口处理的粗 patch 数据 |
| `_aux` | 粒子实际 gather 的全解场，可能是主场 alias，也可能由 fine/coarse patch 合成 |
| `_cax` | coarse aux 的拷贝，供 refinement patch 边缘粒子 gather |
| `_buf` | refinement patch 边缘沉积 buffer |
| `_avg_*` | 时间平均场，常见于 PSATD 时间平均输出或 gather |
| `pml_*` | PML 内部场和源项 |
| `*_external` | 从 openPMD 或输入定义读入的外部场 |

矢量场由 `ArrayFieldTypes` 指定：

```cpp
constexpr FieldType ArrayFieldTypes[] = {
    FieldType::Efield_aux,
    FieldType::Bfield_aux,
    FieldType::Efield_fp,
    FieldType::Bfield_fp,
    FieldType::current_fp,
    FieldType::current_fp_nodal,
    FieldType::current_fp_vay,
    FieldType::current_buf,
    FieldType::current_store,
    FieldType::vector_potential_fp,
```

这解释了为什么有些 `m_fields.get()` 需要 `Direction{0/1/2}`，有些标量场如 `rho_fp`、`phi_fp` 不需要方向。后续讲源码时，必须先判断某个 `FieldType` 是标量还是矢量，否则很容易误读 `m_fields.get(FieldType::rho_fp, lev)` 和 `m_fields.get(FieldType::Efield_fp, Direction{0}, lev)` 的签名差异。

## 6. `AllocLevelData()` 把抽象算法选择落到 MultiFab 分配

源码位置：`../warpx/Source/WarpX.cpp:2271-3050`。

AMReX 新建一个 level 时，WarpX 通过 `MakeNewLevelFromScratch()` 调用 `AllocLevelData()` 和 `InitLevelData()`：

```cpp
void
WarpX::MakeNewLevelFromScratch (int lev, Real time, const BoxArray& new_grids,
                                const DistributionMapping& new_dmap)
{
    AllocLevelData(lev, new_grids, new_dmap);
    InitLevelData(lev, time);
}
```

`AllocLevelData()` 的第一层动作是按当前 grid staggering 给主场和源项分配 fine patch：

```cpp
m_fields.alloc_init(FieldType::Bfield_fp, Direction{0}, lev, amrex::convert(ba, Bx_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
m_fields.alloc_init(FieldType::Bfield_fp, Direction{1}, lev, amrex::convert(ba, By_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
m_fields.alloc_init(FieldType::Bfield_fp, Direction{2}, lev, amrex::convert(ba, Bz_nodal_flag), dm, ncomps, ngEB, 0.0_rt);

m_fields.alloc_init(FieldType::Efield_fp, Direction{0}, lev, amrex::convert(ba, Ex_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
m_fields.alloc_init(FieldType::Efield_fp, Direction{1}, lev, amrex::convert(ba, Ey_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
m_fields.alloc_init(FieldType::Efield_fp, Direction{2}, lev, amrex::convert(ba, Ez_nodal_flag), dm, ncomps, ngEB, 0.0_rt);

m_fields.alloc_init(FieldType::current_fp, Direction{0}, lev, amrex::convert(ba, jx_nodal_flag), dm, ncomps, ngJ, 0.0_rt);
m_fields.alloc_init(FieldType::current_fp, Direction{1}, lev, amrex::convert(ba, jy_nodal_flag), dm, ncomps, ngJ, 0.0_rt);
m_fields.alloc_init(FieldType::current_fp, Direction{2}, lev, amrex::convert(ba, jz_nodal_flag), dm, ncomps, ngJ, 0.0_rt);
```

这段代码体现了 Yee/staggered/collocated/hybrid grid 的核心：`Ex/Ey/Ez`、`Bx/By/Bz`、`Jx/Jy/Jz` 并不必然定义在同一种 index type 上，而是由 `*_nodal_flag` 决定。物理上这是离散 Maxwell 方程中 curl 算子的几何位置；代码上就是 `amrex::convert(ba, flag)` 生成不同 staggered BoxArray。

`rho_fp` 的分配由 solver 和校正策略决定：

```cpp
if (WarpX::electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD) {
    if (do_dive_cleaning || update_with_rho || current_correction) {
        // For the PSATD-JRhom algorithm we can allocate only one rho component (no distinction between old and new)
        rho_ncomps = (WarpX::m_JRhom) ? ncomps : 2*ncomps;
    }
}
if (rho_ncomps > 0)
{
    m_fields.alloc_init(FieldType::rho_fp,
        lev, amrex::convert(ba, rho_nodal_flag), dm,
        rho_ncomps, ngRho, 0.0_rt);
}
```

这里的 `2*ncomps` 对应旧/新电荷密度时间层；而 `JRhom` 路径只分配一个组件，因为源项时间依赖由 JRhom 模型编码。这个差异会影响 `DepositCharge()`、`SyncCurrentAndRho()` 和 PSATD 源项更新。

`Efield_aux/Bfield_aux` 是粒子 gather 的场，而不是总是独立分配的场：

```cpp
if (aux_is_nodal and grid_type != GridType::Collocated)
{
    // Create aux multifabs on Nodal Box Array
    BoxArray const nba = amrex::convert(ba,IntVect::TheNodeVector());

    m_fields.alloc_init(FieldType::Bfield_aux, Direction{0}, lev, nba, dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::Bfield_aux, Direction{1}, lev, nba, dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::Bfield_aux, Direction{2}, lev, nba, dm, ncomps, ngEB, 0.0_rt);

    m_fields.alloc_init(FieldType::Efield_aux, Direction{0}, lev, nba, dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::Efield_aux, Direction{1}, lev, nba, dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::Efield_aux, Direction{2}, lev, nba, dm, ncomps, ngEB, 0.0_rt);
} else if (lev == 0) {
    if (WarpX::fft_do_time_averaging) {
        m_fields.alias_init(FieldType::Bfield_aux, FieldType::Bfield_avg_fp, Direction{0}, lev, 0.0_rt);
```

对物理解释最重要的是这句话：场求解器推进的是 `Efield_fp/Bfield_fp`，粒子看到的是 `Efield_aux/Bfield_aux`。在最简单的 level 0、无特殊平均、无 nodal gather 情况下，aux 可以只是 fp 的 alias；但在 AMR、momentum-conserving gather、时间平均或外场读入时，aux 可能是重新分配或合成后的场。

对于 refinement level，WarpX 还要分配 coarse patch 和 buffer：

```cpp
if (lev > 0)
{
    BoxArray cba = ba;
    cba.coarsen(refRatio(lev-1));
    const std::array<Real,3> cdx = CellSize(lev-1);

    // Create the MultiFabs for B
    m_fields.alloc_init(FieldType::Bfield_cp, Direction{0}, lev, amrex::convert(cba, Bx_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::Bfield_cp, Direction{1}, lev, amrex::convert(cba, By_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
    m_fields.alloc_init(FieldType::Bfield_cp, Direction{2}, lev, amrex::convert(cba, Bz_nodal_flag), dm, ncomps, ngEB, 0.0_rt);
```

这就是 AMR PIC 复杂性的入口：同一个 `lev` 不只有一套 fine patch 主场，还可能有 coarse patch、coarse aux 拷贝、current buffer、rho buffer、gather/current masks。后续讲 AMR 时，必须围绕这些 field types 解释 coarse-fine 接口处的 gather、deposition、同步和守恒误差。

## 7. 第一轮结论

本轮对根层的理解可以压缩成一条主线：

```text
输入参数
  -> WarpX::ReadParameters() 解析为算法/边界/网格/solver 状态
  -> AMReX AmrCore 生命周期创建 level
  -> WarpX::AllocLevelData() 按这些状态分配 m_fields、solver、mask、PML、buffer
  -> InitLevelData() 写入初始场和粒子
  -> Evolve()/OneStep() 在同一套状态和 field registry 上推进 PIC loop
```

后续阶段 1 还需要继续补齐三件事：

1. 逐段展开 `WarpX::WarpX()` 构造函数：哪些子系统在构造期创建，哪些延后到 level 分配。
2. 逐段展开 `AllocLevelData()` 的 EB、PML、hybrid、implicit mass matrix 和 effective potential 分支。
3. 把本笔记回填到 `manuscript/chapters/03-warpx-evolve.md`，作为 `WarpX` 主类状态图和 field registry 小节。
