#!/usr/bin/env python
"""Independent analytic contract for the RZ PICMI EB mirror-reflection case."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries
from scipy.constants import c


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--parser-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sys.path.insert(0, str(args.parser_root.resolve()))
    from input_file_parser import parse_input_file

    case_dir = args.case_dir.resolve()
    input_values = parse_input_file(str(case_dir / "warpx_used_inputs"))
    ts = OpenPMDTimeSeries(str(case_dir / "diags/diag1"))
    iteration = int(ts.iterations[-1])
    x, y, z = ts.get_particle(["x", "y", "z"], species="electrons", iteration=iteration)
    x = float(np.asarray(x)[0])
    y = float(np.asarray(y)[0])
    z = float(np.asarray(z)[0])

    radius = float(input_values["my_constants.radius"][0])
    x0 = float(input_values["electrons.multiple_particles_pos_x"][0])
    z0 = float(input_values["electrons.multiple_particles_pos_z"][0])
    ux0 = float(input_values["electrons.multiple_particles_ux"][0]) * c
    uz0 = float(input_values["electrons.multiple_particles_uz"][0]) * c
    gamma = np.sqrt(1.0 + (ux0**2 + uz0**2) / c**2)
    vx0, vz0 = ux0 / gamma, uz0 / gamma
    a = vx0**2 + vz0**2
    b = 2.0 * (x0 * vx0 + z0 * vz0)
    q = x0**2 + z0**2 - radius**2
    t_impact = (-b - np.sqrt(b**2 - 4.0 * a * q)) / (2.0 * a)
    x_impact, z_impact = x0 + vx0 * t_impact, z0 + vz0 * t_impact
    nx, nz = x_impact / radius, z_impact / radius
    dot = vx0 * nx + vz0 * nz
    vx_reflected, vz_reflected = vx0 - 2.0 * dot * nx, vz0 - 2.0 * dot * nz
    remaining = float(ts.t[-1] - t_impact)
    x_expected = x_impact + vx_reflected * remaining
    z_expected = z_impact + vz_reflected * remaining
    x_error = abs(x - x_expected) / abs(x_expected)
    z_error = abs(z - z_expected) / abs(z_expected)

    result = {
        "case": "test_rz_particle_boundary_interaction_picmi",
        "mpi": 2,
        "iteration": iteration,
        "diagnostic_time": float(ts.t[-1]),
        "radius": radius,
        "numerical": {"x": x, "y": y, "z": z},
        "analytic": {"x": float(x_expected), "y": 0.0, "z": float(z_expected)},
        "relative_errors": {"x": float(x_error), "z": float(z_error), "y_abs": abs(y)},
        "gates": {
            "x_relative_lt_2_percent": bool(x_error < 0.02),
            "z_relative_lt_2_percent": bool(z_error < 0.02),
            "y_abs_lt_1e-8": bool(abs(y) < 1e-8),
        },
        "passed": bool(x_error < 0.02 and z_error < 0.02 and abs(y) < 1e-8),
        "evidence_level": "independent openPMD/PICMI analytic mirror-reflection contract",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# RZ PICMI particle-boundary interaction contract",
        "",
        "- case: `test_rz_particle_boundary_interaction_picmi`",
        "- producer: Python-enabled WarpX RZ build, 2 MPI ranks, 23 steps",
        f"- status: `{('PASS' if result['passed'] else 'FAIL')}`",
        f"- numerical `(x,y,z)`: `({x:.8f}, {y:.3e}, {z:.8f})`",
        f"- analytic `(x,y,z)`: `({x_expected:.8f}, 0, {z_expected:.8f})`",
        f"- relative x error: `{x_error:.6%}`",
        f"- relative z error: `{z_error:.6%}`",
        "",
        "| gate | result |",
        "|---|---|",
    ]
    for name, passed in result["gates"].items():
        lines.append(f"| `{name}` | `{passed}` |")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("RZ particle-boundary interaction contract failed")


if __name__ == "__main__":
    main()
