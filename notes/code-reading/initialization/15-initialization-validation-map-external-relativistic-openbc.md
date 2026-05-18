# `Initialization` 验证补充地图：external fields、relativistic self-field、open-boundary Poisson

绑定源码与验证入口：

- `../warpx/Source/Initialization/WarpXInitData.cpp`
- `../warpx/Source/Initialization/ExternalField.cpp`
- `../warpx/Source/Particles/ExternalParticleFields.cpp`
- `../warpx/Source/Particles/Gather/GetExternalFields.cpp`
- `../warpx/Source/FieldSolver/WarpXSolveFieldsES.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/RelativisticExplicitES.cpp`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.cpp`
- `../warpx/Examples/Tests/load_external_field/`
- `../warpx/Examples/Tests/relativistic_space_charge_initialization/`
- `../warpx/Examples/Tests/open_bc_poisson_solver/`

上一篇 `14-initialization-validation-map.md` 已经整理了：

- `Langmuir`
- `space_charge_initialization`
- `dive_cleaning`
- `gaussian_beam`
- `effective_potential_electrostatic`
- `electrostatic_sphere_eb`
- `projection_div_cleaner`

这一篇只补三条还没单独压实的初始化验证入口：

1. `load_external_field`
2. `relativistic_space_charge_initialization`
3. `open_bc_poisson_solver`

它们共同对应初始化主链里三种不同的“第一步前状态构造”：

- 外部场装填
- 相对论初始 self-field
- 开放边界 Poisson 解

## 1. `load_external_field`：外场装填合同本身就是初始化测试

这组 tests 的核心不是普通粒子推进，而是检验 `LoadExternalFields()` / `ReadExternalFieldFromFile()` / 粒子侧 external field gather 这一整套初始化合同。

从 `CMakeLists.txt` 看，这一组被明确拆成四类：

1. 3D grid external field：
   - `test_3d_load_external_field_grid_picmi`
2. 3D particle external field：
   - `test_3d_load_external_field_particle_picmi`
3. RZ grid / particle external field：
   - `test_rz_load_external_field_grid`
   - `test_rz_load_external_field_particles`
4. 时间依赖与 restart：
   - `test_3d_load_external_field_particle_time*`
   - `test_3d_load_external_field_particle_multi_time*`
   - `test_*_restart`

### 1.1 grid external field 与 particle external field 被明确分开验证

两条最基础的输入分别是：

```python
initial_field = picmi.LoadInitialField(
    read_fields_from_path="../../../../openPMD-example-datasets/example-femm-3d.h5",
    load_E=False,
    warpx_do_initial_div_cleaning=False,
)
```

和

```python
applied_field = picmi.LoadAppliedField(
    read_fields_from_path="../../../../openPMD-example-datasets/example-femm-3d.h5",
    load_E=False,
)
```

前者对应 grid external field，后者对应 particle applied field。源码上这正好对应两条不同路径：

1. grid external field：
   - `ExternalField.*`
   - `WarpX::LoadExternalFields()`
   - `Bfield_fp_external/Efield_fp_external`
   - `WarpX::AddExternalFields()`
2. particle external field：
   - `Particles/ExternalParticleFields.cpp`
   - `MultiParticleContainer::m_B_ext_particle_s / m_E_ext_particle_s`
   - `E_external_particle_field/B_external_particle_field`
   - `Particles/Gather/GetExternalFields.cpp`

这组 test 的意义在于：WarpX 并没有把“外场”当成单一对象，而是明确维护两套不同合同；`load_external_field` 正是在验证这两套合同没有混淆。

### 1.2 `analysis_3d.py` / `analysis_rz.py` 验证的是“装填后的轨道效应”

3D 和 RZ 的 analysis 并不直接比较场数组，而是跟踪一个 `do_not_deposit` 的单粒子在磁镜场中的最终位置：

```python
error = np.min(np.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2))
assert error < tolerance
```

和

```python
error = np.min(np.sqrt((r - r0) ** 2 + (z - z0) ** 2))
assert error < tolerance
```

因此这条 regression 的硬断言对象不是“文件读进来了”，而是：

1. 初始化确实把外部场装进了 WarpX 对应寄存器；
2. 后续 gather 路径消费到的是正确的外场；
3. 单粒子轨道与已知磁镜参考轨道一致。

这对书稿很重要，因为它说明 `load_external_field` 同时验证了“初始化写场”和“粒子消费场”的接口契合。

### 1.3 时间依赖 tests 验证的是 dependency parser，而不是静态字段

`inputs_test_3d_load_external_field_particle_time` 的关键不是普通 `read_from_file`，而是：

```text
particles.B_ext_particle_init_style = "read_from_file"
particles.read_fields_B_dependency(t) = "cos(omega * t + phase_B)"
```

`inputs_test_3d_load_external_field_particle_multi_time` 更进一步：

```text
particles.B_ext_particle_fields = b1 b2
particles.b1.read_fields_B_dependency(t) = "cos(omega * t)"
particles.b2.read_fields_B_dependency(t) = "cos(2*omega * t)"
```

对应的 `analysis_time_scaling.py` 不是检查轨道，而是直接比较两个 plotfile 上某个分量的缩放比：

```python
ratio[mask] = BN[mask] / B0[mask]
assert np.isclose(r_med, args.expected_ratio, ...)
```

所以这部分真正验证的是：

1. 外部场时间依赖 parser 在初始化时是否被正确注册；
2. 多个外场 map 是否按各自 dependency 独立缩放；
3. 场值缩放是否进入 diagnostics 输出，而不只是进入粒子 gather。

### 1.4 restart 变体检验的是外场状态恢复保真

`analysis_default_restart.py` 的 contract 很直接：把 restart 后的 plotfile 与原始 run 的对应输出逐字段逐 species 比较：

```python
for field in ds_benchmark.field_list:
    dr = ad_restart[field].squeeze().v
    db = ad_benchmark[field].squeeze().v
    assert error < tolerance
