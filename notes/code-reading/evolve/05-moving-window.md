# Moving window 精读：窗口坐标、网格平移、连续注入与 boosted frame

绑定源码：`../warpx`，分支 `pkuHEDPbranch`，commit `063f8b586f04321e13150ae3e730e0794ca75cb1`。

本笔记覆盖 `../warpx/Source/Utils/WarpXMovingWindow.cpp`，并对照 `WarpX.cpp`、`WarpX.H`、`Evolve/WarpXEvolve.cpp`、`Initialization/WarpXInit.cpp` 和官方参数文档。它回答阶段 3 的第二个问题：WarpX 的 moving window 不是简单移动坐标轴，而是在每个时间步末尾维护一个连续窗口位置；当连续位移跨过整数网格宽度时，才整体平移场数组、PML、div-cleaner 标量、rho、流体量，并在新露出的物理区域做连续粒子/流体注入。

## 1. 物理图像：为什么需要 moving window

许多 laser-plasma accelerator 或束流等离子体问题中，真正有强相互作用的区域跟随激光脉冲或相对论束团向前传播。如果在实验室系固定网格上模拟整个传播长度，计算域必须覆盖从入口到出口的全部空间；moving window 的思想是让计算盒跟随相互作用区移动，只保留局域窗口。

在 WarpX 中，moving window 沿一个网格方向 `dir` 运动。设窗口实验室系速度为

$$
v_w = \texttt{warpx.moving\_window\_v}\,c.
$$

若没有 boosted-frame，连续窗口左边界的目标位置满足

$$
x_w^{n+1}=x_w^n+v_w\Delta t.
$$

若使用 boosted-frame，窗口速度也要做相对论速度变换。代码使用

$$
v'_w =
\frac{v_w-\beta_b c}{1-v_w\beta_b/c},
$$

其中 $\beta_b c$ 是模拟坐标系相对实验室系的 boost 速度。因此代码中的连续窗口坐标更新为

$$
x_w^{n+1}=x_w^n+
\frac{v_w-\beta_b c}{1-v_w\beta_b/c}\Delta t.
$$

关键点是：`moving_window_x` 是连续坐标；AMReX `Geometry` 和 `MultiFab` 数据只在跨过整数个 cell 时平移。这样可以避免每步做小数格插值，从而保持 PIC 网格量的离散结构。

## 2. 官方参数与初始化入口

官方参数文档位置：`../warpx/Docs/source/usage/parameters.rst:653-676`。

```rst
.. pp:param:: warpx.do_moving_window
    :type: ``integer``
    :default: 0

    Whether to use a moving window for the simulation

.. pp:param:: warpx.moving_window_dir
    :type: either ``x``, ``y`` or ``z``

    The direction of the moving window.

.. pp:param:: warpx.moving_window_v
    :type: ``float``

    The speed of moving window, in units of the speed of light
    (i.e. use ``1.0`` for a moving window that moves exactly at the speed of light)

.. pp:param:: warpx.start_moving_window_step
    :type: ``integer``
    :default: 0

    The timestep at which the moving window starts.

.. pp:param:: warpx.end_moving_window_step
    :type: ``integer``
    :default: ``-1`` for false

    The timestep at which the moving window ends.
```

参数读取在 `../warpx/Source/Initialization/WarpXInit.cpp:116-154`：

```cpp
void warpx::initialization::read_moving_window_parameters(
    int& do_moving_window, int& start_moving_window_step, int& end_moving_window_step,
    [[maybe_unused]] int& moving_window_dir, amrex::Real& moving_window_v)
{
    const amrex::ParmParse pp_warpx("warpx");
    pp_warpx.query("do_moving_window", do_moving_window);
    if (do_moving_window) {
        utils::parser::queryWithParser(
            pp_warpx, "start_moving_window_step", start_moving_window_step);
        utils::parser::queryWithParser(
            pp_warpx, "end_moving_window_step", end_moving_window_step);
        std::string s;
        pp_warpx.get("moving_window_dir", s);

        if (s == "z" || s == "Z") {
#ifdef WARPX_ZINDEX
            moving_window_dir = WARPX_ZINDEX;
#endif
        }
#if defined(WARPX_DIM_3D)
        else if (s == "y" || s == "Y") {
            moving_window_dir = 1;
        }
#endif
#if defined(WARPX_DIM_XZ) || defined(WARPX_DIM_3D)
        else if (s == "x" || s == "X") {
            moving_window_dir = 0;
        }
#endif
        else {
            WARPX_ABORT_WITH_MESSAGE("Unknown moving_window_dir: "+s);
        }

        utils::parser::getWithParser(
            pp_warpx, "moving_window_v", moving_window_v);
        moving_window_v *= PhysConst::c;
    }
}
```

逐块解释：

- `do_moving_window` 是总开关。
- `start_moving_window_step` 和 `end_moving_window_step` 控制窗口生效步数。
- `moving_window_dir` 受编译维度限制。1D-Z 中物理 z 方向的数组索引不是 3D 的 `2`，而是由 `WARPX_ZINDEX` 抽象。
- 用户输入的 `moving_window_v` 是以光速为单位的无量纲数；读取后立即乘以 `PhysConst::c`，后续源码内部使用 SI 速度。

`MakeWarpX()` 在创建单例之前调用这个读取函数。源码位置：`../warpx/Source/WarpX.cpp:274-280`。

```cpp
warpx::initialization::read_moving_window_parameters(
    do_moving_window, start_moving_window_step, end_moving_window_step,
    moving_window_dir, moving_window_v);
```

