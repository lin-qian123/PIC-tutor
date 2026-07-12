#!/usr/bin/env python
"""Build a bounded geometry/order coverage matrix from existing contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CASES = [
    {
        "family": "Esirkepov",
        "geometry": "1D_Z",
        "shape_order": "1",
        "evidence": "field + charge PASS",
        "scope": "Langmuir",
        "contract": "runs/stage-c-validation/esirkepov_langmuir_1d_mpi2/contract.json",
    },
    {
        "family": "Esirkepov",
        "geometry": "XZ",
        "shape_order": "1/2/3/4",
        "evidence": "field + charge PASS",
        "scope": "2D Langmuir siblings",
        "contract": "runs/stage-c-validation/esirkepov_langmuir_2d_particle_shape_4_mpi2/contract.json",
    },
    {
        "family": "Esirkepov",
        "geometry": "3D",
        "shape_order": "1",
        "evidence": "field + charge PASS",
        "scope": "Langmuir",
        "contract": "runs/stage-c-validation/esirkepov_langmuir_3d_mpi2/contract.json",
    },
    {
        "family": "Esirkepov",
        "geometry": "XZ + AMR",
        "shape_order": "1",
        "evidence": "field PASS; level charge BOUNDARY",
        "scope": "2D MR overlay",
        "contract": "runs/stage-c-validation/esirkepov_langmuir_2d_mr_mpi2/contract.json",
    },
    {
        "family": "Esirkepov",
        "geometry": "RZ",
        "shape_order": "1/2/3/4",
        "evidence": "field PASS; correction-on charge BOUNDARY; correction-off refined PASS",
        "scope": "axis-correction/resolution family",
        "contract": "runs/stage-c-validation/esirkepov_langmuir_rz_axis-correction-family/contract.json",
    },
    {
        "family": "Esirkepov",
        "geometry": "RCYLINDER/RSPHERE",
        "shape_order": "1/2/3/4",
        "evidence": "radial Er PASS",
        "scope": "radial field only",
        "contract": "runs/stage-c-validation/esirkepov_radial_geometry_shape-matrix/contract.json",
    },
    {
        "family": "Villasenor implicit",
        "geometry": "XZ",
        "shape_order": "2",
        "evidence": "energy + Gauss-law PASS",
        "scope": "native/filtered/PICMI siblings",
        "contract": "runs/stage-c-validation/implicit_villasenor_2d_jfnk_mpi2/contract.json",
    },
    {
        "family": "Villasenor implicit",
        "geometry": "XZ",
        "shape_order": "4",
        "evidence": "cropping Gauss-law PASS",
        "scope": "near-boundary cropping",
        "contract": "runs/stage-c-validation/implicit_villasenor_2d_cropping_mpi2/contract.json",
    },
    {
        "family": "Villasenor implicit",
        "geometry": "RZ",
        "shape_order": "2",
        "evidence": "build/runtime BOUNDARY",
        "scope": "PETSc missing; amrex_gmres control SIGILL before physics",
        "contract": "notes/code-reading/particles/47-rz-implicit-villasenor-build-boundary.md",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    missing = []
    for case in CASES:
        path = args.root / case["contract"]
        exists = path.is_file()
        if not exists:
            missing.append(case["contract"])
        row = dict(case)
        row["contract_exists"] = exists
        rows.append(row)

    result = {
        "contract": "PIC deposition geometry/order coverage matrix",
        "rows": rows,
        "row_count": len(rows),
        "missing_contracts": missing,
        "passed": not missing,
        "interpretation": (
            "The matrix records the strongest evidence currently available for each family. "
            "A PASS in one geometry/order cell does not imply full geometry, AMR, boundary, "
            "or implicit coverage."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "coverage-matrix.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# PIC deposition geometry/order coverage matrix",
        "",
        f"- rows: `{len(rows)}`",
        f"- contract references present: `{len(rows) - len(missing)}/{len(rows)}`",
        "- scope: bounded evidence index; not a full Cartesian-product regression claim",
        "",
        "| family | geometry | shape/order | evidence | scope | contract |",
        "|---|---|---:|---|---|---|",
    ]
    for row in rows:
        status = "present" if row["contract_exists"] else "MISSING"
        lines.append(
            f"| {row['family']} | {row['geometry']} | {row['shape_order']} | "
            f"{row['evidence']} | {row['scope']} | `{row['contract']}` ({status}) |"
        )
    lines.extend(
        [
            "",
            "## Explicit gaps",
            "",
            "- RZ correction-on charge/Gauss-law remains a diagnostic boundary.",
            "- RCYLINDER/RSPHERE shape matrix is a radial `Er` contract, not a charge contract.",
            "- 2D MR is not a route-count or intermediate-field proof.",
            "- RZ implicit Villasenor is a build/runtime boundary, not a physics pass/fail.",
            "- 3D Esirkepov shape=2/3/4 and full geometry/order cross-products remain unclaimed.",
        ]
    )
    (args.output_dir / "coverage-matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
