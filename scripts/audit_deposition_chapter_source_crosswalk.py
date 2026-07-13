#!/usr/bin/env python
"""Check that Chapter 5 claims still point at current WarpX source surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check(text: str, *needles: str) -> dict[str, object]:
    missing = [needle for needle in needles if needle not in text]
    return {"needles": list(needles), "missing": missing, "passed": not missing}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    chapter = (args.project_root / "manuscript/chapters/05-deposition-shapes.md").read_text(encoding="utf-8")
    container = (args.warpx_root / "Source/Particles/WarpXParticleContainer.cpp").read_text(encoding="utf-8")
    current = (args.warpx_root / "Source/Particles/Deposition/CurrentDeposition.H").read_text(encoding="utf-8")
    charge = (args.warpx_root / "Source/Particles/Deposition/ChargeDeposition.H").read_text(encoding="utf-8")
    bridge = (args.warpx_root / "Source/ablastr/particles/DepositCharge.H").read_text(encoding="utf-8")
    shapes = (args.warpx_root / "Source/Particles/ShapeFactors.H").read_text(encoding="utf-8")

    checks = {
        "chapter_names_charge_bridge": check(chapter, "DepositCharge()", "deposit_charge", "ChargeDeposition.H"),
        "chapter_names_temporal_bridge": check(chapter, "time_shift_delta", "LowerCorner(tilebox, depos_lev, time_shift_delta)", "icomp==0", "icomp==1"),
        "chapter_names_implicit_dispatch": check(chapter, "doChargeConservingDepositionShapeNImplicit", "doVillasenorDepositionShapeNImplicit", "x_n", "u_{n+1/2}"),
        "chapter_names_shared_villasenor": check(chapter, "VillasenorDepositionShapeNKernel", "cell_crossings", "num_segments", "do_cropping"),
        "chapter_names_geometry_surface": check(chapter, "WARPX_DIM_RZ", "WARPX_DIM_RCYLINDER", "WARPX_DIM_RSPHERE", "WARPX_DIM_1D_Z"),
        "container_charge_surface": check(container, "time_shift_delta", "LowerCorner(tilebox, depos_lev, time_shift_delta)", "ablastr::particles::deposit_charge", "doChargeDepositionSharedShapeN<4>"),
        "container_current_dispatch": check(container, "doChargeConservingDepositionShapeNImplicit<4>", "doVillasenorDepositionShapeNImplicit<4>", "CurrentDepositionAlgo::Vay", "doDepositionShapeN<4>"),
        "current_implicit_reconstruction": check(current, "xp_np1 = 2._prt*xp_nph - xp_n", "GetImplicitGammaInverse", "doChargeConservingDepositionShapeNImplicit", "doVillasenorDepositionShapeNImplicit"),
        "current_shared_villasenor_kernel": check(current, "VillasenorDepositionShapeNKernel", "crop_at_boundary", "cell_crossings", "num_segments"),
        "current_geometry_branches": check(current, "WARPX_DIM_RZ", "WARPX_DIM_RCYLINDER", "WARPX_DIM_RSPHERE", "WARPX_DIM_1D_Z"),
        "charge_kernel_surface": check(charge, "doChargeDepositionShapeN", "doChargeDepositionSharedShapeN", "Compute_shape_factor", "invvol"),
        "bridge_level_and_cpu_gpu_surface": check(bridge, "depos_lev", "rel_ref_ratio", "amrex::MultiFab rhoi", "lockAdd"),
        "shape_helper_surface": check(shapes, "Compute_shape_factor", "Compute_shifted_shape_factor", "Compute_shape_factor_pair"),
    }
    result = {
        "contract": "Chapter 5 deposition source crosswalk",
        "classification": "CHAPTER_SOURCE_CROSSWALK_CURRENT_WARPX_ANCHORS_VERIFIED",
        "scope": "Checks representative Chapter 5 claims against current WarpX source markers; not a semantic proof or runtime regression.",
        "chapter": str(args.project_root / "manuscript/chapters/05-deposition-shapes.md"),
        "warpx_root": str(args.warpx_root),
        "checks": checks,
    }
    result["passed"] = all(item["passed"] for item in checks.values())
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Chapter 5 deposition source crosswalk",
        "",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
    ]
    for name, item in checks.items():
        lines.append(f"- `{name}`: `{'PASS' if item['passed'] else 'FAIL'}`")
        if item["missing"]:
            lines.append(f"  - missing: `{', '.join(item['missing'])}`")
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {len(checks)} Chapter 5 source crosswalk groups")
    if not result["passed"]:
        raise SystemExit("Chapter 5 deposition source crosswalk failed")


if __name__ == "__main__":
    main()
