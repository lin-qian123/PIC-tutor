#!/usr/bin/env python
"""Measure deterministic reader-side RZ/RSPHERE axis-charge repeat stability."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rows_from_contract(path: Path, family: str) -> list[dict]:
    data = load(path)
    return [
        {
            "geometry": row["geometry"],
            "correction": row["correction"],
            "resolution": row["resolution"],
            "family": family,
            "axis_residual": row["axis_residual"],
            "off_axis_residual": row["off_axis_residual"],
        }
        for row in data["rows"]
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slope-contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repeat-tolerance", type=float, default=1.0e-10)
    args = parser.parse_args()

    data = load(args.slope_contract)
    rows = data["rows"]
    comparisons = []
    for geometry in ("RZ", "RSPHERE"):
        for correction in ("on", "off"):
            for resolution in (64, 128, 256):
                pair = [
                    row
                    for row in rows
                    if row["geometry"] == geometry
                    and row["correction"] == correction
                    and row["resolution"] == resolution
                ]
                first = next(row for row in pair if row["family"] == "first")
                second = next(row for row in pair if row["family"] == "second")
                axis = max(abs(first["axis_residual"]), abs(second["axis_residual"]))
                absolute_difference = abs(first["axis_residual"] - second["axis_residual"])
                relative_difference = absolute_difference / axis if axis else 0.0
                comparisons.append(
                    {
                        "geometry": geometry,
                        "correction": correction,
                        "resolution": resolution,
                        "first_axis_residual": first["axis_residual"],
                        "second_axis_residual": second["axis_residual"],
                        "first_off_axis_residual": first["off_axis_residual"],
                        "second_off_axis_residual": second["off_axis_residual"],
                        "axis_repeat_relative_difference": relative_difference,
                        "axis_dominates_first": first["axis_residual"] > first["off_axis_residual"],
                        "axis_dominates_second": second["axis_residual"] > second["off_axis_residual"],
                        "repeat_stability_passed": relative_difference <= args.repeat_tolerance,
                    }
                )

    checks = {
        "all_twelve_axis_pairs_present": len(comparisons) == 12,
        "all_repeat_values_finite": all(
            math.isfinite(row[key])
            for row in comparisons
            for key in ("first_axis_residual", "second_axis_residual", "axis_repeat_relative_difference")
        ),
        "all_correction_on_axis_repeats_within_tolerance": all(
            row["repeat_stability_passed"] for row in comparisons if row["correction"] == "on"
        ),
        "correction_on_axis_dominates_both_families": all(
            row["axis_dominates_first"] and row["axis_dominates_second"]
            for row in comparisons
            if row["correction"] == "on"
        ),
    }
    result = {
        "contract": "reader-side axis-charge repeat stability",
        "passed": all(checks.values()),
        "classification": "REPEAT_STABLE_AXIS_CHARGE_BOUNDARY_NOT_KERNEL_ROOT_CAUSE",
        "scope": "two deterministic 2-rank RZ/RSPHERE families; axis/off-axis divE-rho reader-side residual only",
        "repeat_tolerance": args.repeat_tolerance,
        "checks": checks,
        "comparisons": comparisons,
        "interpretation": "The correction-on axis residual is reproducible across both materialized families and remains larger than the off-axis residual at every declared level. Correction-off values are reported as a negative control; their relative differences are not gated because the absolute residual is near the reader/numerical floor. This strengthens the correction-on boundary as a stable reader-side observation; it does not identify the kernel root cause, prove current closure, or close formal order.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Reader-side axis-charge repeat stability",
        "",
        f"- classification: `{result['classification']}`",
        f"- repeat tolerance: `{args.repeat_tolerance:.1e}`",
        "",
        "| geometry | correction | level | first axis | second axis | first off-axis | second off-axis | relative repeat diff | axis dominates |",
        "|---|---|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for row in comparisons:
        dominates = row["axis_dominates_first"] and row["axis_dominates_second"]
        lines.append(
            f"| `{row['geometry']}` | `{row['correction']}` | `{row['resolution']}` | "
            f"`{row['first_axis_residual']:.6e}` | `{row['second_axis_residual']:.6e}` | "
            f"`{row['first_off_axis_residual']:.6e}` | `{row['second_off_axis_residual']:.6e}` | "
            f"`{row['axis_repeat_relative_difference']:.6e}` | `{'PASS' if dominates else 'BOUNDARY'}` |"
        )
    lines.extend(["", result["interpretation"], ""])
    lines.extend(f"- `{name}`: `{'PASS' if value else 'BOUNDARY'}`" for name, value in checks.items())
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
