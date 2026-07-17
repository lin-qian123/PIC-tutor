"""Audit the Muraviev 2021 particle-resampling reading package."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def pdf_pages(pdf: Path) -> int:
    result = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, capture_output=True)
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise ValueError("pdfinfo did not report Pages")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    stem = "2021_MuravievCPC2021_Strategies_for_particle_resampling_in_PIC_simulations"
    paper_dir = args.paper_dir
    source_pdf = paper_dir / f"{stem}.pdf"
    source_md = paper_dir / f"{stem}.md"
    note = paper_dir / f"{stem}-中文讲解.md"
    readme = paper_dir / "README.md"
    access = paper_dir / "access-audit.md"
    reading_log = paper_dir / "reading-log.md"
    images = sorted((paper_dir / "images").glob("*"))
    source = source_md.read_text(encoding="utf-8") if source_md.exists() else ""
    note_text = note.read_text(encoding="utf-8") if note.exists() else ""
    chapter = args.chapter.read_text(encoding="utf-8") if args.chapter.exists() else ""

    checks = {
        "pdf_present": source_pdf.is_file(),
        "pdf_pages": source_pdf.is_file() and pdf_pages(source_pdf) == 50,
        "mineru_markdown_present": source_md.is_file(),
        "section_order": all(
            marker in source
            for marker in (
                "## Abstract",
                "## 1. Introduction",
                "## 2. The principle of agnostic down-sampling",
                "## 3. Strategies of down-sampling",
                "## 4. Comparison of resampling methods on test problems",
                "## 5. Comparison of methods on pertinent physical problems",
                "## 6. Conclusion",
            )
        ),
        "formula_anchors": all(f"\\tag{{{number}}}" in source for number in range(1, 8)),
        "image_assets": len(images) == 38,
        "figure_sequence": all(f"Figure {number}:" in source for number in range(1, 13)),
        "reading_package": all(path.is_file() for path in (note, readme, access, reading_log)),
        "note_markers": all(
            marker in note_text
            for marker in (
                "agnostic down-sampling",
                "number-conservative thinning",
                "energyT",
                "conserv",
                "Weibel",
                "QED cascade",
                "图 10",
                "PICADOR",
            )
        ),
        "chapter_mapping": all(
            marker in chapter
            for marker in (
                "Muraviev 2021",
                "agnostic",
                "resampling",
                "局部总权重",
                "权重尾",
            )
        ),
    }
    result = {
        "contract": "Muraviev 2021 particle-resampling paper asset contract",
        "classification": "FULLTEXT_PAPER_BACKED_RESAMPLING_METHODS_WARPX_MAPPING_RUNTIME_SEPARATE",
        "checks": checks,
        "passed": all(checks.values()),
        "paper_pages": pdf_pages(source_pdf) if source_pdf.exists() else None,
        "image_count": len(images),
        "chapter": str(args.chapter),
        "access_boundary": "PICADOR/hi-chi paper experiments remain separate from WarpX runtime evidence",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Muraviev 2021 particle-resampling paper asset contract",
        "",
        f"- Classification: `{result['classification']}`",
        f"- Paper pages: `{result['paper_pages']}`",
        f"- Extracted images: `{result['image_count']}`",
        f"- Passed: `{result['passed']}`",
        "",
        "| Check | Result |",
        "|---|---|",
    ]
    lines.extend(f"| `{name}` | `{value}` |" for name, value in checks.items())
    lines += [
        "",
        "The package supports a full-text explanation of agnostic down-sampling and its test results. The paper's PICADOR/hi-chi runs are not WarpX runtime evidence.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {sum(checks.values())}/{len(checks)} Muraviev 2021 asset checks")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
