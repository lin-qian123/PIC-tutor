#!/usr/bin/env python
"""Audit representative Chapter 8 diagnostics claims against current WarpX sources."""

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
    chapter = read(project / "manuscript/chapters/08-diagnostics-cases.md")
    sources = {
        "evolve": read(warpx / "Source/Evolve/WarpXEvolve.cpp"),
        "multi": read(warpx / "Source/Diagnostics/MultiDiagnostics.cpp"),
        "full": read(warpx / "Source/Diagnostics/FullDiagnostics.cpp"),
        "full_h": read(warpx / "Source/Diagnostics/FullDiagnostics.H"),
        "openpmd": read(warpx / "Source/Diagnostics/WarpXOpenPMD.H"),
        "reduced_multi": read(warpx / "Source/Diagnostics/ReducedDiags/MultiReducedDiags.cpp"),
        "reduced_base": read(warpx / "Source/Diagnostics/ReducedDiags/ReducedDiags.cpp"),
        "scrape": read(warpx / "Source/Diagnostics/BoundaryScrapingDiagnostics.cpp"),
        "diag_h": read(warpx / "Source/Diagnostics/Diagnostics.H"),
        "analysis_langmuir": read(warpx / "Examples/Tests/langmuir/analysis_1d.py"),
        "analysis_diff_lumi": read(warpx / "Examples/Tests/diff_lumi_diag/analysis.py"),
    }

    checks = [
        ("chapter_taxonomy", "正文 diagnostics 分类", chapter, ["plotfile", "openPMD", "checkpoint", "BoundaryScraping", "physics gate", "writer/schema contract"]),
        ("chapter_evidence_chain", "正文问题到证据的验证链", chapter, ["物理问题", "producer", "consumer", "比较对象", "不能支持的结论"]),
        ("chapter_reduced", "正文 reduced diagnostics 族", chapter, ["FieldProbe", "ParticleHistogram2D", "LoadBalanceCosts", "ColliderRelevant", "DifferentialLuminosity"]),
        ("chapter_source_map", "正文 diagnostics 源码位置", chapter, ["ComputeDiagFunctors/", "ParticleIO", "WarpXOpenPMD", "FlushFormats/"]),
        ("chapter_boundary", "正文 BoundaryScraping/Python 边界", chapter, ["BoundaryScrapingDiagnostics", "Python scraped-particle buffer", "callback", "openPMD"]),
        ("source_evolve", "主循环 diagnostics consumer", sources["evolve"], ["FilterComputePackFlush", "FilterComputePackFlushLastTimestep", "reduced_diags->WriteToFile"]),
        ("source_multi", "Full/BTD/scraping 类型分派", sources["multi"] + sources["diag_h"], ["BoundaryScraping", "FilterComputePackFlush", "DiagTypes::Full", "DiagTypes::BackTransformed"]),
        ("source_full", "Full diagnostics functor 与 flush", sources["full"] + sources["full_h"], ["ComputeDiagFunctors", "FullDiagnostics::Flush", "WriteToFile"]),
        ("source_openpmd", "OpenPMD writer lifecycle", sources["openpmd"], ["WriteOpenPMDParticles", "WriteOpenPMDFieldsAll", "CloseStep", "seriesFlush"]),
        ("source_reduced_dispatch", "reduced diagnostics 类型注册", sources["reduced_multi"], ["FieldProbe", "ParticleHistogram2D", "ColliderRelevant", "DifferentialLuminosity", "LoadBalanceCosts"]),
        ("source_reduced_write", "reduced diagnostics 写盘入口", sources["reduced_multi"] + sources["reduced_base"], ["MultiReducedDiags::WriteToFile", "ReducedDiags::WriteToFile"]),
        ("source_scrape", "BoundaryScraping buffer consumer", sources["scrape"], ["BoundaryScrapingDiagnostics::", "DoComputeAndPack", "Flush", "WriteToFile"]),
        ("source_analysis_consumers", "官方 analysis consumer 代表", sources["analysis_langmuir"] + sources["analysis_diff_lumi"], ["OpenPMDTimeSeries", "assert", "DifferentialLuminosity2d"]),
    ]

    results = []
    for key, label, haystack, needles in checks:
        missing = [needle for needle in needles if needle not in haystack]
        results.append({"id": key, "label": label, "status": "PASS" if not missing else "FAIL", "missing": missing})

    payload = {
        "contract": "Chapter 8 diagnostics source crosswalk",
        "classification": "CHAPTER_8_DIAGNOSTICS_SOURCE_ANCHORS_VERIFIED",
        "scope": "Representative producer/consumer/source anchors; this is not a runtime physics proof or complete diagnostics inventory.",
        "chapter": "manuscript/chapters/08-diagnostics-cases.md",
        "warpx_source_root": "../warpx/Source",
        "check_count": len(results),
        "pass_count": sum(item["status"] == "PASS" for item in results),
        "results": results,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 8 Diagnostics Source Crosswalk",
        "",
        "- classification: `CHAPTER_8_DIAGNOSTICS_SOURCE_ANCHORS_VERIFIED`",
        f"- checks: `{payload['pass_count']}/{payload['check_count']}` PASS",
        "- scope: representative producer/consumer/source anchors only; not a runtime physics proof or complete inventory.",
        "",
        "| Check | Status | Missing |",
        "| --- | --- | --- |",
    ]
    for item in results:
        missing = ", ".join(f"`{x}`" for x in item["missing"]) or "-"
        lines.append(f"| {item['label']} | `{item['status']}` | {missing} |")
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {payload['pass_count']}/{payload['check_count']} Chapter 8 diagnostics source checks")
    return 0 if payload["pass_count"] == payload["check_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
