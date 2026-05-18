# checkpoint / restart、`FlushFormatCheckpoint` 与 `BTDiagnostics` 的缓冲输出链

绑定源码：

- `../warpx/Source/Diagnostics/FlushFormats/FlushFormatCheckpoint.cpp`
- `../warpx/Source/Diagnostics/FlushFormats/FlushFormat.H`
- `../warpx/Source/Diagnostics/WarpXIO.cpp`
- `../warpx/Source/Diagnostics/BTDiagnostics.H`
- `../warpx/Source/Diagnostics/BTDiagnostics.cpp`

前一篇已经把 reduced diagnostics 的 checkpoint 钩子拆开了。这一篇只看“带缓冲的 diagnostics”和 restart/output format 的交界。

关键问题是：

1. checkpoint format 到底保存什么；
2. `BTDiagnostics` 为什么不能套用 full diagnostics 那套瞬时写出模型；
3. buffered diagnostics 的 flush 条件和 restart 语义在哪里真正落地。

## 1. `FlushFormatCheckpoint` 不是 generic diagnostics writer，而是 WarpX 运行态快照 writer

它虽然挂在 `FlushFormats/` 目录下，但语义和：

- plotfile
- openPMD

并不一样。

`FlushFormatCheckpoint::WriteToFile(...)` 实际并不使用传进来的：

- `varnames`
- `mf`

去写 generic diagnostics，而是直接回到 `WarpX::GetInstance()` 里，把真正需要 restart 的运行态字段逐项写出去。

这说明 checkpoint format 在代码组织上属于 diagnostics 模块，但语义上更接近“simulation state serializer”。

## 2. checkpoint 写出的主体是 runtime field registry，而不是某个 diagnostics buffer

`WriteToFile()` 里直接逐 level 写：

- `Efield_fp`
- `Bfield_fp`
- `E_old`
- time-averaged `E/B`（若启用）
- synchronized `current_fp/current_cp`
- coarse-patch `Efield_cp/Bfield_cp`
- PML / PML_RZ 数据

也就是说，checkpoint 写出的不是 `m_mf_output` 这类 diagnostics 结果，而是 WarpX 真正的演化状态。

因此 checkpoint format 和普通 full diagnostics 的根本差异是：

- full diagnostics 关心“给用户看的输出”
- checkpoint 关心“足以 restart 的内部状态”

## 3. checkpoint 的粒子写出路径也不是 `ParticleDiag` 过滤语义

`CheckpointParticles(dir, particle_diags)` 会遍历 `particle_diags`，取：

```cpp
WarpXParticleContainer* pc = part_diag.getParticleContainer();
```

但它构造 `write_real_comps` / `write_int_comps` 的目标是“把 species 必需状态完整写出”，而不是像 plotfile/openPMD 那样应用 `random_fraction`、`uniform_stride` 或 parser filter。

所以虽然函数签名仍复用 `ParticleDiag` 列表，但 checkpoint 的粒子语义不是“用户挑选后写出”，而是“为 restart 保留所需状态”。

## 4. reduced diagnostics 在 checkpoint 里是单独挂接的

checkpoint writer 末尾专门调用：

```cpp
WriteReducedDiagsData(checkpointname);
```

再由：

```cpp
warpx.reduced_diags->WriteCheckpointData(dir);
```

把 reduced diagnostics 的内部持久化状态写进去。

这再次说明 checkpoint 不属于任何单一 diagnostics 子类，而是把：

- fields
- particles
- PML
- reduced diagnostics state

一起序列化。

## 5. restart 端对应的桥接点在 `WarpXIO.cpp`

恢复链中有明确一步：

```cpp
reduced_diags->ReadCheckpointData(restart_chkfile);
```

然后才继续：

```cpp
mypc->AllocData();
mypc->Restart(restart_chkfile);
```

因此 reduced diagnostics 的 restart 恢复，是 WarpX 标准 restart 主链的一部分，不是用户后处理。

## 6. `BTDiagnostics` 的模型和 full diagnostics 最大的区别，是它每步都可能“积一片 slice 到 buffer”

`BTDiagnostics::DoComputeAndPack(step, force_flush)` 直接返回：

```cpp
return ((step >= 0) && (!force_flush));
```

也就是说，只要不是初始化期、也不是单纯强制 flush，它默认每一步都可能去 back-transform 并往 buffer 填数据。

这和 full diagnostics 的模型完全不同。full diagnostics 只有到输出间隔才 compute/pack；BTD 则是“几乎每步都可能积累一部分 snapshot”。

