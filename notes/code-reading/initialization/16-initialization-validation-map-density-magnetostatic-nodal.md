# `Initialization` 验证补充地图：`load_density`、`magnetostatic_eb`、`nodal_electrostatic`

绑定源码与验证入口：

- `../warpx/Source/Utils/SpeciesUtils.cpp`
- `../warpx/Source/Initialization/PlasmaInjector.cpp`
- `../warpx/Source/Initialization/WarpXInitData.cpp`
- `../warpx/Source/FieldSolver/WarpXSolveFieldsES.cpp`
- `../warpx/Source/FieldSolver/MagnetostaticSolver/MagnetostaticSolver.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/RelativisticExplicitES.cpp`
- `../warpx/Docs/source/usage/parameters.rst`
- `../warpx/Examples/Tests/load_density/`
- `../warpx/Examples/Tests/magnetostatic_eb/`
- `../warpx/Examples/Tests/nodal_electrostatic/`

前两篇初始化验证笔记已经覆盖了：

1. `Langmuir`
2. `space_charge_initialization`
3. `dive_cleaning`
4. `gaussian_beam`
5. `effective_potential_electrostatic`
6. `electrostatic_sphere_eb`
7. `projection_div_cleaner`
8. `load_external_field`
9. `relativistic_space_charge_initialization`
10. `open_bc_poisson_solver`

这一篇只补三组之前还停留在粗分类里的入口：

1. `load_density`
2. `magnetostatic_eb`
3. `nodal_electrostatic`

它们分别对应三种初始化合同：

- 从 openPMD mesh 读密度 profile 并驱动连续注入
- `labframe-electromagnetostatic` 初始电静+磁静场与 EB 边界
- collocated relativistic electrostatic 初始 self-field 与 QED 零触发基准

## 1. `load_density`：验证 `read_density_from_path` 和 moving-window 连续注入

这组 tests 最关键的不是普通 `profile=constant`，而是：

```text
electrons.profile = "read_from_file"
electrons.read_density_from_path = "../test_*_load_density_prepare/example-density.h5"
electrons.do_continuous_injection = 1
warpx.do_moving_window = 1
warpx.moving_window_dir = z
warpx.moving_window_v = 1
```

从 `Source/Utils/SpeciesUtils.cpp` 可以直接看到，`profile = read_from_file` 会走：

```cpp
utils::parser::get(pp_species, source_name, "read_density_from_path", density_file);
pp_species.query("read_density_distributed", distributed);
h_inj_rho.reset(new InjectorDensity((InjectorDensityFromFile*)nullptr, density_file, geom, distributed));
```

这说明 `load_density` 不是在验证某个后处理 reader，而是在验证 `SpeciesUtils::parseDensity()` 如何把 openPMD density mesh 装进 `InjectorDensityFromFile`，随后再由 `PlasmaInjector` 和 `AddPlasma` 主链消费。

### 1.1 prepare 脚本本身就是合同的一部分

`CMakeLists.txt` 明确把每个维度拆成两步：

1. `test_*_load_density_prepare`
2. `test_*_load_density`

prepare 脚本先生成 `example-density.h5`。例如 3D 版本写的是：

```python
density_data = (
    on_axis_density
    * (1 + (x**2 + y**2) / channel_radius**2)
    * np.where(z < ramp_length, z / ramp_length, 1)
)
```

RZ 版本则改成 theta-mode mesh：

```python
density.geometry = io.Geometry.thetaMode
density.axis_labels = ["r", "z"]
```

因此这组 regression 同时验证了两层约定：

1. WarpX 期望的 openPMD density mesh 几何和 metadata
2. 初始化时 `read_density_from_path` 对这些几何的解释

### 1.2 analysis 断言的是“注入后的 `rho` 是否重建回原 profile”

这组 analysis 都不直接比较输入文件，而是读取 diagnostics 里的 `rho`：

```python
rho, info = ts.get_field("rho", iteration=iteration)
density_sim = -rho / e
```

然后逐步构造理论 profile，并对所有迭代做比较。例如：

