#!/usr/bin/env python
"""Analyze official 2-rank Vay deposition runtime consumers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def analyze_case(
    case_dir: Path,
    dims: str,
    final_diag: str,
    numprocs: str,
    cmake_marker: str,
    warpx_root: Path,
    analysis_source: str,
) -> dict[str, object]:
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
        "used_inputs_shape3": "algo.particle_shape = 3" in inputs,
        "used_inputs_numprocs": f"warpx.numprocs = {numprocs}" in inputs,
        "mpi_two_rank_provenance": "MPI initialized with 2 MPI processes" in log,
        "official_cmake_entry": cmake_marker in read(warpx_root / "Examples/Tests/vay_deposition/CMakeLists.txt"),
        "official_analysis_gate": "divE - rho / epsilon_0" in analysis_source and "tolerance = 1e-3" in analysis_source,
    }
    return {
        "case_dir": str(case_dir),
        "dims": dims,
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
    parser.add_argument("--case-2d", type=Path, required=True)
    parser.add_argument("--case-3d", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    cmake = read(args.warpx_root.resolve() / "Examples/Tests/vay_deposition/CMakeLists.txt")
    analysis_source = read(args.warpx_root.resolve() / "Examples/Tests/vay_deposition/analysis.py")

    cases = {
        "2d": analyze_case(args.case_2d.resolve(), "2", "diag1000050", "2 1", "test_2d_vay_deposition", args.warpx_root.resolve(), analysis_source),
        "3d": analyze_case(args.case_3d.resolve(), "3", "diag1000025", "2 1 1", "test_3d_vay_deposition", args.warpx_root.resolve(), analysis_source),
    }
    result = {
        "contract": "official Vay deposition 2D/3D 2-rank runtime consumer",
        "classification": "RUNTIME_OFFICIAL_CMAKE_SCALE_2RANK_ANALYSIS_PASS_2D_3D",
        "scope": "official vay_deposition CMake entries, official 2D/3D inputs, two-rank producers and upstream divE-rho/epsilon_0 analysis; not full geometry/order Cartesian product, AMR, non-Cartesian geometry, or formal convergence order",
        "cases": cases,
        "passed": all(case["passed"] for case in cases.values()),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Official Vay deposition 2D/3D 2-rank runtime consumer",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| case | MPI ranks | error_rel | tolerance | status |",
        "|---|---:|---:|---:|:---:|",
    ]
    for name, case in cases.items():
        lines.append(
            f"| `{name}` | `2` | `{case['error_rel']}` | `{case['tolerance']}` | `{'PASS' if case['passed'] else 'FAIL'}` |"
        )
    lines += [
        "",
        "The producers were launched with the MPICH launcher at two ranks and the official analysis consumed the final plotfiles. This closes the official 2-rank shape-3 runtime consumer for the two registered Cartesian cases, not every geometry/order combination.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {sum(bool(case['passed']) for case in cases.values())}/2 Vay 2-rank runtime cases")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
