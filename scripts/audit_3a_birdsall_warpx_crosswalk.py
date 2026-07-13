#!/usr/bin/env python
"""Audit the Chapter 3A Birdsall ES1 to WarpX source crosswalk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check(text: str, *needles: str) -> dict[str, object]:
    missing = [needle for needle in needles if needle not in text]
    return {"needles": list(needles), "missing": missing, "passed": not missing}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    chapter = (args.project_root / "manuscript/chapters/03a-warpx-initialization.md").read_text(encoding="utf-8")
    init = (args.warpx_root / "Source/Initialization/WarpXInitData.cpp").read_text(encoding="utf-8")
    main_source = (args.warpx_root / "Source/main.cpp").read_text(encoding="utf-8")
    evolve = (args.warpx_root / "Source/Evolve/WarpXEvolve.cpp").read_text(encoding="utf-8")
    particles = (args.warpx_root / "Source/Particles/PhysicalParticleContainer.cpp").read_text(encoding="utf-8")
    references = args.project_root / "references/02_books_lecture_notes/1985_BirdsallLangdon_Plasma_physics_via_computer_simulation"
    reference_files = {path.name for path in references.iterdir() if path.is_file()}

    checks = {
        "chapter_stage_chain": check(chapter, "INIT -> SETRHO -> FIELDS -> SETV -> ACCEL -> MOVE -> HISTRY"),
        "chapter_mapping_table": check(chapter, "`SETRHO`", "`FIELDS`", "`SETV`", "`ACCEL`", "`MOVE`", "`HISTRY`"),
        "chapter_boundary_language": check(chapter, "不能把旧程序的子程序名直接当成 WarpX 的函数名", "不是对 `3A ES1` 原程序做逐行复现"),
        "chapter_modern_sources": check(chapter, "WarpXInitData.cpp", "PhysicalParticleContainer", "WarpXEvolve.cpp", "InitFromScratch or InitFromCheckpoint"),
        "chapter_verification_layers": check(chapter, "Langmuir", "initial_distribution", "space_charge_initialization", "projection_div_cleaner"),
        "reference_asset": {"needles": ["Birdsall PDF", "Birdsall Chinese note"], "missing": [] if any("Birdsall" in name for name in reference_files) else ["Birdsall asset files"], "passed": any("Birdsall" in name for name in reference_files)},
        "main_lifecycle": check(main_source, "InitData()", "Evolve()"),
        "init_fresh_restart": check(init, "InitFromScratch", "InitFromCheckpoint", "m_electrostatic_solver->InitData"),
        "init_particle_lifecycle": check(init, "mypc->AllocData", "mypc->InitData"),
        "evolve_dispatch": check(evolve, "OneStep", "PushParticlesandDeposit", "SyncCurrentAndRho"),
        "particle_evolve_surface": check(particles, "PhysicalParticleContainer::InitData", "PhysicalParticleContainer::Evolve"),
    }
    result = {
        "contract": "Chapter 3A Birdsall ES1 to WarpX source crosswalk",
        "classification": "CHAPTER_3A_HISTORICAL_MODERN_MAPPING_SOURCE_ANCHORS_VERIFIED",
        "scope": "Verifies representative historical-stage, modern lifecycle, and validation-layer anchors; not a function-by-function equivalence proof or a new runtime physics regression.",
        "checks": checks,
        "reference_directory": str(references),
    }
    result["passed"] = all(item["passed"] for item in checks.values())
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Chapter 3A Birdsall ES1 to WarpX source crosswalk", "", f"- status: `{'PASS' if result['passed'] else 'FAIL'}`", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}", ""]
    for name, item in checks.items():
        lines.append(f"- `{name}`: `{'PASS' if item['passed'] else 'FAIL'}`")
        if item["missing"]:
            lines.append(f"  - missing: `{', '.join(item['missing'])}`")
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {len(checks)} Chapter 3A crosswalk groups")
    if not result["passed"]:
        raise SystemExit("Chapter 3A Birdsall/WarpX crosswalk failed")


if __name__ == "__main__":
    main()
