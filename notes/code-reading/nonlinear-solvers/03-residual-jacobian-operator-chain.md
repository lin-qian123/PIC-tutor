# residual 到 Jacobian / preconditioner 的消费链

绑定源码：

- `../warpx/Source/NonlinearSolvers/NewtonSolver.H`
- `../warpx/Source/NonlinearSolvers/JacobianFunctionMF.H`
- `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp`
- `../warpx/Source/NonlinearSolvers/JacobiPC.H`
- `../warpx/Source/NonlinearSolvers/CurlCurlMLMGPC.H`
- `../warpx/Source/NonlinearSolvers/MatrixPC.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/SemiImplicitEM.cpp`

前两篇 `nonlinear-solvers/01` 和 `02` 已经分别解释了：

- Picard / Newton 怎样迭代；
- `MatrixPC`、`JacobiPC`、`CurlCurlMLMGPC` 各是什么类型的 preconditioner。

还缺最后一块：WarpX 在一次 Newton / GMRES / PETSc 线性求解里，究竟怎样把

1. 物理 `ComputeRHS()`
2. 非线性残差 `F(U)`
3. matrix-free Jacobian 方向作用
4. preconditioner `Apply()`

串成一条实际可运行的 operator 链。

## 1. `ThetaImplicitEM::ComputeRHS()` / `SemiImplicitEM::ComputeRHS()` 给出的不是残差本身，而是物理右端 `R(U)`

先看 implicit solver 子类。`ThetaImplicitEM::ComputeRHS()` 的结构是：

```cpp
UpdateWarpXFields( a_E, start_time );

const amrex::Real theta_time = start_time + m_theta*m_dt;
PreRHSOp( theta_time, a_nl_iter, a_from_jacobian );

m_WarpX->ImplicitComputeRHSE( m_theta*m_dt, a_RHS);
```

`SemiImplicitEM::ComputeRHS()` 则是：

```cpp
const amrex::Real half_time = start_time + 0.5_rt*m_dt;
m_WarpX->SetElectricFieldAndApplyBCs( a_E, half_time );

PreRHSOp( half_time, a_nl_iter, a_from_jacobian );

m_WarpX->ImplicitComputeRHSE(0.5_rt*m_dt, a_RHS);
```

两者共同点非常重要：

- `a_E` 是 nonlinear solver 当前给出的场猜测；
- `PreRHSOp()` 会据此推进粒子并沉积 `J^{n+1/2}`；
- `ImplicitComputeRHSE()` 才把 `curl(B) - \mu_0 J` 之类的物理右端真正写进 `a_RHS`。

因此 `ComputeRHS()` 返回的是

$$
R(U),
$$

而不是最终要交给 Newton 的残差 `F(U)`。

## 2. `NewtonSolver::EvalResidual()` 把物理右端包装成标准非线性残差

真正的 Newton 残差在 `NewtonSolver::EvalResidual()` 里定义：

```cpp
m_ops->ComputeRHS( m_R, a_U, a_time, a_iter, false );

// Compute residual: F(U) = U - b - R(U)
a_F.Copy(a_U);
a_F -= m_R;
a_F -= a_b;
```

也就是说，WarpX 把隐式系统统一写成

$$
F(U)=U-b-R(U)=0.
$$

这里：

- `U` 是当前未知量，比如 `E^{n+\theta}` 或 `E^{n+1/2}`；
- `b` 是上一步的已知场向量；
- `R(U)` 是上一节说的“给定当前场猜测后，粒子推进和 Maxwell 右端重新组装出来的物理响应”。

这一步很关键，因为后面所有 Jacobian / GMRES / PETSc 都是在处理 `F(U)`，不是直接处理 `R(U)`。

## 3. `JacobianFunctionMF::apply()` 用有限差分近似 `dF/dU`

WarpX 的 Jacobian 默认是 matrix-free。`JacobianFunctionMF::apply()` 里核心是：

```cpp
m_Z.linComb( 1.0, m_Y0, eps, a_dU ); // Z = Y0 + eps*dU
m_ops->ComputeRHS(m_R, m_Z, m_cur_time, -1, true );

// F(Y) = Y - b - R(Y) ==> dF = dF/dY*dU = [1 - dR/dY]*dU
a_dF.linComb( 1.0, a_dU, eps_inv, m_R0 );
a_dF.increment(m_R,-eps_inv);
```

把它按公式展开就是：

