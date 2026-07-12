#!/usr/bin/env python
"""Independent reader-side contract for RCYLINDER/RSPHERE Langmuir runs."""

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
    parser.add_argument("--tolerance", type=float, default=0.12)
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
    er = data[("boxlib", "Er")].to_ndarray()
    if not np.isfinite(er).all():
        raise AssertionError("non-finite Er")

    n = 2.0e24
    epsilon = 0.01
    w0 = 5.0e-6
    wp = np.sqrt((n * e**2) / (m_e * epsilon_0))
    rmax = 20.0e-6
    nr = int(ds.domain_dimensions[0])
    rr = (np.arange(nr) + 0.5) * (rmax / nr)
    theory = epsilon * m_e * c**2 / e * 2.0 * rr / w0**2 * np.exp(-(rr**2) / w0**2) * np.sin(wp * ds.current_time.to_value())
    simulated = er[:, 0, 0]
    relative_error = float(np.max(np.abs(simulated - theory)) / np.max(np.abs(theory)))
    passed = relative_error < args.tolerance
    result = {
        "contract": "Esirkepov radial Langmuir reader-side runtime contract",
        "geometry_dims": dims.group(1),
        "current_deposition": deposition.group(1),
        "particle_shape": int(shape.group(1)),
        "plotfile": args.plotfile,
        "plotfile_dimensions": [int(v) for v in ds.domain_dimensions],
        "relative_er_error": relative_error,
        "tolerance": args.tolerance,
        "passed": passed,
        "scope": "independent radial Er/theory check; not a full charge-conservation or all-combination regression",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# Esirkepov radial Langmuir runtime contract\n\n"
        f"- geometry: `{result['geometry_dims']}`\n"
        f"- current deposition: `{result['current_deposition']}`\n"
        f"- particle shape: `{result['particle_shape']}`\n"
        f"- relative `Er` error: `{relative_error:.8e}`\n"
        f"- gate: `< {args.tolerance:.2f}`\n"
        f"- status: `{'PASS' if passed else 'FAIL'}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(f"{'PASS' if passed else 'FAIL'}: {dims.group(1)} relative Er error={relative_error:.3e}")
    if not passed:
        raise SystemExit("radial Langmuir contract failed")


if __name__ == "__main__":
    main()
