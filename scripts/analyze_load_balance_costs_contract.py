#!/usr/bin/env python
"""Summarize WarpX LoadBalanceCosts efficiency before/after rebalancing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.run_dir)
    path = root / "diags/reducedfiles/LBC.txt"
    data = np.genfromtxt(path)
    if data.ndim == 1:
        data = data[None, :]
    header = path.read_text().splitlines()[0]
    unique_headers = ["".join(ch for ch in word if not ch.isdigit()) for word in header.split()][2:]
    n_data_fields = len(set(unique_headers))
    rows = []
    for index, row in enumerate(data):
        costs = row[2::n_data_fields]
        ranks = row[3::n_data_fields].astype(int)
        rank_to_cost = {rank: 0.0 for rank in set(ranks)}
        for cost, rank in zip(costs, ranks):
            rank_to_cost[rank] += cost
        rank_costs = np.array(list(rank_to_cost.values()))
        efficiency = float(np.mean(rank_costs / rank_costs.max()))
        rows.append(
            {
                "row": index,
                "step": int(row[0]),
                "time": float(row[1]),
                "box_count": int(len(costs)),
                "rank_count": int(len(rank_costs)),
                "rank_costs": {str(rank): float(cost) for rank, cost in rank_to_cost.items()},
                "efficiency": efficiency,
            }
        )

    result = {
        "run_dir": str(root),
        "data_fields_per_box": n_data_fields,
        "rows": rows,
        "efficiency_before": rows[1]["efficiency"],
        "efficiency_after": rows[2]["efficiency"],
        "improved": rows[1]["efficiency"] < rows[2]["efficiency"],
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# LoadBalanceCosts contract report",
                "",
                f"- cost fields per box: `{result['data_fields_per_box']}`",
                f"- efficiency before load balance: `{result['efficiency_before']:.6f}`",
                f"- efficiency after load balance: `{result['efficiency_after']:.6f}`",
                f"- improvement gate: `{'PASS' if result['improved'] else 'FAIL'}`",
                "",
                "The efficiency metric follows WarpX's official analysis: sum box costs per rank, normalize by the maximum rank cost, then average across ranks. Rows 1 and 2 are the official before/after comparison.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not result["improved"]:
        raise SystemExit("LoadBalanceCosts efficiency did not improve")


if __name__ == "__main__":
    main()
