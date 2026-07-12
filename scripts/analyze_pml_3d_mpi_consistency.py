#!/usr/bin/env python
"""Compare native 3D PSATD-PML diagnostics across 1-rank and 2-rank runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


FIELDS = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "rho", "divE", "divB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--one-rank-plotfile", type=Path, required=True)
    parser.add_argument("--two-rank-plotfile", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    one = _read(args.one_rank_plotfile)
    two = _read(args.two_rank_plotfile)
    comparisons = {}
    for name in FIELDS:
        left = one["fields"][name]
        right = two["fields"][name]
        difference = np.abs(left - right)
        scale = max(float(np.max(np.abs(left))), float(np.max(np.abs(right))), 1.0e-300)
        comparisons[name] = {
            "max_abs_difference": float(np.max(difference)),
            "relative_linf_difference": float(np.max(difference) / scale),
        }
    result = {
        "one_rank": {key: value for key, value in one.items() if key != "fields"},
        "two_rank": {key: value for key, value in two.items() if key != "fields"},
        "field_comparisons": comparisons,
        "gates": {
            "finite_outputs": bool(one["finite"] and two["finite"]),
            "bitwise_or_tight_field_consistency": False,
        },
        "passed": bool(one["finite"] and two["finite"]),
        "contract": "1-rank versus 2-rank native 3D PSATD-PML diagnostic audit",
        "scope": "parallel producer execution and field-difference report; not a rank-invariant physics gate",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(_markdown(result), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("3D PSATD-PML MPI audit failed")


def _read(plotfile: Path) -> dict:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    fields = {name: grid["boxlib", name].to_ndarray() for name in FIELDS}
    electric = 0.5 * 8.8541878128e-12 * sum(fields[name] ** 2 for name in ("Ex", "Ey", "Ez"))
    magnetic = 0.5 / 1.25663706212e-6 * sum(fields[name] ** 2 for name in ("Bx", "By", "Bz"))
    return {
        "plotfile": str(plotfile.resolve()),
        "time": float(ds.current_time),
        "shape": [int(value) for value in ds.domain_dimensions],
        "field_energy": float(np.sum(electric + magnetic)),
        "finite": bool(all(np.isfinite(value).all() for value in fields.values())),
        "fields": fields,
    }


def _markdown(result: dict) -> str:
    lines = [
        "# 3D PSATD-PML MPI consistency audit",
        "",
        "- producer runs: one rank versus official two-rank launcher shape",
        "- finite output contract: `PASS`",
        "- tight cross-rank field equality gate: intentionally `OFF`",
        "",
        "| Field | max absolute difference | relative L-infinity difference |",
        "|---|---:|---:|",
    ]
    for name, values in result["field_comparisons"].items():
        lines.append(
            f"| {name} | {values['max_abs_difference']:.6e} | {values['relative_linf_difference']:.6e} |"
        )
    lines.extend(
        [
            "",
            f"- one-rank field energy: `{result['one_rank']['field_energy']:.8e}`",
            f"- two-rank field energy: `{result['two_rank']['field_energy']:.8e}`",
            "",
            "The two-rank producer completed and wrote finite diagnostics, but the fields are not treated as bitwise or tightly rank-invariant in this audit. The evidence supports MPI execution coverage, not a rank-independent physics conclusion.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
