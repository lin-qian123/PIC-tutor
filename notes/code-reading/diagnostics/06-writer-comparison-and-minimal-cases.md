# Diagnostics Writer 对照与最小案例

绑定源码：

- `../warpx/Source/Diagnostics/Diagnostics.*`
- `../warpx/Source/Diagnostics/FullDiagnostics.*`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatPlotfile.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatCheckpoint.cpp`
- `../warpx/Source/Diagnostics/WarpXOpenPMD.cpp`
- `../warpx/Source/Diagnostics/ParticleIO.cpp`

对应文档与例子：

- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/dataanalysis/formats.rst`
- `../warpx/Examples/Tests/restart/inputs_base_3d`
- `../warpx/Examples/Physics_applications/uniform_plasma/inputs_base_3d`
- `../warpx/Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc`
- `../warpx/Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags`

## 1. 三类 writer 的入口分派发生在 `Diagnostics::InitDataBeforeRestart()`

真正把 `<diag>.format` 变成 writer 对象的地方，不在 `MultiDiagnostics`，而在 `Diagnostics.cpp`：

```cpp
if        (m_format == "plotfile"){
    m_flush_format = std::make_unique<FlushFormatPlotfile>() ;
} else if (m_format == "checkpoint"){
    m_flush_format = std::make_unique<FlushFormatCheckpoint>() ;
} else if (m_format == "openpmd"){
    m_flush_format = std::make_unique<FlushFormatOpenPMD>(m_diag_name);
}
```

也就是说：

- `diag_type` 决定 diagnostics 类别
- `format` 决定 flush writer

这是两层独立分派。

## 2. `checkpoint` 不是通用格式选项，而是 `FullDiagnostics` 的受限特例

文档明确写：

- `<diag>.format = checkpoint`
- only works with `<diag>.diag_type = Full`

源码里这一点由两层限制共同保证：

1. `MultiDiagnostics` 只会把 `diag_type` 解析成 `Full`、`TimeAveraged`、`BackTransformed`、`BoundaryScraping`
2. `FullDiagnostics::ReadParameters()` 对 `checkpoint` 额外做强约束

其核心判断是：

```cpp
const bool checkpoint_compatibility = (
    m_format == "checkpoint" &&
    !varnames_specified &&
    !pfield_varnames_specified &&
    !pfield_species_specified &&
    !lo_specified &&
    !hi_specified &&
    !cr_specified &&
    !species_specified );
```

并且随后直接断言：

```cpp
raw_specified == false && checkpoint_compatibility == true
```

所以 checkpoint 模式不是“FullDiagnostics 换个 writer”这么简单，而是：

- 不能自定义 fields 子集
- 不能自定义 particle_fields
- 不能裁剪 `diag_lo/diag_hi`
- 不能 coarsen
- 不能自定义 species 子集
- 不能请求 raw fields

因为 restart 需要的是完整运行态，不是用户筛选后的视图。

## 3. `plotfile` 路径的核心语义是“cell-centered fields + 可选 raw fields + AMReX 粒子 dump”

`FlushFormatPlotfile::WriteToFile()` 的顺序很清楚：

1. `WriteMultiLevelPlotfile(...)`
2. `WriteAllRawFields(...)`
3. `WriteParticles(...)`
4. `WriteJobInfo(...)`
5. `WriteWarpXHeader(...)`

这里的主文件 `WriteMultiLevelPlotfile` 写的是 diagnostics 已经 pack 好的 `m_mf_output`，即：

- 默认是 cell-centered fields
- 已经按 diagnostics 规则做了 coarsening、functor 计算、时间平均等

如果 `plot_raw_fields = 1`，额外再走 `WriteAllRawFields()`，把非 cell-centered 的原始 `MultiFab` 单独写到 `raw_fields/` 子树。

所以 plotfile 天然同时支持两层视角：

- 面向分析的 cell-centered diagnostics
- 面向源码/调试的 raw staggered fields

这也是文档里 `plot_raw_fields` / `plot_raw_fields_guards` 只对 `plotfile` 有效的原因。

## 4. `plotfile` 粒子输出的过滤是在 writer 里复制临时容器完成的

`FlushFormatPlotfile::WriteParticles()` 对每个 `ParticleDiag` 都会：

1. 创建 `tmp = pc->make_alike<>()`
2. 组装
   - `RandomFilter`
   - `UniformFilter`
   - `ParserFilter`
   - `GeometryFilter`
3. 用 `tmp.copyParticles(...)` 复制通过过滤的粒子
4. `tmp.WritePlotFile(...)`

这进一步证明：

- 粒子过滤不在 `ComputeAndPack()` 阶段
- 而是在 writer flush 阶段

这条结论和前一篇 `02-field-and-particle-functors.md` 是一致的，但这里把它落实到了 plotfile writer 的具体代码。

