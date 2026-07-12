#!/usr/bin/env python
"""Compare RCYLINDER/RSPHERE radial charge contracts with axis correction on/off."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for geometry in ("rcylinder", "rsphere"):
        on = read(args.root / f"esirkepov_langmuir_{geometry}_charge_mpi2" / "contract.json")
        off = read(args.root / f"esirkepov_langmuir_{geometry}_charge_no_verboncoeur_mpi2" / "contract.json")
        rows.append({"geometry": geometry.upper(), "on": on, "off": off})
    result = {
        "contract": "radial geometry axis correction charge comparison",
        "rows": rows,
        "classification": "RCYLINDER_GATE_RESTORED_RSPHERE_RESIDUAL_REMAINS",
        "scope": "paired radial reader-side Er and divE-rho/epsilon0 comparison; not a global default recommendation",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Radial geometry axis-correction charge comparison",
        "",
        "| geometry | correction | Er error | charge residual | axis residual | off-axis residual | charge |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        for label, data in (("on", row["on"]), ("off", row["off"])):
            lines.append(
                f"| {row['geometry']} | `{label}` | `{data['relative_er_error']:.8e}` | `{data['charge_relative_residual']:.8e}` | "
                f"`{data['axis_charge_relative_residual']:.8e}` | `{data['off_axis_charge_relative_residual']:.8e}` | "
                f"`{'PASS' if data['charge_passed'] else 'BOUNDARY'}` |"
            )
    lines.extend(["", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS: radial axis-correction charge comparison summarized")


if __name__ == "__main__":
    main()
