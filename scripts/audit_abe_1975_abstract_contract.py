#!/usr/bin/env python
"""Audit the bounded abstract-level literature contract for Abe et al. 1975."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TITLE = "Grid effects on the plasma simulation by the finite-sized particle"
DOI = "10.1016/0021-9991(75)90085-6"
SOURCE = "https://www.sciencedirect.com/science/article/abs/pii/0021999175900856"


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
        "primary_abstract_source_recorded": SOURCE in readme,
        "abstract_topics_recorded": all(term in note_text for term in ("sigma(K_g)", "correlation", "CIC-PIC", "SUDS", "stochastic")),
        "chinese_note_present": bool(note and note.exists()),
        "full_text_boundary_explicit": all(term in audit for term in ("publisher_pdf`: missing", "full_text_line_by_line_compare", "not generated")),
        "note_scope_explicit": "只使用 ScienceDirect abstract record" in note_text and "FULL_TEXT_MISSING" in note_text,
    }
    result = {
        "contract": "Abe et al. 1975 bounded abstract-level literature contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "ABSTRACT_BACKED_METADATA_VERIFIED_FULL_TEXT_MISSING",
        "scope": "abstract-level evidence only; no publisher-PDF or line-by-line claim",
        "source": SOURCE,
        "published": {"title": TITLE, "doi": DOI, "journal": "Journal of Computational Physics 19(2), 134-149 (1975)"},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Abe et al. 1975 bounded abstract-level contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: [{SOURCE}]({SOURCE})",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(["", "The contract records abstract-backed metadata while keeping full-text and line-by-line comparison unavailable."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
