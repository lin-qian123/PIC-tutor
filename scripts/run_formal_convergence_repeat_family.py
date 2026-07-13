#!/usr/bin/env python
"""Preflight or run the preregistered second 2-rank convergence family."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_RANKS = 2


def specs() -> list[dict[str, str]]:
    rows = []
    for geometry, binary, templates in (
        (
            "RZ",
            "../warpx/build_full/bin/warpx.rz.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES",
            {
                "on": "esirkepov_langmuir_rz_mpi2",
                "off": "esirkepov_langmuir_rz_no_verboncoeur_mpi2",
            },
        ),
        (
            "RSPHERE",
            "../warpx/build_full/bin/warpx.rsphere.MPI.OMP.DP.PDP.OPMD.FFT.EB.QED.GENQEDTABLES",
            {
                "on": "esirkepov_langmuir_rsphere_charge_mpi2",
                "off": "esirkepov_langmuir_rsphere_charge_no_verboncoeur_mpi2",
            },
        ),
    ):
        for resolution in (64, 128, 256):
            for correction, template in templates.items():
                if geometry == "RZ":
                    if resolution == 64:
                        template_name = template
                    elif resolution == 128:
                        template_name = f"esirkepov_langmuir_rz_resolution128_{'no_verboncoeur_' if correction == 'off' else ''}mpi2"
                    else:
                        template_name = f"esirkepov_langmuir_rz_resolution256_{'on' if correction == 'on' else 'off'}_mpi2"
                else:
                    if resolution == 64:
                        template_name = template
                    else:
                        template_name = f"esirkepov_langmuir_rsphere_charge_n{resolution}_{correction}_mpi2"
                rows.append(
                    {
                        "geometry": geometry,
                        "resolution": str(resolution),
                        "correction": correction,
                        "template": f"runs/stage-c-validation/{template_name}",
                        "binary": binary,
                    }
                )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--mpi-launcher", default=os.environ.get("MPIEXEC", ""))
    parser.add_argument("--execute", action="store_true", help="run all twelve planned repeat producers")
    args = parser.parse_args()
    root = args.root.resolve()
    launcher = args.mpi_launcher or shutil.which("mpiexec") or shutil.which("mpirun")
    planned = []
    for item in specs():
        template = root / item["template"]
        binary = (root / item["binary"]).resolve()
        run_name = f"formal-repeat-{item['geometry'].lower()}-{item['resolution']}-{item['correction']}"
        planned.append({**item, "run": f"runs/stage-c-validation/{run_name}", "binary_exists": binary.is_file(), "template_exists": template.is_dir()})
    checks = {
        "twelve_runs_declared": len(planned) == 12,
        "templates_present": all(item["template_exists"] for item in planned),
        "binaries_present": all(item["binary_exists"] for item in planned),
        "mpi_launcher_present": bool(launcher),
        "fixed_rank_count": EXPECTED_RANKS == 2,
        "single_rank_substitute_forbidden": True,
    }
    commands = []
    executions = []
    if args.execute:
        if not all(checks.values()):
            raise SystemExit("repeat-family preflight failed; use the report to resolve prerequisites")
        for item in planned:
            template = root / item["template"]
            run_dir = root / item["run"]
            run_dir.mkdir(parents=True, exist_ok=True)
            for name in ("inputs", "inputs_base_rz"):
                source = template / name
                if source.is_file():
                    shutil.copy2(source, run_dir / name)
            binary = (root / item["binary"]).resolve()
            command = [launcher, "-n", str(EXPECTED_RANKS), str(binary), "inputs"]
            commands.append(command)
            with (run_dir / "producer.log").open("w", encoding="utf-8") as log:
                completed = subprocess.run(command, cwd=run_dir, stdout=log, stderr=subprocess.STDOUT, check=False)
            executions.append({"run": item["run"], "returncode": completed.returncode})
        checks["all_producers_exit_zero"] = all(item["returncode"] == 0 for item in executions)
    result = {
        "contract": "formal convergence repeat-family runner preflight",
        "passed": all(checks.values()),
        "ready_to_execute": all(checks.values()),
        "classification": "REPEAT_FAMILY_RUNNER_READY" if all(checks.values()) else "REPEAT_FAMILY_RUNNER_BLOCKED_MPI_LAUNCHER_MISSING",
        "scope": "twelve independent 2-rank producers: RZ/RSPHERE x 64/128/256 x correction on/off",
        "expected_ranks": EXPECTED_RANKS,
        "mpi_launcher": launcher or None,
        "checks": checks,
        "planned": planned,
        "commands": commands,
        "executions": executions,
        "single_rank_substitute": "forbidden",
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Formal convergence repeat-family runner preflight",
        "",
        f"- classification: `{result['classification']}`",
        f"- contract: `{'PASS' if result['passed'] else 'BOUNDARY'}`",
        f"- ready to execute: `{result['ready_to_execute']}`",
        f"- expected MPI ranks: `{EXPECTED_RANKS}`",
        f"- MPI launcher: `{launcher or 'missing'}`",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'BOUNDARY'}` |" for name, passed in checks.items())
    lines.extend(["", "A single-rank run is not an acceptable substitute for this preregistered 2-rank family."])
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
