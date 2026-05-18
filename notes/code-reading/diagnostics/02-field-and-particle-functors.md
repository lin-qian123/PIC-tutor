# `ComputeDiagFunctors`、`ParticleReductionFunctor` 与 writer 粒子过滤链

绑定源码：

- `../warpx/Source/Diagnostics/ComputeDiagFunctors/ComputeDiagFunctor.H`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/JFunctor.H`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/JFunctor.cpp`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.H`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.cpp`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/PhiFunctor.H`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/PhiFunctor.cpp`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/ParticleReductionFunctor.H`
- `../warpx/Source/Diagnostics/ComputeDiagFunctors/ParticleReductionFunctor.cpp`
- `../warpx/Source/Diagnostics/WarpXOpenPMD.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatPlotfile.cpp`
- `../warpx/Source/Diagnostics/ParticleIO.cpp`

前一篇已经把 diagnostics 顶层骨架分清了。这一篇只解决一个更细的误区：

- 哪些代码在“计算 diagnostics 字段”；
- 哪些代码在“筛选要写出的粒子”；
- 哪些代码才真正“把粒子或字段写到文件”。

WarpX 在这三层之间的边界，比表面上看起来清楚得多。

## 1. `ComputeDiagFunctor` 的抽象非常单纯：输入是源场，输出是 diagnostics `MultiFab`

`ComputeDiagFunctor` 的核心接口只有：

```cpp
virtual void operator() (amrex::MultiFab& mf_dst, int dcomp, int i_buffer = 0) const = 0;
```

因此它的职责就是：

- 从 simulation state 中取某个字段或某个派生量；
- 写进 diagnostics 输出 `MultiFab` 的某个 component。

它不负责：

- 粒子过滤；
- writer 文件格式；
- species 粒子变量裁剪。

这意味着 `ComputeDiagFunctors/` 整个子目录，本质上都是“字段计算层”。

## 2. `ComputeDiagFunctor` 的公共工具是 `InterpolateMFForDiag()`

基类里最重要的公共工具是：

```cpp
void InterpolateMFForDiag(
    amrex::MultiFab& mf_dst, const amrex::MultiFab& mf_src, int dcomp,
    const amrex::DistributionMapping& dm, bool convertRZmodes2cartesian) const
