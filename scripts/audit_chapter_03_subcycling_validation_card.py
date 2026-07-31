#!/usr/bin/env python
"""Audit Chapter 3's reader-facing AMR subcycling validation card."""

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
    chapter = (ROOT / "manuscript/chapters/03-warpx-evolve.md").read_text(encoding="utf-8")
    cmake = (warpx / "Examples/Tests/subcycling/CMakeLists.txt").read_text(encoding="utf-8")
    inputs = (warpx / "Examples/Tests/subcycling/inputs_test_2d_subcycling_mr").read_text(encoding="utf-8")
    evolve = (warpx / "Source/Evolve/WarpXEvolve.cpp").read_text(encoding="utf-8")
    fields = (warpx / "Source/Fields.H").read_text(encoding="utf-8")
    regression = (warpx / "Examples/analysis_default_regression.py").read_text(encoding="utf-8")
    developer_docs = (warpx / "Docs/source/developers/repo_organization.rst").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing(
            chapter,
            [
                "### 3.11.3 AMR subcycling 修改后的验证卡：先分清时间层、source 和回归",
                "第一层：先确认这真的是受支持的两级分支",
                "第二层：把一个 coarse 步按 source 生命周期阅读",
                "第三层：正确解读官方测试的 consumer",
                "第四层：按改动对象补上缺失的比较",
                "不能写成“AMR subcycling 的物理正确性已经验证”",
            ],
        ),
        "official_test_contract": missing(
            cmake,
            [
                "test_2d_subcycling_mr",
                "2  # dims",
                "2  # nprocs",
                "OFF  # analysis",
                '"analysis_default_regression.py --path diags/diag1000250"',
            ],
        )
        + missing(
            inputs,
            [
                "max_step = 250",
                "amr.max_level = 1",
                "warpx.do_subcycling = 1",
                "algo.maxwell_solver = \"ckc\"",
                "warpx.do_moving_window = 1",
                "diag1.intervals = 250",
                "diag1.diag_type = Full",
            ],
        ),
        "two_level_source_lifecycle": missing(
            evolve,
            [
                "WarpX::OneStep_sub1",
                "Electrostatic solver cannot be used with sub-cycling.",
                "MR with subcycling algorithm requires exactly two levels of MR",
                "PushParticlesandDeposit(fine_lev, cur_time, SubcyclingHalf::FirstHalf)",
                "RestrictCurrentFromFineToCoarsePatch(",
                "::StoreCurrent(coarse_lev, m_fields)",
                "UpdateAuxiliaryData();",
                "PushParticlesandDeposit(fine_lev, cur_time + dt[fine_lev], SubcyclingHalf::SecondHalf)",
                "::RestoreCurrent(coarse_lev, m_fields)",
                "AddCurrentFromFineLevelandSumBoundary(",
            ],
        )
        + missing(
            fields,
            [
                "Efield_aux, /**< Field that the particles gather from. Obtained from Efield_fp",
                "Bfield_aux, /**< Field that the particles gather from. Obtained from Bfield_fp",
            ],
        ),
        "checksum_scope": missing(
            regression,
            ["def main(args):", "evaluate_checksum(", "test_name=test_name", "output_file=args.path"],
        )
        + missing(
            developer_docs,
            ["WarpX::OneStep_nosub", "WarpX::OneStep_sub1", "when subcycling is ON"],
        ),
    }
    passed = all(not item for item in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_AMR_SUBCYCLING_VALIDATION_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Docs/source/developers/repo_organization.rst",
            "Examples/Tests/subcycling/{CMakeLists.txt,inputs_test_2d_subcycling_mr}",
            "Examples/analysis_default_regression.py",
            "Source/{Evolve/WarpXEvolve.cpp,Fields.H}",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The official test's checksum contract is kept distinct from source-lifecycle or physical validation.",
            "The card does not establish transition-zone route counts, conservation, or AMR physical accuracy.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 3 AMR Subcycling Validation Card",
        "",
        "Classification: `SOURCE_GROUNDED_AMR_SUBCYCLING_VALIDATION_READER_CARD`.",
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