```

因此 `test_*_restart` 在初始化层验证的不是“checkpoint 功能泛化正确”，而更具体地是：

- 通过 `read_from_file` 或 dependency 装填的外部场状态，在 restart 后没有丢失或漂移。

当前活跃最小入口一共 3 条：

1. `test_3d_load_external_field_particle_time_restart`
   - 检查带 `read_fields_B_dependency(t)` 的 particle external field 在恢复后仍保持同一时间缩放状态
2. `test_rz_load_external_field_grid_restart`
   - 检查 RZ `B_ext_grid_init_style = read_from_file` 的 grid external field 在恢复后不漂移
3. `test_rz_load_external_field_particles_restart`
   - 检查 RZ `particles.B_ext_particle_init_style = read_from_file` 的 particle external field 在恢复后不漂移

这三条都不重新引入新的 physics observable；它们的关键合同就是：

- 外场初始化寄存器写入
- checkpoint 持久化
- restart 后逐字段恢复

这条链在外场场景下保持一致。

## 2. `relativistic_space_charge_initialization`：验证 `RelativisticExplicitES`

这组 tests 和前一篇里的 `space_charge_initialization` 形式很像，但 solver 语义不同。输入文件显式写了：

```text
beam.injection_style = "gaussian_beam"
beam.initialize_self_fields = 1
beam.uz = 100.0
beam.self_fields_required_precision = 1.e-4
```

这说明它验证的不是静止高斯电荷团，而是 relativistic bunch 的初始 self-field。源码上这条路径对应：

- `WarpX.cpp` 里 `warpx.do_electrostatic = relativistic` 分派到 `RelativisticExplicitES`
- `RelativisticExplicitES::InitData()`
- `RelativisticExplicitES::ComputeSpaceChargeField()`

analysis 脚本的关键比较是：

```python
Ex_th = factor * factor_z * x_2d
...
plt.title("By: Theory")
plt.imshow(make_2d(Ex_th / scc.c))
...
check(Ex_array, Ex_th, "Ex")
```

也就是说，这组 regression 明确在检验：

1. relativistic Gaussian beam 注入后的横向电场 `Ex`
2. 以及与之配对的磁场 `By ≈ Ex/c`

对初始化书稿的含义是：`initialize_self_fields = 1` 并不只通向 `LabFrameExplicitES`；当 solver 选择是 relativistic 时，初始场构造合同已经改变，analysis 也随之从“纯 Coulomb 场”变成“相对论束流的电磁自场”。

## 3. `open_bc_poisson_solver`：开放边界相对论 Poisson 初始化

这组 tests 直接验证 `boundary.field_lo/hi = open` 加上相对论 Poisson 初始化的组合。

输入文件最关键的部分是：

```text
boundary.field_lo = open open open
boundary.field_hi = open open open
warpx.do_electrostatic = relativistic
warpx.poisson_solver = fft
electron.initialize_self_fields = 1
```

粒子初始化也不是 `gaussian_beam`，而是：

```text
electron.injection_style = "NUniformPerCell"
electron.profile = parse_density_function
electron.density_function(x,y,z) = "..."
electron.uz = 25000
```

所以这条 regression 同时覆盖：

1. `parse_density_function` 形式的初始化密度 functor；
2. `initialize_self_fields`；
3. `RelativisticExplicitES`；
4. `PoissonBoundaryHandler` 对 open boundary 的边界条件设置；
5. `warpx.poisson_solver = fft`；
6. sliced FFT 变体 `warpx.use_2d_slices_fft_solver = 1`。

`analysis.py` 用的是 Basseti-Erskine 公式，逐个 `z` 截面比较 `Ex` 和 `Ey`：

```python
Ex_theory = evaluate_E(grid_x, 0.0, z)[0]
Ey_theory = evaluate_E(0.0, grid_y, z)[1]

