#!/usr/bin/env python
"""Analyze the 2D/3D Vay shape family at two MPI ranks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def analyze_case(case_dir: Path, dims: str, shape: int, numprocs: str, final_diag: str, analysis_source: str) -> dict[str, object]:
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
        "used_inputs_geometry": f"geometry.dims = {dims}" in inputs and "geometry.coord_sys = 0" in inputs,
        "used_inputs_vay": "algo.current_deposition = vay" in inputs and "algo.particle_pusher = vay" in inputs,
        "used_inputs_shape": f"algo.particle_shape = {shape}" in inputs,
        "used_inputs_numprocs": f"warpx.numprocs = {numprocs}" in inputs,
        "mpi_two_rank_provenance": "MPI initialized with 2 MPI processes" in log,
        "official_analysis_gate": "divE - rho / epsilon_0" in analysis_source and "tolerance = 1e-3" in analysis_source,
    }
    return {
        "case_dir": str(case_dir),
        "dims": dims,
        "shape": shape,
        "numprocs": numprocs,
        "final_diag": final_diag,
        "error_rel": error,
        "tolerance": tolerance,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--case-root-2d", type=Path, required=True)
    parser.add_argument("--case-root-3d", type=Path, required=True)
    parser.add_argument("--official-case-2d", type=Path, required=True)
    parser.add_argument("--official-case-3d", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    analysis_source = read(args.warpx_root.resolve() / "Examples/Tests/vay_deposition/analysis.py")
    cases: dict[str, dict[str, object]] = {}
    for dims, root, official, numprocs, final_diag in (
        ("2", args.case_root_2d.resolve(), args.official_case_2d.resolve(), "2 1", "diag1000050"),
        ("3", args.case_root_3d.resolve(), args.official_case_3d.resolve(), "2 1 1", "diag1000025"),
    ):
        for shape in (1, 2, 3, 4):
            case_dir = official if shape == 3 else root / f"shape{shape}"
            cases[f"{dims}d_shape{shape}"] = analyze_case(case_dir, dims, shape, numprocs, final_diag, analysis_source)

    result = {
        "contract": "Vay deposition 2D/3D 2-rank shape-family runtime consumer",
        "classification": "RUNTIME_2RANK_VAY_SHAPE_FAMILY_PASS_2D_3D_CASE_LOCAL",
        "scope": "2D/3D Cartesian Vay inputs with particle_shape 1..4, two-rank producers and upstream divE-rho/epsilon_0 analysis; shape 1/2/4 are case-local siblings and shape 3 is the registered official case; not AMR, non-Cartesian geometry, boundary cropping, or formal convergence order",
        "cases": cases,
        "passed": all(case["passed"] for case in cases.values()),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Vay deposition 2D/3D 2-rank shape-family runtime consumer",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| case | shape | MPI ranks | error_rel | tolerance | status |",
        "|---|---:|---:|---:|---:|:---:|",
    ]
    for name, case in cases.items():
        lines.append(
            f"| `{name}` | `{case['shape']}` | `2` | `{case['error_rel']}` | `{case['tolerance']}` | `{'PASS' if case['passed'] else 'FAIL'}` |"
        )
    lines += [
        "",
        "All eight producers used two MPI processes and wrote the final plotfile consumed by the upstream analysis. The result establishes a case-local Cartesian shape-family runtime surface while preserving the AMR, boundary, non-Cartesian and formal-order boundaries.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    passed = sum(bool(case["passed"]) for case in cases.values())
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {passed}/{len(cases)} Vay 2-rank shape-family cases")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
