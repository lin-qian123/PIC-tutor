# Implicit / Hybrid PIC 源码精读

绑定源码与文档：

- `../warpx/Source/WarpX.cpp:1248-1266,2480-2533`
- `../warpx/Source/FieldSolver/WarpXPushFieldsHybridPIC.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/SemiImplicitEM.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/SemiImplicitEM.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/StrangImplicitSpectralEM.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/StrangImplicitSpectralEM.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverVec.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverDOF.H`
- `../warpx/Source/NonlinearSolvers/NonlinearSolver.H`
- `../warpx/Source/NonlinearSolvers/LinearSolver.H`
- `../warpx/Source/NonlinearSolvers/PicardSolver.H`
- `../warpx/Source/NonlinearSolvers/NewtonSolver.H`
- `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.H`
- `../warpx/Source/FieldSolver/FiniteDifferenceSolver/HybridPICModel/HybridPICModel.cpp`
- `../warpx/Docs/source/usage/parameters.rst:240-320`

这一块代码做的事情和前面的显式 FDTD/PSATD 不一样。这里不再“先沉积，再推进场，再推进粒子”，而是把粒子和场绑进一个非线性系统里，一次步进中同时满足时间离散、麦克斯韦方程、洛伦兹力和欧姆定律。

隐式 EM 的主物理图像可以概括为：

- `theta-implicit`：E 和 B 都在未知量中，场和粒子都隐式耦合。
- `semi-implicit`：E 和粒子隐式耦合，B 仍按显式 leapfrog 推进。
- `strang-implicit-spectral`：先做源自由的谱推进，再把有源项和粒子非线性问题嵌入 Strang 分裂中。
- `hybrid PIC`：离子是 kinetic，电子被流体化，电场由 Ohm 定律闭合，磁场按 Faraday 定律和 RK 子步推进。

## 1. 参数入口和 solver 选择

`WarpX::ReadParameters()` 在 `evolve_scheme` 上选择隐式 solver：

```cpp
// check for implicit evolve scheme
if (evolve_scheme == EvolveScheme::SemiImplicitEM) {
    m_implicit_solver = std::make_unique<SemiImplicitEM>();
}
else if (evolve_scheme == EvolveScheme::ThetaImplicitEM) {
    m_implicit_solver = std::make_unique<ThetaImplicitEM>();
}
else if (evolve_scheme == EvolveScheme::StrangImplicitSpectralEM) {
    m_implicit_solver = std::make_unique<StrangImplicitSpectralEM>();
}

// implicit evolve schemes not setup to use mirrors
if (evolve_scheme == EvolveScheme::SemiImplicitEM ||
    evolve_scheme == EvolveScheme::ThetaImplicitEM) {
    WARPX_ALWAYS_ASSERT_WITH_MESSAGE( m_num_mirrors == 0,
        "Mirrors cannot be used with Implicit evolve schemes.");
}
```

参数文档把非线性求解器、Picard / Newton / PETSc SNES、质量矩阵和预条件器说得很清楚。关键约束是：

- `implicit_evolve.nonlinear_solver = picard` 走固定点迭代。
- `implicit_evolve.nonlinear_solver = newton` 走 PS-JFNK。
- `implicit_evolve.use_mass_matrices_jacobian = true` 可把粒子响应通过 mass matrix 塞进 Jacobian 线性阶段。
- `implicit_evolve.use_mass_matrices_pc = true` 可把 plasma response 塞进 preconditioner。

文档对应的物理边界是：隐式系统不要求 Debye 长度分辨，也不要求 light-wave CFL，但 time step 仍然受粒子越界和物理分辨率限制。

## 2. 抽象层：`ImplicitSolver`、`WarpXSolverVec` 和 `NonlinearSolver`

`ImplicitSolver` 是所有隐式推进器的共同基类。它只定义三件事：

1. `Define()` 读取参数并分配中间量。
2. `OneStep()` 完成一个时间步。
3. `ComputeRHS()` 给非线性迭代器计算右端项。

```cpp
class ImplicitSolver
{
public:
    virtual void Define (WarpX* a_WarpX, bool from_restart) = 0;
    virtual void PrintParameters () const = 0;
    virtual void OneStep ( amrex::Real  a_time,
                           amrex::Real  a_dt,
                           int          a_step ) = 0;
    virtual void ComputeRHS ( WarpXSolverVec&  a_RHS,
                        const WarpXSolverVec&  a_E,
                              amrex::Real      a_time,
                              int              a_nl_iter,
                              bool             a_from_jacobian ) = 0;
```

