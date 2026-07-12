# Comoving first-stage target report

- Target WarpX root: `/Volumes/PHILIPS/programs/PIC/warpx`
- Bundle root: `notes/code-reading/fieldsolver/comoving_first_stage_bundle`
- Overall status: `unstaged`

## Helper status

- Path: `/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/nci_psatd_stability/analysis_comoving.py`
- Status: `missing`
- Detail: helper file is absent

## CMake status

- Path: `/Volumes/PHILIPS/programs/PIC/warpx/Examples/Tests/nci_psatd_stability/CMakeLists.txt`
- Status: `unstaged`
- Detail: analysis line is still OFF
- Current line: `        OFF  # analysis`

## Attached bundle docs

- `notes/code-reading/fieldsolver/comoving_first_stage_bundle/docs/comoving_first_stage_provenance_note.md`
- `notes/code-reading/fieldsolver/comoving_first_stage_bundle/docs/comoving_first_stage_submission_packet.md`
- `notes/code-reading/fieldsolver/comoving_first_stage_bundle/docs/comoving_first_stage_pr_draft.md`

## Recommended next steps

- Run `python scripts/preview_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx` to inspect the exact unified diff before writing anything.
- Run `python scripts/stage_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx --dry-run` to verify the same target files are about to be staged.
- Then run `python scripts/stage_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx` to stage the first-stage helper into the target checkout.
- Re-run `python scripts/audit_comoving_first_stage_patch.py --warpx-root /Volumes/PHILIPS/programs/PIC/warpx` to confirm the checkout moves to `staged`.
