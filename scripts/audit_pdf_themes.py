#!/usr/bin/env python
"""Validate presentation-only PDF renders produced by build_pdf_themes.py."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "technical": (612.0, 792.0),
    "academic": (595.276, 841.89),
    "compact": (595.276, 841.89),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist/themes")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    return parser.parse_args()


def page_size_matches(page: object, expected: tuple[float, float]) -> bool:
    box = page.mediabox
    width = float(box.width)
    height = float(box.height)
    return abs(width - expected[0]) < 0.1 and abs(height - expected[1]) < 0.1


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    checks: dict[str, bool] = {}
    details: dict[str, object] = {}
    for theme, expected_size in THEMES.items():
        pdf = output_dir / f"pic-tutor-v0.110-{theme}.pdf"
        reader = PdfReader(str(pdf)) if pdf.is_file() else None
        pages = list(reader.pages) if reader else []
        text = [page.extract_text() or "" for page in pages]
        checks[f"{theme}_present"] = pdf.is_file()
        checks[f"{theme}_substantial"] = len(pages) >= 200
        checks[f"{theme}_text_extractable"] = bool(pages) and all(item.strip() for item in text)
        checks[f"{theme}_no_replacement_characters"] = not any("\ufffd" in item for item in text)
        checks[f"{theme}_expected_page_size"] = bool(pages) and all(
            page_size_matches(page, expected_size) for page in pages
        )
        details[theme] = {
            "path": pdf.relative_to(ROOT).as_posix() if pdf.exists() else str(pdf),
            "pages": len(pages),
            "expected_page_size_points": expected_size,
        }

    result = {
        "contract": "PIC-tutor themed PDF render",
        "checks": checks,
        "artifacts": details,
        "passed": all(checks.values()),
        "scope": "Checks render integrity and page geometry; it does not approve public redistribution rights.",
    }
    if args.output_json:
        args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.output_md:
        lines = ["# PDF theme audit", "", "| check | status |", "|---|:---:|"]
        lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
        args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
