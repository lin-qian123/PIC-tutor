# 15 implicit Jacobian-preconditioner coupling：`J0 + MM*(E-E0)`、`MassMatrices_PC` 与 preconditioner 消费链

绑定源码：

- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.H`
- `../warpx/Source/NonlinearSolvers/MatrixPC.H`
- `../warpx/Source/NonlinearSolvers/JacobiPC.H`
- `../warpx/Source/NonlinearSolvers/CurlCurlMLMGPC.H`

前一轮 `particles/10-implicit-suborbit-mass-matrices-jfnk.md` 已经把粒子侧的分拆讲清了：implicit JFNK 不是把所有粒子重新推进一遍，而是把电流拆成

$$
J(E)=J_{\rm suborbit}+J_0+MM\,(E-E_0).
$$

这一篇继续补剩下半条链：`ImplicitSolver` 怎样把这三个量整理成 Jacobian 电流和 preconditioner 系数，并最终喂给 `MatrixPC`、`JacobiPC`、`CurlCurlMLMGPC`。

## 1. `InitializeMassMatrices()` 先决定 Jacobian 和 PC 各自需要多大的响应 stencil

`ImplicitSolver::InitializeMassMatrices()` 不是简单分配几块 `MultiFab`。它先看两件事：

1. `m_use_mass_matrices_jacobian`
2. `m_use_mass_matrices_pc`

如果 Jacobian 要用 mass matrices，就按真实 current deposition 算法和 shape order 给 `MassMatrices_X/Y/Z` 分配完整 stencil；如果只给 preconditioner 用，则把主质量矩阵宽度直接退化成纯对角：

```cpp
else { // Mass matrices used for PC only
    for (int dir=0; dir<AMREX_SPACEDIM; dir++) {
        m_ncomp_xx[dir] = 1;
        m_ncomp_xy[dir] = 0;
        ...
        m_ncomp_zz[dir] = 1;
    }
}
```

这意味着 `MassMatrices_X/Y/Z` 的“全响应”语义和 `MassMatrices_PC` 的“预条件器近似”语义从分配时就已经分叉，不是后面再临时截断。

## 2. `MassMatrices_PC` 不是独立沉积出来的一整套矩阵，而是从主 mass matrices 中裁剪出来的可消费近似

当 `m_use_mass_matrices_pc=true` 时，`InitializeMassMatrices()` 还会按 `m_mass_matrices_pc_width` 生成三块 `MassMatrices_PC`：

```cpp
m_ncomp_pc_xx[dir] = std::min(m_ncomp_xx[dir],ncomp_dir_pc);
m_ncomp_pc_yy[dir] = std::min(m_ncomp_yy[dir],ncomp_dir_pc);
m_ncomp_pc_zz[dir] = std::min(m_ncomp_zz[dir],ncomp_dir_pc);
```

这里有两个重要边界：

- 当前 PC 只稳定消费 `xx/yy/zz` 三个对角块；
- `pc_curl_curl_mlmg` 会把 `m_mass_matrices_pc_width` 强制收缩到 `0`，也就是只保留每个方向的纯对角响应。

所以 `MassMatrices_PC` 不是“另一次完整粒子线性化”，而是“从完整响应里裁出一块预条件器能稳妥消费的近似块”。

## 3. `PreLinearSolve()` 是 Jacobian / PC 两条 mass-matrix 路径的统一装配入口

线性求解前，`ImplicitSolver::PreLinearSolve()` 统一做：

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

这里三步各自的物理含义不同：

- `DepositMassMatrices()`：把粒子响应沉到 `MassMatrices_X/Y/Z`，并在需要时给 `MassMatrices_PC` 贡献 suborbit 近似。
- `FinishMassMatrices()`：把对称性省略掉的对角 mass-matrix 分量补齐。
- `SaveE()`：把当前 Newton 参考场保存成 `Efield_fp_save = E0`。
- `SyncMassMatricesPCAndApplyBCs()`：把主质量矩阵里的可用块拷到 `MassMatrices_PC`，并做 exchange + 边界。
- `SetMassMatricesForPC()`：乘上隐式方程里的物理系数，再按 preconditioner 类型决定是否加单位阵。

因此 `PreLinearSolve()` 不是普通“准备一下工作数组”，而是 implicit 线性化装配的主入口。

## 4. `SaveE()` 的作用是把 `MM` 明确绑定到当前 Newton 参考态 `E0`

`SaveE()` 只做一件事：

```cpp
amrex::MultiFab::Copy(*E0[0], *E[0], 0, 0, E[0]->nComp(), E[0]->nGrowVect());
```

它把当前 `Efield_fp` 复制到 `Efield_fp_save`。后面 `ComputeJfromMassMatrices()` 用的不是绝对场 `E`，而是

$$
\delta E = E - E_0.
$$

也就是说，WarpX 的 mass matrices 不是近似整个非线性函数 `J(E)`，而是近似参考态附近的 Fréchet 导数作用：

$$
J(E)\approx J_0 + MM\,(E-E_0).
$$

没有这一步，`MM` 就失去“围绕哪个状态线性化”的锚点。

## 5. `ComputeJfromMassMatrices()` 真正做的是 staggered-grid 上的离散卷积

`ComputeJfromMassMatrices()` 的实际代码远比“矩阵乘向量”更具体。它先为每个耦合块计算 offset：

```cpp
offset_xy[dir] = (Jx_nodal[dir] > Jy_nodal[dir]) ?  (m_ncomp_xy[dir]/2)
                                                 : ((m_ncomp_xy[dir]-1)/2);
