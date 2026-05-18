# LWFA/PWFA：moving window、boosted frame、diagnostics 与前端分裂

绑定源码、examples 与 analysis：

- `../warpx/Examples/Physics_applications/laser_acceleration/README.rst`
- `../warpx/Examples/Physics_applications/laser_acceleration/CMakeLists.txt`
- `../warpx/Examples/Physics_applications/plasma_acceleration/README.rst`
- `../warpx/Examples/Physics_applications/plasma_acceleration/CMakeLists.txt`
- `../warpx/Examples/analysis_default_regression.py`
- `../warpx/Examples/analysis_default_restart.py`

关联底层笔记：

- `../laser/03-laser-validation-map.md`
- `../laser/04-moving-window-external-field-coupling.md`
- `../laser/05-application-and-diagnostic-cases.md`
- `../evolve/05-moving-window.md`
- `../diagnostics/08-template-cases-and-boundaryscraping-example.md`

这一篇不把 `LWFA` 和 `PWFA` 强行写成同一种 physics benchmark，而是回答当前本地 worktree 下更实际的问题：

- `laser_acceleration` 和 `plasma_acceleration` 这两个应用目录，分别在验证什么；
- 哪些条目是强 analysis，哪些只是 workflow/checksum baseline；
- moving window、boosted frame、mesh refinement、PICMI 和 diagnostics 怎样把两者连接成同一类 wakefield runtime architecture。

## 1. 共同物理框架：两者都属于 wakefield acceleration，但驱动器不同

这两组 examples 的共同点不是“都带 acceleration”这么宽泛，而是都在建模 wakefield acceleration：

1. `LWFA`
   - driver 是 laser；
   - 最直接入口是 `GaussianLaser` 天线、moving window 和 underdense plasma。
2. `PWFA`
   - driver 是 relativistic bunch；
   - 最直接入口是 rigid-injected beam、boosted frame 和 plasma channel / density ramp。

所以应用综合章里更准确的组织方式不是“一个 laser 目录，一个 plasma 目录”，而是：

```text
wakefield acceleration
-> LWFA runtime matrix
-> PWFA workflow matrix
```

二者共享的工程关切非常稳定：

- moving window
- boosted frame
- diagnostics
- mesh refinement
- native input vs PICMI front-end

但它们的 physics driver 和现有 regression 强度并不相同。

### 1.1 `Tajima-Dawson 1979` 给这条应用线提供的不是 regression，而是最早期 scaling baseline

当前本地已经 materialize 并开始精读：

- `references/03_pic_foundations/1979_TajimaDawson_Laser_Electron_Accelerator/`

这篇文章对本节最重要的价值，不是提供一个可以直接和当前 WarpX `laser_acceleration` tests 一一对照的 analysis script，而是把 `LWFA` 的最小物理闭环写得非常干净：

```text
laser pulse
-> ponderomotive wake excitation
-> plasma wave with phase velocity near c
-> electron trapping
-> energy gain over long dephasing length
```

当前已经从原文压实的最关键量有：

$$
v_p = v_g^{EM} = c\sqrt{1-\frac{\omega_p^2}{\omega^2}},
$$

$$
L_t = \frac{\lambda_w}{2} = \frac{\pi c}{\omega_p},
$$

$$
eE_L \cong mc\omega_p,
$$

$$
\gamma_{\max} \simeq 2\frac{\omega^2}{\omega_p^2},
\qquad
l_a \cong 2\frac{\omega^2 c}{\omega_p^3}.
$$

所以，把 `LWFA/PWFA` 写成应用综合章时，`Tajima-Dawson 1979` 更适合承担：

- `LWFA earliest scaling baseline`
- wakefield acceleration 历史入口
- dephasing / phase-velocity / accelerating-field 叙事的最早期理论骨架

它现在还能再多承担一层，但仍然要写实：这篇文章已经给出一个最小 relativistic electromagnetic PIC demonstration，而不只是解析草图。当前从原文已压实：

