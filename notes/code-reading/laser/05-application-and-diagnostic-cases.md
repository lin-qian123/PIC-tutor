# Laser 应用层与 diagnostics 场景地图

绑定源码与例子：

- `../warpx/Examples/Physics_applications/laser_ion/`
- `../warpx/Examples/Physics_applications/free_electron_laser/`
- `../warpx/Examples/Tests/laser_on_fine/`

前四篇笔记已经把 laser 的源码主链、moving window 交界和 regression 证据层打通了。这一篇继续往上走一层，回答：

1. 同一条 laser antenna 注入链，进入真实应用场景后最常和哪些物理模块一起工作。
2. 应用层 analysis 通常在验证 laser 本体，还是在验证 laser 驱动后的 diagnostics / downstream physics。
3. `laser_ion`、`free_electron_laser`、`laser_on_fine` 各自处在应用谱系的什么位置。

## 1. `laser_ion`：laser 天线主链进入强场靶相互作用与 diagnostics 组合

### 1.1 输入文件的结构不是“只有一束激光”

`inputs_test_2d_laser_ion_acc` 把以下几类对象绑在了一起：

1. 2D solid-density target
2. `Gaussian` laser antenna
3. PML/open particle boundaries
4. full diagnostics
5. time-averaged diagnostics
6. `ParticleHistogram`
7. `FieldProbe`
8. `LoadBalanceCosts`
9. `ParticleHistogram2D`

也就是说，`laser_ion` 的重点不是“再验证一次 Gaussian profile 是否正确”，而是把 laser 主链接入一个典型的强场靶相互作用工作流，观察：

- 激光沉积怎样驱动电子和离子
- 这些下游粒子如何被 reduced diagnostics 和 full diagnostics 消费

### 1.2 这里的 analysis 真正验证的是 diagnostics 合同

`CMakeLists.txt` 中：

```cmake
add_warpx_test(
    test_2d_laser_ion_acc
    ...
    "analysis_test_laser_ion.py diags/diagInst/"
    "analysis_default_regression.py --path diags/diagInst/"
)
```

`analysis_test_laser_ion.py` 的硬断言不是 target acceleration physics 本身，而是：

```python
compare_time_avg_with_instantaneous_diags(
    dir_inst=sys.argv[1],
    dir_avg="diags/diagTimeAvg/",
)
```

它把：

1. `diagInst` 中最后 5 个 snapshot 的瞬时 `Ez`
2. `diagTimeAvg` 中原位 time-averaged `Ez`

做逐点比较，要求 `np.allclose(..., rtol=1e-12)`。

因此这组 regression 的最硬断言对象是：

- `TimeAveragedFieldDiagnostic`
- openPMD writer
- `laser -> fields -> diagnostics` 的时序一致性

而不是 proton cutoff energy、TNSA 标度之类更高层的应用物理。

### 1.3 `laser_ion` 给书稿带来的真正价值

这组例子最适合在书稿里承担两个角色：

1. 展示 laser 注入主链怎样进入密等离子体/固体靶问题；
2. 展示一组丰富 diagnostics 如何围绕同一束激光组织起来。

尤其是输入文件里同时出现了：

- `ParticleHistogram`
- `FieldProbe`
- `LoadBalanceCosts`
- `ParticleHistogram2D`

说明 `laser_ion` 在项目里更像“应用 + diagnostics 组合样板”，而不是单一激光公式回归。

## 2. `free_electron_laser`：laser 不再是天线源，而是束流在外磁场中自发辐射

### 2.1 这里的“laser”是应用结果，不是输入天线

`inputs_test_1d_fel` 里没有 `lasers.names = ...`。相反，它的核心结构是：

1. boosted frame
2. moving window
3. rigid injected `electrons` + `positrons`
4. 外加 undulator `B_y(z)`
5. `BackTransformed` + boosted-frame full diagnostics

关键输入是：

```text
particles.B_ext_particle_init_style = parse_B_ext_particle_function
particles.By_external_particle_function(x,y,z,t) = if( z>0, Bu*cos(k_u*z), 0 )
```

因此这个场景里，laser/辐射并不是通过 `LaserParticleContainer` 天线直接注入，而是：

- 束流在 undulator 外磁场中自发放大辐射
- diagnostics 再把这种辐射在 boosted 与 lab frame 中重构出来

这使它成为一类重要对照：同样讨论“激光/辐射”，但入口已经从 Laser 模块切到束流 + external particle field + BTD。

### 2.2 analysis 断言的是 FEL 增益与波长，而不是某个 writer 小功能

`analysis_fel.py` 会在 lab-frame diagnostics 上：

1. 提取 `E_x` 峰值沿 `z` 的增长
2. 对 `log(E^2)` 做线性拟合
3. 反推出 gain length `L_g`
4. 再通过 FFT 提取 radiation wavelength

