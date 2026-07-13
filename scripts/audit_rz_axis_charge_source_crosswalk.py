#!/usr/bin/env python
"""Audit the source-level boundary between RZ rho scaling and divE diagnostics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ANCHORS = {
    "axis_parameter_query": ("warpx", 'query("verboncoeur_axis_correction", m_verboncoeur_axis_correction)'),
    "axis_volume_factor": ("push_fields", "m_verboncoeur_axis_correction ? 1.0_rt/3.0_rt : 1.0_rt/4.0_rt"),
    "rho_scaling_definition": ("push_fields", "WarpX::ApplyInverseVolumeScalingToChargeDensity (amrex::MultiFab* Rho, int lev) const"),
    "rho_scaling_after_deposition": ("evolve", "ApplyInverseVolumeScalingToChargeDensity(m_fields.get(FieldType::rho_fp, lev), lev)"),
    "rho_buffer_scaling": ("evolve", "ApplyInverseVolumeScalingToChargeDensity(m_fields.get(FieldType::rho_buf, lev), lev-1)"),
    "rho_diag_redeposition": ("rho_functor", "mypc.GetChargeDensity(m_lev, true)"),
    "rho_diag_boundary_sync": ("rho_functor", "warpx.ApplyFilterandSumBoundaryRho(m_lev, m_lev, *rho, 0, rho->nComp())"),
    "rho_diag_interpolation": ("rho_functor", "InterpolateMFForDiag(mf_dst, *rho, dcomp, warpx.DistributionMap(m_lev)"),
    "dive_solver_entry": ("warpx", "WarpX::ComputeDivE(amrex::MultiFab& divE, const int lev)"),
    "dive_fdtd_or_spectral": ("warpx", "m_fdtd_solver_fp[lev]->ComputeDivE(Efield_aux_lev, divE)"),
    "dive_diag_functor": ("dive_functor", "warpx.ComputeDivE(divE, m_lev)"),
    "dive_diag_coarsen": ("dive_functor", "ablastr::coarsen::sample::Coarsen( mf_dst, divE, dcomp"),
    "separate_diag_functors": ("diagnostics", "std::make_unique<DivEFunctor>"),
}


def line_number(text: str, needle: str) -> int | None:
    for number, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return number
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path(__file__).resolve().parents[2] / "warpx")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    paths = {
        "warpx": args.warpx_root / "Source/WarpX.cpp",
        "push_fields": args.warpx_root / "Source/FieldSolver/WarpXPushFieldsEM.cpp",
        "evolve": args.warpx_root / "Source/Evolve/WarpXEvolve.cpp",
        "rho_functor": args.warpx_root / "Source/Diagnostics/ComputeDiagFunctors/RhoFunctor.cpp",
        "dive_functor": args.warpx_root / "Source/Diagnostics/ComputeDiagFunctors/DivEFunctor.cpp",
        "diagnostics": args.warpx_root / "Source/Diagnostics/FullDiagnostics.cpp",
    }
    source = {name: path.read_text(encoding="utf-8") for name, path in paths.items()}
    checks = {}
    for name, (source_name, needle) in ANCHORS.items():
        count = source[source_name].count(needle)
        checks[name] = {
            "source": str(paths[source_name].relative_to(args.warpx_root)),
            "needle": needle,
            "count": count,
            "line": line_number(source[source_name], needle),
            "passed": count > 0,
        }
    result = {
        "contract": "RZ axis charge source and diagnostic crosswalk",
        "classification": "SOURCE_DIAGNOSTIC_DISCRETIZATION_BOUNDARY",
        "scope": "read-only WarpX source audit; it does not identify a kernel root cause",
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["passed"] for item in checks.values()),
        "passed": all(item["passed"] for item in checks.values()),
        "checks": checks,
        "interpretation": {
            "rho_path": "particle rho is volume-scaled after deposition, including rho_buf at the coarse level",
            "divE_path": "divE is computed from E by the field solver and then coarsened/interpolated by diagnostics",
            "comparison_boundary": "rho and divE are emitted by separate diagnostic functors; residual alone does not isolate the deposition kernel",
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RZ axis charge source and diagnostic crosswalk",
        "",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "## Source boundary",
        "",
        "- `rho`: particle deposition is followed by inverse-volume scaling; `rho_buf` is scaled with coarse-level geometry.",
        "- `divE`: the field solver computes divergence from E; the diagnostic functor coarsens/interpolates that temporary field.",
        "- comparison: `rho` and `divE` use separate diagnostic functors, so the residual is a boundary observable, not a kernel attribution.",
        "",
        "## Anchors",
        "",
    ]
    lines.extend(
        f"- `{name}`: `{item['source']}:{item['line']}` - {'PASS' if item['passed'] else 'FAIL'}"
        for name, item in checks.items()
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {result['passed_anchor_count']}/{result['anchor_count']} RZ axis source crosswalk anchors")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
