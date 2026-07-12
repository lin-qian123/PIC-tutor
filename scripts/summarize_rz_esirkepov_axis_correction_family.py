#!/usr/bin/env python
"""Summarize full correction-on/off RZ Esirkepov shape evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def compact(data: dict) -> dict:
    return {
        "relative_er_error": data["relative_er_error"],
        "relative_ez_error": data["relative_ez_error"],
        "charge_relative_residual": data["charge_relative_residual"],
        "axis_charge_relative_residual": data["axis_charge_relative_residual"],
        "field_passed": data["field_passed"],
        "charge_passed": data["charge_passed"],
        "passed": data["passed"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case",
        action="append",
        required=True,
        metavar="SHAPE=COARSE_ON=COARSE_OFF=REFINED_ON=REFINED_OFF",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for spec in args.case:
        shape_text, coarse_on, coarse_off, refined_on, refined_off = spec.split("=", 4)
        rows.append(
            {
                "particle_shape": int(shape_text),
                "coarse_correction_on": compact(load(coarse_on)),
                "coarse_correction_off": compact(load(coarse_off)),
                "refined_correction_on": compact(load(refined_on)),
                "refined_correction_off": compact(load(refined_off)),
            }
        )
    rows.sort(key=lambda row: row["particle_shape"])
    result = {
        "contract": "RZ Esirkepov axis-correction shape family",
        "rows": rows,
        "refined_field_all_pass": all(
            row["refined_correction_on"]["field_passed"]
            and row["refined_correction_off"]["field_passed"]
            for row in rows
        ),
        "refined_off_all_pass": all(row["refined_correction_off"]["passed"] for row in rows),
        "refined_on_all_charge_boundary": all(
            not row["refined_correction_on"]["charge_passed"] for row in rows
        ),
        "interpretation": (
            "At 128x256, shapes 2/3/4 pass the field gate with correction on and off. "
            "The correction-off siblings also pass the charge gate, while correction-on "
            "retains an axis-dominated charge residual at O(1e-3). This separates the "
            "coarse field boundary from the unresolved correction-on charge diagnostic "
            "boundary; it does not justify changing the global default."
        ),
    }
    result["passed"] = bool(
        result["refined_field_all_pass"]
        and result["refined_off_all_pass"]
        and result["refined_on_all_charge_boundary"]
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ Esirkepov axis-correction shape family",
        "",
        "| shape | refined on Er | refined on charge | refined off Er | refined off charge |",
        "|---:|---:|:---:|---:|:---:|",
    ]
    for row in rows:
        on, off = row["refined_correction_on"], row["refined_correction_off"]
        lines.append(
            f"| `{row['particle_shape']}` | `{on['relative_er_error']:.6e}` | "
            f"`{on['charge_relative_residual']:.6e}` | `{off['relative_er_error']:.6e}` | "
            f"`{off['charge_relative_residual']:.6e}` |"
        )
    lines += [
        "",
        f"- refined field gates: `{'PASS' if result['refined_field_all_pass'] else 'BOUNDARY'}`.",
        f"- refined correction-off full gates: `{'PASS' if result['refined_off_all_pass'] else 'BOUNDARY'}`.",
        f"- refined correction-on charge remains boundary: `{'PASS' if result['refined_on_all_charge_boundary'] else 'NO'}`.",
        f"- interpretation: {result['interpretation']}",
        "- scope: RZ, single-level, shape=2/3/4, project-level refined siblings.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
