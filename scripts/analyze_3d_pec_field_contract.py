#!/usr/bin/env python
"""Independent standing-wave contract for the 3D PEC field test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


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
    max_error = abs(float(np.max(ey)) - expected) / expected
    min_error = abs(float(np.min(ey)) + expected) / expected
    boundary = {"lo": float(np.max(np.abs(ey[:, :, 0]))), "hi": float(np.max(np.abs(ey[:, :, -1])))}
    result = {
        "case": "test_3d_pec_field",
        "plotfile": args.plotfile,
        "ey_max": float(np.max(ey)),
        "ey_min": float(np.min(ey)),
        "expected_amplitude": expected,
        "max_relative_error": max_error,
        "min_relative_error": min_error,
        "reflection_gate": max_error < 0.01 and min_error < 0.01,
        "boundary_abs_max": boundary,
        "note": "The upstream analysis gates standing-wave amplitude; boundary values are reported as an additional diagnostic and are not used as a separate pass gate.",
    }
    result["contract_pass"] = result["reflection_gate"]
    (case_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (case_dir / "contract.md").write_text(
        "\n".join([
            "# 3D PEC field contract", "",
            f"- `Ey_max={result['ey_max']:.9e}`, `Ey_min={result['ey_min']:.9e}`; expected `+/-2.0e5 V/m`.",
            f"- Relative amplitude errors: max `{max_error:.6%}`, min `{min_error:.6%}`; standing-wave gate `{'PASS' if result['reflection_gate'] else 'FAIL'}`.",
            f"- Reported boundary maxima: z-lo `{boundary['lo']:.9e} V/m`, z-hi `{boundary['hi']:.9e} V/m`.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
