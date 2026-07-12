#!/usr/bin/env python
"""Check release artifacts for machine-local paths and absolute local links."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FORBIDDEN_PATHS = ("/Volumes/", "/Users/", "file://")


def inspect(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    forbidden = {needle: text.count(needle) for needle in FORBIDDEN_PATHS if needle in text}
    absolute_links = re.findall(r"(?:href|src)=['\"]/(?!/)[^'\"]+", text)
    return {
        "path": str(path),
        "forbidden_path_counts": forbidden,
        "absolute_local_link_count": len(absolute_links),
        "passed": not forbidden and not absolute_links,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    reports = [inspect(path.resolve()) for path in args.paths]
    result = {
        "contract": "public release path hygiene",
        "reports": reports,
        "passed": all(report["passed"] for report in reports),
        "scope": "release Markdown/HTML only; source manuscript paths remain local-source concerns",
    }
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