- 1D：`z` 线性 ramp + plateau
- 2D：`x` 抛物通道 + `z` ramp
- 3D：`x,y` 抛物通道 + `z` ramp
- RZ：`r` 抛物通道 + `z` ramp

典型断言形式是：

```python
assert np.all(
    abs(density_th[...] - density_sim[...]) / abs(density_th[...]).max() < 0.02
)
```

这里最重要的点不是 2% 或 3% 容差本身，而是脚本会：

```python
for iteration in ts.iterations:
    ...
```

也就是说，这组 tests 不只是验证第 0 步静态初始化，而是在验证 moving window 前进后，`do_continuous_injection` 继续使用同一份 file-driven density 合同。

### 1.3 这组 regression 覆盖的源码链

把输入、分析和源码连起来后，`load_density` 覆盖的是：

1. `SpeciesUtils::parseDensity()` 对 `read_from_file` 的分派
2. `InjectorDensityFromFile` 对 openPMD density mesh 的装载
3. `PhysicalParticleContainer` 中 `do_continuous_injection` 的 species 状态
4. moving window 激活后连续注入如何再次消费这份 density functor
5. 由注入粒子沉积出来的 `rho` 是否重构回输入 profile

所以它应该归入 `Initialization`，而不是留在 `general / to classify`。

## 2. `magnetostatic_eb`：验证 `labframe-electromagnetostatic + EB + initialize_self_fields`

这一组最容易被误判成普通 fieldsolver test，但从初始化角度看，它实际在验证：

- electrostatic solver 选择
- `initialize_self_fields`
- embedded boundary potential
- 初始 magnetostatic solve

之间的联动。

原生 inputs 文件核心部分是：

```text
warpx.do_electrostatic = labframe-electromagnetostatic
warpx.eb_implicit_function = "(x**2+y**2-radius**2)"
warpx.eb_potential(x,y,z,t) = "1."
beam.initialize_self_fields = 1
beam.profile = parse_density_function
beam.density_function(x,y,z) = ((x**2+y**2)<rmax**2) *n0
```

而 `WarpXInitData.cpp` 的 fresh-run 分支清楚写着：

```cpp
ComputeSpaceChargeField(reset_fields);
if (electrostatic_solver_id == ElectrostaticSolverAlgo::LabFrameElectroMagnetostatic) {
    ComputeMagnetostaticField();
}
```

这说明 `magnetostatic_eb` 不是单独调用一个磁静态工具，而是在初始化主链里，先做 electrostatic/self-field，再做 magnetostatic。

### 2.1 原生 CMake 只做 checksum，但 PICMI 输入内嵌了硬断言

`CMakeLists.txt` 对三个 test 都是：

- `analysis = OFF`
- `checksum = analysis_default_regression.py ...`

如果只看 CMake，很容易得出“它只有 checksum”的结论。这个结论不够准确，因为两个 PICMI 输入文件在 `sim.step()` 之后自己带了解析对照。

3D PICMI 版本先计算解析 `E_r`：

```python
def Er_an(r):
    ...
assert er_err < 0.05
```

然后再计算解析 `B_theta`：

```python
def Bt_an(r):
    ...
assert bt_err < 0.05
```

RZ PICMI 版本更严格，分别要求：

```python
assert er_err < 0.02
assert bth_err < 0.02
```

因此这组 regression 的证据层次应该分开写：

1. `inputs_test_3d_magnetostatic_eb`
   - 原生输入路径
   - 当前主要由 checksum 兜底
2. `inputs_test_3d_magnetostatic_eb_picmi.py`
   - PICMI 初始化路径
   - 内嵌解析 `Er/Bt` 误差断言
3. `inputs_test_rz_magnetostatic_eb_picmi.py`
   - RZ/PICMI 初始化路径
   - 内嵌解析 `Er/Btheta` 误差断言

### 2.2 它验证的不是一般 EB，而是“初始化边界条件解”

这组输入把：

- `boundary.field_lo/hi`
- `boundary.potential_lo_z`
- `eb_potential`
- beam current / density

放在同一个初始化合同里。analysis 比较的也不是推进若干步后的结果，而是第 1 步后的平均场剖面。

