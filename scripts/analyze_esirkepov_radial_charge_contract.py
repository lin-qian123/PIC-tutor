#!/usr/bin/env python
"""Independent radial Er and charge contract for RCYLINDER/RSPHERE."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, e, epsilon_0, m_e


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--plotfile", default="diags/diag1000080")
    parser.add_argument("--field-tolerance", type=float, default=0.12)
    parser.add_argument("--charge-tolerance", type=float, default=1.0e-11)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    inputs = (run_dir / "warpx_used_inputs").read_text(encoding="utf-8")
    dims = re.search(r"^geometry\.dims\s*=\s*(\S+)", inputs, re.MULTILINE)
    deposition = re.search(r"^algo\.current_deposition\s*=\s*(\S+)", inputs, re.MULTILINE)
    shape = re.search(r"^algo\.particle_shape\s*=\s*(\S+)", inputs, re.MULTILINE)
    if not dims or dims.group(1) not in {"RCYLINDER", "RSPHERE"}:
        raise AssertionError("expected RCYLINDER or RSPHERE geometry")
    if not deposition or deposition.group(1).lower() != "esirkepov":
        raise AssertionError("expected Esirkepov current deposition")
    if not shape:
        raise AssertionError("missing particle shape")

    ds = yt.load(str(run_dir / args.plotfile))
    data = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    er = data[("boxlib", "Er")].to_ndarray()[:, 0, 0]
    rho = data[("boxlib", "rho")].to_ndarray()[:, 0, 0]
    div_e = data[("boxlib", "divE")].to_ndarray()[:, 0, 0]
    if not all(np.isfinite(values).all() for values in (er, rho, div_e)):
        raise AssertionError("non-finite radial field or source")

    n = 2.0e24
    epsilon = 0.01
    w0 = 5.0e-6
    rmax = 20.0e-6
    nr = int(ds.domain_dimensions[0])
    wp = np.sqrt((n * e**2) / (m_e * epsilon_0))
    rr = (np.arange(nr) + 0.5) * (rmax / nr)
    t = ds.current_time.to_value()
    er_theory = epsilon * m_e * c**2 / e * 2.0 * rr / w0**2 * np.exp(-(rr**2) / w0**2) * np.sin(wp * t)
    field_error = float(np.max(np.abs(er - er_theory)) / np.max(np.abs(er_theory)))
    residual = np.abs(div_e - rho / epsilon_0)
    scale = float(np.max(np.abs(rho / epsilon_0)))
    charge_error = float(np.max(residual) / scale) if scale else 0.0
    axis_error = float(residual[0] / scale) if scale else 0.0
    off_axis_error = float(np.max(residual[1:]) / scale) if scale else 0.0
    field_passed = field_error < args.field_tolerance
    charge_passed = charge_error <= args.charge_tolerance
    result = {
        "contract": "Esirkepov radial Er and charge reader-side runtime contract",
        "geometry_dims": dims.group(1),
        "particle_shape": int(shape.group(1)),
        "relative_er_error": field_error,
        "charge_relative_residual": charge_error,
        "axis_charge_relative_residual": axis_error,
        "off_axis_charge_relative_residual": off_axis_error,
        "field_tolerance": args.field_tolerance,
        "charge_tolerance": args.charge_tolerance,
        "field_passed": field_passed,
        "charge_passed": charge_passed,
        "passed": field_passed and charge_passed,
        "scope": "independent radial Er and same-surface divE-rho/epsilon0 check; not a full geometry/order matrix",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# Esirkepov radial charge runtime contract\n\n"
        f"- geometry: `{result['geometry_dims']}`\n"
        f"- shape: `{result['particle_shape']}`\n"
        f"- relative Er error: `{field_error:.8e}`\n"
        f"- all-cell charge residual: `{charge_error:.8e}`\n"
        f"- axis/off-axis residual: `{axis_error:.8e}/{off_axis_error:.8e}`\n"
        f"- field status: `{'PASS' if field_passed else 'BOUNDARY'}`\n"
        f"- charge status: `{'PASS' if charge_passed else 'BOUNDARY'}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(f"{'PASS' if result['passed'] else 'BOUNDARY'}: {dims.group(1)} Er={field_error:.3e}, charge={charge_error:.3e}")
    if not field_passed:
        raise SystemExit("radial field contract failed")


if __name__ == "__main__":
    main()
