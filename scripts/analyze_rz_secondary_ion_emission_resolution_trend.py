#!/usr/bin/env python
"""Summarize multi-resolution RZ secondary-emission geometry evidence."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", required=True, metavar="N=DIR")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    cases = []
    for item in args.case:
        resolution, directory = item.split("=", 1)
        n = int(resolution)
        data = json.loads((Path(directory) / "contract.json").read_text(encoding="utf-8"))
        cases.append({"resolution": n, "max_relative_distance": max(data["relative_distance_to_closest_impact"]), "contract_pass": data["contract_pass"]})
    cases.sort(key=lambda item: item["resolution"])

    pairwise = []
    for left, right in zip(cases, cases[1:]):
        ratio = left["max_relative_distance"] / right["max_relative_distance"]
        pairwise.append({
            "from": left["resolution"],
            "to": right["resolution"],
            "error_reduction_factor": ratio,
            "empirical_order": math.log(ratio) / math.log(right["resolution"] / left["resolution"]),
        })
    result = {
        "case": "test_rz_secondary_ion_emission_picmi",
        "resolutions": cases,
        "pairwise": pairwise,
        "all_refined_gates_pass": all(item["contract_pass"] for item in cases[1:]),
        "interpretation": "The three-run trend supports resolution-sensitive EB geometry error. The empirical orders are descriptive only and are not a formal convergence study because the particle/event and callback setup is unchanged and only three resolutions are sampled.",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "resolution-trend.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# RZ secondary-emission resolution trend", "", "| resolution | max relative distance | contract |", "|---:|---:|:---:|"]
    lines.extend(f"| {item['resolution']}x{item['resolution']} | `{item['max_relative_distance']:.8%}` | `{'PASS' if item['contract_pass'] else 'FAIL'}` |" for item in cases)
    lines += ["", "| pair | reduction factor | descriptive empirical order |", "|---|---:|---:|"]
    lines.extend(f"| {item['from']} -> {item['to']} | `{item['error_reduction_factor']:.3f}` | `{item['empirical_order']:.3f}` |" for item in pairwise)
    lines += ["", "The trend supports a resolution-sensitive EB geometry diagnosis. The pairwise orders are descriptive, not a formal convergence-order claim."]
    (args.output_dir / "resolution-trend.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["all_refined_gates_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
