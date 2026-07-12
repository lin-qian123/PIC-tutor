#!/usr/bin/env python
"""Render the planned transition-zone route-count ledger flow."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def box(ax, xy, width, height, text, color):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        facecolor=color,
        edgecolor="#33414d",
        linewidth=1.0,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=9, wrap=True)
    return patch


def arrow(ax, start, end, color="#52606d"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13, linewidth=1.5, color=color))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    fig, ax = plt.subplots(figsize=(12, 5.2), constrained_layout=True)
    fig.suptitle("Transition-zone reduced route-count contract", fontsize=15, fontweight="bold")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    box(ax, (0.3, 2.35), 1.9, 1.1, "PartitionParticlesInBuffers\nroute counts + weights", "#d9eaf7")
    box(ax, (2.75, 3.55), 1.65, 1.0, "fine routes\nfine gather/deposit", "#dff2e1")
    box(ax, (2.75, 1.25), 1.65, 1.0, "buffer routes\ncoarse gather/deposit", "#fde4cf")
    box(ax, (5.05, 3.55), 1.7, 1.0, "rho_fp / current_fp\nsource norms", "#e8f0fa")
    box(ax, (5.05, 1.25), 1.7, 1.0, "rho_buf / current_buf\nsource norms", "#fcebdc")
    box(ax, (7.4, 2.35), 1.9, 1.1, "coarsened fine +\nowner-mask ledger", "#eee4f5")
    box(ax, (9.75, 2.35), 1.9, 1.1, "SyncRho / SyncCurrent\npost-sync closure", "#e1e8ec")

    arrow(ax, (2.2, 2.9), (2.72, 4.0))
    arrow(ax, (2.2, 2.9), (2.72, 1.8))
    arrow(ax, (4.45, 4.05), (5.02, 4.05))
    arrow(ax, (4.45, 1.75), (5.02, 1.75))
    arrow(ax, (6.8, 4.05), (7.35, 3.05))
    arrow(ax, (6.8, 1.75), (7.35, 2.75))
    arrow(ax, (9.35, 2.9), (9.7, 2.9))

    ax.text(0.4, 0.5, "Required gates: count closure -> weight closure -> explicit intermediate source fields -> owner-mask-aware sync closure", fontsize=9, color="#425466")
    ax.text(0.4, 0.18, "Design-layer flow only: the current WarpX checkout does not yet emit this ledger or route IDs.", fontsize=9, color="#9b2c2c")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
