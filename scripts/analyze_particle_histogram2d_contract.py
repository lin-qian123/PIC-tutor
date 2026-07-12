#!/usr/bin/env python
"""Run the laser-ion analysis and summarize ParticleHistogram2D output."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--analysis-script", required=True)
    parser.add_argument("--analysis-arg", default="diags/diagInst/")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    completed = subprocess.run(
        [
            sys.executable,
            str(Path(args.analysis_script).resolve()),
            args.analysis_arg,
        ],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    (root / "particle-histogram2d-analysis.log").write_text(
        completed.stdout + completed.stderr
    )

    histograms = {}
    for name in ("PhaseSpaceIons", "PhaseSpaceElectrons"):
        path = root / f"diags/reducedfiles/{name}"
        series = OpenPMDTimeSeries(str(path))
        entries = []
        for iteration in series.iterations:
            data, info = series.get_field("data", iteration=int(iteration))
            axes = {str(key): value for key, value in info.axes.items()}
            axis_values = {
                axis: np.asarray(getattr(info, axis), dtype=float)
                for axis in axes.values()
            }
            entries.append(
                {
                    "iteration": int(iteration),
                    "shape": [int(value) for value in data.shape],
                    "axes": axes,
                    "axis_ranges": {
                        axis: [float(values[0]), float(values[-1])]
                        for axis, values in axis_values.items()
                    },
                    "finite": bool(np.isfinite(data).all()),
                    "nonzero_cells": int(np.count_nonzero(data)),
                    "sum": float(np.sum(data)),
                    "maximum": float(np.max(data)),
                }
            )
        histograms[name] = {
            "iterations": [entry["iteration"] for entry in entries],
            "entries": entries,
            "text_sidecar_bytes": (root / f"diags/reducedfiles/{name}.txt").stat().st_size,
        }

    result = {
        "run_dir": str(root),
        "mpi_processes": _read_mpi_processes(root),
        "official_analysis_exit_code": completed.returncode,
        "official_analysis_passed": completed.returncode == 0,
        "histograms": histograms,
        "configured_bin_contract": _read_bin_contract(root / "warpx_used_inputs"),
        "passed": completed.returncode == 0 and _histogram_gate(histograms),
        "contract": "official laser-ion time-average check plus ParticleHistogram2D openPMD shape/axis/finite-data contract",
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# ParticleHistogram2D contract report",
                "",
                f"- MPI processes: `{result['mpi_processes']}`",
                f"- official laser-ion analysis: `{'PASS' if result['official_analysis_passed'] else 'FAIL'}`",
                "- histogram series: `PhaseSpaceIons`, `PhaseSpaceElectrons`",
                "- iterations: `0, 100`",
                "- shape: `1000 x 1000` for each series",
                "- axes: ordinate `uz`, abscissa `z`",
                f"- `.txt` sidecars: ions `{histograms['PhaseSpaceIons']['text_sidecar_bytes']} bytes`, electrons `{histograms['PhaseSpaceElectrons']['text_sidecar_bytes']} bytes`",
                f"- combined writer contract: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "ParticleHistogram2D writes an openPMD series under the reduced-diagnostics directory; it does not use the ordinary one-line text schema. The empty `.txt` companions therefore record the bypassed text path, while the BP5 series carries the 2D data and axis metadata.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("ParticleHistogram2D contract failed")


def _histogram_gate(histograms: dict) -> bool:
    for value in histograms.values():
        if value["iterations"] != [0, 100] or value["text_sidecar_bytes"] != 0:
            return False
        for entry in value["entries"]:
            if entry["shape"] != [1000, 1000] or not entry["finite"]:
                return False
            if entry["axes"] != {"0": "uz", "1": "z"}:
                return False
            if entry["nonzero_cells"] == 0 or entry["maximum"] <= 0:
                return False
    return True


def _read_bin_contract(path: Path) -> dict:
    text = path.read_text() if path.exists() else ""
    result = {}
    for name in ("PhaseSpaceIons", "PhaseSpaceElectrons"):
        result[name] = {
            key: int(value)
            for key, value in re.findall(
                rf"^{name}\.bin_number_(abs|ord)\s*=\s*(\d+)",
                text,
                re.MULTILINE,
            )
        }
    return result


def _read_mpi_processes(root: Path) -> int | None:
    candidates = sorted(root.glob("diags/diag*/warpx_job_info"))
    if not candidates:
        candidates = sorted(root.glob("diags/diagInst/warpx_job_info"))
    if not candidates:
        input_path = root / "warpx_used_inputs"
        if not input_path.exists():
            input_path = root / "inputs_test"
        match = re.search(r"^warpx\.numprocs\s*=\s*(.+)$", input_path.read_text(), re.MULTILINE)
        if match:
            values = [int(value) for value in match.group(1).split("#", 1)[0].split()]
            return int(np.prod(values))
        return None
    for line in candidates[-1].read_text().splitlines():
        if line.startswith("number of MPI processes:"):
            return int(line.split(":", 1)[1].strip())
    return None


if __name__ == "__main__":
    main()
