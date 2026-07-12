#!/usr/bin/env python
"""Analyze the 1D theta-implicit Picard total-energy contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    reduced = args.run_dir / "diags" / "reducedfiles"
    field = np.loadtxt(reduced / "field_energy.txt", skiprows=1)
    particle = np.loadtxt(reduced / "particle_energy.txt", skiprows=1)
    total = field[:, 2] + particle[:, 2]
    delta = (total - total[0]) / total[0]
    max_abs_delta = float(np.abs(delta).max())
    result = {
        "run_dir": str(args.run_dir),
        "samples": int(total.size),
        "initial_total_energy": float(total[0]),
        "final_total_energy": float(total[-1]),
        "max_abs_relative_energy_change": max_abs_delta,
        "tolerance": 1.0e-14,
        "passed": max_abs_delta < 1.0e-14,
        "contract": "theta-implicit Picard total particle-plus-field energy conservation",
        "official_analysis_note": "official analysis_1d.py selects tolerance from the CMake test directory name",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# Theta-implicit Picard energy contract\n\n"
        f"- status: `{status}`\n"
        f"- samples: `{result['samples']}`\n"
        f"- initial/final total energy: `{total[0]:.16g}` / `{total[-1]:.16g}`\n"
        f"- max absolute relative change: `{max_abs_delta:.8e}`\n"
        f"- tolerance: `{result['tolerance']:.8e}`\n"
        f"- contract: {result['contract']}\n"
        f"- note: {result['official_analysis_note']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("implicit theta Picard energy contract failed")


if __name__ == "__main__":
    main()
