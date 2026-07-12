#!/usr/bin/env python
"""Measure the WarpX FieldProbe single-slit diffraction contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--step", type=int, default=500)
    parser.add_argument("--tolerance-percent", type=float, default=2.5)
    args = parser.parse_args()

    root = Path(args.run_dir)
    data = pd.read_csv(root / "diags/reducedfiles/FP_line.txt", sep=" ")
    data = data.sort_values(by=["[2]part_x_lev0-(m)"])
    sample = data.query(f"`[0]step()` == {args.step}")
    x = sample["[2]part_x_lev0-(m)"].to_numpy()
    signal = sample["[11]part_S_lev0-(W*s/m^2)"].to_numpy()
    intensity_0 = float(np.max(signal))

    argument = np.pi * 0.3e-6 / 0.2e-6 * np.sin(np.arctan(x / 1.7e-6))
    envelope = np.sinc(argument / np.pi) ** 2
    selected_indices = np.arange(60, 140, 2)
    errors = []
    for index in selected_indices:
        expected = intensity_0 * envelope[index]
        errors.append(float(abs((signal[index] - expected) / expected) * 100.0))

    script_average = float(sum(errors) / (len(selected_indices) - 1))
    arithmetic_average = float(np.mean(errors))
    passed = script_average < args.tolerance_percent
    result = {
        "run_dir": str(root),
        "mpi_processes": _read_mpi_processes(root),
        "sample_step": args.step,
        "sample_count": int(len(sample)),
        "selected_count": int(len(selected_indices)),
        "intensity_0": intensity_0,
        "official_script_average_error_percent": script_average,
        "arithmetic_average_error_percent": arithmetic_average,
        "maximum_selected_error_percent": float(max(errors)),
        "tolerance_percent": args.tolerance_percent,
        "passed": passed,
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# FieldProbe single-slit diffraction report",
                "",
                f"- MPI processes: `{result['mpi_processes']}`",
                f"- sampled step: `{result['sample_step']}`",
                f"- FieldProbe samples: `{result['sample_count']}`",
                f"- selected points: `{result['selected_count']}`",
                f"- official-script average error: `{result['official_script_average_error_percent']:.4f}%`",
                f"- arithmetic mean of selected errors: `{result['arithmetic_average_error_percent']:.4f}%`",
                f"- maximum selected error: `{result['maximum_selected_error_percent']:.4f}%`",
                f"- tolerance: `{result['tolerance_percent']:.4f}%`",
                f"- gate result: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "The metric reproduces `Examples/Tests/field_probe/analysis.py`, including its selected index range and denominator. A failed result is evidence about the current checkout and input contract; it must not be relabeled as a successful reduced-diagnostic validation.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))


def _read_mpi_processes(root: Path) -> int | None:
    candidates = sorted(root.glob("diags/diag*/warpx_job_info"))
    if not candidates:
        return None
    for line in candidates[-1].read_text().splitlines():
        if line.startswith("number of MPI processes:"):
            return int(line.split(":", 1)[1].strip())
    return None


if __name__ == "__main__":
    main()
