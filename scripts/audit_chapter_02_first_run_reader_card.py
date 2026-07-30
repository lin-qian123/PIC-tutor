#!/usr/bin/env python
"""Audit Chapter 2's source-grounded first-run reader route."""

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
    chapter = (ROOT / "manuscript/chapters/02-pic-loop.md").read_text(encoding="utf-8")
    install = (warpx / "Docs/source/install/cmake.rst").read_text(encoding="utf-8")
    run_doc = (warpx / "Docs/source/usage/how_to_run.rst").read_text(encoding="utf-8")
    top_cmake = (warpx / "CMakeLists.txt").read_text(encoding="utf-8")
    functions = (warpx / "cmake/WarpXFunctions.cmake").read_text(encoding="utf-8")
    langmuir_cmake = (warpx / "Examples/Tests/langmuir/CMakeLists.txt").read_text(
        encoding="utf-8"
    )

    checks = {
        "reader_route": missing_markers(
            chapter,
            [
                "### 2.8.1 第一次运行的读者路线：构建、CTest 与手动分析各自回答什么",
                "-DWarpX_DIMS=1",
                "ctest --test-dir",
                "test_1d_langmuir_multi",
                '"$WARPX_BUILD/bin/warpx.1d"',
                "warpx_used_inputs",
                "程序退出为零",
            ],
        ),
        "build_contract": missing_markers(
            install,
            [
                "cmake -S . -B build",
                "cmake --build build -j 4",
                "WarpX_DIMS",
                "separate binaries",
            ],
        )
        + missing_markers(
            top_cmake,
            [
                "set(WarpX_DIMS_VALUES 1 2 3 RZ RCYLINDER RSPHERE)",
                'option(WarpX_APP',
                "include(CTest)",
                "if(BUILD_TESTING)",
            ],
        )
        + missing_markers(functions, ["warpx.${SD}", "create_symlink"]),
        "run_contract": missing_markers(
            run_doc,
            [
                "mpirun -np <n_ranks> ./warpx <input_file>",
                "warpx_used_inputs",
                "diags/",
            ],
        ),
        "langmuir_ctest_contract": missing_markers(
            langmuir_cmake,
            [
                "test_1d_langmuir_multi",
                "1  # dims",
                "2  # nprocs",
                "inputs_test_1d_langmuir_multi",
                '"analysis_1d.py diags/diag1000080"',
            ],
        ),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_FIRST_RUN_READER_CONTRACT",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Docs/source/install/cmake.rst",
            "Docs/source/usage/how_to_run.rst",
            "CMakeLists.txt",
            "cmake/WarpXFunctions.cmake",
            "Examples/Tests/langmuir/CMakeLists.txt",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "CTest registration does not establish physics validity beyond the registered input and consumer contract.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 2 First-Run Reader Card",
        "",
        "Classification: `SOURCE_GROUNDED_FIRST_RUN_READER_CONTRACT`.",
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
