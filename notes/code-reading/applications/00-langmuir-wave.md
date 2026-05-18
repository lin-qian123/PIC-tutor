# Langmuir wave：从解析色散关系到源码路径

绑定源码、examples 与 analysis：

- `../warpx/Examples/Tests/langmuir/CMakeLists.txt`
- `../warpx/Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`
- `../warpx/Examples/Tests/langmuir/analysis_1d.py`
- `../warpx/Examples/Tests/langmuir/analysis_2d.py`
- `../warpx/Examples/Tests/langmuir/analysis_3d.py`
- `../warpx/Examples/Tests/langmuir/analysis_rz.py`
- `../warpx/Examples/Tests/langmuir/analysis_r1d.py`
- `../warpx/Examples/Tests/langmuir/analysis_utils.py`
- `../warpx/Examples/Tests/langmuir_fluids/CMakeLists.txt`
- `../warpx/Examples/Tests/langmuir_fluids/inputs_test_1d_langmuir_fluid`
- `../warpx/Examples/Tests/langmuir_fluids/analysis_1d.py`

关联底层笔记：

- `../initialization/14-initialization-validation-map.md`
- `../particles/30-pml-eb-contact-and-mr-validation-map.md`
- `../fluids/02-fluid-pic-coupling.md`
- `../fieldsolver/13-fieldsolver-verification-map.md`
- `../diagnostics/05-reduced-diagnostic-case-studies.md`

这一篇不再逐行解释某个模块，而是回答一个更高层的问题：

- 为什么 `Langmuir wave` 适合作为 WarpX 的最小综合基准；
- 这个问题在当前 worktree 里到底覆盖了哪些源码路径；
- 哪些变体有强 analysis，哪些只是 checksum 或 PICMI scaffold。

## 1. 解析模型：当前 examples 用的是冷等离子体振荡，不是一般 warm dispersion

`Examples/Tests/langmuir/` 和 `langmuir_fluids/` 当前都以冷、周期、线性小振幅扰动为前提。最小 1D 输入里直接定义：

```text
my_constants.epsilon = 0.01
my_constants.n0 = 2.e24
my_constants.wp = sqrt(2.*n0*q_e**2/(epsilon0*m_e))
my_constants.k = 2.*pi/20.e-6
```

这里最关键的不是 `k`，而是：

$$
\omega_p = \sqrt{\frac{2 n_0 e^2}{\epsilon_0 m_e}}.
$$

因子 `2` 不是数值技巧，而是因为当前 PIC Langmuir 基准用的是对称的电子/正电子双 species：

- 电子和正电子质量相同；
- 电荷符号相反；
- 初始密度都设成 `n_0`；
- 两者动量微扰符号相反。

在冷、线性、电静近似下，两种带电流体都对恢复力做出同号贡献，因此本地 tests 采用的基准频率是双 species 版本的 plasma frequency，而不是单电子对静止离子背景的

$$
\omega_{pe}^2 = \frac{n_0 e^2}{\epsilon_0 m_e}.
$$

这也是为什么 `analysis_1d.py`、`analysis_2d.py`、`analysis_3d.py` 里理论电场都写成：

$$
E \propto \epsilon \frac{m_e c^2 k}{e}\sin(\omega_p t).
$$

在当前本地案例里，`Langmuir wave` 的真正任务不是“拟合一般色散关系曲线”，而是：

1. 检查初始化给出的正弦/余弦微扰是否正确进入粒子与场；
2. 检查场求解、gather、deposition 和边界组合后，数值解是否仍贴着这条冷等离子体解析振荡。

## 2. 输入骨架：它首先是一个初始化与最小 PIC 回路基准

最小原生 PIC 入口是：

- `../warpx/Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`

它的骨架非常稳定：

```text
geometry.dims = 1
boundary.field_lo/hi = periodic
algo.field_gathering = energy-conserving
algo.current_deposition = esirkepov
algo.particle_shape = 1
warpx.cfl = 0.8
particles.species_names = electrons positrons
electrons/positrons.injection_style = NUniformPerCell
electrons/positrons.profile = constant
electrons/positrons.momentum_distribution_type = parse_momentum_function
```

这里每一层都有明确职责：

1. `periodic`
   - 去掉开放边界和外部驱动，让误差主要来自初始化、推进和沉积。
2. `NUniformPerCell + constant density`
   - 保证背景粒子装填最简单，便于把问题收缩成“微扰是否被正确叠加”。
