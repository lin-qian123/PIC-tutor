#!/usr/bin/env python
"""Audit Chapter 5's reader-facing deposition validation ladder."""

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
    chapter = (ROOT / "manuscript/chapters/05-deposition-shapes.md").read_text(encoding="utf-8")
    langmuir = warpx / "Examples/Tests/langmuir"
    vay = warpx / "Examples/Tests/vay_deposition"
    source = warpx / "Source/Particles"

    vay_input = (vay / "inputs_test_2d_vay_deposition").read_text(encoding="utf-8")
    vay_cmake = (vay / "CMakeLists.txt").read_text(encoding="utf-8")
    vay_analysis = (vay / "analysis.py").read_text(encoding="utf-8")
    langmuir_cmake = (langmuir / "CMakeLists.txt").read_text(encoding="utf-8")
    langmuir_input = (langmuir / "inputs_test_3d_langmuir_multi").read_text(encoding="utf-8")
    langmuir_base = (langmuir / "inputs_base_3d").read_text(encoding="utf-8")
    langmuir_analysis = (langmuir / "analysis_3d.py").read_text(encoding="utf-8")
    analysis_utils = (langmuir / "analysis_utils.py").read_text(encoding="utf-8")
    deposit_source = (source / "WarpXParticleContainer.cpp").read_text(encoding="utf-8")
    current_source = (source / "Deposition/CurrentDeposition.H").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing_markers(
            chapter,
            [
                "### 5.14.2.3 修改沉积后的验证阶梯：先核 source，再解释场",
                "第一层：先确认配置能够到达对应 kernel",
                "第二层：把 `divE-rho/epsilon_0` 当作 source consumer",
                "第三层：解析场是 field consumer",
                "第四层：checksum 是回归 consumer",
                "未执行检查”误读为 PASS",
            ],
        ),
        "vay_source_contract": missing_markers(
            vay_input,
            [
                "algo.current_deposition = vay",
                "algo.maxwell_solver = psatd",
                "algo.particle_pusher = vay",
                "amr.max_level = 0",
                "diag1.fields_to_plot = By Ex Ez jx jz rho divE",
                "max_step = 50",
            ],
        )
        + missing_markers(
            vay_cmake,
            ["test_2d_vay_deposition", "2  # nprocs", '"analysis.py diags/diag1000050"'],
        )
        + missing_markers(
            vay_analysis,
            [
                "rho/epsilon_0 - div(E)",
                "tolerance = 1e-3",
                "assert error_rel < tolerance",
            ],
        ),
        "esirkepov_field_and_source_contract": missing_markers(
            langmuir_cmake,
            ["test_3d_langmuir_multi", "2  # nprocs", '"analysis_3d.py diags/diag1000040"'],
        )
        + missing_markers(
            langmuir_input,
            ["FILE = inputs_base_3d"],
        )
        + missing_markers(
            langmuir_base,
            [
                "algo.current_deposition = esirkepov",
                "max_step = max_step",
                "algo.particle_shape = 1",
                "diag1.fields_to_plot = Ex Ey Ez Bx By Bz jx jy jz part_per_cell rho divE",
            ],
        )
        + missing_markers(
            langmuir_analysis,
            ["tolerance_rel = 5e-2", "assert error_rel < tolerance_rel", "check_charge_conservation(data)"],
        )
        + missing_markers(
            analysis_utils,
            [
                "current_deposition_esirkepov",
                "and not (geometry_dims_rz or maxwell_solver_psatd)",
                "tolerance = 1e-11",
                "assert error_rel < tolerance",
            ],
        ),
        "dispatch_and_guard_boundaries": missing_markers(
            deposit_source,
            [
                "Charge-conserving current depositions (Esirkepov and Villasenor) cannot be used with a collocated grid.",
                "Cannot do shared memory deposition with Esirkepov algorithm",
                "Cannot do shared memory deposition with Villasenor algorithm",
                "Cannot do shared memory deposition with Vay algorithm",
                "CurrentDepositionAlgo::Esirkepov",
                "doEsirkepovDepositionShapeN<1>",
                "CurrentDepositionAlgo::Villasenor",
                "doVillasenorDepositionShapeNExplicit<1>",
                "CurrentDepositionAlgo::Vay",
                "The Vay algorithm cannot be used with implicit algorithm.",
                "doVayDepositionShapeN<1>",
            ],
        )
        + missing_markers(
            current_source,
            [
                "Vay deposition not implemented in RZ geometry",
                "Vay deposition not implemented in 1D geometry",
                "Vay current deposition",
            ],
        ),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_DEPOSITION_VALIDATION_LADDER_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Source/Particles/WarpXParticleContainer.cpp",
            "Source/Particles/Deposition/CurrentDeposition.H",
            "Examples/Tests/vay_deposition/{inputs_test_2d_vay_deposition,CMakeLists.txt,analysis.py}",
            "Examples/Tests/langmuir/{inputs_test_3d_langmuir_multi,inputs_base_3d,CMakeLists.txt,analysis_3d.py,analysis_utils.py}",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The card separates dispatch preconditions, source residuals, analytic fields, and checksum regression.",
            "It does not establish AMR, RZ, implicit Villasenor, or general geometry-by-shape coverage.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 5 Deposition Validation Ladder",
        "",
        "Classification: `SOURCE_GROUNDED_DEPOSITION_VALIDATION_LADDER_READER_CARD`.",
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
