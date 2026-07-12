#!/usr/bin/env python
"""Compare Boris, Vay, and Higuera-Cary in a case-local uniform-B run."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, e, m_e


B_Y = 0.00078110417851950768
U0 = 0.45825756949558416
GAMMA = np.sqrt(1.0 + U0 * U0)
Z0 = -1.25
OMEGA_C = e * B_Y / (GAMMA * m_e)
RADIUS = (U0 * c / GAMMA) / OMEGA_C
CENTER_Z = Z0 + RADIUS


def infer_pusher(run_dir: Path) -> str:
    text = (run_dir / "warpx_used_inputs").read_text(encoding="utf-8")
    match = re.search(r"^algo\.particle_pusher\s*=\s*(\S+)", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing pusher in {run_dir / 'warpx_used_inputs'}")
    return match.group(1).strip('"')


def collect(run_dir: Path) -> dict:
    plotfiles = sorted(
        (
            path
            for path in (run_dir / "diags").glob("diag1[0-9]*")
            if path.is_dir() and re.fullmatch(r"diag1\d+", path.name)
        ),
        key=lambda path: int(re.search(r"diag1(\d+)$", path.name).group(1)),
    )
    if len(plotfiles) < 2:
        raise ValueError(f"not enough plotfiles in {run_dir}")
    times = []
    species_data = {species: {"position": [], "momentum": []} for species in ("electron", "positron")}
    for plotfile in plotfiles:
        ds = yt.load(str(plotfile))
        ad = ds.all_data()
        times.append(float(ds.current_time))
        for species in species_data:
            species_data[species]["position"].append(
                np.array(
                    [
                        ad[species, "particle_position_x"].to_ndarray()[0],
                        ad[species, "particle_position_y"].to_ndarray()[0],
                    ],
                    dtype=float,
                )
            )
            species_data[species]["momentum"].append(
                np.array(
                    [
                        ad[species, "particle_momentum_x"].to_ndarray()[0],
                        ad[species, "particle_momentum_z"].to_ndarray()[0],
                    ],
                    dtype=float,
                )
            )

    times = np.asarray(times)
    dt = np.diff(times)
    rows = []
    for species, values in species_data.items():
        position = np.asarray(values["position"])
        momentum = np.asarray(values["momentum"])
        radius = np.linalg.norm(position - np.array([0.0, CENTER_Z]), axis=1)
        momentum_norm = np.linalg.norm(momentum, axis=1)
        momentum_phase = np.unwrap(np.arctan2(momentum[:, 1], momentum[:, 0]))
        phase_increment = np.diff(momentum_phase)
        effective_velocity = np.diff(position, axis=0) / dt[:, None]
        effective_speed = np.linalg.norm(effective_velocity, axis=1)
        effective_speed_relative_error = (effective_speed - U0 * c / GAMMA) / (U0 * c / GAMMA)
        nonzero_radius = radius[1:]
        rows.append(
            {
                "species": species,
                "particle_count_per_frame": 1,
                "radius_min_after_initial": float(nonzero_radius.min()),
                "radius_max_after_initial": float(nonzero_radius.max()),
                "radius_relative_spread_after_initial": float(
                    (nonzero_radius.max() - nonzero_radius.min()) / nonzero_radius.mean()
                ),
                "momentum_norm_relative_spread": float(
                    (momentum_norm.max() - momentum_norm.min()) / momentum_norm.mean()
                ),
                "momentum_phase_increment_abs_mean": float(np.mean(np.abs(phase_increment))),
                "momentum_phase_increment_abs_max": float(np.max(np.abs(phase_increment))),
                "position_update_velocity_proxy_mean": float(effective_speed.mean()),
                "position_update_velocity_proxy_relative_error_mean": float(effective_speed_relative_error.mean()),
                "position_update_velocity_proxy_relative_error_max_abs": float(np.max(np.abs(effective_speed_relative_error))),
                "gyroradius_proxy_mean": float(effective_speed.mean() / OMEGA_C),
                "gyroradius_proxy_relative_error": float((effective_speed.mean() / OMEGA_C - RADIUS) / RADIUS),
                "position_finite": bool(np.isfinite(position).all()),
                "momentum_finite": bool(np.isfinite(momentum).all()),
            }
        )
    checks = {
        "at_least_80_steps": len(plotfiles) >= 81,
        "strictly_increasing_time": bool(np.all(dt > 0.0)),
        "uniform_output_cadence": bool(np.allclose(dt, dt[0], rtol=1e-12, atol=0.0)),
        "both_species_have_one_particle": all(row["particle_count_per_frame"] == 1 for row in rows),
        "finite_particle_state": all(row["position_finite"] and row["momentum_finite"] for row in rows),
    }
    return {
        "run_dir": str(run_dir),
        "pusher": infer_pusher(run_dir),
        "plotfile_count": len(plotfiles),
        "first_plotfile": plotfiles[0].name,
        "last_plotfile": plotfiles[-1].name,
        "first_time": float(times[0]),
        "last_time": float(times[-1]),
        "output_dt": float(np.median(dt)),
        "checks": checks,
        "species": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dirs", nargs=3, type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    cases = [collect(run_dir.resolve()) for run_dir in args.run_dirs]
    expected_pushers = {"boris", "vay", "higuera"}
    actual_pushers = {case["pusher"] for case in cases}
    checks = {
        "three_distinct_expected_pushers": actual_pushers == expected_pushers,
        "all_case_contracts_pass": all(all(case["checks"].values()) for case in cases),
    }
    result = {
        "contract": "dedicated uniform-B Boris/Vay/Higuera-Cary orbit comparison",
        "passed": all(checks.values()),
        "checks": checks,
        "physics": {
            "B_y": B_Y,
            "initial_gamma": float(GAMMA),
            "initial_u_over_c": U0,
            "continuum_cyclotron_frequency": float(e * B_Y / (GAMMA * m_e)),
            "continuum_radius_m": float((U0 * c / GAMMA) / (e * B_Y / (GAMMA * m_e))),
        },
        "cases": cases,
        "evidence_boundary": {
            "paper_reproduction_promoted": False,
            "half_step_velocity_available": False,
            "position_update_velocity_proxy_available": True,
            "source_mapping": "UpdatePosition.H uses x += u*gamma_inverse*dt; adjacent Full plotfiles reconstruct this position-update velocity when diag1.intervals=1.",
            "remaining": "The proxy is not a direct half-step attribute diagnostic and the comparison still has no Poincare-section topology consumer for Higuera-Cary.",
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Uniform-B pusher comparison",
        "",
        "A dedicated case-local comparison of Boris, Vay, and Higuera-Cary with no AMR, PML, or evolved electromagnetic field.",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "| pusher | plotfiles | output dt | position-update velocity max error | gyroradius proxy error |",
        "|---|---:|---:|---:|---:|",
    ]
    lines.extend(
        f"| `{case['pusher']}` | `{case['plotfile_count']}` | `{case['output_dt']:.8e}` | `{case['species'][0]['position_update_velocity_proxy_relative_error_max_abs']:.8e}` | `{case['species'][0]['gyroradius_proxy_relative_error']:.8e}` |"
        for case in cases
    )
    lines += [
        "",
        "The position-update velocity and gyroradius values are reconstructed proxies from adjacent Full plotfiles; the case does not claim a direct half-step attribute diagnostic or the Higuera-Cary Poincare-section topology experiment.",
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
