#!/usr/bin/env python
"""Compare the source-defined RZ axis divergence coefficient with a naive one."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


def read_axis(plotfile: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(
        level=ds.max_level,
        left_edge=ds.domain_left_edge,
        dims=ds.domain_dimensions,
    )
    er = grid["boxlib", "Er"].to_ndarray()[0, :, 0]
    ez = grid["boxlib", "Ez"].to_ndarray()[0, :, 0]
    dive = grid["boxlib", "divE"].to_ndarray()[0, :, 0]
    dr = float(ds.domain_width[0] / ds.domain_dimensions[0])
    dz = float(ds.domain_width[1] / ds.domain_dimensions[1])
    return er, ez, dive, dr, dz


def metrics(plotfile: Path) -> dict[str, float | int | str]:
    er, ez, dive, dr, dz = read_axis(plotfile)
    dz_term = np.empty_like(ez)
    dz_term[1:-1] = (ez[2:] - ez[:-2]) / (2.0 * dz)
    dz_term[0] = (ez[1] - ez[0]) / dz
    dz_term[-1] = (ez[-1] - ez[-2]) / dz
    observed_radial_term = dive - dz_term
    result: dict[str, float | int | str] = {
        "plotfile": str(plotfile),
        "axis_samples": int(er.size),
        "dr": dr,
        "dz": dz,
    }
    errors = {}
    for coefficient in (2.0, 4.0):
        residual = observed_radial_term - coefficient * er / dr
        errors[str(int(coefficient))] = {
            "linf": float(np.max(np.abs(residual))),
            "rmse": float(np.sqrt(np.mean(residual**2))),
            "relative_linf_to_observed_radial_term": float(
                np.max(np.abs(residual)) / max(np.max(np.abs(observed_radial_term)), 1.0e-300)
            ),
        }
    result["coefficient_errors"] = errors  # type: ignore[assignment]
    result["source_coefficient_is_closer"] = errors["4"]["rmse"] < errors["2"]["rmse"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--on-plotfile", type=Path, required=True)
    parser.add_argument("--off-plotfile", type=Path, required=True)
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    source_file = args.source_file if args.source_file.is_absolute() else root / args.source_file
    source = source_file.read_text(encoding="utf-8")
    source_anchor = "4._rt*Er(i, j, 0, 0)/dr"
    on = args.on_plotfile if args.on_plotfile.is_absolute() else root / args.on_plotfile
    off = args.off_plotfile if args.off_plotfile.is_absolute() else root / args.off_plotfile
    on_metrics = metrics(on)
    off_metrics = metrics(off)
    checks = {
        "source_axis_regularization_present": source_anchor in source,
        "on_plotfile_present": on.is_dir(),
        "off_plotfile_present": off.is_dir(),
        "on_source_coefficient_closer": on_metrics["source_coefficient_is_closer"],
        "off_source_coefficient_closer": off_metrics["source_coefficient_is_closer"],
    }
    result = {
        "contract": "RZ axis divergence stencil alignment",
        "classification": "RZ_AXIS_STENCIL_ALIGNMENT_OBSERVED_CHARGE_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "source_file": str(source_file),
        "source_anchor": source_anchor,
        "source_interpretation": "axis mode-0 uses 4*Er/dr before the longitudinal DownwardDz term",
        "on": on_metrics,
        "off": off_metrics,
        "scope": (
            "The independent reader removes the same first-order longitudinal estimate from "
            "the axis divE output and compares the source-defined 4*Er/dr term with a naive "
            "2*Er/dr term. The test localizes a stencil-coefficient boundary; it does not "
            "prove rho scaling, deposition-kernel correctness, or full charge closure."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ axis divergence stencil alignment contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        "- source axis coefficient: `4*Er/dr`",
        "",
        "| case | naive `2*Er/dr` RMSE | source `4*Er/dr` RMSE | source coefficient closer |",
        "|---|---:|---:|:---:|",
    ]
    for label, item in (("correction-on", on_metrics), ("correction-off", off_metrics)):
        errors = item["coefficient_errors"]
        lines.append(
            f"| {label} | {errors['2']['rmse']:.6e} | {errors['4']['rmse']:.6e} | "
            f"{'PASS' if item['source_coefficient_is_closer'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "The result supports the narrower claim that the source-defined axis coefficient "
            "is better aligned with the emitted `divE` than the naive coefficient under this "
            "reader approximation. It does not close the RZ charge residual boundary.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
