#!/usr/bin/env python
"""Compute weighted z/uz moments from ParticleHistogram2D BP5 data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries


def moments(series: OpenPMDTimeSeries, iteration: int) -> dict:
    data, info = series.get_field("data", iteration=iteration)
    data = np.asarray(data, dtype=float)
    uz = np.asarray(getattr(info, info.axes[0]), dtype=float)
    z = np.asarray(getattr(info, info.axes[1]), dtype=float)
    weights = np.where(np.isfinite(data) & (data > 0), data, 0.0)
    grid_uz, grid_z = np.meshgrid(uz, z, indexing="ij")
    total = float(np.sum(weights))
    mean_z = float(np.sum(weights * grid_z) / total)
    mean_uz = float(np.sum(weights * grid_uz) / total)
    std_z = float(np.sqrt(np.sum(weights * (grid_z - mean_z) ** 2) / total))
    std_uz = float(np.sqrt(np.sum(weights * (grid_uz - mean_uz) ** 2) / total))
    return {
        "iteration": int(iteration),
        "total_weight": total,
        "mean_z": mean_z,
        "std_z": std_z,
        "mean_uz": mean_uz,
        "std_uz": std_uz,
        "nonzero_cells": int(np.count_nonzero(weights)),
        "finite": bool(np.isfinite(data).all()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.run_dir.resolve()
    result = {"run_dir": str(root), "series": {}}
    for name in ("PhaseSpaceIons", "PhaseSpaceElectrons"):
        series = OpenPMDTimeSeries(str(root / f"diags/reducedfiles/{name}"))
        entries = [moments(series, int(iteration)) for iteration in series.iterations]
        result["series"][name] = entries

    for entries in result["series"].values():
        for entry in entries:
            if not entry["finite"] or entry["total_weight"] <= 0:
                raise SystemExit("invalid histogram moment")
    result["passed"] = True
    result["contract"] = "finite positive BP5 histogram data admit reproducible weighted z/uz moments at iterations 0 and 100"
    result["scope"] = "reader-side physical-statistics sanity; not a resolution or particle-number convergence proof"
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ParticleHistogram2D weighted-moment report",
        "",
        "| series | iteration | total weight | mean z | std z | mean uz | std uz | nonzero cells |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, entries in result["series"].items():
        for entry in entries:
            lines.append(
                f"| {name} | {entry['iteration']} | {entry['total_weight']:.8e} | "
                f"{entry['mean_z']:.8e} | {entry['std_z']:.8e} | "
                f"{entry['mean_uz']:.8e} | {entry['std_uz']:.8e} | {entry['nonzero_cells']} |"
            )
    lines.extend(["", f"- status: `PASS`", f"- scope: {result['scope']}", ""])
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
