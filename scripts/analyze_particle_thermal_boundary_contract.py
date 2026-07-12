#!/usr/bin/env python
"""Independent reduced-energy contract for thermal particle boundaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    case_dir = args.case_dir.resolve()
    field_energy = np.loadtxt(case_dir / "diags/reducedfiles/EF.txt")
    particle_energy = np.loadtxt(case_dir / "diags/reducedfiles/EN.txt")

    ef_reference = float(field_energy[1, 2])
    ef_final = float(field_energy[-1, 2])
    en_initial = float(particle_energy[0, 2])
    en_final = float(particle_energy[-1, 2])
    ef_ratio = ef_final / ef_reference
    en_relative_drift = abs(en_final - en_initial) / en_initial
    result = {
        "case": "test_2d_particle_thermal_boundary",
        "mpi": 2,
        "steps": int(particle_energy[-1, 0]),
        "field_energy_samples": int(len(field_energy)),
        "particle_energy_samples": int(len(particle_energy)),
        "field_energy_reference_step_10": ef_reference,
        "field_energy_final": ef_final,
        "field_energy_final_over_step_10": ef_ratio,
        "particle_energy_initial": en_initial,
        "particle_energy_final": en_final,
        "particle_energy_relative_drift": en_relative_drift,
        "gates": {
            "field_energy_ratio_lt_40": bool(ef_ratio < 40.0),
            "field_energy_final_lt_5e-5": bool(ef_final < 5.0e-5),
            "particle_energy_drift_lt_2_percent": bool(en_relative_drift < 0.02),
            "all_values_finite": bool(np.all(np.isfinite(field_energy)) and np.all(np.isfinite(particle_energy))),
        },
        "passed": bool(ef_ratio < 40.0 and ef_final < 5.0e-5 and en_relative_drift < 0.02),
        "evidence_level": "independent reduced-diagnostic energy contract; not a thermal-equilibrium proof",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Thermal particle-boundary energy contract",
        "",
        "- case: `test_2d_particle_thermal_boundary`",
        "- producer: official 2D input, 2 MPI ranks, 2000 steps",
        f"- status: `{('PASS' if result['passed'] else 'FAIL')}`",
        f"- field energy step-10 reference: `{ef_reference:.12e}`",
        f"- field energy final: `{ef_final:.12e}`",
        f"- field energy final/reference: `{ef_ratio:.6f}`",
        f"- particle energy relative drift: `{en_relative_drift:.6%}`",
        "",
        "| gate | result |",
        "|---|---|",
    ]
    for name, passed in result["gates"].items():
        lines.append(f"| `{name}` | `{passed}` |")
    lines.extend(
        [
            "",
            "The contract follows the upstream analysis semantics: field energy uses the first nonzero step as its reference, while particle energy drift uses the initial reduced-diagnostic row. It is a thermal-boundary short-run stability/energy gate, not a claim of equilibrium convergence.",
        ]
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("thermal particle-boundary contract failed")


if __name__ == "__main__":
    main()
