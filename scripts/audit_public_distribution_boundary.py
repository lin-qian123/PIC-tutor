#!/usr/bin/env python
"""Record whether tracked third-party assets block public redistribution sign-off."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from pypdf import PdfReader


RELEASE = "v0.110"
RELEASE_ARTIFACTS = (
    "dist/pic-tutor-v0.110.md",
    "dist/pic-tutor-v0.110.html",
    "dist/pic-tutor-v0.110.pdf",
)


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def release_artifacts(root: Path, manifest: dict[str, object]) -> tuple[dict[str, dict[str, object]], int]:
    manifest_entries = {
        entry["path"]: entry
        for entry in manifest.get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    artifacts = {}
    for relative in RELEASE_ARTIFACTS:
        path = root / relative
        entry = manifest_entries.get(relative, {})
        bytes_on_disk = path.stat().st_size
        digest = sha256(path)
        artifacts[relative] = {
            "bytes": bytes_on_disk,
            "sha256": digest,
            "manifest_match": (
                entry.get("bytes") == bytes_on_disk
                and entry.get("sha256") == digest
            ),
        }
    # The PDF is part of RELEASE_ARTIFACTS and is deliberately read from the
    # built artifact rather than copied from an editorial note.
    return artifacts, len(PdfReader(str(root / RELEASE_ARTIFACTS[-1])).pages)


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
    manifest_path = root / f"docs/{RELEASE}-release-manifest.json"
    manifest_text = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(manifest_text)
    artifacts, pdf_pages = release_artifacts(root, manifest)
    artifact_integrity_verified = all(item["manifest_match"] for item in artifacts.values())
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
        "release_candidate": {
            "version": RELEASE,
            "pdf_pages": pdf_pages,
            "artifacts": artifacts,
        },
        "release_manifest_excludes_references": "references" in manifest.get("excluded_roots", []),
        "artifact_integrity_verified": artifact_integrity_verified,
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
        "signoff_state": "BLOCKED_PENDING_MAINTAINER_RIGHTS_AND_REPOSITORY_DECISION",
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
        f"- current candidate: `PIC-tutor {RELEASE}` / `{pdf_pages}` PDF pages",
        f"- candidate artifacts match release manifest: `{artifact_integrity_verified}`",
        f"- release manifest excludes `references/`: `{result['release_manifest_excludes_references']}`",
        f"- root license files: `{', '.join(sorted(license_files)) or 'none'}`",
        f"- public redistribution sign-off: `{result['signoff_state']}`",
        "",
        "## Boundary",
        "",
        result["scope"],
        "",
        "## Required Maintainer Decision",
        "",
        result["required_maintainer_decision"],
        "",
        "The reader-facing PDF passed its editorial and layout checks, but that evidence does not grant "
        "redistribution rights for third-party source material.",
        "",
        "## Safe Decision Paths",
        "",
        "1. Confirm rights item by item, record the evidence, then add an appropriate project license and sign the release checklist.",
        "2. Remove unconfirmed third-party material from the public branch, then explicitly decide whether public Git history also needs remediation.",
        "3. Temporarily make the repository private while the rights inventory and project licensing decision remain open.",
        "",
        "This audit records the boundary only. It does not delete files, alter Git history, change repository visibility, or grant a license.",
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if artifact_integrity_verified else 1


if __name__ == "__main__":
    main()
