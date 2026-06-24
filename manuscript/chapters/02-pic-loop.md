# 2. PIC 总循环：从 Vlasov-Maxwell 到离散时间推进

本章先不急着进入某一个 WarpX 函数。生产级 PIC 代码的困难不在于“有粒子、有网格、有 Maxwell 方程”这几个名词，而在于这些对象必须在离散时间层、离散空间布局、并行 guard cells、边界条件和守恒约束之间保持一致。后续逐行读 WarpX 时，本章给出判断代码是否“物理上在做正确事情”的基准。

本章对应的第一批源码阅读笔记保存在 `notes/code-reading/evolve/01-pic-time-layers.md` 和 `notes/code-reading/evolve/02-evolve-source-evidence.md`。

本章当前依据的 WarpX 源码版本是：

- `../warpx`
- 分支：`pkuHEDPbranch`
- commit：`8c488b1a9`

v0.2 校准说明：本章已把主循环相关源码路径同步到当前 WarpX 目录结构 `Source/Evolve/`，并重核 `Evolve()`、`OneStep_nosub()` 与 FDTD/PSATD 分支的关键行号。章节仍保留基础文献缺口；Hockney-Eastwood、Yee 1966 等一手材料的 MinerU 笔记尚未完成，暂不把这些缺口伪装成已闭环引用。

## 2.1 连续模型：Vlasov-Maxwell 系统

对物种 \(s\)，相空间分布函数 \(f_s(\mathbf{x},\mathbf{p},t)\) 满足 Vlasov 方程：

$$
\frac{\partial f_s}{\partial t}
+\mathbf{v}\cdot\nabla_{\mathbf{x}}f_s
+q_s\left(\mathbf{E}+\mathbf{v}\times\mathbf{B}\right)\cdot\nabla_{\mathbf{p}}f_s=0.
$$

相对论动量与速度满足

$$
\mathbf{p}=\gamma m_s\mathbf{v},\qquad
\gamma=\sqrt{1+\frac{|\mathbf{p}|^2}{m_s^2c^2}},
\qquad
\mathbf{v}=\frac{\mathbf{p}}{\gamma m_s}.
$$

电磁场满足 Maxwell 方程：

$$
\frac{\partial \mathbf{B}}{\partial t}=-\nabla\times\mathbf{E},
$$

$$
\frac{\partial \mathbf{E}}{\partial t}
=c^2\nabla\times\mathbf{B}-\frac{\mathbf{J}}{\epsilon_0},
$$

以及约束方程

$$
\nabla\cdot\mathbf{E}=\frac{\rho}{\epsilon_0},
\qquad
\nabla\cdot\mathbf{B}=0.
$$

源项来自分布函数的矩：

$$
\rho(\mathbf{x},t)=\sum_s q_s\int f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{p},
$$

$$
\mathbf{J}(\mathbf{x},t)=\sum_s q_s\int \mathbf{v}(\mathbf{p})f_s(\mathbf{x},\mathbf{p},t)\,d\mathbf{p}.
$$

PIC 的核心任务就是把这套连续耦合系统离散成两个相互交换信息的对象：宏粒子和网格场。

## 2.2 宏粒子表示与形函数

宏粒子近似把 \(f_s\) 写成有限个带权粒子的和：

$$
f_s(\mathbf{x},\mathbf{p},t)
\approx
\sum_{p\in s} w_p
S_x(\mathbf{x}-\mathbf{x}_p(t))
S_p(\mathbf{p}-\mathbf{p}_p(t)).
$$

这里 \(w_p\) 是宏粒子权重，\(S_x\) 是空间形函数。把粒子源项沉积到网格单元或网格点 \(i\)，常见电荷密度形式是

$$
\rho_i^n
=
\frac{1}{\Delta V_i}\sum_p q_p w_p S_i(\mathbf{x}_p^n).
$$

场 gather 则使用同一类形函数从网格插值回粒子位置：

$$
\mathbf{E}_p^n=\sum_i S_i(\mathbf{x}_p^n)\mathbf{E}_i^n,
\qquad
\mathbf{B}_p^n=\sum_i S_i(\mathbf{x}_p^n)\mathbf{B}_i^n.
$$

如果只看这两个公式，很容易以为 PIC 的网格-粒子耦合只是“双向插值”。这个理解不够。电流 \(\mathbf{J}\) 的沉积必须表达粒子在一个时间步内的轨迹，否则离散电荷守恒会被破坏。

