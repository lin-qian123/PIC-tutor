# implicit regression 断言地图：`petsc_matrix`、`planar_pinch` 与守恒测试到底在验证什么

绑定源码与测试：

- `../warpx/Examples/Tests/implicit/CMakeLists.txt`
- `../warpx/Examples/Tests/implicit/analysis_petsc_matrix.py`
- `../warpx/Examples/Tests/implicit/analysis_planar_pinch.py`
- `../warpx/Examples/Tests/implicit/analysis_implicit.py`
- `../warpx/Examples/Tests/implicit/analysis_1d.py`
- `../warpx/Examples/Tests/implicit/analysis_2d_psatd.py`
- `../warpx/Examples/Tests/implicit/analysis_vandb_jfnk_2d.py`
- `../warpx/Examples/Tests/implicit/inputs_test_2d_curl_curl_petsc_pc`
- `../warpx/Examples/Tests/implicit/inputs_test_rcylinder_curl_curl_petsc_pc`
- `../warpx/Examples/Tests/implicit/inputs_test_rz_curl_curl_petsc_pc`
- `../warpx/Examples/Tests/implicit/inputs_test_1d_theta_implicit_planar_pinch`
- `../warpx/Examples/Tests/implicit/inputs_test_2d_theta_implicit_planar_pinch`

前面几篇已经把 implicit solver 的

- residual / Jacobian
- `pc_petsc`
- `WarpXSolverDOF`
- `MatrixPC`
- `curl2_BC_mask`
- `MassMatrices_PC`

这些实现链讲清了。但如果不回到 regression，看不出这些实现链哪些部分被硬验证、哪些还只是“源码上看起来合理”。这一篇的任务就是把 `Examples/Tests/implicit/` 里的断言地图画清楚。

## 1. `CMakeLists.txt` 先把测试分成三类：矩阵装配、planar pinch、守恒基准

`Examples/Tests/implicit/CMakeLists.txt` 里当前可以分出三组：

1. `test_2d_curl_curl_petsc_pc`
   `test_rcylinder_curl_curl_petsc_pc`
   `test_rz_curl_curl_petsc_pc`
   都走 `analysis_petsc_matrix.py`
2. `test_1d_theta_implicit_planar_pinch`
   `test_2d_theta_implicit_planar_pinch`
   都走 `analysis_planar_pinch.py`
3. 其余 uniform plasma / JFNK / symmetry / PSATD 测试分别走
   - `analysis_implicit.py`
   - `analysis_1d.py`
   - `analysis_2d_psatd.py`
   - `analysis_vandb_jfnk_2d.py`

这说明 WarpX 对 implicit regression 不是只看 checksum，而是额外插了“求解器行为级”分析脚本。

## 2. `analysis_petsc_matrix.py` 验证的不是物理解，而是 `pc_petsc` 装配是否足够精确到让 LU 一步收敛

`analysis_petsc_matrix.py` 的核心断言只有两条：

```python
assert total_gmres_iters == num_steps
assert total_newton_iters == num_steps
```

对应注释非常直接：

> Since LU is an exact solver, if the preconditioner matrix is constructed correctly, then there should be 1 Newton and 1 GMRES iteration per time step.

所以这组测试真正验证的是：

- `pc_petsc` 下的 `P` 是否等于当前线性问题足够精确的离散算子；
- `MatrixPC::Assemble()`、`WarpXSolverDOF`、`assemblePCMatrix()`、PETSc `Mat` 提交链是否没有把条目写错。

它**不是**在验证长期物理守恒，也**不是**在验证非线性算法鲁棒性；它验证的是：

$$
\text{若 PC = exact LU target，则每步只需 1 Newton + 1 GMRES。}
$$

## 3. 这组三个 `petsc_matrix` 输入专门覆盖了几何分支，而不是物理场景分支

三组输入分别是：

- 2D Cartesian：`inputs_test_2d_curl_curl_petsc_pc`
- RZ：`inputs_test_rz_curl_curl_petsc_pc`
- RCYLINDER：`inputs_test_rcylinder_curl_curl_petsc_pc`

它们共同的求解器配置都是：

```text
implicit_evolve.nonlinear_solver = "newton"
newton.linear_solver = petsc_ksp
jacobian.pc_type = pc_petsc
pc_petsc.type = lu
```

也就是说，这组三测的设计目的不是覆盖不同 implicit 物理模型，而是专门把：

- 2D
- RZ
- RCYLINDER

三套 `MatrixPC::Assemble()` 几何分支都放到 LU 精确求解器下面做同一条硬断言。

