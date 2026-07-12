#!/usr/bin/env python
"""Independent reader-side contract for the 3D EB particle-scrape case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


ELECTRON = "electrons"
EXPECTED_COUNTS = {20: 612, 40: 612, 60: 0}
EB_Z_LO = -8.65e-5
DOMAIN_LO = np.array([-125e-6, -125e-6, -149e-6])
DOMAIN_HI = np.array([125e-6, 125e-6, 1e-6])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    return parser.parse_args()


def snapshot(case_dir: Path, step: int) -> tuple[int, dict[str, float]]:
    ds = yt.load(case_dir / f"diags/diag1000{step:03d}")
    header = ds.index.particle_headers[ELECTRON]
    count = int(header.num_particles)
    if count == 0:
        return count, {}

    data = ds.all_data()
    fields = {
        name: np.asarray(data[ELECTRON, name].v)
        for name in (
            "particle_position_x",
            "particle_position_y",
            "particle_position_z",
            "particle_weight",
        )
    }
    return count, {
        "weight_sum": float(fields["particle_weight"].sum()),
        "x_min": float(fields["particle_position_x"].min()),
        "x_max": float(fields["particle_position_x"].max()),
        "y_min": float(fields["particle_position_y"].min()),
        "y_max": float(fields["particle_position_y"].max()),
        "z_min": float(fields["particle_position_z"].min()),
        "z_max": float(fields["particle_position_z"].max()),
        "z_mean": float(fields["particle_position_z"].mean()),
    }


def main() -> None:
    args = parse_args()
    case_dir = args.case_dir.resolve()
    snapshots = {}
    for step in EXPECTED_COUNTS:
        count, stats = snapshot(case_dir, step)
        snapshots[str(step)] = {"count": count, **stats}

    count_gate = all(
        snapshots[str(step)]["count"] == expected
        for step, expected in EXPECTED_COUNTS.items()
    )
    weight_20 = snapshots["20"]["weight_sum"]
    weight_40 = snapshots["40"]["weight_sum"]
    weight_relative_difference = abs(weight_40 - weight_20) / weight_20
    weight_gate = weight_relative_difference <= 1e-15

    pre_impact_z_gate = snapshots["40"]["z_max"] < EB_Z_LO
    domain_gate = all(
        snapshots["40"][key] >= DOMAIN_LO[index]
        and snapshots["40"][key] <= DOMAIN_HI[index]
        for index, key in enumerate(("x_min", "y_min", "z_min"))
    ) and all(
        snapshots["40"][key] >= DOMAIN_LO[index]
        and snapshots["40"][key] <= DOMAIN_HI[index]
        for index, key in enumerate(("x_max", "y_max", "z_max"))
    )
    result = {
        "case": "test_3d_particle_scrape",
        "mpi": 2,
        "expected_counts": EXPECTED_COUNTS,
        "snapshots": snapshots,
        "eb_z_lower_face": EB_Z_LO,
        "weight_relative_difference_20_to_40": weight_relative_difference,
        "gates": {
            "count_sequence": count_gate,
            "weight_conservation_before_impact": weight_gate,
            "step_40_pre_impact": pre_impact_z_gate,
            "step_40_inside_domain": domain_gate,
        },
        "passed": all((count_gate, weight_gate, pre_impact_z_gate, domain_gate)),
        "evidence_level": "independent reader-side EB absorption contract; not a scraped-buffer ID-set proof",
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Particle scrape contract",
        "",
        "- case: `test_3d_particle_scrape`",
        "- producer: official 3D input, 2 MPI ranks",
        f"- status: `{('PASS' if result['passed'] else 'FAIL')}`",
        f"- count sequence: `{snapshots['20']['count']}/{snapshots['40']['count']}/{snapshots['60']['count']}` at steps 20/40/60",
        f"- pre-impact weight relative difference: `{weight_relative_difference:.3e}`",
        f"- step-40 z max: `{snapshots['40']['z_max']:.12e} m`",
        f"- EB lower z face: `{EB_Z_LO:.12e} m`",
        "",
        "| gate | result |",
        "|---|---|",
    ]
    for name, passed in result["gates"].items():
        lines.append(f"| `{name}` | `{passed}` |")
    lines.extend(
        [
            "",
            "The contract establishes the expected pre-impact and final-absorption sequence and weight conservation before impact. It does not claim a scraped-buffer particle-ID proof because this official case does not expose that buffer as a separate plotfile species.",
        ]
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("particle scrape contract failed")


if __name__ == "__main__":
    main()