连续系统满足连续性方程：

$$
\frac{\partial \rho}{\partial t}+\nabla\cdot\mathbf{J}=0.
$$

在网格上，电流沉积应尽量满足对应的离散形式：

$$
\frac{\rho_i^{n+1}-\rho_i^n}{\Delta t}
+(\nabla_h\cdot\mathbf{J}^{n+1/2})_i=0.
$$

这解释了为什么 WarpX 这样的代码会提供 Esirkepov、Villasenor-Buneman、Vay 等沉积分支。它们的差异不是表面上的“把电流放到哪里”，而是如何在离散网格上把粒子轨迹、电荷守恒、网格布局和并行边界结合起来。

## 2.3 leapfrog 时间层

显式电磁 PIC 的标准时间层是 leapfrog：

- 粒子位置在整数步：\(\mathbf{x}^n,\mathbf{x}^{n+1}\)。
- 粒子动量在半整数步：\(\mathbf{p}^{n-1/2},\mathbf{p}^{n+1/2}\)。
- 电流自然在半整数步：\(\mathbf{J}^{n+1/2}\)。
- 电磁场在 Yee/FDTD 路径中按半步磁场和整步电场交错推进。

粒子位置推进可写成

$$
\frac{\mathbf{x}^{n+1}-\mathbf{x}^{n}}{\Delta t}
=
\mathbf{v}^{n+1/2}.
$$

动量推进写成抽象形式：

$$
\frac{\mathbf{p}^{n+1/2}-\mathbf{p}^{n-1/2}}{\Delta t}
=
q\left(\mathbf{E}_p^n+\bar{\mathbf{v}}\times\mathbf{B}_p^n\right).
$$

其中 \(\bar{\mathbf{v}}\) 的具体定义取决于 pusher。Boris、Vay、Higuera-Cary 等 pusher 的差别留到粒子推进章节逐行讲解。本章只强调主循环必须给 pusher 提供正确时间层的 \(\mathbf{x}\)、\(\mathbf{p}\)、\(\mathbf{E}\)、\(\mathbf{B}\)。

WarpX 的显式无 subcycling 路径在 `../warpx/Source/Evolve/WarpXEvolve.cpp:515-518` 直接把这个时间层写进注释：

```text
Push particle from x^{n} to x^{n+1}
              from p^{n-1/2} to p^{n+1/2}
Deposit current j^{n+1/2}
Deposit charge density rho^{n}
```

这四行是读 WarpX 主循环的锚点。任何 field gather、collision、ionization、deposition、sync、field solve 的位置都应围绕这些时间层理解。

### 2.3.1 `\omega_p` 不是背景常数，而是时间离散必须尊重的最快等离子体尺度

对电子等离子体，最基本的本征时间尺度是 plasma frequency：

$$
\omega_p=\sqrt{\frac{n_e e^2}{m_e\epsilon_0}}.
$$

它决定了最简单的 Langmuir 振荡周期

$$
T_p=\frac{2\pi}{\omega_p}.
$$

对显式 leapfrog PIC，`稳定` 和 `分辨` 不是同一件事。只要时间层排列正确、场更新满足 CFL，代码也许不会立刻炸掉；但如果

$$
\omega_p \Delta t
$$

已经接近或超过 `1` 的量级，那么单步内粒子和场已经跨过了 plasma oscillation 的核心相位结构，后面看到的高噪声、相位误差、非物理 heating，往往不是“分析脚本太苛刻”，而是主循环本身没有分辨这个最快内禀尺度。

这也是为什么 `Birdsall 1985` 后面会把

$$
\omega_p\Delta t,\qquad
v_t\Delta t/\Delta x
$$

都写成数值健康度的第一层控制量。对 WarpX 来说，这条边界不会自动由 `ComputeDt()` 替你保证。`ComputeDt()` 只根据 solver/CFL、`const_dt`、`max_dt`、`maxParticleVelocity()` 和 AMR refinement 给出一个可运行步长；它并不知道你要不要精确分辨 Langmuir 振荡、electrostatic shielding 或弱不稳定增长率。

所以本章这里先压实一个最重要的判断：

