# Implicit Villasenor runtime contract

审计日期：2026-07-12

## Passed cases

### 2D JFNK baseline

Official input: `Examples/Tests/implicit/inputs_test_2d_theta_implicit_jfnk_vandb`.

- 2-rank producer exit code: `0`
- `shape=2`, periodic 2D, theta-implicit Newton/JFNK
- official analysis: PASS
- independent `scripts/analyze_implicit_villasenor_contract.py`: PASS
- maximum relative total-energy change: `4.098007358098339e-15 < 2e-14`
- Gauss-law RMS: `9.295065316488536e-16 < 2e-15`
- final dimensions: `40x40x1`

### 2D boundary cropping

Official input: `Examples/Tests/implicit/inputs_test_2d_theta_implicit_jfnk_vandb_cropping`.

- 2-rank producer exit code: `0`
- `shape=4`, `16x16` grid, near-boundary cropping path
- official analysis: PASS
- independent contract: PASS
- Gauss-law maximum absolute error: `8.227526205231782e-14 < 1e-13`
- Gauss-law RMS: `3.0023498219284174e-14`

## Boundaries

- RZ `test_rz_theta_implicit_dynamic_pinch` was rejected during `NewtonSolver::Define()` because the current `build_full` binary lacks `AMREX_USE_PETSC`, while the input selects `newton.linear_solver=petsc_ksp`.
- 1D `test_1d_theta_implicit_planar_pinch` reached Newton convergence but then ended with `SIGILL`; only the initial plotfile was written.

These two cases are not counted as physics passes. They identify missing build/runtime prerequisites and remain separate from the two passed 2D contracts.
