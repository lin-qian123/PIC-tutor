#!/usr/bin/env python
"""Audit the Chapter 5 deposition geometry/order gap register."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


GAPS = (
    ("rz_correction_on_charge", "RZ correction-on charge residual", "BOUNDARY", "separate axis-volume/diagnostic route before changing defaults"),
    ("radial_charge_gauss_law", "RCYLINDER/RSPHERE charge and Gauss-law closure", "BOUNDARY", "build a geometry-specific charge/Gauss-law consumer"),
    ("amr_route_count", "2D MR transition-zone route-count ledger", "UNPROVEN", "add a runtime intermediate-field/route ledger without editing WarpX"),
    ("rz_implicit_villasenor", "RZ implicit Villasenor physics runtime", "PRE_PHYSICS_BOUNDARY", "resolve compatible PETSc/AMReX build and rerun the producer"),
    ("villasenor_geometry_order", "Villasenor non-XZ geometry/order runtime family", "PARTIAL", "add one geometry/order sibling at a time with a named consumer"),
    ("vay_geometry_order", "Vay deposition geometry/order family", "PARTIAL", "keep the RZ/1D source guards separate from supported runtime cases"),
    ("formal_convergence_order", "formal convergence order across geometry and shape", "UNPROVEN", "design a resolution study with a fixed observable and error norm"),
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    root = args.project_root.resolve()
    chapter = read(root / "manuscript/chapters/05-deposition-shapes.md")
    note = read(root / "notes/code-reading/particles/72-deposition-geometry-order-gap-register.md")
    matrix = read(root / "notes/code-reading/particles/59-deposition-geometry-order-coverage-matrix.md")

    checks = {
        "chapter_register_heading": "### 5.14.2 geometry/order coverage gap register" in chapter,
        "chapter_register_scope": "negative-space contract" in chapter and "不把缺少 runtime 结果的行写成 PASS" in chapter,
        "note_register_scope": "negative-space contract" in note and "不把缺口写成 PASS" in note,
        "matrix_reference": "geometry/order" in matrix and "覆盖矩阵" in matrix,
        "all_gap_ids_documented": all(item[0] in note for item in GAPS),
        "all_classifications_documented": all(item[2] in note for item in GAPS),
        "all_next_actions_documented": all(
            phrase in note
            for phrase in (
                "分离 axis-volume 与诊断路径",
                "geometry-specific charge/Gauss-law consumer",
                "真实 intermediate-field/route ledger",
                "兼容 PETSc/AMReX build",
                "独立 consumer 的 sibling",
                "RZ/1D source guard",
                "resolution family",
            )
        ),
        "no_runtime_pass_language": all(
            phrase not in note for phrase in ("完整 geometry/order 已通过", "全部组合 PASS", "全组合验证完成")
        ),
    }
    result = {
        "contract": "Chapter 5 deposition geometry/order gap register",
        "scope": "negative-space register; named gaps and next evidence actions only",
        "classification": "KNOWN_GAPS_EXPLICITLY_SCOPED_NO_PASS_INFERENCE",
        "checks": checks,
        "gaps": [
            {"id": i, "label": label, "classification": classification, "next": next_action}
            for i, label, classification, next_action in GAPS
        ],
        "passed": all(checks.values()),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 5 deposition geometry/order gap register", "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}", "",
        "| id | classification | next evidence action |", "|---|---|---|",
    ]
    lines.extend(f"| `{i}` | `{classification}` | {next_action} |" for i, _, classification, next_action in GAPS)
    lines += ["", "The register names missing or partial evidence; it does not infer runtime PASS from source coverage or from an absent row."]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {sum(checks.values())}/{len(checks)} deposition gap-register checks")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
