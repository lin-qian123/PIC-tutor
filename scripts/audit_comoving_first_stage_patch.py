#!/usr/bin/env python
"""Audit whether a WarpX checkout has the comoving first-stage patch staged."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE_DIR = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_bundle"
)
HELPER_REL = Path(
    "warpx/Examples/Tests/nci_psatd_stability/analysis_comoving.py"
)
CMAKE_REL = Path("Examples/Tests/nci_psatd_stability/CMakeLists.txt")
TEST_MARKER = "test_2d_comoving_psatd_hybrid  # name"
OLD_ANALYSIS_LINE = "        OFF  # analysis"
NEW_ANALYSIS_LINE = '        "analysis_comoving.py diags/diag1000400"  # analysis'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report whether a WarpX checkout already has the comoving first-stage patch staged."
    )
    parser.add_argument(
        "--warpx-root",
        type=Path,
        required=True,
        help="Path to the target WarpX repository root.",
    )
    parser.add_argument(
        "--bundle-dir",
        type=Path,
        default=DEFAULT_BUNDLE_DIR,
        help="Path to the generated comoving first-stage bundle.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of plain text.",
    )
    return parser.parse_args()


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def inspect_cmake(text: str) -> dict[str, str]:
    if TEST_MARKER not in text:
        return {
            "status": "missing-test-block",
            "line": "",
            "detail": f"missing marker {TEST_MARKER!r}",
        }

    lines = text.splitlines()
    in_target_block = False

    for line in lines:
        if TEST_MARKER in line:
            in_target_block = True
            continue
        if in_target_block and line.strip() == ")":
            break
        if in_target_block and " # analysis" in line:
            if line == NEW_ANALYSIS_LINE:
                return {
                    "status": "staged",
                    "line": line,
                    "detail": "analysis line matches bundle expectation",
                }
            if line == OLD_ANALYSIS_LINE:
                return {
                    "status": "unstaged",
                    "line": line,
                    "detail": "analysis line is still OFF",
                }
            return {
                "status": "custom",
                "line": line,
                "detail": "analysis line differs from both OFF and bundle expectation",
            }

    return {
        "status": "missing-analysis-line",
        "line": "",
        "detail": "did not find analysis line inside target test block",
    }


def inspect_helper(expected_text: str, actual_path: Path) -> dict[str, str]:
    if not actual_path.exists():
        return {
            "status": "missing",
            "detail": "helper file is absent",
        }
    actual_text = actual_path.read_text(encoding="utf-8")
    if actual_text == expected_text:
        return {
            "status": "staged",
            "detail": "helper matches bundle",
        }
    return {
        "status": "different",
        "detail": "helper exists but differs from bundle",
    }


def derive_overall_status(helper_status: str, cmake_status: str) -> str:
    if helper_status == "staged" and cmake_status == "staged":
        return "staged"
    if helper_status in {"missing"} and cmake_status == "unstaged":
        return "unstaged"
    return "partial"


def main() -> None:
    args = parse_args()
    warpx_root = args.warpx_root.resolve()
    bundle_dir = args.bundle_dir.resolve()

    helper_expected_path = bundle_dir / HELPER_REL
    helper_actual_path = warpx_root / HELPER_REL.relative_to("warpx")
    cmake_path = warpx_root / CMAKE_REL

    helper_expected_text = load_text(helper_expected_path)
    cmake_text = load_text(cmake_path)

    helper = inspect_helper(helper_expected_text, helper_actual_path)
    cmake = inspect_cmake(cmake_text)
    overall = derive_overall_status(helper["status"], cmake["status"])

    report = {
        "warpx_root": str(warpx_root),
        "bundle_dir": str(bundle_dir),
        "overall_status": overall,
        "helper": {
            "path": str(helper_actual_path),
            "status": helper["status"],
            "detail": helper["detail"],
        },
        "cmake": {
            "path": str(cmake_path),
            "status": cmake["status"],
            "detail": cmake["detail"],
            "line": cmake["line"],
        },
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    print(f"overall_status: {overall}")
    print(f"helper_status: {helper['status']}")
    print(f"helper_detail: {helper['detail']}")
    print(f"cmake_status: {cmake['status']}")
    print(f"cmake_detail: {cmake['detail']}")
    if cmake["line"]:
        print(f"cmake_line: {cmake['line']}")


if __name__ == "__main__":
    main()
