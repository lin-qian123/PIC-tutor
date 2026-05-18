# NonlinearSolvers 源码精读入口

绑定源码：`../warpx/Source/NonlinearSolvers`。

## 模块边界

- 构建入口：`NonlinearSolvers/CMakeLists.txt`、`NonlinearSolvers/Make.package`。
- 主要文件：`NonlinearSolver.H`、`LinearSolver.H`、`NewtonSolver.H`、`PicardSolver.H`、`MatrixPC.H`、`JacobiPC.H`、`CurlCurlMLMGPC.H`、`WarpX_PETSc.*`。
- 关联模块：`FieldSolver/ImplicitSolvers`。

## 核心问题

- WarpX 隐式 solver 需要什么 vector、operator、preconditioner 抽象。
- Newton/Picard/KSP/SNES 如何组织残差、Jacobian 和 preconditioner。
- PETSc wrapper 和 AMReX MLMG preconditioner 的边界。

## 精读顺序

1. solver 抽象：`LinearSolver.H`、`NonlinearSolver.H`。
2. `NewtonSolver.H`、`PicardSolver.H`。
3. preconditioner：`MatrixPC.H`、`JacobiPC.H`、`CurlCurlMLMGPC.H`。
4. PETSc wrapper。
5. 与 `FieldSolver/ImplicitSolvers` 对接。

## 输出目标

- `00-solver-abstractions.md`：已建立，覆盖 `NonlinearSolver.H`、`LinearSolver.H`、`Preconditioner.H`、`PicardSolver.H`、`NewtonSolver.H`、`WarpX_PETSc.cpp` 和 `MatrixPC.H` / `CurlCurlMLMGPC.H` 的抽象层。
- `01-newton-picard.md`：已建立，覆盖 Picard 固定点迭代、Newton 残差线性化、`Ops::ComputeRHS()` 契约、`WarpX_PETSc.cpp` 残差/Jacobian 回调和线性求解参数。
- `02-preconditioners-and-petsc.md`：已建立，覆盖 `MatrixPC`、`CurlCurlMLMGPC`、PETSc 向量/矩阵桥接、SNES/KSP wrapper 和隐式电磁预条件器结构。
- `03-residual-jacobian-operator-chain.md`：已建立，覆盖 `ThetaImplicitEM` / `SemiImplicitEM::ComputeRHS()`、`NewtonSolver::EvalResidual()`、`JacobianFunctionMF::apply()`、PETSc shell operator / native preconditioner 回调，以及 `JacobiPC` / `CurlCurlMLMGPC` / `MatrixPC` 的真实消费链。
- `04-petsc-matrixpc-assembly-chain.md`：已建立，覆盖 `StrangImplicitSpectralEM::ComputeRHS()`、SNES Jacobian callback、`assemblePCMatrix()`、`KSPSetOperators(A,P)` 双对象模式，以及 `MatrixPC::Assemble()` 如何把 curl-curl 与 `MassMatrices_PC` 写成 PETSc 稀疏矩阵。
- `05-warpxsolverdof-and-matrixpc-geometry.md`：已建立，覆盖 `WarpXSolverDOF` 的 `{local,global}` 编号契约、dot-mask 裁剪、`WarpXSolverVec` 与线性向量的映射，以及 `MatrixPC::Assemble()` 在 1D / XZ / RZ / 3D / RCYLINDER 下的 curl-curl、mixed-derivative 和 `MassMatrices_PC` 行写入模式。
- `06-bcmask-massmatrix-window-and-petsc-submit.md`：已建立，覆盖 `ThetaImplicitEM::InitializeCurlCurlBCMasks()` 的边界系数预编码、`ImplicitSolver::InitializeMassMatrices()` / `GetMassMatricesPCnComp()` 的 PC 窗口裁剪、`PreLinearSolve()` 的 `MassMatrices_PC` 同步与缩放，以及 `assemblePCMatrix()` 的 device-to-host 行提交链。
- `07-implicit-regression-assertion-map.md`：已建立，覆盖 `Examples/Tests/implicit/` 中 `analysis_petsc_matrix.py`、`analysis_planar_pinch.py`、`analysis_implicit.py` 等脚本分别在验证 DOF 映射、矩阵装配、预条件器质量、能量账本和 Gauss 定律的哪些层次。
- `08-vandb-jfnk-validation-map.md`：已建立，覆盖 `analysis_vandb_jfnk_2d.py`、`analysis_vandb_jfnk_2d_cropping.py` 与对应输入如何分别验证 `JFNK + Villasenor` 的 periodic 守恒、filtering 后守恒、以及 PEC / absorbing / cropping / suborbit 组合下的局部 charge conservation。

## 验证线索

- `Examples/Tests/implicit/`
