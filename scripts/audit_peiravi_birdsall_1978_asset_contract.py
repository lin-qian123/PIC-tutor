#!/usr/bin/env python
"""Audit the local full-text asset contract for Peiravi and Birdsall 1978."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TITLE = "Self-heating of 1d Thermal Plasma"
REPORT_NO = "UCB/ERL M78/32"
RECORD_URL = "https://digicoll.lib.berkeley.edu/record/137351"
PDF_URL = "https://digicoll.lib.berkeley.edu/record/137351/files/ERL-m-78-32.pdf"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    pdf = next(paper_dir.glob("*.pdf"), None)
    mineru_dir = next((path for path in paper_dir.iterdir() if path.is_dir() and (path / "images").is_dir()), None)
    mineru_md = next(mineru_dir.glob("*.md"), None) if mineru_dir else None
    note = next(paper_dir.glob("*-中文讲解.md"), None)
    readme = (paper_dir / "README.md").read_text(encoding="utf-8")
    audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    log = (paper_dir / "reading-log.md").read_text(encoding="utf-8")
    note_text = note.read_text(encoding="utf-8") if note else ""
    image_links = re.findall(r"!\[[^]]*\]\((images/[^)]+)\)", note_text)
    missing_image_links = [link for link in image_links if not (mineru_dir / link).exists()] if mineru_dir else image_links
    checks = {
        "paper_directory_present": paper_dir.is_dir(),
        "pdf_present": bool(pdf and pdf.stat().st_size > 1_000_000),
        "report_metadata_recorded": TITLE.lower() in readme.lower() and REPORT_NO in readme,
        "institutional_record_recorded": RECORD_URL in readme and PDF_URL in readme,
        "mineru_markdown_present": bool(mineru_md and mineru_md.exists()),
        "figure_assets_present": bool(mineru_dir and len(list((mineru_dir / "images").glob("*.jpg"))) >= 10),
        "note_image_links_resolve": not missing_image_links,
        "chinese_note_present": bool(note and note.exists()),
        "note_topics_present": all(term in note_text for term in ("tau_h", "NGP", "CIC", "QS", "k-space", "thermal loader")),
        "note_boundary_present": "不是已确认的期刊 publisher PDF" in note_text and "OCR" in note_text,
        "access_boundary_present": all(term in audit for term in ("institutional_full_text", "publisher_pdf", "journal_version_line_by_line_compare")),
        "reading_log_present": "2026-07-13 第一轮" in log,
    }
    result = {
        "contract": "Peiravi and Birdsall 1978 local full-text technical-report asset contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "INSTITUTIONAL_FULL_TEXT_MINERU_VERIFIED_JOURNAL_VERSION_NOT_ESTABLISHED",
        "scope": "technical-report full text and figures available; no publisher-journal equivalence claim",
        "source": RECORD_URL,
        "report": {"title": "Self-heating of 1d Thermal Plasma; Comparison of Weightings; Optimal Parameter Choices", "report_no": REPORT_NO},
        "note_image_links": {"count": len(image_links), "missing": missing_image_links},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Peiravi and Birdsall 1978 full-text asset contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: [{RECORD_URL}]({RECORD_URL})",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(["", "The report PDF and MinerU assets are local; journal-version equivalence remains unclaimed."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
