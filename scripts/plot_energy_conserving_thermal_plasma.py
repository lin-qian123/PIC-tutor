#!/usr/bin/env python
"""Plot the validated total-energy drift for the 1D/2D sibling cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_case(path: Path) -> tuple[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    run_dir = Path(data["run_dir"])
    label = "1D" if "_1d" in run_dir.name else "2D"
    return label, data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-1d", type=Path, required=True)
    parser.add_argument("--case-2d", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    cases = [load_case(args.case_1d), load_case(args.case_2d)]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1), constrained_layout=True)
    colors = {"1D": "#1769aa", "2D": "#c44e52"}

    for label, data in cases:
        samples = data["samples"]
        index = list(range(len(samples)))
        total = [sample["total_energy"] for sample in samples]
        drift = [sample["relative_drift"] for sample in samples]
        axes[0].plot(index, total, marker="o", linewidth=1.7, label=label, color=colors[label])
        axes[1].plot(index, drift, marker="o", linewidth=1.7, label=label, color=colors[label])

    axes[0].set_title("Total energy: EF + EP")
    axes[0].set_xlabel("Sample index")
    axes[0].set_ylabel("Total energy")
    axes[1].set_title("Relative total-energy drift")
    axes[1].set_xlabel("Sample index")
    axes[1].set_ylabel("Relative drift")
    axes[1].axhline(0.003, color="#333333", linestyle="--", linewidth=1.1, label="gate = 0.003")
    for axis in axes:
        axis.grid(True, alpha=0.25)
        axis.legend(frameon=False)

    fig.suptitle("Energy-conserving thermal plasma: validated 1D/2D siblings")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=180, bbox_inches="tight")
    print(f"[OK] Wrote {args.output}")


if __name__ == "__main__":
    main()