## 5. `openPMD` 路径和 `plotfile` 一样，也是在 writer 内部先复制 `tmp`

`WarpXOpenPMD.cpp` 的 `WriteOpenPMDParticles()` 先做的仍然是：

- 复制出临时容器 `tmp`
- 应用 `Random/Uniform/Parser/Geometry` filters

然后才继续：

- 可选 `storePhiOnParticles(...)`
- 可选 `storeFieldOnParticles(...)`
- 写 openPMD particle records

因此 openPMD 与 plotfile 的根本差别不在“是否过滤粒子”，而在：

- 输出容器模型相同
- 后续 writer 能表达的字段 richer

## 6. `openPMD` 比 `plotfile` 多出来的关键能力，是粒子上再 gather 场/势

文档里写得很明确：

- `Ex/Ey/Ez/Bx/By/Bz` on particles only when writing openPMD
- `phi` on particles only for lab-frame electrostatic solver

源码对应在 `WarpXOpenPMD.cpp`：

```cpp
if (particle_diag.m_plot_phi) {
    storePhiOnParticles(tmp, ..., !use_pinned_pc);
}
if (particle_diag.m_plot_Ex || ... || particle_diag.m_plot_Bz) {
    storeFieldOnParticles(tmp, !use_pinned_pc, ...);
}
```

而 `ParticleIO.cpp` 又进一步给出一条关键约束：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    is_full_diagnostic,
    "... only available with `diag_type = Full`.");
```

所以 openPMD 的粒子附加场能力并不是“所有 openPMD diagnostics 都支持”，而是：

- 只能 `format = openpmd`
- 还必须 `diag_type = Full`

对 `BTDiagnostics`、`BoundaryScrapingDiagnostics` 这类缓冲型粒子输出，WarpX 明确禁止在写出时再 gather `phi/E/B`，因为采样时刻和写出时刻不一致。

## 7. `checkpoint` 路径完全不走 `m_mf_output`

`FlushFormatCheckpoint::WriteToFile()` 的函数签名虽然和其他 writer 一致，但实现基本无视传进来的：

- `varnames`
- `mf`

而是直接从 `warpx.m_fields` 抓运行态寄存器：

- `Efield_fp`
- `Bfield_fp`
- `E_old`
- synchronized `current_fp`
- `Efield_cp/Bfield_cp`
- time-averaged `*_avg_*`
- PML 数据

然后再：

- `CheckpointParticles(...)`
- `WriteDMaps(...)`
- `WriteReducedDiagsData(...)`

这说明 checkpoint writer 的真实语义是：

- 序列化运行态
- 不是序列化 diagnostics view

因此把 checkpoint 理解成“plotfile/openPMD 的另一种格式”是错误的。它更接近一套单独的 restart persistence layer，只是借用了 diagnostics 调度时机。

## 8. `checkpoint` 粒子输出也不是 diagnostics 粒子过滤语义

`CheckpointParticles()` 不是先复制通过过滤的 `tmp`，而是直接对每个物理 species 容器调用：

```cpp
pc->Checkpoint(...)
```

而且 `FullDiagnostics::InitData()` 在 checkpoint 模式下默认会把输出 species 设成：

```cpp
mpc.GetSpeciesAndLasersNames()
```

这和普通 full diagnostics 默认只写 physical species 不同。原因很直接：

- restart 需要 laser particle state
- 也需要 runtime real/int components 完整保留

因此 checkpoint 粒子路径和 plotfile/openPMD 粒子路径在语义上完全不同：

- plot/openPMD：为分析写“筛选后的观测粒子”
- checkpoint：为恢复写“完整容器状态”

## 9. `restart` 恢复不仅恢复粒子/场，还恢复 runtime components 契约

`ParticleIO.cpp::MultiParticleContainer::Restart()` 先读 checkpoint header，再逐个检查当前 species 是否已经有这些 runtime real/int comps：

- 缺失则 `AddRealComp()` / `AddIntComp()`
- 然后才 `pc->Restart(...)`

这说明 restart 不只是把数据块搬回来，还会动态重建当前 species 的运行时属性布局。对前面已经整理过的：

- `prev_x`
- `opticalDepthQSR`
- `x_n/ux_n`
- `ionizationLevel`

这类 runtime attributes，这条恢复链是关键。

## 10. 三类 writer 的最小输入骨架可以直接从现有例子抽出来

### `plotfile` 最小骨架

来自普通 `FullDiagnostics` 默认路径：

```text
diagnostics.diags_names = diag1
diag1.intervals = 4
diag1.diag_type = Full
diag1.fields_to_plot = Bx By Bz Ex Ey Ez jx jy jz rho
```

如果不写 `format`，默认就是 `plotfile`。

### `openPMD` 最小骨架

来自 `laser_ion` 例子：

```text
diagnostics.diags_names = diagInst
diagInst.intervals = 100
diagInst.diag_type = Full
diagInst.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho
diagInst.format = openpmd
diagInst.openpmd_backend = h5
```

### `checkpoint` 最小骨架

来自 `uniform_plasma` / `restart` 例子：

```text
diagnostics.diags_names = diag1 chk
diag1.intervals = 4
diag1.diag_type = Full

