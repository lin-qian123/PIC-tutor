# RZ JRhom first-stage provenance note

This note belongs to the current first-stage WarpX patch draft for `test_rz_psatd_JRhom_LL2`.

## Draft scope

- Keep the first-stage helper at `finite + energy` only.
- Do not hard-code a spike gate yet.
- Keep checksum wiring unchanged.

## Mpi2 ledger source

- Ledger JSON: `runs/fieldsolver-validation/rz-reference-ledgers/rz-jrhom-reference-scan-mpi2.json`
- Command prefix: `['/Users/yuxiangzhang/anaconda3/envs/warpx-cpu-mpich-dev/bin/mpiexec', '-n', '2']`
- Baseline plotfile: `/Volumes/PHILIPS/programs/PIC/PIC-tutor/runs/fieldsolver-validation/rz-jrhom-reference-scan-mpi2/baseline-jrhom-ll2-timeavg-cleaning/diags/diag1000025`
- Reference plotfile: `/Volumes/PHILIPS/programs/PIC/PIC-tutor/runs/fieldsolver-validation/rz-jrhom-reference-scan-mpi2/ll2-no-timeavg-cleaning/diags/diag1000025`
- Baseline status: `ok_with_finalize_error`
- Reference status: `ok_with_finalize_error`

## First-stage energy constant

- `baseline_energy = 2.7378937095024567e+10`
- `energy_ref = 2.8020912961036427e+10`
- `energy_safety_factor = 1.001`
- `TOL_ENERGY = 9.7806649163175208e-01`

## Why energy is now the default gate

- Baseline spike ratio: `2.1161359692328046e+00`
- Reference spike ratio: `2.2339009047374176e+00`
- Baseline/reference energy ratio: `9.7708940222952267e-01`

The repeated/MPI ledger keeps the same ordering already seen in the local `1 1` sample: `ll2-no-timeavg-cleaning` remains the highest-energy sibling, while `ll2-timeavg-no-cleaning` stays below baseline. That is enough evidence to make `finite + energy` the narrow first-stage contract.

## Why spike is deferred

- Spike ordering also separates the candidates, but energy is the narrower and more review-legible first-stage claim.
- A second gate should only be added if upstream reviewers explicitly want the extra local-spike guard.

## Review guidance

If this draft is proposed upstream now, the review claim should stay narrow:

1. RZ JRhom LL2 is upgraded from checksum-only to a first-stage `finite + energy` gate.
2. The current `mpi2` ledger is attached as provenance for `ENERGY_REF` and `TOL_ENERGY`.
3. Any spike gate, `divE` widening, or longer-time-window study remains follow-up work.
