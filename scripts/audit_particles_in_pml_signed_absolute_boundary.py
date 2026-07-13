#!/usr/bin/env python
"""Promote the 3D AMR particles-in-PML signed/absolute split to a public boundary contract."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    frames = source["frames"]
    final = frames[-1]
    finest = final["finest"]
    coarse = final["coarse"]
    fields = finest["fields"]
    coarse_fields = coarse["fields"]
    tolerance = float(source["tolerance_abs"])

    checks = [
        {"name": "two_field_frames_present", "passed": len(frames) >= 2},
        {"name": "final_official_signed_gate_passes", "passed": final["official_signed_pass"] is True},
        {"name": "final_absolute_gate_fails", "passed": final["absolute_pass"] is False},
        {"name": "only_negative_ex_exceeds_tolerance", "passed": source["final_negative_components_exceeding_tolerance"] == ["Ex"]},
        {"name": "absolute_exceeds_tolerance_by_finite_margin", "passed": fields["Ex"]["absolute_max"] > tolerance and math.isfinite(fields["Ex"]["absolute_max"])},
        {"name": "coarse_and_fine_absolute_max_agree", "passed": all(math.isclose(fields[name]["absolute_max"], coarse_fields[name]["absolute_max"], rel_tol=1e-12, abs_tol=1e-12) for name in ("Ex", "Ey", "Ez"))},
        {"name": "negative_peak_is_ex_peak", "passed": fields["Ex"]["negative_min"] < -tolerance and abs(fields["Ex"]["negative_min"]) == fields["Ex"]["absolute_max"]},
    ]
    result = {
        "contract": "3D AMR particles-in-PML signed-vs-absolute boundary",
        "scope": "2-rank official producer; final finest covering grid; signed upstream consumer versus strict per-component absolute reader",
        "contract_pass": False,
        "classification": "PARTICLES_IN_PML_3D_MR_BOUNDARY_SIGNED_PASS_ABSOLUTE_NEGATIVE_EX_FAIL",
        "official_signed_status": "PASS",
        "strict_absolute_status": "FAIL",
        "frame_count": len(frames),
        "tolerance_abs": tolerance,
        "official_signed_max": final["official_signed_max"],
        "absolute_max": final["absolute_max"],
        "negative_components_exceeding_tolerance": source["final_negative_components_exceeding_tolerance"],
        "finest_level": finest["level"],
        "finest_dimensions": finest["dimensions"],
        "checks": checks,
        "interpretation": "The producer and upstream signed gate run successfully, but the stricter absolute residual-field gate fails because the negative Ex peak exceeds the same threshold. This is a criterion boundary; it does not justify changing the WarpX analysis, AMR/PML evolution, or tolerance without a separate upstream decision.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# 3D AMR particles-in-PML signed-vs-absolute boundary",
        "",
        "- classification: `PARTICLES_IN_PML_3D_MR_BOUNDARY_SIGNED_PASS_ABSOLUTE_NEGATIVE_EX_FAIL`",
        f"- official signed max: `{final['official_signed_max']:.8f} < {tolerance:g}`, `PASS`",
        f"- strict absolute max: `{final['absolute_max']:.8f} > {tolerance:g}`, `FAIL`",
        "- exceeding component: negative `Ex` only",
        "- finest covering grid: `" + "x".join(str(value) for value in finest["dimensions"]) + "`",
        "",
        "This contract preserves the upstream signed result and the stricter absolute reader-side result as different evidence layers. It is a boundary record, not an upstream fix or a tolerance recommendation.",
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
