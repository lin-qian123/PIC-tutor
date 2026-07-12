# RZ JRhom first-stage submission packet

This packet is the current upstream-facing handoff for the first-stage `test_rz_psatd_JRhom_LL2` analysis proposal.

## Scope

- Add a first-stage `analysis_rz_jrhom.py` helper.
- Change the test wiring from `analysis=OFF` to `analysis_rz_jrhom.py diags/diag1000025`.
- Keep the existing checksum consumer.
- Do not change diagnostics surfaces yet.
- Do not add a spike gate yet.

## Assets to copy or inspect

- Helper draft: `notes/code-reading/fieldsolver/analysis_rz_jrhom_first_stage_draft.py`
- Unified diff draft: `notes/code-reading/fieldsolver/rz_jrhom_first_stage_patch.diff`
- Provenance note: `notes/code-reading/fieldsolver/rz_jrhom_first_stage_provenance_note.md`
- PR draft: `notes/code-reading/fieldsolver/rz_jrhom_first_stage_pr_draft.md`

## Proposed review claim

This change upgrades the RZ JRhom LL2 test from checksum-only to a narrow first-stage `finite + energy` analysis gate whose constants are reproducible from the current 2-rank ledger. It deliberately does not claim a longer-time-window study or a second spike gate.

## Reproducible constants

- Baseline electric energy: `2.7378937095024567e+10`
- Reference electric energy: `2.8020912961036427e+10`
- Baseline spike ratio: `2.1161359692328046e+00`
- Reference spike ratio: `2.2339009047374176e+00`
- `energy_safety_factor = 1.001`
- `TOL_ENERGY = 9.7806649163175208e-01`

## Why this first-stage shape is narrow enough

- The 2-rank ledger preserves the same unstable-reference ordering already seen in the local `1 1` sample.
- `cl1-timeavg-cleaning` remains a source-level illegal combination, so the main contract should stay focused on the runnable LL2 siblings.
- The helper only asserts what the current plotfiles directly support: finite fields plus end-of-window electric-energy separation.

## Review checklist

1. Confirm the helper stays `finite + energy` only.
2. Confirm the existing checksum path remains in place.
3. Confirm no producer-surface widening such as `divE` is bundled into this first-stage patch.
4. Confirm the provenance note is attached so `ENERGY_REF` and `TOL_ENERGY` can be audited.

## Follow-up boundary

If upstream reviewers want additional guards, any spike gate, repeated longer-time-window scan, or new diagnostic surface should be proposed as follow-up work rather than being retrofitted into this first-stage packet.
