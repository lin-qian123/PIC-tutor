#!/usr/bin/env python
"""Audit the explicit WarpX source guard that rejects Vay with mesh refinement."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument(
        "--runtime-log",
        type=Path,
        help="optional WarpX initialization log from an AMR-enabled Vay input",
    )
    parser.add_argument(
        "--runtime-exit-code",
        type=int,
        help="process exit code paired with --runtime-log",
    )
    parser.add_argument(
        "--copy-runtime-log",
        action="store_true",
        help="copy the local raw log next to --output-json; omit for portable public evidence",
    )
    args = parser.parse_args()

    root = args.warpx_root.resolve()
    project = args.project_root.resolve()
    warpx = read(root / "Source/WarpX.cpp")
    kernel = read(root / "Source/Particles/Deposition/CurrentDeposition.H")
    chapter = read(project / "manuscript/chapters/05-deposition-shapes.md")
    note = read(project / "notes/code-reading/particles/72-deposition-geometry-order-gap-register.md")
    guard = "WarpX::current_deposition_algo != CurrentDepositionAlgo::Vay ||\n            maxLevel() <= 0"
    checks = {
        "source_mesh_refinement_guard": guard in warpx,
        "source_guard_message": "Vay deposition not implemented with mesh refinement" in warpx,
        "source_vay_psatd_guard": "Vay deposition is implemented only for PSATD" in warpx,
        "source_vay_rz_guard": "Vay deposition not implemented in RZ geometry" in kernel,
        "source_vay_1d_guard": "Vay deposition not implemented in 1D geometry" in kernel,
        "chapter_amr_boundary": "AMR、边界裁剪" in chapter and "正式收敛阶" in chapter,
        "chapter_vay_configuration_reader_card": all(
            marker in chapter
            for marker in (
                "### 5.14.2.1 Vay 配置判读卡：先分开 pusher 和 deposition",
                "algo.particle_pusher = vay",
                "algo.current_deposition = vay",
                "配置接受、算法分派和物理验证是三道不同的门",
            )
        ),
        "gap_register_amr_boundary": "AMR 当前由 source guard" in note,
        "no_amr_runtime_pass_claim": "Vay AMR runtime PASS" not in chapter and "Vay AMR runtime PASS" not in note,
    }
    runtime = None
    if args.runtime_log:
        if args.runtime_exit_code is None:
            parser.error("--runtime-exit-code is required with --runtime-log")
        runtime_log = args.runtime_log.resolve()
        log_text = read(runtime_log)
        copied_log = args.output_json.parent / "runtime.log" if args.copy_runtime_log else None
        if copied_log:
            copied_log.parent.mkdir(parents=True, exist_ok=True)
            copied_log.write_text(log_text, encoding="utf-8")
        runtime_checks = {
            "runtime_amrex_initialized": "AMReX" in log_text and "initialized" in log_text,
            "runtime_mesh_refinement_assertion": "maxLevel() <= 0" in log_text,
            "runtime_guard_message": "Vay deposition not implemented with mesh refinement" in log_text,
            "runtime_abort": "MPI_Abort" in log_text,
            "runtime_exit_code": args.runtime_exit_code == 6,
        }
        checks.update(runtime_checks)
        runtime = {
            "log_file": copied_log.name if copied_log else None,
            "log_sha256": hashlib.sha256(log_text.encode("utf-8")).hexdigest(),
            "exit_code": args.runtime_exit_code,
            "raw_log_copied": bool(copied_log),
            "scope": "AMR-enabled Vay input with max_step=0; the process is expected to stop during initialization before a physics producer or consumer runs",
        }
    result = {
        "contract": "Vay deposition mesh-refinement source guard",
        "classification": "CURRENT_UPSTREAM_RUNTIME_GUARD_CONFIRMED_UNSUPPORTED" if runtime else "SOURCE_GUARD_AMR_RUNTIME_INTENTIONALLY_REJECTED",
        "scope": "read-only WarpX initialization/source guards; no AMR producer is interpreted as a physics runtime failure or pass",
        "checks": checks,
        "passed": all(checks.values()),
    }
    if runtime:
        result["runtime"] = runtime
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Vay deposition mesh-refinement source guard",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The current checkout rejects Vay when `maxLevel() > 0` during initialization. This is a source-defined support boundary, not a failed AMR physics experiment.",
    ]
    if runtime:
        lines += [
            "",
            f"Runtime evidence has SHA-256 `{runtime['log_sha256']}` and process exit code `{runtime['exit_code']}`.",
            "The input reaches AMReX initialization and then stops at the Vay/mesh-refinement assertion. It does not enter a field or charge consumer, so it proves an unsupported configuration boundary only.",
        ]
        if runtime["raw_log_copied"]:
            lines.append(f"The local raw log is stored as `{runtime['log_file']}`.")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {sum(checks.values())}/{len(checks)} Vay AMR guard checks")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
