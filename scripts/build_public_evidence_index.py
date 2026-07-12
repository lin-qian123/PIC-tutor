#!/usr/bin/env python
"""Build a path-redacted digest of local validation contracts for public release."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


METRIC_KEY = re.compile(
    r"(error|residual|relative|absolute|energy|charge|field|weight|count|ratio|pages|passed|pass$|gate|status)",
    re.IGNORECASE,
)
FORBIDDEN = ("/Volumes/", "/Users/", "file://")


def safe_scalar(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool))


def status(data: dict[str, Any]) -> str:
    for key in ("passed", "contract_pass", "success", "analysis_passed"):
        if isinstance(data.get(key), bool):
            return "PASS" if data[key] else "FAIL"
    return "UNKNOWN"


def summary_metrics(data: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in data.items():
        if key in {"source", "source_files", "published", "checks", "anchors", "rows", "papers"}:
            continue
        if METRIC_KEY.search(key) and safe_scalar(value):
            if isinstance(value, str) and any(token in value for token in FORBIDDEN):
                continue
            result[key] = value
    return dict(sorted(result.items()))


def evidence_kind(data: dict[str, Any], raw_status: str) -> str:
    classification = str(data.get("classification") or "").upper()
    if any(token in classification for token in ("BOUNDARY", "UNPROVEN", "MISSING")):
        return "BOUNDARY"
    return raw_status


def build_index(root: Path) -> dict[str, Any]:
    records = []
    for path in sorted(root.rglob("contract.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        raw_status = status(data)
        records.append(
            {
                "case": path.parent.name,
                "status": raw_status,
                "evidence_kind": evidence_kind(data, raw_status),
                "contract": data.get("contract") or data.get("case") or path.parent.name,
                "classification": data.get("classification"),
                "scope": data.get("scope"),
                "metrics": summary_metrics(data),
            }
        )
    status_counts = {value: sum(record["status"] == value for record in records) for value in ("PASS", "FAIL", "UNKNOWN")}
    evidence_counts = {value: sum(record["evidence_kind"] == value for record in records) for value in ("PASS", "FAIL", "UNKNOWN", "BOUNDARY")}
    return {
        "index": "PIC-tutor public validation evidence digest",
        "source_scope": "local stage-c-validation contract.json files; raw runs and references remain excluded from public release",
        "record_count": len(records),
        "status_counts": status_counts,
        "evidence_kind_counts": evidence_counts,
        "status_semantics": "status is the raw contract boolean; evidence_kind marks classified boundary, unproven, or missing evidence explicitly",
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    result = build_index(args.input_root.resolve())
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Public validation evidence digest",
        "",
        "This is a path-redacted summary of local validation contracts. Raw `runs/` outputs are intentionally excluded from the public release.",
        "",
        f"- records: `{result['record_count']}`",
        f"- PASS: `{result['status_counts']['PASS']}`",
        f"- FAIL: `{result['status_counts']['FAIL']}`",
        f"- UNKNOWN: `{result['status_counts']['UNKNOWN']}`",
        f"- boundary-classified: `{result['evidence_kind_counts']['BOUNDARY']}`",
        "",
        "`status` preserves the raw contract boolean. `evidence_kind=BOUNDARY` marks records whose classification says the result is a boundary, unproven, or missing-evidence condition; it is not equivalent to a regression.",
        "",
        "| case | raw status | evidence kind | contract | classification | scope | selected metrics |",
        "|---|:---:|:---:|---|---|---|---|",
    ]
    for record in result["records"]:
        metrics = ", ".join(f"`{key}={value}`" for key, value in record["metrics"].items())
        lines.append(
            f"| `{record['case']}` | `{record['status']}` | `{record['evidence_kind']}` | {record['contract'] or ''} | "
            f"`{record['classification'] or ''}` | {record['scope'] or ''} | {metrics} |"
        )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("record_count", "status_counts")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
