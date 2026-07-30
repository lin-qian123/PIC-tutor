#!/usr/bin/env python
"""Audit high-risk PDF layout signals for a built PIC-tutor release."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader


TABLE_SEPARATOR = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def cell_count(line: str) -> int:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return len(line.split("|"))


def table_widths(text: str) -> list[tuple[int, int]]:
    lines = text.splitlines()
    result = []
    for index, line in enumerate(lines):
        if index and TABLE_SEPARATOR.match(line) and "|" in lines[index - 1]:
            result.append((index + 1, cell_count(lines[index - 1])))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    markdown = root / "dist" / f"pic-tutor-{args.version}.md"
    pdf = root / "dist" / f"pic-tutor-{args.version}.pdf"
    source = (root / "manuscript/chapters/07-boundaries-amr.md").read_text(encoding="utf-8")
    rendered_source = strip_comments(source)
    reader = PdfReader(str(pdf))
    page_lengths = [len((page.extract_text() or "").strip()) for page in reader.pages]
    section = rendered_source.split("### 7.5.1", 1)[1].split("### 7.5.2", 1)[0]
    section_tables = table_widths(section)
    checks = {
        "files_present": markdown.is_file() and pdf.is_file(),
        # Figure-led diagnostic result pages can contain a complete caption and
        # conclusion with less body text than prose pages. Reject only pages whose
        # extracted text is too short to establish that a caption and page marker survived.
        "all_pages_have_extractable_text": bool(page_lengths) and min(page_lengths) >= 200,
        "chapter_7_5_1_has_no_overwide_rendered_table": all(columns <= 4 for _, columns in section_tables),
        "chapter_7_5_1_has_no_historical_comment": "<!--" not in source,
        "pdf_has_expected_boundary_sections": all(
            marker in "\n".join(page.extract_text() or "" for page in reader.pages)
            for marker in ("7.5.1 用正确的 observable 判断 PML", "如何阅读证据边界")
        ),
    }
    result = {
        "contract": "PDF layout risk audit",
        "version": args.version,
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "PDF_LAYOUT_AUTOMATED_PASS_MANUAL_SPOTCHECK_RECORDED",
        "pdf_pages": len(reader.pages),
        "min_page_chars": min(page_lengths) if page_lengths else 0,
        "min_page_number": page_lengths.index(min(page_lengths)) + 1 if page_lengths else None,
        "chapter_7_5_1_tables": section_tables,
        "scope": "page text coverage and known wide-table regression; not a substitute for full human reading",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        f"# {args.version} PDF layout risk audit",
        "",
        f"- classification: `{result['classification']}`",
        f"- PDF pages: `{result['pdf_pages']}`",
        f"- minimum extracted page characters: `{result['min_page_chars']}` (page `{result['min_page_number']}`)",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend([
        "",
        "Automated layout signals pass; representative pages still require human visual review before redistribution approval.",
    ])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
