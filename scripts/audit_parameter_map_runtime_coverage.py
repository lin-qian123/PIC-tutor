#!/usr/bin/env python
"""Audit case-local runtime coverage for structured parameter-map entries."""

from __future__ import annotations

import json
from pathlib import Path

import openpmd_api
import yt


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs/stage-c-validation/parameter-map-runtime"
WARPX = ROOT.parent / "warpx"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def readable_bp5(path: Path) -> bool:
    try:
        series = openpmd_api.Series(str(path), openpmd_api.Access.read_only)
        iterations = list(series.iterations)
        series.close()
        return iterations == [0]
    except Exception:
        return False


def main() -> int:
    attrs = RUNS / "attributes"
    fields = RUNS / "particle-fields"
    dsmc = RUNS / "dsmc"
    adios2 = RUNS / "adios2"
    adios2_operator = RUNS / "adios2-operator"
    ref_ratio_vect = RUNS / "ref-ratio-vect"
    attr_plotfile = attrs / "diags/diag1000001"
    field_plotfile = fields / "diags/diag1000000"
    ref_ratio_input = text(ref_ratio_vect / "warpx_used_inputs")
    adios2_input = text(adios2 / "warpx_used_inputs")
    adios2_operator_input = text(adios2_operator / "warpx_used_inputs")

    attr_input = text(attrs / "warpx_used_inputs")
    field_input = text(fields / "warpx_used_inputs")
    attr_ds = yt.load(str(attr_plotfile))
    field_ds = yt.load(str(field_plotfile))
    attr_fields = {name for _, name in attr_ds.field_list if name.startswith("particle_")}
    field_names = {name for _, name in field_ds.field_list if name in {
        "z_electrons", "uz_electrons", "uz_filt_electrons", "zuz_electrons", "jz_electrons",
        "z_protons", "uz_protons", "uz_filt_protons", "zuz_protons", "jz_protons",
        "z_photons", "uz_photons", "uz_filt_photons", "zuz_photons", "jz_photons",
    }}

    source_collision = WARPX / "Examples/Tests/collision/inputs_test_2d_charge_exchange_dsmc"
    source_attribute = WARPX / "Examples/Physics_applications/laser_acceleration/inputs_base_1d"
    records = [
        {
            "parameter_group": "<species_name>.attribute.<name>(...)",
            "coverage": "runtime",
            "passed": all(token in attr_input for token in ("addRealAttributes", "orig_z", "addIntegerAttributes", "regionofinterest"))
            and {"particle_orig_z", "particle_regionofinterest"}.issubset(attr_fields),
            "evidence": "attributes/warpx_used_inputs + attributes/diags/diag1000001",
            "boundary": "small initialization smoke; not a long production physics regression",
        },
        {
            "parameter_group": "<diag_name>.particle_fields.*",
            "coverage": "runtime",
            "passed": all(token in field_input for token in ("particle_fields_to_plot", "particle_fields_species", "do_average", "filter"))
            and len(field_names) == 15
            and (fields / "diags/openpmd/openpmd_000000.h5").is_file(),
            "evidence": "particle-fields/warpx_used_inputs + particle-fields/diags/diag1000000 + openPMD h5",
            "boundary": "max_step=0 diagnostic smoke; reduction values are not promoted to a physics gate",
        },
        {
            "parameter_group": "<collision_name>.<scattering_process>_{cross_section,energy}",
            "coverage": "input_only",
            "passed": source_collision.is_file() and all(token in text(source_collision) for token in ("scattering_processes", "charge_exchange_cross_section")),
            "evidence": "WarpX Examples/Tests/collision/inputs_test_2d_charge_exchange_dsmc + dsmc/run.log",
            "boundary": "short runtime was attempted but stopped before initialization because the local checkout has no warpx-data/MCC_cross_sections/He/charge_exchange.dat; the dynamic key is not promoted to runtime PASS",
        },
        {
            "parameter_group": "<diag_name>.adios2_{operator,engine}.parameters.*",
            "coverage": "runtime",
            "passed": all(token in adios2_input for token in (
                "openpmd.openpmd_backend = \"bp5\"",
                "openpmd.adios2_engine.type = bp5",
                "openpmd.adios2_engine.parameters.NumAggregators = 1",
            ))
            and (adios2 / "diags/openpmd/openpmd_000000.bp5/data.0").is_file()
            and readable_bp5(adios2 / "diags/openpmd/openpmd_000000.bp5")
            and "Writing openPMD file diags/openpmd000000" in text(adios2 / "run.log")
            and all(token in adios2_operator_input for token in (
                "openpmd.openpmd_backend = \"bp5\"",
                "openpmd.adios2_operator.type = blosc",
                "openpmd.adios2_operator.parameters.compressor = zstd",
                "openpmd.adios2_operator.parameters.clevel = 1",
                "openpmd.adios2_operator.parameters.doshuffle = BLOSC_BITSHUFFLE",
                "openpmd.adios2_operator.parameters.threshold = 2048",
            ))
            and (adios2_operator / "diags/openpmd/openpmd_000000.bp5/data.0").is_file()
            and readable_bp5(adios2_operator / "diags/openpmd/openpmd_000000.bp5")
            and "Writing openPMD file diags/openpmd000000" in text(adios2_operator / "run.log"),
            "evidence": "adios2 and adios2-operator warpx_used_inputs + run.log + BP5 series",
            "boundary": "3D max_step=0 BP5 engine/operator smoke; multi-rank engine semantics and compression numerical fidelity are not promoted",
        },
        {
            "parameter_group": "amr.ref_ratio",
            "coverage": "runtime",
            "passed": (ROOT / "runs/stage-c-validation/esirkepov_langmuir_2d_mr_mpi2/warpx_used_inputs").is_file()
            and "amr.ref_ratio = 4" in text(ROOT / "runs/stage-c-validation/esirkepov_langmuir_2d_mr_mpi2/warpx_used_inputs"),
            "evidence": "esirkepov_langmuir_2d_mr_mpi2/warpx_used_inputs + MR contract",
            "boundary": "covers scalar ratio in one MR case, not all AMReX owner defaults or consumers",
        },
        {
            "parameter_group": "amr.ref_ratio_vect",
            "coverage": "runtime",
            "passed": all(token in ref_ratio_input for token in ("amr.ref_ratio_vect = 2 1", "amr.max_level = 1"))
            and (ref_ratio_vect / "diags/diag1000000/Level_1/Cell_H").is_file(),
            "evidence": "ref-ratio-vect/warpx_used_inputs + ref-ratio-vect/diags/diag1000000 Level_0/Level_1",
            "boundary": "2D max_step=0 initialization smoke; it proves vector parsing and two-level materialization, not anisotropic refinement accuracy",
        },
    ]
    checks = {record["parameter_group"]: record["passed"] for record in records}
    result = {
        "contract": "structured parameter-map runtime coverage",
        "passed": all(record["passed"] or record["coverage"] == "source_only" for record in records),
        "classification": "STRUCTURED_PARAMETER_MAP_RUNTIME_COVERAGE_ATTRIBUTE_PARTICLE_FIELD_VECTOR_RATIO_AND_ADIOS2_BP5_SMOKE_DSMC_DATA_BOUNDARY",
        "records": records,
        "checks": checks,
        "runtime_case_count": sum(record["coverage"] == "runtime" for record in records),
        "input_only_case_count": sum(record["coverage"] == "input_only" for record in records),
        "source_only_case_count": sum(record["coverage"] == "source_only" for record in records),
        "scope": "case-local runtime/input/source coverage inventory; not a full parameter semantic or physics regression",
    }
    output_dir = ROOT / "runs/stage-c-validation/parameter-map-runtime-coverage"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Structured parameter-map runtime coverage",
        "",
        f"- status: `{'PASS' if result['passed'] else 'BOUNDARY'}`",
        f"- classification: `{result['classification']}`",
        f"- runtime cases: `{result['runtime_case_count']}`",
        f"- input-only cases: `{result['input_only_case_count']}`",
        f"- source-only gaps: `{result['source_only_case_count']}`",
        "",
        "| parameter group | coverage | result |",
        "|---|---|:---:|",
    ]
    lines.extend(f"| `{record['parameter_group']}` | `{record['coverage']}` | `{'PASS' if record['passed'] else 'BOUNDARY'}` |" for record in records)
    lines += ["", "Source-only and input-only rows remain explicit coverage gaps; the contract does not convert them into runtime PASS."]
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "classification": result["classification"], "runtime_case_count": result["runtime_case_count"], "source_only_case_count": result["source_only_case_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
