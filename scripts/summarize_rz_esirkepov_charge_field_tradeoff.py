#!/usr/bin/env python
"""Unify the existing RZ Esirkepov charge/field tradeoff contracts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs/stage-c-validation"


def read(name: str) -> dict:
    return json.loads((RUNS / name / "contract.json").read_text(encoding="utf-8"))


def main() -> None:
    baseline = read("esirkepov_langmuir_rz_mpi2")
    no_correction = read("esirkepov_langmuir_rz_no_verboncoeur_mpi2")
    cleaning = read("esirkepov_langmuir_rz_cleaning-comparison")
    axis_family = read("esirkepov_langmuir_rz_axis-correction-family")
    highres = read("esirkepov_langmuir_rz_highres_correction-family")
    trend = read("esirkepov_langmuir_rz_resolution-trend")
    refined_family = read("esirkepov_langmuir_rz_shape-resolution-family")

    checks = [
        {"name": "default_axis_correction_field_pass_charge_fail", "passed": baseline["field_passed"] and not baseline["charge_passed"]},
        {"name": "axis_correction_off_baseline_field_charge_pass", "passed": no_correction["field_passed"] and no_correction["charge_passed"]},
        {"name": "cleaning_comparison_is_axis_dominated", "passed": cleaning["cleaning_on"]["axis_charge_relative_residual"] == cleaning["cleaning_on"]["charge_relative_residual"] and cleaning["cleaning_on"]["off_axis_charge_relative_residual"] < cleaning["cleaning_on"]["charge_relative_residual"]},
        {"name": "cleaning_off_residual_increases", "passed": cleaning["charge_residual_off_over_on"] > 1.0},
        {"name": "higher_shape_refined_off_field_charge_pass", "passed": axis_family["refined_field_all_pass"] and axis_family["refined_off_all_pass"]},
        {"name": "higher_shape_refined_on_charge_remains_boundary", "passed": axis_family["refined_on_all_charge_boundary"]},
        {"name": "highest_resolution_all_field_pass", "passed": highres["all_field_pass"]},
        {"name": "highest_resolution_on_charge_remains_boundary", "passed": not highres["on_all_charge_pass"]},
        {"name": "highest_resolution_off_charge_only_shape_3_4_pass", "passed": highres["off_charge_pass_shapes"] == [3, 4]},
        {"name": "correction_on_axis_trend_decreases", "passed": trend["on_axis_residual_monotone_decrease"]},
        {"name": "correction_off_trend_boundary_preserved", "passed": not trend["off_charge_all_pass"]},
        {"name": "refined_higher_shape_family_pass", "passed": refined_family["all_refined_pass"] and refined_family["all_coarse_field_fail"]},
    ]
    result = {
        "contract": "RZ Esirkepov charge/field tradeoff summary",
        "scope": "existing 2-rank RZ Langmuir baseline, cleaning, axis-correction, shape and resolution contracts; summary only, not a new runtime",
        "contract_pass": all(check["passed"] for check in checks),
        "classification": "RZ_ESIRKEPOV_CHARGE_FIELD_TRADEOFF_SUMMARY_BOUNDARY_DEFAULT_AXIS_CHARGE_UNRESOLVED",
        "default_field_status": "PASS",
        "default_charge_status": "BOUNDARY",
        "axis_correction_off_status": "LOCAL_PASS_NOT_GLOBAL_DEFAULT_RECOMMENDATION",
        "refined_higher_shape_status": "PASS_FOR_CORRECTION_OFF_FIELD_AND_CHARGE",
        "correction_on_charge_status": "BOUNDARY",
        "check_count": len(checks),
        "checks": checks,
        "interpretation": "The current RZ evidence separates field accuracy from same-surface divE-rho charge residual. Default Verboncoeur correction preserves the field gate but leaves an axis-dominated O(1e-3) charge boundary; correction-off locally restores charge for selected siblings but trades against coarse/higher-shape field behavior and is not a global default recommendation. The summary does not claim formal convergence or a kernel root cause.",
    }
    output_dir = RUNS / "esirkepov_langmuir_rz-charge-field-tradeoff-summary"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ Esirkepov charge/field tradeoff summary",
        "",
        f"- status: `{'PASS' if result['contract_pass'] else 'FAIL'}`",
        f"- classification: `{result['classification']}`",
        "- default axis correction: field `PASS`, charge `BOUNDARY`",
        "- correction-off: local sibling pass only; not a global default recommendation",
        "- correction-on charge residual: axis-dominated boundary across refined shape family",
        "- scope: summary of existing runtime contracts; no new runtime and no formal convergence claim",
        "",
        "| check | result |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{check['name']}` | `{'PASS' if check['passed'] else 'FAIL'}` |" for check in checks)
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("contract_pass", "classification", "check_count")}, ensure_ascii=False))
    if not result["contract_pass"]:
        raise SystemExit("RZ Esirkepov tradeoff summary contract failed")


if __name__ == "__main__":
    main()
