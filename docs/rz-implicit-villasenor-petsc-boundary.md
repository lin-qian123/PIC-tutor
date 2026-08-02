# RZ implicit Villasenor PETSc runtime boundary

- classification: `PETSC_ENABLED_KSP_CONSTRUCTION_SIGILL_PRE_PHYSICS_BOUNDARY`
- input: `Examples/Tests/implicit/inputs_test_rz_theta_implicit_dynamic_pinch`
- isolated build: `RZ`, MPI, `WarpX_PETSC=ON`, `AMReX_PETSC=ON`, `NOACC`, PETSc `3.25.4`

The independent build configured and linked successfully. Both the two-rank official layout and a one-rank `max_step=1` control initialized AMReX and PETSc, created the WarpX linear-solver DOF object, and printed `KSP_impl: Initialized PETSc's KSP solver.` Both then exited with PETSc error code `59` after a `SIGILL`.

The two-rank and one-rank log SHA-256 values are respectively `c6bf1c1b4920e1e0e4fd18275341e93a0331540a0c4a65dddf26040f9abe2997` and `eed8a8ee52ba07cfd8fe2a80959c15060f21a48dd9f02119625652f6d0d0739b`. The `field_energy`, `particle_energy`, `poynting_flux`, and `newton_solver` files contain their headers only, so no field/charge consumer completed.

As a control, a separate two-rank MPI program successfully executed `PetscInitialize`, `KSPCreate`, `KSPDestroy`, and `PetscFinalize`; its empty successful log has SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The remaining fault is therefore narrower than PETSc installation or generic MPI KSP creation, but is not yet a root-cause attribution to a particular WarpX or PETSc call.

The next admissible action is to instrument or debug `KSP_impl::createObjects` and its PETSc object setup on arm64. This record does not close the RZ implicit Villasenor runtime gap.
