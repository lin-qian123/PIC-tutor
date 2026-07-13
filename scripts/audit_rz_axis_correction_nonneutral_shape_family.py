#!/usr/bin/env python
"""Audit shape-dependent RZ axis correction behavior in a non-neutral family."""

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
        "--pair", nargs=3, action="append", metavar=("SHAPE", "ON_PLOTFILE", "OFF_PLOTFILE"), required=True
    )
    parser.add_argument("--source-files", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    source_files = [resolve(root, path) for path in args.source_files]
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    charge_kernel_source = source_files[0].read_text(encoding="utf-8")
    pairs = []
    for shape_text, on_text, off_text in args.pair:
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
        delta_sum_error = float(
            np.max(
                np.abs(
                    (on_values["rho"] - off_values["rho"])
                    - ((on_values["rho_electrons"] - off_values["rho_electrons"])
                       + (on_values["rho_ions"] - off_values["rho_ions"]))
                )
            )
        )
        fields = {
            field: float(np.max(np.abs(on_values[field] - off_values[field])))
            for field in FIELD_FIELDS
        }
        pairs.append({
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

    pairs.sort(key=lambda item: item["shape"])
    ratios = [pair["rho"]["rho"]["axis_ratio_median"] for pair in pairs]
    checks = {
        "four_shapes_present": [pair["shape"] for pair in pairs] == [1, 2, 3, 4],
        "all_plotfiles_present": all(Path(path).is_dir() for pair in pairs for path in (pair["on_plotfile"], pair["off_plotfile"])),
        "inputs_differ_only_by_axis_toggle": all(pair["inputs_differ_only_by_axis_toggle"] for pair in pairs),
        "shape_declared": all(pair["shape_declared_in_inputs"] for pair in pairs),
        "particle_state_equal": all(
            item["particle_state_equal"]
            for pair in pairs
            for item in pair["particles"].values()
        ),
        "off_axis_unchanged": all(
            pair["rho"][field]["off_axis_ratio_max_abs_deviation"] <= 1.0e-12
            for pair in pairs for field in RHO_FIELDS
        ),
        "axis_ratios_finite_and_below_one": all(np.isfinite(ratio) and 0.0 < ratio < 1.0 for ratio in ratios),
        "axis_ratio_changes_with_shape": all(ratios[index] > ratios[index + 1] for index in range(len(ratios) - 1)),
        "total_rho_delta_is_species_sum": all(pair["delta_sum_max_abs_error"] <= 2.0e-10 for pair in pairs),
        "initial_fields_unchanged": all(
            difference == 0.0
            for pair in pairs for difference in pair["field_max_abs_differences"].values()
        ),
        "charge_kernel_has_rz_shape_path": "std::sqrt(xp*xp + yp*yp)" in source and "sx[ix]*sz[iz]*wq" in source,
        "charge_kernel_does_not_read_axis_toggle": "verboncoeur_axis_correction" not in charge_kernel_source,
        "inverse_volume_scaling_source_present": "ApplyInverseVolumeScalingToChargeDensity" in source,
    }
    result = {
        "contract": "RZ axis correction non-neutral shape family",
        "classification": "RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_AXIS_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "pairs": pairs,
        "axis_ratio_by_shape": {str(pair["shape"]): pair["rho"]["rho"]["axis_ratio_median"] for pair in pairs},
        "source_files": [str(path) for path in source_files],
        "scope": (
            "A non-neutral RZ correction-on/off family keeps the off-axis control unchanged but shows a monotonic "
            "shape-dependent axis ratio for shapes 1 through 4. The source split places RZ shape deposition in the "
            "charge kernel and the axis toggle in the later inverse-volume scaling path; this narrows the boundary "
            "to their coupling without claiming a kernel root cause or charge closure."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ axis correction non-neutral shape family contract", "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`", "",
        "| shape | rho axis on/off ratio | rho off-axis max deviation | total delta sum error |",
        "|---:|---:|---:|---:|",
    ]
    for pair in pairs:
        lines.append(
            f"| {pair['shape']} | {pair['rho']['rho']['axis_ratio_median']:.9f} | "
            f"{pair['rho']['rho']['off_axis_ratio_max_abs_deviation']:.3e} | "
            f"{pair['delta_sum_max_abs_error']:.3e} |"
        )
    lines.extend([
        "",
        "The decreasing axis ratio across shapes and unchanged off-axis control narrow the remaining boundary to the RZ shape/deposition and axis wrap/scaling coupling; this is not a root-cause or charge-closure proof.",
    ])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
