#!/usr/bin/env python
"""Plot the uniform-plasma 1-rank/2-rank consistency boundary."""

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
    import numpy as np

    report = json.loads(args.comparison.read_text(encoding="utf-8"))
    single = report["single_rank_invariants"]
    multi = report["multi_rank_invariants"]
    labels = ["field energy", "particle kinetic", "total energy"]
    keys = ["field_energy", "particle_kinetic_energy", "total_energy"]
    ratios = [multi[key] / single[key] for key in keys]

    groups = {"B": ("Bx", "By", "Bz"), "E": ("Ex", "Ey", "Ez"), "J": ("jx", "jy", "jz"), "rho": ("rho",)}
    field_errors = {
        field["field"][1]: field["l2_relative_error"]
        for field in report["fields"]
        if field["comparison"] == "physical-field"
    }
    group_labels = list(groups)
    group_errors = [max(field_errors[name] for name in names) for names in groups.values()]

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.9), constrained_layout=True)
    axes[0].bar(range(len(labels)), ratios, color=["#4c78a8", "#59a14f", "#f28e2b"], width=0.58)
    axes[0].axhline(1.0, color="#333333", linestyle="--", linewidth=1.0, label="1-rank reference")
    axes[0].set_xticks(range(len(labels)), labels, rotation=20, ha="right")
    axes[0].set_ylabel("2-rank / 1-rank invariant")
    axes[0].set_title("Global invariants")
    axes[0].set_ylim(0.98, 1.025)
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(frameon=False, fontsize=8)
    for index, value in enumerate(ratios):
        axes[0].text(index, value + 0.001, f"{value:.5f}", ha="center", va="bottom", fontsize=8)

    axes[1].bar(group_labels, group_errors, color="#c44e52", width=0.58)
    axes[1].axhline(1.0e-12, color="#333333", linestyle="--", linewidth=1.0, label="machine-level gate")
    axes[1].set_yscale("log")
    axes[1].set_ylabel("max physical-field L2 relative error")
    axes[1].set_title("Field rank dependence")
    axes[1].grid(axis="y", which="both", alpha=0.2)
    axes[1].legend(frameon=False, fontsize=8)
    for index, value in enumerate(group_errors):
        axes[1].text(index, value * 1.15, f"{value:.3f}", ha="center", va="bottom", fontsize=8)

    fig.suptitle("Uniform plasma: MPI layout consistency boundary", fontsize=12)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=220, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
