#!/usr/bin/env python
"""Audit species-rho decomposition in radial Esirkepov plotfiles."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt

yt.funcs.mylog.setLevel("ERROR")


CASES = (
    ("RCYLINDER", 1, "esirkepov_langmuir_rcylinder_shape1_species_rho", True),
    ("RCYLINDER", 2, "esirkepov_langmuir_rcylinder_shape2_mpi2", True),
    ("RCYLINDER", 3, "esirkepov_langmuir_rcylinder_shape3_mpi2", True),
    ("RCYLINDER", 4, "esirkepov_langmuir_rcylinder_shape4_mpi2", True),
    ("RSPHERE", 1, "esirkepov_langmuir_rsphere_charge_mpi2", True),
    ("RSPHERE", 2, "esirkepov_langmuir_rsphere_shape2_mpi2", True),
    ("RSPHERE", 3, "esirkepov_langmuir_rsphere_shape3_mpi2", True),
    ("RSPHERE", 4, "esirkepov_langmuir_rsphere_shape4_mpi2", True),
)

FRAME_RE = re.compile(r"^diag\d+$")


def current_frames(case_dir: Path) -> list[Path]:
    """Return numbered current plotfiles, excluding restart backups."""
    diag_dir = case_dir / "diags"
    return sorted(
        (path for path in diag_dir.iterdir() if path.is_dir() and FRAME_RE.fullmatch(path.name)),
        key=lambda path: int(path.name.removeprefix("diag")),
    )


def inspect_frame(plotfile: Path, tolerance: float) -> dict:
    ds = yt.load(str(plotfile))
    field_names = {name for _, name in ds.field_list}
    has_species_fields = {"rho", "rho_electrons", "rho_ions"}.issubset(field_names)
    result = {"frame": plotfile.name, "has_species_fields": has_species_fields, "passed": False}
    if not has_species_fields:
        return result

    grid = ds.covering_grid(0, ds.domain_left_edge, ds.domain_dimensions)
    rho = grid[("boxlib", "rho")].to_ndarray()
    rho_electrons = grid[("boxlib", "rho_electrons")].to_ndarray()
    rho_ions = grid[("boxlib", "rho_ions")].to_ndarray()
    rho_species = rho_electrons + rho_ions
    residual = rho - rho_species
    # Use the largest participating field as scale; near-neutral frames can
    # have a tiny net rho while the electron and ion fields are large.
    scale = max(
        float(np.max(np.abs(rho))),
        float(np.max(np.abs(rho_electrons))),
        float(np.max(np.abs(rho_ions))),
        1.0e-300,
    )
    result.update(
        {
            "finite": bool(np.isfinite(residual).all()),
            "max_relative_residual": float(np.max(np.abs(residual)) / scale),
            "rms_relative_residual": float(np.sqrt(np.mean(residual**2)) / scale),
        }
    )
    result["passed"] = result["finite"] and result["max_relative_residual"] < tolerance
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=1.0e-12)
    args = parser.parse_args()

    rows = []
    for geometry, shape, case_name, expected_fields in CASES:
        case_dir = args.root / case_name
        frames = current_frames(case_dir)
        frame_results = [inspect_frame(frame, args.tolerance) for frame in frames]
        passed_frames = [frame for frame in frame_results if frame["passed"]]
        residual_frames = [frame for frame in frame_results if "max_relative_residual" in frame]
        worst_frame = max(
            residual_frames,
            key=lambda frame: frame["max_relative_residual"],
            default=None,
        )
        has_species_fields = bool(frame_results) and all(
            frame["has_species_fields"] for frame in frame_results
        )
        row = {
            "geometry": geometry,
            "shape": shape,
            "case": case_name,
            "has_species_fields": has_species_fields,
            "expected_species_fields": expected_fields,
            "frame_count": len(frame_results),
            "passed_frame_count": len(passed_frames),
            "missing_species_frame_count": sum(
                not frame["has_species_fields"] for frame in frame_results
            ),
            "passed": False,
        }
        if worst_frame is not None:
            row.update(
                {
                    "max_relative_residual": worst_frame["max_relative_residual"],
                    "rms_relative_residual": max(
                        frame["rms_relative_residual"] for frame in residual_frames
                    ),
                    "worst_frame": worst_frame["frame"],
                }
            )
        row["passed"] = (
            has_species_fields
            and bool(frame_results)
            and len(passed_frames) == len(frame_results)
        )
        rows.append(row)

    runtime_rows = [row for row in rows if row["has_species_fields"]]
    result = {
        "contract": "RCYLINDER/RSPHERE rho species decomposition observable",
        "passed": all(row["passed"] for row in runtime_rows) and len(runtime_rows) == len(rows),
        "classification": "RADIAL_RHO_DECOMPOSITION_TIME_SERIES_VERIFIED_SHAPE1_EXPORT_COMPLETED",
        "tolerance": args.tolerance,
        "rows": rows,
        "runtime_row_count": len(runtime_rows),
        "missing_species_export_count": len(rows) - len(runtime_rows),
        "total_frame_count": sum(row["frame_count"] for row in rows),
        "passed_frame_count": sum(row["passed_frame_count"] for row in rows),
        "scope": "rho equals rho_electrons plus rho_ions on every current numbered radial plotfile frame; not a full Gauss-law or current-closure proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RCYLINDER/RSPHERE rho species decomposition observable",
        "",
        f"- status: `{'PASS' if result['passed'] else 'BOUNDARY'}`",
        f"- classification: `{result['classification']}`",
        f"- runtime rows: `{result['runtime_row_count']}`",
        f"- checked frames: `{result['passed_frame_count']}/{result['total_frame_count']}`",
        f"- missing species-rho exports: `{result['missing_species_export_count']}`",
        "",
        "| geometry | shape | frames | species fields | max relative residual | worst frame | result |",
        "|---|---:|---:|:---:|---:|---|:---:|",
    ]
    for row in rows:
        residual = row.get("max_relative_residual", "missing")
        residual_text = f"`{residual:.6e}`" if isinstance(residual, float) else f"`{residual}`"
        lines.append(
            f"| `{row['geometry']}` | `{row['shape']}` | `{row['passed_frame_count']}/{row['frame_count']}` | "
            f"`{'yes' if row['has_species_fields'] else 'no'}` | {residual_text} | "
            f"`{row.get('worst_frame', 'missing')}` | `{'PASS' if row['passed'] else 'BOUNDARY'}` |"
        )
    lines.extend(["", f"- scope: {result['scope']}"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "passed": result["passed"],
        "classification": result["classification"],
        "runtime_row_count": result["runtime_row_count"],
        "missing_species_export_count": result["missing_species_export_count"],
    }))
    if not result["passed"]:
        raise SystemExit("radial rho decomposition contract failed")


if __name__ == "__main__":
    raise SystemExit(main())
