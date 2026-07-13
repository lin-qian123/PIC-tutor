#!/usr/bin/env python
"""Audit the paper-level asset contract for Tajima and Dawson 1979."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TITLE = "Laser Electron Accelerator"
DOI = "10.1103/PhysRevLett.43.267"
SOURCE = "https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.43.267"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    stem = "1979_TajimaDawson_Laser_Electron_Accelerator"
    pdf = paper_dir / f"{stem}.pdf"
    conversion_dir = paper_dir / stem
    markdown = conversion_dir / f"{stem}.md"
    images = conversion_dir / "images"
    readme = (paper_dir / "README.md").read_text(encoding="utf-8")
    audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    note = paper_dir / f"{stem}-中文讲解.md"
    note_text = note.read_text(encoding="utf-8")
    checks = {
        "paper_directory_present": paper_dir.is_dir(),
        "pdf_present": pdf.is_file() and pdf.stat().st_size > 200_000,
        "pdf_page_and_size_recorded": "4 pages" in audit and "288,010 bytes" in audit,
        "bibliography_recorded": all(term in readme for term in (TITLE, DOI, SOURCE, "T. Tajima and J. M. Dawson")),
        "mineru_markdown_present": markdown.is_file() and markdown.stat().st_size > 10_000,
        "figure_assets_present": images.is_dir() and len(list(images.glob("*"))) >= 10,
        "chinese_note_present": note.is_file() and note.stat().st_size > 4_000,
        "note_topics_present": all(term in note_text for term in ("driver -> wake -> trapping -> acceleration", "wave-breaking", "Raman", "1 1/2-D", "Fig.1")),
        "runtime_boundary_present": all(term in readme + audit + note_text for term in ("not a modern WarpX regression contract", "regression", "moving-window")),
        "reading_log_present": (paper_dir / "reading-log.md").is_file(),
    }
    result = {
        "contract": "Tajima and Dawson 1979 paper-level full-text asset contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "FULL_TEXT_MINERU_VERIFIED_EARLY_LWFA_SCALING_BASELINE_MODERN_WARPX_RUNTIME_NOT_SUBSTITUTED",
        "source": SOURCE,
        "published": {"title": TITLE, "doi": DOI, "journal": "Physical Review Letters 43(4), 267-270 (1979)"},
        "scope": "paper-backed early LWFA mechanism and scaling; not a current WarpX regression contract",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Tajima and Dawson 1979 asset contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: [{SOURCE}]({SOURCE})",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(["", "The paper is a historical full-text source and scaling baseline; it does not substitute for modern WarpX runtime evidence."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
