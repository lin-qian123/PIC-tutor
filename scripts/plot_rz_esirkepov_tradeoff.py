#!/usr/bin/env python
"""Render the RZ Esirkepov axis-correction/shape tradeoff evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trend", type=Path, required=True)
    parser.add_argument("--family", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    trend = json.loads(args.trend.read_text(encoding="utf-8"))
    family = json.loads(args.family.read_text(encoding="utf-8"))

    fig, (ax_trend, ax_family) = plt.subplots(1, 2, figsize=(12, 5.3), constrained_layout=True)
    fig.suptitle("RZ Esirkepov correction/shape tradeoff", fontsize=15, fontweight="bold")
    colors = {"on": "#d95f02", "off": "#1b9e77"}
    markers = {"on": "o", "off": "s"}

    for correction in ("on", "off"):
        rows = [row for row in trend["rows"] if row["correction"] == correction]
        rows.sort(key=lambda row: row["resolution"][0])
        x = [f"{row['resolution'][0]}x{row['resolution'][1]}" for row in rows]
        y = [row["charge_residual"] for row in rows]
        ax_trend.plot(x, y, marker=markers[correction], lw=2, color=colors[correction], label=f"correction {correction}")
    ax_trend.axhline(1e-11, color="#b2182b", ls="--", lw=1, label="charge gate")
    ax_trend.set_yscale("log")
    ax_trend.set_title("shape=1 resolution trend")
    ax_trend.set_ylabel("axis charge residual")
    ax_trend.set_xlabel("RZ grid")
    ax_trend.grid(axis="y", alpha=0.2)
    ax_trend.legend(frameon=False, fontsize=8)

    on_rows = [row for row in family["rows"] if row["correction"] == "on"]
    shapes = [str(row["shape"]) for row in on_rows]
    on = [row["charge_residual"] for row in on_rows]
    off_rows = [row for row in family["rows"] if row["correction"] == "off"]
    off = [row["charge_residual"] for row in off_rows]
    positions = list(range(len(shapes)))
    width = 0.36
    ax_family.bar([p - width / 2 for p in positions], on, width, color=colors["on"], label="correction on")
    ax_family.bar([p + width / 2 for p in positions], off, width, color=colors["off"], label="correction off")
    ax_family.axhline(1e-11, color="#b2182b", ls="--", lw=1, label="charge gate")
    ax_family.set_yscale("log")
    ax_family.set_xticks(positions, [f"shape {shape}" for shape in shapes])
    ax_family.set_title("256x512 shape family")
    ax_family.set_ylabel("axis charge residual")
    ax_family.grid(axis="y", alpha=0.2)
    ax_family.legend(frameon=False, fontsize=8)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
