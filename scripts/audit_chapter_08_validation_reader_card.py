#!/usr/bin/env python
"""Audit the source and reader-facing contract of Chapter 8 validation card."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    warpx = args.warpx_root.resolve()
    project = args.project_root.resolve()
    chapter = read(project, "manuscript/chapters/08-diagnostics-cases.md")

    field_probe_input = read(warpx, "Examples/Tests/field_probe/inputs_test_2d_field_probe")
    field_probe_analysis = read(warpx, "Examples/Tests/field_probe/analysis.py")
    field_probe_cmake = read(warpx, "Examples/Tests/field_probe/CMakeLists.txt")
    capacitive_input = read(warpx, "Examples/Physics_applications/capacitive_discharge/inputs_base_1d_picmi.py")
    capacitive_analysis = read(warpx, "Examples/Physics_applications/capacitive_discharge/analysis_1d.py")
    capacitive_cmake = read(warpx, "Examples/Physics_applications/capacitive_discharge/CMakeLists.txt")
    pierce_input = read(warpx, "Examples/Physics_applications/pierce_diode/inputs_test_1d_pierce_diode")
    pierce_analysis = read(warpx, "Examples/Physics_applications/pierce_diode/analysis_pierce_diode.py")
    pierce_cmake = read(warpx, "Examples/Physics_applications/pierce_diode/CMakeLists.txt")
    warpx_revision = subprocess.check_output(
        ["git", "-C", str(warpx), "rev-parse", "HEAD"], text=True
    ).strip()

    checks = {
        "reader_card_present": all(
            marker in chapter
            for marker in (
                "### 验证合同判读卡：相同的“通过”并不表示相同的正确性",
                "归一化时间积分 Poynting-flux 形状",
                "interior RMS relative error `< 6%`",
                "`phi[1:]`",
                "不能把一次 PASS 推广成“该应用已经验证”",
            )
        ),
        "capacitive_active_tests_do_not_claim_python_solver": (
            '"inputs_base_1d_picmi.py --test"' in capacitive_cmake
            and '"inputs_base_1d_picmi.py --test --dsmc"' in capacitive_cmake
            and "--pythonsolver" not in capacitive_cmake
        ),
        "capacitive_profile_contract": all(
            marker in capacitive_input + capacitive_analysis
            for marker in (
                "callbacks.installafterstep(self._get_rho_ions)",
                'np.save(f"ion_density_case_{self.n + 1}.npy", self.ion_density_array)',
                'np.load("ion_density_case_1.npy")',
                "density_data[1:-1]",
                "tolerance = 0.06",
                "assert rms_rel_err < tolerance",
            )
        ),
        "field_probe_contract": all(
            marker in field_probe_input + field_probe_analysis + field_probe_cmake
            for marker in (
                "if(WarpX_EB)",
                "FP_line.type = FieldProbe",
                "FP_line.integrate = 1",
                "FP_line.probe_geometry = Line",
                "FP_line.resolution = 201",
                'query("`[0]step()` == 500")',
                '"[11]part_S_lev0-(W*s/m^2)"',
                "assert averror < 2.5",
            )
        ),
        "pierce_diode_contract": all(
            marker in pierce_input + pierce_analysis + pierce_cmake
            for marker in (
                "warpx.do_electrostatic = labframe",
                "ions.flux = J_CL/q_e",
                "diag1.format=openpmd",
                '"analysis_pierce_diode.py diags/diag1/"',
                "phi[1:]",
                "rel_error_jz",
                "tolerance = 0.2",
            )
        ),
    }
    result = {
        "contract": "chapter 8 validation reader card",
        "classification": "SOURCE_GROUNDED_READER_VALIDATION_CONTRACT",
        "warpx_revision": warpx_revision,
        "warpx_source_paths": [
            "Examples/Tests/field_probe/",
            "Examples/Physics_applications/capacitive_discharge/",
            "Examples/Physics_applications/pierce_diode/",
        ],
        "checks": checks,
        "passed": all(checks.values()),
        "scope": (
            "Source and reader-text consistency for three named validation contracts. "
            "It does not rerun WarpX or promote the contracts to general physics proof."
        ),
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 8 validation reader-card contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- WarpX revision: `{warpx_revision}`",
        "- checked source paths: `Examples/Tests/field_probe/`, `Examples/Physics_applications/capacitive_discharge/`, `Examples/Physics_applications/pierce_diode/`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
