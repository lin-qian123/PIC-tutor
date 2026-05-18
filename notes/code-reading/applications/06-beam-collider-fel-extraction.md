# Beam-beam / luminosity / FEL / ion extraction：束流与加速器应用主线

绑定源码、examples 与 analysis：

- `../warpx/Examples/Tests/diff_lumi_diag/*`
- `../warpx/Examples/Physics_applications/beam_beam_collision/*`
- `../warpx/Examples/Physics_applications/free_electron_laser/*`
- `../warpx/Examples/Physics_applications/ion_beam_extraction/*`
- `../warpx/Examples/Tests/accelerator_lattice/*`

关联底层笔记：

- `../diagnostics/05-reduced-diagnostic-case-studies.md`
- `../laser/06-rigid-injection-btd-and-undulator-coupling.md`
- `../utils/07-parameter-validation-links-for-boundary-and-external-fields.md`
- `../accelerator-lattice/03-validation-map.md`

这一篇不重复底层 solver 或 diagnostics 细节，而是把当前 worktree 里分散的束流、对撞机、FEL 和离子抽取材料重新收束成同一条应用主线，并明确每个入口的强弱边界。

## 1. 这条应用线的真实骨架

当前本地工作树里，最容易被混成一桶的是：

- `DifferentialLuminosity`
- `beam_beam_collision`
- `free_electron_laser`
- `ion_beam_extraction`
- `accelerator_lattice`

但它们承担的合同并不在同一层级。更准确的组织方式应当是：

```text
beam / accelerator applications
-> reduced-diagnostic strong benchmark: DifferentialLuminosity
-> collider-QED application baseline: beam_beam_collision
-> boosted rigid-beam radiation benchmark: free_electron_laser
-> electrostatic EB extraction application: ion_beam_extraction
-> beamline optics strong regression: accelerator_lattice
```

这样分层之后，哪些目录是在验证 diagnostics，哪些是在验证物理工作流，哪些是在验证 beamline optics，就不会再互相冒充。

## 2. `DifferentialLuminosity`：这条线里的 diagnostics 强基准

`Examples/Tests/diff_lumi_diag/` 当前是这条应用线里最强的 diagnostics regression。

`CMakeLists.txt` 里 active tests 都同时跑：

- `analysis.py`
- `analysis_default_regression.py --path diags/diag1000080 --rtol 1e-2`

而 `analysis.py` 不是简单画图，它会同时验证：

1. 一维文本表
   - `DifferentialLuminosity_beam1_beam2.txt`
2. 二维 openPMD 网格
   - `DifferentialLuminosity2d_beam1_beam2/`

并直接构造两束 Gaussian beams 的解析 luminosity 谱：

- `dL/dE`
- `d^2L/dE_1 dE_2`

然后做显式误差比较与 `assert`。

因此，这条回归在当前 worktree 中的角色必须写成：

- `reduced-diagnostic strong benchmark`

而不是：

- beam-beam application helper

它解决的是“束流对撞时 diagnostics 是否把能量谱写对”，不是“完整 collider-QED 工作流是否都正确”。

## 3. `beam_beam_collision`：当前不是 luminosity 强谱基准，而是 collider-QED 应用骨架

`Examples/Physics_applications/beam_beam_collision/` 最容易被误写成 luminosity benchmark。但现有证据层更弱，也更偏应用骨架。

已有本地诊断笔记已经压实：

1. active regression 只有
   - `test_3d_beam_beam_collision`
2. `analysis = OFF`
3. 只跑 checksum helper
4. `plot_fields.py` / `plot_reduced.py`
   - 都只是 user-side visualization scripts

因此它当前不能和 `DifferentialLuminosity` 混成同一等级。

### 3.1 它真正覆盖的联合路径

`inputs_test_3d_beam_beam_collision` 当前把这些路径绑在一起：

- `warpx.do_electrostatic = relativistic`
- collocated grid
- 两束 `125 GeV` 电子/正电子 Gaussian bunch 对撞
- `initialize_self_fields = 1`
- Quantum Synchrotron photon emission
- Breit-Wheeler pair creation
- `ColliderRelevant_beam1_beam2`
- `ParticleNumber`
- openPMD full diagnostics

所以它当前真正证明的是：

- collider self-field
- beamstrahlung
- coherent pair generation
- collider-oriented reduced diagnostics

这条联合应用链能稳定接通。

### 3.2 它的真实定位

因此 `beam_beam_collision` 最准确的项目内定位应当是：

- `collider-QED application baseline`

