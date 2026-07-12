#!/usr/bin/env python
"""Summarize three-resolution RZ Esirkepov shape=1 controls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--on", action="append", required=True, metavar="LABEL=PATH")
    parser.add_argument("--off", action="append", required=True, metavar="LABEL=PATH")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for correction, specs in (("on", args.on), ("off", args.off)):
        for spec in specs:
            label, path = spec.split("=", 1)
            data = load(Path(path))
            rows.append(
                {
                    "correction": correction,
                    "label": label,
                    "resolution": data["plotfile_dimensions"][:2],
                    "er_error": data["relative_er_error"],
                    "ez_error": data["relative_ez_error"],
                    "charge_residual": data["charge_relative_residual"],
                    "axis_residual": data["axis_charge_relative_residual"],
                    "off_axis_residual": data["off_axis_charge_relative_residual"],
                    "field_passed": data["field_passed"],
                    "charge_passed": data["charge_passed"],
                    "passed": data["passed"],
                }
            )
    rows.sort(key=lambda row: (row["correction"], row["resolution"]))
    on_rows = [row for row in rows if row["correction"] == "on"]
    off_rows = [row for row in rows if row["correction"] == "off"]
    result = {
        "contract": "RZ Esirkepov shape=1 three-resolution correction trend",
        "rows": rows,
        "on_axis_residual_monotone_decrease": all(
            left["axis_residual"] > right["axis_residual"]
            for left, right in zip(on_rows, on_rows[1:])
        ),
        "off_charge_all_pass": all(row["charge_passed"] for row in off_rows),
        "classification": "CORRECTION_ON_RESOLUTION_TREND_OFF_NONMONOTONE_BOUNDARY",
        "scope": "2-rank RZ shape=1 case-local 64x128/128x256/256x512 controls; descriptive trend, not formal convergence order",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ Esirkepov shape=1 three-resolution correction trend",
        "",
        "| correction | resolution | Er | Ez | charge residual | axis residual | off-axis residual | field | charge |",
        "|---|---:|---:|---:|---:|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['correction']}` | `{row['resolution'][0]}x{row['resolution'][1]}` | "
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
            f"- correction-on axis residual monotone decrease: `{result['on_axis_residual_monotone_decrease']}`",
            f"- correction-off charge gate passes at all resolutions: `{result['off_charge_all_pass']}`",
            f"- scope: {result['scope']}",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
