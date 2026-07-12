#!/usr/bin/env python
"""Analyze the native external-file Gaussian-beam focusing contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries
from scipy.constants import c, eV, m_e, micro, nano


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    energy = 125.0e9 * eV
    gamma = energy / (m_e * c**2)
    sigmax = 516.0 * nano
    sigmay = 7.7 * nano
    sigmaz = 300.0 * micro
    emitx = 50.0 * micro
    emity = 20.0 * nano
    focal_distance = 4.0 * sigmaz
    gridz = np.linspace(-10.0 * sigmaz, 10.0 * sigmaz, 256)
    tol = gridz[1] - gridz[0]

    series = OpenPMDTimeSeries(str(args.run_dir / "diags" / "openpmd"))
    x, y, z, w = series.get_particle(
        ["x", "y", "z", "w"], species="beam1", iteration=0, plot=False
    )
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    w = np.asarray(w)
    if not (x.size == y.size == z.size == w.size and x.size > 0):
        raise SystemExit("Gaussian beam diagnostic has inconsistent or empty particle arrays")

    sx = []
    sy = []
    sx_ref = []
    sy_ref = []
    imin = int(np.argmin(np.abs(gridz + 0.8 * focal_distance)))
    imax = int(np.argmin(np.abs(gridz - 0.8 * focal_distance)))
    for center in gridz[imin:imax]:
        mask = np.abs(z - center) < tol
        if not np.any(mask):
            continue
        weights = w[mask]
        mux = np.average(x[mask], weights=weights)
        muy = np.average(y[mask], weights=weights)
        sx.append(np.sqrt(np.average((x[mask] - mux) ** 2, weights=weights)))
        sy.append(np.sqrt(np.average((y[mask] - muy) ** 2, weights=weights)))
        sx_ref.append(np.sqrt(sigmax**2 + (emitx / gamma) ** 2 * (center - focal_distance) ** 2 / sigmax**2))
        sy_ref.append(np.sqrt(sigmay**2 + (emity / gamma) ** 2 * (center - focal_distance) ** 2 / sigmay**2))

    sx = np.asarray(sx)
    sy = np.asarray(sy)
    sx_ref = np.asarray(sx_ref)
    sy_ref = np.asarray(sy_ref)
    x_rel = np.abs(sx - sx_ref) / sx_ref
    y_rel = np.abs(sy - sy_ref) / sy_ref
    result = {
        "run_dir": str(args.run_dir),
        "iteration": 0,
        "particle_count": int(x.size),
        "total_weight": float(w.sum()),
        "slice_count": int(sx.size),
        "max_relative_sigma_x_error": float(x_rel.max()),
        "max_relative_sigma_y_error": float(y_rel.max()),
        "sigma_x_tolerance": 0.051,
        "sigma_y_tolerance": 0.038,
        "passed": bool(x_rel.max() <= 0.051 and y_rel.max() <= 0.038),
        "contract": "native openPMD external-file Gaussian beam focusing envelope",
        "official_analysis_note": "official CMake names analysis.py for this native variant, but that file is absent; analysis_focusing_beam.py and this independent script were run against the producer output",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# Native external-file Gaussian beam focus contract\n\n"
        f"- status: `{status}`\n"
        f"- particle count / total weight: `{result['particle_count']}` / `{result['total_weight']:.8e}`\n"
        f"- z-slice count: `{result['slice_count']}`\n"
        f"- max relative sigma-x error: `{result['max_relative_sigma_x_error']:.8e}`\n"
        f"- max relative sigma-y error: `{result['max_relative_sigma_y_error']:.8e}`\n"
        f"- tolerances: x `{result['sigma_x_tolerance']:.3f}`, y `{result['sigma_y_tolerance']:.3f}`\n"
        f"- contract: {result['contract']}\n"
        f"- note: {result['official_analysis_note']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("Gaussian beam focus contract failed")


if __name__ == "__main__":
    main()
