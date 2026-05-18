# Newton / Picard 非线性求解器细读

绑定源码与文档：

- `../warpx/Source/NonlinearSolvers/NewtonSolver.H`
- `../warpx/Source/NonlinearSolvers/PicardSolver.H`
- `../warpx/Source/NonlinearSolvers/NonlinearSolver.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/SemiImplicitEM.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/StrangImplicitSpectralEM.cpp`
- `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp`
- `../warpx/Docs/source/usage/parameters.rst:252-320`

这一篇只讲非线性求解“怎么迭代”，不讲 preconditioner 具体怎么做矩阵或 multigrid。WarpX 的隐式推进本质上把场和粒子耦合成一个非线性方程

$$
F(U) = U - b - R(U) = 0
$$

其中：

- `U` 是未知量，一般是场向量，也可能包含某些辅助量。
- `b` 是显式部分或已知项。
- `R(U)` 是通过 `Ops::ComputeRHS()` 计算出的非线性响应。

Picard 和 Newton 的差别就在于：Picard 直接迭代固定点，Newton 线性化残差并求解 Jacobian 方向修正。

## 1. `NonlinearSolver` 的接口约定

`NewtonSolver` 和 `PicardSolver` 都是 `NonlinearSolver<Vec, Ops>` 的具体实现。它们共享的不是物理方程，而是接口契约：

```cpp
template<class Vec, class Ops>
class NonlinearSolver
{
public:
    virtual void Define ( const Vec&, Ops* ) = 0;
    virtual void Solve ( Vec&, const Vec&, amrex::Real, amrex::Real, int) const = 0;
    virtual void PrintParams () const = 0;
    virtual void GetSolverParams (amrex::Real&, amrex::Real&, int&) = 0;
```

关键点是 `Ops` 必须提供 `ComputeRHS()`。这意味着非线性求解器本身不关心隐式物理细节，它只负责：

1. 调 `Ops::ComputeRHS()` 评估残差或右端。
2. 根据算法类型更新 `U`。
3. 判断收敛。

这也是为什么 `ImplicitSolver` 会把自己当作 `Ops` 传给 `NewtonSolver` / `PicardSolver`：隐式 EM 的粒子推进、沉积、场更新都封装在 `ComputeRHS()` 里。

## 2. Picard：固定点迭代

Picard 的注释已经把数学形式写死了：

```cpp
/**
 * \brief Picard fixed-point iteration method to solve nonlinear
 *  equation of form: U = b + R(U). U is the solution vector. b
 *  is a constant. R(U) is some nonlinear function of U, which
 *  is computed in the Ops function ComputeRHS().
 */
```

源码里的核心循环非常直接：

```cpp
for (iter = 0; iter < m_maxits;) {

    // Save previous state for norm calculation
    m_Usave.Copy(a_U);

    // Update the solver state (a_U = a_b + m_R)
    m_ops->ComputeRHS( m_R, a_U, a_time, iter, false );
    a_U.Copy(a_b);
    a_U += m_R;

    // Compute the step norm and update iter
    m_Usave -= a_U;
    norm_abs = m_Usave.norm2();
```

物理上它做的事情就是反复把“当前猜测的场和粒子状态”代入右端项，直到固定点不再变化。

Picard 的优点是结构简单、实现稳、对某些弱非线性问题足够用。缺点也明确：收敛速度慢，强耦合时容易迭代次数很大。

## 3. Newton：残差线性化

Newton 的定义更接近数值分析里的标准方程：

```cpp
/**
 * \brief Newton method to solve nonlinear equation of form:
 * F(U) = U - b - R(U) = 0. U is the solution vector, b is a constant,
 * and R(U) is some nonlinear function of U, which is computed in the
 * ComputeRHS() Ops function.
 */
```

它的 `Define()` 会准备三类中间量：

```cpp
m_dU.Define(a_U);
m_F.Define(a_U); // residual function F(U) = U - b - R(U) = 0
m_R.Define(a_U); // right hand side function R(U)

m_ops = a_ops;

m_linear_function = std::make_unique<JacobianFunctionMF<Vec,Ops>>();
m_linear_function->define(m_F, m_ops, m_pc_type);
```

