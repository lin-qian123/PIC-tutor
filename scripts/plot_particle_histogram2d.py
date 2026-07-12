#!/usr/bin/env python
"""Plot the validated ParticleHistogram2D BP5 series at two iterations."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import LogNorm
    from openpmd_viewer import OpenPMDTimeSeries

    root = args.run_dir.resolve()
    names = ("PhaseSpaceIons", "PhaseSpaceElectrons")
    iterations = (0, 100)
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 7.0), constrained_layout=True)

    for row, name in enumerate(names):
        series = OpenPMDTimeSeries(str(root / f"diags/reducedfiles/{name}"))
        for column, iteration in enumerate(iterations):
            data, info = series.get_field("data", iteration=iteration)
            data = np.asarray(data, dtype=float)
            axis_0 = np.asarray(getattr(info, info.axes[0]), dtype=float)
            axis_1 = np.asarray(getattr(info, info.axes[1]), dtype=float)
            positive = data[data > 0]
            image_data = np.ma.masked_less_equal(data, 0)
            axis = axes[row, column]
            axis.imshow(
                image_data,
                origin="lower",
                aspect="auto",
                extent=[axis_1[0], axis_1[-1], axis_0[0], axis_0[-1]],
                norm=LogNorm(vmin=float(positive.min()), vmax=float(positive.max())),
                cmap="magma",
            )
            rows, columns = np.where(data > 0)
            x_values = axis_1[columns]
            y_values = axis_0[rows]
            x_span = max(float(x_values.max() - x_values.min()), float(axis_1[1] - axis_1[0]))
            y_span = max(float(y_values.max() - y_values.min()), float(axis_0[1] - axis_0[0]))
            axis.set_xlim(float(x_values.min() - 0.08 * x_span), float(x_values.max() + 0.08 * x_span))
            axis.set_ylim(float(y_values.min() - 0.08 * y_span), float(y_values.max() + 0.08 * y_span))
            axis.set_title(f"{name}: iteration {iteration}")
            axis.set_xlabel("z")
            axis.set_ylabel("uz")

    fig.suptitle("ParticleHistogram2D: BP5 phase-space writer output")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
