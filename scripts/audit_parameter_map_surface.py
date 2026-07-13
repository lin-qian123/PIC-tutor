#!/usr/bin/env python
"""Audit the structural surface of the generated WarpX parameter map."""

from __future__ import annotations

import json
import re
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


def source_paths(reference: str) -> list[Path]:
    reference = reference.strip().strip("`")
    if not reference.startswith(("Source/", "Docs/")):
        return []
    if reference in ALIASES:
        reference = ALIASES[reference]
    if any(char in reference for char in "*?["):
        return [path for path in WARPX.glob(reference) if path.is_file()]
    path = WARPX / reference
    return [path] if path.is_file() else []


def parameter_tokens(parameter: str) -> list[str]:
    value = parameter.strip().strip("`")
    tokens = []
    for part in re.split(r"\s*/\s*|/", value):
        for segment in part.split("."):
            if "<" in segment or ">" in segment:
                continue
            segment = segment.split("(", 1)[0]
            segment = re.sub(r"\[[^]]+\]", "", segment)
            if segment and segment not in {"*", "..."}:
                tokens.append(segment)
    return tokens


def main() -> None:
    text = MAP.read_text(encoding="utf-8")
    lines = text.splitlines()
    declared_match = re.search(r"参数条目数：`?(\d+)`?", text)
    declared_data_row_count = int(declared_match.group(1)) if declared_match else None
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
    token_hit_rows = []
    token_unresolved = []
    for line_number, columns in rows:
        tokens = parameter_tokens(columns[0])
        matched_tokens = set()
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
            for path in source_paths(reference):
                source_text = path.read_text(encoding="utf-8", errors="ignore")
                matched_tokens.update(token for token in tokens if token in source_text)
        if matched_tokens:
            token_hit_rows.append({"line": line_number, "parameter": columns[0], "tokens": sorted(matched_tokens)})
        else:
            token_unresolved.append({"line": line_number, "parameter": columns[0], "tokens": tokens})

    result = {
        "contract": "WarpX parameter-map structural surface",
        "parameter_map": str(MAP),
        "data_row_count": len(rows),
        "declared_data_row_count": declared_data_row_count,
        "placeholder_cells": placeholder_cells,
        "missing_source_references": missing_references,
        "resolved_aliases": alias_hits,
        "wildcard_references": wildcard_hits,
        "source_token_hit_rows": len(token_hit_rows),
        "source_token_unresolved": token_unresolved,
        "header_count_matches": declared_data_row_count == len(rows),
        "passed": not placeholder_cells and not missing_references and declared_data_row_count == len(rows),
        "classification": "STRUCTURAL_SOURCE_TOKEN_SURFACE_PASS_MANUAL_PARSER_REVIEW_REMAINS",
        "scope": "row shape, current chapter labels, source-path existence and parameter-token coverage; not semantic parser-function verification",
    }
    output_dir = ROOT / "runs/stage-c-validation/parameter-map-surface-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Parameter-map structural surface contract",
        "",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- data rows: `{result['data_row_count']}`",
        f"- declared data rows: `{result['declared_data_row_count']}`",
        f"- header count matches: `{'PASS' if result['header_count_matches'] else 'FAIL'}`",
        f"- resolved legacy aliases: `{len(alias_hits)}`",
        f"- wildcard references: `{len(wildcard_hits)}`",
        f"- source-token hit rows: `{len(token_hit_rows)}`",
        f"- source-token unresolved rows: `{len(token_unresolved)}`",
        f"- missing source references: `{len(missing_references)}`",
        "- scope: structural audit, row-count consistency and source-token coverage; token hits do not replace manual ParmParse parser review",
        "",
    ]
    lines.append("")
    lines.append("Unresolved source-token rows are retained in `contract.json` as a review queue; they are not treated as automatic failures because templated, companion and external-owner parameters need manual interpretation.")
    for item in alias_hits:
        lines.append(f"- alias line `{item['line']}`: `{item['from']}` -> `{item['to']}`")
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("parameter-map structural surface contract failed")


if __name__ == "__main__":
    main()
