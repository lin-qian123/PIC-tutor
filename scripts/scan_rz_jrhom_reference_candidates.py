#!/usr/bin/env python
"""Scan reference-sibling candidates for `test_rz_psatd_JRhom_LL2`.

The goal is to keep the producer scaffold close to the current RZ workflow
while varying only a few PSATD/JRhom toggles that could plausibly expose a
stable field-energy ordering for a first-stage main analysis.
"""

from __future__ import annotations

import argparse
import json
import shlex
import socket
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_rz_psatd_reference_ledger import load_plotfile_metrics


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WARPX = (
    ROOT
    / ".."
    / "warpx"
    / "build_full"
    / "bin"
    / "warpx.rz.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES"
)
DEFAULT_INPUT = (
    ROOT
    / ".."
    / "warpx"
    / "Examples"
    / "Tests"
    / "nci_psatd_stability"
    / "inputs_test_rz_psatd_JRhom_LL2"
)
DEFAULT_OUTPUT_ROOT = ROOT / "runs" / "fieldsolver-validation" / "rz-jrhom-reference-scan"
DEFAULT_LEDGER_STEM = (
    ROOT
    / "runs"
    / "fieldsolver-validation"
    / "rz-reference-ledgers"
    / "rz-jrhom-reference-scan"
)


