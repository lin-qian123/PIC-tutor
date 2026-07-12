# RSPHERE axis charge resolution boundary

The RCYLINDER/RSPHERE radial field matrix passes the `Er` field gate for shape 1--4, but the shape-1 `rho/divE` contract exposes a separate RSPHERE boundary.

| cells | axis correction | `Er` error | all-cell charge residual | off-axis residual |
|---:|---|---:|---:|---:|
| 64 | on | `2.174e-2` | `4.166e-2` | `2.531e-3` |
| 64 | off | `1.380e-2` | `2.420e-11` | `1.414e-11` |
| 128 | on | `3.389e-2` | `1.390e-2` | `9.504e-4` |
| 128 | off | `1.041e-2` | `9.843e-11` | `3.882e-11` |

The field gate remains below `0.12` in all four cases. Turning off the axis correction improves the 64-cell result substantially, but the 128-cell result is worse than the `1e-11` charge gate. The on/off trends therefore do not support a simple global-default change or a formal convergence-order claim.

The current classification is `RSPHERE_RESOLUTION_SENSITIVE_CHARGE_BOUNDARY`; the machine-readable comparison is `runs/stage-c-validation/esirkepov_rsphere_charge_resolution-comparison/contract.{json,md}`.
