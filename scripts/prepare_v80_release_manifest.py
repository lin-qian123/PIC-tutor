#!/usr/bin/env python
"""Create an auditable allowlist for the PIC-tutor v0.80 public release."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ROOTS = ("docs", "manuscript", "notes", "scripts")
ALLOWED_FILES = (".gitignore", "AGENTS.md", "README.md", "TODO.md")
RELEASE_DIST = ("dist/pic-tutor-v0.80.md", "dist/pic-tutor-v0.80.html", "dist/pic-tutor-v0.80.pdf")
MANIFEST_OUTPUTS = {"docs/v0.80-release-manifest.json", "docs/v0.80-release-manifest.md"}
EXCLUDED_ROOTS = ("runs", "references")
SKIP_NAMES = {".DS_Store", "Backtrace.0.0", "Backtrace.1.0", "bmmntr.txt"}
SKIP_SUFFIXES = (".pyc",)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def is_candidate(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in MANIFEST_OUTPUTS:
        return False
    if path.name in SKIP_NAMES or path.suffix in SKIP_SUFFIXES:
        return False
    if any(part == "__pycache__" for part in path.relative_to(ROOT).parts):
        return False
    if rel in ALLOWED_FILES or rel in RELEASE_DIST:
        return True
    return any(rel == root or rel.startswith(root + "/") for root in ALLOWED_ROOTS)


def iter_candidates() -> list[Path]:
    paths: list[Path] = []
    for rel in ALLOWED_FILES + RELEASE_DIST:
        path = ROOT / rel
        if path.exists():
            paths.append(path)
    for root_name in ALLOWED_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for directory, _, filenames in os.walk(root):
            for filename in filenames:
                path = Path(directory) / filename
                if is_candidate(path):
                    paths.append(path)
    return sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())


def digest(path: Path) -> tuple[int, str]:
    sha = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            sha.update(chunk)
    return size, sha.hexdigest()


def main() -> None:
    args = parse_args()
    entries = []
    for path in iter_candidates():
        size, sha256 = digest(path)
        entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": size, "sha256": sha256})
    total_bytes = sum(entry["bytes"] for entry in entries)
    result = {
        "release": "PIC-tutor v0.80",
        "root": str(ROOT),
        "allowlist_roots": list(ALLOWED_ROOTS),
        "allowlist_files": list(ALLOWED_FILES + RELEASE_DIST),
        "excluded_roots": list(EXCLUDED_ROOTS),
        "excluded_patterns": ["Backtrace.*", "bmmntr.txt", "__pycache__", "*.pyc", "dist/pic-tutor-v0.45 and older"],
        "entry_count": len(entries),
        "total_bytes": total_bytes,
        "entries": entries,
        "notes": [
            "This manifest is a release allowlist, not a git staging operation.",
            "The references/ tree is excluded pending per-item redistribution review.",
            "The runs/ tree is excluded because it contains local producer outputs and logs.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# PIC-tutor v0.80 release manifest",
        "",
        "This is an auditable allowlist for a future staging operation; it does not stage or commit files.",
        "",
        f"- entries: `{len(entries)}`",
        f"- total bytes: `{total_bytes}`",
        f"- allowed roots: `{', '.join(ALLOWED_ROOTS)}`",
        f"- excluded roots: `{', '.join(EXCLUDED_ROOTS)}`",
        "- excluded generated material: `Backtrace.*`, `bmmntr.txt`, `__pycache__`, `*.pyc`, historical `dist/` artifacts",
        "",
        "## Release files",
        "",
        "- `dist/pic-tutor-v0.80.md`",
        "- `dist/pic-tutor-v0.80.html`",
        "- `dist/pic-tutor-v0.80.pdf`",
        "- `manuscript/VERSION-v0.79.md` historical freeze",
        "",
        "## Hashes",
        "",
        "| path | bytes | sha256 |",
        "|---|---:|---|",
    ]
    for entry in entries:
        if entry["path"].startswith("dist/") or entry["path"] in {"README.md", "TODO.md", "manuscript/VERSION.md", "manuscript/VERSION-v0.69.md"}:
            lines.append(f"| `{entry['path']}` | `{entry['bytes']}` | `{entry['sha256']}` |")
    lines.append("")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("release", "entry_count", "total_bytes", "excluded_roots")}, indent=2))


if __name__ == "__main__":
    main()
