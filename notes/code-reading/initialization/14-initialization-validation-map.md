# `Initialization` 验证入口地图：Langmuir、自洽初始场、Gaussian beam、openPMD 注入、电静态与 projection cleaner

绑定源码与验证入口：

- `../warpx/Source/Initialization/WarpXInitData.cpp`
- `../warpx/Source/Initialization/PlasmaInjector.cpp`
- `../warpx/Source/Particles/ParticleCreation/AddParticles.cpp`
- `../warpx/Source/Initialization/DivCleaner/ProjectionDivCleaner.cpp`
- `../warpx/Source/FieldSolver/WarpXSolveFieldsES.cpp`
- `../warpx/Examples/Tests/langmuir/`
- `../warpx/Examples/Tests/space_charge_initialization/`
- `../warpx/Examples/Tests/dive_cleaning/`
- `../warpx/Examples/Tests/gaussian_beam/`
- `../warpx/Examples/Tests/effective_potential_electrostatic/`
- `../warpx/Examples/Tests/electrostatic_sphere_eb/`
- `../warpx/Examples/Tests/projection_div_cleaner/`

前面的初始化笔记已经把启动层、`ReadParameters()`、`AllocLevelMFs()` 和 `InitData()` 后半消费链拆开了。这一篇只回答一个更实际的问题：这些初始化支线在本地 WarpX 里到底由哪些 tests、analysis 脚本和 checksum 在兜底。

结论先写在前面：

1. `Initialization` 没有一套单独的“初始化测试框架”，而是被多组物理 regression 分摊验证。
2. 这些 regression 大体分成两类：
   - 有显式物理断言的 analysis 脚本
   - 只做 checksum 基线对比的默认回归
3. 对写书最有价值的是前一类，因为它们能告诉我们每条初始化路径到底在验证什么量。

## 1. 初始化验证可以分成六类

从源码和 examples 看，当前 `Initialization` 的本地验证入口主要分成：

1. `Langmuir` 基准：
   - 验证 parser 初始化、周期边界、宏粒子装填、初始动量扰动和 selective particle diagnostics。
2. `space_charge_initialization`：
   - 验证 `species.initialize_self_fields` 触发的初始 self-field 求解。
3. `dive_cleaning`：
   - 验证 `warpx.do_dive_cleaning`、PML 和初始 Gaussian beam 组合。
4. `gaussian_beam` / `external_file`：
   - 验证 `gaussian_beam` 注入、focusing、rotation，以及 openPMD 粒子文件注入。
5. `effective_potential_electrostatic` / `electrostatic_sphere_eb`：
   - 验证 electrostatic solver、effective potential 和带 EB 的 Poisson 初始化。
6. `projection_div_cleaner`：
   - 验证 `warpx.do_initial_div_cleaning` 和外部 `B` 场 projection cleaner。

下面逐条写清每类 regression 覆盖哪条初始化源码链。

## 2. `Langmuir` 是初始化基准线，不只是 evolve 基准线

最容易被低估的是 `langmuir`。它当然是时间推进基准，但它同样在验证初始化主链，尤其是：

- `particles.species_names`
- `NUniformPerCell`
- `profile=constant`
- `parse_momentum_function`
- `serialize_initial_conditions`
- 周期边界下的初始场/粒子一致性

以 `inputs_test_1d_langmuir_multi` 为例：

```text
particles.species_names = electrons positrons

electrons.injection_style = "NUniformPerCell"
electrons.profile = constant
electrons.density = n0
electrons.momentum_distribution_type = parse_momentum_function

positrons.injection_style = "NUniformPerCell"
positrons.profile = constant
positrons.density = n0
positrons.momentum_distribution_type = parse_momentum_function
```

这条输入会穿过：

- `PlasmaInjector` 的位置/密度/动量 functor 分派
- `SpeciesUtils::parseDensity()` / `parseMomentum()`
- `AddPlasma()` 的体注入 kernel

而 analysis 脚本不是只看 checksum。`analysis_1d.py`、`analysis_2d.py`、`analysis_3d.py` 都会把输出场直接和解析 Langmuir 波比较。

例如 `analysis_1d.py` 的核心断言是：

```python
E_sim = data[("mesh", field)].to_ndarray()[:, 0, 0]
E_th = get_theoretical_field(field, t0)
max_error = abs(E_sim - E_th).max() / abs(E_th).max()
assert error_rel < tolerance_rel
check_charge_conservation(data)
```

