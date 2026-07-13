#!/usr/bin/env python
"""Analyze direct RZ rho/species observables without treating them as Gauss-law closure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


PLOTFILES = ("diag1000000", "diag1000040", "diag1000080")


def load_frame(path: Path) -> dict:
    ds = yt.load(str(path))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    rho = grid[("boxlib", "rho")].to_ndarray()[:, :, 0]
    rho_e = grid[("boxlib", "rho_electrons")].to_ndarray()[:, :, 0]
    rho_i = grid[("boxlib", "rho_ions")].to_ndarray()[:, :, 0]
    nr, nz = rho.shape
    dr = float(ds.domain_width[0]) / nr
    dz = float(ds.domain_width[1]) / nz
    radius = (np.arange(nr) + 0.5) * dr
    volume = 2.0 * np.pi * radius[:, None] * dr * dz
    species_sum = rho_e + rho_i
    return {
        "integrated_rho_charge": float(np.sum(rho * volume)),
        "integrated_species_charge": float(np.sum(species_sum * volume)),
        "integrated_species_difference": float(np.sum((rho - species_sum) * volume)),
        "species_difference_max_relative": float(
            np.max(np.abs(rho - species_sum)) / max(float(np.max(np.abs(rho))), 1.0e-300)
        ),
        "absolute_rho_charge_scale": float(np.sum(np.abs(rho) * volume)),
        "axis_species_difference_max_relative": float(
            np.max(np.abs(rho[0, :] - species_sum[0, :]))
            / max(float(np.max(np.abs(rho))), 1.0e-300)
        ),
        "off_axis_species_difference_max_relative": float(
            np.max(np.abs(rho[1:, :] - species_sum[1:, :]))
            / max(float(np.max(np.abs(rho))), 1.0e-300)
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", required=True, metavar="SHAPE=RUN_DIR")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    cases = []
    for spec in args.case:
        shape_text, run_dir = spec.split("=", 1)
        directory = Path(run_dir)
        frames = {
            name: load_frame(directory / "diags" / name) for name in PLOTFILES
        }
        charge_series = [frames[name]["integrated_rho_charge"] for name in PLOTFILES]
        max_scale = max(frame["absolute_rho_charge_scale"] for frame in frames.values())
        max_drift = max(abs(value - charge_series[0]) for value in charge_series)
        cases.append(
            {
                "particle_shape": int(shape_text),
                "frames": frames,
                "charge_series": charge_series,
                "max_integrated_charge_drift": max_drift,
                "max_integrated_charge_drift_relative_to_abs_rho": max_drift / max_scale,
                "final_species_difference_pass": frames[PLOTFILES[-1]][
                    "species_difference_max_relative"
                ]
                <= 1.0e-12,
            }
        )
    cases.sort(key=lambda case: case["particle_shape"])
    particle_shapes = [case["particle_shape"] for case in cases]
    result = {
        "contract": "RZ Esirkepov direct rho/species observable",
        "cases": cases,
        "particle_shapes": particle_shapes,
        "scope": (
            "correction-on, RZ, single-level, direct rho/species observable for "
            f"particle_shape={','.join(str(shape) for shape in particle_shapes)}"
        ),
        "all_final_species_difference_pass": all(
            case["final_species_difference_pass"] for case in cases
        ),
        "interpretation": (
            "The rho field agrees with rho_electrons + rho_ions at the final frame to the "
            "species-decomposition tolerance, while the separate divE-rho diagnostic "
            "boundary remains outside this observable. The report therefore supports a "
            "rho-side decomposition contract, not a full Gauss-law or current-conservation "
            "closure claim."
        ),
    }
    result["passed"] = bool(result["all_final_species_difference_pass"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ Esirkepov direct rho/species observable",
        "",
        "| shape | initial/final integrated rho (C) | max drift / abs(rho) scale | final rho-(rho_e+rho_i) |",
        "|---:|---|---:|---:|",
    ]
    for case in cases:
        final = case["frames"][PLOTFILES[-1]]
        lines.append(
            f"| `{case['particle_shape']}` | "
            f"`{case['charge_series'][0]:.6e} -> {case['charge_series'][-1]:.6e}` | "
            f"`{case['max_integrated_charge_drift_relative_to_abs_rho']:.6e}` | "
            f"`{final['species_difference_max_relative']:.6e}` |"
        )
    lines += [
        "",
        f"- final species-decomposition gate: `{'PASS' if result['all_final_species_difference_pass'] else 'BOUNDARY'}`.",
        f"- interpretation: {result['interpretation']}",
        f"- scope: `{result['scope']}`; rho-side only.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
