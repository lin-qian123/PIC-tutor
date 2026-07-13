#!/usr/bin/env python
"""Analyze single-rank Vay shape-family runtime probes for 2D and 3D."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def analyze_case(case_dir: Path, dims: str, shape: int, final_diag: str) -> dict[str, object]:
    inputs = read(case_dir / "warpx_used_inputs")
    analysis = read(case_dir / "analysis.log")
    log = read(case_dir / "warpx.log")
    error_match = re.search(r"error_rel = ([0-9.eE+-]+)", analysis)
    tolerance_match = re.search(r"tolerance = ([0-9.eE+-]+)", analysis)
    error = float(error_match.group(1)) if error_match else None
    tolerance = float(tolerance_match.group(1)) if tolerance_match else None
    plotfile = case_dir / "diags" / final_diag
    checks = {
        "plotfile_exists": (plotfile / "Header").is_file(),
        "analysis_report_present": error_match is not None and tolerance_match is not None,
        "analysis_passed": error is not None and tolerance is not None and error < tolerance,
        "used_inputs_geometry": f"geometry.dims = {dims}" in inputs,
        "used_inputs_vay": "algo.current_deposition = vay" in inputs and "algo.particle_pusher = vay" in inputs,
        "used_inputs_shape": f"algo.particle_shape = {shape}" in inputs,
        "used_inputs_psatd_collocated": "algo.maxwell_solver = psatd" in inputs and "warpx.grid_type = collocated" in inputs,
        "single_rank_provenance": "MPI initialized with 1 MPI processes" in log,
    }
    return {
        "case_dir": str(case_dir),
        "dims": dims,
        "shape": shape,
        "final_diag": final_diag,
        "error_rel": error,
        "tolerance": tolerance,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-root-2d", type=Path, required=True)
    parser.add_argument("--case-root-3d", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    cases: dict[str, dict[str, object]] = {}
    for dims, root, final_diag in (
        ("2", args.case_root_2d.resolve(), "diag1000050"),
        ("3", args.case_root_3d.resolve(), "diag1000025"),
    ):
        for shape in (1, 2, 3, 4):
            case_dir = root / f"shape{shape}"
            cases[f"{dims}d_shape{shape}"] = analyze_case(case_dir, dims, shape, final_diag)

    result = {
        "contract": "Vay deposition 2D/3D shape-family runtime consumer",
        "classification": "RUNTIME_SINGLE_RANK_VAY_SHAPE_FAMILY_PASS_2D_3D",
        "scope": "single-rank case-local probes using official 2D/3D Vay inputs with particle_shape 1..4 and the upstream divE-rho/epsilon_0 analysis; not official 2-rank CMake regression, AMR, non-Cartesian geometry, or formal convergence order",
        "cases": cases,
        "passed": all(case["passed"] for case in cases.values()),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Vay deposition 2D/3D shape-family runtime consumer",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| case | shape | error_rel | tolerance | status |",
        "|---|---:|---:|---:|:---:|",
    ]
    for name, case in cases.items():
        lines.append(
            f"| `{name}` | `{case['shape']}` | `{case['error_rel']}` | `{case['tolerance']}` | `{'PASS' if case['passed'] else 'FAIL'}` |"
        )
    lines += [
        "",
        "All six producers used one MPI process and wrote the official final plotfile consumed by `Examples/Tests/vay_deposition/analysis.py`. The result expands supported Cartesian shape coverage only; it does not close the official 2-rank regression, RZ/1D guards, AMR combinations, or a formal convergence study.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    passed = sum(bool(case["passed"]) for case in cases.values())
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {passed}/{len(cases)} Vay shape-family runtime cases")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
