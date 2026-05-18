# `pc_petsc` 稀疏矩阵装配链：`StrangImplicitSpectralEM`、`assemblePCMatrix()` 与 `MatrixPC::Assemble()`

绑定源码：

- `../warpx/Source/FieldSolver/ImplicitSolvers/StrangImplicitSpectralEM.cpp`
- `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp`
- `../warpx/Source/NonlinearSolvers/MatrixPC.H`
- `../warpx/Source/NonlinearSolvers/JacobianFunctionMF.H`

前一篇 `03-residual-jacobian-operator-chain.md` 已经把

- `R(U)`
- `F(U)=U-b-R(U)`
- `JacobianFunctionMF::apply()`
- native `precond()`

这条 operator 链讲清了。这一篇继续往下补 `pc_petsc` 特有的支线：当 preconditioner 不是 native shell，而是 PETSc 自己消费的稀疏矩阵时，WarpX 到底怎样把本地 curl-curl + mass-matrix 近似写进 `Mat`。

## 1. `StrangImplicitSpectralEM::ComputeRHS()` 是 implicit solver 里最特殊的 `R(U)` 之一

前面 theta / semi-implicit 都是通过 `ImplicitComputeRHSE()` 生成右端。`StrangImplicitSpectralEM` 不一样：

```cpp
UpdateWarpXFields( a_E, half_time );

PreRHSOp( half_time, a_nl_iter, a_from_jacobian );

// For Strang split implicit PSATD, the RHS = -dt*mu*c**2*J
a_RHS.Copy(FieldType::current_fp, warpx::fields::FieldType::None, allow_type_mismatch);
amrex::Real constexpr coeff = PhysConst::c2 * PhysConst::mu0;
a_RHS.scale(-coeff * 0.5_rt*m_dt);
```

也就是说，这条支线的非线性右端不是 curl-curl Maxwell 组合，而是直接把隐式中段的粒子电流写成

$$
R(U)=-\frac{\Delta t}{2}\mu_0 c^2 J^{n+1/2}.
$$

因此在 Strang implicit spectral EM 中：

- source-free Maxwell 部分由前后两次 `SpectralSourceFreeFieldAdvance()` 处理；
- nonlinear solver 只负责中间那段“由电流驱动的 E 更新”。

这解释了为什么同样是 `ComputeRHS()`，Strang 路径和 theta / semi-implicit 的物理语义并不一样。

## 2. `pc_petsc` 的 Jacobian callback 不调用 native `Apply()`，而是触发一次矩阵重装配

在 PETSc SNES 路径里，`JacobianFunction()` 的关键分支是：

```cpp
if (strcmp(pctype,PCNONE) && strcmp(pctype,PCSHELL)) {
    copyVec(context->m_U, a_U);
    auto err = context->assemblePCMatrix(context->m_linop.get());
    AMREX_ALWAYS_ASSERT(err == PETSC_SUCCESS);
}
```

这里的语义很明确：

- 如果 PETSc 当前用的是 `PCSHELL`，WarpX 继续走 native `precond()`；
- 如果不是 `PCSHELL`，WarpX 就要把自己的 preconditioner 近似先装配成 `Mat P`，再交给 PETSc 的 PC/KSP。

因此 `pc_petsc` 的分水岭不在 `JacobianFunctionMF::apply()`，而在 SNES Jacobian callback 是否要求一次新的 `assemblePCMatrix()`。

## 3. `KSP_impl::createObjects()` 明确把 `pc_petsc` 分成“shell operator + sparse PC matrix”双对象模式

PETSc 线性求解器初始化时有两个完全不同的分支。

若不是 `pc_petsc`：

```cpp
PCSetType(pc, PCSHELL);
PCShellSetApply(pc, applyNativePC);
KSPSetOperators( m_ksp->obj, this->m_A->obj, this->m_A->obj );
```

若是 `pc_petsc`：

```cpp
MatCreate( PETSC_COMM_WORLD, &this->m_P->obj );
MatSetType( this->m_P->obj, MATAIJ ... );
...
KSPSetOperators( m_ksp->obj, this->m_A->obj, this->m_P->obj );
```

这表示 WarpX 在 `pc_petsc` 模式下故意分离了：

- `A`：仍然是 matrix-free shell Jacobian operator；
- `P`：单独装配出来给 PETSc PC 使用的稀疏矩阵。

所以 `pc_petsc` 不是“把 Jacobian 全部显式化”，而是：

- Jacobian 仍然 matrix-free；
- 只有 preconditioner 近似被显式装配成 sparse matrix。

## 4. `assemblePCMatrix()` 本身很薄，它真正做的是“从 WarpX 本地稀疏描述搬进 PETSc Mat”

`PETScSolver_impl::assemblePCMatrix()` 的结构只有两步：

1. 让 WarpX 本地 linop 导出稀疏矩阵条目：

```cpp
a_linop->getPCMatrix( r_indices_g, n_nz_cols, c_indices_g, a_ij, n, ncols_max );
```

2. 把 GPU 端数组拷到 host，再逐行 `MatSetValues()`：

```cpp
for (int i = 0; i < n; i++) {
    PetscCall(MatSetValues( m_P->obj,
                            1,
                            &h_r_indices_g[i],
                            h_n_nz_cols[i],
                            &h_c_indices_g[i*ncols_max],
                            &h_a_ij[i*ncols_max],
                            INSERT_VALUES ));
}
```

