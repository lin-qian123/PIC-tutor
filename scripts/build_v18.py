#!/usr/bin/env python
"""Build the PIC-tutor v0.18 Markdown manuscript and optional HTML preview."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT_MD = DIST / "pic-tutor-v0.18.md"
OUTPUT_HTML = DIST / "pic-tutor-v0.18.html"
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
    DIST.mkdir(exist_ok=True)
    front_matter = """---
title: "PIC 程序详解：从物理模型到 WarpX 源码"
subtitle: "v0.18 boosted-frame Galilean 速度闭环版"
author: "PIC-tutor"
date: "2026-06-29"
lang: zh-CN
---
"""
    body = [front_matter]
    for part in PARTS:
        if not part.exists():
            raise FileNotFoundError(part)
        body.append(read_part(part))
    OUTPUT_MD.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")


def build_html() -> bool:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        return False
    subprocess.run(
        [
            pandoc,
            str(OUTPUT_MD),
            "--standalone",
            "--toc",
            "--mathjax",
            "--include-in-header",
            str(HTML_STYLE),
            "--metadata",
            "title=PIC 程序详解：从物理模型到 WarpX 源码",
            "-o",
            str(OUTPUT_HTML),
        ],
        check=True,
        cwd=ROOT,
    )
    return True


def main() -> None:
    build_markdown()
    html_built = build_html()
    print(f"wrote {OUTPUT_MD.relative_to(ROOT)}")
    if html_built:
        print(f"wrote {OUTPUT_HTML.relative_to(ROOT)}")
    else:
        print("skipped HTML preview: pandoc not found")


if __name__ == "__main__":
    main()
