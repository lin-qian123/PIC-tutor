#!/usr/bin/env python
"""Preview the exact diff needed to stage the RZ JRhom first-stage patch."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE_DIR = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "rz_jrhom_first_stage_bundle"
)
HELPER_REL = Path(
    "warpx/Examples/Tests/nci_psatd_stability/analysis_rz_jrhom.py"
)
CMAKE_REL = Path("Examples/Tests/nci_psatd_stability/CMakeLists.txt")
TEST_MARKER = "test_rz_psatd_JRhom_LL2  # name"
OLD_ANALYSIS_LINE = "        OFF  # analysis"
NEW_ANALYSIS_LINE = '        "analysis_rz_jrhom.py diags/diag1000025"  # analysis'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a unified diff preview for staging the RZ JRhom first-stage patch."
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
        help="Path to the generated RZ JRhom first-stage bundle.",
    )
    return parser.parse_args()


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def rewrite_cmake(text: str) -> str:
    if TEST_MARKER not in text:
        raise ValueError(f"missing test marker {TEST_MARKER!r}")

    lines = text.splitlines()
    in_target_block = False
    replaced = False

    for index, line in enumerate(lines):
        if TEST_MARKER in line:
            in_target_block = True
            continue
        if in_target_block and line.strip() == ")":
            break
        if in_target_block and line == NEW_ANALYSIS_LINE:
            replaced = True
            break
        if in_target_block and line == OLD_ANALYSIS_LINE:
            lines[index] = NEW_ANALYSIS_LINE
            replaced = True
            break

    if not replaced:
        raise ValueError(
            "did not find the expected analysis line for test_rz_psatd_JRhom_LL2"
        )

    return "\n".join(lines) + "\n"


def unified_diff(path_from: str, old: str, path_to: str, new: str) -> str:
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=path_from,
            tofile=path_to,
            n=3,
        )
    )


def main() -> None:
    args = parse_args()
    warpx_root = args.warpx_root.resolve()
    bundle_dir = args.bundle_dir.resolve()

    helper_expected = load_text(bundle_dir / HELPER_REL)
    helper_actual_path = warpx_root / HELPER_REL.relative_to("warpx")
    cmake_path = warpx_root / CMAKE_REL

    cmake_actual = load_text(cmake_path)
    cmake_target = rewrite_cmake(cmake_actual)

    helper_actual = ""
    helper_from = "/dev/null"
    if helper_actual_path.exists():
        helper_actual = helper_actual_path.read_text(encoding="utf-8")
        helper_from = str(helper_actual_path.relative_to(warpx_root))

    cmake_diff = unified_diff(
        str(CMAKE_REL),
        cmake_actual,
        str(CMAKE_REL),
        cmake_target,
    )
    helper_diff = unified_diff(
        helper_from,
        helper_actual,
        str(HELPER_REL.relative_to("warpx")),
        helper_expected,
    )

    if not cmake_diff and not helper_diff:
        print("target checkout already matches the current bundle")
        return

    if cmake_diff:
        print(cmake_diff, end="")
    if helper_diff:
        print(helper_diff, end="")


if __name__ == "__main__":
    main()
