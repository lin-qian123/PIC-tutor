#!/usr/bin/env python
"""Audit the chapter-7 PML evidence-gradient matrix and its boundaries."""

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
    chapter = (root / "manuscript/chapters/07-boundaries-amr.md").read_text(encoding="utf-8")
    source_files = {
        "pml": warpx / "Source/BoundaryConditions/PML.cpp",
        "psatd": warpx / "Source/FieldSolver/SpectralSolver/SpectralAlgorithms/PsatdAlgorithmPml.cpp",
        "current": warpx / "Source/BoundaryConditions/PML_current.H",
        "evolve": warpx / "Source/BoundaryConditions/WarpXEvolvePML.cpp",
    }
    sources = {name: path.read_text(encoding="utf-8") for name, path in source_files.items()}
    contracts = (
        "pml_psatd_2d_mpi2/contract.json",
        "pml_rz_psatd_mpi2/contract.json",
        "test_2d_pml_x_psatd_restart/restart-contract.json",
        "particles_in_pml_3d_mr_mpi2/signed-absolute-level-contract.json",
        "pml_psatd_3d_cleaning_contract_mpi2.json",
    )
    checks = {
        "chapter_matrix_heading": "### 7.5.10 v0.77 PML 证据梯度" in chapter,
        "chapter_evidence_rows": all(marker in chapter for marker in (
            "Cartesian FDTD Yee/CKC 反射", "Cartesian PSATD/Galilean 反射",
            "RZ PSATD 残余场", "重启重复性", "粒子入 PML：3D MR", "3D cleaning",
        )),
        "chapter_negative_boundaries": all(marker in chapter for marker in (
            "不能逐项证明 `C1-C25`", "不能把 RZ 结果外推为 Cartesian PML",
            "不能把重复性写成新的吸收精度", "不能隐藏负向 `Ex` 极值",
            "PML_EVIDENCE_GRADIENT_WITH_EXPLICIT_RUNTIME_BOUNDARIES",
        )),
        "source_contract": all(marker in sources["psatd"] for marker in ("C1", "C25", "T2")),
        "source_dispatch": all(marker in sources["pml"] for marker in ("PushPSATD", "PushPMLPSATDSinglePatch")),
        "source_current": "PML_current" in sources["current"] or "PML_current" in sources["evolve"],
        "source_damping": "DampPML" in sources["evolve"],
        "runtime_contracts_present": all((root / "runs/stage-c-validation" / name).exists() for name in contracts),
    }
    result = {
        "contract": "chapter-7 PML evidence gradient",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "PML_EVIDENCE_GRADIENT_WITH_EXPLICIT_RUNTIME_BOUNDARIES",
        "scope": "read-only chapter/source/runtime linkage; not complete PML solver, geometry, AMR, or angle coverage",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# PML evidence gradient contract", "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}", "", "| check | status |", "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
