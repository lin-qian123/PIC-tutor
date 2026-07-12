#!/usr/bin/env python
"""Audit the Esirkepov paper/source/runtime crosswalk.

The contract is intentionally layered. It verifies paper anchors, current
WarpX source surfaces, and the presence/status of representative runtime
contracts. It does not turn boundary classifications into PASS claims and it
does not claim the publisher-formatted CPC PDF has been obtained.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PAPER_BASENAME = (
    "2001_EsirkepovCPC2001_Exact_charge_conservation_scheme_for_Particle-In-Cell_simulation_with_an_arbitrary_form-factor"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, *needles: str) -> bool:
    return all(needle in text for needle in needles)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-dir", type=Path, required=True)
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--runs-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    warpx_root = args.warpx_root.resolve()
    runs_root = args.runs_root.resolve()
    preprint = paper_dir / f"{PAPER_BASENAME}.md"
    chinese_note = paper_dir / f"{PAPER_BASENAME}-中文讲解.md"
    source_text = read(preprint)
    note_text = read(chinese_note)
    current = read(warpx_root / "Source/Particles/Deposition/CurrentDeposition.H")
    shapes = read(warpx_root / "Source/Particles/ShapeFactors.H")
    container = read(warpx_root / "Source/Particles/WarpXParticleContainer.cpp")
    writeback = read(warpx_root / "Source/FieldSolver/WarpXPushFieldsEM.cpp")
    langmuir_cmake = read(warpx_root / "Examples/Tests/langmuir/CMakeLists.txt")

    runtime_paths = {
        "3d_shape_matrix": runs_root / "esirkepov_langmuir_3d_shape-matrix/contract.json",
        "radial_shape_matrix": runs_root / "esirkepov_radial_geometry_shape-matrix/contract.json",
        "rz_shape_matrix": runs_root / "esirkepov_langmuir_rz_highres_shape-family/contract.json",
        "mr_source_contract": runs_root / "esirkepov_mr_source-contract/contract.json",
    }
    runtime = {name: load_json(path) for name, path in runtime_paths.items()}

    checks = {
        "paper_eq23_and_density_decomposition": has(
            source_text, "Eq.(23)", "density decomposition", "finite diferences"
        ),
        "paper_second_order_spline_algorithm": has(
            source_text,
            "## 4 Computing of the current with second-order polynomial form-factor",
            "second-order spline",
            "Eq.(26)",
        ),
        "paper_discrete_continuity_scope": has(
            source_text, "discreetized continuity equation", "not restricted by special Maxwell solver"
        ),
        "note_eq23_source_mapping": has(
            note_text, "Eq.(23)", "one_third", "one_sixth", "sdxi", "sdyj", "sdzk"
        ),
        "source_shape_factor_surfaces": has(
            shapes, "Compute_shape_factor", "Compute_shifted_shape_factor"
        ),
        "source_esirkepov_difference_surfaces": has(
            current, "sdxi", "sdyj", "sdzk", "one_third", "one_sixth", "invdtd"
        ),
        "source_geometry_writeback_surface": has(
            writeback, "ApplyInverseVolumeScalingToCurrentDensity"
        ) and has(
            current, "djr_cmplx", "djt_cmplx"
        ),
        "source_dispatch_and_limits": has(
            container, "CurrentDepositionAlgo::Esirkepov", "doEsirkepovDepositionShapeN", "collocated grid"
        ),
        "runtime_3d_shape_contract_present": runtime_paths["3d_shape_matrix"].exists(),
        "runtime_radial_shape_contract_present": runtime_paths["radial_shape_matrix"].exists(),
        "runtime_rz_shape_contract_present": runtime_paths["rz_shape_matrix"].exists(),
        "runtime_mr_source_contract_present": runtime_paths["mr_source_contract"].exists(),
        "runtime_contracts_keep_boundaries": all(
            "scope" in value or "classification" in value for value in runtime.values()
        ),
        "langmuir_cmake_has_geometry_families": has(
            langmuir_cmake, "inputs_test_3d_langmuir_multi", "inputs_test_rz_langmuir_multi", "inputs_test_rcylinder_langmuir_multi"
        ),
    }

    runtime_summary = {
        name: {
            "passed": value.get("passed"),
            "classification": value.get("classification"),
            "scope": value.get("scope"),
        }
        for name, value in runtime.items()
    }
    result = {
        "contract": "Esirkepov paper/source/runtime crosswalk",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "PREPRINT_SOURCE_RUNTIME_CROSSWALK_PUBLISHER_PDF_MISSING",
        "scope": "paper anchors, current-deposition source surfaces, geometry-family runtime contracts, and active Langmuir wiring; no publisher-PDF line-by-line claim",
        "paper": str(preprint),
        "warpx_root": str(warpx_root),
        "runtime_summary": runtime_summary,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Esirkepov paper/source/runtime crosswalk",
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
    lines += ["", "## Runtime evidence summary", "", "| family | passed | classification |", "|---|:---:|---|"]
    for name, summary in runtime_summary.items():
        lines.append(
            f"| `{name}` | `{summary['passed']}` | `{summary['classification']}` |"
        )
    lines += [
        "",
        "The runtime rows retain their own PASS/BOUNDARY scope. This crosswalk only proves that the paper, source and existing runtime ledgers are linked; it does not make the geometry/order matrix exhaustive.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
