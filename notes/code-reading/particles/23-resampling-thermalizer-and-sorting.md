# `Resampling`、`ParticleThermalizer` 与 `Sorting`

绑定源码：

- `../warpx/Source/Particles/Resampling/Resampling.H`
- `../warpx/Source/Particles/Resampling/Resampling.cpp`
- `../warpx/Source/Particles/Resampling/ResamplingTrigger.H`
- `../warpx/Source/Particles/Resampling/ResamplingTrigger.cpp`
- `../warpx/Source/Particles/Resampling/LevelingThinning.H`
- `../warpx/Source/Particles/Resampling/LevelingThinning.cpp`
- `../warpx/Source/Particles/Resampling/VelocityCoincidenceThinning.H`
- `../warpx/Source/Particles/Resampling/VelocityCoincidenceThinning.cpp`
- `../warpx/Source/Particles/ParticleThermalizer/ParticleThermalizer.H`
- `../warpx/Source/Particles/ParticleThermalizer/ParticleThermalizer.cpp`
- `../warpx/Source/Particles/Sorting/SortingUtils.H`
- `../warpx/Source/Particles/Sorting/SortingUtils.cpp`
- `../warpx/Source/Particles/Sorting/Partition.cpp`
- `../warpx/Source/Evolve/WarpXEvolve.cpp`
- `../warpx/Source/WarpX.cpp`
- `../warpx/Docs/source/usage/parameters.rst`

对应 examples / regressions：

- `../warpx/Examples/Tests/resampling/inputs_test_2d_leveling_thinning`
- `../warpx/Examples/Tests/resampling/inputs_test_1d_resample_velocity_coincidence_thinning`
- `../warpx/Examples/Tests/resampling/inputs_test_1d_resample_velocity_coincidence_thinning_cartesian`
- `../warpx/Examples/Tests/resampling/analysis.py`
- `../warpx/Examples/Tests/resampling/CMakeLists.txt`
- `../warpx/Examples/Physics_applications/capacitive_discharge/inputs_base_1d_picmi.py`

这一篇补的是 `Particles/` 里目前还没正式成文的“性能与数值后处理层”：

1. `Resampling` 何时触发、怎样选算法、怎样删粒子
2. `ParticleThermalizer` 在主循环里的插入位置和局部热化语义
3. `Sorting` 在 WarpX 里到底是 AMR buffer 分区、全局 bin 排序，还是 deposition-locality 优化

---

## 1. `Resampling`：species 级开关，加一个 trigger，再挂一个具体算法

`PhysicalParticleContainer.cpp` 构造期先读：

```cpp
pp_species_name.query("do_resampling", do_resampling);
if (do_resampling) { m_resampler = Resampling(species_name); }
```

也就是说，resampling 不是 `MultiParticleContainer` 的全局策略，而是每个 physical species 自己决定是否打开。

`Resampling` 这个类本身很薄，只做两件事：

- `m_resampling_trigger`
- `m_resampling_algorithm`

构造期默认算法是：

```cpp
resampling_algorithm = leveling_thinning
```

当前只支持两类：

- `leveling_thinning`
- `velocity_coincidence_thinning`

如果名字不对，直接 abort。

---

## 2. `ResamplingTrigger`：不是只看固定步数，也可以按 global average ppc 触发

`ResamplingTrigger.cpp` 读两个参数：

- `<species>.resampling_trigger_intervals`
- `<species>.resampling_trigger_max_avg_ppc`

它的合同不是“到某几步一定重采样”，而是：

$$
\texttt{triggered}
=
(\texttt{intervals.contains(step)})
\;\lor\;
\left(\frac{N_{\mathrm{global}}}{N_{\mathrm{cells,global}}} > \texttt{max\_avg\_ppc}\right)
$$

其中 `N_cells,global` 不是构造期立即可得，所以 `initialize_global_numcells()` 第一次被调用时，才通过 `warpx.boxArray(lev).numPts()` 把所有 AMR level 的 cell 数累加出来。

这意味着当前 resampling 的触发判据是：

