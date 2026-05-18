# `electrostatic_sphere`：初始自场膨胀、solver/frame/grid/weighting 变体的验证地图

绑定对象：

- `../warpx/Examples/Tests/electrostatic_sphere`
- `../warpx/Source/Initialization/WarpXInitData.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolver/*`

这一组条目此前在索引里还停留在：

- `electrostatic / Poisson`
- `待读取输入文件并记录物理检查量`

但实际看完 CMake、analysis 和 inputs 以后，它的真实角色更具体：

- 不是一般的“Poisson 能不能解”
- 而是“一个初始静止均匀电子球在自身 Coulomb 场下膨胀时，初始化出的自场、粒子推进前后的能量账本，以及若干 solver/frame/grid/weighting 变体是否仍成立”

---

## 1. 主 analysis：既测解析电场，也测 lab-frame 势能账本

`analysis_electrostatic_sphere.py` 的核心不是 checksum，而是两类强断言。

### 1.1 电场解析对照

脚本先从输出时间 `t_max` 反求此时电子球半径 `r_end`，再构造解析电场：
$$
E(r)=
\operatorname{sign}(r)\left[
\frac{q_{\mathrm{tot}}}{4\pi\epsilon_0 r^2}\mathbf{1}_{|r|\ge r_{\mathrm{end}}}
\frac{q_{\mathrm{tot}}|r|}{4\pi\epsilon_0 r_{\mathrm{end}}^3}\mathbf{1}_{|r|<r_{\mathrm{end}}}
\right].
$$

然后沿轴提取：

- 3D Cartesian：`Ex/Ey/Ez`
- RZ：`Er/Ez`

并在去掉 PEC 边界影响后的子区间上比较相对 `L2` 误差。

所以这组 test 的第一主合同是：

- `initialize_self_fields` 之后得到的初始自场
- 再加上后续 electrostatic 演化
- 是否仍与均匀带电球的解析膨胀解一致

### 1.2 只在 lab-frame 变体上检查能量守恒

脚本的第二层断言只有在粒子 openPMD diagnostics 含 `phi` 时才会触发。

这正对应输入里：

- `warpx.do_electrostatic = labframe`
- `diag2.electron.variables = ... phi`

脚本用粒子 `phi` 重建：

- 动能
- 自场势能 `0.5 \sum w q \phi`

然后比较初末总能量。

因此 `electrostatic_sphere` 不是所有变体都在做能量检查，而是：

- 所有变体都做解析电场对照
- 只有 lab-frame 粒子写出带 `phi` 的那些变体额外做能量账本验证

---

## 2. 这组 test 真正覆盖的是 `initialize_self_fields` 主链，而不只是 Poisson

从输入结构看，这组 case 的公共骨架是：

- 静止电子球
- `profile = parse_density_function`
- `momentum_distribution_type = at_rest`
- electrostatic solver
- diagnostics 在最后一步输出

更关键的是它不是手工塞一个解析 `E` 场进来，而是要求 WarpX 自己从初始电荷分布得到空间电场，再让球体在这个自场下膨胀。

因此它实际覆盖的是：

1. 初始粒子云几何是否被正确注入；
2. `InitData()`/solver 初始化后是否能给出自洽初始自场；
3. 后续 electrostatic 推进是否保留了解析膨胀行为。

所以这组更准确的分类应是：

- `initialization / electrostatic self-field expansion`

而不是笼统的 `electrostatic / Poisson`。

---

## 3. 各输入变体测的不是同一件事

### 3.1 `inputs_test_3d_electrostatic_sphere`

它只是基线 3D relativistic electrostatic 版本：

- `FILE = inputs_base_3d`
- `warpx.do_electrostatic = relativistic`

因此它主要验证：

- 3D relativistic electrostatic 自场初始化
- 以及解析膨胀场解

### 3.2 `inputs_test_3d_electrostatic_sphere_lab_frame`

这个变体只改了两件关键事：

- `warpx.do_electrostatic = labframe`
- `diag2.electron.variables = x y z ux uy uz w phi`

因此它相对基线新增的不是几何，而是：

- 用粒子 `phi` 打通 lab-frame electrostatic 能量账本

所以它应记成：

- `lab-frame self-field expansion + energy conservation`

### 3.3 `inputs_test_3d_electrostatic_sphere_lab_frame_mr_emass_10`

这组同时打开了：

- `amr.max_level = 1`
- 全域 refine
- `warpx.do_electrostatic = labframe`
- `electron.mass = 10`
- `max_step = 2`

这里 `electron.mass = 10` 不是物理设定，而是数值手段：减慢膨胀速度，让 MR + lab-frame 自场解在更短步数内仍能被稳定比较。

因此它更准确的角色是：

