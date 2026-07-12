#!/usr/bin/env python
"""Audit the electron/ion-impact DSMC regression wiring without running WarpX."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WARPX = ROOT.parent / "warpx"


ANCHORS = {
    "cmake_electron_analysis_enabled": (
        WARPX / "Examples/Tests/ionization_dsmc/CMakeLists.txt",
        '    "analysis_ionization_dsmc_3d.py"  # analysis',
    ),
    "cmake_ion_analysis_disabled": (
        WARPX / "Examples/Tests/ionization_dsmc/CMakeLists.txt",
        'OFF # "analysis_ionization_dsmc_3d.py"  # analysis',
    ),
    "cmake_ion_checksum_surface": (
        WARPX / "Examples/Tests/ionization_dsmc/CMakeLists.txt",
        '"analysis_default_regression.py --path diags/diag1000250"  # checksum',
    ),
    "electron_input_cross_section": (
        WARPX / "Examples/Tests/ionization_dsmc/inputs_test_3d_ionization_electron_dsmc",
        "electron_impact_ionization.dat",
    ),
    "electron_input_species": (
        WARPX / "Examples/Tests/ionization_dsmc/inputs_test_3d_ionization_electron_dsmc",
        "ioniz.species = electrons neutrals",
    ),
    "ion_input_cross_section": (
        WARPX / "Examples/Tests/ionization_dsmc/inputs_test_3d_ionization_ion_dsmc",
        "ion_impact_ionization.dat",
    ),
    "ion_input_species": (
        WARPX / "Examples/Tests/ionization_dsmc/inputs_test_3d_ionization_ion_dsmc",
        "ioniz.species = ions neutrals",
    ),
    "analysis_electron_cross_section": (
        WARPX / "Examples/Tests/ionization_dsmc/analysis_ionization_dsmc_3d.py",
        "electron_impact_ionization.dat",
    ),
    "analysis_electron_species": (
        WARPX / "Examples/Tests/ionization_dsmc/analysis_ionization_dsmc_3d.py",
        'species="electrons"',
    ),
    "analysis_qmc_rate_model": (
        WARPX / "Examples/Tests/ionization_dsmc/analysis_ionization_dsmc_3d.py",
        "MultivariateNormalQMC",
    ),
}


def main() -> None:
    checks = []
    for name, (path, needle) in ANCHORS.items():
        text = path.read_text(encoding="utf-8")
        matches = [index + 1 for index, line in enumerate(text.splitlines()) if needle in line]
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
        "contract": "3D DSMC electron/ion-impact source and regression wiring",
        "anchor_count": len(checks),
        "passed_anchor_count": sum(item["matched"] for item in checks),
        "passed": passed,
        "classification": "ION_IMPACT_CHECKSUM_ONLY_ELECTRON_IMPACT_ANALYSIS_ACTIVE",
        "scope": "CMake/input/analysis source wiring; no runtime physics claim",
        "checks": checks,
    }
    output_dir = ROOT / "runs/stage-c-validation/ionization-dsmc-source-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 3D DSMC electron/ion-impact source contract",
        "",
        f"- status: `{'PASS' if passed else 'FAIL'}`",
        f"- anchors: `{result['passed_anchor_count']}/{result['anchor_count']}`",
        "- electron-impact sibling: active `analysis_ionization_dsmc_3d.py` plus checksum",
        "- ion-impact sibling: analysis disabled, final `diag1000250` checksum only",
        "- runtime boundary: this is a source/wiring audit, not an executed ion-impact physics validation",
        "",
    ]
    for item in checks:
        lines.append(
            f"- `{item['name']}`: `{'PASS' if item['matched'] else 'FAIL'}` "
            f"at `{item['path']}` lines `{item['line_numbers']}`"
        )
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit("ionization DSMC source contract failed")


if __name__ == "__main__":
    main()
