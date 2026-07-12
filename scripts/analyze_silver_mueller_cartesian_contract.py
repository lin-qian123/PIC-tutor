#!/usr/bin/env python
"""Independently verify Cartesian Silver-Mueller residual fields."""

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
    parser.add_argument("--tolerance", type=float, default=1.0e-2)
    args = parser.parse_args()

    ds = yt.load(str(args.plotfile))
    if ds.dimensionality not in (1, 2):
        raise SystemExit(f"expected a Cartesian 1D or 2D plotfile, got dimensionality={ds.dimensionality}")
    grid = ds.covering_grid(level=ds.max_level, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    field_max = {}
    for name in ("Ex", "Ey", "Ez"):
        array = grid["boxlib", name].to_ndarray()
        field_max[name] = float(np.max(np.abs(array)))
    maximum = max(field_max.values())
    result = {
        "plotfile": str(args.plotfile),
        "dimensionality": int(ds.dimensionality),
        "domain_dimensions": ds.domain_dimensions.tolist(),
        "field_max_abs_V_per_m": field_max,
        "max_abs_field_V_per_m": maximum,
        "tolerance_V_per_m": args.tolerance,
        "passed": bool(np.isfinite(maximum) and maximum < args.tolerance),
        "contract": "Cartesian Silver-Mueller low-residual-field contract",
        "scope": "official WarpX Cartesian input; 2-rank run; independent yt reader; not the upstream checksum benchmark",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# Cartesian Silver-Mueller contract\n\n"
        f"- status: `{status}`\n"
        f"- dimensions: `{result['domain_dimensions']}`\n"
        f"- max |Ex|: `{field_max['Ex']:.8e} V/m`\n"
        f"- max |Ey|: `{field_max['Ey']:.8e} V/m`\n"
        f"- max |Ez|: `{field_max['Ez']:.8e} V/m`\n"
        f"- max field: `{maximum:.8e} V/m`\n"
        f"- gate: max field `< {args.tolerance:.1e} V/m`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("Cartesian Silver-Mueller contract failed")


if __name__ == "__main__":
    main()
