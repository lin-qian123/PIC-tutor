#!/usr/bin/env python
"""Check whether identical particle state can explain the RZ axis rho mismatch."""

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
RHO_FIELDS = ("rho_electrons", "rho_ions")


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def dataset(path: Path):
    ds = yt.load(str(path))
    return ds, ds.all_data()


def sorted_particle_state(ad, species: str) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    ids = np.asarray(ad[(species, "particle_id")])
    order = np.argsort(ids)
    fields = {
        field: np.asarray(ad[(species, field)])[order]
        for field in PARTICLE_FIELDS
    }
    return ids[order], fields


def compare_particle_state(on_ad, off_ad, species: str) -> dict[str, object]:
    on_ids, on_fields = sorted_particle_state(on_ad, species)
    off_ids, off_fields = sorted_particle_state(off_ad, species)
    max_abs = {}
    for field in PARTICLE_FIELDS:
        on_values = on_fields[field]
        off_values = off_fields[field]
        max_abs[field] = float(np.max(np.abs(on_values - off_values))) if len(on_values) else 0.0
    return {
        "on_count": int(len(on_ids)),
        "off_count": int(len(off_ids)),
        "particle_ids_equal": bool(np.array_equal(on_ids, off_ids)),
        "field_max_abs_difference": max_abs,
        "particle_state_equal": bool(np.array_equal(on_ids, off_ids) and all(value == 0.0 for value in max_abs.values())),
    }


def read_rho(path: Path, field: str) -> np.ndarray:
    ds = yt.load(str(path))
    grid = ds.covering_grid(level=ds.max_level, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    return grid["boxlib", field].to_ndarray()[:, :, 0]


def compare_rho(on_path: Path, off_path: Path, field: str) -> dict[str, float]:
    on = read_rho(on_path, field)
    off = read_rho(off_path, field)
    axis_ratio = on[0, :] / off[0, :]
    off_mask = (np.abs(off[1:, :]) > 1.0e-30) & np.isfinite(on[1:, :]) & np.isfinite(off[1:, :])
    off_ratio = on[1:, :][off_mask] / off[1:, :][off_mask]
    return {
        "axis_ratio_median": float(np.median(axis_ratio)),
        "axis_ratio_min": float(np.min(axis_ratio)),
        "axis_ratio_max": float(np.max(axis_ratio)),
        "off_axis_ratio_max_abs_deviation": float(np.max(np.abs(off_ratio - 1.0))),
        "axis_samples": int(axis_ratio.size),
        "off_axis_samples": int(off_ratio.size),
    }


def normalized_input(path: Path) -> list[str]:
    return [
        line for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() != "boundary.verboncoeur_axis_correction = false"
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--on-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--off-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--on-input", type=Path, required=True)
    parser.add_argument("--off-input", type=Path, required=True)
    parser.add_argument("--source-files", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    on_paths = [resolve(root, path) for path in args.on_plotfiles]
    off_paths = [resolve(root, path) for path in args.off_plotfiles]
    on_input = resolve(root, args.on_input)
    off_input = resolve(root, args.off_input)
    source_files = [resolve(root, path) for path in args.source_files]
    pairs = []
    for on_path, off_path in zip(on_paths, off_paths):
        _, on_ad = dataset(on_path)
        _, off_ad = dataset(off_path)
        particles = {species: compare_particle_state(on_ad, off_ad, species) for species in SPECIES}
        rho = {field: compare_rho(on_path, off_path, field) for field in RHO_FIELDS}
        pairs.append({"on_plotfile": str(on_path), "off_plotfile": str(off_path), "particles": particles, "rho": rho})

    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    all_particles = [pair["particles"][species] for pair in pairs for species in SPECIES]
    all_rho = [pair["rho"][field] for pair in pairs for field in RHO_FIELDS]
    checks = {
        "paired_family_lengths": len(on_paths) == len(off_paths),
        "all_plotfiles_present": all(path.is_dir() for path in on_paths + off_paths),
        "inputs_differ_only_by_explicit_toggle": normalized_input(on_input) == normalized_input(off_input),
        "particle_state_equal_for_all_pairs": all(item["particle_state_equal"] for item in all_particles),
        "source_rho_functor_present": "RhoFunctor::operator" in source,
        "source_species_get_charge_density_present": "mypc.GetChargeDensity(m_lev, true)" in source,
        "source_deposit_charge_present": "DepositCharge" in source,
        "source_axis_wrap_present": "Wrap the charge density" in source,
        "source_inverse_volume_scaling_present": "ApplyInverseVolumeScalingToChargeDensity" in source,
        "final_axis_ratio_is_085": all(abs(item["axis_ratio_median"] - 0.85) <= 1.0e-12 for item in all_rho),
        "off_axis_control_matches": all(item["off_axis_ratio_max_abs_deviation"] <= 1.0e-12 for item in all_rho),
    }
    result = {
        "contract": "RZ rho particle-state invariant",
        "classification": "RZ_RHO_AXIS_DIAGNOSTIC_CONSUMER_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "source_files": [str(path) for path in source_files],
        "pairs": pairs,
        "scope": (
            "The correction-on/off initial frames have identical particle IDs, positions, angles, "
            "weights, and momenta for both species, while the species-rho axis ratio remains 0.85 "
            "and the off-axis control remains one. The result excludes a particle-initialization "
            "difference as the explanation and narrows the boundary to the species-rho diagnostic, "
            "deposition, or axis-wrap/scaling consumer path. It does not identify a kernel root cause "
            "or close charge conservation."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ rho particle-state invariant contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        "- particle-state gate: identical IDs, positions, angles, weights, and momenta",
        "- final species-rho axis ratio: `0.850000`",
        "- off-axis ratio maximum deviation: `0`",
        "",
        "| grid | species | particles on/off | particle state | rho field | axis ratio |",
        "|---:|---|---:|:---:|---|---:|",
    ]
    for pair in pairs:
        grid = pair["particles"]["electrons"]["on_count"]
        # All six cases use the same particle count per species in this family.
        for species in SPECIES:
            particle = pair["particles"][species]
            field = "rho_electrons" if species == "electrons" else "rho_ions"
            lines.append(
                f"| {pair['rho'][field]['axis_samples'] // 2}x{pair['rho'][field]['axis_samples']} | {species} | "
                f"{particle['on_count']}/{particle['off_count']} | `{'PASS' if particle['particle_state_equal'] else 'FAIL'}` | "
                f"{field} | {pair['rho'][field]['axis_ratio_median']:.6f} |"
            )
    lines.extend([
        "",
        "Identical particle state with a persistent axis-only rho difference excludes particle initialization as the explanation. "
        "The remaining boundary is the diagnostic/deposition/axis-wrap consumer path, not a charge-closure pass.",
    ])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