`WarpX::ReadParameters()` 中进一步做几何合法性检查。源码位置：`../warpx/Source/WarpX.cpp:705-717`。

```cpp
if (do_moving_window)
{
#if defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
    WARPX_ABORT_WITH_MESSAGE("Moving window not supported with RCYLINDER and RSPHERE");
    moving_window_dir = 0;
#endif
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
        Geom(0).isPeriodic(moving_window_dir) == 0,
        "The problem must be non-periodic in the moving window direction");
    moving_window_x = geom[0].ProbLo(moving_window_dir);
}
```

这段给出两个重要边界：

- RCYLINDER 和 RSPHERE 不支持 moving window。
- moving window 方向必须非周期。物理上，moving window 代表新物理区域进入计算域；若该方向周期，则“新区域”会和旧区域周期连接，语义冲突。

## 3. active 判定：生效步数的闭开边界

`WarpX.H` 中保存 moving window 的静态状态，并定义 active 判定。源码位置：`../warpx/Source/WarpX.H:752-765`。

```cpp
static int do_moving_window; // boolean
static int start_moving_window_step; // the first step to move window
static int end_moving_window_step; // the last step to move window
/** Returns true if the moving window is active for the provided step
 *
 * @param step time step
 * @return true if active, else false
 */
static int moving_window_active (int const step) {
    bool const step_before_end = (step < end_moving_window_step) || (end_moving_window_step < 0);
    bool const step_after_start = (step >= start_moving_window_step);
    return do_moving_window && step_before_end && step_after_start;
}
static int moving_window_dir;
static amrex::Real moving_window_v;
```

因此 active 区间是

$$
\texttt{start\_moving\_window\_step}\le n < \texttt{end\_moving\_window\_step},
$$

而 `end_moving_window_step < 0` 表示没有终止步。`MoveWindow(step+1, ...)` 的调用会用下一步编号判断，因为窗口移动发生在本步完成后、进入下一步状态之前。

## 4. 初始连续注入位置

构造 `MultiParticleContainer` 之后，`WarpX::WarpX()` 会给每个粒子/激光容器设置当前注入面位置。源码位置：`../warpx/Source/WarpX.cpp:354-372`。

```cpp
mypc = std::make_unique<MultiParticleContainer>(this);

// Loop over species (particles and lasers)
// and set current injection position per species
if (do_moving_window){
    const int n_containers = mypc->nContainers();
    for (int i=0; i<n_containers; i++)
    {
        WarpXParticleContainer& pc = mypc->GetParticleContainer(i);

        // Storing injection position for all species, regardless of whether
        // they are continuously injected, since it makes looping over the
        // elements of current_injection_position easier elsewhere in the code.
        if (moving_window_v > 0._rt)
        {
            // Inject particles continuously from the right end of the box
            pc.m_current_injection_position = geom[0].ProbHi(moving_window_dir);
        }
        else if (moving_window_v < 0._rt)
        {
            // Inject particles continuously from the left end of the box
            pc.m_current_injection_position = geom[0].ProbLo(moving_window_dir);
        }
```

这不是立刻注入粒子，而是建立“连续注入面的初始位置”：

- 窗口向正方向运动，新网格从高端进入，所以从 `ProbHi(dir)` 注入。
- 窗口向负方向运动，新网格从低端进入，所以从 `ProbLo(dir)` 注入。
- 即使某个 species 不做 continuous injection，也保留这个标量，方便后续统一循环。

## 5. 主循环调用点

`MoveWindow()` 在全局时间步完成主要场粒子推进之后调用。源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:240-270`。

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

// Update the accelerator lattice element finder if the window has moved,
// from either a moving window or a boosted frame
if (num_moved != 0 || gamma_boost > 1) {
    for (int lev = 0; lev <= finest_level; ++lev) {
        m_accelerator_lattice[lev]->UpdateElementFinder(lev, gett_new());
    }
}

HandleParticlesAtBoundaries(step, cur_time, num_moved);
```

调用顺序含义：

1. 本步推进完成，`cur_time` 增加。
2. 若使用 Galilean 坐标，先更新 Galilean 边界。
3. 更新时间层数组 `t_old/t_new`。
4. `MoveWindow(step+1, move_j)` 尝试移动窗口。
5. 若窗口或 boosted frame 改变了几何关系，更新 accelerator lattice finder。
6. 再处理粒子边界、连续通量注入和 scraping。

