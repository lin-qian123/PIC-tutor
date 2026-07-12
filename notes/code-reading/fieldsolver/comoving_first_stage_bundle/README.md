# Comoving first-stage upstream staging bundle

This directory mirrors the minimum assets needed to stage the current first-step
`test_2d_comoving_psatd_hybrid` proposal into a WarpX worktree.

## Contents

- `warpx/Examples/Tests/nci_psatd_stability/analysis_comoving.py`
- `warpx/comoving_first_stage_patch.diff`
- `docs/comoving_first_stage_provenance_note.md`
- `docs/comoving_first_stage_submission_packet.md`
- `docs/comoving_first_stage_pr_draft.md`

## Suggested use

1. Copy `warpx/Examples/Tests/nci_psatd_stability/analysis_comoving.py` into the target WarpX checkout.
2. Apply `warpx/comoving_first_stage_patch.diff` from the WarpX repository root, or edit `Examples/Tests/nci_psatd_stability/CMakeLists.txt` equivalently.
3. Attach the three files under `docs/` when preparing the actual upstream proposal.
4. Keep the first-stage scope at `finite + spike`; do not retrofit an energy gate into this bundle without a new calibration pass.

PIC-tutor also provides a helper installer:

```bash
python scripts/stage_comoving_first_stage_patch.py --warpx-root /path/to/warpx --dry-run
python scripts/stage_comoving_first_stage_patch.py --warpx-root /path/to/warpx
python scripts/audit_comoving_first_stage_patch.py --warpx-root /path/to/warpx
python scripts/report_comoving_first_stage_patch.py --warpx-root /path/to/warpx
python scripts/preview_comoving_first_stage_patch.py --warpx-root /path/to/warpx
```

This script copies the helper and rewrites the comoving test's analysis line in
`Examples/Tests/nci_psatd_stability/CMakeLists.txt` without touching any other
test block.

The audit script stays read-only and reports whether the target checkout is
`unstaged`, `partial`, or fully `staged`.

The report script stays read-only as well, but writes a markdown preflight note
that summarizes the target checkout status and the exact next command to run.

The preview script also stays read-only and prints the exact unified diff that
the staging step would apply to the target checkout.

This bundle is generated from:
- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-stable-vs-no-comoving.json`
- `runs/fieldsolver-validation/comoving-reference-ledgers/comoving-velocity-scan.json`

Bundle root: `notes/code-reading/fieldsolver/comoving_first_stage_bundle`