@dataclass
class VariantSpec:
    label: str
    description: str
    overrides: list[str]
    run_dir: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run and summarize local RZ JRhom sibling candidates."
    )
    parser.add_argument("--warpx-bin", type=Path, default=DEFAULT_WARPX)
    parser.add_argument("--input-file", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--ledger-stem", type=Path, default=DEFAULT_LEDGER_STEM)
    parser.add_argument(
        "--numprocs-override",
        default="1 1",
        help=(
            "Value passed as `warpx.numprocs=<value>`. Use `none` to keep the "
            "input-file default instead of overriding it. Default: '1 1'."
        ),
    )
    parser.add_argument(
        "--command-prefix",
        nargs="+",
        help=(
            "Optional command prefix such as `mpiexec -n 2`. The prefix is "
            "prepended before the WarpX binary."
        ),
    )
    parser.add_argument(
        "--command-prefix-str",
        help=(
            "String form of the optional command prefix, parsed with shlex.split. "
            "Useful when the prefix itself contains option-like tokens such as "
            "`mpiexec -n 2`."
        ),
    )
    parser.add_argument(
        "--target-step",
        type=int,
        default=25,
        help=(
            "Stop each sibling at the plotfile surface consumed by the current "
            "checksum contract. Default: 25 (for diags/diag1000025)."
        ),
    )
    parser.add_argument(
        "--force-rerun",
        action="store_true",
        help="Re-run generated siblings even if diag1000025 already exists.",
    )
    return parser.parse_args()


def build_variants(
    output_root: Path, target_step: int, numprocs_override: str | None
) -> list[VariantSpec]:
    base = [f"max_step={target_step}"]
    if numprocs_override is not None:
        base.insert(0, f"warpx.numprocs={numprocs_override}")
    return [
        VariantSpec(
            label="baseline-jrhom-ll2-timeavg-cleaning",
            description="Current RZ JRhom LL2 workflow with time averaging and div cleaning enabled.",
            overrides=base,
            run_dir=output_root / "baseline-jrhom-ll2-timeavg-cleaning",
        ),
        VariantSpec(
            label="cl1-timeavg-cleaning",
            description="Keep time averaging and cleaning, but switch JRhom time dependence to CL1.",
            overrides=base + ['psatd.JRhom="CL1"'],
            run_dir=output_root / "cl1-timeavg-cleaning",
        ),
        VariantSpec(
            label="ll2-no-timeavg-cleaning",
            description="Keep JRhom LL2 and cleaning, but disable time averaging.",
            overrides=base + ["psatd.do_time_averaging=0"],
            run_dir=output_root / "ll2-no-timeavg-cleaning",
        ),
        VariantSpec(
            label="ll2-timeavg-no-cleaning",
            description="Keep JRhom LL2 and time averaging, but disable both divE/divB cleaning routes.",
            overrides=base + ["warpx.do_dive_cleaning=0", "warpx.do_divb_cleaning=0"],
            run_dir=output_root / "ll2-timeavg-no-cleaning",
        ),
        VariantSpec(
            label="cl1-no-timeavg-no-cleaning",
            description="Joint contrast candidate: CL1 plus no time averaging and no cleaning.",
            overrides=base
            + ['psatd.JRhom="CL1"', "psatd.do_time_averaging=0", "warpx.do_dive_cleaning=0", "warpx.do_divb_cleaning=0"],
            run_dir=output_root / "cl1-no-timeavg-no-cleaning",
        ),
    ]


def plotfile_for(run_dir: Path) -> Path:
    return run_dir / "diags" / "diag1000025"


def classify_failed_run(stderr_text: str) -> str:
    if "warpx.numprocs, if specified" in stderr_text:
        return "process_count_mismatch"
    return "run_failed"


def failed_result_from_logs(variant: VariantSpec, plotfile: Path) -> dict[str, Any] | None:
    stderr_path = variant.run_dir / "stderr.log"
    if plotfile.exists() or not stderr_path.exists():
        return None
    stderr_text = stderr_path.read_text(encoding="utf-8")
    return {
        "label": variant.label,
        "description": variant.description,
        "run_dir": str(variant.run_dir.resolve()),
        "plotfile": str(plotfile.resolve()),
        "overrides": variant.overrides,
        "status": classify_failed_run(stderr_text),
        "returncode": None,
        "stderr_tail": stderr_text.splitlines()[-8:],
    }


def run_variant(args: argparse.Namespace, variant: VariantSpec) -> dict[str, Any]:
    variant.run_dir.mkdir(parents=True, exist_ok=True)
    plotfile = plotfile_for(variant.run_dir)
    existing_failed = failed_result_from_logs(variant, plotfile)
    if not args.force_rerun and existing_failed is not None:
        return existing_failed
    if args.force_rerun or not plotfile.exists():
        command: list[str] = []
        if args.command_prefix:
            command.extend(args.command_prefix)
        command.extend(
            [
                str(args.warpx_bin.resolve()),
                str(args.input_file.resolve()),
                *variant.overrides,
            ]
        )
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
        if completed.returncode != 0 and not plotfile.exists():
            stderr_tail = completed.stderr.splitlines()[-8:]
            status = classify_failed_run(completed.stderr)
            return {
                "label": variant.label,
                "description": variant.description,
                "run_dir": str(variant.run_dir.resolve()),
                "plotfile": str(plotfile.resolve()),
                "overrides": variant.overrides,
                "status": status,
                "returncode": completed.returncode,
                "stderr_tail": stderr_tail,
            }
    if not plotfile.exists():
        return {
            "label": variant.label,
            "description": variant.description,
            "run_dir": str(variant.run_dir.resolve()),
            "plotfile": str(plotfile.resolve()),
            "overrides": variant.overrides,
            "status": "missing_plotfile",
        }
    metrics = load_plotfile_metrics(variant.label, plotfile.resolve())
    status = "ok"
    returncode = 0
    stderr_tail: list[str] | None = None
    stderr_path = variant.run_dir / "stderr.log"
    if stderr_path.exists():
        stderr_text = stderr_path.read_text(encoding="utf-8")
        stderr_tail = stderr_text.splitlines()[-8:]
        if "MPI_Finalize failed" in stderr_text and "OFI poll failed" in stderr_text:
            status = "ok_with_finalize_error"
            returncode = 143
    return {
        "label": variant.label,
        "description": variant.description,
        "run_dir": str(variant.run_dir.resolve()),
        "plotfile": str(plotfile.resolve()),
        "overrides": variant.overrides,
        "status": status,
        "returncode": returncode,
        "stderr_tail": stderr_tail,
        "metrics": asdict(metrics),
    }


def derive_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    successful = [item for item in results if item["status"].startswith("ok")]
    if not successful:
        return {
            "baseline_label": "baseline-jrhom-ll2-timeavg-cleaning",
            "baseline_energy": None,
            "baseline_spike_ratio": None,
            "ranked_by_energy": [],
            "ranked_by_spike": [],
            "candidates": results,
        }

    baseline = next(
        item
        for item in successful
        if item["label"] == "baseline-jrhom-ll2-timeavg-cleaning"
    )
    baseline_energy = baseline["metrics"]["electric_energy"]
    baseline_spike = baseline["metrics"]["spike_ratio"]

    candidates: list[dict[str, Any]] = []
    for item in results:
        candidate = dict(item)
        if item["status"] == "ok":
            candidate["baseline_energy_ratio"] = (
                item["metrics"]["electric_energy"] / baseline_energy
            )
            candidate["baseline_spike_ratio"] = (
                item["metrics"]["spike_ratio"] / baseline_spike
            )
        elif item["status"].startswith("ok"):
            candidate["baseline_energy_ratio"] = (
                item["metrics"]["electric_energy"] / baseline_energy
            )
            candidate["baseline_spike_ratio"] = (
                item["metrics"]["spike_ratio"] / baseline_spike
            )
        candidates.append(candidate)

    ranked_by_energy = sorted(
        successful, key=lambda item: item["metrics"]["electric_energy"], reverse=True
    )
    ranked_by_spike = sorted(
        successful, key=lambda item: item["metrics"]["spike_ratio"], reverse=True
    )
    return {
        "baseline_label": baseline["label"],
        "baseline_energy": baseline_energy,
        "baseline_spike_ratio": baseline_spike,
        "ranked_by_energy": [item["label"] for item in ranked_by_energy],
        "ranked_by_spike": [item["label"] for item in ranked_by_spike],
        "candidates": candidates,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# RZ JRhom reference-candidate scan",
        "",
        "This file is generated from current local run directories.",
        "",
        "## Provenance",
        "",
        f"- Generated at (UTC): `{payload['generated_at_utc']}`",
        f"- Hostname: `{payload['hostname']}`",
        f"- Working directory: `{payload['cwd']}`",
        f"- WarpX binary: `{payload['warpx_bin']}`",
        f"- Input file: `{payload['input_file']}`",
        "",
        "## Candidate Summary",
        "",
        "| Candidate | Status | Electric Energy | Energy / Baseline | Spike Ratio | Spike / Baseline |",
        "|---|---|---:|---:|---:|---:|",
    ]

    def fmt(value: Any) -> str:
        if value is None:
            return "n/a"
        if isinstance(value, (int, float)):
            return f"{value:.16e}"
        return str(value)

    for item in summary["candidates"]:
        if item["status"].startswith("ok"):
            lines.append(
                f"| `{item['label']}` | `{item['status']}` | "
                f"`{fmt(item['metrics']['electric_energy'])}` | "
                f"`{fmt(item['baseline_energy_ratio'])}` | "
                f"`{fmt(item['metrics']['spike_ratio'])}` | "
                f"`{fmt(item['baseline_spike_ratio'])}` |"
            )
        else:
            lines.append(
                f"| `{item['label']}` | `{item['status']}` | `n/a` | `n/a` | `n/a` | `n/a` |"
            )

    lines.extend(
        [
            "",
            "## Ranking",
            "",
            f"- Ranked by electric energy: `{summary['ranked_by_energy']}`",
            f"- Ranked by spike ratio: `{summary['ranked_by_spike']}`",
            "",
            "## Candidate Rationale",
            "",
        ]
    )
    for item in summary["candidates"]:
        lines.extend(
            [
                f"### `{item['label']}`",
                "",
                f"- Description: {item['description']}",
                f"- Overrides: `{item['overrides']}`",
                f"- Run directory: `{item['run_dir']}`",
                f"- Plotfile: `{item['plotfile']}`",
                f"- Status: `{item['status']}`",
                "",
            ]
        )
    return "\n".join(lines)


def write_outputs(payload: dict[str, Any], output_stem: Path) -> None:
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    md_path = output_stem.with_suffix(".md")
    json_path = output_stem.with_suffix(".json")
    md_path.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


def main() -> None:
    args = parse_args()
    if args.command_prefix and args.command_prefix_str:
        raise SystemExit(
            "Use either --command-prefix or --command-prefix-str, not both."
        )
    if args.command_prefix_str:
        args.command_prefix = shlex.split(args.command_prefix_str)
    numprocs_override = args.numprocs_override
    if numprocs_override is not None and numprocs_override.strip().lower() == "none":
        numprocs_override = None
    variants = build_variants(
        args.output_root.resolve(), args.target_step, numprocs_override
    )
    results = [run_variant(args, variant) for variant in variants]
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "cwd": str(Path.cwd()),
        "warpx_bin": str(args.warpx_bin.resolve()),
        "input_file": str(args.input_file.resolve()),
        "numprocs_override": numprocs_override,
        "command_prefix": args.command_prefix,
        "target_step": args.target_step,
        "summary": derive_summary(results),
    }
    write_outputs(payload, args.ledger_stem.resolve())


if __name__ == "__main__":
    main()
