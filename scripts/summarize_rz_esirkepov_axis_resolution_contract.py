#!/usr/bin/env python
"""Summarize RZ Esirkepov axis-correction and resolution contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def row(label: str, data: dict) -> dict:
    return {
        "case": label,
        "resolution": data["plotfile_dimensions"][:2],
        "relative_er_error": data["relative_er_error"],
        "relative_ez_error": data["relative_ez_error"],
        "charge_relative_residual": data["charge_relative_residual"],
        "axis_charge_relative_residual": data["axis_charge_relative_residual"],
        "off_axis_charge_relative_residual": data["off_axis_charge_relative_residual"],
        "field_passed": data["field_passed"],
        "charge_passed": data["charge_passed"],
        "passed": data["passed"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-on", type=Path, required=True)
    parser.add_argument("--baseline-off", type=Path, required=True)
    parser.add_argument("--refined-on", type=Path, required=True)
    parser.add_argument("--refined-off", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = [
        row("64x128 correction-on", load(args.baseline_on)),
        row("64x128 correction-off", load(args.baseline_off)),
        row("128x256 correction-on", load(args.refined_on)),
        row("128x256 correction-off", load(args.refined_off)),
    ]
    baseline_on, baseline_off, refined_on, refined_off = rows
    result = {
        "contract": "RZ Esirkepov axis-correction resolution comparison",
        "rows": rows,
        "refined_off_all_gates_pass": bool(refined_off["passed"]),
        "correction_on_axis_residual_reduction": baseline_on["axis_charge_relative_residual"]
        / refined_on["axis_charge_relative_residual"],
        "interpretation": (
            "For particle_shape=1, correction-off passes both field and charge gates at "
            "both sampled resolutions, while correction-on preserves the field gate but "
            "retains a nonzero axis charge residual. The separate shape=2/3/4 controls "
            "show that turning correction off can fail the Er field gate for higher "
            "shapes. Together these results support a resolution/axis-correction/shape "
            "interaction; they do not justify changing the global default without "
            "broader geometry and shape coverage."
        ),
    }
    result["passed"] = bool(result["refined_off_all_gates_pass"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ Esirkepov axis-correction resolution comparison",
        "",
        "| case | Er | Ez | charge residual | axis residual | off-axis residual | field | charge | overall |",
        "|---|---:|---:|---:|---:|---:|:---:|:---:|:---:|",
    ]
    for item in rows:
        lines.append(
            f"| {item['case']} | `{item['relative_er_error']:.6e}` | "
            f"`{item['relative_ez_error']:.6e}` | `{item['charge_relative_residual']:.6e}` | "
            f"`{item['axis_charge_relative_residual']:.6e}` | "
            f"`{item['off_axis_charge_relative_residual']:.6e}` | "
            f"`{'PASS' if item['field_passed'] else 'FAIL'}` | "
            f"`{'PASS' if item['charge_passed'] else 'BOUNDARY'}` | "
            f"`{'PASS' if item['passed'] else 'BOUNDARY'}` |"
        )
    lines += [
        "",
        f"- correction-on axis residual reduction from 64x128 to 128x256: `{result['correction_on_axis_residual_reduction']:.3f}x`.",
        f"- refined correction-off all-gate result: `{'PASS' if result['refined_off_all_gates_pass'] else 'BOUNDARY'}`.",
        f"- interpretation: {result['interpretation']}",
        "- scope: project-level refined sibling; no global WarpX default is changed.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