## 7. `BTDiagnostics::DoDump()` 的判据来自 buffer 状态，不只是时间间隔

它的 flush 条件是三选一：

1. 当前 buffer 已满；
2. 当前 lab-frame snapshot 的最后一个有效 z-slice 已填到；
3. 结束时 `force_flush`，且 buffer 不是空的。

源码里对应的是：

```cpp
const auto is_buffer_full = buffer_full(i_buffer);
const auto last_z_slice_filled = (m_lastValidZSlice[i_buffer] == 1);
const auto do_forced_flush = (force_flush && !buffer_empty(i_buffer));
```

因此 BTD 的输出不是“到点就写”，而是“按 snapshot buffer 的占用状态写”。

## 8. `BTDiagnostics` 真的分配了自己的 field buffer 和 particle buffer

这也是它与 full diagnostics 的本质差异。

在 `DerivedInitData()` 中，它会：

- 初始化 lab-frame snapshot 几何、时间和计数器；
- 为每个 snapshot 分配 `m_particles_buffer` / `m_totalParticles_in_buffer`；
- 为所有 level 定义 cell-centered field staging `m_cell_centered_data_name`；
- 为每个 snapshot 维护：
  - `m_buffer_counter`
  - `m_snapshot_full`
  - `m_buffer_flush_counter`
  - `m_buffer_box`
  - `m_geom_snapshot`

因此 BTD 不是“瞬时计算后立刻写”，而是显式维护一套跨时间步存在的缓冲对象。

## 9. BTD 的字段主线是“全域 cell-center -> flatten 到 coarse -> slice/back-transform -> 填 buffer”

`PrepareFieldDataForOutput()` 先对所有 level 的 cell-center functors 做：

```cpp
m_cell_center_functors[lev][icomp]->operator()(*fields.get(m_cell_centered_data_name, lev), ...)
```

然后再从 finest 往 coarse 做：

```cpp
ablastr::coarsen::sample::Coarsen(...)
```

把数据 flatten 到 coarse 基础上。

接着，针对每个 snapshot 和当前 z-slice，再通过 back-transform functor 把这一片 lab-frame slice 填进当前 buffer `m_mf_output[i_buffer][0]`。

所以 BTD 的字段链可以概括为：

`runtime fields -> cell-centered staging over whole domain -> flattened coarse representation -> one slice at a time into lab-frame buffer`

## 10. BTD 的粒子主线是真正的 `ComputeParticleDiagFunctor` 路径

这和 full diagnostics 完全不同。

`InitializeParticleFunctors()` 会为每个 species 创建：

```cpp
BackTransformParticleFunctor(...)
```

`InitializeParticleBuffer()` 则真的为每个 snapshot / species 分配：

```cpp
m_particles_buffer[i][isp] = std::make_unique<WarpXParticleContainer::Base>(...)
```

并把这个 pinned buffer 作为 `ParticleDiag` 的 `pinned_pc` 传进去。

因此 BTD 粒子输出不是 writer 再去主 species 容器里筛选，而是先把 back-transformed 粒子真正存进 diagnostics 自己的缓冲区。

## 11. BTD flush 前还要先重布粒子 buffer，并临时放宽 box 边界

`BTDiagnostics::Flush()` 开头对粒子 buffer 做了一件很特别的事：

1. 暂时把 buffer box 在 moving-window 方向两端各扩一格；
2. 用这个更宽的 box 重设 particle geometry / box array；
3. `RedistributeParticleBuffer(i_buffer)`；
4. 写出；
5. 再把 box 缩回原尺寸。

源码注释说明原因很具体：

- back-transformed 粒子最多可能比 buffer 几何域外多半格到一格；
- plotfile / redistribute 在定位粒子时会要求粒子必须落在 box 范围内；
- 因此 flush 前必须临时放宽 box，避免 locateParticle 失败。

这是 BTD 这种 buffered diagnostics 才会有的几何修正逻辑，普通 full diagnostics 没有这层复杂度。

## 12. BTD 的 `Flush()` 真正写出的不是“当前一步”，而是“当前 snapshot 的一段 buffer”

`Flush()` 调 `m_flush_format->WriteToFile(...)` 时会传入：

- `use_pinned_pc = true`
- `isBTD = true`
- `snapshotID = i_buffer`
- `bufferID = m_buffer_flush_counter[i_buffer]`
- `numBuffers = m_max_buffer_multifabs[i_buffer]`
- `full_BTD_snapshot = m_geom_snapshot[i_buffer][0]`
- `isLastBTDFlush = snapshot_full || force_flush`

