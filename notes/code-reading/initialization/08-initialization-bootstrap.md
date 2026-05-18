# `WarpXAMReXInit` / `WarpXInit`：初始化启动层

绑定源码：

- `../warpx/Source/main.cpp`
- `../warpx/Source/Initialization/WarpXAMReXInit.H`
- `../warpx/Source/Initialization/WarpXAMReXInit.cpp`
- `../warpx/Source/Initialization/WarpXInit.H`
- `../warpx/Source/Initialization/WarpXInit.cpp`
- `../warpx/Source/WarpX.cpp`

绑定文档：

- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/developers/warning_logger.rst`

前面的 `Initialization` 笔记大多从 `WarpX::InitData()` 往后讲，这一篇补的是更早的一层：在真正进入 `InitData()` 之前，WarpX 怎样完成 MPI / AMReX / FFT / PETSc 启动、怎样改写 AMReX 默认参数、怎样把 `geometry.dims` 与可执行文件维度对齐、以及 moving window 与 warning manager 这些“全局运行时语义”到底在哪个阶段锁定。

## 1. 顶层启动顺序

`main.cpp` 的最外层顺序非常短：

```cpp
int
main (int argc, char* argv[]) {
    warpx::initialization::initialize_external_libraries(argc, argv);
    {
        auto& warpx = WarpX::GetInstance();
        warpx.InitData();
        warpx.Evolve();
        WarpX::Finalize();
    }
    warpx::initialization::finalize_external_libraries();
}
```

因此，`Initialization/` 启动层的真正职责不是“生成初始粒子”，而是先把外部库和全局运行时环境建立起来，让后面的 `WarpX::GetInstance()`、`InitData()`、`Evolve()` 有一套合法的 communicator、geometry parser、GPU/OMP 缺省值和 warning 行为。

## 2. `initialize_external_libraries()`：先 MPI，再 AMReX，再 FFT/PETSc

`WarpXInit.cpp` 把最外层初始化固定成：

```cpp
ablastr::parallelization::mpi_init(argc, argv);
warpx::initialization::amrex_init(argc, argv);
ablastr::math::anyfft::setup();
#ifdef AMREX_USE_PETSC
    PETSC_COMM_WORLD = amrex::ParallelContext::CommunicatorSub();
    PetscInitialize(&argc, &argv, nullptr, "WarpX with PETSc");
#endif
```

这里的语义边界很明确：

1. MPI 先于 AMReX。
2. AMReX 初始化之后，WarpX 才开始拥有 `ParmParse`、`Geometry`、`ParallelContext` 这些基础设施。
3. FFT 和 PETSc 不是 AMReX 的一部分，而是 WarpX 在 AMReX 之后追加初始化的外部库。

对应的收尾顺序完全反过来：

```cpp
#ifdef AMREX_USE_PETSC
    PetscFinalize();
