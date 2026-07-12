#!/usr/bin/env python
"""Stage the generated RZ JRhom first-stage bundle into a target WarpX checkout."""

from __future__ import annotations

import argparse
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
        description="Copy the first-stage RZ JRhom helper into a WarpX tree and update CMake wiring."
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report planned changes without writing files.",
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


def ensure_parent(path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()
    warpx_root = args.warpx_root.resolve()
    bundle_dir = args.bundle_dir.resolve()

    helper_src = bundle_dir / HELPER_REL
    helper_dst = warpx_root / HELPER_REL.relative_to("warpx")
    cmake_path = warpx_root / CMAKE_REL

    helper_text = load_text(helper_src)
    cmake_text = load_text(cmake_path)
    rewritten_cmake = rewrite_cmake(cmake_text)

    if args.dry_run:
        print(f"would copy {helper_src} -> {helper_dst}")
        if cmake_text == rewritten_cmake:
            print(f"would keep {cmake_path} unchanged")
        else:
            print(f"would rewrite {cmake_path}")
        return

    ensure_parent(helper_dst, dry_run=False)
    helper_dst.write_text(helper_text, encoding="utf-8")
    cmake_path.write_text(rewritten_cmake, encoding="utf-8")

    print(f"wrote {helper_dst}")
    print(f"updated {cmake_path}")


if __name__ == "__main__":
    main()
