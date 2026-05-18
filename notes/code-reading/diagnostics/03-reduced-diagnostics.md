# `ReducedDiags`、`MultiReducedDiags` 与 reduced diagnostics 的 checkpoint 钩子

绑定源码：

- `../warpx/Source/Diagnostics/ReducedDiags/MultiReducedDiags.H`
- `../warpx/Source/Diagnostics/ReducedDiags/MultiReducedDiags.cpp`
- `../warpx/Source/Diagnostics/ReducedDiags/ReducedDiags.H`
- `../warpx/Source/Diagnostics/ReducedDiags/ReducedDiags.cpp`
- `../warpx/Source/Diagnostics/ReducedDiags/FieldEnergy.cpp`
- `../warpx/Source/Diagnostics/ReducedDiags/ParticleEnergy.cpp`
- `../warpx/Source/Diagnostics/ReducedDiags/FieldPoyntingFlux.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatCheckpoint.cpp`
- `../warpx/Source/Diagnostics/WarpXIO.cpp`

前几篇讲的是 `Diagnostics/` 顶层类和 full / boundary / BTD 的主框架。这一篇只看 reduced diagnostics。

关键问题不是“它能输出哪些量”，而是：

1. reduced diagnostics 在 WarpX 里为什么单独成体系；
2. 它和 full diagnostics 的调度方式有什么根本不同；
3. 它何时只是一行一行地写表格，何时又需要 checkpoint 持久化内部状态。

## 1. reduced diagnostics 根本不走 `Diagnostics` / `FlushFormat` 那条 `MultiFab + particle_diags` 主线

`MultiReducedDiags` 和 `ReducedDiags` 是 `Source/Diagnostics/ReducedDiags/` 里的另一套平行体系。

它们没有继承 `Diagnostics`，也不实现：

- `InitializeFieldFunctors`
- `ComputeAndPack`
- `Flush`

相反，它们的接口是：

- `InitData()`
- `LoadBalance()`
- `ComputeDiags(step)`
- `ComputeDiagsMidStep(step)`
- `WriteToFile(step)`
- `WriteCheckpointData(dir)`
- `ReadCheckpointData(dir)`

这说明 reduced diagnostics 的核心抽象不是“堆叠字段/粒子，再交给 writer”，而是“每个诊断自己计算一小组 reduced numbers，然后写成文本或自定义格式”。

## 2. `MultiReducedDiags` 是 reduced diagnostics 的工厂和调度器

构造函数先读：

```cpp
warpx.reduced_diags_names
```

如果这个列表不存在，`m_plot_rd = 0`，整套 reduced diagnostics 直接关闭。

如果存在，就再逐个读取每个 `<reduced_diag_name>.type`，并通过一个字典工厂映射到具体类：

- `ParticleEnergy`
- `ParticleMomentum`
- `ParticleNumber`
- `FieldEnergy`
- `FieldMaximum`
- `FieldMomentum`
- `FieldPoyntingFlux`
- `ParticleHistogram`
- `FieldProbe`
- `LoadBalanceCosts`
- ...

因此 `MultiReducedDiags` 的角色和 `MultiDiagnostics` 类似，但对象完全不同：

- `MultiDiagnostics` 分派 `Full/BTD/BoundaryScraping`
- `MultiReducedDiags` 分派各种 reduced quantity calculators

## 3. reduced diagnostics 的“是否执行”逻辑更简单

`MultiReducedDiags::DoDiags(step)` 本质上只是对所有子诊断做：

```cpp
result = result || m_multi_rd[i_rd]->DoDiags(step);
```

而 `ReducedDiags::DoDiags(step)` 又只是：

```cpp
return m_intervals.contains(step+1);
```

也就是说，reduced diagnostics 没有 full diagnostics 那种：

- `DoComputeAndPack`
- `DoDump`
- buffer fullness
- moving-window domain shift

的复杂双阶段逻辑。它的基本模型是：到点就算，到点就写。

## 4. `ReducedDiags` 基类的真正核心是“统一表格输出协议”

`ReducedDiags` 基类持有的公共状态包括：

- `m_path`
- `m_extension`
- `m_rd_name`
- `m_intervals`
- `m_sep`
- `m_precision`
- `m_data`
- `m_write_header`

默认输出目录是：

```cpp
./diags/reducedfiles/
```

默认扩展名是：

```cpp
txt
```

而 `WriteToFile(step)` 的统一格式也很直接：

1. 第一列：`step+1`
2. 第二列：`WarpX::gett_new(0)`
3. 后面所有列：`m_data`

所以 reduced diagnostics 共享的是“一行一行写表格”的协议，而不是共享 field/particle writer。

## 5. `ReducedDiags` 的构造期就考虑了 restart 语义

构造函数里先检查：

```cpp
amr.restart
```

再决定 `m_write_header` 是否为真：

```cpp
m_write_header = IsNotRestart || !amrex::FileExists(rd_full_file_name);
```

这意味着 reduced diagnostics 的文本文件在 restart 场景下默认不是每次都 truncate 重写，而是：

- 不是 restart，或文件不存在：重新建文件并写 header
- 是 restart 且文件已存在：沿用旧文件，继续 append

因此 reduced diagnostics 的最基础 restart 语义，首先是“表格文件续写”。

