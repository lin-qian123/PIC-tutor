#!/usr/bin/env python
"""Scan local comoving-velocity sibling candidates for the 2D hybrid PSATD test.

The goal is narrow: keep the producer scaffold as unchanged as possible, vary
only the `v_comoving` path, and compare which sibling candidates actually
inflate electric-field energy or spike metrics relative to the stable baseline.
"""

from __future__ import annotations

import argparse
import json
import math
import shlex
import socket
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_comoving_reference_ledger import load_plotfile_metrics


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WARPX = (
    ROOT
    / ".."
    / "warpx"
    / "build_full"
    / "bin"
    / "warpx.2d.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES"
)
DEFAULT_INPUT = (
    ROOT
    / ".."
    / "warpx"
    / "Examples"
    / "Tests"
    / "nci_psatd_stability"
    / "inputs_test_2d_comoving_psatd_hybrid"
)
DEFAULT_OUTPUT_ROOT = ROOT / "runs" / "fieldsolver-validation" / "comoving-velocity-scan"
DEFAULT_LEDGER_STEM = (
    ROOT
    / "runs"
    / "fieldsolver-validation"
    / "comoving-reference-ledgers"
    / "comoving-velocity-scan"
)


@dataclass
class VariantSpec:
    label: str
    kind: str
    description: str
    normalized_vz: float | None
    overrides: list[str]
    run_dir: Path
    reused_existing: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run and summarize local comoving velocity sibling candidates."
    )
    parser.add_argument(
        "--warpx-bin",
        type=Path,
        default=DEFAULT_WARPX,
        help="Path to the WarpX 2D executable.",
    )
    parser.add_argument(
        "--input-file",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to inputs_test_2d_comoving_psatd_hybrid.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory holding per-variant run folders.",
    )
    parser.add_argument(
        "--ledger-stem",
        type=Path,
        default=DEFAULT_LEDGER_STEM,
        help="Output stem for the scan summary markdown/json.",
    )
    parser.add_argument(
        "--force-rerun",
        action="store_true",
        help="Re-run generated siblings even if diag1000400 already exists.",
    )
    return parser.parse_args()


def load_gamma_boost(input_file: Path) -> float:
    for line in input_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("warpx.gamma_boost"):
            _, value = stripped.split("=", 1)
            return float(value.strip().rstrip("."))
    raise ValueError(f"Could not find warpx.gamma_boost in {input_file}")


def build_variants(output_root: Path, beta: float) -> list[VariantSpec]:
    existing_root = ROOT / "runs" / "fieldsolver-validation"
    return [
        VariantSpec(
            label="stable-default-selector",
            kind="reused",
            description="Existing stable baseline with psatd.use_default_v_comoving=1",
            normalized_vz=-beta,
            overrides=["warpx.numprocs=1 1"],
            run_dir=existing_root / "comoving-stable-baseline",
            reused_existing=True,
        ),
        VariantSpec(
            label="zero-comoving",
            kind="reused",
            description="Existing sibling with default selector disabled and v_comoving pinned to zero",
            normalized_vz=0.0,
            overrides=[
                "warpx.numprocs=1 1",
                "psatd.use_default_v_comoving=0",
                "psatd.v_comoving=0. 0. 0.",
            ],
            run_dir=existing_root / "comoving-unstable-no-comoving",
            reused_existing=True,
        ),
        VariantSpec(
            label="explicit-default-beta",
            kind="generated",
            description="Same comoving magnitude as the default selector, but set explicitly",
            normalized_vz=-beta,
            overrides=[
                "warpx.numprocs=1 1",
                "psatd.use_default_v_comoving=0",
                f"psatd.v_comoving=0. 0. {-beta:.16f}",
            ],
            run_dir=output_root / "explicit-default-beta",
            reused_existing=False,
        ),
        VariantSpec(
            label="half-default-beta",
            kind="generated",
            description="Half of the default comoving velocity magnitude",
            normalized_vz=-0.5 * beta,
            overrides=[
                "warpx.numprocs=1 1",
                "psatd.use_default_v_comoving=0",
                f"psatd.v_comoving=0. 0. {-0.5 * beta:.16f}",
            ],
            run_dir=output_root / "half-default-beta",
            reused_existing=False,
        ),
        VariantSpec(
            label="positive-default-beta",
            kind="generated",
            description="Same magnitude as default, but with the opposite sign",
            normalized_vz=beta,
            overrides=[
                "warpx.numprocs=1 1",
                "psatd.use_default_v_comoving=0",
                f"psatd.v_comoving=0. 0. {beta:.16f}",
            ],
            run_dir=output_root / "positive-default-beta",
            reused_existing=False,
        ),
    ]


