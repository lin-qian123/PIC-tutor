#!/usr/bin/env python
"""Verify the v0.68 Markdown/HTML/PDF artifact contract after building."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader

from audit_public_release_paths import inspect


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CHAPTERS = sorted((ROOT / "manuscript" / "chapters").glob("*.md"))
MERGED_MARKDOWN = ROOT / "dist" / "pic-tutor-v0.68.md"
HTML = ROOT / "dist" / "pic-tutor-v0.68.html"
PDF = ROOT / "dist" / "pic-tutor-v0.68.pdf"
EXPECTED_PDF_PAGES = 323


def image_links(text: str) -> list[str]:
    return re.findall(r"!\[\]\(([^)]+figures/[^)]+)\)", text)


def chapter_subheading_numbers(path: Path, chapter: str) -> list[tuple[int, ...]]:
    pattern = re.compile(rf"^### ({re.escape(chapter)}\.\d+\.\d+)\b", re.MULTILINE)
    return [tuple(int(part) for part in match.split(".")) for match in pattern.findall(path.read_text(encoding="utf-8"))]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-log", type=Path)
    args = parser.parse_args()

    source = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_CHAPTERS)
    merged = MERGED_MARKDOWN.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8", errors="ignore")
    reader = PdfReader(str(PDF))
    pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    chapter_5_numbers = chapter_subheading_numbers(
        ROOT / "manuscript" / "chapters" / "05-deposition-shapes.md", "5"
    )
    chapter_6_numbers = chapter_subheading_numbers(
        ROOT / "manuscript" / "chapters" / "06-field-solvers.md", "6"
    )

    checks = {
        "pdf_pages": len(reader.pages) == EXPECTED_PDF_PAGES,
        "source_image_links": len(image_links(source)) == 16,
        "merged_image_links": len(image_links(merged)) == 16,
        "image_links_relative": all(
            not link.startswith("/") for link in image_links(source) + image_links(merged)
        ),
        "html_embedded_images": html.count("data:image/png;base64,") >= 16,
        "figure_markers": all(f"图 8-{index}" in pdf_text for index in range(1, 13)),
        "appendix_marker": "附录 A：符号、时间层与源码变量" in pdf_text,
        "chapter_5_subheading_order": chapter_5_numbers == sorted(chapter_5_numbers)
        and len(chapter_5_numbers) == len(set(chapter_5_numbers)),
        "chapter_6_subheading_order": chapter_6_numbers == sorted(chapter_6_numbers)
        and len(chapter_6_numbers) == len(set(chapter_6_numbers)),
        "chapter_9_exercises": all(
            marker in source
            for marker in (
                "## 9.9 练习与复核",
                "### 9.9.1 证据层分类练习",
                "### 9.9.2 合同复核练习",
                "### 9.9.3 acquisition 排序练习",
            )
        ),
        "chapter_8_source_contract_heading": "## 8.14 本章正文与源码同步合同" in source
        and "### 8.14.1 本章正文与源码同步合同" not in source,
        "public_path_hygiene_markdown": inspect(MERGED_MARKDOWN)["passed"],
        "public_path_hygiene_html": inspect(HTML)["passed"],
    }

    if args.build_log:
        log = args.build_log.read_text(encoding="utf-8", errors="ignore")
        checks["build_log_clean"] = not any(
            marker in log
            for marker in (
                "Could not fetch resource",
                "Could not convert TeX math",
                "Missing character",
            )
        )

    print("v0.68 artifact verification")
    for name, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    if not all(checks.values()):
        raise SystemExit("v0.68 artifact verification failed")
    print("[PASS] all v0.68 artifact checks")


if __name__ == "__main__":
    main()
