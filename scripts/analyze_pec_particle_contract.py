#!/usr/bin/env python
"""Compare the PEC-particle case with its periodic-field control."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


FIELD_NAMES = ("Ex", "Ey", "Ez")
SPECIES = ("electron", "proton")
PARTICLE_FIELDS = (
    "particle_position_x",
    "particle_position_y",
    "particle_position_z",
    "particle_momentum_x",
    "particle_momentum_y",
    "particle_momentum_z",
)


def load_case(plotfile: Path) -> tuple[dict[str, dict[str, float]], dict[str, np.ndarray], list[int]]:
    ds = yt.load(str(plotfile))
    stats: dict[str, dict[str, float]] = {}
    grid = ds.covering_grid(level=ds.max_level, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    for name in FIELD_NAMES:
        array = grid["boxlib", name].to_ndarray()
        stats[name] = {
            "min": float(np.min(array)),
            "max": float(np.max(array)),
            "max_abs": float(np.max(np.abs(array))),
            "rms": float(np.sqrt(np.mean(array * array))),
        }
    particles: dict[str, np.ndarray] = {}
    counts: list[int] = []
    ad = ds.all_data()
    for species in SPECIES:
        arrays = [ad[(species, field)].to_ndarray() for field in PARTICLE_FIELDS]
        if any(array.size != 1 for array in arrays):
            raise SystemExit(f"expected one {species} particle in {plotfile}")
        particles[species] = np.array([float(array[0]) for array in arrays])
        counts.append(int(arrays[0].size))
    return stats, particles, counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pec", type=Path, required=True)
    parser.add_argument("--periodic", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--ratio-tolerance", type=float, default=1.0e-2)
    args = parser.parse_args()

    pec_fields, pec_particles, pec_counts = load_case(args.pec)
    periodic_fields, periodic_particles, periodic_counts = load_case(args.periodic)
    field_ratios = {
        name: pec_fields[name]["max_abs"] / periodic_fields[name]["max_abs"]
        for name in FIELD_NAMES
    }
    pec_max = max(item["max_abs"] for item in pec_fields.values())
    periodic_max = max(item["max_abs"] for item in periodic_fields.values())
    max_ratio = pec_max / periodic_max
    ey_ratio = field_ratios["Ey"]
    particle_differences = {
        species: float(np.max(np.abs(pec_particles[species] - periodic_particles[species])))
        for species in SPECIES
    }
    result = {
        "pec_plotfile": str(args.pec),
        "periodic_control_plotfile": str(args.periodic),
        "pec_field_stats": pec_fields,
        "periodic_field_stats": periodic_fields,
        "field_max_abs_ratios": field_ratios,
        "pec_max_abs_E": pec_max,
        "periodic_max_abs_E": periodic_max,
        "max_abs_E_ratio": max_ratio,
        "Ey_max_abs_ratio": ey_ratio,
        "pec_particle_counts": pec_counts,
        "periodic_particle_counts": periodic_counts,
        "max_particle_state_absolute_differences": particle_differences,
        "ratio_tolerance": args.ratio_tolerance,
        "particle_state_tolerance": 1.0e-12,
        "passed": bool(
            np.isfinite(max_ratio)
            and np.isfinite(ey_ratio)
            and max_ratio < args.ratio_tolerance
            and ey_ratio < args.ratio_tolerance
            and pec_counts == periodic_counts == [1, 1]
            and max(particle_differences.values()) < 1.0e-12
        ),
        "contract": "3D PEC near-boundary field suppression relative to periodic control",
        "scope": "official PEC input plus local periodic-field control; 2-rank reader-side comparison; not direct particle-gather instrumentation",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# 3D PEC particle contract\n\n"
        f"- status: `{status}`\n"
        f"- PEC max |E|: `{pec_max:.8e} V/m`\n"
        f"- periodic-control max |E|: `{periodic_max:.8e} V/m`\n"
        f"- max |E| ratio: `{max_ratio:.8e}`\n"
        f"- max |Ey| ratio: `{ey_ratio:.8e}`\n"
        f"- gate: both ratios `< {args.ratio_tolerance:.1e}`\n"
        f"- particle counts (PEC/control): `{pec_counts}` / `{periodic_counts}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("3D PEC particle contract failed")


if __name__ == "__main__":
    main()
