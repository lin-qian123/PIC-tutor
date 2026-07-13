#!/usr/bin/env python
"""Audit whether existing deposition data is ready for a formal convergence study."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def pairwise_order(rows: list[dict], key: str) -> list[float]:
    rows = sorted(rows, key=lambda row: row["resolution"][0])
    return [math.log(left[key] / right[key], 2) for left, right in zip(rows, rows[1:])]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    chapter = (root / "manuscript/chapters/05-deposition-shapes.md").read_text(encoding="utf-8")
    rows = data["rows"]
    by_correction = {name: sorted((row for row in rows if row["correction"] == name), key=lambda row: row["resolution"][0]) for name in ("on", "off")}
    checks = {
        "chapter_heading": "### 5.14.5 v0.79 收敛研究就绪合同" in chapter,
        "chapter_boundary": all(marker in chapter for marker in (
            "不能只凭单调下降", "CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN",
            "不能把经验 order 当作论文或 WarpX 的正式收敛阶",
        )),
        "three_resolution_families": all(len(by_correction[name]) == 3 for name in by_correction),
        "refinement_ratios": all(
            rows_[1]["resolution"][0] == 2 * rows_[0]["resolution"][0]
            and rows_[2]["resolution"][0] == 2 * rows_[1]["resolution"][0]
            and rows_[1]["resolution"][1] == 2 * rows_[0]["resolution"][1]
            and rows_[2]["resolution"][1] == 2 * rows_[1]["resolution"][1]
            for rows_ in by_correction.values()
        ),
        "field_charge_split": all(marker in chapter for marker in ("field observable", "charge observable", "axis charge")),
        "formal_order_unproven": "正式收敛阶" in data["scope"] or "formal convergence order" in data["scope"].lower(),
        "axis_charge_boundary": any(row["axis_residual"] > 1e-4 for row in by_correction["on"]),
        "nonmonotone_control_preserved": by_correction["off"][-1]["charge_passed"] is False,
    }
    orders = {
        correction: {
            key: pairwise_order(family, key)
            for key in ("er_error", "ez_error", "charge_residual", "axis_residual", "off_axis_residual")
        }
        for correction, family in by_correction.items()
    }
    result = {
        "contract": "deposition convergence readiness",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "CONVERGENCE_READINESS_WITH_FORMAL_ORDER_UNPROVEN",
        "scope": "existing RZ Esirkepov shape=1 three-resolution controls; descriptive pairwise order only",
        "pairwise_orders": orders,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Deposition convergence readiness contract", "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}", "", "| correction | observable | pairwise orders (64->128, 128->256) |", "|---|---|---:|",
    ]
    for correction, values in orders.items():
        for key, pairwise in values.items():
            lines.append(f"| `{correction}` | `{key}` | `{pairwise[0]:.3f}, {pairwise[1]:.3f}` |")
    lines.extend(["", "The pairwise orders are descriptive. The contract does not establish a formal convergence order or close the axis-charge boundary."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
