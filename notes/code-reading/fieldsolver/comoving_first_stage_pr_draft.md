# Draft PR: add first-stage analysis for comoving PSATD test

## Proposed title

`Add first-stage analysis_comoving.py for test_2d_comoving_psatd_hybrid`

## Summary

- wire `test_2d_comoving_psatd_hybrid` to a new `analysis_comoving.py` helper;
- keep the existing checksum consumer unchanged;
- enforce `finite + spike` only in this first-stage helper;
- defer any energy gate to a follow-up once a stronger comoving contrast is validated.

## Review claim

This PR upgrades the comoving PSATD test from checksum-only to a narrow first-stage analysis gate. The helper always checks field finiteness and rejects runs whose `spike_ratio` exceeds a reproducible stable-baseline envelope. It does not yet claim a validated comoving energy-ordering gate.

## Reproducible constants

- Stable electric energy: `8.1520684623101725e+14`
- Stable spike ratio: `1.1103719982074416e+00`
- Zero-comoving electric energy: `7.7864117768828750e+14`
- `stable_over_unstable_energy_ratio = 1.0469608718245416e+00`
- `spike_ratio_ref_stable = 1.1103719982074416`
- `safety_factor = 1.001`
- `SPIKE_RATIO_MAX = 1.1114823702056489`

## Local cross-check

- Explicit-default beta energy/stable = `1.0000000000000131e+00`
- Positive-default beta spike/stable = `1.0622177820830927e+00`
- Positive-default beta energy/stable = `8.0281253219914006e-01`
- The local velocity-only scan shows that spike can worsen without producing a larger final electric energy inside the same comoving family.

## Real MPI=2 cross-check

- Explicit/default energy relative difference = `1.199e-14`
- Explicit/default spike relative difference = `4.030e-14`
- Positive-sign spike/stable = `1.0636724700037294e+00`
- The MPI pair supports selector equivalence and sign sensitivity, but not an energy-gate claim.

## Out of scope

- no `divE` or other producer-surface widening in this PR;
- no comoving energy gate in this PR;
- no claim that the current local `no-comoving` sibling is the final upstream unstable-energy reference.

## Reviewer checklist

1. The helper stays limited to `finite + spike`.
2. The existing checksum path remains in place.
3. The provenance note and ledger-backed constants are attached.
4. Follow-up work for energy-gate validation remains explicitly deferred.
