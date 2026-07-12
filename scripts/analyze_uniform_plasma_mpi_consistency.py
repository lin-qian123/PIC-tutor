#!/usr/bin/env python
"""Compare uniform-plasma final fields and particle records across MPI layouts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, epsilon_0, m_e, mu_0


def _grid(path: Path):
    dataset = yt.load(str(path))
    if hasattr(dataset, "force_periodicity"):
        dataset.force_periodicity()
    return dataset, dataset.covering_grid(
        level=0,
        left_edge=dataset.domain_left_edge,
        dims=dataset.domain_dimensions,
    )


def _particle_array(dataset, field):
    data = np.asarray(dataset.all_data()[field].to_ndarray()).reshape(-1)
    if field[1] != "particle_id":
        ids = np.asarray(dataset.all_data()[(field[0], "particle_id")].to_ndarray()).reshape(-1)
        data = data[np.argsort(ids, kind="stable")]
    else:
        data = np.sort(data)
    return data


def _invariants(dataset):
    data = dataset.all_data()
    cell_volume = float(np.prod(dataset.domain_width) / np.prod(dataset.domain_dimensions))
    electric = sum(
        np.sum(data[("boxlib", name)].to_value() ** 2)
        for name in ("Ex", "Ey", "Ez")
    )
    magnetic = sum(
        np.sum(data[("boxlib", name)].to_value() ** 2)
        for name in ("Bx", "By", "Bz")
    )
    field_energy = cell_volume * (0.5 * epsilon_0 * electric + 0.5 * magnetic / mu_0)
    weights = data[("electrons", "particle_weight")].to_value()
    momenta = np.column_stack(
        [data[("electrons", f"particle_momentum_{axis}")].to_value() for axis in "xyz"]
    )
    gamma = np.sqrt(1.0 + np.sum(momenta**2, axis=1) / (m_e * c) ** 2)
    particle_kinetic = float(np.sum(weights * m_e * c**2 * (gamma - 1.0)))
    return {
        "particle_count": int(weights.size),
        "particle_weight_sum": float(np.sum(weights)),
        "field_energy": float(field_energy),
        "particle_kinetic_energy": particle_kinetic,
        "total_energy": float(field_energy + particle_kinetic),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("single_rank_plotfile", type=Path)
    parser.add_argument("multi_rank_plotfile", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=1.0e-12)
    args = parser.parse_args()

    single, single_grid = _grid(args.single_rank_plotfile)
    multi, multi_grid = _grid(args.multi_rank_plotfile)
    if single.domain_dimensions.tolist() != multi.domain_dimensions.tolist():
        raise SystemExit("single-rank and multi-rank domain dimensions differ")

    records = []
    for field in sorted(set(single.field_list) & set(multi.field_list)):
        if field[1].startswith("particle_"):
            reference = _particle_array(single, field)
            candidate = _particle_array(multi, field)
        else:
            reference = np.asarray(single_grid[field].to_ndarray())
            candidate = np.asarray(multi_grid[field].to_ndarray())
        if reference.shape != candidate.shape:
            raise SystemExit(f"field shape differs for {field}: {reference.shape} vs {candidate.shape}")
        absolute = float(np.max(np.abs(candidate - reference)))
        scale = max(float(np.max(np.abs(reference))), 1.0e-300)
        relative = absolute / scale
        l2_scale = max(float(np.linalg.norm(reference.ravel())), 1.0e-300)
        l2_relative = float(np.linalg.norm((candidate - reference).ravel()) / l2_scale)
        comparison = "metadata" if field[1] == "particle_cpu" else (
            "particle-record" if field[1].startswith("particle_") else "physical-field"
        )
        records.append(
            {
                "field": list(field),
                "comparison": comparison,
                "max_absolute_error": absolute,
                "max_relative_error": relative,
                "l2_relative_error": l2_relative,
                "passed": bool(np.isfinite(relative) and relative < args.tolerance),
            }
        )

    physical = [item for item in records if item["comparison"] == "physical-field"]
    max_absolute = max(item["max_absolute_error"] for item in physical)
    max_relative = max(item["max_relative_error"] for item in physical)
    max_l2_relative = max(item["l2_relative_error"] for item in physical)
    single_invariants = _invariants(single)
    multi_invariants = _invariants(multi)
    invariant_relative_differences = {
        key: abs(multi_invariants[key] - single_invariants[key]) / max(abs(single_invariants[key]), 1.0e-300)
        for key in ("particle_weight_sum", "field_energy", "particle_kinetic_energy", "total_energy")
    }
    result = {
        "single_rank_plotfile": str(args.single_rank_plotfile),
        "multi_rank_plotfile": str(args.multi_rank_plotfile),
        "field_count": len(records),
        "max_absolute_error": max_absolute,
        "max_relative_error": max_relative,
        "max_physical_field_l2_relative_error": max_l2_relative,
        "single_rank_invariants": single_invariants,
        "multi_rank_invariants": multi_invariants,
        "invariant_relative_differences": invariant_relative_differences,
        "tolerance": args.tolerance,
        "rank_invariant_physical_fields": bool(
            np.isfinite(max_l2_relative) and max_l2_relative < args.tolerance
        ),
        "scope": "project-level reader-side comparison; not an upstream checksum replacement",
        "fields": records,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# Uniform-plasma MPI consistency report\n\n"
        f"- compared fields: `{len(records)}`\n"
        f"- maximum absolute error: `{max_absolute:.8e}`\n"
        f"- maximum physical-field pointwise relative error: `{max_relative:.8e}`\n"
        f"- maximum physical-field L2 relative error: `{max_l2_relative:.8e}`\n"
        f"- total-energy relative difference: `{invariant_relative_differences['total_energy']:.8e}`\n"
        f"- field-energy relative difference: `{invariant_relative_differences['field_energy']:.8e}`\n"
        f"- tolerance: `{args.tolerance:.3e}`\n"
        f"- rank-invariant physical-field status: `{'PASS' if result['rank_invariant_physical_fields'] else 'FAIL'}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
