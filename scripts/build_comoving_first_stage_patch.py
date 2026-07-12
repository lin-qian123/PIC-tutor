#!/usr/bin/env python
"""Regenerate the first-stage comoving patch draft assets from a reference ledger.

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
    / "comoving-reference-ledgers"
    / "comoving-stable-vs-no-comoving.json"
)
DEFAULT_SCAN_JSON = (
    ROOT
    / "runs"
    / "fieldsolver-validation"
    / "comoving-reference-ledgers"
    / "comoving-velocity-scan.json"
)
DEFAULT_MPI2_JSON = (
    ROOT
    / "runs"
    / "fieldsolver-validation"
    / "comoving-reference-ledgers"
    / "comoving-mpi2-pair-contract"
    / "contract.json"
)
DEFAULT_HELPER_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "analysis_comoving_first_stage_draft.py"
)
DEFAULT_DIFF_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_patch.diff"
)
DEFAULT_NOTE_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_provenance_note.md"
)
DEFAULT_PACKET_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_submission_packet.md"
)
DEFAULT_PR_DRAFT_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_pr_draft.md"
)
DEFAULT_BUNDLE_DIR = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_bundle"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the first-stage comoving helper draft and unified diff from a ledger."
    )
    parser.add_argument(
        "--ledger-json",
        type=Path,
        default=DEFAULT_LEDGER_JSON,
        help="Reference ledger JSON with derived_contract_observations.",
    )
    parser.add_argument(
        "--safety-factor",
        type=float,
        default=1.001,
        help="Multiplier applied to spike_ratio_ref_stable. Default: 1.001",
    )
    parser.add_argument(
        "--scan-json",
        type=Path,
        default=DEFAULT_SCAN_JSON,
        help="Optional comoving velocity scan summary JSON.",
    )
    parser.add_argument(
        "--mpi2-json",
        type=Path,
        default=DEFAULT_MPI2_JSON,
        help="Optional real MPI=2 stable/explicit/sign contract JSON.",
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
    derived = payload.get("derived_contract_observations") or {}
    spike_ratio_ref_stable = derived.get("spike_ratio_ref_stable")
    if spike_ratio_ref_stable is None:
        raise KeyError(
            f"{path} is missing derived_contract_observations.spike_ratio_ref_stable"
        )
    return payload


def validate_ledger(payload: dict, path: Path) -> tuple[float, float]:
    derived = payload.get("derived_contract_observations") or {}
    spike_ratio_ref_stable = derived.get("spike_ratio_ref_stable")
    if spike_ratio_ref_stable is None:
        raise KeyError(
            f"{path} is missing derived_contract_observations.spike_ratio_ref_stable"
        )
    return float(spike_ratio_ref_stable), float(payload["stable_metrics"]["spike_ratio"])


def load_scan_payload(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def render_helper(spike_ratio_ref_stable: float, safety_factor: float) -> str:
    spike_ratio_max = spike_ratio_ref_stable * safety_factor
    return f"""#!/usr/bin/env python
\"\"\"
Draft WarpX-side first-stage analysis for test_2d_comoving_psatd_hybrid.

This file is intentionally stored in PIC-tutor as a patch draft asset. It is
the smallest helper shape that matches the current evidence boundary:

- always enforce finite-field sanity
- enforce a first-stage spike-ratio gate
- do not yet enforce an energy gate

Why no energy gate here?
Because the current local calibration audit shows that the obvious
`no-comoving` sibling does not yield the same unstable-energy ordering that the
analogous Galilean family does, so a hard-coded comoving `energy_ref` would
overstate what has actually been validated.
\"\"\"

import sys

import numpy as np
import yt

yt.funcs.mylog.setLevel(0)


FIELD_NAMES = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho")

