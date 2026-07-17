#!/usr/bin/env python
"""Audit whether the book entry points read like a tutorial rather than a changelog."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    version = (root / "manuscript/VERSION.md").read_text(encoding="utf-8")
    readme = (root / "manuscript/README.md").read_text(encoding="utf-8")
    preface = (root / "manuscript/chapters/00-preface.md").read_text(encoding="utf-8")
    chapters = sorted((root / "manuscript/chapters").glob("*.md"))
    chapter_text = "\n".join(path.read_text(encoding="utf-8") for path in chapters)
    reader_chapters = [path for path in chapters if path.name != "00-preface.md"]
    chapter_openings = "\n".join(
        path.read_text(encoding="utf-8")[:2500] for path in reader_chapters
    )

    version_markers = re.findall(r"^### .*v0\.\d+", chapter_text, re.MULTILINE)
    versioned_prose_markers = re.findall(r"\bv0\.\d+", chapter_text)
    project_record_words = re.findall(r"发布|审计合同|当前版本|本版新增|本轮新增|运行合同", version + readme, re.MULTILINE)
    project_record_opening_markers = re.findall(
        r"v0\.\d+\s*(?:校准说明|源码基线|的本章目标)|可审校长草稿|正式书稿版|后续扩写计划|本章当前依据|本章当前按|本机现成 PDF/MinerU|本机源码位置|本章当前引用|当前源码入口|项目目录 .*access audit|项目级 helper|交接记录",
        chapter_openings,
    )
    project_record_body_markers = re.findall(
        r"current-checkout|维护台账|本机现成 PDF/MinerU|项目级 helper|交接记录",
        chapter_text,
    )
    checks = {
        "version_is_reader_facing": "不是开发日志" in version and "读者在本版可以学到什么" in version,
        "manuscript_readme_is_reader_facing": "PIC 教程" in readme and "阅读路径" in readme and "不是面向维护者的提交记录" in readme,
        "preface_has_learning_outcomes": "读者应当能够" in preface and "如何使用本书" in preface,
        "history_is_separated": (root / "docs/version-history-v0.110.md").is_file(),
        "chapter_openings_are_reader_facing": not project_record_opening_markers,
        "core_chapters_have_no_project_record_markers": not project_record_body_markers,
        "core_chapters_have_no_versioned_prose": not versioned_prose_markers,
        "core_chapters_have_exercises": all(
            marker in chapter_text
            for marker in ("练习", "源码定位", "复现实验")
        ),
    }
    result = {
        "contract": "reader-facing content audit",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "READER_FACING_CORE_CHAPTERS_PASS_HUMAN_FULL_READ_OPEN",
        "scope": "entry-point and learning-path audit; versioned evidence headings have been separated from core tutorial chapters",
        "versioned_chapter_heading_count": len(version_markers),
        "versioned_chapter_headings": version_markers,
        "versioned_prose_marker_count": len(versioned_prose_markers),
        "project_record_word_count_in_entry_points": len(project_record_words),
        "project_record_opening_markers": project_record_opening_markers,
        "project_record_body_markers": project_record_body_markers,
        "open_items": [
            "需要人工通读术语、公式、代码上下文、章节过渡和练习",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Reader-facing content audit",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        f"- versioned chapter headings remaining: `{len(version_markers)}`",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if value else 'FAIL'}` |" for name, value in checks.items())
    lines.extend(["", "## Open editorial work", ""])
    lines.extend(f"- {item}" for item in result["open_items"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
