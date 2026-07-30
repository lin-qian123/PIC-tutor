#!/usr/bin/env python
"""Audit transition-zone branch activation without overclaiming route closure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def contains(path: Path, marker: str) -> bool:
    return path.is_file() and marker in path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--source-contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    run_dir = args.run_dir if args.run_dir.is_absolute() else root / args.run_dir
    source_contract_path = (
        args.source_contract
        if args.source_contract.is_absolute()
        else root / args.source_contract
    )
    inputs = run_dir / "warpx_used_inputs"
    runtime_log = run_dir / "run.log"
    output_contract = run_dir / "contract.json"
    source_contract = json.loads(source_contract_path.read_text(encoding="utf-8"))
    workflow_contract = json.loads(output_contract.read_text(encoding="utf-8"))
    chapter = (root / "manuscript/chapters/07-boundaries-amr.md").read_text(
        encoding="utf-8"
    )

    checks = {
        "source_contract_passed": source_contract.get("passed") is True,
        "two_level_amr_workflow": contains(inputs, "amr.max_level = 1"),
        "subcycling_enabled": contains(inputs, "warpx.do_subcycling = 1"),
        "deposit_on_main_grid_species_declared": contains(
            inputs, "particles.deposit_on_main_grid = plasma_e plasma_p"
        ),
        "buffer_controls_present": contains(inputs, "warpx.n_current_deposition_buffer")
        and contains(inputs, "warpx.n_field_gather_buffer"),
        "partition_runtime_marker": contains(
            runtime_log, "PhysicalParticleContainer::PartitionParticlesInBuffers"
        ),
        "owner_mask_runtime_marker": contains(runtime_log, "OwnerMask()"),
        "workflow_contract_passed": workflow_contract.get("passed") is True,
        "chapter_transition_zone_reader_card": all(
            marker in chapter
            for marker in (
                "### 7.9.1 Transition-zone 判读卡：分支被进入，不等于每条 route 已验证",
                "gather 与 deposition 分别有自己的 buffer mask",
                "runtime marker 说明相关分支曾被进入",
                "route ledger 才说明每条 route",
            )
        ),
        "route_count_not_claimed": True,
    }
    result = {
        "contract": "transition-zone runtime activation boundary",
        "classification": "RUNTIME_TRANSITION_ZONE_BRANCH_ACTIVATION_OBSERVED_ROUTE_LEDGER_UNPROVEN",
        "passed": all(checks.values()),
        "checks": checks,
        "run_dir": str(run_dir),
        "runtime_markers": {
            "partition": "PhysicalParticleContainer::PartitionParticlesInBuffers",
            "owner_mask": "OwnerMask()",
        },
        "scope": (
            "Existing 2-rank two-level AMR subcycling run and source audit show that the "
            "transition-zone partition/synchronization branch was exercised. The run does "
            "not expose per-particle route IDs, fine/buffer route counts, current_buf/rho_buf "
            "pre-sync values, or post-sync ledger fields, so route-count closure remains open."
        ),
        "source_contract": str(source_contract_path),
        "workflow_contract": str(output_contract),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Transition-zone runtime activation contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- run: `{run_dir}`",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(
        f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |"
        for name, passed in checks.items()
    )
    lines.extend(
        [
            "",
            "The runtime log shows branch activation, including "
            "`PartitionParticlesInBuffers` and `OwnerMask()`. It does not provide a "
            "route-count ledger or pre/post-sync `current_buf/rho_buf` fields; the "
            "transition-zone closure therefore remains open.",
        ]
    )
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
