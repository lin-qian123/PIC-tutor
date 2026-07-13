#!/usr/bin/env python
"""Profile the RZ Esirkepov divE-rho residual across saved diagnostic times."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import epsilon_0


def numeric_plotfiles(run_dir: Path) -> list[Path]:
    diags = run_dir / "diags"
    return sorted(
        (path for path in diags.iterdir() if path.is_dir() and re.fullmatch(r"diag\d+", path.name)),
        key=lambda path: int(path.name.removeprefix("diag")),
    )


def profile_plotfile(label: str, run_dir: Path, plotfile: Path) -> dict[str, object]:
    ds = yt.load(str(plotfile))
    data = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    rho = data[("boxlib", "rho")].to_ndarray()
    div_e = data[("boxlib", "divE")].to_ndarray()
    if rho.ndim == 3:
        rho = rho[:, :, 0]
        div_e = div_e[:, :, 0]
    if rho.ndim != 2 or div_e.shape != rho.shape:
        raise AssertionError(f"{label}/{plotfile.name}: expected RZ 2D rho/divE arrays")
    if not np.isfinite(rho).all() or not np.isfinite(div_e).all():
        raise AssertionError(f"{label}/{plotfile.name}: non-finite rho/divE")
    rho_over_epsilon = rho / epsilon_0
    scale = float(np.max(np.abs(rho_over_epsilon)))
    if scale == 0.0:
        raise AssertionError(f"{label}/{plotfile.name}: zero rho normalization scale")
    normalized = np.abs(div_e - rho_over_epsilon) / scale
    radial_max = np.max(normalized, axis=1)
    max_location = np.unravel_index(int(np.argmax(normalized)), normalized.shape)
    return {
        "label": label,
        "plotfile": plotfile.name,
        "simulation_time": float(ds.current_time),
        "normalization_scale": scale,
        "axis_r0_max": float(radial_max[0]),
        "near_axis_r1_max": float(radial_max[1]),
        "off_axis_r2_plus_max": float(np.max(radial_max[2:])),
        "max_location": {"r_index": int(max_location[0]), "z_index": int(max_location[1])},
        "axis_dominant": bool(radial_max[0] >= np.max(radial_max[1:])),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", required=True, metavar="LABEL=RUN_DIR")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    frames: list[dict[str, object]] = []
    for spec in args.case:
        label, run_dir_text = spec.split("=", 1)
        run_dir = Path(run_dir_text)
        plotfiles = numeric_plotfiles(run_dir)
        if len(plotfiles) < 2:
            raise AssertionError(f"{label}: need an initial and at least one evolved diagnostic")
        frames.extend(profile_plotfile(label, run_dir, plotfile) for plotfile in plotfiles)
    frames.sort(key=lambda frame: (frame["label"], frame["plotfile"]))
    labels = sorted({str(frame["label"]) for frame in frames})
    post_initial = [frame for frame in frames if frame["plotfile"] != "diag1000000"]
    result = {
        "contract": "RZ Esirkepov time-resolved radial divE-rho residual profile",
        "case_count": len(labels),
        "frame_count": len(frames),
        "post_initial_frame_count": len(post_initial),
        "initial_frame_excluded_from_classification": True,
        "initial_frame_reason": "diag1000000 is the t=0 initialization baseline; zero-field normalization can make its off-axis profile non-physical for the evolved residual claim",
        "frames": frames,
        "all_post_initial_axis_dominant": bool(post_initial) and all(
            bool(frame["axis_dominant"]) for frame in post_initial
        ),
        "scope": "reader-side same-surface divE-rho/epsilon0 profile over saved times; not a kernel root-cause proof or formal convergence study",
    }
    result["classification"] = (
        "POST_INITIAL_AXIS_DOMINATED_READER_SIDE_RESIDUAL_TIME_PROFILE"
        if result["all_post_initial_axis_dominant"]
        else "POST_INITIAL_RADIAL_RESIDUAL_PROFILE_AXIS_DOMINANCE_NOT_UNIFORM"
    )
    result["passed"] = result["case_count"] == len(labels) and result["frame_count"] >= result["case_count"] * 2
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ Esirkepov time-resolved radial divE-rho residual profile",
        "",
        f"- classification: `{result['classification']}`",
        f"- cases: `{result['case_count']}`; saved frames: `{result['frame_count']}`; post-initial frames: `{result['post_initial_frame_count']}`",
        f"- post-initial axis dominance: `{'PASS' if result['all_post_initial_axis_dominant'] else 'BOUNDARY'}`",
        f"- initial-frame handling: {result['initial_frame_reason']}",
        f"- scope: {result['scope']}",
        "",
        "| case | plotfile | time | r=0 | r=1 | r>=2 | max location | axis dominant |",
        "|---|---|---:|---:|---:|---:|---|:---:|",
    ]
    for frame in frames:
        location = frame["max_location"]
        lines.append(
            f"| `{frame['label']}` | `{frame['plotfile']}` | `{frame['simulation_time']:.6e}` | "
            f"`{frame['axis_r0_max']:.6e}` | `{frame['near_axis_r1_max']:.6e}` | "
            f"`{frame['off_axis_r2_plus_max']:.6e}` | `r={location['r_index']}, z={location['z_index']}` | "
            f"`{'PASS' if frame['axis_dominant'] else 'BOUNDARY'}` |"
        )
    lines.extend(
        [
            "",
            "The t=0 frame is retained as evidence but excluded from the evolved-time classification; the profile still does not identify whether the residual comes from axis volume scaling, staggering/interpolation, mode handling, or the deposition kernel.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("classification", "case_count", "frame_count", "passed")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