因此只要这组三测中任何一个失败，更优先怀疑的就是：

- `curl2_BC_mask`
- `MatrixPC` 几何 stencil
- `WarpXSolverDOF` 编号
- `assemblePCMatrix()` 提交

而不是“某个物理模型近似失效”。

## 4. `analysis_petsc_matrix.py` 实际只依赖 `newton_solver.txt`

这也很重要。脚本没有读 plotfile，没有读 field/particle energy，而是只读：

```python
newton_solver = np.loadtxt("diags/reduced_files/newton_solver.txt", skiprows=1)
```

然后检查累计：

- `num_steps`
- `total_newton_iters`
- `total_gmres_iters`

因此它给出的证据是“求解器轨迹级”的，不是“场数据级”的。如果这里断言失败，但 checksum 仍接近，说明问题可能出在：

- 线性系统更难解了；
- preconditioner 不再是 exact-equivalent；
- 但物理解未必已经明显崩坏。

## 5. `analysis_planar_pinch.py` 验证的是更综合的三层：能量、线性/非线性效率、Gauss 定律

`analysis_planar_pinch.py` 的断言明显比 `petsc_matrix` 更厚：

1. 能量账本：

```python
assert max_rel_net_energy < rel_net_energy_tol
```

2. GMRES 每次 Newton 的平均代价：

```python
assert total_gmres_iters / total_newton_iters < gmres_iters_tol
```

3. Newton 每步平均代价：

```python
assert total_newton_iters / num_steps < newton_iters_tol
```

4. Gauss 定律 RMS 误差：

```python
assert drho_rms < tolerance_rel_charge
```

所以 planar pinch 不是单一“solver smoke test”，而是一个同时检查：

- 物理能量账本
- 线性/非线性求解器效率
- 电荷守恒 / Gauss 定律

的综合基准。

## 6. planar pinch 的能量检查显式把边界 Poynting flux 纳入账本

脚本不是只看 `field_energy + particle_energy`，而是：

```python
dE = Efields + Eplasma + dE_poynting
rel_net_energy = np.abs(dE - dE[0]) / Eplasma
```

其中 `dE_poynting` 来自 reduced diagnostic `poynting_flux.txt`。

这说明这个测试并不是闭域总能量守恒，而是在检查：

$$
\Delta(E_{\text{field}} + E_{\text{plasma}}) + E_{\text{Poynting out}}
$$

是否守恒。

因此它验证的不只是 particle pusher / current deposition，也同时验证：

- reduced diagnostic 的边界能流统计
- 边界条件下场更新的能量一致性

## 7. planar pinch 对 preconditioner 的要求不是“精确一步收敛”，而是“效率不劣化到阈值外”

2D 输入 `inputs_test_2d_theta_implicit_planar_pinch` 配的是：

```text
implicit_evolve.use_mass_matrices_jacobian = true
implicit_evolve.use_mass_matrices_pc = true
implicit_evolve.mass_matrices_pc_width = 1
jacobian.pc_type = pc_petsc
pc_petsc.type = asm
pc_petsc.asm_overlap = 4
pc_petsc.sub_type = lu
```

这和 `analysis_petsc_matrix.py` 的 `pc_petsc.type = lu` 很不一样。这里不是 exact full LU，而是：

- 外层 PETSc `asm`
- 子块 `lu`
- 还带重叠

所以它对应的断言自然变成“平均迭代数低于阈值”，而不是“每步恰好 1 次 GMRES / Newton”。

换句话说，planar pinch 测的是：

$$
\text{preconditioner 是否仍然足够好用}
$$

而不是：

$$
\text{preconditioner 是否与 exact solve 等价}
$$

## 8. 1D 与 2D planar pinch 还同时比较两套 preconditioner 路线

1D 输入 `inputs_test_1d_theta_implicit_planar_pinch` 用的是：

```text
jacobian.pc_type = "pc_curl_curl_mlmg"
pc_curl_curl_mlmg.max_iter = 1
```

2D 输入则用的是：

```text
jacobian.pc_type = pc_petsc
pc_petsc.type = asm
pc_petsc.sub_type = lu
```

但两者共享同一个 `analysis_planar_pinch.py`。

这说明这个 analysis 脚本本质上不关心 preconditioner 是哪一族，它关心的是：

- 在当前问题和当前维度下，整体 nonlinear solve 是否维持可接受效率；
- 物理守恒与 Gauss 定律是否仍成立。

所以它是“跨 preconditioner 家族”的综合验收脚本。

## 9. `analysis_implicit.py`、`analysis_1d.py`、`analysis_2d_psatd.py` 是“机器精度守恒”类基准

