#!/usr/bin/env python
"""Promote the RZ secondary-emission resolution trend to a public contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trend", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    trend = json.loads(args.trend.read_text(encoding="utf-8"))
    resolutions = trend["resolutions"]
    expected = {64: False, 128: True, 256: True}
    checks = []
    checks.append({"name": "expected_resolutions_present", "passed": {item["resolution"] for item in resolutions} == set(expected)})
    checks.append({"name": "baseline_failure_preserved", "passed": next((item["contract_pass"] is False for item in resolutions if item["resolution"] == 64), False)})
    checks.append({"name": "refined_128_gate_pass", "passed": next((item["contract_pass"] is True for item in resolutions if item["resolution"] == 128), False)})
    checks.append({"name": "refined_256_gate_pass", "passed": next((item["contract_pass"] is True for item in resolutions if item["resolution"] == 256), False)})
    checks.append({"name": "error_decreases_at_each_refinement", "passed": all(left["max_relative_distance"] > right["max_relative_distance"] for left, right in zip(resolutions, resolutions[1:]))})
    checks.append({"name": "refined_errors_below_two_percent", "passed": all(item["max_relative_distance"] < 0.02 for item in resolutions if item["resolution"] > 64)})
    checks.append({"name": "interpretation_rejects_formal_order_claim", "passed": "not a formal convergence study" in trend["interpretation"]})

    result = {
        "case": trend["case"],
        "contract": "RZ secondary-emission resolution-aware geometry boundary",
        "scope": "64x64 baseline plus 128x128/256x256 refined controls; official 2% EB impact-point gate",
        "contract_pass": False,
        "classification": "RZ_SECONDARY_EMISSION_BOUNDARY_BASELINE_FAIL_REFINED_CONTROLS_PASS",
        "baseline_status": "FAIL",
        "refined_status": "PASS",
        "resolution_count": len(resolutions),
        "baseline_max_relative_distance": resolutions[0]["max_relative_distance"],
        "refined_128_max_relative_distance": resolutions[1]["max_relative_distance"],
        "refined_256_max_relative_distance": resolutions[2]["max_relative_distance"],
        "max_error_reduction_64_to_128": trend["pairwise"][0]["error_reduction_factor"],
        "checks": checks,
        "interpretation": "The default 64x64 geometry gate remains a failure. Both refined controls pass and the monotone three-run trend supports a resolution-sensitive EB geometry diagnosis; it does not close the upstream baseline or establish a formal convergence order.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ secondary-emission resolution-aware geometry boundary",
        "",
        "- raw contract status: `FAIL` (the default baseline remains outside the official gate)",
        "- classification: `RZ_SECONDARY_EMISSION_BOUNDARY_BASELINE_FAIL_REFINED_CONTROLS_PASS`",
        f"- `64x64`: `{resolutions[0]['max_relative_distance']:.4%}` relative impact-point error, `FAIL`",
        f"- `128x128`: `{resolutions[1]['max_relative_distance']:.4%}`, `PASS`",
        f"- `256x256`: `{resolutions[2]['max_relative_distance']:.4%}`, `PASS`",
        "",
        "The refined controls support a resolution-sensitive EB geometry diagnosis. This is a boundary record, not a claim that the default upstream regression passes or that a formal convergence order has been established.",
        "",
        "| check | result |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{check['name']}` | `{'PASS' if check['passed'] else 'FAIL'}` |" for check in checks)
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"contract_pass": result["contract_pass"], "classification": result["classification"], "checks": checks}, ensure_ascii=False))
    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
