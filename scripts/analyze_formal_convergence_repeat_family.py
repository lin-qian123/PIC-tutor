#!/usr/bin/env python
"""Compare two preregistered RZ/RSPHERE resolution families."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


RZ_METRICS = ("er_error", "ez_error", "axis_residual", "off_axis_residual")
RSPHERE_METRICS = ("relative_er_error", "axis_residual", "off_axis_residual")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(geometry: str, correction: str, family: str, data: dict, resolution: int) -> dict:
    if geometry == "RZ":
        values = {
            "er_error": data["relative_er_error"],
            "ez_error": data["relative_ez_error"],
            "axis_residual": data["axis_charge_relative_residual"],
            "off_axis_residual": data["off_axis_charge_relative_residual"],
        }
    else:
        values = {
            "relative_er_error": data["relative_er_error"],
            "axis_residual": data["axis_charge_relative_residual"],
            "off_axis_residual": data["off_axis_charge_relative_residual"],
        }
    return {
        "geometry": geometry,
        "correction": correction,
        "family": family,
        "resolution": resolution,
        **values,
    }


def first_rows(path: Path, geometry: str) -> list[dict]:
    data = load(path)
    rows = []
    for row in data["rows"]:
        correction = row["correction"]
        resolution = row.get("cells", row.get("resolution", [None])[0])
        if geometry == "RZ":
            values = {
                "er_error": row["er_error"],
                "ez_error": row["ez_error"],
                "axis_residual": row["axis_residual"],
                "off_axis_residual": row["off_axis_residual"],
            }
        else:
            values = {
                "relative_er_error": row["relative_er_error"],
                "axis_residual": row["axis_residual"],
                "off_axis_residual": row["off_axis_residual"],
            }
        rows.append({"geometry": geometry, "correction": correction, "family": "first", "resolution": resolution, **values})
    return rows


def second_rows(root: Path, geometry: str) -> list[dict]:
    rows = []
    for correction in ("on", "off"):
        for resolution in (64, 128, 256):
            prefix = "rz" if geometry == "RZ" else "rsphere"
            data = load(root / f"{prefix}-{resolution}-{correction}.json")
            rows.append(normalize(geometry, correction, "second", data, resolution))
    return rows


def slopes(rows: list[dict], metrics: tuple[str, ...]) -> dict[str, list[float]]:
    result = {}
    for metric in metrics:
        values = [row[metric] for row in sorted(rows, key=lambda item: item["resolution"])]
        result[metric] = [math.log(left / right, 2) for left, right in zip(values, values[1:])]
    return result


def grouped(rows: list[dict], family: str, geometry: str, correction: str) -> list[dict]:
    return [
        row
        for row in rows
        if row["family"] == family and row["geometry"] == geometry and row["correction"] == correction
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-rz", type=Path, required=True)
    parser.add_argument("--first-rsphere", type=Path, required=True)
    parser.add_argument("--second-analysis-dir", type=Path, required=True)
    parser.add_argument("--runner-contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = first_rows(args.first_rz, "RZ") + first_rows(args.first_rsphere, "RSPHERE")
    rows += second_rows(args.second_analysis_dir, "RZ") + second_rows(args.second_analysis_dir, "RSPHERE")
    metrics = {"RZ": RZ_METRICS, "RSPHERE": RSPHERE_METRICS}
    slope_table = {}
    for geometry in ("RZ", "RSPHERE"):
        slope_table[geometry] = {}
        for family in ("first", "second"):
            slope_table[geometry][family] = {}
            for correction in ("on", "off"):
                slope_table[geometry][family][correction] = slopes(
                    grouped(rows, family, geometry, correction), metrics[geometry]
                )

    runner = load(args.runner_contract)
    finite = all(
        math.isfinite(value)
        for row in rows
        for metric in metrics[row["geometry"]]
        for value in (row[metric],)
    )
    level_contract = all(
        len(grouped(rows, family, geometry, correction)) == 3
        for family in ("first", "second")
        for geometry in ("RZ", "RSPHERE")
        for correction in ("on", "off")
    )
    second_charge_boundary = any(
        row["correction"] == "on" and row["axis_residual"] > 1.0e-11
        for row in rows
    )
    checks = {
        "two_independent_families_present": level_contract,
        "all_declared_levels_present": level_contract,
        "all_observables_finite": finite,
        "second_family_execution_pass": runner["classification"] == "REPEAT_FAMILY_RUNNER_EXECUTION_PASS",
        "all_pairwise_slopes_computed": True,
        "separate_geometry_reporting": True,
        "formal_order_closure": False,
    }
    result = {
        "contract": "formal convergence second-family slope comparison",
        "passed": all(checks.values()),
        "checks": checks,
        "classification": "FORMAL_CONVERGENCE_SECOND_FAMILY_MATERIALIZED_ORDER_COMPARISON_OPEN",
        "scope": "two independent 2-rank RZ/RSPHERE families; all declared 64/128/256 adjacent pairs; no pooled geometry fit",
        "runner_contract": str(args.runner_contract),
        "runtime_environment": runner.get("runtime_environment", {}),
        "rows": rows,
        "pairwise_slopes": slope_table,
        "second_family_correction_on_charge_boundary": second_charge_boundary,
        "interpretation": "The second independent family is materialized and its pairwise slopes are reported beside the first family. Formal closure remains open because the preregistration requires repeat-slope comparison under a declared tolerance and an independent charge interpretation; correction-on axis charge remains a boundary.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Formal convergence second-family slope comparison",
        "",
        f"- classification: `{result['classification']}`",
        f"- runtime environment: `{json.dumps(result['runtime_environment'], ensure_ascii=False, sort_keys=True)}`",
        "",
        "| geometry | correction | observable | first family slopes | second family slopes |",
        "|---|---|---|---:|---:|",
    ]
    for geometry in ("RZ", "RSPHERE"):
        for correction in ("on", "off"):
            for metric in metrics[geometry]:
                first = slope_table[geometry]["first"][correction][metric]
                second = slope_table[geometry]["second"][correction][metric]
                lines.append(
                    f"| `{geometry}` | `{correction}` | `{metric}` | "
                    f"`{first[0]:.6f}, {first[1]:.6f}` | `{second[0]:.6f}, {second[1]:.6f}` |"
                )
    lines.extend(["", result["interpretation"], ""])
    lines.extend(f"- `{name}`: `{'PASS' if value else 'BOUNDARY'}`" for name, value in checks.items())
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
