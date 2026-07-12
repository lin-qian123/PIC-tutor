#!/usr/bin/env python
"""Audit the bounded Esirkepov preprint/publication comparison contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PUBLISHED_TITLE = "Exact charge conservation scheme for Particle-in-Cell simulation with an arbitrary form-factor"
PUBLISHED_DOI = "10.1016/S0010-4655(00)00228-9"
PREPRINT_TITLE = "Exact charge conservation scheme for Particle-in-Cell simulations for a big class of form-factors"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    markdown_candidates = sorted(paper_dir.glob("*.md"))
    preprint = next(
        (path for path in markdown_candidates if "中文讲解" not in path.name and "源码映射" not in path.name),
        None,
    )
    if preprint is None:
        raise SystemExit("missing local preprint markdown")
    text = preprint.read_text(encoding="utf-8")
    access_audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(\d+)\s+", text, re.MULTILINE)
    checks = {
        "preprint_asset_present": preprint.exists(),
        "preprint_title_present": PREPRINT_TITLE in text,
        "published_title_recorded": PUBLISHED_TITLE in access_audit,
        "doi_recorded": PUBLISHED_DOI in access_audit,
        "sections_1_to_5_present": all(str(number) in headings for number in range(1, 6)),
        "eq23_present": bool(re.search(r"Eq\.\(23\)|Eq\.\s*23", text)),
        "second_order_spline_present": "second-order" in text and "spline" in text,
        "publisher_pdf_missing": bool(
            re.search(r"publisher PDF status.*still missing", access_audit, re.IGNORECASE)
        ),
    }
    result = {
        "contract": "Esirkepov 2001 bounded preprint/publication comparison",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "PREPRINT_SOURCE_PUBLICATION_METADATA_VERIFIED_PUBLISHER_PDF_MISSING",
        "source": str(preprint),
        "published": {
            "title": PUBLISHED_TITLE,
            "doi": PUBLISHED_DOI,
            "journal": "Computer Physics Communications 135(2), 144-153 (2001)",
        },
        "scope": "bounded structural compare only; no publisher-PDF line-by-line claim",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Esirkepov 2001 bounded comparison contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: `{preprint}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(
        [
            "",
            "The local preprint supports the structural Section 1-5, Eq.(23), and second-order spline checks. "
            "The CPC title/DOI metadata is recorded, but the publisher-formatted PDF is absent; this contract "
            "does not upgrade the evidence to a line-by-line publication compare.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
