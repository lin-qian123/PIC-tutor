# FieldSolver regression analysis 判据精读

绑定源码与脚本：

- `../warpx/Examples/Tests/nci_fdtd_stability/analysis_ncicorr.py`
- `../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py`
- `../warpx/Examples/Tests/electrostatic_sphere/analysis_electrostatic_sphere.py`
- `../warpx/Examples/Tests/implicit/analysis_*.py`
- `../warpx/Examples/Tests/ohm_solver_*/analysis*.py`
- 对应实现：`../warpx/Source/FieldSolver/FiniteDifferenceSolver/`、`../warpx/Source/FieldSolver/SpectralSolver/`、`../warpx/Source/FieldSolver/ElectrostaticSolvers/`、`../warpx/Source/FieldSolver/ImplicitSolvers/`、`../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/`

这篇笔记接在 `13-fieldsolver-verification-map.md` 后面。前一篇解决“哪些测试覆盖 FieldSolver”；本篇解决“这些测试实际用什么物理量判定通过”。当前仍是源码/脚本精读，不表示已经在本机跑完这些 regression。

## 1. 判据分层：analysis assert 与 checksum 不等价

WarpX 的 Examples tests 通常有两层验证：

1. `analysis*.py`：脚本内显式计算物理/数值量并 `assert`，例如能量增长、Gauss law 误差、解析场 L2 误差、Newton/GMRES 迭代数。
2. `analysis_default_regression.py --path ...`：checksum 回归，比较 plotfile 或 openPMD 输出的字段/粒子统计量。它能发现数值输出漂移，但它本身不解释漂移对应哪个物理守恒律。

因此本书写验证时应优先引用 `analysis*.py` 的物理量；对于只有 checksum 或只画图的脚本，需要写明“这是输出回归或可视化线索，不是独立物理判据”。

## 2. NCI FDTD：用 EB 场能增长检验 corrector

脚本：`../warpx/Examples/Tests/nci_fdtd_stability/analysis_ncicorr.py:20-47`。

源码核心片段：

```python
fn = sys.argv[1]
use_MR = re.search("nci_correctorMR", fn) is not None

if use_MR:
    energy_corrector_off = 5.0e32
    energy_threshold = 1.0e28
else:
    energy_corrector_off = 1.5e26
    energy_threshold = 1.0e24

ds = yt.load(filename)
ad0 = ds.covering_grid(
    level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions
)
ex = ad0["boxlib", "Ex"].v
ez = ad0["boxlib", "Ez"].v
by = ad0["boxlib", "By"].v
energy = np.sum(ex**2 + ez**2 + scc.c**2 * by**2)

assert energy < energy_threshold
```

物理意义：

- NCI 是 relativistic drift plasma 中的数值 Cherenkov 不稳定性。它会把场能推高，尤其在 `E_x/E_z/B_y` 这些与漂移和 Yee 色散耦合的分量上明显。
- 这里不计算绝对电磁能量密度的 SI 归一化，而用

$$
\mathcal E_{\mathrm{diag}}=\sum_{\mathrm{grid}}\left(E_x^2+E_z^2+c^2B_y^2\right)
$$

作为增长指示量。若 corrector 关闭，基准场能会达到 `1.5e26` 或 MR 情况下 `5.0e32` 的量级；测试要求 corrector 开启后低于 `1.0e24` 或 `1.0e28`。

对应源码覆盖：

- FDTD 更新：`FiniteDifferenceSolver/EvolveE.cpp`、`EvolveB.cpp`。
- NCI corrector 参数与分支需要继续回到 `WarpX.cpp` 与相关 finite-difference / filtering 代码确认。本篇只记录脚本判据。

## 3. NCI PSATD：用电场能量比与 Gauss law 检验 Galilean/current correction

脚本：`../warpx/Examples/Tests/nci_psatd_stability/analysis_galilean.py:27-116`。

源码核心片段：

