# FieldSolver 验证样例索引

绑定源码、示例和分析脚本：

- `../warpx/Examples/Tests/nci_fdtd_stability/`
- `../warpx/Examples/Tests/nci_psatd_stability/`
- `../warpx/Examples/Tests/electrostatic_sphere/`
- `../warpx/Examples/Tests/implicit/`
- `../warpx/Examples/Tests/ohm_solver_em_modes/`
- `../warpx/Examples/Tests/ohm_solver_ion_beam_instability/`
- `../warpx/Examples/Tests/ohm_solver_ion_Landau_damping/`
- `../warpx/Examples/Tests/ohm_solver_cylinder_compression/`
- `../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/`
- `../warpx/Docs/source/usage/examples.rst`

这一篇不是物理推导，而是给 FieldSolver 章节建立“源码讲解如何被测试覆盖”的索引。当前没有直接运行整套回归测试；这里先记录每组测试覆盖的 solver 路径、输入文件和 analysis 判据，后续可以据此选择小批量本地验证。

## 1. FDTD NCI corrector

目录：`../warpx/Examples/Tests/nci_fdtd_stability/`

覆盖模块：

- `particles.use_fdtd_nci_corr`
- FDTD boosted / drifting plasma 的数值 Cherenkov 抑制
- mesh refinement 版本的 corrector 行为

`CMakeLists.txt` 定义两个测试：

```cmake
add_warpx_test(
    test_2d_nci_corrector  # name
    2  # dims
    2  # nprocs
    inputs_test_2d_nci_corrector  # inputs
    "analysis_ncicorr.py diags/diag1000600"  # analysis
    "analysis_default_regression.py --path diags/diag1000600"  # checksum
    OFF  # dependency
)

add_warpx_test(
    test_2d_nci_corrector_mr  # name
    2  # dims
    2  # nprocs
    inputs_test_2d_nci_corrector_mr  # inputs
    "analysis_ncicorr.py diags/diag1000600"  # analysis
    "analysis_default_regression.py --path diags/diag1000600"  # checksum
    OFF  # dependency
)
```

代表性 input 其实是一个更具体的 2D drifting-plasma 骨架，而不只是“把 corrector 打开”：

```ini
warpx.use_filter = 1
algo.current_deposition = esirkepov
algo.particle_shape = 3
warpx.cfl = 1.0
warpx.do_subcycling = 1
particles.species_names = electrons ions
particles.use_fdtd_nci_corr = 1
electrons.uz_m = 1000.
ions.uz = 1000.
max_step = 600
```

`inputs_test_2d_nci_corrector` 只是在这个 base 上再次显式固定

```ini
amr.max_level = 0
particles.use_fdtd_nci_corr = 1
```

而 `inputs_test_2d_nci_corrector_mr` 则把它切到全域 refined 的 mesh-refinement 版本：

```ini
amr.max_level = 1
amr.n_cell = 64 64
warpx.fine_tag_hi =  20.e-6  20.e-6
warpx.fine_tag_lo = -20.e-6 -20.e-6
```

analysis 判据不是看单个场值，而是从最终 `Ex/Ez/By` 构造 NCI 场能代理并要求低于阈值：

```python
if use_MR:
    energy_corrector_off = 5.0e32
    energy_threshold = 1.0e28
else:
    energy_corrector_off = 1.5e26
    energy_threshold = 1.0e24

ex = ad0["boxlib", "Ex"].v
ez = ad0["boxlib", "Ez"].v
by = ad0["boxlib", "By"].v
energy = np.sum(ex**2 + ez**2 + scc.c**2 * by**2)

assert energy < energy_threshold
```

这里要单独记一个当前源码树边界：`analysis_ncicorr.py` 用

```python
use_MR = re.search("nci_correctorMR", fn) is not None
```

来区分 MR/non-MR，但当前 `CMakeLists.txt` 给两条活跃测试传入的 analysis 参数都写成 `diags/diag1000600`。因此，从可见测试注册层看，MR 阈值分支并没有被单独显式选通。保守表述应是：

- non-MR 路径的 `1e24` 阈值是当前活跃注册直接可见的强断言；
- MR 版本的目标显然是“mesh refinement 下同样抑制 NCI”，但 `1e28` 阈值分支目前更像 analysis 脚本里预留的路径区分逻辑，而不是从注册参数层就能直接证实的独立入口。