- 时间调度
- 或 species 全局平均 `ppc`

而不是局部 tile/cell 自适应阈值。

### 2.1 调用位置在主循环里是 `istep[0]+1`

`WarpXEvolve.cpp` 调用的是：

```cpp
mypc->doResampling(Geom(), istep[0]+1, verbose_step);
```

所以 `IntervalsParser` 匹配的是“下一步编号”，不是当前 `istep[0]` 原值。

---

## 3. `doResampling()` 的壳：先全局计数，再 `Redistribute()`，最后统一删 invalid 粒子

`MultiParticleContainer::doResampling()` 只负责遍历所有 `do_resampling` 的 species，真正逻辑在：

```cpp
PhysicalParticleContainer::resample(...)
```

这条链的真实顺序是：

1. `TotalNumberOfParticles()` 做一次全局计数
2. `m_resampler.triggered(...)` 决定是否触发
3. 触发时先 `Redistribute()`
4. 再按 level/tile 调具体 resampling kernel
5. 最后 `deleteInvalidParticles()`

也就是说，resampling 不是“边 merge 边立刻压紧数组”，而是：

- kernel 里先把多余粒子标 invalid
- tile 层结束后再统一删

这和 collision、boundary absorb、EB scrape 的 invalid-id 合同是一致的。

---

## 4. `LevelingThinning`：按 cell 平均权重定义 `level_weight`，再做 Bernoulli thinning

`LevelingThinning` 的输入核心是：

- `resampling_algorithm_target_ratio`
- `resampling_min_ppc`

并明确拒绝旧参数：

- `resampling_algorithm_min_ppc`

### 4.1 它不是全局平权，而是每个 cell 独立做

`LevelingThinning.cpp` 先用：

```cpp
ParticleUtils::findParticlesInEachCell(...)
```

把 tile 内粒子按 cell 分组。对每个 cell：

1. 若 `cell_numparts < min_ppc`，直接跳过
2. 先算 cell 内平均权重
   $$
   \bar w_{\mathrm{cell}}
   $$
3. 定义
   $$
   w_{\mathrm{level}} = \bar w_{\mathrm{cell}} \times \texttt{target\_ratio}
   $$
4. 对所有 `w_i <= w_level` 的粒子做 Bernoulli thinning：
   - 以概率
     $$
     1 - \frac{w_i}{w_{\mathrm{level}}}
     $$
     删除
   - 否则把权重抬到 `w_level`

所以这条算法的物理语义不是“把所有粒子往平均权重拉齐”，而是：

- cell 内只抬小权重粒子
- 大权重粒子完全不动

### 4.2 `analysis.py` 真正在验证什么

`Examples/Tests/resampling/analysis.py` 同时验证两种人为构造的 species：

- `resampled_part1`
  - 所有 cell 都有粒子
  - 初始权重完全相同
  - 验证 resampling 后总粒子数接近
    $$
    N_{\mathrm{final}} \approx \frac{N_{\mathrm{init}}}{t_r^2}
    $$
  - 且所有保留粒子的最终权重都变成同一个 `t_r^2`
- `resampled_part2`
  - 只有一个 cell 有粒子
  - 初始权重按人为构造的 Gaussian 分布
  - 验证 level weight、leveled 粒子数和 untouched heavy tail 都符合解析估计

因此 `test_2d_leveling_thinning` 的 analysis 强度是比较高的，不是普通 checksum。

---

## 5. `VelocityCoincidenceThinning`：先按速度空间分 bin，再把一个 cluster 压成两粒子

这条算法的输入更多：

- `resampling_min_ppc`
- 可选 `resampling_algorithm_target_weight`
- `resampling_algorithm_velocity_grid_type = spherical | cartesian`

若是 spherical grid，还要给：

- `resampling_algorithm_delta_ur`
- `resampling_algorithm_n_theta`
- `resampling_algorithm_n_phi`

若是 cartesian grid，还要给：

- `resampling_algorithm_delta_u = dux duy duz`

### 5.1 它不是简单抽稀，而是 cluster merge

`VelocityCoincidenceThinning.cpp` 的总流程是：