然后在 boosted-frame diagnostics 上重复一次，并要求：

- gain length 相对误差小于 `15%`
- wavelength 相对误差小于 `1%`

这意味着 `free_electron_laser` 的最硬断言对象是：

1. boosted-frame 物理建模是否正确
2. BTD / boosted diagnostics 是否能保真重建 lab-frame radiation
3. external particle field 驱动的 undulator 问题是否给出正确的 FEL 标度

所以它虽然不走 `LaserParticleContainer`，却非常适合在书稿中放到 laser 相关应用章节里，作为“激光/辐射现象不一定来自激光天线输入”的重要反例。

## 3. `laser_on_fine`：这不是应用 physics test，而是 AMR/placement 边界测试

`laser_on_fine` 的 `CMakeLists.txt` 明确写的是：

```cmake
add_warpx_test(
    test_2d_laser_on_fine
    ...
    OFF
    "analysis_default_regression.py --path diags/diag1000050"
)
```

它没有独立 analysis，当前主要依赖 checksum。

输入里也能看出它的重点不在应用物理，而在 placement/mesh 边界：

1. `amr.max_level = 1`
2. 显式 `fine_tag_lo/fine_tag_hi`
3. `laser1.prob_lo/prob_hi`
4. `warpx.do_moving_window = 0`

这说明它更像在验证：

- 激光天线与 refined patch 的空间关系
- pml + AMR + antenna placement 的组合是否稳定

而不是在验证某个 downstream application observable。

因此在应用层谱系里，`laser_on_fine` 更适合作为“边界型/几何型对照例子”，提醒读者：

- 不是所有带 laser 的 examples 都是在讲物理应用；
- 有些 tests 本质上是在给 AMR placement 和 field solve 提供 checksum 基线。

## 4. 三组场景的角色对照

可以把这三组例子压成下表：

| 例子 | Laser 入口角色 | 主要联动模块 | 最硬断言对象 |
|---|---|---|---|
| `laser_ion` | 真正的 `GaussianLaser` 天线输入 | 靶等离子体、full/time-averaged/reduced diagnostics | time-averaged 与 instantaneous diagnostics 一致性 |
| `free_electron_laser` | 无 laser 天线；辐射由束流 + undulator 自发产生 | boosted frame、external particle field、BTD | FEL gain length 与 radiation wavelength |
| `laser_on_fine` | 真正的 laser 天线输入 | AMR patch、PML、placement | checksum 基线，主要是几何/求解稳定性 |

这张表有一个对书稿很重要的结论：

- “laser 应用”这个说法在 WarpX 里至少包含三种不同结构：
  1. 激光直接输入并驱动 plasma/target
  2. 外磁场驱动束流辐射，laser/辐射只是输出结果
  3. 激光输入本身作为 AMR/solver 组合的 placement test

## 5. 对当前 regression 索引最重要的改写方向

基于这轮源码与 examples 阅读，相关条目在索引里应避免三种误判：

1. 把 `laser_ion` 写成“验证 proton acceleration physics”。
   - 当前最硬断言实际上是 `diagTimeAvg` 与 `diagInst` 的一致性。
2. 把 `free_electron_laser` 写成普通 laser injection test。
   - 它根本不走 `lasers.names`，主链是 boosted rigid bunch + external particle field + BTD。
3. 把 `laser_on_fine` 写成应用场景。
   - 它更像 AMR/placement checksum test。

## 6. 对当前书稿最重要的结论

到这一层，Laser 模块已经不只是 profile 和天线注入本身，而是开始分叉成三条不同应用语义：

1. `laser_ion` 代表“laser 作为驱动器，diagnostics 作为主要观测合同”。
2. `free_electron_laser` 代表“辐射/laser 作为结果量，由束流与外场共同产生”。
3. `laser_on_fine` 代表“laser 作为几何/AMR placement 测试对象”。

这对整本书的结构有直接影响：后续“Laser 应用案例”章节不能只按 profile 分类，而应按“驱动器 / 结果量 / placement test”这三种角色重新组织。

## 7. `laser_acceleration`：这不是一组 laser-injection 单元测试，而是 LWFA workflow matrix

`Examples/Physics_applications/laser_acceleration/` 最容易被误写成 “laser injection/LPI examples”。当前本地 WarpX checkout 里，这个目录的真实边界更接近一套 `LWFA runtime matrix`：

1. `README.rst` 明确写的是 laser-wakefield acceleration 应用，但 `Analyze` 章节仍是 `TODO`；
2. 活跃 `CMakeLists.txt` 中绝大多数 tests 都是 `analysis = OFF`；
3. 目录里真正的强 analysis 只有 3 条：
   - `analysis_1d_fluid_boosted.py`
   - `analysis_refined_injection.py`
   - `analysis_openpmd_rz.py`