#endif
ablastr::math::anyfft::cleanup();
amrex::Finalize();
ablastr::parallelization::mpi_finalize();
```

这说明 PETSc、FFT、AMReX、MPI 的生命周期边界在 WarpX 里是显式维护的，不是把所有初始化都丢给 `amrex::Initialize()`。

## 3. `amrex_init()` 的核心不是简单调用 `amrex::Initialize()`，而是先覆盖默认 parser 行为

`WarpXAMReXInit.cpp` 的真正入口是：

```cpp
amrex::Initialize(
    argc,
    argv,
    build_parm_parse,
    MPI_COMM_WORLD,
    ::overwrite_amrex_parser_defaults
);
```

也就是说，WarpX 把一个回调 `overwrite_amrex_parser_defaults` 注入到了 AMReX 初始化阶段。它不是等 AMReX 启动完再零散改参数，而是在构造 `ParmParse` 默认值时就直接改掉运行时缺省。

这个回调当前统一做了七件事：

1. `add_constants()`：向 parser 注入 `clight`、`epsilon0`、`mu0`、`q_e`、`m_e`、`m_p`、`pi` 等常量。
2. `override_default_abort_on_out_of_gpu_memory()`：把 `amrex.abort_on_out_of_gpu_memory` 的缺省改成更激进的 abort 行为。
3. `override_default_the_arena_is_managed()`：把 `amrex.the_arena_is_managed` 缺省改成 `false`。
4. `override_default_omp_threads()`：把 `amrex.omp_threads` 缺省从“system”改成 `"nosmt"`。
5. `apply_workaround_for_warpx_numprocs()`：若启用了 `warpx.numprocs` 域分解方案，就把 `amr.blocking_factor` 强行降到 1，避开 AMReX 对 blocking factor 整除性的断言。
6. `set_device_synchronization()`：把 `warpx.do_device_synchronize` 传到 `tiny_profiler.device_synchronize_around_region`。
7. `override_default_tiling_option_for_particles()`：GPU 下默认 `particles.do_tiling = false`，CPU 下默认 `true`。

这层非常关键，因为它解释了很多“明明输入文件没写，为什么运行行为已经不是 AMReX 默认值”的现象。

## 4. `geometry.is_periodic` 在 WarpX 里不是用户主入口，而是由 field/particle 边界反推出来的

`set_periodicity_according_to_boundary_types()` 做的不是直接读取用户 `geometry.is_periodic`，而是：

1. 先解析 `boundary.field_lo/hi`。
2. 再基于 field periodicity 解析 `boundary.particle_lo/hi`。
3. 最后合成一个 `geom_periodicity` 数组并写回 `geometry.is_periodic`。

核心逻辑是：

```cpp
if (field_boundary_lo[idim] == FieldBoundaryType::Periodic ||
    field_boundary_hi[idim] == FieldBoundaryType::Periodic ||
    particle_boundary_lo[idim] == ParticleBoundaryType::Periodic ||
    particle_boundary_hi[idim] == ParticleBoundaryType::Periodic ) {
        geom_periodicity[idim] = 1;
}
pp_geometry.addarr("is_periodic", geom_periodicity);
```

所以在 WarpX 里：

- 用户应当写的是 `boundary.field_*` 和 `boundary.particle_*`；
- `geometry.is_periodic` 只是内部供 `Geometry`、`FillBoundary`、通信层使用的派生量。

这也和前面 boundary 笔记里“field / particle periodic 必须一致”那条主线完全对上。

## 5. `prob_lo/prob_hi/n_cell` 会在 `amrex_post_initialize()` 里被预解析和回写

AMReX 自己不会替 WarpX 解析带表达式的几何输入，所以 `WarpXAMReXInit.cpp` 在 `amrex::Initialize()` 之后立刻执行：

```cpp
parse_geometry_input();
```

这里会对：

- `geometry.prob_lo`
- `geometry.prob_hi`

调用 `utils::parser::getArrWithParser(...)`，把表达式求值后再用 `pp_geometry.addarr(...)` 写回 parser。

同一个函数还会把 `amr.n_cell`、`max_grid_size*`、`blocking_factor*` 等整数数组也做预解析，并在必要时替换原始字符串版本。源码注释明确写了一个实际动机：`n_cell` 必须回写成解析后的数值形式，因为 `warpx_job_info` 会把它输出给 `yt`，而 `yt` 期待读到可直接解析的整数。

因此，这一层不只是“方便表达式输入”，而是在主动保证：

- 后续几何对象拿到的是实数/整数值；
- job info 和 reader 工具链不会再看到未展开的 parser 表达式。

## 6. `WarpX::MakeWarpX()` 是运行时语义锁定点，不只是单例工厂

`WarpX.cpp` 里的 `MakeWarpX()` 先后做：

```cpp
warpx::initialization::check_dims();
warpx::initialization::read_moving_window_parameters(...);
ConvertLabParamsToBoost();
parse_field_boundaries();
parse_particle_boundaries(...);
CheckGriddingForRZSpectral();
m_instance = new WarpX();
```

所以 `MakeWarpX()` 的语义比“new 一个单例”重得多。它在真正进入构造函数前就锁定了四类全局运行时事实：

1. 可执行文件维度和 `geometry.dims` 是否匹配。
2. moving window 是否开启、方向是什么、速度是多少。
3. field / particle 边界类型是什么。
4. RZ spectral 的 gridding 约束是否满足。

后面的 `WarpX` 构造函数再基于这些已经确定的全局变量去做 `ReadParameters()`、`InitEB()` 等动作。

## 7. `check_dims()`：把二进制编译维度和输入文件维度强绑定

`check_dims()` 先根据编译宏得到当前可执行文件对应的维度标签：

- `3`
- `2`
- `1`
- `RZ`
- `RCYLINDER`
- `RSPHERE`

然后读取 `geometry.dims`，最后直接：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(dims == dims_compiled, dims_error);
```

