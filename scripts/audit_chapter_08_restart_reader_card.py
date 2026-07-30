#!/usr/bin/env python
"""Audit the source-grounded reader contract for Chapter 8 restart coverage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_markers(text: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    warpx = args.warpx_root.resolve()
    chapter = (ROOT / "manuscript/chapters/08-diagnostics-cases.md").read_text(encoding="utf-8")
    cmake = (warpx / "Examples/Physics_applications/uniform_plasma/CMakeLists.txt").read_text(encoding="utf-8")
    inputs_base = (warpx / "Examples/Physics_applications/uniform_plasma/inputs_base_3d").read_text(encoding="utf-8")
    inputs_restart = (warpx / "Examples/Physics_applications/uniform_plasma/inputs_test_3d_uniform_plasma_restart").read_text(encoding="utf-8")
    consumer = (warpx / "Examples/analysis_default_restart.py").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": require_markers(chapter, [
            "### Checkpoint/restart 的读者合同：续跑一致性与跨布局比较不是同一问题",
            "同一 CTest 布局下", "epsilon_f", "不能从 `epsilon_f < 1e-12` 自动推出",
            "checksum 能发现指定输出相对基线是否改变",
        ]),
        "restart_ctest_contract": require_markers(cmake, [
            "test_3d_uniform_plasma", "test_3d_uniform_plasma_restart",
            "inputs_test_3d_uniform_plasma_restart",
            '"analysis_default_restart.py diags/diag1000010"',
            '"analysis_default_regression.py --path diags/diag1000010 --rtol 1e-12"',
            "test_3d_uniform_plasma  # dependency",
        ]),
        "checkpoint_input_contract": require_markers(inputs_base, [
            "chk.intervals = 6", "chk.diag_type = Full", "chk.format = checkpoint",
            "diag1.diag_type = Full", "diag1.fields_to_plot = Bx By Bz Ex Ey Ez jx jy jz rho",
        ]) + require_markers(inputs_restart, [
            "FILE = inputs_test_3d_uniform_plasma",
            'amr.restart = "../test_3d_uniform_plasma/diags/chk000006"',
        ]),
        "consumer_contract": require_markers(consumer, [
            "tolerance=1e-12", 'os.getcwd().replace("_restart", "")',
            "ds_benchmark.field_list", "covering_grid(",
            "np.amax(np.abs(db)) != 0.0", "assert error < tolerance",
        ]),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_RESTART_READER_CONTRACT",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Examples/Physics_applications/uniform_plasma/CMakeLists.txt",
            "Examples/Physics_applications/uniform_plasma/inputs_base_3d",
            "Examples/Physics_applications/uniform_plasma/inputs_test_3d_uniform_plasma_restart",
            "Examples/analysis_default_restart.py",
        ],
        "scope": [
            "No WarpX run is performed by this audit.",
            "The contract does not establish cross-layout equivalence or thermal-plasma physics closure.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 8 Restart Reader Card", "",
        "Classification: `SOURCE_GROUNDED_RESTART_READER_CONTRACT`.", "",
        f"Result: {'PASS' if passed else 'FAIL'}.", "", "## Source Routes", "",
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
