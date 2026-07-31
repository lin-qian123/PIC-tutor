#!/usr/bin/env python
"""Audit Chapter 1's thermal-plasma energy and noise validation card."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def missing(text: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    warpx = args.warpx_root.resolve()
    chapter = (ROOT / "manuscript/chapters/01-kinetic-models.md").read_text(encoding="utf-8")
    parameters = (warpx / "Docs/source/usage/parameters.rst").read_text(encoding="utf-8")
    theory = (warpx / "Docs/source/theory/models_algorithms/explicit_em_pic.rst").read_text(
        encoding="utf-8"
    )
    amr_theory = (warpx / "Docs/source/theory/amr.rst").read_text(encoding="utf-8")
    test_root = warpx / "Examples/Tests/energy_conserving_thermal_plasma"
    cmake = (test_root / "CMakeLists.txt").read_text(encoding="utf-8")
    input_1d = (test_root / "inputs_test_1d_energy_conserving_thermal_plasma").read_text(
        encoding="utf-8"
    )
    input_2d = (test_root / "inputs_test_2d_energy_conserving_thermal_plasma").read_text(
        encoding="utf-8"
    )
    analysis = (test_root / "analysis.py").read_text(encoding="utf-8")
    particle_energy = (warpx / "Source/Diagnostics/ReducedDiags/ParticleEnergy.H").read_text(
        encoding="utf-8"
    )
    field_energy = (warpx / "Source/Diagnostics/ReducedDiags/FieldEnergy.H").read_text(
        encoding="utf-8"
    )

    checks = {
        "reader_card_present": missing(
            chapter,
            [
                "### 1.9.1 统计噪声与能量账本验证卡：能量漂移小不等于热平衡或低噪声",
                "第一层：先固定它实际产生了什么",
                "第二层：再核对 consumer 到底比较了什么",
                "第三层：明确这张账本没有测量什么",
                "第四层：修改后重新建立两本账",
                "能量漂移小不等于热平衡或低噪声",
                "原来的 `0.003` 已不再是自动有效的合同",
            ],
        ),
        "official_producers": missing(
            cmake,
            [
                "test_1d_energy_conserving_thermal_plasma",
                "test_2d_energy_conserving_thermal_plasma",
                "1  # dims",
                "2  # dims",
                "2  # nprocs",
                '"analysis.py"',
                '"analysis_default_regression.py --path diags/diag1000500"',
            ],
        )
        + missing(
            input_1d,
            [
                "max_step = 500",
                "warpx.do_electrostatic = labframe",
                "algo.field_gathering = energy-conserving",
                "algo.particle_shape = 2",
                "warpx.use_filter = 0",
                "boundary.field_lo = periodic",
                "electrons.num_particles_per_cell_each_dim = 4",
                "protons.num_particles_per_cell_each_dim = 4",
                "EP.type = ParticleEnergy",
                "EF.type = FieldEnergy",
                "EP.intervals = 100",
                "EF.intervals =100",
            ],
        )
        + missing(
            input_2d,
            [
                "geometry.dims = 2",
                "boundary.field_lo = periodic periodic",
                "electrons.num_particles_per_cell_each_dim = 2 2",
                "protons.num_particles_per_cell_each_dim = 2 2",
                "electrons.momentum_distribution_type = gaussian",
                "protons.momentum_distribution_type = gaussian",
            ],
        ),
        "energy_consumer": missing(
            analysis,
            [
                'np.genfromtxt("./diags/reducedfiles/EF.txt")',
                'np.genfromtxt("./diags/reducedfiles/EP.txt")',
                "field_energy = EFdata[:, 2]",
                "particle_energy = EPdata[:, 2]",
                "E = field_energy + particle_energy",
                "assert np.all(abs(E - E[0]) / E[0] < 0.003)",
            ],
        )
        + missing(
            particle_energy,
            [
                "particle relativistic kinetic energy",
                "sqrt( p^2 c^2 + m^2 c^4 ) - m c^2",
            ],
        )
        + missing(
            field_energy,
            [
                "EF = sum( 1/2 * (|E|^2 * eps0 + |B|^2 / mu0) * dV )",
            ],
        ),
        "gather_and_mesh_boundary": missing(
            parameters,
            [
                "energy-conserving",
                "gathers directly from the grid points",
                "momentum-conserving",
            ],
        )
        + missing(
            theory,
            [
                "at the limit of infinitesimal time steps",
                "better conservation of the respective quantities for a finite",
            ],
        )
        + missing(
            amr_theory,
            [
                "there is no self-force of the particle acting on itself",
                "on average within one cell if using the \u201cenergy conserving\u201d gathering scheme",
                "results in a net spurious self-force",
            ],
        ),
    }
    passed = all(not absent for absent in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_THERMAL_PLASMA_ENERGY_AND_NOISE_READER_CARD",
        "passed": passed,
        "checks": checks,
        "source_routes": [
            "Docs/source/{usage/parameters.rst,theory/models_algorithms/explicit_em_pic.rst,theory/amr.rst}",
            "Examples/Tests/energy_conserving_thermal_plasma/{CMakeLists.txt,inputs_test_1d_energy_conserving_thermal_plasma,inputs_test_2d_energy_conserving_thermal_plasma,analysis.py}",
            "Source/Diagnostics/ReducedDiags/{ParticleEnergy.H,FieldEnergy.H}",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The card separates the fixed periodic thermal-plasma producer, the sampled total energy consumer, and independent noise or thermal observables.",
            "It does not establish thermal equilibrium, a noise spectrum, strict conservation, arbitrary gathering behavior, AMR-interface behavior, collisions, laser propagation, or a threshold for a modified producer.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 1 Thermal-Plasma Energy Validation Card",
        "",
        "Classification: `SOURCE_GROUNDED_THERMAL_PLASMA_ENERGY_AND_NOISE_READER_CARD`.",
        "",
        f"Result: `{'PASS' if passed else 'FAIL'}`.",
        "",
        "## Source Routes",
        "",
    ]
    lines.extend(f"- `{route}`" for route in payload["source_routes"])
    lines.extend(["", "## Checks", ""])
    for name, absent in checks.items():
        lines.append(f"- `{name}`: `{'PASS' if not absent else 'FAIL'}`")
        lines.extend(f"  - missing: `{marker}`" for marker in absent)
    lines.extend(["", "## Scope", ""])
    lines.extend(f"- {item}" for item in payload["scope"])
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
