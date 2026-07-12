#!/usr/bin/env python
"""Audit the bounded indexed-abstract contract for Yee 1966."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TITLE = "Numerical solution of initial boundary value problems involving Maxwell's equations in isotropic media"
DOI = "10.1109/TAP.1966.1138693"
OPENAIRE_URL = "https://explore.openaire.eu/search/publication?pid=10.1109%2Ftap.1966.1138693"


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
        "indexed_abstract_source_recorded": OPENAIRE_URL in readme,
        "abstract_scope_recorded": all(term in audit for term in ("finite-difference equations", "field-point", "conducting cylinder")),
        "chinese_note_present": bool(note and note.exists()),
        "full_text_boundary_explicit": all(term in audit for term in ("publisher_pdf`: missing", "full_text_line_by_line_compare", "not completed")),
        "access_response_recorded": "HTTP `418`" in audit and "text/html" in audit,
        "note_scope_explicit": "indexed abstract" in note_text and "full-text missing" in note_text,
    }
    result = {
        "contract": "Yee 1966 bounded indexed-abstract literature contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "INDEXED_ABSTRACT_BACKED_METADATA_VERIFIED_IEEE_FULL_TEXT_MISSING",
        "scope": "indexed abstract-level evidence only; no IEEE publisher-PDF or line-by-line claim",
        "source": OPENAIRE_URL,
        "published": {"title": TITLE, "doi": DOI, "journal": "IEEE Transactions on Antennas and Propagation 14(3), 302-307 (1966)"},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Yee 1966 bounded indexed-abstract contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: [{OPENAIRE_URL}]({OPENAIRE_URL})",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(["", "The contract records indexed abstract evidence and the IEEE full-text access boundary separately."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
