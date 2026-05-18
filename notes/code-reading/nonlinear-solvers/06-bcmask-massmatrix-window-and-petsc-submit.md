# `curl2_BC_mask`、`MassMatrices_PC` 窗口裁剪与 PETSc 行提交链

绑定源码：

- `../warpx/Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.H`
- `../warpx/Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp`
- `../warpx/Source/NonlinearSolvers/WarpX_PETSc.cpp`

前一篇 `05-warpxsolverdof-and-matrixpc-geometry.md` 已经把：

- `WarpXSolverDOF` 的 `{local,global}` 编号契约
- `MatrixPC::Assemble()` 在各几何下的局域行写入模式

讲清了。这一篇继续补另外三块还没闭合的来源链：

1. `BC_mask_Edir_arr` 这些 mask 到底从哪里来；
2. `GetMassMatricesPCnComp()` 返回的窗口宽度是怎样从 Jacobian mass matrices 裁出来的；
3. `assemblePCMatrix()` 怎样把 WarpX 本地的 device 行存数组交给 PETSc `Mat`。

## 1. `GetCurl2BCmask()` 本身没有逻辑，真正的逻辑在 `InitializeCurlCurlBCMasks()`

`ThetaImplicitEM::GetCurl2BCmask()` 只是把之前分配好的 field 取回来：

```cpp
const amrex::MultiFab* mask = m_WarpX->m_fields.get(FieldType::curl2_BC_mask,
                                                    Direction{field_dir}, lev);
```

因此 `MatrixPC::Assemble()` 里看到的 `BC_mask_Edir_arr` 并不是临时计算的，而是 `ThetaImplicitEM::Define()` 时预先建好的静态系数场。

初始化条件也很明确：

```cpp
const PreconditionerType pc_type = m_nlsolver->GetPreconditionerType();
if (pc_type == PreconditionerType::pc_petsc) { InitializeCurlCurlBCMasks(); }
```

也就是说，这套 mask 不是 implicit solver 的通用基础设施，而是专门为了 `pc_petsc` 这条显式矩阵装配路径准备的。

## 2. `curl2_BC_mask` 的分量数直接对应不同几何下的 stencil 结构

`InitializeCurlCurlBCMasks()` 先按几何分配不同分量数：

```cpp
#if defined(WARPX_DIM_1D_Z)
const int ncomps_Ex = 2; const int ncomps_Ey = 2; const int ncomps_Ez = 0;
#elif defined(WARPX_DIM_RCYLINDER) || defined(WARPX_DIM_RSPHERE)
const int ncomps_Ex = 0; const int ncomps_Ey = 2; const int ncomps_Ez = 2;
#elif defined(WARPX_DIM_XZ) || defined(WARPX_DIM_RZ)
const int ncomps_Ex = 3; const int ncomps_Ey = 4; const int ncomps_Ez = 3;
#elif defined(WARPX_DIM_3D)
const int ncomps_Ex = 6; const int ncomps_Ey = 6; const int ncomps_Ez = 6;
#endif
```

这和 `MatrixPC::Assemble()` 的几何模板是一一对应的：

- 1D：只需要“二阶对角项 / 邻点项”两类 mask；
- XZ/RZ：in-plane 分量需要“对角 / 邻点 / cross-term”三类，out-of-plane 分量需要两组二阶项，共四类；
- 3D：每个分量都要同时覆盖两组横向二阶项和两组 mixed derivative，一共六类。

因此 `BC_mask_Edir_arr(i,j,k,comp)` 不是通用标签，而是“第 `comp` 类 stencil 条目在这个边界点上应该乘多少”的预编码表。

## 3. 这些 mask 不是布尔量，而是经过边界条件重写后的实际 stencil 系数

`InitializeCurlCurlBCMasks()` 并不只写 `0/1`。例如 out-of-plane path：

```cpp
if (bc_type == FieldBoundaryType::PEC){
    val0 = 0.0_rt;
    val1 = 0.0_rt;
}
if (bc_type == FieldBoundaryType::PMC){
    val0 = 1.0_rt;
    val1 = 2.0_rt;
}
if (bc_type == FieldBoundaryType::Absorbing_SilverMueller) {
    val0 = 0.5_rt;
    val1 = 1.0_rt;
}
```

in-plane path 还会写三元组：

```cpp
val0 = ...; // diagonal
val1 = ...; // off-diagonal 2nd derivative
val2 = ...; // cross term
```

因此这些 mask 的真正角色不是“开关某个条目”，而是把边界处原本的 centered stencil 直接改写成满足 PEC、PMC、Silver-Mueller、PECInsulator 的离散系数。例如源码注释已经明确：

