#!/usr/bin/env python
"""Audit the reproducible pre-physics boundary of the RZ implicit case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def marker(text: str, needle: str) -> dict[str, object]:
    count = text.count(needle)
    return {"needle": needle, "count": count, "passed": count > 0}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warpx-root", type=Path, required=True)
    parser.add_argument("--runtime-log", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    input_path = args.warpx_root / "Examples/Tests/implicit/inputs_test_rz_theta_implicit_dynamic_pinch"
    theta_path = args.warpx_root / "Source/FieldSolver/ImplicitSolvers/ThetaImplicitEM.cpp"
    implicit_path = args.warpx_root / "Source/FieldSolver/ImplicitSolvers/ImplicitSolver.cpp"
    particle_path = args.warpx_root / "Source/Particles/WarpXParticleContainer.cpp"
    chapter_path = Path(__file__).resolve().parents[1] / "manuscript/chapters/05-deposition-shapes.md"
    input_text = input_path.read_text(encoding="utf-8")
    theta_text = theta_path.read_text(encoding="utf-8")
    implicit_text = implicit_path.read_text(encoding="utf-8")
    particle_text = particle_path.read_text(encoding="utf-8")
    chapter_text = chapter_path.read_text(encoding="utf-8")
    runtime_text = args.runtime_log.read_text(encoding="utf-8")
    checks = {
        "input_rz": marker(input_text, "geometry.dims = RZ"),
        "input_theta_implicit": marker(input_text, 'algo.evolve_scheme = "theta_implicit_em"'),
        "input_villasenor": marker(input_text, 'algo.current_deposition = "villasenor"'),
        "input_petsc_ksp": marker(input_text, "newton.linear_solver = petsc_ksp"),
        "input_petsc_preconditioner": marker(input_text, "jacobian.pc_type = pc_petsc"),
        "theta_defines_solver": marker(theta_text, "m_nlsolver->Define(m_E, this);"),
        "theta_masks_are_petsc_only": marker(theta_text, "if (pc_type == PreconditionerType::pc_petsc) { InitializeCurlCurlBCMasks(); }"),
        "petsc_compile_guard": marker(implicit_text, "AMREX_USE_PETSC must be defined"),
        "implicit_rhs_precedes_particle_source": marker(theta_text, "PreRHSOp( theta_time, a_nl_iter, a_from_jacobian );"),
        "pre_rhs_pushes_and_deposits": marker(implicit_text, "m_WarpX->PushParticlesandDeposit(a_cur_time, skip_deposition, PositionPushType::Full, MomentumPushType::Full, &options);"),
        "implicit_villasenor_dispatch": marker(particle_text, "doVillasenorDepositionShapeNImplicit"),
        "runtime_reaches_dof": marker(runtime_text, "Defined DOF object for linear solves"),
        "runtime_sigill": marker(runtime_text, "SIGILL Invalid, privileged, or ill-formed instruction"),
        "runtime_mpi_abort": marker(runtime_text, "MPI_Abort"),
        "chapter_reader_card": marker(chapter_text, "### 5.14.2.2 RZ implicit Villasenor 判读卡：初始化停止不等于沉积失败"),
        "chapter_does_not_overclaim_physics": marker(chapter_text, "当前分类是 **pre-physics boundary**"),
        "chapter_requires_source_and_consumer": marker(chapter_text, "source/field 有限且时间层明确 + Gauss-law 或能量等独立 observable 通过"),
    }
    result = {
        "contract": "RZ implicit Villasenor pre-physics build boundary",
        "classification": "RZ_IMPLICIT_VILLASENOR_PREPHYSICS_SIGILL_BOUNDARY",
        "scope": "The runtime control reaches solver DOF setup but fails before particle push/current deposition; this is not a Villasenor physics pass/fail.",
        "source_files": {"input": str(input_path), "theta_solver": str(theta_path), "implicit_solver": str(implicit_path), "particle_dispatch": str(particle_path)},
        "runtime_log": str(args.runtime_log),
        "checks": checks,
    }
    result["passed"] = all(item["passed"] for item in checks.values())
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# RZ implicit Villasenor build boundary", "", f"- status: `{'PASS' if result['passed'] else 'FAIL'}`", f"- classification: `{result['classification']}`", f"- scope: {result['scope']}", ""]
    for name, item in checks.items():
        lines.append(f"- `{name}`: `{item['count']}` occurrence(s) - {'PASS' if item['passed'] else 'FAIL'}")
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{'PASS' if result['passed'] else 'FAIL'}: RZ implicit Villasenor boundary contract")
    if not result["passed"]:
        raise SystemExit("RZ implicit Villasenor boundary contract failed")


if __name__ == "__main__":
    main()
