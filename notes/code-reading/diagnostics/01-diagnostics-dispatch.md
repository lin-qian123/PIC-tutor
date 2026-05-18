# `MultiDiagnostics`、`Diagnostics`、`FullDiagnostics` 与 `ParticleDiag` 的调度骨架

绑定源码：

- `../warpx/Source/Diagnostics/MultiDiagnostics.H`
- `../warpx/Source/Diagnostics/MultiDiagnostics.cpp`
- `../warpx/Source/Diagnostics/Diagnostics.H`
- `../warpx/Source/Diagnostics/Diagnostics.cpp`
- `../warpx/Source/Diagnostics/FullDiagnostics.H`
- `../warpx/Source/Diagnostics/FullDiagnostics.cpp`
- `../warpx/Source/Diagnostics/ParticleDiag/ParticleDiag.H`
- `../warpx/Source/Diagnostics/ParticleDiag/ParticleDiag.cpp`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/ComputeParticleDiagFunctor.H`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormat.H`
- `../warpx/Source/Diagnostics/WarpXOpenPMD.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatPlotfile.cpp`

前一篇已经单独拆开了 `BoundaryScrapingDiagnostics`。这一篇回到 diagnostics 主干，只回答四个问题：

1. diagnostics 在 WarpX 主循环里是怎样被统一调度的；
2. `Diagnostics` 基类到底提供了哪些模板骨架；
3. `FullDiagnostics` 在字段和粒子两条线上分别补了什么；
4. `ParticleDiag` 是粒子 buffer，还是 species 输出配置对象。

## 1. `MultiDiagnostics` 只负责“建表和分派”，不负责具体字段或粒子算法

`MultiDiagnostics` 的构造函数先读：

```cpp
diagnostics.diags_names
```

再逐个读每个 `<diag>.diag_type`，把字符串映射到：

```cpp
DiagTypes {Full, BackTransformed, BoundaryScraping, TimeAveraged}
```

然后按类型实例化：

```cpp
if (diags_types[i] == DiagTypes::Full || diags_types[i] == DiagTypes::TimeAveraged) {
    alldiags[i] = std::make_unique<FullDiagnostics>(...);
} else if (diags_types[i] == DiagTypes::BackTransformed) {
    alldiags[i] = std::make_unique<BTDiagnostics>(...);
} else if (diags_types[i] == DiagTypes::BoundaryScraping) {
    alldiags[i] = std::make_unique<BoundaryScrapingDiagnostics>(...);
}
```

所以 `MultiDiagnostics` 的职责边界非常窄：

- 读 diagnostics 列表；
- 根据 `diag_type` 选子类；
- 在每一步把调用转发给这些子类。

它本身并不知道 `Ex` 怎么 cell-center，也不知道 species 粒子怎么过滤。

## 2. 主循环里真正的入口是 `NewIteration()` 和 `FilterComputePackFlush()`

`MultiDiagnostics` 提供的主要运行时接口有三个：

- `NewIteration()`
- `DoComputeAndPack(step)`
- `FilterComputePackFlush(step, force_flush, BackTransform)`

其中最关键的是：

```cpp
diag->FilterComputePackFlush(step, force_flush);
```

若 `BackTransform=false`，它会跳过 `BTDiagnostics`，只处理普通 diagnostics；若 `BackTransform=true`，则只处理 back-transformed diagnostics。

也就是说，WarpX 把：

- full / time-averaged / boundary-scraping
- back-transformed

这两大族在主循环层面已经分开调度。

## 3. `Diagnostics` 基类给出的不是“实现”，而是一套固定生命周期

`Diagnostics` 是真正的模板骨架类。它把 diagnostics 生命周期拆成：

1. 读参数和构造输出对象；
2. 初始化 field functors、particle handles、output buffers；
3. 每一步决定是否需要 compute/pack；
4. 每一步决定是否需要 flush；
5. 调用具体子类实现。

最关键的统一调度函数是：

