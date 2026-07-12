#!/usr/bin/env python
"""Build a reference ledger for RZ PSATD plotfiles.

The initial target is `test_rz_psatd_JRhom_LL2`: record field-energy and spike
metrics for the stable baseline and one candidate sibling, without claiming
that the observed ordering is already the final WarpX regression gate.
"""

from __future__ import annotations

import argparse
import json
import math
import socket
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


EPSILON_0 = 8.8541878128e-12
MU_0 = 1.25663706212e-6
REQUIRED_FIELD_NAMES = ["Er", "Ez", "Bt", "jr", "jz", "rho"]
OPTIONAL_FIELD_NAMES = ["rho_driver", "rho_plasma_e", "rho_plasma_p", "divE", "F", "G"]


@dataclass
class FieldSummary:
    name: str
    finite: bool
    min_value: float
    max_value: float
    max_abs: float


@dataclass
class PlotfileMetrics:
    label: str
    plotfile: str
    domain_dimensions: list[int]
    all_fields_finite: bool
    electric_energy: float
    magnetic_energy: float
    electric_energy_density_mean: float
    magnetic_energy_density_mean: float
    e_mag_max: float
    e_mag_p99: float
    spike_ratio: float
    field_summaries: list[FieldSummary]


def load_plotfile_metrics(label: str, plotfile: Path) -> PlotfileMetrics:
    try:
        import yt
    except ImportError as exc:
        raise RuntimeError(
            "yt is required to read WarpX plotfiles. Install yt in the current "
            "python environment before running this script."
        ) from exc

    yt.funcs.mylog.setLevel(0)
    ds = yt.load(str(plotfile))
    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()
    grid = ds.covering_grid(
        level=0,
        left_edge=ds.domain_left_edge,
        dims=ds.domain_dimensions,
    )

    arrays: dict[str, np.ndarray] = {}
    summaries: list[FieldSummary] = []
    all_finite = True
    available_fields = set(ds.field_list)

    for name in REQUIRED_FIELD_NAMES + OPTIONAL_FIELD_NAMES:
        key = ("boxlib", name)
        if key not in available_fields:
            if name in REQUIRED_FIELD_NAMES:
                raise RuntimeError(f"{plotfile} is missing required field {name}")
            continue
        arr = np.asarray(grid[key].squeeze().v)
        finite = bool(np.all(np.isfinite(arr)))
        all_finite = all_finite and finite
        arrays[name] = arr
        summaries.append(
            FieldSummary(
                name=name,
                finite=finite,
                min_value=float(np.min(arr)),
                max_value=float(np.max(arr)),
                max_abs=float(np.max(np.abs(arr))),
            )
        )

    er = arrays["Er"]
    ez = arrays["Ez"]
    bt = arrays["Bt"]
    electric_energy_density = EPSILON_0 * 0.5 * (er**2 + ez**2)
    magnetic_energy_density = 0.5 / MU_0 * (bt**2)
    e_mag = np.sqrt(er**2 + ez**2)
    e_mag_max = float(np.max(e_mag))
    e_mag_p99 = float(np.percentile(e_mag, 99))
    spike_ratio = e_mag_max / (e_mag_p99 + 1e-300)

    return PlotfileMetrics(
        label=label,
        plotfile=str(plotfile),
        domain_dimensions=[int(v) for v in np.asarray(ds.domain_dimensions)],
        all_fields_finite=all_finite,
        electric_energy=float(np.sum(electric_energy_density)),
        magnetic_energy=float(np.sum(magnetic_energy_density)),
        electric_energy_density_mean=float(np.mean(electric_energy_density)),
        magnetic_energy_density_mean=float(np.mean(magnetic_energy_density)),
        e_mag_max=e_mag_max,
        e_mag_p99=e_mag_p99,
        spike_ratio=float(spike_ratio),
        field_summaries=summaries,
    )


