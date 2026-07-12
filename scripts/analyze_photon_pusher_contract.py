#!/usr/bin/env python
"""Analyze the official massless photon straight-line propagation contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, m_e


SPECIES = [
    "p_xp_1", "p_xn_1", "p_yp_1", "p_yn_1", "p_zp_1", "p_zn_1", "p_dp_1", "p_dn_1",
    "p_xp_10", "p_xn_10", "p_yp_10", "p_yn_10", "p_zp_10", "p_zn_10", "p_dp_10", "p_dn_10",
]
GAMMA_BETA = np.array([
    [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1], [1, 1, 1], [-1, -1, -1],
    [10, 0, 0], [-10, 0, 0], [0, 10, 0], [0, -10, 0], [0, 0, 10], [0, 0, -10], [10, 10, 10], [-10, -10, -10],
], dtype=float)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfile", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    ds = yt.load(str(args.plotfile))
    all_data = ds.all_data()
    sim_time = float(ds.current_time)
    expected_pos = sim_time * c * GAMMA_BETA / np.linalg.norm(GAMMA_BETA, axis=1, keepdims=True)
    expected_mom = m_e * c * GAMMA_BETA
    simulated_pos = []
    simulated_mom = []
    for species in SPECIES:
        simulated_pos.append([
            all_data[species, "particle_position_x"].to_ndarray()[0],
            all_data[species, "particle_position_y"].to_ndarray()[0],
            all_data[species, "particle_position_z"].to_ndarray()[0],
        ])
        simulated_mom.append([
            all_data[species, "particle_momentum_x"].to_ndarray()[0],
            all_data[species, "particle_momentum_y"].to_ndarray()[0],
            all_data[species, "particle_momentum_z"].to_ndarray()[0],
        ])
    simulated_pos = np.asarray(simulated_pos)
    simulated_mom = np.asarray(simulated_mom)
    pos_errors = np.linalg.norm(simulated_pos - expected_pos, axis=1) / np.linalg.norm(expected_pos, axis=1)
    mom_errors = np.linalg.norm(simulated_mom - expected_mom, axis=1) / np.linalg.norm(expected_mom, axis=1)
    result = {
        "plotfile": str(args.plotfile),
        "current_time": sim_time,
        "species_count": len(SPECIES),
        "max_position_relative_error": float(pos_errors.max()),
        "position_tolerance": 1.0e-14,
        "max_momentum_relative_error": float(mom_errors.max()),
        "momentum_tolerance": float(np.finfo(np.float64).eps),
        "passed": bool(pos_errors.max() <= 1.0e-14 and mom_errors.max() <= np.finfo(np.float64).eps),
        "contract": "massless photons propagate at c along initial direction and conserve momentum",
    }
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        status = "PASS" if result["passed"] else "FAIL"
        args.output_md.write_text(
            "# Photon pusher contract\n\n"
            f"- status: `{status}`\n"
            f"- current time: `{sim_time:.16g}`\n"
            f"- species count: `{len(SPECIES)}`\n"
            f"- max position relative error: `{pos_errors.max():.8e}`\n"
            f"- max momentum relative error: `{mom_errors.max():.8e}`\n"
            f"- contract: {result['contract']}\n",
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("photon pusher contract failed")


if __name__ == "__main__":
    main()
