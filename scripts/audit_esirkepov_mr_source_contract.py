#!/usr/bin/env python
"""Audit the source-level AMR routing skeleton used by Esirkepov deposition."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ANCHORS = {
    "MultiParticleContainer.cpp": [
        "fields.get(current_fp_string",
        "FieldType::current_buf",
        "pc->Evolve(fields, lev, current_fp_string",
    ],
    "WarpXParticleContainer.cpp": [
        "depos_lev==(lev-1)",
        "tile box is different when depositing in the buffers",
        "amrex::coarsen(pti.tilebox(),ref_ratio)",
        "WarpX::LowerCorner(tilebox, depos_lev",
        "domain_double",
        "do_cropping",
    ],
    "WarpX.cpp": [
        "alloc_init(FieldType::current_buf",
        "current_buffer_masks[lev]",
    ],
    "WarpXEvolve.cpp": [
        "void WarpX::SyncCurrentAndRho",
        "SyncCurrent(current_fp_string)",
        "AddCurrentFromFineLevelandSumBoundary",
        "FieldType::current_buf",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path("../warpx"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    source_map = {
        "MultiParticleContainer.cpp": args.warpx_root / "Source/Particles/MultiParticleContainer.cpp",
        "WarpXParticleContainer.cpp": args.warpx_root / "Source/Particles/WarpXParticleContainer.cpp",
        "WarpX.cpp": args.warpx_root / "Source/WarpX.cpp",
        "WarpXEvolve.cpp": args.warpx_root / "Source/Evolve/WarpXEvolve.cpp",
    }
    results = []
    for name, patterns in ANCHORS.items():
        text = source_map[name].read_text(encoding="utf-8")
        for pattern in patterns:
            found = re.search(re.escape(pattern), text) is not None
            results.append({"file": name, "pattern": pattern, "found": found})

    missing = [item for item in results if not item["found"]]
    result = {
        "contract": "Esirkepov AMR routing source contract",
        "warpx_root": str(args.warpx_root.resolve()),
        "anchor_count": len(results),
        "missing_count": len(missing),
        "passed": not missing,
        "scope": "source skeleton only; does not prove runtime route counts or numerical source closure",
        "anchors": results,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Esirkepov AMR routing source contract",
        "",
        f"- anchors: `{len(results)}`",
        f"- missing: `{len(missing)}`",
        f"- status: `{'PASS' if not missing else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| source file | anchor | status |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| `{item['file']}` | `{item['pattern']}` | `{'PASS' if item['found'] else 'FAIL'}` |"
        for item in results
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if missing:
        raise SystemExit("missing source anchors: " + ", ".join(item["pattern"] for item in missing))
    print(f"PASS: {len(results)} AMR routing source anchors")


if __name__ == "__main__":
    main()
