#!/usr/bin/env python
"""Audit Chapter 7's reader-facing load-balance validation card."""

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
    chapter = (ROOT / "manuscript/chapters/07-boundaries-amr.md").read_text(encoding="utf-8")
    reduced_diags = warpx / "Examples/Tests/reduced_diags"
    cmake = (reduced_diags / "CMakeLists.txt").read_text(encoding="utf-8")
    inputs = (reduced_diags / "inputs_base_3d").read_text(encoding="utf-8")
    heuristic = (
        reduced_diags / "inputs_test_3d_reduced_diags_load_balance_costs_heuristic"
    ).read_text(encoding="utf-8")
    timers = (
        reduced_diags / "inputs_test_3d_reduced_diags_load_balance_costs_timers"
    ).read_text(encoding="utf-8")
    analysis = (reduced_diags / "analysis_reduced_diags_load_balance_costs.py").read_text(
        encoding="utf-8"
    )
    regrid = (warpx / "Source/Parallelization/WarpXRegrid.cpp").read_text(encoding="utf-8")
    parameters = (warpx / "Docs/source/usage/parameters.rst").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing(
            chapter,
            [
                "### 7.8.1 修改 load balance 或 `RemakeLevel()` 后的验证卡：效率、迁移与物理量分开检查",
                "第一层：先确认 producer 有足够的 boxes、实际生成成本记录",
                "第二层：用正确的 consumer 判断映射效率",
                "第三层：把“提议”与“真正迁移的状态”分开",
                "第四层：按改动对象补上状态或物理 consumer",
                "不能写成“load balance 后的物理结果已经验证”",
            ],
        ),
        "official_load_balance_producer": missing(
            cmake,
            [
                "test_3d_reduced_diags_load_balance_costs_heuristic",
                "test_3d_reduced_diags_load_balance_costs_timers",
                "3  # dims",
                "2  # nprocs",
                '"analysis_reduced_diags_load_balance_costs.py diags/diag1000003"',
                '"analysis_default_regression.py --path diags/diag1000003"',
            ],
        )
        + missing(
            inputs,
            [
                "max_step = 3",
                "amr.n_cell =   128 32 128",
                "amr.max_grid_size = 32",
                "amr.max_level = 0",
                "algo.load_balance_intervals = 2",
                "warpx.reduced_diags_names = LBC",
                "LBC.type = LoadBalanceCosts",
                "LBC.intervals = 1",
            ],
        )
        + missing(heuristic, ["algo.load_balance_costs_update = Heuristic"])
        + missing(timers, ["algo.load_balance_costs_update = Timers"]),
        "efficiency_consumer": missing(
            analysis,
            [
                "data = np.genfromtxt(\"./diags/reducedfiles/LBC.txt\")",
                "rank_to_cost_map[r] += c",
                "efficiencies /= efficiencies.max()",
                "efficiency_before, efficiency_after = get_efficiency(1), get_efficiency(2)",
                "assert efficiency_before < efficiency_after",
            ],
        )
        + missing(
            parameters,
            [
                "is unchanged, but its owner is changed in order to have better performance.",
                "LoadBalanceCosts",
                "Until costs are recorded, load balance efficiency is output as ``-1``",
            ],
        ),
        "migration_scope": missing(
            regrid,
            [
                "WarpX::CheckLoadBalance (int step)",
                "load_balance_intervals.contains(step+1)",
                "proposedEfficiency > load_balance_efficiency_ratio_threshold*currentEfficiency",
                "RemakeLevel(lev, t_new[lev], boxArray(lev), newdm)",
                "if (ba == boxArray(lev))",
                "RemakeLevel: to be implemented",
                "m_fields.remake_level(lev, dm)",
                "BuildBufferMasks();",
                "multi_diags->InitializeFieldFunctors( lev );",
                "mypc->Redistribute();",
                "m_particle_boundary_buffer->redistribute();",
                "reduced_diags->LoadBalance();",
            ],
        ),
    }
    passed = all(not absent for absent in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_LOAD_BALANCE_VALIDATION_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Docs/source/usage/{parameters.rst,workflows/plot_distribution_mapping.rst}",
            "Examples/Tests/reduced_diags/{CMakeLists.txt,inputs_base_3d,inputs_test_3d_reduced_diags_load_balance_costs_{heuristic,timers},analysis_reduced_diags_load_balance_costs.py}",
            "Source/Parallelization/WarpXRegrid.cpp",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The card separates cost-distribution efficiency from state migration and physical validation.",
            "It does not establish AMR topology regridding, transition-zone route counts, physics accuracy, or wall-clock speedup for arbitrary inputs.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 7 Load-Balance Validation Card",
        "",
        "Classification: `SOURCE_GROUNDED_LOAD_BALANCE_VALIDATION_READER_CARD`.",
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