这些参数说明 BTD 的 writer 不是单纯按 step 写，而是需要知道：

- 这是哪个 snapshot；
- 这是该 snapshot 的第几段 buffer；
- 总共预计多少段；
- 这次是不是最后一次 flush。

这也解释了为什么 BTD 的 `Flush()` 迟迟没有完全并回 `Diagnostics` 基类通用实现。

## 13. BTD flush 后必须显式重置一整组缓冲状态

写完后它会：

- `ResetBufferCounter(i_buffer)`
- `m_field_buffer_multifab_defined[i_buffer] = 0`
- `IncrementBufferFlushCounter(i_buffer)`
- `NullifyFirstFlush(i_buffer)`
- `ResetTotalParticlesInBuffer(i_buffer)`
- `ClearParticleBuffer(i_buffer)`
- 更新下一个 buffer 的 `m_buffer_k_index_hi`

因此 BTD 的 flush 不是纯 I/O 事件，而是一次真实的“消费并推进 buffer state machine”。

## 14. BTD 与 checkpoint/restart 的共同主题：都不是瞬时输出，而是状态机输出

现在可以把这篇和上一篇的逻辑合起来看：

- checkpoint format 保存的是“simulation restart state”
- BTD 保存的是“逐步积累的 snapshot buffer state”

它们和普通 full diagnostics 的共同区别是：都不能理解成“到点现算现写、写完就没有历史依赖”。

换句话说，`Source/Diagnostics` 里真正“有状态机”的两大分支就是：

1. checkpoint / restart
2. BTD buffer filling / flushing

## 15. diagnostics 模块到这里可以分成四族

经过这几篇笔记后，可以把 diagnostics 模块稳定分成四族：

1. `FullDiagnostics`
   - 瞬时或 time-averaged field/particle snapshot
2. `BoundaryScrapingDiagnostics`
   - 直接消费 `ParticleBoundaryBuffer`
3. `ReducedDiags`
   - 运行中把数值约化成表格或定制小数据结构
4. `BTDiagnostics`
   - 跨时间步累积 slice / particle buffer，再分段 flush

而 checkpoint/restart 则是横跨这些族的运行态持久化机制。

## 16. 对第 8 章的直接结论

这篇最重要的三个结论是：

1. checkpoint format 不等于普通 diagnostics 格式，它本质上保存的是 WarpX restart state。
2. `BTDiagnostics` 不是“另一种 full diagnostics”，而是一套真正的 slice/buffer 状态机。
3. reduced diagnostics 与 BTD 都可能有跨步内部状态，因此 diagnostics 模块里不能只用“到 interval 就写一次”来理解所有分支。

## 17. `restart/` 目录里还有一组更窄的 PICMI 合同：checkpoint 不是只给大应用用

当前本地 checkout 里，`Examples/Tests/restart/` 不只有 3D acceleration 这类传统 restart 场景，还有两条更窄但很有代表性的 PICMI 输入：

- `inputs_test_2d_id_cpu_read_picmi.py`
- `inputs_test_2d_runtime_components_picmi.py`

它们说明 checkpoint/restart 在 WarpX 里不只是“大场景接着跑”的机制，还承担两类更细的接口合同：

1. Python runtime particle attributes 和 `idcpu` 这类底层字段，在 PICMI 前端下能否被稳定写入、读取与恢复；
2. `picmi.Checkpoint(...)` 与 `amr.restart=...` 这套 Python-front-end 配线，是否能作为后续 restart regression 的最小 scaffold。

其中 `inputs_test_2d_runtime_components_picmi.py` 最典型：主测试当前通过脚本内断言检查动态 `newPid` 组件，而 `test_2d_runtime_components_picmi_restart` 仍在 `CMakeLists.txt` 里保留为 `FIXME` scaffold。也就是说，这条线已经证明：

- checkpoint front-end 接线存在；
- runtime components 的写入合同存在；

但还没有把“restart 后这些动态组件仍保持一致”升级成活跃的独立 regression。

同一个 `restart/` 目录里还有一条更传统、但更严格的 field-level restart 基准：`test_3d_acceleration` / `test_3d_acceleration_restart`。它们的输入本身几乎不引入新 physics，核心合同在 `analysis_default_restart.py`：

`load_external_field` 家族则把同一 restart helper 用在更窄但很重要的一类状态恢复上：

