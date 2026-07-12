#!/usr/bin/env python
"""Audit the source/documentation boundary behind the RZ Esirkepov charge result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ANCHORS = {
    "official_rz_exclusion": ("official_analysis_utils", "geometry_dims_rz or maxwell_solver_psatd"),
    "official_exclusion_comment": ("official_analysis_utils", "do not check with Esirkepov deposition in RZ geometry"),
    "compute_div_e_entry": ("warpx", "WarpX::ComputeDivE"),
    "compute_div_e_fdtd": ("warpx", "m_fdtd_solver_fp[lev]->ComputeDivE"),
    "div_e_rz_node_path": ("div_e_functor", "amrex::IntVect::TheNodeVector()"),
    "div_e_compute": ("div_e_functor", "warpx.ComputeDivE(divE, m_lev)"),
    "rho_get_charge_density": ("rho_functor", "GetChargeDensity(m_lev, true)"),
    "rho_guard_transfer": ("rho_functor", "ApplyFilterandSumBoundaryRho"),
    "rho_interpolation": ("rho_functor", "InterpolateMFForDiag"),
    "full_diag_div_e_functor": ("full_diagnostics", "std::make_unique<DivEFunctor>"),
    "full_diag_rho_functor": ("full_diagnostics", "std::make_unique<RhoFunctor>"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path(__file__).resolve().parents[2] / "warpx")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    paths = {
        "official_analysis_utils": args.warpx_root / "Examples/Tests/langmuir/analysis_utils.py",
        "warpx": args.warpx_root / "Source/WarpX.cpp",
        "div_e_functor": args.warpx_root / "Source/Diagnostics/ComputeDiagFunctors/DivEFunctor.cpp",
        "rho_functor": args.warpx_root / "Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.cpp",
        "full_diagnostics": args.warpx_root / "Source/Diagnostics/FullDiagnostics.cpp",
    }
    source = {name: path.read_text(encoding="utf-8") for name, path in paths.items()}
    checks = {}
    for name, (source_name, needle) in ANCHORS.items():
        count = source[source_name].count(needle)
        checks[name] = {"source": source_name, "needle": needle, "count": count, "passed": count > 0}

    result = {
        "contract": "RZ Esirkepov charge diagnostic boundary source contract",
        "scope": "read-only source audit; explains diagnostic evidence boundary and is not a physics regression",
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["passed"] for item in checks.values()),
        "passed": all(item["passed"] for item in checks.values()),
        "checks": checks,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RZ Esirkepov charge diagnostic source contract",
        "",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
    ]
    lines.extend(f"- `{name}`: `{item['count']}` occurrence(s) - {'PASS' if item['passed'] else 'FAIL'}" for name, item in checks.items())
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {result['passed_anchor_count']}/{result['anchor_count']} RZ diagnostic anchors")
    if not result["passed"]:
        raise SystemExit("RZ charge diagnostic source contract failed")


if __name__ == "__main__":
    main()
