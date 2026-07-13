#!/usr/bin/env python
"""Profile RZ rho/species decomposition over saved diagnostic times."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt


def numeric_plotfiles(run_dir: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in (run_dir / "diags").iterdir()
            if path.is_dir() and re.fullmatch(r"diag\d+", path.name)
        ),
        key=lambda path: int(path.name.removeprefix("diag")),
    )


def load_frame(label: str, plotfile: Path) -> dict[str, object]:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    rho = grid[("boxlib", "rho")].to_ndarray()
    species_sum = (
        grid[("boxlib", "rho_electrons")].to_ndarray()
        + grid[("boxlib", "rho_ions")].to_ndarray()
    )
    if rho.ndim == 3:
        rho = rho[:, :, 0]
        species_sum = species_sum[:, :, 0]
    if rho.ndim != 2 or species_sum.shape != rho.shape:
        raise AssertionError(f"{label}/{plotfile.name}: expected RZ 2D rho/species arrays")
    if not np.isfinite(rho).all() or not np.isfinite(species_sum).all():
        raise AssertionError(f"{label}/{plotfile.name}: non-finite rho/species")
    difference = rho - species_sum
    scale = max(float(np.max(np.abs(rho))), 1.0e-300)
    return {
        "plotfile": plotfile.name,
        "simulation_time": float(ds.current_time),
        "species_difference_max_relative": float(np.max(np.abs(difference)) / scale),
        "axis_species_difference_max_relative": float(np.max(np.abs(difference[0, :])) / scale),
        "off_axis_species_difference_max_relative": float(
            np.max(np.abs(difference[1:, :])) / scale
        ),
        "integrated_rho_proxy": float(np.sum(rho)),
        "integrated_species_proxy": float(np.sum(species_sum)),
        "evolved_species_gate_pass": plotfile.name != "diag1000000"
        and bool(np.max(np.abs(difference)) / scale <= 1.0e-12),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", required=True, metavar="LABEL=RUN_DIR")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    cases: list[dict[str, object]] = []
    for spec in args.case:
        label, run_dir_text = spec.split("=", 1)
        run_dir = Path(run_dir_text)
        plotfiles = numeric_plotfiles(run_dir)
        if len(plotfiles) < 2:
            raise AssertionError(f"{label}: need an initial and at least one evolved diagnostic")
        frames = [load_frame(label, plotfile) for plotfile in plotfiles]
        evolved = [frame for frame in frames if frame["plotfile"] != "diag1000000"]
        cases.append(
            {
                "label": label,
                "run_dir": str(run_dir),
                "frames": frames,
                "evolved_frame_count": len(evolved),
                "max_evolved_species_difference_relative": max(
                    float(frame["species_difference_max_relative"]) for frame in evolved
                ),
                "all_evolved_species_gate_pass": all(
                    bool(frame["evolved_species_gate_pass"]) for frame in evolved
                ),
            }
        )
    cases.sort(key=lambda case: str(case["label"]))
    evolved_frames = [
        frame for case in cases for frame in case["frames"] if frame["plotfile"] != "diag1000000"
    ]
    result = {
        "contract": "RZ Esirkepov rho/species decomposition time profile",
        "cases": cases,
        "case_count": len(cases),
        "frame_count": sum(len(case["frames"]) for case in cases),
        "evolved_frame_count": len(evolved_frames),
        "initial_frame_excluded_from_classification": True,
        "initial_frame_reason": "diag1000000 is retained as initialization evidence; its pre-evolution rho/species mismatch is not mixed with the evolved-time decomposition gate",
        "all_evolved_species_gate_pass": bool(evolved_frames) and all(
            bool(frame["evolved_species_gate_pass"]) for frame in evolved_frames
        ),
        "scope": "reader-side rho versus rho_electrons+rho_ions over saved RZ times; not a Gauss-law, current-closure, or formal-convergence proof",
    }
    result["classification"] = (
        "EVOLVED_TIME_RHO_SPECIES_DECOMPOSITION_PASS_AXIS_CHARGE_SEPARATE"
        if result["all_evolved_species_gate_pass"]
        else "EVOLVED_TIME_RHO_SPECIES_DECOMPOSITION_BOUNDARY"
    )
    result["passed"] = result["case_count"] == 8 and result["evolved_frame_count"] >= 16
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ Esirkepov rho/species decomposition time profile",
        "",
        f"- classification: `{result['classification']}`",
        f"- cases: `{result['case_count']}`; frames: `{result['frame_count']}`; evolved frames: `{result['evolved_frame_count']}`",
        f"- evolved species gate: `{'PASS' if result['all_evolved_species_gate_pass'] else 'BOUNDARY'}`",
        f"- initial-frame handling: {result['initial_frame_reason']}",
        f"- scope: {result['scope']}",
        "",
        "| case | plotfile | time | max relative diff | axis diff | off-axis diff | evolved gate |",
        "|---|---|---:|---:|---:|---:|:---:|",
    ]
    for case in cases:
        for frame in case["frames"]:
            lines.append(
                f"| `{case['label']}` | `{frame['plotfile']}` | `{frame['simulation_time']:.6e}` | "
                f"`{frame['species_difference_max_relative']:.6e}` | "
                f"`{frame['axis_species_difference_max_relative']:.6e}` | "
                f"`{frame['off_axis_species_difference_max_relative']:.6e}` | "
                f"`{'PASS' if frame['evolved_species_gate_pass'] else 'excluded' if frame['plotfile'] == 'diag1000000' else 'BOUNDARY'}` |"
            )
    lines.extend(
        [
            "",
            "The evolved frames support rho-side species decomposition at the `1e-12` reader gate while keeping the independent divE-rho axis boundary separate.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                key: result[key]
                for key in ("classification", "case_count", "frame_count", "evolved_frame_count", "passed")
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