所以 `Langmuir` 对初始化层的真实价值是：

1. 验证 parser 形式的初始动量扰动确实被写进粒子。
2. 验证初始粒子分布和周期边界能生成正确的 plasma-wave 初态。
3. 验证 diagnostics 中场和粒子 selective output 没把初始化状态写坏。
4. 在部分变体里继续顺手验证离散电荷守恒。

`analysis_3d.py` 还多做了一步：从 openPMD diagnostics 里读取粒子位置上的 `Ex/Ey/Ez`，与理论值比较。这说明 `langmuir` 同时给“初始化后的粒子状态”和“粒子上场采样”做了联通验证。

进一步往当前本地 checkout 看，这条验证树已经不是只有 1D 主例子：

- 2D/3D/RZ 原生输入族大多直接复用 `analysis_2d.py`、`analysis_3d.py`、`analysis_rz.py`
- nodal、PSATD、`JRhom_LL2/LL4`、current-correction、Vay deposition 这些变体并不是新 analysis，而是在同一个解析 Langmuir-wave 合同上测试不同 solver/deposition 组合
- `langmuir_fluids` 是另一棵独立验证树：它不再只看场，而是把 `E/J/rho` 一起和冷流体解析解比较
- 只有 2D/3D/RZ 的 PICMI 变体当前仍主要停留在 `analysis=OFF` 的前端 + checksum scaffold；它们证明的是 PICMI 配线能接上，而不是复用了完整物理 hard assert

## 3. `space_charge_initialization` 直接锚定 `initialize_self_fields`

这是初始化层最直接的一组 regression。`inputs_test_3d_space_charge_initialization` 明确写了：

```text
beam.injection_style = "gaussian_beam"
beam.initialize_self_fields = 1
beam.momentum_distribution_type = "at_rest"
```

这一组输入直接对应源码里的 fresh-run 条件分支：

- `PhysicalParticleContainer::initialize_self_fields`
- `WarpXInitData.cpp` 里对 `has_initialize_self_fields` 的聚合
- `ComputeSpaceChargeField(reset_fields=false)`

analysis 脚本也不是做泛化 checksum，而是直接把 `Ex/Ey/Ez` 和高斯电荷团理论场比较：

```python
factor = (
    Qtot
    / (4 * np.pi * scc.epsilon_0 * r2**1.5)
    * gammainc(3.0 / 2, r2 / (2.0 * r0**2))
)
Ex_th = factor * x_2d
...
assert np.allclose(E, E_th, atol=tolerance_rel * E_th.max())
```

因此这一组 test 的真实验证对象不是一般的 Gaussian beam 注入，而是更具体的：

1. `gaussian_beam` 把初始粒子云生成出来。
2. `initialize_self_fields=1` 触发初始 self-field solve。
3. `ComputeSpaceChargeField()` 在第一个时间步前给出正确的 Coulomb 场。

这里的 checksum 只是第二层保险；第一层硬断言仍然是解析场比较。

## 4. `dive_cleaning` 验证的是“带错误初态的初始化后处理”

`dive_cleaning` 这组 test 不应被误读成纯演化功能测试。它实际验证的是：

- 初始 Gaussian beam 状态先带着 `div(E)-rho/epsilon0` 误差进入系统；
- `warpx.do_dive_cleaning=1` 与 PML 一起，把这份误差传播并吸收掉；
- 最终场回到理论 Gaussian beam 电场。

输入文件关键参数是：

```text
boundary.field_lo = pml pml pml
boundary.field_hi = pml pml pml

warpx.do_dive_cleaning = 1

beam.injection_style = "gaussian_beam"
beam.momentum_distribution_type = "at_rest"
```

而 `analysis.py` 最终比较的是完整电场和理论值：

```python
E_array = (Ex_array**2 + Ey_array**2 + Ez_array**2) ** 0.5
E_th = (Ex_th**2 + Ey_th**2 + Ez_th**2) ** 0.5
assert np.allclose(E, E_th, atol=relative_tolerance * E_th.max())
```

因此这条 regression 覆盖的初始化链是：

1. `gaussian_beam` 初始粒子构造。
2. `ReadParameters()` 中 `do_dive_cleaning` 对 field registry 与 solver contract 的影响。
3. 初始化后第一次真实演化如何从一个并不完全离散一致的初态收敛回正确物理场。

