#!/usr/bin/env python
"""Audit the explicit WarpX source guard that rejects Vay with mesh refinement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.warpx_root.resolve()
    project = args.project_root.resolve()
    warpx = read(root / "Source/WarpX.cpp")
    kernel = read(root / "Source/Particles/Deposition/CurrentDeposition.H")
    chapter = read(project / "manuscript/chapters/05-deposition-shapes.md")
    note = read(project / "notes/code-reading/particles/72-deposition-geometry-order-gap-register.md")
    guard = "WarpX::current_deposition_algo != CurrentDepositionAlgo::Vay ||\n            maxLevel() <= 0"
    checks = {
        "source_mesh_refinement_guard": guard in warpx,
        "source_guard_message": "Vay deposition not implemented with mesh refinement" in warpx,
        "source_vay_psatd_guard": "Vay deposition is implemented only for PSATD" in warpx,
        "source_vay_rz_guard": "Vay deposition not implemented in RZ geometry" in kernel,
        "source_vay_1d_guard": "Vay deposition not implemented in 1D geometry" in kernel,
        "chapter_amr_boundary": "AMR、边界裁剪" in chapter and "正式收敛阶" in chapter,
        "gap_register_amr_boundary": "AMR 当前由 source guard" in note,
        "no_amr_runtime_pass_claim": "Vay AMR runtime PASS" not in chapter and "Vay AMR runtime PASS" not in note,
    }
    result = {
        "contract": "Vay deposition mesh-refinement source guard",
        "classification": "SOURCE_GUARD_AMR_RUNTIME_INTENTIONALLY_REJECTED",
        "scope": "read-only WarpX initialization/source guards; no AMR producer is interpreted as a physics runtime failure or pass",
        "checks": checks,
        "passed": all(checks.values()),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Vay deposition mesh-refinement source guard",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The current checkout rejects Vay when `maxLevel() > 0` during initialization. This is a source-defined support boundary, not a failed AMR physics experiment.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {sum(checks.values())}/{len(checks)} Vay AMR guard checks")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
