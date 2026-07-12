#!/usr/bin/env python
"""Build the PIC-tutor v0.39 Markdown manuscript and optional HTML preview."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT_MD = DIST / "pic-tutor-v0.39.md"
OUTPUT_HTML = DIST / "pic-tutor-v0.39.html"
HTML_STYLE = ROOT / "manuscript" / "assets" / "pic-tutor-html-style.html"

PARTS = [
    ROOT / "manuscript" / "VERSION.md",
    ROOT / "manuscript" / "chapters" / "00-preface.md",
    ROOT / "manuscript" / "chapters" / "01-kinetic-models.md",
    ROOT / "manuscript" / "chapters" / "02-pic-loop.md",
    ROOT / "manuscript" / "chapters" / "03-warpx-evolve.md",
    ROOT / "manuscript" / "chapters" / "03a-warpx-initialization.md",
    ROOT / "manuscript" / "chapters" / "04-particle-pushers.md",
    ROOT / "manuscript" / "chapters" / "05-deposition-shapes.md",
    ROOT / "manuscript" / "chapters" / "06-field-solvers.md",
    ROOT / "manuscript" / "chapters" / "07-boundaries-amr.md",
    ROOT / "manuscript" / "chapters" / "08-diagnostics-cases.md",
    ROOT / "manuscript" / "chapters" / "09-literature-roadmap.md",
    ROOT / "manuscript" / "appendices" / "A-symbols.md",
]


def read_part(path: Path) -> str:
    text = path.read_text(encoding="utf-8").rstrip()
    rel = path.relative_to(ROOT)
    return f"\n\n<!-- source: {rel} -->\n\n{text}\n"


def build_markdown() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    content = "".join(read_part(path) for path in PARTS).lstrip()
    OUTPUT_MD.write_text(content, encoding="utf-8")


def build_html() -> None:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        print("[INFO] pandoc not found; skipped HTML build.")
        return

    cmd = [
        pandoc,
        str(OUTPUT_MD),
        "--standalone",
        "--toc",
        "--number-sections",
        "--metadata",
        "title=PIC-tutor v0.39",
        "--css",
        str(HTML_STYLE),
        "-o",
        str(OUTPUT_HTML),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    build_markdown()
    build_html()
    print(f"[OK] Built {OUTPUT_MD}")
    if OUTPUT_HTML.exists():
        print(f"[OK] Built {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