它验证的不是 projection cleaner，而是演化态 `F`-field / hyperbolic `div(E)` cleaning 体系。

## 5. `gaussian_beam` 验证注入几何，而 `external_file` 验证 openPMD 粒子导入合同

这一组要拆成两半看。

### 5.1 `gaussian_beam` 本体：focusing 和 rotation

`inputs_test_3d_focusing_gaussian_beam` 的关键初始化参数是：

```text
beam1.injection_style = gaussian_beam
beam1.focal_distance = focal_distance
beam1.momentum_distribution_type = gaussian
beam1.ux_m = ux
beam1.uy_m = uy
beam1.uz_m = uz
beam1.ux_th = dux
beam1.uy_th = duy
beam1.uz_th = duz
```

`analysis_focusing_beam.py` 读取 openPMD 粒子输出，按 `z` 切片重建束流横向尺寸，然后与理论焦斑公式比较：

```python
sx.append(np.sqrt(np.average((x[i] - mux) ** 2, weights=w[i])))
...
sx_theory = s(subgrid, sigmax, emitx / gamma)
assert np.allclose(sx, sx_theory, rtol=0.051, atol=0)
```

所以它验证的是：

1. `setupGaussianBeam()` 对 position / momentum 的协同初始化。
2. `focal_distance` 如何把“在焦点定义的高斯束”回推到当前初始面。
3. 初始化后的粒子统计量是否符合束流光学理论。

`inputs_test_3d_rotated_gaussian_beam` 则额外打开：

```text
beam1.do_gaussian_beam_rotation = 1
beam1.do_gaussian_beam_rotation_momenta = 1
beam1.gaussian_beam_rotation_angle = rotation_angle
beam1.gaussian_beam_rotation_axis = 0 1 0
```

`analysis_rotated_beam.py` 会先把束流旋回原坐标系，再同时检查：

1. 各 `z` slice 上的束斑尺寸。
2. 平均纵向动量 `uz_m ≈ gamma`。
3. 横向动量方差 `ux_th ≈ emitx / sigmax`。

这条 regression 因而直接覆盖了 `PlasmaInjector::setupGaussianBeam()` 里位置旋转和动量旋转两条支线。

### 5.2 `external_file`：openPMD 粒子文件注入

`inputs_test_3d_focusing_gaussian_beam_from_openpmd` 的初始化 contract 更直接：

```text
beam1.injection_style = external_file
beam1.injection_file = ../test_3d_focusing_gaussian_beam_from_openpmd_prepare/openpmd_generated_particles.h5
```

配套的准备脚本 `inputs_test_3d_focusing_gaussian_beam_from_openpmd_prepare.py` 先用 `openpmd_api` 生成文件，并显式写入：

```python
electrons["weighting"][SCALAR].make_constant(npart / nmacropart)
electrons["mass"][SCALAR].make_constant(m_e)
electrons["charge"][SCALAR].make_constant(-e)
electrons["momentum"]["x"].unit_SI = m_e * c
```

这正好对上 `setupExternalFile()` / `AddPlasmaFromFile()` 的核心合同：

1. 读质量、电荷、位置、动量和权重。
2. 识别 `momentum.unit_SI = m_e*c`，把 SI 动量换成 WarpX 的 `u = p/m`。
3. 读取 `positionOffset` 并叠加坐标偏移。

当前本地 checkout 里，这组 test 还存在一个值得记录的实现边界：

- `CMakeLists.txt` 把 `test_3d_focusing_gaussian_beam_from_openpmd` 的 analysis 写成了 `analysis.py`
- 但 `../warpx/Examples/Tests/gaussian_beam/` 目录下当前并没有这个文件

因此对这条 regression 的最稳妥表述应再拆成两层：

1. workflow / checksum 层已经成立：
   - `prepare.py -> external_file inputs -> analysis_default_regression.py`
   - 这一链已经足以证明 native openPMD variant 的输入文件生成、`external_file` 读入和历史输出基线是 active coverage。
2. 强 analysis 层当前仍不成立：
   - `CMakeLists.txt` 名义上要求 `analysis.py`
   - 但当前本地源码树里这个脚本并不存在
   - 因此不能把 native 版本夸大成已经有与 PICMI 版同等级的束斑统计物理断言。

