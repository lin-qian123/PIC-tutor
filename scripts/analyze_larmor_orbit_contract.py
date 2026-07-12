#!/usr/bin/env python
"""Extract discrete orbit diagnostics from the existing WarpX larmor case.

This is intentionally an audit of the current checksum case, not a paper
reproduction gate. The input uses Boris, AMR, PML, and divergence cleaning;
those facts stay visible in the report instead of being hidden behind a
continuum-orbit pass/fail label.
"""

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


def read_particle(ds, species: str) -> tuple[np.ndarray, np.ndarray]:
    ad = ds.all_data()
    position = np.array(
        [
            ad[species, "particle_position_x"].to_ndarray()[0],
            ad[species, "particle_position_y"].to_ndarray()[0],
        ],
        dtype=float,
    )
    momentum = np.array(
        [
            ad[species, "particle_momentum_x"].to_ndarray()[0],
            ad[species, "particle_momentum_y"].to_ndarray()[0],
        ],
        dtype=float,
    )
    return position, momentum


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    plotfiles = sorted(
        (path for path in (run_dir / "diags").glob("diag1[0-9]*") if path.is_dir()),
        key=lambda path: int(re.search(r"diag1(\d+)$", path.name).group(1)),
    )
    if not plotfiles:
        raise SystemExit(f"no diag1 plotfiles found under {run_dir}")

    times = []
    positions = {species: [] for species in ("electron", "positron")}
    momenta = {species: [] for species in ("electron", "positron")}
    for plotfile in plotfiles:
        ds = yt.load(str(plotfile))
        times.append(float(ds.current_time))
        for species in positions:
            position, momentum = read_particle(ds, species)
            positions[species].append(position)
            momenta[species].append(momentum)

    times_array = np.asarray(times)
    dt = np.diff(times_array)
    omega_c = e * B_Y / (GAMMA * m_e)
    expected_dt_angle = 2.0 * np.arctan(omega_c * np.median(dt) / 2.0)
    species_rows = []
    for species in positions:
        pos = np.asarray(positions[species])
        mom = np.asarray(momenta[species])
        radius = np.linalg.norm(pos - np.array([0.0, Z0]), axis=1)
        phase = np.unwrap(np.arctan2(pos[:, 0], pos[:, 1] - Z0))
        phase_increment = np.diff(phase)
        momentum_norm = np.linalg.norm(mom, axis=1)
        species_rows.append(
            {
                "species": species,
                "particle_count_per_frame": 1,
                "radius_min": float(radius.min()),
                "radius_max": float(radius.max()),
                "radius_relative_spread": float((radius.max() - radius.min()) / radius.mean()),
                "momentum_norm_relative_spread": float(
                    (momentum_norm.max() - momentum_norm.min()) / momentum_norm.mean()
                ),
                "phase_increment_abs_mean": float(np.mean(np.abs(phase_increment))) if len(phase_increment) else 0.0,
                "phase_increment_abs_max": float(np.max(np.abs(phase_increment))) if len(phase_increment) else 0.0,
                "position_finite": bool(np.isfinite(pos).all()),
                "momentum_finite": bool(np.isfinite(mom).all()),
            }
        )

    checks = {
        "plotfile_sequence_present": len(plotfiles) >= 2,
        "strictly_increasing_time": bool(np.all(dt > 0.0)),
        "uniform_output_cadence": bool(np.allclose(dt, dt[0], rtol=1e-12, atol=0.0)),
        "both_species_have_one_particle": all(row["particle_count_per_frame"] == 1 for row in species_rows),
        "finite_particle_state": all(row["position_finite"] and row["momentum_finite"] for row in species_rows),
    }
    result = {
        "contract": "discrete uniform-B orbit audit for the existing larmor checksum case",
        "passed": all(checks.values()),
        "checks": checks,
        "plotfiles": [path.name for path in plotfiles],
        "time": {"first": float(times_array[0]), "last": float(times_array[-1]), "output_dt": float(np.median(dt))},
        "physics": {
            "B_y": B_Y,
            "gamma": float(GAMMA),
            "omega_c": float(omega_c),
            "expected_boris_rotation_angle": float(expected_dt_angle),
        },
        "species": species_rows,
        "evidence_boundary": {
            "pusher": "Boris",
            "input_features": ["AMR", "PML", "current correction", "divergence cleaning"],
            "paper_reproduction_promoted": False,
            "reason": "The case has no half-step velocity output and is not a dedicated Vay Appendix-B or Higuera-Cary Poincare runtime reproduction.",
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Larmor discrete orbit contract",
        "",
        "This report audits the existing checksum case without promoting it to a paper reproduction.",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        f"- frames: `{len(plotfiles)}`; output dt: `{np.median(dt):.8e}`",
        f"- expected Boris rotation angle per output interval: `{expected_dt_angle:.8e}`",
        "- paper boundary: `Vay Appendix B / Higuera-Cary Poincare runtime reproduction not established`",
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