def plotfile_for(run_dir: Path) -> Path:
    return run_dir / "diags" / "diag1000400"


def run_variant(args: argparse.Namespace, variant: VariantSpec) -> dict[str, Any]:
    variant.run_dir.mkdir(parents=True, exist_ok=True)
    plotfile = plotfile_for(variant.run_dir)
    if not variant.reused_existing and (args.force_rerun or not plotfile.exists()):
        command = [
            str(args.warpx_bin.resolve()),
            str(args.input_file.resolve()),
            *variant.overrides,
        ]
        completed = subprocess.run(
            command,
            cwd=variant.run_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        (variant.run_dir / "stdout.log").write_text(completed.stdout, encoding="utf-8")
        (variant.run_dir / "stderr.log").write_text(completed.stderr, encoding="utf-8")
        (variant.run_dir / "command.txt").write_text(
            " ".join(shlex.quote(part) for part in command) + "\n",
            encoding="utf-8",
        )
        if completed.returncode != 0:
            return {
                "label": variant.label,
                "kind": variant.kind,
                "description": variant.description,
                "normalized_vz": variant.normalized_vz,
                "reused_existing": variant.reused_existing,
                "run_dir": str(variant.run_dir.resolve()),
                "plotfile": str(plotfile.resolve()),
                "overrides": variant.overrides,
                "status": "run_failed",
                "returncode": completed.returncode,
                "stderr_tail": completed.stderr.splitlines()[-5:],
            }
    if not plotfile.exists():
        return {
            "label": variant.label,
            "kind": variant.kind,
            "description": variant.description,
            "normalized_vz": variant.normalized_vz,
            "reused_existing": variant.reused_existing,
            "run_dir": str(variant.run_dir.resolve()),
            "plotfile": str(plotfile.resolve()),
            "overrides": variant.overrides,
            "status": "missing_plotfile",
        }
    metrics = load_plotfile_metrics(variant.label, plotfile.resolve())
    return {
        "label": variant.label,
        "kind": variant.kind,
        "description": variant.description,
        "normalized_vz": variant.normalized_vz,
        "reused_existing": variant.reused_existing,
        "run_dir": str(variant.run_dir.resolve()),
        "plotfile": str(plotfile.resolve()),
        "overrides": variant.overrides,
        "status": "ok",
        "metrics": asdict(metrics),
    }


def derive_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    successful = [item for item in results if item["status"] == "ok"]
    stable = next(item for item in successful if item["label"] == "stable-default-selector")
    stable_energy = stable["metrics"]["electric_energy"]
    stable_spike = stable["metrics"]["spike_ratio"]

    candidates: list[dict[str, Any]] = []
    for item in results:
        candidate = dict(item)
        if item["status"] == "ok":
            energy = item["metrics"]["electric_energy"]
            spike = item["metrics"]["spike_ratio"]
            candidate["stable_energy_ratio"] = energy / stable_energy
            candidate["stable_spike_ratio"] = spike / stable_spike
        candidates.append(candidate)

    ranked_by_energy = sorted(
        successful, key=lambda item: item["metrics"]["electric_energy"], reverse=True
    )
    ranked_by_spike = sorted(
        successful, key=lambda item: item["metrics"]["spike_ratio"], reverse=True
    )
    return {
        "stable_label": stable["label"],
        "stable_energy": stable_energy,
        "stable_spike_ratio": stable_spike,
        "ranked_by_energy_desc": [item["label"] for item in ranked_by_energy],
        "ranked_by_spike_desc": [item["label"] for item in ranked_by_spike],
        "best_energy_inflator": ranked_by_energy[0]["label"],
        "best_spike_inflator": ranked_by_spike[0]["label"],
        "candidates": candidates,
    }


def fmt(value: float) -> str:
    return f"{value:.16e}"


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Comoving Velocity Candidate Scan",
        "",
        "This file records a local sibling scan that keeps the 2D hybrid comoving PSATD scaffold fixed and varies only the `v_comoving` path.",
        "",
        "## Provenance",
        "",
        f"- Generated at (UTC): `{payload['generated_at_utc']}`",
        f"- Hostname: `{payload['hostname']}`",
        f"- Working directory: `{payload['cwd']}`",
        f"- WarpX executable: `{payload['warpx_bin']}`",
        f"- Input file: `{payload['input_file']}`",
        f"- Gamma boost: `{payload['gamma_boost']}`",
        f"- Default normalized beta magnitude: `{payload['beta']:.16f}`",
        "",
        "## Candidate Summary",
        "",
        "| Label | Kind | normalized vz/c | Electric energy | Energy / stable | Spike ratio | Spike / stable |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for item in payload["derived_summary"]["candidates"]:
        if item["status"] == "ok":
            lines.append(
                f"| `{item['label']}` | `{item['kind']}` | "
                f"`{item['normalized_vz']:.16f}` | "
                f"`{fmt(item['metrics']['electric_energy'])}` | "
                f"`{fmt(item['stable_energy_ratio'])}` | "
                f"`{fmt(item['metrics']['spike_ratio'])}` | "
                f"`{fmt(item['stable_spike_ratio'])}` |"
            )
        else:
            lines.append(
                f"| `{item['label']}` | `{item['kind']}` | "
                f"`{item['normalized_vz']:.16f}` | `n/a` | `n/a` | `n/a` | `n/a` |"
            )

    lines.extend(
        [
            "",
            "## Ranking",
            "",
            f"- Highest electric energy: `{payload['derived_summary']['best_energy_inflator']}`",
            f"- Highest spike ratio: `{payload['derived_summary']['best_spike_inflator']}`",
            "",
            "## Per-candidate Notes",
            "",
        ]
    )

    for item in payload["derived_summary"]["candidates"]:
        lines.extend(
            [
                f"### `{item['label']}`",
                "",
                f"- Description: `{item['description']}`",
                f"- Run directory: `{item['run_dir']}`",
                f"- Plotfile: `{item['plotfile']}`",
                f"- Reused existing run: `{item['reused_existing']}`",
                f"- Overrides: `{'; '.join(item['overrides'])}`",
                f"- Status: `{item['status']}`",
                "",
            ]
        )
        if item["status"] == "ok":
            lines.extend(
                [
                    f"- Electric energy: `{fmt(item['metrics']['electric_energy'])}`",
                    f"- Spike ratio: `{fmt(item['metrics']['spike_ratio'])}`",
                    f"- Energy / stable: `{fmt(item['stable_energy_ratio'])}`",
                    f"- Spike / stable: `{fmt(item['stable_spike_ratio'])}`",
                    "",
                ]
            )
        elif item.get("stderr_tail"):
            lines.extend(
                [
                    "- stderr tail:",
                    "",
                    "```text",
                    *item["stderr_tail"],
                    "```",
                    "",
                ]
            )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    gamma_boost = load_gamma_boost(args.input_file.resolve())
    beta = math.sqrt(1.0 - 1.0 / (gamma_boost * gamma_boost))
    variants = build_variants(args.output_root.resolve(), beta)
    results = [run_variant(args, variant) for variant in variants]
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "cwd": str(ROOT),
        "warpx_bin": str(args.warpx_bin.resolve()),
        "input_file": str(args.input_file.resolve()),
        "gamma_boost": gamma_boost,
        "beta": beta,
        "results": results,
        "derived_summary": derive_summary(results),
    }

    args.ledger_stem.parent.mkdir(parents=True, exist_ok=True)
    md_path = args.ledger_stem.with_suffix(".md")
    json_path = args.ledger_stem.with_suffix(".json")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {md_path.relative_to(ROOT)}")
    print(f"wrote {json_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
