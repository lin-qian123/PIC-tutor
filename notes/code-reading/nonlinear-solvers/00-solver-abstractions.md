# NonlinearSolvers 抽象层源码精读

绑定源码：

- `../warpx/Source/NonlinearSolvers/NonlinearSolver.H`
- `../warpx/Source/NonlinearSolvers/LinearSolver.H`
- `../warpx/Source/NonlinearSolvers/Preconditioner.H`
- `../warpx/Source/NonlinearSolvers/PicardSolver.H`
- `../warpx/Source/NonlinearSolvers/NewtonSolver.H`
- `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp`
- `../warpx/Source/NonlinearSolvers/MatrixPC.H`
- `../warpx/Source/NonlinearSolvers/CurlCurlMLMGPC.H`
- `../warpx/Docs/source/usage/parameters.rst:252-320`

隐式 PIC 的核心不是某个单独的数值公式，而是一个完整的 solver 栈：

1. `Ops` 负责定义残差 `ComputeRHS()`。
2. `Vec` 负责承载解向量和残差向量。
3. `NonlinearSolver` 负责 Picard / Newton / PETSc SNES 的迭代框架。
4. `LinearSolver` 负责 Newton 线性化阶段的 GMRES / KSP。
5. `Preconditioner` 负责构造和应用近似 Jacobian 或近似 curl-curl operator。

这层抽象让 `ThetaImplicitEM`、`SemiImplicitEM`、`StrangImplicitSpectralEM` 只需要关心“物理残差怎么写”，而不需要分别实现 Picard、Newton、GMRES、PETSc SNES。

## 1. `NonlinearSolver`：统一的非线性求解接口

`NonlinearSolver` 的接口很短，但含义很重。它要求继承类实现 `Define()`、`Solve()`、`PrintParams()`、`GetSolverParams()`：

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

约定是：

- Picard 求 `U = b + R(U)`。
- Newton 求 `F(U)=U-b-R(U)=0`。

这和显式推进器不同。这里残差是 solver 的中心，而不是时间推进的附带量。

## 2. `LinearSolver`：Newton 线性化阶段的通用接口

`LinearSolver` 只做一件事：解 `A x = b`。它是给 Jacobian 线性化用的：

```cpp
template <typename Vec, typename Ops>
class LinearSolver
{
public:
    virtual void define(Ops& linop) = 0;
    virtual void solve(Vec& a_sol,
                        Vec const& a_rhs,
                        RT a_tol_rel,
                        RT a_tol_abs,
                        int a_its=-1) = 0;
```

在 WarpX 里，Newton 的线性 solver 可以是 AMReX GMRES，也可以是 PETSc KSP。也就是说，`LinearSolver` 不是 PETSc 专属，而是把线性代数后端隐藏起来。

## 3. `Preconditioner`：Jacobians / operators 的近似逆

`Preconditioner<T,Ops>` 是一个更底层的抽象。它要求：

```cpp
template <class T, class Ops>
class Preconditioner
{
public:
    virtual void Define (const T&, Ops*) = 0;
    virtual void Update ( const T& a_U ) = 0;
    virtual void Apply (T& a_x, const T& a_b) = 0;
```

这里有两个重要分支：

- `MatrixPC`：显式组装 sparse matrix 形式的 Jacobian 近似，再交给外部线性代数库解。
- `CurlCurlMLMGPC`：把 preconditioner 写成 curl-curl operator，用 AMReX MLMG 求近似解。

`CurlCurlMLMGPC` 的注释已经把数学形式写出来：

$$
\nabla\times\left(\alpha\nabla\times \mathbf E\right)+\beta \mathbf E=\mathbf b.
$$

```cpp
/**
 * \brief Curl-curl Preconditioner
 *
 *  Preconditioner that solves the curl-curl equation for the E-field, given
 *  a RHS. Uses AMReX's curl-curl linear operator and multigrid solver.
 */
```

它之所以重要，是因为 theta-implicit / semi-implicit 的线性阶段本质上都离不开近似 Maxwell operator。

## 4. `PicardSolver`：固定点迭代

Picard solver 的物理含义是“给定当前 guess 的场，重算 RHS，再回代更新解”。源码定义很直接：

```cpp
// Picard fixed-point iteration method to solve nonlinear
// equation of form: U = b + R(U)
```

参数由 `picard.*` 读取：

```cpp
const amrex::ParmParse pp_picard("picard");
pp_picard.query("verbose",             this->m_verbose);
pp_picard.query("absolute_tolerance",  m_atol);
pp_picard.query("relative_tolerance",  m_rtol);
pp_picard.query("max_iterations",      m_maxits);
pp_picard.query("require_convergence", m_require_convergence);
```

`Solve()` 的循环就是标准 fixed-point iteration：

```cpp
// Update the solver state (a_U = a_b + m_R)
m_ops->ComputeRHS( m_R, a_U, a_time, iter, false );
a_U.Copy(a_b);
a_U += m_R;
```

这意味着 Picard 的收敛性完全依赖物理系统的非线性强度和 time step。参数文档里说它适合小步长，就是这个原因。

## 5. `NewtonSolver`：PS-JFNK

Newton solver 把问题写成

$$
F(U)=U-b-R(U)=0.
$$

源码里它保存 residual `m_F`、增量 `m_dU`、rhs `m_R`，再把 Jacobian 线性化器交给 `JacobianFunctionMF`：

```cpp
m_dU.Define(a_U);
m_F.Define(a_U); // residual function F(U) = U - b - R(U) = 0
m_R.Define(a_U); // right hand side function R(U)

m_linear_function = std::make_unique<JacobianFunctionMF<Vec,Ops>>();
m_linear_function->define(m_F, m_ops, m_pc_type);
```

