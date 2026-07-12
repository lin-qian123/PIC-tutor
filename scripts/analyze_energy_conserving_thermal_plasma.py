#!/usr/bin/env python
"""Summarize WarpX's reduced-energy thermal-plasma analysis contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--tolerance", type=float, default=0.003)
    args = parser.parse_args()

    root = Path(args.run_dir)
    field = np.genfromtxt(root / "diags/reducedfiles/EF.txt")
    particle = np.genfromtxt(root / "diags/reducedfiles/EP.txt")
    total = field[:, 2] + particle[:, 2]
    drift = np.abs(total - total[0]) / abs(total[0])
    result = {
        "run_dir": str(root),
        "sample_count": int(total.size),
        "initial_total_energy": float(total[0]),
        "final_total_energy": float(total[-1]),
        "max_relative_drift": float(np.max(drift)),
        "final_relative_drift": float(drift[-1]),
        "tolerance": args.tolerance,
        "passed": bool(np.all(drift < args.tolerance)),
        "samples": [
            {
                "field_energy": float(field[index, 2]),
                "particle_energy": float(particle[index, 2]),
                "total_energy": float(total[index]),
                "relative_drift": float(drift[index]),
            }
            for index in range(total.size)
        ],
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# Energy-conserving thermal-plasma report",
                "",
                f"- reduced-energy samples: `{result['sample_count']}`",
                f"- maximum relative total-energy drift: `{result['max_relative_drift']:.3e}`",
                f"- final relative total-energy drift: `{result['final_relative_drift']:.3e}`",
                f"- official tolerance: `{result['tolerance']:.3e}`",
                f"- gate result: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "This is the same EF+EP reduced-diagnostic contract consumed by WarpX's official analysis.py; it is distinct from the uniform-plasma reader-side summary.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("energy-conserving thermal-plasma gate failed")


if __name__ == "__main__":
    main()
