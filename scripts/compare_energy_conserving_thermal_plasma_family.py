#!/usr/bin/env python
"""Compare the shared reduced-energy gate across 1D and 2D siblings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", help="JSON reports from sibling runs")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    reports = [json.loads(Path(path).read_text()) for path in args.reports]
    result = {
        "siblings": [
            {
                "run_dir": report["run_dir"],
                "sample_count": report["sample_count"],
                "max_relative_drift": report["max_relative_drift"],
                "tolerance": report["tolerance"],
                "passed": report["passed"],
            }
            for report in reports
        ],
        "all_passed": all(report["passed"] for report in reports),
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    rows = [
        "# Energy-conserving thermal-plasma family comparison",
        "",
        "| sibling | samples | max relative drift | tolerance | result |",
        "|---|---:|---:|---:|---|",
    ]
    for sibling in result["siblings"]:
        dimension = "1D" if "_1d" in sibling["run_dir"] else "2D"
        rows.append(
            f"| `{dimension}` | {sibling['sample_count']} | "
            f"`{sibling['max_relative_drift']:.3e}` | "
            f"`{sibling['tolerance']:.3e}` | "
            f"`{'PASS' if sibling['passed'] else 'FAIL'}` |"
        )
    rows.extend(
        [
            "",
            "Both geometry siblings consume the same reduced `EF+EP` contract; this report checks family-level agreement, not equivalence of the physical trajectories.",
            "",
        ]
    )
    Path(args.output_md).write_text("\n".join(rows))
    print(json.dumps(result, indent=2))
    if not result["all_passed"]:
        raise SystemExit("one or more energy-conserving siblings failed")


if __name__ == "__main__":
    main()
