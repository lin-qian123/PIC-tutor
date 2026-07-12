#!/usr/bin/env python
"""Compare FieldProbe diffraction errors at matched physical time."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    reports = [json.loads(Path(path).read_text()) for path in args.reports]
    result = {
        "reports": reports,
        "coarse_passed": reports[0]["passed"],
        "refined_passed": reports[-1]["passed"],
        "resolution_conclusion": (
            reports[0]["passed"] is False
            and reports[-1]["passed"] is True
            and reports[-1]["official_script_average_error_percent"]
            < reports[0]["official_script_average_error_percent"]
        ),
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    rows = [
        "# FieldProbe resolution comparison",
        "",
        "| case | MPI ranks | sample step | selected-point mean | max selected error | gate |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for report in reports:
        rows.append(
            f"| `{Path(report['run_dir']).name}` | {report['mpi_processes']} | "
            f"{report['sample_step']} | "
            f"`{report['official_script_average_error_percent']:.4f}%` | "
            f"`{report['maximum_selected_error_percent']:.4f}%` | "
            f"`{'PASS' if report['passed'] else 'FAIL'}` |"
        )
    rows.extend(
        [
            "",
            "The refined case uses step 1000 because its halved timestep makes it the same physical time as step 500 in the coarse case. The comparison supports a spatial-discretization explanation for the coarse-case failure; it does not change the official coarse-case result.",
            "",
        ]
    )
    Path(args.output_md).write_text("\n".join(rows))
    print(json.dumps(result, indent=2))
    if not result["resolution_conclusion"]:
        raise SystemExit("FieldProbe resolution comparison did not support the expected conclusion")


if __name__ == "__main__":
    main()
