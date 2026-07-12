#!/usr/bin/env python
"""Record the RZ JRhom LL2 first-stage positive/negative energy contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


EPSILON_0 = 8.8541878128e-12
FIELD_NAMES = ("Er", "Ez", "Bt", "jr", "jz", "rho")


def summarize(plotfile: Path) -> dict:
    yt.funcs.mylog.setLevel(0)
    ds = yt.load(str(plotfile))
    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    arrays = {name: np.asarray(grid["boxlib", name].squeeze().v) for name in FIELD_NAMES}
    finite_fields = {name: bool(np.all(np.isfinite(array))) for name, array in arrays.items()}
    e_mag = np.sqrt(arrays["Er"] ** 2 + arrays["Ez"] ** 2)
    return {
        "plotfile": str(plotfile),
        "domain_dimensions": [int(value) for value in np.asarray(ds.domain_dimensions)],
        "all_fields_finite": bool(all(finite_fields.values())),
        "finite_fields": finite_fields,
        "electric_energy": float(np.sum(0.5 * EPSILON_0 * (arrays["Er"] ** 2 + arrays["Ez"] ** 2))),
        "spike_ratio": float(np.max(e_mag) / (np.percentile(e_mag, 99) + 1.0e-300)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-plotfile", type=Path, required=True)
    parser.add_argument("--reference-plotfile", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--energy-safety-factor", type=float, default=1.001)
    args = parser.parse_args()

    baseline = summarize(args.baseline_plotfile)
    reference = summarize(args.reference_plotfile)
    tolerance = baseline["electric_energy"] / reference["electric_energy"] * args.energy_safety_factor
    baseline_ratio = baseline["electric_energy"] / reference["electric_energy"]
    reference_ratio = reference["electric_energy"] / reference["electric_energy"]
    result = {
        "baseline": baseline,
        "reference": reference,
        "energy_reference": reference["electric_energy"],
        "energy_tolerance": tolerance,
        "baseline_energy_ratio": baseline_ratio,
        "reference_energy_ratio": reference_ratio,
        "baseline_accepted": bool(baseline["all_fields_finite"] and baseline_ratio <= tolerance),
        "reference_rejected": bool(not (reference["all_fields_finite"] and reference_ratio <= tolerance)),
        "passed": bool(baseline["all_fields_finite"] and baseline_ratio <= tolerance and reference_ratio > tolerance),
        "contract": "finite fields plus baseline/reference energy ceiling accepts JRhom LL2 baseline and rejects the no-time-averaging reference",
        "spike_gate": "reported only; not enabled in the first-stage contract",
        "scope": "project-level repeated/MPI ledger validation, not WarpX upstream CI",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# RZ JRhom LL2 first-stage contract\n\n"
        f"- status: `{status}`\n"
        f"- baseline energy ratio: `{baseline_ratio:.16e}`\n"
        f"- reference energy ratio: `{reference_ratio:.16e}`\n"
        f"- energy tolerance: `{tolerance:.16e}`\n"
        f"- baseline accepted: `{result['baseline_accepted']}`\n"
        f"- reference rejected: `{result['reference_rejected']}`\n"
        "- spike gate: `reported only; disabled`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("RZ JRhom first-stage contract failed")


if __name__ == "__main__":
    main()
