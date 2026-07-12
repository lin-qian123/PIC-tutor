#!/usr/bin/env python
"""Audit the paper-to-WarpX notation bridge for the Esirkepov current kernel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    source_path = args.warpx_root / "Source/Particles/Deposition/CurrentDeposition.H"
    text = source_path.read_text(encoding="utf-8")
    anchors = [
        ("esirkepov_entrypoint", "doEsirkepovDepositionShapeN"),
        ("inverse_dt_cell_area", "amrex::XDim3 const invdtd = amrex::XDim3{(1.0_rt/dt)*dinv.y*dinv.z"),
        ("old_new_shape_x", "Compute_shifted_shape_factor< depos_order > compute_shifted_shape_factor"),
        ("old_new_x_arrays", "double sx_new[depos_order + 3] = {0.};"),
        ("old_new_y_arrays", "double sy_new[depos_order + 3] = {0.};"),
        ("old_new_z_arrays", "double sz_new[depos_order + 3] = {0.};"),
        ("directional_prefix_x", "amrex::Real sdxi = 0._rt;"),
        ("directional_prefix_y", "amrex::Real sdyj = 0._rt;"),
        ("directional_prefix_z", "amrex::Real sdzk = 0._rt;"),
        ("mixed_average_coefficients", "one_third*(sy_new[j]*sz_new[k] + sy_old[j]*sz_old[k])"),
        ("mixed_average_cross_terms", "one_sixth*(sy_new[j]*sz_old[k] + sy_old[j]*sz_new[k])"),
        ("jx_writeback", "&Jx_arr(lo.x+i_new-1+i, lo.y+j_new-1+j, lo.z+k_new-1+k)"),
        ("jy_writeback", "&Jy_arr(lo.x+i_new-1+i, lo.y+j_new-1+j, lo.z+k_new-1+k)"),
        ("jz_writeback", "&Jz_arr(lo.x+i_new-1+i, lo.y+j_new-1+j, lo.z+k_new-1+k)"),
    ]
    checks = []
    lines = text.splitlines()
    for name, needle in anchors:
        matches = [index for index, line in enumerate(lines, start=1) if needle in line]
        checks.append({"name": name, "needle": needle, "matched": bool(matches), "line_numbers": matches})

    result = {
        "contract": "Esirkepov paper-to-WarpX notation bridge",
        "source": str(source_path),
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["matched"] for item in checks),
        "passed": all(item["matched"] for item in checks),
        "checks": checks,
        "notation": {
            "W1": "x-direction shape difference accumulated into sdxi and Jx",
            "W2": "y-direction shape difference accumulated into sdyj and Jy",
            "W3": "z-direction shape difference accumulated into sdzk and Jz",
            "transverse_factor": "one_third/one_sixth old-new tensor-product average",
            "normalization": "invdtd.direction = transverse inverse cell area / dt",
        },
        "scope": "source mapping only; does not claim publisher-PDF line-by-line equivalence or all geometry/order runtime coverage",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    status = "PASS" if result["passed"] else "FAIL"
    lines_out = [
        "# Esirkepov paper-to-WarpX notation contract",
        "",
        f"- status: `{status}`",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        f"- source: `{source_path}`",
        "- `W1/W2/W3`: x/y/z directional old-new shape differences mapped to `sdxi/sdyj/sdzk`",
        "- transverse factor: `one_third/one_sixth` mixed old/new tensor-product average",
        "- normalization: `invdtd` uses transverse inverse cell area divided by `dt`",
        f"- scope: {result['scope']}",
        "",
        "| anchor | status | source lines |",
        "|---|:---:|---:|",
    ]
    for item in checks:
        lines_out.append(
            f"| `{item['name']}` | {'PASS' if item['matched'] else 'FAIL'} | `{item['line_numbers']}` |"
        )
    (args.output_dir / "contract.md").write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