所以这组测试主要验证“FDTD NCI corrector 抑制了 boosted/drifting-plasma 场景中的非物理场能量增长”，而 MR 变体当前应按“目标明确、参数层区分尚不完全显式”的边界来记录。

## 2. PSATD NCI / Galilean / JRhom

目录：`../warpx/Examples/Tests/nci_psatd_stability/`

覆盖模块：

- `SpectralSolver/`
- Galilean PSATD
- current correction
- averaged Galilean PSATD
- hybrid grid PSATD
- JRhom 一阶/二阶源项时间依赖
- RZ PSATD

这些测试只有在 `WarpX_FFT` 打开时加入：

```cmake
if(WarpX_FFT)
    add_warpx_test(
        test_2d_galilean_psatd_current_correction  # name
        2  # dims
        2  # nprocs
        inputs_test_2d_galilean_psatd_current_correction  # inputs
        "analysis_galilean.py diags/diag1000400"  # analysis
        "analysis_default_regression.py --path diags/diag1000400 --rtol 1e-8"  # checksum
        OFF  # dependency
    )
endif()
```

JRhom 覆盖包括 3D 和 RZ：

```cmake
add_warpx_test(
    test_3d_uniform_plasma_psatd_JRhom_CC1  # name
    3  # dims
    2  # nprocs
    inputs_test_3d_uniform_plasma_psatd_JRhom_CC1  # inputs
    "analysis_psatd_CC1.py diags/diag1000300"  # analysis
    "analysis_default_regression.py --path diags/diag1000300"  # checksum
    OFF  # dependency
)

add_warpx_test(
    test_rz_psatd_JRhom_LL2  # name
    RZ  # dims
    2  # nprocs
    inputs_test_rz_psatd_JRhom_LL2  # inputs
    OFF  # analysis
    "analysis_default_regression.py --path diags/diag1000025"  # checksum
    OFF  # dependency
)
```

代表性 input 中直接设置：

```ini
diag1.fields_to_plot = Bx By Bz divE Ex Ey Ez F G jx jy jz rho
psatd.JRhom = "CC1"
```

这里要单独记一条边界：`test_3d_uniform_plasma_psatd_JRhom_CC1` 虽然名字里带 `uniform_plasma`，但它并不属于 `Examples/Physics_applications/uniform_plasma/` 那组“并行噪声 + writer/checkpoint 基线”。它实际属于 `nci_psatd_stability` 的 PSATD 稳定性回归，analysis 也不是检查温度噪声或粒子统计，而是用 `analysis_psatd_CC1.py` 直接比较最终电场能量相对一个已知不稳定参考值的比例是否足够小，从而验证：

- `psatd.JRhom = CC1`
- `warpx.do_divb_cleaning = 1`
- `warpx.do_dive_cleaning = 1`

这组组合是否能把 NCI 压到参考能量以下。

同一目录里其余 active PSATD tests 现在也应分成三层，而不再混成一个 “PSATD / spectral solver” 桶：

1. `analysis_galilean.py` 族
   - 覆盖 2D / 3D / RZ
   - 覆盖普通 Galilean、`current_correction`、`current_correction + periodic_single_box_fft`
   - 以及 averaged Galilean 与其 hybrid-grid 版本
   - 共同判据是：最终电场能量相对已知不稳定参考值必须足够小；若打开 `current_correction`，还要额外检查 `divE-rho/eps0` 误差
2. `analysis_psatd_CC1.py`
   - 只覆盖 `test_3d_uniform_plasma_psatd_JRhom_CC1`
   - 重点是 `JRhom = CC1 + divergence cleaning` 的 NCI 抑制
3. checksum-only 族
   - `test_2d_comoving_psatd_hybrid`
   - `test_2d_galilean_psatd_hybrid`
   - `test_rz_psatd_JRhom_LL2`
   当前都没有独立 analysis，应诚实记成工作流/输出基线，而不是强稳定性断言

这组测试对应第 6 章 PSATD 相关小节：普通/Galilean PSATD、current correction、hybrid grid、RZ 和 JRhom。

### 2.1 用 Birdsall 读 `nci_psatd_stability`

如果把 Birdsall Chapter 8、9、12 接进来，这组 tests 的物理边界可以写得更准确：

1. Chapter 8
   - 这里检查的不是抽象“谱求解器是否高级”，而是 alias branches 是否被压回足够低的能量水平。