它内部保存的不是单个标量，而是当前求解器所需的场容器、粒子参数、质量矩阵和非线性求解器对象：

```cpp
    amrex::Real m_theta = 0.5;
    NonlinearSolverType m_nlsolver_type;
    std::unique_ptr<NonlinearSolver<WarpXSolverVec,ImplicitSolver>> m_nlsolver;
    amrex::ParticleReal m_particle_tolerance = amrex::ParticleReal(1.0e-10);
    int m_max_particle_iterations = 21;
    bool m_particle_suborbits = false;
    bool m_use_mass_matrices = false;
    bool m_use_mass_matrices_jacobian = false;
    bool m_use_mass_matrices_pc = false;
```

`WarpXSolverVec` 是一个给 nonlinear / linear solver 用的场向量包装。它不是“任意数组”，而是和 WarpX field registry 对齐的 `MultiFab` 视图，能执行 `Copy`、`+=`、`-=`
、`linComb`、`scale` 等操作：

```cpp
class WarpXSolverVec
{
public:
    void Define ( WarpX*  a_WarpX,
             const std::string&  a_vector_type_name,
             const std::string&  a_scalar_type_name = "none" );
    [[nodiscard]] RT dotProduct( const WarpXSolverVec&  a_X ) const;
    void Copy ( warpx::fields::FieldType  a_array_type,
                warpx::fields::FieldType  a_scalar_type = warpx::fields::FieldType::None,
                bool allow_type_mismatch = false);
    inline void linComb (const RT a, const WarpXSolverVec& X, const RT b, const WarpXSolverVec& Y)
```

它的设计重点是“求解器视角下的解向量”，而不是“物理模块视角下的场注册表”。例如 theta-implicit 的未知量是 `Efield_fp`，所以 `WarpXSolverVec` 的 array part 直接绑定到 `Efield_fp`。

非线性求解器抽象在 `NonlinearSolver<Vec,Ops>`。它要求 `Ops` 提供 `ComputeRHS(RHS,U,time,iter,from_jacobian)`，因此隐式 EM 的 solver 类本身就是那个 `Ops`：

```cpp
template<class Vec, class Ops>
class NonlinearSolver
{
public:
    virtual void Define ( const Vec&,
                          Ops* ) = 0;
    virtual void Solve ( Vec&,
                   const Vec&,
                         amrex::Real,
                         amrex::Real,
                         int) const = 0;
    virtual void PrintParams () const = 0;
    virtual void GetSolverParams (amrex::Real&, amrex::Real&, int&) = 0;
```

Picard 是固定点迭代 `U=b+R(U)`：

```cpp
// Picard fixed-point iteration method to solve nonlinear
// equation of form: U = b + R(U)
```

Newton 则是把问题写成 `F(U)=U-b-R(U)=0`，再用 GMRES 或 PETSc KSP 解 Jacobian 线性化系统：

```cpp
// Newton method to solve nonlinear equation of form:
// F(U) = U - b - R(U) = 0.
```

这里的关键不是“调用了一个求解器”，而是 `Ops::ComputeRHS()` 必须把粒子更新、沉积、边界和 field update 的全部逻辑塞进可重复求值的残差函数里。这也是隐式 PIC 真正复杂的地方。

## 3. `ThetaImplicitEM`：完全隐式的电磁推进

`ThetaImplicitEM` 的文件注释把时间离散写得很清楚：

$$
E_g^{n+1}=E_g^n+c^2\Delta t\left(\nabla\times B_g^{n+\theta}-\mu_0J_g^{n+1/2}\right),
$$

$$
B_g^{n+1}=B_g^n-\Delta t\,\nabla\times E_g^{n+\theta},
$$

$$
x_p^{n+1}=x_p^n+\Delta t\,u_p^{n+1/2}/\left[0.5(\gamma_p^n+\gamma_p^{n+1})\right],
$$

$$
u_p^{n+1}=u_p^n+\Delta t\,q_p/m_p\left(E_p^{n+\theta}+u_p^{n+1/2}/\gamma_p^{n+1/2}\times B_p^{n+\theta}\right),
$$

其中

