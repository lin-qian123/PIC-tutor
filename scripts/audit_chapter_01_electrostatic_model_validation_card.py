#!/usr/bin/env python
"""Audit Chapter 1's reader-facing electrostatic model-validation card."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def missing(text: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    warpx = args.warpx_root.resolve()
    chapter = (ROOT / "manuscript/chapters/01-kinetic-models.md").read_text(encoding="utf-8")
    parameters = (warpx / "Docs/source/usage/parameters.rst").read_text(encoding="utf-8")
    theory = (warpx / "Docs/source/theory/models_algorithms/electrostatic_pic.rst").read_text(
        encoding="utf-8"
    )
    test_root = warpx / "Examples/Tests/electrostatic_sphere_eb"
    cmake = (test_root / "CMakeLists.txt").read_text(encoding="utf-8")
    inputs = (test_root / "inputs_test_3d_electrostatic_sphere_eb").read_text(
        encoding="utf-8"
    )
    analysis = (test_root / "analysis.py").read_text(encoding="utf-8")
    evolve = (warpx / "Source/Evolve/WarpXEvolve.cpp").read_text(encoding="utf-8")
    initialization = (warpx / "Source/Initialization/WarpXInitData.cpp").read_text(
        encoding="utf-8"
    )

    checks = {
        "reader_card_present": missing(
            chapter,
            [
                "### 1.5.1 模型选择与验证卡：Poisson 可解不等于完整电磁问题已被解决",
                "第一层：先判断问题是否仍需传播电磁自由度",
                "第二层：明确实际解的是什么",
                "第三层：用一个有解析 reference 的 producer 检查指定对象",
                "第四层：让 consumer 与所问问题一一对应",
                "Poisson 残差小，所以激光传播也正确",
                "没有 electromagnetic CFL，所以时间步不再需要物理判断",
            ],
        ),
        "official_model_contract": missing(
            parameters,
            [
                "warpx.do_electrostatic",
                "instead of updating",
                "the fields at each iteration with the full Maxwell equations",
                "There is no limitation on the timestep in this case",
                "electromagnetic effects (e.g. propagation of radiation, lasers, etc.)",
            ],
        )
        + missing(
            theory,
            [
                "only the electric field is",
                "electrostatic potential from the charge density",
                r"\boldsymbol{\nabla}^2 \phi = - \rho/\epsilon_0",
                "Electromagnetostatic",
            ],
        ),
        "official_sphere_producer": missing(
            cmake,
            [
                "test_3d_electrostatic_sphere_eb",
                "3  # dims",
                "2  # nprocs",
                '"analysis.py"',
                '"analysis_default_regression.py --path diags/diag1/"',
            ],
        )
        + missing(
            inputs,
            [
                "max_step = 1",
                "warpx.do_electrostatic = labframe",
                "boundary.field_lo = pec pec pec",
                "warpx.eb_implicit_function",
                "warpx.eb_potential(x,y,z,t) = \"1.\"",
                "diag1.fields_to_plot = Ex Ey Ez rho phi eb_covered",
                "eb_charge.type = ChargeOnEB",
                "eb_charge_one_eighth.weighting_function(x,y,z)",
            ],
        ),
        "geometry_and_charge_consumers": missing(
            analysis,
            [
                "q_th = 4 * np.pi * epsilon_0 * phi_0 * R",
                "data = np.loadtxt(\"diags/reducedfiles/eb_charge.txt\")",
                "assert abs((q_sim - q_th) / q_th) < 0.06",
                "assert abs((q_sim_eighth - q_th / 8) / (q_th / 8)) < 0.06",
                "ts.get_field(\"eb_covered\", iteration=0)",
                "assert np.all(eb_covered >= 0)",
                "assert np.all(eb_covered[r < R - info.dx] == 1)",
                "assert np.all(eb_covered[r > R + info.dx] == 0)",
            ],
        ),
        "execution_and_combination_boundary": missing(
            initialization,
            [
                "ComputeSpaceChargeField(reset_E_field, reset_B_field)",
            ],
        )
        + missing(
            evolve,
            [
                "if( electrostatic_solver_id != ElectrostaticSolverAlgo::None",
                "bool const reset_E_field = true",
                "ComputeSpaceChargeField( reset_E_field, reset_B_field )",
                "Electrostatic solver cannot be used with sub-cycling.",
            ],
        ),
    }
    passed = all(not absent for absent in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_ELECTROSTATIC_MODEL_SELECTION_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Docs/source/{usage/parameters.rst,theory/models_algorithms/electrostatic_pic.rst}",
            "Examples/Tests/electrostatic_sphere_eb/{CMakeLists.txt,inputs_test_3d_electrostatic_sphere_eb,analysis.py}",
            "Source/{Initialization/WarpXInitData.cpp,Evolve/WarpXEvolve.cpp}",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The card separates model selection, a fixed-potential EB producer, charge and geometry consumers, and checksum regression.",
            "It does not establish electromagnetic propagation, laser physics, arbitrary Poisson accuracy, arbitrary EB geometry, particle kinetics, or electrostatic plus subcycling support.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 1 Electrostatic Model Validation Card",
        "",
        "Classification: `SOURCE_GROUNDED_ELECTROSTATIC_MODEL_SELECTION_READER_CARD`.",
        "",
        f"Result: `{'PASS' if passed else 'FAIL'}`.",
        "",
        "## Source Routes",
        "",
    ]
    lines.extend(f"- `{route}`" for route in payload["source_routes"])
    lines.extend(["", "## Checks", ""])
    for name, absent in checks.items():
        lines.append(f"- `{name}`: `{'PASS' if not absent else 'FAIL'}`")
        lines.extend(f"  - missing: `{marker}`" for marker in absent)
    lines.extend(["", "## Scope", ""])
    lines.extend(f"- {item}" for item in payload["scope"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
