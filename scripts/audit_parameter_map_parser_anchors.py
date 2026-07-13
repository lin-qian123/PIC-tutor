#!/usr/bin/env python
"""Audit parser-call anchors for the generated WarpX parameter map.

This is deliberately a source-text audit, not a C++ semantic proof. It turns
the remaining manual ParmParse review into an explicit, reproducible queue.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from audit_parameter_map_surface import MAP, parameter_tokens, source_paths


PARSER_WORDS = re.compile(
    r"\b(?:query|queryarr|queryWithParser|queryWithParserWithDefault|"
    r"queryWithParserAndValidate|contains|add|get|getarr)\b"
)


def candidate_keys(parameter: str) -> list[str]:
    value = parameter.strip().strip("`")
    keys = [value]
    if "." in value:
        keys.append(value.rsplit(".", 1)[1])
    keys.extend(parameter_tokens(value))
    return sorted({key for key in keys if key and key not in {"*", "..."}}, key=len, reverse=True)


def parser_literals(text: str) -> set[str]:
    found: set[str] = set()
    for match in re.finditer(r'"([^"\\]*(?:\\.[^"\\]*)*)"', text):
        start = max(0, match.start() - 180)
        end = min(len(text), match.end() + 80)
        if PARSER_WORDS.search(text[start:end]):
            found.add(match.group(1))
    return found


def main() -> None:
    text = MAP.read_text(encoding="utf-8")
    rows = []
    for line_number, line in enumerate(text.splitlines()[10:], 11):
        if not line.startswith("|"):
            continue
        columns = [column.strip() for column in line.split("|")[1:-1]]
        if len(columns) >= 8:
            rows.append((line_number, columns))

    records = []
    for line_number, columns in rows:
        parameter = columns[0]
        references = [item.strip().strip("`") for item in columns[6].split(",")]
        literals: set[str] = set()
        source_token_seen = set()
        source_file_count = 0
        for reference in references:
            for path in source_paths(reference):
                source_file_count += 1
                source_text = path.read_text(encoding="utf-8", errors="ignore")
                source_token_seen.update(key for key in candidate_keys(parameter) if key in source_text)
                literals.update(parser_literals(source_text))
        keys = candidate_keys(parameter)
        matched_literals = sorted(key for key in keys if key in literals)
        if matched_literals:
            category = "parser_literal_anchor"
        elif source_token_seen:
            category = "consumer_or_dynamic_review"
        elif "AMReX-owned" in columns[6] or "AMReX-owned" in columns[7]:
            category = "external_owner_review"
        else:
            category = "no_source_token_review"
        records.append(
            {
                "line": line_number,
                "parameter": parameter,
                "category": category,
                "parser_literal_keys": matched_literals,
                "source_token_keys": sorted(source_token_seen),
                "source_file_count": source_file_count,
            }
        )

    counts = {category: sum(item["category"] == category for item in records) for category in (
        "parser_literal_anchor", "consumer_or_dynamic_review", "external_owner_review", "no_source_token_review"
    )}
    result = {
        "contract": "WarpX parameter-map parser-anchor review surface",
        "parameter_map": str(MAP),
        "row_count": len(records),
        "category_counts": counts,
        "parser_anchor_rows": counts["parser_literal_anchor"],
        "manual_review_rows": len(records) - counts["parser_literal_anchor"],
        "contract_pass": True,
        "classification": "PARSER_LITERAL_ANCHOR_SURFACE_AUDITED_MANUAL_VALUE_SEMANTICS_REMAINS",
        "scope": "cited-source text, parser-like API adjacency and explicit review queue; not C++ AST or runtime value semantics",
        "records": records,
    }
    output_dir = MAP.parent.parent / "runs/stage-c-validation/parameter-map-parser-anchor-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Parameter-map parser-anchor review surface",
        "",
        f"- rows: `{len(records)}`",
        f"- parser-literal anchor rows: `{counts['parser_literal_anchor']}`",
        f"- manual review rows: `{result['manual_review_rows']}`",
        f"- classification: `{result['classification']}`",
        "",
        "This contract records where cited source files contain a parser-like API adjacent to a parameter literal. `consumer_or_dynamic_review` and `external_owner_review` remain explicit manual queues; this report does not claim that a literal anchor proves defaults, validation, aliases, or runtime value semantics.",
        "",
        "| category | rows |",
        "|---|---:|",
    ]
    lines.extend(f"| `{category}` | `{count}` |" for category, count in counts.items())
    lines.extend(["", "## Manual review queue", "", "| line | parameter | category | source-token keys |", "|---:|---|---|---|"])
    for item in records:
        if item["category"] != "parser_literal_anchor":
            lines.append(f"| `{item['line']}` | `{item['parameter']}` | `{item['category']}` | `{', '.join(item['source_token_keys'])}` |")
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"row_count": len(records), "category_counts": counts, "manual_review_rows": result["manual_review_rows"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