```

它的语义不是任意插值，而是 diagnostics 专用的：

- 对 Cartesian，调用 `ablastr::coarsen::sample::Coarsen(...)`；
- 对 RZ，可选先把各 mode 合成 Cartesian-like 单分量，再 coarsen；
- 最终统一写到 diagnostics `mf_dst`。

所以大多数具体 functor 的模式都可以概括成：

1. 找到或构造源 `MultiFab`；
2. 需要时先做 guard-cell / filter / Poisson solve / cell-center 准备；
3. 最后统一调用 `InterpolateMFForDiag()`。

## 3. `JFunctor` 代表的是真正的“字段 functor”，不是 writer 辅助函数

`JFunctor::operator()` 的结构很典型：

```cpp
amrex::MultiFab* m_mf_src = warpx.m_fields.get(FieldType::current_fp, Direction{m_dir}, m_lev);
...
InterpolateMFForDiag(mf_dst, *m_mf_src, dcomp, warpx.DistributionMap(m_lev), m_convertRZmodes2cartesian);
```

如果 `m_deposit_current` 为真，它还会先触发一次 current deposition，再做 boundary fill。

因此 `JFunctor` 表示的是：

- diagnostics 需要的 `j` 字段怎么从 runtime state 中拿到；
- 在某些 solver 场景下，如果 simulation 没有自然留下 current，还要先为 diagnostics 现算一次。

这个阶段仍属于“字段计算层”，还没进入 writer。

## 4. `RhoFunctor` 的关键边界：它不是从现成 `rho_fp` 直接抄，而是会重新构造 charge density

`RhoFunctor::operator()` 先根据是否指定 species 决定：

- 总 `rho`
- 某个 species 的 `rho`

然后通过：

```cpp
rho = mypc.GetChargeDensity(m_lev, true);
```

重新拿到电荷密度；若有 fluid species，还要额外叠加 fluid charge deposition。

接着再统一做：

```cpp
warpx.ApplyFilterandSumBoundaryRho(...)
```

在 RZ PSATD 场景下，还可能再做一次谱空间 filter。

这说明 diagnostics 里的 `rho` 不是简单把某个全局寄存器裸写到文件，而是有自己的一套“构造和整理 charge density”的过程。

## 5. `PhiFunctor` 的关键边界：有现成 `phi_fp` 就读，没有就为 diagnostics 临时解一次 Poisson

`PhiFunctor::operator()` 先检查：

```cpp
warpx.m_fields.has(FieldType::phi_fp, m_lev)
```

如果有现成 `phi_fp`，直接拿来 coarsen。

如果没有，就临时：

1. 用 `ComputeDivE()` 生成 `rho = epsilon0 * divE`
2. 分配 `phi_vec`
3. 调 `ElectrostaticSolver::computePhi(...)`
4. 再 `InterpolateMFForDiag(...)`

所以 `phi` diagnostics 的真实语义是：

- 并不要求 simulation 本身一直保存 electrostatic potential；
- 在 EM solver 下，如果用户要求 `phi`，diagnostics 可以为输出步临时补做一次 Poisson solve。

这再次说明 `ComputeDiagFunctors` 不是“搬运现成数组”，而是“为 diagnostics 构造所需字段”。

## 6. `ParticleReductionFunctor` 虽然和粒子有关，但它仍然属于字段计算层

这是最容易混淆的一点。

`ParticleReductionFunctor` 在 `FullDiagnostics::InitializeFieldFunctors()` 中，是通过：

```cpp
particle_fields_to_plot -> ParticleReductionFunctor
```

接进 `m_all_field_functors` 的。

也就是说，虽然它内部读取粒子，但输出仍然是 cell-centered `MultiFab`，而不是粒子文件。

## 7. `ParticleReductionFunctor` 的算法是“ParticleToMesh + parser map/filter + cell reduction”

它构造时会编译两个 parser：

- `m_map_fn(x,y,z,ux,uy,uz)`
- 可选 `m_filter_fn(x,y,z,ux,uy,uz)`

运行时核心是：

```cpp
ParticleToMesh(pc, red_mf, m_lev, lambda)
```

对每个粒子：

1. 先取 WarpX 约定下的 `(x,y,z)`；
2. 再把 `ux,uy,uz` 归一化成 parser 使用的 `gamma v / c`；
3. 可选先过 `filter_fn`；
4. 再计算 `map_fn`；
5. 用粒子权重 `w` 把结果累加到粒子所在 cell。

如果 `m_do_average=true`，它还会额外再做一遍 `ParticleToMesh`，统计权重和，再把累计量除以粒子总权重。

最后才：

```cpp
ablastr::coarsen::sample::Coarsen(mf_dst, red_mf, ...)
```

所以 `ParticleReductionFunctor` 不是 particle writer，而是“从粒子构造 cell field”的一个特殊 field functor。

## 8. 到这里为止，所有这些 functor 都只写 `m_mf_output`

无论是：

- `JFunctor`
- `RhoFunctor`
- `PhiFunctor`
- `ParticleReductionFunctor`

它们最终都只做一件事：

- 把一个 diagnostics 字段写进 `mf_dst`

它们不接触：

- `ParticleDiag.m_plot_flags`
- `RandomFilter`
- `UniformFilter`
- `ParserFilter`
- openPMD / plotfile 文件结构

这条边界必须记死：`ComputeDiagFunctors/` 是字段计算层，不是粒子写出层。

## 9. `ParticleDiag` 的过滤规则真正是在 writer 里消费

这条链在 `WarpXOpenPMD.cpp` 和 `FlushFormatPlotfile.cpp` 里非常清楚。

writer 开始时先取：

```cpp
WarpXParticleContainer* pc = particle_diag.getParticleContainer();
WarpXParticleContainer::Base* pinned_pc = particle_diag.getPinnedParticleContainer();
```

然后从 `ParticleDiag` 里构造：

```cpp
RandomFilter const random_filter(...);
UniformFilter const uniform_filter(...);
ParserFilter parser_filter(...);
GeometryFilter const geometry_filter(...);
```

接着并不是直接写原 species 容器，而是先创建一个临时容器：

```cpp
WarpXParticleContainer::Base tmp = ... make_alike<>();
tmp.SetArena(amrex::The_Pinned_Arena());
```

再通过：

```cpp
tmp.copyParticles(*pc or *pinned_pc, predicate, true);
```

把满足四类过滤器乘积条件的粒子复制进 `tmp`。

因此粒子过滤真实发生的位置是：

- writer 阶段
- `copyParticles()` 到临时 `tmp` 容器时

而不是 `ParticleDiag` 构造阶段，也不是 `ComputeAndPack()` 的 field-functor 阶段。

## 10. `ParticleDiag.m_plot_flags` 也是 writer 阶段才被消费

在 openPMD 路径里：

```cpp
amrex::Vector<int> real_flags = particle_diag.m_plot_flags;
```

在 plotfile 路径里同样会做：

```cpp
real_flags = part_diag.m_plot_flags;
```

再配合 runtime-added real/int comps 一起组织最终输出列。

所以 `m_plot_flags` 的角色是：

- 在构造阶段被解析；
- 在 writer 阶段决定哪些 real comps 真正写到文件。

它不是 field functor 层的输入。

## 11. `phi` / `E` / `B` on particles 不是 field functor 层，而是 writer 对临时 `tmp` 的后处理

这一点也很容易误解。

在 `WarpXOpenPMD.cpp` 中，writer 完成 `tmp.copyParticles(...)` 之后，还可能继续：

```cpp
storePhiOnParticles(tmp, ...);
storeFieldOnParticles(tmp, ...);
```

也就是说：

- `phi on particles`
- `Ex/Ey/Ez/Bx/By/Bz on particles`

不是写主粒子容器里的现成属性；
- 也不是 `ComputeDiagFunctors/` 产物；
- 而是 writer 在“已经过滤好的临时粒子副本 `tmp`”上再 gather 一次字段。

这解释了为什么这些量属于 `ParticleDiag` 的额外布尔选项，而不是 `m_plot_flags` 的普通 SoA 分量。

## 12. 这些附加粒子场只允许 `diag_type = Full`

`ParticleIO.cpp` 里 `storePhiOnParticles()` 和 `storeFieldOnParticles()` 都有同一个硬断言：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    is_full_diagnostic,
    "... only available with `diag_type = Full`.");
```