`HandleParticlesAtBoundaries()` 中还有连续通量注入。源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:710-717`。

```cpp
void WarpX::HandleParticlesAtBoundaries (int step, amrex::Real cur_time, int num_moved)
{
    mypc->ContinuousFluxInjection(cur_time, dt[0]);

    ExecutePythonCallback("particlescraper");

    mypc->ApplyBoundaryConditions();
```

这和 moving-window continuous injection 不是同一件事：

- moving-window continuous injection 是新网格单元进入计算域时填充体分布。
- `ContinuousFluxInjection` 是从定义平面连续注入粒子通量。

## 6. `MoveWindow()` 第一段：连续坐标到整数 cell shift

`MoveWindow()` 开头做 active 判定、连续坐标更新、注入面更新和整数平移数计算。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:356-397`。

```cpp
int
WarpX::MoveWindow (const int step, bool move_j)
{
    ABLASTR_PROFILE("WarpX::MoveWindow");

    using ablastr::fields::Direction;
    using warpx::fields::FieldType;

    bool const skip_lev0_coarse_patch = true;

    if (step == start_moving_window_step) {
        amrex::Print() << Utils::TextMsg::Info("Starting moving window");
    }
    if (step == end_moving_window_step) {
        amrex::Print() << Utils::TextMsg::Info("Stopping moving window");
    }
    if (!moving_window_active(step)) { return 0; }

    // Update the continuous position of the moving window,
    // and of the plasma injection
    moving_window_x += (moving_window_v - WarpX::beta_boost * PhysConst::c)/(1 - moving_window_v * WarpX::beta_boost / PhysConst::c) * dt[0];
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

这里有两个坐标尺度：

- `moving_window_x` 是连续窗口目标位置。
- `current_lo[dir]` 是当前 AMReX 几何左边界。
- `(moving_window_x-current_lo[dir])/dx` 的整数部分给出需要移动几个 base-level cell。

若 `num_shift_base == 0`，说明连续窗口还没有跨过一个完整 cell，网格数组保持不变。

这也是为什么 moving window 可以和常规 PIC 时间步兼容：粒子/场推进仍发生在静态网格上；只有在步末把计算域整体平移整数 cell。

## 7. `UpdateInjectionPosition()`：从 bulk momentum 到注入面速度

moving window 前沿的新物理区域不一定静止。若等离子体有 bulk velocity，注入面的位置要跟随该 bulk motion 更新。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:257-349`。

```cpp
void
UpdateInjectionPosition (
    MultiParticleContainer& mpc,
    const amrex::Real gamma_boost,
    const amrex::Real beta_boost,
    const amrex::Vector<int>& boost_direction,
    const int moving_window_dir,
    const amrex::Real a_dt)
{
    const int dir = moving_window_dir;

    // Loop over species (particles and lasers)
    const int n_containers = mpc.nContainers();
    for (int i=0; i<n_containers; i++)
    {
        WarpXParticleContainer& pc = mpc.GetParticleContainer(i);

        // Continuously inject plasma in new cells (by default only on level 0)
        if (pc.doContinuousInjection())
        {
            // Get bulk momentum and velocity of plasma
            // 1D: dir=0 is z
            // 2D: dir=0 is x, dir=1 is z
            // 3D: dir=0 is x, dir=1 is y, dir=2 is z
            amrex::Vector<amrex::Real> current_injection_position = {0._rt, 0._rt, 0._rt};
#if defined(WARPX_DIM_1D_Z)
            current_injection_position[2] = pc.m_current_injection_position;
#elif defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
            current_injection_position[0] = pc.m_current_injection_position;
#elif defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
            current_injection_position[dir*2] = pc.m_current_injection_position;
#else // 3D
            current_injection_position[dir] = pc.m_current_injection_position;
#endif

            // This only uses the base plasma injector
            PlasmaInjector* plasma_injector = pc.GetPlasmaInjector(0);

            amrex::Real v_shift = 0._rt;
            if (plasma_injector != nullptr)
            {
                const amrex::XDim3 u_bulk = plasma_injector->getInjectorMomentumHost()->getBulkMomentum(
                    current_injection_position[0],
                    current_injection_position[1],
                    current_injection_position[2]);
#if defined(WARPX_DIM_1D_Z)
                amrex::Vector<amrex::Real> u_bulk_vec = {u_bulk.z};
#elif defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
                amrex::Vector<amrex::Real> u_bulk_vec = {u_bulk.x};
#elif defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
                amrex::Vector<amrex::Real> u_bulk_vec = {u_bulk.x, u_bulk.z};
#else // 3D
                amrex::Vector<amrex::Real> u_bulk_vec = {u_bulk.x, u_bulk.y, u_bulk.z};
#endif
                v_shift = PhysConst::c * u_bulk_vec[dir] / std::sqrt(1._rt + u_bulk_vec[dir]*u_bulk_vec[dir]);
            }
```

`getBulkMomentum()` 返回的是归一化动量

$$
u=\gamma\beta=\frac{p}{mc}.
$$

从 $u$ 到速度的关系是

$$
\gamma=\sqrt{1+u^2},\qquad
\beta=\frac{u}{\sqrt{1+u^2}},\qquad
v=c\frac{u}{\sqrt{1+u^2}}.
$$

这正是源码中的

```cpp
v_shift = PhysConst::c * u_bulk_vec[dir] / std::sqrt(1._rt + u_bulk_vec[dir]*u_bulk_vec[dir]);
```

boosted-frame 变换继续在同一函数中完成：

```cpp
            // In boosted-frame simulations, the plasma has moved since the last
            // call to this function, and injection position needs to be updated.
            // Note that the bulk velocity v, obtained from getBulkMomentum, is
            // transformed to the boosted frame velocity v' via the formula
            // v' = (v-c*beta)/(1-v*beta/c)
            if (gamma_boost > 1._rt)
            {
                v_shift = (v_shift - PhysConst::c*beta_boost)
                        / (1._rt - v_shift*beta_boost/PhysConst::c);
#if defined(WARPX_DIM_3D)
                v_shift *= boost_direction[dir];
#elif defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
                // In 2D, dir=0 corresponds to x and dir=1 corresponds to z.
                // This needs to be converted to access boost_direction,
                // which has always 3 components.
                v_shift *= boost_direction[2*dir];
#elif defined(WARPX_DIM_1D_Z)
                // In 1D, dir=0 corresponds to z.
                // This needs to be converted to access boost_direction,
                // which has always 3 components.
                v_shift *= boost_direction[2];
                amrex::ignore_unused(dir);
#elif defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
                // In 1D radial, dir=0 corresponds to x.
                // This needs to be converted to access boost_direction,
                // which has always 3 components.
                v_shift *= boost_direction[0];
                amrex::ignore_unused(dir);
#endif
            }

            // Update current injection position
            pc.m_current_injection_position += v_shift * a_dt;
        }
    }
}
```

因此注入面位置更新公式是

$$
x_{\mathrm{inj}}^{n+1}
=x_{\mathrm{inj}}^n+v'_{\mathrm{bulk},dir}\Delta t.
$$

这里的一个源码细节很重要：函数注释写明 “This only uses the base plasma injector”。也就是说，连续注入面速度由 `pc.GetPlasmaInjector(0)` 的 bulk momentum 决定；如果一个物种有多个注入源，moving-window 注入面推进并不会分别追踪每个源的速度。

## 8. 几何域整体平移

当 `num_shift_base != 0` 时，`MoveWindow()` 更新 AMReX 几何域。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:399-413`。

```cpp
// update the problem domain. Note the we only do this on the base level because
// amrex::Geometry objects share the same, static RealBox.
for (int i=0; i<AMREX_SPACEDIM; i++) {
    new_lo[i] = current_lo[i];
    new_hi[i] = current_hi[i];
}
new_lo[dir] = current_lo[dir] + num_shift_base * cdx[dir];
new_hi[dir] = current_hi[dir] + num_shift_base * cdx[dir];

ResetProbDomain(amrex::RealBox(new_lo, new_hi));
```

这说明 WarpX 不直接重建所有网格对象，而是通过 `ResetProbDomain()` 修改共享的 `RealBox`。base level 的 shift 数会在 AMR level 中按 refinement ratio 放大：

```cpp
int num_shift      = num_shift_base;
int num_shift_crse = num_shift;

// Shift the mesh fields
for (int lev = 0; lev <= finest_level; ++lev) {

    if (lev > 0) {
        num_shift_crse = num_shift;
        num_shift *= refRatio(lev-1)[dir];
    }
```

如果 level 1 相对 level 0 在 moving-window 方向细化比为 $r$，base level 移动 1 个 cell，则 fine level 的数组移动 $r$ 个 fine cells。

## 9. `shiftMF()`：MultiFab 数据如何平移

`shiftMF()` 是真正移动网格量的底层 helper。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:55-120`。

```cpp
void shiftMF (
    amrex::MultiFab& mf, const amrex::Geometry& geom,
    int num_shift, int dir,
    bool safe_guard_cells, bool do_single_precision_comms,
    amrex::LayoutData<amrex::Real>* cost,
    amrex::Real external_field=0.0, bool useparser = false,
    amrex::ParserExecutor<3> const& field_parser={},
    const bool PMLRZ_flag = false)
{
    using namespace amrex::literals;
    ABLASTR_PROFILE("warpx::shiftMF()");
    const amrex::BoxArray& ba = mf.boxArray();
    const amrex::DistributionMapping& dm = mf.DistributionMap();
    const int nc = mf.nComp();
    const amrex::IntVect& ng = mf.nGrowVect();

    AMREX_ALWAYS_ASSERT(ng[dir] >= std::abs(num_shift));

    amrex::MultiFab tmpmf(ba, dm, nc, ng);
    amrex::MultiFab::Copy(tmpmf, mf, 0, 0, nc, ng);

    if ( safe_guard_cells ) {
        // Fill guard cells.
        ablastr::utils::communication::FillBoundary(tmpmf, do_single_precision_comms, geom.periodicity());
    } else {
        amrex::IntVect ng_mw = amrex::IntVect::TheUnitVector();
        // Enough guard cells in the MW direction
        ng_mw[dir] = std::abs(num_shift);
        // Make sure we don't exceed number of guard cells allocated
        ng_mw = ng_mw.min(ng);
        // Fill guard cells.
        ablastr::utils::communication::FillBoundary(tmpmf, ng_mw, do_single_precision_comms, geom.periodicity());
    }
```

第一层逻辑：

- 要移动的 `MultiFab` 先复制到 `tmpmf`。
- 要求 moving-window 方向 guard cell 数至少覆盖本次 shift 的 cell 数。
- safe mode 会填所有 guard cells；普通模式至少填 moving-window 方向需要的数据。

然后代码建立“新露出区域”的盒子：

```cpp
// Make a box that covers the region that the window moved into
const amrex::IndexType& typ = ba.ixType();
const amrex::Box& domainBox = geom.Domain();
amrex::Box adjBox;
if (num_shift > 0) {
    adjBox = adjCellHi(domainBox, dir, ng[dir]);
} else {
    adjBox = adjCellLo(domainBox, dir, ng[dir]);
}
adjBox = amrex::convert(adjBox, typ);

for (int idim = 0; idim < AMREX_SPACEDIM; ++idim) {
    if (idim == dir and typ.nodeCentered(dir)) {
        if (num_shift > 0) {
            adjBox.growLo(idim, -1);
        } else {
            adjBox.growHi(idim, -1);
        }
    } else if (idim != dir) {
        adjBox.growLo(idim, ng[idim]);
        adjBox.growHi(idim, ng[idim]);
    }
}
```

这里必须考虑 index type：

- cell-centered 量和 node-centered 量的物理坐标不在同一点。
- 如果 moving-window 方向是 nodal，临界面上会多一个节点；代码用 `growLo/growHi` 修正新区域盒子的范围。
- 非 moving-window 方向需要覆盖 guard cells，因为平移后边缘 guard 区也要有一致数据。

新区域初始化有两种路径。常量外场路径：

```cpp
const amrex::Box& outbox = mfi.growntilebox() & adjBox;

if (outbox.ok()) {
    if (!useparser) {
        AMREX_PARALLEL_FOR_4D ( outbox, nc, i, j, k, n,
        {
            srcfab(i,j,k,n) = external_field;
        })
    } else {
```

parser 外场路径需要按 staggered index type 算真实坐标：

```cpp
amrex::ParallelFor (outbox, nc,
    [=] AMREX_GPU_DEVICE (int i, int j, int k, int n) noexcept
{
    // Compute x,y,z co-ordinates based on index type of mf
#if defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
    const amrex::Real fac_x = (1.0_rt - mf_type[0]) * dx[0]*0.5_rt;
    const amrex::Real x = i*dx[0] + real_box.lo(0) + fac_x;
    const amrex::Real y = 0.0;
    const amrex::Real fac_z = (1.0_rt - mf_type[1]) * dx[1]*0.5_rt;
    const amrex::Real z = j*dx[1] + real_box.lo(1) + fac_z;
#else
    const amrex::Real fac_x = (1.0_rt - mf_type[0]) * dx[0]*0.5_rt;
    const amrex::Real x = i*dx[0] + real_box.lo(0) + fac_x;
    const amrex::Real fac_y = (1.0_rt - mf_type[1]) * dx[1]*0.5_rt;
    const amrex::Real y = j*dx[1] + real_box.lo(1) + fac_y;
    const amrex::Real fac_z = (1.0_rt - mf_type[2]) * dx[2]*0.5_rt;
    const amrex::Real z = k*dx[2] + real_box.lo(2) + fac_z;
#endif
    srcfab(i,j,k,n) = field_parser(x,y,z);
});
```

`mf_type[d] = 1` 表示 nodal，`0` 表示 cell-centered。坐标偏移

$$
f_d=(1-\mathrm{mf\_type}_d)\frac{\Delta x_d}{2}
$$

保证 cell-centered 数据在 cell 中心取 parser，nodal 数据在节点取 parser。

最后才执行数组平移。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:180-190`。

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

数学上，这是

$$
F_{\mathrm{new}}(\mathbf{i})=
F_{\mathrm{old}}(\mathbf{i}+\mathbf{s}),
\qquad
\mathbf{s}=N_{\mathrm{shift}}\hat e_{\mathrm{dir}}.
$$

当 `num_shift > 0` 时，窗口向正方向移动，高端是新区域，旧数据整体向低索引搬移；读取源索引 `i+shift` 正好体现这一点。

## 10. 哪些场会被平移

`MoveWindow()` 对每个 AMR level 平移多个 field registry 条目。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:442-618`。

电磁场、平均场、电流和 PML：

```cpp
// Shift each component of vector fields (E, B, j)
for (int dim = 0; dim < 3; ++dim) {
    // Fine grid
    amrex::ParserExecutor<3> Bfield_parser;
    amrex::ParserExecutor<3> Efield_parser;
    bool use_Bparser = false;
    bool use_Eparser = false;
    if (m_p_ext_field_params->B_ext_grid_type ==
            ExternalFieldType::parse_ext_grid_function) {
        use_Bparser = true;
        if (dim == 0) { Bfield_parser = m_p_ext_field_params->Bxfield_parser->compile<3>(); }
        if (dim == 1) { Bfield_parser = m_p_ext_field_params->Byfield_parser->compile<3>(); }
        if (dim == 2) { Bfield_parser = m_p_ext_field_params->Bzfield_parser->compile<3>(); }
    }
    if (m_p_ext_field_params->E_ext_grid_type ==
            ExternalFieldType::parse_ext_grid_function) {
        use_Eparser = true;
        if (dim == 0) { Efield_parser = m_p_ext_field_params->Exfield_parser->compile<3>(); }
        if (dim == 1) { Efield_parser = m_p_ext_field_params->Eyfield_parser->compile<3>(); }
        if (dim == 2) { Efield_parser = m_p_ext_field_params->Ezfield_parser->compile<3>(); }
    }
    ::shiftMF(*m_fields.get(FieldType::Bfield_fp, Direction{dim}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev,
        m_p_ext_field_params->B_external_grid[dim], use_Bparser, Bfield_parser);
    ::shiftMF(*m_fields.get(FieldType::Efield_fp, Direction{dim}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev,
        m_p_ext_field_params->E_external_grid[dim], use_Eparser, Efield_parser);
    if (fft_do_time_averaging) {
        ablastr::fields::MultiLevelVectorField Efield_avg_fp = m_fields.get_mr_levels_alldirs(FieldType::Efield_avg_fp, finest_level);
        ablastr::fields::MultiLevelVectorField Bfield_avg_fp = m_fields.get_mr_levels_alldirs(FieldType::Bfield_avg_fp, finest_level);
        ::shiftMF(*Bfield_avg_fp[lev][dim], geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev,
            m_p_ext_field_params->B_external_grid[dim], use_Bparser, Bfield_parser);
        ::shiftMF(*Efield_avg_fp[lev][dim], geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev,
           m_p_ext_field_params-> E_external_grid[dim], use_Eparser, Efield_parser);
    }
    if (move_j) {
        ::shiftMF(*m_fields.get(FieldType::current_fp, Direction{dim}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
    }
```

这里有三个算法细节：

- `Efield_fp/Bfield_fp` 的新区域可以由外场常量或 parser 初始化。
- 若使用 FFT time averaging，对平均场也做同样平移。
- `current_fp` 只有 `move_j` 为真时才平移；主循环注释说明这是为了同步状态下下一步能用正确的 `j` 推进 `E` 半步。

AMR coarse patch、aux field、PML coarse patch 也被处理：

```cpp
if (lev > 0) {
    // coarse grid
    ::shiftMF(*m_fields.get(FieldType::Bfield_cp, Direction{dim}, lev), geom[lev-1], num_shift_crse, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev,
        m_p_ext_field_params->B_external_grid[dim], use_Bparser, Bfield_parser);
    ::shiftMF(*m_fields.get(FieldType::Efield_cp, Direction{dim}, lev), geom[lev-1], num_shift_crse, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev,
        m_p_ext_field_params->E_external_grid[dim], use_Eparser, Efield_parser);
    ::shiftMF(*m_fields.get(FieldType::Bfield_aux, Direction{dim}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
    ::shiftMF(*m_fields.get(FieldType::Efield_aux, Direction{dim}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
```

div-cleaner 标量 `F/G` 和 PML 中的 `F/G` 也要平移：

```cpp
// Shift scalar field F with div(E) cleaning in valid domain
if (m_fields.has(FieldType::F_fp, lev))
{
    // Fine grid
    ::shiftMF(*m_fields.get(FieldType::F_fp, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
    if (lev > 0)
    {
        // Coarse grid
        ::shiftMF(*m_fields.get(FieldType::F_cp, lev), geom[lev-1], num_shift_crse, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
    }
}

// Shift scalar field G with div(B) cleaning in valid domain
if (m_fields.has(FieldType::G_fp, lev))
{
    // Fine grid
    ::shiftMF(*m_fields.get(FieldType::G_fp, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
    if (lev > 0)
    {
        // Coarse grid
        ::shiftMF(*m_fields.get(FieldType::G_cp, lev), geom[lev-1], num_shift_crse, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
    }
}
```

`rho` 也跟随 `move_j`：

```cpp
// Shift scalar component rho
if (move_j) {
    if (m_fields.has(FieldType::rho_fp, lev)) {
        // Fine grid
        ::shiftMF(*m_fields.get(FieldType::rho_fp,lev),   geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
        if (lev > 0){
            // Coarse grid
            ::shiftMF(*m_fields.get(FieldType::rho_cp,lev), geom[lev-1], num_shift_crse, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev);
        }
    }
}
```

流体 species 的 `N` 和 `NU` 同样平移：

```cpp
// Shift values of N, NU for each fluid species
if (do_fluid_species) {
    const int n_fluid_species = myfl->nSpecies();
    for (int i=0; i<n_fluid_species; i++) {
        WarpXFluidContainer const& fl = myfl->GetFluidContainer(i);
        ::shiftMF( *m_fields.get(fl.name_mf_N, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev );
        ::shiftMF( *m_fields.get(fl.name_mf_NU, Direction{0}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev );
        ::shiftMF( *m_fields.get(fl.name_mf_NU, Direction{1}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev );
        ::shiftMF( *m_fields.get(fl.name_mf_NU, Direction{2}, lev), geom[lev], num_shift, dir, m_safe_guard_cells, do_single_precision_comms, cost_lev );
    }
}
```

所以 moving window 的状态迁移覆盖的是完整计算状态，而不是只移动 `E/B` 两个数组。若某个场量没有同步移动，下一步 PIC loop 的 Maxwell 更新、沉积、诊断和边界条件就会在不同坐标系中读写数据。

## 11. 连续粒子注入：只填新露出的整数 cell 区域

网格域平移后，新区域必须生成背景粒子。`WarpXParticleContainer` 的接口说明在 `../warpx/Source/Particles/WarpXParticleContainer.H:429-444`：

```cpp
// If particles start outside of the domain, ContinuousInjection
// makes sure that they are initialized when they enter the domain, and
// NOT before. Virtual function, overriden by derived classes.
// Current status:
// PhysicalParticleContainer: implemented.
// LaserParticleContainer: implemented.
// RigidInjectedParticleContainer: not implemented.
virtual void ContinuousInjection(const amrex::RealBox& /*injection_box*/) {}

/**
 * \brief Update antenna position for continuous injection of lasers
 *        in a boosted frame. Empty function for containers other than lasers.
 */
virtual void UpdateAntennaPosition(const amrex::Real /*dt*/) {}

bool doContinuousInjection() const {return do_continuous_injection;}
```

`MoveWindow()` 中真正构造注入盒子。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:620-660`。

```cpp
// Loop over species (particles and lasers)
const int n_containers = mypc->nContainers();
for (int i=0; i<n_containers; i++)
{
    WarpXParticleContainer& pc = mypc->GetParticleContainer(i);

    // Continuously inject plasma in new cells (by default only on level 0)
    if (pc.doContinuousInjection())
    {
        const int lev = 0;

        // particleBox encloses the cells where we generate particles
        // (only injects particles in an integer number of cells,
        // for correct particle spacing)
        amrex::RealBox particleBox = geom[lev].ProbDomain();
        amrex::Real new_injection_position = pc.m_current_injection_position;
        if (moving_window_v > 0._rt)
        {
            // Forward-moving window
            const amrex::Real dx = geom[lev].CellSize(dir);
            new_injection_position = pc.m_current_injection_position +
                std::floor( (geom[lev].ProbHi(dir) - pc.m_current_injection_position)/dx ) * dx;
        }
        else if (moving_window_v < 0._rt)
        {
            // Backward-moving window
            const amrex::Real dx = geom[lev].CellSize(dir);
            new_injection_position = pc.m_current_injection_position -
                std::floor( (pc.m_current_injection_position - geom[lev].ProbLo(dir))/dx) * dx;
        }
        // Modify the corresponding bounds of the particleBox
        if (moving_window_v > 0._rt)
        {
            particleBox.setLo( dir, pc.m_current_injection_position );
            particleBox.setHi( dir, new_injection_position );
        }
        else if (moving_window_v < 0._rt)
        {
            particleBox.setLo( dir, new_injection_position );
            particleBox.setHi( dir, pc.m_current_injection_position );
        }

        if (particleBox.ok() and (pc.m_current_injection_position != new_injection_position)){
            // Performs continuous injection of all WarpXParticleContainer
            // in mypc.
            pc.ContinuousInjection(particleBox);
            pc.m_current_injection_position = new_injection_position;
        }
    }
}
```

这里的 `floor(.../dx)*dx` 是物理正确性和数值一致性的关键。它保证每次只在整数个 cell 宽度上创建粒子，从而保持 `num_particles_per_cell` 对应的采样 spacing。若直接从连续位置注入到窗口边界，会产生半格或非整数宽度注入层，规则粒子采样和权重归一化都更难保持一致。

对于正向窗口：

$$
x_{\mathrm{inj,new}}
=x_{\mathrm{inj}}+
\left\lfloor
\frac{x_{\mathrm{hi}}-x_{\mathrm{inj}}}{\Delta x}
\right\rfloor\Delta x.
$$

粒子生成区域是

$$
[x_{\mathrm{inj}},x_{\mathrm{inj,new}}].
$$

对负向窗口则反过来，生成区域是

$$
[x_{\mathrm{inj,new}},x_{\mathrm{inj}}].
$$

一个容易误读的细节是：`UpdateInjectionPosition()` 先按 plasma bulk velocity 移动 `m_current_injection_position`；这里再把它推进到最接近窗口边界的整数 cell 位置并注入。这两步共同表达“物理注入面随等离子体运动，但实际宏粒子创建只落在整格层中”。

## 12. 连续流体注入与宏观介质重算

流体 species 没有粒子采样盒，而是在新露出的网格节点上重新初始化 `N/NU`。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:662-690`。

```cpp
// Continuously inject fluid species in new cells (by default only on level 0)
const int lev = 0;
// Find box in which to initialize new fluid cells
amrex::Box injection_box = geom[lev].Domain();
injection_box.surroundingNodes(); // get nodal box
// Restrict box in the direction of the moving window, to only include the new cells
if (moving_window_v > 0._rt)
{
    injection_box.setSmall( dir, injection_box.bigEnd(dir) - num_shift_base + 1 );
}
else if (moving_window_v < 0._rt)
{
    injection_box.setBig( dir, injection_box.smallEnd(dir) + num_shift_base - 1 );
}
// Loop over fluid species, and fill the values of the new cells
if (do_fluid_species) {
    const int n_fluid_species = myfl->nSpecies();
    const amrex::Real cur_time = t_new[0];
    for (int i=0; i<n_fluid_species; i++) {
        WarpXFluidContainer& fl = myfl->GetFluidContainer(i);
        fl.InitData( m_fields, injection_box, cur_time, lev, geom[lev], gamma_boost, beta_boost);
    }
}
```

随后，如果电磁介质是 macroscopic medium，还要重新初始化介质属性。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:692-702`。

```cpp
// Recompute macroscopic properties of the medium
if (m_em_solver_medium == MediumForEM::Macroscopic) {
    const int lev_zero = 0;
    m_macroscopic_properties->InitData(
        Geom(lev_zero),
        m_fields.get(FieldType::Efield_fp, Direction{0}, lev_zero)->ixType().toIntVect(),
        m_fields.get(FieldType::Efield_fp, Direction{1}, lev_zero)->ixType().toIntVect(),
        m_fields.get(FieldType::Efield_fp, Direction{2}, lev_zero)->ixType().toIntVect()
    );
}
```

这解释了为什么 moving window 属于全局状态操作：它不仅改变 field 数组，还改变物理介质初始化区域。

## 13. Galilean boundary 与 moving window 的区别

同一文件中还有 `ShiftGalileanBoundary()`。源码位置：`../warpx/Source/Utils/WarpXMovingWindow.cpp:706-758`。

```cpp
void
WarpX::ShiftGalileanBoundary ()
{
    const amrex::Real cur_time = t_new[0];
    amrex::Real new_lo[AMREX_SPACEDIM];
    amrex::Real new_hi[AMREX_SPACEDIM];
    const amrex::Real* current_lo = geom[0].ProbLo();
    const amrex::Real* current_hi = geom[0].ProbHi();

    const amrex::Real time_shift = (cur_time - time_of_last_gal_shift);

#if defined(WARPX_DIM_3D)
        m_galilean_shift = {
            m_v_galilean[0]*time_shift,
            m_v_galilean[1]*time_shift,
            m_v_galilean[2]*time_shift };
#elif defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
        m_galilean_shift = {
            m_v_galilean[0]*time_shift,
            std::numeric_limits<amrex::Real>::quiet_NaN(),
            m_v_galilean[2]*time_shift };
#elif defined(WARPX_DIM_1D_Z)
        m_galilean_shift = {
            std::numeric_limits<Real>::quiet_NaN(),
            std::numeric_limits<Real>::quiet_NaN(),
            m_v_galilean[2]*time_shift };
#endif

#if defined(WARPX_DIM_3D)
        for (int i=0; i<AMREX_SPACEDIM; i++) {
            new_lo[i] = current_lo[i] + m_galilean_shift[i];
            new_hi[i] = current_hi[i] + m_galilean_shift[i];
        }
```

Galilean shift 和 moving window 都调用 `ResetProbDomain()`，但语义不同：

- Galilean boundary 表示以 Galilean 速度移动坐标参考框，重点服务于特定 field solver 的数值稳定性和相对漂移处理。
- moving window 表示计算盒追随物理相互作用区域，并且会平移 `MultiFab` 数据、PML、粒子/流体注入状态。

主循环里先调用 `ShiftGalileanBoundary()`，再调用 `MoveWindow()`。这意味着 moving window 的 `current_lo/current_hi` 已经包含 Galilean 边界更新后的几何域状态。

## 14. PML 与 subcycling 的特殊调用点

`WarpXEvolve.cpp` 中 PML 在 subcycling 场推进附近也会检查 moving window active。源码位置：`../warpx/Source/Evolve/WarpXEvolve.cpp:1248-1256`。

```cpp
if (do_pml) {
    if (moving_window_active(istep[0]+1)){
        // Exchange guard cells of PMLs only (0 cells are exchanged for the
        // regular B field MultiFab). This is required as B and F have just been
        // evolved.
        FillBoundaryB(coarse_lev, PatchType::fine, IntVect::TheZeroVector(),
                      WarpX::sync_nodal_points);
        FillBoundaryF(coarse_lev, PatchType::fine, IntVect::TheZeroVector(),
                      WarpX::sync_nodal_points);
    }
    DampPML(coarse_lev, PatchType::fine);
```

这说明 moving window 不只是步末数组平移；它还影响 PML guard exchange 的时序。因为 B 和 F 刚刚演化，moving window active 时需要在 PML damping 前保证 PML 数据交换一致。

## 15. 与 refined injection 的关系

`PhysicalParticleContainer::findRefinedInjectionBox()` 会在 moving window active 且使用 refined plasma continuous injection 时，缓存 refined injection box。源码位置：`../warpx/Source/Particles/PhysicalParticleContainer.cpp:1727-1748`。

```cpp
bool
PhysicalParticleContainer::findRefinedInjectionBox (amrex::Box& a_fine_injection_box, amrex::IntVect& a_rrfac)
{
    ABLASTR_PROFILE("PhysicalParticleContainer::findRefinedInjectionBox");

    // This does not work if the mesh is dynamic.  But in that case, we should
    // not use refined injected either.  We also assume there is only one fine level.
    static bool refine_injection = false;
    static Box fine_injection_box;
    static amrex::IntVect rrfac(AMREX_D_DECL(1,1,1));
    if (!refine_injection and WarpX::moving_window_active(WarpX::GetInstance().getistep(0)+1) and WarpX::refine_plasma and do_continuous_injection and numLevels() == 2) {
        refine_injection = true;
        fine_injection_box = ParticleBoxArray(1).minimalBox();
        fine_injection_box.setSmall(WarpX::moving_window_dir, std::numeric_limits<int>::lowest()/2);
        fine_injection_box.setBig(WarpX::moving_window_dir, std::numeric_limits<int>::max()/2);
        rrfac = m_gdb->refRatio(0);
        fine_injection_box.coarsen(rrfac);
    }
    a_fine_injection_box = fine_injection_box;
    a_rrfac = rrfac;
    return refine_injection;
}
```

这里的注释提醒：动态网格和 refined injection 不兼容。moving window 的连续注入路径假设 refined injection box 可以在一个 fine level 上缓存并沿窗口方向延伸；如果网格本身动态变化，这个静态缓存就不再可靠。

## 16. 本节调用链总结

moving window 的主链可以写成：

```text
Initialization/WarpXInit.cpp
  read_moving_window_parameters()
    -> WarpX::do_moving_window/start/end/dir/v

WarpX.cpp
  MakeWarpX()
    -> read_moving_window_parameters()
  WarpX::ReadParameters()
    -> reject unsupported geometry
    -> require non-periodic moving-window direction
    -> moving_window_x = ProbLo(dir)
  WarpX::WarpX()
    -> set pc.m_current_injection_position to ProbHi/ProbLo

Evolve/WarpXEvolve.cpp
  WarpX::Evolve()
    -> cur_time += dt[0]
    -> ShiftGalileanBoundary()
    -> MoveWindow(step+1, move_j)
      -> update continuous moving_window_x
      -> UpdateInjectionPosition()
      -> UpdateAntennaPosition()
      -> compute integer num_shift_base
      -> ResetProbDomain()
      -> shift E/B/current/PML/F/G/rho/fluid MultiFabs
      -> continuous particle injection into new cells
      -> continuous fluid initialization in new nodal cells
      -> macroscopic medium re-initialization
    -> HandleParticlesAtBoundaries()
```

物理上，它把三个速度概念分开：

- window speed `moving_window_v`：计算盒追随相互作用区的速度，用户以 `c` 为单位输入，源码内部转换为 SI。
- plasma bulk speed：由 injector 的 bulk momentum 计算，用于更新连续注入面位置。
- boosted-frame transformed speed：当 `gamma_boost>1` 时，window speed 和 plasma bulk speed都必须按相对论速度变换进入模拟坐标系。

数值上，它把两个位置概念分开：

- 连续位置：`moving_window_x` 和 `pc.m_current_injection_position`。
- 整数网格位置：`num_shift_base` 和 `new_injection_position`，只在完整 cell 层上移动数组与创建粒子。

这正是 PIC moving window 能保持离散 field/particle 结构的核心。

