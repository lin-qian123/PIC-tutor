#!/usr/bin/env python
"""Verify the v0.74 Markdown/HTML/PDF artifact contract after building."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader

from audit_public_release_paths import inspect


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CHAPTERS = sorted((ROOT / "manuscript" / "chapters").glob("*.md"))
MERGED_MARKDOWN = ROOT / "dist" / "pic-tutor-v0.74.md"
HTML = ROOT / "dist" / "pic-tutor-v0.74.html"
PDF = ROOT / "dist" / "pic-tutor-v0.74.pdf"
EXPECTED_PDF_PAGES = 329


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
        "vay_2014_review_closure": all(
            marker in source
            for marker in (
                "### 4.4.2 v0.74 文献闭环：Vay--Godfrey 2014 review",
                "### 6.6.7 v0.74 文献闭环：Vay--Godfrey 2014 review",
                "9 页 PDF、MinerU 原文、43 张抽取图",
                "`psatd.current_correction` 是离散连续性/Gauss-law projection",
            )
        ),
        "chapter_8_source_contract_heading": "## 8.14 本章正文与源码同步合同" in source
        and "### 8.14.1 本章正文与源码同步合同" not in source,
        "chapter_8_minimal_diagnostics_section": "### 8.14.1 reduced diagnostics 最小输入合同" in source,
        "chapter_5_geometry_order_gap_register": all(
            marker in source
            for marker in (
                "### 5.14.2 geometry/order coverage gap register",
                "negative-space contract",
                "RZ 默认 axis correction 下的 charge residual",
                "跨 geometry/shape 的正式收敛阶",
                "Vay 官方 wiring",
                "SOURCE_REGRESSION_WIRING_PARTIAL_RUNTIME_FAMILY",
                "RUNTIME_SINGLE_RANK_OFFICIAL_ANALYSIS_PASS_2D_3D",
                "RUNTIME_SINGLE_RANK_VAY_SHAPE_FAMILY_PASS_2D_3D",
                "RUNTIME_OFFICIAL_CMAKE_SCALE_2RANK_ANALYSIS_PASS_2D_3D",
                "RUNTIME_2RANK_VAY_SHAPE_FAMILY_PASS_2D_3D_CASE_LOCAL",
                "SOURCE_GUARD_AMR_RUNTIME_INTENTIONALLY_REJECTED",
            )
        ),
        "esirkepov_publication_boundary_contract": all(
            marker in source
            for marker in (
                "发表版缺口审计契约",
                "PREPRINT_FORMULA_SOURCE_RUNTIME_PUBLISHER_BOUNDARY_EXPLICIT",
                "publisher-PDF line-by-line compare 仍未完成",
            )
        ),
        "andriyash_fourier_bessel_literature_closure": all(
            marker in source
            for marker in (
                "6.8.6 v0.74 文献闭环：Andriyash 2016 Fourier-Bessel PSATD",
                "FULL_TEXT_MINERU_CHINESE_NOTE_VERIFIED_WARPX_EQUIVALENCE_BOUNDARY",
                "Andriyash 2016",
            )
        ),
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

    print("v0.74 artifact verification")
    for name, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    if not all(checks.values()):
        raise SystemExit("v0.74 artifact verification failed")
    print("[PASS] all v0.74 artifact checks")


if __name__ == "__main__":
    main()
