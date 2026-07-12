#!/usr/bin/env python
"""Summarize the local Boris/Vay/Higuera-Cary force-free comparison."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for pusher in ("boris", "vay", "higuera"):
        path = args.root / pusher / "contract.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append(
            {
                "pusher": pusher,
                "max_abs_position_x": data["max_abs_position_x"],
                "tolerance": data["tolerance"],
                "passed": data["passed"],
                "current_time": data["current_time"],
            }
        )
    result = {
        "case": "official particle_pusher force-free input with pusher-only sibling override",
        "comparison_scope": "local sibling comparison, not an official CMake regression",
        "rows": rows,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Particle pusher sibling comparison",
        "",
        "This is a local sibling comparison using the official force-free input with only `algo.particle_pusher` overridden.",
        "It is not an independent official CMake regression.",
        "",
        "| pusher | current time | max abs x | 1e-3 gate | result |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        status = "PASS" if row["passed"] else "FAIL (expected contrast)"
        lines.append(
            f"| `{row['pusher']}` | `{row['current_time']:.16g}` | "
            f"`{row['max_abs_position_x']:.8e}` | `< {row['tolerance']:.1e}` | {status} |"
        )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
