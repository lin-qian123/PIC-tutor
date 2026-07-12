#!/usr/bin/env python
"""Independently summarize Cartesian and RZ PSATD-PML absorption contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import epsilon_0, mu_0


def field_energy(plotfile: Path) -> float:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    fields = {name: grid["boxlib", name].to_ndarray() for name in ("Ex", "Ey", "Ez", "Bx", "By", "Bz")}
    electric = 0.5 * epsilon_0 * sum(fields[name] ** 2 for name in ("Ex", "Ey", "Ez"))
    magnetic = 0.5 / mu_0 * sum(fields[name] ** 2 for name in ("Bx", "By", "Bz"))
    return float(np.sum(electric + magnetic))


def rz_max_field(plotfile: Path) -> dict[str, float]:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    return {
        "max_abs_Er": float(np.max(np.abs(grid["boxlib", "Er"].to_ndarray()))),
        "max_abs_Ez": float(np.max(np.abs(grid["boxlib", "Ez"].to_ndarray()))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cartesian-initial", type=Path, required=True)
    parser.add_argument("--cartesian-final", type=Path, required=True)
    parser.add_argument("--rz-final", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    cartesian_initial = field_energy(args.cartesian_initial)
    cartesian_final = field_energy(args.cartesian_final)
    expected_initial = 7.282940112203595e-08
    initial_reference_error = abs(cartesian_initial - expected_initial) / expected_initial
    reflectivity = cartesian_final / cartesian_initial
    rz = rz_max_field(args.rz_final)
    rz_max = max(rz.values())
    result = {
        "cartesian_initial_energy": cartesian_initial,
        "cartesian_expected_initial_energy": expected_initial,
        "cartesian_initial_reference_relative_error": initial_reference_error,
        "cartesian_final_energy": cartesian_final,
        "cartesian_reflectivity": reflectivity,
        "cartesian_initial_reference_tolerance": 1.0e-14,
        "cartesian_reflectivity_tolerance": 1.0e-6,
        "rz_final_field": rz,
        "rz_max_abs_field": rz_max,
        "rz_field_tolerance": 2.0,
        "cartesian_passed": bool(initial_reference_error < 1.0e-14 and reflectivity < 1.0e-6),
        "rz_passed": bool(rz_max < 2.0),
        "passed": bool(initial_reference_error < 1.0e-14 and reflectivity < 1.0e-6 and rz_max < 2.0),
        "contract": "Cartesian PSATD-PML low reflectivity plus RZ radial-PML residual-field decay",
        "scope": "official WarpX inputs, project-level independent reader-side summary, one rank",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# PSATD-PML contract\n\n"
        f"- status: `{status}`\n"
        f"- Cartesian initial reference relative error: `{initial_reference_error:.8e}`\n"
        f"- Cartesian reflectivity: `{reflectivity:.8e}`\n"
        f"- RZ max |Er|: `{rz['max_abs_Er']:.8e}`\n"
        f"- RZ max |Ez|: `{rz['max_abs_Ez']:.8e}`\n"
        f"- RZ max field: `{rz_max:.8e}`\n"
        "- contracts: Cartesian reflectivity `< 1e-6`; RZ residual field `< 2`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("PSATD-PML contract failed")


if __name__ == "__main__":
    main()
