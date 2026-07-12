#!/usr/bin/env python
"""Run and summarize WarpX collider-relevant diagnostics validation."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import openpmd_api as io
import pandas as pd
from scipy.constants import c


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--analysis-script", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    completed = subprocess.run(
        [sys.executable, str(Path(args.analysis_script).resolve())],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    log = completed.stdout + completed.stderr
    (root / "collider-relevant-analysis.log").write_text(log)

    collider_path = root / "diags/reducedfiles/ColliderRelevant_beam_e_beam_p.txt"
    collider = pd.read_csv(collider_path, sep=" ")
    particle_extrema = {
        species: _read_data_rows(
            root / f"diags/reducedfiles/ParticleExtrema_{species}.txt"
        )
        for species in ("beam_e", "beam_p")
    }
    dldt_openpmd = _read_openpmd_dldt(root / "diags/diag2/openpmd_%T.h5")
    dldt_reduced = collider.iloc[:, 2].to_numpy(dtype=float)
    dldt_relative_errors = [
        _relative_error(reference, observed)
        for reference, observed in zip(dldt_openpmd, dldt_reduced)
    ]

    result = {
        "run_dir": str(root),
        "mpi_processes": _read_mpi_processes(root),
        "official_analysis_exit_code": completed.returncode,
        "official_analysis_passed": completed.returncode == 0,
        "openpmd_iterations": list(range(len(dldt_openpmd))),
        "collider_relevant_rows": int(len(collider)),
        "collider_relevant_columns": int(len(collider.columns)),
        "particle_extrema_rows": particle_extrema,
        "dldt_openpmd": [float(value) for value in dldt_openpmd],
        "dldt_reduced": [float(value) for value in dldt_reduced],
        "dldt_relative_errors": dldt_relative_errors,
        "max_dldt_relative_error": max(dldt_relative_errors),
        "dldt_tolerance": 1.0e-8,
        "passed": completed.returncode == 0
        and len(dldt_openpmd) == len(dldt_reduced)
        and max(dldt_relative_errors) <= 1.0e-8,
        "contract": "official ColliderRelevant/ParticleExtrema checks plus independent openPMD dL/dt reconstruction",
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# Collider-relevant diagnostics contract report",
                "",
                f"- MPI processes: `{result['mpi_processes']}`",
                f"- openPMD iterations: `{len(result['openpmd_iterations'])}`",
                f"- ColliderRelevant rows / columns: `{result['collider_relevant_rows']} / {result['collider_relevant_columns']}`",
                f"- ParticleExtrema rows: `beam_e={particle_extrema['beam_e']}`, `beam_p={particle_extrema['beam_p']}`",
                f"- reconstructed dL/dt: `{result['dldt_openpmd'][0]:.15e}`",
                f"- maximum openPMD vs reduced dL/dt relative error: `{result['max_dldt_relative_error']:.3e}`",
                f"- official analysis result: `{'PASS' if result['official_analysis_passed'] else 'FAIL'}`",
                f"- combined contract result: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "The official WarpX test checks chi, weighted position statistics, angle extrema/statistics, ParticleExtrema, and ColliderRelevant outputs. This wrapper additionally reconstructs luminosity rate from the two openPMD charge-density meshes and compares it with the reduced diagnostic.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("collider-relevant diagnostics contract failed")


def _read_data_rows(path: Path) -> int:
    data = np.loadtxt(path)
    return int(data.shape[0]) if data.ndim > 1 else 1


def _read_openpmd_dldt(path: Path) -> list[float]:
    series = io.Series(str(path), io.Access.read_only)
    values = []
    for iteration_number in series.iterations:
        iteration = series.iterations[iteration_number]
        rho_e = iteration.meshes["rho_beam_e"][io.Mesh_Record_Component.SCALAR]
        rho_p = iteration.meshes["rho_beam_p"][io.Mesh_Record_Component.SCALAR]
        charge_e = iteration.particles["beam_e"]["charge"][
            io.Mesh_Record_Component.SCALAR
        ]
        charge_p = iteration.particles["beam_p"]["charge"][
            io.Mesh_Record_Component.SCALAR
        ]
        rho_e_data = rho_e.load_chunk()
        rho_p_data = rho_p.load_chunk()
        charge_e_data = charge_e.load_chunk()
        charge_p_data = charge_p.load_chunk()
        series.flush()
        q_e = float(charge_e_data[0])
        q_p = float(charge_p_data[0])
        if not np.all(charge_e_data == q_e) or not np.all(charge_p_data == q_p):
            raise ValueError("beam particle charges are not uniform")
        d_volume = float(np.prod(iteration.meshes["rho_beam_e"].grid_spacing))
        values.append(float(2.0 * np.sum((rho_e_data / q_e) * (rho_p_data / q_p) * d_volume * c)))
    series.close()
    return values


def _relative_error(reference: float, observed: float) -> float:
    scale = max(abs(reference), abs(observed), np.finfo(float).tiny)
    return float(abs(reference - observed) / scale)


def _read_mpi_processes(root: Path) -> int | None:
    candidates = sorted(root.glob("diags/diag*/warpx_job_info"))
    if not candidates:
        return None
    for line in candidates[-1].read_text().splitlines():
        if line.startswith("number of MPI processes:"):
            return int(line.split(":", 1)[1].strip())
    return None


if __name__ == "__main__":
    main()