最后统一 `MatAssemblyBegin/End`。

所以这一步不负责“推导矩阵”，它只负责：

- 从 WarpX 取出本地 CSR-like 行存格式；
- 在 PETSc 侧完成真实 `Mat` 装配。

## 5. `getPCMatrix()` 最终还是回到 `MatrixPC`

在 `JacobianFunctionMF` 里，PETSc 要的矩阵条目继续转发给 preconditioner：

```cpp
m_preCond->getPCMatrix(a_ridx_g, a_nnz, a_cidx_g, a_aij, a_n, a_ncols_max);
```

而当前真正实现这条接口的，是 `MatrixPC`。这也解释了为什么：

- `MatrixPC::Apply()` 可以不实现 native 解法；
- 但 `MatrixPC::Assemble()` 必须做得很细。

它的职责是“提供 PC 的显式稀疏表示”，不是“在 WarpX 内部亲自解这个线性系统”。

## 6. `MatrixPC::Assemble()` 写入的是 `A = I + curl(alpha curl[]) + M`

`MatrixPC::Assemble()` 一开始先无条件给每一行写入单位对角：

```cpp
const int cidx_g_lhs = dof_arr(i,j,k,1);
const amrex::Real val = 1.0_rt;
```

随后若 `thetaDt > 0`，再加入 curl-curl stencil。它先算

```cpp
const RT thetaDt = m_ops->GetThetaForPC()*this->m_dt;
const RT alpha = (thetaDt*PhysConst::c) * (thetaDt*PhysConst::c);
```

然后按几何分支把离散 curl-curl 的二阶差分和 mixed-derivative 耦合逐条 `insertOrAdd()` 写进本行。

最后若 `m_include_mass_matrices=true`，再把 `MassMatrices_PC` 的局域 stencil 写进去：

```cpp
const int cidx_g_rhs = dof_arr(iv_base + iv_shift,1);
const amrex::Real val = sigma_ii_arr(iv_base,mm_comp);
```

因此它真正形成的是

$$
A_{\rm PC} \approx I + \nabla\times(\alpha\nabla\times \cdot) + M_{\rm PC},
$$

而不是纯粹的 `curl-curl` 或纯粹的 `mass matrix`。

## 7. `insertOrAdd()` 的存在说明同一行里的多个物理来源会累加到同一列

`MatrixPC::Assemble()` 不是简单“按 stencil 顺序写值”。它每次都通过 `MatrixPCUtils::insertOrAdd(...)`：

- 若列索引第一次出现，就新增；
- 若该列已经存在，就把新贡献累加到旧值上。

这很重要，因为同一个矩阵元素可能同时收到：

- 单位阵贡献；
- curl-curl 对角项；
- mixed-derivative 交叉项；
- mass-matrix 局域耦合项。

所以 `MatrixPC` 的装配本质不是模板输出，而是“同一物理行的多来源局域耦合汇总”。

## 8. `MatrixPC::Assemble()` 的第一层组织单位不是物理分量名，而是 `WarpXSolverDOF`

装配时真正作为行列号锚点的是 DOF 映射：

```cpp
const auto& dofs_obj = a_U.getDOFsObject();
const auto& dofs_mfarrvec = dofs_obj->m_array;
...
const int ridx_l = dof_arr(i,j,k,0);
const int ridx_g = dof_arr(i,j,k,1);
```

这说明 `MatrixPC` 不是在“Ex 写一块、Ey 写一块、Ez 写一块”的抽象层上工作，而是在：

1. 先由 `WarpXSolverDOF` 把 staggered `Efield_fp` 展成全局自由度编号；
2. 再按每个 DOF 的局域 stencil 写全局稀疏矩阵条目。

因此如果后面要继续追 `pc_petsc` 的正确性，不能只盯着 `MatrixPC`，还要一起看 `WarpXSolverDOF` 的编号规则。

## 9. 现在可以把 `pc_petsc` 支线完整拼起来

当用户选择 PETSc 预条件器时，WarpX 当前走的是：

1. implicit solver 的 `ComputeRHS()` 仍然定义物理右端 `R(U)`。
2. Newton / JFNK 仍然通过 `JacobianFunctionMF::apply()` 做 matrix-free Jacobian 方向作用。
3. SNES Jacobian callback 发现 PC 不是 `PCSHELL` 后，触发 `assemblePCMatrix()`。
4. `assemblePCMatrix()` 调 `getPCMatrix()`，实际落到 `MatrixPC::Assemble()`。
5. `MatrixPC::Assemble()` 用 `WarpXSolverDOF`、curl-curl stencil 和 `MassMatrices_PC` 生成稀疏矩阵条目。
6. PETSc 再把这块显式 `Mat P` 当作自己的 preconditioner operator。

所以 `pc_petsc` 不是“WarpX 把一切都交给 PETSc”，而是：

- WarpX 继续定义物理残差和 Jacobian 方向作用；
- 只把 preconditioner 的近似线性算子显式输出给 PETSc 消费。

## 10. 当前还没继续下钻的两处

- `MatrixPC::Assemble()` 在不同几何维度下的 curl-curl / mixed-derivative 细节还可以再拆一层。
- `WarpXSolverDOF` 的 local/global row-column 编号如何保证与 staggered field 一致，还没单独成文。

这两处就是下一轮再往下打时最自然的入口。
