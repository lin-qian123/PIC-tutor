#!/usr/bin/env python
"""Independent histogram-tail contract for the absorbing-boundary case."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries


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
    ts = OpenPMDTimeSeries(str(case_dir / "diags/reducedfiles/PhaseSpaceElectrons"))
    iteration = 8000
    data, _ = ts.get_field(field="data", iteration=iteration, plot=False)
    data = np.asarray(data)

    nz = int(input_values["PhaseSpaceElectrons.bin_number_abs"][0])
    zmin = float(input_values["PhaseSpaceElectrons.bin_min_abs"][0])
    zmax = float(input_values["PhaseSpaceElectrons.bin_max_abs"][0])
    nuz = int(input_values["PhaseSpaceElectrons.bin_number_ord"][0])
    uzmin = float(input_values["PhaseSpaceElectrons.bin_min_ord"][0])
    uzmax = float(input_values["PhaseSpaceElectrons.bin_max_ord"][0])

    region_z = (0.0, 50.0e-6)
    region_uz = (-5.0, -1.0)
    ilo = int(np.ceil((region_uz[0] - uzmin) / (uzmax - uzmin) * nuz))
    ihi = int(np.ceil((region_uz[1] - uzmin) / (uzmax - uzmin) * nuz))
    jlo = int(np.ceil((region_z[0] - zmin) / (zmax - zmin) * nz))
    jhi = int(np.ceil((region_z[1] - zmin) / (zmax - zmin) * nz))
    tail_weight = float(data[ilo:ihi, jlo:jhi].sum())
    result = {
        "case": "test_1d_particle_absorbing_boundary",
        "mpi": 1,
        "iteration": iteration,
        "available_iterations": ts.iterations.tolist(),
        "histogram_shape": list(data.shape),
        "bin_shape_from_inputs": [nuz, nz],
        "region_z": list(region_z),
        "region_uz": list(region_uz),
        "selected_bin_window": {"uz": [ilo, ihi], "z": [jlo, jhi]},
        "region_weight": tail_weight,
        "region_weight_limit": 3.2e20,
        "total_histogram_weight": float(data.sum()),
        "gates": {
            "iteration_8000_present": iteration in ts.iterations,
            "histogram_shape_matches_inputs": tuple(data.shape) == (nuz, nz),
            "all_values_finite": bool(np.all(np.isfinite(data))),
            "tail_weight_below_limit": tail_weight < 3.2e20,
        },
        "passed": bool(
            iteration in ts.iterations
            and tuple(data.shape) == (nuz, nz)
            and np.all(np.isfinite(data))
            and tail_weight < 3.2e20
        ),
        "evidence_level": "independent ParticleHistogram2D tail-weight contract; not a full thermalizer distribution proof",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Absorbing particle-boundary histogram contract",
        "",
        "- case: `test_1d_particle_absorbing_boundary`",
        "- producer: official 1D input, 1 MPI rank, 8000 steps",
        f"- status: `{('PASS' if result['passed'] else 'FAIL')}`",
        f"- histogram shape: `{tuple(data.shape)}`",
        f"- selected region: `z=[0,50] um`, `uz=[-5,-1]`",
        f"- selected region weight: `{tail_weight:.12e}`",
        f"- limit: `{3.2e20:.12e}`",
        "",
        "| gate | result |",
        "|---|---|",
    ]
    for name, passed in result["gates"].items():
        lines.append(f"| `{name}` | `{passed}` |")
    lines.extend(
        [
            "",
            "The input parser values are read from the produced `warpx_used_inputs`, so the bin-window calculation follows the active runtime bin contract rather than hard-coding array indices.",
        ]
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("absorbing particle-boundary contract failed")


if __name__ == "__main__":
    main()
