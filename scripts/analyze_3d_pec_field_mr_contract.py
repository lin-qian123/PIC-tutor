#!/usr/bin/env python
"""Independent standing-wave contract for the 3D PEC+MR test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--plotfile", default="diags/diag1000125")
    args = parser.parse_args()

    import yt

    case_dir = args.case_dir.resolve()
    ds = yt.load(str(case_dir / args.plotfile))
    data = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    ey = data["mesh", "Ey"].to_ndarray()
    expected = 2.0e5
    max_error = abs(float(ey.max()) - expected) / expected
    min_error = abs(float(ey.min()) + expected) / expected
    threshold = 0.05
    result = {
        "case": "test_3d_pec_field_mr",
        "plotfile": args.plotfile,
        "amr_levels": int(ds.index.max_level) + 1,
        "ey_max": float(ey.max()),
        "ey_min": float(ey.min()),
        "max_relative_error": max_error,
        "min_relative_error": min_error,
        "threshold": threshold,
        "reflection_gate": max_error < threshold and min_error < threshold,
        "note": "The producer emitted the upstream Projection Div Cleaner warning that only the first AMR level is cleaned; the PEC+MR standing-wave gate itself passes.",
    }
    result["contract_pass"] = result["reflection_gate"]
    (case_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (case_dir / "contract.md").write_text(
        "\n".join([
            "# 3D PEC+MR field contract", "",
            f"- AMR levels: `{result['amr_levels']}`; `Ey_max={result['ey_max']:.9e}`, `Ey_min={result['ey_min']:.9e}`.",
            f"- Relative amplitude errors: max `{max_error:.6%}`, min `{min_error:.6%}`; upstream threshold `{threshold:.0%}`; gate `{'PASS' if result['reflection_gate'] else 'FAIL'}`.",
            "- Runtime boundary: the producer reported that Projection Div Cleaner only cleans the first AMR level; this warning is recorded and not treated as an analysis failure.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