> `[1 -2 1] ==> [0 -2 2]`

所以 `MatrixPC::Assemble()` 里乘上的不是“是否保留该项”，而是“该项在边界重构后应该取什么系数”。

## 4. `PECInsulator` 和轴线例外说明 mask 已经吸收了几何细节

在 RZ / RCYLINDER 中，`InitializeCurlCurlBCMasks()` 对 `PECInsulator` 和 axis `None` 还会继续改写：

```cpp
const amrex::Real geom_p = ibdry_real / (ibdry_real + 0.5_rt);
const amrex::Real geom_m = ibdry_real / (ibdry_real - 0.5_rt);
```

然后写出诸如：

```cpp
val0_Et = (bdry_side == 0 ? geom_p : geom_m) / (geom_p + geom_m);
val1_Et = 1.0_rt;
```

或轴线下：

```cpp
val0 = 2.0_rt;
val1 = 4.0_rt;
val2 = 4.0_rt;
```

这说明圆柱几何下的边界修正不是靠 `MatrixPC` 装配时临时识别的，而是在 mask 构造阶段已经吸收了：

- `1/r` 几何修正
- axis 特例
- `PECInsulator` 的 `E`-set / `B`-set 区分

因此后续矩阵行生成只需要机械地乘这些 mask 值即可。

## 5. `GetMassMatricesPCnComp()` 只是取值器，窗口真正来源于 `InitializeMassMatrices()`

`ImplicitSolver.H` 里：

```cpp
int GetMassMatricesPCnComp (const int field_dir, const int space_dir) const
{
    if      (field_dir == 0) { return m_ncomp_pc_xx[space_dir]; }
    else if (field_dir == 1) { return m_ncomp_pc_yy[space_dir]; }
    else if (field_dir == 2) { return m_ncomp_pc_zz[space_dir]; }
}
```

这说明 `MatrixPC::Assemble()` 并不决定 PC mass matrix 的 stencil 尺寸；它只是读取 `m_ncomp_pc_*`。

真正的来源在 `InitializeMassMatrices()`。

## 6. `mass_matrices_pc_width` 是用户可控裁剪宽度，但 3D 被硬限制为零宽

在 `parseNonlinearSolverParams()` 里：

```cpp
if (m_use_mass_matrices_pc) {
    m_mass_matrices_pc_width = 0;
#if AMREX_SPACEDIM != 3
    pp.query("mass_matrices_pc_width", m_mass_matrices_pc_width);
#endif
}
```

而同时：

```cpp
#if defined(WARPX_DIM_3D)
WARPX_ALWAYS_ASSERT_WITH_MESSAGE(
    !m_use_mass_matrices_jacobian,
    "Using mass matrices for jacobian can not be used for DIM = 3");
#endif
```

这两段合起来说明：

- 在 1D / 2D，PC 可以通过 `mass_matrices_pc_width` 保留一个有限局域窗口；
- 在 3D，当前并不允许 Jacobian mass matrices 路径，因此 PC 侧实际上只保留最窄的局域近似。

这也解释了为什么前一篇里 `MatrixPC::Assemble()` 在 3D 的 `MassMatrices_PC` 仍然是“同分量局域 stencil”，而没有继续扩成更宽的 3D 张量块。

## 7. `m_ncomp_pc_xx/yy/zz` 是在 Jacobian 窗口上再做一次裁剪

`InitializeMassMatrices()` 在已经得到完整 `m_ncomp_xx/yy/zz` 后，PC 窗口这样生成：

```cpp
const int ncomp_dir_pc = (m_use_mass_matrices_jacobian ? 1 + 2*m_mass_matrices_pc_width : 1);
for (int dir=0; dir<AMREX_SPACEDIM; dir++) {
    m_ncomp_pc_xx[dir] = std::min(m_ncomp_xx[dir],ncomp_dir_pc);
    m_ncomp_pc_yy[dir] = std::min(m_ncomp_yy[dir],ncomp_dir_pc);
    m_ncomp_pc_zz[dir] = std::min(m_ncomp_zz[dir],ncomp_dir_pc);
}
```

因此 PC 的 mass matrix 宽度不是独立重新推导，而是：

1. 先按实际 deposition 算法和 shape 得到完整 Jacobian 窗口 `m_ncomp_*`；
2. 再按 `mass_matrices_pc_width` 把 diagonal block `xx/yy/zz` 裁短；
3. 最终只把裁短后的 `m_ncomp_pc_xx/yy/zz` 暴露给 `MatrixPC`、`JacobiPC`、`CurlCurlMLMGPC`。

## 8. `MassMatrices_PC` 当前只从 `xx/yy/zz` 三条对角块提取，不带 `xy/xz/...` 交叉块

