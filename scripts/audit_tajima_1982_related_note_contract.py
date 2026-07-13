#!/usr/bin/env python
"""Audit the full-text asset contract for the related Tajima 1982 note."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TITLE = "Laser accelerator by plasma waves for ultra-high energies"
FNAL = "https://lss.fnal.gov/conf/C8209271/"
FNAL_PDF = "https://lss.fnal.gov/conf/C8209271/p169.pdf"
MIRROR = "https://s3.cern.ch/inspire-prod-files/f/f67b6a23b61b8c9d9b9416870e409a72"
FORMAL_DOI = "10.1063/1.33805"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    pdf = paper_dir / "1982_Tajima_related_FNAL_conference_note_Laser_accelerator_by_plasma_waves.pdf"
    conversion_dir = paper_dir / "1982_Tajima_related_FNAL_conference_note_Laser_accelerator_by_plasma_waves"
    markdown = conversion_dir / "1982_Tajima_related_FNAL_conference_note_Laser_accelerator_by_plasma_waves.md"
    images = conversion_dir / "images"
    readme = (paper_dir / "README.md").read_text(encoding="utf-8")
    audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    note = next(paper_dir.glob("*-中文讲解.md"), None)
    note_text = note.read_text(encoding="utf-8") if note else ""
    checks = {
        "paper_directory_present": paper_dir.is_dir(),
        "pdf_present": pdf.is_file() and pdf.stat().st_size > 1_000_000,
        "pdf_page_and_size_recorded": "26 pages" in audit and "1,513,200 bytes" in audit,
        "title_recorded": TITLE.lower() in readme.lower() and TITLE.lower() in markdown.read_text(encoding="utf-8").lower(),
        "provenance_urls_recorded": all(url in readme for url in (FNAL, FNAL_PDF, MIRROR)),
        "mineru_markdown_present": markdown.is_file() and markdown.stat().st_size > 10_000,
        "mineru_images_present": images.is_dir() and len(list(images.glob("*"))) >= 50,
        "chinese_note_present": bool(note and note.exists()),
        "note_topics_recorded": all(term in note_text for term in ("beat-wave", "前向 Raman", "退相位", "丝化", "Brillouin")),
        "formal_item_not_substituted": all(term in (readme + audit + note_text) for term in (FORMAL_DOI, "不能替代", "not substituted")),
        "ocr_boundary_recorded": "OCR" in audit and "PDF" in audit,
    }
    result = {
        "contract": "Tajima 1982 related FNAL conference note full-text asset contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "RELATED_SINGLE_AUTHOR_CONFERENCE_NOTE_FULL_TEXT_MINERU_VERIFIED_FORMAL_TAJIMA_DAWSON_ITEM_NOT_SUBSTITUTED",
        "formal_item": {"doi": FORMAL_DOI, "full_text_status": "missing; tracked separately"},
        "sources": [FNAL, FNAL_PDF, MIRROR],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Tajima 1982 related note contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- formal Tajima--Dawson DOI: `{FORMAL_DOI}`; status: separate missing-full-text record",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(["", "The related conference note is full-text materialized, but it does not substitute the formal Tajima--Dawson item."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
