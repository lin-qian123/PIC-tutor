#!/usr/bin/env python
"""Deterministic regression checks for the sampled Poincare classifier."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "classify_higuera_poincare_topology.py"
SPEC = importlib.util.spec_from_file_location("higuera_topology", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_ordering_separates_time_artifact() -> None:
    square = [(-1.0, -1.0), (1.0, 1.0), (-1.0, 1.0), (1.0, -1.0)]
    assert MODULE.segment_intersections(square, square) // 2 == 1
    ordered = MODULE.angularly_ordered_points(square)
    assert MODULE.segment_intersections(ordered, ordered) // 2 == 0
    assert abs(MODULE.polygon_area(ordered)) > 0.0


def test_nested_angular_candidates_do_not_cross() -> None:
    outer = [(2.0, 0.0), (0.0, 2.0), (-2.0, 0.0), (0.0, -2.0)]
    inner = [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]
    outer = MODULE.angularly_ordered_points(outer)
    inner = MODULE.angularly_ordered_points(inner)
    assert MODULE.segment_intersections(outer, inner) == 0


def test_short_input_remains_insufficient() -> None:
    points = [
        {"y_over_L0": 0.0, "py": 0.5, "I_y": 0.25},
        {"y_over_L0": 0.5, "py": 0.0, "I_y": 0.25},
        {"y_over_L0": 0.0, "py": -0.5, "I_y": 0.25},
    ]
    case = {
        "pusher": "boris",
        "species": {
            "p05": {"points": points, "invariant_ledger": {"I_y_initial": 0.25}},
            "p10": {"points": points, "invariant_ledger": {"I_y_initial": 0.5}},
        },
    }
    result = MODULE.classify_case(case)
    assert result["status"] == "INSUFFICIENT_SAMPLING"
    assert result["sampling_sufficient"] is False


def main() -> None:
    test_ordering_separates_time_artifact()
    test_nested_angular_candidates_do_not_cross()
    test_short_input_remains_insufficient()
    print("higuera topology deterministic tests: PASS")


if __name__ == "__main__":
    main()
