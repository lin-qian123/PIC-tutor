#!/usr/bin/env python
"""Plot the validated BeamRelevant truncated-Gaussian contract."""

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
    import numpy as np

    data = json.loads(args.report.read_text(encoding="utf-8"))
    charge_ratio = data["observed_charge"] / data["expected_charge"]
    observed_rms = [*data["observed_transverse_rms"], data["observed_z_rms"]]
    expected_rms = [0.25, 0.25, data["expected_z_rms"]]

    fig, axes = plt.subplots(1, 2, figsize=(8.7, 3.9), constrained_layout=True)
    axes[0].bar([0], [charge_ratio], color="#1769aa", width=0.5)
    axes[0].axhline(1.0, color="#333333", linestyle="--", linewidth=1.1, label="expected")
    axes[0].set_xticks([0], ["total charge"])
    axes[0].set_ylabel("Observed / expected")
    axes[0].set_title("Truncated-Gaussian charge")
    axes[0].set_ylim(0.97, 1.03)
    axes[0].text(0, charge_ratio, f"{charge_ratio:.7f}", ha="center", va="bottom", fontsize=9)
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(frameon=False)

    x = np.arange(3)
    axes[1].bar(x - 0.17, observed_rms, 0.34, label="observed", color="#2171b5")
    axes[1].bar(x + 0.17, expected_rms, 0.34, label="expected", color="#9ecae1")
    axes[1].set_xticks(x, ["x rms", "y rms", "z rms"])
    axes[1].set_ylabel("RMS position (m)")
    axes[1].set_title("Position moments")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].legend(frameon=False)

    fig.suptitle("BeamRelevant: minimal 3D truncated-Gaussian contract")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
