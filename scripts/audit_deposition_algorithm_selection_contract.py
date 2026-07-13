#!/usr/bin/env python
"""Audit the chapter-5 deposition algorithm selection matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--warpx-root", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    warpx_root = (args.warpx_root or root.parent / "warpx").resolve()
    chapter = (root / "manuscript/chapters/05-deposition-shapes.md").read_text(encoding="utf-8")
    dispatch = (warpx_root / "Source/Particles/WarpXParticleContainer.cpp").read_text(encoding="utf-8")
    current = (warpx_root / "Source/Particles/Deposition/CurrentDeposition.H").read_text(encoding="utf-8")
    warpx = (warpx_root / "Source/WarpX.cpp").read_text(encoding="utf-8")

    checks = {
        "chapter_matrix_heading": "### 5.14.3 v0.75 沉积算法选择矩阵" in chapter,
        "chapter_selection_order": all(
            marker in chapter
            for marker in (
                "geometry/grid 约束",
                "explicit/implicit 时间层",
                "source-side 守恒机制",
                "当前可引用证据",
            )
        ),
        "chapter_algorithm_rows": all(
            marker in chapter for marker in ("Direct", "Esirkepov", "Villasenor", "Vay")
        ),
        "dispatch_families": all(
            marker in dispatch
            for marker in (
                "CurrentDepositionAlgo::Esirkepov",
                "CurrentDepositionAlgo::Villasenor",
                "CurrentDepositionAlgo::Vay",
                "doDepositionShapeN",
            )
        ),
        "kernel_families": all(
            marker in current
            for marker in (
                "doEsirkepovDepositionShapeN",
                "doVillasenorDepositionShapeNExplicit",
                "doVayDepositionShapeN",
            )
        ),
        "explicit_guards": all(
            marker in warpx
            for marker in (
                "Vay deposition not implemented with mesh refinement",
                "Vay deposition is implemented only for PSATD",
            )
        ),
        "negative_boundaries": all(
            marker in chapter
            for marker in (
                "不把 Direct 自动变成 Esirkepov 或 Villasenor",
                "任何单一 Langmuir PASS 都不能外推",
                "SOURCE_AND_RUNTIME_SELECTION_MATRIX_WITH_EXPLICIT_BOUNDARIES",
            )
        ),
        "runtime_contracts_present": all(
            (root / "runs/stage-c-validation" / name / "contract.json").exists()
            for name in (
                "esirkepov_langmuir_3d_shape-matrix",
                "villasenor-1992-paper-asset",
                "vay-runtime",
            )
        ),
    }
    result = {
        "contract": "chapter-5 deposition algorithm selection matrix",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "SOURCE_AND_RUNTIME_SELECTION_MATRIX_WITH_EXPLICIT_BOUNDARIES",
        "scope": "read-only chapter/source/runtime linkage; not equal physics coverage across algorithms",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Deposition algorithm selection contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
