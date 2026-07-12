#!/usr/bin/env python
"""Independent reader-side contract for the RZ PSATD Langmuir sibling."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, e, epsilon_0, m_e


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--plotfile", default="diags/diag1000080")
    parser.add_argument("--field-tolerance", type=float, default=0.12)
    parser.add_argument("--charge-tolerance", type=float, default=1.0e-9)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    inputs = (run_dir / "warpx_used_inputs").read_text(encoding="utf-8")
    dims = re.search(r"^geometry\.dims\s*=\s*(\S+)", inputs, re.MULTILINE)
    solver = re.search(r"^algo\.maxwell_solver\s*=\s*(\S+)", inputs, re.MULTILINE)
    deposition = re.search(r"^algo\.current_deposition\s*=\s*(\S+)", inputs, re.MULTILINE)
    correction = re.search(r"^psatd\.current_correction\s*=\s*(\S+)", inputs, re.MULTILINE)
    if not dims or dims.group(1) != "RZ":
        raise AssertionError("expected RZ geometry")
    if not solver or solver.group(1).lower() != "psatd":
        raise AssertionError("expected PSATD solver")
    if not deposition or deposition.group(1).lower() != "direct":
        raise AssertionError("expected direct current deposition")
    if not correction or correction.group(1) != "1":
        raise AssertionError("expected psatd.current_correction = 1")

    yt.funcs.mylog.setLevel(0)
    ds = yt.load(str(run_dir / args.plotfile))
    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()
    data = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    er = data["boxlib", "Er"].to_ndarray()[:, :, 0]
    ez = data["boxlib", "Ez"].to_ndarray()[:, :, 0]
    rho = data["boxlib", "rho"].to_ndarray()[:, :, 0]
    div_e = data["boxlib", "divE"].to_ndarray()[:, :, 0]
    if not all(np.isfinite(values).all() for values in (er, ez, rho, div_e)):
        raise AssertionError("non-finite RZ field or source")

    n = 2.0e24
    epsilon = 0.01
    w0 = 5.0e-6
    n_osc_z = 2
    rmax = 20.0e-6
    zmin = -20.0e-6
    zmax = 20.0e-6
    nr = int(ds.domain_dimensions[0])
    nz = int(ds.domain_dimensions[1])
    wp = np.sqrt((n * e**2) / (m_e * epsilon_0))
    k0 = 2.0 * np.pi * n_osc_z / (zmax - zmin)
    rr = (np.arange(nr) + 0.5)[:, None] * (rmax / nr)
    zz = zmin + (np.arange(nz) + 0.5)[None, :] * ((zmax - zmin) / nz)
    t = ds.current_time.to_value()
    er_theory = (
        epsilon * m_e * c**2 / e * 2.0 * rr / w0**2
        * np.exp(-(rr**2) / w0**2) * np.sin(k0 * zz) * np.sin(wp * t)
    )
    ez_theory = (
        -epsilon * m_e * c**2 / e * k0 * np.exp(-(rr**2) / w0**2)
        * np.cos(k0 * zz) * np.sin(wp * t)
    )
    er_error = float(np.max(np.abs(er - er_theory)) / np.max(np.abs(er_theory)))
    ez_error = float(np.max(np.abs(ez - ez_theory)) / np.max(np.abs(ez_theory)))
    residual = np.abs(div_e - rho / epsilon_0)
    scale = float(np.max(np.abs(rho / epsilon_0)))
    charge_relative = float(np.max(residual) / scale) if scale else 0.0
    axis_charge_relative = float(np.max(residual[0, :]) / scale) if scale else 0.0
    off_axis_charge_relative = float(np.max(residual[1:, :]) / scale) if scale else 0.0
    field_passed = max(er_error, ez_error) < args.field_tolerance
    charge_passed = charge_relative <= args.charge_tolerance
    result = {
        "contract": "RZ PSATD current-correction Langmuir reader-side contract",
        "geometry_dims": dims.group(1),
        "maxwell_solver": solver.group(1),
        "current_deposition": deposition.group(1),
        "current_correction": int(correction.group(1)),
        "plotfile_dimensions": [int(v) for v in ds.domain_dimensions],
        "relative_er_error": er_error,
        "relative_ez_error": ez_error,
        "field_tolerance": args.field_tolerance,
        "charge_relative_residual": charge_relative,
        "axis_charge_relative_residual": axis_charge_relative,
        "off_axis_charge_relative_residual": off_axis_charge_relative,
        "charge_tolerance": args.charge_tolerance,
        "field_passed": field_passed,
        "charge_passed": charge_passed,
        "passed": field_passed and charge_passed,
        "scope": "independent RZ analytic Er/Ez and same-surface divE-rho/epsilon0 check",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# RZ PSATD current-correction Langmuir contract\n\n"
        f"- field relative errors (`Er/Ez`): `{er_error:.8e}/{ez_error:.8e}`\n"
        f"- field gate: `< {args.field_tolerance:.2f}`\n"
        f"- charge relative residual: `{charge_relative:.8e}`\n"
        f"- axis/off-axis charge residual: `{axis_charge_relative:.8e}/{off_axis_charge_relative:.8e}`\n"
        f"- charge gate: `<= {args.charge_tolerance:.1e}`\n"
        f"- field status: `{'PASS' if field_passed else 'FAIL'}`\n"
        f"- charge status: `{'PASS' if charge_passed else 'FAIL'}`\n"
        f"- overall status: `{'PASS' if result['passed'] else 'BOUNDARY'}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not field_passed:
        raise SystemExit("RZ PSATD Langmuir field contract failed")


if __name__ == "__main__":
    main()
