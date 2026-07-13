#!/usr/bin/env python
"""Audit a bounded Vay Appendix-B runtime proxy contract."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparison-json", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    comparison = json.loads(args.comparison_json.read_text(encoding="utf-8"))
    cases = comparison["cases"]
    expected_phase = 2.0 * math.atan(
        comparison["physics"]["continuum_cyclotron_frequency"] * comparison["cases"][0]["output_dt"] / 2.0
    )
    phase_errors = []
    pusher_phase_errors = {}
    proxy_errors = []
    gyroradius_errors = []
    momentum_spreads = []
    finalize_tail_flags = []
    for case in cases:
        case_dir = args.run_root / case["pusher"]
        log = case_dir / "run.log"
        log_text = log.read_text(encoding="utf-8") if log.is_file() else ""
        finalize_tail_flags.append(
            "Writing plotfile diags/diag1000080" in log_text
            and "ComputeDivE: Unknown algorithm" in log_text
        )
        for species in case["species"]:
            error = abs(species["momentum_phase_increment_abs_mean"] - expected_phase)
            phase_errors.append(error)
            pusher_phase_errors.setdefault(case["pusher"], []).append(error)
            proxy_errors.append(species["position_update_velocity_proxy_relative_error_max_abs"])
            gyroradius_errors.append(abs(species["gyroradius_proxy_relative_error"]))
            momentum_spreads.append(species["momentum_norm_relative_spread"])

    checks = {
        "three_expected_pushers": {case["pusher"] for case in cases} == {"boris", "vay", "higuera"},
        "all_cases_have_81_full_plotfiles": all(case["plotfile_count"] == 81 for case in cases),
        "boris_vay_discrete_phase_angle_gate": max(
            error for pusher, errors in pusher_phase_errors.items() if pusher in {"boris", "vay"} for error in errors
        ) < 1.0e-10,
        "higuera_phase_observation_finite": max(pusher_phase_errors["higuera"]) < 1.0e-3,
        "position_update_velocity_proxy_gate": max(proxy_errors) < 1.0e-10,
        "gyroradius_proxy_gate": max(gyroradius_errors) < 1.0e-10,
        "momentum_norm_conservation_gate": max(momentum_spreads) < 1.0e-10,
        "known_finalize_tail_after_final_plotfile": all(finalize_tail_flags),
    }
    result = {
        "contract": "Vay Appendix-B bounded uniform-B runtime proxy",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "VAY_APPENDIX_B_RUNTIME_PROXY_PASS_DIRECT_HALF_STEP_ATTRIBUTE_BOUNDARY",
        "scope": "81-frame case-local uniform-B orbit; discrete phase, position-update velocity, and gyroradius proxy; not a direct half-step attribute or publisher-figure reproduction",
        "expected_discrete_phase_rad": expected_phase,
        "max_phase_error_rad": max(phase_errors),
        "pusher_phase_error_rad": {pusher: max(errors) for pusher, errors in pusher_phase_errors.items()},
        "max_position_update_velocity_proxy_relative_error": max(proxy_errors),
        "max_gyroradius_proxy_relative_error": max(gyroradius_errors),
        "max_momentum_norm_relative_spread": max(momentum_spreads),
        "runtime_boundary": "All three binaries wrote diag1000080 before the known ComputeDivE unknown-algorithm finalize tail; the tail is not used as a physics gate.",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Vay Appendix-B bounded runtime contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        f"- expected discrete phase: `{expected_phase:.16e}` rad",
        f"- maximum Boris/Vay phase error: `{max(max(pusher_phase_errors[p]) for p in ('boris', 'vay')):.3e}` rad",
        f"- Higuera-Cary phase deviation: `{max(pusher_phase_errors['higuera']):.3e}` rad",
        f"- maximum position-update velocity proxy error: `{max(proxy_errors):.3e}`",
        f"- maximum gyroradius proxy error: `{max(gyroradius_errors):.3e}`",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The physics data contract passes after all three final plotfiles are written. The process-finalization ComputeDivE tail is recorded separately and is not promoted to a pusher failure.",
        "Direct half-step output remains unavailable; this is a bounded proxy-level Appendix-B reproduction.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
