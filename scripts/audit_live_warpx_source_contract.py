#!/usr/bin/env python
"""Record the exact WarpX revision and scope of the book's live source audit."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# These are the source and official-analysis files consumed by the six
# crosswalks below.  Keep the list explicit so a dirty sibling worktree cannot
# silently broaden a "current source" statement beyond the inspected surface.
SOURCE_ANCHORS = (
    "Source/main.cpp",
    "Source/WarpX.cpp",
    "Source/Initialization/WarpXInitData.cpp",
    "Source/Evolve/WarpXEvolve.cpp",
    "Source/Particles/PhysicalParticleContainer.cpp",
    "Source/Particles/Pusher/UpdateMomentumBoris.H",
    "Source/Particles/Pusher/PushSelector.H",
    "Source/Particles/WarpXParticleContainer.cpp",
    "Source/Particles/Deposition/CurrentDeposition.H",
    "Source/Particles/Deposition/ChargeDeposition.H",
    "Source/ablastr/particles/DepositCharge.H",
    "Source/Particles/ShapeFactors.H",
    "Source/FieldSolver/WarpXPushFieldsEM.cpp",
    "Source/FieldSolver/SpectralSolver/SpectralSolver.cpp",
    "Source/FieldSolver/SpectralSolver/SpectralSolverRZ.cpp",
    "Source/BoundaryConditions/PMLComponent.H",
    "Source/BoundaryConditions/PML.cpp",
    "Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp",
    "Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp",
    "Source/FieldSolver/FiniteDifferenceSolver/EvolveBPML.cpp",
    "Source/FieldSolver/FiniteDifferenceSolver/EvolveEPML.cpp",
    "Source/BoundaryConditions/WarpXFieldBoundaries.cpp",
    "Source/BoundaryConditions/PEC_Insulator.H",
    "Source/BoundaryConditions/FieldBoundaries.cpp",
    "Source/Particles/ParticleBoundaries.cpp",
    "Source/BoundaryConditions/WarpXEvolvePML.cpp",
    "Source/Parallelization/WarpXComm.cpp",
    "Source/Parallelization/GuardCellManager.cpp",
    "Source/Parallelization/WarpXRegrid.cpp",
    "Source/Utils/WarpXMovingWindow.cpp",
    "Source/Diagnostics/BoundaryScrapingDiagnostics.cpp",
    "Source/Particles/ParticleBoundaries_K.H",
    "Source/Diagnostics/MultiDiagnostics.cpp",
    "Source/Diagnostics/FullDiagnostics.cpp",
    "Source/Diagnostics/FullDiagnostics.H",
    "Source/Diagnostics/WarpXOpenPMD.H",
    "Source/Diagnostics/ReducedDiags/MultiReducedDiags.cpp",
    "Source/Diagnostics/ReducedDiags/ReducedDiags.cpp",
    "Source/Diagnostics/Diagnostics.H",
    "Examples/Tests/langmuir/analysis_1d.py",
    "Examples/Tests/diff_lumi_diag/analysis.py",
)


def command_output(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).rstrip()


def dirty_entries(root: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for line in command_output(root, "status", "--porcelain=v1", "--untracked-files=all").splitlines():
        if not line:
            continue
        status, path = line[:2], line[3:]
        # Rename records retain both paths; either is relevant to an anchor.
        for candidate in path.split(" -> "):
            entries.append({"status": status, "path": candidate})
    return entries


def report_passed(report: dict[str, object]) -> bool:
    if "passed" in report:
        return bool(report["passed"])
    return report.get("pass_count") == report.get("check_count") and "check_count" in report


def run_crosswalks(project: Path, warpx: Path, work: Path) -> list[dict[str, object]]:
    specs = [
        (
            "chapter_3a",
            [
                "audit_3a_birdsall_warpx_crosswalk.py", "--project-root", str(project),
                "--warpx-root", str(warpx), "--output-json", str(work / "chapter_3a.json"),
                "--output-md", str(work / "chapter_3a.md"),
            ],
            work / "chapter_3a.json",
        ),
        (
            "chapter_4_boris",
            [
                "audit_boris_source_crosswalk.py", "--warpx-root", str(warpx),
                "--chapter", str(project / "manuscript/chapters/04-particle-pushers.md"),
                "--output-dir", str(work / "chapter_4_boris"),
            ],
            work / "chapter_4_boris" / "contract.json",
        ),
        (
            "chapter_5_deposition",
            [
                "audit_deposition_chapter_source_crosswalk.py", "--project-root", str(project),
                "--warpx-root", str(warpx), "--output-json", str(work / "chapter_5.json"),
                "--output-md", str(work / "chapter_5.md"),
            ],
            work / "chapter_5.json",
        ),
        (
            "chapter_6_field_solver",
            [
                "audit_field_solver_chapter_source_crosswalk.py", "--project-root", str(project),
                "--warpx-root", str(warpx), "--output-json", str(work / "chapter_6.json"),
                "--output-md", str(work / "chapter_6.md"),
            ],
            work / "chapter_6.json",
        ),
        (
            "chapter_7_boundary_amr",
            [
                "audit_boundary_amr_chapter_source_crosswalk.py", "--project-root", str(project),
                "--warpx-root", str(warpx), "--output-json", str(work / "chapter_7.json"),
                "--output-md", str(work / "chapter_7.md"),
            ],
            work / "chapter_7.json",
        ),
        (
            "chapter_8_diagnostics",
            [
                "audit_diagnostics_chapter_source_crosswalk.py", "--project-root", str(project),
                "--warpx-root", str(warpx), "--output-json", str(work / "chapter_8.json"),
                "--output-md", str(work / "chapter_8.md"),
            ],
            work / "chapter_8.json",
        ),
    ]
    results: list[dict[str, object]] = []
    for name, arguments, output in specs:
        completed = subprocess.run(
            [sys.executable, str(project / "scripts" / arguments[0]), *arguments[1:]],
            text=True,
            capture_output=True,
            check=False,
        )
        report = json.loads(output.read_text(encoding="utf-8")) if output.exists() else {}
        passed = report_passed(report)
        results.append(
            {
                "id": name,
                "status": "PASS" if completed.returncode == 0 and passed else "FAIL",
                "returncode": completed.returncode,
                "classification": report.get("classification"),
                "output": str(output.relative_to(work)),
                "stderr": completed.stderr.strip(),
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    project = args.project_root.resolve()
    warpx = args.warpx_root.resolve()
    with tempfile.TemporaryDirectory(prefix="pic-tutor-live-source-") as temporary:
        crosswalks = run_crosswalks(project, warpx, Path(temporary))

    dirty = dirty_entries(warpx)
    dirty_paths = {entry["path"] for entry in dirty}
    anchor_dirty_paths = sorted(set(SOURCE_ANCHORS) & dirty_paths)
    passed = all(item["status"] == "PASS" for item in crosswalks) and not anchor_dirty_paths
    payload = {
        "contract": "PIC-tutor live WarpX source scope audit",
        "classification": (
            "CURRENT_WARPX_CORE_CHAPTER_SOURCE_ANCHORS_VERIFIED_DIRTY_UNRELATED_PATHS_RECORDED"
            if passed else "CURRENT_WARPX_SOURCE_AUDIT_REVIEW_REQUIRED"
        ),
        "scope": (
            "Runs the Chapter 3A--8 representative source crosswalks at one Git revision. "
            "A dirty WarpX worktree is acceptable only when none of its paths intersects the explicit audited anchors; "
            "this is not a clean-tree assertion, a semantic equivalence proof, or a runtime physics regression."
        ),
        "warpx_head": command_output(warpx, "rev-parse", "HEAD"),
        "warpx_dirty_entries": dirty,
        "source_anchor_count": len(SOURCE_ANCHORS),
        "source_anchor_dirty_paths": anchor_dirty_paths,
        "crosswalks": crosswalks,
        "passed": passed,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# PIC-tutor live WarpX source scope audit",
        "",
        f"- status: `{'PASS' if passed else 'FAIL'}`",
        f"- classification: `{payload['classification']}`",
        f"- WarpX revision: `{payload['warpx_head']}`",
        f"- audited source/analysis anchors: `{payload['source_anchor_count']}`",
        f"- dirty worktree paths: `{len(dirty)}`",
        f"- dirty paths intersecting audited anchors: `{len(anchor_dirty_paths)}`",
        f"- scope: {payload['scope']}",
        "",
        "## Crosswalks",
        "",
        "| Chapter surface | Status | Classification |",
        "|---|:---:|---|",
    ]
    for item in crosswalks:
        lines.append(f"| `{item['id']}` | `{item['status']}` | `{item['classification'] or '-'}` |")
    lines += ["", "## Dirty WarpX paths", ""]
    if dirty:
        lines.extend(f"- `{entry['status']} {entry['path']}`" for entry in dirty)
    else:
        lines.append("- none")
    if anchor_dirty_paths:
        lines += ["", "## Review-required anchor intersections", ""]
        lines.extend(f"- `{path}`" for path in anchor_dirty_paths)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if passed else 'FAIL'}: live WarpX source scope audit")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
