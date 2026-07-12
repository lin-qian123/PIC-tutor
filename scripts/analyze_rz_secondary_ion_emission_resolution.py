#!/usr/bin/env python
"""Compare RZ secondary-emission geometry contracts at two resolutions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("refined", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    baseline = load(args.baseline / "contract.json")
    refined = load(args.refined / "contract.json")
    base_max = max(baseline["relative_distance_to_closest_impact"])
    refined_max = max(refined["relative_distance_to_closest_impact"])
    result = {
        "case": "test_rz_secondary_ion_emission_picmi",
        "baseline": {"resolution": "64x64", "max_relative_distance": base_max, "contract_pass": baseline["contract_pass"]},
        "refined": {"resolution": "128x128", "max_relative_distance": refined_max, "contract_pass": refined["contract_pass"]},
        "max_error_reduction_factor": base_max / refined_max,
        "refined_gate_pass": refined["contract_pass"],
        "trend_supports_resolution_diagnosis": refined_max < base_max and refined["contract_pass"],
        "interpretation": "The refined producer passes the 2% EB impact-point gate while the baseline does not; this supports a resolution-sensitive EB geometry error diagnosis, not a claim that the baseline implementation is acceptable.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "resolution-comparison.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ secondary-emission resolution comparison",
        "",
        f"- 64x64 maximum relative impact-point distance: `{base_max:.8%}`; contract: `{'PASS' if baseline['contract_pass'] else 'FAIL'}`.",
        f"- 128x128 maximum relative impact-point distance: `{refined_max:.8%}`; contract: `{'PASS' if refined['contract_pass'] else 'FAIL'}`.",
        f"- Maximum-error reduction factor: `{base_max / refined_max:.3f}`.",
        "- Interpretation: the refined run passes the official 2% geometry gate, supporting a resolution-sensitive EB intersection diagnosis. This does not make the 64x64 baseline a passing case.",
    ]
    (args.output_dir / "resolution-comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["trend_supports_resolution_diagnosis"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
