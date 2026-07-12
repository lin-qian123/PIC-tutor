#!/usr/bin/env python
"""Independent openPMD contract for the RZ EB scraping cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from openpmd_viewer import OpenPMDTimeSeries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--mode", choices=("full", "filter"), required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def particle(ts: OpenPMDTimeSeries, field: str, iteration: int) -> np.ndarray:
    (values,) = ts.get_particle([field], iteration=iteration)
    return np.asarray(values)


def main() -> None:
    args = parse_args()
    case_dir = args.case_dir.resolve()
    full = OpenPMDTimeSeries(str(case_dir / "diags/diag2"))
    scraped = OpenPMDTimeSeries(str(case_dir / "diags/diag3/particles_at_eb"))

    iterations = np.asarray(full.iterations, dtype=int)
    scrape_iteration = int(scraped.iterations[-1])
    step_scraped = particle(scraped, "stepScraped", scrape_iteration)
    scraped_ids = particle(scraped, "id", scrape_iteration)
    scraped_weights = particle(scraped, "w", scrape_iteration)
    scraped_z = particle(scraped, "z", scrape_iteration)
    initial_ids = particle(full, "id", int(iterations[0]))
    final_ids = particle(full, "id", int(iterations[-1]))
    initial_weight = float(particle(full, "w", int(iterations[0])).sum())
    final_weight = float(particle(full, "w", int(iterations[-1])).sum())
    scraped_weight = float(scraped_weights.sum())

    remaining_counts = []
    scraped_counts = []
    remaining_weights = []
    for iteration in iterations:
        weights = particle(full, "w", int(iteration))
        remaining_counts.append(len(weights))
        remaining_weights.append(float(weights.sum()))
        scraped_counts.append(int(np.count_nonzero(step_scraped <= iteration)))

    remaining_counts = np.asarray(remaining_counts)
    scraped_counts = np.asarray(scraped_counts)
    remaining_weights = np.asarray(remaining_weights)

    if args.mode == "full":
        count_conservation = np.all(remaining_counts + scraped_counts == remaining_counts[0])
        id_conservation = np.array_equal(
            np.sort(initial_ids), np.sort(np.concatenate((scraped_ids, final_ids)))
        )
        filter_gate = True
    else:
        count_conservation = np.all(2 * scraped_counts + remaining_counts == remaining_counts[0])
        id_conservation = None
        filter_gate = bool(np.all(scraped_z > 0))

    weight_relative_error = abs(final_weight + (scraped_weight if args.mode == "full" else 2 * scraped_weight) - initial_weight) / initial_weight
    result = {
        "case": "test_rz_scraping_filter" if args.mode == "filter" else "test_rz_scraping",
        "mode": args.mode,
        "mpi": 2,
        "iterations": iterations.tolist(),
        "remaining_counts": remaining_counts.tolist(),
        "scraped_counts": scraped_counts.tolist(),
        "initial_particle_count": int(remaining_counts[0]),
        "final_particle_count": int(remaining_counts[-1]),
        "scraped_particle_count": int(len(scraped_ids)),
        "initial_weight": initial_weight,
        "final_weight": final_weight,
        "scraped_weight": scraped_weight,
        "weight_relative_error": float(weight_relative_error),
        "scraped_step_min": float(step_scraped.min()),
        "scraped_step_max": float(step_scraped.max()),
        "scraped_z_min": float(scraped_z.min()),
        "scraped_z_max": float(scraped_z.max()),
        "gates": {
            "count_conservation": bool(count_conservation),
            "weight_conservation": bool(weight_relative_error <= 1e-15),
            "id_conservation": id_conservation,
            "filter_z_positive": bool(filter_gate),
        },
        "passed": bool(count_conservation and weight_relative_error <= 1e-15 and (id_conservation is not False) and filter_gate),
        "evidence_level": "independent openPMD scraping contract; full mode includes ID conservation, filter mode includes z>0 selection",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# RZ scraping contract",
        "",
        f"- case: `{result['case']}`",
        "- producer: official RZ input, 2 MPI ranks",
        f"- status: `{('PASS' if result['passed'] else 'FAIL')}`",
        f"- remaining count first/last: `{remaining_counts[0]}/{remaining_counts[-1]}`",
        f"- scraped count: `{len(scraped_ids)}`",
        f"- weight relative error: `{weight_relative_error:.3e}`",
        f"- scraped step range: `{step_scraped.min():.0f}..{step_scraped.max():.0f}`",
        f"- scraped z range: `{scraped_z.min():.6f}..{scraped_z.max():.6f}`",
        "",
        "| gate | result |",
        "|---|---|",
    ]
    for name, passed in result["gates"].items():
        lines.append(f"| `{name}` | `{passed}` |")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("RZ scraping contract failed")


if __name__ == "__main__":
    main()