与之相对，`test_3d_focusing_gaussian_beam_from_openpmd_picmi` 明确复用了 `analysis_focusing_beam.py`，因此 PICMI 版本的 openPMD 注入至少在束斑统计层有显式物理断言。

## 6. electrostatic / EB 初始化由两组例子分工兜底

### 6.1 `effective_potential_electrostatic`

这条 test 的输入是一个 PICMI 脚本，不是传统 inputs 文件。它组合了：

- `Simulation(warpx_serialize_initial_conditions=True)`
- `EmbeddedBoundary(implicit_function=..., potential=0.0)`
- `ElectrostaticSolver(..., warpx_effective_potential=True)`
- 高斯电子云和高斯离子云

它验证的不是“一次 Poisson 解是否看起来正常”，而是更具体的 effective-potential electrostatic 初态和后续演化。

`analysis.py` 的断言对象是电子径向密度：

```python
rho_e, info = ts.get_field(field="rho_electrons", iteration=it)
r_grid, n_e = get_radial_function(-rho_e / constants.q_e, info)
n_e_analytic = get_analytic_density(r_grid, ts.t[ii])
assert np.all(rms_errors < 0.07)
```

因此它对初始化层的覆盖是：

1. PICMI 高斯团分布怎样进入粒子容器。
2. effective-potential electrostatic solver 如何初始化 `phi`、`rho` 与额外的 `effective_potential_sigma`。
3. 带 EB 金属球约束的 electrostatic 初始条件能否进入正确的 adiabatic expansion 基准。

### 6.2 `electrostatic_sphere_eb`

这组则更接近“Poisson 初始化 contract 的纯测”。

`inputs_test_3d_electrostatic_sphere_eb` 关键输入是：

```text
warpx.do_electrostatic = labframe
warpx.eb_implicit_function = "-(x**2+y**2+z**2-0.1**2)"
warpx.eb_potential(x,y,z,t) = "1."
diag1.fields_to_plot = Ex Ey Ez rho phi eb_covered
```

analysis 脚本做了两类断言：

1. reduced diagnostics `ChargeOnEB` 和理论电容球电荷比较：

```python
q_th = 4 * np.pi * epsilon_0 * phi_0 * R
q_sim = data[1, 2]
assert abs((q_sim - q_th) / q_th) < 0.06
```

2. `eb_covered` 场的几何正确性：

```python
assert np.all(eb_covered[r < R - info.dx] == 1)
assert np.all(eb_covered[r > R + info.dx] == 0)
```

RZ 版本 `analysis_rz.py` 则直接把 `phi(r)` 和 `Er(r)` 与解析圆柱解比较。

因此这组例子对初始化主链的意义是：

1. 验证 `InitEB()` 和 electrostatic Poisson 边界条件联动。
2. 验证 `boundary.potential_*` 与 `eb_potential(...)` 共同定义的初始势问题。
3. 验证初始化后 `phi / E / eb_covered / reduced diagnostics` 的第一帧就已经自洽。

## 7. `projection_div_cleaner` 是初始化里最独立的一条验证支线

这组 tests 专门对应前面第 5 篇笔记讲的 `ProjectionDivCleaner`，它们和 `dive_cleaning` 不是一回事。

### 7.1 RZ 文件外场版本

`inputs_test_rz_projection_div_cleaner` 直接给出：

```text
warpx.B_ext_grid_init_style = "read_from_file"
warpx.read_fields_from_path = "../../../../openPMD-example-datasets/example-femm-thetaMode.h5"
warpx.do_initial_div_cleaning = true
warpx.projection_div_cleaner.rtol = 5e-12
```

这条输入会走：

- `LoadExternalFields()`
- `ReadExternalFieldFromFile()`
- `ProjectionCleanDivB()`

`analysis.py` 则在 `raw` staggered `Bx_aux/Bz_aux` 上直接离散重建 `divB`，并检查其二范数足够小：

```python
divB = dBrdr + dBzdz
error = np.sqrt((divB[1:-1, 1:-1] ** 2).sum())
assert error < tolerance
```

这正是 projection cleaner 本体的硬断言，而不是泛化 checksum。

### 7.2 3D PICMI 文件外场版本

`inputs_test_3d_projection_div_cleaner_picmi.py` 用 `picmi.LoadInitialField` 从 openPMD 文件加载 `B` 场，再在脚本末尾直接对 `Bx_aux/By_aux/Bz_aux` 重建 `divB`：

