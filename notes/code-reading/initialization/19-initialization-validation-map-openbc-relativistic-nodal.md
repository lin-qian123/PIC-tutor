# `nodal_electrostatic`、`open_bc_poisson_solver` 与 `relativistic_space_charge_initialization` 的验证边界

绑定对象：

- `../warpx/Examples/Tests/nodal_electrostatic`
- `../warpx/Examples/Tests/open_bc_poisson_solver`
- `../warpx/Examples/Tests/relativistic_space_charge_initialization`

这三组条目此前在索引里仍被统一挂在：

- `initialization / electrostatic / Poisson`

但实际看完 inputs 和 analysis 以后，它们分别验证的是三条不同的初始化合同：

- collocated relativistic electrostatic 的零触发基准
- open boundary + FFT Poisson 的 relativistic 初始自场
- relativistic Gaussian beam 的初始 self-field

---

## 1. `nodal_electrostatic`：不是场解对照，而是 QED 零触发基准

这组当前只有一个 test：

- `test_3d_nodal_electrostatic_solver`

输入的关键组合是：

- `warpx.do_electrostatic = relativistic`
- `warpx.grid_type = collocated`
- `beam_p.initialize_self_fields = 1`
- `beam_p.do_qed_quantum_sync = 1`

也就是说，这组并不想验证 photon 产额本身，而是在验证：

- collocated relativistic electrostatic 初始化出来的自场
- 不应强到足以假触发 QED

analysis 的两个断言也完全匹配这个目的：

1. `ParticleExtrema_beam_p.txt` 中的 `chi_max` 必须始终极小；
2. `ParticleNumber.txt` 中 photon 数必须始终为 `0`。

因此这组更准确的分类应当是：

- `initialization / collocated relativistic electrostatic / zero-trigger baseline`

而不只是泛写成 `Poisson`。

---

## 2. `open_bc_poisson_solver`：open boundary relativistic FFT Poisson 初始化

这组 test 有两个变体：

- `test_3d_open_bc_poisson_solver`
- `test_3d_open_bc_poisson_solver_sliced`

### 2.1 物理-算法组合

基线输入把几件事绑在一起：

- `boundary.field_lo = open open open`
- `boundary.field_hi = open open open`
- `warpx.do_electrostatic = relativistic`
- `warpx.poisson_solver = fft`
- `electron.initialize_self_fields = 1`

粒子分布不是 `gaussian_beam`，而是 parser 形式的 3D Gaussian bunch。

因此它测的是：

- open boundary 条件下
- relativistic bunch 初始 self-field
- FFT Poisson solver

这一整条初始化合同。

### 2.2 analysis 的真实断言

`analysis.py` 不看时间推进，而是直接在第 0/1 步输出上取：

- `Ex`
- `Ey`

然后逐个 `z` 截面与 Basseti-Erskine 公式比较。

因此它属于非常明确的强分析：

- 不是 checksum-only
- 也不是泛化的 electrostatic regression

### 2.3 sliced 变体

第二个输入只是在基线上新增：

- `warpx.use_2d_slices_fft_solver = 1`

因此它更准确的角色是：

- `open-boundary relativistic FFT Poisson / sliced-FFT variant`

而不是另一个独立物理 benchmark。

---

## 3. `relativistic_space_charge_initialization`：relativistic Gaussian beam 自场

这组当前只有：

- `test_3d_relativistic_space_charge_initialization`

输入的关键组合是：

- `beam.injection_style = gaussian_beam`
- `beam.initialize_self_fields = 1`
- `beam.uz = 100.0`

因此它和普通 `space_charge_initialization` 的主要区别不是几何，而是：

- self-field 要走 relativistic solver 分支

analysis 的断言也对应这点：

- `Ex` 与理论 relativistic Gaussian beam 自场比较
- `By` 与 `Ex / c` 对应关系比较

所以它更准确的分类应是：

- `initialization / relativistic self-field / Gaussian beam`

而不是继续和一般 `Poisson` 条目混写。

---

## 4. 这三组放回 Initialization 验证图后的最小拆分

把这三组加上前两轮已经压实的静电条目之后，Initialization 里的 electrostatic 验证图至少可以拆成：

1. self-field expansion
   - `electrostatic_sphere`
2. lab-frame / relativistic bunch self-field
   - `space_charge_initialization`
   - `relativistic_space_charge_initialization`
3. collocated zero-trigger baseline
   - `nodal_electrostatic`
4. open-boundary FFT Poisson
   - `open_bc_poisson_solver`
5. time-dependent Dirichlet BC
   - `electrostatic_dirichlet_bc`
6. effective-potential electrostatic
   - `effective_potential_electrostatic`
7. EB / conductor / potential
   - `electrostatic_sphere_eb`
   - `magnetostatic_eb`

这样 `initialization / electrostatic / Poisson` 这个过粗的占位桶就可以继续缩小。

---

## 5. 当前阶段性判断

到这一步，Initialization validation 中静电相关的主要粗分类条目已经明显减少。

下一步更自然的是二选一：

1. 继续把剩余仍挂在 `electrostatic / Poisson` 下的 initialization 条目压实；
2. 或切回计划中的 `ParmParse -> chapter` 参数索引主线。
