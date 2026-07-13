#!/usr/bin/env python
"""Audit the Esirkepov publisher-indexed-abstract compare artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    note = (root / "notes/code-reading/particles/63-esirkepov-publisher-abstract-compare.md").read_text(
        encoding="utf-8"
    )
    chapter = (root / "manuscript/chapters/05-deposition-shapes.md").read_text(encoding="utf-8")
    access = next((root / "references").glob("04_particle_pushers_deposition_shapes/*Esirkepov*/access-audit.md"))
    access_text = access.read_text(encoding="utf-8")
    checks = {
        "note_exists_and_has_boundary": all(
            marker in note
            for marker in (
                "indexed-abstract compare",
                "publisher-formatted PDF",
                "publisher-PDF line-by-line compare 仍未完成",
            )
        ),
        "note_has_publisher_claims": all(
            marker in note
            for marker in (
                "Cartesian geometry",
                "arbitrary quasi-particle form-factor",
                "straight-line",
                "2D and 3D computation scheme",
            )
        ),
        "note_has_preprint_claims": all(
            marker in note
            for marker in (
                "density decomposition",
                "parabolic spline form-factor",
                "n-dimensional form-factor",
            )
        ),
        "note_has_sources": all(
            marker in note
            for marker in (
                "sciencedirect.com/science/article/pii/S0010465500002289",
                "arxiv.org/abs/physics/9901047",
            )
        ),
        "chapter_has_updated_boundary": all(
            marker in chapter
            for marker in (
                "publication-metadata + indexed-abstract verified",
                "63-esirkepov-publisher-abstract-compare.md",
            )
        ),
        "access_audit_retains_pdf_boundary": all(
            marker in access_text
            for marker in ("publisher PDF status", "still missing", "HTTP/2 403")
        ),
    }
    result = {
        "contract": "Esirkepov publisher indexed abstract compare",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "PUBLISHER_METADATA_ABSTRACT_VERIFIED_PREPRINT_SOURCE_RUNTIME_PDF_MISSING",
        "scope": "indexed abstract versus arXiv preprint; no publisher-PDF line-by-line claim",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Esirkepov publisher abstract compare contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
