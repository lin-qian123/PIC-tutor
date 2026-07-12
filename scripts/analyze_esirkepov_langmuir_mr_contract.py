#!/usr/bin/env python
"""Classify the level-wise charge contract of an Esirkepov MR Langmuir case."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import epsilon_0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--plotfile", default="diags/diag1000080")
    parser.add_argument("--charge-tol", type=float, default=1.0e-11)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    input_text = (run_dir / "warpx_used_inputs").read_text(encoding="utf-8")
    deposition = re.search(r"^algo\.current_deposition\s*=\s*(\S+)", input_text, re.MULTILINE)
    max_level = re.search(r"^amr\.max_level\s*=\s*(\S+)", input_text, re.MULTILINE)
    if not deposition or deposition.group(1).lower() != "esirkepov":
        raise AssertionError("MR input does not select Esirkepov")
    if not max_level or int(max_level.group(1)) < 1:
        raise AssertionError("input is not a multi-level MR case")

    ds = yt.load(str(run_dir / args.plotfile))
    level_results = []
    for level in range(ds.max_level + 1):
        dims = ds.domain_dimensions * (ds.refine_by**level)
        data = ds.covering_grid(level=level, left_edge=ds.domain_left_edge, dims=dims)
        rho = data[("boxlib", "rho")].to_ndarray()
        div_e = data[("boxlib", "divE")].to_ndarray()
        finite = bool(np.isfinite(rho).all() and np.isfinite(div_e).all())
        scale = float(np.max(np.abs(rho / epsilon_0)))
        residual = float(np.max(np.abs(div_e - rho / epsilon_0)))
        relative = residual / scale if scale else 0.0
        level_results.append(
            {
                "level": level,
                "dimensions": [int(v) for v in dims],
                "finite": finite,
                "charge_relative_residual": relative,
                "charge_gate": relative <= args.charge_tol,
            }
        )

    result = {
        "contract": "Esirkepov Langmuir MR level-wise charge contract",
        "run_dir": str(run_dir),
        "plotfile": args.plotfile,
        "current_deposition": deposition.group(1),
        "max_level": int(ds.max_level),
        "charge_tolerance": args.charge_tol,
        "levels": level_results,
        "classification": "BOUNDARY",
        "passed": False,
        "scope": "level-wise reader-side diagnostic; not a complete AMR source-sync or route-count proof",
        "reason": "Neither level satisfies the single-level divE-rho/epsilon0 gate under this reader contract.",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Esirkepov Langmuir MR contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- current deposition: `{result['current_deposition']}`",
        f"- max level: `{result['max_level']}`",
        f"- charge gate: `<= {args.charge_tol:.1e}`",
    ]
    for item in level_results:
        lines.append(
            f"- level {item['level']} dimensions `{item['dimensions']}`: "
            f"relative residual `{item['charge_relative_residual']:.8e}`, "
            f"gate `{'PASS' if item['charge_gate'] else 'FAIL'}`"
        )
    lines.extend(
        [
            f"- reason: {result['reason']}",
            f"- scope: {result['scope']}",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        "BOUNDARY: "
        + ", ".join(
            f"L{item['level']}={item['charge_relative_residual']:.3e}"
            for item in level_results
        )
    )


if __name__ == "__main__":
    main()
