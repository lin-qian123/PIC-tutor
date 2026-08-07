#!/usr/bin/env python
"""Audit the local-only publisher-PDF closure records for two literature gaps."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


PAPERS = (
    {
        "key": "esirkepov",
        "pdf": "references/04_particle_pushers_deposition_shapes/2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor/publisher/2001_EsirkepovCPC2001_publisher-final.pdf",
        "compare": "docs/esirkepov-publisher-version-compare.md",
        "sha256": "cb03ca28144aa351ca964bbc8ba5012d4e88f5ba8f3a7a10e4b437c1afb07855",
        "pages": 10,
        "markers": ("`Eq. (23)`", "Second-order spline algorithm", "Git"),
    },
    {
        "key": "lee",
        "pdf": "references/08_boundaries_pml_geometry/2015_LeeCPC2015_Efficiency_of_the_PML_with_high-order_FD_and_pseudo-spectral_Maxwell_solvers/publisher/2015_LeeCPC2015_publisher-final.pdf",
        "compare": "docs/leecpc2015-publisher-version-compare.md",
        "sha256": "920ec7958bdcd45168ac43e60eeb2acdfe4fa63222f671413f0c41c83572a41e",
        "pages": 9,
        "markers": ("PSTD", "Appendices", "Git"),
    },
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    checks: dict[str, bool] = {}
    assets: dict[str, dict[str, object]] = {}
    for paper in PAPERS:
        pdf = root / paper["pdf"]
        compare = root / paper["compare"]
        compare_text = compare.read_text(encoding="utf-8") if compare.is_file() else ""
        key = str(paper["key"])
        checks[f"{key}_publisher_pdf_present"] = pdf.is_file()
        checks[f"{key}_publisher_pdf_hash_matches"] = pdf.is_file() and sha256(pdf) == paper["sha256"]
        checks[f"{key}_publisher_pdf_page_count_matches"] = pdf.is_file() and len(PdfReader(str(pdf)).pages) == paper["pages"]
        checks[f"{key}_bounded_compare_present"] = compare.is_file()
        checks[f"{key}_bounded_compare_markers_present"] = all(marker in compare_text for marker in paper["markers"])
        assets[key] = {"pages": paper["pages"], "sha256": paper["sha256"]}

    result = {
        "contract": "local publisher-PDF bounded comparison closure",
        "classification": "LOCAL_PUBLISHER_PDF_BOUNDED_COMPARE_CLOSED_NOT_FOR_REDISTRIBUTION",
        "scope": "validates two local PDFs and public comparison records; does not validate redistribution rights or WarpX runtime behavior",
        "checks": checks,
        "assets": assets,
        "passed": all(checks.values()),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Publisher-PDF bounded comparison closure", "", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}", "", "| check | status |", "|---|:---:|"]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
