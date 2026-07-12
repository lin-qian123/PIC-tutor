#!/usr/bin/env python
"""Independent reader-side contract for the 2D cylinder EB flux-injection test."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.constants import c, m_e
from scipy.special import erf


def gaussian(u, u_th):
    return np.exp(-(u**2) / (2.0 * u_th**2)) / (np.sqrt(2.0 * np.pi) * u_th)


def gaussian_flux(u, u_th, u_m):
    norm = u_th**2 * np.exp(-(u_m**2) / (2.0 * u_th**2)) + np.sqrt(np.pi / 2.0) * u_m * u_th * (1.0 + erf(u_m / np.sqrt(2.0 * u_th**2)))
    return np.where(u > 0.0, u * np.exp(-((u - u_m) ** 2) / (2.0 * u_th**2)) / norm, 0.0)


def check_histogram(u, weight, theory, tolerance_fraction):
    bins = 50
    du = 1.0 / bins
    hist, edges = np.histogram(u, bins=bins, weights=weight / du, range=(-0.5, 0.5))
    centers = 0.5 * (edges[1:] + edges[:-1])
    expected = theory(centers)
    residual = float(np.max(np.abs(hist - expected)))
    threshold = float(tolerance_fraction * np.max(expected))
    return {"max_abs_residual": residual, "threshold": threshold, "pass": residual <= threshold}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--parser-root", type=Path, required=True)
    parser.add_argument("--plotfile", default="diags/diag1000020")
    args = parser.parse_args()

    sys.path.insert(0, str(args.parser_root))
    import yt

    case_dir = args.case_dir.resolve()
    data = yt.load(str(case_dir / args.plotfile)).all_data()
    x = data["electron", "particle_position_x"].to_ndarray()
    z = data["electron", "particle_position_y"].to_ndarray()
    ux = data["electron", "particle_momentum_x"].to_ndarray() / (m_e * c)
    uy = data["electron", "particle_momentum_y"].to_ndarray() / (m_e * c)
    uz = data["electron", "particle_momentum_z"].to_ndarray() / (m_e * c)
    weight = data["electron", "particle_weight"].to_ndarray()

    radius = 2.0
    expected_weight = 1.0 * (2.0 * np.pi * radius) * 0.5e-8
    radial = np.sqrt(x**2 + z**2)
    nx, nz = x / radial, z / radial
    normal = ux * nx + uz * nz
    sign = nx / np.abs(nx)
    perpendicular = -sign * uy
    sx, sz = sign * nz, -sign * nx
    perpendicular2 = ux * sx + uz * sz

    total = float(np.sum(weight))
    normal_check = check_histogram(normal, weight, lambda u: expected_weight * gaussian_flux(u, 0.1, 0.07), 0.05)
    perp_check = check_histogram(perpendicular, weight, lambda u: expected_weight * gaussian(u, 0.01), 0.07)
    perp2_check = check_histogram(perpendicular2, weight, lambda u: expected_weight * gaussian(u, 0.01), 0.07)
    result = {
        "case": "test_2d_flux_injection_from_eb",
        "particle_count": int(weight.size),
        "total_weight": total,
        "expected_weight": expected_weight,
        "total_weight_relative_error": abs(total - expected_weight) / expected_weight,
        "min_radius_ratio": float(np.min(radial / radius)),
        "total_weight_pass": abs(total - expected_weight) / expected_weight <= 0.01,
        "eb_outside_pass": bool(np.all(radial / radius > 0.98)),
        "normal_distribution": normal_check,
        "perpendicular_distribution": perp_check,
        "perpendicular2_distribution": perp2_check,
    }
    result["contract_pass"] = bool(result["total_weight_pass"] and result["eb_outside_pass"] and normal_check["pass"] and perp_check["pass"] and perp2_check["pass"])
    (case_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (case_dir / "contract.md").write_text(
        "\n".join([
            "# 2D cylinder EB flux-injection contract", "",
            f"- Particle count: `{weight.size}`; total weight relative error: `{result['total_weight_relative_error']:.6%}`.",
            f"- Minimum `r/R`: `{result['min_radius_ratio']:.8f}`; total-weight and EB-outside gates: `{'PASS' if result['total_weight_pass'] and result['eb_outside_pass'] else 'FAIL'}`.",
            f"- Distribution gates: normal `{'PASS' if normal_check['pass'] else 'FAIL'}`, perpendicular `{'PASS' if perp_check['pass'] else 'FAIL'}`, perpendicular2 `{'PASS' if perp2_check['pass'] else 'FAIL'}`.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
