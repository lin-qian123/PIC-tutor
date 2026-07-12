#!/usr/bin/env python
"""Independently summarize a Cartesian PSATD-PML initial/final pair."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import epsilon_0, mu_0


EXPECTED_INITIAL_ENERGY = 7.282940112203595e-08


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    initial = _field_energy(args.initial)
    final = _field_energy(args.final)
    reference_error = abs(initial - EXPECTED_INITIAL_ENERGY) / EXPECTED_INITIAL_ENERGY
    reflectivity = final / initial
    result = {
        "initial_energy": initial,
        "expected_initial_energy": EXPECTED_INITIAL_ENERGY,
        "initial_reference_relative_error": reference_error,
        "final_energy": final,
        "reflectivity": reflectivity,
        "initial_reference_tolerance": 1.0e-14,
        "reflectivity_tolerance": 1.0e-6,
        "passed": bool(reference_error < 1.0e-14 and reflectivity < 1.0e-6),
        "contract": "Cartesian PSATD-PML initial-energy and low-reflectivity contract",
        "scope": "2-rank project-level independent reader-side summary; official analysis separately rerun",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# Cartesian PSATD-PML contract\n\n"
        f"- initial reference relative error: `{reference_error:.8e}`\n"
        f"- reflectivity: `{reflectivity:.8e}`\n"
        "- gates: initial error `<1e-14`; reflectivity `<1e-6`\n"
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("Cartesian PSATD-PML contract failed")


def _field_energy(plotfile: Path) -> float:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    fields = {name: grid["boxlib", name].to_ndarray() for name in ("Ex", "Ey", "Ez", "Bx", "By", "Bz")}
    electric = 0.5 * epsilon_0 * sum(fields[name] ** 2 for name in ("Ex", "Ey", "Ez"))
    magnetic = 0.5 / mu_0 * sum(fields[name] ** 2 for name in ("Bx", "By", "Bz"))
    return float(np.sum(electric + magnetic))


if __name__ == "__main__":
    main()
