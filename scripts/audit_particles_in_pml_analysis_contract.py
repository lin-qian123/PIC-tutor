#!/usr/bin/env python
"""Audit the signed-vs-absolute residual-field contract in WarpX's PML analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check(text: str, needle: str) -> dict[str, object]:
    return {"needle": needle, "present": needle in text}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    upstream = args.warpx_root.resolve()
    official_path = upstream / "Examples/Tests/particles_in_pml/analysis_particles_in_pml.py"
    independent_path = Path(__file__).resolve().parent / "analyze_particles_in_pml_contract.py"
    official = official_path.read_text(encoding="utf-8")
    independent = independent_path.read_text(encoding="utf-8")

    official_checks = [
        check(official, "max_Efield = max(Ex_array.max(), Ey_array.max(), Ez_array.max())"),
        check(official, "assert max_Efield < tolerance_abs"),
        check(official, "np.abs"),
    ]
    independent_checks = [
        check(independent, "np.max(np.abs(grid[\"boxlib\", name].to_ndarray()))"),
        check(independent, '"max_abs_Efield"'),
    ]
    result = {
        "official_analysis": str(official_path),
        "independent_analysis": str(independent_path),
        "official_checks": official_checks,
        "independent_checks": independent_checks,
        "official_uses_signed_component_max": all(
            item["present"] for item in official_checks[:2]
        ) and not official_checks[2]["present"],
        "independent_uses_absolute_component_max": all(
            item["present"] for item in independent_checks
        ),
        "interpretation": (
            "The upstream consumer takes component maxima without abs(), so a negative "
            "peak can be invisible to its gate. The project reader-side contract takes "
            "the maximum absolute value and is intentionally stricter."
        ),
    }
    result["passed"] = bool(
        result["official_uses_signed_component_max"]
        and result["independent_uses_absolute_component_max"]
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    status = "PASS" if result["passed"] else "FAIL"
    lines = [
        "# Particles-in-PML analysis source contract",
        "",
        f"- status: `{status}`",
        f"- upstream analysis: `{official_path}`",
        f"- project independent analysis: `{independent_path}`",
        "- upstream gate: `max(Ex.max(), Ey.max(), Ez.max()) < tolerance_abs` (signed component maxima)",
        "- project gate: `max(abs(Ex), abs(Ey), abs(Ez)) < tolerance_abs`",
        "- interpretation: the independent contract is deliberately stricter because it detects negative residual-field peaks.",
        "- scope: source semantics only; this does not alter `../warpx`.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
