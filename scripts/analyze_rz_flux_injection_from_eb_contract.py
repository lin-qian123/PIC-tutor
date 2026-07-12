#!/usr/bin/env python
"""Independent reader-side contract for the RZ EB flux-injection test."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.constants import c, m_e
from scipy.special import erf


def gaussian(u: np.ndarray, u_th: float) -> np.ndarray:
    return np.exp(-(u**2) / (2.0 * u_th**2)) / (np.sqrt(2.0 * np.pi) * u_th)


def gaussian_flux(u: np.ndarray, u_th: float, u_m: float) -> np.ndarray:
    norm = u_th**2 * np.exp(-(u_m**2) / (2.0 * u_th**2)) + np.sqrt(np.pi / 2.0) * u_m * u_th * (1.0 + erf(u_m / np.sqrt(2.0 * u_th**2)))
    return np.where(u > 0.0, u * np.exp(-((u - u_m) ** 2) / (2.0 * u_th**2)) / norm, 0.0)


def histogram_residual(u: np.ndarray, w: np.ndarray, theory, tolerance_fraction: float) -> dict:
    bins = 50
    low, high = -0.5, 0.5
    du = (high - low) / bins
    weighted, edges = np.histogram(u, bins=bins, weights=w / du, range=(low, high))
    centers = 0.5 * (edges[1:] + edges[:-1])
    expected = theory(centers)
    residual = float(np.max(np.abs(weighted - expected)))
    threshold = float(tolerance_fraction * np.max(expected))
    return {"max_abs_residual": residual, "threshold": threshold, "pass": residual <= threshold}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--parser-root", type=Path, required=True)
    parser.add_argument("--plotfile", default="diags/diag1000020")
    args = parser.parse_args()

    sys.path.insert(0, str(args.parser_root))
    from input_file_parser import input_has_value, parse_input_file
    import yt

    case_dir = args.case_dir.resolve()
    ds = yt.load(str(case_dir / args.plotfile))
    data = ds.all_data()
    inputs = parse_input_file(str(case_dir / "warpx_used_inputs"))
    if not input_has_value(inputs, "geometry.dims", "RZ"):
        raise ValueError("This contract expects an RZ plotfile")

    theta = data["electron", "particle_theta"].to_ndarray()
    radial = data["electron", "particle_position_x"].to_ndarray()
    z = data["electron", "particle_position_y"].to_ndarray()
    x, y = radial * np.cos(theta), radial * np.sin(theta)
    ux = data["electron", "particle_momentum_x"].to_ndarray() / (m_e * c)
    uy = data["electron", "particle_momentum_y"].to_ndarray() / (m_e * c)
    uz = data["electron", "particle_momentum_z"].to_ndarray() / (m_e * c)
    weight = data["electron", "particle_weight"].to_ndarray()

    radius = 2.0
    flux = 1.0
    injection_duration = 0.5e-8
    expected_weight = flux * (4.0 * np.pi * radius**2) * injection_duration
    total_weight = float(np.sum(weight))
    radius_ratio = np.sqrt(x**2 + y**2 + z**2) / radius
    nx, ny, nz = x / (radius * radius_ratio), y / (radius * radius_ratio), z / (radius * radius_ratio)
    normal = ux * nx + uy * ny + uz * nz
    vx = ny / np.sqrt(nx**2 + ny**2)
    vy = -nx / np.sqrt(nx**2 + ny**2)
    perpendicular = ux * vx + uy * vy
    wx, wy, wz = -nz * vy, nz * vx, nx * vy - ny * vx
    perpendicular2 = ux * wx + uy * wy + uz * wz

    normal_check = histogram_residual(normal, weight, lambda u: expected_weight * gaussian_flux(u, 0.1, 0.07), 0.05)
    perp_check = histogram_residual(perpendicular, weight, lambda u: expected_weight * gaussian(u, 0.01), 0.07)
    perp2_check = histogram_residual(perpendicular2, weight, lambda u: expected_weight * gaussian(u, 0.01), 0.07)
    result = {
        "case": "test_rz_flux_injection_from_eb",
        "particle_count": int(weight.size),
        "total_weight": total_weight,
        "expected_weight": expected_weight,
        "total_weight_relative_error": abs(total_weight - expected_weight) / expected_weight,
        "min_radius_ratio": float(np.min(radius_ratio)),
        "eb_outside_pass": bool(np.all(radius_ratio > 0.98)),
        "normal_distribution": normal_check,
        "perpendicular_distribution": perp_check,
        "perpendicular2_distribution": perp2_check,
    }
    result["total_weight_pass"] = result["total_weight_relative_error"] <= 0.01
    result["contract_pass"] = bool(result["total_weight_pass"] and result["eb_outside_pass"] and normal_check["pass"] and perp_check["pass"] and perp2_check["pass"])
    out_json = case_dir / "contract.json"
    out_md = case_dir / "contract.md"
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out_md.write_text(
        "\n".join([
            "# RZ EB flux-injection contract",
            "",
            f"- Particle count: `{weight.size}`; total weight `{total_weight:.12e}` vs expected `{expected_weight:.12e}`.",
            f"- Total-weight relative error: `{result['total_weight_relative_error']:.6%}`; gate `{'PASS' if result['total_weight_pass'] else 'FAIL'}`.",
            f"- Minimum particle radius ratio `r/R`: `{result['min_radius_ratio']:.8f}`; EB-outside gate `{'PASS' if result['eb_outside_pass'] else 'FAIL'}`.",
            f"- Distribution gates: normal `{'PASS' if normal_check['pass'] else 'FAIL'}`, perpendicular `{'PASS' if perp_check['pass'] else 'FAIL'}`, perpendicular2 `{'PASS' if perp2_check['pass'] else 'FAIL'}`.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