`analysis_implicit.py` 与 `analysis_vandb_jfnk_2d.py` 的主断言是：

```python
assert max_delta_E < tolerance_rel_energy
assert drho_rms < tolerance_rel_charge
```

`analysis_1d.py`、`analysis_2d_psatd.py` 则重点看总能量机器精度守恒。

这些测试和 `petsc_matrix` / `planar_pinch` 的区别是：

- 它们更直接对应“exactly energy-conserving implicit method” 的物理离散性质；
- 它们不专门针对 `pc_petsc` 的矩阵装配；
- 它们主要验证 `ComputeRHS()`、particle update、charge/current deposition、Gauss 定律保持这些更高层的离散结构。

因此它们给 `pc_petsc` 的证据是间接的，而不是专门的。

## 10. 可以把这几类 implicit regression 对源码链的覆盖范围画成表

### A. `analysis_petsc_matrix.py`

直接强覆盖：

- `WarpXSolverDOF`
- `MatrixPC::Assemble()`
- `curl2_BC_mask`
- `MassMatrices_PC`
- `assemblePCMatrix()`
- PETSc `KSPSetOperators(A,P)` 路线

弱覆盖：

- 物理守恒
- charge conservation

### B. `analysis_planar_pinch.py`

直接强覆盖：

- implicit field/particle 耦合
- `PreLinearSolve()` / mass matrices
- preconditioner 质量
- energy + Poynting flux 账本
- Gauss 定律

间接覆盖：

- `pc_petsc` 装配正确性
- `pc_curl_curl_mlmg` 近似质量

### C. `analysis_implicit.py` / `analysis_1d.py` / `analysis_2d_psatd.py` / `analysis_vandb_jfnk_2d.py`

直接强覆盖：

- 能量守恒
- Gauss 定律
- JFNK 粒子-场固定点主链

间接覆盖：

- solver 具体矩阵装配实现

## 11. 这也解释了为什么 `TODO` 里“验证”不能被源码阅读替代

前面几轮源码精读已经能说明：

- `pc_petsc` 这条链在实现上怎样工作；
- `MatrixPC` 怎样写条目；
- `assemblePCMatrix()` 怎样提交。

但只有 regression analysis 才告诉我们：

- 哪些地方已经被测试硬断言覆盖；
- 哪些地方仍然只是“代码上看起来合理”。

对当前 `pc_petsc` 支线来说，最有力的硬证据不是 checksum，而是：

1. `analysis_petsc_matrix.py` 的 `1 Newton + 1 GMRES / step`
2. `analysis_planar_pinch.py` 的能量、迭代数和 Gauss law 三重断言

## 12. 现在可以把 implicit family 的 regression 正式拆成五条合同

结合 `CMakeLists.txt` 和 analysis 脚本，当前 `Examples/Tests/implicit/` 不应再被写成一个笼统的 “implicit solver” 桶，而应至少拆成：

1. `analysis_1d.py`
   - 1D Picard energy-conservation
   - 其中 `semi_implicit_picard` 允许有限容差，`theta_implicit_picard` 要求机器精度
2. `analysis_implicit.py`
   - exactly energy-conserving implicit EM
   - 周期/对称边界下同时检查能量和 Gauss law RMS
3. `analysis_2d_psatd.py`
   - `strang_implicit_spectral_em + psatd`
   - 重点是 spectral Strang-split 没有破坏能量守恒
4. `analysis_planar_pinch.py`
   - planar pinch
   - 同时检查能量账本、边界 Poynting flux、Newton/GMRES 效率与 Gauss law
5. `analysis_vandb_jfnk_2d.py` / `analysis_vandb_jfnk_2d_cropping.py`
   - JFNK + Villasenor 周期热等离子体守恒
   - 以及 PEC cropping / suborbit fallback 下的局部 Gauss-law 约束

这样一来，`filtered` 与 `PICMI` 变体也就有了更准确的位置：

- `filtered` 不是新 physics benchmark，而是给同一 JFNK/Villasenor 守恒合同加了一条 “filter 不能破坏守恒” 的强约束；
- `PICMI` 也不是独立物理 benchmark，而是前端映射后仍必须满足原生输入同一 analysis 合同。

## 13. 下一步最自然的继续方向

- 把这一层拆分同步回 `example-regression-map.md`、第 6 章正文和项目 README/TODO。
- 再继续清理边界侧的 `Silver-Mueller` family，把 boundary 章节和 regression-map 的颗粒度拉到和 implicit family 同一水平。