$$
f^{n+\theta}=(1-\theta)f^n+\theta f^{n+1},\qquad 0.5\le \theta \le 1.
$$

源码中 `Define()` 做四件事：定义 `E`/`Eold` 容器，分配 `B_old`，解析 `implicit_evolve.theta`，再定义非线性求解器：

```cpp
// Define E and Eold vectors
m_E.Define(m_WarpX, "Efield_fp");
m_Eold.Define(m_E);

// Define B_old MultiFab
for (int lev = 0; lev < m_num_amr_levels; ++lev) {
    const auto& ba_Bx = m_WarpX->m_fields.get(FieldType::Bfield_fp, Direction{0}, lev)->boxArray();
    ...
    m_WarpX->m_fields.alloc_init(FieldType::B_old, Direction{0}, lev, ba_Bx, dm, 1, ngb, 0.0_rt);
}

const amrex::ParmParse pp("implicit_evolve");
pp.query("theta", m_theta);
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    m_theta>=0.5 && m_theta<=1.0,
    "theta parameter for theta implicit time solver must be between 0.5 and 1.0");

parseNonlinearSolverParams( pp );
m_nlsolver->Define(m_E, this);
```

`OneStep()` 的流程是：

1. 保存粒子初值。
2. 用上一时间步的 `E^{n-1+\theta}` 给当前步提供初值。
3. 调 `m_nlsolver->Solve()` 求 `E^{n+\theta}`。
4. 用求解出的 `E` 更新 WarpX owned fields。
5. 完成粒子 `n+1/2 -> n+1` 的隐式后处理。
6. 用线性关系还原 `E^{n+1}`，并把 `B^{n+\theta}` 推到 `n+1`。

```cpp
// Initial guess for Eg^{n+theta} is Eg^{n-1+theta}
m_E.linComb(1.0_rt - m_theta, m_Eold, m_theta, m_E);
...
m_nlsolver->Solve(m_E, m_Eold, start_time, m_dt, a_step);
...
UpdateWarpXFields(m_E, start_time);
...
m_WarpX->FinishImplicitParticleUpdate();
...
FinishFieldUpdate(end_time);
```

`ComputeRHS()` 则把隐式系统写成残差的右端。它先把当前迭代的 `E` 写回 WarpX，然后用这个场推动粒子、沉积电流，再调用 `ImplicitComputeRHSE()` 形成

$$
R(E)=c^2\theta\Delta t\left(\nabla\times B^{n+\theta}-\mu_0J^{n+1/2}\right).
$$

```cpp
UpdateWarpXFields( a_E, start_time );
const amrex::Real theta_time = start_time + m_theta*m_dt;
PreRHSOp( theta_time, a_nl_iter, a_from_jacobian );
m_WarpX->ImplicitComputeRHSE( m_theta*m_dt, a_RHS);
```

这说明 theta-implicit 的“未知量”是 time-centered electric field，粒子则以这个场为输入反复迭代，直到场-粒子自洽。

## 4. `SemiImplicitEM`：E 隐式、B 显式

semi-implicit 的核心差异是 B 仍然使用标准 leapfrog，而 E 和粒子在中间时刻隐式耦合。源码注释给出的 stencil 是：

$$
E_g^{n+1}=E_g^n+c^2\Delta t(\nabla\times B_g^{n+1/2}-\mu_0J_g^{n+1/2}),
$$

$$
B_g^{n+3/2}=B_g^{n+1/2}-\Delta t\nabla\times E_g^{n+1},
$$

粒子则在 `n+1/2` 上按同样的隐式电场更新。

`Define()` 只定义 `E`/`Eold` 和非线性求解器，不保存 `B_old`，因为 B 不是 solver 的未知量：

```cpp
// Define E and Eold vectors
m_E.Define(m_WarpX, "Efield_fp");
m_Eold.Define(m_E);

parseNonlinearSolverParams(pp);
m_nlsolver->Define(m_E, this);
```

`OneStep()` 的时间分裂更清楚：

```cpp
// Advance WarpX owned Bfield_fp from t_{n} to t_{n+1/2}
m_WarpX->EvolveB(0.5_rt*m_dt, SubcyclingHalf::FirstHalf, start_time);
...
// Solve nonlinear system for Eg at t_{n+1/2}
m_nlsolver->Solve(m_E, m_Eold, start_time, m_dt, a_step);
...
// Advance WarpX owned Bfield_fp from t_{n+1/2} to t_{n+1}
m_WarpX->EvolveB(0.5_rt*m_dt, SubcyclingHalf::SecondHalf, half_time);
```

