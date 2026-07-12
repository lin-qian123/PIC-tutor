#!/usr/bin/env python
"""Analyze the RZ secondary-ion-emission PICMI contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.constants import c


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--parser-root", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, str(args.parser_root))
    from input_file_parser import parse_input_file
    from openpmd_viewer import OpenPMDTimeSeries

    case_dir = args.case_dir.resolve()
    ts = OpenPMDTimeSeries(str(case_dir / "diags/diag1"))
    iteration = ts.iterations[-1]
    x, y, z, ux, uy, uz = ts.get_particle(
        ["x", "y", "z", "ux", "uy", "uz"],
        species="electrons",
        iteration=iteration,
    )
    x, y, z, ux, uy, uz = [np.asarray(v) for v in (x, y, z, ux, uy, uz)]

    inputs = parse_input_file(str(case_dir / "warpx_used_inputs"))
    radius = float(inputs["my_constants.radius"][0])
    ion_x0 = np.asarray(inputs["ions.multiple_particles_pos_x"], dtype=float)
    ion_z0 = np.asarray(inputs["ions.multiple_particles_pos_z"], dtype=float)
    ion_ux0 = np.asarray(inputs["ions.multiple_particles_ux"], dtype=float) * c
    ion_uz0 = np.asarray(inputs["ions.multiple_particles_uz"], dtype=float) * c
    gamma = np.sqrt(1.0 + (ion_ux0**2 + ion_uz0**2) / c**2)
    vx0, vz0 = ion_ux0 / gamma, ion_uz0 / gamma
    a = vx0**2 + vz0**2
    b = 2.0 * (ion_x0 * vx0 + ion_z0 * vz0)
    cc = ion_x0**2 + ion_z0**2 - radius**2
    t_impact = (-b - np.sqrt(b**2 - 4.0 * a * cc)) / (2.0 * a)
    x_impact = ion_x0 + vx0 * t_impact
    z_impact = ion_z0 + vz0 * t_impact

    gamma_e = np.sqrt(1.0 + ux**2 + uy**2 + uz**2)
    vx, vy, vz = ux * c / gamma_e, uy * c / gamma_e, uz * c / gamma_e
    distances = []
    parents = []
    for i in range(len(z)):
        candidate = np.sqrt(
            (x[i] - vx[i] * (ts.t[-1] - t_impact) - x_impact) ** 2
            + (y[i] - vy[i] * (ts.t[-1] - t_impact)) ** 2
            + (z[i] - vz[i] * (ts.t[-1] - t_impact) - z_impact) ** 2
        )
        parent = int(np.argmin(candidate))
        parents.append(parent)
        distances.append(float(candidate[parent] / radius))

    result = {
        "case": "test_rz_secondary_ion_emission_picmi",
        "iteration": int(iteration),
        "electron_count": int(len(z)),
        "expected_electron_count": 2,
        "relative_distance_to_closest_impact": distances,
        "closest_parent_ion": parents,
        "tolerance": 0.02,
        "count_pass": len(z) == 2,
        "geometry_pass": bool(distances) and max(distances) < 0.02,
        "contract_pass": len(z) == 2 and bool(distances) and max(distances) < 0.02,
        "note": "The producer emits the expected count; contract_pass records whether the official 2% back-propagated EB geometry gate passes.",
    }
    (case_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ secondary ion emission contract",
        "",
        f"- Official producer: `test_rz_secondary_ion_emission_picmi`",
        f"- Final iteration: `{iteration}`; emitted electrons: `{len(z)}` (expected `2`).",
        f"- Relative distances to closest analytical ion impact: `{[round(v, 8) for v in distances]}`; tolerance `{0.02}`.",
        f"- Contract result: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        "- The run completed and emitted the expected count, but the current checkout's EB back-propagation geometry must satisfy the 2% gate before this case can be called passing.",
    ]
    (case_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