- `ComputeDt()` 保证的是一层离散稳定性和时间步组织契约；
- `\omega_p \Delta t` 是否足够小，仍然是物理建模和分辨率设计问题。

### 2.3.2 `\lambda_D` 不只是一条长度定义，它直接约束 `\Delta x`

和 `\omega_p` 对偶的空间尺度是 Debye length。对非相对论热电子，

$$
\lambda_D=\sqrt{\frac{\epsilon_0 k_B T_e}{n_e e^2}}
=\frac{v_{th,e}}{\omega_p}.
$$

这条式子把热速度、plasma frequency 和 shielding length 绑在了一起。对 PIC 而言，`能否把 plasma 当作 collective medium` 与 `网格是否真的分辨了 shielding` 不是分开的两个问题。

如果

$$
\Delta x \gg \lambda_D,
$$

那么 cell 内已经把最基本的 shielding 结构粗化掉了。接下来即使宏观波形看起来还能跑，field fluctuation、aliasing、self-force 和 nonphysical collisionality 也会被系统性放大。这就是为什么第 1 章已经把 `\lambda_D`、`N_D` 和统计时间尺度单独拎出来；在第 2 章里，它进一步变成主循环的硬分辨率边界：

- `\Delta t` 决定是否分辨 `\omega_p`；
- `\Delta x` 决定是否分辨 `\lambda_D`；
- 两者一起决定 leapfrog + grid PIC 到底是在近似同一个 plasma，还是已经换成了另一个更噪、更热、更强 alias 的离散模型。

## 2.4 FDTD 场更新的数学骨架

忽略 PML、divergence cleaning、宏观介质和边界时，Yee/FDTD 的主更新可以写成三段：

$$
\mathbf{B}^{n+1/2}
=
\mathbf{B}^{n}
-\frac{\Delta t}{2}\nabla_h\times\mathbf{E}^{n},
$$

$$
\mathbf{E}^{n+1}
=
\mathbf{E}^{n}
+c^2\Delta t\nabla_h\times\mathbf{B}^{n+1/2}
-\frac{\Delta t}{\epsilon_0}\mathbf{J}^{n+1/2},
$$

$$
\mathbf{B}^{n+1}
=
\mathbf{B}^{n+1/2}
-\frac{\Delta t}{2}\nabla_h\times\mathbf{E}^{n+1}.
$$

这说明一个电磁 PIC step 的顺序不能随意交换。电场更新需要本步沉积出来的 \(\mathbf{J}^{n+1/2}\)，所以粒子推进与电流沉积必须在 `EvolveE(dt)` 之前完成。WarpX 的 FDTD 路径正是这样组织的：

对应的核心源码节选来自 `../warpx/Source/Evolve/WarpXEvolve.cpp:559-628`，这里保留源项同步和 FDTD 场推进部分；PSATD 分支和 PML 后处理在第 3 章继续展开：

```cpp
// Synchronize J and rho:
// filter (if used), exchange guard cells, interpolate across MR levels
// and apply boundary conditions
SyncCurrentAndRho();

// For extended PML: copy J from regular grid to PML, and damp J in PML
if (do_pml && pml_has_particles) { CopyJPML(); }
if (do_pml && do_pml_j_damping) { DampJPML(); }

ExecutePythonCallback("beforeEsolve");

EvolveF(0.5_rt * dt[0], /*rho_comp=*/0);
EvolveG(0.5_rt * dt[0]);
FillBoundaryF(guard_cells.ng_FieldSolverF);
FillBoundaryG(guard_cells.ng_FieldSolverG);

EvolveB(0.5_rt * dt[0], SubcyclingHalf::FirstHalf, a_cur_time); // We now have B^{n+1/2}
FillBoundaryB(guard_cells.ng_FieldSolver, WarpX::sync_nodal_points);

if (m_em_solver_medium == MediumForEM::Vacuum) {
    // vacuum medium
    EvolveE(dt[0], a_cur_time); // We now have E^{n+1}
} else if (m_em_solver_medium == MediumForEM::Macroscopic) {
    // macroscopic medium
    MacroscopicEvolveE(dt[0], a_cur_time); // We now have E^{n+1}
} else {
    WARPX_ABORT_WITH_MESSAGE("Medium for EM is unknown");
}
FillBoundaryE(guard_cells.ng_FieldSolver, WarpX::sync_nodal_points);

EvolveF(0.5_rt * dt[0], /*rho_comp=*/1);
EvolveG(0.5_rt * dt[0]);
EvolveB(0.5_rt * dt[0], SubcyclingHalf::SecondHalf, a_cur_time + 0.5_rt * dt[0]); // We now have B^{n+1}
```