3. `parse_momentum_function`
   - 把解析微扰直接写成 parser，可同时验证 `SpeciesUtils`、`PlasmaInjector` 和粒子创建路径。
4. `energy-conserving gather + esirkepov`
   - 给 charge conservation 检查提供最经典的最小合同。

因此 `Langmuir wave` 在当前项目里首先是一个初始化基准，只有在这层稳定后，才进一步承担沉积、PSATD、MR、PICMI 等更细路径的 regression 角色。

## 3. 源码路径：这一条应用主线实际横跨 4 个模块

当前 worktree 下，`Langmuir wave` 不是单个目录的局部例子，而是贯穿：

1. `Initialization/`
2. `Particles/`
3. `FieldSolver/`
4. `Diagnostics/`

### 3.1 初始化：parser 微扰如何落进粒子

最直接的源码入口已经在 `initialization/14` 和第 3A 章压实：

- `SpeciesUtils::parseDensity/parseMomentum`
- `PlasmaInjector`
- `AddPlasma()`

对 Langmuir 来说，真正重要的不是 `gaussian_beam` 这类特殊输入，而是：

- `NUniformPerCell`
- `profile = constant`
- `parse_momentum_function_*`

这意味着 Langmuir 直接验证：

```text
ParmParse
-> parser string
-> SpeciesUtils parser functor
-> PlasmaInjector
-> AddPlasma()
-> 初始粒子相空间分布
```

### 3.2 粒子推进与沉积：解析振荡为什么能暴露 gather/deposition 问题

Langmuir 的另一个价值在于，它对 `Particles/` 路径高度敏感：

- `FieldGather.H`
- `ChargeDeposition.H`
- `CurrentDeposition.H`

因为解析解极其简单，一旦：

- gather 错位；
- deposition 不守恒；
- shape / staggering / nodal 组合不一致；

误差会立刻体现在：

- `Ex/Ez` 与解析解偏离；
- `divE - rho/epsilon0` 超阈值；
- PSATD current correction 失效。

这也是为什么 `analysis_utils.py` 把 charge conservation 检查写成共享后处理，而不是把 Langmuir 只当成“看电场像不像正弦波”的单一测试。

### 3.3 场求解：它也是最干净的 solver regression 骨架之一

在当前回归树里，Langmuir 还承担了求解器组合的最小骨架：

- Yee/FDTD
- PSATD
- PSATD + current correction
- PSATD + JRhom
- nodal
- Vay deposition
- momentum-conserving gather

它的好处很直接：

- 解析波形已知；
- 周期边界避免边界层干扰；
- 无外场、无复杂 target、无碰撞；
- 因此求解器分支变化可以在最小物理背景下单独观察。

### 3.4 诊断：它同时覆盖 full diagnostics 与 openPMD reader-side 合同

1D 最小输入本身已经同时写：

```text
diag1.diag_type = Full
diag1.fields_to_plot = ... rho divE
openpmd.diag_type = Full
openpmd.format = openpmd
```

因此 Langmuir 不只验证数值物理，还覆盖：

- plotfile/full diagnostics
- openPMD writer
- `yt` / `openPMD` reader-side analysis

尤其是 3D 版本，analysis 还会检查：

- selective particle output
- on-particle `Ex/Ey/Ez`

这让它成为 diagnostics 章节里最值得保留的最小 reader-side 真例子之一。

## 4. 强 analysis 主树：原生 PIC 版本已经很完整

当前 `Examples/Tests/langmuir/CMakeLists.txt` 的主树不是 checksum-only，而是：

- `analysis_1d.py`
- `analysis_2d.py`
- `analysis_3d.py`
- `analysis_rz.py`
- `analysis_r1d.py`
+ checksum helper

也就是说，对原生输入的 1D/2D/3D/RZ/RCYLINDER/RSPHERE 版本，应把 checksum 看成历史输出基线，而不是主要物理判据。

### 4.1 1D：最直接的 `Ez` 逐点比较

`analysis_1d.py` 的主断言很简单：

```python
E_sim = data[("mesh", "Ez")].to_ndarray()[:, 0, 0]
E_th = get_theoretical_field("Ez", t0)
max_error = abs(E_sim - E_th).max() / abs(E_th).max()
assert error_rel < 0.05
check_charge_conservation(data)
```

这条 test 已经证明：

- 初始微扰进入了正确的时间层；
- 数值 `Ez` 在 `t = current_time` 仍贴着解析振荡；
- 若当前组合适用，还会继续验证 Gauss 定律误差。

### 4.2 2D/3D：不是简单复制 1D，而是多分量场解