所以 semi-implicit 更像“把 E 放进非线性闭环里，而把 B 仍交给显式推进”。它的主要优点是光波色散比 theta-implicit 更接近显式 Maxwell；代价是仍然受 CFL 约束。

`ComputeRHS()` 也比 theta 版本短：它只要把 `E^{n+1/2}` 写回去，预处理粒子后，右端就是

$$
R(E)=c^2\frac{\Delta t}{2}\left(\nabla\times B^{n+1/2}-\mu_0J^{n+1/2}\right).
$$

```cpp
const amrex::Real half_time = start_time + 0.5_rt*m_dt;
m_WarpX->SetElectricFieldAndApplyBCs( a_E, half_time );
PreRHSOp( half_time, a_nl_iter, a_from_jacobian );
m_WarpX->ImplicitComputeRHSE(0.5_rt*m_dt, a_RHS);
```

## 5. `StrangImplicitSpectralEM`：源自由谱推进 + 非线性闭环

这是 implicit solver 里最不容易看错的一个。它在每个时间步前后都做一次 source-free spectral advance，中间把带源项的非线性系统放在 Strang 分裂中间层。

文件注释把流程写成：

1. `E^n, B^n -> E^{n+1/2}, B^{n+1/2}` 做源自由推进。
2. 在中间层迭代粒子和场，求 `E^{n+1/2}`。
3. 再做一次源自由推进得到 `E^{n+1}, B^{n+1}`。

`Define()` 仍然围绕 `E` / `Eold` 和非线性求解器展开：

```cpp
m_E.Define(m_WarpX, "Efield_fp");
m_Eold.Define(m_E);
...
parseNonlinearSolverParams( pp_implicit_evolve );
m_nlsolver->Define(m_E, this);
```

`OneStep()` 的关键是两次 `SpectralSourceFreeFieldAdvance()`：

```cpp
// Advance the fields to time n+1/2 source free
m_WarpX->SpectralSourceFreeFieldAdvance(start_time);
...
// Advance the fields to time n+1 source free
m_WarpX->SpectralSourceFreeFieldAdvance(half_time);
```

这告诉我们它不是普通的隐式 Maxwell，而是把光场线性传播部分交给频域无源推进器，非线性部分只负责粒子和源项闭环。对于单盒 periodic FFT 时可以严格能量守恒；多 box 情况下源码注释已经提醒过，单盒周期假设不再和电流一致，所以不再严格守恒。

`ComputeRHS()` 在这里更简单：它只返回

$$
R(E)=-\frac{\mu_0 c^2\Delta t}{2}J^{n+1/2},
$$

因为源自由传播已经单独处理了：

```cpp
// For Strang split implicit PSATD, the RHS = -dt*mu*c**2*J
bool const allow_type_mismatch = true;
a_RHS.Copy(FieldType::current_fp, warpx::fields::FieldType::None, allow_type_mismatch);
amrex::Real constexpr coeff = PhysConst::c2 * PhysConst::mu0;
a_RHS.scale(-coeff * 0.5_rt*m_dt);
```

这也是为什么这个算法看起来像“隐式 PSATD”，但本质上是“PSATD 线性部分 + 非线性粒子闭环”的 Strang 分裂实现。

## 6. 非线性求解器：Picard、Newton、GMRES、PETSc

`parseNonlinearSolverParams()` 把 `implicit_evolve.nonlinear_solver` 映射成 `PicardSolver` 或 `NewtonSolver` / `PETScSNES`：

```cpp
pp.get("nonlinear_solver", m_nlsolver_type);

if (m_nlsolver_type == NonlinearSolverType::picard) {
    m_nlsolver = std::make_unique<PicardSolver<WarpXSolverVec,ImplicitSolver>>();
    m_max_particle_iterations = 1;
    m_particle_tolerance = 0.0;
}
else if (      (m_nlsolver_type == NonlinearSolverType::newton)
            || (m_nlsolver_type == NonlinearSolverType::petsc_snes) ) {
    if (m_nlsolver_type == NonlinearSolverType::newton) {
        m_nlsolver = std::make_unique<NewtonSolver<WarpXSolverVec,ImplicitSolver>>();
    } else {
        m_nlsolver = std::make_unique<PETScSNES<WarpXSolverVec,ImplicitSolver>>();
    }
```

