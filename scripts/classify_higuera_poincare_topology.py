#!/usr/bin/env python
"""Classify sampled Higuera-Cary Poincare polygons without overclaiming topology."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


MIN_POINTS_FOR_TOPOLOGY = 16
MAX_REFERENCE_CURVE_RELATIVE_RESIDUAL = 1.0e-2
B_COEFF = 2.0


def orientation(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def proper_intersection(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    d: tuple[float, float],
) -> bool:
    ab_c = orientation(a, b, c)
    ab_d = orientation(a, b, d)
    cd_a = orientation(c, d, a)
    cd_b = orientation(c, d, b)
    return ab_c * ab_d < 0.0 and cd_a * cd_b < 0.0


def segment_intersections(first: list[tuple[float, float]], second: list[tuple[float, float]]) -> int:
    count = 0
    for i, point in enumerate(first):
        next_point = first[(i + 1) % len(first)]
        for j, other in enumerate(second):
            other_next = second[(j + 1) % len(second)]
            if proper_intersection(point, next_point, other, other_next):
                count += 1
    return count


def polygon_area(points: list[tuple[float, float]]) -> float:
    x = np.asarray([point[0] for point in points])
    y = np.asarray([point[1] for point in points])
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def invariant_band_order(case: dict) -> dict:
    bands = {
        species: (
            min(float(point["I_y"]) for point in data["points"]),
            max(float(point["I_y"]) for point in data["points"]),
        )
        for species, data in case["species"].items()
    }
    ordered = sorted(bands, key=lambda species: sum(bands[species]) / 2.0)
    adjacent_disjoint = all(bands[first][1] < bands[second][0] for first, second in zip(ordered, ordered[1:]))
    return {
        "bands": bands,
        "order": ordered,
        "adjacent_bands_disjoint": adjacent_disjoint,
        "invariant_order_gate_passed": adjacent_disjoint,
    }


def analytic_curve_reference(case: dict) -> dict:
    rows = {}
    for species, data in case["species"].items():
        target = float(data["invariant_ledger"]["I_y_initial"])
        residuals = []
        for point in data["points"]:
            y = float(point["y_over_L0"])
            py = float(point["py"])
            reference_i = py * py + (0.5 * B_COEFF * y * y) ** 2
            residuals.append(abs(reference_i - target) / max(abs(target), 1.0e-30))
        rows[species] = {
            "I_y_reference": target,
            "relative_residual_max": max(residuals) if residuals else None,
            "reference_curve_gate_passed": bool(residuals)
            and max(residuals) <= MAX_REFERENCE_CURVE_RELATIVE_RESIDUAL,
        }
    ordered = sorted(rows, key=lambda species: rows[species]["I_y_reference"])
    nested = all(
        rows[first]["I_y_reference"] < rows[second]["I_y_reference"]
        for first, second in zip(ordered, ordered[1:])
    )
    return {
        "equation": f"p_y^2 + (b*y_over_L0^2/2)^2 = I_y, with b={B_COEFF:g} and canonical p_z=0",
        "maximum_allowed_relative_residual": MAX_REFERENCE_CURVE_RELATIVE_RESIDUAL,
        "curves": rows,
        "order": ordered,
        "nested_reference_order_passed": nested,
        "reference_curve_gate_passed": nested and all(row["reference_curve_gate_passed"] for row in rows.values()),
    }


def classify_case(case: dict) -> dict:
    polygons = {
        species: [(float(point["y_over_L0"]), float(point["py"])) for point in data["points"]]
        for species, data in case["species"].items()
    }
    point_counts = {species: len(points) for species, points in polygons.items()}
    enough_points = all(count >= MIN_POINTS_FOR_TOPOLOGY for count in point_counts.values())
    self_intersections = {
        species: segment_intersections(points, points) // 2 if len(points) >= 3 else 0
        for species, points in polygons.items()
    }
    pairwise_intersections = {}
    names = sorted(polygons)
    for index, first_name in enumerate(names):
        for second_name in names[index + 1 :]:
            first = polygons[first_name]
            second = polygons[second_name]
            pairwise_intersections[f"{first_name}__{second_name}"] = (
                segment_intersections(first, second) if enough_points else None
            )
    return {
        "pusher": case["pusher"],
        "point_counts": point_counts,
        "minimum_points_for_topology": MIN_POINTS_FOR_TOPOLOGY,
        "sampling_sufficient": enough_points,
        "invariant_order": invariant_band_order(case),
        "analytic_curve_reference": analytic_curve_reference(case),
        "signed_polygon_area": {
            species: polygon_area(points) if len(points) >= 3 else None for species, points in polygons.items()
        },
        "self_intersection_candidates": self_intersections,
        "pairwise_intersection_candidates": pairwise_intersections,
        "topology_gate_passed": False,
        "status": "INSUFFICIENT_SAMPLING" if not enough_points else "REVIEW_REQUIRED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.input_json.read_text(encoding="utf-8"))
    cases = [classify_case(case) for case in source["cases"]]
    checks = {
        "source_section_contract_passed": bool(source.get("passed")),
        "three_pushers_present": {case["pusher"] for case in cases} == {"boris", "vay", "higuera"},
        "topology_classifier_executed": True,
    }
    sampling_sufficient = all(case["sampling_sufficient"] for case in cases)
    invariant_order_gate_passed = all(case["invariant_order"]["invariant_order_gate_passed"] for case in cases)
    analytic_reference_gate_passed = all(case["analytic_curve_reference"]["reference_curve_gate_passed"] for case in cases)
    signatures = [
        (
            tuple(sorted(case["self_intersection_candidates"].items())),
            tuple(sorted(case["pairwise_intersection_candidates"].items())),
        )
        for case in cases
    ]
    candidate_signature_consistent = len(set(signatures)) == 1
    if sampling_sufficient:
        status = "REVIEW_REQUIRED"
        reason = "The invariant-order gate passes, but time-ordered polyline intersections need a validated section-point ordering and denser reference orbit before they can be promoted to resonance-island or trajectory-crossing evidence."
        next_required_evidence = "Review the section-point ordering against a denser reference orbit and add a validated topology definition before enabling the physical gate."
    else:
        status = "INSUFFICIENT_SAMPLING"
        reason = "The available runtime contract contains too few section points per orbit. Polygon crossings at this sampling density are candidates, not a reliable resonance-island or trajectory-crossing classification."
        next_required_evidence = "Rerun the three pushers with enough positive-p_x crossings to meet the minimum point threshold, then review self- and pairwise-intersection candidates against a denser reference orbit."
    result = {
        "contract": "Higuera-Cary sampled Poincare topology classifier",
        "passed": all(checks.values()),
        "checks": checks,
        "topology_gate_passed": False,
        "invariant_order_gate_passed": invariant_order_gate_passed,
        "analytic_reference_curve_gate_passed": analytic_reference_gate_passed,
        "status": status,
        "minimum_points_for_topology": MIN_POINTS_FOR_TOPOLOGY,
        "candidate_signature_consistent_across_pushers": candidate_signature_consistent,
        "cases": cases,
        "evidence_boundary": {
            "topology_gate_promoted": False,
            "reason": reason,
            "next_required_evidence": next_required_evidence,
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Higuera-Cary sampled Poincare topology classifier",
        "",
        f"Status: `{result['status']}`; topology gate: `{'PASS' if result['topology_gate_passed'] else 'NOT_PROMOTED'}`.",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", "| pusher | min/max point count | sampling | self-intersection candidates |", "|---|---:|:---:|---:|"]
    for case in cases:
        counts = list(case["point_counts"].values())
        lines.append(
            f"| `{case['pusher']}` | `{min(counts)}/{max(counts)}` | `{'READY' if case['sampling_sufficient'] else 'INSUFFICIENT'}` | `{case['self_intersection_candidates']}` |"
        )
    lines += [
        "",
        f"Invariant-order gate: `{'PASS' if result['invariant_order_gate_passed'] else 'FAIL'}`.",
        f"Analytic quartic reference-curve gate: `{'PASS' if result['analytic_reference_curve_gate_passed'] else 'FAIL'}`.",
        result["evidence_boundary"]["reason"],
        "",
        result["evidence_boundary"]["next_required_evidence"],
    ]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
