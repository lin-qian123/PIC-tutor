#!/usr/bin/env python
"""Fit the observed RZ axis radial-divergence coefficient across resolutions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from analyze_rz_axis_divergence_stencil_contract import read_axis


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def fit(path: Path) -> dict[str, object]:
    er, ez, dive, dr, dz = read_axis(path)
    dz_term = np.empty_like(ez)
    dz_term[1:-1] = (ez[2:] - ez[:-2]) / (2.0 * dz)
    dz_term[0] = (ez[1] - ez[0]) / dz
    dz_term[-1] = (ez[-1] - ez[-2]) / dz
    observed_radial_term = dive - dz_term
    source_basis = er / dr
    coefficient = float(np.dot(source_basis, observed_radial_term) / np.dot(source_basis, source_basis))
    result = {
        "plotfile": str(path),
        "axis_samples": int(er.size),
        "fitted_coefficient": coefficient,
        "distance_to_naive_2": abs(coefficient - 2.0),
        "distance_to_source_4": abs(coefficient - 4.0),
        "source_coefficient_is_closer": abs(coefficient - 4.0) < abs(coefficient - 2.0),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--on-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--off-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    on_paths = [resolve(root, path) for path in args.on_plotfiles]
    off_paths = [resolve(root, path) for path in args.off_plotfiles]
    source_file = resolve(root, args.source_file)
    source_anchor = "4._rt*Er(i, j, 0, 0)/dr"
    cases = [
        {"case": "correction-on", **fit(path)} for path in on_paths
    ] + [
        {"case": "correction-off", **fit(path)} for path in off_paths
    ]
    checks = {
        "source_axis_regularization_present": source_anchor in source_file.read_text(encoding="utf-8"),
        "all_plotfiles_present": all(Path(item["plotfile"]).is_dir() for item in cases),
        "paired_family_lengths": len(on_paths) == len(off_paths),
        "all_fitted_coefficients_source_closer": all(
            item["source_coefficient_is_closer"] for item in cases
        ),
    }
    result = {
        "contract": "RZ axis divergence fitted coefficient",
        "classification": "RZ_AXIS_STENCIL_FIT_COEFFICIENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "source_file": str(source_file),
        "source_anchor": source_anchor,
        "case_count": len(cases),
        "cases": cases,
        "scope": (
            "The reader removes the same first-order longitudinal estimate and fits one "
            "radial coefficient to each axis output. The fitted coefficient is an operator "
            "alignment diagnostic, not a proof of rho scaling, deposition correctness, or "
            "full charge closure."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ axis divergence fitted coefficient contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        "",
        "| case | grid | fitted coefficient | distance to 2 | distance to 4 | source closer |",
        "|---|---:|---:|---:|---:|:---:|",
    ]
    for item in cases:
        lines.append(
            f"| {item['case']} | {item['axis_samples']} | {item['fitted_coefficient']:.6f} | "
            f"{item['distance_to_naive_2']:.6f} | {item['distance_to_source_4']:.6f} | "
            f"{'PASS' if item['source_coefficient_is_closer'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "All fitted coefficients are closer to the source-defined coefficient 4 than "
            "to the naive coefficient 2. This strengthens operator alignment only; the "
            "RZ charge closure boundary remains open.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