Picard 的 `Solve()` 是经典固定点迭代：

```cpp
// Update the solver state (a_U = a_b + m_R)
m_ops->ComputeRHS( m_R, a_U, a_time, iter, false );
a_U.Copy(a_b);
a_U += m_R;
```

Newton 则把残差写成 `F(U)=U-b-R(U)`，再构造 JacobianFunction 和线性求解器：

```cpp
m_linear_function = std::make_unique<JacobianFunctionMF<Vec,Ops>>();
m_linear_function->define(m_F, m_ops, m_pc_type);
...
if (m_linear_solver_type == LinearSolverType::amrex_gmres) {
    m_linear_solver = std::make_unique<AMReXGMRES<Vec,JacobianFunctionMF<Vec,Ops>>>();
} else if (m_linear_solver_type == LinearSolverType::petsc_ksp) {
    m_linear_solver = std::make_unique<PETScKSP<Vec,JacobianFunctionMF<Vec,Ops>>>();
}
```

这和前面的显式场推进不一样：这里的线性代数对象不是 field update 的副产品，而是 solve loop 的核心。

## 7. mass matrices 和 Jacobian / preconditioner

隐式 solver 的一个关键加速手段是 mass matrices。`PreLinearSolve()` 先调用 `DepositMassMatrices()`，然后按选项把它们用于 Jacobian 或 preconditioner：

```cpp
if (m_use_mass_matrices) {

    m_WarpX->DepositMassMatrices();

    if (m_use_mass_matrices_jacobian) {
        FinishMassMatrices();
        SaveE();
    }

    if (m_use_mass_matrices_pc) {
        SyncMassMatricesPCAndApplyBCs();
        const amrex::Real theta_dt = m_theta*m_dt;
        SetMassMatricesForPC( theta_dt );
    }
}
```

`ComputeJfromMassMatrices()` 这段代码的物理含义是把

$$
\delta J \approx \mathbf M\,\delta E
$$

离散化成不同偏导方向上的 mass matrix 元素。它不是随手乘个系数，而是在不同 stencil 和 node/cell staggering 上精确存储 `dJx/dEx`、`dJx/dEy`、`dJx/dEz` 等响应项：

```cpp
// dJx = MassMatrices_xx*dEx + MassMatrices_xy*dEy + MassMatrices_xz*dEz
// dJy = MassMatrices_yx*dEx + MassMatrices_yy*dEy + MassMatrices_yz*dEz
// dJz = MassMatrices_zx*dEx + MassMatrices_zy*dEy + MassMatrices_zz*dEz
```

`InitializeMassMatrices()` 会根据当前 current deposition 算法、粒子形函数阶数和维度，决定每个方向的 mass-matrix component 数量。比如 Direct deposition 和 Villasenor deposition 的 component 布局明显不同，说明这里并不是“一个统一的响应矩阵”。

## 8. `HybridPICModel`：kinetic ions + fluid electrons

Hybrid PIC 是单层模拟。`WarpX::HybridPICEvolveFields()` 一上来就断言 `finest_level == 0`：

```cpp
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    finest_level == 0,
    "Ohm's law E-solve only works with a single level.");
```

它的时间推进是一个 split + RK 子步结构：

1. 可选地减去外部场分裂部分。
2. 沉积粒子和流体的 `rho/J`。
3. 计算外部电流。
4. 用 `BfieldEvolveRK()` 把 `B` 从 `n` 推到 `n+1`，中间同步更新 `E`。
5. 重新计算 `E`，再把外部场加回去。

```cpp
// The particles have now been pushed to their t_{n+1} positions.
// Perform charge deposition at t_{n+1} and current deposition at t_{n+1/2}.
HybridPICDepositRhoAndJ();
...
// Push the B field from t=n to t=n+1/2 using the current and density
// at t=n, while updating the E field along with B using the electron
// momentum equation
for (int sub_step = 0; sub_step < sub_steps_per_half; sub_step++)
{
    m_hybrid_pic_model->BfieldEvolveRK(..., dt[0]/sub_steps, SubcyclingHalf::FirstHalf, ...);
}
```

Hybrid model 的参数在 `hybrid_pic_model` 段里读取。它包含：

