# Formal convergence repeat-family runner preflight

- classification: `REPEAT_FAMILY_RUNNER_EXECUTION_PASS`
- contract: `PASS`
- ready to execute: `True`
- expected MPI ranks: `2`
- MPI launcher: `/Users/yuxiangzhang/anaconda3/envs/warpx-cpu-mpich-dev/bin/mpiexec`
- runtime environment: `{"FI_PROVIDER": "tcp"}`

| check | status |
|---|:---:|
| `twelve_runs_declared` | `PASS` |
| `templates_present` | `PASS` |
| `binaries_present` | `PASS` |
| `inputs_present` | `PASS` |
| `referenced_input_files_present` | `PASS` |
| `diagnostics_configured` | `PASS` |
| `mpi_launcher_present` | `PASS` |
| `fixed_rank_count` | `PASS` |
| `single_rank_substitute_forbidden` | `PASS` |
| `all_producers_exit_zero` | `PASS` |
| `producer_log_present` | `PASS` |
| `used_inputs_present` | `PASS` |
| `diagnostics_present` | `PASS` |
| `diagnostic_dirs_present` | `PASS` |

A single-rank run is not an acceptable substitute for this preregistered 2-rank family.
