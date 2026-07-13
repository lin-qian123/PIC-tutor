#!/usr/bin/env python
"""Audit representative Chapter 6 claims against the current WarpX source tree."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    project = args.project_root.resolve()
    warpx = args.warpx_root.resolve()
    chapter = read(project / "manuscript/chapters/06-field-solvers.md")

    sources = {
        "evolve": read(warpx / "Source/Evolve/WarpXEvolve.cpp"),
        "push_em": read(warpx / "Source/FieldSolver/WarpXPushFieldsEM.cpp"),
        "spectral": read(warpx / "Source/FieldSolver/SpectralSolver/SpectralSolver.cpp"),
        "spectral_rz": read(warpx / "Source/FieldSolver/SpectralSolver/SpectralSolverRZ.cpp"),
        "pml_component": read(warpx / "Source/BoundaryConditions/PMLComponent.H"),
        "pml": read(warpx / "Source/BoundaryConditions/PML.cpp"),
        "fdtd_b": read(warpx / "Source/FieldSolver/FiniteDifferenceSolver/EvolveB.cpp"),
        "fdtd_e": read(warpx / "Source/FieldSolver/FiniteDifferenceSolver/EvolveE.cpp"),
        "pml_b": read(warpx / "Source/FieldSolver/FiniteDifferenceSolver/EvolveBPML.cpp"),
        "pml_e": read(warpx / "Source/FieldSolver/FiniteDifferenceSolver/EvolveEPML.cpp"),
    }

    checks = [
        ("chapter_topology", "正文外层推进顺序与 JRhom 入口", chapter, ["SyncCurrentAndRho()", "PushPSATD()", "EvolveB(dt/2)", "OneStep_JRhom"]),
        ("chapter_fdtd_pml", "正文 FDTD/PML 入口", chapter, ["EvolveB.cpp", "EvolveE.cpp", "EvolveBPML.cpp", "EvolveEPML.cpp", "PML::Exchange()"]),
        ("chapter_spectral", "正文 Cartesian spectral 分派", chapter, ["PsatdAlgorithmPml", "PsatdAlgorithmGalilean", "PsatdAlgorithmJRhom"]),
        ("chapter_rz", "正文 RZ spectral 结构", chapter, ["PsatdAlgorithmRZ", "Hankel", "Ep/Em"]),
        ("chapter_regression", "正文 regression 证据边界", chapter, ["analysis_galilean.py", "checksum", "RZ PSATD-JRhom", "Hybrid Ohm"]),
        ("source_outer_loop", "WarpXEvolve 外层入口", sources["evolve"], ["SyncCurrentAndRho", "PushPSATD", "EvolveB", "EvolveE", "OneStep_JRhom"]),
        ("source_psatd_correction", "PSATD current correction/Vay 入口", sources["push_em"], ["PSATDCurrentCorrection", "current_fp_vay", "PushPSATD"]),
        ("source_spectral_dispatch", "Cartesian spectral algorithm 分派", sources["spectral"], ["PsatdAlgorithmPml", "PsatdAlgorithmGalilean", "PsatdAlgorithmJRhomFirstOrder", "PsatdAlgorithmJRhomSecondOrder"]),
        ("source_rz_dispatch", "RZ spectral algorithm 分派", sources["spectral_rz"], ["PsatdAlgorithmPmlRZ", "PsatdAlgorithmRZ", "PsatdAlgorithmGalileanRZ"]),
        ("source_fdtd_dispatch", "FDTD Yee/curl kernel", sources["fdtd_b"] + sources["fdtd_e"], ["CartesianYeeAlgorithm", "UpwardDx", "DownwardDx"]),
        ("source_pml_split", "PML split field 与交换", sources["pml_component"] + sources["pml"], ["struct PMLComp", "Exchange(", "ForwardTransform", "BackwardTransform"]),
        ("source_pml_kernels", "PML E/B kernel", sources["pml_b"] + sources["pml_e"], ["PMLComp::", "EvolveBPMLCartesian", "EvolveEPMLCartesian"]),
    ]

    results = []
    for key, label, haystack, needles in checks:
        missing = [needle for needle in needles if needle not in haystack]
        results.append({"id": key, "label": label, "status": "PASS" if not missing else "FAIL", "missing": missing})

    payload = {
        "contract": "Chapter 6 field solver source crosswalk",
        "classification": "CHAPTER_6_FIELDSOLVER_SOURCE_ANCHORS_VERIFIED",
        "scope": "Representative chapter/source anchors; this is not semantic equivalence or runtime physics proof.",
        "chapter": "manuscript/chapters/06-field-solvers.md",
        "warpx_source_root": "../warpx/Source",
        "check_count": len(results),
        "pass_count": sum(item["status"] == "PASS" for item in results),
        "results": results,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 6 FieldSolver Source Crosswalk",
        "",
        "- classification: `CHAPTER_6_FIELDSOLVER_SOURCE_ANCHORS_VERIFIED`",
        f"- checks: `{payload['pass_count']}/{payload['check_count']}` PASS",
        "- scope: representative source anchors only; this does not prove semantic equivalence or runtime physics.",
        "",
        "| Check | Status | Missing |",
        "| --- | --- | --- |",
    ]
    for item in results:
        missing = ", ".join(f"`{x}`" for x in item["missing"]) or "-"
        lines.append(f"| {item['label']} | `{item['status']}` | {missing} |")
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {payload['pass_count']}/{payload['check_count']} Chapter 6 field solver source checks")
    return 0 if payload["pass_count"] == payload["check_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
