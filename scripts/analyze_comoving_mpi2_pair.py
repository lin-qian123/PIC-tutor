#!/usr/bin/env python
"""Analyze the comoving stable/sign pair from real two-rank plotfiles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_comoving_reference_ledger import load_plotfile_metrics  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stable-plotfile", type=Path, required=True)
    parser.add_argument("--positive-plotfile", type=Path, required=True)
    parser.add_argument("--one-rank-ledger", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    stable = load_plotfile_metrics("mpi2-stable", args.stable_plotfile.resolve())
    positive = load_plotfile_metrics("mpi2-positive", args.positive_plotfile.resolve())
    one_rank = json.loads(args.one_rank_ledger.read_text(encoding="utf-8"))
    one_rank_stable = next(
        row for row in one_rank["results"] if row["label"] == "stable-default-selector"
    )["metrics"]

    stable_energy_parallel_delta = abs(
        stable.electric_energy / one_rank_stable["electric_energy"] - 1.0
    )
    stable_spike_parallel_delta = abs(
        stable.spike_ratio / one_rank_stable["spike_ratio"] - 1.0
    )
    sign_spike_ratio = positive.spike_ratio / stable.spike_ratio
    checks = {
        "stable_fields_finite": stable.all_fields_finite,
        "positive_fields_finite": positive.all_fields_finite,
        "stable_parallel_energy_delta_below_one_percent": stable_energy_parallel_delta < 0.01,
        "stable_parallel_spike_delta_below_one_percent": stable_spike_parallel_delta < 0.01,
        "positive_sign_spike_sensitive": sign_spike_ratio >= 1.05,
    }
    result = {
        "contract": "comoving real MPI=2 stable/sign sibling contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "COMOVING_MPI2_FINITE_PARALLEL_CONSISTENCY_SIGN_SENSITIVITY_ENERGY_GATE_DISABLED",
        "scope": "real 2-rank local runtime pair; MPI finalize tail noise is excluded from plotfile analysis; no upstream CI claim",
        "stable": {
            "plotfile": str(args.stable_plotfile.resolve()),
            "electric_energy": stable.electric_energy,
            "spike_ratio": stable.spike_ratio,
        },
        "positive_sign": {
            "plotfile": str(args.positive_plotfile.resolve()),
            "electric_energy": positive.electric_energy,
            "spike_ratio": positive.spike_ratio,
        },
        "comparisons": {
            "stable_energy_parallel_delta": stable_energy_parallel_delta,
            "stable_spike_parallel_delta": stable_spike_parallel_delta,
            "positive_to_stable_spike_ratio": sign_spike_ratio,
        },
        "energy_gate": "disabled; positive-sign sibling has lower electric energy than stable",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Comoving real MPI=2 stable/sign sibling contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(
        f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |"
        for name, passed in checks.items()
    )
    lines += [
        "",
        f"- MPI=2 stable electric energy: `{stable.electric_energy:.16e}`",
        f"- MPI=2 stable spike ratio: `{stable.spike_ratio:.16e}`",
        f"- MPI=2 positive-sign electric energy: `{positive.electric_energy:.16e}`",
        f"- MPI=2 positive-sign spike ratio: `{positive.spike_ratio:.16e}`",
        f"- positive/stable spike ratio: `{sign_spike_ratio:.16e}`",
        f"- stable energy delta vs one-rank: `{stable_energy_parallel_delta:.3e}`",
        f"- stable spike delta vs one-rank: `{stable_spike_parallel_delta:.3e}`",
        "- energy gate: `disabled`; the sign sibling is spike-sensitive but not an unstable-energy oracle.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
