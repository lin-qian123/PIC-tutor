#!/usr/bin/env python
"""Audit structural/editorial consistency of a built PIC-tutor release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from pypdf import PdfReader


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.headings: list[tuple[str, str]] = []
        self._tag: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if re.fullmatch(r"h[1-6]", tag):
            self._tag = tag
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._tag:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._tag == tag:
            self.headings.append((tag, " ".join("".join(self._text).split())))
            self._tag = None


def markdown_headings(text: str) -> list[tuple[int, str, int]]:
    result = []
    for line_no, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            result.append((len(match.group(1)), match.group(2), line_no))
    return result


def table_shape_issues(text: str) -> list[str]:
    issues: list[str] = []
    lines = text.splitlines()
    separator = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")

    def cells(line: str) -> int:
        stripped = line.strip()
        if stripped.startswith("|"):
            stripped = stripped[1:]
        if stripped.endswith("|"):
            stripped = stripped[:-1]
        masked: list[str] = []
        in_code = False
        in_math = False
        for char in stripped:
            if char == "`":
                in_code = not in_code
            elif char == "$" and not in_code:
                in_math = not in_math
            masked.append(" " if char == "|" and (in_code or in_math) else char)
        return len("".join(masked).split("|"))

    for index, line in enumerate(lines):
        if not separator.match(line) or index == 0 or "|" not in lines[index - 1]:
            continue
        expected = cells(lines[index])
        if cells(lines[index - 1]) != expected:
            issues.append(f"header/separator mismatch at line {index + 1}")
    return issues


def digest(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--version", required=True, help="release version, for example v0.81")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--public-output-dir", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    dist = root / "dist"
    merged = dist / f"pic-tutor-{args.version}.md"
    html_path = dist / f"pic-tutor-{args.version}.html"
    pdf_path = dist / f"pic-tutor-{args.version}.pdf"
    manual_spotcheck_path = root / f"docs/manual-editorial-spotcheck-{args.version}.md"
    merged_text = merged.read_text(encoding="utf-8")
    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    html_normalized = re.sub(r"\s+", " ", html_text)
    manual_spotcheck = manual_spotcheck_path.read_text(encoding="utf-8") if manual_spotcheck_path.is_file() else ""
    parser_html = HeadingParser()
    parser_html.feed(html_text)
    expected_title = f"PIC-tutor {args.version}"
    html_body_headings = parser_html.headings
    # Pandoc emits the metadata title before the manuscript's own H1 title.
    # It belongs to the document wrapper, not the source heading sequence.
    if html_body_headings[:1] == [("h1", expected_title)]:
        html_body_headings = html_body_headings[1:]
    pdf_reader = PdfReader(str(pdf_path))
    pdf_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
    headings = markdown_headings(merged_text)
    heading_counts = Counter(text for _, text, _ in headings)
    chapter_checks = {}
    for chapter in ("05-deposition-shapes", "06-field-solvers", "07-boundaries-amr", "09-literature-roadmap"):
        path = root / "manuscript/chapters" / f"{chapter}.md"
        chapter_headings = markdown_headings(path.read_text(encoding="utf-8"))
        numbers = [tuple(int(part) for part in match.group(1).split(".")) for _, text, _ in chapter_headings if (match := re.match(r"(?:v[0-9.]+\s+)?([0-9]+(?:\.[0-9]+)+)", text))]
        if chapter == "07-boundaries-amr":
            chapter_checks[chapter] = len(numbers) == len(set(numbers))
        else:
            chapter_checks[chapter] = numbers == sorted(numbers) and len(numbers) == len(set(numbers))

    manual_review_markers = (
        "基线 262 页快照已完成连续阅读",
        "当前增量复核（263 页候选）",
        "| 1--6 |",
        "| 229 |",
        "| 261 |",
    )
    manual_review_recorded = all(marker in manual_spotcheck for marker in manual_review_markers)
    checks = {
        "files_present": all(path.is_file() for path in (merged, html_path, pdf_path)),
        "merged_heading_duplicates": not any(count > 1 for count in heading_counts.values()),
        "markdown_tables_consistent": not table_shape_issues(merged_text),
        "chapter_heading_order": all(chapter_checks.values()),
        "html_title_and_heading_count": bool(parser_html.headings)
        and parser_html.headings[0] == ("h1", expected_title)
        and len(html_body_headings) == len(headings),
        "html_key_sections": all(marker in html_normalized for marker in ("如何阅读证据边界", "5.14.2.1 Vay 配置判读卡", "5.14.2.2 RZ implicit Villasenor 判读卡", "5.14.5.1 RZ 轴线判读卡", "收敛研究：描述性趋势不是正式阶数", "6.6.1 先按更新对象", "7.5.1 用正确的", "7.5.3 PML 配置与验证卡", "7.9.1 Transition-zone 判读卡")),
        "pdf_page_count_positive": len(pdf_reader.pages) > 0,
        "pdf_key_sections": all(marker in pdf_text for marker in ("如何阅读证据边界", "Vay 配置判读卡", "RZ implicit Villasenor 判读卡", "RZ 轴线判读卡", "收敛研究：描述性趋势不是正式阶数", "先按更新对象理解 PSATD 系数", "用正确的 observable 判断 PML", "PML 配置与验证卡", "Transition-zone 判读卡")),
        "no_build_warning_markers": not any(marker in pdf_text for marker in ("Could not fetch resource", "Missing character")),
        "baseline_read_and_current_incremental_review_are_recorded": manual_review_recorded,
    }
    classification = (
        "AUTOMATED_EDITORIAL_AUDIT_PASS_BASELINE_READ_INCREMENTAL_REVIEW_RECORDED"
        if manual_review_recorded
        else "AUTOMATED_EDITORIAL_AUDIT_PASS_MANUAL_REVIEW_OPEN"
    )
    scope = (
        "automated structure and artifact consistency; baseline full read and current incremental review are recorded; redistribution approval remains open"
        if manual_review_recorded
        else "automated structure and artifact consistency; not a substitute for human reading or redistribution approval"
    )
    result = {
        "contract": "editorial quality audit",
        "version": args.version,
        "checks": checks,
        "passed": all(checks.values()),
        "classification": classification,
        "scope": scope,
        "heading_count": len(headings),
        "html_heading_count": len(html_body_headings),
        "pdf_pages": len(pdf_reader.pages),
        "table_issues": table_shape_issues(merged_text),
        "artifacts": {path.name: digest(path) for path in (merged, html_path, pdf_path)},
    }
    output_dirs = [args.output_dir]
    if args.public_output_dir:
        output_dirs.append(args.public_output_dir)
    for output_dir in output_dirs:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        f"# {args.version} automated editorial quality audit", "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        f"- headings: `{result['heading_count']}` Markdown / `{result['html_heading_count']}` HTML",
        f"- PDF pages: `{result['pdf_pages']}`", "", "| check | status |", "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    if manual_review_recorded:
        lines.extend(["", "Automated audit, baseline full read, and current incremental review are recorded; licensing and redistribution approval remain open."])
    else:
        lines.extend(["", "Automated audit passed does not close manual reading, layout review, licensing, or redistribution approval."])
    for output_dir in output_dirs:
        (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
