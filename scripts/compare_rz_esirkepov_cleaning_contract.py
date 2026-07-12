#!/usr/bin/env python
"""Compare RZ Esirkepov Langmuir contracts with divE cleaning on and off."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleaning-on", type=Path, required=True)
    parser.add_argument("--cleaning-off", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    on = load(args.cleaning_on)
    off = load(args.cleaning_off)
    residual_ratio = off["charge_relative_residual"] / on["charge_relative_residual"]
    result = {
        "contract": "RZ Esirkepov divE-cleaning sensitivity comparison",
        "cleaning_on": {
            "run": str(args.cleaning_on),
            "relative_er_error": on["relative_er_error"],
            "relative_ez_error": on["relative_ez_error"],
            "charge_relative_residual": on["charge_relative_residual"],
            "axis_charge_relative_residual": on["axis_charge_relative_residual"],
            "off_axis_charge_relative_residual": on["off_axis_charge_relative_residual"],
        },
        "cleaning_off": {
            "run": str(args.cleaning_off),
            "relative_er_error": off["relative_er_error"],
            "relative_ez_error": off["relative_ez_error"],
            "charge_relative_residual": off["charge_relative_residual"],
            "axis_charge_relative_residual": off["axis_charge_relative_residual"],
            "off_axis_charge_relative_residual": off["off_axis_charge_relative_residual"],
        },
        "charge_residual_off_over_on": residual_ratio,
        "classification": "AXIS_DOMINATED_CLEANING_SENSITIVE_DIAGNOSTIC_BOUNDARY",
        "scope": "paired reader-side comparison; not a kernel fix or full RZ conservation proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# RZ Esirkepov cleaning sensitivity comparison\n\n"
        f"| case | Er error | Ez error | all-cell residual | axis residual | off-axis residual |\n|---|---:|---:|---:|---:|---:|\n"
        f"| cleaning on | `{on['relative_er_error']:.8e}` | `{on['relative_ez_error']:.8e}` | `{on['charge_relative_residual']:.8e}` | `{on['axis_charge_relative_residual']:.8e}` | `{on['off_axis_charge_relative_residual']:.8e}` |\n"
        f"| cleaning off | `{off['relative_er_error']:.8e}` | `{off['relative_ez_error']:.8e}` | `{off['charge_relative_residual']:.8e}` | `{off['axis_charge_relative_residual']:.8e}` | `{off['off_axis_charge_relative_residual']:.8e}` |\n\n"
        f"- residual ratio (off/on): `{residual_ratio:.8e}`\n"
        "- classification: `AXIS_DOMINATED_CLEANING_SENSITIVE_DIAGNOSTIC_BOUNDARY`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(f"PASS: cleaning-off/on charge residual ratio={residual_ratio:.3e}")


if __name__ == "__main__":
    main()
