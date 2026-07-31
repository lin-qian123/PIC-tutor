#!/usr/bin/env python
"""Audit Chapter 3A's independent distribution and self-field reader contracts."""

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
    chapter = (ROOT / "manuscript/chapters/03a-warpx-initialization.md").read_text(
        encoding="utf-8"
    )
    distribution_input = (
        warpx / "Examples/Tests/initial_distribution/inputs_test_3d_initial_distribution"
    ).read_text(encoding="utf-8")
    distribution_cmake = (warpx / "Examples/Tests/initial_distribution/CMakeLists.txt").read_text(
        encoding="utf-8"
    )
    distribution_analysis = (warpx / "Examples/Tests/initial_distribution/analysis.py").read_text(
        encoding="utf-8"
    )
    field_input = (
        warpx / "Examples/Tests/space_charge_initialization/inputs_test_2d_space_charge_initialization"
    ).read_text(encoding="utf-8")
    field_cmake = (warpx / "Examples/Tests/space_charge_initialization/CMakeLists.txt").read_text(
        encoding="utf-8"
    )
    field_analysis = (warpx / "Examples/Tests/space_charge_initialization/analysis.py").read_text(
        encoding="utf-8"
    )
    init_source = (warpx / "Source/Initialization/WarpXInitData.cpp").read_text(encoding="utf-8")
    parameters = (warpx / "Docs/source/usage/parameters.rst").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing_markers(
            chapter,
            [
                "### 3A.13.1 初始化验证卡：分布统计和初始自场是两份合同",
                "合同 A：粒子分布。",
                "合同 B：初始自场。",
                "producer -> observable -> consumer 链",
                "它把比较对象限定为初始化完成后、尚未由时间推进改变的粒子统计",
                "不能合并成“初始化失败”",
            ],
        ),
        "distribution_producer_and_consumer": missing_markers(
            distribution_input,
            [
                "max_step             = 0",
                "warpx.reduced_diags_names",
                "h1x.type                                 = ParticleHistogram",
                "h4x.type                                 = ParticleHistogram",
                "bmmntr.type",
            ],
        )
        + missing_markers(
            distribution_cmake,
            ["test_3d_initial_distribution", '"analysis.py"'],
        )
        + missing_markers(
            distribution_analysis,
            [
                "This script tests initial distributions.",
                'read_reduced_diags_histogram("h1x.txt")',
                "assert f1_error < tolerance",
                "assert f4_error < tolerance",
                "assert charge_error < tolerance",
            ],
        ),
        "self_field_producer_and_consumer": missing_markers(
            field_input,
            [
                "max_step = 1",
                'beam.injection_style = "gaussian_beam"',
                "beam.initialize_self_fields = 1",
                'beam.momentum_distribution_type = "at_rest"',
                "diag1.diag_type = Full",
                "diag1.fields_to_plot = Ex Ey Ez jx jy jz",
            ],
        )
        + missing_markers(
            field_cmake,
            [
                "test_2d_space_charge_initialization",
                "test_3d_space_charge_initialization",
                '"analysis.py diags/diag1000001"',
            ],
        )
        + missing_markers(
            field_analysis,
            [
                "This script checks the space-charge initialization routine",
                "Ex_th =",
                "Ey_th =",
                "tolerance_rel = 0.165",
                "check(Ex_array, Ex_th, \"Ex\")",
                "check(Ey_array, Ey_th, \"Ey\")",
            ],
        ),
        "initialization_source_contract": missing_markers(
            init_source,
            [
                "bool has_initialize_self_fields = false;",
                "has_initialize_self_fields |= species->initialize_self_fields;",
                "has_initialize_self_fields ||",
                "ComputeSpaceChargeField(reset_E_field, reset_B_field);",
            ],
        )
        + missing_markers(
            parameters,
            [
                "Whether to calculate the space-charge fields associated with this species",
                "at the beginning of the simulation.",
            ],
        ),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_INITIALIZATION_TWO_CONTRACT_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Source/Initialization/WarpXInitData.cpp",
            "Docs/source/usage/parameters.rst",
            "Examples/Tests/initial_distribution/inputs_test_3d_initial_distribution",
            "Examples/Tests/initial_distribution/CMakeLists.txt",
            "Examples/Tests/initial_distribution/analysis.py",
            "Examples/Tests/space_charge_initialization/inputs_test_2d_space_charge_initialization",
            "Examples/Tests/space_charge_initialization/CMakeLists.txt",
            "Examples/Tests/space_charge_initialization/analysis.py",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The reader card separates zero-step particle-distribution statistics from initial self-field validation.",
            "It does not establish relativistic, open-boundary, embedded-boundary, pusher, or cross-layout correctness.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 3A Initialization Reader Card",
        "",
        "Classification: `SOURCE_GROUNDED_INITIALIZATION_TWO_CONTRACT_READER_CARD`.",
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
