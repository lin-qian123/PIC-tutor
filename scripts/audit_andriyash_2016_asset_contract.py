#!/usr/bin/env python
"""Audit the local Andriyash 2016 Fourier-Bessel PIC paper package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


PAPER = "2016_AndriyashPoP2016_Laser-plasma_interactions_with_a_Fourier-Bessel_particle-in-cell_method"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = (args.root / "references/03_pic_foundations" / PAPER).resolve()
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
                "## I. INTRODUCTION",
                "## II. PHYSICAL AND MATHEMATICAL MODELS",
                "## III. SIMULATIONS",
                "## Appendix A: Definition of Fourier-Bessel transform",
                "## Appendix B: Useful diferential properties of Fourier-Bessel transform",
            )
        ),
        "image_count_is_twenty_six": len(list((paper_dir / "images").glob("*"))) == 26,
        "note_formula_surface": all(
            marker in note_text
            for marker in (
                "\\tag{1}",
                "\\tag{3a}",
                "\\tag{5}",
                "\\tag{7}",
                "\\tag{8}",
                "\\tag{9}",
                "\\tag{A1}",
                "\\tag{B1}",
            )
        ),
        "note_image_surface": all(
            marker in note_text
            for marker in (
                "images/06c8f8fa6cea2ccf46a8b640200507a625159b2f21ddbe72877165ba400368b6.jpg",
                "images/dfe72677d850f09772d6e8adda3fc06015e50823da3a92fa6534e1ed40f33f4a.jpg",
                "images/000f9d2e7c267e2ca9943cb1b6cbd9f166ae7d45edc465eb85018129d445e456.jpg",
                "images/439cea85305f25514d78372097fc31f70e729288fc6f76c77327811f879e5e79.jpg",
                "images/2c193125b8089e715cf3970df28d22923828c9984a16fd8b3c0d5dfa70d24995.jpg",
            )
        ),
        "ocr_curl_correction_recorded": "OCR" in note_text and "\\nabla\\times\\mathbf{b}" in note_text,
        "metadata_and_boundary_recorded": all(
            marker in access_text
            for marker in ("10.1063/1.4943281", "PLARES-PIC", "WarpX equivalence")
        ),
        "reading_log_present": reading_log.exists() and reading_log.stat().st_size > 0,
    }
    result = {
        "contract": "Andriyash 2016 Fourier-Bessel PIC paper asset",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "FULL_TEXT_MINERU_CHINESE_NOTE_VERIFIED_WARPX_EQUIVALENCE_BOUNDARY",
        "scope": "local paper asset, formula/figure reading and PLARES-PIC versus WarpX evidence boundary; not a WarpX runtime reproduction",
        "paper_dir": str(paper_dir),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Andriyash 2016 Fourier-Bessel PIC paper asset contract",
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
        "The package is a formula-level full-text asset for the PLARES-PIC paper. It does not claim function-level or runtime equivalence with WarpX.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