1. 仍按 cell 分组
2. 再在 cell 内把粒子投到 velocity bins
3. 用自带的 device heap-sort 把同 bin 粒子排到一起
4. 对每个 bin 内的 cluster，累计：
   - 总权重
   - 加权平均位置
   - 加权平均动量
   - 总动能
5. 若 cluster 里粒子数 `> 2`
   - 保留 2 个粒子
   - 两者各拿一半总权重
   - 位置都设成 cluster 加权平均位置
   - 动量构造成关于平均动量对称的一对，保证线动量和动能守恒
   - 其余粒子全部标 invalid

所以它和 `LevelingThinning` 的第一性区别是：

- `LevelingThinning` 只改权重和粒子存活
- `VelocityCoincidenceThinning` 会真正改写位置和动量，并做局域动量-能量守恒的二粒子压缩

### 5.2 `target_weight` 的真实语义

若给了：

- `resampling_algorithm_target_weight`

代码会把内部 `m_cluster_weight` 设成它的两倍。原因很直接：每个 cluster 最终要压成两粒子，所以单 cluster 的总权重阈值应对应两个保留粒子之和。

### 5.3 当前 regression 边界

`Examples/Tests/resampling/CMakeLists.txt` 里：

- `test_1d_resample_velocity_coincidence_thinning`
- `test_1d_resample_velocity_coincidence_thinning_cartesian`

都只有 checksum，没有独立 analysis。

因此这两条当前只能稳妥地表述成：

- 覆盖 spherical/cartesian 两种速度网格配置
- 覆盖 `do_resampling + trigger_intervals + velocity binning + merge`
- 但还没有像 `LevelingThinning` 那样把守恒量和统计量写成独立 analysis 断言

---

## 6. `ParticleThermalizer`：全局块参数，插在 boundary 之后、collisions 之前

`ParticleThermalizer` 不在 species 段读参数，而是读单独的：

- `particle_thermalizer.*`

它要求：

- `normal`
- `start`
- `end`
- `momentum_threshold`
- `theta`
- 可选 `species`

并明确限制：

- 支持 1D/2D/3D Cartesian
- 不支持 `RZ`、`RCYLINDER`、`RSPHERE`

### 6.1 主循环插入位置

`WarpXEvolve.cpp` 里的顺序是：

1. moving window
2. `HandleParticlesAtBoundaries(...)`
3. `m_particle_thermalizer.applyThermalizer(*mypc)`
4. collisions

所以 thermalizer 的真实语义是：

- 先让粒子完成越界处理、scraping、sorting
- 再在保留下来的粒子上做局部热化
- 然后这些热化后的动量才会进入后续 collisions

### 6.2 它不是硬墙重置，而是带空间渐进概率的 thermal region

对每个 tile，代码先和 thermalizer region 求 overlap。对落在区域内的粒子，沿指定法向位置 `norm_pos` 定义：

- 区域外左侧：`prob = 0`
- 接近末端：`prob = 1`
- 中间区：
  $$
  \texttt{prob}
  =
  1 - \left(
  \frac{h_{\mathrm{end}}-\Delta x-\texttt{norm\_pos}}
       {h_{\mathrm{end}}-\Delta x-h_{\mathrm{start}}}
  \right)^{1/4}
  $$

然后只对抽中的粒子、且某个方向上
$$
|u_i| > u_{\mathrm{threshold}} c
$$
的分量，重新采一个 Gaussian：

$$
u_i \leftarrow \mathrm{sign}(u_i)\,\mathcal N(0,\sqrt{\theta})\,c
$$

所以这条路径当前更接近“局部热化吸收层”而不是“简单 momentum clipper”。

### 6.3 当前验证边界

这轮检索到：

- 文档参数页有完整描述
- 源码已经接在主循环里
- `particle_absorbing_boundary` 输入实际已经打开 `particle_thermalizer.*`
- `particle_absorbing_boundary/analysis.py` 还会直接断言边界附近反向高速电子权重被压低

因此目前对 thermalizer 最稳妥的结论应该改成：

