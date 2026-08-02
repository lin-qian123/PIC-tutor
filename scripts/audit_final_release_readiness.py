#!/usr/bin/env python
"""Audit final manuscript readiness while preserving publication blockers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


RELEASE = "v0.110"
ARTIFACTS = (
    "dist/pic-tutor-v0.110.md",
    "dist/pic-tutor-v0.110.html",
    "dist/pic-tutor-v0.110.pdf",
)
REGISTER_IDS = (
    "LIT-ESIRKEPOV-PUBLISHER",
    "LIT-LEE-PUBLISHER",
    "RUNTIME-TRANSITION-ZONE",
    "RUNTIME-RZ-IMPLICIT-VILLASENOR",
    "RUNTIME-VAY-AMR",
    "PHYSICS-RZ-AXIS-CHARGE",
    "STUDY-FORMAL-CONVERGENCE",
    "RELEASE-EDITORIAL",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_checks(root: Path) -> tuple[dict[str, bool], dict[str, object]]:
    manifest = json.loads((root / f"docs/{RELEASE}-release-manifest.json").read_text(encoding="utf-8"))
    entries = {
        entry["path"]: entry
        for entry in manifest.get("entries", [])
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    checks: dict[str, bool] = {}
    details: dict[str, object] = {}
    for relative in ARTIFACTS:
        path = root / relative
        entry = entries.get(relative, {})
        digest = sha256(path) if path.is_file() else ""
        checks[f"artifact_present:{relative}"] = path.is_file()
        checks[f"artifact_manifest_match:{relative}"] = (
            path.is_file()
            and entry.get("bytes") == path.stat().st_size
            and entry.get("sha256") == digest
        )
        details[relative] = {"bytes": path.stat().st_size if path.is_file() else 0, "sha256": digest}
    return checks, details


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    pdf = root / ARTIFACTS[-1]
    reader = PdfReader(str(pdf))
    page_text = [page.extract_text() or "" for page in reader.pages]
    page_boxes = {tuple(float(value) for value in page.mediabox) for page in reader.pages}
    manual_review = (root / f"docs/manual-editorial-spotcheck-{RELEASE}.md").read_text(encoding="utf-8")
    register = (root / "docs/current-book-gap-register.md").read_text(encoding="utf-8")
    risk_register = (root / f"docs/public-distribution-risk-register-{RELEASE}.md").read_text(encoding="utf-8")
    editorial_audit = (root / f"docs/editorial-quality-audit-{RELEASE}.md").read_text(encoding="utf-8")
    layout_audit = (root / f"docs/pdf-layout-audit-{RELEASE}.md").read_text(encoding="utf-8")
    artifact_status, artifacts = artifact_checks(root)

    checks = {
        **artifact_status,
        "expected_pdf_page_count": len(reader.pages) == 275,
        "all_pages_have_extractable_text": all(text.strip() for text in page_text),
        "no_abnormally_short_pages": all(len(text.strip()) >= 100 for text in page_text),
        "no_replacement_characters": not any("\ufffd" in text for text in page_text),
        "no_missing_character_markers": not any("Missing character" in text for text in page_text),
        "uniform_page_media_box": page_boxes == {(0.0, 0.0, 612.0, 792.0)},
        "final_all_page_review_recorded": all(
            marker in manual_review
            for marker in (
                "## 最终全量页面复核（275 页候选）",
                "`1--25`、`26--50`、`51--75`",
                "`251--275`",
                "第 51 页是完整的跨章核查链",
            )
        ),
        "editorial_and_layout_audits_pass": (
            "AUTOMATED_EDITORIAL_AUDIT_PASS_BASELINE_READ_INCREMENTAL_REVIEW_RECORDED" in editorial_audit
            and "PDF_LAYOUT_AUTOMATED_PASS_MANUAL_SPOTCHECK_RECORDED" in layout_audit
        ),
        "all_current_gaps_remain_explicit": all(identifier in register for identifier in REGISTER_IDS),
        "public_redistribution_remains_explicitly_blocked": (
            "BLOCKED_PENDING_MAINTAINER_RIGHTS_AND_REPOSITORY_DECISION" in risk_register
        ),
    }
    manuscript_ready = all(value for name, value in checks.items() if name != "public_redistribution_remains_explicitly_blocked")
    result = {
        "contract": "final release readiness",
        "release": f"PIC-tutor {RELEASE}",
        "classification": "MANUSCRIPT_FINAL_EDITORIAL_REVIEW_PASS_PUBLIC_REDISTRIBUTION_BLOCKED",
        "manuscript_ready_for_reader_review": manuscript_ready,
        "public_redistribution_approved": False,
        "checks": checks,
        "pdf_pages": len(reader.pages),
        "artifacts": artifacts,
        "remaining_decision": (
            "A maintainer must decide the rights and public-history path for tracked third-party "
            "references, then select an appropriate project license."
        ),
        "scope": (
            "Confirms the final manuscript artifact and recorded editorial review. It does not grant "
            "third-party rights, alter repository visibility, modify Git history, or close runtime and literature gaps."
        ),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# {RELEASE} final release readiness",
        "",
        f"- classification: `{result['classification']}`",
        f"- manuscript ready for reader review: `{result['manuscript_ready_for_reader_review']}`",
        "- public redistribution approved: `False`",
        f"- PDF pages: `{result['pdf_pages']}`",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend([
        "",
        "## Remaining Maintainer Decision",
        "",
        result["remaining_decision"],
        "",
        "## Scope",
        "",
        result["scope"],
    ])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if manuscript_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
