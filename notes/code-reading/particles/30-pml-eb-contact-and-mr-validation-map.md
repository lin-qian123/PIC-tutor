# `point_of_contact_eb`、`particles_in_pml`、`subcycling_mr` 与 `Langmuir multi_mr` 的验证边界

绑定对象：

- `../warpx/Examples/Tests/point_of_contact_eb`
- `../warpx/Examples/Tests/particles_in_pml`
- `../warpx/Examples/Tests/subcycling`
- `../warpx/Examples/Tests/langmuir`
- `../warpx/Source/Diagnostics/BoundaryScrapingDiagnostics.*`
- `../warpx/Source/Particles/ParticleBoundaryBuffer.cpp`

这一组条目都与粒子直接相关，但验证对象并不相同：

- `point_of_contact_eb`：BoundaryScraping/openPMD 写出的接触点、接触时刻和法向
- `particles_in_pml`：带粒子的 PML 是否真正吸掉粒子留下的场
- `subcycling_mr`：AMR + subcycling + moving-window + continuous injection 的组合稳定性
- `Langmuir multi_mr`：mesh refinement 下 Langmuir 波场解与 charge conservation 是否仍保持解析一致

---

## 1. `point_of_contact_eb`：真正验证的是 BoundaryScraping 记录下来的接触几何

### 1.1 输入结构

这组 test 同时有：

- `inputs_test_3d_point_of_contact_eb`
- `inputs_test_rz_point_of_contact_eb`

共同结构都很直接：

- `algo.maxwell_solver = none`
- 单个电子
- 一个简单解析 EB
- `electron.save_particles_at_eb = 1`
- 两套 diagnostics：
  - `diag1 = Full`
  - `diag2 = BoundaryScraping`

其中关键不是 full plotfile，而是：

```text
diag2.diag_type = BoundaryScraping
diag2.format = openpmd
```

也就是说，这组 regression 在测的不是“粒子最终在哪”，而是：

- 撞到 EB 的那个瞬间
- `BoundaryScraping` 输出里是否记录了正确的
  - `stepScraped`
  - `deltaTimeScraped`
  - `x/y/z`
  - `nx/ny/nz`

### 1.2 3D analysis 的真实断言

`analysis.py` 直接打开：

```python
ts_scraping = OpenPMDTimeSeries("./diags/diag2/particles_at_eb/")
```

读取的就是 `particles_at_eb` 里的 scraped-particle 记录，而不是主 species。

它把数值值和一个解析参考值比较：

- `step_scraped`
- `deltaTimeScraped`
- `x/y/z`
- `nx/ny/nz`

容差非常紧：

- 位置相对误差 `1e-3`
- 时间戳相对误差 `1e-2`
- 法向相对误差 `1e-2`

因此这组 regression 真正验证的是：

- EB scraping 不只是“粒子删掉了”
- 而是 `BoundaryScraping` 输出中接触点的几何量与时间量都是对的

### 1.3 RZ 变体的边界

`inputs_test_rz_point_of_contact_eb` 用的是：

- `geometry.dims = RZ`
- `warpx.eb_implicit_function = "-(x**2 -0.2**2)"`

analysis 仍然复用同一个脚本，因此它测的是相同的 writer 合同，只是几何变成：

- RZ + periodic z
- 轴对称 EB 接触点

所以 `point_of_contact_eb` 更准确的分类应当是：

- `embedded boundary / BoundaryScraping / openPMD contact geometry`

而不是笼统的 “EB test”。

---

## 2. `particles_in_pml`：真正验证的是粒子离域后场是否被 clean 掉

### 2.1 analysis 看的不是粒子，而是剩余 `E`

`analysis_particles_in_pml.py` 逻辑非常集中：

1. 读取最后一个 full diagnostics
2. 如果有 MR，就先按 `max_level` 重建覆盖网格尺寸
3. 取 `Ex/Ey/Ez`
4. 比较整个域内最大电场幅值是否低于阈值

关键判断是：

```python
max_Efield = max(Ex_array.max(), Ey_array.max(), Ez_array.max())
assert max_Efield < tolerance_abs
```

这组 test 的物理含义是：

- 如果 PML 只吸场不吸粒子，离开的粒子会留下伪电荷和伪场
- 打开 `warpx.pml_has_particles = 1` 后，这个残余场应该显著下降

因此它在验证：

- 带粒子 PML 的粒子吸收路径
- `do_pml_in_domain`
- `do_pml_j_damping`

最终是否把粒子离开后留下的 spurious field 压到足够小。

### 2.2 2D/3D 与 MR 变体的区别

2D 与 3D 的 base 输入都采用：

- 单个电子和单个质子
- 相反方向出射
- `warpx.pml_has_particles = 1`
- `algo.particle_pusher = vay`
- `algo.current_deposition = esirkepov`

但 tolerance 明显按维度和 MR 分开：

- 2D level 0：`3e-4`
- 2D level 1：`6e-4`
- 3D level 0：`10`
- 3D level 1：`110`

MR 版本则进一步打开：

- `amr.max_level = 1`
- 2D：`ref_patch_function(...)`
- 3D：`fine_tag_lo/hi`

因此 `particles_in_pml` 这一组应当理解成：

- 同一条 physics contract
- 在 `2D/3D` 与 `single-level/MR` 四种组合下重复验证

