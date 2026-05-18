# 预条件器与 PETSc 适配

绑定源码与文档：

- `../warpx/Source/NonlinearSolvers/Preconditioner.H`
- `../warpx/Source/NonlinearSolvers/MatrixPC.H`
- `../warpx/Source/NonlinearSolvers/CurlCurlMLMGPC.H`
- `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverVec.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/WarpXSolverDOF.H`
- `../warpx/Docs/source/usage/parameters.rst:252-320`

这篇讲的是 Newton / PETSc 链路里的“线性代数侧”。如果说上一节回答的是“怎么迭代”，那这一节回答的是“每次迭代里那个线性问题怎么近似、怎么求解、怎么和 WarpX 的场容器对接”。

WarpX 在这层里主要有两类预条件器实现：

1. `MatrixPC`：显式组装稀疏 Jacobian 矩阵。
2. `CurlCurlMLMGPC`：用 AMReX 的 curl-curl operator 和 multigrid 求解器构造预条件器。

PETSc 侧则负责把 WarpX 的 `Vec` / `Mat` / `PC` 回调接进 SNES/KSP。

## 1. 预条件器接口

`Preconditioner<T, Ops>` 是统一抽象。它并不规定预条件器一定是矩阵，也不规定一定是 multigrid，只要求：

- `Define(const T&, Ops*)`
- `Update(const T&)`
- `Apply(T&, const T&)`
- `printParameters()`

`MatrixPC` 和 `CurlCurlMLMGPC` 都是这个接口的具体实现。

## 2. `MatrixPC`：显式稀疏矩阵预条件

`MatrixPC` 的注释把边界讲得很清楚：

```cpp
/**
 * \brief Matrix Preconditione
 *
 *  This class is templated on a solution-type class T and an operator class Ops. It implements
 *  a preconditioner based on constructing and solving the sparse matrix representation of the
 *  Jacobian. Currently, it implements constructing/assembling the sparse matrix. An external
 *  library with sparse matrix solvers (for example, PETSc) is needed to apply the preconditioner.
 */
```

它的核心状态不是一个单独矩阵，而是 GPU 端可搬运的稀疏结构：

```cpp
amrex::Gpu::DeviceVector<int> m_r_indices_g;
amrex::Gpu::DeviceVector<int> m_num_nz;
amrex::Gpu::DeviceVector<int> m_c_indices_g;
amrex::Gpu::DeviceVector<amrex::Real> m_a_ij;
```

再加上网格几何、AMR 层数和是否包含 mass matrices 等信息：

```cpp
int m_num_amr_levels = 0;
amrex::Vector<amrex::Geometry> m_geom;
int m_ndofs_l = 0;
int m_ndofs_g = 0;
bool m_pc_diag_only = false;
int m_pc_mat_nnz = 1;
bool m_include_mass_matrices = false;
```

`MatrixPC` 的用途很直接：把 Jacobian 的局部 stencil 显式装配成矩阵，再交给外部求解器求解或近似求解。它更适合结构明确、局部耦合可枚举的问题。

`insertOrAdd()` 这个 helper 体现了装配时最关键的逻辑：如果同一个列索引已经存在，就累加；不存在就插入新列。

```cpp
bool insertOrAdd( const int a_cidx,
                  const amrex::Real a_val,
                  int* const a_cidxs,
                  amrex::Real* const a_aij,
                  const int a_nnz,
                  int& a_ncol )
```

这说明 `MatrixPC` 不是“把矩阵写死”，而是逐点累积局部算子贡献。

## 3. `CurlCurlMLMGPC`：curl-curl + multigrid

这个 preconditioner 更接近隐式电磁场的物理结构。它的注释明确写了求解对象：

```cpp
/**
 * \brief Curl-curl Preconditioner
 *
 *  Preconditioner that solves the curl-curl equation for the E-field, given
 *  a RHS. Uses AMReX's curl-curl linear operator and multigrid solver.
 *
 *  The equation solves for Eg in:
 *  curl ( alpha * curl ( Eg ) ) + beta * Eg = b
 */
```

这和隐式 Maxwell 方程非常贴近。因为隐式 EM 的线性化阶段常常会落成类似

