#!/usr/bin/env python
"""Compare RZ axis rho output ratios with the source volume-factor prediction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def read_axis_and_off_axis(plotfile: Path, field: str) -> tuple[np.ndarray, np.ndarray]:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(
        level=ds.max_level,
        left_edge=ds.domain_left_edge,
        dims=ds.domain_dimensions,
    )
    values = grid["boxlib", field].to_ndarray()[:, :, 0]
    return values[0, :], values[1:, :]


def pair_metrics(on_plotfile: Path, off_plotfile: Path) -> dict[str, object]:
    field_metrics = {}
    for field in ("rho_electrons", "rho_ions"):
        on_axis, on_off_axis = read_axis_and_off_axis(on_plotfile, field)
        off_axis, off_off_axis = read_axis_and_off_axis(off_plotfile, field)
        axis_mask = np.abs(off_axis) > 1.0e-30
        off_mask = (np.abs(off_off_axis) > 1.0e-30) & np.isfinite(on_off_axis) & np.isfinite(off_off_axis)
        axis_ratio = on_axis[axis_mask] / off_axis[axis_mask]
        off_ratio = on_off_axis[off_mask] / off_off_axis[off_mask]
        field_metrics[field] = {
            "axis_ratio_median": float(np.median(axis_ratio)),
            "axis_ratio_min": float(np.min(axis_ratio)),
            "axis_ratio_max": float(np.max(axis_ratio)),
            "off_axis_ratio_max_abs_deviation": float(np.max(np.abs(off_ratio - 1.0))),
            "axis_samples": int(axis_ratio.size),
            "off_axis_samples": int(off_ratio.size),
        }
    return {
        "on_plotfile": str(on_plotfile),
        "off_plotfile": str(off_plotfile),
        "fields": field_metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--on-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--off-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--on-input", type=Path, required=True)
    parser.add_argument("--off-input", type=Path, required=True)
    parser.add_argument("--source-files", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    on_paths = [resolve(root, path) for path in args.on_plotfiles]
    off_paths = [resolve(root, path) for path in args.off_plotfiles]
    on_input = resolve(root, args.on_input)
    off_input = resolve(root, args.off_input)
    source_files = [resolve(root, path) for path in args.source_files]
    pairs = [pair_metrics(on, off) for on, off in zip(on_paths, off_paths)]
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    predicted_axis_ratio = (1.0 / 4.0) / (1.0 / 3.0)
    all_fields = [pair["fields"][field] for pair in pairs for field in ("rho_electrons", "rho_ions")]
    checks = {
        "source_query_present": 'query("verboncoeur_axis_correction", m_verboncoeur_axis_correction)' in source,
        "source_axis_scaling_present": "1.0_rt/3.0_rt" in source and "1.0_rt/4.0_rt" in source,
        "source_rho_scaling_function_present": "ApplyInverseVolumeScalingToChargeDensity" in source,
        "on_input_uses_default_true": "boundary.verboncoeur_axis_correction" not in on_input.read_text(encoding="utf-8"),
        "off_input_disables_correction": "boundary.verboncoeur_axis_correction = false" in off_input.read_text(encoding="utf-8"),
        "paired_family_lengths": len(on_paths) == len(off_paths),
        "all_plotfiles_present": all(path.is_dir() for path in on_paths + off_paths),
        "off_axis_control_matches": all(item["off_axis_ratio_max_abs_deviation"] <= 1.0e-12 for item in all_fields),
        "axis_ratio_stable": all(abs(item["axis_ratio_median"] - 0.85) <= 1.0e-12 for item in all_fields),
        "axis_ratio_differs_from_pure_volume_prediction": all(
            abs(item["axis_ratio_median"] - predicted_axis_ratio) > 1.0e-3 for item in all_fields
        ),
    }
    result = {
        "contract": "RZ rho axis correction ratio boundary",
        "classification": "RZ_RHO_AXIS_CORRECTION_RATIO_MISMATCH_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "source_files": [str(path) for path in source_files],
        "predicted_axis_ratio_from_volume_factors": predicted_axis_ratio,
        "case_count": len(pairs),
        "pairs": pairs,
        "scope": (
            "Identical correction-on/off inputs produce an off-axis rho control ratio of one, "
            "while the initial axis species-rho ratio is 0.85 rather than the 0.75 ratio from "
            "the source 1/3 and 1/4 axis volume factors alone. This isolates an additional "
            "axis/deposition/diagnostic boundary; it does not identify its root cause or close charge."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ rho axis correction ratio contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- pure volume-factor predicted axis ratio: `{predicted_axis_ratio:.6f}`",
        "",
        "| correction | grid | field | axis on/off ratio | off-axis max deviation |",
        "|---|---:|---|---:|---:|",
    ]
    for pair in pairs:
        grid = pair["fields"]["rho_electrons"]["axis_samples"]
        grid_label = f"{grid // 2}x{grid}"
        for field in ("rho_electrons", "rho_ions"):
            item = pair["fields"][field]
            lines.append(
                f"| on/off pair | {grid_label} | {field} | {item['axis_ratio_median']:.6f} | "
                f"{item['off_axis_ratio_max_abs_deviation']:.3e} |"
            )
    lines.extend(
        [
            "",
            "The off-axis control is unchanged while the axis ratio is stably 0.85, "
            "which differs from the pure 1/3-versus-1/4 volume-factor prediction 0.75. "
            "This is a boundary diagnostic, not a charge-closure pass or kernel root-cause proof.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