```python
with open("./warpx_used_inputs", "r") as f:
    warpx_used_inputs = f.read()
if re.search("geometry.dims\s*=\s*2", warpx_used_inputs):
    dims = "2D"
elif re.search("geometry.dims\s*=\s*RZ", warpx_used_inputs):
    dims = "RZ"
elif re.search("geometry.dims\s*=\s*3", warpx_used_inputs):
    dims = "3D"
if re.search("psatd.current_correction\s*=\s*1", warpx_used_inputs):
    current_correction = True
if re.search("psatd.do_time_averaging\s*=\s*1", warpx_used_inputs):
    time_averaging = True

energy = np.sum(scc.epsilon_0 / 2 * (Ex**2 + Ey**2 + Ez**2))
err_energy = energy / energy_ref
assert err_energy < tol_energy

if current_correction:
    divE = all_data["boxlib", "divE"].squeeze().v
    rho = all_data["boxlib", "rho"].squeeze().v / scc.epsilon_0
    err_charge = np.amax(np.abs(divE - rho)) / max(np.amax(divE), np.amax(rho))
    assert err_charge < tol_charge
```

物理意义：

- `energy_ref` 是用“不稳定配置”得到的参考电场能量：Galilean 测试对应 `psatd.v_galilean=(0,0,0)`，averaging 测试对应关闭 time averaging。通过条件是

$$
\frac{\sum \epsilon_0 |\mathbf E|^2/2}{\mathcal E_{\mathrm{NCI,ref}}}<\mathrm{tol}_{E}.
$$

- `current_correction` 打开时还检查谱空间电流校正是否维持离散 Gauss law：

$$
\epsilon_0\nabla\cdot\mathbf E=\rho,
\qquad
\epsilon_{\rho}=
\frac{\|\nabla\cdot\mathbf E-\rho/\epsilon_0\|_{\infty}}
{\max(\|\nabla\cdot\mathbf E\|_{\infty},\|\rho/\epsilon_0\|_{\infty})}.
$$

脚本中的容差随维度和 FFT 模式改变：

- 默认 `tol_energy=1e-8`，`tol_charge=1e-9`。
- 2D 非 single-box current correction：`tol_energy=2e-8`，`tol_charge=2e-4`。
- 2D time averaging：`tol_energy=1e-6`。
- RZ 非 single-box current correction：`tol_charge=3e-4`。
- 3D 非 single-box current correction：`tol_charge=1e-2`。
- 3D time averaging：`tol_energy=1e-4`。

对应源码覆盖：

- `SpectralAlgorithms/PsatdAlgorithmGalilean.cpp` 的 `C/S_ck/T2/X1-X4` 系数与 `v_galilean`。
- `SpectralBaseAlgorithm.H` / PSATD current correction 分支。
- RZ case 还覆盖 `SpectralSolverRZ.cpp`、`PsatdAlgorithmGalileanRZ.cpp`。

## 4. 静电球：解析展开半径、电场 L2 和势能-动能守恒

脚本：`../warpx/Examples/Tests/electrostatic_sphere/analysis_electrostatic_sphere.py:10-211`。

解析模型源码：

```python
# The solution r(t) solves the ODE: r''(t) = a/(r(t)**2) with initial conditions
# r(0) = r_0, r'(0) = 0, and a = q_e*q_tot/(4*pi*epsilon_0*e_mass)
def v_exact(r):
    return np.sqrt(q_e * q_tot / (2 * pi * e_mass * epsilon_0) * (1 / r_0 - 1 / r))

def t_exact(r):
    return np.sqrt(r_0**3 * 2 * pi * e_mass * epsilon_0 / (q_e * q_tot)) * (
        np.sqrt(r / r_0 - 1) * np.sqrt(r / r_0)
        + np.log(np.sqrt(r / r_0 - 1) + np.sqrt(r / r_0))
    )

r_end = fsolve(func, r_0)[0]

def E_exact(r):
    return np.sign(r) * (
        q_tot / (4 * pi * epsilon_0 * r**2) * (abs(r) >= r_end)
        + q_tot * abs(r) / (4 * pi * epsilon_0 * r_end**3) * (abs(r) < r_end)
    )
```