$$
\nabla\times(\alpha \nabla\times E) + \beta E = b
$$

这样的系统。

它的运行参数包括：

- `verbose`
- `bottom_verbose`
- `agglomeration`
- `consolidation`
- `max_iter`
- `max_coarsening_level`
- `absolute_tolerance`
- `relative_tolerance`
- `use_gmres`
- `use_gmres_pc`

对应代码是：

```cpp
const amrex::ParmParse pp(amrex::getEnumNameString(PreconditionerType::pc_curl_curl_mlmg));
pp.query("verbose", m_verbose);
pp.query("bottom_verbose", m_bottom_verbose);
pp.query("max_iter", m_max_iter);
pp.query("agglomeration", m_agglomeration);
pp.query("consolidation", m_consolidation);
pp.query("max_coarsening_level", m_max_coarsening_level);
pp.query("absolute_tolerance",  m_atol);
pp.query("relative_tolerance",  m_rtol);
pp.query("use_gmres",  m_use_gmres);
pp.query("use_gmres_pc",  m_use_gmres_pc);
```

这个类和 `MatrixPC` 的最大差别在于：它不显式存储完整稀疏 Jacobian，而是直接用 AMReX 的 `MLCurlCurl` / `MLMGT` / `GMRESMLMGT` 进行预条件求解。

## 4. PETSc wrapper：把 WarpX 语义映射到 SNES/KSP

`WarpX_PETSc.cpp` 是 PETSc 适配层。它的作用不是自己发明求解器，而是把 WarpX 的 vector / linear operator / preconditioner 接到 PETSc 的回调机制里。

最基本的桥接是向量拷贝：

```cpp
void copyVec(VecType& a_wvec, const Vec& a_pvec)
{
    const PetscScalar* Yarr;
    VecGetArrayRead(a_pvec,&Yarr);
    a_wvec.copyFrom( static_cast<const amrex::Real*>(Yarr) );
    VecRestoreArrayRead(a_pvec,&Yarr);
}
```

和反向拷贝：

```cpp
void copyVec( Vec& a_pvec, const VecType& a_wvec)
{
    PetscScalar* Yarr;
    VecGetArray(a_pvec,&Yarr);
    a_wvec.copyTo( static_cast<amrex::Real*>(Yarr) );
    VecRestoreArray(a_pvec,&Yarr);
}
```

PETSc SNES 的残差函数则把 WarpX 的 `computeRHS()` 包装进去：

```cpp
PetscErrorCode RHSFunction( SNES a_solver, Vec a_U, Vec a_F, void* ctxt)
{
    SNES_impl *context = (SNES_impl*) ctxt;
    copyVec(context->m_U, a_U);
    context->computeRHS(context->m_F, context->m_U);
    copyVec(a_F, context->m_F);
    VecAXPBY(a_F, 1.0, -1.0, a_U);
```

Jacobian 回调则在需要时更新 preconditioner matrix：

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

这说明 WarpX 里 PETSc 不是一个黑盒替换件，而是一个严格受控的外壳：

- 残差怎么定义，仍然由 WarpX 决定。
- Jacobian / PC 怎么更新，也由 WarpX 决定。
- PETSc 只负责外层迭代框架和线性代数调度。

## 5. 与隐式 EM 的对应关系

前一篇已经讲过，隐式 EM 的核心 `Ops` 是 `ImplicitSolver` 子类。到预条件层面，这些对象通常通过：

- `WarpXSolverVec`
- `WarpXSolverDOF`
- `JacobianFunctionMF`
- `Preconditioner`

把物理场、自由度组织成可以求解的代数系统。

所以这里的正确阅读方式是：

1. 先看非线性残差是什么。
2. 再看 Jacobian 怎么近似。
3. 最后才看 PETSc 或 MLMG 具体如何求。

## 6. 这一层的结论

- `MatrixPC` 适合显式装配 Jacobian。
- `CurlCurlMLMGPC` 适合隐式电磁里的 curl-curl 结构。
- PETSc wrapper 不改变物理，只改变求解框架。
- WarpX 的 Newton/PETSc 路径本质上是“物理残差 + 可插拔线性代数内核”的组合。
