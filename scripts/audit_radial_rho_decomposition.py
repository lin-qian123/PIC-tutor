#!/usr/bin/env python
"""Audit species-rho decomposition in radial Esirkepov plotfiles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


CASES = (
    ("RCYLINDER", 1, "esirkepov_langmuir_rcylinder_charge_mpi2", False),
    ("RCYLINDER", 2, "esirkepov_langmuir_rcylinder_shape2_mpi2", True),
    ("RCYLINDER", 3, "esirkepov_langmuir_rcylinder_shape3_mpi2", True),
    ("RCYLINDER", 4, "esirkepov_langmuir_rcylinder_shape4_mpi2", True),
    ("RSPHERE", 1, "esirkepov_langmuir_rsphere_charge_mpi2", True),
    ("RSPHERE", 2, "esirkepov_langmuir_rsphere_shape2_mpi2", True),
    ("RSPHERE", 3, "esirkepov_langmuir_rsphere_shape3_mpi2", True),
    ("RSPHERE", 4, "esirkepov_langmuir_rsphere_shape4_mpi2", True),
)


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
        plotfile = case_dir / "diags/diag1000080"
        ds = yt.load(str(plotfile))
        field_names = {name for _, name in ds.field_list}
        has_species_fields = {"rho", "rho_electrons", "rho_ions"}.issubset(field_names)
        row = {
            "geometry": geometry,
            "shape": shape,
            "case": case_name,
            "has_species_fields": has_species_fields,
            "expected_species_fields": expected_fields,
            "passed": False,
        }
        if has_species_fields:
            grid = ds.covering_grid(0, ds.domain_left_edge, ds.domain_dimensions)
            rho = grid[("boxlib", "rho")].to_ndarray()
            rho_species = (
                grid[("boxlib", "rho_electrons")].to_ndarray()
                + grid[("boxlib", "rho_ions")].to_ndarray()
            )
            residual = rho - rho_species
            scale = max(float(np.max(np.abs(rho))), 1.0e-300)
            row.update(
                {
                    "finite": bool(np.isfinite(residual).all()),
                    "max_relative_residual": float(np.max(np.abs(residual)) / scale),
                    "rms_relative_residual": float(np.sqrt(np.mean(residual**2)) / scale),
                }
            )
            row["passed"] = row["finite"] and row["max_relative_residual"] < args.tolerance
        rows.append(row)

    missing_exports = [row for row in rows if not row["has_species_fields"]]
    runtime_rows = [row for row in rows if row["has_species_fields"]]
    result = {
        "contract": "RCYLINDER/RSPHERE rho species decomposition observable",
        "passed": all(row["passed"] for row in runtime_rows) and len(missing_exports) == 1,
        "classification": "RADIAL_RHO_DECOMPOSITION_OBSERVABLE_VERIFIED_SHAPE1_EXPORT_BOUNDARY",
        "tolerance": args.tolerance,
        "rows": rows,
        "runtime_row_count": len(runtime_rows),
        "missing_species_export_count": len(missing_exports),
        "scope": "rho equals rho_electrons plus rho_ions on archived radial plotfiles; not a full Gauss-law or current-closure proof",
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
        f"- missing species-rho exports: `{result['missing_species_export_count']}`",
        "",
        "| geometry | shape | species fields | max relative residual | result |",
        "|---|---:|:---:|---:|:---:|",
    ]
    for row in rows:
        residual = row.get("max_relative_residual", "missing")
        residual_text = f"`{residual:.6e}`" if isinstance(residual, float) else f"`{residual}`"
        lines.append(
            f"| `{row['geometry']}` | `{row['shape']}` | `{'yes' if row['has_species_fields'] else 'no'}` | "
            f"{residual_text} | `{'PASS' if row['passed'] else 'BOUNDARY'}` |"
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
