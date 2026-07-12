#!/usr/bin/env python
"""Independently verify particles-in-PML residual-field contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfile", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=None)
    args = parser.parse_args()

    ds = yt.load(str(args.plotfile))
    dims = ds.domain_dimensions.tolist()
    if ds.dimensionality not in (2, 3):
        raise SystemExit(f"expected a 2D or 3D plotfile, got dimensionality={ds.dimensionality}, dims={dims}")
    if ds.dimensionality == 2 and dims[2] != 1:
        raise SystemExit(f"expected a 2D plotfile with a singleton third dimension, got dims={dims}")
    covering_dims = list(dims)
    if ds.max_level == 1:
        covering_dims[0] *= 2
        covering_dims[1] *= 2
        if ds.dimensionality == 3:
            covering_dims[2] *= 2
    grid = ds.covering_grid(
        level=ds.max_level, left_edge=ds.domain_left_edge, dims=covering_dims
    )
    tolerance = args.tolerance
    if tolerance is None:
        if ds.dimensionality == 2:
            tolerance = 6.0e-4 if ds.max_level == 1 else 3.0e-4
        else:
            tolerance = 110.0 if ds.max_level == 1 else 10.0
    field_max = {
        name: float(np.max(np.abs(grid["boxlib", name].to_ndarray())))
        for name in ("Ex", "Ey", "Ez")
    }
    max_abs = max(field_max.values())
    result = {
        "plotfile": str(args.plotfile),
        "dimensionality": int(ds.dimensionality),
        "domain_dimensions": dims,
        "max_level": int(ds.max_level),
        "covering_grid_dimensions": covering_dims,
        "field_max_abs": field_max,
        "max_abs_Efield": max_abs,
        "tolerance_abs": tolerance,
        "passed": bool(np.isfinite(max_abs) and max_abs < tolerance),
        "contract": "particles-in-PML residual electric-field absorption",
        "scope": "official WarpX input; 2-rank run; independent yt reader; not the upstream checksum benchmark",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# Particles-in-PML contract\n\n"
        f"- status: `{status}`\n"
        f"- dimensionality / max level: `{ds.dimensionality}D / {ds.max_level}`\n"
        f"- domain dimensions: `{dims}`\n"
        f"- covering-grid dimensions: `{covering_dims}`\n"
        f"- max |Ex|: `{field_max['Ex']:.8e}`\n"
        f"- max |Ey|: `{field_max['Ey']:.8e}`\n"
        f"- max |Ez|: `{field_max['Ez']:.8e}`\n"
        f"- max absolute electric field: `{max_abs:.8e}`\n"
        f"- gate: max absolute electric field `< {tolerance:.1e}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("2D particles-in-PML contract failed")


if __name__ == "__main__":
    main()
