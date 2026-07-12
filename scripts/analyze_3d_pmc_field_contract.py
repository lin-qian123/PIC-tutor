#!/usr/bin/env python
"""Independent standing-wave contract for the 3D PMC field test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--plotfile", default="diags/diag1000134")
    args = parser.parse_args()

    import yt

    case_dir = args.case_dir.resolve()
    ds = yt.load(str(case_dir / args.plotfile))
    data = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    ey = data["mesh", "Ey"].to_ndarray()
    expected = 2.0e5
    max_error = abs(float(ey.max()) - expected) / expected
    min_error = abs(float(ey.min()) + expected) / expected
    result = {
        "case": "test_3d_pmc_field",
        "plotfile": args.plotfile,
        "ey_max": float(ey.max()),
        "ey_min": float(ey.min()),
        "expected_amplitude": expected,
        "max_relative_error": max_error,
        "min_relative_error": min_error,
        "reflection_gate": max_error < 0.01 and min_error < 0.01,
        "note": "This is the same standing-wave amplitude consumer used by the upstream PMC analysis; it does not claim a separate magnetic-boundary component proof.",
    }
    result["contract_pass"] = result["reflection_gate"]
    (case_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (case_dir / "contract.md").write_text(
        "\n".join([
            "# 3D PMC field contract", "",
            f"- `Ey_max={result['ey_max']:.9e}`, `Ey_min={result['ey_min']:.9e}`; expected `+/-2.0e5 V/m`.",
            f"- Relative amplitude errors: max `{max_error:.6%}`, min `{min_error:.6%}`; standing-wave gate `{'PASS' if result['reflection_gate'] else 'FAIL'}`.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
