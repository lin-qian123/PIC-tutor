# Formal convergence repeat-family preflight

本文件保留 v0.85 的执行前合同历史；当前 v0.92 的真实执行合同见 `docs/formal-convergence-repeat-family-v0.92.{json,md}`。

- historical classification: `REPEAT_FAMILY_RUNNER_BLOCKED_MPI_LAUNCHER_MISSING`
- planned family: `RZ/RSPHERE x 64/128/256 x correction on/off`
- required launch: `mpiexec -n 2`
- historical environment: default shell `PATH` did not expose `mpiexec` or `mpirun`
- input contract: all 12 templates have `inputs`, referenced `FILE` files, `Full` diagnostics and intervals
- output contract after execution: zero exit code, `producer.log`, `warpx_used_inputs` and at least one `diags/diag*` directory per run

The repeat runner is implemented in `scripts/run_formal_convergence_repeat_family.py`. It has separate prerequisite and post-execution checks: it validates the existing case input templates before launch, then copies only those templates, runs the fixed 2-rank binaries, records producer return codes, and validates the expected output contract. It refuses to substitute a single-rank run. The current execution used `/Users/yuxiangzhang/anaconda3/envs/warpx-cpu-mpich-dev/bin/mpiexec` with `FI_PROVIDER=tcp`; 12/12 producers returned zero and passed the output contract. Raw current evidence is written to `runs/stage-c-validation/formal-convergence-repeat-family-v0.92-tcp/contract.{json,md}`.

The current second family is materialized, but the separate slope comparison remains open because the preregistration has no numerical repeat-slope tolerance and correction-on axis charge remains a boundary. See `docs/formal-convergence-second-family-v0.92.{json,md}`.
