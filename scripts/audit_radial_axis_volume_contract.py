#!/usr/bin/env python
"""Audit radial geometry axis-volume correction semantics in current WarpX."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ANCHORS = {
    "parameter_default": ("parameters", "boundary.verboncoeur_axis_correction"),
    "parameter_volume_note": ("parameters", "pi*\\Delta dr^2/4"),
    "parameter_query": ("warpx", "query(\"verboncoeur_axis_correction\", m_verboncoeur_axis_correction)"),
    "member_default": ("warpx_header", "bool m_verboncoeur_axis_correction = true"),
    "rz_cylinder_on_off": ("push_fields", "m_verboncoeur_axis_correction ? 1.0_rt/3.0_rt : 1.0_rt/4.0_rt"),
    "sphere_on_off": ("push_fields", "m_verboncoeur_axis_correction ? 1.0_rt/4.0_rt : 1.0_rt/8.0_rt"),
    "charge_scaling_entry": ("push_fields", "WarpX::ApplyInverseVolumeScalingToChargeDensity"),
    "charge_scaling_definition": ("push_fields", "void\nWarpX::ApplyInverseVolumeScalingToChargeDensity"),
    "evolve_charge_scaling": ("evolve", "ApplyInverseVolumeScalingToChargeDensity(m_fields.get(FieldType::rho_fp, lev), lev)"),
    "evolve_buffer_scaling": ("evolve", "ApplyInverseVolumeScalingToChargeDensity(m_fields.get(FieldType::rho_buf, lev), lev-1)"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path(__file__).resolve().parents[2] / "warpx")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    paths = {
        "parameters": args.warpx_root / "Docs/source/usage/parameters.rst",
        "warpx": args.warpx_root / "Source/WarpX.cpp",
        "warpx_header": args.warpx_root / "Source/WarpX.H",
        "push_fields": args.warpx_root / "Source/FieldSolver/WarpXPushFieldsEM.cpp",
        "evolve": args.warpx_root / "Source/Evolve/WarpXEvolve.cpp",
    }
    source = {name: path.read_text(encoding="utf-8") for name, path in paths.items()}
    checks = {}
    for name, (source_name, needle) in ANCHORS.items():
        count = source[source_name].count(needle)
        checks[name] = {"source": source_name, "needle": needle, "count": count, "passed": count > 0}
    result = {
        "contract": "radial geometry axis-volume correction source contract",
        "scope": "read-only source audit; not a numerical regression or default-change recommendation",
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["passed"] for item in checks.values()),
        "passed": all(item["passed"] for item in checks.values()),
        "checks": checks,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Radial geometry axis-volume correction source contract",
        "",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
    ]
    lines.extend(f"- `{name}`: `{item['count']}` occurrence(s) - {'PASS' if item['passed'] else 'FAIL'}" for name, item in checks.items())
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {result['passed_anchor_count']}/{result['anchor_count']} radial axis-volume anchors")
    if not result["passed"]:
        raise SystemExit("radial axis-volume source contract failed")


if __name__ == "__main__":
    main()
