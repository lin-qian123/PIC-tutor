#!/usr/bin/env python
"""Audit the live WarpX transition-zone source contract without editing WarpX."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


CHECKS = {
    "buffer_width_controls": (
        "Source/WarpX.H",
        ["n_field_gather_buffer", "n_current_deposition_buffer", "BuildBufferMasks"],
    ),
    "mask_construction": (
        "Source/WarpX.cpp",
        ["BuildBufferMasksInBox", "BuildBufferMasks ()"],
    ),
    "particle_partition": (
        "Source/Particles/Sorting/Partition.cpp",
        ["PartitionParticlesInBuffers", "stablePartition"],
    ),
    "evolve_route_inputs": (
        "Source/Particles/PhysicalParticleContainer.cpp",
        ["PartitionParticlesInBuffers", "nfine_deposit", "nfine_gather", "Efield_cax", "current_buf", "rho_buf"],
    ),
    "coarse_fine_sync": (
        "Source/Parallelization/WarpXComm.cpp",
        ["SyncCurrent", "SyncRho", "current_buf", "rho_buf"],
    ),
}


def find_line_numbers(text: str, patterns: list[str]) -> dict[str, int | None]:
    lines = text.splitlines()
    result = {}
    for pattern in patterns:
        result[pattern] = next(
            (index for index, line in enumerate(lines, start=1) if pattern in line), None
        )
    return result


def contains_any(root: Path, pattern: str, relative_dirs: tuple[str, ...]) -> list[str]:
    hits = []
    for relative_dir in relative_dirs:
        directory = root / relative_dir
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if re.search(pattern, text):
                hits.append(str(path.relative_to(root)))
    return hits


def git_commit(root: Path) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, default=Path("../warpx"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    root = args.warpx_root.resolve()

    check_results = {}
    for name, (relative_path, patterns) in CHECKS.items():
        path = root / relative_path
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        matches = find_line_numbers(text, patterns)
        check_results[name] = {
            "path": relative_path,
            "matches": matches,
            "passed": bool(path.exists() and all(value is not None for value in matches.values())),
        }

    dedicated_source_hits = contains_any(root, r"TransitionZoneRoutes", ("Source",))
    dedicated_test_hits = contains_any(root, r"amr_transition_zone|TransitionZoneRoutes", ("Examples/Tests",))
    result = {
        "warpx_root": str(root),
        "warpx_commit": git_commit(root),
        "checks": check_results,
        "dedicated_route_source_hits": dedicated_source_hits,
        "dedicated_route_test_hits": dedicated_test_hits,
        "all_source_contract_checks_passed": all(item["passed"] for item in check_results.values()),
        "dedicated_route_in_current_checkout": bool(dedicated_source_hits or dedicated_test_hits),
        "passed": all(item["passed"] for item in check_results.values()) and not (dedicated_source_hits or dedicated_test_hits),
        "evidence_level": "live source contract audit; not a runtime route-count regression",
        "scope": "read-only audit of the adjacent WarpX checkout",
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    status = "PASS" if result["passed"] else "FAIL"
    lines = [
        "# Transition-zone live source contract audit",
        "",
        f"- status: `{status}`",
        f"- WarpX commit: `{result['warpx_commit']}`",
        f"- source contract checks: `{result['all_source_contract_checks_passed']}`",
        f"- dedicated route implementation in checkout: `{result['dedicated_route_in_current_checkout']}`",
        f"- evidence level: {result['evidence_level']}",
        "",
        "| check | source | status | matched anchors |",
        "|---|---|---|---|",
    ]
    for name, item in check_results.items():
        anchors = ", ".join(f"`{key}`:{value}" for key, value in item["matches"].items())
        lines.append(f"| {name} | `{item['path']}` | `{item['passed']}` | {anchors} |")
    lines.extend(
        [
            "",
            "The absence of `TransitionZoneRoutes` and `amr_transition_zone` is recorded as a current-checkout boundary, not as a runtime pass.",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("transition-zone source contract audit failed")


if __name__ == "__main__":
    main()
