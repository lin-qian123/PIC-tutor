#!/usr/bin/env python
"""Audit Chapter 4's reader-facing pusher validation ladder."""

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
    chapter = (ROOT / "manuscript/chapters/04-particle-pushers.md").read_text(encoding="utf-8")
    pusher_dir = warpx / "Examples/Tests/particle_pusher"
    single_dir = warpx / "Examples/Tests/single_particle"
    photon_dir = warpx / "Examples/Tests/photon_pusher"
    larmor_dir = warpx / "Examples/Tests/larmor"
    pusher_input = (pusher_dir / "inputs_test_3d_particle_pusher").read_text(encoding="utf-8")
    pusher_cmake = (pusher_dir / "CMakeLists.txt").read_text(encoding="utf-8")
    pusher_analysis = (pusher_dir / "analysis.py").read_text(encoding="utf-8")
    sync_input = (single_dir / "inputs_test_1d_synchronize_velocity").read_text(encoding="utf-8")
    sync_cmake = (single_dir / "CMakeLists.txt").read_text(encoding="utf-8")
    sync_analysis = (single_dir / "analysis_synchronize_velocity.py").read_text(encoding="utf-8")
    photon_input = (photon_dir / "inputs_test_3d_photon_pusher").read_text(encoding="utf-8")
    photon_cmake = (photon_dir / "CMakeLists.txt").read_text(encoding="utf-8")
    photon_analysis = (photon_dir / "analysis.py").read_text(encoding="utf-8")
    larmor_cmake = (larmor_dir / "CMakeLists.txt").read_text(encoding="utf-8")
    selector = (warpx / "Source/Particles/Pusher/PushSelector.H").read_text(encoding="utf-8")
    photon_source = (warpx / "Source/Particles/PhotonParticleContainer.cpp").read_text(encoding="utf-8")
    position_source = (warpx / "Source/Particles/Pusher/UpdatePosition.H").read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing_markers(
            chapter,
            [
                "### 4.13.8.1 推进器修改后的验证阶梯：先选对 consumer，再解释结果",
                "第一层：带质量粒子的 momentum--position 链。",
                "第二层：输出时间层，而不是轨道算法。",
                "第三层：无质量粒子是另一条容器链。",
                "第四层：checksum 仍有价值，但不是解析 gate。",
                "单粒子通过不能完成验证",
            ],
        ),
        "massive_pusher_contract": missing_markers(
            pusher_input,
            [
                "max_step = 10000",
                'algo.particle_pusher = "higuera"',
                'positron.injection_style = "SingleParticle"',
                'particles.B_ext_particle_init_style = "constant"',
                "diag1.intervals = 10000",
            ],
        )
        + missing_markers(
            pusher_cmake,
            ["test_3d_particle_pusher", '"analysis.py diags/diag1010000"'],
        )
        + missing_markers(
            pusher_analysis,
            ["using a force-free field", "tolerance = 0.001", 'ad["particle_position_x"]', "assert abs(x) < tolerance"],
        ),
        "diagnostic_time_contract": missing_markers(
            sync_input,
            [
                "warpx.synchronize_velocity_for_diagnostics = 1",
                "diag1.intervals = 5",
                "particles.E_ext_particle_init_style = constant",
            ],
        )
        + missing_markers(
            sync_cmake,
            ["test_1d_synchronize_velocity", '"analysis_synchronize_velocity.py diags/diag1000005"'],
        )
        + missing_markers(
            sync_analysis,
            ["Half backward advance of velocity", "for _ in range(5):", "tolerance_rel = 1.0e-15", "assert error_rel < tolerance_rel"],
        ),
        "photon_contract": missing_markers(
            photon_input,
            [
                "max_step = 50",
                "p_xp_1.species_type = photon",
                "p_dp_10.single_particle_u = 10.0 10.0 10.0",
                "diag1.intervals = 50",
            ],
        )
        + missing_markers(
            photon_cmake,
            ["test_3d_photon_pusher", "2  # nprocs", '"analysis.py diags/diag1000050"'],
        )
        + missing_markers(
            photon_analysis,
            ["tol_pos = 1.0e-14", "tol_mom = np.finfo(np.float64).eps", "assert (max(disc_pos) <= tol_pos) and (max(disc_mom) <= tol_mom)"],
        ),
        "source_and_checksum_boundaries": missing_markers(
            selector,
            ["ParticlePusherAlgo::HigueraCary", "UpdateMomentumHigueraCary"],
        )
        + missing_markers(
            photon_source,
            ["PhotonParticleContainer::PushPX", "UpdatePosition(x, y, z, ux[i], uy[i], uz[i], dt, mass)", "photons carry no charge"],
        )
        + missing_markers(
            position_source,
            ["GetExplicitPusherDisplacement", "using the standard leapfrog algorithm"],
        )
        + missing_markers(
            larmor_cmake,
            ["test_2d_larmor", "OFF  # analysis", '"analysis_default_regression.py --path diags/diag1000010"'],
        ),
    }
    passed = all(not missing for missing in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_PUSHER_VALIDATION_LADDER_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Source/Particles/Pusher/PushSelector.H",
            "Source/Particles/Pusher/UpdatePosition.H",
            "Source/Particles/PhotonParticleContainer.cpp",
            "Examples/Tests/particle_pusher/{inputs_test_3d_particle_pusher,CMakeLists.txt,analysis.py}",
            "Examples/Tests/single_particle/{inputs_test_1d_synchronize_velocity,CMakeLists.txt,analysis_synchronize_velocity.py}",
            "Examples/Tests/photon_pusher/{inputs_test_3d_photon_pusher,CMakeLists.txt,analysis.py}",
            "Examples/Tests/larmor/CMakeLists.txt",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The card separates massive-pusher, diagnostic-time-level, massless-photon, and checksum-only evidence.",
            "It does not establish a general pusher accuracy ranking, deposition correctness, or self-consistent field validity.",
        ],
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 4 Pusher Validation Ladder",
        "",
        "Classification: `SOURCE_GROUNDED_PUSHER_VALIDATION_LADDER_READER_CARD`.",
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
