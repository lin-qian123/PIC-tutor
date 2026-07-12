#!/usr/bin/env python
"""Summarize ParticleHistogram2D sensitivity across particles-per-cell runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries


SPECIES = ("PhaseSpaceIons", "PhaseSpaceElectrons")
THRESHOLDS = {"total_weight": 1.0e-3, "std_z": 1.0e-2, "std_uz": 5.0e-2}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        action="append",
        required=True,
        help="label=run-directory; provide at least two runs in increasing particle count",
    )
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    runs = [_parse_run(value) for value in args.run]
    moments = {label: _load_run(root) for label, root in runs}
    pairwise = []
    for (left_label, _), (right_label, _) in zip(runs, runs[1:]):
        pairwise.append(_compare_pair(left_label, right_label, moments))
    result = {
        "runs": {label: str(root) for label, root in runs},
        "moments": moments,
        "pairwise": pairwise,
        "gates": {
            "finite_positive": all(
                entry["finite"] and entry["total_weight"] > 0
                for run in moments.values()
                for entry in run.values()
            ),
            "thresholds": THRESHOLDS,
        },
        "passed": all(
            entry["finite_positive"] for pair in pairwise for entry in pair["series"].values()
        ),
        "contract": "pairwise matched-time particle-number sensitivity; not a formal convergence-order proof",
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(_markdown(result))
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("ParticleHistogram2D particle-count report failed")


def _parse_run(value: str) -> tuple[str, Path]:
    label, separator, raw_path = value.partition("=")
    if not separator or not label or not raw_path:
        raise SystemExit(f"invalid --run value: {value!r}")
    return label, Path(raw_path).resolve()


def _load_run(root: Path) -> dict[str, dict]:
    result = {}
    for name in SPECIES:
        series = OpenPMDTimeSeries(str(root / "diags/reducedfiles" / name))
        # All cases are configured for the same output interval; use the final frame.
        iteration = int(series.iterations[-1])
        data, info = series.get_field("data", iteration=iteration)
        weights = np.asarray(data, dtype=float)
        z = np.asarray(info.z, dtype=float)
        uz = np.asarray(info.uz, dtype=float)
        zz, uu = np.meshgrid(z, uz)
        finite = bool(np.isfinite(weights).all())
        total = float(np.sum(weights))
        if finite and total > 0:
            mean_z = float(np.sum(weights * zz) / total)
            mean_uz = float(np.sum(weights * uu) / total)
            std_z = float(np.sqrt(np.sum(weights * (zz - mean_z) ** 2) / total))
            std_uz = float(np.sqrt(np.sum(weights * (uu - mean_uz) ** 2) / total))
        else:
            mean_z = mean_uz = std_z = std_uz = float("nan")
        result[name] = {
            "iteration": iteration,
            "time": float(series.t[-1]),
            "total_weight": total,
            "mean_z": mean_z,
            "std_z": std_z,
            "mean_uz": mean_uz,
            "std_uz": std_uz,
            "nonzero_cells": int(np.count_nonzero(weights)),
            "finite": finite,
        }
    return result


def _compare_pair(left: str, right: str, moments: dict) -> dict:
    series = {}
    for name in SPECIES:
        a = moments[left][name]
        b = moments[right][name]
        relative = {
            key: _relative_difference(a[key], b[key])
            for key in ("total_weight", "std_z", "std_uz")
        }
        series[name] = {
            "time_difference": float(abs(a["time"] - b["time"])),
            "relative_differences": relative,
            "absolute_mean_differences": {
                key: float(abs(a[key] - b[key])) for key in ("mean_z", "mean_uz")
            },
            "finite_positive": bool(
                a["finite"] and b["finite"] and a["total_weight"] > 0 and b["total_weight"] > 0
            ),
            "weighted_width_stability": all(
                relative[key] < threshold for key, threshold in THRESHOLDS.items()
            ),
        }
    return {"left": left, "right": right, "series": series}


def _relative_difference(left: float, right: float) -> float:
    return float(abs(left - right) / max(abs(left), abs(right), 1.0e-300))


def _markdown(result: dict) -> str:
    lines = [
        "# ParticleHistogram2D particle-count sensitivity report",
        "",
        "- scope: matched-time reader-side weighted-moment sensitivity",
        "- thresholds: total weight `<1e-3`, `std(z)` `<1e-2`, `std(uz)` `<5e-2`",
        "- this report does not claim a formal physical convergence order",
        f"- finite-data contract: `{'PASS' if result['passed'] else 'FAIL'}`",
        "",
        "| Pair | Series | time diff | rel. d(total) | rel. d(std z) | rel. d(std uz) | stability |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for pair in result["pairwise"]:
        for name, entry in pair["series"].items():
            d = entry["relative_differences"]
            lines.append(
                f"| {pair['left']} -> {pair['right']} | {name} | {entry['time_difference']:.3e} | "
                f"{d['total_weight']:.6e} | {d['std_z']:.6e} | {d['std_uz']:.6e} | "
                f"{'PASS' if entry['weighted_width_stability'] else 'FAIL'} |"
            )
    lines.extend(
        [
            "",
            "The pairwise result is an evidence boundary: higher particle count can reduce sampling sensitivity in selected moments, but three deterministic runs do not establish a physical convergence rate or an upstream regression gate.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