源码注释也解释了原因：

- 对 `BackTransformed`、`BoundaryScraping` 这类带粒子缓冲区的 diagnostics，
  粒子被“写出”的时间并不等于粒子被“收集”的 PIC 时间；
- 如果这时再去 gather `phi` 或 `E/B`，拿到的是写出时刻的场，不是粒子被收集时刻的场；
- 为了避免语义错配，WarpX 直接禁止这种请求。

这条边界非常关键。不要把 `additional_variables = phi Ex ...` 理解成对所有 diagnostics 都可用。

## 13. openPMD 和 plotfile 的共同模式：都先复制过滤后的 `tmp`，再由各自 writer 写格式

两条 writer 路径虽然输出格式不同，但模式一致：

1. 从 `ParticleDiag` 取容器句柄和过滤配置；
2. 用 `tmp.copyParticles(...)` 生成过滤后的临时粒子容器；
3. 可选为 `tmp` 加上 `phi` 或 `E/B` on particles；
4. 再根据格式各自：
   - 组织名字
   - 组织 flags
   - 调底层 writer

因此格式差异在最后一步，过滤语义和临时粒子副本语义在更上层已经统一。

## 14. 现在可以把 diagnostics 主链彻底拆成三层

把这一篇和前一篇合起来，普通 diagnostics 可以明确拆成：

### 第一层：field compute

- `ComputeDiagFunctors/`
- `JFunctor` / `RhoFunctor` / `PhiFunctor`
- `ParticleReductionFunctor`

职责：从 simulation fields 或 particles 生成 diagnostics field `MultiFab`。

### 第二层：particle filter and staging

- `ParticleDiag`
- `RandomFilter`
- `UniformFilter`
- `ParserFilter`
- `GeometryFilter`
- `tmp.copyParticles(...)`

职责：根据 species 变量选择和过滤配置，生成待写出的临时粒子副本。

### 第三层：writer flush

- `WarpXOpenPMD.cpp`
- `FlushFormatPlotfile.cpp`
- 以及其他 `FlushFormat*`

职责：把字段 `m_mf_output` 和临时粒子容器 `tmp` 写成具体文件格式。

## 15. 这一层对第 8 章最重要的结论

这一篇真正要修正的认知有三条：

1. `ParticleReductionFunctor` 虽然读粒子，但它属于字段计算层，因为输出是 cell-centered `MultiFab`。
2. `ParticleDiag` 的过滤规则不是在构造时执行，而是在 writer 复制 `tmp` 粒子容器时执行。
3. `phi` / `E` / `B` on particles` 是 writer 对 `tmp` 的附加 gather，而且只允许 `diag_type = Full`。

如果这三条不区分清楚，就会很容易把 diagnostics 模块误读成“所有粒子相关量都在同一层处理”。源码表明并不是这样。
