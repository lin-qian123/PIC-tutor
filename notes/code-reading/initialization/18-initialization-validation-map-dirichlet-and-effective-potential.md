# `electrostatic_dirichlet_bc` 与 `effective_potential_electrostatic` 的验证边界

绑定对象：

- `../warpx/Examples/Tests/electrostatic_dirichlet_bc`
- `../warpx/Examples/Tests/effective_potential_electrostatic`
- `../warpx/Source/FieldSolver/ElectrostaticSolver/*`
- `../warpx/Source/Initialization/WarpXInitData.cpp`

这两组条目此前都还停留在：

- `electrostatic / Poisson`

但它们的真实验证对象并不一样：

- `electrostatic_dirichlet_bc`
  - 测的是时变 Dirichlet 边界势是否真正进入 electrostatic 求解器
- `effective_potential_electrostatic`
  - 测的是 effective-potential Poisson solver 在带导体球约束下的绝热膨胀近似

---

## 1. `electrostatic_dirichlet_bc`：时变边界势合同，不是一般静电场解

### 1.1 CMake 结构

这组当前只有两个 test：

- `test_2d_dirichlet_bc`
- `test_2d_dirichlet_bc_picmi`

两者都跑同一个 `analysis.py`，再配通用 checksum。

因此这里的物理解读不需要按 native / PICMI 分成两套 analysis；PICMI 只是前端改写。

### 1.2 native 输入到底在测什么

原生输入的核心设置是：

```text
warpx.do_electrostatic = labframe
boundary.field_lo = pec periodic
boundary.field_hi = pec periodic
boundary.potential_lo_x = 150.0*sin(2*pi*6.78e+06*t)
boundary.potential_hi_x = 450.0*sin(2*pi*13.56e+06*t)
diag1.fields_to_plot = phi
```

因此它测的不是内部带电粒子如何演化，而是：

- 空域基本为空
- x 两侧的 electrostatic Dirichlet potential 随时间按给定正弦变化
- 这些边界势是否在每个输出步真正进入求解出来的 `phi`

### 1.3 analysis 的真实断言对象

`analysis.py` 做的事情很直接：

1. 读所有 full diagnostics
2. 取边界两侧的平均 `phi`
3. 与理论时间函数比较

理论式就是：
$$
\phi_{\mathrm{lo}}(t)=150\sin(2\pi\cdot 6.78\times 10^6 t),
$$
$$
\phi_{\mathrm{hi}}(t)=450\sin(2\pi\cdot 13.56\times 10^6 t).
$$

脚本最后只检查：

- `potentials_lo`
- `potentials_hi`

是否分别与理论值 `allclose(rtol=0.1)`。

因此这组 regression 真正验证的是：

- `boundary.potential_lo_x / potential_hi_x`
- time-dependent parser
- electrostatic lab-frame Dirichlet BC
- diagnostics 中 `phi` 的边界保真

### 1.4 PICMI 变体的角色

PICMI 输入并不新增物理断言，只是把同一件事改成：

- `Cartesian2DGrid(lower_boundary_conditions=["dirichlet", ...])`
- `warpx_potential_lo_x`
- `warpx_potential_hi_x`
- `ElectrostaticSolver(method="Multigrid")`

所以它的角色更准确地是：

- `time-dependent Dirichlet BC / PICMI front-end`

而不是一个新物理 benchmark。

### 1.5 更准确的分类

这组至少应记成：

- `initialization / electrostatic / time-dependent Dirichlet BC`

而不是继续泛写成 `electrostatic / Poisson`。

---

## 2. `effective_potential_electrostatic`：effective-potential solver 的 PICMI-only 绝热膨胀基准

### 2.1 当前只有一个 PICMI 入口

这组 CMake 当前只定义：

- `test_3d_effective_potential_electrostatic_picmi`

没有并列的 native inputs test。

因此它不是“native + PICMI 一一对应”的回归，而是：

- PICMI-only
- 带源码层强 analysis

### 2.2 输入真正打开的物理-算法组合

PICMI 脚本做了几件关键事：

1. 用 `GaussianBunchDistribution` 初始化电子和离子球团；
2. 放进一个导体球 EB：
   - `EmbeddedBoundary(implicit_function="x**2+y**2+z**2-R**2", potential=0.0)`
3. 选择 electrostatic solver：
   - `method="Multigrid"`
   - `warpx_effective_potential=True`
   - `warpx_effective_potential_factor=C_EP`

所以这组 test 并不是普通 self-field Poisson，而是：

- effective-potential electrostatic solver
- embedded conducting sphere
- 绝热膨胀近似 benchmark

### 2.3 analysis 真正在比较什么

`analysis.py` 先从 `sim_parameters.dpkl` 读回：

- `sigma_0`
- `M`
- `T_e`
- `T_i`
- `n_plasma`

然后构造特征时间：
$$
\tau=\sigma_0\sqrt{\frac{M}{k_B(T_e+T_i)}}.
$$

再用 Connor et al. 绝热膨胀近似给出电子密度解析式：
$$
n_e(r,t)=n_0\left(\frac{T(t)}{T_e}\right)^{3/2}
\exp\left(-\frac{r^2}{2\sigma(t)^2}\right),
$$
其中：
$$
T(t)=\frac{T_e}{1+t^2/\tau^2},\qquad
\sigma(t)=\sigma_0\sqrt{1+t^2/\tau^2}.
$$

脚本随后：

1. 从 openPMD 读取 `rho_electrons`
2. 做球坐标采样并平均出径向电子密度
3. 与解析 `n_e(r,t)` 比较 RMS 误差

最终要求所有输出时刻都满足：

- `rms_errors < 0.07`

因此它真正验证的是：

- effective-potential solver 产生的电子密度演化
- 是否仍跟随绝热膨胀近似

不是单独验证某个瞬时 `phi` 场形状。

### 2.4 这组 test 的工程边界

这组还有两个容易被忽略的点：

1. 它把 `sim_parameters.dpkl` 写到本地，用于 analysis 复原理论参数；
2. 它没有 native inputs 版本，因此当前验证链天然包含：
   - PICMI front-end
   - pickle sidecar
   - openPMD diagnostics

所以这组更准确的写法应当是：

- `initialization / effective-potential electrostatic / PICMI`

而不是宽泛的 `electrostatic / Poisson`。

---

## 3. 两组条目放回 Initialization 验证图里的位置

把这两组整理清楚以后，Initialization 的静电验证图可以更明确地拆成：

1. self-field expansion：
   - `electrostatic_sphere`
   - `space_charge_initialization`
   - `relativistic_space_charge_initialization`
2. time-dependent electrostatic boundary driving：
   - `electrostatic_dirichlet_bc`
3. effective-potential electrostatic：
   - `effective_potential_electrostatic`
4. conductor / EB electrostatic：
   - `electrostatic_sphere_eb`
   - `magnetostatic_eb`
5. open-boundary / FFT electrostatic：
   - `open_bc_poisson_solver`

这样就能把“静电初始化”内部不同合同拆开，而不是让所有条目都挤在一个 `Poisson` 桶里。

---

## 4. 当前阶段性判断

到这一步，`Initialization` validation 里最明显的静电粗分类条目已经继续缩小到了更少几组：

- `electrostatic_sphere`
- `electrostatic_dirichlet_bc`
- `effective_potential_electrostatic`

其中这一轮已经把后两组压实。接下来更自然的方向是：

1. 继续清理仍残留在 `electrostatic / Poisson` 下的其他初始化条目；
2. 或切回参数索引主线，开始系统整理 `ParmParse -> chapter` 映射。
