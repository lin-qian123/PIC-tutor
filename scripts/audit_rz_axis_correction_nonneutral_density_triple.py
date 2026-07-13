#!/usr/bin/env python
"""Audit non-neutral RZ axis-correction shape behavior across three ion densities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from audit_rz_axis_correction_nonneutral_control import (
    FIELD_FIELDS,
    PARTICLE_FIELDS,
    RHO_FIELDS,
    input_lines,
    load,
    particle_state,
    resolve,
    rho_metrics,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--family",
        nargs=4,
        action="append",
        metavar=("DENSITY", "SHAPE", "ON_PLOTFILE", "OFF_PLOTFILE"),
        required=True,
    )
    parser.add_argument("--source-files", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    source_files = [resolve(root, path) for path in args.source_files]
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    charge_kernel_source = source_files[0].read_text(encoding="utf-8")
    cases = []
    for density, shape_text, on_text, off_text in args.family:
        shape = int(shape_text)
        on_plot = resolve(root, Path(on_text))
        off_plot = resolve(root, Path(off_text))
        on_input = on_plot.parent.parent / "warpx_used_inputs"
        off_input = off_plot.parent.parent / "warpx_used_inputs"
        on_ds, _, on_values = load(on_plot)
        off_ds, _, off_values = load(off_plot)
        particles = {}
        for species in ("electrons", "ions"):
            on_state = particle_state(on_ds, species)
            off_state = particle_state(off_ds, species)
            max_abs = {
                field: float(np.max(np.abs(on_state["fields"][field] - off_state["fields"][field])))
                if on_state["count"] else 0.0
                for field in PARTICLE_FIELDS
            }
            particles[species] = {
                "on_count": on_state["count"],
                "off_count": off_state["count"],
                "particle_state_equal": bool(
                    on_state["count"] == off_state["count"]
                    and np.array_equal(on_state["ids"], off_state["ids"])
                    and all(value == 0.0 for value in max_abs.values())
                ),
            }
        rho = {field: rho_metrics(on_values[field], off_values[field]) for field in RHO_FIELDS}
        fields = {
            field: float(np.max(np.abs(on_values[field] - off_values[field])))
            for field in FIELD_FIELDS
        }
        delta_sum_error = float(
            np.max(
                np.abs(
                    (on_values["rho"] - off_values["rho"])
                    - ((on_values["rho_electrons"] - off_values["rho_electrons"])
                       + (on_values["rho_ions"] - off_values["rho_ions"]))
                )
            )
        )
        cases.append({
            "density": density,
            "shape": shape,
            "on_plotfile": str(on_plot),
            "off_plotfile": str(off_plot),
            "on_input": str(on_input),
            "off_input": str(off_input),
            "inputs_differ_only_by_axis_toggle": input_lines(on_input) == input_lines(off_input),
            "shape_declared_in_inputs": f"algo.particle_shape = {shape}" in on_input.read_text(encoding="utf-8"),
            "particles": particles,
            "rho": rho,
            "field_max_abs_differences": fields,
            "delta_sum_max_abs_error": delta_sum_error,
        })

    cases.sort(key=lambda item: (float(item["density"]), item["shape"]))
    by_density = {}
    for case in cases:
        by_density.setdefault(case["density"], []).append(case)
    densities = sorted(by_density, key=float)
    species_ratios = {
        density: {str(case["shape"]): case["rho"]["rho_ions"]["axis_ratio_median"] for case in by_density[density]}
        for density in densities
    }
    total_ratios = {
        density: {str(case["shape"]): case["rho"]["rho"]["axis_ratio_median"] for case in by_density[density]}
        for density in densities
    }
    checks = {
        "three_densities_present": densities == ["0.25", "0.5", "0.75"],
        "four_shapes_per_density": all(
            [case["shape"] for case in by_density[density]] == [1, 2, 3, 4]
            for density in densities
        ),
        "all_plotfiles_present": all(
            Path(path).is_dir()
            for case in cases
            for path in (case["on_plotfile"], case["off_plotfile"])
        ),
        "inputs_differ_only_by_axis_toggle": all(case["inputs_differ_only_by_axis_toggle"] for case in cases),
        "shape_declared": all(case["shape_declared_in_inputs"] for case in cases),
        "particle_state_equal": all(
            item["particle_state_equal"] for case in cases for item in case["particles"].values()
        ),
        "off_axis_unchanged": all(
            case["rho"][field]["off_axis_ratio_max_abs_deviation"] <= 1.0e-12
            for case in cases for field in RHO_FIELDS
        ),
        "initial_fields_unchanged": all(
            difference == 0.0 for case in cases for difference in case["field_max_abs_differences"].values()
        ),
        "species_shape_ratio_monotonic": all(
            species_ratios[density][str(shape)] > species_ratios[density][str(shape + 1)]
            for density in densities for shape in (1, 2, 3)
        ),
        "species_ratio_density_stable": max(
            abs(species_ratios[left][str(shape)] - species_ratios[right][str(shape)])
            for left_index, left in enumerate(densities)
            for right in densities[left_index + 1:]
            for shape in (1, 2, 3, 4)
        ) <= 1.0e-8,
        "outer_total_rho_shape_monotonic": all(
            total_ratios[density][str(shape)] > total_ratios[density][str(shape + 1)]
            for density in ("0.25", "0.75") for shape in (1, 2, 3)
        ),
        "outer_density_total_rho_consistent": max(
            abs(total_ratios["0.25"][str(shape)] - total_ratios["0.75"][str(shape)])
            for shape in (1, 2, 3, 4)
        ) <= 1.0e-8,
        "half_total_rho_cancellation_observed": all(
            abs(total_ratios["0.5"][str(shape)] - 1.0) <= 1.0e-12
            for shape in (2, 3, 4)
        ),
        "density_changes_total_rho_visibility": min(
            max(
                abs(total_ratios[outer_density][str(shape)] - total_ratios["0.5"][str(shape)])
                for shape in (2, 3, 4)
            )
            for outer_density in ("0.25", "0.75")
        ) > 1.0e-3,
        "total_rho_delta_is_species_sum": all(case["delta_sum_max_abs_error"] <= 2.0e-10 for case in cases),
        "charge_kernel_has_rz_shape_path": "std::sqrt(xp*xp + yp*yp)" in source and "sx[ix]*sz[iz]*wq" in source,
        "charge_kernel_does_not_read_axis_toggle": "verboncoeur_axis_correction" not in charge_kernel_source,
        "inverse_volume_scaling_source_present": "ApplyInverseVolumeScalingToChargeDensity" in source,
    }
    result = {
        "contract": "RZ axis correction non-neutral shape family across three densities",
        "classification": "RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_SAMPLED_AXIS_CANCELLATION_SPECIAL_RATIO_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "species_axis_ratio_by_density": species_ratios,
        "total_rho_axis_ratio_by_density": total_ratios,
        "cases": cases,
        "source_files": [str(path) for path in source_files],
        "scope": (
            "The species-level shape ratio is stable across 0.25*n0, 0.5*n0, and 0.75*n0. The outer densities "
            "show the same shape-monotonic total-rho visibility, while 0.5*n0 cancels for shapes 2-4 at the "
            "sampled axis cells. This is a special-ratio sampled-axis cancellation boundary, without claiming a "
            "kernel root cause or charge closure."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ axis correction non-neutral shape family across three densities contract", "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`", "",
        "| ions density | shape | species rho axis on/off | total rho axis on/off |",
        "|---:|---:|---:|---:|",
    ]
    for case in cases:
        lines.append(
            f"| {case['density']} | {case['shape']} | {case['rho']['rho_ions']['axis_ratio_median']:.9f} | "
            f"{case['rho']['rho']['axis_ratio_median']:.9f} |"
        )
    lines.extend([
        "",
        "The species-level shape ratio is stable across all three densities. `0.25*n0` and `0.75*n0` have the same shape-monotonic total-rho visibility, while `0.5*n0` shows sampled-axis cancellation for shapes 2-4; this is an open special-ratio boundary, not a charge-closure or root-cause proof.",
    ])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
