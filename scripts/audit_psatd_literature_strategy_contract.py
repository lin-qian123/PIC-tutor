#!/usr/bin/env python
"""Audit the local PSATD/NCI literature-to-source strategy matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PAPERS = {
    "godfrey_2014": {
        "directory": "references/06_stability_filtering_nci/2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm",
        "keywords": ("NCI", "filter", "PSATD"),
        "chapter_markers": ("Godfrey 2014", "fixed-grid PSATD", "nci_psatd_stability"),
        "source_markers": ("PsatdAlgorithm", "use_filter"),
        "runtime_markers": ("nci_psatd_stability", "analysis_galilean.py"),
    },
    "lehe_2016": {
        "directory": "references/06_stability_filtering_nci/2016_LehePRE2016_Elimination_of_NCI_by_Galilean_coordinates",
        "keywords": ("Galilean", "continuity", "NCI"),
        "chapter_markers": ("Lehe et al. 2016", "Galilean PSATD", "离散连续性方程"),
        "source_markers": ("PsatdAlgorithmGalilean", "rho_old_mod"),
        "runtime_markers": ("analysis_galilean.py", "current-correction"),
    },
    "kirchen_2016": {
        "directory": "references/06_stability_filtering_nci/2016_KirchenPOP2016_Stable_discrete_representation_of_relativistically_drifting_plasmas",
        "keywords": ("boosted", "Galilean", "plasma"),
        "chapter_markers": ("Kirchen et al. 2016", "boosted-frame", "psatd.use_default_v_galilean"),
        "source_markers": ("gamma_boost", "v_galilean"),
        "runtime_markers": ("boosted-frame", "analysis_galilean.py"),
    },
}


def files_present(paper_dir: Path) -> bool:
    pdf = next(paper_dir.glob("*.pdf"), None)
    markdown = next(
        (path for path in paper_dir.glob("*.md") if "中文讲解" not in path.name), None
    )
    chinese_note = next(paper_dir.glob("*-中文讲解.md"), None)
    return all(path is not None and path.exists() for path in (pdf, markdown, chinese_note)) and (
        paper_dir / "reading-log.md"
    ).exists()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--source-notes", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    chapter = args.chapter.resolve().read_text(encoding="utf-8")
    source_notes = "\n".join(path.read_text(encoding="utf-8") for path in args.source_notes.resolve().glob("*.md"))
    papers = {}
    for key, spec in PAPERS.items():
        paper_dir = root / spec["directory"]
        papers[key] = {
            "directory": str(paper_dir),
            "local_assets_present": files_present(paper_dir),
            "asset_keywords_present": all(any(word.lower() in path.read_text(encoding="utf-8", errors="ignore").lower() for path in paper_dir.glob("*.md")) for word in spec["keywords"]),
            "chapter_mapping_present": all(marker.lower() in chapter.lower() for marker in spec["chapter_markers"]),
            "source_mapping_present": all(marker.lower() in source_notes.lower() or marker.lower() in chapter.lower() for marker in spec["source_markers"]),
            "runtime_mapping_present": all(marker.lower() in chapter.lower() or marker.lower() in source_notes.lower() for marker in spec["runtime_markers"]),
        }
        papers[key]["passed"] = all(value for name, value in papers[key].items() if name.endswith("present") or name == "local_assets_present")

    result = {
        "contract": "PSATD/NCI literature-to-source strategy matrix",
        "papers": papers,
        "passed": all(paper["passed"] for paper in papers.values()),
        "classification": "FULL_TEXT_SOURCE_GROUNDED_RUNTIME_STRATEGY_MATRIX",
        "scope": "indexing contract across Godfrey fixed-grid PSATD, Lehe Galilean PSATD, and Kirchen boosted-frame application; not a new physics regression",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# PSATD/NCI literature-to-source strategy matrix",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| paper | local assets | chapter | source | runtime | status |",
        "|---|:---:|:---:|:---:|:---:|:---:|",
    ]
    for key, paper in papers.items():
        lines.append(
            f"| `{key}` | `{'PASS' if paper['local_assets_present'] else 'FAIL'}` | "
            f"`{'PASS' if paper['chapter_mapping_present'] else 'FAIL'}` | "
            f"`{'PASS' if paper['source_mapping_present'] else 'FAIL'}` | "
            f"`{'PASS' if paper['runtime_mapping_present'] else 'FAIL'}` | "
            f"`{'PASS' if paper['passed'] else 'FAIL'}` |"
        )
    lines.extend(["", "This matrix indexes existing full-text, source-grounded and runtime evidence; it does not claim that the three papers are numerically equivalent or that every branch is regression-covered."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