4. `plot_3d.py` 只是把 `Ey/rho` 画成 2-panel slice 的可视化 helper，不构成 regression 断言。

### 7.1 四个 `inputs_base_*` 本质上是在定义不同维度的运行骨架

- `inputs_base_1d`
  - 1D moving window
  - 连续电子注入
  - Gaussian laser antenna
  - `FieldProbe`
- `inputs_base_2d`
  - PML
  - moving window
  - level-1 refined patch
  - 连续背景电子
  - Gaussian `beam`
- `inputs_base_3d`
  - 3D moving window
  - openPMD Full diagnostics
  - 自定义粒子属性 `regionofinterest/initialenergy`
- `inputs_base_rz`
  - quasi-cylindrical `RZ`
  - `n_rz_azimuthal_modes = 2`
  - beam + plasma 共存
  - species 变量输出

也就是说，这些 base inputs 首先定义的是：

- moving window
- continuous injection
- laser antenna
- diagnostics
- 自定义 particle attributes

这条应用骨架，而不是某个单独的 laser 包络解析对照。

### 7.2 当前 active tests 真正区分的是 runtime path，不是统一的 physics observable

当前活跃变体可以压成 6 条路径：

1. 1D native / PICMI skeleton
   - `test_1d_laser_acceleration`
   - `test_1d_laser_acceleration_picmi`
2. 1D boosted fluid benchmark
   - `test_1d_laser_acceleration_fluid_boosted`
3. 2D boosted LWFA runtime path
   - `test_2d_laser_acceleration_boosted`
4. 2D MR / refined injection
   - `test_2d_laser_acceleration_mr`
   - `test_2d_laser_acceleration_mr_picmi`
   - `test_2d_refined_injection`
5. 3D native / PICMI / Python callback / single-precision communications
   - `test_3d_laser_acceleration`
   - `test_3d_laser_acceleration_picmi`
   - `test_3d_laser_acceleration_python`
   - `test_3d_laser_acceleration_single_precision_comms`
6. RZ plain / openPMD / PICMI
   - `test_rz_laser_acceleration`
   - `test_rz_laser_acceleration_opmd`
   - `test_rz_laser_acceleration_picmi`

因此这组 family 当前真正承担的是：

- LWFA workflow baseline
- boosted / MR / PICMI / Python / RZ / openPMD 的路径覆盖

而不是一套统一的 wake amplitude、dephasing length 或 beam-loading 解析 benchmark。

### 7.3 三条 analysis 的对象其实各不相同

- `analysis_1d_fluid_boosted.py`
  - 比的是 `Ez/Jz/rho/Vz`
  - 对照的是 ponderomotive-envelope fluid ODE 解
  - 真正验证的是 fluid WFA 模型
- `analysis_refined_injection.py`
  - 比的是 moving-window 连续注入后的总粒子数
  - 和 refinement-edge 前方 `rho` 的均匀性
  - 真正验证的是 `warpx.refine_plasma = 1`
- `analysis_openpmd_rz.py`
  - 比的是 openPMD+RZ 的 mesh shape
  - species ordering
  - `rho_<species>` 的物理中心位置
  - 真正验证的是 diagnostics 合同

所以这三条 analysis 不能再被统称成 “laser_acceleration 已有强 physics analysis”。

### 7.4 一个必须写进索引的边界：README 的 `Analyze` 仍是 `TODO`

这意味着当前目录虽然已经是成熟应用骨架，但并没有提供“目录级统一分析规范”。

因此在索引和正文里，必须把 `laser_acceleration` 写成：

- 大多数条目：application/runtime checksum baseline
- 少数条目：fluid theory / refined injection / RZ openPMD diagnostics 的局部强断言

而不能把整组目录误判成 laser injection 或 LWFA physics 的完整 benchmark suite。

## 8. `plasma_acceleration`：这不是 laser 天线回归，而是 PWFA workflow baseline

`Examples/Physics_applications/plasma_acceleration/` 很容易被误写成 “LWFA/PWFA application with diagnostics”。但当前本地 WarpX checkout 里，它的边界其实更窄，也更工程化：

1. `README.rst` 明确写的是 beam-driven wakefield acceleration，也就是 PWFA，不是 laser-driven LWFA；
2. 活跃 `CMakeLists.txt` 里的全部 tests 都是 `analysis = OFF`；
3. 目录里的 `analysis_default_regression.py` 只是本地 checksum helper，不提供 wakefield 物理 hard assert；
4. 这一组真正覆盖的是 moving window、boosted frame、rigid bunch、NCI correction、mesh refinement、hybrid grid 和 PICMI front-end 这些运行骨架能否稳定接通。

### 7.1 2D/3D 原生输入在验证哪条骨架

`inputs_base_2d` 和 `inputs_base_3d` 已经把这组应用的主语义分开了：