判据源码：

```python
L2_error = np.sqrt(sum((E_exact_grid - E_grid) ** 2)) / np.sqrt(
    sum((E_exact_grid) ** 2)
)

assert L2_error_x < l2_tolerance
assert L2_error_y < l2_tolerance
assert L2_error_z < l2_tolerance

if "phi" in ts.avail_record_components["electron"]:
    assert Ep_f < 0.7 * Ep_i
    assert abs((Ek_i + Ep_i) - (Ek_f + Ep_f)) < energy_fraction * (
        Ek_i + Ep_i
    )
```

物理推导要点：

- 初始为均匀带电电子球，半径 `r_0=0.1`，总电荷 `q_tot=-1e-15 C`。球壳按库仑斥力自相似展开。
- 半径满足

$$
\ddot r=\frac{a}{r^2},
\qquad
a=\frac{q_e q_{\mathrm{tot}}}{4\pi\epsilon_0 m_e}.
$$

两边乘以 $\dot r$ 并积分得到

$$
v(r)^2=\frac{q_e q_{\mathrm{tot}}}{2\pi m_e\epsilon_0}
\left(\frac{1}{r_0}-\frac{1}{r}\right),
$$

脚本中的 `v_exact(r)` 正是这一式。再由 $dt=dr/v(r)$ 积分得到 `t_exact(r)`，用 `fsolve` 反求终止时刻的 `r_end`。

- 电场是均匀球的解析库仑场：

$$
E_r(r)=
\begin{cases}
\dfrac{q_{\mathrm{tot}}}{4\pi\epsilon_0}\dfrac{r}{r_{\mathrm{end}}^3},& |r|<r_{\mathrm{end}},\\
\dfrac{q_{\mathrm{tot}}}{4\pi\epsilon_0}\dfrac{1}{r^2}\operatorname{sign}(r),& |r|\ge r_{\mathrm{end}}.
\end{cases}
$$

判据：

- 普通 case：三轴电场相对 L2 误差 `< 0.05`。
- `emass_10` case：`< 0.096`。
- 若 openPMD 粒子诊断含 `phi`，还要求势能显著释放 `Ep_f < 0.7 Ep_i`，并要求总能量相对漂移小于 `0.0032`，`uniform_weighting` 放宽到 `0.012`。

对应源码覆盖：

- `ElectrostaticSolvers/ElectrostaticSolver.cpp`。
- `LabFrameExplicitES.cpp`、`RelativisticExplicitES.cpp`、`EffectivePotentialES.cpp`。
- Poisson 边界处理：`PoissonBoundaryHandler.cpp`。

## 5. 隐式 EM：总能量、Gauss law、Newton/GMRES 迭代数

隐式场求解 regression 的共同逻辑是：如果 theta-implicit、semi-implicit、JFNK、PETSc matrix/preconditioner 组合正确，能量漂移、Gauss law 残差和线性/非线性迭代数应落在非常小的阈值内。

### 5.1 1D Picard 隐式周期等离子体

脚本：`../warpx/Examples/Tests/implicit/analysis_1d.py:17-35`。

```python
field_energy = np.loadtxt("diags/reducedfiles/field_energy.txt", skiprows=1)
particle_energy = np.loadtxt("diags/reducedfiles/particle_energy.txt", skiprows=1)

total_energy = field_energy[:, 2] + particle_energy[:, 2]
delta_E = (total_energy - total_energy[0]) / total_energy[0]
max_delta_E = np.abs(delta_E).max()

if re.match("test_1d_semi_implicit_picard", test_name):
    tolerance_rel = 2.5e-5
elif re.match("test_1d_theta_implicit_picard", test_name):
    tolerance_rel = 1.0e-14

assert max_delta_E < tolerance_rel
```