而不是：

- `luminosity strong benchmark`

它可以作为这一整条 beam/collider 应用线的“完整工作流代表”，但不能替代 `DifferentialLuminosity` 的解析谱对照合同。

## 4. `free_electron_laser`：boosted rigid-beam + undulator + BTD 的强 benchmark

`Examples/Physics_applications/free_electron_laser/README.rst` 已经把物理图景写得很清楚：

- relativistic electron beam
- undulator external magnetic field
- radiation grows exponentially
- simulation is done in a boosted frame
- physical observables are reconstructed with `BackTransformed` diagnostics

这条应用线在当前 worktree 中不能再被简化成“一个 laser example”，因为它本质上没有 laser antenna。已有本地笔记已经压实：

- 核心是 `RigidInjectedParticleContainer`
- `particles.By_external_particle_function(...)` 提供 undulator 外加粒子磁场
- `BackTransformed` diagnostics 与 boosted-frame full diagnostics 的一致性

### 4.1 当前强断言不是 writer，而是 FEL 标度

本地已有笔记已明确 `analysis_fel.py` 的两层强断言：

1. 在 `diag_labframe` 里对 `log(E_x^2)` 的线性增长区做拟合
   - 要求 gain length 接近 `0.22 m`
   - 相对误差小于 `15%`
2. 在 lab-frame 与 boosted-frame diagnostics 上做 FFT
   - 要求恢复出的 radiation wavelength 满足 undulator 理论值
   - 误差小于 `1%`

因此 `free_electron_laser` 当前最准确的角色应当是：

- `boosted rigid-beam radiation benchmark`

而不是：

- generic laser application
- generic BTD writer demo

它把：

- rigid bunch
- external particle-field undulator
- boosted-frame push
- BTD/lab-frame reconstruction

压在同一个强分析合同里。

### 4.2 `Dawson 1983` 里的 FEL 是这条应用线的历史前身，而不是现代 WarpX 合同本身

`Dawson 1983` 把 free-electron laser 专门拿来当 relativistic electromagnetic particle model 的代表例子。这一点很重要，因为它说明 FEL 在经典 PIC 文献里的作用不是“又一个束流应用”，而是展示：

- relativistic beam
- static helical ripple field
- electromagnetic radiation growth
- electrostatic beam wave coupling
- nonlinear trapping saturation

怎样在同一个 reduced-dimension EM-PIC model 里闭合。

文中给出的最小物理图景有两层：

1. lab frame 下，螺旋磁场周期 `\lambda_0` 与 relativistic beam 共同把辐射波长压到

$$
\lambda \simeq \frac{\lambda_0}{2\gamma^2};
$$

2. beam frame 下，ripple field 等价于 pump electromagnetic wave，并通过 Raman-like 参数不稳定满足

$$
k_{\mathrm{pump}} = k_{\mathrm{EM}} + k_p,
$$

$$
\omega_{\mathrm{pump}} = \omega_{\mathrm{EM}} + \omega_p(k_p).
$$

作者还明确给出了这条历史 simulation line 的硬结果：

- electromagnetic / electrostatic spectra 同时满足 matching condition；
- 饱和时 longitudinal current 下降约 `36%`；
- 约 `30%` 的束流能量转成辐射；
- 波长约 `2\lambda_0` 的 backward mode 会变得危险；
- saturation 的核心机制是 electrostatic-wave trapping，而不是单纯线性增益耗尽。

这条文献边界和当前 WarpX `free_electron_laser` 的关系应写得很克制：

- `Dawson 1983`
  - 支撑的是 FEL 作为 relativistic EM-PIC representative problem 的历史物理图景；
- 当前 worktree 的 `free_electron_laser`
  - 支撑的是 boosted rigid-beam + undulator + BTD 的现代强 regression 合同。

两者之间有明确谱系关系，但不能把 1983 综述直接拿来冒充现代 WarpX `analysis_fel.py` 的逐项验证文献。

从图像合同上看，`Dawson 1983` 这条历史 FEL 线也已经相当完整：

- `Fig.54`
  - 给出 helical ripple field 下的 lab-frame kinematics 与 beam-frame pump-wave 重写；
- `Fig.55`
  - 用 EM / electrostatic spectra 证明 matching condition 真正成立；
- `Fig.56`
  - 把 EM energy、electrostatic energy 与 longitudinal current 放在同一张图里，显式展示 gain、beam degradation 与 saturation 的同步出现；
