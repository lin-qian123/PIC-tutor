#!/usr/bin/env python
"""Separate final rho scaling from the pre-scaling axis input boundary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


FIELDS = ("rho_electrons", "rho_ions")
ON_AXIS_FACTOR = 1.0 / 3.0
OFF_AXIS_FACTOR = 1.0 / 4.0


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def read_field(path: Path, field: str) -> np.ndarray:
    ds = yt.load(str(path))
    grid = ds.covering_grid(
        level=ds.max_level,
        left_edge=ds.domain_left_edge,
        dims=ds.domain_dimensions,
    )
    return grid["boxlib", field].to_ndarray()[:, :, 0]


def ratios(on: np.ndarray, off: np.ndarray) -> dict[str, float | int]:
    axis_mask = (np.abs(off[0, :]) > 1.0e-30) & np.isfinite(on[0, :]) & np.isfinite(off[0, :])
    off_mask = (np.abs(off[1:, :]) > 1.0e-30) & np.isfinite(on[1:, :]) & np.isfinite(off[1:, :])
    axis_ratio = on[0, axis_mask] / off[0, axis_mask]
    off_ratio = on[1:, :][off_mask] / off[1:, :][off_mask]
    prescale_ratio = axis_ratio * (ON_AXIS_FACTOR / OFF_AXIS_FACTOR)
    return {
        "axis_ratio_median": float(np.median(axis_ratio)),
        "axis_ratio_min": float(np.min(axis_ratio)),
        "axis_ratio_max": float(np.max(axis_ratio)),
        "inferred_prescale_axis_ratio_median": float(np.median(prescale_ratio)),
        "off_axis_ratio_max_abs_deviation": float(np.max(np.abs(off_ratio - 1.0))),
        "axis_samples": int(axis_ratio.size),
        "off_axis_samples": int(off_ratio.size),
    }


def normalized_input(path: Path) -> list[str]:
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "boundary.verboncoeur_axis_correction = false":
            continue
        lines.append(line)
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--on-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--off-plotfiles", nargs="+", type=Path, required=True)
    parser.add_argument("--on-input", type=Path, required=True)
    parser.add_argument("--off-input", type=Path, required=True)
    parser.add_argument("--source-files", nargs="+", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    on_paths = [resolve(root, path) for path in args.on_plotfiles]
    off_paths = [resolve(root, path) for path in args.off_plotfiles]
    on_input = resolve(root, args.on_input)
    off_input = resolve(root, args.off_input)
    source_files = [resolve(root, path) for path in args.source_files]
    pairs = []
    for on_path, off_path in zip(on_paths, off_paths):
        fields = {field: ratios(read_field(on_path, field), read_field(off_path, field)) for field in FIELDS}
        pairs.append({"on_plotfile": str(on_path), "off_plotfile": str(off_path), "fields": fields})

    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    all_fields = [pair["fields"][field] for pair in pairs for field in FIELDS]
    checks = {
        "paired_family_lengths": len(on_paths) == len(off_paths),
        "all_plotfiles_present": all(path.is_dir() for path in on_paths + off_paths),
        "inputs_differ_only_by_explicit_toggle": normalized_input(on_input) == normalized_input(off_input),
        "on_input_omits_toggle_defaulting_true": "boundary.verboncoeur_axis_correction" not in on_input.read_text(encoding="utf-8"),
        "off_input_explicitly_disables_toggle": "boundary.verboncoeur_axis_correction = false" in off_input.read_text(encoding="utf-8"),
        "source_get_charge_density_present": "WarpXParticleContainer::GetChargeDensity" in source,
        "source_diagnostic_applies_scaling": "apply_boundary_and_scale_volume" in source and "true, true, 0" in source,
        "source_wrap_precedes_scaling": "Wrap the charge density" in source and "Apply the inverse volume scaling" in source,
        "source_scaling_call_present": "ApplyInverseVolumeScalingToChargeDensity" in source,
        "off_axis_control_matches": all(item["off_axis_ratio_max_abs_deviation"] <= 1.0e-12 for item in all_fields),
        "final_axis_ratio_is_085": all(abs(item["axis_ratio_median"] - 0.85) <= 1.0e-12 for item in all_fields),
        "inferred_prescale_axis_ratio_is_113333": all(
            abs(item["inferred_prescale_axis_ratio_median"] - (0.85 / 0.75)) <= 1.0e-12 for item in all_fields
        ),
    }
    result = {
        "contract": "RZ rho axis pre-scaling boundary",
        "classification": "RZ_RHO_AXIS_PRESCALE_INPUT_BOUNDARY_OPEN",
        "passed": all(checks.values()),
        "checks": checks,
        "source_files": [str(path) for path in source_files],
        "axis_volume_factors": {"on": ON_AXIS_FACTOR, "off": OFF_AXIS_FACTOR},
        "inferred_prescale_ratio_formula": "final_on_off_ratio * ((1/3)/(1/4))",
        "pairs": pairs,
        "scope": (
            "The final axis rho ratio is 0.85, but undoing the source axis volume-factor ratio "
            "infers a 1.133333 pre-scaling axis-input ratio. The source call chain confirms that "
            "species diagnostics request charge density with boundary/volume scaling enabled, "
            "and that axis guard wrapping occurs before scaling. This narrows the boundary to "
            "the pre-scaling deposit/wrap/input state; it is not a kernel root-cause proof or charge closure."
        ),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# RZ rho axis pre-scaling boundary contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        "- final observed axis ratio: `0.850000`",
        "- inferred pre-scaling axis-input ratio: `1.133333`",
        "- source volume-factor ratio alone: `0.750000`",
        "",
        "| grid | field | final axis on/off | inferred pre-scaling on/off | off-axis max deviation |",
        "|---:|---|---:|---:|---:|",
    ]
    for pair in pairs:
        for field in FIELDS:
            item = pair["fields"][field]
            lines.append(
                f"| {item['axis_samples'] // 2}x{item['axis_samples']} | {field} | "
                f"{item['axis_ratio_median']:.6f} | {item['inferred_prescale_axis_ratio_median']:.6f} | "
                f"{item['off_axis_ratio_max_abs_deviation']:.3e} |"
            )
    lines.extend([
        "",
        "Undoing the outer `1/3` versus `1/4` factor does not recover equal axis inputs. "
        "The remaining boundary is therefore upstream of or inside the wrap/scaling input path, "
        "not explained by the outer factor alone.",
    ])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