chk.intervals = 6
chk.diag_type = Full
chk.format = checkpoint
```

重启时再配：

```text
amr.restart = "../test_xxx/diags/chk000006"
```

要注意当前本地 `uniform_plasma` 目录里的验证边界并不强。`test_2d_uniform_plasma` 和 `test_3d_uniform_plasma` 在 `CMakeLists.txt` 中都是 `analysis=OFF`，所以它们主要证明：

- full diagnostics 能按预期写出
- checkpoint diagnostics 能生成 `chk*`
- 周期热等离子体最小骨架在并行下能稳定给出历史 checksum

真正的强断言只出现在 `test_3d_uniform_plasma_restart`：它复用顶层 `Examples/analysis_default_restart.py`，逐字段比较 restart 与非 restart 输出，要求相对误差低于 `1e-12`。因此这组例子更适合被写成 `writer / checkpoint / restart reproducibility baseline`，而不是独立的热等离子体 physics benchmark。

## 11. `FieldProbe`、`ParticleHistogram2D`、`LoadBalanceCosts` 的最小可运行入口已经在本地例子里齐了

### `FieldProbe`

最小 line probe 入口可以直接复用：

```text
FieldProbe_Z.type = FieldProbe
FieldProbe_Z.intervals = 100
FieldProbe_Z.probe_geometry = Line
FieldProbe_Z.x_probe = 0.0
FieldProbe_Z.z_probe = -5.0e-6
FieldProbe_Z.x1_probe = 0.0
FieldProbe_Z.z1_probe = 25.0e-6
FieldProbe_Z.resolution = 3712
```

对应例子：

- `Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc`
- `Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags`

### `ParticleHistogram2D`

最小二维相空间入口也已经在 `laser_ion` 里：

```text
PhaseSpaceElectrons.type = ParticleHistogram2D
PhaseSpaceElectrons.intervals = 100
PhaseSpaceElectrons.species = electrons
PhaseSpaceElectrons.bin_number_abs = 1000
PhaseSpaceElectrons.bin_number_ord = 1000
PhaseSpaceElectrons.histogram_function_abs(t,x,y,z,ux,uy,uz,w) = "z"
PhaseSpaceElectrons.histogram_function_ord(t,x,y,z,ux,uy,uz,w) = "uz"
PhaseSpaceElectrons.value_function(t,x,y,z,ux,uy,uz,w) = "w"
```

当前源码实现里，`value_function` 虽然文档写成 optional，但 `ComputeDiags()` 会无条件调用 `fun_valueparser(...)`。同时 `compileParser(nullptr)` 返回默认 executor，而不是显式的 `w` fallback。由此可以合理推断：

- 为避免依赖默认 executor 的隐式行为
- 实际案例里应始终显式写出 `value_function`

这里是基于源码行为的谨慎结论，不是文档已经正式声明的规则。

### `LoadBalanceCosts`

最小入口最简单：

```text
warpx.reduced_diags_names = LBC
LBC.type = LoadBalanceCosts
LBC.intervals = 100
```

对应后处理和 workflow 文档：

- `Examples/Tests/reduced_diags/analysis_reduced_diags_load_balance_costs.py`
- `Docs/source/usage/workflows/plot_distribution_mapping.rst`

## 12. 当前 diagnostics 模块的“最小对照图”可以这样理解

### `plotfile`

- 目标：通用 full diagnostics 输出
- 场：cell-centered diagnostics `MultiFab`
- 可选：`raw_fields`
- 粒子：writer 阶段过滤后 `tmp.WritePlotFile(...)`
- 适合：yt / AMReX 原生后处理 / raw staggered debug

### `openPMD`

- 目标：标准化 field + particle 输出
- 场：cell-centered diagnostics meshes
- 粒子：writer 阶段过滤后写 openPMD particle records
- 额外能力：`phi` / `E,B` on particles
- 限制：这些附加粒子场只对 `diag_type = Full` 可用

### `checkpoint`

- 目标：restart persistence
- 场：真实运行态寄存器，不是 diagnostics view
- 粒子：完整 species + lasers 状态
- 额外：DM、PML、reduced-diag checkpoint state
- 限制：不能自定义字段/粒子子集或裁剪区域

这三条链看起来都从 diagnostics 出发，但真正服务的对象已经完全不同：

- `plotfile` 服务分析
- `openPMD` 服务分析与跨生态交换
- `checkpoint` 服务恢复