2. Chapter 9
   - 对 Galilean / averaged Galilean / JRhom 来说，analysis 脚本里直接盯最终电场能量，就是在监控是否还存在会继续喂大 nonphysical growth 的时间/空间 branch coupling。
3. Chapter 12
   - 这些 tests 本质上不是在看单个 mode 的漂亮图像，而是在看一个不稳定参考问题的 fluctuation energy 是否被成功压低；这和 `(\rho^2)_{k,\omega}`、field-energy density 以及非物理增热风险是一条线上的观测量。

因此：

- `analysis_galilean.py`
  - 应理解为 NCI field-energy suppression probe
- `analysis_psatd_CC1.py`
  - 应理解为 `JRhom + divergence cleaning` 的 unstable-energy suppression probe

而不是把它们都笼统写成“电场能量比参考值小”这么机械的脚本说明。

## 3. Maxwell hybrid QED

目录：`../warpx/Examples/Tests/maxwell_hybrid_qed/`

覆盖模块：

- `warpx.use_hybrid_QED`
- `warpx.quantum_xi`
- `PushPSATD()` 中的 hybrid-QED 真空修正
- collocated PSATD 下的外加 `E/B` 初值传播

`CMakeLists.txt` 里这组只有在 `WarpX_FFT` 打开时加入：

```cmake
if(WarpX_FFT)
    add_warpx_test(
        test_2d_maxwell_hybrid_qed_solver  # name
        2  # dims
        2  # nprocs
        inputs_test_2d_maxwell_hybrid_qed_solver  # inputs
        "analysis.py diags/diag1000300"  # analysis
        "analysis_default_regression.py --path diags/diag1000300"  # checksum
        OFF  # dependency
    )
endif()
```

代表性 input 不是粒子 QED 事件，而是一个纯 field-solver 基准：

```ini
warpx.grid_type = collocated
algo.maxwell_solver = psatd
warpx.use_hybrid_QED = 1
warpx.quantum_xi = 1.e-23

warpx.E_ext_grid_init_style = parse_E_ext_grid_function
warpx.Ey_external_grid_function(x,y,z) = "exp(-z**2/L**2)*cos(2*pi*z/wavelength) + Es"

warpx.B_ext_grid_init_style = parse_B_ext_grid_function
warpx.Bx_external_grid_function(x,y,z)= "-sqrt((1+(12*xi*Es**2)/epsilon0)/(1+(4*xi*Es**2)/epsilon0))*exp(-z**2/L**2)*cos(2*pi*z/wavelength)/clight"
```

analysis 判据也不是 photon emission / pair production，而是测脉冲相速度：

```python
EyQED = EyQED_2d[EyQED_2d.shape[0] // 2, :]
z_end = dsQED.domain_left_edge[1].v + np.argmax(EyQED) * dz
phase_velocity_pic = (z_end - z_start) / dsQED.current_time.v
phase_velocity_theory = scc.c / np.sqrt(
    (1.0 + 12.0 * xi * Es**2 / scc.epsilon_0) / (1.0 + 4.0 * xi * Es**2 / scc.epsilon_0)
)
error_percent = (
    100.0 * np.abs(phase_velocity_pic - phase_velocity_theory) / phase_velocity_theory
)
assert error_percent < 1.25
```

也就是说，这条 regression 真正验证的是：

- hybrid-QED 真空修正打开后，
- 在静态背景场 `Es` 上传播的平面波包，
- 是否产生了与理论色散关系一致的相速度偏移。

它更接近“Maxwell solver with vacuum-polarization correction”的基准，而不是第 4 章那类粒子 QED 事件回归。

同时也要记一条 helper 边界：目录里的 `analysis_default_regression.py` 是本地 checksum helper 副本，职责与顶层 `Examples/analysis_default_regression.py` 一样，只负责输出比较，不提供 hybrid-QED 的物理定义断言。

## 4. Electrostatic sphere

目录：`../warpx/Examples/Tests/electrostatic_sphere/`

覆盖模块：

- lab-frame electrostatic Poisson
- relativistic electrostatic self fields
- adaptive / mesh-refined variants
- RZ electrostatic
- uniform weighting 变体

`CMakeLists.txt` 中核心测试包括：

