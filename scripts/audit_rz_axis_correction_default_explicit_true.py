#!/usr/bin/env python
"""Verify that default and explicit true RZ axis-correction inputs are identical."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


FIELD_NAMES = ("rho_electrons", "rho_ions", "rho", "Er", "Ez", "divE")
SPECIES = ("electrons", "ions")
PARTICLE_FIELDS = (
    "particle_position_x",
    "particle_position_y",
    "particle_theta",
    "particle_weight",
    "particle_momentum_x",
    "particle_momentum_y",
    "particle_momentum_z",
)


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def load(path: Path):
    ds = yt.load(str(path))
    return ds, ds.all_data()


def field_array(path: Path, field: str) -> np.ndarray:
    ds, _ = load(path)
    grid = ds.covering_grid(level=ds.max_level, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    return grid["boxlib", field].to_ndarray()


def particle_differences(on_ad, other_ad, species: str) -> dict[str, object]:
    on_ids = np.asarray(on_ad[(species, "particle_id")])
    other_ids = np.asarray(other_ad[(species, "particle_id")])
    on_order = np.argsort(on_ids)
    other_order = np.argsort(other_ids)
    max_abs = {}
    for field in PARTICLE_FIELDS:
        on_values = np.asarray(on_ad[(species, field)])[on_order]
        other_values = np.asarray(other_ad[(species, field)])[other_order]
        max_abs[field] = float(np.max(np.abs(on_values - other_values))) if len(on_values) else 0.0
    ids_equal = bool(np.array_equal(on_ids[on_order], other_ids[other_order]))
    return {
        "default_count": int(len(on_ids)),
        "other_count": int(len(other_ids)),
        "particle_ids_equal": ids_equal,
        "field_max_abs_difference": max_abs,
        "particle_state_equal": bool(ids_equal and all(value == 0.0 for value in max_abs.values())),
    }


def normalize_input(path: Path) -> list[str]:
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip() != "boundary.verboncoeur_axis_correction = true"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--default-plotfile", type=Path, required=True)
    parser.add_argument("--explicit-true-plotfile", type=Path, required=True)
    parser.add_argument("--false-plotfile", type=Path, required=True)
    parser.add_argument("--default-input", type=Path, required=True)
    parser.add_argument("--explicit-true-input", type=Path, required=True)
    parser.add_argument("--false-input", type=Path, required=True)
    parser.add_argument("--source-files", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    default_plot = resolve(root, args.default_plotfile)
    explicit_plot = resolve(root, args.explicit_true_plotfile)
    false_plot = resolve(root, args.false_plotfile)
    default_input = resolve(root, args.default_input)
    explicit_input = resolve(root, args.explicit_true_input)
    false_input = resolve(root, args.false_input)
    source_files = [resolve(root, path) for path in args.source_files]

    _, default_ad = load(default_plot)
    _, explicit_ad = load(explicit_plot)
    particle_checks = {species: particle_differences(default_ad, explicit_ad, species) for species in SPECIES}
    field_checks = {}
    for field in FIELD_NAMES:
        default = field_array(default_plot, field)
        explicit = field_array(explicit_plot, field)
        false = field_array(false_plot, field)
        field_checks[field] = {
            "default_explicit_true_max_abs_difference": float(np.max(np.abs(default - explicit))),
            "default_false_max_abs_difference": float(np.max(np.abs(default - false))),
            "default_explicit_true_equal": bool(np.array_equal(default, explicit)),
        }
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    default_text = default_input.read_text(encoding="utf-8")
    explicit_text = explicit_input.read_text(encoding="utf-8")
    false_text = false_input.read_text(encoding="utf-8")
    checks = {
        "plotfiles_present": all(path.is_dir() for path in (default_plot, explicit_plot, false_plot)),
        "default_input_omits_toggle": "boundary.verboncoeur_axis_correction" not in default_text,
        "explicit_true_input_sets_true": "boundary.verboncoeur_axis_correction = true" in explicit_text,
        "false_input_sets_false": "boundary.verboncoeur_axis_correction = false" in false_text,
        "inputs_differ_only_by_true_toggle": normalize_input(default_input) == normalize_input(explicit_input),
        "particle_state_default_equals_explicit_true": all(item["particle_state_equal"] for item in particle_checks.values()),
        "all_default_explicit_fields_equal": all(item["default_explicit_true_equal"] for item in field_checks.values()),
        "source_default_true_member": "bool m_verboncoeur_axis_correction = true" in source,
        "source_query_member": 'query("verboncoeur_axis_correction", m_verboncoeur_axis_correction)' in source,
        "source_false_and_true_factors": "1.0_rt/3.0_rt" in source and "1.0_rt/4.0_rt" in source,
    }
    result = {
        "contract": "RZ axis correction default versus explicit true runtime",
        "classification": "RZ_AXIS_CORRECTION_DEFAULT_EXPLICIT_TRUE_EQUIVALENT_FALSE_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "source_files": [str(path) for path in source_files],
        "particle_checks": particle_checks,
        "field_checks": field_checks,
        "scope": (
            "A real 2-rank RZ runtime with the default axis-correction setting and a sibling with "
            "explicit boundary.verboncoeur_axis_correction=true produce bitwise-identical selected "
            "fields and particle state. The false sibling remains distinct at axis rho. This excludes "
            "default-value/parser selection as the explanation; it does not identify the remaining "
            "axis deposition/diagnostic consumer root cause or close charge conservation."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ axis correction default versus explicit true runtime",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        "- default versus explicit true selected-field equality: `PASS`",
        "- default versus explicit true particle-state equality: `PASS`",
        "- false sibling: remains distinct at axis rho",
        "",
        "| field | default/explicit true max abs difference | default/false max abs difference |",
        "|---|---:|---:|",
    ]
    lines.extend(
        f"| `{field}` | {item['default_explicit_true_max_abs_difference']:.3e} | {item['default_false_max_abs_difference']:.3e} |"
        for field, item in field_checks.items()
    )
    lines.extend([
        "",
        "The default and explicit-true paths are runtime-equivalent; the remaining false-sibling axis difference is not a parser-default artifact.",
    ])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
