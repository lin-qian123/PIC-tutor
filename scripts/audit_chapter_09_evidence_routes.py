#!/usr/bin/env python
"""Audit the source and reader-facing contract of Chapter 9 evidence routes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    warpx = args.warpx_root.resolve()
    project = args.project_root.resolve()
    chapter = read(project, "manuscript/chapters/09-literature-roadmap.md")
    langmuir_cmake = read(warpx, "Examples/Tests/langmuir/CMakeLists.txt")
    langmuir_input = read(warpx, "Examples/Tests/langmuir/inputs_base_3d")
    langmuir_analysis = read(warpx, "Examples/Tests/langmuir/analysis_3d.py")
    langmuir_utils = read(warpx, "Examples/Tests/langmuir/analysis_utils.py")
    deposition_source = read(warpx, "Source/Particles/Deposition/CurrentDeposition.H")
    particle_container = read(warpx, "Source/Particles/WarpXParticleContainer.cpp")
    galilean_cmake = read(warpx, "Examples/Tests/nci_psatd_stability/CMakeLists.txt")
    galilean_input = read(warpx, "Examples/Tests/nci_psatd_stability/inputs_test_2d_galilean_psatd")
    galilean_analysis = read(warpx, "Examples/Tests/nci_psatd_stability/analysis_galilean.py")
    spectral_solver = read(warpx, "Source/FieldSolver/SpectralSolver/SpectralSolver.cpp")
    pml_cmake = read(warpx, "Examples/Tests/pml/CMakeLists.txt")
    pml_input = read(warpx, "Examples/Tests/pml/inputs_test_2d_pml_x_psatd")
    pml_analysis = read(warpx, "Examples/Tests/pml/analysis_pml_psatd.py")
    push_fields = read(warpx, "Source/FieldSolver/WarpXPushFieldsEM.cpp")
    pml_algorithm = read(
        warpx, "Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPml.cpp"
    )
    warpx_revision = subprocess.check_output(
        ["git", "-C", str(warpx), "rev-parse", "HEAD"], text=True
    ).strip()

    checks = {
        "reader_card_present": all(
            marker in chapter
            for marker in (
                "### 9.6.1 三条从文献走到可观察量的读者路线",
                "并不证明所有 shape、二维或 RZ",
                "不是解析 NCI growth rate",
                "不是对 LeeCPC2015 所有系数或扫描的复现",
                "论文 -> 实现 -> 输入 -> consumer",
            )
        ),
        "esirkepov_route_contract": all(
            marker in langmuir_cmake + langmuir_input + langmuir_analysis + langmuir_utils
            for marker in (
                "test_3d_langmuir_multi",
                "inputs_test_3d_langmuir_multi",
                "algo.current_deposition = esirkepov",
                '"analysis_3d.py diags/diag1000040"',
                "tolerance_rel = 5e-2",
                "check_charge_conservation(data)",
                "tolerance = 1e-11",
                "assert error_rel < tolerance",
            )
        ) and all(
            marker in deposition_source + particle_container
            for marker in ("doEsirkepovDepositionShapeN", "CurrentDepositionAlgo::Esirkepov")
        ),
        "galilean_route_contract": all(
            marker in galilean_cmake + galilean_input + galilean_analysis + spectral_solver
            for marker in (
                "test_2d_galilean_psatd",
                '"analysis_galilean.py diags/diag1000400"',
                "algo.current_deposition = direct",
                "psatd.current_correction = 0",
                "energy_ref = 35657.41657683263",
                "assert err_energy < tol_energy",
                "if current_correction:",
                "assert err_charge < tol_charge",
                "PsatdAlgorithmGalilean",
            )
        ),
        "pml_route_contract": all(
            marker in pml_cmake + pml_input + pml_analysis + push_fields + pml_algorithm
            for marker in (
                "test_2d_pml_x_psatd",
                '"analysis_pml_psatd.py diags/diag1000300"',
                "algo.maxwell_solver = psatd",
                "psatd.current_correction = 0",
                'filename_init = os.path.join(cwd, "diags/diag1000050")',
                "reflectivity_max = 1e-6",
                "assert reflectivity < reflectivity_max",
                "pml[lev]->PushPSATD",
                "PsatdAlgorithmPml::pushSpectralFields",
            )
        ),
    }
    result = {
        "contract": "chapter 9 evidence routes reader card",
        "classification": "SOURCE_GROUNDED_READER_EVIDENCE_ROUTES",
        "warpx_revision": warpx_revision,
        "warpx_source_paths": [
            "Examples/Tests/langmuir/",
            "Examples/Tests/nci_psatd_stability/",
            "Examples/Tests/pml/",
            "Source/Particles/Deposition/",
            "Source/FieldSolver/SpectralSolver/",
        ],
        "checks": checks,
        "passed": all(checks.values()),
        "scope": (
            "Source and reader-text consistency for three Chapter 9 evidence routes. "
            "It does not rerun WarpX or establish equivalence between a paper, every WarpX path, "
            "or a general physics result."
        ),
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 9 evidence-routes reader-card contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- WarpX revision: `{warpx_revision}`",
        "- checked source paths: `Examples/Tests/langmuir/`, `Examples/Tests/nci_psatd_stability/`, `Examples/Tests/pml/`, `Source/Particles/Deposition/`, `Source/FieldSolver/SpectralSolver/`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
