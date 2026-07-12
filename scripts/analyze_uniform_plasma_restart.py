#!/usr/bin/env python
"""Reproduce the field-by-field restart comparison for uniform plasma."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


def load_covering_grid(path: Path):
    dataset = yt.load(str(path))
    if hasattr(dataset, "force_periodicity"):
        dataset.force_periodicity()
    return dataset, dataset.covering_grid(
        level=0,
        left_edge=dataset.domain_left_edge,
        dims=dataset.domain_dimensions,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("benchmark_plotfile")
    parser.add_argument("restart_plotfile")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--tolerance", type=float, default=1.0e-12)
    args = parser.parse_args()

    benchmark_dataset, benchmark_grid = load_covering_grid(Path(args.benchmark_plotfile))
    restart_dataset, restart_grid = load_covering_grid(Path(args.restart_plotfile))
    fields = []
    max_relative_error = 0.0
    max_absolute_error = 0.0
    passed = True

    for field in benchmark_dataset.field_list:
        benchmark = np.asarray(benchmark_grid[field].squeeze().v)
        restart = np.asarray(restart_grid[field].squeeze().v)
        absolute_error = float(np.max(np.abs(restart - benchmark)))
        benchmark_max = float(np.max(np.abs(benchmark)))
        relative_error = (
            absolute_error / benchmark_max if benchmark_max != 0.0 else absolute_error
        )
        field_passed = relative_error < args.tolerance
        fields.append(
            {
                "field": list(field),
                "absolute_error": absolute_error,
                "relative_error": float(relative_error),
                "passed": bool(field_passed),
            }
        )
        max_absolute_error = max(max_absolute_error, absolute_error)
        max_relative_error = max(max_relative_error, relative_error)
        passed = passed and field_passed

    result = {
        "benchmark_plotfile": str(Path(args.benchmark_plotfile)),
        "restart_plotfile": str(Path(args.restart_plotfile)),
        "field_count": len(fields),
        "max_absolute_error": max_absolute_error,
        "max_relative_error": max_relative_error,
        "tolerance": args.tolerance,
        "passed": passed,
        "fields": fields,
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# Uniform-plasma restart report",
                "",
                f"- compared fields: `{result['field_count']}`",
                f"- maximum absolute error: `{result['max_absolute_error']:.3e}`",
                f"- maximum relative error: `{result['max_relative_error']:.3e}`",
                f"- tolerance: `{result['tolerance']:.3e}`",
                f"- gate result: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "The comparison follows WarpX's `analysis_default_restart.py`: level-0 covering grids are compared field by field, with absolute error used when the benchmark field is identically zero.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit("uniform-plasma restart gate failed")


if __name__ == "__main__":
    main()
