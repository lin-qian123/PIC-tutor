#!/usr/bin/env python
"""Plot normalized ParticleHistogram2D particle-count sensitivity gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


THRESHOLDS = {"total_weight": 1.0e-3, "std_z": 1.0e-2, "std_uz": 5.0e-2}
METRIC_LABELS = {
    "total_weight": "total weight",
    "std_z": "std(z)",
    "std_uz": "std(uz)",
}
COLORS = {"total_weight": "#1f77b4", "std_z": "#d62728", "std_uz": "#2ca02c"}
MARKERS = {"total_weight": "o", "std_z": "s", "std_uz": "^"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-png", required=True)
    parser.add_argument("--output-pdf", required=True)
    args = parser.parse_args()

    result = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    pairs = result["pairwise"]
    labels = [f"{pair['left']} to {pair['right']}" for pair in pairs]

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.25), sharey=True)
    for ax, species in zip(axes, ("PhaseSpaceIons", "PhaseSpaceElectrons")):
        x = range(len(pairs))
        for metric, color in COLORS.items():
            values = [
                pair["series"][species]["relative_differences"][metric] / THRESHOLDS[metric]
                for pair in pairs
            ]
            ax.plot(
                x,
                values,
                color=color,
                marker=MARKERS[metric],
                linewidth=1.5,
                markersize=4.5,
                label=METRIC_LABELS[metric],
            )
        ax.axhline(1.0, color="#444444", linewidth=1.0, linestyle="--")
        ax.set_xticks(list(x), labels, rotation=28, ha="right")
        ax.set_title("ions" if species.endswith("Ions") else "electrons")
        ax.grid(axis="y", color="#d9d9d9", linewidth=0.6)
        ax.set_ylim(1.0e-4, 4.0)
        ax.set_yscale("log")

    axes[0].set_ylabel("relative difference / local gate")
    axes[0].legend(frameon=False, fontsize=8, loc="upper right")
    fig.suptitle("ParticleHistogram2D particle-count sensitivity", fontsize=11)
    fig.text(
        0.5,
        0.01,
        "Dashed line = gate boundary; values below 1 pass the local reader-side gate",
        ha="center",
        fontsize=7.5,
    )
    fig.tight_layout(rect=(0, 0.08, 1, 0.92))
    Path(args.output_png).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_pdf).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_png, dpi=300, bbox_inches="tight")
    fig.savefig(args.output_pdf, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
