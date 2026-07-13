#!/usr/bin/env python
"""Analyze single-rank executions of the official 2D/3D Vay cases."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def case_contract(case_dir: Path, dims: str, final_diag: str) -> dict[str, object]:
    inputs = read(case_dir / "warpx_used_inputs")
    analysis = read(case_dir / "analysis.log")
    match = re.search(r"error_rel = ([0-9.eE+-]+)", analysis)
    tolerance = re.search(r"tolerance = ([0-9.eE+-]+)", analysis)
    error = float(match.group(1)) if match else None
    tol = float(tolerance.group(1)) if tolerance else None
    plotfile = case_dir / "diags" / final_diag
    checks = {
        "plotfile_exists": (plotfile / "Header").is_file(),
        "analysis_report_present": match is not None and tolerance is not None,
        "analysis_passed": error is not None and tol is not None and error < tol,
        "used_inputs_geometry": f"geometry.dims = {dims}" in inputs,
        "used_inputs_vay": "algo.current_deposition = vay" in inputs and "algo.particle_pusher = vay" in inputs,
        "used_inputs_psatd_collocated": "algo.maxwell_solver = psatd" in inputs and "warpx.grid_type = collocated" in inputs,
        "used_inputs_shape3": "algo.particle_shape = 3" in inputs,
        "single_rank_provenance": "MPI initialized with 1 MPI processes" in read(case_dir / "warpx.log"),
    }
    return {
        "case_dir": str(case_dir),
        "dims": dims,
        "final_diag": final_diag,
        "error_rel": error,
        "tolerance": tol,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-2d", type=Path, required=True)
    parser.add_argument("--case-3d", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    cases = {
        "2d": case_contract(args.case_2d.resolve(), "2", "diag1000050"),
        "3d": case_contract(args.case_3d.resolve(), "3", "diag1000025"),
    }
    result = {
        "contract": "official Vay deposition 2D/3D runtime consumer",
        "classification": "RUNTIME_SINGLE_RANK_OFFICIAL_ANALYSIS_PASS_2D_3D",
        "scope": "official Vay inputs, single-rank producers, final plotfiles and upstream divE-rho/epsilon_0 analysis; not the official 2-rank Cartesian-product regression",
        "cases": cases,
        "passed": all(case["passed"] for case in cases.values()),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Official Vay deposition 2D/3D runtime consumer", "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}", "",
        "| case | error_rel | tolerance | status |", "|---|---:|---:|:---:|",
    ]
    for name, case in cases.items():
        lines.append(f"| `{name}` | `{case['error_rel']}` | `{case['tolerance']}` | `{'PASS' if case['passed'] else 'FAIL'}` |")
    lines += [
        "",
        "Both producers were run with `warpx.numprocs='1 1'` or `warpx.numprocs='1 1 1'`. The official CMake entries request two MPI ranks; this contract therefore proves a single-rank reproduction of the official analysis, not the full 2-rank regression.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: Vay 2D/3D runtime consumer")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
