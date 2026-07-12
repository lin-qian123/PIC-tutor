#!/usr/bin/env python
"""Summarize highest-resolution RZ Esirkepov correction-on shape family."""

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
    for shape in (1, 2, 3, 4):
        suffix = "resolution256_on_mpi2" if shape == 1 else f"shape{shape}_resolution256_mpi2"
        case_dir = args.root / f"esirkepov_langmuir_rz_{suffix}"
        data = json.loads((case_dir / "contract.json").read_text(encoding="utf-8"))
        rows.append(
            {
                "shape": shape,
                "resolution": data["plotfile_dimensions"][:2],
                "er_error": data["relative_er_error"],
                "ez_error": data["relative_ez_error"],
                "charge_residual": data["charge_relative_residual"],
                "axis_residual": data["axis_charge_relative_residual"],
                "off_axis_residual": data["off_axis_charge_relative_residual"],
                "field_passed": data["field_passed"],
                "charge_passed": data["charge_passed"],
                "run_dir": str(case_dir),
            }
        )
    result = {
        "contract": "RZ Esirkepov correction-on highest-resolution shape family",
        "rows": rows,
        "all_field_pass": all(row["field_passed"] for row in rows),
        "all_charge_pass": all(row["charge_passed"] for row in rows),
        "classification": "RZ_HIGHRES_FIELD_PASS_AXIS_CHARGE_BOUNDARY",
        "scope": "2-rank RZ correction-on 256x512 shape=1/2/3/4 controls; no global-default or formal convergence claim",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RZ Esirkepov correction-on highest-resolution shape family",
        "",
        "| shape | resolution | Er | Ez | charge residual | axis residual | off-axis residual | field | charge |",
        "|---:|---:|---:|---:|---:|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['shape']}` | `{row['resolution'][0]}x{row['resolution'][1]}` | "
            f"`{row['er_error']:.6e}` | `{row['ez_error']:.6e}` | "
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
    print("PASS: 4 RZ high-resolution correction-on shape contracts summarized")


if __name__ == "__main__":
    raise SystemExit(main())
