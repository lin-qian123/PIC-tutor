#!/usr/bin/env python
"""Summarize RCYLINDER/RSPHERE Esirkepov radial charge contracts."""

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
    for geometry in ("rcylinder", "rsphere"):
        for shape in (2, 3, 4):
            case_dir = args.root / f"esirkepov_langmuir_{geometry}_shape{shape}_mpi2"
            data = json.loads((case_dir / "charge-contract.json").read_text(encoding="utf-8"))
            rows.append(
                {
                    "geometry": geometry.upper(),
                    "shape": shape,
                    "field_error": data["relative_er_error"],
                    "charge_residual": data["charge_relative_residual"],
                    "axis_residual": data["axis_charge_relative_residual"],
                    "off_axis_residual": data["off_axis_charge_relative_residual"],
                    "field_passed": data["field_passed"],
                    "charge_passed": data["charge_passed"],
                    "run_dir": str(case_dir),
                }
            )

    result = {
        "contract": "RCYLINDER/RSPHERE Esirkepov radial charge shape matrix",
        "rows": rows,
        "all_field_pass": all(row["field_passed"] for row in rows),
        "all_charge_pass": all(row["charge_passed"] for row in rows),
        "classification": "RADIAL_SHAPE_CHARGE_BOUNDARY",
        "scope": "2-rank reader-side radial Er and same-surface divE-rho/epsilon0; shape=2/3/4 only; not a full Gauss-law proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RCYLINDER/RSPHERE Esirkepov radial charge shape matrix",
        "",
        "| geometry | shape | Er error | charge residual | axis residual | off-axis residual | field | charge |",
        "|---|---:|---:|---:|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['geometry']}` | `{row['shape']}` | `{row['field_error']:.6e}` | "
            f"`{row['charge_residual']:.6e}` | `{row['axis_residual']:.6e}` | "
            f"`{row['off_axis_residual']:.6e}` | "
            f"`{'PASS' if row['field_passed'] else 'BOUNDARY'}` | "
            f"`{'PASS' if row['charge_passed'] else 'BOUNDARY'}` |"
        )
    lines.extend(
        [
            "",
            f"- classification: `{result['classification']}`",
            f"- scope: {result['scope']}",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {len(rows)} radial shape charge contracts summarized")


if __name__ == "__main__":
    main()
