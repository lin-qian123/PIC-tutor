#!/usr/bin/env python
"""Audit the current book-gap register against project evidence and chapter 9."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REGISTER_IDS = (
    "LIT-ESIRKEPOV-PUBLISHER",
    "LIT-LEE-PUBLISHER",
    "RUNTIME-TRANSITION-ZONE",
    "RUNTIME-RZ-IMPLICIT-VILLASENOR",
    "RUNTIME-VAY-AMR",
    "PHYSICS-RZ-AXIS-CHARGE",
    "STUDY-FORMAL-CONVERGENCE",
    "RELEASE-EDITORIAL",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    register = (root / "docs/current-book-gap-register.md").read_text(encoding="utf-8")
    chapter = (root / "manuscript/chapters/09-literature-roadmap.md").read_text(encoding="utf-8")
    evidence_paths = (
        "runs/stage-c-validation/esirkepov-publication-boundary/contract.json",
        "runs/stage-c-validation/leecpc2015-accepted-manuscript-contract/contract.json",
        "runs/stage-c-validation/transition-zone-runtime-activation-v0.98/contract.json",
        "runs/stage-c-validation/transition-zone-source-contract.json",
        "runs/stage-c-validation/rz-implicit-villasenor-build-boundary/contract.json",
        "runs/stage-c-validation/vay-amr-guard/contract.json",
        "runs/stage-c-validation/esirkepov_langmuir_rz-charge-field-tradeoff-summary/contract.json",
        "runs/stage-c-validation/deposition-convergence-readiness/contract.json",
        "runs/stage-c-validation/rz-axis-charge-source-diagnostic-crosswalk-v0.94/contract.json",
        "runs/stage-c-validation/rz-axis-divergence-resolution-v0.99/contract.json",
        "runs/stage-c-validation/rz-axis-divergence-fit-v0.100/contract.json",
        "runs/stage-c-validation/formal-convergence-repeat-slope-gate-v0.95/contract.json",
    )
    checks = {
        "register_heading": register.startswith("# PIC-tutor 当前成书缺口登记"),
        "all_ids_present": all(identifier in register for identifier in REGISTER_IDS),
        "evidence_paths_present": all((root / path).is_file() for path in evidence_paths),
        "chapter_section": "## 9.8 当前成书缺口登记" in chapter,
        "chapter_link": "docs/current-book-gap-register.md" in chapter and "scripts/audit_current_gap_register.py" in chapter,
        "rz_axis_stencil_evidence": all(marker in register for marker in (
            "rz-axis-divergence-stencil-v0.98/contract.json",
            "rz-axis-divergence-resolution-v0.99/contract.json",
            "rz-axis-divergence-fit-v0.100/contract.json",
            "80-rz-axis-divergence-resolution-alignment.md",
            "81-rz-axis-divergence-fitted-coefficient.md",
            "RZ_AXIS_STENCIL_FIT_COEFFICIENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN",
        )),
        "editorial_audit_evidence": all(
            (root / path).is_file()
            for path in (
                "docs/pdf-layout-audit-v0.100.md",
                "runs/stage-c-validation/pdf-layout-v0.100/contract.json",
                "docs/editorial-quality-audit-v0.100.md",
                "runs/stage-c-validation/editorial-quality-v0.100/contract.json",
                "runs/stage-c-validation/cross-geometry-convergence-trends/contract.json",
                "docs/formal-convergence-preregistration.json",
                "runs/stage-c-validation/formal-convergence-preregistration/contract.json",
            )
        ) and all(marker in register for marker in (
            "PDF_LAYOUT_AUTOMATED_PASS_MANUAL_SPOTCHECK_RECORDED",
            "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN",
            "SOURCE_DIAGNOSTIC_DISCRETIZATION_BOUNDARY",
        )),
        "classification_boundaries": all(marker in register for marker in (
            "OPEN_EXTERNAL_ACCESS", "RUNTIME_TRANSITION_ZONE_BRANCH_ACTIVATION_OBSERVED_ROUTE_LEDGER_UNPROVEN", "PRE_PHYSICS_BOUNDARY",
            "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN", "RELEASE-EDITORIAL",
        )),
        "closure_language": all(marker in register for marker in ("关闭条件", "真实 `current_buf/rho_buf`", "publisher PDF")),
        "exercise_renumbering": all(marker in chapter for marker in ("## 9.10 练习与复核", "### 9.10.1", "### 9.10.2", "### 9.10.3")),
    }
    result = {
        "contract": "current book gap register",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "CURRENT_BOOK_GAP_REGISTER_WITH_EVIDENCE_AND_CLOSURE_CRITERIA",
        "scope": "project-level gap inventory; does not close any listed gap",
        "gap_count": len(REGISTER_IDS),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Current book gap register contract", "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        f"- gap count: `{result['gap_count']}`", "", "| check | status |", "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.append("\nThe contract validates inventory consistency only; it does not close any gap.")
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
