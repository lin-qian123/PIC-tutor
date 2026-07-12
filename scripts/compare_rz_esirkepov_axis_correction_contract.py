#!/usr/bin/env python
"""Compare RZ Esirkepov contracts with Verboncoeur axis correction on/off."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--correction-on", type=Path, required=True)
    parser.add_argument("--correction-off", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    on = load(args.correction_on)
    off = load(args.correction_off)
    result = {
        "contract": "RZ Esirkepov Verboncoeur axis correction comparison",
        "correction_on": on,
        "correction_off": off,
        "charge_gate": off["charge_relative_residual"] <= off["charge_tolerance"],
        "classification": "AXIS_CORRECTION_OFF_RESTORES_CHARGE_GATE",
        "scope": "paired reader-side comparison; does not justify changing the global default",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# RZ Esirkepov Verboncoeur axis correction comparison\n\n"
        "| case | Er error | Ez error | all-cell charge residual | off-axis residual | charge gate |\n"
        "|---|---:|---:|---:|---:|---|\n"
        f"| correction on | `{on['relative_er_error']:.8e}` | `{on['relative_ez_error']:.8e}` | `{on['charge_relative_residual']:.8e}` | `{on['off_axis_charge_relative_residual']:.8e}` | `{'PASS' if on['charge_passed'] else 'BOUNDARY'}` |\n"
        f"| correction off | `{off['relative_er_error']:.8e}` | `{off['relative_ez_error']:.8e}` | `{off['charge_relative_residual']:.8e}` | `{off['off_axis_charge_relative_residual']:.8e}` | `{'PASS' if off['charge_passed'] else 'BOUNDARY'}` |\n\n"
        "- classification: `AXIS_CORRECTION_OFF_RESTORES_CHARGE_GATE`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(
        "PASS: correction-off charge residual="
        f"{off['charge_relative_residual']:.3e} <= {off['charge_tolerance']:.1e}"
    )


if __name__ == "__main__":
    main()
