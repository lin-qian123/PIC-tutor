#!/usr/bin/env python
"""Validate the formal-convergence preregistration against current contracts."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def levels(rows: list[dict]) -> list[int]:
    return [row.get("resolution", [row.get("cells")])[0] for row in sorted(rows, key=lambda row: row.get("resolution", [row.get("cells")])[0])]


def slopes(rows: list[dict], key: str) -> list[float]:
    ordered = sorted(rows, key=lambda row: row.get("resolution", [row.get("cells")])[0])
    return [math.log(left[key] / right[key], 2) for left, right in zip(ordered, ordered[1:])]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    spec_path = args.spec or root / "docs/formal-convergence-preregistration.json"
    spec = load(spec_path)
    sources = {name: root / path for name, path in spec["data_sources"].items()}
    data = {name: load(path) for name, path in sources.items()}
    repeat_preflight_path = root / spec["repeat_execution_preflight"]
    repeat_preflight = load(repeat_preflight_path) if repeat_preflight_path.is_file() else {}
    grouped = {}
    for geometry, contract in data.items():
        grouped[geometry] = {
            correction: [row for row in contract["rows"] if row["correction"] == correction]
            for correction in spec["design"]["correction_controls"]
        }
    expected_levels = spec["design"]["resolution_levels"]
    level_checks = {
        geometry: {correction: levels(rows) == expected_levels for correction, rows in controls.items()}
        for geometry, controls in grouped.items()
    }
    finite_checks = {
        geometry: {
            correction: all(
                field in row and isinstance(row[field], (int, float)) and math.isfinite(row[field])
                for row in rows
                for field in spec["contract_metric_fields"][geometry.upper()]
            )
            for correction, rows in controls.items()
        }
        for geometry, controls in grouped.items()
    }
    slope_report = {
        geometry: {
            correction: {
                field: slopes(rows, field)
                for field in spec["observables"]["primary"] + spec["observables"]["secondary"]
                if all(field in row for row in rows)
            }
            for correction, rows in controls.items()
        }
        for geometry, controls in grouped.items()
    }
    checks = {
        "spec_version_present": spec.get("version") == "v0.84-pre",
        "source_contracts_present": all(path.is_file() for path in sources.values()),
        "independent_geometries_declared": spec["design"]["geometry_units"] == ["RZ", "RSPHERE"],
        "resolution_levels_declared": expected_levels == [64, 128, 256],
        "adjacent_ratio_declared": spec["design"]["required_refinement_ratio"] == 2,
        "all_current_levels_present": all(all(values.values()) for values in level_checks.values()),
        "norms_are_explicit": all(spec["norms"][name].get("formula") for name in ("field", "charge")),
        "primary_observables_separate": spec["observables"]["primary"] == ["axis_residual", "off_axis_residual"],
        "no_geometry_pooling": spec["design"]["pooled_geometry_fit"] is False,
        "repeat_requirement_declared": spec["design"]["minimum_independent_families_per_geometry"] >= 2,
        "repeat_runner_contract_present": repeat_preflight_path.is_file(),
        "repeat_runner_keeps_two_rank_requirement": repeat_preflight.get("expected_ranks") == 2 and repeat_preflight.get("single_rank_substitute") == "forbidden",
        "closure_stays_open": spec["current_status"]["current_data_meets_formal_closure"] is False,
    }
    result = {
        "contract": "formal convergence study preregistration",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": spec["classification"],
        "scope": spec["scope"],
        "current_data_meets_formal_closure": False,
        "current_replication": spec["design"]["current_independent_families_per_geometry"],
        "required_replication": spec["design"]["minimum_independent_families_per_geometry"],
        "level_checks": level_checks,
        "finite_checks": finite_checks,
        "pairwise_slope_report": slope_report,
        "blocking_gates": spec["current_status"]["blocking_gates"],
        "repeat_preflight": {
            "classification": repeat_preflight.get("classification"),
            "ready_to_execute": repeat_preflight.get("ready_to_execute"),
        },
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Formal convergence study preregistration audit",
        "",
        f"- classification: `{result['classification']}`",
        f"- preregistration contract: `{'PASS' if result['passed'] else 'FAIL'}`",
        "- formal convergence closure: `OPEN`",
        f"- independent families: `{result['current_replication']}/{result['required_replication']}` per geometry",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines.extend(["", "Formal closure remains open until the required independent family and charge-boundary gates are satisfied."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
