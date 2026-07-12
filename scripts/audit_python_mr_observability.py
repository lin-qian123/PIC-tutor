#!/usr/bin/env python
"""Audit the Python-side observability boundary for MR intermediate fields."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ANCHORS = {
    "register_list": ("Source/Python/MultiFabRegister.cpp", '"list"'),
    "register_has": ("Source/Python/MultiFabRegister.cpp", '"has"'),
    "register_get": ("Source/Python/MultiFabRegister.cpp", '"_get"'),
    "picmi_fields_property": ("Python/pywarpx/picmi.py", "def fields"),
    "current_fp_python_regression": (
        "Examples/Tests/particle_data_python/inputs_test_2d_particle_attr_access_picmi.py",
        'deposit_current(\n    "current_fp"',
    ),
    "current_buf_allocation": ("Source/WarpX.cpp", "alloc_init(FieldType::current_buf"),
    "rho_buf_allocation": ("Source/WarpX.cpp", "alloc_init(FieldType::rho_buf"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path("../warpx"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for name, (relative_path, needle) in ANCHORS.items():
        path = args.warpx_root / relative_path
        text = path.read_text(encoding="utf-8")
        rows.append(
            {
                "name": name,
                "path": relative_path,
                "needle": needle,
                "found": needle in text,
            }
        )
    missing = [row for row in rows if not row["found"]]
    result = {
        "contract": "Python MR intermediate-field observability audit",
        "anchors": rows,
        "missing_count": len(missing),
        "source_api_present": not missing,
        "classification": "INTERFACE_PRESENT_RUNTIME_LEDGER_UNPROVEN",
        "scope": "source/API observability boundary; not a runtime current_buf/rho_buf proof",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Python MR intermediate-field observability audit",
        "",
        f"- source API anchors: `{len(rows) - len(missing)}/{len(rows)}`",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| anchor | source | status |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| `{row['name']}` | `{row['path']}` | `{'PASS' if row['found'] else 'FAIL'}` |"
        for row in rows
    )
    lines.extend(
        [
            "",
            "The binding exposes a generic field-register API and WarpX allocates `current_buf/rho_buf`, "
            "but the existing Python regression only proves `current_fp`; no runtime MR ledger is claimed.",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if missing:
        raise SystemExit("missing observability anchors: " + ", ".join(row["name"] for row in missing))
    print(f"PASS: {len(rows)} observability anchors; runtime MR ledger remains unproven")


if __name__ == "__main__":
    main()
