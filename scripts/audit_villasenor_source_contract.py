#!/usr/bin/env python
"""Audit source anchors for the crossing-driven Villasenor deposition skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ANCHORS = {
    "kernel": "VillasenorDepositionShapeNKernel",
    "explicit_entrypoint": "doVillasenorDepositionShapeNExplicit",
    "implicit_entrypoint": "doVillasenorDepositionShapeNImplicit",
    "segment_initialization": "int num_segments = 1",
    "x_crossing_count": "cell_crossings_x = std::abs(i_new-i_old)",
    "y_crossing_count": "cell_crossings_y = std::abs(j_new-j_old)",
    "z_crossing_count": "cell_crossings_z = std::abs(k_new-k_old)",
    "segment_loop": "for (int ns=0; ns<num_segments; ns++)",
    "segment_end_condition": "if (ns == num_segments-1)",
    "segment_fraction_x": "seg_factor_x",
    "segment_fraction_y": "seg_factor_y",
    "segment_fraction_z": "seg_factor_z",
    "x_flux_writeback": "this_Jx",
    "y_flux_writeback": "this_Jy",
    "z_flux_writeback": "this_Jz",
    "segment_continuation": "if (ns < num_segments-1)",
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
        "contract": "Villasenor crossing-driven segment source skeleton",
        "scope": "read-only source audit; not a runtime or kernel numerical regression",
        "checks": checks,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Villasenor source contract audit",
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
        raise SystemExit("Villasenor source contract audit failed")


if __name__ == "__main__":
    main()
