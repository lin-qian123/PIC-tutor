#!/usr/bin/env python
"""Independent reader-side residual-field contract for RZ Silver-Mueller."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--plotfile", default="diags/diag1000500")
    args = parser.parse_args()

    import yt

    case_dir = args.case_dir.resolve()
    ds = yt.load(str(case_dir / args.plotfile))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    components = {name: grid["boxlib", name].v.squeeze() for name in ("Er", "Et", "Ez")}
    maxima = {name: float(np.max(np.abs(values))) for name, values in components.items()}
    threshold = 0.01
    result = {
        "case": "test_rz_silver_mueller_z",
        "plotfile": args.plotfile,
        "max_abs_field": maxima,
        "threshold": threshold,
        "component_pass": {name: value < threshold for name, value in maxima.items()},
    }
    result["contract_pass"] = all(result["component_pass"].values())
    (case_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (case_dir / "contract.md").write_text(
        "\n".join([
            "# RZ Silver-Mueller contract", "",
            f"- Plotfile: `{args.plotfile}`; threshold: `< {threshold} V/m`.",
            f"- Maximum absolute fields: `Er={maxima['Er']:.9e}`, `Et={maxima['Et']:.9e}`, `Ez={maxima['Ez']:.9e}` V/m.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
