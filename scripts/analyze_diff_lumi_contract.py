#!/usr/bin/env python
"""Run and summarize WarpX differential-luminosity validation."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--analysis-script", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    completed = subprocess.run(
        [sys.executable, str(Path(args.analysis_script).resolve())],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    log = completed.stdout + completed.stderr
    (root / "diff-lumi-analysis.log").write_text(log)
    errors = [float(value) for value in re.findall(r"Relative error:\s+([0-9.eE+-]+)", log)]
    tolerances = [float(value) for value in re.findall(r"Tolerance:\s+([0-9.eE+-]+)", log)]
    if len(errors) != 2 or len(tolerances) != 2:
        raise SystemExit("official differential-luminosity analysis did not emit two gates")

    one_d_path = root / "diags/reducedfiles/DifferentialLuminosity_beam1_beam2.txt"
    one_d_header = one_d_path.read_text().splitlines()[0]
    energy_bins = np.array(
        [float(value) for value in re.findall(r"=(.*?)\(", one_d_header)], dtype=float
    )
    one_d = np.loadtxt(one_d_path)
    series = OpenPMDTimeSeries(
        str(root / "diags/reducedfiles/DifferentialLuminosity2d_beam1_beam2")
    )
    iteration = int(series.iterations[-1])
    two_d, info = series.get_field("d2L_dE1_dE2", iteration=iteration)
    result = {
        "run_dir": str(root),
        "test_family": _test_family(root.name),
        "mpi_processes": _read_mpi_processes(root),
        "amr_max_level": _read_input_value(root / "warpx_used_inputs", "amr.max_level"),
        "official_analysis_exit_code": completed.returncode,
        "official_analysis_passed": completed.returncode == 0,
        "relative_errors": errors,
        "tolerances": tolerances,
        "gate_passed": [error < tolerance for error, tolerance in zip(errors, tolerances)],
        "one_d_rows": int(one_d.shape[0]),
        "one_d_columns": int(one_d.shape[1]),
        "one_d_final_step": int(one_d[-1, 0]),
        "one_d_final_time": float(one_d[-1, 1]),
        "one_d_energy_bins": int(len(energy_bins)),
        "two_d_iterations": [int(value) for value in series.iterations],
        "two_d_final_iteration": iteration,
        "two_d_shape": [int(value) for value in two_d.shape],
        "two_d_axes": {str(key): value for key, value in info.axes.items()},
        "two_d_max": float(np.max(two_d)),
        "passed": completed.returncode == 0
        and all(error < tolerance for error, tolerance in zip(errors, tolerances)),
        "contract": "official 1D and 2D differential-luminosity diagnostics compared with analytic Gaussian-beam spectra",
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# Differential-luminosity contract report",
                "",
                f"- test family: `{result['test_family']}`",
                f"- MPI processes: `{result['mpi_processes']}`",
                f"- AMR max level: `{result['amr_max_level']}`",
                f"- 1D final step / rows / energy bins: `{result['one_d_final_step']} / {result['one_d_rows']} / {result['one_d_energy_bins']}`",
                f"- 2D iterations / final shape: `{result['two_d_iterations']} / {result['two_d_shape']}`",
                f"- 1D relative error / tolerance: `{errors[0]:.6%} / {tolerances[0]:.6%}`",
                f"- 2D relative error / tolerance: `{errors[1]:.6%} / {tolerances[1]:.6%}`",
                f"- official analysis result: `{'PASS' if result['official_analysis_passed'] else 'FAIL'}`",
                f"- combined contract result: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "The wrapped official analysis compares the 1D differential-luminosity spectrum and 2D differential-luminosity grid with the analytic Gaussian-beam reference. The artifact fields above additionally record the reduced-output shape and final iteration, including the AMR sibling boundary.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("differential-luminosity contract failed")


def _test_family(name: str) -> str:
    if "photons" in name:
        return "photons"
    if "mr" in name:
        return "leptons_amr"
    return "leptons"


def _read_input_value(path: Path, key: str) -> int | None:
    if not path.exists():
        return None
    pattern = re.compile(rf"^{re.escape(key)}\s*=\s*([^\s]+)", re.MULTILINE)
    match = pattern.search(path.read_text())
    return int(match.group(1)) if match else None


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
