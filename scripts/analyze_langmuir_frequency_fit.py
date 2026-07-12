#!/usr/bin/env python
"""Fit the Langmuir mode and check charge conservation from plotfiles."""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, e, epsilon_0, m_e
from scipy.optimize import minimize_scalar


def load_snapshots(pattern: str) -> list[dict[str, float]]:
    paths = sorted(glob.glob(pattern))
    if not paths:
        raise FileNotFoundError(pattern)
    snapshots = []
    for path in paths:
        ds = yt.load(path)
        data = ds.covering_grid(0, ds.domain_left_edge, ds.domain_dimensions)
        ez = data[("mesh", "Ez")].to_ndarray()[:, 0, 0]
        rho = data[("boxlib", "rho")].to_ndarray()[:, 0, 0]
        div_e = data[("boxlib", "divE")].to_ndarray()[:, 0, 0]
        denominator = np.max(np.abs(rho / epsilon_0))
        charge_error = (
            float(np.max(np.abs(div_e - rho / epsilon_0)) / denominator)
            if denominator > 0.0
            else 0.0
        )
        snapshots.append(
            {
                "path": str(Path(path)),
                "time": float(ds.current_time.to_value()),
                "ez": ez,
                "charge_error": charge_error,
                "left": float(ds.domain_left_edge[0]),
                "right": float(ds.domain_right_edge[0]),
            }
        )
    return snapshots


def fit_mode(snapshots: list[dict[str, float]], expected_wp: float) -> tuple[float, float]:
    times = np.array([item["time"] for item in snapshots])
    amplitudes = []
    for item in snapshots:
        z = np.linspace(item["left"], item["right"], item["ez"].size, endpoint=False)
        basis = np.sin(2.0 * np.pi * 2.0 * z / (item["right"] - item["left"]))
        amplitudes.append(2.0 * np.dot(item["ez"], basis) / basis.size)
    amplitudes = np.array(amplitudes)

    def residual(omega: float) -> float:
        design = np.column_stack((np.sin(omega * times), np.cos(omega * times)))
        coefficients, *_ = np.linalg.lstsq(design, amplitudes, rcond=None)
        return float(np.sum((design @ coefficients - amplitudes) ** 2))

    result = minimize_scalar(
        residual,
        bounds=(0.5 * expected_wp, 1.5 * expected_wp),
        method="bounded",
        options={"xatol": expected_wp * 1.0e-12},
    )
    return float(result.x), float(np.sqrt(result.fun))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="glob for plotfiles, e.g. diags/diag10000*")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    snapshots = load_snapshots(args.pattern)
    expected_wp = np.sqrt(4.0e24 * e**2 / (m_e * epsilon_0))
    fitted_wp, fit_residual = fit_mode(snapshots, expected_wp)
    payload = {
        "snapshot_count": len(snapshots),
        "expected_wp": float(expected_wp),
        "fitted_wp": fitted_wp,
        "relative_frequency_error": float(abs(fitted_wp - expected_wp) / expected_wp),
        "fit_residual_l2": fit_residual,
        "max_charge_conservation_error": max(item["charge_error"] for item in snapshots),
        "snapshots": [
            {key: value for key, value in item.items() if key != "ez"}
            for item in snapshots
        ],
    }
    Path(args.output_json).write_text(json.dumps(payload, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# Langmuir frequency-fit report",
                "",
                f"- snapshots: `{payload['snapshot_count']}`",
                f"- expected plasma frequency: `{expected_wp:.12e}`",
                f"- fitted plasma frequency: `{fitted_wp:.12e}`",
                f"- relative frequency error: `{payload['relative_frequency_error']:.3e}`",
                f"- maximum `divE-rho/epsilon_0` error: `{payload['max_charge_conservation_error']:.3e}`",
                f"- mode-fit residual L2: `{fit_residual:.3e}`",
                "",
                "The fit uses the projected `Ez` mode and a two-quadrature sinusoidal model. It is a reader-side validation of the recorded run, not a replacement for WarpX's official analysis script.",
                "",
            ]
        )
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
