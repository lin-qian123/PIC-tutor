#!/usr/bin/env python
"""Audit Chapter 1's thermal-plasma Debye-resolution calculation card."""

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
    input_1d = (
        warpx / "Examples/Tests/energy_conserving_thermal_plasma/inputs_test_1d_energy_conserving_thermal_plasma"
    ).read_text(encoding="utf-8")
    input_2d = (
        warpx / "Examples/Tests/energy_conserving_thermal_plasma/inputs_test_2d_energy_conserving_thermal_plasma"
    ).read_text(encoding="utf-8")
    analysis = (
        warpx / "Examples/Tests/energy_conserving_thermal_plasma/analysis.py"
    ).read_text(encoding="utf-8")

    checks = {
        "reader_card_present": missing(
            chapter,
            [
                "### 1.10.1 尺度计算卡：能量回归通过不等于 Debye 屏蔽已分辨",
                "测试名和物理判据必须分开读",
                r"\frac{\lambda_{De}}{\Delta x}\approx1.119\times10^{-2}",
                r"\omega_{pe}\Delta t=0.2",
                "能量回归通过不等于 Debye 屏蔽已分辨",
                "建立新的分辨率合同",
                "并不运行 WarpX，也不宣布某个通用的",
            ],
        ),
        "official_1d_input_scales": missing(
            input_1d,
            [
                "amr.n_cell =  8",
                "my_constants.Te = 100.",
                "my_constants.wpe = q_e*sqrt(n0/(m_e*epsilon0))",
                "my_constants.de0 = clight/wpe",
                "my_constants.dt = ( 0.2 )/wpe",
                "geometry.prob_hi = 10.*de0",
                "electrons.ux_th = sqrt(Te*q_e/m_e)/clight",
                "EP.type = ParticleEnergy",
                "EF.type = FieldEnergy",
            ],
        ),
        "official_2d_input_scales": missing(
            input_2d,
            [
                "amr.n_cell =  8 8",
                "my_constants.Te = 100.",
                "geometry.prob_hi = 10.*de0 10.*de0",
                "electrons.num_particles_per_cell_each_dim = 2 2",
            ],
        ),
        "energy_consumer_does_not_measure_resolution": missing(
            analysis,
            [
                "field_energy = EFdata[:, 2]",
                "particle_energy = EPdata[:, 2]",
                "assert np.all(abs(E - E[0]) / E[0] < 0.003)",
            ],
        ),
    }
    passed = all(not absent for absent in checks.values())
    payload = {
        "classification": "SOURCE_GROUNDED_THERMAL_PLASMA_DEBYE_RESOLUTION_READER_CARD",
        "passed": passed,
        "checks": checks,
        "derived_scales": {
            "lambda_De_over_de0": 0.0139891071,
            "dx_over_de0": 1.25,
            "lambda_De_over_dx": 0.0111912857,
            "omega_pe_dt": 0.2,
            "v_te_dt_over_dx": 0.00223825714,
        },
        "source_routes": [
            "Examples/Tests/energy_conserving_thermal_plasma/{inputs_test_1d_energy_conserving_thermal_plasma,inputs_test_2d_energy_conserving_thermal_plasma,analysis.py}",
            "Chapter 1 Debye definitions and thermal-plasma energy-validation card",
        ],
        "scope": [
            "No WarpX build or runtime execution is performed by this audit.",
            "The derived scales use the input's electron thermal-speed convention, d_e0=c/omega_pe, L=10 d_e0, and N_x=8.",
            "The card does not impose a universal Debye-resolution threshold or establish Landau damping, shielding, a fluctuation spectrum, or convergence for this producer.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Chapter 1 Thermal-Plasma Debye-Resolution Card",
        "",
        "Classification: `SOURCE_GROUNDED_THERMAL_PLASMA_DEBYE_RESOLUTION_READER_CARD`.",
        "",
        f"Result: `{'PASS' if passed else 'FAIL'}`.",
        "",
        "## Derived Scales",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in payload["derived_scales"].items())
    lines.extend(["", "## Source Routes", ""])
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
