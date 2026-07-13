#!/usr/bin/env python
"""Audit the metadata/access boundary for the unavailable Boris 1970 source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TITLE = "Relativistic plasma simulation--optimization of a hybrid code"
DTIC = "https://apps.dtic.mil/sti/citations/ADA023511"
PDF = "https://apps.dtic.mil/sti/tr/pdf/ADA023511.pdf"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    readme = (paper_dir / "README.md").read_text(encoding="utf-8")
    audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    note = next(paper_dir.glob("*-中文*.md"), None)
    note_text = note.read_text(encoding="utf-8") if note else ""
    checks = {
        "paper_directory_present": paper_dir.is_dir(),
        "title_recorded": TITLE in readme,
        "dtic_record_recorded": DTIC in readme and "ADA023511" in audit,
        "pdf_endpoint_recorded": PDF in readme,
        "bibliographic_scope_recorded": all(term in readme for term in ("J. P. Boris", "pp. 3--67", "1970")),
        "rate_limit_boundary_recorded": "Too many requests" in readme and "rate-limited" in audit,
        "no_local_full_text_claim": all(term in audit for term in ("no Boris 1970 proceedings PDF", "not PDF")),
        "secondary_source_boundary_recorded": "Birdsall and Langdon 1985" in readme and "二手讲解" in note_text,
        "source_mapping_boundary_recorded": "UpdateMomentumBoris.H" in note_text and "逐项相同" in note_text,
        "chinese_note_present": bool(note and note.exists()),
        "reading_log_present": (paper_dir / "reading-log.md").is_file(),
    }
    result = {
        "contract": "Boris 1970 metadata and access-boundary contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "METADATA_BACKED_HISTORICAL_SOURCE_FULL_TEXT_MISSING_SECONDARY_DERIVATION_AVAILABLE",
        "source": DTIC,
        "scope": "bibliographic identity and access boundary only; no original proceedings PDF or line-by-line claim",
        "published": {"title": TITLE, "venue": "Proceedings of the Fourth Conference on Numerical Simulation of Plasmas", "pages": "3-67", "year": 1970},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Boris 1970 metadata contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: [{DTIC}]({DTIC})",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(["", "The contract keeps the original Boris proceedings source separate from the Birdsall secondary derivation and WarpX implementation source."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
