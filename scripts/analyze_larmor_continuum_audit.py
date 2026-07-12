#!/usr/bin/env python
"""Audit the larmor checksum case against a uniform-B continuum orbit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, e, m_e


B_Y = 0.00078110417851950768
U0 = 0.45825756949558416
GAMMA = np.sqrt(1.0 + U0 * U0)
Z0 = -1.25


def expected(direction: float, time: float) -> tuple[np.ndarray, np.ndarray]:
    omega = e * B_Y / (GAMMA * m_e)
    velocity = U0 * c / GAMMA
    radius = velocity / omega
    position = np.array([
        direction * radius * np.sin(omega * time),
        Z0 + radius * (1.0 - np.cos(omega * time)),
    ])
    momentum = np.array([direction * U0 * m_e * c, 0.0])
    return position, momentum


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfile", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    ds = yt.load(str(args.plotfile))
    ad = ds.all_data()
    time = float(ds.current_time)
    rows = []
    for species, direction in (("electron", -1.0), ("positron", 1.0)):
        expected_pos, expected_mom = expected(direction, time)
        actual_pos = np.array([
            ad[species, "particle_position_x"].to_ndarray()[0],
            ad[species, "particle_position_y"].to_ndarray()[0],
        ])
        actual_mom = np.array([
            ad[species, "particle_momentum_x"].to_ndarray()[0],
            ad[species, "particle_momentum_z"].to_ndarray()[0],
        ])
        displacement_error = float(np.linalg.norm(actual_pos - expected_pos))
        trajectory_scale = float(np.linalg.norm(expected_pos - np.array([0.0, Z0])))
        rows.append({
            "species": species,
            "position_error_abs": displacement_error,
            "position_error_relative_to_displacement": displacement_error / trajectory_scale,
            "momentum_error_relative": float(np.linalg.norm(actual_mom - expected_mom) / np.linalg.norm(expected_mom)),
        })
    max_position_error = max(row["position_error_relative_to_displacement"] for row in rows)
    result = {
        "plotfile": str(args.plotfile),
        "current_time": time,
        "rows": rows,
        "max_position_error_relative_to_displacement": max_position_error,
        "continuum_orbit_gate": "not promoted; this case is checksum-only and includes MR/PML/div-cleaning",
        "passed": False,
        "contract": "uniform-B continuum orbit audit, not an official regression gate",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# Larmor continuum audit\n\n"
        "This audit does not promote the checksum case to a strong continuum gate.\n\n"
        f"- current time: `{time:.16g}`\n"
        f"- maximum trajectory-relative position error: `{max_position_error:.8e}`\n"
        f"- status: `checksum-only; continuum gate not promoted`\n"
        "- reason: the input combines external B, MR, PML, and divergence cleaning.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