- `substeps`：B 的子循环数，源码强制为偶数。
- `elec_temp`、`n0_ref`、`gamma`：电子压强状态方程。
- `plasma_resistivity(rho,J)`、`plasma_hyper_resistivity(rho,B)`：欧姆定律中的电阻项和超电阻项。
- `Jx_external_grid_function(...)` 等：外部电流。
- `add_external_fields`：是否叠加外部矢势/场分裂。

```cpp
utils::parser::queryWithParser(pp_hybrid, "substeps", m_substeps);
if (m_substeps % 2 != 0) {
    ablastr::warn_manager::WMRecordWarning(
        "HybridPIC",
        "hybrid_pic_model.substeps must be divisible by 2. "
        "The value " + std::to_string(m_substeps) + " is not valid. "
        "Automatically adjusting to " + std::to_string(m_substeps + 1) + ".",
        ablastr::warn_manager::WarnPriority::medium);
    m_substeps += 1;
}
...
if (!utils::parser::queryWithParser(pp_hybrid, "elec_temp", m_elec_temp)) {
    Abort("hybrid_pic_model.elec_temp must be specified when using the hybrid solver");
}
```

### 8.1 hybrid 所需的额外 field

`AllocateLevelMFs()` 会额外分配电子压强、临时电荷/电流、plasma current、external current，以及可选 external vector potential 的 field：

```cpp
fields.alloc_init(FieldType::hybrid_electron_pressure_fp,
    lev, amrex::convert(ba, rho_nodal_flag),
    dm, ncomps, ngRho, 0.0_rt);

fields.alloc_init(FieldType::hybrid_rho_fp_temp,
    lev, amrex::convert(ba, rho_nodal_flag),
    dm, ncomps, ngRho, 0.0_rt);

fields.alloc_init(FieldType::hybrid_current_fp_plasma, Direction{0},
    lev, amrex::convert(ba, jx_nodal_flag),
    dm, ncomps, ngJ, 0.0_rt);
```

这说明 hybrid PIC 并不是直接复用显式 EM 的 field registry，而是额外保存了一层 Ohm 定律闭合所需的中间量。

### 8.2 `HybridPICDepositRhoAndJ()`

这一步把粒子和流体的源项同步成 hybrid solver 需要的形式：

```cpp
// Perform charge deposition in component 0 of rho_fp at current time.
mypc->DepositCharge(m_fields.get_mr_levels(FieldType::rho_fp, finest_level), 0._rt);
// Perform current deposition at t_{n-1/2}.
mypc->DepositCurrent(m_fields.get_mr_levels_alldirs(FieldType::current_fp, finest_level), dt[0], -0.5_rt * dt[0]);

// Perform Temperature Deposition at time t_{n}
mypc->DepositTemperatures(m_fields, 0.0_rt);
```

如果存在流体 species，还会把流体电荷和电流加进去，再做 `SyncCurrentAndRho()` 和 `FillBoundary`：

```cpp
if (do_fluid_species) {
    myfl->DepositCharge(m_fields, *m_fields.get(FieldType::rho_fp, lev), lev);
    myfl->DepositCurrent(m_fields,
        *m_fields.get(FieldType::current_fp, Direction{0}, lev),
        *m_fields.get(FieldType::current_fp, Direction{1}, lev),
        *m_fields.get(FieldType::current_fp, Direction{2}, lev),
        lev);
}
...
SyncCurrentAndRho();
```

### 8.3 `CalculatePlasmaCurrent()` 和 Ohm 定律

plasma current 不是直接取粒子 current，而是用 Ampere 定律重构：

$$
\mathbf J_\mathrm{plasma}=\frac{1}{\mu_0}\nabla\times\mathbf B-\mathbf J_\mathrm{ext}.
$$

源码里它先调用 FDTD solver 的 `CalculateCurrentAmpere()`，再减去外部 current：

```cpp
ablastr::fields::VectorField current_fp_plasma = warpx.m_fields.get_alldirs(FieldType::hybrid_current_fp_plasma, lev);
warpx.get_pointer_fdtd_solver_fp(lev)->CalculateCurrentAmpere(
    current_fp_plasma, Bfield, eb_update_E, lev
);
...
if (m_has_external_current) {
    ablastr::fields::VectorField current_fp_external = warpx.m_fields.get_alldirs(FieldType::hybrid_current_fp_external, lev);
    for (int i=0; i<3; i++) {
        current_fp_plasma[i]->minus(*current_fp_external[i], 0, 1, 1);
    }
}
```