```

然后在每个 `J` 分量上，对相应 `E` 分量的局域 stencil 做卷积，例如

```cpp
SxxdEx += Sxx(i,j,k,Nc)*( Ex(i+ii,j+jj,k+kk,n)
                      -  Ex0(i+ii,j+jj,k+kk,n) );
...
Jx(i,j,k,n) += Jx0(i,j,k,n) + SxxdEx + SxydEy + SxzdEz;
```

这说明这里的 `MM*(E-E0)` 不是抽象线性代数对象，而是：

- 每个 `Jx/Jy/Jz` 各自有一套局域响应 stencil；
- stencil 宽度随 deposition 算法、shape 阶数、staggering 变化；
- mixed terms `dJx/dEy`、`dJy/dEz` 等在 Jacobian 路径里是真实存在的。

因此 `ComputeJfromMassMatrices()` 的核心不是“省一次粒子推进”，而是“把粒子对场扰动的局域线性响应显式离散化到网格上”。

## 6. `a_J_from_MM_only` 决定 linear stage 是否还保留 suborbit 电流

`ComputeJfromMassMatrices()` 一开始会看：

```cpp
if (a_J_from_MM_only) {
    J[0]->setVal(0.0);
    J[1]->setVal(0.0);
    J[2]->setVal(0.0);
}
```

而 `PreRHSOp()` 在 JFNK linear stage 中给出的逻辑是：

```cpp
if (m_particle_suborbits) {
    options.evolve_suborbit_particles_only = true;
    m_WarpX->PushParticlesandDeposit(..., &options);
}
const bool J_from_MM_only = !options.evolve_suborbit_particles_only;
ComputeJfromMassMatrices( J_from_MM_only );
```

所以：

- 没有 suborbit 时，`current_fp` 先清零，整个 `J` 直接来自 `J0 + MM(E-E0)`；
- 有 suborbit 时，`current_fp` 里已经有 `J_suborbit`，`ComputeJfromMassMatrices()` 只在其上叠加 `J0 + MM(E-E0)`。

这正好把前一篇粒子笔记里的三项分拆真正落实到 field-solver 侧。

## 7. `SyncMassMatricesPCAndApplyBCs()` 把主质量矩阵裁成 preconditioner 可用的系数场

preconditioner 不直接读取 `MassMatrices_X/Y/Z`。`ImplicitSolver` 先把需要的对角块切到 `MassMatrices_PC`：

```cpp
amrex::MultiFab::Add(*MM_PC[0], *MM_xx, mm_comp_start, mm_pc_comp_start, m_ncomp_pc_xx[0], MM_xx->nGrowVect());
...
m_WarpX->SyncMassMatricesPC();
...
m_WarpX->ApplyJfieldBoundary(... FieldType::MassMatrices_PC ...)
```

这一步做了三件事：

1. 从完整 `MM_xx/MM_yy/MM_zz` 中裁出指定宽度的中心块；
2. 对 `MassMatrices_PC` 做 add-op exchange；
3. 把 `J` 型边界条件施加到 `MassMatrices_PC`。

所以 preconditioner 看到的不是粒子原始沉积结果，而是已经过“裁剪、通信、边界化”的可消费系数场。

## 8. `SetMassMatricesForPC()` 把纯粒子响应变成隐式线性算子里的 `beta`

preconditioner 真正要解的不是“裸 mass matrix”，而是类似

$$
\nabla\times(\alpha\nabla\times E)+\beta E=b
$$

里的 `beta` 部分。因此 `SetMassMatricesForPC()` 先乘物理系数：

```cpp
const amrex::Real pc_factor = PhysConst::c2 * PhysConst::mu0 * a_theta_dt;
MMxx_PC->mult(pc_factor, 0, MMxx_PC->nComp());
```

若使用 `pc_curl_curl_mlmg`，还要在对角项上补 `1`：

```cpp
MMxx_PC->plus(1.0_rt, diag_comp_Mxx, 1, 0);
```

这说明 `MassMatrices_PC` 在 deposit 结束后仍然不是最终 preconditioner 系数；还必须先乘上时间推进和 Maxwell 系统里的尺度因子，必要时再加单位阵，才会成为线性算子的 `beta` 系数。

## 9. 三类 preconditioner 消费 `MassMatrices_PC` 的方式并不一样

### 9.1 `MatrixPC`

`MatrixPC::Define()` 直接通过

```cpp
m_bcoefs = m_ops->GetMassMatricesCoeff();
```

拿到 `MassMatrices_PC` 指针。后面 `Assemble()` 构造的矩阵形式是：

```cpp
// A = curl (alpha * curl []) + M
```

其中 `alpha = (thetaDt*c)^2`，而 `M` 就来自 `m_bcoefs`。这类 preconditioner 会显式装配稀疏矩阵，因此它最像“把 `MassMatrices_PC` 当作离散线性算子的系数块直接塞进矩阵”。

### 9.2 `JacobiPC`

`JacobiPC` 同样读取 `m_bcoefs`，但它不组全矩阵，而是在 `Update()` 阶段只关心：

- 有没有 off-diagonal stencil；
- 最大 stencil width 多大；
- 是否需要 `x_ghost`。

也就是说，`JacobiPC` 消费 `MassMatrices_PC` 的方式更轻：它把这些系数当成局域块 Jacobi 的离散权重，而不是全局矩阵条目。

### 9.3 `CurlCurlMLMGPC`

`CurlCurlMLMGPC::Update()` 会把 `MassMatrices_PC` 直接设置为 MLMG 的 beta 系数：

```cpp
m_curl_curl->setBeta({Array<MultiFab const*,3>{ (*m_bcoefs)[n][0],
                                                (*m_bcoefs)[n][1],
                                                (*m_bcoefs)[n][2]}});
