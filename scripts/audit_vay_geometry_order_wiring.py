#!/usr/bin/env python
"""Audit official Vay deposition geometry/order wiring without editing WarpX."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    root = args.warpx_root.resolve()

    vay_dir = root / "Examples/Tests/vay_deposition"
    langmuir_dir = root / "Examples/Tests/langmuir"
    source = read(root / "Source/Particles/WarpXParticleContainer.cpp")
    kernel = read(root / "Source/Particles/Deposition/CurrentDeposition.H")
    vay_cmake = read(vay_dir / "CMakeLists.txt")
    vay_2d = read(vay_dir / "inputs_test_2d_vay_deposition")
    vay_3d = read(vay_dir / "inputs_test_3d_vay_deposition")
    vay_analysis = read(vay_dir / "analysis.py")
    shape4_cmake = read(langmuir_dir / "CMakeLists.txt")
    shape4_input = read(langmuir_dir / "inputs_test_2d_langmuir_multi_psatd_vay_deposition_particle_shape_4")

    checks = {
        "official_vay_2d_test": "test_2d_vay_deposition" in vay_cmake and "inputs_test_2d_vay_deposition" in vay_cmake,
        "official_vay_3d_test": "test_3d_vay_deposition" in vay_cmake and "inputs_test_3d_vay_deposition" in vay_cmake,
        "vay_2d_shape3": "algo.particle_shape = 3" in vay_2d,
        "vay_3d_shape3": "algo.particle_shape = 3" in vay_3d,
        "vay_2d_cartesian": "geometry.dims = 2" in vay_2d and "geometry.coord_sys = 0" in vay_2d,
        "vay_3d_cartesian": "geometry.dims = 3" in vay_3d and "geometry.coord_sys = 0" in vay_3d,
        "vay_2d_psatd_collocated": "algo.maxwell_solver = psatd" in vay_2d and "warpx.grid_type = collocated" in vay_2d,
        "vay_3d_psatd_collocated": "algo.maxwell_solver = psatd" in vay_3d and "warpx.grid_type = collocated" in vay_3d,
        "vay_2d_analysis_surface": "analysis.py diags/diag1000050" in vay_cmake,
        "vay_3d_analysis_surface": "analysis.py diags/diag1000025" in vay_cmake,
        "analysis_charge_gate": "divE - rho / epsilon_0" in vay_analysis and "tolerance = 1e-3" in vay_analysis,
        "shape4_test_registered": "test_2d_langmuir_multi_psatd_vay_deposition_particle_shape_4" in shape4_cmake,
        "shape4_input_vay": "algo.current_deposition = vay" in shape4_input,
        "shape4_input_order": "algo.particle_shape = 4" in shape4_input,
        "source_vay_shape1_to4": all(f"doVayDepositionShapeN<{order}>" in source for order in range(1, 5)),
        "source_vay_rz_guard": "Vay deposition not implemented in RZ geometry" in kernel,
        "source_vay_1d_guard": "Vay deposition not implemented in 1D geometry" in kernel,
        "source_vay_implicit_guard": "The Vay algorithm cannot be used with implicit algorithm." in source,
    }
    result = {
        "contract": "Vay deposition geometry/order official wiring",
        "classification": "SOURCE_REGRESSION_WIRING_PARTIAL_RUNTIME_FAMILY",
        "scope": "official 2D/3D shape-3 cases, 2D shape-4 sibling, analysis consumers and source guards; not full Cartesian-product runtime proof",
        "checks": checks,
        "passed": all(checks.values()),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Vay deposition geometry/order official wiring",
        "",
        f"- classification: `{result['classification']}`",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- scope: {result['scope']}",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += [
        "",
        "The contract confirms official input/CMake/source wiring. It does not claim that every Vay geometry/order combination has an independent runtime consumer or that the full Cartesian product is covered.",
    ]
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: {sum(checks.values())}/{len(checks)} Vay geometry/order wiring checks")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