# Candidate first-stage ceiling derived from the current stable baseline:
# spike_ratio_ref_stable = {spike_ratio_ref_stable:.16f}
# safety_factor = {safety_factor}
SPIKE_RATIO_MAX = {spike_ratio_max:.16f}


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

    ex = fields["Ex"]
    ey = fields["Ey"]
    ez = fields["Ez"]
    e_mag = np.sqrt(ex**2 + ey**2 + ez**2)
    spike_ratio = np.max(e_mag) / (np.percentile(e_mag, 99) + 1e-300)

    print("\\nCheck finite-field sanity:")
    print("all_fields_finite = True")

    print("\\nCheck spike-ratio sanity:")
    print(f"spike_ratio = {{spike_ratio}}")
    print(f"spike_ratio_max = {{SPIKE_RATIO_MAX}}")
    assert spike_ratio <= SPIKE_RATIO_MAX


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
        "         test_2d_comoving_psatd_hybrid  # name",
        "         2  # dims",
        "         2  # nprocs",
        "         inputs_test_2d_comoving_psatd_hybrid  # inputs",
        "-        OFF  # analysis",
        '+        "analysis_comoving.py diags/diag1000400"  # analysis',
        '         "analysis_default_regression.py --path diags/diag1000400"  # checksum',
        "         OFF  # dependency",
        "     )",
        " endif()",
        "diff --git a/Examples/Tests/nci_psatd_stability/analysis_comoving.py b/Examples/Tests/nci_psatd_stability/analysis_comoving.py",
        "new file mode 100755",
        "index 0000000..0000000",
        "--- /dev/null",
        "+++ b/Examples/Tests/nci_psatd_stability/analysis_comoving.py",
        "@@",
    ]
    diff_lines.extend(f"+{line}" for line in helper_lines)
    return "\n".join(diff_lines) + "\n"


