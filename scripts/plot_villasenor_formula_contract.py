#!/usr/bin/env python
"""Render the deterministic Villasenor formula-contract figure."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_villasenor_formula_contract import _split_at_cell_crossings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    segments = _split_at_cell_crossings(-0.8, -0.65, 2.25, 1.75)
    colors = ("#1769aa", "#d95f02", "#1b9e77", "#7570b3", "#e7298a")
    residuals = {
        "4-boundary": 4.440892098500626e-16,
        "segments": 4.440892098500626e-16,
        "3D faces": 1.7763568394002505e-15,
        "3D volume": 1.7763568394002505e-15,
    }

    fig, (ax_path, ax_residual) = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    fig.suptitle("Villasenor-Buneman formula contract", fontsize=15, fontweight="bold")

    for ix in range(-1, 3):
        for iy in range(-1, 3):
            ax_path.add_patch(Rectangle((ix, iy), 1, 1, fill=False, lw=0.8, ec="#b8c2cc"))
    x0, y0 = -0.8, -0.65
    x1, y1 = 2.25, 1.75
    ax_path.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="->", mutation_scale=14, lw=1.2, color="#202a33"))
    for index, (sx, sy, dx, dy) in enumerate(segments):
        ex, ey = sx + dx, sy + dy
        ax_path.add_patch(
            FancyArrowPatch(
                (sx, sy),
                (ex, ey),
                arrowstyle="-|>",
                mutation_scale=11,
                lw=3.0,
                color=colors[index % len(colors)],
                alpha=0.9,
            )
        )
        ax_path.scatter((sx, ex), (sy, ey), s=16, color=colors[index % len(colors)], zorder=4)
        ax_path.text((sx + ex) / 2, (sy + ey) / 2 + 0.08, f"S{index + 1}", fontsize=9, ha="center")
    ax_path.scatter((x0, x1), (y0, y1), s=34, color="#202a33", zorder=5)
    ax_path.text(x0 - 0.05, y0 - 0.22, "old", ha="right", fontsize=9)
    ax_path.text(x1 + 0.05, y1 + 0.08, "new", fontsize=9)
    ax_path.set_title("Repeated earliest-crossing segmentation")
    ax_path.set_xlabel("x / cell")
    ax_path.set_ylabel("y / cell")
    ax_path.set_aspect("equal")
    ax_path.set_xlim(-1.05, 2.55)
    ax_path.set_ylim(-1.0, 2.15)
    ax_path.grid(alpha=0.15)

    names = list(residuals)
    values = list(residuals.values())
    bars = ax_residual.bar(names, values, color=("#1769aa", "#d95f02", "#1b9e77", "#7570b3"))
    ax_residual.set_yscale("log")
    ax_residual.set_ylim(1e-17, 1e-14)
    ax_residual.axhline(1e-14, color="#b2182b", ls="--", lw=1, label="contract gate")
    ax_residual.set_title("Deterministic closure residuals")
    ax_residual.set_ylabel("maximum absolute residual")
    ax_residual.tick_params(axis="x", labelrotation=22)
    ax_residual.grid(axis="y", alpha=0.2)
    ax_residual.legend(frameon=False, fontsize=8, loc="lower left")
    for bar, value in zip(bars, values):
        ax_residual.text(bar.get_x() + bar.get_width() / 2, value * 1.35, f"{value:.1e}", ha="center", va="bottom", fontsize=8)

    fig.text(
        0.5,
        0.01,
        "The figure validates the paper/geometric layer only; it is not a bitwise WarpX-kernel or full geometry/order regression.",
        ha="center",
        fontsize=9,
        color="#4d5963",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
