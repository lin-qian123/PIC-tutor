#!/usr/bin/env python
"""Audit the source wiring behind the RZ secondary-emission geometry gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WARPX = ROOT.parent / "warpx"

ANCHORS = {
    "python_callback_buffer_wrapper": (
        WARPX / "Examples/Tests/secondary_ion_emission/inputs_test_rz_secondary_ion_emission_picmi.py",
        "ParticleBoundaryBufferWrapper()",
    ),
    "python_reads_rz_position": (
        WARPX / "Examples/Tests/secondary_ion_emission/inputs_test_rz_secondary_ion_emission_picmi.py",
        'get_particle_scraped_this_step("ions", "eb", "r", lev)',
    ),
    "python_reads_eb_normal": (
        WARPX / "Examples/Tests/secondary_ion_emission/inputs_test_rz_secondary_ion_emission_picmi.py",
        'get_particle_scraped_this_step("ions", "eb", "nx", lev)',
    ),
    "python_reads_scrape_time": (
        WARPX / "Examples/Tests/secondary_ion_emission/inputs_test_rz_secondary_ion_emission_picmi.py",
        'get_particle_scraped_this_step("ions", "eb", "deltaTimeScraped", lev)',
    ),
    "python_remaining_dt_reinjection": (
        WARPX / "Examples/Tests/secondary_ion_emission/inputs_test_rz_secondary_ion_emission_picmi.py",
        "x=xe + (dt - delta_te) * uxe",
    ),
    "python_callback_registered": (
        WARPX / "Examples/Tests/secondary_ion_emission/inputs_test_rz_secondary_ion_emission_picmi.py",
        "callbacks.installafterstep(secondary_emission)",
    ),
    "wrapper_filters_current_step": (
        WARPX / "Python/pywarpx/particle_containers.py",
        "data[step == current_step]",
    ),
    "eb_signed_distance_selection": (
        WARPX / "Source/Particles/ParticleBoundaryBuffer.cpp",
        "return phi_value < 0.0 ? 1 : 0;",
    ),
    "eb_intersection_transform": (
        WARPX / "Source/Particles/ParticleBoundaryBuffer.cpp",
        "FindEmbeddedBoundaryIntersection{step_scraped_index, delta_index",
    ),
    "eb_buffer_timestamp_components": (
        WARPX / "Source/Particles/ParticleBoundaryBuffer.cpp",
        'buffer[i].AddRealComp("deltaTimeScraped", true);',
    ),
}


def main() -> None:
    checks = []
    for name, (path, needle) in ANCHORS.items():
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        matches = [index + 1 for index, line in enumerate(lines) if needle in line]
        checks.append(
            {
                "name": name,
                "path": str(path),
                "needle": needle,
                "matched": bool(matches),
                "line_numbers": matches,
            }
        )
    passed = all(item["matched"] for item in checks)
    result = {
        "contract": "RZ secondary-emission EB callback/source wiring audit",
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["matched"] for item in checks),
        "passed": passed,
        "checks": checks,
        "interpretation": "source wiring is present; this does not close the 64x64 runtime impact-point geometry gate",
    }
    output_dir = ROOT / "runs/stage-c-validation/secondary-emission-eb-source-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    status = "PASS" if passed else "FAIL"
    lines = [
        "# RZ secondary-emission EB source contract",
        "",
        f"- status: `{status}`",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        "- source chain: signed-distance EB selection -> intersection/normal/time stamp -> current-step Python callback -> remaining-dt reinjection",
        "- runtime boundary: this source audit does not close the 64x64 impact-point geometry gate",
        "",
    ]
    for item in checks:
        lines.append(f"- `{item['name']}`: `{'PASS' if item['matched'] else 'FAIL'}` at `{item['path']}` lines `{item['line_numbers']}`")
    (output_dir / "contract.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit("secondary-emission EB source contract failed")


if __name__ == "__main__":
    main()
