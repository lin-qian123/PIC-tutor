#!/usr/bin/env python
"""Build a consistent family matrix from the three RZ Langmuir PSATD contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_CASES = {
    "standard": "runs/stage-c-validation/rz_langmuir_multi_psatd_mpi2/contract.json",
    "current-correction": "runs/stage-c-validation/rz_langmuir_multi_psatd_current_correction_mpi1/contract.json",
    "JRhom-CL4": "runs/stage-c-validation/rz_langmuir_multi_psatd_jrhom_ll4_mpi2/contract.json",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    for label, default in DEFAULT_CASES.items():
        parser.add_argument(f"--{label.replace('_', '-')}-json", type=Path, default=default)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    paths = {
        "standard": args.standard_json,
        "current-correction": args.current_correction_json,
        "JRhom-CL4": args.JRhom_CL4_json,
    }
    cases = {label: json.loads(path.read_text(encoding="utf-8")) for label, path in paths.items()}
    for label, case in cases.items():
        if case.get("geometry_dims") != "RZ" or case.get("maxwell_solver") != "psatd":
            raise AssertionError(f"{label} is not an RZ PSATD contract")
        if not case.get("passed"):
            raise AssertionError(f"{label} field contract did not pass")
        if case.get("current_deposition") != "direct":
            raise AssertionError(f"{label} does not use direct deposition")

    rows = []
    for label, case in cases.items():
        rows.append(
            {
                "case": label,
                "plotfile_dimensions": case.get("plotfile_dimensions"),
                "current_correction": case.get("current_correction"),
                "jrhom": case.get("jrhom"),
                "er_error": case["relative_er_error"],
                "ez_error": case["relative_ez_error"],
                "field_tolerance": case["field_tolerance"],
                "charge_status": "PASS" if case.get("charge_passed") else "NOT_APPLICABLE",
                "overall_status": "PASS",
            }
        )
    result = {
        "contract": "RZ Langmuir PSATD family matrix",
        "case_count": len(rows),
        "all_field_contracts_passed": True,
        "rows": rows,
        "interpretation": {
            "standard": "standard RZ PSATD analytic field and filter workflow",
            "current-correction": "analytic field plus same-surface charge-conservation gate",
            "JRhom-CL4": "RZ PSATD-JRhom CL4 analytic field and filter workflow; charge gate not applicable",
        },
        "scope": "project-level family matrix from official-input runtime contracts; not an all-geometry convergence study",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# RZ Langmuir PSATD family matrix",
        "",
        "| case | dimensions | current correction | JRhom | Er error | Ez error | charge | status |",
        "|---|---|---:|---|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['case']}` | `{row['plotfile_dimensions']}` | `{row['current_correction']}` | "
            f"`{row['jrhom'] or '-'}` | `{row['er_error']:.6e}` | `{row['ez_error']:.6e}` | "
            f"`{row['charge_status']}` | `PASS` |"
        )
    lines.extend(
        [
            "",
            "- All three cases use RZ + PSATD + direct deposition and pass the `<0.12` analytic `Er/Ez` field gate.",
            "- Only the current-correction sibling adds the `1e-9` same-surface charge-conservation gate.",
            "- The matrix is a family-level evidence summary, not an all-geometry or formal convergence study.",
            "",
        ]
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
