#!/usr/bin/env python
"""Compare ParticleHistogram2D moments at matched physical time and resolution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries


SPECIES = ("PhaseSpaceIons", "PhaseSpaceElectrons")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-dir", required=True)
    parser.add_argument("--refined-dir", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument(
        "--study-label",
        default="matched-physical-time reader-side resolution sensitivity",
    )
    parser.add_argument("--allow-fail", action="store_true")
    args = parser.parse_args()

    baseline_root = Path(args.baseline_dir).resolve()
    refined_root = Path(args.refined_dir).resolve()
    baseline = _load_series(baseline_root)
    refined = _load_series(refined_root)
    comparisons = {}
    for name in SPECIES:
        b = _select_last_common_time(baseline[name], refined[name])
        r = _select_last_common_time(refined[name], baseline[name])
        comparisons[name] = {
            "baseline": b,
            "refined": r,
            "time_difference": float(abs(b["time"] - r["time"])),
            "relative_differences": {
                key: _relative_difference(b[key], r[key])
                for key in ("total_weight", "mean_z", "std_z", "mean_uz", "std_uz")
            },
            "absolute_differences": {
                key: float(abs(b[key] - r[key]))
                for key in ("mean_z", "mean_uz")
            },
        }

    finite_gate = all(
        entry["baseline"]["finite"]
        and entry["refined"]["finite"]
        and entry["baseline"]["total_weight"] > 0
        and entry["refined"]["total_weight"] > 0
        for entry in comparisons.values()
    )
    stability_gate = all(
        entry["relative_differences"]["total_weight"] < 1.0e-3
        and entry["relative_differences"]["std_z"] < 1.0e-2
        and entry["relative_differences"]["std_uz"] < 5.0e-2
        for entry in comparisons.values()
    )
    result = {
        "baseline_dir": str(baseline_root),
        "refined_dir": str(refined_root),
        "series": comparisons,
        "gates": {
            "finite_positive": finite_gate,
            "weighted_width_stability": stability_gate,
            "thresholds": {
                "total_weight_relative_difference": 1.0e-3,
                "std_z_relative_difference": 1.0e-2,
                "std_uz_relative_difference": 5.0e-2,
            },
        },
        "passed": finite_gate and stability_gate,
        "contract": f"{args.study_label}; not a formal physical convergence proof",
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(_markdown(result, args.study_label))
    print(json.dumps(result, indent=2))
    if not result["passed"] and not args.allow_fail:
        raise SystemExit("ParticleHistogram2D resolution comparison failed")


def _load_series(root: Path) -> dict[str, dict]:
    result = {}
    for name in SPECIES:
        series = OpenPMDTimeSeries(str(root / "diags/reducedfiles" / name))
        entries = []
        for iteration, time in zip(series.iterations, series.t):
            data, info = series.get_field("data", iteration=int(iteration))
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
            entries.append(
                {
                    "iteration": int(iteration),
                    "time": float(time),
                    "total_weight": total,
                    "mean_z": mean_z,
                    "std_z": std_z,
                    "mean_uz": mean_uz,
                    "std_uz": std_uz,
                    "nonzero_cells": int(np.count_nonzero(weights)),
                    "finite": finite,
                }
            )
        result[name] = entries
    return result


def _select_last_common_time(entries: list[dict], other: list[dict]) -> dict:
    target = float(other[-1]["time"])
    return min(entries, key=lambda entry: abs(entry["time"] - target))


def _relative_difference(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1.0e-300)
    return float(abs(left - right) / scale)


def _markdown(result: dict, study_label: str) -> str:
    lines = [
        "# ParticleHistogram2D sensitivity report",
        "",
        f"- comparison: {study_label}",
        "- scope: reader-side weighted-moment sensitivity; this is not a formal physical convergence proof",
        "- stability gate: relative differences below `1e-3` for total weight, `1e-2` for `std(z)`, and `5e-2` for `std(uz)`",
        f"- contract: `{'PASS' if result['passed'] else 'FAIL'}`",
        "",
        "| Series | baseline iteration/time | refined iteration/time | rel. d(total weight) | rel. d(std(z)) | rel. d(std(uz)) | abs. d(mean z) | abs. d(mean uz) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name in SPECIES:
        entry = result["series"][name]
        b = entry["baseline"]
        r = entry["refined"]
        d = entry["relative_differences"]
        lines.append(
            f"| {name} | {b['iteration']} / {b['time']:.9e} | {r['iteration']} / {r['time']:.9e} | "
            f"{d['total_weight']:.6e} | {d['std_z']:.6e} | {d['std_uz']:.6e} | "
            f"{entry['absolute_differences']['mean_z']:.6e} | {entry['absolute_differences']['mean_uz']:.6e} |"
        )
    lines.extend(
        [
            "",
            f"The comparison tests {study_label}. It does not establish a formal physical convergence rate, because the particle count and stochastic sampling are not independently controlled here.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