- 2D 基础骨架是：
  - `CKC`
  - PML
  - moving window
  - level-1 refined patch
  - Gaussian `driver/beam`
  - `plasma_e` 连续注入
- 3D 基础骨架是：
  - boosted frame
  - moving window
  - rigid-injected `driver/beam`
  - `driverback` backward propagation
  - `particles.use_fdtd_nci_corr = 1`
  - plasma density ramp

因此 `plasma_acceleration` 目录里的“主例子”并不是在解析验证 wake amplitude、dephasing length 或 beam-loading，而是在给一套典型 PWFA 工作流保留稳定输出基线。

### 7.2 active 变体真正区分的不是 physics observable，而是 runtime path

当前活跃变体可压成 5 条路径：

1. `test_1d_plasma_acceleration_picmi`
   - 1D PICMI 最小 wakefield skeleton
2. `test_2d_plasma_acceleration_boosted`
   - 2D boosted + rigid bunch + moving window
3. `test_2d_plasma_acceleration_mr` / `..._mr_momentum_conserving`
   - refined patch
   - 以及同一骨架下 `momentum-conserving` gather 分支
4. `test_3d_plasma_acceleration_boosted` / `..._boosted_hybrid`
   - 3D boosted 主骨架
   - 以及 `grid_type = hybrid` 的 Maxwell 路径
5. `test_3d_plasma_acceleration_picmi` / `..._mr_picmi`
   - 3D PICMI front-end
   - 以及 refined-region front-end

也就是说，这组 family 当前更像“PWFA application workflow matrix”，而不是“PWFA theory benchmark suite”。

### 7.3 一个必须写进索引的源码树边界

`README.rst` 里明确保留了：

- Python PICMI input file should use the boosted frame method
- like `inputs_test_3d_plasma_acceleration_boosted`
- but this is still TODO

因此：

- `inputs_test_3d_plasma_acceleration_boosted`
  是原生 boosted PWFA 骨架；
- `inputs_test_3d_plasma_acceleration_picmi.py`
  目前还不是它的等价 PICMI 前端；
- 只能诚实记成 non-boosted PICMI scaffold。

这条边界如果不写清，很容易把 “3D PICMI 版已经覆盖 boosted PWFA” 误当成已验证事实。

## 9. `plasma_mirror`：典型 laser-solid 场景，但当前只有 workflow checksum

`Examples/Physics_applications/plasma_mirror/` 代表的是另一类 laser 应用：不是稀薄等离子体中的加速或辐射，而是 laser-solid surface-plasma interaction。

但当前本地 WarpX checkout 里，它的 regression 证据层并不强：

1. `CMakeLists.txt` 里只有
   - `test_2d_plasma_mirror`
   - `analysis = OFF`
   - `analysis_default_regression.py --path diags/diag1000020`
2. 目录里没有独立 `analysis.py`
3. `README.rst` 的 Analyze/Visualize 仍是 `TODO`
4. 也还没有 PICMI 版输入

因此它现在不能被写成：

- plasma-mirror reflectivity benchmark
- high-harmonic-generation benchmark
- 或带实验对照的强 laser-solid regression

### 8.1 这组输入真正覆盖的是什么

`inputs_test_2d_plasma_mirror` 本体把以下几类对象绑在一起：

- 2D Gaussian laser antenna
- PML
- cubic particle shape
- field filter
- 电子/离子双 species
- 具有
  - front exponential ramp
  - overdense plateau
  - rear exponential ramp
  的 solid-density target
- full diagnostics

也就是说，这组例子当前真正覆盖的是：

- laser antenna 进入 dense-target/surface-plasma 场景
- parser density profile 对固体靶前后梯度的表达
- laser-solid 工作流在当前实现下的输出稳定性

### 8.2 这组 family 在应用谱系里的位置

和前面几组对照起来：

- `laser_ion`
  更像 `laser + diagnostics` 组合样板；
- `free_electron_laser`
  是束流 + external particle field 生成辐射；
- `plasma_acceleration`
  当前是 PWFA workflow matrix；
- `plasma_mirror`
  则是最小的 laser-solid surface-plasma checksum baseline。

因此它最准确的角色不是“验证 plasma-mirror 物理量”，而是：

- 给 laser-solid / overdense-target 这条应用骨架保留一个最小 native-input baseline。

## 10. 下一步最自然的工作

从这一层继续推进，最合理的下一步是：

1. 把 `docs/example-regression-map.md` 里的 `laser_ion`、`free_electron_laser`、`laser_on_fine` 相关条目改成上述更准确的断言口径。
2. 然后决定是继续沿 `laser_ion -> field_ionization / collisions / QED` 进入多物理主线，还是切到 `free_electron_laser -> rigid injection / BTD / external particle field` 继续向束流应用层展开。
