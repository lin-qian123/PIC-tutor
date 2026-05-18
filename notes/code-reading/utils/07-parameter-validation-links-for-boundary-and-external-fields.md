# Boundary / External-Field 参数到 Validation 的闭环

绑定源码与例子：

- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/ExternalVectorPotential.*`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/PoissonBoundaryHandler.*`
- `../warpx/Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.*`
- `../warpx/Examples/Tests/electrostatic_dirichlet_bc/*`
- `../warpx/Examples/Tests/open_bc_poisson_solver/*`
- `../warpx/Examples/Tests/effective_potential_electrostatic/*`
- `../warpx/Examples/Physics_applications/ion_beam_extraction/*`

前一篇 [06-external-vector-potential-and-poisson-boundary-parameters.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/06-external-vector-potential-and-poisson-boundary-parameters.md) 只把：

- `external_vector_potential.*`
- `boundary.potential_*`
- `warpx.eb_potential(x,y,z,t)`

拆到了 `parent gate / subobject parse / parser build / runtime apply`。

这篇继续补最后一层：这些参数在本地 WarpX examples / analysis 里到底如何被验证。

---

## 1. 总图

这组参数目前能闭合到四条代表性 validation 链：

1. `boundary.potential_*`
   -> `electrostatic_dirichlet_bc`
2. open boundary + Poisson 边界处理
   -> `open_bc_poisson_solver`
3. effective-potential 电静求解
   -> `effective_potential_electrostatic`
4. `warpx.eb_potential(x,y,z,t)`
   -> `ion_beam_extraction`

其中：

- 前三条是强 analysis regression；
- 第四条更像 physics-application benchmark，但它直接锚定了 `eb_potential(...)` 的真实消费语义。

`external_vector_potential.*` 这一组本轮没有在 `Examples/` 中找到同等级、单独直指该参数族的 analysis regression。
它目前更适合先通过：

- [05-deep-solver-object-parameter-families.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/05-deep-solver-object-parameter-families.md)
- [06-external-vector-potential-and-poisson-boundary-parameters.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/utils/06-external-vector-potential-and-poisson-boundary-parameters.md)
- [12-hybrid-pic-model-deep-dive.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/fieldsolver/12-hybrid-pic-model-deep-dive.md)

这三篇去闭合源码与输入合同。

---

## 2. `boundary.potential_*` -> `electrostatic_dirichlet_bc`

### 2.1 输入合同

[inputs_test_2d_dirichlet_bc](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/electrostatic_dirichlet_bc/inputs_test_2d_dirichlet_bc) 直接给出：

```text
warpx.do_electrostatic = labframe
boundary.field_lo = pec periodic
boundary.field_hi = pec periodic
boundary.potential_lo_x = 150.0*sin(2*pi*6.78e+06*t)
boundary.potential_hi_x = 450.0*sin(2*pi*13.56e+06*t)
```

这条链验证的不是一般 electrostatic 正确性，而是：

- `PoissonBoundaryHandler::ReadParameters()` 是否读到 `boundary.potential_*`
- `BuildParsers()` 是否把只依赖 `t` 的边界势字符串编译成 parser
- `setPhiBC()` 是否把该时间依赖势值正确写进 `phi` 边界

### 2.2 analysis 真正断言什么

[analysis.py](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/electrostatic_dirichlet_bc/analysis.py) 对每个输出时刻：

- 读取 `phi`
- 取两侧边界平均值
- 与两条目标正弦势函数逐时比较

核心断言是：

```python
assert np.allclose(potentials_lo, expected_potentials_lo, rtol=0.1)
assert np.allclose(potentials_hi, expected_potentials_hi, rtol=0.1)
```

所以这条 regression 的真实名字应理解为：

- time-dependent Dirichlet boundary potential fidelity

而不只是“又一个 electrostatic 测试”。

---

## 3. open boundary / Poisson 边界 -> `open_bc_poisson_solver`

### 3.1 输入合同

