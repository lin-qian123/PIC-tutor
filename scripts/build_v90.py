#!/usr/bin/env python
"""Build the PIC-tutor v0.90 Markdown, HTML, and optional PDF manuscript."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT_MD = DIST / "pic-tutor-v0.90.md"
OUTPUT_HTML = DIST / "pic-tutor-v0.90.html"
OUTPUT_PDF = DIST / "pic-tutor-v0.90.pdf"
HTML_STYLE = ROOT / "manuscript" / "assets" / "pic-tutor-html-style.html"
PROJECT_ROOT_TEXT = ROOT.as_posix()
WARPX_ROOT_TEXT = (ROOT.parent / "warpx").as_posix()

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
    # Source chapters resolve assets from manuscript/; the merged file lives in dist/.
    content = content.replace("../assets/figures/", "manuscript/assets/figures/")
    content = sanitize_public_paths(content)
    OUTPUT_MD.write_text(content, encoding="utf-8")


def sanitize_public_paths(content: str) -> str:
    """Keep local source commands readable without leaking machine-specific paths."""
    content = content.replace(f"({PROJECT_ROOT_TEXT}/", "(../")
    content = content.replace(f"{WARPX_ROOT_TEXT}/", "$WARPX_ROOT/")
    content = content.replace(f"{PROJECT_ROOT_TEXT}/", "PIC-tutor/")
    return content.replace(PROJECT_ROOT_TEXT, "PIC-tutor")


def build_html() -> None:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        print("[INFO] pandoc not found; skipped HTML build.")
        return

    cmd = [
        pandoc,
        str(OUTPUT_MD),
        "--from=markdown+tex_math_single_backslash+tex_math_dollars",
        "--standalone",
        "--toc",
        "--metadata",
            "title=PIC-tutor v0.90",
        "--mathjax",
        "--embed-resources",
        "--css",
        str(HTML_STYLE),
        "-o",
        str(OUTPUT_HTML),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)
    # Keep generated HTML deterministic and free of formatter-only trailing spaces.
    OUTPUT_HTML.write_text(
        "\n".join(line.rstrip() for line in OUTPUT_HTML.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )


def build_pdf() -> None:
    pandoc = shutil.which("pandoc")
    xelatex = shutil.which("xelatex")
    if pandoc is None or xelatex is None:
        print("[INFO] pandoc/xelatex not found; skipped PDF build.")
        return

    font = _find_cjk_font()
    cmd = [
        pandoc,
        str(OUTPUT_MD),
        "--from=markdown+tex_math_single_backslash+tex_math_dollars",
        "--standalone",
        "--toc",
        "--metadata",
            "title=PIC-tutor v0.90",
        "--pdf-engine=xelatex",
        "-V",
        "geometry:margin=2cm",
    ]
    if font:
        cmd.extend(["-V", f"CJKmainfont={font}"])
    cmd.extend(["-o", str(OUTPUT_PDF)])
    subprocess.run(cmd, check=True, cwd=ROOT)


def _find_cjk_font() -> str | None:
    fc_match = shutil.which("fc-match")
    if fc_match is None:
        return None
    for candidate in (
        "PingFang SC",
        "Hiragino Sans GB",
        "STSong",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
    ):
        completed = subprocess.run(
            [fc_match, "-f", "%{family}", candidate],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            continue
        family = completed.stdout.split(",", 1)[0].strip()
        if family and family.lower() == candidate.lower():
            return family
    return None


def main() -> None:
    build_markdown()
    build_html()
    build_pdf()
    print(f"[OK] Built {OUTPUT_MD}")
    if OUTPUT_HTML.exists():
        print(f"[OK] Built {OUTPUT_HTML}")
    if OUTPUT_PDF.exists():
        print(f"[OK] Built {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
