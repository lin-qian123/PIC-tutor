#!/usr/bin/env python
"""Record the local finite+spike contract for the comoving first-stage draft."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


FIELD_NAMES = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho")
SPIKE_RATIO_MAX = 1.1114823702056489


def summarize(plotfile: Path) -> dict:
    yt.funcs.mylog.setLevel(0)
    ds = yt.load(str(plotfile))
    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()
    grid = ds.covering_grid(level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
    arrays = {name: np.asarray(grid["boxlib", name].squeeze().v) for name in FIELD_NAMES}
    finite_fields = {name: bool(np.all(np.isfinite(array))) for name, array in arrays.items()}
    e_mag = np.sqrt(arrays["Ex"] ** 2 + arrays["Ey"] ** 2 + arrays["Ez"] ** 2)
    ratio = float(np.max(e_mag) / (np.percentile(e_mag, 99) + 1.0e-300))
    return {
        "plotfile": str(plotfile),
        "domain_dimensions": [int(value) for value in np.asarray(ds.domain_dimensions)],
        "all_fields_finite": bool(all(finite_fields.values())),
        "finite_fields": finite_fields,
        "spike_ratio": ratio,
        "spike_ratio_max": SPIKE_RATIO_MAX,
        "spike_gate_passed": bool(all(finite_fields.values()) and ratio <= SPIKE_RATIO_MAX),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stable-plotfile", type=Path, required=True)
    parser.add_argument("--reference-plotfile", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    stable = summarize(args.stable_plotfile)
    reference = summarize(args.reference_plotfile)
    result = {
        "stable": stable,
        "reference": reference,
        "stable_gate_passed": stable["spike_gate_passed"],
        "reference_rejected": not reference["spike_gate_passed"],
        "passed": bool(stable["spike_gate_passed"] and not reference["spike_gate_passed"]),
        "contract": "finite fields plus stable-baseline spike ceiling accepts the comoving baseline and rejects the no-comoving reference",
        "energy_gate": "disabled; current local calibration does not justify an energy oracle",
        "scope": "project-level local calibration, not WarpX upstream CI",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    args.output_md.write_text(
        "# Comoving first-stage contract\n\n"
        f"- status: `{status}`\n"
        f"- stable spike ratio: `{stable['spike_ratio']:.16e}`\n"
        f"- no-comoving reference spike ratio: `{reference['spike_ratio']:.16e}`\n"
        f"- spike ceiling: `{SPIKE_RATIO_MAX:.16e}`\n"
        f"- stable baseline accepted: `{result['stable_gate_passed']}`\n"
        f"- reference rejected: `{result['reference_rejected']}`\n"
        "- energy gate: `disabled`\n"
        f"- scope: {result['scope']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("comoving first-stage contract failed")


if __name__ == "__main__":
    main()