这意味着 `geometry.dims` 在 WarpX 里不是可选装饰项，而是二进制 ABI 级别的契约：

- 如果缺失，会报“请显式加上 `geometry.dims = ...`”；
- 如果和当前可执行文件不一致，会要求换可执行文件或重编译。

因此，WarpX 的“维度”不是运行时完全自由切换的，它首先受编译产物边界约束。

## 8. `read_moving_window_parameters()`：moving window 的运行时语义在构造前就已经确定

这个函数做的事情比单纯读几个参数更系统：

1. 先看 `warpx.do_moving_window` 是否开启。
2. 解析 `start_moving_window_step` 和 `end_moving_window_step`。
3. 把字符串方向 `x/y/z` 映射到整型 `moving_window_dir`。
4. 用 parser 读取 `moving_window_v`，再乘上 `c`。

也就是说，输入文件写的 `moving_window_v` 在这里还是一个“以光速为单位的无量纲数”，真正进入 `WarpX` 全局状态前才被转换成物理速度。

这也解释了为什么前面 evolve 笔记里 `MoveWindow()`、`ShiftGalileanBoundary()`、`GuardCellManager` 都直接消费：

- `do_moving_window`
- `moving_window_dir`
- `moving_window_v`

因为这些量在 `GetInstance()` 阶段就已经固定成了全局静态状态。

## 9. `initialize_warning_manager()`：warning 行为也是启动层语义，不是运行中临时选项

`WarpX` 构造函数一开始就调用：

```cpp
warpx::initialization::initialize_warning_manager();
```

它读取的不是数值算法参数，而是 warning policy：

- `warpx.always_warn_immediately`
- `warpx.abort_on_warning_threshold`

后者支持：

- `low`
- `medium`
- `high`

否则直接 abort。

这说明 WarpX 把 warning manager 视作运行时控制平面的一部分，而不是“日志美化”。它决定的是：

- warning 是不是一记录就打印；
- 某个优先级以上的 warning 是否直接升级成 abort。

这层和 `developers/warning_logger.rst` 里的设计说明正好对上。

## 10. 当前 `Initialization` 阶段的结构可以重新分成两层

到这里，`Initialization` 实际已经能清楚分成两大层：

### 启动层

- `main.cpp`
- `WarpXAMReXInit.*`
- `WarpXInit.*`
- `WarpX::MakeWarpX()`

它们负责：

- 外部库生命周期；
- AMReX parser 默认覆盖；
- 几何和 periodicity 预处理；
- 维度契约；
- moving window / warning policy 这类全局运行时语义。

### 初态构造层

- `WarpX::InitData()`
- `InitFromScratch()/InitFromCheckpoint()`
- `ExternalField.*`
- `PlasmaInjector.*`
- `SpeciesUtils.*`
- `AddParticles.cpp`
- `ProjectionDivCleaner.*`

它们负责：

- 真正生成 fields、particles、diagnostics 和初态约束修正。

前面的 0-7 号笔记主要都属于第二层；这一篇补上之后，`Initialization` 的前置启动边界也终于闭合了。
