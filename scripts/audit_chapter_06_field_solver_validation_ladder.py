#!/usr/bin/env python
"""Audit Chapter 6's reader-facing field-solver validation ladder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def missing_markers(text: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    warpx = args.warpx_root.resolve()
    chapter = (ROOT / "manuscript/chapters/06-field-solvers.md").read_text(encoding="utf-8")
    pml = warpx / "Examples/Tests/pml"
    nci = warpx / "Examples/Tests/nci_psatd_stability"
    sphere = warpx / "Examples/Tests/electrostatic_sphere"
    field_solver = warpx / "Source/FieldSolver"

    pml_cmake = (pml / "CMakeLists.txt").read_text(encoding="utf-8")
    pml_analysis = (pml / "analysis_pml_yee.py").read_text(encoding="utf-8")
    pml_restart_analysis = (warpx / "Examples/analysis_default_restart.py").read_text(
        encoding="utf-8"
    )
    nci_cmake = (nci / "CMakeLists.txt").read_text(encoding="utf-8")
    nci_input = (nci / "inputs_test_2d_galilean_psatd_current_correction").read_text(
        encoding="utf-8"
    )
    nci_analysis = (nci / "analysis_galilean.py").read_text(encoding="utf-8")
    sphere_cmake = (sphere / "CMakeLists.txt").read_text(encoding="utf-8")
    sphere_input = (sphere / "inputs_test_3d_electrostatic_sphere_lab_frame").read_text(
        encoding="utf-8"
    )
    sphere_analysis = (sphere / "analysis_electrostatic_sphere.py").read_text(encoding="utf-8")
    push_fields = (field_solver / "WarpXPushFieldsEM.cpp").read_text(encoding="utf-8")
    electrostatic = (field_solver / "ElectrostaticSolvers/ElectrostaticSolver.cpp").read_text(
        encoding="utf-8"
    )
    solve_fields_es = (field_solver / "WarpXSolveFieldsES.cpp").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing_markers(
            chapter,
            [
                "### 6.11.10 场求解器修改后的验证阶梯：先匹配场量，再解释通过",
                "第一层：FDTD/PML 应先看反射率，而不是 checksum",
                "第二层：改 PSATD、Galilean frame 或 current correction 时看 NCI consumer",
                "第三层：改 Poisson 求解或 $\\phi\\to\\mathbf E$ 离散梯度时看解析场",
                "第四层：restart 和 checksum 是生命周期回归 consumer",
                "不是 PASS",
            ],
        ),
        "pml_reflectivity_contract": missing_markers(
            pml_cmake,
            ["test_2d_pml_x_yee", "2  # nprocs", '"analysis_pml_yee.py diags/diag1000300"'],
        )
        + missing_markers(
            pml_analysis,
            ["Reflectivity_theory", "tolerance_rel = 5.0 / 100", "assert error_rel < tolerance_rel"],
        )
        + missing_markers(
            push_fields,
            ["EvolveBPML(", "EvolveEPML(", "WarpX::PushPSATD"],
        ),
        "galilean_current_correction_contract": missing_markers(
            nci_cmake,
            [
                "test_2d_galilean_psatd_current_correction",
                "2  # nprocs",
                '"analysis_galilean.py diags/diag1000400"',
            ],
        )
        + missing_markers(
            nci_input,
            ["psatd.current_correction = 1", "psatd.periodic_single_box_fft = 0"],
        )
        + missing_markers(
            nci_analysis,
            [
                "reference energy corresponds to unstable results due to NCI",
                "tol_energy = 2e-8",
                "tol_charge = 2e-4",
                "assert err_energy < tol_energy",
                "assert err_charge < tol_charge",
            ],
        ),
        "electrostatic_sphere_contract": missing_markers(
            sphere_cmake,
            [
                "test_3d_electrostatic_sphere_lab_frame",
                "2  # nprocs",
                '"analysis_electrostatic_sphere.py diags/diag1000030"',
            ],
        )
        + missing_markers(sphere_input, ["warpx.do_electrostatic = labframe", "phi"])
        + missing_markers(
            sphere_analysis,
            [
                "l2_tolerance = 0.05",
                "assert L2_error_x < l2_tolerance",
                "assert L2_error_y < l2_tolerance",
                "assert L2_error_z < l2_tolerance",
                "energy_fraction = 0.0032",
                "assert abs((Ek_i + Ep_i) - (Ek_f + Ep_f)) < energy_fraction",
            ],
        )
        + missing_markers(
            solve_fields_es,
            ["WarpX::ComputeSpaceChargeField", "m_electrostatic_solver->ComputeSpaceChargeField"],
        )
        + missing_markers(electrostatic, ["ElectrostaticSolver::computePhi", "ElectrostaticSolver::computeE"]),
        "restart_contract": missing_markers(
            pml_cmake,
            ["test_2d_pml_x_yee_restart", '"analysis_default_restart.py diags/diag1000300"'],
        )
        + missing_markers(
            pml_restart_analysis,
            ["def check_restart(filename, tolerance=1e-12):", "for field in ds_benchmark.field_list:", "assert error < tolerance"],
        ),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_FIELD_SOLVER_VALIDATION_LADDER_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Source/FieldSolver/WarpXPushFieldsEM.cpp",
            "Source/FieldSolver/WarpXSolveFieldsES.cpp",
            "Source/FieldSolver/ElectrostaticSolvers/ElectrostaticSolver.cpp",
            "Examples/Tests/pml/{CMakeLists.txt,analysis_pml_yee.py}",
            "Examples/Tests/nci_psatd_stability/{CMakeLists.txt,inputs_test_2d_galilean_psatd_current_correction,analysis_galilean.py}",
            "Examples/Tests/electrostatic_sphere/{CMakeLists.txt,inputs_test_3d_electrostatic_sphere_lab_frame,analysis_electrostatic_sphere.py}",
            "Examples/analysis_default_restart.py",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The card separates PML absorption, NCI/current-correction, electrostatic analytic fields, and restart/checksum consumers.",
            "It does not establish cross-geometry, AMR, arbitrary MPI-layout, or convergence coverage.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 6 Field-Solver Validation Ladder",
        "",
        "Classification: `SOURCE_GROUNDED_FIELD_SOLVER_VALIDATION_LADDER_READER_CARD`.",
        "",
        f"Result: {'PASS' if passed else 'FAIL'}.",
        "",
        "## Source Routes",
        "",
    ]
    lines.extend(f"- `{route}`" for route in payload["source_routes"])
    lines.extend(["", "## Checks", ""])
    for name, missing in checks.items():
        lines.append(f"- `{name}`: `{'PASS' if not missing else 'FAIL'}`")
        if missing:
            lines.extend(f"  - missing: `{marker}`" for marker in missing)
    lines.extend(["", "## Scope", ""])
    lines.extend(f"- {item}" for item in payload["scope"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
