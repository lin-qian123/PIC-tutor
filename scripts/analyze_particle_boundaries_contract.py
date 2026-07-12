#!/usr/bin/env python
"""Independent analytic contract for the 3D particle-boundary case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, m_e


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def wrap(value: np.ndarray) -> np.ndarray:
    result = value.copy()
    result[result < -1.0] += 2.0
    result[result > 1.0] -= 2.0
    return result


def reflect(value: np.ndarray) -> np.ndarray:
    result = value.copy()
    result[result < -1.0] = -2.0 - result[result < -1.0]
    result[result > 1.0] = 2.0 - result[result > 1.0]
    return result


def main() -> None:
    args = parse_args()
    case_dir = args.case_dir.resolve()
    final_path = case_dir / "diags/diag1000008"
    initial_path = case_dir / "diags/diag1000000"
    initial = yt.load(initial_path).all_data()
    final_ds = yt.load(final_path)
    final = final_ds.all_data()
    time = float(final_ds.current_time)

    def values(data, species, field):
        return np.asarray(data[species, field].v)

    reflect_id0 = values(initial, "reflecting_particles", "particle_id")
    reflect_id = values(final, "reflecting_particles", "particle_id")
    periodic_id0 = values(initial, "periodic_particles", "particle_id")
    periodic_id = values(final, "periodic_particles", "particle_id")
    reflect_order0 = np.argsort(reflect_id0)
    reflect_order = np.argsort(reflect_id)
    periodic_order0 = np.argsort(periodic_id0)
    periodic_order = np.argsort(periodic_id)

    ux0 = values(initial, "reflecting_particles", "particle_momentum_x")[reflect_order0] / (m_e * c)
    ux = values(final, "reflecting_particles", "particle_momentum_x")[reflect_order] / (m_e * c)
    x0 = values(initial, "reflecting_particles", "particle_position_x")[reflect_order0]
    x = values(final, "reflecting_particles", "particle_position_x")[reflect_order]
    vx0 = ux0 / np.sqrt(1.0 + ux0**2) * c
    x_expected = reflect(x0 + vx0 * time)

    uz0 = values(initial, "periodic_particles", "particle_momentum_z")[periodic_order0] / (m_e * c)
    uz = values(final, "periodic_particles", "particle_momentum_z")[periodic_order] / (m_e * c)
    z0 = values(initial, "periodic_particles", "particle_position_z")[periodic_order0]
    z = values(final, "periodic_particles", "particle_position_z")[periodic_order]
    vz0 = uz0 / np.sqrt(1.0 + uz0**2) * c
    z_expected = wrap(z0 + vz0 * time)

    reflecting_position_error = float(np.max(np.abs(x - x_expected)))
    periodic_position_error = float(np.max(np.abs(z - z_expected)))
    reflecting_velocity_error = float(np.max(np.abs(ux + ux0)))
    periodic_velocity_error = float(np.max(np.abs(uz - uz0)))
    absorbing_count = int(len(values(final, "absorbing_particles", "particle_id")))

    gates = {
        "reflecting_position_abs": reflecting_position_error <= 1e-15,
        "periodic_position_abs": periodic_position_error <= 1e-15,
        "reflecting_velocity_abs": reflecting_velocity_error <= 1e-15,
        "periodic_velocity_abs": periodic_velocity_error <= 1e-15,
        "absorbing_remaining_count": absorbing_count == 1,
    }
    result = {
        "case": "test_3d_particle_boundaries",
        "mpi": 2,
        "time": time,
        "counts": {
            "reflecting_initial": int(len(reflect_id0)),
            "reflecting_final": int(len(reflect_id)),
            "absorbing_initial": int(len(values(initial, "absorbing_particles", "particle_id"))),
            "absorbing_final": absorbing_count,
            "periodic_initial": int(len(periodic_id0)),
            "periodic_final": int(len(periodic_id)),
        },
        "errors": {
            "reflecting_position_abs": reflecting_position_error,
            "periodic_position_abs": periodic_position_error,
            "reflecting_velocity_normalized_abs": reflecting_velocity_error,
            "periodic_velocity_normalized_abs": periodic_velocity_error,
        },
        "gates": gates,
        "passed": all(gates.values()),
        "evidence_level": "independent analytic reader-side contract for reflecting/absorbing/periodic particle boundaries",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Particle domain-boundary contract",
        "",
        "- case: `test_3d_particle_boundaries`",
        "- producer: official 3D input, 2 MPI ranks",
        f"- status: `{('PASS' if result['passed'] else 'FAIL')}`",
        f"- simulation time: `{time:.16e}`",
        "",
        "| contract | observed error/count | gate |",
        "|---|---:|---|",
        f"| reflecting position | `{reflecting_position_error:.3e}` | `{gates['reflecting_position_abs']}` |",
        f"| periodic position | `{periodic_position_error:.3e}` | `{gates['periodic_position_abs']}` |",
        f"| reflecting velocity sign flip | `{reflecting_velocity_error:.3e}` | `{gates['reflecting_velocity_abs']}` |",
        f"| periodic velocity preservation | `{periodic_velocity_error:.3e}` | `{gates['periodic_velocity_abs']}` |",
        f"| absorbing remaining count | `{absorbing_count}` | `{gates['absorbing_remaining_count']}` |",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("particle boundary contract failed")


if __name__ == "__main__":
    main()
