#!/usr/bin/env python
"""Audit local full-text assets used by the Chapter 4 pusher literature line."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CONFIGS = {
    "Vay": {
        "label": "Vay 2008",
        "title": "Simulation of beams or plasmas crossing at relativistic velocity",
        "doi": "10.1063/1.2837054",
        "pages": 7,
        "images": 38,
        "source_markers": ("II. PUSHING PARTICLES", "III. SOLVING FOR THE FIELDS", "APPENDIX A", "APPENDIX B", "gyroradius", "moving frame"),
        "note_markers": ("frame", "moving frame", "WarpX", "解析"),
        "classification": "FULLTEXT_SOURCE_GROUNDED_FRAME_CONSISTENCY_APPENDIX_BOUNDARY",
        "scope": "local full-text PDF and MinerU package support Vay frame-consistency, explicit-gamma and gyroradius explanations; dedicated Appendix-B runtime reproduction remains open",
        "chapter_markers": ("Vay 2008", "UpdateMomentumVay.H", "Appendix A", "gyroradius"),
    },
    "Higuera": {
        "label": "Higuera-Cary 2017",
        "title": "Structure-preserving second-order integration of relativistic charged particle trajectories in electromagnetic fields",
        "doi": "10.1063/1.4979989",
        "pages": 9,
        "images": 44,
        "source_markers": ("II. Second-order charged particle integrators", "III. Explicit evaluation", "IV. Preservation of limiting solutions", "V. Volume-preservation", "VI. Numerical results", "Jacobian", "volume-preserving"),
        "note_markers": ("Jacobian", "volume-preserving", "drift", "WarpX", "resonance island"),
        "classification": "FULLTEXT_SOURCE_GROUNDED_VOLUME_DRIFT_JACOBIAN_BOUNDARY",
        "scope": "local full-text PDF and MinerU package support Higuera-Cary volume/drift/Jacobian explanations; dedicated phase-space-topology runtime reproduction remains open",
        "chapter_markers": ("Higuera-Cary 2017", "UpdateMomentumHigueraCary.H", "Jacobian", "volume-preserving"),
    },
}


def pdf_page_count(pdf_path: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page(?:\s|/|>)", pdf_path.read_bytes()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    key = next((name for name in CONFIGS if name.lower() in paper_dir.name.lower()), None)
    if key is None:
        raise SystemExit(f"cannot infer pusher config from {paper_dir}")
    config = CONFIGS[key]
    pdf = next(paper_dir.glob("*.pdf"), None)
    source_md = next(
        (
            p
            for p in paper_dir.glob("*.md")
            if "中文讲解" not in p.name and p.name not in {"README.md", "access-audit.md", "reading-log.md"}
        ),
        None,
    )
    note = next(paper_dir.glob("*-中文讲解.md"), None)
    readme = paper_dir / "README.md"
    access_audit = paper_dir / "access-audit.md"
    chapter_text = args.chapter.resolve().read_text(encoding="utf-8")
    source_text = source_md.read_text(encoding="utf-8") if source_md else ""
    note_text = note.read_text(encoding="utf-8") if note else ""
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    audit_text = access_audit.read_text(encoding="utf-8") if access_audit.exists() else ""
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
        "readme_scope_recorded": config["title"].lower() in readme_text.lower() and "Chapter 4" in readme_text,
        "bibliographic_identity_recorded": config["title"].lower() in readme_text.lower() and config["doi"] in readme_text,
        "access_boundary_recorded": config["classification"] in audit_text and "runtime" in audit_text.lower(),
        "chapter_mapping_recorded": all(marker in chapter_text for marker in config["chapter_markers"]),
    }
    result = {
        "contract": f"{config['label']} Chapter 4 pusher paper asset contract",
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
        f"# {config['label']} pusher paper asset contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", "The contract validates the local reading package and chapter mapping without claiming a dedicated runtime reproduction of every paper figure."]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