## 6. `FieldEnergy` 和 `ParticleEnergy` 说明 reduced diagnostics 的主流模型是“现算标量/向量，再落表”

`FieldEnergy` 的结构很典型：

- 构造期根据 `amr.max_level` 决定 `m_data` 长度；
- 若 `m_write_header`，就写列名；
- `ComputeDiags(step)` 到点后，按 level 读取 `Efield_aux/Bfield_aux`，求能量；
- 把结果写进 `m_data`。

`ParticleEnergy` 的模式也类似：

- 构造期读取 species 数，决定 `m_data` 结构；
- 到点后遍历 species，调用 `sumParticleWeightAndEnergy(false)`；
- 再填充总能量和平均能量。

这两类例子说明 reduced diagnostics 的主流路径就是：

`ComputeDiags(step) -> fill m_data -> base WriteToFile(step)`

并不需要任何 `MultiFab` output buffer。

## 7. reduced diagnostics 里也有“状态型”成员，不全是每步可重算的纯函数

很多人会误以为 reduced diagnostics 只是瞬时统计，因此 checkpoint 时完全可以不管。

这对部分类型成立，但并不普遍。

最直接的反例是 `FieldPoyntingFlux`。它不仅保存当前步的边界 flux，还在：

```cpp
m_data[ii + 2*AMREX_SPACEDIM] += m_data[ii] * dt;
```

中维护时间积分量。

这类 accumulated diagnostic 不是单看当前 WarpX 状态就能恢复的；如果 restart 时不把积分历史带上，后续输出会断裂。

## 8. 因此 `ReducedDiags` 基类专门预留了 checkpoint 钩子

基类默认给出空实现：

- `WriteCheckpointData(dir)`
- `ReadCheckpointData(dir)`

大多数简单 reduced diagnostics 不需要覆写它们，因为：

- 当前步重算即可；
- 历史文件本身继续 append 即可。

但像 `FieldPoyntingFlux` 这种带内部累积状态的类型，就必须覆写。

## 9. `FieldPoyntingFlux` 是 reduced diagnostics checkpoint 语义的关键例子

`FieldPoyntingFlux::WriteCheckpointData(dir)` 会把时间积分的那部分 `m_data` 写到：

```cpp
dir + "/FieldPoyntingFlux_data.txt"
```

而 `ReadCheckpointData(dir)` 会在 restart 时把这些值读回来。

这说明 reduced diagnostics 的 checkpoint 不是统一保存整张文本输出，而是：

- 文本表格继续 append；
- 需要延续的内部状态，单独通过诊断自己的 checkpoint 钩子写出和恢复。

## 10. reduced diagnostics 与 checkpoint 的桥接点在两处

第一处是 checkpoint 写出端：

```cpp
FlushFormatCheckpoint::WriteReducedDiagsData(dir)
{
    warpx.reduced_diags->WriteCheckpointData(dir);
}
```

也就是说，checkpoint format 并不会把 reduced diagnostics 当成 `ParticleDiag` 或 field `MultiFab` 来处理，而是单独回调 `MultiReducedDiags`。

第二处是 restart 读入端：

```cpp
reduced_diags->ReadCheckpointData(restart_chkfile);
```

这在 `WarpXIO.cpp` 的 restart 链里发生在：

- fields/PML/EB 恢复之后
- particles restart 之前

所以 reduced diagnostics 的恢复是 WarpX restart 主链里的正式一步，不是可有可无的附属脚本。

## 11. `MultiReducedDiags::WriteToFile()` 还有一个实现边界：只在 I/O rank 写

写表格时它先判断：

```cpp
if (!ParallelDescriptor::IOProcessor()) { return; }
```

然后再对每个子诊断检查：

```cpp
m_multi_rd[i_rd]->m_intervals.contains(step+1)
```

再调用 `WriteToFile(step)`。

这说明 reduced diagnostics 的输出模型默认是假设：

- 诊断内部已经完成 MPI 归约；
- 最终只让 I/O rank 落地。

因此 MPI reduction 是每个 reduced diagnostic 自己计算逻辑的一部分，而不是统一 writer 才做。

## 12. reduced diagnostics 和 full diagnostics 的真正分界

可以把两套体系的分界明确写成：

### full / BTD / boundary-scraping

- 目标：输出字段快照、粒子快照或 buffered snapshot
- 核心载体：`MultiFab`、`ParticleDiag`、`FlushFormat`
- 结构：`InitData -> ComputeAndPack -> Flush`

### reduced diagnostics

- 目标：输出少量 runtime-reduced 标量/向量/直方图/探针数据
- 核心载体：`m_data`
- 结构：`ComputeDiags -> WriteToFile`

两边都在 `Source/Diagnostics/` 下面，但抽象完全不同。

## 13. 这一层对后续 diagnostics 精读的意义

这一篇给出两个后续阅读支点：

1. `ReducedDiags/` 应该按“诊断类型族”去读，而不是按 `ComputeDiagFunctor` 思路去读。
2. checkpoint/restart 对 diagnostics 来说至少有两条线：
   - full/checkpoint format 保存场和粒子状态
   - reduced diagnostics 通过独立钩子保存内部累积量

这为下一篇 `checkpoint/restart + BTD + FlushFormats` 的笔记打基础。