`analysis_2d.py` 和 `analysis_3d.py` 会比较：

- `Ex`
- `Ez`
- 3D 时额外扩展到 `Ey` / on-particle field 采样

它们的解析解已经从 1D 的单正弦，扩展成：

$$
E_x \propto \sin(k_x x)\cos(k_z z)\sin(\omega_p t), \qquad
E_z \propto \cos(k_x x)\sin(k_z z)\sin(\omega_p t).
$$

因此 2D/3D 版本真正验证的是：

- 多维 parser 微扰是否正确进入；
- staggered field layout 与 reader-side 采样是否一致；
- 粒子/场维度扩展后，解析模式结构是否仍保持。

### 4.3 RZ / RCYLINDER / RSPHERE：坐标系特化仍有解析对照

`analysis_rz.py` 和 `analysis_r1d.py` 说明 Langmuir 家族不是“只适合 Cartesian”：

- RZ 版本继续比较 `Er/Ez`
- RCYLINDER / RSPHERE 继续比较径向 `Er`

所以这条应用主线本身就把非 Cartesian 坐标的最小解析基准接上了。

## 5. `analysis_utils.py` 的真实作用：不是附加小工具，而是守恒判据总线

`analysis_utils.py` 当前干的事很关键：

1. 读取 `warpx_used_inputs`
2. 判断当前是不是：
   - Esirkepov
   - Vay deposition
   - PSATD current correction
3. 只在这些组合下才执行

$$
\max \frac{| \nabla \cdot E - \rho/\epsilon_0 |}{\max |\rho/\epsilon_0|}
$$

的强断言。

这意味着 Langmuir 家族不是单一测试，而是一棵共享“解析波形 + 条件式守恒检查”的验证树。

也正因为如此，像下面这些名字：

- `..._psatd_current_correction`
- `..._psatd_vay_deposition`
- `..._momentum_conserving`

都不应再在项目文档里被拆成互不相关的小应用；它们本质上是同一条 Langmuir 应用主线下的数值分支。

## 6. MR、PSATD、Vay、JRhom：Langmuir 是数值分支的总挂钩

当前 worktree 里，Langmuir 家族已经把一批非常重要的数值分支挂到了同一解析基准上：

1. `multi_mr`
   - mesh refinement 下继续比较解析场解；
2. `..._psatd`
   - 谱求解器下继续比较解析场解；
3. `..._current_correction`
   - 在 PSATD current correction 下额外强制 Gauss 定律；
4. `..._JRhom_LL2/LL4`
   - 作为 PSATD J-rho 耦合的最小波动基准；
5. `..._vay_deposition`
   - 用更宽容差验证 Vay deposition 的守恒边界；
6. `..._momentum_conserving`
   - 检查 momentum-conserving gather 的最小稳定性合同。

从应用综合章的角度，Langmuir wave 的价值恰恰在这里：

- 不是只有一个 textbook 例子；
- 而是整个显式 PIC 数值分支的共同“试纸”。

## 7. PICMI 与 checksum-only 边界：不能写过头

当前 worktree 下，2D/3D/RZ 的 PICMI Langmuir 变体大多是：

- `analysis = OFF`
- 只有 checksum

因此在书稿里必须明确：

1. 原生输入族：
   - 有强 analysis
2. PICMI 变体：
   - 当前多半只是前端配线 + writer/output scaffold

唯一需要单独记住的例外是：

- `test_3d_langmuir_multi_psatd_JRhom_LL2_picmi`

它虽然来自 PICMI 输入，但 `CMakeLists.txt` 中仍直接跑 `analysis_3d.py`，所以不能一概写成 PICMI 全是 checksum-only scaffold。

## 8. `langmuir_fluids`：同一物理问题上的 cold-fluid 对照树

`langmuir_fluids` 不是附属小测试，而是本地 `Fluids/` 最直接的 validation 入口。

它和普通 PIC Langmuir 的区别很清楚：

- PIC Langmuir 主要比较 `E`，并在适用时检查 `divE` 与 `rho`
- fluid Langmuir 直接比较：
  - `Ez`
  - `Jz`
  - `rho`

`analysis_1d.py` 里已经明确：

```python
J_sim = data[("mesh", "Jz")].to_ndarray()[:, 0, 0]
rho_sim = data[("boxlib", "rho")].to_ndarray()[:, 0, 0]
...
assert error_rel < 0.05
```

因此，应用综合章里最准确的表述是：

