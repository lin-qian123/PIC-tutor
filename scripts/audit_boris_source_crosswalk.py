#!/usr/bin/env python
"""Audit the current WarpX Boris kernel and selector/source crosswalk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def contains(text: str, *terms: str) -> bool:
    return all(term in text for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.warpx_root.resolve()
    kernel_path = root / "Source/Particles/Pusher/UpdateMomentumBoris.H"
    selector_path = root / "Source/Particles/Pusher/PushSelector.H"
    kernel = kernel_path.read_text(encoding="utf-8") if kernel_path.is_file() else ""
    selector = selector_path.read_text(encoding="utf-8") if selector_path.is_file() else ""
    chapter = args.chapter.resolve().read_text(encoding="utf-8")

    checks = {
        "kernel_present": kernel_path.is_file(),
        "kernel_function_and_modes": contains(kernel, "void UpdateMomentumBoris", "MomentumPushType::FirstHalf", "MomentumPushType::SecondHalf", "MomentumPushType::Full"),
        "electric_half_pushes": contains(kernel, "// First half-push for E", "// Second half-push for E", "ux += econst*Ex"),
        "relativistic_gamma_and_rotation": contains(kernel, "inv_gamma", "// Magnetic rotation", "const amrex::ParticleReal ux_p", "const amrex::ParticleReal uy_p", "const amrex::ParticleReal uz_p"),
        "half_angle_rescaling": contains(kernel, "tan(alpha/2)", "tan(alpha/4)", "const amrex::ParticleReal factor"),
        "rotation_coefficients": contains(kernel, "tsqi", "const amrex::ParticleReal sx", "const amrex::ParticleReal sy", "const amrex::ParticleReal sz"),
        "selector_boris_dispatch": contains(selector, "pusher_algo == ParticlePusherAlgo::Boris", "UpdateMomentumBoris(", "momentum_push_type"),
        "selector_rr_boundary": contains(selector, "UpdateMomentumBorisWithRadiationReaction", "if (do_crr)", "else if (pusher_algo == ParticlePusherAlgo::Boris)"),
        "chapter_crosswalk_recorded": contains(chapter, "Boris 1970", "UpdateMomentumBoris.H", "三层证据"),
    }
    result = {
        "contract": "WarpX Boris kernel/source crosswalk",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "CURRENT_WARPX_SOURCE_GROUNDED_BORIS_CROSSWALK_HISTORICAL_PROCEEDINGS_FULL_TEXT_MISSING",
        "scope": "read-only current WarpX source mapping; not a line-by-line reconstruction of the 1970 proceedings paper",
        "source_files": [
            "Source/Particles/Pusher/UpdateMomentumBoris.H",
            "Source/Particles/Pusher/PushSelector.H",
        ],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Boris source crosswalk contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", "The source crosswalk is read-only and keeps current implementation evidence separate from the unavailable historical proceedings full text."]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
