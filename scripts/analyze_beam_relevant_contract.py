#!/usr/bin/env python
"""Validate a minimal 3D BeamRelevant Gaussian-beam diagnostic case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.special import erf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    path = root / "bmmntr.txt"
    lines = path.read_text().splitlines()
    header = lines[0]
    data = np.loadtxt(path)
    if data.ndim == 1:
        data = data[None, :]
    row = data[-1]

    q_tot = -1.0e-20
    z_cut = 2.0
    sigma = 0.25
    truncation = erf(z_cut / np.sqrt(2.0))
    expected_charge = q_tot * truncation
    normal_pdf = np.exp(-0.5 * z_cut**2) / np.sqrt(2.0 * np.pi)
    expected_z_rms = sigma * np.sqrt(1.0 - 2.0 * z_cut * normal_pdf / truncation)
    checks = {
        "header_columns": header.count("]") == 24,
        "row_count": len(data) == 1,
        "column_count": data.shape[1] == 24,
        "finite": bool(np.isfinite(data).all()),
        "charge": abs((row[23] - expected_charge) / expected_charge) < 0.02,
        "mean_position": bool(np.max(np.abs(row[2:5])) < 0.01),
        "transverse_rms": bool(np.max(np.abs(row[[9, 10]] - sigma) / sigma) < 0.02),
        "longitudinal_rms": abs((row[11] - expected_z_rms) / expected_z_rms) < 0.02,
        "positive_moments": bool(np.all(row[[8, 16, 17, 18, 21, 22]] > 0.0)),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    result = {
        "run_dir": str(root),
        "mpi_processes": 1,
        "rows": int(len(data)),
        "columns": int(data.shape[1]),
        "expected_charge": expected_charge,
        "observed_charge": float(row[23]),
        "charge_relative_error": float(abs((row[23] - expected_charge) / expected_charge)),
        "expected_z_rms": expected_z_rms,
        "observed_z_rms": float(row[11]),
        "observed_position_mean": [float(value) for value in row[2:5]],
        "observed_transverse_rms": [float(value) for value in row[[9, 10]]],
        "observed_gamma_mean": float(row[8]),
        "observed_emittance": [float(value) for value in row[16:19]],
        "checks": checks,
        "passed": all(checks.values()),
        "contract": "3D BeamRelevant output schema plus truncated-Gaussian position and charge gates",
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# BeamRelevant contract report",
                "",
                "- case: minimal 3D Gaussian beam, 1 MPI rank, initialization-only",
                f"- output rows / columns: `{result['rows']} / {result['columns']}`",
                f"- observed charge / expected charge: `{result['observed_charge']:.9e} / {result['expected_charge']:.9e}`",
                f"- charge relative error: `{result['charge_relative_error']:.3e}`",
                f"- observed z rms / expected z rms: `{result['observed_z_rms']:.9e} / {result['expected_z_rms']:.9e}`",
                f"- contract result: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "The expected charge includes the `z_cut = 2` truncation of the Gaussian beam. The position gates check the two transverse rms values and the analytically truncated longitudinal rms; the remaining BeamRelevant moments are required to be finite and physically positive where applicable.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("BeamRelevant contract failed")


if __name__ == "__main__":
    main()