`theta_implicit_picard` 被期望接近机器精度守恒；`semi_implicit_picard` 是更弱的近似能量守恒，容差放宽到 `2.5e-5`。

### 5.2 Exactly energy-conserving implicit EM

脚本：`../warpx/Examples/Tests/implicit/analysis_implicit.py:19-66`。

```python
total_energy = field_energy[:, 2] + particle_energy[:, 2]
delta_E = (total_energy - total_energy[0]) / total_energy[0]
max_delta_E = np.abs(delta_E).max()

tolerance_rel_energy = 2.0e-14
tolerance_rel_charge = 2.0e-14
assert max_delta_E < tolerance_rel_energy

drho = (rho - epsilon_0 * divE) / e / ne0
drho2_avg = (drho**2).sum() / (nX * nY * nZ)
drho_rms = np.sqrt(drho2_avg)
assert drho_rms < tolerance_rel_charge
```

这里的 charge check 是归一化 Gauss law RMS：

$$
\epsilon_{\mathrm{Gauss,rms}}
=
\left[
\frac{1}{N}\sum_{\mathbf i}
\left(
\frac{\rho_{\mathbf i}-\epsilon_0(\nabla\cdot \mathbf E)_{\mathbf i}}
{e n_{e0}}
\right)^2
\right]^{1/2}
<2\times10^{-14}.
$$

### 5.3 Planar pinch 与 preconditioner 效率

脚本：`../warpx/Examples/Tests/implicit/analysis_planar_pinch.py:19-94`。

```python
dE = Efields + Eplasma + dE_poynting
rel_net_energy = np.abs(dE - dE[0]) / Eplasma
max_rel_net_energy = rel_net_energy.max()
rel_net_energy_tol = 1.0e-12
assert max_rel_net_energy < rel_net_energy_tol

assert total_gmres_iters / total_newton_iters < gmres_iters_tol
assert total_newton_iters / num_steps < newton_iters_tol

drho = (rho - epsilon_0 * divE) / e / n0
drho_trimmed = drho[:-1, ...]
drho_rms = np.sqrt((drho_trimmed**2).sum() / drho_trimmed.size)
assert drho_rms < tolerance_rel_charge
```

物理意义：

- planar pinch 有边界能流，不能只看场能+粒子能，必须加上 `poynting_flux` 记录的边界流出/流入。
- 1D 的 `gmres_iters_tol=10`，2D 的 `gmres_iters_tol=5`；Newton 平均迭代数 `<5`。
- Gauss law RMS 容差 `1e-12`。

### 5.4 PETSc matrix 精确预条件器

脚本：`../warpx/Examples/Tests/implicit/analysis_petsc_matrix.py:18-28`。

```python
newton_solver = np.loadtxt("diags/reduced_files/newton_solver.txt", skiprows=1)
num_steps = newton_solver[-1, 0]
total_newton_iters = newton_solver[-1, 3]
total_gmres_iters = newton_solver[-1, 7]

assert total_gmres_iters == num_steps
assert total_newton_iters == num_steps
```

这不是物理守恒判据，而是 solver 结构判据：当 PETSc LU 作为精确求解器/预条件器时，每个时间步应只需要 1 次 Newton 和 1 次 GMRES。它主要验证 matrix assembly、DOF 映射和 PETSc 桥接没有错位。

对应源码覆盖：

- `ImplicitSolvers/ThetaImplicitEM.*`、`SemiImplicitEM.*`、`StrangImplicitSpectralEM.*`。
- `ImplicitSolvers/WarpXSolverVec.H`、`WarpXSolverDOF.H`。
- `NonlinearSolvers/NewtonSolver.H`、`PicardSolver.H`、`WarpX_PETSc.cpp`、`MatrixPC.H`、`CurlCurlMLMGPC.H`。

## 6. Hybrid Ohm solver：色散谱、增长率、阻尼率、重联率

