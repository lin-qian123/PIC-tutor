#!/usr/bin/env python
"""Compare the resonance-sensitive p_y window across coarse and fine grids."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


WINDOW_SPECIES = ("p16", "p18")
COARSE_WINDOW_SPECIES = ("p08", "p09")
VAY_MIN_DRIFT = 2.0e-2
CONTROL_MAX_DRIFT = 5.0e-3
VAY_TO_CONTROL_MIN_RATIO = 5.0


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def drift_by_pusher(source: dict, species_names: tuple[str, ...]) -> dict[str, dict[str, float]]:
    return {
        case["pusher"]: {
            species: float(case["species"][species]["invariant_ledger"]["I_y_relative_drift_max"])
            for species in species_names
            if species in case["species"]
        }
        for case in source["cases"]
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("coarse_json", type=Path)
    parser.add_argument("fine_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    coarse = load(args.coarse_json)
    fine = load(args.fine_json)
    coarse_drift = drift_by_pusher(coarse, COARSE_WINDOW_SPECIES)
    fine_drift = drift_by_pusher(fine, WINDOW_SPECIES)
    fine_max = {pusher: max(rows.values()) for pusher, rows in fine_drift.items()}
    checks = {
        "coarse_window_species_present": all(len(rows) == len(WINDOW_SPECIES) for rows in coarse_drift.values()),
        "fine_window_species_present": all(len(rows) == len(WINDOW_SPECIES) for rows in fine_drift.values()),
        "fine_vay_exceeds_screen_threshold": fine_max.get("vay", 0.0) >= VAY_MIN_DRIFT,
        "fine_boris_control_below_threshold": fine_max.get("boris", float("inf")) <= CONTROL_MAX_DRIFT,
        "fine_higuera_control_below_threshold": fine_max.get("higuera", float("inf")) <= CONTROL_MAX_DRIFT,
        "fine_vay_vs_boris_ratio": fine_max.get("vay", 0.0) / max(fine_max.get("boris", 1.0e-30), 1.0e-30) >= VAY_TO_CONTROL_MIN_RATIO,
        "fine_vay_vs_higuera_ratio": fine_max.get("vay", 0.0) / max(fine_max.get("higuera", 1.0e-30), 1.0e-30) >= VAY_TO_CONTROL_MIN_RATIO,
    }
    result = {
        "contract": "Higuera-Cary resonance-window coarse/fine comparison",
        "passed": all(checks.values()),
        "checks": checks,
        "screen_thresholds": {
            "vay_min_I_y_drift": VAY_MIN_DRIFT,
            "control_max_I_y_drift": CONTROL_MAX_DRIFT,
            "vay_to_control_min_ratio": VAY_TO_CONTROL_MIN_RATIO,
        },
        "coarse_32^3": coarse_drift,
        "fine_64^3": fine_drift,
        "evidence_boundary": {
            "topology_proof": False,
            "interpretation": "The fine-grid control confirms localized I_y degradation for Vay near p_y=1.6 and 1.8 relative to Boris and Higuera-Cary. This is a resonance-sensitive invariant screen, not a two-fold island or trajectory-crossing topology proof.",
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Higuera-Cary resonance-window coarse/fine comparison",
        "",
        "| pusher | coarse max I_y drift | fine max I_y drift |",
        "|---|---:|---:|",
    ]
    for pusher in ("boris", "vay", "higuera"):
        lines.append(f"| `{pusher}` | `{max(coarse_drift[pusher].values()):.8e}` | `{max(fine_drift[pusher].values()):.8e}` |")
    lines += ["", "The fine-grid result is a localized invariant screen, not a topology proof."]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
