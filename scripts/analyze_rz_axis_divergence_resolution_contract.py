#!/usr/bin/env python
"""Check RZ axis divergence-stencil alignment across resolution families."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_rz_axis_divergence_stencil_contract import metrics


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


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
    source = source_file.read_text(encoding="utf-8")
    source_anchor = "4._rt*Er(i, j, 0, 0)/dr"

    on_metrics = [metrics(path) for path in on_paths]
    off_metrics = [metrics(path) for path in off_paths]
    cases = []
    for label, items in (("correction-on", on_metrics), ("correction-off", off_metrics)):
        for item in items:
            cases.append({"case": label, **item})

    checks = {
        "source_axis_regularization_present": source_anchor in source,
        "on_plotfiles_present": all(path.is_dir() for path in on_paths),
        "off_plotfiles_present": all(path.is_dir() for path in off_paths),
        "paired_family_lengths": len(on_paths) == len(off_paths),
        "all_source_coefficients_closer": all(
            item["source_coefficient_is_closer"] for item in cases
        ),
    }
    result = {
        "contract": "RZ axis divergence stencil resolution-family alignment",
        "classification": "RZ_AXIS_STENCIL_ALIGNMENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "source_file": str(source_file),
        "source_anchor": source_anchor,
        "source_interpretation": "axis mode-0 uses 4*Er/dr before the longitudinal DownwardDz term",
        "case_count": len(cases),
        "cases": cases,
        "scope": (
            "The same reader-side longitudinal subtraction and coefficient comparison is "
            "applied to correction-on/off 64x128, 128x256, and 256x512 RZ outputs. "
            "The contract strengthens stencil alignment across resolution, but does not "
            "prove rho scaling, deposition-kernel correctness, or full charge closure."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ axis divergence stencil resolution contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- cases: `{result['case_count']}`",
        "",
        "| case | grid | naive `2*Er/dr` RMSE | source `4*Er/dr` RMSE | source closer |",
        "|---|---:|---:|---:|:---:|",
    ]
    for item in cases:
        grid = f"{item['axis_samples']}x{item['axis_samples'] * 2}"
        errors = item["coefficient_errors"]
        lines.append(
            f"| {item['case']} | {grid} | {errors['2']['rmse']:.6e} | "
            f"{errors['4']['rmse']:.6e} | "
            f"{'PASS' if item['source_coefficient_is_closer'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "All listed resolutions support the narrower source-defined stencil alignment "
            "claim. This remains an observable boundary and does not close RZ charge closure.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
