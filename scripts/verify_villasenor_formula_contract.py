#!/usr/bin/env python
"""Verify the bounded 2D Villasenor formula and crossing-split identities."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=1992)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    max_four_boundary_residual = 0.0
    max_segment_sum_residual = 0.0
    max_flux_sum_residual = 0.0
    max_3d_face_sum_residual = 0.0
    max_3d_volume_closure_residual = 0.0
    max_crossing_count = 0

    for _ in range(args.samples):
        x0 = rng.uniform(-0.9, 0.9)
        y0 = rng.uniform(-0.9, 0.9)
        x1 = x0 + rng.uniform(-2.4, 2.4)
        y1 = y0 + rng.uniform(-2.4, 2.4)
        segments = _split_at_cell_crossings(x0, y0, x1, y1)
        max_crossing_count = max(max_crossing_count, len(segments) - 1)

        sum_dx = sum(segment[2] for segment in segments)
        sum_dy = sum(segment[3] for segment in segments)
        max_segment_sum_residual = max(
            max_segment_sum_residual,
            abs(sum_dx - (x1 - x0)),
            abs(sum_dy - (y1 - y0)),
        )

        for sx0, sy0, dx, dy in segments:
            flux = _four_boundary_flux(sx0, sy0, dx, dy)
            max_four_boundary_residual = max(
                max_four_boundary_residual,
                abs(flux[0] + flux[1] - dx),
                abs(flux[2] + flux[3] - dy),
            )
            max_flux_sum_residual = max(
                max_flux_sum_residual,
                abs(sum(flux[0:2]) - dx),
                abs(sum(flux[2:4]) - dy),
            )

        xi_bar = rng.uniform(-0.9, 0.9)
        eta_bar = rng.uniform(-0.9, 0.9)
        zeta_bar = rng.uniform(-0.9, 0.9)
        dx3 = rng.uniform(-2.4, 2.4)
        dy3 = rng.uniform(-2.4, 2.4)
        dz3 = rng.uniform(-2.4, 2.4)
        x_faces, y_faces, z_faces = _three_d_face_fluxes(
            xi_bar, eta_bar, zeta_bar, dx3, dy3, dz3
        )
        max_3d_face_sum_residual = max(
            max_3d_face_sum_residual,
            abs(sum(x_faces) - dx3),
            abs(sum(y_faces) - dy3),
            abs(sum(z_faces) - dz3),
        )
        after = (
            xi_bar + 0.5 * dx3,
            eta_bar + 0.5 * dy3,
            zeta_bar + 0.5 * dz3,
        )
        before = (
            xi_bar - 0.5 * dx3,
            eta_bar - 0.5 * dy3,
            zeta_bar - 0.5 * dz3,
        )
        volume_difference = (
            after[0] * after[1] * after[2] - before[0] * before[1] * before[2]
        )
        flux_difference = (
            dx3 * eta_bar * zeta_bar
            + dy3 * zeta_bar * xi_bar
            + dz3 * xi_bar * eta_bar
            + dx3 * dy3 * dz3 / 4.0
        )
        max_3d_volume_closure_residual = max(
            max_3d_volume_closure_residual,
            abs(volume_difference - flux_difference),
        )

    passed = max(
        max_four_boundary_residual,
        max_segment_sum_residual,
        max_flux_sum_residual,
        max_3d_face_sum_residual,
        max_3d_volume_closure_residual,
    ) < 1.0e-14
    result = {
        "samples": args.samples,
        "seed": args.seed,
        "max_crossing_count": max_crossing_count,
        "max_four_boundary_residual": max_four_boundary_residual,
        "max_segment_sum_residual": max_segment_sum_residual,
        "max_flux_sum_residual": max_flux_sum_residual,
        "max_3d_face_sum_residual": max_3d_face_sum_residual,
        "max_3d_volume_closure_residual": max_3d_volume_closure_residual,
        "passed": passed,
        "contract": "2D four-boundary and 3D cross-term flux/volume identities plus arbitrary crossing-split displacement closure",
        "scope": "paper formula and geometric segmentation identities; not a WarpX kernel equivalence or end-to-end regression",
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(_markdown(result))
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit("Villasenor formula contract failed")


def _four_boundary_flux(x: float, y: float, dx: float, dy: float) -> tuple[float, float, float, float]:
    return (
        dx * (0.5 - y - 0.5 * dy),
        dx * (0.5 + y + 0.5 * dy),
        dy * (0.5 - x - 0.5 * dx),
        dy * (0.5 + x + 0.5 * dx),
    )


def _three_d_face_fluxes(
    xi: float, eta: float, zeta: float, dx: float, dy: float, dz: float
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...]]:
    cross = dx * dy * dz / 12.0
    x_faces = (
        dx * eta * zeta + cross,
        dx * (1.0 - eta) * zeta - cross,
        dx * eta * (1.0 - zeta) - cross,
        dx * (1.0 - eta) * (1.0 - zeta) + cross,
    )
    y_faces = _rotate_faces(eta, zeta, xi, dy, dz, dx)
    z_faces = _rotate_faces(zeta, xi, eta, dz, dx, dy)
    return x_faces, y_faces, z_faces


def _rotate_faces(
    primary: float,
    transverse_a: float,
    transverse_b: float,
    d_primary: float,
    d_a: float,
    d_b: float,
) -> tuple[float, ...]:
    cross = d_primary * d_a * d_b / 12.0
    return (
        d_primary * transverse_a * transverse_b + cross,
        d_primary * (1.0 - transverse_a) * transverse_b - cross,
        d_primary * transverse_a * (1.0 - transverse_b) - cross,
        d_primary * (1.0 - transverse_a) * (1.0 - transverse_b) + cross,
    )


def _split_at_cell_crossings(x0: float, y0: float, x1: float, y1: float) -> list[tuple[float, float, float, float]]:
    dx = x1 - x0
    dy = y1 - y0
    parameters = [0.0, 1.0]
    if dx != 0.0:
        lo, hi = sorted((x0, x1))
        for boundary in range(math.floor(lo) + 1, math.floor(hi) + 1):
            t = (boundary - x0) / dx
            if 0.0 < t < 1.0:
                parameters.append(t)
    if dy != 0.0:
        lo, hi = sorted((y0, y1))
        for boundary in range(math.floor(lo) + 1, math.floor(hi) + 1):
            t = (boundary - y0) / dy
            if 0.0 < t < 1.0:
                parameters.append(t)
    parameters = sorted(set(parameters))
    segments = []
    for ta, tb in zip(parameters, parameters[1:]):
        segments.append(
            (
                x0 + ta * dx,
                y0 + ta * dy,
                (tb - ta) * dx,
                (tb - ta) * dy,
            )
        )
    return segments


def _markdown(result: dict) -> str:
    lines = [
        "# Villasenor formula contract",
        "",
        f"- samples: `{result['samples']}` (seed `{result['seed']}`)",
        f"- maximum crossing count: `{result['max_crossing_count']}`",
        f"- four-boundary flux residual: `{result['max_four_boundary_residual']:.6e}`",
        f"- segment displacement residual: `{result['max_segment_sum_residual']:.6e}`",
        f"- flux-sum residual: `{result['max_flux_sum_residual']:.6e}`",
        f"- 3D face-sum residual: `{result['max_3d_face_sum_residual']:.6e}`",
        f"- 3D volume-closure residual: `{result['max_3d_volume_closure_residual']:.6e}`",
        f"- contract: `{'PASS' if result['passed'] else 'FAIL'}`",
        "",
        "This check verifies the paper's four-boundary identities, 3D cross-term/volume closure, and the geometric fact that repeated crossing-defined segments recover the original displacement. It does not prove bitwise equivalence to every WarpX shape order, geometry branch, or boundary path.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
