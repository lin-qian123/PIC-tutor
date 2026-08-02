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
        "runs/stage-c-validation/rz-rho-axis-correction-ratio-v0.101/contract.json",
        "runs/stage-c-validation/rz-rho-axis-prescale-boundary-v0.102/contract.json",
        "runs/stage-c-validation/rz-rho-particle-state-invariant-v0.103/contract.json",
        "runs/stage-c-validation/rz-axis-correction-default-explicit-true-v0.104/contract.json",
        "runs/stage-c-validation/rz-axis-correction-nonneutral-control-v0.105/contract.json",
        "runs/stage-c-validation/rz-axis-correction-nonneutral-shape-family-v0.106/contract.json",
        "runs/stage-c-validation/rz-axis-correction-nonneutral-shape-resolution-family-v0.107/contract.json",
        "runs/stage-c-validation/rz-axis-correction-nonneutral-density-family-v0.108/contract.json",
        "runs/stage-c-validation/rz-axis-correction-nonneutral-density-triple-v0.109/contract.json",
        "runs/stage-c-validation/formal-convergence-second-family-v0.110/contract.json",
        "runs/stage-c-validation/formal-convergence-repeat-slope-gate-v0.110/contract.json",
        "runs/stage-c-validation/formal-convergence-repeat-slope-gate-v0.95/contract.json",
    )
    checks = {
        "register_heading": register.startswith("# PIC-tutor 当前成书缺口登记"),
        "all_ids_present": all(identifier in register for identifier in REGISTER_IDS),
        "evidence_paths_present": all((root / path).is_file() for path in evidence_paths),
        "chapter_section": "## 9.8 如何阅读证据边界" in chapter,
        "chapter_boundary_summary": all(marker in chapter for marker in (
            "文献边界",
            "实现边界",
            "数值边界",
            "收敛边界",
            "第 8 章的验证矩阵",
        )),
        "rz_axis_stencil_evidence": all(marker in register for marker in (
            "rz-axis-divergence-stencil-v0.98/contract.json",
            "rz-axis-divergence-resolution-v0.99/contract.json",
            "rz-axis-divergence-fit-v0.100/contract.json",
            "80-rz-axis-divergence-resolution-alignment.md",
            "81-rz-axis-divergence-fitted-coefficient.md",
            "RZ_AXIS_STENCIL_FIT_COEFFICIENT_CROSS_RESOLUTION_OBSERVED_CHARGE_BOUNDARY_OPEN",
            "RZ_RHO_AXIS_CORRECTION_RATIO_MISMATCH_BOUNDARY_OPEN",
            "rz-rho-axis-correction-ratio-v0.101/contract.json",
            "82-rz-rho-axis-correction-ratio-boundary.md",
            "RZ_RHO_AXIS_PRESCALE_INPUT_BOUNDARY_OPEN",
            "rz-rho-axis-prescale-boundary-v0.102/contract.json",
            "83-rz-rho-axis-prescale-boundary.md",
            "RZ_RHO_AXIS_DIAGNOSTIC_CONSUMER_BOUNDARY_OPEN",
            "rz-rho-particle-state-invariant-v0.103/contract.json",
            "84-rz-rho-particle-state-invariant.md",
            "RZ_AXIS_CORRECTION_DEFAULT_EXPLICIT_TRUE_EQUIVALENT_FALSE_BOUNDARY_OPEN",
            "rz-axis-correction-default-explicit-true-v0.104/contract.json",
            "85-rz-axis-correction-default-explicit-true.md",
            "RZ_NONNEUTRAL_AXIS_CORRECTION_REVEALS_TOTAL_RHO_CONTRIBUTION_BOUNDARY_OPEN",
            "rz-axis-correction-nonneutral-control-v0.105/contract.json",
            "86-rz-axis-correction-nonneutral-control.md",
            "RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_AXIS_BOUNDARY_OPEN",
            "rz-axis-correction-nonneutral-shape-family-v0.106/contract.json",
            "87-rz-axis-correction-nonneutral-shape-family.md",
            "RZ_NONNEUTRAL_AXIS_CORRECTION_SHAPE_DEPENDENT_CROSS_RESOLUTION_BOUNDARY_OPEN",
            "rz-axis-correction-nonneutral-shape-resolution-family-v0.107/contract.json",
            "88-rz-axis-correction-nonneutral-shape-resolution-family.md",
            "RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_CANCELLATION_DENSITY_SENSITIVE_BOUNDARY_OPEN",
            "rz-axis-correction-nonneutral-density-family-v0.108/contract.json",
            "89-rz-axis-correction-nonneutral-density-family.md",
            "RZ_NONNEUTRAL_AXIS_CORRECTION_TOTAL_RHO_SAMPLED_AXIS_CANCELLATION_SPECIAL_RATIO_BOUNDARY_OPEN",
            "rz-axis-correction-nonneutral-density-triple-v0.109/contract.json",
            "90-rz-axis-correction-nonneutral-density-triple.md",
            "formal-convergence-second-family-v0.110/contract.json",
            "formal-convergence-repeat-slope-gate-v0.110/contract.json",
            "91-formal-convergence-repeat-slope-gate-v0.110.md",
        )),
        "editorial_audit_evidence": all(
            (root / path).is_file()
            for path in (
                "docs/pdf-layout-audit-v0.110.md",
                "runs/stage-c-validation/pdf-layout-v0.110/contract.json",
                "docs/editorial-quality-audit-v0.110.md",
                "runs/stage-c-validation/editorial-quality-v0.110/contract.json",
                "runs/stage-c-validation/cross-geometry-convergence-trends/contract.json",
                "docs/formal-convergence-preregistration.json",
                "runs/stage-c-validation/formal-convergence-preregistration/contract.json",
                "docs/public-distribution-risk-register-v0.110.md",
                "scripts/audit_public_distribution_boundary.py",
                "docs/final-release-readiness-v0.110.md",
                "scripts/audit_final_release_readiness.py",
            )
        ) and all(marker in register for marker in (
            "MANUSCRIPT_FINAL_EDITORIAL_REVIEW_PASS_PUBLIC_REDISTRIBUTION_BLOCKED",
            "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN",
            "SOURCE_DIAGNOSTIC_DISCRETIZATION_BOUNDARY",
            "PUBLIC_REPOSITORY_THIRD_PARTY_ASSETS_TRACKED_REMEDIATION_REQUIRED",
            "docs/public-distribution-risk-register-v0.110.md",
        )),
        "release_editorial_read_closure": all(marker in register for marker in (
            "READER_FACING_CORE_CHAPTERS_PASS_BASELINE_READ_INCREMENTAL_REVIEW_RECORDED",
            "MANUSCRIPT_FINAL_EDITORIAL_REVIEW_PASS_PUBLIC_REDISTRIBUTION_BLOCKED",
            "275 页最终全量页面复核已记录",
            "不再以“继续人工通读”替代权利决定",
        )) and all(
            (root / path).is_file()
            for path in (
                "docs/manual-editorial-spotcheck-v0.110.md",
                "docs/reader-facing-editorial-audit-v0.110.md",
                "docs/final-release-readiness-v0.110.md",
            )
        ),
        "classification_boundaries": all(marker in register for marker in (
            "OPEN_EXTERNAL_ACCESS", "RUNTIME_TRANSITION_ZONE_BRANCH_ACTIVATION_OBSERVED_ROUTE_LEDGER_UNPROVEN", "PRE_PHYSICS_BOUNDARY",
            "FORMAL_CONVERGENCE_REPEAT_SLOPE_GATE_PASS_CHARGE_CLOSURE_OPEN", "PUBLIC_REPOSITORY_THIRD_PARTY_ASSETS_TRACKED_REMEDIATION_REQUIRED", "RELEASE-EDITORIAL",
        )),
        "closure_language": all(marker in register for marker in ("关闭条件", "真实 `current_buf/rho_buf`", "publisher PDF")),
        "exercise_renumbering": all(
            marker in chapter
            for marker in (
                "## 9.11 练习与复核",
                "### 9.11.1",
                "### 9.11.2",
                "### 9.11.3",
                "### 9.11.4",
            )
        ),
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
