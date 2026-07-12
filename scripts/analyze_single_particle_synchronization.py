#!/usr/bin/env python
"""Rebuild the single-particle diagnostic velocity synchronization contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


E_CHARGE = 1.602176634e-19
E_MASS = 9.1093837015e-31
C_LIGHT = 299792458.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfile", type=Path)
    parser.add_argument("--steps", type=int, default=5)
    parser.add_argument("--dt", type=float, default=1.0e-6)
    parser.add_argument("--ez", type=float, default=-1.0)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    z_expected = 0.1
    uz_expected = 0.0
    uz_expected -= -E_CHARGE / E_MASS * args.ez * args.dt / 2.0
    for _ in range(args.steps):
        uz_expected += -E_CHARGE / E_MASS * args.ez * args.dt
        gamma = np.sqrt((uz_expected / C_LIGHT) ** 2 + 1.0)
        z_expected += (uz_expected / gamma) * args.dt
    uz_expected += -E_CHARGE / E_MASS * args.ez * args.dt / 2.0

    ds = yt.load(str(args.plotfile))
    ad = ds.all_data()
    z_sim = float(ad["electron", "particle_position_x"].to_ndarray()[0])
    uz_sim = float(ad["electron", "particle_momentum_z"].to_ndarray()[0] / E_MASS)
    error_rel = abs((uz_expected - uz_sim) / uz_expected)
    result = {
        "plotfile": str(args.plotfile),
        "steps": args.steps,
        "dt": args.dt,
        "ez": args.ez,
        "z_expected": z_expected,
        "z_sim": z_sim,
        "uz_expected": uz_expected,
        "uz_sim": uz_sim,
        "error_rel": error_rel,
        "tolerance_rel": 1.0e-15,
        "passed": error_rel < 1.0e-15,
        "contract": "diagnostic velocity is synchronized with particle position time level",
    }
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        status = "PASS" if result["passed"] else "FAIL"
        args.output_md.write_text(
            "# Single-particle velocity synchronization contract\n\n"
            f"- status: `{status}`\n"
            f"- plotfile: `{result['plotfile']}`\n"
            f"- z expected/simulated: `{z_expected:.16g}` / `{z_sim:.16g}`\n"
            f"- uz expected/simulated: `{uz_expected:.16g}` / `{uz_sim:.16g}`\n"
            f"- relative velocity error: `{error_rel:.8e}`\n"
            f"- tolerance: `{result['tolerance_rel']:.8e}`\n"
            f"- contract: {result['contract']}\n",
            encoding="utf-8",
        )

    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("single-particle synchronization contract failed")


if __name__ == "__main__":
    main()
