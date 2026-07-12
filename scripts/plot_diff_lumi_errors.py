#!/usr/bin/env python
"""Plot 1D/2D differential-luminosity errors for all validated siblings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=Path, nargs=3, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import matplotlib.pyplot as plt
    import numpy as np

    reports = [json.loads(path.read_text(encoding="utf-8")) for path in args.reports]
    labels = ["leptons", "leptons + AMR", "photons"]
    errors = np.asarray([[100 * value for value in report["relative_errors"]] for report in reports])
    tolerances = np.asarray([[100 * value for value in report["tolerances"]] for report in reports])
    x = np.arange(len(labels))
    width = 0.34

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.1), constrained_layout=True)
    for axis, column, title in zip(axes, (0, 1), ("1D differential luminosity", "2D differential luminosity")):
        bars = axis.bar(x, errors[:, column], width, color="#1769aa", label="error")
        axis.plot(x, tolerances[:, column], "k--", marker="o", linewidth=1.2, label="case gate")
        axis.set_title(title)
        axis.set_ylabel("Relative error (%)")
        axis.set_xticks(x, labels, rotation=12)
        axis.grid(axis="y", alpha=0.25)
        for bar, value in zip(bars, errors[:, column]):
            axis.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.3f}%", ha="center", va="bottom", fontsize=8)
        axis.legend(frameon=False)

    fig.suptitle("DifferentialLuminosity: validated 1D/2D Gaussian-beam gates")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