```cmake
add_warpx_test(
    test_3d_electrostatic_sphere_lab_frame  # name
    3  # dims
    2  # nprocs
    inputs_test_3d_electrostatic_sphere_lab_frame  # inputs
    "analysis_electrostatic_sphere.py diags/diag1000030"  # analysis
    "analysis_default_regression.py --path diags/diag1000030"  # checksum
    OFF  # dependency
)

add_warpx_test(
    test_rz_electrostatic_sphere  # name
    RZ  # dims
    2  # nprocs
    inputs_test_rz_electrostatic_sphere  # inputs
    "analysis_electrostatic_sphere.py diags/diag1000030"  # analysis
    "analysis_default_regression.py --path diags/diag1000030"  # checksum
    OFF  # dependency
)
```

代表性 input：

```ini
warpx.do_electrostatic = labframe
```

analysis 脚本验证带电球膨胀的解析解和电场解：

```python
def E_exact(r):
    return np.sign(r) * (
        q_tot / (4 * pi * epsilon_0 * r**2) * (abs(r) >= r_end)
        + q_tot * abs(r) / (4 * pi * epsilon_0 * r_end**3) * (abs(r) < r_end)
    )
```

这组测试是 `06-field-solvers.md` 的 electrostatic / Poisson 路径的主要端到端验证。

## 5. Implicit EM solver

目录：`../warpx/Examples/Tests/implicit/`

覆盖模块：

- `theta_implicit_em`
- `semi_implicit_em`
- Picard nonlinear solver
- Newton / JFNK
- PETSc curl-curl preconditioner
- mass matrices
- Strang implicit spectral EM

基本 Picard 能量守恒测试：

```cmake
add_warpx_test(
    test_1d_theta_implicit_picard  # name
    1  # dims
    2  # nprocs
    inputs_test_1d_theta_implicit_picard  # inputs
    "analysis_1d.py"  # analysis
    "analysis_default_regression.py --path diags/diag1000100"  # checksum
    OFF  # dependency
)
```

PETSc 相关测试受 `AMReX_PETSC` 条件保护：

```cmake
if(AMReX_PETSC)
    add_warpx_test(
        test_2d_curl_curl_petsc_pc  # name
        2  # dims
        2  # nprocs
        inputs_test_2d_curl_curl_petsc_pc  # inputs
        "analysis_petsc_matrix.py diags/diag1000200"  # analysis
        "analysis_default_regression.py --path diags/diag1000200"  # checksum
        OFF  # dependency
    )
endif()
```

这里最硬的不是 plotfile 场值本身，而是 `analysis_petsc_matrix.py` 对求解器结构的直接断言：

```python
assert total_gmres_iters == num_steps
assert total_newton_iters == num_steps
```

也就是说，这组三测

- `test_2d_curl_curl_petsc_pc`
- `test_rz_curl_curl_petsc_pc`
- `test_rcylinder_curl_curl_petsc_pc`

真正验证的是：当 `jacobian.pc_type = pc_petsc` 且 `pc_petsc.type = lu` 时，`MatrixPC`、`WarpXSolverDOF` 和 PETSc bridge 装配出来的精确预条件器足以让每个时间步只需要 `1` 次 Newton 和 `1` 次 GMRES。

代表性 input：

```ini
algo.evolve_scheme = theta_implicit_em
implicit_evolve.nonlinear_solver = "picard"
algo.current_deposition = esirkepov
algo.field_gathering = energy-conserving
```

`analysis_1d.py` 的判据是总能量相对变化：

```python
total_energy = field_energy[:, 2] + particle_energy[:, 2]
delta_E = (total_energy - total_energy[0]) / total_energy[0]
max_delta_E = np.abs(delta_E).max()

assert max_delta_E < tolerance_rel
```

这组测试直接对应 `ImplicitSolvers/` 与 `NonlinearSolvers/` 的章节。

## 6. Ohm solver / Hybrid PIC tests

目录：

- `../warpx/Examples/Tests/ohm_solver_em_modes/`
- `../warpx/Examples/Tests/ohm_solver_ion_beam_instability/`
- `../warpx/Examples/Tests/ohm_solver_ion_Landau_damping/`
- `../warpx/Examples/Tests/ohm_solver_cylinder_compression/`
- `../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/`

这些测试对应 `HybridPICModel` 和 `HybridPICSolveE.cpp`。

EM modes 测试：

```cmake
add_warpx_test(
    test_1d_ohm_solver_em_modes_picmi  # name
    1  # dims
    2  # nprocs
    "inputs_test_1d_ohm_solver_em_modes_picmi.py --test --dim 1 --bdir z"  # inputs
    "analysis.py"  # analysis
    "analysis_default_regression.py --path diags/field_diag000250"  # checksum
    OFF  # dependency
)
```

