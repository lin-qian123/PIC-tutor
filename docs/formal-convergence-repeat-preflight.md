# Formal convergence repeat-family preflight

- classification: `REPEAT_FAMILY_RUNNER_BLOCKED_MPI_LAUNCHER_MISSING`
- planned family: `RZ/RSPHERE x 64/128/256 x correction on/off`
- required launch: `mpiexec -n 2`
- current environment: no `mpiexec` or `mpirun` executable was found
- input contract: all 12 templates have `inputs`, referenced `FILE` files, `Full` diagnostics and intervals
- output contract after execution: zero exit code, `producer.log`, `warpx_used_inputs` and at least one `diags/diag*` directory per run

The repeat runner is implemented in `scripts/run_formal_convergence_repeat_family.py`. It has separate prerequisite and post-execution checks: it validates the existing case input templates before launch, then copies only those templates, runs the fixed 2-rank binaries, records producer return codes, and validates the expected output contract. It refuses to substitute a single-rank run. Raw preflight evidence is written to `runs/stage-c-validation/formal-convergence-repeat-preflight/contract.{json,md}`.

This is an execution boundary, not a convergence result. The existing one-family RZ/RSPHERE evidence remains the only materialized family until a compatible MPI launcher is available.
