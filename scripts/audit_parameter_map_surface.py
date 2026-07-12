#!/usr/bin/env python
"""Audit the structural surface of the generated WarpX parameter map."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WARPX = ROOT.parent / "warpx"
MAP = ROOT / "docs/parameter-map.md"

ALIASES = {
    "Source/AcceleratorLattice/LatticeElementBase.cpp":
        "Source/AcceleratorLattice/LatticeElements/LatticeElementBase.cpp",
    "Source/Utils/Parser/IntervalsParser.cpp":
        "Source/Utils/Parser/BTDIntervalsParser.cpp",
}


def source_exists(reference: str) -> bool:
    reference = reference.strip().strip("`")
    if not reference or reference.startswith(("http://", "https://")):
        return True
    if not reference.startswith(("Source/", "Docs/")):
        return True
    if reference in ALIASES:
        reference = ALIASES[reference]
    if any(char in reference for char in "*?["):
        return any(path.is_file() for path in WARPX.glob(reference))
    return (WARPX / reference).exists()


def main() -> None:
    lines = MAP.read_text(encoding="utf-8").splitlines()
    rows = []
    for line_number, line in enumerate(lines[10:], 11):
        if not line.startswith("|"):
            continue
        columns = [column.strip() for column in line.split("|")[1:-1]]
        if len(columns) >= 8:
            rows.append((line_number, columns))

    placeholder_cells = [
        {"line": line_number, "parameter": columns[0]}
        for line_number, columns in rows
        if "初步源码命中" in "|".join(columns) or "待定" in columns[5]
    ]
    missing_references = []
    alias_hits = []
    wildcard_hits = []
    for line_number, columns in rows:
        for raw_reference in columns[6].split(","):
            reference = raw_reference.strip().strip("`")
            if reference in ALIASES:
                alias_hits.append(
                    {
                        "line": line_number,
                        "from": reference,
                        "to": ALIASES[reference],
                    }
                )
            if any(char in reference for char in "*?[") and reference.startswith(("Source/", "Docs/")):
                wildcard_hits.append({"line": line_number, "reference": reference})
            if not source_exists(reference):
                missing_references.append({"line": line_number, "reference": reference})

    result = {
        "contract": "WarpX parameter-map structural surface",
        "parameter_map": str(MAP),
        "data_row_count": len(rows),
        "placeholder_cells": placeholder_cells,
        "missing_source_references": missing_references,
        "resolved_aliases": alias_hits,
        "wildcard_references": wildcard_hits,
        "passed": not placeholder_cells and not missing_references,
        "classification": "STRUCTURAL_SURFACE_PASS_MANUAL_PARSER_REVIEW_REMAINS",
        "scope": "row shape, current chapter labels, and source-path existence; not semantic parser-function verification",
    }
    output_dir = ROOT / "runs/stage-c-validation/parameter-map-surface-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Parameter-map structural surface contract",
        "",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- data rows: `{result['data_row_count']}`",
        f"- resolved legacy aliases: `{len(alias_hits)}`",
        f"- wildcard references: `{len(wildcard_hits)}`",
        f"- missing source references: `{len(missing_references)}`",
        "- scope: structural audit only; it does not replace manual ParmParse parser review",
        "",
    ]
    for item in alias_hits:
        lines.append(f"- alias line `{item['line']}`: `{item['from']}` -> `{item['to']}`")
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("parameter-map structural surface contract failed")


if __name__ == "__main__":
    main()
