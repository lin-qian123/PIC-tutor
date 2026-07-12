# Draft PR: add first-stage analysis for RZ JRhom LL2 test

## Proposed title

`Add first-stage analysis_rz_jrhom.py for test_rz_psatd_JRhom_LL2`

## Summary

- wire `test_rz_psatd_JRhom_LL2` to a new `analysis_rz_jrhom.py` helper;
- keep the existing checksum consumer unchanged;
- enforce `finite + energy` only in this first-stage helper;
- defer any spike gate or diagnostic widening to a follow-up.

## Review claim

This PR upgrades the RZ JRhom LL2 test from checksum-only to a narrow first-stage analysis gate. The helper always checks field finiteness and rejects runs whose final electric energy is too close to the current unstable-reference sibling. It does not yet claim a longer-time-window validation or a second spike gate.

## Reproducible constants

- Baseline electric energy: `2.7378937095024567e+10`
- Reference electric energy: `2.8020912961036427e+10`
- Baseline spike ratio: `2.1161359692328046e+00`
- Reference spike ratio: `2.2339009047374176e+00`
- `energy_safety_factor = 1.001`
- `TOL_ENERGY = 9.7806649163175208e-01`

## Local cross-check

- The same energy ordering appears in both the local `1 1` scan and the repeated/MPI `mpiexec -n 2` scan.
- `cl1-timeavg-cleaning` remains a source-level illegal combination in both cases.
- `ll2-timeavg-no-cleaning` stays below baseline energy, so cleaning-only removal is still not the unstable-reference route.

## Out of scope

- no spike gate in this PR;
- no `divE` or other producer-surface widening in this PR;
- no claim that `diag1000025` is already the final best time surface for all future JRhom LL2 studies.

## Reviewer checklist

1. The helper stays limited to `finite + energy`.
2. The existing checksum path remains in place.
3. The provenance note and mpi2 ledger-backed constants are attached.
4. Follow-up work for spike-gate or longer-window validation remains explicitly deferred.
