#!/usr/bin/env python
"""Audit the LeeCPC2015 paper/source/regression crosswalk.

This is a read-only evidence contract. It checks that the local accepted
manuscript contains the claimed PSTD and reflection anchors, that the current
WarpX checkout contains the implementation-side coefficient surfaces, and that
the official Cartesian PSATD-PML regression exposes the expected reflectivity
consumer. It does not claim publisher-PDF identity or coefficient equivalence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PAPER_NAME = (
    "2015_LeeCPC2015_Efficiency_of_the_PML_with_high-order_FD_and_pseudo-spectral_Maxwell_solvers"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def contains(text: str, *needles: str) -> bool:
    return all(needle in text for needle in needles)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    warpx_root = args.warpx_root.resolve()
    source_md = paper_dir / f"{PAPER_NAME}.md"
    paper_text = read(source_md)

    pml_source = warpx_root / "Source" / "BoundaryConditions" / "PML.cpp"
    psatd_source = (
        warpx_root
        / "Source"
        / "FieldSolver"
        / "SpectralSolver"
        / "SpectralAlgorithms"
        / "PsatdAlgorithmPml.cpp"
    )
    analysis_source = warpx_root / "Examples" / "Tests" / "pml" / "analysis_pml_psatd.py"
    cmake_source = warpx_root / "Examples" / "Tests" / "pml" / "CMakeLists.txt"

    pml_text = read(pml_source)
    psatd_text = read(psatd_source)
    analysis_text = read(analysis_source)
    cmake_text = read(cmake_source)

    checks = {
        "paper_pstd_section": contains(
            paper_text,
            "## Application to Staggered-Grid Pseudo-Spectral Time-Domain (PSTD) Solvers",
            "Fourier transformation",
            "staggered grid",
        ),
        "paper_staggered_phase_anchor": contains(
            paper_text, "exp ( - i k", "represent the shifts"
        ),
        "paper_reflection_recurrence": contains(
            paper_text,
            "## Coefficient of Reflection of the Entire PML Layer",
            "R _ { j }",
            "iterated recursively",
        ),
        "paper_pstd_infinite_order_claim": contains(
            paper_text, "infinite order", "efficiency of absorption"
        ),
        "paper_sigma_profile_anchor": contains(
            paper_text, "sigma _ { i }", "sigma _ { m a x }", "delta = 5 \\Delta x", "n = 2"
        ),
        "warpx_pml_profile_surface": contains(
            pml_text, "sigma", "sigma_star", "sigma_cumsum", "sigma_star_cumsum"
        ),
        "warpx_psatd_propagator_surface": contains(
            psatd_text,
            "const amrex::Real C1",
            "const Complex C10",
            "const Complex C23",
            "const Complex C25",
            "const Complex T2",
        ),
        "warpx_cleaning_extension_surface": contains(
            psatd_text, "Idx.Fx", "Idx.Gx", "C23_c2"
        ),
        "warpx_regression_reflectivity_consumer": contains(
            analysis_text,
            "energy_start",
            "reflectivity_max = 1e-6",
            "assert reflectivity < reflectivity_max",
        ),
        "warpx_regression_cmake_wiring": contains(
            cmake_text, "test_2d_pml_x_psatd", "analysis_pml_psatd.py diags/diag1000300"
        ),
    }
    result = {
        "contract": "LeeCPC2015 paper/source/regression crosswalk",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "ACCEPTED_MANUSCRIPT_SOURCE_CROSSWALK_PUBLISHER_PDF_STILL_MISSING",
        "scope": "paper anchors, WarpX implementation surfaces, and official regression wiring; no publisher-PDF or coefficient-equivalence claim",
        "paper": str(source_md),
        "warpx_root": str(warpx_root),
        "source_paths": {
            "pml_profile": str(pml_source),
            "psatd_propagator": str(psatd_source),
            "analysis": str(analysis_source),
            "cmake": str(cmake_source),
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# LeeCPC2015 paper/source/regression crosswalk",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(
        f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |"
        for name, passed in checks.items()
    )
    lines += [
        "",
        "A PASS means the three evidence surfaces are present and internally linked; it does not make the accepted manuscript a publisher-formatted CPC PDF or prove that Lee's equations are identical to WarpX C1-C25.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
