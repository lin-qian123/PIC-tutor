#!/usr/bin/env python
"""Render the canonical PIC-tutor Markdown manuscript with named PDF themes."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dist/pic-tutor-v0.110.md"
THEME_DIR = ROOT / "manuscript/assets/themes"
THEMES = ("technical", "academic", "compact")
FONT_CANDIDATES = (
    "PingFang SC",
    "Hiragino Sans GB",
    "STSong",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", choices=THEMES, action="append", help="Theme to render; repeat to select several")
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist/themes")
    parser.add_argument("--manifest", type=Path, help="Write render metadata here; defaults to <output-dir>/manifest.json")
    return parser.parse_args()


def find_cjk_font() -> str | None:
    fc_match = shutil.which("fc-match")
    if fc_match is None:
        return None
    for candidate in FONT_CANDIDATES:
        completed = subprocess.run(
            [fc_match, "-f", "%{family}", candidate],
            check=False,
            capture_output=True,
            text=True,
        )
        family = completed.stdout.split(",", 1)[0].strip()
        if completed.returncode == 0 and family and family.lower() == candidate.lower():
            return family
    return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render(source: Path, output_dir: Path, theme: str, font: str | None) -> Path:
    pandoc = shutil.which("pandoc")
    xelatex = shutil.which("xelatex")
    if pandoc is None or xelatex is None:
        raise RuntimeError("pandoc and xelatex are required to render themed PDFs")

    output = output_dir / f"pic-tutor-v0.110-{theme}.pdf"
    command = [
        pandoc,
        str(source),
        "--from=markdown+tex_math_single_backslash+tex_math_dollars",
        "--standalone",
        "--toc",
        "--metadata",
        f"title=PIC-tutor v0.110 ({theme} theme)",
        "--pdf-engine=xelatex",
        "--include-in-header",
        str(THEME_DIR / f"{theme}.tex"),
        "-o",
        str(output),
    ]
    if font:
        command.extend(["-V", f"CJKmainfont={font}"])
    subprocess.run(command, check=True, cwd=ROOT)
    return output


def main() -> None:
    args = parse_args()
    source = args.source.resolve()
    output_dir = args.output_dir.resolve()
    manifest_path = (args.manifest or output_dir / "manifest.json").resolve()
    themes = tuple(args.theme or THEMES)
    if not source.is_file():
        raise FileNotFoundError(f"canonical merged manuscript is missing: {source}")

    output_dir.mkdir(parents=True, exist_ok=True)
    font = find_cjk_font()
    artifacts = []
    for theme in themes:
        output = render(source, output_dir, theme, font)
        artifacts.append(
            {
                "theme": theme,
                "path": output.relative_to(ROOT).as_posix(),
                "bytes": output.stat().st_size,
                "sha256": sha256(output),
            }
        )

    manifest = {
        "contract": "PIC-tutor themed PDF renders",
        "source_edition": "v0.110",
        "source": source.relative_to(ROOT).as_posix(),
        "source_sha256": sha256(source),
        "engine": "pandoc + xelatex",
        "cjk_font": font,
        "artifacts": artifacts,
        "scope": "Theme renders share one Markdown source and change presentation only.",
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
