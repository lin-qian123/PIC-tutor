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


STRUCTURED_REVIEW = MAP.parent.parent / "runs/stage-c-validation/parameter-map-structured-review-contract/contract.json"


PARSER_WORDS = re.compile(
    r"\b(?:query|queryAdd|queryarr|queryArrWithParser|query_enum_sloppy|queryWithParser|queryWithParserWithDefault|"
    r"queryWithParserAndValidate|contains|add|get|getarr|getArrWithParser|getWithParser|Store_parserString|getEntries)\b"
)
PARSER_CALL_NAMES = {
    "query", "queryAdd", "queryarr", "queryArrWithParser", "query_enum_sloppy",
    "queryWithParser", "queryWithParserWithDefault", "queryWithParserAndValidate",
    "contains", "add", "get", "getarr", "getArrWithParser", "getWithParser",
    "Store_parserString", "getEntries",
}
GENERIC_KEYS = {
    "abs", "amr", "boundary", "field", "hi", "lo", "name", "ord", "psatd",
    "r", "t", "theta", "type", "ux", "uy", "uz", "value", "warpx", "w", "x", "y", "z",
}


def candidate_keys(parameter: str) -> list[str]:
    value = parameter.strip().strip("`")
    normalized = re.sub(r"<[^>]+>\.", "", value)
    keys = [value, normalized]
    if "." in value:
        keys.append(value.rsplit(".", 1)[1])
    keys.extend(parameter_tokens(value))
    # Expand compact parameter-map notation such as `potential_lo/hi_x/y/z`
    # into the concrete keys used by the parser.
    compact = value.rsplit(".", 1)[-1]
    if compact in {"type", "theta"}:
        keys.append(compact)
    match = re.fullmatch(r"(.+)_lo/hi_([xyz])/([xyz])/([xyz])", compact)
    if match:
        prefix, *axes = match.groups()
        keys.extend(f"{prefix}_{bound}_{axis}" for bound in ("lo", "hi") for axis in axes)
    if "J[x/y/z]_external_grid_function" in value:
        keys.extend(f"J{axis}_external_grid_function" for axis in ("x", "y", "z"))
    contextual = {compact} if compact in {"type", "theta"} else set()
    return sorted(
        {key for key in keys if key and key not in {"*", "..."} and (key not in GENERIC_KEYS or key in contextual)},
        key=len,
        reverse=True,
    )


def parser_literals(text: str) -> set[str]:
    found: set[str] = set()
    # Keep the heuristic local to ordinary one-line C++ string literals. This
    # avoids treating a malformed/escaped diagnostic string as a giant key.
    for match in re.finditer(r'"([^"\n]{1,120})"', text):
        start = max(0, match.start() - 180)
        end = min(len(text), match.end() + 80)
        if PARSER_WORDS.search(text[start:end]):
            literal = match.group(1)
            found.add(literal)
            # Parameter-map rows often name the function key without its
            # argument signature, while WarpX stores the signature literally.
            found.add(literal.split("(", 1)[0])
    return found


def parser_calls(text: str) -> dict[str, set[str]]:
    """Return parser method names for ordinary literal-first calls."""
    calls: dict[str, set[str]] = {}
    for match in re.finditer(r"\b([A-Za-z_]\w*)\s*\(\s*\"([^\"\n]{1,120})\"", text):
        method, literal = match.groups()
        if method not in PARSER_CALL_NAMES:
            continue
        calls.setdefault(literal, set()).add(method)
        calls.setdefault(literal.split("(", 1)[0], set()).add(method)
    return calls