因此它更准确的归类应该是：

- `initialization / electrostatic / magnetostatic / EB`

而不是泛化成 fieldsolver 或 boundary 的普通例子。

## 3. `nodal_electrostatic`：collocated relativistic self-field 的间接零触发验证

这组 tests 已经粗分类成 `electrostatic / Poisson`，但注释还没写清它到底在断言什么。

输入文件的关键组合是：

```text
warpx.do_electrostatic = relativistic
warpx.grid_type = collocated
algo.particle_pusher = vay
beam_p.initialize_self_fields = 1
beam_p.do_qed_quantum_sync = 1
```

文档里也明确写了：

- `warpx.grid_type = collocated` 推荐给相关 electrostatic/QED 组合
- QED 场推送当前只支持 collocated grid

因此这组 test 的第一个作用，是验证 `ReadParameters()` 允许这一组：

- relativistic electrostatic
- collocated grid
- Vay pusher
- positron beam 自洽初始场
- QED quantum synchrotron

共同落成可运行对象图。

### 3.1 analysis 不比较场，而是比较“本应为零的辐射副作用”

`analysis.py` 很短，但语义很强：

```python
chi_max = np.loadtxt(fname)[:, 19]
assert np.all(chi_max < 2e-8)
```

和

```python
pho_num = np.loadtxt(fname)[:, 7]
assert pho_num.all() == 0.0
```

这说明它验证的不是“场值长什么样”，而是：

1. 初始 self-field 求解没有制造出过强的局域场
2. collocated relativistic electrostatic 初始化不会假激发 QED quantum synchrotron
3. 因而不会错误地产生 photon species

换句话说，这是一个“零触发基准”。它通过 `ParticleExtrema` 和 `ParticleNumber` 两个 reduced diagnostics，间接检验初始化态是否物理自洽。

### 3.2 它仍然属于初始化验证，但证据类型和前两组不同

这组 regression 和前面的区别是：

1. `load_density`
   - 直接比较沉积回来的 `rho`
2. `magnetostatic_eb`
   - 直接比较解析 `E/B` 剖面
3. `nodal_electrostatic`
   - 间接比较初始化场是否诱发了本不该出现的 QED observable

所以它应该保留在 `electrostatic / Poisson` 大类下，但说明里要明确写成：

- collocated relativistic self-field 的 reduced-diagnostic 零触发验证

而不是笼统写“待定”。

## 4. 回填到 initialization 验证总图后的结论

把这三组补上后，第 3A 章可以把 `Initialization` 的本地证据压成更完整的 13 类：

1. parser 初始化与常规宏粒子装填：`Langmuir`
2. `gaussian_beam` 注入几何：`focusing_gaussian_beam`、`rotated_gaussian_beam`
3. openPMD 粒子文件注入：`focusing_gaussian_beam_from_openpmd*`
4. file-driven density 注入与连续装填：`load_density*`
5. lab-frame 初始 self-field：`space_charge_initialization`
6. relativistic 初始 self-field：`relativistic_space_charge_initialization`
7. electrostatic / effective potential / open-boundary Poisson：`effective_potential_electrostatic`、`open_bc_poisson_solver*`
8. electrostatic / magnetostatic / EB 联合初始化：`magnetostatic_eb*`
9. electrostatic / EB Poisson：`electrostatic_sphere_eb*`
10. 外部 grid / particle fields：`load_external_field*`
11. projection cleaner：`projection_div_cleaner*`
12. collocated relativistic electrostatic 零触发基准：`nodal_electrostatic`
13. 演化态 `div(E)` cleaning：`dive_cleaning`

因此这三组都应并入 initialization 验证地图，而不是继续留在“待分类”状态。

## 5. 当前边界

这篇笔记仍然只基于：

- 本地源码
- examples / CMake / inputs / analysis
- 官方参数文档

没有运行 WarpX 二进制，也没有重新生成这些 regression 的数值结果。

所以这里记录的是“当前本地代码树如何声明和验证初始化合同”，不是本轮现场复现实验结果。
