#!/usr/bin/env python
"""Apply the preregistered repeat-slope comparison gate to two families."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preregistration", type=Path, required=True)
    parser.add_argument("--slope-contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    prereg = load(args.preregistration)
    contract = load(args.slope_contract)
    repeat_spec = prereg["repeat_slope_comparison"]
    tolerance = repeat_spec["absolute_slope_delta_tolerance"]
    gated_corrections = tuple(repeat_spec["gated_corrections"])
    slope_table = contract["pairwise_slopes"]
    comparisons = []
    for geometry, geometry_data in slope_table.items():
        for family_control, control_data in geometry_data["first"].items():
            if family_control not in gated_corrections:
                continue
            first_metrics = control_data
            second_metrics = geometry_data["second"][family_control]
            for metric, first_values in first_metrics.items():
                second_values = second_metrics[metric]
                for interval, (first, second) in enumerate(zip(first_values, second_values), 1):
                    delta = abs(first - second)
                    comparisons.append({
                        "geometry": geometry,
                        "correction": family_control,
                        "metric": metric,
                        "interval": interval,
                        "first_slope": first,
                        "second_slope": second,
                        "absolute_delta": delta,
                        "passed": math.isfinite(delta) and delta <= tolerance,
                    })

    max_delta = max(item["absolute_delta"] for item in comparisons)
    negative_control_deltas = [
        abs(first - second)
        for geometry_data in slope_table.values()
        for metric, first_values in geometry_data["first"]["off"].items()
        for first, second in zip(first_values, geometry_data["second"]["off"][metric])
    ]
    passed = bool(comparisons) and all(item["passed"] for item in comparisons)
    result = {
        "contract": "formal convergence repeat-slope comparison gate",
        "classification": "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN" if passed else "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_FAIL",
        "scope": "RZ/RSPHERE independent families; correction-on gate and descriptive correction-off negative control",
        "passed": passed,
        "comparison_count": len(comparisons),
        "absolute_slope_delta_tolerance": tolerance,
        "gated_corrections": list(gated_corrections),
        "max_absolute_slope_delta": max_delta,
        "negative_control_max_absolute_slope_delta": max(negative_control_deltas),
        "comparisons": comparisons,
        "formal_order_closure": False,
        "charge_boundary_remains_open": contract.get("second_family_correction_on_charge_boundary", True),
        "interpretation": "The two materialized families pass the preregistered slope-repeat gate. This is an order-comparison gate only; it does not establish a formal numerical order and does not close the correction-on axis-charge boundary.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Formal convergence repeat-slope comparison gate",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if passed else 'FAIL'}`",
        f"- comparisons: `{result['comparison_count']}`",
        f"- gated corrections: `{', '.join(gated_corrections)}`",
        f"- absolute slope-delta tolerance: `{tolerance:.1e}`",
        f"- maximum absolute slope delta: `{max_delta:.3e}`",
        f"- correction-off negative-control maximum delta: `{result['negative_control_max_absolute_slope_delta']:.3e}`",
        "",
        "| geometry | correction | observable | interval | abs delta | status |",
        "|---|---|---|---:|---:|:---:|",
    ]
    lines.extend(
        f"| `{item['geometry']}` | `{item['correction']}` | `{item['metric']}` | `{item['interval']}` | `{item['absolute_delta']:.3e}` | `{'PASS' if item['passed'] else 'FAIL'}` |"
        for item in comparisons
    )
    lines.extend(["", result["interpretation"], ""])
    (args.output_dir / "contract.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
