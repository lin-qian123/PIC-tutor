#!/usr/bin/env python
"""Unify the existing Higuera-Cary Poincare/topology evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs/stage-c-validation"


def read(relative: str) -> dict:
    return json.loads((RUNS / relative).read_text(encoding="utf-8"))


def main() -> int:
    short = read("higuera_poincare_comparison/topology.json")
    long = read("higuera_poincare_long_comparison/topology.json")
    dense = read("higuera_poincare_dense_comparison/topology.json")
    resonance = read("higuera_poincare_dense_comparison/resonance-window.json")
    resolution = read("higuera_poincare_resonance_comparison/resolution-contract.json")

    checks = {
        "short_run_is_insufficient_sampling": short["status"] == "INSUFFICIENT_SAMPLING",
        "long_run_sampling_is_sufficient": all(case["sampling_sufficient"] for case in long["cases"]),
        "long_run_invariant_and_reference_gates_pass": long["invariant_order_gate_passed"] and long["analytic_reference_curve_gate_passed"],
        "long_run_angular_candidates_have_no_intersections": all(
            case["angular_order"]["self_intersections_absent"] and case["angular_order"]["pairwise_intersections_absent"]
            for case in long["cases"]
        ),
        "long_run_topology_not_promoted": not long["topology_gate_passed"] and long["status"] == "REVIEW_REQUIRED",
        "dense_run_reference_gate_boundary": not dense["analytic_reference_curve_gate_passed"],
        "dense_run_candidate_signature_boundary": not dense["candidate_signature_consistent_across_pushers"],
        "resonance_screen_passes": resonance["passed"],
        "resolution_screen_passes": resolution["passed"],
        "all_topology_gates_remain_unpromoted": not short["topology_gate_passed"] and not long["topology_gate_passed"] and not dense["topology_gate_passed"],
    }
    result = {
        "contract": "Higuera-Cary Poincare evidence boundary summary",
        "passed": all(checks.values()),
        "classification": "HIGUERA_POINCARE_INVARIANT_AND_RESONANCE_SCREEN_VERIFIED_TOPOLOGY_REMAINS_UNPROMOTED",
        "checks": checks,
        "evidence_layers": {
            "short": "INSUFFICIENT_SAMPLING",
            "long": "INVARIANT_AND_ANALYTIC_REFERENCE_PASS_ANGULAR_CANDIDATE_NO_INTERSECTION_TOPOLOGY_REVIEW_REQUIRED",
            "dense": "RESONANCE_SCREEN_PASS_REFERENCE_CURVE_AND_CANDIDATE_SIGNATURE_BOUNDARY",
        },
        "scope": "summary of existing case-local Poincare, invariant, dense-family and resolution contracts; no new runtime",
        "boundary": "The current evidence supports invariant ordering, the quartic reference curve for the long family, and a localized Vay resonance-sensitive screen. It does not establish a paper-equivalent two-fold island or trajectory-crossing topology gate.",
    }
    output_dir = RUNS / "higuera-poincare-evidence-summary"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Higuera-Cary Poincare evidence boundary summary",
        "",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- classification: `{result['classification']}`",
        "- short family: insufficient sampling",
        "- long family: invariant/reference pass; topology not promoted",
        "- dense family: resonance screen pass; reference/signature boundary",
        "- topology gate: not promoted",
        "",
        "| check | result |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", result["boundary"]]
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "classification": result["classification"], "check_count": len(checks)}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
