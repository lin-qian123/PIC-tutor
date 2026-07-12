#!/usr/bin/env python
"""Screen the Higuera-Cary Poincare contract for a localized p_y anomaly."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


WINDOW_LO = 1.5
WINDOW_HI = 1.9
ANOMALY_RATIO = 3.0
CONTROL_RATIO_MAX = 2.0


def initial_py(row: dict) -> float:
    return float(row["invariant_ledger"]["I_y_initial"]) ** 0.5


def summarize_case(case: dict) -> dict:
    window = []
    outside = []
    for species, row in case["species"].items():
        py0 = initial_py(row)
        drift = float(row["invariant_ledger"]["I_y_relative_drift_max"])
        record = {"species": species, "initial_py": py0, "I_y_relative_drift_max": drift}
        (window if WINDOW_LO <= py0 <= WINDOW_HI else outside).append(record)
    window_max = max((row["I_y_relative_drift_max"] for row in window), default=0.0)
    outside_max = max((row["I_y_relative_drift_max"] for row in outside), default=0.0)
    ratio = window_max / max(outside_max, 1.0e-30)
    return {
        "pusher": case["pusher"],
        "window": {"p_y_min": WINDOW_LO, "p_y_max": WINDOW_HI, "rows": window, "max_drift": window_max},
        "outside_window": {"rows": outside, "max_drift": outside_max},
        "window_to_outside_max_drift_ratio": ratio,
        "localized_anomaly_candidate": ratio >= ANOMALY_RATIO,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.input_json.read_text(encoding="utf-8"))
    cases = [summarize_case(case) for case in source["cases"]]
    by_pusher = {case["pusher"]: case for case in cases}
    checks = {
        "three_pushers_present": set(by_pusher) == {"boris", "vay", "higuera"},
        "vay_localized_anomaly_candidate": by_pusher.get("vay", {}).get("localized_anomaly_candidate", False),
        "boris_control_not_localized": by_pusher.get("boris", {}).get("window_to_outside_max_drift_ratio", float("inf")) < CONTROL_RATIO_MAX,
        "higuera_control_not_localized": by_pusher.get("higuera", {}).get("window_to_outside_max_drift_ratio", float("inf")) < CONTROL_RATIO_MAX,
    }
    result = {
        "contract": "Higuera-Cary resonance-sensitive invariant screen",
        "passed": all(checks.values()),
        "checks": checks,
        "window": {"p_y_min": WINDOW_LO, "p_y_max": WINDOW_HI, "anomaly_ratio_threshold": ANOMALY_RATIO},
        "cases": cases,
        "evidence_boundary": {
            "screen_is_topology_proof": False,
            "interpretation": "This screen identifies localized I_y degradation near the paper's p_y≈1.7 resonance-sensitive region. It does not classify a two-fold island or trajectory topology.",
            "resolution_boundary": "The dense family uses a 32^3 grid; use a finer-grid p_y-window control before promoting the anomaly beyond a screening result.",
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Higuera-Cary resonance-sensitive invariant screen",
        "",
        "This is a localized invariant-drift screen, not a Poincare topology proof.",
        "",
        "| pusher | window max drift | outside max drift | ratio | candidate |",
        "|---|---:|---:|---:|:---:|",
    ]
    for case in cases:
        lines.append(
            f"| `{case['pusher']}` | `{case['window']['max_drift']:.8e}` | `{case['outside_window']['max_drift']:.8e}` | `{case['window_to_outside_max_drift_ratio']:.4f}` | `{'YES' if case['localized_anomaly_candidate'] else 'NO'}` |"
        )
    lines += ["", result["evidence_boundary"]["interpretation"], result["evidence_boundary"]["resolution_boundary"]]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