- `test_3d_load_external_field_particle_time_restart`
- `test_rz_load_external_field_grid_restart`
- `test_rz_load_external_field_particles_restart`

它们的输入都只是：

- `FILE = <对应非 restart 输入>`
- `amr.restart = ../<对应基线 test>/diags/chk000150`

因此真正验证的不是新的轨道 physics，而是：

1. `read_from_file` 装填的 grid external field 状态能否被 checkpoint 正确保留；
2. `read_from_file` / dependency parser 装填的 particle external field 状态能否被 checkpoint 正确保留；
3. 恢复后的 plotfile 是否仍与非 restart 路径逐字段一致。

这说明 restart 在 WarpX 里不仅验证“场和粒子继续跑”，也验证初始化阶段构造出来的外场寄存器状态能否被完整持久化。

- 基线 run 只提供非 restart 参考 plotfile；
- restart run 从 `chk000005` 恢复；
- analysis 逐字段比较 restart 与非 restart 输出；
- 要求每个字段的最大相对误差都小于 `1e-12`。

这说明这组回归真正验证的不是“加速物理现象”，而是 3D acceleration 基线上的 restart 可重复性。

同一个 `restart/` 目录里还挂着一串更细的 PSATD 变体：

- `test_3d_acceleration_psatd`
- `test_3d_acceleration_psatd_restart`
- `test_3d_acceleration_psatd_time_avg`
- `test_3d_acceleration_psatd_time_avg_restart`

它们的结构和 `test_3d_acceleration` / `test_3d_acceleration_restart` 一样，也是“先跑一条非 restart baseline，再从 `chk000005` 恢复并做逐字段对照”，但工作流语义更窄：

1. `inputs_test_3d_acceleration_psatd` 把 `algo.maxwell_solver` 切到 `psatd`，关闭 `particles.use_fdtd_nci_corr` 与 `psatd.current_correction`，并打开 `psatd.use_default_v_galilean = 1`；
2. `inputs_test_3d_acceleration_psatd_time_avg` 再在此基础上额外打开 `psatd.do_time_averaging = 1`；
3. 两条 restart 变体都只做：
   - `FILE = <对应非 restart 输入>`
   - `amr.restart = ../<对应基线 test>/diags/chk000005`
   然后复用同一个 `analysis_default_restart.py`。

因此这组条目的真实定位不是独立的“PSATD 色散 benchmark”，而是：

- `PSATD + Galilean acceleration workflow` 的 restart 可重复性；
- `PSATD + time averaging` 打开后同一工作流的 restart 可重复性。

它们证明的是 spectral / time-averaged update 路径不会在 checkpoint 边界上丢失状态，而不是重新验证 PSATD 理论公式本身。

`restart_eb/` 则提供了另一条更窄的边界：`inputs_test_3d_eb_picmi.py` 明确把：

- PICMI front-end
- embedded boundary
- `picmi.Checkpoint(...)`
- `amr.restart=...`
- `warpx_save_particles_at_xhi/eb`

放进同一个最小脚本里。当前活跃 test 仍是 checksum-only，显式 restart 变体在 `CMakeLists.txt` 里还是 `FIXME` scaffold。因此它能证明的是：

- EB + PICMI + checkpoint 这条前端配线已经能稳定建起来；

但还不能被夸大成“EB restart 后所有状态都已有独立强 analysis 覆盖”。

这条边界还可以再写得更精确一点。`restart_eb/` 目录里确实同时放着：

- `analysis_default_regression.py`
- `analysis_default_restart.py`

但当前活跃 `CMakeLists.txt` 只注册了：

- `test_3d_eb_picmi`
  - `analysis = OFF`
  - `checksum = "analysis_default_regression.py --path diags/diag1000060"`

而显式 restart 变体整段仍被注释成 `FIXME`：

- `test_3d_eb_picmi_restart`
  - `"inputs_test_3d_eb_picmi.py amr.restart='../test_3d_eb_picmi/diags/chk000030'"`
  - `"analysis_default_restart.py diags/diag1000060"`

因此 `restart_eb/analysis_default_restart.py` 在当前本地 checkout 里的角色，不是“已有活跃强回归”，而是：

1. 代码层已经准备好的 field-level restart helper；
2. 但注册层仍未真正打开的 EB restart scaffold。

这点很重要，因为它说明 `restart_eb/` 目前已经证明：

- EB + PICMI + checkpoint 输出链能稳定运行；

但还没有证明：

- `amr.restart=...` 后 EB 几何、场和粒子状态已经在活跃 CI 中被逐字段强对照覆盖。
