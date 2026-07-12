#!/usr/bin/env python
"""Audit geometry and particle-shape dispatch in the current WarpX checkout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check(source: str, needle: str, minimum: int = 1) -> dict[str, object]:
    count = source.count(needle)
    return {"needle": needle, "count": count, "passed": count >= minimum}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path(__file__).resolve().parents[2] / "warpx")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    files = {
        "charge_kernel": args.warpx_root / "Source/Particles/Deposition/ChargeDeposition.H",
        "charge_bridge": args.warpx_root / "Source/ablastr/particles/DepositCharge.H",
        "particle_container": args.warpx_root / "Source/Particles/WarpXParticleContainer.cpp",
        "startup": args.warpx_root / "Source/WarpX.cpp",
    }
    sources = {name: path.read_text(encoding="utf-8") for name, path in files.items()}

    checks: dict[str, dict[str, object]] = {}

    for macro in ("WARPX_DIM_1D_Z", "WARPX_DIM_XZ", "WARPX_DIM_RZ", "WARPX_DIM_RCYLINDER", "WARPX_DIM_RSPHERE", "WARPX_DIM_3D"):
        checks[f"charge_kernel_geometry_{macro}"] = check(sources["charge_kernel"], macro)
    for macro in ("WARPX_DIM_1D_Z", "WARPX_DIM_XZ", "WARPX_DIM_RZ", "WARPX_DIM_RCYLINDER", "WARPX_DIM_RSPHERE", "WARPX_DIM_3D"):
        checks[f"charge_bridge_geometry_{macro}"] = check(sources["charge_bridge"], macro)

    for family in (
        "doChargeDepositionShapeN",
        "doChargeDepositionSharedShapeN",
    ):
        for order in range(1, 5):
            checks[f"{family}_{order}"] = check(sources["particle_container"] if "Shared" in family else sources["charge_bridge"], f"{family}<{order}>")

    for family in (
        "doDepositionShapeN",
        "doDepositionShapeNImplicit",
        "doEsirkepovDepositionShapeN",
        "doChargeConservingDepositionShapeNImplicit",
        "doVillasenorDepositionShapeNExplicit",
        "doVillasenorDepositionShapeNImplicit",
        "doVayDepositionShapeN",
        "doDepositionSharedShapeN",
    ):
        for order in range(1, 5):
            checks[f"current_{family}_{order}"] = check(sources["particle_container"], f"{family}<{order}>")

    checks["startup_shape_range"] = check(
        sources["startup"],
        "(particle_shape >= 1) && (particle_shape <=4)",
    )

    result = {
        "contract": "deposition geometry/order source dispatch",
        "scope": "read-only source audit; does not claim runtime coverage for every geometry/order combination",
        "source_files": {name: str(path) for name, path in files.items()},
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["passed"] for item in checks.values()),
        "passed": all(item["passed"] for item in checks.values()),
        "checks": checks,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Deposition geometry/order source contract",
        "",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
    ]
    for name, item in checks.items():
        lines.append(f"- `{name}`: `{item['count']}` occurrence(s) - {'PASS' if item['passed'] else 'FAIL'}")
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {result['passed_anchor_count']}/{result['anchor_count']} deposition geometry/order anchors")
    if not result["passed"]:
        raise SystemExit("deposition geometry/order source contract failed")


if __name__ == "__main__":
    main()