- 源码主链和参数合同是完整的
- 本地已有一条耦合式 example-level regression 入口
- 但还缺 dedicated thermalizer-only 物理验证入口

更细的验证边界见 [24-thermalizer-validation-and-checksum-boundaries.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/24-thermalizer-validation-and-checksum-boundaries.md)。

---

## 7. `Sorting`：要和 `PartitionParticlesInBuffers()` 区分，它是全局性能排序，不是 AMR 物理分流

前面的 [11-particle-boundaries-buffer-sorting.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/particles/11-particle-boundaries-buffer-sorting.md) 已经覆盖过：

- `PartitionParticlesInBuffers()`

但那条逻辑属于 AMR coarse-fine 物理分流。这里要分开的，是 WarpX 的全局排序优化。

### 7.1 触发点在 `HandleParticlesAtBoundaries()` 最后

`WarpXEvolve.cpp` 里：

```cpp
if (sort_intervals.contains(step+1)) {
    mypc->SortParticlesByBin(
        sort_bin_size, m_sort_particles_for_deposition, m_sort_idx_type);
}
```

也就是说，sorting 不是每个 deposition kernel 自己做，而是在：

- boundary 处理
- EB scraping
- invalid 删除

之后，作为一个独立阶段触发。

### 7.2 默认值是平台相关的

`WarpX.cpp` 里：

- 若存在 species 或 lasers
- GPU 默认 `sort_intervals = 4`
- CPU 默认 `sort_intervals = -1`

文档也明确写了：

- GPU 默认开排序是为了 memory locality
- CPU 默认关

这说明 sorting 的第一目的就是性能，不是物理修正。

### 7.3 两种排序模式

文档和 `MultiParticleContainer::SortParticlesByBin()` 一起看，当前有两种模式：

1. `sort_particles_for_deposition = true`
   - 调 `pc->SortParticlesForDeposition(sort_idx_type)`
   - 对不沉积的 species 直接跳过
   - 目的是让 deposition 更局域、更适合高 ppc GPU
2. `sort_particles_for_deposition = false`
   - 调 `pc->SortParticlesByBin(sort_bin_size)`
   - 按用户给的 cell-bin 大小做一般性空间排序

文档里还明确给了：

- `sort_idx_type = {0,0,0}`：cell-centered
- `{1,1,1}`：node-centered
- `{2,2,2}`：compromise

所以 `Sorting` 不是单一算法名，而是一组：

- 触发间隔
- deposition-specialized vs generic bin sort
- index-type / bin-size 网格语义

的性能配置面板。

### 7.4 `SortingUtils` 只是基础积木

`SortingUtils.H/cpp` 本身不实现全局策略，只提供：

- `fillWithConsecutiveIntegers`
- `stablePartition`
- `copyAndReorder`
- `fillBufferFlag`
- `fillBufferFlagRemainingParticles`

这些既被 AMR buffer 分区用，也被全局粒子重排用。

因此它的角色更准确地说是：

- 粒子重排和按 mask 打标的底层 device-friendly 工具库

不是又一套独立物理算法。

---

## 8. 这一轮补出的结构结论

到这里，`Particles/` 当前剩下的“性能与数值后处理层”已经有了第一篇正式笔记：

1. `Resampling`
   - species 级开关
   - trigger = intervals 或 global average ppc
   - 统一走 invalid 粒子删除合同
2. `LevelingThinning`
   - 按 cell 平均权重定义 `level_weight`
   - 只抬小权重粒子并随机删粒子
   - 有较强的解析 analysis
3. `VelocityCoincidenceThinning`
   - 按速度空间 bin 聚类
   - 每个 cluster 压成两粒子
   - 保动量和动能
   - 当前只有 checksum
4. `ParticleThermalizer`
   - 全局参数块
   - boundary 之后、collisions 之前介入
   - 当前源码链完整，但缺独立 regression
5. `Sorting`
   - 是独立性能阶段，不是 AMR 物理分流
   - GPU 默认开，CPU 默认关
   - 分成 deposition-specialized 和 generic bin sort 两种模式
