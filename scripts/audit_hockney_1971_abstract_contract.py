#!/usr/bin/env python
"""Audit the bounded abstract-level Hockney 1971 literature contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TITLE = "Measurements of collision and heating times in a two-dimensional thermal computer plasma"
DOI = "10.1016/0021-9991(71)90032-5"
IBM_URL = "https://research.ibm.com/publications/measurements-of-collision-and-heating-times-in-a-two-dimensional-thermal-computer-plasma"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    readme = (paper_dir / "README.md").read_text(encoding="utf-8")
    audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    note = next(paper_dir.glob("*-中文讲解.md"), None)
    note_text = note.read_text(encoding="utf-8") if note else ""
    checks = {
        "paper_directory_present": paper_dir.is_dir(),
        "title_recorded": TITLE in readme,
        "doi_recorded": DOI in readme,
        "primary_abstract_source_recorded": IBM_URL in readme,
        "abstract_topics_recorded": all(
            term in audit for term in ("NGP", "CIC", "HNGP", "HCIC", "optimum", "K_2")
        ),
        "chinese_note_present": bool(note and note.exists()),
        "full_text_boundary_explicit": all(
            term in audit for term in ("publisher_pdf`: missing", "full_text_line_by_line_compare", "not completed")
        ),
        "note_scope_explicit": "只使用 IBM Research" in note_text and "full-text missing" in note_text,
    }
    result = {
        "contract": "Hockney 1971 bounded abstract-level literature contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "ABSTRACT_BACKED_METADATA_VERIFIED_FULL_TEXT_MISSING",
        "scope": "abstract-level evidence only; no publisher-PDF or line-by-line claim",
        "source": IBM_URL,
        "published": {"title": TITLE, "doi": DOI, "journal": "Journal of Computational Physics 8(1), 19-44 (1971)"},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Hockney 1971 bounded abstract-level contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: [{IBM_URL}]({IBM_URL})",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.append("")
    lines.append("The contract upgrades the local evidence to abstract-backed, while keeping the missing full-text boundary explicit.")
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