`HybridPICSolveE()` 再调用 FDTD solver 中专门的 Ohm 定律闭合，把

$$
\mathbf E = -\mathbf u_e\times\mathbf B - \nabla p_e/(en_e) + \eta \mathbf J + \cdots
$$

这类项写进 E 更新。源码层面这个细节被封装到 `HybridPICSolveE(..., this, solve_for_Faraday)` 里，因此 hybrid solver 的物理复杂性主要落在 FDTD solver 的专用分支里。

### 8.4 RK4 风格的 B 推进

`BfieldEvolveRK()` 对 `B` 做 4-stage RK 子步。源码清晰地保存 `B_old`，构造 `K`，然后按四步组合：

```cpp
// Step 1:
FieldPush(..., 0.5_rt*dt, subcycling_half, ng, nodal_sync);
// Step 2:
FieldPush(..., 0.5_rt*dt, subcycling_half, ng, nodal_sync);
// Step 3:
FieldPush(..., dt, subcycling_half, ng, nodal_sync);
// Step 4:
FieldPush(..., 0.5_rt*dt, subcycling_half, ng, nodal_sync);
```

最后用 `K0/K1/K2/K3` 组装 `B^{n+1}`。这表明 hybrid PIC 的磁场推进不是简单欧拉步，而是显式稳定性更好的 RK 子循环。

`FieldPush()` 的顺序是：

1. `CalculatePlasmaCurrent()`
2. `HybridPICSolveE(..., solve_for_Faraday=true)`
3. `EvolveB()`
4. `FillBoundaryE/B()`

```cpp
// Calculate J = curl x B / mu0 - J_ext
CalculatePlasmaCurrent(Bfield, eb_update_E);
// Calculate the E-field from Ohm's law
HybridPICSolveE(Efield, Jfield, Bfield, rhofield, eb_update_E, true);
...
// Push forward the B-field using Faraday's law
warpx.EvolveB(dt, subcycling_half, t_old);
```

### 8.5 外部场分裂

如果设置了外部 vector potential，Hybrid PIC 会在推进前把外场减掉、推进后再加回去：

```cpp
if (add_external_fields) {
    m_hybrid_pic_model->m_external_vector_potential->UpdateHybridExternalFields(
        gett_old(0),
        0.5_rt*dt[0]);

    for (int lev = 0; lev <= finest_level; ++lev) {
        for (int idim = 0; idim < 3; ++idim) {
            MultiFab::Subtract(
                *m_fields.get(FieldType::Bfield_fp, Direction{idim}, lev),
                *m_fields.get(FieldType::hybrid_B_fp_external, Direction{idim}, lev),
                0, 0, 1,
                m_fields.get(FieldType::Bfield_fp, Direction{idim}, lev)->nGrowVect());
        }
    }
}
```

这类 split-field 处理和前面的 PML 外场分离是同一个思路：避免把外部场和自洽场混在同一推进器里。

## 9. 小结：隐式和 hybrid 的依赖关系

这一组代码的依赖顺序是：

1. `WarpX::ReadParameters()` 按 `evolve_scheme` 选择 `SemiImplicitEM`、`ThetaImplicitEM` 或 `StrangImplicitSpectralEM`。
2. `ImplicitSolver` 负责统一的粒子/场耦合接口、质量矩阵和非线性迭代准备。
3. `NonlinearSolvers` 提供 Picard / Newton / PETSc SNES 与 GMRES/KSP 的通用实现。
4. `ThetaImplicitEM`、`SemiImplicitEM`、`StrangImplicitSpectralEM` 负责把各自物理 stencil 写成 `ComputeRHS()`。
5. `HybridPICModel` 负责 kinetic ions + fluid electrons 的 Ohm 定律闭合、外电流、电子压强和 RK B 推进。
6. `WarpXPushFieldsHybridPIC.cpp` 则把 hybrid 的每步时间推进串成一个稳定的 field-particle-coupling 算法。

从物理上看，隐式 EM 的核心是“把场和粒子耦合成一个非线性问题”；hybrid PIC 的核心是“把电子动力学替换成流体 Ohm 定律”。这两类方法都不再是显式 Maxwell PIC 的简单变体，而是各自引入了新的闭合假设、求解器抽象和数值稳定性边界。
