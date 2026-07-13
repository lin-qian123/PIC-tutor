# Formal convergence study preregistration

- version: `v0.84-pre`
- classification: `FORMAL_CONVERGENCE_PREREGISTERED_CURRENT_DATA_INSUFFICIENT`
- scope: RZ and RSPHERE Esirkepov Langmuir resolution families; independent geometry fits only

## Fixed design

| item | preregistered rule |
|---|---|
| geometry units | `RZ` and `RSPHERE`, fitted separately |
| correction controls | `on` and `off`; the latter is a negative control |
| resolution levels | `64`, `128`, `256` with refinement ratio `2` |
| fit interval | all adjacent pairs; no post-hoc omission |
| independent families | at least `2` per geometry; currently `1` is materialized |
| geometry pooling | forbidden |

## Norms and observables

Field errors use `max(abs(numerical - analytic)) / max(abs(analytic))`. Charge residuals use `max(abs(divE - rho/epsilon_0)) / max(abs(rho/epsilon_0))`. The primary observables are axis and off-axis charge residuals; `Er`, `Ez`, and all-cell charge residual are secondary observables. Axis and off-axis values remain separate.

Every declared level must use the same density, perturbation, domain, final time, particle shape, deposition method, MPI layout, and reader-side norm. The `correction=off` family is a control, not a reason to select a favorable fit interval.

## Current evidence boundary

The existing RZ and RSPHERE contracts satisfy the three-level exploratory design, but each geometry currently has only one independent family. Correction-on axis charge remains a boundary, and the observed slopes are descriptive rather than repeat-validated. Therefore this preregistration is complete while formal convergence closure remains open.

Machine audit: `scripts/audit_formal_convergence_preregistration.py`; raw report: `runs/stage-c-validation/formal-convergence-preregistration/contract.{json,md}`.
