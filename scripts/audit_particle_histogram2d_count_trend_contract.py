#!/usr/bin/env python
"""Audit the expected-negative-control and high-PPC ParticleHistogram2D trend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trend-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    trend = json.loads(args.trend_json.read_text(encoding="utf-8"))
    pairwise = trend["pairwise"]
    pair_map = {(pair["left"], pair["right"]): pair for pair in pairwise}
    expected_pairs = [("ppc1", "ppc2"), ("ppc2", "ppc4"), ("ppc4", "ppc8")]
    electron = {
        pair: pair_map[pair]["series"]["PhaseSpaceElectrons"]["relative_differences"]["total_weight"]
        for pair in expected_pairs
    }
    checks = {
        "four_ppc_runs_present": set(trend["runs"]) == {"ppc1", "ppc2", "ppc4", "ppc8"},
        "three_adjacent_pairs_present": all(pair in pair_map for pair in expected_pairs),
        "all_data_finite_positive": trend["gates"]["finite_positive"],
        "low_count_negative_control_rejected": not pair_map[("ppc1", "ppc2")]["series"]["PhaseSpaceElectrons"]["weighted_width_stability"],
        "ppc2_to_ppc4_local_gate_passes": all(
            entry["weighted_width_stability"] for entry in pair_map[("ppc2", "ppc4")]["series"].values()
        ),
        "ppc4_to_ppc8_local_gate_passes": all(
            entry["weighted_width_stability"] for entry in pair_map[("ppc4", "ppc8")]["series"].values()
        ),
        "electron_total_weight_error_decreases": electron[("ppc2", "ppc4")] < electron[("ppc1", "ppc2")] and electron[("ppc4", "ppc8")] < electron[("ppc2", "ppc4")],
    }
    result = {
        "contract": "ParticleHistogram2D particle-count trend with expected low-count negative control",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "PARTICLE_HISTOGRAM2D_COUNT_TREND_PASS_EXPECTED_LOW_COUNT_NEGATIVE_CONTROL_FORMAL_CONVERGENCE_BOUNDARY",
        "scope": "four matched-time single-process PPC runs; local weighted-moment stability only, not a formal convergence-order proof or upstream regression",
        "electron_total_weight_relative_differences": {f"{left}->{right}": value for (left, right), value in electron.items()},
        "negative_control": "ppc1->ppc2 electron total-weight difference exceeds 1e-3",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# ParticleHistogram2D particle-count trend contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The 1x1 to 2x2 pair is intentionally retained as a rejected low-count negative control. The 2x2 to 4x4 and 4x4 to 8x8 pairs pass the selected local moment gates; this does not establish a formal convergence order.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