- `langmuir`
  - 是显式 PIC 主链的最小解析基准
- `langmuir_fluids`
  - 是 `Fluids/` runtime layer 的最小解析基准

两者共享同一个物理问题，但落点不同。

## 9. 对书稿最重要的总结构

把当前 worktree 证据压缩成一句话，`Langmuir wave` 在本项目里真正代表的是：

```text
解析冷等离子体振荡
-> parser/常密度/均匀装填初始化
-> gather/pusher/deposition/solver 的最小 PIC 主链
-> full diagnostics 与 openPMD reader-side analysis
-> MR / PSATD / current correction / Vay / JRhom / PICMI / fluids 分支
```

所以它已经足够承担应用综合章的第一篇案例，而不是只是第 8 章开头的一小段例子说明。

## 10. 当前边界

当前这条应用主线还没有做的，不是源码阅读，而是更高一层的收口：

1. 把 `Langmuir wave` 的应用级讲解继续压进正式综合章结构；
2. 若后续要满足“至少一个本地运行记录”，还需要把：
   - 命令
   - 环境
   - 输出目录
   - 物理检查量
   记录成独立 run note。

但从“解析模型到源码路径”的要求看，当前 worktree 证据已经足够把 `TODO` 里的 `Langmuir wave` 从未开始推进到可正式成文的状态。

## 10A. 本地最小运行记录

2026-05-18 已做第一条真实运行记录，工作目录：

- `/Volumes/PHILIPS/programs/PIC/PIC-tutor/runs/stage-c-validation/langmuir_1d`

实际命令：

```bash
env OMP_NUM_THREADS=1 FI_PROVIDER=tcp \
  /Volumes/PHILIPS/programs/PIC/warpx/build_full/bin/warpx.1d.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES \
  /Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/langmuir/inputs_test_1d_langmuir_multi
```

这里必须单独记住两点：

1. 在 Codex 默认沙箱里直接运行会因为 MPI/OFI 访问 `utun6` 失败而中止；
2. 切到无沙箱运行后，1D case 可以正常完成，并产出：
   - `diags/diag1000080`
   - `diags/openpmd/openpmd_000080.bp5`
   - `warpx_used_inputs`

WarpX 自带 `analysis_1d.py` 这轮没有原样跑通，因为当前本机可直接调用的 Python 环境缺：

- `matplotlib`
- `yt`

但其核心物理断言已经按同一公式手工复现：

- 解析场比较：
  $$
  \max \frac{|E_z^{\mathrm{sim}}-E_z^{\mathrm{th}}|}{|E_z^{\mathrm{th}}|}
  = 1.7027848999745115\times 10^{-3}
  < 5\times 10^{-2}
  $$
- 电荷守恒比较：
  $$
  \max \frac{|\nabla\cdot E-\rho/\epsilon_0|}{|\rho/\epsilon_0|}
  = 8.34503170903001\times 10^{-12}
  < 10^{-11}
  $$

所以这条最小运行记录已经支持一个更硬的判断：

- `test_1d_langmuir_multi`
  - 不是只“能跑完”
  - 而是当前本地已经有：
    - 真实运行命令
    - 真实输出目录
    - 解析场误差
    - `divE-rho/\epsilon_0` 误差

换句话说，它现在已经不只是源码级强基准，也是本项目当前 Stage C 第一条已落地的运行级强基准。

## 11. 用 Birdsall 重新读 `langmuir`

Birdsall-Langdon 的 Chapter 8、10、12 给这棵树补了三层更硬的解释：

1. Chapter 8
   - `langmuir` 的解析场解不只是“波形对不对”，而是在最小背景下检查 sampled density、shape、field differencing 和 alias branches 是否还共同落在受控 dispersion relation 上。
2. Chapter 10
   - 当输入显式切到 `momentum-conserving gather`、`current_correction`、Vay deposition 或 JRhom/PSATD 变体时，本地 tests 其实是在问：这套离散守恒合同有没有把 `divE-rho/\epsilon_0` 和主模结构一并守住。
3. Chapter 12
   - 对 `langmuir` 家族来说，`analysis_utils.py` 里的 charge-conservation 检查不只是附属小 assert；它正好是把 Birdsall 的 fluctuation / effective-collision 风险挡在门外的最低门槛。

所以 `langmuir` 在当前项目里最准确的定位应写成：

- 解析 Langmuir 模 benchmark
- 离散守恒合同探针
- diagnostics/openPMD reader-side 最小真例子

而不是只写成“最基础的 plasma oscillation test”。
