#!/usr/bin/env python
"""Audit local full-text assets used by the Chapter 5 deposition literature line."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CONFIGS = {
    "Villasenor": {
        "label": "Villasenor-Buneman 1992",
        "title": "Rigorous charge conservation for local electromagnetic field solvers",
        "doi": "10.1016/0010-4655(92)90169-Y",
        "pages": 11,
        "images": 27,
        "source_markers": (
            "Introduction",
            "Calculating the fluxes and currents",
            "Field updating",
            "Implementation",
            "Extension to three dimensions",
            "four boundaries",
            "seven-boundary",
            "tenboundary",
            "charge conservation",
        ),
        "note_markers": ("four-boundary", "seven-boundary", "ten-boundary", "WarpX", r"\Delta x \Delta y \Delta z / 12"),
        "audit_markers": ("local full-text status", "publisher web access", "first-round"),
        "classification": "LOCAL_FULLTEXT_SOURCE_GROUNDED_FORMULA_AUDIT_PUBLISHER_PROVENANCE_PENDING",
        "scope": "local full-text PDF and MinerU package support a first-round formula/source walkthrough; publisher provenance and final-formula transcription remain open",
    },
    "Esirkepov": {
        "label": "Esirkepov 1999/2001",
        "title": "Exact charge conservation scheme for Particle-in-Cell",
        "doi": "10.1016/S0010-4655(00)00228-9",
        "pages": 13,
        "images": 39,
        "source_markers": (
            "1 Introduction",
            "2 Continuity equation in finite",
            "3 Density decomposition",
            "4 Computing of the current",
            "5 Conclusion",
            "tag{12}",
            "tag{15}",
            "tag{20}",
            "tag{23}",
            "tag{27}",
            "tag{34}",
        ),
        "note_markers": ("Eq.(23)", "1/3", "1/6", "second-order", "WarpX", "发表版"),
        "audit_markers": ("publisher PDF status", "arXiv preprint", "publisher-formatted CPC PDF", "bounded final-version comparison"),
        "classification": "PREPRINT_AND_LOCAL_PUBLISHER_CPC_BOUNDED_COMPARE_SOURCE_GROUNDED",
        "scope": "author-posted arXiv preprint supports the formula walkthrough, while a local publisher PDF supplies a bounded title/abstract/section/Eq.(23)/spline comparison; no redistribution or runtime claim follows",
    },
}


def pdf_page_count(pdf_path: Path) -> int:
    data = pdf_path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?:\s|/|>)", data))


def find_source_markdown(paper_dir: Path) -> Path | None:
    candidates = sorted(
        path
        for path in paper_dir.glob("*.md")
        if not any(token in path.name for token in ("中文讲解", "源码", "README", "access-audit", "reading-log"))
    )
    return candidates[0] if candidates else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    key = next((name for name in CONFIGS if name.lower() in paper_dir.name.lower()), None)
    if key is None:
        raise SystemExit(f"cannot infer paper config from {paper_dir}")
    config = CONFIGS[key]
    pdf = next(paper_dir.glob("*.pdf"), None)
    source_md = find_source_markdown(paper_dir)
    note = next(paper_dir.glob("*-中文讲解.md"), None)
    readme = (paper_dir / "README.md").read_text(encoding="utf-8")
    audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    source_text = source_md.read_text(encoding="utf-8") if source_md else ""
    note_text = note.read_text(encoding="utf-8") if note else ""
    images_dir = paper_dir / "images"
    images = sorted(images_dir.glob("*")) if images_dir.is_dir() else []

    checks = {
        "paper_directory_present": paper_dir.is_dir(),
        "pdf_present": bool(pdf and pdf.exists()),
        "pdf_page_count_matches": bool(pdf and pdf_page_count(pdf) == config["pages"]),
        "mineru_markdown_present": bool(source_md and source_md.exists()),
        "source_structure_and_formula_anchors_present": all(marker in source_text for marker in config["source_markers"]),
        "expected_image_count_present": len(images) == config["images"],
        "chinese_note_present": bool(note and note.exists()),
        "chinese_note_scope_present": all(marker in note_text for marker in config["note_markers"]),
        "bibliographic_identity_recorded": config["title"].lower() in readme.lower() and config["doi"] in readme,
        "access_boundary_recorded": all(marker in audit for marker in config["audit_markers"]),
    }
    result = {
        "contract": f"{config['label']} Chapter 5 deposition paper asset contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": config["classification"],
        "scope": config["scope"],
        "published": {"title": config["title"], "doi": config["doi"]},
        "asset": {"pdf_pages": pdf_page_count(pdf) if pdf else 0, "image_count": len(images)},
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        f"# {config['label']} deposition paper asset contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", "The contract validates the preprint reading package and bounded publisher-version evidence; it does not validate redistribution or WarpX runtime behavior."]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
