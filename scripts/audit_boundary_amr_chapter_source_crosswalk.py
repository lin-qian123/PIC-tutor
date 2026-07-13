#!/usr/bin/env python
"""Audit representative Chapter 7 boundary/AMR claims against current WarpX sources."""

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
    chapter = read(project / "manuscript/chapters/07-boundaries-amr.md")
    sources = {
        "warpx": read(warpx / "Source/WarpX.cpp"),
        "init": read(warpx / "Source/Initialization/WarpXInitData.cpp"),
        "field_boundary": read(warpx / "Source/BoundaryConditions/WarpXFieldBoundaries.cpp"),
        "field_parse": read(warpx / "Source/BoundaryConditions/FieldBoundaries.cpp"),
        "particle_parse": read(warpx / "Source/Particles/ParticleBoundaries.cpp"),
        "pml_evolve": read(warpx / "Source/BoundaryConditions/WarpXEvolvePML.cpp"),
        "pml": read(warpx / "Source/BoundaryConditions/PML.cpp"),
        "comm": read(warpx / "Source/Parallelization/WarpXComm.cpp"),
        "guard": read(warpx / "Source/Parallelization/GuardCellManager.cpp"),
        "regrid": read(warpx / "Source/Parallelization/WarpXRegrid.cpp"),
        "window": read(warpx / "Source/Utils/WarpXMovingWindow.cpp"),
        "scrape": read(warpx / "Source/Diagnostics/BoundaryScrapingDiagnostics.cpp"),
        "particle_kernel": read(warpx / "Source/Particles/ParticleBoundaries_K.H"),
    }

    checks = [
        ("chapter_boundary_order", "正文 field/particle 参数先后与 periodic 继承", chapter, ["parse_field_boundaries()", "parse_particle_boundaries()", "periodic", "field boundary"]),
        ("chapter_field_dispatch", "正文 PEC/PMC/Silver-Mueller/PECInsulator 分派", chapter, ["ApplyEfieldBoundary", "ApplyBfieldBoundary", "PECInsulator", "Silver-Mueller"]),
        ("chapter_pml", "正文 PML split-field 与电流路径", chapter, ["split fields", "DampPML()", "PML::Exchange()", "pml_has_particles"]),
        ("chapter_comm_guard", "正文通信与 guard-cell 预算", chapter, ["FillBoundary", "GuardCellManager", "guard cell", "ng_FieldSolver"]),
        ("chapter_amr", "正文 AMR 重建与 coarse-fine 交界", chapter, ["RemakeLevel", "coarse-fine", "SyncCurrent", "SyncRho"]),
        ("chapter_window_scrape", "正文 moving window 与 scraping diagnostics", chapter, ["MoveWindow", "BoundaryScrapingDiagnostics", "boundary buffer"]),
        ("chapter_transition_boundary", "正文 transition-zone 未完成边界", chapter, ["TransitionZoneRoutes", "RUNTIME_LEDGER_UNPROVEN", "专门 route proof 待实现"]),
        ("source_boundary_order", "WarpX 构造期边界解析", sources["warpx"], ["parse_field_boundaries", "get_periodicity_array", "parse_particle_boundaries"]),
        ("source_field_dispatch", "场边界运行时分派", sources["field_boundary"], ["ApplyEfieldBoundary", "ApplyBfieldBoundary", "PECInsulator", "ApplySilverMuellerBoundary"]),
        ("source_pml_lifecycle", "PML 初始化、阻尼与交换", sources["init"] + sources["pml_evolve"] + sources["pml"], ["InitPML", "CheckGuardCells", "DampPML", "Exchange("]),
        ("source_comm_guard", "场通信与 guard-cell 检查", sources["comm"] + sources["guard"], ["FillBoundaryE", "FillBoundaryB", "requested more guard cells than allocated", "ng_FieldSolver"]),
        ("source_amr_window", "AMR 重建与 moving window", sources["regrid"] + sources["window"], ["RemakeLevel", "MoveWindow", "shiftMF", "UpdateInjectionPosition"]),
        ("source_scrape_particle", "粒子边界与 scraping consumer", sources["scrape"] + sources["particle_kernel"], ["BoundaryScrapingDiagnostics::", "DoComputeAndPack", "Flush", "apply_boundary"]),
    ]

    results = []
    for key, label, haystack, needles in checks:
        missing = [needle for needle in needles if needle not in haystack]
        results.append({"id": key, "label": label, "status": "PASS" if not missing else "FAIL", "missing": missing})

    payload = {
        "contract": "Chapter 7 boundary AMR source crosswalk",
        "classification": "CHAPTER_7_BOUNDARY_AMR_SOURCE_ANCHORS_VERIFIED",
        "scope": "Representative chapter/source anchors; transition-zone runtime route ledger remains explicitly unproven.",
        "chapter": "manuscript/chapters/07-boundaries-amr.md",
        "warpx_source_root": "../warpx/Source",
        "check_count": len(results),
        "pass_count": sum(item["status"] == "PASS" for item in results),
        "results": results,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 7 Boundary/AMR Source Crosswalk",
        "",
        "- classification: `CHAPTER_7_BOUNDARY_AMR_SOURCE_ANCHORS_VERIFIED`",
        f"- checks: `{payload['pass_count']}/{payload['check_count']}` PASS",
        "- scope: representative source anchors only; transition-zone runtime route ledger remains unproven.",
        "",
        "| Check | Status | Missing |",
        "| --- | --- | --- |",
    ]
    for item in results:
        missing = ", ".join(f"`{x}`" for x in item["missing"]) or "-"
        lines.append(f"| {item['label']} | `{item['status']}` | {missing} |")
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {payload['pass_count']}/{payload['check_count']} Chapter 7 boundary/AMR source checks")
    return 0 if payload["pass_count"] == payload["check_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