def format_float(value: float) -> str:
    if math.isfinite(value):
        return f"{value:.16e}"
    return str(value)


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    stable_metrics = load_plotfile_metrics("stable", args.stable_plotfile.resolve())
    candidate_metrics = None
    if args.candidate_plotfile is not None:
        candidate_metrics = load_plotfile_metrics(
            "candidate", args.candidate_plotfile.resolve()
        )

    derived: dict[str, Any] = {}
    if candidate_metrics is not None:
        derived["stable_over_candidate_energy_ratio"] = (
            stable_metrics.electric_energy / candidate_metrics.electric_energy
        )
        derived["stable_over_candidate_spike_ratio"] = (
            stable_metrics.spike_ratio / candidate_metrics.spike_ratio
        )
        derived["candidate_energy_ref"] = candidate_metrics.electric_energy
        derived["stable_spike_ratio_ref"] = stable_metrics.spike_ratio

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "cwd": str(Path.cwd()),
        "label": args.label,
        "warpx_commit": args.warpx_commit,
        "stable_input": str(args.stable_input.resolve()) if args.stable_input else None,
        "candidate_input": (
            str(args.candidate_input.resolve()) if args.candidate_input else None
        ),
        "producer_command": args.producer_command,
        "note": args.note,
        "stable_metrics": asdict(stable_metrics),
        "candidate_metrics": asdict(candidate_metrics) if candidate_metrics else None,
        "derived_contract_observations": derived,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    stable = payload["stable_metrics"]
    candidate = payload["candidate_metrics"]
    derived = payload["derived_contract_observations"]

    lines = [
        f"# RZ PSATD Reference Ledger: {payload['label']}",
        "",
        "This file is generated from current plotfiles on disk.",
        "",
        "## Provenance",
        "",
        f"- Generated at (UTC): `{payload['generated_at_utc']}`",
        f"- Hostname: `{payload['hostname']}`",
        f"- Working directory: `{payload['cwd']}`",
        f"- WarpX commit: `{payload['warpx_commit'] or 'unknown'}`",
        f"- Stable plotfile: `{stable['plotfile']}`",
        f"- Stable input: `{payload['stable_input'] or 'unknown'}`",
        (
            f"- Candidate plotfile: `{candidate['plotfile']}`"
            if candidate
            else "- Candidate plotfile: `not provided`"
        ),
        (
            f"- Candidate input: `{payload['candidate_input'] or 'unknown'}`"
            if candidate
            else "- Candidate input: `not provided`"
        ),
        f"- Producer command: `{payload['producer_command'] or 'unknown'}`",
        f"- Note: `{payload['note'] or 'none'}`",
        "",
        "## Stable Metrics",
        "",
        "| Quantity | Value |",
        "|---|---:|",
        f"| all_fields_finite | `{stable['all_fields_finite']}` |",
        f"| domain_dimensions | `{stable['domain_dimensions']}` |",
        f"| electric_energy | `{format_float(stable['electric_energy'])}` |",
        f"| magnetic_energy | `{format_float(stable['magnetic_energy'])}` |",
        f"| electric_energy_density_mean | `{format_float(stable['electric_energy_density_mean'])}` |",
        f"| magnetic_energy_density_mean | `{format_float(stable['magnetic_energy_density_mean'])}` |",
        f"| e_mag_max | `{format_float(stable['e_mag_max'])}` |",
        f"| e_mag_p99 | `{format_float(stable['e_mag_p99'])}` |",
        f"| spike_ratio | `{format_float(stable['spike_ratio'])}` |",
        "",
        "## Stable Field Extrema",
        "",
        "| Field | Finite | Min | Max | Max Abs |",
        "|---|---|---:|---:|---:|",
    ]

    for item in stable["field_summaries"]:
        lines.append(
            f"| `{item['name']}` | `{item['finite']}` | "
            f"`{format_float(item['min_value'])}` | "
            f"`{format_float(item['max_value'])}` | "
            f"`{format_float(item['max_abs'])}` |"
        )

    if candidate:
        lines.extend(
            [
                "",
                "## Candidate Metrics",
                "",
                "| Quantity | Value |",
                "|---|---:|",
                f"| all_fields_finite | `{candidate['all_fields_finite']}` |",
                f"| domain_dimensions | `{candidate['domain_dimensions']}` |",
                f"| electric_energy | `{format_float(candidate['electric_energy'])}` |",
                f"| magnetic_energy | `{format_float(candidate['magnetic_energy'])}` |",
                f"| electric_energy_density_mean | `{format_float(candidate['electric_energy_density_mean'])}` |",
                f"| magnetic_energy_density_mean | `{format_float(candidate['magnetic_energy_density_mean'])}` |",
                f"| e_mag_max | `{format_float(candidate['e_mag_max'])}` |",
                f"| e_mag_p99 | `{format_float(candidate['e_mag_p99'])}` |",
                f"| spike_ratio | `{format_float(candidate['spike_ratio'])}` |",
                "",
                "## Derived Contract Observations",
                "",
                "| Quantity | Value |",
                "|---|---:|",
                f"| candidate_energy_ref | `{format_float(derived['candidate_energy_ref'])}` |",
                f"| stable_spike_ratio_ref | `{format_float(derived['stable_spike_ratio_ref'])}` |",
                f"| stable_over_candidate_energy_ratio | `{format_float(derived['stable_over_candidate_energy_ratio'])}` |",
                f"| stable_over_candidate_spike_ratio | `{format_float(derived['stable_over_candidate_spike_ratio'])}` |",
                "",
                "These values are observations from the current pair of plotfiles. "
                "They are not an automatic recommendation to hard-code final tolerances.",
            ]
        )

    return "\n".join(lines) + "\n"


def write_outputs(
    payload: dict[str, Any],
    output_stem: Path | None,
    emit_json: bool,
    emit_markdown: bool,
) -> None:
    markdown = render_markdown(payload)
    if output_stem is None:
        sys.stdout.write(markdown)
        return

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    if emit_markdown:
        md_path = output_stem.with_suffix(".md")
        md_path.write_text(markdown, encoding="utf-8")
        print(f"wrote {md_path}")
    if emit_json:
        json_path = output_stem.with_suffix(".json")
        json_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {json_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a reference ledger for RZ PSATD plotfiles."
    )
    parser.add_argument("--stable-plotfile", type=Path, required=True)
    parser.add_argument("--candidate-plotfile", type=Path)
    parser.add_argument("--stable-input", type=Path)
    parser.add_argument("--candidate-input", type=Path)
    parser.add_argument("--label", default="rz-jrhom-reference")
    parser.add_argument("--warpx-commit", default=None)
    parser.add_argument("--producer-command", default=None)
    parser.add_argument("--note", default=None)
    parser.add_argument("--output-stem", type=Path, default=None)
    parser.add_argument("--no-json", action="store_true")
    parser.add_argument("--no-markdown", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_payload(args)
    write_outputs(
        payload,
        args.output_stem,
        emit_json=not args.no_json,
        emit_markdown=not args.no_markdown,
    )


if __name__ == "__main__":
    main()
