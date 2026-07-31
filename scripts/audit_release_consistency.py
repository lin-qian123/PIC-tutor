#!/usr/bin/env python
"""Audit that current release metadata points to the same published version."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CURRENT_VERSION = "v0.110"


def check(root: Path, relative: str, expected: str) -> dict[str, object]:
    path = root / relative
    actual = path.read_text(encoding="utf-8") if path.exists() else ""
    passed = expected in actual
    return {"path": relative, "expected": expected, "passed": passed}


def build_report(root: Path) -> dict[str, object]:
    checks = [
        check(root, "README.md", f"当前可审阅版本为 `{CURRENT_VERSION}`"),
        check(root, "README.md", "## 阅读书稿"),
        check(root, "README.md", "## 准确性约定"),
        check(root, "README.md", "## 维护记录"),
        check(root, "manuscript/README.md", "读者的核查顺序"),
        check(root, "manuscript/VERSION.md", "# PIC-tutor"),
        check(root, "manuscript/VERSION.md", "建议的阅读方式"),
        check(root, "docs/public-repo-release-audit.md", f"dist/pic-tutor-{CURRENT_VERSION}.pdf"),
        check(root, "docs/public-repo-release-audit.md", "## 当前可审计候选"),
        check(root, "docs/public-repo-release-audit.md", "PDF 为 `274` 页"),
        check(root, "docs/public-repo-release-audit.md", "## 历史快照"),
        check(root, "docs/public-distribution-risk-register-v0.110.md", "PIC-tutor v0.110` / `274` PDF pages"),
        check(root, "docs/public-distribution-risk-register-v0.110.md", "BLOCKED_PENDING_MAINTAINER_RIGHTS_AND_REPOSITORY_DECISION"),
        check(root, "docs/v0.110-release-manifest.json", f'"release": "PIC-tutor {CURRENT_VERSION}"'),
        check(root, "scripts/build_v110.py", f"pic-tutor-{CURRENT_VERSION}"),
        check(root, "scripts/verify_v110_build.py", f"v0.110 artifact verification"),
    ]
    forbidden_current_refs = []
    for relative in ("README.md", "manuscript/README.md", "manuscript/VERSION.md"):
        text = (root / relative).read_text(encoding="utf-8")
        if "当前收束版本是 `v0.67`" in text or "scripts/verify_v67_build.py` 覆盖" in text:
            forbidden_current_refs.append(relative)
    readme = (root / "README.md").read_text(encoding="utf-8")
    for marker in ("当前成书版本为 `v0.76`", "指向同一 v0.76", "当前成书版本为 `v0.77`", "当前成书版本为 `v0.78`", "当前成书版本为 `v0.79`"):
        if marker in readme:
            forbidden_current_refs.append(f"README.md:{marker}")
    return {
        "contract": "current release metadata consistency",
        "current_version": CURRENT_VERSION,
        "checks": checks,
        "forbidden_current_reference_files": forbidden_current_refs,
        "passed": all(item["passed"] for item in checks) and not forbidden_current_refs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = build_report(args.root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
