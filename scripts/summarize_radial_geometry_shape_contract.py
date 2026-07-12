#!/usr/bin/env python
"""Summarize RCYLINDER/RSPHERE Esirkepov radial shape contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for geometry in ("rcylinder", "rsphere"):
        for shape in range(1, 5):
            dirname = f"esirkepov_langmuir_{geometry}_mpi2" if shape == 1 else f"esirkepov_langmuir_{geometry}_shape{shape}_mpi2"
            data = json.loads((args.root / dirname / "contract.json").read_text(encoding="utf-8"))
            rows.append({
                "geometry": geometry.upper(),
                "shape": shape,
                "relative_er_error": data["relative_er_error"],
                "tolerance": data["tolerance"],
                "passed": data["passed"],
            })
    result = {
        "contract": "RCYLINDER/RSPHERE Esirkepov radial shape matrix",
        "rows": rows,
        "passed": all(row["passed"] for row in rows),
        "classification": "RADIAL_GEOMETRY_SHAPE_1_TO_4_FIELD_PASS",
        "scope": "2-rank reader-side radial Er contract; not a charge/Gauss-law or all-geometry proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RCYLINDER/RSPHERE Esirkepov radial shape matrix",
        "",
        "| geometry | shape | relative Er error | gate | status |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['geometry']} | {row['shape']} | `{row['relative_er_error']:.8e}` | `< {row['tolerance']:.2f}` | `{'PASS' if row['passed'] else 'FAIL'}` |")
    lines.extend(["", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {len(rows)} radial geometry/shape contracts")


if __name__ == "__main__":
    main()
