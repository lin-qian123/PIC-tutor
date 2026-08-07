#!/usr/bin/env python
"""Audit the bounded LeeCPC2015 accepted-manuscript asset contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TITLE = "Efficiency of the Perfectly Matched Layer with High-Order Finite Difference and Pseudo-Spectral Maxwell Solvers"
DOI = "10.1016/j.cpc.2015.04.004"
ESCHOLARSHIP_URL = "https://escholarship.org/uc/item/49m2k3vj"


def pdf_page_count(pdf_path: Path) -> int:
    data = pdf_path.read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?:\s|/|>)", data))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    pdf = next(paper_dir.glob("*.pdf"), None)
    source_md = next(
        (path for path in paper_dir.glob("*.md") if "中文讲解" not in path.name and "公式" not in path.name and "access-audit" not in path.name and path.name != "README.md"),
        None,
    )
    note = next(paper_dir.glob("*-中文讲解.md"), None)
    readme = (paper_dir / "README.md").read_text(encoding="utf-8")
    audit = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    source_text = source_md.read_text(encoding="utf-8") if source_md else ""
    note_text = note.read_text(encoding="utf-8") if note else ""
    publisher_compare = paper_dir.parents[2] / "docs/leecpc2015-publisher-version-compare.md"
    publisher_compare_text = publisher_compare.read_text(encoding="utf-8") if publisher_compare.is_file() else ""
    images = sorted((paper_dir / "images").glob("*")) if (paper_dir / "images").is_dir() else []
    referenced_images = set(re.findall(r"images/([^\s)]+)", source_text))
    image_names = {path.name for path in images}

    checks = {
        "paper_directory_present": paper_dir.is_dir(),
        "accepted_manuscript_pdf_present": bool(pdf and pdf.exists()),
        "accepted_manuscript_pdf_is_seven_pages": bool(pdf and pdf_page_count(pdf) == 7),
        "mineru_markdown_present": bool(source_md and source_md.exists()),
        "mineru_structure_present": all(
            heading in source_text
            for heading in (
                "## INTRODUCTION",
                "## PERFECTLY MATCHED LAYER (PML)",
                "## Discretization of the PML",
                "## Application to Staggered-Grid Pseudo-Spectral Time-Domain (PSTD) Solvers",
                "## REFLECTION OF A PLANE WAVE STRIKING A PML",
                "## RESULTS",
                "## CONCLUSION",
            )
        ),
        "formula_anchors_present": all(
            marker in source_text for marker in ("tag{1}", "tag{2}", "tag{3}", "tag{4}", "R _ { j }", "exp ( - i k")
        ),
        "all_referenced_images_present": bool(referenced_images) and referenced_images <= image_names,
        "thirteen_extracted_images_present": len(images) == 13,
        "chinese_note_present": bool(note and note.exists()),
        "chinese_note_covers_formula_and_source_boundary": all(
            term in note_text
            for term in (
                "PML medium",
                "反射系数",
                "staggered-grid",
                "C1-C25",
                "publisher",
                "accepted/submitted manuscript",
            )
        ),
        "bibliographic_identity_recorded": TITLE.lower() in readme.lower() and DOI in readme,
        "primary_asset_source_recorded": ESCHOLARSHIP_URL in readme or ESCHOLARSHIP_URL in audit,
        "publisher_boundary_explicit": all(
            term in audit
            for term in (
                "accepted/submitted manuscript",
                "publisher-formatted CPC version",
                "publisher-formatted CPC PDF",
            )
        ),
        "publisher_abstract_boundary_recorded": "ScienceDirect indexed" in audit and "abstract-level" in audit,
        "publisher_version_comparison_recorded": publisher_compare.is_file() and all(
            term in publisher_compare_text for term in ("9-page", "PSTD", "Appendices")
        ),
        "publisher_boundary_not_overclaimed_in_note": all(
            term in note_text for term in ("不能直接等同于 WarpX", "仍需", "不能")
        ),
    }
    result = {
        "contract": "LeeCPC2015 accepted-manuscript source-grounded literature contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "ACCEPTED_MANUSCRIPT_AND_LOCAL_PUBLISHER_CPC_BOUNDED_COMPARE_SOURCE_GROUNDED",
        "scope": "the seven-page accepted/submitted manuscript supports first-round source mapping, while a locally retained nine-page publisher PDF supplies a bounded version comparison; no redistribution or runtime claim follows",
        "source": ESCHOLARSHIP_URL,
        "published": {"title": TITLE, "doi": DOI, "journal": "Computer Physics Communications 194, 1-9 (2015)"},
        "asset": {
            "pdf_pages": pdf_page_count(pdf) if pdf else 0,
            "image_count": len(images),
            "referenced_image_count": len(referenced_images),
        },
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# LeeCPC2015 accepted-manuscript contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- source: [{ESCHOLARSHIP_URL}]({ESCHOLARSHIP_URL})",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The contract validates the accepted-manuscript package and its bounded publisher-version record; it does not validate redistribution or WarpX runtime behavior.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
