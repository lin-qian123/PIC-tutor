#!/usr/bin/env python
"""Audit Chapter 9 claims against the materialized literature tree."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check(name: str, condition: bool, detail: str) -> dict[str, object]:
    return {"name": name, "status": "PASS" if condition else "FAIL", "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.project_root.resolve()
    chapter = (root / "manuscript/chapters/09-literature-roadmap.md").read_text()
    literature_map = (root / "docs/literature-map.md").read_text()
    inventory = (root / "references/00_index/current_inventory.md").read_text()

    assets = {
        "Birdsall 1985": root / "references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation",
        "Tajima-Dawson 1979": root / "references/03_pic_foundations/1979_TajimaDawson_Laser_Electron_Accelerator",
        "Dawson 1983": root / "references/03_pic_foundations/1983_Dawson_Particle_simulation_of_plasmas",
        "Vay 2008": root / "references/04_particle_pushers_deposition_shapes/2008_VayPOP2008_Simulation_of_beams_or_plasmas_crossing_at_relativistic_velocity",
        "Higuera-Cary 2017": root / "references/04_particle_pushers_deposition_shapes/2017_HigueraPOP2017_Structure-preserving_second-order_integration_of_relativistic_charged_particle_trajectories_in_electromagnetic_fields",
        "Godfrey 2014": root / "references/06_stability_filtering_nci/2014_GodfreyJCP2014_Numerical_stability_analysis_of_the_PSATD_PIC_algorithm",
        "Kirchen 2016": root / "references/06_stability_filtering_nci/2016_KirchenPOP2016_Stable_discrete_representation_of_relativistically_drifting_plasmas",
        "Lehe 2016": root / "references/06_stability_filtering_nci/2016_LehePRE2016_Elimination_of_NCI_by_Galilean_coordinates",
    }
    results: list[dict[str, object]] = []
    results.append(check("evidence tiers", all(x in chapter for x in ("A. 已 materialize 的正文资产", "B. 已取得 PDF 但未完成精读", "C. metadata / abstract 级线索", "D. 旁证或相关文献")), "Chapter 9 defines A-D evidence tiers."))
    results.append(check("tier rule", "只有 A 层资产" in chapter and "不能把摘要内容冒充成论文正文结论" in chapter, "Chapter 9 states the A-tier and metadata boundary."))
    results.append(check("core literature tree", all(path.is_dir() for path in assets.values()), "All eight core materialized literature directories exist."))
    results.append(check("core names in chapter", all(name in chapter for name in assets), "Chapter 9 names every core literature line."))
    map_anchors = ("Birdsall-Langdon", "TajimaDawson", "Dawson", "Vay", "Higuera", "GodfreyJCP2014", "Kirchen", "Lehe")
    results.append(check("core names in map", all(anchor in literature_map for anchor in map_anchors), "The global literature map contains the core author anchors."))
    results.append(check("inventory is generated", "Total PDF files:" in inventory and "Counts By Category" in inventory, "The reference inventory has generated-count markers."))
    results.append(check("Tajima related boundary", "正式 Tajima--Dawson AIP item 仍是独立的全文缺失缺口" in chapter, "The related FNAL note is explicitly not promoted to the formal AIP item."))
    results.append(check("Esirkepov gap", "仍缺出版商 CPC PDF 对照" in chapter and (root / "runs/stage-c-validation/esirkepov-paper-asset-contract/contract.json").is_file(), "Esirkepov publisher-version gap and contract are both recorded."))
    results.append(check("Lee gap", "仍缺 publisher-formatted CPC PDF" in chapter and (root / "runs/stage-c-validation/leecpc2015-accepted-manuscript-contract/contract.json").is_file(), "Lee accepted-manuscript boundary and contract are both recorded."))
    results.append(check("Yee gap", "Yee 1966" in chapter and "无本地 PDF/MinerU" in chapter, "Yee remains metadata-level, as stated."))
    results.append(check("Hockney gap", "Hockney-Eastwood" in chapter and "无本地合法 PDF" in chapter, "Hockney-Eastwood remains an acquisition gap, as stated."))
    results.append(check("chapter route", "docs/literature-map.md" in chapter and "references/00_index/books_to_locate.md" in chapter, "Chapter 9 points acquisition back to the maintained indexes."))

    passed = sum(result["status"] == "PASS" for result in results)
    payload = {"chapter": "09-literature-roadmap", "checks": results, "passed": passed, "total": len(results)}
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Chapter 9 Literature Roadmap Asset Contract", "", f"- Result: **{passed}/{len(results)} PASS**", "", "| Check | Status | Detail |", "|---|---|---|"]
    lines.extend(f"| {item['name']} | {item['status']} | {item['detail']} |" for item in results)
    args.output_md.write_text("\n".join(lines) + "\n")
    print(f"{'PASS' if passed == len(results) else 'FAIL'}: {passed}/{len(results)} Chapter 9 literature checks")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
