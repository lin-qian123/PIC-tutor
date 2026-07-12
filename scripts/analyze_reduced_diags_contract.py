#!/usr/bin/env python
"""Run and summarize WarpX's reduced-diagnostics contract analysis."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ERROR_RE = re.compile(r"^relative error =\s+(.+)$")
YT_RE = re.compile(r"^values_yt\[(.+)\] =\s+(.+)$")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("plotfile")
    parser.add_argument("--analysis-script", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    args = parser.parse_args()

    root = Path(args.run_dir).resolve()
    completed = subprocess.run(
        [sys.executable, str(Path(args.analysis_script).resolve()), args.plotfile],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    log = completed.stdout + completed.stderr
    (root / "reduced-diags-analysis.log").write_text(log)

    current_key = None
    comparisons = []
    for line in log.splitlines():
        match = YT_RE.match(line)
        if match:
            current_key = match.group(1)
            continue
        match = ERROR_RE.match(line)
        if match and current_key is not None:
            value = float(match.group(1))
            comparisons.append({"observable": current_key, "relative_error": value})
            current_key = None

    if not comparisons:
        raise SystemExit("official reduced-diags analysis produced no comparison records")

    max_record = max(comparisons, key=lambda item: item["relative_error"])
    non_energy = [
        item for item in comparisons if item["observable"] != "field energy"
    ]
    result = {
        "run_dir": str(root),
        "plotfile": args.plotfile,
        "mpi_processes": _read_mpi_processes(root),
        "official_analysis_exit_code": completed.returncode,
        "comparison_count": len(comparisons),
        "max_relative_error": max_record["relative_error"],
        "max_relative_error_observable": max_record["observable"],
        "max_non_field_energy_relative_error": max(
            item["relative_error"] for item in non_energy
        ),
        "field_energy_relative_error": next(
            item["relative_error"]
            for item in comparisons
            if item["observable"] == "field energy"
        ),
        "field_energy_tolerance": 0.3,
        "other_observable_tolerance": 1.0e-12,
        "passed": completed.returncode == 0,
        "comparisons": comparisons,
    }
    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n")
    Path(args.output_md).write_text(
        "\n".join(
            [
                "# Reduced-diagnostics contract report",
                "",
                f"- MPI processes: `{result['mpi_processes']}`",
                f"- compared observables: `{result['comparison_count']}`",
                f"- maximum relative error: `{result['max_relative_error']:.3e}` (`{result['max_relative_error_observable']}`)",
                f"- field-energy relative error: `{result['field_energy_relative_error']:.3e}`",
                f"- maximum non-field-energy relative error: `{result['max_non_field_energy_relative_error']:.3e}`",
                f"- official analysis result: `{'PASS' if result['passed'] else 'FAIL'}`",
                "",
                "The report wraps WarpX's official `analysis_reduced_diags.py`; field energy uses its dedicated `0.3` tolerance because the plotfile reference is cell-centered while the reduced diagnostic uses Yee-staggered fields. Other observables retain the official `1e-12` tolerance.",
                "",
            ]
        )
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("official reduced-diags analysis failed")


def _read_mpi_processes(root: Path) -> int | None:
    candidates = sorted(root.glob("diags/diag*/warpx_job_info"))
    if not candidates:
        return None
    for line in candidates[-1].read_text().splitlines():
        if line.startswith("number of MPI processes:"):
            return int(line.split(":", 1)[1].strip())
    return None


if __name__ == "__main__":
    main()