assert np.allclose(Ex_warpx, Ex_theory, rtol=0.032, atol=0)
assert np.allclose(Ey_warpx, Ey_theory, rtol=0.029, atol=0)
```

这说明它验证的不是单纯“open boundary 可用”，而是：

- 开放边界下 relativistic bunch 的初始 Poisson 解，在空间剖面上和解析加速器束流公式一致。

换句话说，这组例子正好把第 3A 章里“边界 potential、solver 选择、density parser、`initialize_self_fields`”四条支线并到了一起。

## 4. 把这三组例子加进初始化验证总图后，覆盖图变成什么

到这一步，`Initialization` 章节的本地验证入口可以更细地分层：

1. parser 初始化与常规宏粒子装填：
   - `Langmuir`
2. `gaussian_beam` 注入几何：
   - `focusing_gaussian_beam`
   - `rotated_gaussian_beam`
3. openPMD 粒子文件注入：
   - `focusing_gaussian_beam_from_openpmd*`
4. lab-frame 初始 self-field：
   - `space_charge_initialization`
5. relativistic 初始 self-field：
   - `relativistic_space_charge_initialization`
6. electrostatic / effective potential / EB：
   - `effective_potential_electrostatic`
   - `electrostatic_sphere_eb*`
7. 外部 grid / particle fields：
   - `load_external_field*`
8. projection cleaner：
   - `projection_div_cleaner*`
9. 开放边界 relativistic Poisson 初始化：
   - `open_bc_poisson_solver*`
10. 演化态 `div(E)` cleaning：
   - `dive_cleaning`

## 5. 这轮顺手澄清的两个边界

### 5.1 `load_external_field` 不是纯 diagnostics 测试

它虽然最终通过粒子位置或 plotfile 比较来断言，但核心仍是初始化阶段：

- 场从哪里读入；
- 读进哪个 registry；
- 是否只给粒子看还是要加回主网格；
- dependency parser 是否在开始前就注册好。

### 5.2 `open_bc_poisson_solver` 不是一般 electrostatic 基准

它特意把：

- open boundaries
- relativistic bunch
- FFT Poisson
- sliced FFT solver

绑在一起，验证的是一个比普通 `initialize_self_fields` 更窄但也更强的初始化合同。

## 6. 当前还没补进这条验证支线的内容

尽管这轮把三组主要入口补齐了，初始化验证层仍有后续工作：

1. `docs/example-regression-map.md` 里相关条目虽然会在本轮同步清理一批，但整个 initialization 相关区块还没有完全细分完。
2. `load_density`、`magnetostatic_eb`、`nodal_electrostatic` 等仍和 initialization 有交叉，后续还应判断是否单独并入初始化验证地图。
3. 这条验证图仍然以 examples / regressions 阅读为主，没有实际运行本地 WarpX 二进制。