```cpp
void Diagnostics::FilterComputePackFlush (int step, bool force_flush)
{
    MovingWindowAndGalileanDomainShift(step);

    if (DoComputeAndPack(step, force_flush)) {
        ComputeAndPack();
    }

    for (int i_buffer = 0; i_buffer < m_num_buffers; ++i_buffer) {
        if (!DoDump(step, i_buffer, force_flush)) { continue; }
        Flush(i_buffer, force_flush);
    }
}
```

这段骨架把 diagnostics 统一拆成三个阶段：

- 先更新 diagnostics 观测域的物理位置；
- 再决定要不要计算/打包；
- 最后逐个 buffer 决定要不要 flush。

因此后面的子类差异，本质上只是对这三个钩子函数的不同实现：

- `DoComputeAndPack`
- `DoDump`
- `Flush`

## 4. 初始化阶段的统一骨架：先 field functor，再 output buffer，再 species 句柄

`Diagnostics::InitData()` 的固定顺序是：

1. `InitBaseData()`
2. `DerivedInitData()`
3. 对每个 `i_buffer`、每个 level 调 `InitializeFieldFunctors(lev)`
4. 对输出 level 调 `InitializeBufferData(i_buffer, lev)`
5. 若 `write_species=1`，再调：
   - `InitializeParticleBuffer(mpc)`
   - `InitializeParticleFunctors()`

这里有个很重要的层次区别：

- `field functors` 是“如何从 simulation fields 计算 diagnostics 字段”；
- `buffer data` 是“把输出 `MultiFab/Geometry` 实际分配出来”；
- `particle buffer` 是“为 species 输出建立句柄或临时容器”。

这三件事在代码里是严格分开的。

## 5. `InitBaseData()` 真正做了四类公共资源分配

`InitBaseData()` 做的公共工作主要有四类。

第一，构造输出 writer：

```cpp
if (m_format == "plotfile") ...
else if (m_format == "checkpoint") ...
else if (m_format == "openpmd") ...
```

也就是说，每个 diagnostics 在初始化时就已经绑定了自己的 `FlushFormat` 实例。

第二，分配 field output buffer：

- `m_mf_output`
- `m_sum_mf_output`（仅 time-averaged）
- `m_geom_output`

第三，分配 species 输出槽位：

```cpp
m_output_species.resize(m_num_buffers);
```

第四，在 moving-window restart 场景里，提前把 `diag_lo/diag_hi` 平移到当前窗口位置。

因此 `InitBaseData()` 不涉及任何具体物理量；它做的是 diagnostics 运行时内存和 writer 框架搭建。

## 6. `ComputeAndPack()` 里字段和粒子的两条线是并排写的，但含义并不相同

统一执行函数是：

```cpp
void Diagnostics::ComputeAndPack ()
{
    PrepareBufferData();
    PrepareFieldDataForOutput();
    PrepareParticleDataForOutput();
    ...
    for (...) {
        m_all_field_functors[lev][icomp]->operator()(m_mf_output[i_buffer][lev], ...);
        ...
    }
    ...
    for (int isp = 0; isp < m_all_particle_functors.size(); ++isp) {
        m_all_particle_functors[isp]->operator()(*m_particles_buffer[i_buffer][isp], ...);
    }
}
```

这很容易让人误以为所有 diagnostics 都会同时：

- 计算 field output；
- 再 pack 一份 particle buffer。

但实际不是这样。

字段线对所有 diagnostics 都存在，因为 `m_all_field_functors` 是通用抽象。

粒子线只对“真的需要独立粒子 buffer 的 diagnostics”才生效，典型就是 `BTDiagnostics`。对普通 `FullDiagnostics`，`m_all_particle_functors` 默认是空的，这个 loop 根本不会运行。

## 7. 这意味着 `FullDiagnostics` 的粒子输出默认不是“先 pack 到 diagnostics 粒子缓冲区”

`FullDiagnostics` 只覆写了：

```cpp
void InitializeParticleBuffer (const MultiParticleContainer& mpc) override;
```

而没有覆写 `InitializeParticleFunctors()`。