$$
J_F(U_0)\,\delta U
\approx
\delta U-\frac{R(U_0+\epsilon\delta U)-R(U_0)}{\epsilon}.
$$

这说明 `JacobianFunctionMF` 的 operator 不是“重新写一套隐式 Maxwell Jacobian”，而是：

1. 取基态 `Y0 = U_0`；
2. 沿方向 `dU` 做一次扰动；
3. 再调用同一个 `ComputeRHS()`；
4. 用差商构造 `dF/dU` 的方向作用。

所以 WarpX 的 matrix-free JFNK 关键不是手推完整 Jacobian，而是保证：

- `ComputeRHS()` 在 `a_from_jacobian=true` 时仍然逻辑一致；
- 粒子和场的线性化近似在这个调用模式下是可重复、可微近似的。

## 4. `setBaseSolution()` 和 `setBaseRHS()` 给 finite-difference Jacobian 提供锚点

`JacobianFunctionMF` 之所以能做差商，是因为每次 nonlinear residual 评估后，都会保存一组基态：

```cpp
void setBaseSolution ( const T&  a_U )
{
    m_Y0.Copy(a_U);
    m_normY0 = this->norm2(m_Y0);
}

void setBaseRHS ( const T&  a_R )
{
    m_R0.Copy(a_R);
}
```

在 PETSc SNES 路径里，这一步在 `SNES_impl::computeRHS()` 之后立刻完成：

```cpp
dynamic_cast<JacobianFunctionMF<VecType,TIType>*>(m_linop.get())->setBaseSolution(a_U);
dynamic_cast<JacobianFunctionMF<VecType,TIType>*>(m_linop.get())->setBaseRHS(a_F);
```

因此 finite-difference Jacobian 的基准点不是某个隐含的全局状态，而是“刚刚用于 residual 评估的那一份 `U` 和 `R(U)`”。

## 5. `a_from_jacobian=true` 会把 `ComputeRHS()` 切到 linear-stage 语义

`JacobianFunctionMF::apply()` 调 `ComputeRHS()` 时最后一个参数是 `true`：

```cpp
m_ops->ComputeRHS(m_R, m_Z, m_cur_time, -1, true );
```

这会一路传进 `ImplicitSolver::PreRHSOp()`，从而触发不同于普通 nonlinear residual 的路径：

- JFNK linear stage 时允许只推进 suborbit 粒子；
- 非 suborbit 粒子可改用 `ComputeJfromMassMatrices()` 的 `J0 + MM(E-E0)` 近似；
- `PreLinearSolve()` 的刷新时机也可能变化。

所以 `JacobianFunctionMF` 看似只是在做数值差分，实际上它依赖 `ComputeRHS(..., from_jacobian=true)` 提供一套与 linear stage 相容的物理近似。

## 6. `LinearFunction::precond()` 走的是完全独立于 `apply()` 的另一条链

`JacobianFunctionMF` 同时还定义了：

```cpp
void precond ( T& a_U, const T& a_X ) override
{
    if (m_usePreCond) {
        a_U.zero();
        m_preCond->Apply(a_U, a_X);
    } else {
        a_U.Copy(a_X);
    }
}
```

因此在 GMRES 或 PETSc KSP 看来，有两类完全不同的回调：

- `apply()`：近似 `J_F(U)\,\delta U`
- `precond()`：近似求解某个更容易的线性系统 `P x = b`

这两者共享同一套物理对象，但语义并不相同。前者是 Jacobian 的方向作用，后者是人工构造的近似逆。

## 7. PETSc 的 `applyMatOp` / `applyNativePC` 只是把 WarpX 回调接到 KSP/SNES

在 `WarpX_PETSc.cpp` 里，PETSc shell matrix 的 operator apply 很薄：

```cpp
copyVec( context->m_U, a_U );
context->applyOp( context->m_F, context->m_U, context->m_linop );
copyVec( a_F, context->m_F);
```

而 native preconditioner 也是：

```cpp
copyVec( context->m_U, a_X );
context->applyPC( context->m_F, context->m_U, linop );
copyVec( a_Y, context->m_F );
```

继续往下看：

```cpp
a_linop->apply(a_F, a_U);
...
a_linop->precond(a_F, a_U);
```

所以 PETSc 在这里并没有改变 WarpX 的物理或 Jacobian 定义。它只是把 WarpX 已经实现好的

- `apply()`
- `precond()`

接成了 PETSc 需要的 `MatShell` / `PCShell` 回调。

