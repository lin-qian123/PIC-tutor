#!/usr/bin/env python
"""Summarize coarse-to-refined RZ Esirkepov correction-off shape evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case",
        action="append",
        required=True,
        metavar="SHAPE=COARSE_JSON=REFINED_JSON",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for spec in args.case:
        shape_text, coarse_path, refined_path = spec.split("=", 2)
        coarse = load(coarse_path)
        refined = load(refined_path)
        rows.append(
            {
                "particle_shape": int(shape_text),
                "coarse": {
                    "resolution": coarse["plotfile_dimensions"][:2],
                    "relative_er_error": coarse["relative_er_error"],
                    "relative_ez_error": coarse["relative_ez_error"],
                    "charge_relative_residual": coarse["charge_relative_residual"],
                    "field_passed": coarse["field_passed"],
                    "charge_passed": coarse["charge_passed"],
                    "passed": coarse["passed"],
                },
                "refined": {
                    "resolution": refined["plotfile_dimensions"][:2],
                    "relative_er_error": refined["relative_er_error"],
                    "relative_ez_error": refined["relative_ez_error"],
                    "charge_relative_residual": refined["charge_relative_residual"],
                    "field_passed": refined["field_passed"],
                    "charge_passed": refined["charge_passed"],
                    "passed": refined["passed"],
                },
            }
        )
    rows.sort(key=lambda row: row["particle_shape"])
    result = {
        "contract": "RZ Esirkepov correction-off shape-resolution family",
        "rows": rows,
        "all_refined_pass": all(row["refined"]["passed"] for row in rows),
        "all_coarse_field_fail": all(not row["coarse"]["field_passed"] for row in rows),
        "interpretation": (
            "For shapes 2/3/4, the correction-off coarse siblings fail the Er field gate "
            "while the refined siblings pass both field and charge gates. This supports a "
            "coarse-resolution field boundary across the higher-shape family. It does not "
            "close correction-on charge residuals or justify changing the global axis "
            "correction default."
        ),
    }
    result["passed"] = bool(result["all_refined_pass"] and result["all_coarse_field_fail"])

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ Esirkepov correction-off shape-resolution family",
        "",
        "| shape | coarse Er | refined Er | coarse charge | refined charge | coarse | refined |",
        "|---:|---:|---:|---:|---:|:---:|:---:|",
    ]
    for row in rows:
        coarse, refined = row["coarse"], row["refined"]
        lines.append(
            f"| `{row['particle_shape']}` | `{coarse['relative_er_error']:.6e}` | "
            f"`{refined['relative_er_error']:.6e}` | `{coarse['charge_relative_residual']:.6e}` | "
            f"`{refined['charge_relative_residual']:.6e}` | "
            f"`{'PASS' if coarse['passed'] else 'BOUNDARY'}` | "
            f"`{'PASS' if refined['passed'] else 'BOUNDARY'}` |"
        )
    lines += [
        "",
        f"- all refined gates: `{'PASS' if result['all_refined_pass'] else 'BOUNDARY'}`.",
        f"- all coarse field gates fail: `{'PASS' if result['all_coarse_field_fail'] else 'BOUNDARY'}`.",
        f"- interpretation: {result['interpretation']}",
        "- scope: correction-off, RZ, single-level, project-level refined siblings only.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
