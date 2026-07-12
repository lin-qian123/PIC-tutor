#!/usr/bin/env python
"""Compare RZ Esirkepov shape=1..4 with Verboncoeur correction on/off."""

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

    rows = []
    for shape in range(1, 5):
        on_name = "esirkepov_langmuir_rz_mpi2" if shape == 1 else f"esirkepov_langmuir_rz_shape{shape}_mpi2"
        off_name = "esirkepov_langmuir_rz_no_verboncoeur_mpi2" if shape == 1 else f"esirkepov_langmuir_rz_shape{shape}_no_verboncoeur_mpi2"
        on = read(args.root / on_name / "contract.json")
        off = read(args.root / off_name / "contract.json")
        rows.append({
            "shape": shape,
            "correction_on": {
                "er": on["relative_er_error"],
                "ez": on["relative_ez_error"],
                "charge": on["charge_relative_residual"],
                "field_passed": on["field_passed"],
                "charge_passed": on["charge_passed"],
            },
            "correction_off": {
                "er": off["relative_er_error"],
                "ez": off["relative_ez_error"],
                "charge": off["charge_relative_residual"],
                "field_passed": off["field_passed"],
                "charge_passed": off["charge_passed"],
            },
        })
    result = {
        "contract": "RZ Esirkepov shape and axis-correction matrix",
        "rows": rows,
        "classification": "AXIS_CORRECTION_CHARGE_FIELD_TRADEOFF_BY_SHAPE",
        "scope": "paired 2-rank reader-side comparison; does not justify changing the global default",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RZ Esirkepov shape/axis-correction matrix",
        "",
        "| shape | correction | Er error | Ez error | charge residual | field | charge |",
        "|---:|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        for label, values in (("on", row["correction_on"]), ("off", row["correction_off"])):
            lines.append(
                f"| {row['shape']} | `{label}` | `{values['er']:.8e}` | `{values['ez']:.8e}` | "
                f"`{values['charge']:.8e}` | `{'PASS' if values['field_passed'] else 'BOUNDARY'}` | "
                f"`{'PASS' if values['charge_passed'] else 'BOUNDARY'}` |"
            )
    lines.extend(["", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS: shape/axis-correction matrix summarized")


if __name__ == "__main__":
    main()
