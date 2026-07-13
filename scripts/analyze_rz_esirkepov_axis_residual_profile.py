#!/usr/bin/env python
"""Profile the RZ Esirkepov divE-rho residual by radial cell."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import epsilon_0


def analyze_case(label: str, run_dir: Path, plotfile: str) -> dict[str, object]:
    inputs = (run_dir / "warpx_used_inputs").read_text(encoding="utf-8")
    correction = re.search(r"^boundary\.verboncoeur_axis_correction\s*=\s*(\S+)", inputs, re.MULTILINE)
    shape = re.search(r"^algo\.particle_shape\s*=\s*(\S+)", inputs, re.MULTILINE)
    if not shape:
        raise AssertionError(f"{label}: missing particle-shape input")
    ds = yt.load(str(run_dir / plotfile))
    data = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    rho = data[("boxlib", "rho")].to_ndarray()
    div_e = data[("boxlib", "divE")].to_ndarray()
    if rho.ndim == 3:
        rho = rho[:, :, 0]
        div_e = div_e[:, :, 0]
    if rho.ndim != 2 or div_e.shape != rho.shape:
        raise AssertionError(f"{label}: expected RZ 2D rho/divE arrays, got {rho.shape}/{div_e.shape}")
    if not np.isfinite(rho).all() or not np.isfinite(div_e).all():
        raise AssertionError(f"{label}: non-finite rho/divE")
    residual = np.abs(div_e - rho / epsilon_0)
    scale = float(np.max(np.abs(rho / epsilon_0)))
    if scale == 0.0:
        raise AssertionError(f"{label}: zero rho normalization scale")
    normalized = residual / scale
    radial_max = np.max(normalized, axis=1)
    max_index = np.unravel_index(int(np.argmax(normalized)), normalized.shape)
    off_axis = radial_max[2:] if len(radial_max) > 2 else np.array([], dtype=float)
    return {
        "label": label,
        "run_dir": str(run_dir),
        "plotfile": plotfile,
        "resolution": [int(v) for v in ds.domain_dimensions[:2]],
        "particle_shape": int(shape.group(1)),
        "axis_correction": correction.group(1).lower() if correction else "default",
        "normalization_scale": scale,
        "axis_r0_max": float(radial_max[0]),
        "near_axis_r1_max": float(radial_max[1]),
        "off_axis_r2_plus_max": float(np.max(off_axis)) if off_axis.size else 0.0,
        "radial_max_first_eight": [float(v) for v in radial_max[:8]],
        "max_location": {"r_index": int(max_index[0]), "z_index": int(max_index[1])},
        "axis_dominant": bool(radial_max[0] >= np.max(radial_max[1:])),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", required=True, metavar="LABEL=RUN_DIR")
    parser.add_argument("--plotfile", default="diags/diag1000080")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    cases = []
    for spec in args.case:
        label, run_dir = spec.split("=", 1)
        cases.append(analyze_case(label, Path(run_dir), args.plotfile))
    cases.sort(key=lambda case: case["label"])
    result = {
        "contract": "RZ Esirkepov radial divE-rho residual profile",
        "cases": cases,
        "all_axis_dominant": all(case["axis_dominant"] for case in cases),
        "scope": "reader-side same-surface divE-rho/epsilon0 profile; not a kernel root-cause proof or formal convergence study",
        "classification": (
            "AXIS_DOMINATED_READER_SIDE_RESIDUAL_PROFILE"
            if all(case["axis_dominant"] for case in cases)
            else "RADIAL_RESIDUAL_PROFILE_AXIS_DOMINANCE_NOT_UNIFORM"
        ),
    }
    result["passed"] = bool(result["cases"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ Esirkepov radial divE-rho residual profile",
        "",
        f"- classification: `{result['classification']}`",
        f"- all cases axis dominant: `{'PASS' if result['all_axis_dominant'] else 'BOUNDARY'}`",
        f"- scope: {result['scope']}",
        "",
        "| case | correction | shape | resolution | r=0 | r=1 | r>=2 | max location |",
        "|---|:---:|---:|---|---:|---:|---:|---|",
    ]
    for case in cases:
        location = case["max_location"]
        lines.append(
            f"| `{case['label']}` | `{case['axis_correction']}` | `{case['particle_shape']}` | "
            f"`{case['resolution'][0]}x{case['resolution'][1]}` | `{case['axis_r0_max']:.6e}` | "
            f"`{case['near_axis_r1_max']:.6e}` | `{case['off_axis_r2_plus_max']:.6e}` | "
            f"`r={location['r_index']}, z={location['z_index']}` |"
        )
    lines.extend(
        [
            "",
            "The profile localizes the reader-side maximum by radial cell; it does not identify whether the contribution comes from axis volume scaling, staggering/interpolation, mode handling, or the deposition kernel.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("classification", "all_axis_dominant", "passed")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
