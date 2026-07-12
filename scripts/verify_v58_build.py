#!/usr/bin/env python
"""Verify the v0.58 Markdown/HTML/PDF artifact contract after building."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CHAPTER = ROOT / "manuscript" / "chapters" / "08-diagnostics-cases.md"
MERGED_MARKDOWN = ROOT / "dist" / "pic-tutor-v0.58.md"
HTML = ROOT / "dist" / "pic-tutor-v0.58.html"
PDF = ROOT / "dist" / "pic-tutor-v0.58.pdf"


def image_links(text: str) -> list[str]:
    return re.findall(r"!\[\]\(([^)]+figures/[^)]+)\)", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-log", type=Path)
    args = parser.parse_args()

    source = SOURCE_CHAPTER.read_text(encoding="utf-8")
    merged = MERGED_MARKDOWN.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8", errors="ignore")
    reader = PdfReader(str(PDF))
    pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)

    checks = {
        "pdf_pages": len(reader.pages) == 310,
        "source_image_links": len(image_links(source)) == 12,
        "merged_image_links": len(image_links(merged)) == 12,
        "image_links_relative": all(
            not link.startswith("/") for link in image_links(source) + image_links(merged)
        ),
        "html_embedded_images": html.count("data:image/png;base64,") >= 12,
        "figure_markers": all(f"图 8-{index}" in pdf_text for index in range(1, 13)),
        "appendix_marker": "附录 A：符号、时间层与源码变量" in pdf_text,
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

    print("v0.58 artifact verification")
    for name, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    if not all(checks.values()):
        raise SystemExit("v0.58 artifact verification failed")
    print("[PASS] all v0.58 artifact checks")


if __name__ == "__main__":
    main()
