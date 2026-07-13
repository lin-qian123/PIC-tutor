#!/usr/bin/env python
"""Audit the current WarpX Yee/FDTD source crosswalk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def has(text: str, *terms: str) -> bool:
    return all(term in text for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--chapters", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.warpx_root.resolve()
    paths = {
        "yee_algorithm": root / "Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceAlgorithms/CartesianYeeAlgorithm.H",
        "solver_dispatch": root / "Source/FieldSolver/FiniteDifferenceSolver/FiniteDifferenceSolver.cpp",
        "b_update": root / "Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp",
        "e_update": root / "Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp",
    }
    text = {name: path.read_text(encoding="utf-8") if path.is_file() else "" for name, path in paths.items()}
    chapters = "\n".join(path.resolve().read_text(encoding="utf-8") for path in args.chapters)
    checks = {
        "cartesian_yee_algorithm_present": paths["yee_algorithm"].is_file(),
        "yee_stencil_coefficients_and_cfl": has(text["yee_algorithm"], "InitializeStencilCoefficients", "ComputeMaxDt", "GetMaxGuardCell"),
        "staggered_forward_backward_derivatives": has(text["yee_algorithm"], "UpwardDx", "DownwardDx", "F(i+1,j,k,ncomp) - F(i,j,k,ncomp)", "F(i,j,k,ncomp) - F(i-1,j,k,ncomp)"),
        "solver_selects_yee": has(text["solver_dispatch"], "fdtd_algo == ElectromagneticSolverAlgo::Yee", "CartesianYeeAlgorithm::InitializeStencilCoefficients"),
        "b_update_selects_yee": has(text["b_update"], "EvolveBCartesian <CartesianYeeAlgorithm>", "EvolveBCylindrical <CylindricalYeeAlgorithm>"),
        "e_update_selects_yee": has(text["e_update"], "EvolveECartesian <CartesianYeeAlgorithm>", "EvolveECylindrical <CylindricalYeeAlgorithm>"),
        "chapter_maps_indexed_abstract_boundary": has(chapters, "Yee 1966", "indexed-abstract", "IEEE 原文 PDF/MinerU 仍未取得"),
        "chapter_maps_source_paths": has(chapters, "CartesianYeeAlgorithm.H", "EvolveB.cpp", "EvolveE.cpp"),
        "chapter_preserves_non_equivalence": has(chapters, "不能把当前 WarpX 的完整 Yee stencil 写成已逐式来自 Yee 原文"),
    }
    result = {
        "contract": "WarpX Yee/FDTD source crosswalk",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "CURRENT_WARPX_SOURCE_GROUNDED_YEE_CROSSWALK_INDEXED_ABSTRACT_HISTORICAL_FULL_TEXT_MISSING",
        "scope": "read-only current FDTD source mapping; not a line-by-line reconstruction of the 1966 IEEE paper",
        "source_files": [str(path.relative_to(root)) for path in paths.values()],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Yee source crosswalk contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", "The crosswalk keeps the current WarpX implementation separate from the unavailable IEEE full text."]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