```python
divB = dBxdx + dBydy + dBzdz
error = np.sqrt((divB[2:-2, 2:-2, 2:-2] ** 2).sum())
assert error < tolerance
```

这说明 PICMI 外场加载路径和原生输入路径都在验证同一件事：初始化完成后 `B_aux` 上的离散散度应被 projection 逼近到数值零。

### 7.3 Python callback 版本

`inputs_test_3d_projection_div_cleaner_callback_picmi.py` 更重要，因为它把前面笔记里的 callback 窗口也接上了。

它通过：

```python
init_field = picmi.LoadInitialFieldFromPython(
    load_from_python=load_current_ring,
    warpx_do_divb_cleaning_external=True,
    load_E=False,
)
```

把外部 `B` 场从 Python callback 直接灌进 `Bfield_fp_external`，然后在脚本末尾从 `Bfield_aux` 再次重建 `divB` 并断言为零。

这条 regression 的真实意义是：

1. 验证初始化 callback 能把外部场写进 field registry。
2. 验证 projection cleaner 会消费 callback 生成的外场，而不只消费文件外场。
3. 验证清理后的结果确实进入 `aux` 主 gather 路径。

### 7.4 2D 解析外场版本

`inputs_test_2d_projection_div_cleaner_initial_analytical_field_picmi.py` 则用：

```python
B_ext = picmi.AnalyticInitialField(
    Bx_expression=Bx,
    By_expression=By,
    Bz_expression=Bz,
    warpx_do_initial_div_cleaning=True,
    warpx_projection_div_cleaner_rtol=5e-12,
)
```

说明 projection cleaner 还覆盖了 parser/analytic 外场分支，而不只覆盖文件和 callback。

### 7.5 `flux_injection`：`setupNFluxPerCell()` 的运行态验证入口

前面几组主要在覆盖“初始化后就静止或只做一步输出”的合同，但 `Examples/Tests/flux_injection/` 更直接对应：

- `PlasmaInjector::setupNFluxPerCell()`
- `PhysicalParticleContainer::AddPlasmaFlux()`
- `gaussianflux` rejection sampling

这组 regression 应拆成三类：

1. `analysis_flux_injection_3d.py`
   - 对 3D `NFluxPerCell` 场景同时检查：
   - 总发射权重是否等于 `flux * surface * t_max`
   - 法向是否符合 Gaussian-flux 分布
   - 切向是否符合普通 Gaussian 分布
2. `analysis_flux_injection_rz.py`
   - 对 `flux_normal_axis = t` 的 RZ 连续注入做更窄但更硬的检查：
   - 粒子始终停留在预期 Larmor 半径带
   - 总通量仍与理论一致
3. `analysis_flux_injection_from_eb.py`
   - 验证 `inject_from_embedded_boundary = 1` 时：
   - 发射总数正确
   - 法向/切向速度统计正确
   - 发射后粒子不落在 EB 内部

因此 `flux_injection` 的地位不是普通“边界或 emitter 示例”，而是 `NFluxPerCell` 这条 species 入口在运行态上的最直接强 regression。

## 8. 这一组验证地图给第 3A 章提供了什么

把这些 regression 放回初始化主链里，可以得到一张更实用的覆盖图：

1. `PlasmaInjector` 的常规 parser 初始化：
   - 由 `Langmuir` 系列和一大批 checksum regression 兜底。
2. `gaussian_beam`：
   - 由 `focusing_gaussian_beam`、`rotated_gaussian_beam` 做显式统计断言。
3. `external_file` openPMD 粒子导入：
   - 由 `focusing_gaussian_beam_from_openpmd*` 覆盖输入路径；
   - PICMI 版本有显式束斑 analysis；
   - 原生 inputs 版本已经有 `prepare -> inject -> checksum` 的 workflow coverage；
   - 但当前本地 checkout 里仍缺名义上的 `analysis.py`，所以它的强 analysis 级别仍未闭环。
4. `initialize_self_fields`：
   - 由 `space_charge_initialization` 直接锚定。
5. electrostatic / effective potential / EB：
   - 由 `effective_potential_electrostatic` 和 `electrostatic_sphere_eb*` 分工覆盖。