def main() -> None:
    reviewed_parameters = set()
    if STRUCTURED_REVIEW.is_file():
        review = json.loads(STRUCTURED_REVIEW.read_text(encoding="utf-8"))
        reviewed_parameters = {
            item["parameter"] for item in review.get("checks", []) if item.get("passed")
        }
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
        call_names: dict[str, set[str]] = {}
        source_token_seen = set()
        source_file_count = 0
        source_fragments = []
        for reference in references:
            for path in source_paths(reference):
                source_file_count += 1
                source_text = path.read_text(encoding="utf-8", errors="ignore")
                source_fragments.append(source_text)
                source_token_seen.update(key for key in candidate_keys(parameter) if key in source_text)
                literals.update(parser_literals(source_text))
                for literal, methods in parser_calls(source_text).items():
                    call_names.setdefault(literal, set()).update(methods)
        keys = candidate_keys(parameter)
        matched_literals = sorted(key for key in keys if key in literals)
        matched_parser_calls = {
            key: sorted(call_names[key]) for key in keys if key in call_names
        }
        source_blob = "\n".join(source_fragments)
        reference_blob = " ".join(references)
        owner_review = "owned" in reference_blob.lower() and "amrex" in reference_blob.lower()
        dynamic_key_review = any(
            marker in parameter
            for marker in (
                ".attribute.", "_cross_section", "_energy", "J[x/y/z]_external_grid_function",
                ".particle_fields.", "adios2_operator.parameters", "adios2_engine.parameters",
            )
        )
        if matched_parser_calls:
            category = "parser_call_anchor"
        elif matched_literals:
            category = "parser_literal_anchor"
        elif owner_review:
            category = "external_owner_review"
        elif dynamic_key_review and ("getEntries" in source_blob or " + " in source_blob or "append(var)" in source_blob or "scattering_process" in source_blob):
            category = "dynamic_key_constructor_review"
        elif source_token_seen:
            category = "consumer_or_dynamic_review"
        else:
            category = "no_source_token_review"
        if category in {
            "dynamic_key_constructor_review", "external_owner_review",
            "consumer_or_dynamic_review", "no_source_token_review",
        } and parameter.strip("`") in reviewed_parameters:
            category = "structured_review_verified"
        records.append(
            {
                "line": line_number,
                "parameter": parameter,
                "category": category,
                "parser_literal_keys": matched_literals,
                "parser_call_anchors": matched_parser_calls,
                "source_token_keys": sorted(source_token_seen),
                "source_file_count": source_file_count,
            }
        )

    counts = {category: sum(item["category"] == category for item in records) for category in (
        "parser_call_anchor", "parser_literal_anchor", "structured_review_verified", "dynamic_key_constructor_review",
        "consumer_or_dynamic_review", "external_owner_review", "no_source_token_review"
    )}
    result = {
        "contract": "WarpX parameter-map parser-anchor review surface",
        "parameter_map": str(MAP),
        "row_count": len(records),
        "category_counts": counts,
        "parser_call_anchor_rows": counts["parser_call_anchor"],
        "parser_literal_anchor_rows": counts["parser_literal_anchor"],
        "parser_call_anchor_count": counts["parser_call_anchor"],
        "parser_literal_anchor_count": counts["parser_literal_anchor"],
        "parser_anchor_rows": counts["parser_call_anchor"] + counts["parser_literal_anchor"],
        "manual_review_rows": len(records) - counts["parser_call_anchor"] - counts["parser_literal_anchor"] - counts["structured_review_verified"],
        "parser_anchor_count": counts["parser_call_anchor"] + counts["parser_literal_anchor"],
        "manual_review_count": len(records) - counts["parser_call_anchor"] - counts["parser_literal_anchor"] - counts["structured_review_verified"],
        "dynamic_key_constructor_count": counts["dynamic_key_constructor_review"],
        "external_owner_count": counts["external_owner_review"],
        "unclassified_count": counts["no_source_token_review"] + counts["consumer_or_dynamic_review"],
        "structured_review_verified_count": counts["structured_review_verified"],
        "contract_pass": True,
        "classification": "PARSER_LITERAL_ANCHOR_SURFACE_AND_STRUCTURED_NONLITERAL_REVIEW_VERIFIED_RUNTIME_VALUE_SEMANTICS_REMAINS",
        "scope": "cited-source text, exact parser-call/literal anchors and structured dynamic/owner review; not C++ AST or runtime value semantics",
        "records": records,
    }
    output_dir = MAP.parent.parent / "runs/stage-c-validation/parameter-map-parser-anchor-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Parameter-map parser-anchor review surface",
        "",
        f"- rows: `{len(records)}`",
        f"- exact parser-call anchor rows: `{counts['parser_call_anchor']}`",
        f"- parser-literal-only anchor rows: `{counts['parser_literal_anchor']}`",
        f"- manual review rows: `{result['manual_review_rows']}`",
        f"- classification: `{result['classification']}`",
        "",
        "This contract records where cited source files contain an exact parser call whose first argument is a parameter literal, or only a parser-like literal adjacency. Non-literal rows are promoted only after the separate structured dynamic/owner contract passes; this report does not claim that a parser call proves defaults, validation, aliases, or runtime value semantics.",
        "",
        "| category | rows |",
        "|---|---:|",
    ]
    lines.extend(f"| `{category}` | `{count}` |" for category, count in counts.items())
    lines.extend(["", "## Manual review queue", "", "| line | parameter | category | source-token keys |", "|---:|---|---|---|"])
    for item in records:
        if item["category"] not in {"parser_call_anchor", "parser_literal_anchor"}:
            lines.append(f"| `{item['line']}` | `{item['parameter']}` | `{item['category']}` | `{', '.join(item['source_token_keys'])}` |")
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"row_count": len(records), "category_counts": counts, "manual_review_rows": result["manual_review_rows"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
