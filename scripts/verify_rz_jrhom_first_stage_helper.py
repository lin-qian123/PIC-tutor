#!/usr/bin/env python
"""Run and verify the RZ JRhom first-stage helper on positive/negative plotfiles."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_helper(helper: Path, plotfile: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(helper.resolve()), str(plotfile.resolve())],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "plotfile": str(plotfile.resolve()),
        "returncode": completed.returncode,
        "accepted": completed.returncode == 0,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--helper", type=Path, required=True)
    parser.add_argument("--baseline-plotfile", type=Path, required=True)
    parser.add_argument("--reference-plotfile", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    baseline = run_helper(args.helper, args.baseline_plotfile)
    reference = run_helper(args.helper, args.reference_plotfile)
    checks = {
        "baseline_helper_accepts": baseline["accepted"],
        "reference_helper_rejects": not reference["accepted"],
    }
    result = {
        "contract": "RZ JRhom first-stage helper execution contract",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "RZ_JRHOM_HELPER_BASELINE_ACCEPT_REFERENCE_REJECT",
        "scope": "direct execution of the generated helper on project-level MPI=2 plotfiles; not upstream CI",
        "helper": str(args.helper.resolve()),
        "baseline": baseline,
        "reference": reference,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# RZ JRhom first-stage helper execution contract",
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
        f"- baseline return code: `{baseline['returncode']}`",
        f"- reference return code: `{reference['returncode']}`",
        "- The reference rejection is expected from the generated energy ceiling; stdout/stderr are preserved in `contract.json`.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
