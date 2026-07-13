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


def input_contract(root: Path, template: Path) -> dict[str, object]:
    input_path = template / "inputs"
    if not input_path.is_file():
        return {
            "inputs_present": False,
            "referenced_files_present": False,
            "diagnostics_configured": False,
            "input_files": [],
        }
    text = input_path.read_text(encoding="utf-8")
    referenced = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("FILE ="):
            referenced.append(stripped.split("=", 1)[1].strip())
    input_files = [input_path]
    input_files.extend(template / name for name in referenced)
    return {
        "inputs_present": input_path.stat().st_size > 0,
        "referenced_files_present": all(path.is_file() for path in input_files),
        "diagnostics_configured": all(
            marker in "\n".join(path.read_text(encoding="utf-8") for path in input_files)
            for marker in ("diag_type = Full", "intervals")
        ),
        "input_files": [str(path.relative_to(root)) for path in input_files],
    }


def output_contract(run_dir: Path) -> dict[str, bool]:
    diagnostic_dirs = [path for path in (run_dir / "diags").glob("diag*") if path.is_dir()]
    return {
        "producer_log_present": (run_dir / "producer.log").is_file(),
        "used_inputs_present": (run_dir / "warpx_used_inputs").is_file(),
        "diagnostics_present": (run_dir / "diags").is_dir(),
        "diagnostic_dirs_present": bool(diagnostic_dirs),
    }


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
        contract = input_contract(root, template) if template.is_dir() else {
            "inputs_present": False,
            "referenced_files_present": False,
            "diagnostics_configured": False,
            "input_files": [],
        }
        planned.append(
            {
                **item,
                "run": f"runs/stage-c-validation/{run_name}",
                "binary_exists": binary.is_file(),
                "template_exists": template.is_dir(),
                **contract,
            }
        )
    prerequisite_checks = {
        "twelve_runs_declared": len(planned) == 12,
        "templates_present": all(item["template_exists"] for item in planned),
        "binaries_present": all(item["binary_exists"] for item in planned),
        "inputs_present": all(item["inputs_present"] for item in planned),
        "referenced_input_files_present": all(item["referenced_files_present"] for item in planned),
        "diagnostics_configured": all(item["diagnostics_configured"] for item in planned),
        "mpi_launcher_present": bool(launcher),
        "fixed_rank_count": EXPECTED_RANKS == 2,
        "single_rank_substitute_forbidden": True,
    }
    commands = []
    executions = []
    runtime_environment = {
        name: os.environ.get(name)
        for name in ("FI_PROVIDER", "FI_LOG_LEVEL", "MPICH_OFI_STARTUP_CONNECT")
        if os.environ.get(name) is not None
    }
    if args.execute:
        if not all(prerequisite_checks.values()):
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
                completed = subprocess.run(
                    command,
                    cwd=run_dir,
                    env=os.environ.copy(),
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    check=False,
                )
            executions.append(
                {
                    "run": item["run"],
                    "returncode": completed.returncode,
                    "output_contract": output_contract(run_dir),
                }
            )
    execution_checks = {}
    if args.execute:
        execution_checks = {
            "all_producers_exit_zero": all(item["returncode"] == 0 for item in executions),
            **{
                name: all(item["output_contract"][name] for item in executions)
                for name in ("producer_log_present", "used_inputs_present", "diagnostics_present", "diagnostic_dirs_present")
            },
        }
    checks = {**prerequisite_checks, **execution_checks}
    if all(checks.values()):
        classification = "REPEAT_FAMILY_RUNNER_READY" if not args.execute else "REPEAT_FAMILY_RUNNER_EXECUTION_PASS"
    elif not prerequisite_checks["mpi_launcher_present"]:
        classification = "REPEAT_FAMILY_RUNNER_BLOCKED_MPI_LAUNCHER_MISSING"
    else:
        classification = "REPEAT_FAMILY_RUNNER_BLOCKED_INPUT_OR_OUTPUT_CONTRACT"
    result = {
        "contract": "formal convergence repeat-family runner preflight",
        "passed": all(checks.values()),
        "ready_to_execute": all(prerequisite_checks.values()),
        "classification": classification,
        "scope": "twelve independent 2-rank producers: RZ/RSPHERE x 64/128/256 x correction on/off",
        "expected_ranks": EXPECTED_RANKS,
        "mpi_launcher": launcher or None,
        "checks": checks,
        "planned": planned,
        "commands": commands,
        "executions": executions,
        "runtime_environment": runtime_environment,
        "execution_requested": args.execute,
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
        f"- runtime environment: `{json.dumps(runtime_environment, ensure_ascii=False, sort_keys=True)}`",
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
