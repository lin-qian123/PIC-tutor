# Vay deposition mesh-refinement source guard

- classification: `CURRENT_UPSTREAM_RUNTIME_GUARD_CONFIRMED_UNSUPPORTED`
- status: `PASS`
- scope: read-only WarpX initialization/source guards; no AMR producer is interpreted as a physics runtime failure or pass

| check | status |
|---|:---:|
| `source_mesh_refinement_guard` | `PASS` |
| `source_guard_message` | `PASS` |
| `source_vay_psatd_guard` | `PASS` |
| `source_vay_rz_guard` | `PASS` |
| `source_vay_1d_guard` | `PASS` |
| `chapter_amr_boundary` | `PASS` |
| `chapter_vay_configuration_reader_card` | `PASS` |
| `gap_register_amr_boundary` | `PASS` |
| `no_amr_runtime_pass_claim` | `PASS` |
| `runtime_amrex_initialized` | `PASS` |
| `runtime_mesh_refinement_assertion` | `PASS` |
| `runtime_guard_message` | `PASS` |
| `runtime_abort` | `PASS` |
| `runtime_exit_code` | `PASS` |

The current checkout rejects Vay when `maxLevel() > 0` during initialization. This is a source-defined support boundary, not a failed AMR physics experiment.

Runtime evidence has SHA-256 `b3ffcbf1a0773418e39b46b1eb5df6c378fc3294cb8f9e379acdbe61069ca911` and process exit code `6`.
The input reaches AMReX initialization and then stops at the Vay/mesh-refinement assertion. It does not enter a field or charge consumer, so it proves an unsupported configuration boundary only.
