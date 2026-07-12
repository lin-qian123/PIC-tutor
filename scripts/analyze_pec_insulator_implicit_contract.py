#!/usr/bin/env python
"""Independent reduced-ledger contract for PECInsulator implicit energy balance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--case-name", default="test_2d_pec_field_insulator_implicit")
    args = parser.parse_args()

    case_dir = args.case_dir.resolve()
    reduced = case_dir / "diags/reducedfiles"
    fieldenergy = np.loadtxt(reduced / "fieldenergy.txt", skiprows=1)
    poynting = np.loadtxt(reduced / "poyntingflux.txt", skiprows=1)
    flux_loss = poynting[:, 7:].sum(axis=1)
    normalized_difference = (fieldenergy[:, 2] + flux_loss) / fieldenergy[:, 2].max()
    max_error = float(np.max(np.abs(normalized_difference)))
    threshold = 1.0e-13
    result = {
        "case": args.case_name,
        "fieldenergy_samples": int(fieldenergy.shape[0]),
        "poynting_samples": int(poynting.shape[0]),
        "initial_field_energy": float(fieldenergy[0, 2]),
        "final_field_energy": float(fieldenergy[-1, 2]),
        "max_normalized_energy_difference": max_error,
        "threshold": threshold,
        "energy_gate": max_error < threshold,
        "contract_pass": max_error < threshold,
    }
    (case_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (case_dir / "contract.md").write_text(
        "\n".join([
            "# PECInsulator implicit energy contract", "",
            f"- Reduced samples: field energy `{fieldenergy.shape[0]}`, Poynting flux `{poynting.shape[0]}`.",
            f"- Field energy: `{fieldenergy[0, 2]:.9e} -> {fieldenergy[-1, 2]:.9e} J`.",
            f"- Maximum normalized energy-accounting error: `{max_error:.9e}`; threshold `{threshold:.1e}`.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
