#!/usr/bin/env python
"""Regenerate the first-stage RZ JRhom patch draft assets from the mpi2 ledger.

The generated assets stay in PIC-tutor on purpose. They are staging artifacts
for a future WarpX proposal, not an upstream patch applied in-place.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_JSON = (
    ROOT
    / "runs"
    / "fieldsolver-validation"
    / "rz-reference-ledgers"
    / "rz-jrhom-reference-scan-mpi2.json"
)
DEFAULT_HELPER_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "analysis_rz_jrhom_first_stage_draft.py"
)
DEFAULT_DIFF_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "rz_jrhom_first_stage_patch.diff"
)
DEFAULT_NOTE_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "rz_jrhom_first_stage_provenance_note.md"
)
DEFAULT_PACKET_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "rz_jrhom_first_stage_submission_packet.md"
)
DEFAULT_PR_DRAFT_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "rz_jrhom_first_stage_pr_draft.md"
)
DEFAULT_BUNDLE_DIR = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "rz_jrhom_first_stage_bundle"
)
DEFAULT_BASELINE_LABEL = "baseline-jrhom-ll2-timeavg-cleaning"
DEFAULT_REFERENCE_LABEL = "ll2-no-timeavg-cleaning"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the first-stage RZ JRhom helper draft and unified diff from the mpi2 ledger."
    )
    parser.add_argument(
        "--ledger-json",
        type=Path,
        default=DEFAULT_LEDGER_JSON,
        help="Reference sibling scan JSON with mpi2 metrics.",
    )
    parser.add_argument(
        "--energy-safety-factor",
        type=float,
        default=1.001,
        help="Multiplier applied to the stable/reference energy ratio. Default: 1.001",
    )
    parser.add_argument(
        "--helper-output",
        type=Path,
        default=DEFAULT_HELPER_PATH,
        help="Output path for the first-stage analysis helper draft.",
    )
    parser.add_argument(
        "--diff-output",
        type=Path,
        default=DEFAULT_DIFF_PATH,
        help="Output path for the unified diff draft.",
    )
    parser.add_argument(
        "--note-output",
        type=Path,
        default=DEFAULT_NOTE_PATH,
        help="Output path for the provenance note markdown.",
    )
    parser.add_argument(
        "--packet-output",
        type=Path,
        default=DEFAULT_PACKET_PATH,
        help="Output path for the submission packet markdown.",
    )
    parser.add_argument(
        "--pr-draft-output",
        type=Path,
        default=DEFAULT_PR_DRAFT_PATH,
        help="Output path for the PR draft markdown.",
    )
    parser.add_argument(
        "--bundle-dir",
        type=Path,
        default=DEFAULT_BUNDLE_DIR,
        help="Output directory for the upstream staging bundle.",
    )
    return parser.parse_args()


def load_ledger(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    summary = payload.get("summary") or {}
    by_label = {item["label"]: item for item in summary.get("candidates", [])}
    baseline = by_label.get(DEFAULT_BASELINE_LABEL)
    reference = by_label.get(DEFAULT_REFERENCE_LABEL)
    if baseline is None or reference is None:
        raise KeyError("Ledger is missing baseline or reference candidate.")
    if "metrics" not in baseline or "metrics" not in reference:
        raise KeyError("Baseline or reference candidate has no metrics.")
    return payload


def compute_contract(payload: dict, energy_safety_factor: float) -> dict:
    by_label = {
        item["label"]: item for item in payload["summary"]["candidates"]
    }
    baseline = by_label[DEFAULT_BASELINE_LABEL]
    reference = by_label[DEFAULT_REFERENCE_LABEL]
    baseline_energy = float(baseline["metrics"]["electric_energy"])
    reference_energy = float(reference["metrics"]["electric_energy"])
    baseline_spike = float(baseline["metrics"]["spike_ratio"])
    reference_spike = float(reference["metrics"]["spike_ratio"])
    tol_energy = (baseline_energy / reference_energy) * energy_safety_factor
    return {
        "baseline": baseline,
        "reference": reference,
        "baseline_energy": baseline_energy,
        "reference_energy": reference_energy,
        "baseline_spike": baseline_spike,
        "reference_spike": reference_spike,
        "tol_energy": tol_energy,
        "energy_safety_factor": energy_safety_factor,
    }


def render_helper(contract: dict) -> str:
    return f"""#!/usr/bin/env python3
\"\"\"
Draft WarpX-side first-stage analysis for test_rz_psatd_JRhom_LL2.

This file is intentionally stored in PIC-tutor as a patch draft asset. It is
the smallest helper shape that matches the current mpi2 evidence boundary:

- always enforce finite-field sanity
- enforce a first-stage energy gate
- defer any spike gate to a follow-up
\"\"\"

import sys

import numpy as np
import yt

yt.funcs.mylog.setLevel(0)