它做的事只是：

```cpp
m_output_species[i_buffer].push_back(
    ParticleDiag(m_diag_name, species, mpc.GetParticleContainerPtr(idx))
);
```

也就是说，对 full diagnostics：

- `ParticleDiag` 直接指向 simulation 里的 species 容器；
- 没有额外的 `ComputeParticleDiagFunctor` 去先生成一份 diagnostics 专属 particle buffer；
- 粒子真正的过滤和变量裁剪发生在后面的 writer 里，而不是 `ComputeAndPack()` 里。

这和 `BTDiagnostics` 完全不同。`BTDiagnostics` 会显式分配：

- `m_particles_buffer`
- `m_totalParticles_in_buffer`
- `m_all_particle_functors`

然后用 `BackTransformParticleFunctor` 真正生成 snapshot 粒子缓冲区。

因此不能把 `FullDiagnostics` 和 `BTDiagnostics` 的粒子路径混为一谈。

## 8. `ParticleDiag` 更像“species 输出配置对象”，不是粒子数据容器

`ParticleDiag` 内部真正保存的是：

- `m_pc`：主 species 容器指针；
- `m_pinned_pc`：可选 pinned particle container 指针；
- `m_plot_flags`：哪些 real comps 要写；
- `m_plot_phi/Ex/Ey/...`：哪些额外场上粒子量要写；
- `m_do_random_filter`
- `m_do_uniform_filter`
- `m_do_parser_filter`
- `m_do_geom_filter`
- `m_random_fraction`
- `m_uniform_stride`
- `m_particle_filter_parser`
- `m_diag_domain`

这不是“粒子数组本身”，而是一组输出配置和过滤参数，再加上“从哪里取粒子”的句柄。

## 9. `ParticleDiag` 构造函数真正做了三类解析

第一类是变量选择。

如果 `<diag>.<species>.variables` 被指定，它会先把全部 `m_plot_flags` 清零，再只打开请求的变量。

第二类是额外场上粒子量：

- `phi`
- `Ex/Ey/Ez`
- `Bx/By/Bz`

这些量并不是 species 自带 SoA 分量，所以要单独用布尔位记录，而不是写进 `m_plot_flags`。

第三类是粒子过滤：

- `random_fraction`
- `uniform_stride`
- `plot_filter_function(t,x,y,z,ux,uy,uz)`

parser filter 在构造期就编译成 `amrex::Parser`，但真正执行仍在后面的 writer。

## 10. `ParticleDiag` 的过滤不是在构造函数里执行，而是在 writer 阶段消费

`rg` 到的调用点很清楚：

- `FlushFormatPlotfile.cpp`
- `WarpXOpenPMD.cpp`

都会读：

- `particle_diag.m_plot_flags`
- `particle_diag.m_do_random_filter`
- `particle_diag.m_do_uniform_filter`
- `particle_diag.m_do_parser_filter`

因此 `ParticleDiag` 不是“构造时就把粒子筛掉”，而是“把筛选规则和变量选择存起来，等 writer 真正写文件时再应用”。

这也解释了为什么 `FullDiagnostics` 不需要单独 particle compute functor。

## 11. `FullDiagnostics` 的字段主线，核心是“functor 树 + cell-centered output MultiFab”

`FullDiagnostics::InitializeFieldFunctors(lev)` 会按 `fields_to_plot` 构造一棵 functor 树。

典型映射包括：

- `Ex/Ey/Ez`、`Bx/By/Bz` -> `CellCenterFunctor`
- `jx/jy/jz` -> `JFunctor`
- `rho` / `rho_<species>` -> `RhoFunctor`
- `T_<species>` -> `TemperatureFunctor`
- `phi` -> `PhiFunctor`
- `divE` / `divB` -> `DivEFunctor` / `DivBFunctor`
- `part_per_cell` / `part_per_grid` -> 对应粒子计数 functor
- `particle_fields_to_plot` -> `ParticleReductionFunctor`

然后 `ComputeAndPack()` 再把这些 functor 的结果依次堆叠到：