## 8. `JacobiPC::Apply()` 解的是一个局域固定点修正问题

`JacobiPC::Apply()` 先做纯对角初值：

```cpp
x_arr(i,j,k) = b_arr(i,j,k)
    / (RT(1.0) + a_arr(i,j,k,diag_comp));
```

若存在 off-diagonal mass-matrix stencil，再做松弛修正：

```cpp
mx += a_arr(i,j,k,comp) * xg_arr(ii,jj,kk);
...
const RT r = b_arr(i,j,k) - w_arr(i,j,k);
x_arr(i,j,k) += om * r
    / (RT(1.0) + a_arr(i,j,k,diag_comp));
```

这里解的不是完整 Maxwell Jacobian，而是一个局域近似系统：

$$
(I+M_{\rm PC})x \approx b
$$

再用若干次 weighted Jacobi 把局域耦合补进去。

因此 `JacobiPC` 的本质不是“矩阵对角线求逆”，而是“以对角部分为基底，对本地 mass-matrix stencil 做少量平滑迭代”。

## 9. `CurlCurlMLMGPC::Apply()` 解的是 curl-curl 椭圆系统

`CurlCurlMLMGPC::Apply()` 的注释写得更直接：

```cpp
//  Given a right-hand-side b, solve:
//      A x = b
//  where A is the linear operator, in this case, the curl-curl
//  operator:
//      A x = curl (alpha * curl (x) ) + beta * x
```

实际执行时，它把 `WarpX` 的 `Efield_fp` 排布改造成 AMReX `MLCurlCurl` 期待的分量顺序，然后调用：

```cpp
m_curl_curl->prepareRHS({&rhs});
if (m_use_gmres) {
    m_gmres_solver->solve(solution, rhs, m_rtol, m_atol);
} else {
    m_solver->solve({&solution}, {&rhs}, m_rtol, m_atol);
}
```

因此 `CurlCurlMLMGPC` 是真正“解一个预条件椭圆问题”的 operator-form preconditioner，不是简单局域平滑。

## 10. `MatrixPC` 在 native 路径里不求解，只负责装配给外部库

`MatrixPC::Apply()` 当前直接 abort：

```cpp
WARPX_ABORT_WITH_MESSAGE("MatrixPC<T,Ops>::Apply() - native matrix solvers not implemented. Use with external library, eg, PETSc.");
```

这说明 `MatrixPC` 的定位不是 native WarpX 里自己解 `Ax=b`，而是：

1. 用 `Assemble()` 把 preconditioner 稀疏矩阵装配出来；
2. 由 PETSc 或其他外部 sparse solver 真正消费。

所以当 `pc_type = pc_petsc` 时，重点不在 `MatrixPC::Apply()`，而在 `assemblePCMatrix()` 和 PETSc 的 `PCSetOperators()` / 外部 KSP 路径。

## 11. 现在可以把一次 Newton / GMRES 线性求解链完整写出来

把上面几层拼起来，一次 implicit Newton 迭代里与线性求解相关的主链是：

1. `ThetaImplicitEM::ComputeRHS()` 或 `SemiImplicitEM::ComputeRHS()` 根据当前场猜测重组物理右端 `R(U)`。
2. `NewtonSolver::EvalResidual()` 形成 `F(U)=U-b-R(U)`。
3. `JacobianFunctionMF::setBaseSolution()` / `setBaseRHS()` 保存本次 residual 的线性化基态。
4. GMRES / PETSc KSP 请求 Jacobian 方向作用时，`JacobianFunctionMF::apply()` 用差商近似 `J_F(U)\,\delta U`。
5. 若启用 preconditioner，则 `JacobianFunctionMF::precond()` 调用 `JacobiPC`、`CurlCurlMLMGPC` 或外部 `MatrixPC` 路径来近似求解 `P x = b`。
6. PETSc 只是把 `apply()` / `precond()` 映射成 shell matrix 和 shell preconditioner 回调，不改变前面的物理定义。

## 12. 这一层最容易看错的地方

- `ComputeRHS()` 不是残差，而是 `R(U)`。
- Newton 真正线性化的是 `F(U)=U-b-R(U)`，不是单独线性化 `R(U)`。
- `apply()` 和 `precond()` 虽然都依赖同一套 mass matrices / field state，但一个表示 Jacobian 方向作用，一个表示近似逆，不能混为一谈。
- PETSc 在这里不是“另一个算法”，而是 WarpX 本地 operator 的外层调度器。
