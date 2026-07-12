#!/usr/bin/env python
"""Independent contract for implicit Villasenor deposition cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import e, epsilon_0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--plotfile", required=True)
    parser.add_argument("--n0", type=float, required=True)
    parser.add_argument("--energy-tol", type=float, default=None)
    parser.add_argument("--charge-tol", type=float, required=True)
    parser.add_argument("--require-filter", action="store_true")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    used_inputs = (run_dir / "warpx_used_inputs").read_text(encoding="utf-8")
    ds = yt.load(str(Path(args.plotfile).resolve()))
    grid = ds.covering_grid(
        level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions
    )

    fields = {}
    for name in ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "rho", "divE"):
        fields[name] = np.asarray(grid["boxlib", name].value)
    finite_fields = all(np.isfinite(value).all() for value in fields.values())
    drho = (fields["rho"] - epsilon_0 * fields["divE"]) / e / args.n0
    charge_rms = float(np.sqrt(np.mean(drho**2)))
    charge_max = float(np.max(np.abs(drho)))

    energy_result = None
    if args.energy_tol is not None:
        field_energy = np.loadtxt(run_dir / "diags/reducedfiles/field_energy.txt", skiprows=1)
        particle_energy = np.loadtxt(run_dir / "diags/reducedfiles/particle_energy.txt", skiprows=1)
        total_energy = field_energy[:, 2] + particle_energy[:, 2]
        delta = (total_energy - total_energy[0]) / total_energy[0]
        max_energy_delta = float(np.max(np.abs(delta)))
        energy_result = {
            "max_relative_change": max_energy_delta,
            "tolerance": args.energy_tol,
            "passed": max_energy_delta < args.energy_tol,
        }

    result = {
        "run_dir": str(run_dir),
        "plotfile": str(Path(args.plotfile).resolve()),
        "domain_dimensions": [int(value) for value in ds.domain_dimensions],
        "current_time": float(ds.current_time),
        "fields_finite": finite_fields,
        "charge": {
            "rms": charge_rms,
            "max_abs": charge_max,
            "tolerance": args.charge_tol,
            "passed": charge_rms < args.charge_tol,
        },
        "energy": energy_result,
        "input_contract": {
            "villasenor": "current_deposition = \"villasenor\"" in used_inputs,
            "theta_implicit": "evolve_scheme = \"theta_implicit_em\"" in used_inputs,
            "filter_enabled": "warpx.use_filter = 1" in used_inputs,
        },
        "contract": "implicit Villasenor reader-side energy/Gauss-law contract; not bitwise kernel equivalence",
    }
    result["passed"] = bool(
        result["fields_finite"]
        and result["charge"]["passed"]
        and result["input_contract"]["villasenor"]
        and result["input_contract"]["theta_implicit"]
        and (not args.require_filter or result["input_contract"]["filter_enabled"])
        and (energy_result is None or energy_result["passed"])
    )
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    Path(args.output_md).write_text(_markdown(result), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("implicit Villasenor contract failed")


def _markdown(result: dict) -> str:
    lines = [
        "# Implicit Villasenor contract",
        "",
        "- scope: independent reader-side contract for an official implicit Villasenor case",
        f"- contract: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- domain dimensions: `{result['domain_dimensions']}`",
        f"- finite fields: `{'PASS' if result['fields_finite'] else 'FAIL'}`",
        f"- Gauss-law RMS: `{result['charge']['rms']:.6e}` < `{result['charge']['tolerance']:.6e}`",
        f"- Gauss-law max abs: `{result['charge']['max_abs']:.6e}`",
        f"- input contract: `{result['input_contract']}`",
    ]
    if result["energy"] is not None:
        lines.append(
            f"- total-energy relative change: `{result['energy']['max_relative_change']:.6e}` < `"
            f"{result['energy']['tolerance']:.6e}`"
        )
    lines.extend(
        [
            "",
            "This contract verifies finite fields, input dispatch, reader-side Gauss-law consistency, and optionally the reduced energy ledger. It does not prove bitwise equivalence of every shape order, geometry, boundary crop, or implicit solver branch.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
