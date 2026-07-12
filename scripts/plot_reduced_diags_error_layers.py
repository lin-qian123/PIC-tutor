#!/usr/bin/env python
"""Plot the two error scales in the reduced-diagnostics contract."""

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
    comparisons = data["comparisons"]
    non_field = [
        item["relative_error"]
        for item in comparisons
        if item["observable"] != "field energy"
    ]
    field_energy = data["field_energy_relative_error"]
    non_field.sort()

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.1), constrained_layout=True)
    axes[0].plot(range(1, len(non_field) + 1), non_field, color="#1769aa", marker=".", linewidth=1)
    axes[0].axhline(data["other_observable_tolerance"], color="#333333", linestyle="--", linewidth=1.1)
    axes[0].set_yscale("log")
    axes[0].set_title("59 non-field-energy observables")
    axes[0].set_xlabel("Observable rank after sorting")
    axes[0].set_ylabel("Relative error")
    axes[0].text(
        0.04,
        0.93,
        f"max = {data['max_non_field_energy_relative_error']:.3e}\ngate = 1e-12",
        transform=axes[0].transAxes,
        va="top",
        fontsize=9,
    )
    axes[0].grid(True, which="both", alpha=0.2)

    axes[1].bar([0], [field_energy], color="#c44e52", width=0.5)
    axes[1].axhline(data["field_energy_tolerance"], color="#333333", linestyle="--", linewidth=1.1)
    axes[1].set_xticks([0], ["field\nenergy"])
    axes[1].set_ylabel("Relative error")
    axes[1].set_title("Staggered field-energy special case")
    axes[1].set_ylim(0, 0.34)
    axes[1].text(0, field_energy, f"{field_energy:.4f}", ha="center", va="bottom", fontsize=9)
    axes[1].text(0.04, 0.93, "gate = 0.3", transform=axes[1].transAxes, va="top", fontsize=9)
    axes[1].grid(axis="y", alpha=0.25)

    fig.suptitle("Reduced diagnostics vs full-state reference: error layers")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