这说明 Newton 的核心不是“把方程直接解掉”，而是先把残差 `F(U)` 和 Jacobian 方向导数对象准备好，再交给线性求解器。

在 WarpX 里，Newton 常和 matrix-free Jacobian 搭配使用。`WarpX_PETSc.cpp` 中的 PETSc 残差回调就是这个逻辑的外壳：

```cpp
PetscErrorCode RHSFunction( SNES a_solver, Vec a_U, Vec a_F, void* ctxt)
{
    SNES_impl *context = (SNES_impl*) ctxt;
    copyVec(context->m_U, a_U);
    context->computeRHS(context->m_F, context->m_U);
    copyVec(a_F, context->m_F);
    VecAXPBY(a_F, 1.0, -1.0, a_U);
```

这里 `a_F` 最后变成 `R(U) - U` 或等价的残差形式。也就是说，WarpX 不是把 Newton 写成纯数学符号，而是把它落成 PETSc SNES 需要的残差回调。

Jacobian 回调则决定线性化阶段是否需要重新装配预条件矩阵：

```cpp
PetscErrorCode JacobianFunction( SNES a_solver,
                                 Vec a_U,
                                 Mat a_A,
                                 Mat a_P,
                                 void* ctxt )
{
    ...
    if (strcmp(pctype,PCNONE) && strcmp(pctype,PCSHELL)) {
        copyVec(context->m_U, a_U);
        auto err = context->assemblePCMatrix(context->m_linop.get());
        AMREX_ALWAYS_ASSERT(err == PETSC_SUCCESS);
    }
```

这一步和 Picard 的差别是本质性的：

- Picard 只求固定点，不显式构造 Jacobian。
- Newton 需要 Jacobian 的方向作用，哪怕这个 Jacobian 是 matrix-free 的。

## 4. 迭代参数和收敛判据

两个求解器都维护相似的参数：

- 相对/绝对容差。
- 最大迭代步数。
- 是否强制收敛。
- 诊断输出。

Picard 的参数解析是：

```cpp
const amrex::ParmParse pp_picard("picard");
pp_picard.query("verbose",             this->m_verbose);
pp_picard.query("absolute_tolerance",  m_atol);
pp_picard.query("relative_tolerance",  m_rtol);
pp_picard.query("max_iterations",      m_maxits);
pp_picard.query("require_convergence", m_require_convergence);
```

Newton 的成员变量则更细，包括线性求解器、预条件器、restart length 等：

```cpp
amrex::Real m_linsol_rtol = 1.0e-4;
amrex::Real m_linsol_atol = 0.;
int m_linsol_maxits = 1000;
int m_linsol_restart_length = 30;
PreconditionerType m_pc_type = PreconditionerType::none;
LinearSolverType m_linear_solver_type = LinearSolverType::amrex_gmres;
```

这说明 WarpX 的 Newton 并不是“一个函数”，而是一个嵌套结构：

1. 外层 nonlinear iteration。
2. 内层 linear solve。
3. 可选 preconditioner。

## 5. `ComputeRHS()` 是真正的物理接口

不管 Picard 还是 Newton，真正决定物理正确性的函数都不是求解器模板本身，而是 `Ops::ComputeRHS()`。

在隐式 EM 里，这个 `Ops` 就是具体的 `ImplicitSolver` 子类。也就是说，粒子隐式推进、场更新、边界处理、沉积、质量矩阵等，全部都要在重复求值时保持一致。

这也是阅读 WarpX 隐式路径时最重要的判断标准：

- 如果某个行为影响残差，就必须在 `ComputeRHS()` 里体现。
- 如果某个行为只影响线性化或预条件，就应该落在 Jacobian/PC 路径里。

## 6. 这篇笔记对应源码阅读时应该抓住的结论

- Picard 是固定点迭代，Newton 是残差线性化。
- `ComputeRHS()` 是两者共同依赖的物理核。
- `WarpX_PETSc.cpp` 只是把 WarpX 的向量和回调适配到 PETSc SNES/KSP。
- 隐式推进的复杂性主要不在求解器模板，而在 `Ops` 具体如何重新组装场和粒子状态。
