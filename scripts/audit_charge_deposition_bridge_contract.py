#!/usr/bin/env python
"""Audit the source-level ABLASTR charge-deposition bridge contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ANCHORS = {
    "WarpXParticleContainer.cpp": [
        "time_shift_delta = (icomp == 0",
        "doChargeDepositionSharedShapeN<1>",
        "ablastr::particles::deposit_charge",
        "local_rho",
        "lockAdd(local_rho",
    ],
    "DepositCharge.H": [
        "depos_lev.value() == (lev-1)",
        "numParticlesOutOfRange",
        "amrex::make_alias",
        "doChargeDepositionShapeN<1>",
    ],
    "ChargeDeposition.H": [
        "q*wp[ip]*invvol",
        "rho_type = rho_fab.box().type()",
        "Gpu::Atomic::AddNoRet",
        "WARPX_DIM_RZ",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path("../warpx"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    source_map = {
        "WarpXParticleContainer.cpp": args.warpx_root / "Source/Particles/WarpXParticleContainer.cpp",
        "DepositCharge.H": args.warpx_root / "Source/ablastr/particles/DepositCharge.H",
        "ChargeDeposition.H": args.warpx_root / "Source/Particles/Deposition/ChargeDeposition.H",
    }

    rows = []
    for name, needles in ANCHORS.items():
        text = source_map[name].read_text(encoding="utf-8")
        for needle in needles:
            rows.append({"file": name, "needle": needle, "found": needle in text})
    missing = [row for row in rows if not row["found"]]
    result = {
        "contract": "ABLASTR charge-deposition bridge source contract",
        "anchor_count": len(rows),
        "missing_count": len(missing),
        "passed": not missing,
        "scope": "source mapping only; not a numerical charge-deposition regression",
        "anchors": rows,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ABLASTR charge-deposition bridge source contract",
        "",
        f"- anchors: `{len(rows)}`",
        f"- missing: `{len(missing)}`",
        f"- status: `{'PASS' if not missing else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| source file | anchor | status |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| `{row['file']}` | `{row['needle']}` | `{'PASS' if row['found'] else 'FAIL'}` |"
        for row in rows
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if missing:
        raise SystemExit("missing bridge anchors: " + ", ".join(row["needle"] for row in missing))
    print(f"PASS: {len(rows)} charge-deposition bridge anchors")


if __name__ == "__main__":
    main()