```cpp
m_mf_output[i_buffer][lev]
```

里。

因此 `FullDiagnostics` 的字段路径本质是：

`requested names -> functor objects -> packed cell-centered MultiFab -> FlushFormat`

## 12. `PrepareFieldDataForOutput()` 也顺手决定了粒子 diagnostics 的几何过滤域

`FullDiagnostics::PrepareFieldDataForOutput()` 先做：

```cpp
warpx.FillBoundaryE(...)
warpx.FillBoundaryB(...)
warpx.UpdateAuxilaryData()
warpx.FillBoundaryAux(...)
```

然后又做了一件很容易忽略的事：

```cpp
m_output_species[i_buffer][i].m_diag_domain = m_geom_output[i_buffer][0].ProbDomain();
```

也就是说，particle diagnostics 的几何过滤域并不是在 `ParticleDiag` 构造时就固定，而是在每次准备 field output 时，用当前 diagnostics 几何域去更新。

这对 moving window / Galilean shift 很关键，因为 diagnostics 观测域可能会移动。

## 13. `diag_lo/diag_hi` 在当前实现里会直接把 full diagnostics 的粒子 I/O 关掉

`Diagnostics::InitData()` 和 `InitDataAfterRestart()` 都有同一段逻辑。

若用户指定了 `diag_lo` 或 `diag_hi`，它会先给每个 `ParticleDiag` 打开：

```cpp
v.m_do_geom_filter = true;
```

但紧接着又直接：

```cpp
m_output_species.at(i_buffer).clear();
```

并发出 warning，说明 reduced-domain diagnostics 目前不支持 particle I/O。

因此当前实现的真实边界不是“局部窗口粒子过滤已经可用”，而是“几何过滤标志先留好了，但 full diagnostics 仍把 particle output 暂时禁掉”。

## 14. `TimeAveraged` 不是新类，而是 `FullDiagnostics` 的一个模式

`MultiDiagnostics` 在 `diag_type=TimeAveraged` 时仍然实例化 `FullDiagnostics`。

区别只在：

- `m_diag_type == DiagTypes::TimeAveraged`
- 额外使用 `m_sum_mf_output`
- `DoComputeAndPack()` / `Flush()` 走时间平均分支

所以在源码结构上，WarpX 把 time-averaged diagnostics 理解成：

“沿用 full diagnostics 的字段与粒子框架，只把字段输出从瞬时值改为求和/平均后写出”

而不是另一套独立 diagnostics 系统。

## 15. 统一骨架可以概括成四层

把这几个类串起来，普通 diagnostics 主干可以概括为：

1. `MultiDiagnostics`
   - 读 diagnostics 列表
   - 按 `diag_type` 选子类
   - 在主循环里分派
2. `Diagnostics`
   - 定义初始化、compute/pack、flush 的统一骨架
   - 持有 `FlushFormat`、output MultiFab、species 输出槽位
3. `FullDiagnostics`
   - 把 `fields_to_plot` 映射成具体 field functors
   - 定义 `plotfile/openPMD/checkpoint/...` 下的 full/time-averaged 语义
4. `ParticleDiag`
   - 为每个 species 记录变量选择、过滤规则、附加粒子场和粒子来源句柄

## 16. 这一层对后续 diagnostics 精读的意义

这一篇解决的是 diagnostics 模块最基础的边界问题：

- 哪些类只负责调度，哪些类才负责计算；
- 哪些 diagnostics 真有粒子缓冲区，哪些只是直接引用 species；
- `ParticleDiag` 是配置对象，不是另一套粒子存储；
- full diagnostics 的粒子过滤主要发生在 writer 阶段，而不是 `ComputeAndPack()` 阶段。

把这层搞清，后面再继续读：

- `ComputeDiagFunctors/`
- `FlushFormats/`
- `ParticleIO` / `WarpXOpenPMD`

就不会再把“字段计算”、“粒子筛选”、“writer 落盘”和“BTD 缓冲区”混成一层。
