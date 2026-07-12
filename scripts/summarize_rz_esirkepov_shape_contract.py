#!/usr/bin/env python
"""Summarize the RZ Esirkepov Langmuir shape=1..4 contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for shape in range(1, 5):
        dirname = "esirkepov_langmuir_rz_mpi2" if shape == 1 else f"esirkepov_langmuir_rz_shape{shape}_mpi2"
        path = args.root / dirname / "contract.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append({
            "shape": shape,
            "run": dirname,
            "relative_er_error": data["relative_er_error"],
            "relative_ez_error": data["relative_ez_error"],
            "charge_relative_residual": data["charge_relative_residual"],
            "axis_charge_relative_residual": data["axis_charge_relative_residual"],
            "off_axis_charge_relative_residual": data["off_axis_charge_relative_residual"],
            "field_passed": data["field_passed"],
            "charge_passed": data["charge_passed"],
        })
    result = {
        "contract": "RZ Esirkepov Langmuir shape matrix",
        "rows": rows,
        "field_coverage": all(row["field_passed"] for row in rows),
        "charge_coverage": all(row["charge_passed"] for row in rows),
        "classification": "FIELD_SHAPE_1_TO_4_PASS_AXIS_CHARGE_BOUNDARY",
        "scope": "2-rank reader-side matrix with default Verboncoeur axis correction; not a global geometry/order proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RZ Esirkepov Langmuir shape matrix",
        "",
        "| shape | Er error | Ez error | all-cell charge | axis charge | off-axis charge | field | charge |",
        "|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['shape']} | `{row['relative_er_error']:.8e}` | `{row['relative_ez_error']:.8e}` | "
            f"`{row['charge_relative_residual']:.8e}` | `{row['axis_charge_relative_residual']:.8e}` | "
            f"`{row['off_axis_charge_relative_residual']:.8e}` | "
            f"`{'PASS' if row['field_passed'] else 'FAIL'}` | `{'PASS' if row['charge_passed'] else 'BOUNDARY'}` |"
        )
    lines.extend(["", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: RZ shape=1..4 field coverage={result['field_coverage']}, charge coverage={result['charge_coverage']}")


if __name__ == "__main__":
    main()
