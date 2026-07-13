#!/usr/bin/env python
"""Audit the Vranic 2015 particle-merging reading package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    source_md = paper_dir / "2015_Vranic2015_Particle_merging_algorithm_for_PIC_codes.md"
    note = paper_dir / "2015_Vranic2015_Particle_merging_algorithm_for_PIC_codes-中文讲解.md"
    pdf = paper_dir / "2015_Vranic2015_Particle_merging_algorithm_for_PIC_codes.pdf"
    readme = paper_dir / "README.md"
    audit = paper_dir / "access-audit.md"
    chapter = args.chapter.resolve().read_text(encoding="utf-8")
    source = source_md.read_text(encoding="utf-8") if source_md.exists() else ""
    note_text = note.read_text(encoding="utf-8") if note.exists() else ""
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    audit_text = audit.read_text(encoding="utf-8") if audit.exists() else ""
    images = sorted((paper_dir / "images").glob("*")) if (paper_dir / "images").is_dir() else []

    checks = {
        "pdf_present": pdf.exists(),
        "pdf_page_count_24": pdf.exists() and len(PdfReader(str(pdf)).pages) == 24,
        "mineru_markdown_present": source_md.exists(),
        "source_section_order": all(marker in source for marker in ("## 1. Introduction", "## 2. Algorithm", "## 3. Merging rate", "## 4. Numerical simulations", "## 5. Conclusions")),
        "source_formula_anchors": all(marker in source for marker in ("tag{1}", "tag{3}", "tag{7}", "tag{17}", "tag{18}")),
        "extracted_images_32": len(images) == 32,
        "chinese_note_present": note.exists(),
        "chinese_note_figures_and_formulas": all(marker in note_text for marker in ("images/38db895", "images/e19df43", "images/672b42", "$$", "WarpX")),
        "bibliographic_identity": all(marker in readme_text for marker in ("Particle merging algorithm for PIC codes", "10.1016/j.cpc.2015.01.020")),
        "access_boundary": "FULLTEXT_PAPER_BACKED_PARTICLE_MERGING_WARPX_MAPPING_RUNTIME_SEPARATE" in audit_text and "runtime" in audit_text,
        "chapter_mapping": all(marker in chapter for marker in ("Vranic 2015", "VelocityCoincidenceThinning", "两粒子", "checksum")),
    }
    result = {
        "contract": "Vranic 2015 particle-merging paper asset contract",
        "classification": "FULLTEXT_PAPER_BACKED_PARTICLE_MERGING_WARPX_MAPPING_RUNTIME_SEPARATE",
        "scope": "local PDF/MinerU/Chinese note and Chapter 4 mapping; no claim of WarpX paper-case reproduction",
        "checks": checks,
        "passed": all(checks.values()),
        "asset": {"pdf_pages": len(PdfReader(str(pdf)).pages) if pdf.exists() else 0, "image_count": len(images)},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Vranic 2015 particle-merging paper asset contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", "The local paper package supports algorithm explanation and a bounded WarpX mapping; it does not replace a dedicated WarpX resampling physics consumer."]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {sum(checks.values())}/{len(checks)} Vranic 2015 asset checks")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
