# Comoving first-stage provenance note

This note belongs to the current first-stage WarpX patch draft for `test_2d_comoving_psatd_hybrid`.

## Draft scope

- Keep the first-stage helper at `finite + spike` only.
- Do not hard-code an energy gate yet.
- Keep checksum wiring unchanged.

## Stable ledger source

- Ledger JSON: `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-no-comoving.json`
- Stable plotfile: `/Volumes/PHILIPS/programs/PIC/PIC-tutor/runs/fieldsolver-validation/comoving-stable-baseline/diags/diag1000400`
- Unstable plotfile: `/Volumes/PHILIPS/programs/PIC/PIC-tutor/runs/fieldsolver-validation/comoving-unstable-no-comoving/diags/diag1000400`
- Stable input: `/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid`
- Unstable input: `/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid`
- Producer command: `stable: /Volumes/PHILIPS/programs/PIC/warpx/build_full/bin/warpx.2d.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES /Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/nci_psatd_stability/inputs_test_2d_comoving_psatd_hybrid warpx.numprocs='1 1'; unstable: same + psatd.use_default_v_comoving=0 psatd.v_comoving='0. 0. 0.'`

## First-stage spike constant

- `spike_ratio_ref_stable = 1.1103719982074416`
- `safety_factor = 1.001`
- `SPIKE_RATIO_MAX = 1.1114823702056489`

## Why there is no energy gate

- Stable electric energy: `8.1520684623101725e+14`
- Zero-comoving electric energy: `7.7864117768828750e+14`
- `stable_over_unstable_energy_ratio = 1.0469608718245416e+00`

The current local sibling does not inflate electric energy above the stable baseline, so `energy_ref_unstable` is not yet a defensible first-stage CI constant.

## Velocity-only sibling scan cross-check

- Scan JSON: `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan.json`
- Explicit default beta energy/stable = `1.0000000000000131e+00`
- Half-default beta energy/stable = `9.8803444339222468e-01`
- Positive-default beta energy/stable = `8.0281253219914006e-01`
- Positive-default beta spike/stable = `1.0622177820830927e+00`

The velocity-only scan confirms two things: default selector and explicit default velocity are numerically equivalent, and spike can worsen without producing a higher electric-energy ordering.

## Review guidance

If this draft is proposed upstream now, the review claim should stay narrow:

1. comoving first-stage analysis now has a reproducible stable spike envelope;
2. local evidence supports `finite + spike` as the honest first-stage gate;
3. energy-gate work is deferred to a follow-up that uses stronger repeated/MPI contrast evidence.
