#!/usr/bin/env python
"""Plot the validated FieldProbe coarse/refined resolution comparison."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparison", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    data = json.loads(args.comparison.read_text(encoding="utf-8"))
    reports = data["reports"]
    labels = ["coarse\nλ/16, step 500", "refined\nλ/32, step 1000"]
    avg = [report["official_script_average_error_percent"] for report in reports]
    maximum = [report["maximum_selected_error_percent"] for report in reports]
    colors = ["#c44e52" if not report["passed"] else "#2a9d8f" for report in reports]
    x = list(range(len(reports)))

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.1), constrained_layout=True)
    axes[0].bar(x, avg, color=colors, width=0.58)
    axes[0].axhline(2.5, color="#333333", linestyle="--", linewidth=1.1, label="gate = 2.5%")
    axes[0].set_title("Official average error")
    axes[0].set_ylabel("Relative error (%)")
    axes[1].bar(x, maximum, color=colors, width=0.58)
    axes[1].set_title("Maximum selected-point error")
    axes[1].set_ylabel("Relative error (%)")

    for axis, values in zip(axes, (avg, maximum)):
        axis.set_xticks(x, labels)
        axis.grid(axis="y", alpha=0.25)
        for index, value in enumerate(values):
            axis.text(index, value, f"{value:.3f}%", ha="center", va="bottom", fontsize=9)

    axes[0].legend(frameon=False)
    fig.suptitle("FieldProbe single-slit diffraction: resolution comparison")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