- 使用 `1 1/2-D` relativistic electromagnetic code
- one spatial dimension
- three velocity / field dimensions
- Gaussian finite-size particles
- 固定离子背景
- 通过改变 `c` 扫描 `\omega/\omega_p`

并得到三条很硬的数值结果：

1. wake longitudinal field 达到
   $$
   E_L \sim 0.6\,\frac{mc\omega_p}{e},
   $$
   约为冷等离子体理论上限的 `0.6`；
2. electromagnetic spectrum 会裂成多峰，作者明确解释为 successive / multiple forward Raman scattering；
3. simulation 中的最大电子能量随 `(\omega/\omega_p)^2` 的变化基本贴合最早期解析 scaling，只是在高端开始受有限系统尺寸和周期边界影响。

因此，它对本节最准确的补充角色是：

- `earliest LWFA scaling + minimal EM PIC demonstration`

而不是：

- 现代 `laser_acceleration` active tests 的 analysis template。

还需要再保留一条文末边界，避免把这篇 paper 过度现代化：

1. 原文的 `feasible within present-day technology`
   - 只是 1979 年语境下的工程判断；
   - 紧跟着就承认 short-pulse shaping 仍需改进。
2. 原文明确保留了
   - `\Delta\omega = \omega_p`
   - two-laser / beat-wave alternative
   这条岔路；
   所以它支撑的是更宽的 early wakefield family，而不只是今天常说的单脉冲 `LWFA`。
3. 文末的 pulsar / cosmic-ray speculation
   - 只能当历史语境补充；
   - 不能写进现代 WarpX `laser_acceleration` 应用合同。

再往前一步，当前精读还说明这篇 paper 的图像证据组织方式本身也值得保留：

- `Fig.1`
  - 不是普通结果拼图；
  - 而是 `transverse quiver -> longitudinal wake -> accelerating field` 的三联机制图。
- `Fig.2(a)`
  - 不是普通谱展宽图；
  - 而是 driver spectrum splitting、multiple Raman scattering 与 photon deceleration 的证据图。
- `Fig.2(b)`
  - 不是普通参数扫描；
  - 而是 earliest LWFA scaling 是否被最小 EM-PIC 演示支持的关键对照图。

而不是承担：

- 现代 WarpX runtime matrix 的逐项 regression contract
- boosted-frame / PICMI / openPMD / MR 路径的直接验证依据

## 2. `laser_acceleration`：它是 LWFA runtime matrix，不是 laser-injection 单元测试

`Examples/Physics_applications/laser_acceleration/README.rst` 明确写的是 `Laser-Wakefield Acceleration of Electrons`，但当前本地 worktree 里它的 `Analyze` 章节仍是 `TODO`。这和 `CMakeLists.txt` 一起决定了它的真实边界：

1. 目录定位是 `LWFA application`；
2. 活跃 tests 里绝大多数是 `analysis = OFF`；
3. 目录里的多数条目首先是在覆盖 runtime path，而不是统一的 wakefield physics hard assert。

### 2.1 四个 `inputs_base_*` 本质上是四套运行骨架

`laser_acceleration` 当前更像是把 LWFA 常见运行模式拆成了四个 base skeleton：

1. `inputs_base_1d`
   - 1D moving window
   - 连续电子注入
   - Gaussian laser antenna
   - `FieldProbe`
2. `inputs_base_2d`
   - PML
   - moving window
   - refined patch
   - 连续背景电子
   - Gaussian `beam`
3. `inputs_base_3d`
   - 3D moving window
   - full/openPMD diagnostics
   - 自定义粒子属性
4. `inputs_base_rz`
   - `RZ`
   - `n_rz_azimuthal_modes = 2`
   - beam/plasma 共存
   - species 变量输出

这些 base inputs 首先定义的是：

- laser antenna
- moving window
- 连续注入
- diagnostics
- 维度/geometry 变体

而不是单独某个包络公式的解析基准。

