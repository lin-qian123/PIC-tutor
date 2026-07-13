#!/usr/bin/env python
"""Audit WarpX's explicit momentum-to-position leapfrog source crosswalk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def contains(text: str, *terms: str) -> bool:
    return all(term in text for term in terms)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.warpx_root.resolve()
    position_path = root / "Source/Particles/Pusher/UpdatePosition.H"
    container_path = root / "Source/Particles/PhysicalParticleContainer.cpp"
    selector_path = root / "Source/Particles/Pusher/PushSelector.H"
    particle_container_header_path = root / "Source/Particles/WarpXParticleContainer.H"
    algorithm_selection_path = root / "Source/Utils/WarpXAlgorithmSelection.H"
    higuera_path = root / "Source/Particles/Pusher/UpdateMomentumHigueraCary.H"
    position = read(position_path)
    container = read(container_path)
    selector = read(selector_path)
    particle_container_header = read(particle_container_header_path)
    algorithm_selection = read(algorithm_selection_path)
    higuera = read(higuera_path)
    chapter = args.chapter.resolve().read_text(encoding="utf-8")

    checks = {
        "position_source_present": position_path.is_file(),
        "time_centered_position_contract": contains(
            position,
            "using the standard leapfrog algorithm",
            "v(t+dt/2)*dt",
            "const amrex::ParticleReal ux",
        ),
        "massive_particle_gamma_inverse": contains(
            position,
            "amrex::ParticleReal const u2",
            "const amrex::ParticleReal inv_gamma",
            "u2*inv_c2",
            "x += ux * inv_gamma * dt",
        ),
        "dimension_gated_position_updates": contains(
            position,
            "#if !defined(WARPX_DIM_1D_Z)",
            "#if defined(WARPX_DIM_3D)",
            "#if !defined(WARPX_DIM_RCYLINDER)",
        ),
        "momentum_then_position_order": contains(
            container,
            "doParticleMomentumPush<0>(ux[ip]",
            "if (position_push_type == PositionPushType::Full)",
            "UpdatePosition(xp, yp, zp, ux[ip], uy[ip], uz[ip], dt, mass)",
        ),
        "selector_split_contract": contains(
            selector + particle_container_header + algorithm_selection,
            "FirstHalf,",
            "SecondHalf,",
            "MomentumPushType::Full",
        ),
        "higuera_no_split_argument": contains(
            higuera,
            "void UpdateMomentumHigueraCary",
            "const amrex::Real dt",
        ) and "momentum_push_type" not in higuera.split("UpdateMomentumHigueraCary(", 1)[-1].split(")", 1)[0],
        "chapter_crosswalk_recorded": contains(
            chapter,
            "UpdatePosition.H",
            "时间中心",
            "半步速度",
            "直接半步速度属性",
        ),
    }
    result = {
        "contract": "WarpX explicit leapfrog position/source crosswalk",
        "checks": checks,
        "passed": all(checks.values()),
        "classification": "CURRENT_WARPX_SOURCE_GROUNDED_TIME_CENTERED_POSITION_DIRECT_HALF_STEP_ATTRIBUTE_NOT_EXPORTED",
        "scope": "read-only source mapping; adjacent Full plotfiles provide a velocity proxy but do not prove a direct half-step diagnostic attribute",
        "source_files": [
            "Source/Particles/Pusher/UpdatePosition.H",
            "Source/Particles/PhysicalParticleContainer.cpp",
            "Source/Particles/Pusher/PushSelector.H",
        ],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "contract.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Explicit leapfrog position source crosswalk contract",
        "",
        f"- classification: `{result['classification']}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The source establishes that the explicit position update consumes the time-centered momentum after the momentum push. It does not establish a public direct half-step velocity attribute.",
    ]
    (args.output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
