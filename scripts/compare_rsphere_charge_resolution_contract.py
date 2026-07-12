#!/usr/bin/env python
"""Summarize RSPHERE charge residual sensitivity to resolution and axis correction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    specs = [
        (64, "on", "esirkepov_langmuir_rsphere_charge_mpi2"),
        (64, "off", "esirkepov_langmuir_rsphere_charge_no_verboncoeur_mpi2"),
        (128, "on", "esirkepov_langmuir_rsphere_charge_n128_on_mpi2"),
        (128, "off", "esirkepov_langmuir_rsphere_charge_n128_off_mpi2"),
        (256, "on", "esirkepov_langmuir_rsphere_charge_n256_on_mpi2"),
        (256, "off", "esirkepov_langmuir_rsphere_charge_n256_off_mpi2"),
    ]
    rows = []
    for cells, correction, dirname in specs:
        data = read(args.root / dirname / "contract.json")
        rows.append({
            "cells": cells,
            "correction": correction,
            "relative_er_error": data["relative_er_error"],
            "charge_residual": data["charge_relative_residual"],
            "axis_residual": data["axis_charge_relative_residual"],
            "off_axis_residual": data["off_axis_charge_relative_residual"],
            "field_passed": data["field_passed"],
            "charge_passed": data["charge_passed"],
        })
    result = {
        "contract": "RSPHERE charge resolution/axis-correction comparison",
        "rows": rows,
        "classification": "RSPHERE_RESOLUTION_SENSITIVE_CHARGE_BOUNDARY",
        "scope": "paired 2-rank reader-side Er and charge comparison; not a convergence-order proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RSPHERE charge resolution/axis-correction comparison",
        "",
        "| cells | correction | Er error | charge residual | axis residual | off-axis residual | field | charge |",
        "|---:|---|---:|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['cells']} | `{row['correction']}` | `{row['relative_er_error']:.8e}` | `{row['charge_residual']:.8e}` | "
            f"`{row['axis_residual']:.8e}` | `{row['off_axis_residual']:.8e}` | "
            f"`{'PASS' if row['field_passed'] else 'BOUNDARY'}` | `{'PASS' if row['charge_passed'] else 'BOUNDARY'}` |"
        )
    lines.extend(["", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS: RSPHERE resolution/axis-correction comparison summarized")


if __name__ == "__main__":
    main()
