#!/usr/bin/env python
"""Summarize RZ Esirkepov 256x512 correction-on/off shape controls."""

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
    for correction in ("on", "off"):
        for shape in (1, 2, 3, 4):
            if shape == 1:
                dirname = f"esirkepov_langmuir_rz_resolution256_{correction}_mpi2"
            elif correction == "on":
                dirname = f"esirkepov_langmuir_rz_shape{shape}_resolution256_mpi2"
            else:
                dirname = f"esirkepov_langmuir_rz_shape{shape}_resolution256_off_mpi2"
            case_dir = args.root / dirname
            data = json.loads((case_dir / "contract.json").read_text(encoding="utf-8"))
            rows.append(
                {
                    "correction": correction,
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
        "contract": "RZ Esirkepov 256x512 correction-on/off shape family",
        "rows": rows,
        "all_field_pass": all(row["field_passed"] for row in rows),
        "on_all_charge_pass": all(row["charge_passed"] for row in rows if row["correction"] == "on"),
        "off_charge_pass_shapes": [
            row["shape"] for row in rows if row["correction"] == "off" and row["charge_passed"]
        ],
        "classification": "RZ_HIGHRES_CORRECTION_SHAPE_TRADEOFF",
        "scope": "2-rank RZ 256x512 shape=1/2/3/4 correction-on/off controls; not a global-default or formal convergence claim",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RZ Esirkepov 256x512 correction-on/off shape family",
        "",
        "| correction | shape | Er | Ez | charge residual | axis residual | off-axis residual | field | charge |",
        "|---|---:|---:|---:|---:|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['correction']}` | `{row['shape']}` | `{row['er_error']:.6e}` | "
            f"`{row['ez_error']:.6e}` | `{row['charge_residual']:.6e}` | "
            f"`{row['axis_residual']:.6e}` | `{row['off_axis_residual']:.6e}` | "
            f"`{'PASS' if row['field_passed'] else 'BOUNDARY'}` | "
            f"`{'PASS' if row['charge_passed'] else 'BOUNDARY'}` |"
        )
    lines.extend(
        [
            "",
            f"- classification: `{result['classification']}`",
            f"- correction-on all charge gates: `{result['on_all_charge_pass']}`",
            f"- correction-off charge-pass shapes: `{result['off_charge_pass_shapes']}`",
            f"- scope: {result['scope']}",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS: 8 RZ high-resolution correction contracts summarized")


if __name__ == "__main__":
    raise SystemExit(main())