| 数学动作 | WarpX 源码位置 |
|---|---|
| 粒子从 \(\mathbf{x}^n,\mathbf{p}^{n-1/2}\) 推到 \(\mathbf{x}^{n+1},\mathbf{p}^{n+1/2}\)，并沉积源项 | `../warpx/Source/Evolve/WarpXEvolve.cpp:520-557` |
| 同步 \(\rho,\mathbf{J}\)：滤波、guard cells、AMR、边界 | `../warpx/Source/Evolve/WarpXEvolve.cpp:559-564` 与 `SyncCurrentAndRho()` |
| \(F,G\) 半步、\(\mathbf{B}\) 半步 | `../warpx/Source/Evolve/WarpXEvolve.cpp:607-613` |
| \(\mathbf{E}\) 整步 | `../warpx/Source/Evolve/WarpXEvolve.cpp:615-623` |
| \(F,G\) 半步、\(\mathbf{B}\) 半步 | `../warpx/Source/Evolve/WarpXEvolve.cpp:626-628` |
| PML 与 guard cell 处理 | `../warpx/Source/Evolve/WarpXEvolve.cpp:630-642` |

这里的 \(F,G\) 是 divergence cleaning 相关辅助场，不是最小 Maxwell 更新必需项。WarpX 把它们插在场推进两侧，是为了在实际模拟中控制 \(\nabla\cdot\mathbf{E}\) 或 \(\nabla\cdot\mathbf{B}\) 误差及 PML 相关处理。

### 2.4.1 `CFL` 不是经验参数，而是离散 Maxwell 更新的因果上界

WarpX 的 `ComputeDt()` 不会把 FDTD 时间步写死成 `min(\Delta x_i)/c`，而是把这件事委托给具体差分算法。`../warpx/Source/Evolve/WarpXComputeDt.cpp:68-88` 直接把 solver 分叉写死在主类层：

```cpp
} else if (electromagnetic_solver_id == ElectromagneticSolverAlgo::PSATD) {
    deltat = cfl * minDim(dx) / PhysConst::c;
} else {
#if defined(WARPX_DIM_RZ) || defined(WARPX_DIM_RCYLINDER)
    if (electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee) {
        deltat = cfl * CylindricalYeeAlgorithm::ComputeMaxDt(dx,  n_rz_azimuthal_modes);
#elif defined(WARPX_DIM_RSPHERE)
    if (electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee) {
        deltat = cfl * SphericalYeeAlgorithm::ComputeMaxDt(dx);
#else
    if (grid_type == GridType::Collocated) {
        deltat = cfl * CartesianNodalAlgorithm::ComputeMaxDt(dx);
    } else if (electromagnetic_solver_id == ElectromagneticSolverAlgo::Yee
                || electromagnetic_solver_id == ElectromagneticSolverAlgo::ECT) {
        deltat = cfl * CartesianYeeAlgorithm::ComputeMaxDt(dx);
    } else if (electromagnetic_solver_id == ElectromagneticSolverAlgo::CKC) {
        deltat = cfl * CartesianCKCAlgorithm::ComputeMaxDt(dx);
```