线性 solver 由参数选择：

```cpp
if (m_linear_solver_type == LinearSolverType::amrex_gmres) {
    m_linear_solver = std::make_unique<AMReXGMRES<Vec,JacobianFunctionMF<Vec,Ops>>>();
} else if (m_linear_solver_type == LinearSolverType::petsc_ksp) {
    m_linear_solver = std::make_unique<PETScKSP<Vec,JacobianFunctionMF<Vec,Ops>>>();
}
```

Newton 的关键不是“更高级”，而是它允许把 particle update 和 field update 的耦合写成 Jacobian-free residual / linear solve 的组合，这就是 PS-JFNK。

参数解析里也能看出它和粒子迭代、mass matrices 的耦合：

```cpp
pp.query("max_particle_iterations", m_max_particle_iterations);
pp.query("particle_tolerance", m_particle_tolerance);
pp.query("particle_suborbits", m_particle_suborbits);
pp.query("use_mass_matrices_jacobian", m_use_mass_matrices_jacobian);
pp.query("use_mass_matrices_pc", m_use_mass_matrices_pc);
```

如果启用了 mass matrices for Jacobian，Newton 会用更便宜的粒子响应近似替代直接粒子计算。这个设计是隐式 PIC 的性能关键。

## 6. PETSc SNES：把 Newton 包成外部非线性框架

WarpX 的 PETSc 路径在 `WarpX_PETSc.cpp` 中包装成 `SNES_impl`。构造函数先读 `newton` 和 `gmres` 参数，再设置 Jacobian / PC：

```cpp
const amrex::ParmParse pp_newton("newton");
pp_newton.query("verbose",             m_verbose);
pp_newton.query("absolute_tolerance",  m_atol);
pp_newton.query("relative_tolerance",  m_rtol);
pp_newton.query("max_iterations",      m_maxits);

const amrex::ParmParse pp_gmres("gmres");
pp_gmres.query("verbose_int",         m_verbose_l);
pp_gmres.query("absolute_tolerance",  m_atol_l);
pp_gmres.query("relative_tolerance",  m_rtol_l);
pp_gmres.query("max_iterations",      m_maxits_l);
```

核心 PETSc 对象是：

```cpp
SNESCreate(PETSC_COMM_WORLD, &m_snes->obj);
SNESSetType( m_snes->obj, SNESNEWTONLS );
SNESSetFunction(m_snes->obj, nullptr, RHSFunction, this);
```

Jacobian 和 preconditioner 有两条路：

```cpp
if (this->m_pc_type != PreconditionerType::pc_petsc) {
    PCSetType(pc, PCSHELL);
    PCShellSetApply(pc, applyNativePC);
    SNESSetJacobian(m_snes->obj, this->m_A->obj, this->m_A->obj, JacobianFunction, this);
} else {
    PCSetFromOptions(pc);
    SNESSetJacobian(m_snes->obj, this->m_A->obj, this->m_P->obj, JacobianFunction, this);
}
```

也就是说，WarpX 既能走自定义 preconditioner，也能把 PETSc 自己的 PC 接进来。这里的 boundary / operator 约束，后面都落在 `JacobianFunctionMF` 和 `Preconditioner` 具体实现里。

`solve()` 最后直接调用 `SNESSolve()`，再读回迭代次数、线性迭代次数和收敛原因：

```cpp
SNESSolve(m_snes->obj, this->m_b->obj, this->m_x->obj);

SNESGetIterationNumber(m_snes->obj, &m_niters);
SNESGetLinearSolveIterations(m_snes->obj, &m_niters_l);
SNESGetConvergedReason( m_snes->obj, &reason );
```

## 7. `MatrixPC` 和 `CurlCurlMLMGPC`

`MatrixPC` 的用途是把 Jacobian 组装成 sparse matrix。它维护 CSR-like index/value vectors：

```cpp
amrex::Gpu::DeviceVector<int> m_r_indices_g;
amrex::Gpu::DeviceVector<int> m_num_nz;
amrex::Gpu::DeviceVector<int> m_c_indices_g;
amrex::Gpu::DeviceVector<amrex::Real> m_a_ij;
```

`CurlCurlMLMGPC` 则是 curl-curl preconditioner：

```cpp
/**
 * \brief Curl-curl Preconditioner
 *
 *  Preconditioner that solves the curl-curl equation for the E-field, given
 *  a RHS. Uses AMReX's curl-curl linear operator and multigrid solver.
 */
```

它的参数包括：

- `verbose`
- `bottom_verbose`
- `agglomeration`
- `consolidation`
- `max_iter`
- `max_coarsening_level`
- `relative_tolerance`
- `absolute_tolerance`

这和 `ThetaImplicitEM` / `SemiImplicitEM` 里提到的 `GetThetaForPC()` 是联动的：preconditioner 需要知道 time-step fraction，才能把光波项和 plasma response 写成近似可解的 operator。

## 8. 小结

`NonlinearSolvers` 这一层的角色可以概括成：

- `NonlinearSolver` 决定外层固定点或 Newton 迭代框架。
- `LinearSolver` 决定 Newton 的线性化后端。
- `Preconditioner` 决定 Jacobian 的近似逆。
- `PicardSolver` 适合较温和的非线性和小时间步。
- `NewtonSolver` 适合大步长但依赖更强的线性/预条件设计。
- PETSc SNES 只是把同一套物理残差换成 PETSc 非线性框架去跑。

对隐式 PIC 来说，真正的难点不是把一个方程解出来，而是把“粒子推进 -> 沉积 -> 场更新 -> 预条件器”这一整套闭环做成可收敛、可分辨、可跨维度的 solver 体系。
