#!/usr/bin/env python
"""Analyze the official particle_pusher Higuera-Cary contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plotfile", type=Path)
    parser.add_argument("--pusher", default="higuera")
    parser.add_argument("--tolerance", type=float, default=1.0e-3)
    parser.add_argument("--allow-failure", action="store_true")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    ds = yt.load(str(args.plotfile))
    ad = ds.all_data()
    x = ad["particle_position_x"].to_ndarray()
    max_abs_x = float(abs(x).max())
    result = {
        "plotfile": str(args.plotfile),
        "current_time": float(ds.current_time),
        "particle_count": int(x.size),
        "max_abs_position_x": max_abs_x,
        "tolerance": args.tolerance,
        "passed": max_abs_x < args.tolerance,
        "pusher": args.pusher,
        "contract": "force-free pusher keeps x approximately zero",
    }

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        status = "PASS" if result["passed"] else "FAIL"
        args.output_md.write_text(
            "# Particle pusher contract\n\n"
            f"- status: `{status}`\n"
            f"- plotfile: `{result['plotfile']}`\n"
            f"- current time: `{result['current_time']:.16g}`\n"
            f"- particle count: `{result['particle_count']}`\n"
            f"- max abs position x: `{result['max_abs_position_x']:.8e}`\n"
            f"- tolerance: `{result['tolerance']:.8e}`\n"
            f"- pusher: `{result['pusher']}`\n"
            f"- contract: {result['contract']}\n",
            encoding="utf-8",
        )

    print(json.dumps(result, indent=2))
    if not result["passed"] and not args.allow_failure:
        raise SystemExit("particle pusher contract failed")


if __name__ == "__main__":
    main()