ion beam、Landau damping、cylinder compression 和 reconnection 覆盖不同 hybrid 物理情形：

```cmake
add_warpx_test(
    test_2d_ohm_solver_magnetic_reconnection_picmi  # name
    2  # dims
    2  # nprocs
    "inputs_test_2d_ohm_solver_magnetic_reconnection_picmi.py --test"  # inputs
    "analysis.py"  # analysis
    "analysis_default_regression.py --path diags/diag1000020"  # checksum
    OFF  # dependency
)
```

`ohm_solver_em_modes/analysis.py` 从 reduced field probe 读数据，做时空 FFT 并和解析色散关系比较：

```python
def get_analytic_R_mode(w):
    return w / np.sqrt(1.0 + abs(w))

def get_analytic_L_mode(w):
    return w / np.sqrt(1.0 - abs(w))
```

因此这组测试不能只记成“程序能跑”，但也不能笼统写成“全部都有强物理断言”。

更准确的分层应是：

- `ohm_solver_em_modes/analysis_rz.py`
  - 对 Hankel-Fourier 频谱的四个固定采样点做显式 `assert`
  - 属于脚本级强回归
- `ohm_solver_ion_beam_instability/analysis.py`
  - 对 `m=4,5,6` 模增长率拟合后的 RMS error 做显式 `assert`
  - 属于脚本级强回归
- `ohm_solver_em_modes/analysis.py`
  - 只画 Cartesian parallel/perpendicular EM mode 谱图
  - 没有 `assert`
  - 自动化主要依赖 checksum
- `ohm_solver_ion_Landau_damping/analysis.py`
  - 只把衰减曲线与理论指数衰减画在一起
  - 没有 `assert`
  - 自动化主要依赖 checksum
- `ohm_solver_magnetic_reconnection/analysis.py`
  - 只画平均重联率与可选动画
  - 没有 `assert`
  - 自动化主要依赖 checksum
- `ohm_solver_cylinder_compression`
  - `analysis=OFF`
  - 只有 checksum

所以 Hybrid Ohm solver 这组更适合写成：

- 有硬断言的 normal-mode / instability regression
- 加上 Landau damping / reconnection / cylinder compression 这类物理图像或应用级输出回归

而不是一句话把它们全都并成同等级“benchmark”。

## 7. 后续本地验证建议

由于这组测试跨 MPI、FFT、PETSc、PICMI Python 和 slow 标签，建议分三层执行：

1. 轻量检查：只解析 input / CMake / analysis，确认章节引用的参数和判据存在。
2. 小规模运行：选择 `test_2d_nci_corrector`、`test_3d_electrostatic_sphere_lab_frame`、`test_1d_theta_implicit_picard`、`test_1d_ohm_solver_em_modes_picmi`。
3. 条件运行：在确认本地 WarpX 构建启用 `WarpX_FFT` 和 `AMReX_PETSC` 后，再运行 PSATD 和 PETSc 相关测试。

本索引目前只完成第 1 层，后续要把实际运行命令、输出路径、analysis 结果和失败原因继续追加到本文件。

## 8. `divb_cleaning` 与 `dive_cleaning` 的验证合同不同

当前本地 regressions 里，这两组 cleaning test 不应再共用一个粗分类桶。

`Examples/Tests/divb_cleaning/analysis.py` 读取连续三个输出时刻的 `divB` 与辅助标量 `G`，直接检查离散 hyperbolic-cleaning 关系

$$
c^2 \nabla \cdot \mathbf{B} \approx \frac{\partial G}{\partial t}.
$$

因此 `divb_cleaning` 更准确地应归到：

- `field solver / div(B) cleaning`

而不是一般的“待分类”条目。

`Examples/Tests/dive_cleaning/analysis.py` 则不是看 cleaning 标量本身，而是把最终 `Ex/Ey/Ez` 与高斯电荷团理论 Coulomb 场直接比较，验证：

1. 初始不一致 `div(E)-rho/\epsilon_0` 误差被 hyperbolic cleaning 激发；
2. 误差随后被 PML 传播并吸收；
3. 最终场回到正确物理解。

所以 `dive_cleaning` 更准确地应归到：

- `field solver / div(E) cleaning / PML`

它和初始化阶段的 `ProjectionDivCleaner` 不是一回事。