### 2.2 当前 active tests 真正区分的是 runtime path

`CMakeLists.txt` 里当前活跃的变体，最合理的归纳方式是：

1. 1D native / PICMI skeleton
   - `test_1d_laser_acceleration`
   - `test_1d_laser_acceleration_picmi`
2. 2D boosted baseline
   - `test_2d_laser_acceleration_boosted`
3. 2D mesh-refinement baseline
   - `test_2d_laser_acceleration_mr`
   - `test_2d_laser_acceleration_mr_picmi`
4. 3D native / Python / PICMI baselines
   - `test_3d_laser_acceleration`
   - `test_3d_laser_acceleration_python`
   - `test_3d_laser_acceleration_picmi`
   - `test_3d_laser_acceleration_single_precision_comms`
5. RZ native / PICMI baselines
   - `test_rz_laser_acceleration`
   - `test_rz_laser_acceleration_picmi`
6. 少数强 analysis 分支
   - `test_1d_laser_acceleration_fluid_boosted`
   - `test_2d_refined_injection`
   - `test_rz_laser_acceleration_opmd`

这意味着 `laser_acceleration` 当前最准确的角色是：

- `LWFA runtime matrix`
- 不是统一 observable 的 physics benchmark 集

### 2.3 当前最强的 3 条 analysis 只覆盖局部合同

现有强 analysis 只有三条：

1. `analysis_1d_fluid_boosted.py`
   - boosted 1D 冷流体对照；
   - 检查 `Ez/Jz/rho/Vz` 是否贴合 theory。
2. `analysis_refined_injection.py`
   - refined injection 合同；
   - 检查 `warpx.refine_plasma = 1` 时粒子数和 refinement-edge 前方 `rho` 均匀性。
3. `analysis_openpmd_rz.py`
   - RZ openPMD diagnostics 合同；
   - 检查 mesh shape、species ordering 和 `rho_<species>` 的物理中心位置。

因此不能把 `laser_acceleration` 目录整体说成：

- 已有完整 LWFA wake amplitude hard assert；
- 已有统一 beam energy gain benchmark；
- 已有完整 laser diffraction/beamloading 解析对照。

当前 worktree 里，它仍主要是一套 wakefield runtime architectures 的 coverage tree。

## 3. `plasma_acceleration`：它是 PWFA workflow matrix，不是解析 wake benchmark

`Examples/Physics_applications/plasma_acceleration/README.rst` 明确写的是 `Beam-Driven Wakefield Acceleration of Electrons`。这点必须写死，因为它直接排除了“把它和 `LWFA` 一起混成 generic laser-plasma acceleration”的误写。

目录当前的另一个关键事实也很硬：

- `README.rst` 里 `Analyze` 是 `TODO`
- `Visualize` 是 `TODO`
- 3D PICMI boosted-frame 等价性也被源码文档自己标成 `TODO`

### 3.1 目录本体当前没有强 analysis

`CMakeLists.txt` 中所有 active tests 都是：

```cmake
OFF  # analysis
"analysis_default_regression.py --path ..."
```

也就是说，这组目录当前没有独立 `analysis.py`。它的真实角色应该写成：

- `PWFA workflow matrix`
- `beam-driven wakefield application baseline`

而不是：

- PWFA 解析 wakefield 强基准；
- beam loading / dephasing / bubble shape 的统一 hard assert。

### 3.2 当前实际覆盖的是一套 beam-driven runtime path

现有 active inputs 合起来覆盖：

1. `test_1d_plasma_acceleration_picmi`
   - 1D PICMI minimal workflow
2. `test_2d_plasma_acceleration_boosted`
   - 2D boosted + moving window baseline
3. `test_2d_plasma_acceleration_mr`
   - 2D refined-patch baseline
4. `test_2d_plasma_acceleration_mr_momentum_conserving`
   - 2D refined patch + `momentum-conserving` gather
5. `test_3d_plasma_acceleration_boosted`
   - 3D boosted baseline
