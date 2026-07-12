#!/usr/bin/env python
"""Validate the comoving velocity sibling scan without enabling an energy gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.ledger_json.read_text(encoding="utf-8"))
    rows = {row["label"]: row for row in payload["results"]}

    stable = rows["stable-default-selector"]["metrics"]
    explicit = rows["explicit-default-beta"]["metrics"]
    zero = rows["zero-comoving"]["metrics"]
    positive = rows["positive-default-beta"]["metrics"]

    explicit_energy_rel = abs(explicit["electric_energy"] / stable["electric_energy"] - 1.0)
    explicit_spike_rel = abs(explicit["spike_ratio"] / stable["spike_ratio"] - 1.0)
    checks = {
        "all_candidates_completed": all(row["status"] == "ok" for row in rows.values()),
        "explicit_default_matches_selector_energy": explicit_energy_rel <= 1.0e-10,
        "explicit_default_matches_selector_spike": explicit_spike_rel <= 1.0e-10,
        "no_comoving_exceeds_current_spike_ceiling": zero["spike_ratio"] > 1.1114823702056489,
        "positive_sign_is_spike_sensitive": positive["spike_ratio"] / stable["spike_ratio"] >= 1.05,
    }
    result = {
        "contract": "comoving velocity selector and sign sibling contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "COMOVING_SELECTOR_EQUIVALENCE_SIGN_SENSITIVITY_ENERGY_GATE_DISABLED",
        "scope": "local 2D hybrid PSATD sibling scan; no unstable-energy oracle and no upstream CI claim",
        "metrics": {
            "explicit_default_energy_relative_difference": explicit_energy_rel,
            "explicit_default_spike_relative_difference": explicit_spike_rel,
            "stable_spike_ratio": stable["spike_ratio"],
            "no_comoving_spike_ratio": zero["spike_ratio"],
            "positive_sign_spike_ratio": positive["spike_ratio"],
        },
        "energy_gate": "disabled",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Comoving velocity selector and sign sibling contract",
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
        f"- explicit/default energy relative difference: `{explicit_energy_rel:.3e}`",
        f"- explicit/default spike relative difference: `{explicit_spike_rel:.3e}`",
        f"- no-comoving spike ratio: `{zero['spike_ratio']:.16e}`",
        f"- positive-sign spike ratio: `{positive['spike_ratio']:.16e}`",
        "- energy gate: `disabled`; the scan does not identify a reliable unstable-energy oracle.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
