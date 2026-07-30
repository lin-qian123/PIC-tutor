#!/usr/bin/env python
"""Audit Chapter 3's source-grounded input-to-consumer lifecycle trace."""

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
    chapter = (ROOT / "manuscript/chapters/03-warpx-evolve.md").read_text(encoding="utf-8")
    warpx_cpp = (warpx / "Source/WarpX.cpp").read_text(encoding="utf-8")
    main_cpp = (warpx / "Source/main.cpp").read_text(encoding="utf-8")
    init_cpp = (warpx / "Source/Initialization/WarpXInitData.cpp").read_text(encoding="utf-8")
    evolve_cpp = (warpx / "Source/Evolve/WarpXEvolve.cpp").read_text(encoding="utf-8")
    input_file = (warpx / "Examples/Tests/langmuir/inputs_test_1d_langmuir_multi").read_text(
        encoding="utf-8"
    )
    cmake = (warpx / "Examples/Tests/langmuir/CMakeLists.txt").read_text(encoding="utf-8")
    analysis = (warpx / "Examples/Tests/langmuir/analysis_1d.py").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing_markers(
            chapter,
            [
                "### 3.12.1 生命周期追踪卡：一项输入何时成为可解释的证据",
                "参数被读取。",
                "初始化已经越过记录点。",
                "参数实际限制外层循环。",
                "consumer 给出可支持的结论。",
                "`warpx_used_inputs` 出现能证明",
                "不能证明 `Evolve()` 已执行一步",
                "不能统一归因成“参数无效”或“Langmuir 物理失败”",
            ],
        ),
        "main_and_parameter_contract": missing_markers(
            main_cpp,
            ["WarpX::GetInstance()", "warpx.InitData()", "warpx.Evolve()"],
        )
        + missing_markers(
            warpx_cpp,
            ["WarpX::WarpX ()", "ReadParameters();", 'queryWithParser(pp, "max_step", max_step)'],
        ),
        "initialization_evidence_contract": missing_markers(
            init_cpp,
            [
                "if (restart_chkfile.empty())",
                "ComputeDt();",
                "InitFromScratch();",
                "InitDiagnostics();",
                "::WriteUsedInputsFile();",
                'std::string filename = "warpx_used_inputs"',
            ],
        ),
        "evolve_and_diagnostic_contract": missing_markers(
            evolve_cpp,
            [
                "const int numsteps_max = (numsteps < 0)?(max_step):(istep[0] + numsteps);",
                "bool const final_time_step = (istep[0] == max_step)",
                "FilterComputePackFlushLastTimestep",
            ],
        )
        + missing_markers(
            input_file,
            ["max_step = 80", "diag1.intervals = 40", "diag1.diag_type = Full"],
        ),
        "consumer_contract": missing_markers(
            cmake,
            [
                "test_1d_langmuir_multi",
                "1  # dims",
                "2  # nprocs",
                '"analysis_1d.py diags/diag1000080"',
            ],
        )
        + missing_markers(
            analysis,
            [
                "fn = sys.argv[1]",
                "t0 = ds.current_time.to_value()",
                "tolerance_rel = 0.05",
                "check_charge_conservation(data)",
            ],
        ),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_LIFECYCLE_TRACE_READER_CONTRACT",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Source/main.cpp",
            "Source/WarpX.cpp",
            "Source/Initialization/WarpXInitData.cpp",
            "Source/Evolve/WarpXEvolve.cpp",
            "Examples/Tests/langmuir/inputs_test_1d_langmuir_multi",
            "Examples/Tests/langmuir/CMakeLists.txt",
            "Examples/Tests/langmuir/analysis_1d.py",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The lifecycle trace distinguishes parameter ingestion, initialization evidence, diagnostic production, and the registered consumer.",
            "It does not establish physics validity outside the registered Langmuir input, two-rank layout, and analysis contract.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 3 Lifecycle Trace Reader Card",
        "",
        "Classification: `SOURCE_GROUNDED_LIFECYCLE_TRACE_READER_CONTRACT`.",
        "",
        f"Result: {'PASS' if passed else 'FAIL'}.",
        "",
        "## Source Routes",
        "",
    ]
    lines.extend(f"- `{route}`" for route in payload["source_routes"])
    lines.extend(["", "## Checks", ""])
    for name, missing in checks.items():
        lines.append(f"- `{name}`: {'PASS' if not missing else 'FAIL'}")
        lines.extend(f"  - missing `{marker}`" for marker in missing)
    lines.extend(["", "## Scope", ""])
    lines.extend(f"- {item}" for item in payload["scope"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