`InitializeMassMatrices()` 只给 PC 分配：

```cpp
FieldType::MassMatrices_PC, Direction{0}
FieldType::MassMatrices_PC, Direction{1}
FieldType::MassMatrices_PC, Direction{2}
```

而 `PreLinearSolve()` 里真正填充它们时，也是从：

```cpp
MM_xx = FieldType::MassMatrices_X, Direction{0}
MM_yy = FieldType::MassMatrices_Y, Direction{1}
MM_zz = FieldType::MassMatrices_Z, Direction{2}
```

裁出来：

```cpp
amrex::MultiFab::Add(*MM_PC[0], *MM_xx, ...)
amrex::MultiFab::Add(*MM_PC[1], *MM_yy, ...)
amrex::MultiFab::Add(*MM_PC[2], *MM_zz, ...)
```

所以当前 `pc_petsc` 的 `M_PC` 不是完整九块响应张量，而是：

- 只保留 `xx/yy/zz` 三个同分量块；
- 并且只保留这三个块中心附近的局域窗口。

这和前面看到的 `MatrixPC::Assemble()` 只使用 `sigma_ii_arr` 完全一致。

## 9. `PreLinearSolve()` 里，`MassMatrices_PC` 在装配前还要经过同步和边界处理

`PreLinearSolve()` 对 PC 路径的顺序是：

```cpp
SyncMassMatricesPCAndApplyBCs();
SetMassMatricesForPC(theta_dt);
```

而 `SyncMassMatricesPCAndApplyBCs()` 内部先：

```cpp
m_WarpX->SyncMassMatricesPC();
```

再：

```cpp
m_WarpX->ApplyJfieldBoundary(... FieldType::MassMatrices_PC ...)
```

这说明 `MatrixPC::Assemble()` 读到的 `MassMatrices_PC` 已经不是原始沉积结果，而是已经过：

- overlap/addOp 交换
- J-field 边界条件
- 后续 `c^2 mu0 theta dt` 缩放

的预处理版本。

## 10. `SetMassMatricesForPC()` 说明 `pc_petsc` 和 `pc_curl_curl_mlmg` 对单位阵的处理边界不同

`SetMassMatricesForPC()` 先统一缩放：

```cpp
const amrex::Real pc_factor = PhysConst::c2 * PhysConst::mu0 * a_theta_dt;
MMxx_PC->mult(pc_factor, 0, MMxx_PC->nComp());
```

然后只在 `pc_curl_curl_mlmg` 下额外对角加一：

```cpp
if (pc_type == PreconditionerType::pc_curl_curl_mlmg) {
    MMxx_PC->plus(1.0_rt, diag_comp_Mxx, 1, 0);
}
```

源码注释明确写了：

> `pc_type petsc already has the one from the curl curl operator`

因此：

- 对 `pc_curl_curl_mlmg`，单位阵需要直接塞进 `MassMatrices_PC`；
- 对 `pc_petsc`，单位阵由 `MatrixPC::Assemble()` 自己先写，`MassMatrices_PC` 不再重复加一。

## 11. `assemblePCMatrix()` 的 ownership 模型是“WarpX 决定本地行，PETSc 决定全局分发”

在 `KSP_impl::createObjects()` 里，`Mat P` 的尺寸设成：

```cpp
MatSetSizes(this->m_P->obj,
            this->m_ndofs_l, this->m_ndofs_l,
            PETSC_DETERMINE, PETSC_DETERMINE);
```

这里 local 行/列大小来自 `WarpXSolverDOF` 的本 rank DOF 数 `m_ndofs_l`，global 大小交给 PETSc 通过 communicator 自行确定。

这意味着 row ownership 契约是：

- WarpX 先决定“我这一 rank 拥有哪几行”；
- PETSc 再据此建立全局 `Mat` 的并行分块。

`assemblePCMatrix()` 后面逐行调用 `MatSetValues()` 时，只对本 rank 的 `n = m_ndofs_l` 行提交条目：

```cpp
for (int i = 0; i < n; i++) {
    PetscCall(MatSetValues(... &h_r_indices_g[i], ...));
}
```

所以这条链并没有再做任何二次 repartition；它完全沿用 `WarpXSolverDOF` 给出的 local row 拥有关系。

## 12. PETSc 提交链是 `device row-store -> host vectors -> MatSetValues -> assembly`

`assemblePCMatrix()` 的流程很薄，但边界很清楚：

1. 先从 linop 取出 device 端行存数组：

```cpp
a_linop->getPCMatrix(r_indices_g, n_nz_cols, c_indices_g, a_ij, n, ncols_max);
```

2. 再一次性拷回 host：

