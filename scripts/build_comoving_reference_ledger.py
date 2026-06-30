#!/usr/bin/env python
"""Build a stable/unstable reference ledger for comoving PSATD plotfiles.

The script reads WarpX plotfiles through yt, extracts field statistics used by
the planned `analysis_comoving.py`, and writes a provenance-friendly markdown
and/or JSON ledger. It does not guess final tolerances; instead it records the
observed ratios that later patch reviews can cite directly.
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
FIELD_NAMES = ["Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho"]


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
    electric_energy_density_mean: float
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
    for name in FIELD_NAMES:
        arr = np.asarray(grid["boxlib", name].squeeze().v)
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

    ex = arrays["Ex"]
    ey = arrays["Ey"]
    ez = arrays["Ez"]
    energy_density = EPSILON_0 * 0.5 * (ex**2 + ey**2 + ez**2)
    e_mag = np.sqrt(ex**2 + ey**2 + ez**2)
    e_mag_max = float(np.max(e_mag))
    e_mag_p99 = float(np.percentile(e_mag, 99))
    spike_ratio = e_mag_max / (e_mag_p99 + 1e-300)

    return PlotfileMetrics(
        label=label,
        plotfile=str(plotfile),
        domain_dimensions=[int(v) for v in np.asarray(ds.domain_dimensions)],
        all_fields_finite=all_finite,
        electric_energy=float(np.sum(energy_density)),
        electric_energy_density_mean=float(np.mean(energy_density)),
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
    unstable_metrics = None
    if args.unstable_plotfile is not None:
        unstable_metrics = load_plotfile_metrics(
            "unstable", args.unstable_plotfile.resolve()
        )

    derived: dict[str, Any] = {}
    if unstable_metrics is not None:
        derived["stable_over_unstable_energy_ratio"] = (
            stable_metrics.electric_energy / unstable_metrics.electric_energy
        )
        derived["stable_over_unstable_spike_ratio"] = (
            stable_metrics.spike_ratio / unstable_metrics.spike_ratio
        )
        derived["minimum_tol_energy_for_observed_stable_sample"] = (
            derived["stable_over_unstable_energy_ratio"]
        )
        derived["energy_ref_unstable"] = unstable_metrics.electric_energy
        derived["spike_ratio_ref_stable"] = stable_metrics.spike_ratio

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "cwd": str(Path.cwd()),
        "label": args.label,
        "warpx_commit": args.warpx_commit,
        "stable_input": str(args.stable_input.resolve()) if args.stable_input else None,
        "unstable_input": (
            str(args.unstable_input.resolve()) if args.unstable_input else None
        ),
        "producer_command": args.producer_command,
        "note": args.note,
        "stable_metrics": asdict(stable_metrics),
        "unstable_metrics": asdict(unstable_metrics) if unstable_metrics else None,
        "derived_contract_observations": derived,
    }
    return payload


def render_markdown(payload: dict[str, Any]) -> str:
    stable = payload["stable_metrics"]
    unstable = payload["unstable_metrics"]
    derived = payload["derived_contract_observations"]

    lines = [
        f"# Comoving Reference Ledger: {payload['label']}",
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
        f"- Unstable plotfile: `{unstable['plotfile']}`" if unstable else "- Unstable plotfile: `not provided`",
        f"- Unstable input: `{payload['unstable_input'] or 'unknown'}`" if unstable else "- Unstable input: `not provided`",
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
        f"| electric_energy_density_mean | `{format_float(stable['electric_energy_density_mean'])}` |",
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

    if unstable:
        lines.extend(
            [
                "",
                "## Unstable Metrics",
                "",
                "| Quantity | Value |",
                "|---|---:|",
                f"| all_fields_finite | `{unstable['all_fields_finite']}` |",
                f"| domain_dimensions | `{unstable['domain_dimensions']}` |",
                f"| electric_energy | `{format_float(unstable['electric_energy'])}` |",
                f"| electric_energy_density_mean | `{format_float(unstable['electric_energy_density_mean'])}` |",
                f"| e_mag_max | `{format_float(unstable['e_mag_max'])}` |",
                f"| e_mag_p99 | `{format_float(unstable['e_mag_p99'])}` |",
                f"| spike_ratio | `{format_float(unstable['spike_ratio'])}` |",
                "",
                "## Derived Contract Observations",
                "",
                "| Quantity | Value |",
                "|---|---:|",
                f"| energy_ref_unstable | `{format_float(derived['energy_ref_unstable'])}` |",
                f"| spike_ratio_ref_stable | `{format_float(derived['spike_ratio_ref_stable'])}` |",
                f"| stable_over_unstable_energy_ratio | `{format_float(derived['stable_over_unstable_energy_ratio'])}` |",
                f"| stable_over_unstable_spike_ratio | `{format_float(derived['stable_over_unstable_spike_ratio'])}` |",
                f"| minimum_tol_energy_for_observed_stable_sample | `{format_float(derived['minimum_tol_energy_for_observed_stable_sample'])}` |",
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
        description=(
            "Extract comoving PSATD reference metrics from stable/unstable "
            "WarpX plotfiles and write a provenance-friendly ledger."
        )
    )
    parser.add_argument("--label", default="comoving-psatd-reference")
    parser.add_argument("--stable-plotfile", type=Path, required=True)
    parser.add_argument("--unstable-plotfile", type=Path)
    parser.add_argument("--stable-input", type=Path)
    parser.add_argument("--unstable-input", type=Path)
    parser.add_argument("--warpx-commit")
    parser.add_argument("--producer-command")
    parser.add_argument("--note")
    parser.add_argument(
        "--output-stem",
        type=Path,
        help=(
            "Write `<stem>.md` and/or `<stem>.json`. If omitted, markdown is "
            "printed to stdout."
        ),
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="When --output-stem is set, write only JSON.",
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="When --output-stem is set, write only Markdown.",
    )
    args = parser.parse_args()
    if args.json_only and args.markdown_only:
        parser.error("--json-only and --markdown-only cannot be used together")
    return args


def main() -> int:
    args = parse_args()
    payload = build_payload(args)

    emit_json = not args.markdown_only
    emit_markdown = not args.json_only
    write_outputs(payload, args.output_stem, emit_json, emit_markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
