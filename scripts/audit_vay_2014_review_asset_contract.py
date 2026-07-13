#!/usr/bin/env python
"""Audit the local Vay-Godfrey 2014 relativistic PIC review package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


PAPER = "2014_VayFRACAD2014_Modeling_of_relativistic_plasmas_with_the_Particle-In-Cell_method"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = (args.root / "references/01_reviews_surveys" / PAPER).resolve()
    pdf = paper_dir / f"{PAPER}.pdf"
    markdown = paper_dir / f"{PAPER}.md"
    note = paper_dir / f"{PAPER}-中文讲解.md"
    access = paper_dir / "access-audit.md"
    reading_log = paper_dir / "reading-log.md"
    md_text = markdown.read_text(encoding="utf-8")
    note_text = note.read_text(encoding="utf-8")
    access_text = access.read_text(encoding="utf-8")

    checks = {
        "pdf_present": pdf.exists() and pdf.stat().st_size > 0,
        "pdf_is_nine_pages": pdf.exists() and len(PdfReader(str(pdf)).pages) == 9,
        "mineru_markdown_present": markdown.exists() and markdown.stat().st_size > 0,
        "mineru_section_surface": all(
            marker in md_text
            for marker in (
                "## 1. Introduction",
                "## 2. Particle-In-Cell main steps",
                "## 2.1.3. Pseudo Spectral Analytical Time Domain (PSATD)",
                "## 3. Numerical stability",
                "## 4. Conclusion",
            )
        ),
        "image_count_is_forty_three": len(list((paper_dir / "images").glob("*"))) == 43,
        "note_formula_surface": all(
            marker in note_text
            for marker in (
                "\\tag{5}",
                "\\tag{22--24}",
                "\\tag{32--35}",
                "\\tag{39}",
                "C=\\cos(k\\Delta t)",
                "g(\\alpha,k)",
            )
        ),
        "note_figure_surface": all(
            marker in note_text
            for marker in (
                "images/66e6c3ea9d58f09321242dcfa15d2925b03fcfc4452c037adff180a2ca44c1fd.jpg",
                "images/badbf811d884ff5857e014253529dc0428691100e090e33164d8791bef1a3d4b.jpg",
                "images/c5cee7fa3524c01e4a755acee5803f58a85237c719cbf12c98a1e61d2f0493e7.jpg",
                "images/c5cc80fc62cb38c50ffc26e5e1c034772f27f902fc2dc7a67d37acb789d13d81.jpg",
            )
        ),
        "metadata_and_boundary_recorded": all(
            marker in access_text
            for marker in (
                "10.1016/j.crme.2014.07.006",
                "Warp/WarpX boundary",
                "current WarpX equivalence is not claimed",
            )
        ),
        "reading_log_present": reading_log.exists() and reading_log.stat().st_size > 0,
    }
    result = {
        "contract": "Vay-Godfrey 2014 relativistic PIC review asset",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "FULL_TEXT_MINERU_CHINESE_NOTE_VERIFIED_WARP_ERA_REVIEW_WARPX_RUNTIME_BOUNDARY",
        "scope": "review-level equations, algorithm taxonomy and NCI source; not a current WarpX function-level or runtime equivalence proof",
        "paper_dir": str(paper_dir),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Vay-Godfrey 2014 relativistic PIC review asset contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The package is a full-text review asset. Its historical Warp results remain separate from current WarpX source and runtime evidence.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