```cpp
amrex::Gpu::copy(deviceToHost, ...);
```

3. 最后逐行提交给 PETSc：

```cpp
MatSetValues(m_P->obj, 1, &h_r_indices_g[i], h_n_nz_cols[i],
             &h_c_indices_g[i*ncols_max], &h_a_ij[i*ncols_max], INSERT_VALUES);
```

4. 统一做：

```cpp
MatAssemblyBegin(m_P->obj, MAT_FINAL_ASSEMBLY);
MatAssemblyEnd(m_P->obj, MAT_FINAL_ASSEMBLY);
```

因此当前 `pc_petsc` 不是 device-native 稀疏矩阵直接就地装配；它是：

- WarpX 在 GPU/CPU 侧生成本地 CSR-like 行存格式；
- 再搬回 host；
- 再交给 PETSc 做最终 `Mat` 装配。

## 13. 预分配是非常保守的，真正的非零个数靠后续放宽错误选项承接

CPU 路径下的预分配是：

```cpp
MatMPIAIJSetPreallocation(this->m_P->obj, 1, NULL, 1, NULL);
MatSetOption(this->m_P->obj, MAT_NEW_NONZERO_LOCATION_ERR, PETSC_FALSE);
MatSetOption(this->m_P->obj, MAT_NEW_NONZERO_ALLOCATION_ERR, PETSC_FALSE);
```

这说明 WarpX 没有把 `MatrixPC` 的真实 stencil 宽度提前精确告诉 PETSc，而是：

- 先用极保守的最小预分配启动；
- 允许后续 `MatSetValues()` 增加新列位置和触发额外分配。

所以性能上这条路显然不是“最强预分配”实现，它优先保证的是功能正确和接口简单。

## 14. `pc_petsc` 的提交链在 nonlinear / linear 两条路径里都会触发

`KSP_impl::solve()` 中：

```cpp
if (m_linop->pcType() == PreconditionerType::pc_petsc) {
    auto err = assemblePCMatrix(m_linop);
}
```

而 SNES Jacobian callback 中也有：

```cpp
if (strcmp(pctype,PCNONE) && strcmp(pctype,PCSHELL)) {
    auto err = context->assemblePCMatrix(context->m_linop.get());
}
```

这说明：

- 纯 KSP 线性求解时，每次 `solve()` 前直接重装配 `P`；
- SNES / JFNK 非线性求解时，每次 PETSc 请求 Jacobian 更新时也会重装配 `P`。

所以 `assemblePCMatrix()` 不只是初始化动作，而是迭代过程中反复消费 `MatrixPC` 当前状态的接口。

## 15. 现在可以把这条来源链完整闭合

对 `pc_petsc`，当前完整路径是：

1. `ThetaImplicitEM::Define()` 发现 preconditioner 是 `pc_petsc`，于是预先构造 `curl2_BC_mask`。
2. `ImplicitSolver::InitializeMassMatrices()` 按 deposition 算法、shape 和 `mass_matrices_pc_width` 决定 `m_ncomp_pc_xx/yy/zz`，并分配 `MassMatrices_PC`。
3. `PreLinearSolve()` 在每次线性化前同步、裁边并缩放 `MassMatrices_PC`。
4. `MatrixPC::Assemble()` 读取：
   - `WarpXSolverDOF` 的 local/global 编号
   - `curl2_BC_mask`
   - `MassMatrices_PC`
   把本 rank 的局域行存条目写到 device 数组。
5. `assemblePCMatrix()` 把这些 device 数组拷到 host，并逐行 `MatSetValues()` 提交给 PETSc `Mat P`。
6. `KSPSetOperators(A,P)` 让 PETSc 用 shell `A` 做 Jacobian 乘法、用显式 `P` 做 PC。

这意味着 `pc_petsc` 的正确性不是只靠 `MatrixPC::Assemble()` 一层决定，而是同时依赖：

- DOF 编号
- 边界 mask 预编码
- `MassMatrices_PC` 窗口裁剪与边界同步
- PETSc 并行矩阵的本地行提交

四个环节一起闭合。

## 16. 下一层最自然的继续方向

- 继续追 `ApplyJfieldBoundary()` 对 `MassMatrices_PC` 的具体修改规则，把“PC 边界处理”直接连回 boundary 模块。
- 继续追 GPU 路径下 `MATAIJCUSPARSE` / `MATAIJHIPSPARSE` 的真实装配行为，确认当前 host 提交方式在设备后端的代价边界。
- 若要做真实性验证，下一步应切回 `Examples/Tests/implicit/`，把这些矩阵装配链和 `petsc_matrix` / `planar_pinch` 的硬断言对上。