[inputs_test_3d_open_bc_poisson_solver](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/open_bc_poisson_solver/inputs_test_3d_open_bc_poisson_solver) 的关键点是：

```text
boundary.field_lo = open open open
boundary.field_hi = open open open
warpx.do_electrostatic = relativistic
warpx.poisson_solver = fft
electron.initialize_self_fields = 1
```

这条链并不直接用 `boundary.potential_*`，
但它验证 `PoissonBoundaryHandler` 和 electrostatic solver 如何在 open boundary 合同下协同工作。

### 3.2 analysis 真正断言什么

[analysis.py](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/open_bc_poisson_solver/analysis.py) 读取 `Ex`、`Ey`，
并与 Basseti-Erskine 解析场逐个 `z` 切片比较：

```python
assert np.allclose(Ex_warpx, Ex_theory, rtol=0.032, atol=0)
assert np.allclose(Ey_warpx, Ey_theory, rtol=0.029, atol=0)
```

因此这条 regression 的真实语义是：

- open-boundary relativistic FFT Poisson self-field accuracy

而不是笼统的“Poisson solver 能跑”。

---

## 4. effective potential -> `effective_potential_electrostatic`

### 4.1 输入合同

这条链对应的是：

- `warpx.do_electrostatic = labframe-effective-potential`
- `warpx.effective_potential_factor`
- `warpx.effective_potential_time_filter`
- `warpx.effective_potential_density_floor`

这几个参数如何进入 [EffectivePotentialES.cpp](/Volumes/PHILIPS/programs/PIC/warpx/Source/FieldSolver/ElectrostaticSolvers/EffectivePotentialES.cpp)
的 `ComputeSigma()` 与 variable-coefficient Poisson 主链。

### 4.2 analysis 真正断言什么

[analysis.py](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/effective_potential_electrostatic/analysis.py)：

- 从 `rho_electrons` 重建径向电子密度
- 用输入参数构造解析绝热膨胀密度
- 对每个输出时刻算 RMS 误差

最终要求：

```python
assert np.all(rms_errors < 0.07)
```

所以它验证的是：

- effective-potential solver 的物理模型合同

不是一般 electrostatic diagnostics 格式。

---

## 5. `warpx.eb_potential(x,y,z,t)` -> `ion_beam_extraction`

### 5.1 输入合同

[inputs_test_3d_ion_beam_extraction](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Physics_applications/ion_beam_extraction/inputs_test_3d_ion_beam_extraction) 里同时出现：

```text
warpx.do_electrostatic = labframe
boundary.potential_lo_z = 0
warpx.eb_potential(x,y,z,t) = "-40e3*(z>16e-3) - 41e3*(z>9e-3)*(z<16e-3)"
```

这里有两个不同层级：

- `boundary.potential_lo_z`
  是域边界势
- `warpx.eb_potential(x,y,z,t)`
  是 embedded boundary 电极势

它们都由 `PoissonBoundaryHandler` 保存和编译，但作用域不同。

### 5.2 官方 README 已明确的实现边界

[README.rst](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Physics_applications/ion_beam_extraction/README.rst) 已明确写出：

- WarpX 只在 electrodes 上评估 `warpx.eb_potential(x,y,z,t)`
- 电极间真空区的势分布仍由 electrostatic solver 解出

这正好对应前一篇参数笔记中
`BuildParsersEB()` 与 Poisson/EB solve 的职责分工。

### 5.3 analysis 真正断言什么

[analysis_ion_beam_extraction.py](/Volumes/PHILIPS/programs/PIC/warpx/Examples/Physics_applications/ion_beam_extraction/analysis_ion_beam_extraction.py) 会：

- 读 `phi`
- 读 `eb_covered`
- 读 `Dplus` 粒子
- 检查抽出离子束尾部能量是否接近 `40 keV`

核心断言是：

```python
assert np.all(rel_error_energy < tolerance)
```

其中：

- `target_energy_keV = 40`
- `tolerance = 0.05`

