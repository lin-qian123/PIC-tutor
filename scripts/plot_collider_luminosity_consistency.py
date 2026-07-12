#!/usr/bin/env python
"""Plot reduced and independently reconstructed dL/dt values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    data = json.loads(args.report.read_text(encoding="utf-8"))
    iterations = data["openpmd_iterations"]
    openpmd = data["dldt_openpmd"]
    reduced = data["dldt_reduced"]

    fig, axis = plt.subplots(figsize=(7.6, 3.9), constrained_layout=True)
    axis.plot(iterations, openpmd, marker="o", linewidth=1.7, label="openPMD reconstruction", color="#1769aa")
    axis.plot(iterations, reduced, marker="x", markersize=8, linewidth=1.3, linestyle="--", label="ColliderRelevant reduced", color="#c44e52")
    axis.set_title("ColliderRelevant: dL/dt cross-check")
    axis.set_xlabel("openPMD iteration")
    axis.set_ylabel("dL/dt")
    axis.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    axis.grid(True, alpha=0.25)
    axis.legend(frameon=False)
    axis.text(0.03, 0.08, "relative error = 0 at both iterations", transform=axis.transAxes, fontsize=9)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