6. `test_3d_plasma_acceleration_boosted_hybrid`
   - 3D boosted + hybrid-grid baseline
7. `test_3d_plasma_acceleration_mr_picmi`
   - 3D PICMI refined-region scaffold
8. `test_3d_plasma_acceleration_picmi`
   - 3D PICMI non-boosted scaffold

这些路径共同覆盖的是：

- moving window
- boosted frame
- rigid bunch
- density ramp / plasma channel
- `particles.use_fdtd_nci_corr = 1`
- MR
- hybrid grid
- PICMI front-end
- field / particle diagnostics

### 3.3 3D PICMI 不是 native boosted 的等价前端

当前 `README.rst` 自己就写着：

```text
TODO: The Python (PICMI) input file should use the boosted frame method,
like the inputs_test_3d_plasma_acceleration_boosted file.
```

这条边界必须保留，因为它决定了当前文档不能说：

- `inputs_test_3d_plasma_acceleration_picmi.py` 已经等价覆盖 native boosted PWFA

更准确的说法只能是：

- native 输入已经给出 boosted PWFA 主骨架；
- 3D PICMI 输入当前仍是 non-boosted scaffold；
- 因此目录里存在明确的 native/PICMI 能力不对齐。

## 4. 共同架构：`LWFA/PWFA` 真正能被合并的是 runtime concerns

把这两个目录并排以后，当前最值得在应用综合章里强调的不是“都能加速电子”，而是它们共享的 runtime architecture：

1. moving window
   - 都用它缩短长传播问题；
2. boosted frame
   - 都把它作为长距离传播场景的主要加速手段；
3. diagnostics
   - 都依赖 full diagnostics/checksum tree，而不是目录内成熟的统一 physics analysis；
4. mesh refinement
   - 都有 MR 变体，用来检查 refined patch 与主流程是否稳定；
5. PICMI front-end
   - 都在 native input 之外给出 PICMI scaffold，但能力覆盖不总是等价。

所以 `LWFA/PWFA` 在应用综合章里的正确组织方式不是：

```text
一组 laser physics benchmark
```

而应该是：

```text
wakefield acceleration runtime architectures
-> laser-driven branch (LWFA)
-> beam-driven branch (PWFA)
```

## 5. diagnostics 边界：当前这两组目录都更偏 workflow/output 合同

这两组目录有一个共同工程现实：

- README 的分析章节都没有真正成文；
- 目录内强 analysis 都是局部合同，不是统一 application observable；
- 活跃 regression 主体依然靠 checksum baseline。

因此它们在当前项目里更适合承担：

1. moving-window / boosted-frame application skeleton；
2. diagnostics 输出链稳定性；
3. native/PICMI/python front-end 路径覆盖；
4. MR / hybrid-grid / single-precision-comms 这类工程变体覆盖。

而不应被夸大成：

- 一套现成的 LWFA/PWFA 理论闭环 benchmark 书写模板。

## 6. 对应用综合章最重要的结论

到当前 worktree 为止，`LWFA/PWFA` 这条应用主线已经足够写成第三条正式应用入口，但它的核心结论必须写实：

1. `laser_acceleration`
   - 是 `LWFA runtime matrix`
   - 只有少量局部强 analysis
   - 多数条目是 runtime/checksum baseline
2. `plasma_acceleration`
   - 是 `PWFA workflow matrix`
   - 当前 active tree 全部 checksum-only
   - 3D PICMI 仍未达到 native boosted 等价覆盖
3. 二者共享的真正主线是：
   - moving window
   - boosted frame
   - diagnostics
   - MR
   - PICMI/native front-end split

因此，后续书稿如果要从应用角度组织 wakefield acceleration，一章里最自然的结构不是按“laser 目录 / plasma 目录”切，而是先讲 shared runtime architecture，再分别讲：

- laser-driven branch
- beam-driven branch

这比把它们直接混写成一个统一 benchmark 更符合当前本地证据。