EPSILON_0 = 8.8541878128e-12
FIELD_NAMES = ("Er", "Ez", "Bt", "jr", "jz", "rho")

# Candidate first-stage constants derived from the current mpi2 ledger:
# baseline_energy = {contract['baseline_energy']:.16e}
# energy_ref = {contract['reference_energy']:.16e}
# energy_safety_factor = {contract['energy_safety_factor']}
ENERGY_REF = {contract['reference_energy']:.16e}
TOL_ENERGY = {contract['tol_energy']:.16e}


def main() -> None:
    filename = sys.argv[1]
    ds = yt.load(filename)

    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()

    grid = ds.covering_grid(
        level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions
    )

    fields = {{}}
    for name in FIELD_NAMES:
        arr = grid["boxlib", name].squeeze().v
        if not np.all(np.isfinite(arr)):
            raise AssertionError(f"{{name}} contains non-finite values")
        fields[name] = arr

    er = fields["Er"]
    ez = fields["Ez"]
    energy = np.sum(EPSILON_0 * 0.5 * (er**2 + ez**2))
    err_energy = energy / ENERGY_REF

    print("\\nCheck finite-field sanity:")
    print("all_fields_finite = True")

    print("\\nCheck numerical stability:")
    print(f"energy = {{energy}}")
    print(f"energy_ref = {{ENERGY_REF}}")
    print(f"err_energy = {{err_energy}}")
    print(f"tol_energy = {{TOL_ENERGY}}")
    assert err_energy <= TOL_ENERGY


if __name__ == "__main__":
    main()
