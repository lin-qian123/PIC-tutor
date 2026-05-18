# Reduced Diagnostics 代表性案例精读

绑定源码：

- `../warpx/Source/Diagnostics/ReducedDiags/FieldProbe.*`
- `../warpx/Source/Diagnostics/ReducedDiags/FieldProbeParticleContainer.*`
- `../warpx/Source/Diagnostics/ReducedDiags/ParticleHistogram.*`
- `../warpx/Source/Diagnostics/ReducedDiags/ParticleHistogram2D.*`
- `../warpx/Source/Diagnostics/ReducedDiags/LoadBalanceCosts.*`
- `../warpx/Source/Diagnostics/ReducedDiags/LoadBalanceEfficiency.*`

对应文档与例子：

- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Docs/source/dataanalysis/formats.rst`
- `../warpx/Docs/source/usage/workflows/plot_distribution_mapping.rst`
- `../warpx/Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags`
- `../warpx/Examples/Tests/reduced_diags/analysis_reduced_diags.py`
- `../warpx/Examples/Tests/reduced_diags/analysis_reduced_diags_impl.py`
- `../warpx/Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags_load_balance_costs_*`
- `../warpx/Examples/Tests/reduced_diags/analysis_reduced_diags_load_balance_costs.py`
- `../warpx/Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc`

## 1. `FieldProbe` 不是“取一个网格点”，而是“放一批只 gather 不 evolve 的探针粒子”

`FieldProbe` 继承自 `ReducedDiags`，但内部又自带一个独立粒子容器：

```cpp
FieldProbeParticleContainer m_probe;
```

这意味着它不是直接对某个 `MultiFab` 索引做采样，而是先在 `InitData()` 里构造探针粒子，再在 `ComputeDiags()` 里对这些粒子做 `doGatherShapeN(...)`。

`FieldProbeParticleContainer` 也不是普通物理 species。它是一个 `ParticleContainerPureSoA`，只保存：

- 位置
- `Ex/Ey/Ez`
- `Bx/By/Bz`
- `S`
- RZ/球坐标额外角变量

没有动量、权重、沉积或 push 主链。

## 2. 三种几何其实都在构造“探针粒子云”

`<reduced_diag>.probe_geometry` 只决定 `InitData()` 怎样生成这批粒子：

- `Point`：放一个点。
- `Line`：在 `(x_probe,y_probe,z_probe)` 到 `(x1_probe,y1_probe,z1_probe)` 之间等距放 `resolution` 个点。
- `Plane`：以 `(x_probe,y_probe,z_probe)` 为中心，按 `target_normal` 和 `target_up` 构造一个正方形平面，并沿两个方向各放 `resolution` 个点，总数是 `resolution^2`。

也就是说，`FieldProbe` 的 line/plane 并没有额外的数据结构；本质上仍然是更多 probe particles。

## 3. `FieldProbe` 采样的是 `aux` 场，不是原始 `fp` 场

`ComputeDiags()` 在每个 level 上取的是：

```cpp
FieldType::Efield_aux
FieldType::Bfield_aux
```

而不是 `Efield_fp/Bfield_fp`。这说明 field probe 默认站在 WarpX 的“给粒子 gather 用的辅助场”一侧，而不是“场推进器主寄存器”一侧。

因此它天然继承了前面 AMR 笔记里已经梳理过的那条链：

1. `UpdateAuxilaryData*()` 生成 `aux`
2. probe particles 对 `aux` 做 gather
3. line/plane/point 只是 probe-particle 几何布置不同

## 4. `FieldProbe` 的 moving window 不是场回推，而是直接平移探针粒子

`do_moving_window_FP = 1` 时，`FieldProbe::ComputeDiags()` 会在每次计算前按：

```cpp
move_dist = dt * WarpX::moving_window_v * step_diff;
```

把 probe particle 坐标沿 moving-window 方向整体平移。

这说明 moving-window 支持不是“对历史场做 back-transform”，而是“让探针跟着窗口一起跑”。文档也明确指出 boosted-frame 下这里只记录 boosted-frame 数据，不做 Lorentz back transformation。

## 5. `integrate = 1` 的语义是“每步都积”，不是“输出时再积分”

`FieldProbe` 有两套节拍：

- `m_intervals.contains(step+1)` 决定何时写出
- `integrate = 1` 决定是否每步把采样值乘 `dt` 累加到粒子属性

源码里这两件事被明确拆开：

```cpp
if (temp_field_probe_integrate) {
    part_Ex[ip] += Exp * dt;
    ...
} else {
    part_Ex[ip] = Exp;
    ...
}
```

所以积分型 probe 的真实语义是：

- 每个时间步都继续 gather
- 到输出步才把累计结果写文件

这和 `FieldPoyntingFlux` 一样，也是一种“内部跨步状态”，只是状态存在 probe 粒子 SoA 里。

## 6. `FieldProbe` 的输出不是一张二维表，而是一行一个探针粒子

普通 reduced diagnostics 常见格式是：

- 一步一行
- 多个 quantity 做列

但 `FieldProbe::WriteToFile()` 不是这样。它会把同一步的所有 probe particles 逐个写成多行：

- 每行仍有 `step,time`
- 后面跟一个探针粒子的 `x,y,z,Ex,Ey,Ez,Bx,By,Bz,S`

写之前还会先按 particle id 排序，保证 line/plane 探针输出顺序稳定。

因此 `FieldProbe` 虽然属于 `ReducedDiags`，但它的文件布局已经明显偏离“单行标量表”；更像是“时间步标签 + 探针点采样表”。

## 7. `ParticleHistogram` 是 parser 驱动的一维 weighted binning

`ParticleHistogram` 的核心输入是：

```cpp
histogram_function(t,x,y,z,ux,uy,uz)
```

WarpX 会对每个粒子先算这个标量，再按

```cpp
bin = floor((f - bin_min) / bin_size)
```

决定落到哪个 bin。

默认累加的是粒子权重 `w`；`unity_particle_weight` 才改成每个粒子记 `1`。因此它首先是“带权 histogram”，不是默认的“数 macro-particles”。

另外它的 `ux,uy,uz` 在代码里会除以 `c`，即 parser 收到的是无量纲的 `gamma v / c`。

## 8. `ParticleHistogram` 的几种 normalization 都发生在 MPI 归约之后

实现顺序是：

1. GPU/CPU kernel 对本 rank 粒子做原始 bin 累加
2. `ReduceRealSum(...)` 汇总到 IO rank
3. 只有在 IO rank 上才做：
   - `max_to_unity`
   - `area_to_unity`

这意味着：

- 归一化是全局 histogram 归一化
- 不是每个 MPI rank 各自先归一化再合并

这个细节决定了它可以稳定用于真正的全局分布函数，而不受并行分区影响。

## 9. `ParticleHistogram2D` 已经不是文本表，而是 openPMD 网格输出

`ParticleHistogram2D` 仍然继承自 `ReducedDiags`，但它完全重写了 `WriteToFile()`，把二维表写成 openPMD mesh：

```cpp
auto f_mesh = i.meshes["data"];
data.resetDataset(dataset);
data.storeChunkRaw(...);
```

对应文档 `formats.rst` 也明确把 `ParticleHistogram2D` 列为需要 openPMD 的 reduced diagnostics 例外。

所以它和一维 histogram 的分界线非常清楚：

- `ParticleHistogram`：文本列文件
- `ParticleHistogram2D`：openPMD 二维网格

## 10. `ParticleHistogram2D` 的本体是“二维坐标 parser + 可选 value parser”

它有三类 parser：

- `histogram_function_abs(...)`
- `histogram_function_ord(...)`
- `value_function(...)`

前两者决定粒子落在哪个二维 bin，第三者决定该粒子向该 bin 累加多少值。示例 `laser_ion` 里常直接设置：

```text
value_function(...) = "w"
```

也就是按粒子权重累加，形成 phase-space density 风格的图。

因此 `ParticleHistogram2D` 和一维 histogram 的根本区别不只是“多一个维度”，而是它把“坐标映射”和“累加值”彻底分离了。

## 11. `ParticleHistogram2D` 的 writer 还自带物理坐标轴元数据

openPMD writer 会把这些元数据一起写进去：

- `function_abscissa`
- `function_ordinate`
- `filter`
- `gridGlobalOffset = {bin_min_ord, bin_min_abs}`
- `gridSpacing = {bin_size_ord, bin_size_abs}`
- `axisLabels = {ordinate, abscissa}`

这说明输出不是裸数组，而是一个带坐标和 parser 语义的二维诊断场。后处理时不需要自己再猜 bin 中心和轴定义。

## 12. `LoadBalanceCosts` 记录的不是抽象效率，而是每个 box 的完整负载快照

`LoadBalanceCosts` 输出的数据粒度是 box，而不是 rank。每个 box 会写：

- `cost`
- `proc`
- `lev`
- `i_low/j_low/k_low`
- `num_cells`
- `num_macro_particles`
- GPU 运行时的 `gpu_ID`
- 额外收集的 `hostname`

其中 `cost` 来源有两条路：

- `Heuristic`：先复制 `WarpX::getCosts(lev)`，再调用 `warpx.ComputeCostsHeuristic(costs)`
- `Timers`：直接使用已有 timers 累积出来的 costs

所以 `LoadBalanceCosts` 不是再算一套独立性能模型；它只是把 load-balance 决策真正使用的 box-cost 状态原样导出。

## 13. `LoadBalanceCosts` 的文件格式故意保留“分布映射几何”

它不仅写 box cost，还写每个 box 的低端索引和 rank/hostname。这正是 `plot_distribution_mapping.rst` 能把结果重新画成：

- rank layout
- cost heatmap

的原因。也就是说，`LoadBalanceCosts` 的目标不是“给一个 scalar 性能数字”，而是把当前 distribution mapping 的几何布局完整暴露给后处理。

## 14. `LoadBalanceCosts` 的最终文件会被补成矩形表

不同时间步 box 数可能不同，所以原始逐步追加会形成 jagged rows。`WriteToFile()` 在最后一步会：

1. 重新打开原文件
2. 按 `m_nBoxesMax` 重写 header
3. 用 `NaN` 把短行补齐
4. 原子替换原始文件

这意味着它不是单纯 append-only；最后一次写出会做一次“表整形”，保证 Python/NumPy 后处理能把整个文件当规则矩阵读入。

## 15. `LoadBalanceEfficiency` 只是对当前 WarpX 负载状态的轻薄包装

`LoadBalanceEfficiency::ComputeDiags()` 本体很薄：

```cpp
m_data[lev] = warpx.getLoadBalanceEfficiency(lev);
```

也就是说：

- 它不重建 box-level costs

## 16. `ColliderRelevant` 的合同不是“再抄一份 ParticleExtrema”，而是把束流碰撞可观测量打包成一张 reduced 表

`Examples/Tests/collider_relevant_diags/` 给了一条很硬的 regression。输入里同时打开：

- `ColliderRelevant_beam_e_beam_p.type = ColliderRelevant`
- `ParticleExtrema_beam_e.type = ParticleExtrema`
- `ParticleExtrema_beam_p.type = ParticleExtrema`

而 analysis 不是只看文件存在，而是逐项核对：

1. `chi_min / chi_max / chi_ave`
2. `theta_x/theta_y` 的 min/ave/max/std
3. 从 full openPMD `rho_beam_e/rho_beam_p` 重建的 `dL/dt`

这里最重要的边界是：`ColliderRelevant` 并不替代 `ParticleExtrema`，它是把 collider 场景真正关心的聚合量压成一张 reduced diagnostics 表，再用 `ParticleExtrema` 和 full diagnostics 交叉验证一致性。

## 17. `DifferentialLuminosity` 和 `DifferentialLuminosity2D` 已经是带解析谱对照的 reduced-diagnostic 强基准

`Examples/Tests/diff_lumi_diag/` 的 analysis 同时验证两条 reduced diagnostics：

1. 一维文本表 `DifferentialLuminosity_beam1_beam2.txt`
2. 二维 openPMD 网格 `DifferentialLuminosity2d_beam1_beam2/`

analysis 直接构造两束高斯束流对撞的解析 luminosity 谱：

- `dL/dE`
- `d^2L/dE_1dE_2`

然后分别和 1D/2D diagnostics 比较，并要求最大相对误差低于设定容差。

这组 regression 的意义是：

1. `DifferentialLuminosity` 不是“随手统计一个 beam observable”，而是有解析谱对照的物理 diagnostics。
2. `DifferentialLuminosity2D` 也不是普通文本列扩展，而是真正通过 openPMD 网格写出二维能量空间分布。
3. photon 版本虽然用 `parse_density_function`、容差更宽，但验证对象与 lepton Gaussian-beam 版本相同。

## 18. `beam_beam_collision` 当前不是 `DifferentialLuminosity` 那类强谱基准，而是 collider-QED 应用骨架

`Examples/Physics_applications/beam_beam_collision/` 很容易被误写成 “luminosity benchmark”。但当前本地 WarpX checkout 里，这组 active regression 的证据层更弱，也更偏应用骨架：

1. `CMakeLists.txt` 里只有
   - `test_3d_beam_beam_collision`
   - `analysis = OFF`
   - `analysis_default_regression.py --path diags/diag1/`
2. 目录内没有独立 `analysis.py`
3. `plot_fields.py` 和 `plot_reduced.py` 都只是后处理可视化脚本

因此它不能和前面的 `ColliderRelevant` / `DifferentialLuminosity` 强 regression 混成一个等级。

### 18.1 这组输入真正覆盖的是哪条联合路径

`inputs_test_3d_beam_beam_collision` 本体把以下几条 runtime 路径绑在一起：

- `warpx.do_electrostatic = relativistic`
- collocated grid
- 两束 `125 GeV` 电子/正电子 Gaussian bunch 对撞
- `initialize_self_fields = 1`
- Quantum Synchrotron photon emission
- Breit-Wheeler pair creation
- `ColliderRelevant_beam1_beam2`
- `ParticleNumber`
- openPMD full diagnostics

也就是说，它当前真正覆盖的是：

- collider self-field
- beamstrahlung
- coherent pair generation
- collider-oriented reduced diagnostics

这条联合应用链能否稳定接通，而不是某个单独 observables 的解析 hard assert。

### 18.2 这组 helper 脚本能说明什么，不能说明什么

- `plot_fields.py`
  只是把 `|E|`、`|B|`、主束荷密度和次级对荷密度切片画出来。
- `plot_reduced.py`
  只是从 `ColliderRelevant_beam1_beam2.txt` 和 `ParticleNumber.txt` 读取：
  - `dL/dt`
  - photon 数
  - NLBW pair 数
  然后画出每个 beam particle 的时间曲线。

它们能说明这组应用输出围绕哪些物理量组织，但不能替代：

- `ColliderRelevant` 的定义断言
- `DifferentialLuminosity` 的解析谱断言
- 或 Yakimenko 2019 的文献级 benchmark

因此在本项目索引里，`beam_beam_collision` 最准确的定位应当是：

- `collider QED application baseline`

而不是：

- `luminosity strong benchmark`
- 不重建 rank map
- 只是把 WarpX 当前的效率标量按 level 写出来

文档里还明确说明，在 costs 尚未建立前，它可能输出 `-1`；最早通常要到 step 2 才有意义。

因此：

- `LoadBalanceCosts` 适合解释“为什么会这样分配”
- `LoadBalanceEfficiency` 适合快速看“当前分配是否更均衡”

## 16. `analysis_reduced_diags_impl.py` 与 `analysis_reduced_diags_load_balance_costs.py` 的断言边界不同

`analysis_reduced_diags_impl.py` 的策略是：

- 从 plotfile 重新计算 field/particle reduced quantities
- 再与 `EF.txt`、`EP.txt`、`PF.txt`、`PP.txt`、`MF.txt`、`MR.txt`、`NP.txt`、`FR_*.txt` 对比

因此它主要验证：

- reduced diagnostics 的物理定义
- 与 full diagnostics / plotfile 一致的数值结果

它不是在专门验证 `FieldProbe` 或 `ParticleHistogram2D`。

相反，`analysis_reduced_diags_load_balance_costs.py` 根本不读 plotfile，而是直接从 `LBC.txt` 读出 box costs，再按 rank 聚合出：

$$
\text{efficiency}=\frac{\text{mean rank cost}}{\max \text{ rank cost}}.
$$

然后只断言：

```python
efficiency_before < efficiency_after
```

所以这个 regression 验证的是：

- `LoadBalanceCosts` 文件能否忠实暴露当前 box/rank cost 分布
- load balancing 之后效率是否真的改善

它不要求和某个固定物理场解逐点一致。

## 17. `inputs_test_3d_reduced_diags` 证明 reduced diagnostics regression 是“混合断言”

这个测试同时放了：

- `FieldEnergy`
- `ParticleEnergy`
- `FieldMomentum`
- `ParticleMomentum`
- `FieldMaximum`
- `FieldPoyntingFlux`
- `FieldProbe`
- `RhoMaximum`
- `FieldReduction`

并在最后配一个 full diagnostics plotfile：

```text
diag1.diag_type = Full
diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz rho rho_electrons rho_protons
```

所以这组 regression 的真实结构不是“只测 reduced diagnostics 自己”，而是：

- reduced diagnostics 给出 compact observable
- full plotfile 提供 reference state
- analysis 脚本重新从 plotfile 算 reference observable

这是 reduced diagnostics 在 WarpX 里最常见的验证方式。

## 18. 目前的 diagnostics 案例层已经能支持三类不同讲解

基于这几类源码和回归例子，第 8 章现在已经可以分别讲清：

1. 物理采样型 reduced diagnostics  
   `FieldProbe`
2. 分布函数/相空间型 reduced diagnostics  
   `ParticleHistogram` / `ParticleHistogram2D`
3. 并行性能与分布映射型 reduced diagnostics  
   `LoadBalanceCosts` / `LoadBalanceEfficiency`

它们共用 `ReducedDiags` 基类，但：

- 输出格式不同
- 内部状态复杂度不同
- regression 断言口径不同

这正好说明 reduced diagnostics 不是一个“只有一套表格 writer 的简单家族”，而是 WarpX 用统一入口挂接多类紧凑观测量的总线。

`FieldProbe` 现在还有一组比 `reduced_diags/` 更直接的强 regression：`Examples/Tests/field_probe/`。

## 19. `Examples/Tests/reduced_diags/` 当前应拆成两棵验证树

当前本地 `reduced_diags` family 不能再写成一个统一的 “reduced diagnostics” 桶。至少要拆成两棵树：

1. `analysis_reduced_diags.py` / `analysis_reduced_diags_impl.py`
   - 对 `inputs_test_3d_reduced_diags`
   - 用 full plotfile 重算：
     - `FieldEnergy`
     - `ParticleEnergy`
     - `FieldMomentum`
     - `ParticleMomentum`
     - `FieldMaximum`
     - `RhoMaximum`
     - parser 驱动的 `FieldReduction`
   - 再和 `EF/EP/PF/PP/MF/MR/NP/FR_*/Edotj.txt` 逐项比
   - 默认容差是 `1e-12`
   - 只有 field energy 因 staggered-vs-cell-centered 差异放宽到 `0.3`
2. `analysis_reduced_diags_load_balance_costs.py`
   - 对 `inputs_test_3d_reduced_diags_load_balance_costs_*`
   - 根本不读 plotfile
   - 只从 `LBC.txt` 重建每个 rank 的总成本
   - 然后检查

$$
\text{efficiency}_{\text{before}} < \text{efficiency}_{\text{after}}.
$$

这说明 `reduced_diags/` 当前同时覆盖：

- 物理量压缩输出和 full-state reference 的一致性
- 并行负载均衡运行态是否被 reduced diagnostics 正确暴露

## 20. `timers_psatd` 与 `single_precision` 目前都只能按边界事实记录

这组 family 里还有两个容易被误写的名字：

1. `inputs_test_3d_reduced_diags_load_balance_costs_timers_psatd`
   - 当前本地 input 只做：
     - `FILE = inputs_base_3d`
     - `algo.load_balance_costs_update = Timers`
   - 并没有真的把 `algo.maxwell_solver` 切到 `psatd`
   - 因此这条只能按“遗留测试名下的 timer-cost workflow baseline”记录
2. `test_3d_reduced_diags_single_precision`
   - 当前本地能确认的是：
     - `analysis_reduced_diags_impl.py` 里预留了 `single_precision=True` 时把容差放宽到 `5e-3` 的代码路径
   - 但没有在 `Examples/Tests/reduced_diags/CMakeLists.txt` 里找到活跃 test/input
   - 所以它当前也只能按 legacy checksum 名记录

这组例子不是只证明 `FieldProbe` 文件能写出来，而是把它接到单缝衍射解析解上。输入里定义：

- 2D plane wave
- embedded boundary single slit
- `FP_line.type = FieldProbe`
- `probe_geometry = Line`
- `integrate = 1`

analysis 读 `diags/reducedfiles/FP_line.txt` 后，会抽取 step 500 的 line probe 通量，再与解析衍射包络

$$
I(x)=I_0\,\mathrm{sinc}^2\!\left(\frac{\pi a}{\lambda}\sin(\arctan(x/D))\right)
$$

逐点比较，并要求远离边界异常区后的平均相对误差小于 `2.5%`。

因此这组 regression 同时绑定了：

- `FieldProbe` 的 line geometry
- probe-particle gather 与积分语义
- reduced text writer 的输出布局
- 以及它作为电磁通量观测量时的物理正确性
