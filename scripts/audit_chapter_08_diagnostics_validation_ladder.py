#!/usr/bin/env python
"""Audit Chapter 8's reader-facing diagnostics validation ladder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def missing_markers(text: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    warpx = args.warpx_root.resolve()
    chapter = (ROOT / "manuscript/chapters/08-diagnostics-cases.md").read_text(encoding="utf-8")
    reduced = warpx / "Examples/Tests/reduced_diags"
    diff_lumi = warpx / "Examples/Tests/diff_lumi_diag"
    field_probe = warpx / "Examples/Tests/field_probe"
    uniform = warpx / "Examples/Physics_applications/uniform_plasma"
    source = warpx / "Source"

    reduced_cmake = (reduced / "CMakeLists.txt").read_text(encoding="utf-8")
    reduced_input = (reduced / "inputs_test_3d_reduced_diags").read_text(encoding="utf-8")
    reduced_analysis = (reduced / "analysis_reduced_diags_impl.py").read_text(encoding="utf-8")
    diff_cmake = (diff_lumi / "CMakeLists.txt").read_text(encoding="utf-8")
    diff_input = (diff_lumi / "inputs_base_3d").read_text(encoding="utf-8")
    diff_analysis = (diff_lumi / "analysis.py").read_text(encoding="utf-8")
    probe_cmake = (field_probe / "CMakeLists.txt").read_text(encoding="utf-8")
    probe_input = (field_probe / "inputs_test_2d_field_probe").read_text(encoding="utf-8")
    probe_analysis = (field_probe / "analysis.py").read_text(encoding="utf-8")
    uniform_cmake = (uniform / "CMakeLists.txt").read_text(encoding="utf-8")
    uniform_restart = (uniform / "inputs_test_3d_uniform_plasma_restart").read_text(encoding="utf-8")
    restart_analysis = (warpx / "Examples/analysis_default_restart.py").read_text(encoding="utf-8")
    evolve = (source / "Evolve/WarpXEvolve.cpp").read_text(encoding="utf-8")
    multi_diags = (source / "Diagnostics/MultiDiagnostics.cpp").read_text(encoding="utf-8")
    reduced_source = (source / "Diagnostics/ReducedDiags/ReducedDiags.cpp").read_text(encoding="utf-8")
    poynting = (source / "Diagnostics/ReducedDiags/FieldPoyntingFlux.cpp").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing_markers(
            chapter,
            [
                "### 8.14.3 修改诊断后的验证阶梯：先核 producer，再解释输出",
                "第一层：先确认调度与时间层真的到达",
                "第二层：改 compact reduced observable 时，以 full state 作 reference",
                "第三层：改 bin、轴标签或 openPMD reduced mesh 时，用解析谱而非文件形状验收",
                "第四层：改 sampling geometry、gather 或时间积分时，让 observable 匹配采样定义",
                "第五层：有跨步状态时，restart 与 checksum 只检查各自的生命周期",
                "不能把缺少 comparison 写成通过",
            ],
        ),
        "diagnostic_scheduling_contract": missing_markers(
            evolve,
            [
                "multi_diags->NewIteration()",
                "multi_diags->DoComputeAndPack(step) || reduced_diags->DoDiags(step)",
                "SynchronizeVelocityWithPosition()",
                "reduced_diags->ComputeDiags(step)",
                "reduced_diags->WriteToFile(step)",
                "multi_diags->FilterComputePackFlush( step )",
            ],
        )
        + missing_markers(multi_diags, ["MultiDiagnostics::DoComputeAndPack", "MultiDiagnostics::FilterComputePackFlush"])
        + missing_markers(reduced_source, ["ReducedDiags::WriteToFile", "ofs << step+1", "for (const auto& item : m_data)"]),
        "reduced_full_state_contract": missing_markers(
            reduced_cmake,
            ["test_3d_reduced_diags", "3  # dims", "2  # nprocs", '"analysis_reduced_diags.py diags/diag1000200"'],
        )
        + missing_markers(reduced_input, ["warpx.reduced_diags_names", "diagnostics.diags_names = diag1", "diag1.diag_type = Full"])
        + missing_markers(
            reduced_analysis,
            ["values_yt", "values_rd", "field_energy_tolerance = 0.3", "tolerance = 5e-3 if single_precision else 1e-12", "assert error[k] < tol"],
        ),
        "differential_luminosity_contract": missing_markers(
            diff_cmake,
            ["test_3d_diff_lumi_diag_leptons", "3  # dims", "2  # nprocs", '"analysis.py"'],
        )
        + missing_markers(
            diff_input,
            ["DifferentialLuminosity_beam1_beam2.type = DifferentialLuminosity", "DifferentialLuminosity2d_beam1_beam2.type = DifferentialLuminosity2D", "bin_number = 128", "bin_number_1 = 128", "bin_number_2 = 128"],
        )
        + missing_markers(
            diff_analysis,
            ["assert info.axes[0] == \"E2\"", "assert info.axes[1] == \"E1\"", "tol1 = 0.02", "tol2 = 0.04", "assert error1 < tol1", "assert error2 < tol2"],
        ),
        "field_probe_sampling_contract": missing_markers(
            probe_cmake,
            ["test_2d_field_probe", "2  # dims", "2  # nprocs", '"analysis.py"'],
        )
        + missing_markers(probe_input, ["FP_line.type = FieldProbe", "FP_line.integrate = 1", "FP_line.probe_geometry = Line", "FP_line.resolution = 201"])
        + missing_markers(probe_analysis, ["`[0]step()` == 500", "np.sinc", "assert averror < 2.5"]),
        "restart_and_accumulator_contract": missing_markers(
            uniform_cmake,
            ["test_3d_uniform_plasma_restart", "3  # dims", "2  # nprocs", '"analysis_default_restart.py diags/diag1000010"', "--rtol 1e-12"],
        )
        + missing_markers(uniform_restart, ["amr.restart = \"../test_3d_uniform_plasma/diags/chk000006\""])
        + missing_markers(restart_analysis, ["def check_restart(filename, tolerance=1e-12):", "for field in ds_benchmark.field_list:", "assert error < tolerance"])
        + missing_markers(poynting, ["FieldPoyntingFlux::WriteCheckpointData", "FieldPoyntingFlux::ReadCheckpointData", "FieldPoyntingFlux_data.txt"]),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_DIAGNOSTICS_VALIDATION_LADDER_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Source/Evolve/WarpXEvolve.cpp",
            "Source/Diagnostics/{MultiDiagnostics.cpp,ReducedDiags/ReducedDiags.cpp,ReducedDiags/FieldPoyntingFlux.cpp}",
            "Examples/Tests/reduced_diags/{CMakeLists.txt,inputs_test_3d_reduced_diags,analysis_reduced_diags_impl.py}",
            "Examples/Tests/diff_lumi_diag/{CMakeLists.txt,inputs_base_3d,analysis.py}",
            "Examples/Tests/field_probe/{CMakeLists.txt,inputs_test_2d_field_probe,analysis.py}",
            "Examples/Physics_applications/uniform_plasma/{CMakeLists.txt,inputs_test_3d_uniform_plasma_restart}",
            "Examples/analysis_default_restart.py",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The card separates scheduling, reduced/full-state consistency, analytic spectra, sampled fluence, and restart/checksum consumers.",
            "It does not establish new geometry, interval, binning, MPI-layout, or physical-reference coverage.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 8 Diagnostics Validation Ladder",
        "",
        "Classification: `SOURCE_GROUNDED_DIAGNOSTICS_VALIDATION_LADDER_READER_CARD`.",
        "",
        f"Result: {'PASS' if passed else 'FAIL'}.",
        "",
        "## Source Routes",
        "",
    ]
    lines.extend(f"- `{route}`" for route in payload["source_routes"])
    lines.extend(["", "## Checks", ""])
    for name, missing in checks.items():
        lines.append(f"- `{name}`: `{'PASS' if not missing else 'FAIL'}`")
        if missing:
            lines.extend(f"  - missing: `{marker}`" for marker in missing)
    lines.extend(["", "## Scope", ""])
    lines.extend(f"- {item}" for item in payload["scope"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
