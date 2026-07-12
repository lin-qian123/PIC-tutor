#!/usr/bin/env python
"""Audit source anchors for the explicit Esirkepov deposition skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ANCHORS = {
    "entrypoint": "doEsirkepovDepositionShapeN",
    "shifted_shape_helper": "Compute_shifted_shape_factor",
    "inverse_dt_area": "invdtd",
    "one_third": "one_third = 1.0_rt / 3.0_rt",
    "one_sixth": "one_sixth = 1.0_rt / 6.0_rt",
    "x_prefix_accumulator": "amrex::Real sdxi = 0._rt",
    "y_prefix_accumulator": "amrex::Real sdyj = 0._rt",
    "z_prefix_accumulator": "amrex::Real sdzk = 0._rt",
    "x_old_new_difference": "sx_old[i] - sx_new[i]",
    "y_old_new_difference": "sy_old[j] - sy_new[j]",
    "z_old_new_difference": "sz_old[k] - sz_new[k]",
    "x_current_writeback": "Jx_arr",
    "y_current_writeback": "Jy_arr",
    "z_current_writeback": "Jz_arr",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--warpx-root",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "warpx",
    )
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    source_path = args.warpx_root / "Source/Particles/Deposition/CurrentDeposition.H"
    source = source_path.read_text(encoding="utf-8")
    checks = {
        name: {
            "needle": needle,
            "count": source.count(needle),
            "passed": source.count(needle) > 0,
        }
        for name, needle in ANCHORS.items()
    }
    result = {
        "source": str(source_path),
        "source_bytes": len(source.encode("utf-8")),
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["passed"] for item in checks.values()),
        "passed": all(item["passed"] for item in checks.values()),
        "contract": "explicit Esirkepov old/new-shape source skeleton",
        "scope": "read-only source audit; not a runtime or kernel numerical regression",
        "checks": checks,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Esirkepov source contract audit",
        "",
        f"- source: `{source_path}`",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
    ]
    lines.extend(
        f"- `{name}`: `{item['count']}` occurrence(s)"
        for name, item in checks.items()
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("Esirkepov source contract audit failed")


if __name__ == "__main__":
    main()
