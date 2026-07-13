#!/usr/bin/env python
"""Audit the chapter-5 deposition paper/source/runtime evidence gradient."""

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
    warpx = (args.warpx_root or root.parent / "warpx").resolve()
    chapter = (root / "manuscript/chapters/05-deposition-shapes.md").read_text(encoding="utf-8")
    source = (warpx / "Source/Particles/WarpXParticleContainer.cpp").read_text(encoding="utf-8")
    current = (warpx / "Source/Particles/Deposition/CurrentDeposition.H").read_text(encoding="utf-8")
    contracts = (
        "esirkepov-density-decomposition/contract.json",
        "esirkepov-paper-source-runtime-crosswalk/contract.json",
        "villasenor_formula_contract/contract.json",
        "villasenor-source-contract/contract.json",
        "implicit_villasenor_2d_jfnk_mpi2/contract.json",
        "vay-runtime/contract.json",
    )
    checks = {
        "chapter_heading": "### 5.14.4 v0.78 沉积证据梯度" in chapter,
        "chapter_rows": all(marker in chapter for marker in (
            "| Direct |", "| Esirkepov |", "| Villasenor-Buneman |", "| Vay |",
            "论文或公式层", "WarpX 源码层", "runtime consumer",
        )),
        "chapter_boundaries": all(marker in chapter for marker in (
            "不能写成 CPC 定稿逐式已核对", "不能把 RZ pre-physics boundary",
            "不能把 case-local sibling 写成上游注册项",
            "DEPOSITION_PAPER_SOURCE_RUNTIME_GRADIENT_WITH_EXPLICIT_GAPS",
        )),
        "source_dispatch": "DepositCurrent" in source,
        "source_families": all(marker in current for marker in (
            "doDepositionShapeNKernel", "doEsirkepovDepositionShapeN",
            "VillasenorDepositionShapeNKernel", "doVayDepositionShapeN",
        )),
        "source_esirkepov_markers": all(marker in current for marker in (
            "one_third", "one_sixth", "sdxi", "sdyj", "sdzk",
        )),
        "source_villasenor_markers": all(marker in current for marker in (
            "cell_crossings", "num_segments", "seg_factor_x", "this_Jx",
        )),
        "runtime_contracts_present": all((root / "runs/stage-c-validation" / name).is_file() for name in contracts),
    }
    result = {
        "contract": "chapter-5 deposition paper/source/runtime evidence gradient",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "DEPOSITION_PAPER_SOURCE_RUNTIME_GRADIENT_WITH_EXPLICIT_GAPS",
        "scope": "read-only chapter/source/runtime linkage; not complete deposition physics coverage",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Deposition evidence gradient contract", "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}", "", "| check | status |", "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