def render_note(
    ledger_payload: dict,
    scan_payload: dict | None,
    mpi2_payload: dict | None,
    safety_factor: float,
) -> str:
    stable = ledger_payload["stable_metrics"]
    unstable = ledger_payload["unstable_metrics"]
    derived = ledger_payload["derived_contract_observations"]
    spike_ratio_ref_stable = derived["spike_ratio_ref_stable"]
    spike_ratio_max = spike_ratio_ref_stable * safety_factor
    lines = [
        "# Comoving first-stage provenance note",
        "",
        "This note belongs to the current first-stage WarpX patch draft for `test_2d_comoving_psatd_hybrid`.",
        "",
        "## Draft scope",
        "",
        "- Keep the first-stage helper at `finite + spike` only.",
        "- Do not hard-code an energy gate yet.",
        "- Keep checksum wiring unchanged.",
        "",
        "## Stable ledger source",
        "",
        f"- Ledger JSON: `{DEFAULT_LEDGER_JSON.relative_to(ROOT)}`",
        f"- Stable plotfile: `{stable['plotfile']}`",
        f"- Unstable plotfile: `{unstable['plotfile']}`",
        f"- Stable input: `{ledger_payload.get('stable_input')}`",
        f"- Unstable input: `{ledger_payload.get('unstable_input')}`",
        f"- Producer command: `{ledger_payload.get('producer_command')}`",
        "",
        "## First-stage spike constant",
        "",
        f"- `spike_ratio_ref_stable = {spike_ratio_ref_stable:.16f}`",
        f"- `safety_factor = {safety_factor}`",
        f"- `SPIKE_RATIO_MAX = {spike_ratio_max:.16f}`",
        "",
        "## Why there is no energy gate",
        "",
        f"- Stable electric energy: `{stable['electric_energy']:.16e}`",
        f"- Zero-comoving electric energy: `{unstable['electric_energy']:.16e}`",
        f"- `stable_over_unstable_energy_ratio = {derived['stable_over_unstable_energy_ratio']:.16e}`",
        "",
        "The current local sibling does not inflate electric energy above the stable baseline, so `energy_ref_unstable` is not yet a defensible first-stage CI constant.",
        "",
    ]
    if scan_payload is not None:
        by_label = {
            item["label"]: item
            for item in scan_payload["derived_summary"]["candidates"]
            if item["status"] == "ok"
        }
        positive = by_label.get("positive-default-beta")
        half_default = by_label.get("half-default-beta")
        explicit = by_label.get("explicit-default-beta")
        lines.extend(
            [
                "## Velocity-only sibling scan cross-check",
                "",
                f"- Scan JSON: `{DEFAULT_SCAN_JSON.relative_to(ROOT)}`",
                f"- Explicit default beta energy/stable = `{explicit['stable_energy_ratio']:.16e}`",
                f"- Half-default beta energy/stable = `{half_default['stable_energy_ratio']:.16e}`",
                f"- Positive-default beta energy/stable = `{positive['stable_energy_ratio']:.16e}`",
                f"- Positive-default beta spike/stable = `{positive['stable_spike_ratio']:.16e}`",
                "",
                "The velocity-only scan confirms two things: default selector and explicit default velocity are numerically equivalent, and spike can worsen without producing a higher electric-energy ordering.",
                "",
            ]
        )
    if mpi2_payload is not None:
        metrics = mpi2_payload["comparisons"]
        stable = mpi2_payload["stable"]
        explicit = mpi2_payload["explicit_default"]
        positive = mpi2_payload["positive_sign"]
        lines.extend(
            [
                "## Real MPI=2 cross-check",
                "",
                f"- Contract JSON: `{DEFAULT_MPI2_JSON.relative_to(ROOT)}`",
                f"- Stable electric energy: `{stable['electric_energy']:.16e}`",
                f"- Explicit-default electric energy: `{explicit['electric_energy']:.16e}`",
                f"- Explicit/default energy relative difference: `{metrics['explicit_to_stable_energy_delta']:.3e}`",
                f"- Explicit/default spike relative difference: `{metrics['explicit_to_stable_spike_delta']:.3e}`",
                f"- Positive-sign spike/stable = `{metrics['positive_to_stable_spike_ratio']:.16e}`",
                "",
                "The real MPI=2 pair confirms selector equivalence and sign sensitivity at the plotfile level; it still does not justify an energy gate.",
                "",
            ]
        )
    lines.extend(
        [
            "## Review guidance",
            "",
            "If this draft is proposed upstream now, the review claim should stay narrow:",
            "",
            "1. comoving first-stage analysis now has a reproducible stable spike envelope;",
            "2. local evidence supports `finite + spike` as the honest first-stage gate;",
            "3. energy-gate work is deferred to a follow-up that uses stronger repeated/MPI contrast evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def render_packet(
    ledger_payload: dict,
    scan_payload: dict | None,
    mpi2_payload: dict | None,
    safety_factor: float,
) -> str:
    stable = ledger_payload["stable_metrics"]
    unstable = ledger_payload["unstable_metrics"]
    derived = ledger_payload["derived_contract_observations"]
    spike_ratio_ref_stable = derived["spike_ratio_ref_stable"]
    spike_ratio_max = spike_ratio_ref_stable * safety_factor
    lines = [
        "# Comoving first-stage submission packet",
        "",
        "This packet is the current upstream-facing handoff for the first-stage `test_2d_comoving_psatd_hybrid` analysis proposal.",
        "",
        "## Scope",
        "",
        "- Add a first-stage `analysis_comoving.py` helper.",
        "- Change the test wiring from `analysis=OFF` to `analysis_comoving.py diags/diag1000400`.",
        "- Keep the existing checksum consumer.",
        "- Do not change diagnostics surfaces yet.",
        "- Do not add an energy gate yet.",
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
        "This change upgrades the comoving PSATD test from checksum-only to a narrow first-stage `finite + spike` analysis gate whose threshold is reproducible from a stable local ledger. It deliberately does not claim a validated comoving energy-gate ordering.",
        "",
        "## Stable spike envelope",
        "",
        f"- Stable electric energy: `{stable['electric_energy']:.16e}`",
        f"- Stable spike ratio: `{stable['spike_ratio']:.16e}`",
        f"- `spike_ratio_ref_stable = {spike_ratio_ref_stable:.16f}`",
        f"- `safety_factor = {safety_factor}`",
        f"- `SPIKE_RATIO_MAX = {spike_ratio_max:.16f}`",
        "",
        "## Why energy gate is deferred",
        "",
        f"- Zero-comoving electric energy: `{unstable['electric_energy']:.16e}`",
        f"- `stable_over_unstable_energy_ratio = {derived['stable_over_unstable_energy_ratio']:.16e}`",
        "- The obvious local `no-comoving` sibling does not produce a higher electric-energy ordering than the stable baseline.",
        "",
    ]
    if scan_payload is not None:
        by_label = {
            item["label"]: item
            for item in scan_payload["derived_summary"]["candidates"]
            if item["status"] == "ok"
        }
        positive = by_label.get("positive-default-beta")
        lines.extend(
            [
                "## Velocity-only cross-check",
                "",
                f"- Positive-default beta spike/stable = `{positive['stable_spike_ratio']:.16e}`",
                f"- Positive-default beta energy/stable = `{positive['stable_energy_ratio']:.16e}`",
                "- This confirms that spike can get worse without producing a stronger electric-energy ordering inside the same comoving family.",
                "",
            ]
        )
    if mpi2_payload is not None:
        metrics = mpi2_payload["comparisons"]
        lines.extend(
            [
                "## Real MPI=2 cross-check",
                "",
                f"- Explicit/default energy relative difference = `{metrics['explicit_to_stable_energy_delta']:.3e}`",
                f"- Explicit/default spike relative difference = `{metrics['explicit_to_stable_spike_delta']:.3e}`",
                f"- Positive-sign spike/stable = `{metrics['positive_to_stable_spike_ratio']:.16e}`",
                "- This strengthens the selector/sign evidence without enabling an energy gate.",
                "",
            ]
        )
    lines.extend(
        [
            "## Review checklist",
            "",
            "1. Confirm the helper stays `finite + spike` only.",
            "2. Confirm checksum wiring is preserved.",
            "3. Confirm no producer-surface widening such as `divE` is bundled into this first-stage patch.",
            "4. Confirm the provenance note is attached so the spike constant can be audited.",
            "",
            "## Follow-up boundary",
            "",
            "If stronger repeated/MPI contrast later demonstrates a reliable comoving energy ordering, that should be proposed as a follow-up patch rather than being retrofitted into this first-stage packet.",
            "",
        ]
    )
    return "\n".join(lines)


def render_pr_draft(
    ledger_payload: dict,
    scan_payload: dict | None,
    mpi2_payload: dict | None,
    safety_factor: float,
) -> str:
    stable = ledger_payload["stable_metrics"]
    unstable = ledger_payload["unstable_metrics"]
    derived = ledger_payload["derived_contract_observations"]
    spike_ratio_ref_stable = derived["spike_ratio_ref_stable"]
    spike_ratio_max = spike_ratio_ref_stable * safety_factor

    lines = [
        "# Draft PR: add first-stage analysis for comoving PSATD test",
        "",
        "## Proposed title",
        "",
        "`Add first-stage analysis_comoving.py for test_2d_comoving_psatd_hybrid`",
        "",
        "## Summary",
        "",
        "- wire `test_2d_comoving_psatd_hybrid` to a new `analysis_comoving.py` helper;",
        "- keep the existing checksum consumer unchanged;",
        "- enforce `finite + spike` only in this first-stage helper;",
        "- defer any energy gate to a follow-up once a stronger comoving contrast is validated.",
        "",
        "## Review claim",
        "",
        "This PR upgrades the comoving PSATD test from checksum-only to a narrow first-stage analysis gate. The helper always checks field finiteness and rejects runs whose `spike_ratio` exceeds a reproducible stable-baseline envelope. It does not yet claim a validated comoving energy-ordering gate.",
        "",
        "## Reproducible constants",
        "",
        f"- Stable electric energy: `{stable['electric_energy']:.16e}`",
        f"- Stable spike ratio: `{stable['spike_ratio']:.16e}`",
        f"- Zero-comoving electric energy: `{unstable['electric_energy']:.16e}`",
        f"- `stable_over_unstable_energy_ratio = {derived['stable_over_unstable_energy_ratio']:.16e}`",
        f"- `spike_ratio_ref_stable = {spike_ratio_ref_stable:.16f}`",
        f"- `safety_factor = {safety_factor}`",
        f"- `SPIKE_RATIO_MAX = {spike_ratio_max:.16f}`",
        "",
    ]

    if scan_payload is not None:
        by_label = {
            item["label"]: item
            for item in scan_payload["derived_summary"]["candidates"]
            if item["status"] == "ok"
        }
        positive = by_label.get("positive-default-beta")
        explicit = by_label.get("explicit-default-beta")
        lines.extend(
            [
                "## Local cross-check",
                "",
                f"- Explicit-default beta energy/stable = `{explicit['stable_energy_ratio']:.16e}`",
                f"- Positive-default beta spike/stable = `{positive['stable_spike_ratio']:.16e}`",
                f"- Positive-default beta energy/stable = `{positive['stable_energy_ratio']:.16e}`",
                "- The local velocity-only scan shows that spike can worsen without producing a larger final electric energy inside the same comoving family.",
                "",
            ]
        )
    if mpi2_payload is not None:
        metrics = mpi2_payload["comparisons"]
        lines.extend(
            [
                "## Real MPI=2 cross-check",
                "",
                f"- Explicit/default energy relative difference = `{metrics['explicit_to_stable_energy_delta']:.3e}`",
                f"- Explicit/default spike relative difference = `{metrics['explicit_to_stable_spike_delta']:.3e}`",
                f"- Positive-sign spike/stable = `{metrics['positive_to_stable_spike_ratio']:.16e}`",
                "- The MPI pair supports selector equivalence and sign sensitivity, but not an energy-gate claim.",
                "",
            ]
        )

    lines.extend(
        [
            "## Out of scope",
            "",
            "- no `divE` or other producer-surface widening in this PR;",
            "- no comoving energy gate in this PR;",
            "- no claim that the current local `no-comoving` sibling is the final upstream unstable-energy reference.",
            "",
            "## Reviewer checklist",
            "",
            "1. The helper stays limited to `finite + spike`.",
            "2. The existing checksum path remains in place.",
            "3. The provenance note and ledger-backed constants are attached.",
            "4. Follow-up work for energy-gate validation remains explicitly deferred.",
            "",
        ]
    )
    return "\n".join(lines)


def render_bundle_readme(bundle_dir: Path) -> str:
    rel_bundle = bundle_dir.relative_to(ROOT)
    return "\n".join(
        [
            "# Comoving first-stage upstream staging bundle",
            "",
            "This directory mirrors the minimum assets needed to stage the current first-step",
            "`test_2d_comoving_psatd_hybrid` proposal into a WarpX worktree.",
            "",
            "## Contents",
            "",
            "- `warpx/Examples/Tests/nci_psatd_stability/analysis_comoving.py`",
            "- `warpx/comoving_first_stage_patch.diff`",
            "- `docs/comoving_first_stage_provenance_note.md`",
            "- `docs/comoving_first_stage_submission_packet.md`",
            "- `docs/comoving_first_stage_pr_draft.md`",
            "",
            "## Suggested use",
            "",
            "1. Copy `warpx/Examples/Tests/nci_psatd_stability/analysis_comoving.py` into the target WarpX checkout.",
            "2. Apply `warpx/comoving_first_stage_patch.diff` from the WarpX repository root, or edit `Examples/Tests/nci_psatd_stability/CMakeLists.txt` equivalently.",
            "3. Attach the three files under `docs/` when preparing the actual upstream proposal.",
            "4. Keep the first-stage scope at `finite + spike`; do not retrofit an energy gate into this bundle without a new calibration pass.",
            "",
            "PIC-tutor also provides a helper installer:",
            "",
            "```bash",
            "python scripts/stage_comoving_first_stage_patch.py --warpx-root /path/to/warpx --dry-run",
            "python scripts/stage_comoving_first_stage_patch.py --warpx-root /path/to/warpx",
            "python scripts/audit_comoving_first_stage_patch.py --warpx-root /path/to/warpx",
            "python scripts/report_comoving_first_stage_patch.py --warpx-root /path/to/warpx",
            "python scripts/preview_comoving_first_stage_patch.py --warpx-root /path/to/warpx",
            "```",
            "",
            "This script copies the helper and rewrites the comoving test's analysis line in",
            "`Examples/Tests/nci_psatd_stability/CMakeLists.txt` without touching any other",
            "test block.",
            "",
            "The audit script stays read-only and reports whether the target checkout is",
            "`unstaged`, `partial`, or fully `staged`.",
            "",
            "The report script stays read-only as well, but writes a markdown preflight note",
            "that summarizes the target checkout status and the exact next command to run.",
            "",
            "The preview script also stays read-only and prints the exact unified diff that",
            "the staging step would apply to the target checkout.",
            "",
            "This bundle is generated from:",
            f"- `{DEFAULT_LEDGER_JSON.relative_to(ROOT)}`",
            f"- `{DEFAULT_SCAN_JSON.relative_to(ROOT)}`",
            "",
            f"Bundle root: `{rel_bundle}`",
            "",
        ]
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def write_bundle(
    bundle_dir: Path,
    helper_text: str,
    diff_text: str,
    note_text: str,
    packet_text: str,
    pr_draft_text: str,
) -> None:
    bundle_root = bundle_dir.resolve()
    helper_path = (
        bundle_root / "warpx" / "Examples" / "Tests" / "nci_psatd_stability" / "analysis_comoving.py"
    )
    diff_path = bundle_root / "warpx" / "comoving_first_stage_patch.diff"
    note_path = bundle_root / "docs" / "comoving_first_stage_provenance_note.md"
    packet_path = bundle_root / "docs" / "comoving_first_stage_submission_packet.md"
    pr_path = bundle_root / "docs" / "comoving_first_stage_pr_draft.md"
    readme_path = bundle_root / "README.md"

    write_text(helper_path, helper_text)
    write_text(diff_path, diff_text)
    write_text(note_path, note_text)
    write_text(packet_path, packet_text)
    write_text(pr_path, pr_draft_text)
    write_text(readme_path, render_bundle_readme(bundle_root))


def main() -> None:
    args = parse_args()
    ledger_path = args.ledger_json.resolve()
    ledger_payload = load_ledger(ledger_path)
    spike_ratio_ref_stable, stable_spike_ratio = validate_ledger(
        ledger_payload, ledger_path
    )
    if abs(spike_ratio_ref_stable - stable_spike_ratio) > 1e-12:
        raise ValueError(
            "spike_ratio_ref_stable does not match stable_metrics.spike_ratio in ledger"
        )

    scan_payload = load_scan_payload(args.scan_json.resolve())
    mpi2_payload = load_scan_payload(args.mpi2_json.resolve())
    helper_text = render_helper(spike_ratio_ref_stable, args.safety_factor)
    diff_text = render_diff(helper_text)
    note_text = render_note(ledger_payload, scan_payload, mpi2_payload, args.safety_factor)
    packet_text = render_packet(ledger_payload, scan_payload, mpi2_payload, args.safety_factor)
    pr_draft_text = render_pr_draft(ledger_payload, scan_payload, mpi2_payload, args.safety_factor)
    write_text(args.helper_output.resolve(), helper_text)
    write_text(args.diff_output.resolve(), diff_text)
    write_text(args.note_output.resolve(), note_text)
    write_text(args.packet_output.resolve(), packet_text)
    write_text(args.pr_draft_output.resolve(), pr_draft_text)
    write_bundle(
        args.bundle_dir,
        helper_text,
        diff_text,
        note_text,
        packet_text,
        pr_draft_text,
    )


if __name__ == "__main__":
    main()
