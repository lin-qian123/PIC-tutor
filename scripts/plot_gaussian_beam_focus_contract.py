#!/usr/bin/env python
"""Plot measured and theoretical Gaussian-beam focus envelopes."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries
from scipy.constants import c, eV, m_e, micro, nano


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
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
    imin = int(np.argmin(np.abs(gridz + 0.8 * focal_distance)))
    imax = int(np.argmin(np.abs(gridz - 0.8 * focal_distance)))

    series = OpenPMDTimeSeries(str(args.run_dir / "diags" / "openpmd"))
    x, y, z, w = series.get_particle(
        ["x", "y", "z", "w"], species="beam1", iteration=0, plot=False
    )
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    w = np.asarray(w)

    measured_x = []
    measured_y = []
    centers = gridz[imin:imax]
    for center in centers:
        mask = np.abs(z - center) < tol
        if not np.any(mask):
            continue
        weights = w[mask]
        mux = np.average(x[mask], weights=weights)
        muy = np.average(y[mask], weights=weights)
        measured_x.append(np.sqrt(np.average((x[mask] - mux) ** 2, weights=weights)))
        measured_y.append(np.sqrt(np.average((y[mask] - muy) ** 2, weights=weights)))

    centers = centers[: len(measured_x)]
    measured_x = np.asarray(measured_x)
    measured_y = np.asarray(measured_y)
    theory_x = np.sqrt(sigmax**2 + (emitx / gamma) ** 2 * (centers - focal_distance) ** 2 / sigmax**2)
    theory_y = np.sqrt(sigmay**2 + (emity / gamma) ** 2 * (centers - focal_distance) ** 2 / sigmay**2)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8), constrained_layout=True)
    z_mm = centers / 1e-3
    axes[0].plot(z_mm, measured_x / nano, "o", ms=3.0, color="#1769aa", label="native output")
    axes[0].plot(z_mm, theory_x / nano, color="#d94801", linewidth=1.5, label="theory")
    axes[0].set_title("Horizontal envelope")
    axes[0].set_ylabel("sigma_x (nm)")
    axes[1].plot(z_mm, measured_y / nano, "o", ms=3.0, color="#238b45", label="native output")
    axes[1].plot(z_mm, theory_y / nano, color="#d94801", linewidth=1.5, label="theory")
    axes[1].set_title("Vertical envelope")
    axes[1].set_ylabel("sigma_y (nm)")
    for axis in axes:
        axis.set_xlabel("z (mm)")
        axis.grid(alpha=0.25)
        axis.legend(frameon=False, fontsize=8)
    fig.suptitle("Native openPMD external-file Gaussian beam focus contract")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