- `lab-frame + MR self-field expansion`

而不是“另一组普通 sphere test”。

### 3.4 `inputs_test_3d_electrostatic_sphere_rel_nodal`

这组最关键的变化是：

- `warpx.grid_type = collocated`

也就是说，它不是换物理，而是在验证：

- collocated / nodal electrostatic field layout
- 对同一解析膨胀问题是否仍然成立

因此应单独记成：

- `collocated relativistic self-field expansion`

### 3.5 `inputs_test_3d_electrostatic_sphere_adaptive`

这组不再给 `const_dt`，而是打开：

- `stop_time`
- `warpx.cfl`
- `warpx.dt_update_interval`
- `warpx.max_dt`
- reduced diagnostic `Timestep`

analysis 本身没有直接读取 `timestep` reduced diag，但它会使用输出文件里的实际 `t_max` 反解理论半径，因此仍然可以对 adaptive-dt 的最终状态做强分析。

所以它应记成：

- `adaptive-dt self-field expansion`

而不是普通 3D 基线。

### 3.6 `inputs_test_rz_electrostatic_sphere`

这组切到：

- `geometry.dims = RZ`
- `warpx.do_electrostatic = labframe`
- `diag2` 写粒子 `phi`

因此它同时验证：

- RZ electrostatic 自场膨胀
- `Er/Ez` 的轴向解析对照
- 以及 lab-frame 势能账本

### 3.7 `inputs_test_rz_electrostatic_sphere_uniform_weighting`

这组相对上一条新增：

- `electron.num_particles_per_cell_each_dim = 6 2 2`
- `electron.radial_numpercell_power = 1.`
- `electron.xmax = R0`

也就是显式切到 RZ uniform-weighting 粒子装填。

analysis 里也为它单独放宽了能量容差。

因此这组真正新增验证的是：

- `uniform radial weighting` 下的自场初始化与能量账本

---

## 4. `analysis_default_regression.py` 与 `catalyst_pipeline.py` 的边界

这组里还有两个容易被误读的文件。

### 4.1 `analysis_default_regression.py`

它只是通用 checksum helper：

- 自动识别 plotfile / openPMD
- 调 `checksumAPI.evaluate_checksum(...)`

不提供新的物理断言。

### 4.2 `catalyst_pipeline.py`

这是 ParaView Catalyst 的可视化脚本：

- 计算 `|E|`
- threshold
- clip
- PNG extractor

因此它是：

- in-situ / postprocess visualization artifact

不是 regression analysis。

---

## 5. 这组条目整理后，应怎样写进索引

`electrostatic_sphere` 这组至少应拆成以下几类：

- `analysis_electrostatic_sphere.py`
  - `initialization / electrostatic self-field expansion`
- `inputs_test_3d_electrostatic_sphere`
  - `relativistic self-field expansion`
- `inputs_test_3d_electrostatic_sphere_lab_frame`
  - `lab-frame self-field expansion + energy conservation`
- `inputs_test_3d_electrostatic_sphere_lab_frame_mr_emass_10`
  - `lab-frame + MR self-field expansion`
- `inputs_test_3d_electrostatic_sphere_rel_nodal`
  - `collocated relativistic self-field expansion`
- `inputs_test_3d_electrostatic_sphere_adaptive`
  - `adaptive-dt self-field expansion`
- `inputs_test_rz_electrostatic_sphere`
  - `RZ self-field expansion + energy conservation`
- `inputs_test_rz_electrostatic_sphere_uniform_weighting`
  - `RZ uniform-weighting self-field expansion`
- `analysis_default_regression.py`
  - checksum helper
- `catalyst_pipeline.py`
  - visualization helper

这样它才不会继续和：

- `electrostatic_sphere_eb`
- `open_bc_poisson_solver`
- `effective_potential_electrostatic`

这几组完全不同的 electrostatic 初始化合同混在一起。

---

## 6. 当前阶段性判断

到这一步，`Initialization` 的 electrostatic 验证层已经可以清楚分成三类：

1. self-field expansion：
   - `electrostatic_sphere`
   - `space_charge_initialization`
   - `relativistic_space_charge_initialization`
2. electrostatic / EB / conductor：
   - `electrostatic_sphere_eb`
   - `effective_potential_electrostatic`
3. open / mixed / geometry-specific Poisson contracts：
   - `open_bc_poisson_solver`
   - `magnetostatic_eb`
   - `nodal_electrostatic`

因此下一步最自然的不是再回头补这一组源码主链，而是继续把：

- `electrostatic_sphere`
- `electrostatic_dirichlet_bc`
- `effective_potential_electrostatic`

这几条尚未完全压实的 initialization validation 条目继续从粗分类里拆出来。