不是四个互相独立的物理问题。

### 2.3 当前最准确的分类

它更适合记成：

- `PML / particle absorption / residual-field cleanup`

而不是只写 `PML`。

---

## 3. `subcycling_mr`：当前是只有 checksum 的 AMR 组合稳定性基线

`subcycling/CMakeLists.txt` 当前只有：

- `test_2d_subcycling_mr`
- `analysis = OFF`
- 只保留 checksum

输入 `inputs_test_2d_subcycling_mr` 打开的是一整组组合条件：

- `warpx.do_subcycling = 1`
- `amr.max_level = 1`
- moving window
- driver beam + witness beam
- plasma continuous injection
- `particles.deposit_on_main_grid = plasma_e plasma_p`
- `n_current_deposition_buffer = 0`
- `n_field_gather_buffer = 0`

因此它当前并不是单独验证某个局部公式，而是：

- `AMR + subcycling + moving window + continuous injection + deposit_on_main_grid`

这整组粒子/网格组合在 2D accelerator-like 场景下是否稳定。

因为没有独立 analysis，这条 regression 当前最准确的表述应当是：

- 组合稳定性 checksum 基线
- 不是强物理量断言

也不该误写成“已经单独验证 refined injection 均匀性”。

这里还要单独记一条 helper 边界：`subcycling/analysis_default_regression.py` 只是目录内 checksum helper 副本，代码与顶层 `Examples/analysis_default_regression.py` 同构。当前 `CMakeLists.txt` 只有：

- `test_2d_subcycling_mr`
  - `analysis = OFF`
  - `checksum = "analysis_default_regression.py --path diags/diag1000250"`

因此 helper 本身不增加新的 AMR/subcycling 物理断言；它只负责给这条组合工作流提供历史输出基线。

---

## 4. `Langmuir multi_mr`：MR 不是只看 checksum，而是继续复用解析场解与 charge conservation

和 `subcycling_mr` 不同，`langmuir` 里的 MR 变体仍然复用 `analysis_2d.py`，因此它们是有强 analysis 的。

这也意味着 `multi_mr` 只是更大 Langmuir 家族里的一个切片，而不是单独的 MR-only smoke test。后续如果在回归索引里看到 `test_2d_langmuir_multi_psatd*`、`..._nodal`、`..._current_correction`、`..._vay_deposition`，应优先把它们归回同一个 `analysis_2d.py` 解析场解合同，而不是误拆成互不相关的小类。

共同主线是：

- 从 `inputs_base_2d` 继承
- 再打开不同 mesh-refinement 组合
- 继续比较 `Ex/Ez` 与解析 Langmuir-wave 场解
- 必要时再做 `divE - rho/eps0` 的 charge-conservation 检查

`analysis_2d.py` 的关键断言是：

1. 直接从 diagnostics 取 `Ex/Ez`
2. 与理论场
   $$
   E_x \propto \sin(k_x x)\cos(k_z z)\sin(\omega_p t),\quad
   E_z \propto \cos(k_x x)\sin(k_z z)\sin(\omega_p t)
   $$
   比较
3. 检查最大相对误差是否低于容差
4. 再调用 `check_charge_conservation(data)`

而 `analysis_utils.py` 说明，charge conservation 只在以下组合下强制检查：

- Esirkepov
- Vay deposition
- 或 PSATD current correction

### 4.1 这一组 MR 变体当前分别在改什么

从输入可以看出：

- `inputs_test_2d_langmuir_multi_mr`
  - `amr.max_level = 1`
  - `amr.ref_ratio = 4`
- `..._anisotropic`
  - `amr.ref_ratio_vect = 4 2`
- `..._maxlevel2`
  - `amr.max_level = 2`
  - `amr.ref_ratio = 2`
- `..._momentum_conserving`
  - `algo.field_gathering = momentum-conserving`
- `..._psatd`
  - `algo.maxwell_solver = psatd`
  - `psatd.current_correction = 0`

所以这组条目的真实角色不是“MR 打开了就顺手测一下”，而是：

- MR 基础版本
- 各向异性 refinement ratio
- 更深层级数
- gather scheme 切换
- solver 切换

在同一个 Langmuir-wave 解析基准上做系统覆盖。

### 4.2 当前最准确的分类

这些条目更适合记成：

- `Langmuir wave / mesh refinement / field-theory consistency`

而不是简单写成 `Langmuir wave / plasma oscillation`。

---

## 5. 这组条目对 `Particles` validation 图景的补充

把这四类合起来之后，`Particles` 相关的验证层又补上了一块此前容易混乱的区域：

1. `point_of_contact_eb`
   - 验证 EB 接触点被 `BoundaryScraping/openPMD` 正确记录
2. `particles_in_pml`
   - 验证带粒子 PML 后，粒子离域留下的残余场是否足够小
3. `subcycling_mr`
   - 当前仍是粒子-AMR 组合稳定性的 checksum 基线
4. `Langmuir multi_mr`
   - 则是 mesh refinement 下继续保留解析场解和 charge-conservation 强检查的真正 MR 基准

因此索引里不应再把它们混成：

- `general / to classify`
- 纯 `PML`
- 或过粗的 `plasma oscillation`

它们各自验证的是不同层面的粒子/网格合同。
