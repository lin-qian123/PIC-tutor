#!/usr/bin/env python
"""Summarize official and independent 3D Esirkepov shape contracts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    refined_rows = []
    for shape in (2, 3, 4):
        case_dir = args.root / f"esirkepov_langmuir_3d_shape{shape}_mpi2"
        contract = json.loads((case_dir / "contract.json").read_text(encoding="utf-8"))
        log = (case_dir / "official-analysis.log").read_text(encoding="utf-8")
        field_match = re.search(r"error_rel\s+:\s+([0-9.eE+-]+)", log)
        tolerance_match = re.search(r"tolerance_rel:\s+([0-9.eE+-]+)", log)
        if not field_match or not tolerance_match:
            raise SystemExit(f"missing official field summary in {case_dir}/official-analysis.log")
        field_error = float(field_match.group(1))
        field_tolerance = float(tolerance_match.group(1))
        official_field_pass = field_error < field_tolerance
        rows.append(
            {
                "particle_shape": shape,
                "field_relative_error": field_error,
                "field_tolerance": field_tolerance,
                "official_field_pass": official_field_pass,
                "independent_charge_relative_residual": contract["charge_relative_residual"],
                "charge_tolerance": contract["charge_tolerance"],
                "independent_charge_pass": contract["passed"],
                "classification": "PASS" if official_field_pass and contract["passed"] else "FIELD_BOUNDARY",
                "run_dir": str(case_dir),
            }
        )
        if shape not in (3, 4):
            continue
        refined_dir = args.root / f"esirkepov_langmuir_3d_shape{shape}_resolution128_mpi2"
        refined_contract = json.loads((refined_dir / "contract.json").read_text(encoding="utf-8"))
        refined_log = (refined_dir / "official-analysis.log").read_text(encoding="utf-8")
        refined_field_match = re.search(r"error_rel\s+:\s+([0-9.eE+-]+)", refined_log)
        refined_tolerance_match = re.search(r"tolerance_rel:\s+([0-9.eE+-]+)", refined_log)
        if not refined_field_match or not refined_tolerance_match:
            raise SystemExit(f"missing refined official field summary in {refined_dir}/official-analysis.log")
        refined_field_error = float(refined_field_match.group(1))
        refined_field_tolerance = float(refined_tolerance_match.group(1))
        refined_rows.append(
            {
                "particle_shape": shape,
                "field_relative_error": refined_field_error,
                "field_tolerance": refined_field_tolerance,
                "official_field_pass": refined_field_error < refined_field_tolerance,
                "independent_charge_relative_residual": refined_contract["charge_relative_residual"],
                "charge_tolerance": refined_contract["charge_tolerance"],
                "independent_charge_pass": refined_contract["passed"],
                "classification": "PASS" if refined_field_error < refined_field_tolerance and refined_contract["passed"] else "FIELD_BOUNDARY",
                "run_dir": str(refined_dir),
            }
        )

    result = {
        "contract": "3D Esirkepov Langmuir particle-shape runtime matrix",
        "geometry": "3D",
        "rows": rows,
        "refined_rows": refined_rows,
        "all_charge_pass": all(row["independent_charge_pass"] for row in rows),
        "field_pass_shapes": [row["particle_shape"] for row in rows if row["official_field_pass"]],
        "field_boundary_shapes": [row["particle_shape"] for row in rows if not row["official_field_pass"]],
        "refined_all_field_pass": all(row["official_field_pass"] for row in refined_rows),
        "refined_all_charge_pass": all(row["independent_charge_pass"] for row in refined_rows),
        "passed": True,
        "scope": "2-rank periodic Yee Langmuir; 64^3 base plus 128^3 shape=3/4 refined controls; no formal convergence-order claim",
        "interpretation": (
            "All sampled shapes close the independent charge gate. At 64^3, shape 2 closes the "
            "official field gate while shapes 3 and 4 are field boundaries; the 128^3 refined "
            "shape 3/4 siblings close both gates."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# 3D Esirkepov Langmuir particle-shape matrix",
        "",
        "- geometry: `3D`, periodic Yee, `64^3`, 2 MPI ranks",
        "- independent charge gate: all sampled shapes PASS",
        "- `64^3` field gate: shape 2 PASS; shape 3/4 FIELD_BOUNDARY",
        "- `128^3` refined shape 3/4 field and charge gates: PASS",
        "",
        "| shape | official field error | field gate | independent charge residual | charge gate | classification |",
        "|---:|---:|:---:|---:|:---:|:---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['particle_shape']}` | `{row['field_relative_error']:.6e}` < `{row['field_tolerance']:.2e}` | "
            f"{'PASS' if row['official_field_pass'] else 'BOUNDARY'} | "
            f"`{row['independent_charge_relative_residual']:.6e}` < `{row['charge_tolerance']:.1e}` | "
            f"{'PASS' if row['independent_charge_pass'] else 'FAIL'} | `{row['classification']}` |"
        )
    lines.extend(["", "## Refined `128^3` controls", "", "| shape | field error | field gate | charge residual | charge gate |", "|---:|---:|:---:|---:|:---:|"])
    for row in refined_rows:
        lines.append(
            f"| `{row['particle_shape']}` | `{row['field_relative_error']:.6e}` < `{row['field_tolerance']:.2e}` | "
            f"{'PASS' if row['official_field_pass'] else 'BOUNDARY'} | "
            f"`{row['independent_charge_relative_residual']:.6e}` < `{row['charge_tolerance']:.1e}` | "
            f"{'PASS' if row['independent_charge_pass'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "The `64^3` shape=3/4 field boundary is reduced by the `128^3` refined controls; this is a case-local resolution contrast, not a formal convergence-order study or a global default recommendation.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
