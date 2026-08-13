#!/usr/bin/env python
"""Build the PIC-tutor native LaTeX book (Phase 1 sample).

Copies manuscript/latex + manuscript/assets/figures into a clean build tree
under build/latex (disposable intermediates; outside tracked sources), runs
``latexmk -xelatex`` for the requested theme, and publishes the PDF to
``dist/latex/pic-tutor-<edition>-<theme>.pdf`` together with a manifest.json.

Usage:
  python scripts/build_latex_book.py [--theme academic|technical|compact]
                                     [--edition latex-sample]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "manuscript" / "latex"
FIGURES = ROOT / "manuscript" / "assets" / "figures"
BUILD = ROOT / "build" / "latex"
DIST = ROOT / "dist" / "latex"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd: list[str], cwd: Path) -> None:
    print("+", " ".join(cmd))
    env = dict(__import__("os").environ)
    # Fixed timestamp so clean rebuilds are byte-identical (Phase 4 gate:
    # reproducible twice from clean output directories).
    env["SOURCE_DATE_EPOCH"] = "0"
    subprocess.run(cmd, cwd=cwd, check=True, env=env)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", default="academic", choices=["academic", "technical", "compact"])
    ap.add_argument("--edition", default="v0.120")
    args = ap.parse_args()

    if not SRC.exists():
        raise SystemExit(f"missing source tree: {SRC}")

    # Clean build tree with a disposable copy of the manuscript/latex sources.
    shutil.rmtree(BUILD, ignore_errors=True)
    (BUILD / "src").mkdir(parents=True)
    shutil.copytree(SRC, BUILD / "src", dirs_exist_ok=True)
    # Figures live under manuscript/assets/figures; graphicspath in
    # preamble/floats-tables.tex is ../../assets/figures/ relative to src.
    shutil.copytree(FIGURES, BUILD / "assets" / "figures", dirs_exist_ok=True)

    # Theme wrapper in the copied tree (cwd = src, so relative inputs resolve).
    job = f"main-{args.theme}"
    (BUILD / "src" / f"{job}.tex").write_text(
        "\\providecommand{\\TheTheme}{" + args.theme + "}\n"
        "\\input{main.tex}\n",
        encoding="utf-8",
    )

    run(["latexmk", "-xelatex", "-interaction=nonstopmode", job], cwd=BUILD / "src")
    pdf = BUILD / "src" / f"{job}.pdf"
    if not pdf.exists():
        raise SystemExit(f"build failed: {pdf} missing")

    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / f"pic-tutor-{args.edition}-{args.theme}.pdf"
    shutil.copy2(pdf, out)

    git = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT)
    xelatex = subprocess.run(["xelatex", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    font_cjk = "Songti SC (CJK main); PingFang SC (CJK sans); Menlo (Latin mono)"
    entry = {
        "edition": args.edition,
        "theme": args.theme,
        "pdf": out.relative_to(ROOT).as_posix(),
        "pdf_sha256": sha256(out),
        "source_commit": git.stdout.strip() if git.returncode == 0 else "unknown",
        "engine": xelatex,
        "fonts": font_cjk,
        "reproducible": "SOURCE_DATE_EPOCH=0; byte-identical across clean rebuilds",
        "baseline": {"tag": "v1.0", "edition": "v0.110"},
    }
    # Cumulative manifest: keep entries of other themes.
    manifest_path = DIST / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:  # pragma: no cover
            manifest = {}
    manifest.setdefault("edition", args.edition)
    manifest.setdefault("source_commit", entry["source_commit"])
    manifest.setdefault("engine", entry["engine"])
    manifest.setdefault("fonts", entry["fonts"])
    manifest.setdefault("reproducible", entry["reproducible"])
    manifest.setdefault("baseline", entry["baseline"])
    manifest.setdefault("note", (
        "Provisional edition identifier; final numbering and any public release "
        "pending maintainer approval of the Phase 1 decision point and "
        "redistribution rights. See docs/latex-migration-plan.md."
    ))
    manifest["themes"] = manifest.get("themes", {})
    manifest["themes"][args.theme] = {"pdf": entry["pdf"], "pdf_sha256": entry["pdf_sha256"]}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"published {out} ({pdf.stat().st_size} bytes)")
    print(f"manifest {DIST / 'manifest.json'}")


if __name__ == "__main__":
    main()
