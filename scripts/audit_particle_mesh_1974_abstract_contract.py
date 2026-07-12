#!/usr/bin/env python
"""Audit bounded abstract-level contracts for two 1974 particle-mesh papers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PAPERS = {
    "qpm_pppm": {
        "title": "Quiet high-resolution computer models of a plasma",
        "doi": "10.1016/0021-9991(74)90010-2",
        "source": "https://www.sciencedirect.com/science/article/pii/0021999174900102",
        "terms": ("QPM", "PPPM", "Gaussian", "potential shaping", "noise", "sub-mesh"),
    },
    "force_shaping": {
        "title": "Shaping the force law in two-dimensional particle-mesh models",
        "doi": "10.1016/0021-9991(74)90044-8",
        "source": "https://www.sciencedirect.com/science/article/abs/pii/0021999174900448",
        "terms": ("NGP", "CIC", "nine-point", "potential-correction", "anisotropy", "0.5%"),
    },
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qpm-dir", type=Path, required=True)
    parser.add_argument("--force-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    dirs = {"qpm_pppm": args.qpm_dir.resolve(), "force_shaping": args.force_dir.resolve()}
    papers = {}
    checks = {}
    for key, paper in PAPERS.items():
        paper_dir = dirs[key]
        readme = (paper_dir / "README.md").read_text(encoding="utf-8")
        audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
        note = next(paper_dir.glob("*-中文讲解.md"), None)
        note_text = note.read_text(encoding="utf-8") if note else ""
        paper_checks = {
            "directory_present": paper_dir.is_dir(),
            "title_recorded": paper["title"] in readme,
            "doi_recorded": paper["doi"] in readme,
            "primary_source_recorded": paper["source"] in readme,
            "abstract_topics_recorded": all(term.lower() in audit.lower() or term.lower() in note_text.lower() for term in paper["terms"]),
            "chinese_note_present": bool(note and note.exists()),
            "full_text_boundary_explicit": all(term in audit for term in ("publisher_pdf`: missing", "full_text_line_by_line_compare", "not completed")),
            "note_scope_explicit": "只使用" in note_text and "full-text missing" in note_text,
        }
        papers[key] = {"metadata": paper, "checks": paper_checks}
        checks[key] = all(paper_checks.values())

    result = {
        "contract": "1974 particle-mesh bounded abstract-level literature contracts",
        "papers": papers,
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "ABSTRACT_BACKED_METADATA_VERIFIED_FULL_TEXT_MISSING",
        "scope": "abstract-level evidence only; no publisher-PDF or line-by-line claim",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# 1974 particle-mesh bounded abstract-level contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| paper | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{key}` | `{'PASS' if passed else 'FAIL'}` |" for key, passed in checks.items())
    lines.extend(["", "Both papers are abstract-backed, while publisher full text and line-by-line comparison remain missing."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