对标准 Cartesian Yee，真正的 CFL 上界在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H:48-55`：

```cpp
static amrex::Real ComputeMaxDt ( amrex::Real const * const dx ) {
    using namespace amrex::literals;
    amrex::Real const delta_t  = 1._rt / ( std::sqrt( AMREX_D_TERM(
                                       1._rt / (dx[0]*dx[0]),
                                     + 1._rt / (dx[1]*dx[1]),
                                     + 1._rt / (dx[2]*dx[2])
                                 ) ) * PhysConst::c );
    return delta_t;
}
```

也就是

$$
\Delta t_{\max}^{\mathrm{Yee}}
=
\frac{1}{c\sqrt{\Delta x^{-2}+\Delta y^{-2}+\Delta z^{-2}}}.
$$

它表达的是离散光锥约束：单步内，Yee curl stencil 不能让信息传播得比离散网格所允许的因果速度更快。`warpx.cfl` 只是把这个严格上界再乘一个安全系数，不是“拍脑袋调参”。

### 2.4.2 数值色散从这里开始：连续光锥被离散 stencil 改写

一旦用有限差分近似 curl，连续真空色散关系

$$
\omega^2=c^2|\mathbf{k}|^2
$$

就不再原样保留。以 Yee 为例，差分导数对应的是

$$
k_d \;\longrightarrow\; \frac{2}{\Delta d}\sin\frac{k_d\Delta d}{2},
$$

于是离散色散关系变成近似的

$$
\sin^2\frac{\omega\Delta t}{2}
=
c^2\Delta t^2
\sum_d
\frac{\sin^2(k_d\Delta d/2)}{\Delta d^2}.
$$

这意味着 phase velocity 和 group velocity 都会偏离连续值，且偏离大小依赖传播方向、波数和网格各向异性。数值色散不是后处理图里才会出现的现象，它在 `UpwardDx()` / `DownwardDx()` 这种最基本的差分定义处就已经写进去了。

Yee 的 `x` 向导数在 `../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H:69-96`：

```cpp
static amrex::Real UpwardDx (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {
    ...
    amrex::Real const inv_dx = coefs_x[0];
    return inv_dx*( F(i+1,j,k,ncomp) - F(i,j,k,ncomp) );
}

template< typename T_Field>
static amrex::Real DownwardDx (
    T_Field const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {
    ...
    amrex::Real const inv_dx = coefs_x[0];
    return inv_dx*( F(i,j,k,ncomp) - F(i-1,j,k,ncomp) );
}
```

也就是 staggered grid 上的前/后向一阶差分：

$$
D_x^+F_i=\frac{F_{i+1}-F_i}{\Delta x},
\qquad
D_x^-F_i=\frac{F_i-F_{i-1}}{\Delta x}.
$$

这里的 `Upward/Downward` 不只是“正向/反向”，而是在 nodal 与 cell-centered 位置之间搬运离散导数。正是这种 staggered 几何，让 Yee 在保持二阶精度的同时把 `E/B` 交错布置起来。

### 2.4.3 `Yee / Nodal / CKC` 的差别本质上是离散色散合同不同

对 collocated/nodal solver，WarpX 的 `CartesianNodalAlgorithm` 不再用 staggered 前后差分，而是直接用中心差分。`../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianNodalAlgorithm.H:71-102`：

```cpp
static amrex::Real UpwardDx (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_x, int const /*n_coefs_x*/,
    int const i, int const j, int const k, int const ncomp=0 ) {
    ...
    Real const inv_dx = coefs_x[0];
    return 0.5_rt*inv_dx*( F(i+1,j,k,ncomp) - F(i-1,j,k,ncomp) );
}

static amrex::Real DownwardDx (
    amrex::Array4<amrex::Real const> const& F,
    amrex::Real const * const coefs_x, int const n_coefs_x,
    int const i, int const j, int const k, int const ncomp=0 ) {
    ...
    return UpwardDx( F, coefs_x, n_coefs_x, i, j, k ,ncomp);
}
```

所以 nodal grid 上 `UpwardDx` 和 `DownwardDx` 等价，说明这里已经没有 Yee 那种 staggered 位置语义，而是一个 collocated 中心差分系统。它的 CFL 上界虽然在当前实现里和 Yee 一样都是

$$
\Delta t_{\max}\sim \frac{1}{c\sqrt{\sum_d \Delta d^{-2}}},
$$

但数值色散与奇偶模耦合特征已经不同。

CKC 则更进一步，不再满足“一个方向只看一对最近邻”的局部导数定义。`../warpx/Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianCKCAlgorithm.H:107-123,131-158`：

```cpp
static amrex::Real ComputeMaxDt ( amrex::Real const * const dx ) {
#if (defined WARPX_DIM_1D_Z)
        amrex::Real const delta_t = dx[0]/PhysConst::c;
#elif (defined WARPX_DIM_XZ)
        amrex::Real const delta_t = std::min( dx[0], dx[1] )/PhysConst::c;
#else
        amrex::Real const delta_t = std::min( dx[0], std::min( dx[1], dx[2] ) ) / PhysConst::c;
#endif
    return delta_t;
}
...
return alphax * (F(i+1,j  ,k  ,ncomp) - F(i,  j,  k  ,ncomp))
     + betaxy * (F(i+1,j+1,k  ,ncomp) - F(i  ,j+1,k  ,ncomp)
              +  F(i+1,j-1,k  ,ncomp) - F(i  ,j-1,k  ,ncomp))
     + betaxz * (F(i+1,j  ,k+1,ncomp) - F(i  ,j  ,k+1,ncomp)
              +  F(i+1,j  ,k-1,ncomp) - F(i  ,j  ,k-1,ncomp))
```

这说明 CKC 的真实目标不是“换一套写法”，而是通过更宽的横向耦合 stencil 改写离散色散关系，从而改善高方向性传播下的 phase error。代价则是：

- stencil 更宽；
- 算法/geometry 适用范围更窄；
- guard-cell 和边界处理的组合空间更复杂。

## 2.5 PSATD 与 FDTD 的主循环差异

FDTD 在实空间用局部 stencil 近似 curl。PSATD 则在谱空间解析积分线性 Maxwell 方程的一部分。物理方程相同，但离散算法不同：

- FDTD 的优势是局部、显式、边界和 AMR 工程路径相对直接。
- PSATD 能显著降低数值色散，适合相对论束流、激光等问题，但对 FFT、并行 domain decomposition、边界、current correction 和时间平均场有更复杂要求。

这条分界线和前面几节正好连起来：

- `leapfrog` 规定了粒子、场和源项的时间层合同；
- `\omega_p` 与 `\lambda_D` 规定了 plasma 自身是否被当前 `\Delta t/\Delta x` 分辨；
- `CFL` 规定了 Maxwell 更新是否还能保持离散因果；
- `Yee/Nodal/CKC/PSATD` 则进一步决定同一组 `\Delta t,\Delta x` 会把波动相速度、群速度和 aliasing 改写成什么样。

所以“主循环能跑”不等于“主循环近似的是对的物理系统”。真正的 PIC loop 要同时满足：

$$
\text{time-layer consistency}
\;+\;
\text{charge/source consistency}
\;+\;
\text{physical scale resolution}
\;+\;
\text{solver-dependent stability/dispersion control}.
$$

WarpX 在 `OneStep_nosub()` 内部把两者清楚分开：

- PSATD 分支在 `../warpx/Source/Evolve/WarpXEvolve.cpp:576-605`，核心是 `PushPSATD(a_cur_time)`。
- FDTD 分支在 `../warpx/Source/Evolve/WarpXEvolve.cpp:606-642`，核心是 `EvolveB/EvolveE/EvolveB`。

这意味着本书后续讲 field solver 时不能把“Maxwell solver”写成单一算法。`algo.maxwell_solver` 的选择会改变主循环内的场推进、同步、边界和可用功能。

## 2.6 一个真实 PIC step 的工程层次

把物理动作映射到生产代码，一个时间步至少包含这些层次：

1. 用户 callback、信号、诊断、负载均衡和步长更新。
2. 场 gather 前的 guard cell 与 auxiliary field 准备。
3. 电离、QED、粒子注入等改变粒子集合的多物理模块。
4. 粒子推进、碰撞、沉积电流和电荷。
5. 源项同步：滤波、guard cells、AMR fine/coarse 交换、边界条件。
6. 场推进：FDTD、PSATD、implicit、electrostatic 或 hybrid。
7. PML、moving window、粒子边界、重分布、排序。
8. 诊断写出和终止条件检查。

WarpX 的 `../warpx/Source/Evolve/WarpXEvolve.cpp:147-390` 正是围绕这些层次组织外层 `Evolve()` 循环。真正的主循环不是教科书五行伪代码，而是把守恒离散化、时间层一致性和大规模并行工程组合起来的控制流。

## 2.7 本章后的源码阅读入口

读者现在可以从三个源码入口继续：

| 目标 | 入口 |
|---|---|
| 看外层时间步如何组织 | `../warpx/Source/Evolve/WarpXEvolve.cpp:147-390` |
| 看显式电磁无 subcycling 的标准 step | `../warpx/Source/Evolve/WarpXEvolve.cpp:507-646` |
| 看主循环如何进入粒子容器 | `../warpx/Source/Evolve/WarpXEvolve.cpp:1311-1415` |

## 2.8 参数示例与最小运行案例

如果把本章压回一个最小、可运行、可验证的输入骨架，当前最合适的入口还是：

- `../warpx/Examples/Tests/langmuir/inputs_test_1d_langmuir_multi`

它把本章真正讨论的五类量都放在同一个最小问题上：

- `geometry.dims = 1`
- `algo.maxwell_solver = yee`
- `algo.current_deposition = esirkepov`
- `algo.field_gathering = energy-conserving`
- `warpx.cfl = 0.8`
- `max_step = 80`
- 周期场边界

也就是说，本章的抽象讨论并不是悬空的。这里的：

- `leapfrog` 时间层
- `\omega_p`
- `\lambda_D`
- FDTD curl 更新
- `rho/J` 连续性合同

都能在这条最小 Langmuir 主线上落到真实输入。

当前本地最小运行记录已经建立在：

- `/Volumes/PHILIPS/programs/PIC/PIC-tutor/runs/stage-c-validation/langmuir_1d`

对应命令：

```bash
env OMP_NUM_THREADS=1 FI_PROVIDER=tcp \
  /Volumes/PHILIPS/programs/PIC/warpx/build_full/bin/warpx.1d.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES \
  /Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/langmuir/inputs_test_1d_langmuir_multi
```

它对本章最重要的不是“程序成功退出”，而是：

- 解析场相对误差 `1.7027848999745115e-3 < 5e-2`
- `divE-rho/\epsilon_0` 相对误差 `8.34503170903001e-12 < 1e-11`

所以本章已经具备：

- 参数示例
- 最小运行案例
- 物理检查量

而不是只停在连续模型和离散方程层。

## 2.9 本章当前基础文献清单

本章当前已经直接依托的基础来源是：

- `Birdsall 1985`
  - leapfrog 最小教学骨架
  - `\omega_p \Delta t`
  - `v_t \Delta t/\Delta x`
  - finite-grid / aliasing / heating 主线
- `Dawson 1983`
  - electrostatic / full EM 的数值模型边界
  - full EM 时间步与 light mode / CFL 的关系
  - Darwin 作为 radiation-free low-frequency route

本章当前还没有直接依托其正文细节的一手来源是：

- `Yee 1966`
  - 当前只到 metadata/acquisition 边界
- `Hockney-Eastwood`
  - 当前原书与 article-level fallback 仍未 materialize 为项目内 full-text + MinerU 资产

更完整的基础章节文献状态、local-materialization 状态和“可直接作为正文证据/只可作待补边界”的分工，统一见：

- [基础章节文献清单](/Volumes/PHILIPS/programs/PIC/PIC-tutor/docs/foundations-literature-list.md)

## 2.10 进一步阅读与练习

进一步阅读：

1. [03-warpx-evolve.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/manuscript/chapters/03-warpx-evolve.md)：把本章的 PIC loop 抽象结构接到 `main.cpp -> WarpX::Evolve()` 的真实调用链。
2. [Birdsall 1985 中文讲解](/Volumes/PHILIPS/programs/PIC/PIC-tutor/references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation-中文讲解.md)：继续看 `\omega_p\Delta t`、`\lambda_D/\Delta x`、finite-grid aliasing 和 numerical heating。
3. [Dawson 1983 中文讲解](/Volumes/PHILIPS/programs/PIC/PIC-tutor/references/03_pic_foundations/1983_Dawson_Particle_simulation_of_plasmas/1983_Dawson_Particle_simulation_of_plasmas-中文讲解.md)：继续看 full EM、Darwin、quiet start 和 statistical measurements 如何改变“PIC 总循环”的解释方式。

练习题：

1. 解释为什么 `ComputeDt()` 给出的可运行时间步，不自动保证 `\omega_p \Delta t \ll 1`。
2. 用本章的 `\lambda_D` 讨论说明：为什么 `\Delta x \gg \lambda_D` 时，即使主循环稳定，也可能已经不是同一个物理 plasma。
3. 对照 [00-langmuir-wave.md](/Volumes/PHILIPS/programs/PIC/PIC-tutor/notes/code-reading/applications/00-langmuir-wave.md)，指出 `analysis_1d.py` 的两条核心断言分别对应本章哪两类理论边界。

下一章将逐段解释这些源码，并把 `main.cpp`、`WarpX` 单例、`ReadParameters()`、`InitData()`、`ComputeDt()` 和 `Evolve()` 接成完整调用链。