所以这条应用例子的真实价值是：

- 直接证明 `boundary.potential_* + warpx.eb_potential(...) + electrostatic solve + EB geometry`
  这组参数合同能共同产生正确的电极加速能量尺度。

---

## 6. 这组参数当前没有什么

### 6.1 `external_vector_potential.*` 还没有同等级单独 regression

本轮没有在 `Examples/Tests` 中找到像：

- `electrostatic_dirichlet_bc`
- `open_bc_poisson_solver`
- `effective_potential_electrostatic`

这样直接以 `external_vector_potential.*` 为核心断言对象的 analysis regression。

当前更稳妥的说法应是：

- `ExternalVectorPotential` 的输入合同已经有源码级闭合；
- 它在 `HybridPICModel` 正文里已有 runtime 语义闭合；
- 但尚未在本项目索引里压出单独、同等级的 example-level 强断言入口。

本轮把最接近的运行态覆盖也单独核对了一遍。

本地 `Examples/Tests/ohm_solver_cylinder_compression/` 目录下只有：

- `inputs_test_3d_ohm_solver_cylinder_compression_picmi.py`
- `inputs_test_rz_ohm_solver_cylinder_compression_picmi.py`
- `CMakeLists.txt`

这两个 PICMI 输入都通过：

- `picmi.HybridPICSolver(..., A_external=A_ext, ...)`

把两类外部矢势同时接进 hybrid solver：

- `uniform_file`
  - `read_from_file = True`
  - `path = "Afield.h5"`
  - `A_time_external_function = ...`
- `uniform_analytical`
  - `Ax/Ay/Az_external_function = ...`
  - `A_time_external_function = ...`

也就是说，`external_vector_potential.*` 至少已经有：

- file-backed split vector potential runtime 路径
- analytical split vector potential runtime 路径
- 统一时间门函数 `A_time_external_function(t)`

这三层运行态覆盖。

但 `CMakeLists.txt` 里这两个 test 的 `analysis = OFF`，只保留：

- `analysis_default_regression.py --path diags/diag1000010 --rtol 5e-4`
- `analysis_default_regression.py --path diags/diag1000020 --rtol 1e-6`

所以它们应被记成：

- `external_vector_potential.*` 当前最近的 example-level runtime coverage
- 但仍然只是 PICMI + checksum baseline
- 不是像 `electrostatic_dirichlet_bc`、`open_bc_poisson_solver` 那样直接把参数合同单独拿出来做强 analysis 的 regression

### 6.2 `analysis_default_regression.py` 不是这层的强证据

像 `ion_beam_extraction/analysis_default_regression.py` 这类文件，
仍然只应记成：

- checksum helper

不能与上面几条显式 physics / boundary-condition 断言混写。

---

## 7. 可回写到索引层的最稳定结论

1. `boundary.potential_*` 当前最强 validation 入口是
   `electrostatic_dirichlet_bc`。
2. `PoissonBoundaryHandler` 的 open-boundary 侧当前最强 validation 入口是
   `open_bc_poisson_solver`。
3. effective-potential 专属参数当前最强 validation 入口是
   `effective_potential_electrostatic`。
4. `warpx.eb_potential(x,y,z,t)` 的最直接应用级验证入口是
   `ion_beam_extraction`。
5. `external_vector_potential.*` 当前最接近的 example-level 入口是
   `ohm_solver_cylinder_compression` 两个 PICMI tests；
   但它们只是 hybrid PIC 应用级 runtime coverage + checksum baseline。
6. 因此 `external_vector_potential.*` 现在仍更适合作为
   “源码入口图 + hybrid runtime 语义 + 最近 checksum 覆盖”
   的闭合项，而不是假装已经有独立强 regression。

---

## 8. 下一步

1. 回到 `parameter-map.md`，继续清理剩余少量 `species / laser / writer` 尾项。
2. 或继续把 `external_vector_potential.*` 的 example/search 面再扩一轮，只在找到真正 analysis 入口时再写进 validation map。
