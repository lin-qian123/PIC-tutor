#!/usr/bin/env python3
"""Build a filesystem-based inventory for the downloaded reference PDFs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("references")
OUT = ROOT / "00_index" / "current_inventory.md"


def main() -> int:
    pdfs = sorted(ROOT.glob("**/*.pdf"))
    by_category: dict[str, list[Path]] = {}
    for pdf in pdfs:
        rel = pdf.relative_to(ROOT)
        category = rel.parts[0]
        by_category.setdefault(category, []).append(rel)

    lines = [
        "# Current Reference Inventory",
        "",
        "This inventory is generated from the current files on disk.",
        "",
        f"- Total PDF files: {len(pdfs)}",
        "",
        "## Counts By Category",
        "",
    ]
    for category in sorted(by_category):
        lines.append(f"- `{category}`: {len(by_category[category])}")

    lines.extend(["", "## Files", ""])
    for category in sorted(by_category):
        lines.append(f"### `{category}`")
        lines.append("")
        for rel in by_category[category]:
            title = rel.name[:-4]
            lines.append(f"- [{title}](../{rel.as_posix()})")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} with {len(pdfs)} PDFs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
