#!/usr/bin/env python
"""Audit the minimal reduced-diagnostics examples used in Chapter 8."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.project_root.resolve()
    warpx = args.warpx_root.resolve()
    chapter = (root / "manuscript/chapters/08-diagnostics-cases.md").read_text(encoding="utf-8")
    reduced = (warpx / "Examples/Tests/reduced_diags/inputs_test_3d_reduced_diags").read_text(encoding="utf-8")
    laser = (warpx / "Examples/Physics_applications/laser_ion/inputs_test_2d_laser_ion_acc").read_text(encoding="utf-8")
    lbc_analysis = (warpx / "Examples/Tests/reduced_diags/analysis_reduced_diags_load_balance_costs.py").read_text(encoding="utf-8")
    cmake = (warpx / "Examples/Tests/reduced_diags/CMakeLists.txt").read_text(encoding="utf-8")

    checks = [
        ("reduced input exists", "warpx.reduced_diags_names" in reduced),
        ("FieldProbe scalar", "FP.type = FieldProbe" in reduced and "FP.intervals" in reduced),
        ("FieldProbe integrated line", "FP_integrate.integrate = 1" in reduced and "FP_line.probe_geometry = Line" in reduced),
        ("FieldProbe plane", "FP_plane.probe_geometry = Plane" in reduced),
        ("laser application exists", "warpx.reduced_diags_names" in laser),
        ("ParticleHistogram2D type", "PhaseSpaceIons.type                                 = ParticleHistogram2D" in laser and "PhaseSpaceElectrons.type                                 = ParticleHistogram2D" in laser),
        ("ParticleHistogram2D axes", "histogram_function_abs" in laser and "histogram_function_ord" in laser and "value_function" in laser),
        ("LoadBalanceCosts type", "LBC.type = LoadBalanceCosts" in laser and "algo.load_balance_costs_update" in laser),
        ("LoadBalanceCosts analysis", "efficiency_before" in lbc_analysis and "efficiency_after" in lbc_analysis),
        ("official CMake consumer", "analysis_reduced_diags_load_balance_costs.py" in cmake),
        ("chapter minimal-input section", "8.14.1" in chapter and "ParticleHistogram2D" in chapter and "LoadBalanceCosts" in chapter),
        ("chapter boundary language", "不把 `ParticleHistogram2D` writer/schema 变成物理收敛证明" in chapter and "不把 `LoadBalanceCosts` 的效率比较与场精度混为同一类 physics gate" in chapter),
    ]
    records = [{"name": name, "status": "PASS" if passed else "FAIL"} for name, passed in checks]
    passed = sum(record["status"] == "PASS" for record in records)
    payload = {"contract": "chapter-8-diagnostics-minimal-inputs", "passed": passed, "total": len(records), "checks": records}
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Chapter 8 Diagnostics Minimal Inputs Contract", "", f"- Result: **{passed}/{len(records)} PASS**", "", "| Check | Status |", "|---|---|"]
    lines.extend(f"| {record['name']} | {record['status']} |" for record in records)
    args.output_md.write_text("\n".join(lines) + "\n")
    print(f"{'PASS' if passed == len(records) else 'FAIL'}: {passed}/{len(records)} Chapter 8 minimal-input checks")
    return 0 if passed == len(records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
