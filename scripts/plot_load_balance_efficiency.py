#!/usr/bin/env python
"""Plot before/after LoadBalanceCosts efficiency for validated siblings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=Path, nargs=2, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import matplotlib.pyplot as plt
    import numpy as np

    reports = [json.loads(path.read_text(encoding="utf-8")) for path in args.reports]
    labels = ["Heuristic", "Timers"]
    before = [report["efficiency_before"] for report in reports]
    after = [report["efficiency_after"] for report in reports]
    x = np.arange(len(labels))
    width = 0.34

    fig, axis = plt.subplots(figsize=(7.4, 4.0), constrained_layout=True)
    bars_before = axis.bar(x - width / 2, before, width, label="before", color="#9ecae1")
    bars_after = axis.bar(x + width / 2, after, width, label="after", color="#2171b5")
    axis.set_title("LoadBalanceCosts: rank-level efficiency improvement")
    axis.set_ylabel("Efficiency η")
    axis.set_xticks(x, labels)
    axis.set_ylim(0, 1.08)
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False)
    for bars in (bars_before, bars_after):
        for bar in bars:
            axis.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=9)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