- `Fig.57`
  - 再把 trapping-based efficiency estimate
    $$
    \eta = \frac{\gamma_0-\gamma_{\mathrm{ph}}}{\gamma_0-1}
    $$
    及其大-$\gamma$ 近似
    $$
    \eta \simeq \omega_{po}(2k_0 c \gamma^{3/2})^{-1}
    $$
    与 simulation 做并排比较。

这意味着这条经典文献真正完成的是：

```text
mechanism verification
-> nonlinear saturation
-> rough efficiency scaling
```

而当前 WarpX `free_electron_laser` 则把这条谱系进一步推进成：

```text
boosted rigid-beam implementation
-> lab-frame / BTD reconstruction
-> gain-length and wavelength regression
```

## 5. `ion_beam_extraction`：EB electrostatic extraction 的强应用入口

`Examples/Physics_applications/ion_beam_extraction/` 当前是这条应用线里最直接的 electrostatic + embedded-boundary beam-source application。

它的物理结构是：

- `z<0` 的 plasma source
- 电极 held at fixed electrostatic potentials
- embedded-boundary electrode geometry
- 持续 boundary injection
- 最终抽出约 `40 keV` 的离子束

### 5.1 当前最关键的合同不是 geometry 本身，而是势场与能量尺度

已有参数-验证笔记已经压实：

- `boundary.potential_lo_z`
  - 是域边界势
- `warpx.eb_potential(x,y,z,t)`
  - 是 embedded-boundary 电极势

WarpX 只在电极表面评估 `warpx.eb_potential(...)`，而电极间真空区势分布由 electrostatic solver 自己解出。这一点正是它作为应用入口的价值所在：它把

- domain potential
- EB potential
- electrostatic solver
- embedded-boundary geometry
- extraction beam dynamics

接成了一条完整链。

### 5.2 当前 analysis 是强应用级断言

`analysis_ion_beam_extraction.py` 当前会：

- 读 `phi`
- 读 `eb_covered`
- 读 `Dplus` 粒子
- 检查抽出离子束尾部能量是否接近 `40 keV`

核心断言是：

- `target_energy_keV = 40`
- `tolerance = 0.05`

因此它的真实角色不是 checksum baseline，而是：

- `electrostatic EB extraction strong application check`

也就是说，这条应用线当前明确验证的是：

- `boundary.potential_* + warpx.eb_potential(...) + electrostatic solve + EB geometry`

这组合同能够共同产生正确的抽取能量尺度。

## 6. `accelerator_lattice`：这条应用线里的 beamline optics 强回归层

如果只写 collider、FEL 和 extraction，这条总节还少了一块真正对应 beamline 模块本身的强验证层。

这个位置当前最自然的入口是：

- `Examples/Tests/accelerator_lattice/`

已有本地 `accelerator-lattice/03-validation-map.md` 已经压实：

- `test_3d_hard_edged_quadrupoles`
- `test_3d_hard_edged_quadrupoles_boosted`
- `test_3d_hard_edged_quadrupoles_moving`

都同时跑：

- `analysis.py`
- checksum helper

而 `analysis.py` 的真实断言对象是：

- 重新读回 `lattice.elements` / `line*` / `drift*` / `quad*`
- 在 Python 中按解析 hard-edged quadrupole optics 逐段积分
- 最后要求最终粒子 `x`、`u_x` 与解析解足够接近

这使它在当前 worktree 里的正确角色是：

- `beamline optics strong regression`

而不是：

- 只是加速器模块“能读输入”

同时它还覆盖了三种运行态：

- lab frame
- boosted frame
- moving window

所以它恰好补上了这条总节中“加速器模块”这一半。

## 7. 当前 worktree 下这条总节真正成立的分层

把这组材料压成最保守也最准确的一组结论：

1. `DifferentialLuminosity`
   - 是束流应用线里的 reduced-diagnostic 强谱基准；
2. `beam_beam_collision`
   - 是 collider-QED 应用骨架；
3. `free_electron_laser`
   - 是 boosted rigid-beam + undulator + BTD 的强 benchmark；
4. `ion_beam_extraction`
   - 是 electrostatic + EB beam extraction 的强应用入口；
5. `accelerator_lattice`
   - 是 beamline optics 的强 regression 层。

因此，当前书稿里这条应用综合主线最合理的组织方式不是：

```text
beam-related examples
```

而应该是：

```text
beam and accelerator applications
-> luminosity diagnostics benchmark
-> collider-QED workflow baseline
-> FEL boosted-frame radiation benchmark
-> electrostatic ion-source extraction
-> accelerator-lattice optics regression
```
