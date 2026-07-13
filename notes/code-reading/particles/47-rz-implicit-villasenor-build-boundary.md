# RZ implicit Villasenor build boundary

审计日期：2026-07-12

## 两条启动路径

官方输入 `Examples/Tests/implicit/inputs_test_rz_theta_implicit_dynamic_pinch` 固定：

- `geometry.dims = RZ`
- `algo.current_deposition = "villasenor"`
- `implicit_evolve.nonlinear_solver = "newton"`
- `newton.linear_solver = petsc_ksp`

使用当前 `build_full` binary 和 2-rank launcher 时，官方路径在 `NewtonSolver::Define()` 直接拒绝：binary 未启用 `AMREX_USE_PETSC`。

随后做了一个仅在命令行覆盖参数的 project-local control：

```bash
FI_PROVIDER=tcp OMP_NUM_THREADS=1 \
  /Users/yuxiangzhang/anaconda3/envs/warpx-cpu-mpich-dev/bin/mpiexec -n 2 \
  /Volumes/PHILIPS/programs/PIC/warpx/build_full/bin/warpx.rz.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES \
  /Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/implicit/inputs_test_rz_theta_implicit_dynamic_pinch \
  newton.linear_solver=amrex_gmres
```

该 control 仍未进入物理时间推进，在：

```text
WarpX::InitData()
  -> ThetaImplicitEM::Define()
  -> ThetaImplicitEM::InitializeCurlCurlBCMasks()
```

触发 `SIGILL`。因此当前 RZ 结论应拆成两层：

1. 官方 PETSc 路径的直接 blocker 是 `AMREX_USE_PETSC` 未编译；
2. 非 PETSc `amrex_gmres` control 也在 RZ theta-implicit boundary-mask 初始化阶段失败。

这不是 Villasenor current kernel 的 physics pass 或 physics fail，因为粒子推进和 current deposition 尚未开始。当前 2D implicit Villasenor contracts 仍有效，但不能外推到 RZ theta-implicit；要关闭该缺口，需要具备兼容 PETSc/AMReX 构建的 RZ binary，或先定位当前 arm64 `InitializeCurlCurlBCMasks()` 的 `SIGILL`。

## 2026-07-13 复核

再次用同一 `build_full` binary、同一官方输入、`FI_PROVIDER=tcp`、`OMP_NUM_THREADS=1` 和 MPI=2 执行 `newton.linear_solver=amrex_gmres` control。结果稳定出现 `Defined DOF object for linear solves (total DOFs = 5392)`，随后在初始化阶段出现 `SIGILL` 和 `MPI_Abort`；project-local 原始摘要保存在 `runs/stage-c-validation/rz-implicit-villasenor-build-boundary/command-output.txt`。

源码顺序也固定了边界：`ThetaImplicitEM::Define()` 先定义 nonlinear solver，再仅在 `pc_petsc` 下调用 `InitializeCurlCurlBCMasks()`；官方输入的 `petsc_ksp` 仍依赖 `AMREX_USE_PETSC`。因此本次结果只能分类为 `RZ_IMPLICIT_VILLASENOR_PREPHYSICS_SIGILL_BOUNDARY`，不能称为 Villasenor current kernel 的 physics pass/fail。可重复合同为 `scripts/audit_rz_implicit_villasenor_build_boundary.py`。
