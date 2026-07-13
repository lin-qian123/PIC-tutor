#!/usr/bin/env python
"""Audit a non-neutral RZ correction-on/off control for axis rho visibility."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


SPECIES = ("electrons", "ions")
PARTICLE_FIELDS = (
    "particle_position_x",
    "particle_position_y",
    "particle_theta",
    "particle_weight",
    "particle_momentum_x",
    "particle_momentum_y",
    "particle_momentum_z",
)
RHO_FIELDS = ("rho_electrons", "rho_ions", "rho")
FIELD_FIELDS = ("Er", "Ez", "divE")


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def load(path: Path):
    ds = yt.load(str(path))
    grid = ds.covering_grid(level=ds.max_level, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    values = {
        field: grid["boxlib", field].to_ndarray()[:, :, 0]
        for field in RHO_FIELDS + FIELD_FIELDS
    }
    return ds, grid, values


def rho_metrics(on: np.ndarray, off: np.ndarray) -> dict[str, float | int]:
    axis_mask = np.abs(off[0, :]) > 1.0e-30
    off_mask = (np.abs(off[1:, :]) > 1.0e-30) & np.isfinite(on[1:, :]) & np.isfinite(off[1:, :])
    axis_ratio = on[0, axis_mask] / off[0, axis_mask]
    off_ratio = on[1:, :][off_mask] / off[1:, :][off_mask]
    return {
        "axis_ratio_median": float(np.median(axis_ratio)),
        "axis_ratio_min": float(np.min(axis_ratio)),
        "axis_ratio_max": float(np.max(axis_ratio)),
        "off_axis_ratio_max_abs_deviation": float(np.max(np.abs(off_ratio - 1.0))),
        "axis_samples": int(axis_ratio.size),
        "off_axis_samples": int(off_ratio.size),
        "max_abs_difference": float(np.max(np.abs(on - off))),
        "axis_max_abs_difference": float(np.max(np.abs(on[0, :] - off[0, :]))),
        "off_axis_max_abs_difference": float(np.max(np.abs(on[1:, :] - off[1:, :]))),
    }


def particle_state(ds, species: str) -> dict[str, object]:
    data = ds.all_data()
    ids = np.asarray(data[(species, "particle_id")])
    order = np.argsort(ids)
    fields = {field: np.asarray(data[(species, field)])[order] for field in PARTICLE_FIELDS}
    return {"ids": ids[order], "fields": fields, "count": int(ids.size)}


def input_lines(path: Path) -> list[str]:
    return [
        line for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() != "boundary.verboncoeur_axis_correction = false"
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--on-plotfile", type=Path, required=True)
    parser.add_argument("--off-plotfile", type=Path, required=True)
    parser.add_argument("--on-input", type=Path, required=True)
    parser.add_argument("--off-input", type=Path, required=True)
    parser.add_argument("--source-files", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    on_plot = resolve(root, args.on_plotfile)
    off_plot = resolve(root, args.off_plotfile)
    on_input = resolve(root, args.on_input)
    off_input = resolve(root, args.off_input)
    source_files = [resolve(root, path) for path in args.source_files]
    on_ds, _, on_values = load(on_plot)
    off_ds, _, off_values = load(off_plot)

    particles = {}
    for species in SPECIES:
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
            "particle_ids_equal": bool(np.array_equal(on_state["ids"], off_state["ids"])),
            "field_max_abs_difference": max_abs,
            "particle_state_equal": bool(
                on_state["count"] == off_state["count"]
                and np.array_equal(on_state["ids"], off_state["ids"])
                and all(value == 0.0 for value in max_abs.values())
            ),
        }

    rho = {field: rho_metrics(on_values[field], off_values[field]) for field in RHO_FIELDS}
    fields = {
        field: {
            "max_abs_difference": float(np.max(np.abs(on_values[field] - off_values[field]))),
            "axis_max_abs_difference": float(np.max(np.abs(on_values[field][0, :] - off_values[field][0, :]))),
        }
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
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    checks = {
        "plotfiles_present": on_plot.is_dir() and off_plot.is_dir(),
        "inputs_differ_only_by_axis_toggle": input_lines(on_input) == input_lines(off_input),
        "on_input_declares_nonneutral_density": "ions.density = 0.5*n0" in on_input.read_text(encoding="utf-8"),
        "off_input_declares_false": "boundary.verboncoeur_axis_correction = false" in off_input.read_text(encoding="utf-8"),
        "particle_state_equal": all(item["particle_state_equal"] for item in particles.values()),
        "species_axis_ratio_is_085": all(abs(item["axis_ratio_median"] - 0.85) <= 1.0e-12 for item in rho.values()),
        "species_off_axis_unchanged": all(item["off_axis_ratio_max_abs_deviation"] <= 1.0e-12 for item in rho.values()),
        "total_rho_axis_difference_visible": rho["rho"]["axis_max_abs_difference"] > 1.0e-12,
        "total_rho_difference_is_species_sum": delta_sum_error <= 1.0e-10,
        "field_values_unchanged_in_initial_frame": all(item["max_abs_difference"] == 0.0 for item in fields.values()),
        "source_rho_functor_present": "RhoFunctor::operator" in source,
        "source_total_and_species_charge_paths_present": "GetChargeDensity(m_lev, true)" in source,
        "source_axis_wrap_and_scaling_present": "Wrap the charge density" in source and "ApplyInverseVolumeScalingToChargeDensity" in source,
    }
    result = {
        "contract": "RZ axis correction non-neutral control",
        "classification": "RZ_NONNEUTRAL_AXIS_CORRECTION_REVEALS_TOTAL_RHO_CONTRIBUTION_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "particles": particles,
        "rho": rho,
        "fields": fields,
        "delta_sum_max_abs_error": delta_sum_error,
        "source_files": [str(path) for path in source_files],
        "scope": (
            "A non-neutral 2-rank RZ control makes the same axis-only species-rho discrepancy visible in total rho; "
            "the neutral control can hide it through electron-ion cancellation. This separates cancellation from the "
            "remaining deposition/diagnostic boundary, but does not identify the kernel root cause or close charge."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ axis correction non-neutral control contract", "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        "", "| field | axis on/off ratio | axis max difference | off-axis max difference |", "|---|---:|---:|---:|",
    ]
    for field, item in rho.items():
        lines.append(f"| {field} | {item['axis_ratio_median']:.6f} | {item['axis_max_abs_difference']:.6g} | {item['off_axis_max_abs_difference']:.6g} |")
    lines.extend([
        "", f"- delta(total rho) minus delta(species sum) max error: `{delta_sum_error:.3e}`",
        "- The non-neutral control exposes the axis discrepancy in total rho; it does not constitute charge closure or a kernel root-cause proof.",
    ])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
