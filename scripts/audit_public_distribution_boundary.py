#!/usr/bin/env python
"""Record whether tracked third-party assets block public redistribution sign-off."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def tracked_files(root: Path, prefix: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", prefix],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [path for path in result.stdout.decode("utf-8").split("\0") if path]


def size_bytes(root: Path, paths: list[str]) -> int:
    return sum((root / path).stat().st_size for path in paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    references = tracked_files(root, "references")
    pdf_count = sum(path.lower().endswith(".pdf") for path in references)
    image_count = sum(path.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")) for path in references)
    manifest = (root / "docs/v0.110-release-manifest.json").read_text(encoding="utf-8")
    license_files = [path.name for path in root.glob("LICENSE*")] + [path.name for path in root.glob("COPYING*")]
    result = {
        "contract": "public distribution boundary",
        "classification": "PUBLIC_REPOSITORY_THIRD_PARTY_ASSETS_TRACKED_REMEDIATION_REQUIRED",
        "tracked_references": {
            "file_count": len(references),
            "bytes": size_bytes(root, references),
            "pdf_count": pdf_count,
            "image_count": image_count,
        },
        "release_manifest_excludes_references": '"references"' in manifest,
        "root_license_files": sorted(license_files),
        "remediation_open": bool(references) or not license_files,
        "scope": (
            "Local Git inventory only. A release manifest does not remove files already tracked "
            "by Git or control distribution through public repository history."
        ),
        "required_maintainer_decision": (
            "Confirm redistribution rights per tracked third-party item, or remove the items from "
            "the public branch and decide whether public history must be rewritten."
        ),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Public distribution boundary",
        "",
        f"- classification: `{result['classification']}`",
        f"- tracked `references/` files: `{len(references)}`",
        f"- tracked reference bytes: `{result['tracked_references']['bytes']}`",
        f"- tracked reference PDFs: `{pdf_count}`",
        f"- tracked reference images: `{image_count}`",
        f"- release manifest excludes `references/`: `{result['release_manifest_excludes_references']}`",
        f"- root license files: `{', '.join(sorted(license_files)) or 'none'}`",
        "",
        "## Boundary",
        "",
        result["scope"],
        "",
        "## Required Maintainer Decision",
        "",
        result["required_maintainer_decision"],
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    main()
