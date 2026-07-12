#!/usr/bin/env python
"""Summarize particle and field-energy invariants for a uniform-plasma run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, epsilon_0, m_e, mu_0


def summarize(path: str) -> dict[str, float | str]:
    ds = yt.load(path)
    data = ds.all_data()
    cell_volume = float(np.prod(ds.domain_width) / np.prod(ds.domain_dimensions))
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
        "path": str(Path(path)),
        "time": float(ds.current_time.to_value()),
        "particle_count": int(weights.size),
        "particle_weight_sum": float(np.sum(weights)),
        "field_energy": float(field_energy),
        "particle_kinetic_energy": particle_kinetic,
        "total_energy": float(field_energy + particle_kinetic),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfiles", nargs="+", help="plotfiles in chronological order")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    snapshots = [summarize(path) for path in args.plotfiles]
    initial = snapshots[0]
    final = snapshots[-1]
    result = {"initial": initial, "final": final, "snapshots": snapshots}
    for key in ("particle_weight_sum", "field_energy", "particle_kinetic_energy", "total_energy"):
        denominator = abs(initial[key])
        result[f"{key}_relative_change"] = (
            float(abs(final[key] - initial[key]) / denominator) if denominator else None
        )
        result[f"{key}_max_absolute_relative_change"] = max(
            (
                abs(snapshot[key] - initial[key]) / denominator
                for snapshot in snapshots
            ),
            default=None,
        ) if denominator else None

    def display_change(key: str) -> str:
        value = result[f"{key}_relative_change"]
        return f"{value:.3e}" if value is not None else "undefined (zero baseline)"

    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# Uniform-plasma conservation report",
                "",
                f"- initial particle count: `{initial['particle_count']}`",
                f"- final particle count: `{final['particle_count']}`",
                f"- particle-weight relative change: `{display_change('particle_weight_sum')}`",
                f"- field-energy relative change: `{display_change('field_energy')}`",
                f"- particle-kinetic relative change: `{display_change('particle_kinetic_energy')}`",
                f"- total-energy relative change: `{display_change('total_energy')}`",
                f"- maximum absolute total-energy relative change: `{display_change('total_energy_max_absolute')}`",
                "",
                "The report is a reader-side diagnostic summary. It does not replace WarpX's checksum regression or assert thermal-equilibrium energy conservation by itself.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