Hybrid Ohm solver 的 regression 分为两类：一类带 explicit assert，另一类主要输出物理图像并依靠 checksum。

### 6.1 RZ EM normal modes：Hankel-Fourier 谱采样

脚本：`../warpx/Examples/Tests/ohm_solver_em_modes/analysis_rz.py:27-183`。

```python
def transform_spatially(data_for_transform):
    interp = RegularGridInterpolator(
        (info.z, info.r), data_for_transform, method="linear"
    )
    data_interp = interp((zg, rg))

    Fmz = np.einsum("ijkl,kl->ij", proj, data_interp)
    Fmn = fft.fftshift(fft.fft(Fmz, axis=1), axes=1)
    return Fmn

F_kw = fft.fftshift(fft.fft(results, axis=0), axes=0)

amps = np.abs(F_kw[2, 1, len(kz) // 2 - 2 : len(kz) // 2 + 2])
assert np.allclose(
    amps, np.array([55.65891974, 31.29213566, 70.13683876, 15.395433])
)
```

这里的物理对象是柱坐标 normal modes：先沿径向用 Bessel roots 构造手动 Hankel 投影，再沿 z 和时间做 Fourier transform，得到 $E_\theta(k_z,m,\omega)$。脚本画出 fast/slow branch 和热共振线；显式 assert 只抽取谱上四个固定采样点与历史数值匹配，因此更接近“谱结构回归”而不是完整色散关系拟合。

### 6.2 Cartesian EM modes：谱图为主，checksum 为自动判据

脚本：`../warpx/Examples/Tests/ohm_solver_em_modes/analysis.py`。

该脚本读取 `par_field_data.txt` 或 `perp_field_data.txt`，对 `B_L=(B_x+iB_y)/sqrt(2)` 或 `E_z` 做二维 FFT，画出 parallel R/L mode 或 perpendicular X/Bernstein mode：

```python
if sim.B_dir == "z":
    Bl = (data[:, :, 0] + 1.0j * data[:, :, 1]) / np.sqrt(2.0)
    field_kw = np.fft.fftshift(np.fft.fft2(Bl))
else:
    field_kw = np.fft.fftshift(np.fft.fft2(data[:, :, 2]))
```

但这个脚本没有 `assert`。CMake 中配套 checksum 会检测 `diags/field_diag000250` 是否漂移；物理层面需要人工比对谱峰是否沿 R/L、X 和 Bernstein 分支分布。

### 6.3 Ion beam R instability：低阶 Fourier 模增长率

脚本：`../warpx/Examples/Tests/ohm_solver_ion_beam_instability/analysis.py:84-232`。

```python
field_kt = np.fft.fft(data[:, :], axis=1)
k = 2 * np.pi * np.fft.fftfreq(resolution, dz) * sim.l_i
t_grid = np.arange(num_steps) * dt * sim.w_ci

gamma4 = 0.1915611861780133
gamma5 = 0.20087036355662818
gamma6 = 0.17123024228396777
idx = np.where((t_grid > 10) & (t_grid < 40))
t_points = t_grid[idx]

A4 = np.exp(np.mean(np.log(np.abs(field_kt[idx, 4] / sim.B0)) - t_points * gamma4))
m4_rms_error = np.sqrt(
    np.mean(
        (np.abs(field_kt[idx, 4] / sim.B0) - A4 * np.exp(t_points * gamma4)) ** 2
    )
)

assert np.isclose(m4_rms_error, 1.546, atol=0.01)
assert np.isclose(m5_rms_error, 0.734, atol=0.01)
assert np.isclose(m6_rms_error, 0.367, atol=0.01)
```

物理意义：

- 对 `B_y(z,t)` 沿空间 FFT，追踪 `m=4,5,6` 模。
- 理论增长率来自 Munoz et al. 2018 Fig. 12a，窗口是 $10<t\Omega_i<40$。
- 断言比较的是 RMS error 的历史值，不是直接要求 RMS error 趋近 0。脚本注释明确说这些容差来自测试创建时的误差；失败时应 rerun full benchmark 并人工比较增长率到饱和前的理论趋势。

