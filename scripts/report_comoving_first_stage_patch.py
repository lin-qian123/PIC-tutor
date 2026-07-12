#!/usr/bin/env python
"""Generate a preflight report for staging the comoving first-stage patch."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE_DIR = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_bundle"
)
DEFAULT_REPORT_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_target_report.md"
)
AUDIT_SCRIPT = ROOT / "scripts" / "audit_comoving_first_stage_patch.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a markdown preflight report for a target WarpX checkout."
    )
    parser.add_argument(
        "--warpx-root",
        type=Path,
        required=True,
        help="Path to the target WarpX repository root.",
    )
    parser.add_argument(
        "--bundle-dir",
        type=Path,
        default=DEFAULT_BUNDLE_DIR,
        help="Path to the generated comoving first-stage bundle.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Markdown output path for the report.",
    )
    return parser.parse_args()


def run_audit(warpx_root: Path, bundle_dir: Path) -> dict:
    cmd = [
        sys.executable,
        str(AUDIT_SCRIPT),
        "--warpx-root",
        str(warpx_root),
        "--bundle-dir",
        str(bundle_dir),
        "--json",
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=ROOT)
    return json.loads(result.stdout)


def render_next_steps(report: dict, warpx_root: Path) -> list[str]:
    overall = report["overall_status"]
    stage_cmd = (
        f"python scripts/stage_comoving_first_stage_patch.py --warpx-root {warpx_root}"
    )
    preview_cmd = (
        f"python scripts/preview_comoving_first_stage_patch.py --warpx-root {warpx_root}"
    )
    dry_run_cmd = (
        f"python scripts/stage_comoving_first_stage_patch.py --warpx-root {warpx_root} --dry-run"
    )
    audit_cmd = f"python scripts/audit_comoving_first_stage_patch.py --warpx-root {warpx_root}"

    if overall == "unstaged":
        return [
            f"- Run `{preview_cmd}` to inspect the exact unified diff before writing anything.",
            f"- Run `{dry_run_cmd}` to verify the same target files are about to be staged.",
            f"- Then run `{stage_cmd}` to stage the first-stage helper into the target checkout.",
            f"- Re-run `{audit_cmd}` to confirm the checkout moves to `staged`.",
        ]
    if overall == "partial":
        return [
            f"- Inspect the helper and CMake divergence reported below before writing anything.",
            f"- Run `{preview_cmd}` to compare the current checkout against the bundle as a unified diff.",
            f"- Use `{dry_run_cmd}` to compare the target checkout with the current PIC-tutor bundle.",
            f"- After reconciling local edits, run `{audit_cmd}` again to verify whether the tree is now `partial` or `staged`.",
        ]
    return [
        f"- The target checkout already matches the current bundle.",
        "- If you change the ledger-derived helper or review assets later, regenerate the bundle first and re-run the audit.",
    ]


def render_report(report: dict, warpx_root: Path, bundle_dir: Path) -> str:
    helper = report["helper"]
    cmake = report["cmake"]
    next_steps = render_next_steps(report, warpx_root)
    rel_bundle = bundle_dir.relative_to(ROOT)

    lines = [
        "# Comoving first-stage target report",
        "",
        f"- Target WarpX root: `{warpx_root}`",
        f"- Bundle root: `{rel_bundle}`",
        f"- Overall status: `{report['overall_status']}`",
        "",
        "## Helper status",
        "",
        f"- Path: `{helper['path']}`",
        f"- Status: `{helper['status']}`",
        f"- Detail: {helper['detail']}",
        "",
        "## CMake status",
        "",
        f"- Path: `{cmake['path']}`",
        f"- Status: `{cmake['status']}`",
        f"- Detail: {cmake['detail']}",
    ]
    if cmake["line"]:
        lines.append(f"- Current line: `{cmake['line']}`")

    lines.extend(
        [
            "",
            "## Attached bundle docs",
            "",
            "- `notes/code-reading/fieldsolver/comoving_first_stage_bundle/docs/comoving_first_stage_provenance_note.md`",
            "- `notes/code-reading/fieldsolver/comoving_first_stage_bundle/docs/comoving_first_stage_submission_packet.md`",
            "- `notes/code-reading/fieldsolver/comoving_first_stage_bundle/docs/comoving_first_stage_pr_draft.md`",
            "",
            "## Recommended next steps",
            "",
        ]
    )
    lines.extend(next_steps)
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    warpx_root = args.warpx_root.resolve()
    bundle_dir = args.bundle_dir.resolve()
    report = run_audit(warpx_root, bundle_dir)
    markdown = render_report(report, warpx_root, bundle_dir)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
