#!/usr/bin/env python
"""Check the RZ charge-density volume and particle-charge contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


ELECTRON_CHARGE = -1.602176634e-19


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfile", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    ds = yt.load(str(args.plotfile))
    if ds.parameters.get("geometry.dims") != "RZ":
        raise SystemExit("the volume contract requires an RZ plotfile")
    dims = np.asarray(ds.domain_dimensions, dtype=int)
    nr, nz = int(dims[0]), int(dims[1])
    rlo, zlo = ds.domain_left_edge[:2].to_ndarray()
    rhi, zhi = ds.domain_right_edge[:2].to_ndarray()
    dr = (rhi - rlo) / nr
    dz = (zhi - zlo) / nz
    radius = rlo + (np.arange(nr) + 0.5) * dr
    cell_volume = (2.0 * np.pi * radius[:, None]) * dr * dz

    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=dims)
    rho = grid[("boxlib", "rho")].to_ndarray()[:, :, 0]
    integrated_rho_charge = float(np.sum(rho * cell_volume))
    data = ds.all_data()
    particle_weight = data[("electron", "particle_weight")].to_ndarray()
    particle_charge = float(np.sum(particle_weight) * ELECTRON_CHARGE)
    relative_mismatch = abs(integrated_rho_charge - particle_charge) / abs(particle_charge)
    result = {
        "plotfile": str(args.plotfile),
        "geometry": "RZ",
        "grid_shape_rz": [nr, nz],
        "cell_size": [float(dr), float(dz)],
        "particle_count": int(particle_weight.size),
        "particle_charge": particle_charge,
        "integrated_rho_charge": integrated_rho_charge,
        "relative_charge_mismatch": relative_mismatch,
        "tolerance": 0.01,
        "passed": bool(relative_mismatch < 0.01),
        "contract": "RZ rho density integrated with cylindrical cell volume equals particle charge",
        "volume_formula": "2*pi*r_center*dr*dz",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# RZ charge-volume contract\n\n"
        f"- status: `{status}`\n"
        f"- grid shape (r,z): `{nr} x {nz}`\n"
        f"- particle count: `{result['particle_count']}`\n"
        f"- particle charge: `{particle_charge:.8e} C`\n"
        f"- integrated rho charge: `{integrated_rho_charge:.8e} C`\n"
        f"- relative mismatch: `{relative_mismatch:.8e}`\n"
        f"- tolerance: `{result['tolerance']:.2e}`\n"
        f"- volume formula: `{result['volume_formula']}`\n"
        f"- contract: {result['contract']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("RZ charge-volume contract failed")


if __name__ == "__main__":
    main()
