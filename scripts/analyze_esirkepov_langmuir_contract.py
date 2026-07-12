#!/usr/bin/env python
"""Independent reader-side contract for Esirkepov Langmuir cases."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import epsilon_0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--plotfile", default="diags/diag1000080")
    parser.add_argument("--charge-tol", type=float, default=1.0e-11)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    input_text = (run_dir / "warpx_used_inputs").read_text(encoding="utf-8")
    deposition = re.search(r"^algo\.current_deposition\s*=\s*(\S+)", input_text, re.MULTILINE)
    dimensions = re.search(r"^geometry\.dims\s*=\s*(\S+)", input_text, re.MULTILINE)
    shape = re.search(r"^algo\.particle_shape\s*=\s*(\S+)", input_text, re.MULTILINE)
    if not deposition or deposition.group(1).lower() != "esirkepov":
        raise AssertionError("warpx_used_inputs does not select Esirkepov")
    if not dimensions or not shape:
        raise AssertionError("missing geometry or particle-shape contract")

    ds = yt.load(str(run_dir / args.plotfile))
    data = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    rho = data[("boxlib", "rho")].to_ndarray()
    div_e = data[("boxlib", "divE")].to_ndarray()
    field_names = ["Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz"]
    field_max_abs = {}
    for name in field_names:
        values = data[("boxlib", name)].to_ndarray()
        if not np.isfinite(values).all():
            raise AssertionError(f"non-finite values in {name}")
        field_max_abs[name] = float(np.max(np.abs(values)))
    if not np.isfinite(rho).all() or not np.isfinite(div_e).all():
        raise AssertionError("non-finite rho/divE")

    charge_residual = float(np.max(np.abs(div_e - rho / epsilon_0)))
    charge_scale = float(np.max(np.abs(rho / epsilon_0)))
    charge_relative = charge_residual / charge_scale if charge_scale else 0.0
    if charge_relative > args.charge_tol:
        raise AssertionError(f"charge relative residual {charge_relative:.8e} > {args.charge_tol:.8e}")

    result = {
        "contract": "Esirkepov Langmuir reader-side runtime contract",
        "run_dir": str(run_dir),
        "plotfile": args.plotfile,
        "geometry_dims": dimensions.group(1),
        "particle_shape": int(shape.group(1)),
        "current_deposition": deposition.group(1),
        "plotfile_domain_dimensions": [int(v) for v in ds.domain_dimensions],
        "charge_residual_max": charge_residual,
        "charge_scale_max": charge_scale,
        "charge_relative_residual": charge_relative,
        "charge_tolerance": args.charge_tol,
        "field_max_abs": field_max_abs,
        "passed": True,
        "scope": "reader-side runtime fields and discrete divE-rho/epsilon0; not a bitwise kernel proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# Esirkepov Langmuir runtime contract\n\n"
        f"- geometry: `{result['geometry_dims']}`\n"
        f"- particle shape: `{result['particle_shape']}`\n"
        f"- current deposition: `{result['current_deposition']}`\n"
        f"- plotfile dimensions: `{result['plotfile_domain_dimensions']}`\n"
        f"- charge relative residual: `{charge_relative:.8e}`\n"
        f"- gate: `<= {args.charge_tol:.1e}`\n"
        "- finite field/rho/divE check: `PASS`\n"
        "- status: `PASS`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(
        f"PASS: dims={result['geometry_dims']}, "
        f"charge relative residual={charge_relative:.3e}"
    )


if __name__ == "__main__":
    main()
