#!/usr/bin/env python
"""Independent residual-field contract for the RZ PSATD-PML test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotfile", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=2.0)
    args = parser.parse_args()

    yt.funcs.mylog.setLevel(0)
    ds = yt.load(str(args.plotfile.resolve()))
    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    fields = {
        name: np.asarray(grid["boxlib", name].to_ndarray())
        for name in ("Er", "Ez")
    }
    finite = {name: bool(np.isfinite(value).all()) for name, value in fields.items()}
    maxima = {f"max_abs_{name}": float(np.max(np.abs(value))) for name, value in fields.items()}
    max_field = max(maxima.values())
    result = {
        "contract": "RZ PSATD radial-PML residual-field contract",
        "plotfile": str(args.plotfile.resolve()),
        "domain_dimensions": [int(value) for value in np.asarray(ds.domain_dimensions)],
        "finite_fields": finite,
        **maxima,
        "max_abs_field": max_field,
        "tolerance": args.tolerance,
        "passed": bool(all(finite.values()) and max_field < args.tolerance),
        "scope": "independent reader-side RZ residual-field check on the official 2-rank producer",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        "# RZ PSATD-PML 2-rank contract\n\n"
        f"- domain dimensions: `{result['domain_dimensions']}`\n"
        f"- max |Er|: `{result['max_abs_Er']:.8e}`\n"
        f"- max |Ez|: `{result['max_abs_Ez']:.8e}`\n"
        f"- max field: `{max_field:.8e}`\n"
        f"- gate: `< {args.tolerance:.1f}`\n"
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("RZ PSATD-PML contract failed")


if __name__ == "__main__":
    main()
