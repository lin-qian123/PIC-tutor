#!/usr/bin/env python
"""Verify the explicit PECInsulator boundary-drive field contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


FIELD_NAMES = ("Ex", "Ey", "Ez", "Bx", "By", "Bz")


def read_fields(plotfile: Path) -> tuple[yt.Dataset, dict[str, np.ndarray]]:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(level=ds.max_level, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    fields = {name: grid["boxlib", name].to_ndarray()[:, :, 0] for name in FIELD_NAMES}
    return ds, fields


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--relative-tolerance", type=float, default=5.0e-2)
    args = parser.parse_args()

    initial_ds, initial = read_fields(args.initial)
    final_ds, final = read_fields(args.final)
    if initial_ds.domain_dimensions.tolist() != [32, 32, 1] or final_ds.domain_dimensions.tolist() != [32, 32, 1]:
        raise SystemExit("expected 32x32 2D PECInsulator plotfiles")

    initial_max = max(float(np.max(np.abs(array))) for array in initial.values())
    final_max = max(float(np.max(np.abs(array))) for array in final.values())
    dz = float(final_ds.domain_width[1]) / final_ds.domain_dimensions[1]
    z_centers = float(final_ds.domain_left_edge[1]) + (np.arange(32) + 0.5) * dz
    active = (z_centers >= 2.25e-2) & (z_centers <= 2.75e-2)
    boundary_by = final["By"][-1, active]
    expected_by = min(float(final_ds.current_time) / 1.0e-12, 1.0) * 1.0e1 * 3.3e-4
    central_by = float(np.max(boundary_by))
    central_relative_error = abs(central_by - expected_by) / expected_by
    lower_boundary_by = float(np.max(np.abs(final["By"][0, :])))
    final_energy_proxy = float(sum(np.sum(array * array) for array in final.values()))
    result = {
        "initial_plotfile": str(args.initial),
        "final_plotfile": str(args.final),
        "initial_max_abs_field": initial_max,
        "final_max_abs_field": final_max,
        "final_time": float(final_ds.current_time),
        "active_z_cell_count": int(np.count_nonzero(active)),
        "active_boundary_by_min": float(np.min(boundary_by)),
        "active_boundary_by_max": central_by,
        "expected_boundary_by": expected_by,
        "active_boundary_by_relative_error": central_relative_error,
        "lower_boundary_by_max_abs": lower_boundary_by,
        "final_field_energy_proxy": final_energy_proxy,
        "initial_zero_tolerance": 1.0e-14,
        "relative_tolerance": args.relative_tolerance,
        "lower_boundary_tolerance": 1.0e-14,
        "passed": bool(
            initial_max < 1.0e-14
            and np.isfinite(final_max)
            and final_energy_proxy > 0.0
            and central_relative_error < args.relative_tolerance
            and lower_boundary_by < 1.0e-14
        ),
        "contract": "2D explicit PECInsulator boundary-drive localization and By amplitude",
        "scope": "official WarpX explicit input; 2-rank reader-side contract; cell-centered By boundary sample; not the implicit Poynting-ledger contract",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# 2D explicit PECInsulator contract\n\n"
        f"- status: `{status}`\n"
        f"- initial max |field|: `{initial_max:.8e}`\n"
        f"- final max |field|: `{final_max:.8e}`\n"
        f"- active z cells: `{int(np.count_nonzero(active))}`\n"
        f"- boundary By max / expected: `{central_by:.8e}` / `{expected_by:.8e}`\n"
        f"- active By relative error: `{central_relative_error:.8e}`\n"
        f"- lower-boundary max |By|: `{lower_boundary_by:.8e}`\n"
        f"- gates: initial `<1e-14`; active By relative error `<{args.relative_tolerance:.1e}`; lower boundary `<1e-14`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("2D explicit PECInsulator contract failed")


if __name__ == "__main__":
    main()
