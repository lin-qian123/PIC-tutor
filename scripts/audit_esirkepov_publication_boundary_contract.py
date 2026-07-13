#!/usr/bin/env python
"""Audit the explicit publication-boundary contract for Esirkepov 2001."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PAPER_DIRNAME = (
    "2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-in-Cell_simulation_with_an_arbitrary_form-factor"
)
CLASSIFICATION = "PREPRINT_FORMULA_SOURCE_RUNTIME_PUBLISHER_BOUNDARY_EXPLICIT"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    paper_dir = root / "references/04_particle_pushers_deposition_shapes" / PAPER_DIRNAME
    chapter = (root / "manuscript/chapters/05-deposition-shapes.md").read_text(encoding="utf-8")
    access = (paper_dir / "access-audit.md").read_text(encoding="utf-8")
    crosswalk = root / "runs/stage-c-validation/esirkepov-paper-source-runtime-crosswalk/contract.json"
    preprint_pdf = next(paper_dir.glob("*.pdf"), None)
    preprint_md = next(
        path
        for path in paper_dir.glob("*.md")
        if "中文讲解" not in path.name and "源码映射" not in path.name and path.name != "access-audit.md"
    )
    note = next(paper_dir.glob("*中文讲解.md"), None)

    checks = {
        "preprint_pdf_present": preprint_pdf is not None and preprint_pdf.stat().st_size > 0,
        "preprint_markdown_present": preprint_md.exists() and preprint_md.stat().st_size > 0,
        "mineru_image_set_present": len(list(paper_dir.glob("images/*"))) == 39,
        "chinese_note_present": note is not None and note.stat().st_size > 0,
        "publication_metadata_present": all(
            marker in access
            for marker in (
                "10.1016/S0010-4655(00)00228-9",
                "Computer Physics Communications 135(2), 144-153",
                "Exact charge conservation scheme for Particle-in-Cell simulation with an arbitrary form-factor",
            )
        ),
        "publisher_pdf_missing_recorded": "publisher PDF status**: still missing" in access,
        "publisher_endpoint_boundary_recorded": "HTTP 403" in access and "content-type: text/html" in access,
        "chapter_formula_source_mapping_present": all(
            marker in chapter for marker in ("Eq.(23)", "one_third", "one_sixth", "sdxi/sdyj/sdzk")
        ),
        "chapter_boundary_wording_present": all(
            marker in chapter
            for marker in (
                "发表版缺口审计契约",
                "publisher-PDF line-by-line compare",
                "不能把它写成 CPC 定稿逐式已核对",
            )
        ),
        "crosswalk_boundary_classification_present": crosswalk.exists()
        and json.loads(crosswalk.read_text(encoding="utf-8"))["classification"]
        == "PREPRINT_SOURCE_RUNTIME_CROSSWALK_PUBLISHER_PDF_MISSING",
        "no_false_publisher_pdf_completion_claim": "publisher PDF 已完成逐行核对" not in chapter,
    }
    result = {
        "contract": "Esirkepov 2001 publication boundary contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": CLASSIFICATION,
        "scope": "preprint formula/source/runtime evidence and explicit CPC publisher-PDF negative-space boundary; no publisher-PDF line-by-line claim",
        "paper_dir": str(paper_dir),
        "crosswalk": str(crosswalk),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Esirkepov 2001 publication boundary contract",
        "",
        f"- classification: `{CLASSIFICATION}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "This contract makes the missing publisher-formatted CPC PDF an explicit, testable boundary. It does not downgrade the available preprint formula, current WarpX source, or existing runtime ledgers.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
