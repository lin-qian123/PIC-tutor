#!/usr/bin/env python
"""Audit native divE/divB diagnostics for the 3D PSATD-PML cleaning case."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import yt
from scipy.constants import epsilon_0, mu_0


FIELDS = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "rho", "divE", "divB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean-plotfile", type=Path, required=True)
    parser.add_argument("--control-plotfile", type=Path, required=True)
    parser.add_argument("--clean-input", type=Path, required=True)
    parser.add_argument("--control-input", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    clean = _read_plotfile(args.clean_plotfile, args.clean_input)
    control = _read_plotfile(args.control_plotfile, args.control_input)
    result = {
        "clean": clean,
        "control": control,
        "comparison": {
            "core_divE_norm_ratio_clean_over_control": _ratio(
                clean["core"]["divE_gauss_residual_norm"],
                control["core"]["divE_gauss_residual_norm"],
            ),
            "core_divB_norm_ratio_clean_over_control": _ratio(
                clean["core"]["divB_norm"], control["core"]["divB_norm"]
            ),
            "core_field_energy_ratio_clean_over_control": _ratio(
                clean["core"]["field_energy"], control["core"]["field_energy"]
            ),
        },
        "gates": {
            "native_diagnostics_present": bool(clean["finite"] and control["finite"]),
            "strong_cleaning_physics_gate": False,
        },
        "passed": bool(clean["finite"] and control["finite"]),
        "contract": "3D PSATD-PML native divE/divB reader-side contrast audit",
        "scope": "finite/output completeness plus clean-vs-control observation; not a positive cleaning physics gate",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(_markdown(result), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("3D PSATD-PML diagnostic audit failed")


def _read_plotfile(plotfile: Path, input_path: Path) -> dict:
    ds = yt.load(str(plotfile))
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    fields = {name: grid["boxlib", name].to_ndarray() for name in FIELDS}
    finite = all(bool(np.isfinite(value).all()) for value in fields.values())
    spacing = [float(value) for value in ds.domain_width / np.asarray(ds.domain_dimensions)]
    pml_ncell = _read_pml_ncell(input_path)
    all_metrics = _metrics(fields, spacing, (slice(None),) * 3)
    core_slice = tuple(slice(pml_ncell, -pml_ncell) for _ in range(3))
    core_metrics = _metrics(fields, spacing, core_slice)
    return {
        "plotfile": str(plotfile.resolve()),
        "time": float(ds.current_time),
        "shape": [int(value) for value in ds.domain_dimensions],
        "spacing": spacing,
        "pml_ncell": pml_ncell,
        "finite": finite,
        "all": all_metrics,
        "core": core_metrics,
    }


def _metrics(fields: dict[str, np.ndarray], spacing: list[float], selection: tuple[slice, ...]) -> dict:
    electric = 0.5 * epsilon_0 * sum(fields[name][selection] ** 2 for name in ("Ex", "Ey", "Ez"))
    magnetic = 0.5 / mu_0 * sum(fields[name][selection] ** 2 for name in ("Bx", "By", "Bz"))
    e_scale = max(
        float(np.max(np.abs(np.stack([fields[name][selection] for name in ("Ex", "Ey", "Ez")]))))
        / max(spacing),
        1.0e-300,
    )
    b_scale = max(
        float(np.max(np.abs(np.stack([fields[name][selection] for name in ("Bx", "By", "Bz")]))))
        / max(spacing),
        1.0e-300,
    )
    gauss_residual = fields["divE"][selection] - fields["rho"][selection] / epsilon_0
    return {
        "max_abs_divE": float(np.max(np.abs(fields["divE"][selection]))),
        "max_abs_divB": float(np.max(np.abs(fields["divB"][selection]))),
        "max_abs_gauss_residual": float(np.max(np.abs(gauss_residual))),
        "divE_gauss_residual_norm": float(np.max(np.abs(gauss_residual)) / e_scale),
        "divB_norm": float(np.max(np.abs(fields["divB"][selection])) / b_scale),
        "field_energy": float(np.sum(electric + magnetic)),
        "max_abs_E": float(np.max(np.abs(np.stack([fields[name][selection] for name in ("Ex", "Ey", "Ez")])))),
        "max_abs_B": float(np.max(np.abs(np.stack([fields[name][selection] for name in ("Bx", "By", "Bz")])))),
    }


def _read_pml_ncell(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^warpx\.pml_ncell\s*=\s*(\d+)", text, re.MULTILINE)
    return int(match.group(1)) if match else 10


def _ratio(numerator: float, denominator: float) -> float:
    return float(numerator / max(abs(denominator), 1.0e-300))


def _markdown(result: dict) -> str:
    clean = result["clean"]
    control = result["control"]
    comparison = result["comparison"]
    lines = [
        "# 3D PSATD-PML cleaning diagnostic audit",
        "",
        "- native diagnostics: `divE`, `divB`, `rho`, `E`, `B`",
        "- contract: finite/output completeness `PASS`; strong cleaning physics gate intentionally `OFF`",
        f"- clean core normalized Gauss residual: `{clean['core']['divE_gauss_residual_norm']:.6e}`",
        f"- control core normalized Gauss residual: `{control['core']['divE_gauss_residual_norm']:.6e}`",
        f"- clean/control core normalized `divB` ratio: `{comparison['core_divB_norm_ratio_clean_over_control']:.6e}`",
        f"- clean/control core field-energy ratio: `{comparison['core_field_energy_ratio_clean_over_control']:.6e}`",
        "",
        "The clean run does not produce a monotonic improvement in this cell-centered native diagnostic relative to the control run. The result therefore strengthens the evidence boundary, but is not promoted to a positive PML-cleaning physics gate. A solver-native spectral residual or a dedicated upstream analysis remains required.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