### 6.4 Ion Landau damping：阻尼率图像，无显式 assert

脚本：`../warpx/Examples/Tests/ohm_solver_ion_Landau_damping/analysis.py:20-113`。

```python
expected_gamma = np.interp(
    sim.T_ratio, theoretical_damping_rate[:, 0], theoretical_damping_rate[:, 1]
)

field_kt = np.fft.fft(data[:, :], axis=1)
t_norm = 2.0 * np.pi * sim.m / sim.Lz * sim.v_ti
t_points = np.arange(num_steps) * dt * t_norm
ax1.plot(
    t_points,
    np.abs(field_kt[:, sim.m] / field_kt[0, sim.m]),
    "r",
    label=f"$T_i/T_e$ = {sim.T_ratio:.2f}",
)
ax1.plot(t_points, np.exp(-t_points * expected_gamma), "k--", lw=2)
```

脚本将 $|E_z(k_m,t)|/|E_z(k_m,0)|$ 与 $\exp(-\gamma t)$ 比较，`gamma` 从 Munoz et al. 2018 Fig. 14b 插值得到。没有显式 `assert`，所以自动化通过主要依赖 checksum；物理写作时应把它作为 Landau damping 可视化验证，而不是强判据。

### 6.5 Magnetic reconnection：重联率图像，无显式 assert

脚本：`../warpx/Examples/Tests/ohm_solver_magnetic_reconnection/analysis.py:23-45`。

```python
plane_data = np.loadtxt("diags/plane.dat", skiprows=1)
steps = np.unique(plane_data[:, 0])
num_steps = len(steps)
num_cells = plane_data.shape[0] // num_steps
plane_data = plane_data.reshape((num_steps, num_cells, plane_data.shape[1]))

times = plane_data[:, 0, 1]
plt.plot(
    times / sim.t_ci,
    np.mean(plane_data[:, :, Ey_idx], axis=1) / (sim.vA * sim.B0),
    "o-",
)
```

重联率采用

$$
R(t)=\frac{\langle E_y\rangle}{v_A B_0}.
$$

脚本只画出 `reconnection_rate.png`，没有数值断言；CMake 还跑 `analysis_default_regression.py --path diags/diag1000020`。这类测试更适合在书中作为“hybrid PIC 物理案例和输出回归”，不能当作独立证明某个 Ohm 项精确正确。

### 6.6 Cylinder compression：checksum only

`ohm_solver_cylinder_compression/CMakeLists.txt` 中 analysis 为 `OFF`，只运行 checksum：

- `diags/diag1000010 --rtol 5e-4`
- `diags/diag1000020 --rtol 1e-6`

这覆盖 cylindrical compression 的输出稳定性，但没有额外物理量 assert。

## 7. 写入第 6 章时的使用规则

后续把验证内容回填到 `manuscript/chapters/06-field-solvers.md` 时，应按如下层次写：

1. 对 FDTD/PSATD NCI：先解释数值 Cherenkov 的物理来源，再写 EB/electric energy 判据和 Gauss law 判据。
2. 对 electrostatic：给出均匀带电球展开的解析推导，再贴 `analysis_electrostatic_sphere.py` 的 `v_exact/t_exact/E_exact` 和 L2/energy assert。
3. 对 implicit：不要只说“测试通过”，要明确总能量、Poynting 边界通量、Gauss law RMS、Newton/GMRES 迭代数分别检验哪一层代码。
4. 对 hybrid Ohm：区分有 assert 的 RZ EM modes / ion beam instability 和无 assert 的 Landau damping / reconnection / Cartesian EM modes / cylinder compression。

当前下一步应先尝试发现本地 WarpX 可执行文件；如果能找到可执行文件，优先选择一个轻量隐式或静电测试跑通，并把命令、输出目录和失败/通过状态补入本验证链。
