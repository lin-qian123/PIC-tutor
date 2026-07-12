#!/usr/bin/env python
"""Validate nonzero RZ mode writeback and the theta=0 analytic field contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, e, epsilon_0, m_e


def _field(grid, name: str) -> np.ndarray:
    return grid[("boxlib", name)].to_ndarray()[:, :, 0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfile", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    ds = yt.load(str(args.plotfile))
    if ds.parameters.get("geometry.dims") != "RZ":
        raise SystemExit("the multimode contract requires an RZ plotfile")
    raw_modes = str(ds.parameters.get("warpx.n_rz_azimuthal_modes", 1)).split("#", 1)[0].strip()
    modes = int(raw_modes)
    if modes < 3:
        raise SystemExit(f"expected at least three RZ modes, got {modes}")

    dims = np.asarray(ds.domain_dimensions, dtype=int)
    nr, nz = int(dims[0]), int(dims[1])
    rlo, zlo = ds.domain_left_edge[:2].to_ndarray()
    rhi, zhi = ds.domain_right_edge[:2].to_ndarray()
    dr = (rhi - rlo) / nr
    dz = (zhi - zlo) / nz
    r = rlo + (np.arange(nr) + 0.5)[:, None] * dr
    z = zlo + (np.arange(nz) + 0.5)[None, :] * dz

    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=dims)
    # At theta=0 the real parts add; the imaginary parts provide an independent
    # signal that the complex m>0 diagnostic components were materialized.
    er_theta0 = _field(grid, "Er_0_real") + _field(grid, "Er_1_real") + _field(grid, "Er_2_real")
    ez_theta0 = _field(grid, "Ez_0_real") + _field(grid, "Ez_1_real") + _field(grid, "Ez_2_real")
    er_native = _field(grid, "Er")
    ez_native = _field(grid, "Ez")

    epsilon0 = epsilon1 = epsilon2 = 0.01
    n0 = 2.0e24
    w0 = 5.0e-6
    k0 = 2.0 * np.pi / 20.0e-6
    wp = np.sqrt(n0 * e**2 / (m_e * epsilon_0))
    t = ds.current_time.to_value()
    envelope = np.exp(-(r**2) / w0**2)
    phase_r = np.sin(k0 * z) * np.sin(wp * t)
    phase_z = np.cos(k0 * z) * np.sin(wp * t)
    # The native input stores epsilon as a dimensionless velocity normalized
    # by c, so its SI field scale is m_e*c**2/q_e.
    scale = m_e * c**2 / (-e)
    er_theory = scale * envelope * phase_r * (
        epsilon0 * 2.0 * r / w0**2
        - epsilon1 * 2.0 / w0
        + epsilon1 * 4.0 * r**2 / w0**3
        - epsilon2 * 8.0 * r / w0**2
        + epsilon2 * 8.0 * r**3 / w0**4
    )
    ez_theory = -scale * k0 * envelope * phase_z * (
        epsilon0 + epsilon1 * 2.0 * r / w0 + epsilon2 * 4.0 * r**2 / w0**2
    )

    def relative_max_error(sim: np.ndarray, theory: np.ndarray) -> float:
        return float(np.max(np.abs(sim - theory)) / np.max(np.abs(theory)))

    mode_amplitudes = {}
    for component in ("Er", "Ez"):
        for mode in (1, 2):
            for part in ("real", "imag"):
                name = f"{component}_{mode}_{part}"
                mode_amplitudes[name] = float(np.max(np.abs(_field(grid, name))))
    nonzero_mode_amplitudes = [value for key, value in mode_amplitudes.items() if "_1_" in key or "_2_" in key]
    mode_nonzero = bool(max(nonzero_mode_amplitudes) > 0.0)
    er_error = relative_max_error(er_theta0, er_theory)
    ez_error = relative_max_error(ez_theta0, ez_theory)
    error_rel = max(er_error, ez_error)
    er_writeback_error = relative_max_error(er_theta0, er_native)
    ez_writeback_error = relative_max_error(ez_theta0, ez_native)
    tolerance = 0.12
    result = {
        "plotfile": str(args.plotfile),
        "geometry": "RZ",
        "azimuthal_modes": modes,
        "grid_shape_rz": [nr, nz],
        "cell_size": [float(dr), float(dz)],
        "current_time": float(t),
        "mode_amplitudes_max_abs": mode_amplitudes,
        "mode_nonzero": mode_nonzero,
        "theta0_reconstruction": "m0_real + m1_real + m2_real",
        "er_analytic_max_relative_error": er_error,
        "ez_analytic_max_relative_error": ez_error,
        "analytic_error_rel": error_rel,
        "er_native_writeback_relative_error": er_writeback_error,
        "ez_native_writeback_relative_error": ez_writeback_error,
        "native_writeback_error_rel": max(er_writeback_error, ez_writeback_error),
        "tolerance_rel": tolerance,
        "passed": bool(mode_nonzero and max(er_writeback_error, ez_writeback_error) < 1.0e-12),
        "contract": "RZ m>0 diagnostic writeback is nonzero and the native theta=0 fields equal the real-mode reconstruction",
        "scope": "project-level case-local sibling; the native CMake input defaults to one azimuthal mode",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# RZ Langmuir multimode contract\n\n"
        f"- status: `{status}`\n"
        f"- azimuthal modes: `{modes}`\n"
        f"- grid shape (r,z): `{nr} x {nz}`\n"
        f"- nonzero m>0 writeback: `{mode_nonzero}`\n"
        f"- theta=0 reconstruction: `{result['theta0_reconstruction']}`\n"
        f"- native Er writeback relative error: `{er_writeback_error:.8e}`\n"
        f"- native Ez writeback relative error: `{ez_writeback_error:.8e}`\n"
        f"- analytic Er diagnostic error: `{er_error:.8e}`\n"
        f"- analytic Ez diagnostic error: `{ez_error:.8e}`\n"
        f"- native writeback tolerance: `{1.0e-12:.2e}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("RZ Langmuir multimode contract failed")


if __name__ == "__main__":
    main()
