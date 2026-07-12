#!/usr/bin/env python
"""Audit 2D AMR subcycling output completeness and moving-window geometry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c


FIELD_NAMES = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz")
SPECIES = ("driver", "beam", "plasma_e", "plasma_p")


def read_plotfile(plotfile: Path) -> tuple[yt.Dataset, dict[str, float], dict[str, int]]:
    ds = yt.load(str(plotfile))
    dims = list(ds.domain_dimensions)
    if ds.dimensionality == 2:
        dims[2] = 1
    if ds.max_level == 1:
        dims[0] *= 2
        dims[1] *= 2
    grid = ds.covering_grid(level=ds.max_level, left_edge=ds.domain_left_edge, dims=dims)
    fields = {
        name: float(np.max(np.abs(grid["boxlib", name].to_ndarray())))
        for name in FIELD_NAMES
    }
    ad = ds.all_data()
    counts = {
        species: (
            int(ad[(species, "particle_position_x")].size)
            if (species, "particle_position_x") in ds.field_list
            else 0
        )
        for species in SPECIES
    }
    return ds, fields, counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    initial_ds, initial_fields, initial_counts = read_plotfile(args.initial)
    final_ds, final_fields, final_counts = read_plotfile(args.final)
    if final_ds.dimensionality != 2 or final_ds.max_level != 1:
        raise SystemExit("expected a 2D two-level AMR final plotfile")
    if final_ds.domain_dimensions.tolist() != [64, 256, 1]:
        raise SystemExit(f"unexpected final dimensions: {final_ds.domain_dimensions.tolist()}")

    actual_shift = float(final_ds.domain_left_edge[1] - initial_ds.domain_left_edge[1])
    expected_shift = float(c * final_ds.current_time)
    coarse_dz = float(initial_ds.domain_width[1] / initial_ds.domain_dimensions[1])
    shift_error = abs(actual_shift - expected_shift)
    finite = all(np.isfinite(value) for value in initial_fields.values()) and all(
        np.isfinite(value) for value in final_fields.values()
    )
    result = {
        "initial_plotfile": str(args.initial),
        "final_plotfile": str(args.final),
        "initial_time": float(initial_ds.current_time),
        "final_time": float(final_ds.current_time),
        "final_max_level": int(final_ds.max_level),
        "final_domain_dimensions": final_ds.domain_dimensions.tolist(),
        "initial_domain_left_edge": [float(v) for v in initial_ds.domain_left_edge],
        "final_domain_left_edge": [float(v) for v in final_ds.domain_left_edge],
        "actual_moving_window_shift_z": actual_shift,
        "expected_c_times_time_shift_z": expected_shift,
        "moving_window_shift_error": shift_error,
        "coarse_dz_tolerance": coarse_dz,
        "initial_field_max_abs": initial_fields,
        "final_field_max_abs": final_fields,
        "initial_particle_counts": initial_counts,
        "final_particle_counts": final_counts,
        "finite_fields": finite,
        "moving_window_gate": bool(shift_error <= coarse_dz),
        "particle_presence_gate": bool(all(count > 0 for count in final_counts.values())),
        "passed": bool(
            finite
            and shift_error <= coarse_dz
            and all(count > 0 for count in final_counts.values())
        ),
        "contract": "2D AMR subcycling output completeness and moving-window geometry",
        "scope": "official WarpX input; 2-rank producer; independent yt reader; not a transition-zone route-count or conservation proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# 2D AMR subcycling contract\n\n"
        f"- status: `{status}`\n"
        f"- final time: `{result['final_time']:.8e} s`\n"
        f"- AMR level / dimensions: `{result['final_max_level']} / {result['final_domain_dimensions']}`\n"
        f"- moving-window actual / c*t shift: `{actual_shift:.8e}` / `{expected_shift:.8e} m`\n"
        f"- shift error / coarse dz: `{shift_error:.8e}` / `{coarse_dz:.8e} m`\n"
        f"- final particle counts: `{final_counts}`\n"
        "- gates: finite E/B/J; moving-window shift error <= coarse dz; all four species remain present\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("2D AMR subcycling contract failed")


if __name__ == "__main__":
    main()