```

同时 `alpha` 仍由

```cpp
const RT alpha = (thetaDt*PhysConst::c) * (thetaDt*PhysConst::c);
m_curl_curl->setScalars(alpha, RT(1.0));
```

控制。这里 `MassMatrices_PC` 已经完全变成了 MLMG 椭圆算子里的多分量 `beta` 场，而不再以“粒子响应”名义出现。

## 10. `PreRHSOp()` 还决定了 `PreLinearSolve()` 在 native Newton 和 PETSc SNES 下的刷新时机

`PreLinearSolve()` 并不是每次 `ComputeRHS()` 都调用。`PreRHSOp()` 里写得很明确：

```cpp
if (m_nlsolver_type == NonlinearSolverType::petsc_snes && !a_from_jacobian) {
    PreLinearSolve();
}
```

源码注释说明 native Newton 会在真正需要线性求解前调用它，而 PETSc SNES 不提供同样优化，所以 WarpX 必须在 RHS 路径里主动刷新。

这意味着同一套 mass-matrix 装配逻辑在不同 nonlinear backend 下，调用时机并不完全相同；如果后面要看性能或迭代数，不能忽略这个 backend 差异。

## 11. 现在可以把 implicit 线性化链条完整拼起来

把粒子侧和 field-solver 侧合起来，当前 WarpX implicit JFNK / PC 的主链可以写成：

1. 粒子推进决定哪些粒子直接贡献 `J_suborbit`，哪些粒子线性化成 `J0 + MM(E-E0)`。
2. `DepositMassMatrices()` 把线性化响应沉到 `MassMatrices_X/Y/Z`，并在需要时给 `MassMatrices_PC` 加 suborbit 近似贡献。
3. `PreLinearSolve()` 调 `FinishMassMatrices()`、`SaveE()`、`SyncMassMatricesPCAndApplyBCs()`、`SetMassMatricesForPC()`。
4. linear stage 中 `ComputeJfromMassMatrices()` 把 `current_fp_non_suborbit`、`Efield_fp_save` 和 `MassMatrices_X/Y/Z` 重新拼成 `current_fp`。
5. `MatrixPC` / `JacobiPC` / `CurlCurlMLMGPC` 再通过 `GetMassMatricesCoeff()` 消费已经缩减并缩放过的 `MassMatrices_PC`。

因此这条链的核心不是“implicit solver 更复杂”这么泛泛一句，而是它把粒子响应拆成：

- 一个参考态电流 `J0`，
- 一个局域线性响应 `MM(E-E0)`，
- 一个只给 preconditioner 用的裁剪近似 `MassMatrices_PC`，
- 以及一个必须直接推进的剩余 `J_suborbit`。

只有把这四类对象分开，后面再看 `ThetaImplicitEM` / `SemiImplicitEM` 的残差、`JacobianFunctionMF` 的线性算子和 PETSc/MLMG 预条件器，才不会把“物理电流”“Jacobian 近似”和“预条件器系数”混成一类东西。