"""


def render_diff(helper_text: str) -> str:
    helper_lines = helper_text.rstrip("\n").splitlines()
    diff_lines = [
        "diff --git a/Examples/Tests/nci_psatd_stability/CMakeLists.txt b/Examples/Tests/nci_psatd_stability/CMakeLists.txt",
        "index 0000000..0000000 100644",
        "--- a/Examples/Tests/nci_psatd_stability/CMakeLists.txt",
        "+++ b/Examples/Tests/nci_psatd_stability/CMakeLists.txt",
        "@@",
        " if(WarpX_FFT)",
        "     add_warpx_test(",
        "         test_rz_psatd_JRhom_LL2  # name",
        "         RZ  # dims",
        "         2  # nprocs",
        "         inputs_test_rz_psatd_JRhom_LL2  # inputs",
        "-        OFF  # analysis",
        '+        "analysis_rz_jrhom.py diags/diag1000025"  # analysis',
        '         "analysis_default_regression.py --path diags/diag1000025"  # checksum',
        "         OFF  # dependency",
        "     )",
        " endif()",
        "diff --git a/Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py b/Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py",
        "new file mode 100755",
        "index 0000000..0000000",
        "--- /dev/null",
        "+++ b/Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py",
        "@@",
    ]
    diff_lines.extend(f"+{line}" for line in helper_lines)
    return "\n".join(diff_lines) + "\n"


def render_note(payload: dict, contract: dict) -> str:
    baseline = contract["baseline"]
    reference = contract["reference"]
    lines = [
        "# RZ JRhom first-stage provenance note",
        "",
        "This note belongs to the current first-stage WarpX patch draft for `test_rz_psatd_JRhom_LL2`.",
        "",
        "## Draft scope",
        "",
        "- Keep the first-stage helper at `finite + energy` only.",
        "- Do not hard-code a spike gate yet.",
        "- Keep checksum wiring unchanged.",
        "",
        "## Mpi2 ledger source",
        "",
        f"- Ledger JSON: `{DEFAULT_LEDGER_JSON.relative_to(ROOT)}`",
        f"- Command prefix: `{payload.get('command_prefix')}`",
        f"- Baseline plotfile: `{baseline['plotfile']}`",
        f"- Reference plotfile: `{reference['plotfile']}`",
        f"- Baseline status: `{baseline['status']}`",
        f"- Reference status: `{reference['status']}`",
        "",
        "## First-stage energy constant",
        "",
        f"- `baseline_energy = {contract['baseline_energy']:.16e}`",
        f"- `energy_ref = {contract['reference_energy']:.16e}`",
        f"- `energy_safety_factor = {contract['energy_safety_factor']}`",
        f"- `TOL_ENERGY = {contract['tol_energy']:.16e}`",
        "",
        "## Why energy is now the default gate",
        "",
        f"- Baseline spike ratio: `{contract['baseline_spike']:.16e}`",
        f"- Reference spike ratio: `{contract['reference_spike']:.16e}`",
        f"- Baseline/reference energy ratio: `{contract['baseline_energy'] / contract['reference_energy']:.16e}`",
        "",
        "The repeated/MPI ledger keeps the same ordering already seen in the local `1 1` sample: `ll2-no-timeavg-cleaning` remains the highest-energy sibling, while `ll2-timeavg-no-cleaning` stays below baseline. That is enough evidence to make `finite + energy` the narrow first-stage contract.",
        "",
        "## Why spike is deferred",
        "",
        "- Spike ordering also separates the candidates, but energy is the narrower and more review-legible first-stage claim.",
        "- A second gate should only be added if upstream reviewers explicitly want the extra local-spike guard.",
        "",
        "## Review guidance",
        "",
        "If this draft is proposed upstream now, the review claim should stay narrow:",
        "",
        "1. RZ JRhom LL2 is upgraded from checksum-only to a first-stage `finite + energy` gate.",
        "2. The current `mpi2` ledger is attached as provenance for `ENERGY_REF` and `TOL_ENERGY`.",
        "3. Any spike gate, `divE` widening, or longer-time-window study remains follow-up work.",
        "",
    ]
    return "\n".join(lines)


def render_packet(contract: dict) -> str:
    lines = [
        "# RZ JRhom first-stage submission packet",
        "",
        "This packet is the current upstream-facing handoff for the first-stage `test_rz_psatd_JRhom_LL2` analysis proposal.",
        "",
        "## Scope",
        "",
        "- Add a first-stage `analysis_rz_jrhom.py` helper.",
        "- Change the test wiring from `analysis=OFF` to `analysis_rz_jrhom.py diags/diag1000025`.",
        "- Keep the existing checksum consumer.",
        "- Do not change diagnostics surfaces yet.",
        "- Do not add a spike gate yet.",
        "",
        "## Assets to copy or inspect",
        "",
        f"- Helper draft: `{DEFAULT_HELPER_PATH.relative_to(ROOT)}`",
        f"- Unified diff draft: `{DEFAULT_DIFF_PATH.relative_to(ROOT)}`",
        f"- Provenance note: `{DEFAULT_NOTE_PATH.relative_to(ROOT)}`",
        f"- PR draft: `{DEFAULT_PR_DRAFT_PATH.relative_to(ROOT)}`",
        "",
        "## Proposed review claim",
        "",
        "This change upgrades the RZ JRhom LL2 test from checksum-only to a narrow first-stage `finite + energy` analysis gate whose constants are reproducible from the current 2-rank ledger. It deliberately does not claim a longer-time-window study or a second spike gate.",
        "",
        "## Reproducible constants",
        "",
        f"- Baseline electric energy: `{contract['baseline_energy']:.16e}`",
        f"- Reference electric energy: `{contract['reference_energy']:.16e}`",
        f"- Baseline spike ratio: `{contract['baseline_spike']:.16e}`",
        f"- Reference spike ratio: `{contract['reference_spike']:.16e}`",
        f"- `energy_safety_factor = {contract['energy_safety_factor']}`",
        f"- `TOL_ENERGY = {contract['tol_energy']:.16e}`",
        "",
        "## Why this first-stage shape is narrow enough",
        "",
        "- The 2-rank ledger preserves the same unstable-reference ordering already seen in the local `1 1` sample.",
        "- `cl1-timeavg-cleaning` remains a source-level illegal combination, so the main contract should stay focused on the runnable LL2 siblings.",
        "- The helper only asserts what the current plotfiles directly support: finite fields plus end-of-window electric-energy separation.",
        "",
        "## Review checklist",
        "",
        "1. Confirm the helper stays `finite + energy` only.",
        "2. Confirm the existing checksum path remains in place.",
        "3. Confirm no producer-surface widening such as `divE` is bundled into this first-stage patch.",
        "4. Confirm the provenance note is attached so `ENERGY_REF` and `TOL_ENERGY` can be audited.",
        "",
        "## Follow-up boundary",
        "",
        "If upstream reviewers want additional guards, any spike gate, repeated longer-time-window scan, or new diagnostic surface should be proposed as follow-up work rather than being retrofitted into this first-stage packet.",
        "",
    ]
    return "\n".join(lines)


def render_pr_draft(contract: dict) -> str:
    lines = [
        "# Draft PR: add first-stage analysis for RZ JRhom LL2 test",
        "",
        "## Proposed title",
        "",
        "`Add first-stage analysis_rz_jrhom.py for test_rz_psatd_JRhom_LL2`",
        "",
        "## Summary",
        "",
        "- wire `test_rz_psatd_JRhom_LL2` to a new `analysis_rz_jrhom.py` helper;",
        "- keep the existing checksum consumer unchanged;",
        "- enforce `finite + energy` only in this first-stage helper;",
        "- defer any spike gate or diagnostic widening to a follow-up.",
        "",
        "## Review claim",
        "",
        "This PR upgrades the RZ JRhom LL2 test from checksum-only to a narrow first-stage analysis gate. The helper always checks field finiteness and rejects runs whose final electric energy is too close to the current unstable-reference sibling. It does not yet claim a longer-time-window validation or a second spike gate.",
        "",
        "## Reproducible constants",
        "",
        f"- Baseline electric energy: `{contract['baseline_energy']:.16e}`",
        f"- Reference electric energy: `{contract['reference_energy']:.16e}`",
        f"- Baseline spike ratio: `{contract['baseline_spike']:.16e}`",
        f"- Reference spike ratio: `{contract['reference_spike']:.16e}`",
        f"- `energy_safety_factor = {contract['energy_safety_factor']}`",
        f"- `TOL_ENERGY = {contract['tol_energy']:.16e}`",
        "",
        "## Local cross-check",
        "",
        "- The same energy ordering appears in both the local `1 1` scan and the repeated/MPI `mpiexec -n 2` scan.",
        "- `cl1-timeavg-cleaning` remains a source-level illegal combination in both cases.",
        "- `ll2-timeavg-no-cleaning` stays below baseline energy, so cleaning-only removal is still not the unstable-reference route.",
        "",
        "## Out of scope",
        "",
        "- no spike gate in this PR;",
        "- no `divE` or other producer-surface widening in this PR;",
        "- no claim that `diag1000025` is already the final best time surface for all future JRhom LL2 studies.",
        "",
        "## Reviewer checklist",
        "",
        "1. The helper stays limited to `finite + energy`.",
        "2. The existing checksum path remains in place.",
        "3. The provenance note and mpi2 ledger-backed constants are attached.",
        "4. Follow-up work for spike-gate or longer-window validation remains explicitly deferred.",
        "",
    ]
    return "\n".join(lines)


def render_bundle_readme(bundle_dir: Path) -> str:
    rel_bundle = bundle_dir.relative_to(ROOT)
    return "\n".join(
        [
            "# RZ JRhom first-stage upstream staging bundle",
            "",
            "This directory mirrors the minimum assets needed to hand the current RZ JRhom LL2 first-stage proposal to another WarpX worktree or reviewer.",
            "",
            "## Contents",
            "",
            "- `warpx/Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py`",
            "- `warpx/rz_jrhom_first_stage_patch.diff`",
            "- `docs/rz_jrhom_first_stage_provenance_note.md`",
            "- `docs/rz_jrhom_first_stage_submission_packet.md`",
            "- `docs/rz_jrhom_first_stage_pr_draft.md`",
            "",
            "## Source of truth",
            "",
            f"The bundle is generated from `{rel_bundle.parent / 'analysis_rz_jrhom_first_stage_draft.py'}` and siblings by `scripts/build_rz_jrhom_first_stage_patch.py`.",
            "",
            "Do not hand-edit the mirrored files here; regenerate the bundle instead.",
            "",
        ]
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_bundle(
    bundle_dir: Path,
    helper_text: str,
    diff_text: str,
    note_text: str,
    packet_text: str,
    pr_draft_text: str,
) -> None:
    helper_path = bundle_dir / "warpx" / "Examples" / "Tests" / "nci_psatd_stability" / "analysis_rz_jrhom.py"
    diff_path = bundle_dir / "warpx" / "rz_jrhom_first_stage_patch.diff"
    docs_dir = bundle_dir / "docs"
    write_text(bundle_dir / "README.md", render_bundle_readme(bundle_dir))
    write_text(helper_path, helper_text)
    write_text(diff_path, diff_text)
    write_text(docs_dir / "rz_jrhom_first_stage_provenance_note.md", note_text)
    write_text(docs_dir / "rz_jrhom_first_stage_submission_packet.md", packet_text)
    write_text(docs_dir / "rz_jrhom_first_stage_pr_draft.md", pr_draft_text)


def main() -> None:
    args = parse_args()
    payload = load_ledger(args.ledger_json)
    contract = compute_contract(payload, args.energy_safety_factor)

    helper_text = render_helper(contract)
    diff_text = render_diff(helper_text)
    note_text = render_note(payload, contract)
    packet_text = render_packet(contract)
    pr_draft_text = render_pr_draft(contract)

    write_text(args.helper_output, helper_text)
    write_text(args.diff_output, diff_text)
    write_text(args.note_output, note_text)
    write_text(args.packet_output, packet_text)
    write_text(args.pr_draft_output, pr_draft_text)
    write_bundle(
        args.bundle_dir,
        helper_text,
        diff_text,
        note_text,
        packet_text,
        pr_draft_text,
    )

    print(f"wrote {args.helper_output.relative_to(ROOT)}")
    print(f"wrote {args.diff_output.relative_to(ROOT)}")
    print(f"wrote {args.note_output.relative_to(ROOT)}")
    print(f"wrote {args.packet_output.relative_to(ROOT)}")
    print(f"wrote {args.pr_draft_output.relative_to(ROOT)}")
    print(f"wrote {args.bundle_dir.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
