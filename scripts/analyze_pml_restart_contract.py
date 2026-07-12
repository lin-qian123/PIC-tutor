#!/usr/bin/env python
"""Independently compare a PML restart plotfile with its baseline sibling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--restart", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    baseline = yt.load(str(args.baseline))
    restart = yt.load(str(args.restart))
    if baseline.domain_dimensions.tolist() != restart.domain_dimensions.tolist():
        raise SystemExit("baseline/restart domain dimensions differ")

    baseline_grid = baseline.covering_grid(
        level=0, left_edge=baseline.domain_left_edge, dims=baseline.domain_dimensions
    )
    restart_grid = restart.covering_grid(
        level=0, left_edge=restart.domain_left_edge, dims=restart.domain_dimensions
    )
    fields = sorted(set(baseline.field_list) & set(restart.field_list))
    errors = {}
    for field in fields:
        reference = baseline_grid[field].to_ndarray()
        candidate = restart_grid[field].to_ndarray()
        if reference.shape != candidate.shape:
            raise SystemExit(f"field shape differs: {field}")
        absolute = float(np.max(np.abs(candidate - reference)))
        scale = max(float(np.max(np.abs(reference))), 1.0e-300)
        errors[str(field)] = {
            "max_absolute_error": absolute,
            "max_relative_error": absolute / scale,
        }

    max_absolute = max(item["max_absolute_error"] for item in errors.values())
    max_relative = max(item["max_relative_error"] for item in errors.values())
    result = {
        "baseline": str(args.baseline),
        "restart": str(args.restart),
        "fields_compared": len(errors),
        "field_errors": errors,
        "max_absolute_error": max_absolute,
        "max_relative_error": max_relative,
        "tolerance": 1.0e-12,
        "passed": bool(np.isfinite(max_absolute) and np.isfinite(max_relative) and max_relative < 1.0e-12),
        "contract": "Cartesian PSATD-PML restart field reproducibility",
        "scope": "2-rank project-level independent reader-side comparison; official analysis separately rerun",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# Cartesian PSATD-PML restart contract\n\n"
        f"- fields compared: `{len(errors)}`\n"
        f"- maximum absolute error: `{max_absolute:.8e}`\n"
        f"- maximum relative error: `{max_relative:.8e}`\n"
        "- gate: maximum relative error `<1e-12`\n"
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("Cartesian PSATD-PML restart contract failed")


if __name__ == "__main__":
    main()
