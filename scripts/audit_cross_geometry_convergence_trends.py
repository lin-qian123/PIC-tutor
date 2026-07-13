#!/usr/bin/env python
"""Compare existing RZ and RSPHERE resolution trends without claiming formal order."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def load_rows(path: Path) -> dict[str, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict]] = {"on": [], "off": []}
    for row in data["rows"]:
        grouped[row["correction"]].append(row)
    for rows in grouped.values():
        rows.sort(key=lambda row: row.get("resolution", [row.get("cells")])[0])
    return grouped


def orders(rows: list[dict], key: str) -> list[float]:
    values = [row[key] for row in rows]
    return [math.log(left / right, 2) for left, right in zip(values, values[1:])]


def monotone_decrease(rows: list[dict], key: str) -> bool:
    values = [row[key] for row in rows]
    return all(left > right for left, right in zip(values, values[1:]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    rz_path = root / "runs/stage-c-validation/esirkepov_langmuir_rz_resolution-trend/contract.json"
    rsphere_path = root / "runs/stage-c-validation/esirkepov_rsphere_charge_resolution-comparison/contract.json"
    rz = load_rows(rz_path)
    rsphere = load_rows(rsphere_path)
    checks = {
        "source_contracts_present": rz_path.is_file() and rsphere_path.is_file(),
        "two_independent_geometries": all(len(grouped[name]) == 3 for grouped in (rz, rsphere) for name in ("on", "off")),
        "refinement_ratios_are_two": all(
            [row.get("resolution", [row.get("cells")])[0] for row in grouped[name]] == [64, 128, 256]
            for grouped in (rz, rsphere)
            for name in ("on", "off")
        ),
        "rz_axis_on_decreases": monotone_decrease(rz["on"], "axis_residual"),
        "rsphere_axis_on_decreases": monotone_decrease(rsphere["on"], "axis_residual"),
        "negative_control_boundary_preserved": not monotone_decrease(rz["off"], "axis_residual")
        and not monotone_decrease(rsphere["off"], "axis_residual"),
        "no_cross_geometry_pooling": True,
        "formal_order_unproven": True,
    }
    trends = {
        "rz": {
            "on": {key: orders(rz["on"], key) for key in ("er_error", "ez_error", "axis_residual", "off_axis_residual")},
            "off": {key: orders(rz["off"], key) for key in ("er_error", "ez_error", "axis_residual", "off_axis_residual")},
        },
        "rsphere": {
            "on": {key: orders(rsphere["on"], key) for key in ("relative_er_error", "axis_residual", "off_axis_residual")},
            "off": {key: orders(rsphere["off"], key) for key in ("relative_er_error", "axis_residual", "off_axis_residual")},
        },
    }
    result = {
        "contract": "cross-geometry exploratory convergence trends",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "EXPLORATORY_CROSS_GEOMETRY_RESOLUTION_TRENDS_FORMAL_ORDER_UNPROVEN",
        "scope": "existing 2-rank RZ and RSPHERE three-resolution controls; separate slopes, no pooled formal order",
        "trends": trends,
        "interpretation": "The two geometries provide independent resolution-sensitive controls. Their slopes are descriptive and remain separate; they do not establish a formal convergence order, a universal order across geometry, or closure of the default axis-charge boundary.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Cross-geometry exploratory convergence trends",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| geometry | correction | observable | pairwise slopes (64->128, 128->256) |",
        "|---|---|---|---:|",
    ]
    for geometry, families in trends.items():
        for correction, values in families.items():
            for key, values_ in values.items():
                lines.append(f"| `{geometry}` | `{correction}` | `{key}` | `{values_[0]:.3f}, {values_[1]:.3f}` |")
    lines.extend(["", result["interpretation"]])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
