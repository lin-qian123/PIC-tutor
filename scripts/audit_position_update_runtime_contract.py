#!/usr/bin/env python
"""Verify the explicit position-update formula against Full plotfiles."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, m_e


ROOT = Path(__file__).resolve().parents[1]
WARPX_ROOT = ROOT.parent / "warpx"
PUSHER_CASES = {
    "boris": ROOT / "runs/stage-c-validation/pusher_uniform_b_boris",
    "vay": ROOT / "runs/stage-c-validation/pusher_uniform_b_vay",
    "higuera": ROOT / "runs/stage-c-validation/pusher_uniform_b_higuera",
}


def source_contract() -> dict[str, bool]:
    update = (WARPX_ROOT / "Source/Particles/Pusher/UpdatePosition.H").read_text(encoding="utf-8")
    evolve = (WARPX_ROOT / "Source/Particles/PhysicalParticleContainer.cpp").read_text(encoding="utf-8")
    return {
        "update_position_formula": "x += ux * inv_gamma * dt" in update,
        "gamma_inverse_definition": "inv_gamma = 1._prt/std::sqrt(1._prt + u2*inv_c2)" in update,
        "full_position_push_dispatch": "position_push_type == PositionPushType::Full" in evolve,
        "position_update_call": "UpdatePosition" in evolve,
    }


def plotfiles(case_dir: Path) -> list[Path]:
    files = [
        path
        for path in (case_dir / "diags").glob("diag1*")
        if path.is_dir() and re.fullmatch(r"diag1\d+", path.name)
    ]
    return sorted(files, key=lambda path: int(path.name.removeprefix("diag1")))


def load_state(plotfile: Path) -> tuple[float, np.ndarray, np.ndarray]:
    ds = yt.load(str(plotfile))
    ad = ds.all_data()
    position = np.array(
        [
            ad["electron", "particle_position_x"].to_ndarray()[0],
            ad["electron", "particle_position_y"].to_ndarray()[0],
        ],
        dtype=float,
    )
    momentum = np.array(
        [
            ad["electron", "particle_momentum_x"].to_ndarray()[0],
            ad["electron", "particle_momentum_y"].to_ndarray()[0],
            ad["electron", "particle_momentum_z"].to_ndarray()[0],
        ],
        dtype=float,
    ) / (m_e * c)
    return float(ds.current_time), position, momentum


def analyze_case(name: str, case_dir: Path) -> dict:
    files = plotfiles(case_dir)
    states = [load_state(path) for path in files]
    errors = {"old": [], "new": [], "midpoint": []}
    for (time_old, position_old, u_old), (time_new, position_new, u_new) in zip(states, states[1:]):
        dt = time_new - time_old
        actual = position_new - position_old
        for alignment, u in (("old", u_old), ("new", u_new), ("midpoint", (u_old + u_new) / 2.0)):
            gamma_inverse = 1.0 / math.sqrt(1.0 + float(np.dot(u, u)))
            predicted = c * gamma_inverse * np.array([u[0], u[2]]) * dt
            scale = max(float(np.linalg.norm(actual)), float(np.linalg.norm(predicted)), 1.0e-30)
            errors[alignment].append(float(np.linalg.norm(actual - predicted) / scale))
    return {
        "pusher": name,
        "plotfile_count": len(files),
        "step_count": len(errors["midpoint"]),
        "max_relative_vector_error_by_alignment": {alignment: max(values) for alignment, values in errors.items()},
        "midpoint_proxy_mean_relative_error": float(np.mean(errors["midpoint"])),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    source = source_contract()
    cases = [analyze_case(name, path) for name, path in PUSHER_CASES.items()]
    max_midpoint_error = max(case["max_relative_vector_error_by_alignment"]["midpoint"] for case in cases)
    max_frame_error = max(
        case["max_relative_vector_error_by_alignment"][alignment]
        for case in cases
        for alignment in ("old", "new")
    )
    checks = {
        **source,
        "all_cases_have_81_plotfiles": all(case["plotfile_count"] == 81 for case in cases),
        "all_cases_have_80_position_steps": all(case["step_count"] == 80 for case in cases),
        "direct_frame_pairing_is_not_exact": max_frame_error > 1.0e-2,
        "midpoint_proxy_is_finite_and_bounded": max_midpoint_error < 1.0e-2,
    }
    result = {
        "contract": "explicit position update source/runtime formula contract",
        "passed": all(checks.values()),
        "classification": "POSITION_UPDATE_SOURCE_CONFIRMED_OUTPUT_STAGGERING_BOUNDARY_DIRECT_HALF_STEP_ATTRIBUTE_REMAINS",
        "formula": "x[n+1] - x[n] = c * u[n+1/2] * gamma_inverse[n+1/2] * dt",
        "checks": checks,
        "cases": cases,
        "max_midpoint_proxy_relative_vector_error": max_midpoint_error,
        "max_single_frame_pairing_relative_vector_error": max_frame_error,
        "scope": "three existing case-local uniform-B Full-plotfile series; previous, next and midpoint mechanical-momentum alignments are compared against UpdatePosition displacement",
        "boundary": "The source formula is confirmed, but neither the previous nor next Full-plotfile momentum directly reproduces the displacement. A midpoint momentum proxy is bounded at the present cadence; this does not claim a separately exposed half-step velocity attribute or reproduce a publisher figure.",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Explicit position-update source/runtime contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- maximum single-frame pairing error: `{max_frame_error:.3e}`",
        f"- maximum midpoint proxy error: `{max_midpoint_error:.3e}`",
        "- formula: `x[n+1]-x[n] = c*u[n+1/2]*gamma_inverse*dt`",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The source formula is present, but single-frame Full-plotfile momentum does not directly reproduce the displacement. The midpoint proxy is bounded, so the output staggering and direct half-step attribute remain explicit boundaries.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "classification": result["classification"], "max_midpoint_proxy_error": max_midpoint_error, "max_single_frame_error": max_frame_error}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