6. `ProjectionCleanDivB()`：
   - 由 `projection_div_cleaner` 的 file / callback / analytic 三条分支直接覆盖。
7. `NFluxPerCell` / flux injection：
   - 由 `flux_injection` 的 3D / RZ / embedded-boundary 三条分支直接覆盖。
8. `warpx.do_dive_cleaning`：
   - 由 `dive_cleaning` 和 Langmuir 某些变体继续覆盖。
9. 粒子分布与 parser 密度 profile：
   - 由 `initial_distribution` 和 `initial_plasma_profile` 继续覆盖。

## 9. 当前本地 checkout 里仍应明确记录的缺口

这篇验证地图不能写得比现状更乐观。当前本地源码树里至少有三个应保留的边界：

1. `gaussian_beam/CMakeLists.txt` 里的 `test_3d_focusing_gaussian_beam_from_openpmd` 指向 `analysis.py`，但目录下当前没有这个文件。
2. `Langmuir` 家族虽然已经在 `docs/example-regression-map.md` 里细分了主流 1D/2D/3D/RZ、MR、PSATD 和 fluid 变体，但仍有少量遗留 benchmark 名和单精度尾项只剩 checksum 树记录，没有对应活跃 example 输入。
3. 并不是每条初始化路径都有显式解析理论；很多路径仍主要依赖 checksum 回归，而不是物理量 hard assert。

所以这篇地图的用途不是宣称“初始化层已被完整严格证明”，而是给出：

- 哪些路径已经有物理断言，
- 哪些路径目前只是 checksum，
- 哪些地方需要后续继续补分类或核对脚本缺口。

## 10. `initial_distribution`：内建与 parser 初始化分布的综合强基准

`Examples/Tests/initial_distribution/` 当前本地 checkout 里是初始化层最集中的 distribution 合同回归之一。它同一套输入同时覆盖：

- `gaussian`
- `maxwell_boltzmann`
- `maxwell_juttner`
- `gaussian_beam`
- parser 温度
- parser bulk velocity
- `uniform`
- parser-Gaussian 动量统计

analysis 脚本会把 reduced histogram、束斑统计和解析分布逐条对照。因此它更准确地是在验证：

1. `PlasmaInjector` / `SpeciesUtils` 的内建动量分布分派；
2. parser 定义的温度、漂移速度和均值/方差是否真的进入初始化；
3. `gaussian_beam` 在 distribution-level 上的统计合同。

## 11. `initial_plasma_profile`：`parse_density_function` 抛物型通道的 checksum 基线

`Examples/Tests/initial_plasma_profile/` 当前只有：

- `inputs_test_2d_parabolic_channel_initialization`
- `analysis_default_regression.py`

没有独立 `analysis.py`。但输入本身很明确：它在二维电子 species 上使用

- `injection_style = NUniformPerCell`
- `profile = parse_density_function`

把横向 parabolic channel 与纵向 ramp / plateau / ramp 组合成初始等离子体密度。因此这组条目应被记录为：

1. `parse_density_function` 初始化合同的直接 example-level 入口；
2. 当前主要依赖 checksum 的 parabolic-channel 基线；
3. 尚无独立强 analysis 的一条已知证据边界。

## 12. `repelling_particles`：双宏粒子自场建立与后续动力学的最小联立基准

`Examples/Tests/repelling_particles/` 也不该继续留在未分类状态。它虽然只有两个 `SingleParticle` species，但输入同时打开了：

- `electron1.initialize_self_fields = 1`
- `electron2.initialize_self_fields = 1`

因此它不是普通单粒子轨道 test，而是在验证：

1. 初始 electrostatic self-field 是否真的为两颗同号宏粒子建立起来；
2. 建立后的场和后续 Vay pusher 联立起来，是否能给出正确的非相对论减速动力学。

analysis 脚本直接从连续 plotfiles 中读取两粒子的 `x` 位置和 `beta_x`，并用两体排斥下的能量守恒关系

$$
\beta(t)^2 = \beta(0)^2 + 2wr_e \log\frac{d(0)}{d(t)}
$$

构造解析速度，再要求两粒子的数值速度都与理论值在 `0.01` 绝对容差内一致。

所以这组 regression 最准确的定位是：

- `initialize_self_fields` 建场
- electrostatic particle-particle interaction
- 显式 pusher 后续消费初始自场

三者联立后的最小强基准。
