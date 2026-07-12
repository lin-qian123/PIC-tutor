#!/usr/bin/env python
"""Render the bounded deposition geometry/order coverage matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


COLORS = {
    "PASS": "#1b9e77",
    "MIXED": "#d95f02",
    "BOUNDARY": "#d73027",
    "LIMITED": "#4575b4",
}
SHORT_LABELS = {"PASS": "PASS", "MIXED": "MIX", "BOUNDARY": "EDGE", "LIMITED": "LIMIT"}


def classify(evidence: str) -> str:
    upper = evidence.upper()
    if "BOUNDARY" in upper and "PASS" in upper:
        return "MIXED"
    if "BOUNDARY" in upper:
        return "BOUNDARY"
    if "RADIAL ER PASS" in upper:
        return "LIMITED"
    return "PASS"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    rows = data["rows"]
    states = [classify(row["evidence"]) for row in rows]

    fig, (ax_matrix, ax_counts) = plt.subplots(
        1, 2, figsize=(12, 5.8), gridspec_kw={"width_ratios": [3.2, 1.25]}, constrained_layout=True
    )
    fig.suptitle("PIC deposition geometry/order coverage", fontsize=15, fontweight="bold")

    ax_matrix.set_xlim(-0.5, 3.5)
    ax_matrix.set_ylim(-0.8, len(rows) - 0.2)
    ax_matrix.set_xticks(range(4), ["family", "geometry", "shape/order", "evidence"])
    ax_matrix.set_yticks(range(len(rows)), [f"{i + 1:02d}" for i in range(len(rows))])
    ax_matrix.invert_yaxis()
    ax_matrix.tick_params(axis="y", length=0, labelsize=8)
    ax_matrix.grid(axis="y", alpha=0.18)
    ax_matrix.set_title("Evidence cells (bounded, not Cartesian-product coverage)", fontsize=11)
    for index, (row, state) in enumerate(zip(rows, states)):
        ax_matrix.scatter(3, index, s=260, color=COLORS[state], edgecolor="white", linewidth=1.2, zorder=3)
        ax_matrix.text(3, index, SHORT_LABELS[state], ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
        ax_matrix.text(0, index, row["family"], ha="center", va="center", fontsize=8)
        ax_matrix.text(1, index, row["geometry"], ha="center", va="center", fontsize=8)
        ax_matrix.text(2, index, row["shape_order"], ha="center", va="center", fontsize=8)
    ax_matrix.spines[["top", "right", "left"]].set_visible(False)
    ax_matrix.spines["bottom"].set_color("#aab4be")
    ax_matrix.legend(
        handles=[Line2D([0], [0], marker="o", color="w", label=key, markerfacecolor=value, markersize=8) for key, value in COLORS.items()],
        loc="lower left",
        bbox_to_anchor=(0, -0.18),
        ncol=4,
        frameon=False,
        fontsize=8,
    )

    counts = {key: states.count(key) for key in COLORS}
    keys = [key for key in COLORS if counts[key]]
    bars = ax_counts.bar(keys, [counts[key] for key in keys], color=[COLORS[key] for key in keys])
    ax_counts.set_title("Rows by evidence state", fontsize=11)
    ax_counts.set_ylabel("matrix rows")
    ax_counts.set_ylim(0, max(counts.values()) + 2)
    ax_counts.grid(axis="y", alpha=0.2)
    ax_counts.tick_params(axis="x", labelrotation=25)
    for bar in bars:
        ax_counts.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08, f"{int(bar.get_height())}", ha="center", fontsize=9)
    ax_counts.text(
        0.02,
        -0.29,
        "PASS = strongest available evidence\nMIXED = pass plus boundary\nLIMITED = field-only evidence",
        transform=ax_counts.transAxes,
        fontsize=8,
        color="#4d5963",
        va="top",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
