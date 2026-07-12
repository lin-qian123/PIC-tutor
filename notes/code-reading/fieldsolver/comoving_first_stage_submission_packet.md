# Comoving first-stage submission packet

This packet is the current upstream-facing handoff for the first-stage `test_2d_comoving_psatd_hybrid` analysis proposal.

## Scope

- Add a first-stage `analysis_comoving.py` helper.
- Change the test wiring from `analysis=OFF` to `analysis_comoving.py diags/diag1000400`.
- Keep the existing checksum consumer.
- Do not change diagnostics surfaces yet.
- Do not add an energy gate yet.

## Assets to copy or inspect

- Helper draft: `notes/code-reading/fieldsolver/analysis_comoving_first_stage_draft.py`
- Unified diff draft: `notes/code-reading/fieldsolver/comoving_first_stage_patch.diff`
- Provenance note: `notes/code-reading/fieldsolver/comoving_first_stage_provenance_note.md`
- PR draft: `notes/code-reading/fieldsolver/comoving_first_stage_pr_draft.md`

## Proposed review claim

This change upgrades the comoving PSATD test from checksum-only to a narrow first-stage `finite + spike` analysis gate whose threshold is reproducible from a stable local ledger. It deliberately does not claim a validated comoving energy-gate ordering.

## Stable spike envelope

- Stable electric energy: `8.1520684623101725e+14`
- Stable spike ratio: `1.1103719982074416e+00`
- `spike_ratio_ref_stable = 1.1103719982074416`
- `safety_factor = 1.001`
- `SPIKE_RATIO_MAX = 1.1114823702056489`

## Why energy gate is deferred

- Zero-comoving electric energy: `7.7864117768828750e+14`
- `stable_over_unstable_energy_ratio = 1.0469608718245416e+00`
- The obvious local `no-comoving` sibling does not produce a higher electric-energy ordering than the stable baseline.

## Velocity-only cross-check

- Positive-default beta spike/stable = `1.0622177820830927e+00`
- Positive-default beta energy/stable = `8.0281253219914006e-01`
- This confirms that spike can get worse without producing a stronger electric-energy ordering inside the same comoving family.

## Review checklist

1. Confirm the helper stays `finite + spike` only.
2. Confirm checksum wiring is preserved.
3. Confirm no producer-surface widening such as `divE` is bundled into this first-stage patch.
4. Confirm the provenance note is attached so the spike constant can be audited.

## Follow-up boundary

If stronger repeated/MPI contrast later demonstrates a reliable comoving energy ordering, that should be proposed as a follow-up patch rather than being retrofitted into this first-stage packet.
