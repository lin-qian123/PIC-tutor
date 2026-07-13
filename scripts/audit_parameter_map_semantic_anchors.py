#!/usr/bin/env python
"""Audit consumer/default/validation anchors for structured parameter-map rows."""

from __future__ import annotations

import json
from pathlib import Path

from audit_parameter_map_structured_review import CASES, rows_by_parameter, source_paths


ROOT = Path(__file__).resolve().parents[1]


SEMANTIC_CASES = {
    "<species_name>.attribute.<name>(x,y,z,ux,uy,uz,t)": {
        "kind": "dynamic_key_consumer_and_type",
        "required": ["makeParser", "compile<7>()", "AddIntComp", "AddRealComp", "static_cast<int>"],
        "interpretation": "parser expression is compiled during particle initialization and written to typed runtime components",
    },
    "<collision_name>.<scattering_process>_cross_section": {
        "kind": "dynamic_key_consumer_and_validation",
        "required": ["query(kw_cross_section", "ScatteringProcess process", "process.type() != ScatteringProcessType::INVALID"],
        "interpretation": "dynamic cross-section key is loaded into a ScatteringProcess and invalid process types are rejected",
    },
    "<collision_name>.<scattering_process>_energy": {
        "kind": "dynamic_key_consumer_and_validation",
        "required": ["getWithParser", "ScatteringProcess process", "process.type() != ScatteringProcessType::INVALID"],
        "interpretation": "conditional energy key is parser-read before process construction and participates in process validation",
    },
    "<diag_name>.adios2_operator.parameters.*": {
        "kind": "dynamic_key_consumer_and_forwarding",
        "required": ["getEntries(prefix)", "pp.get(k, v)", "operator_parameters.insert", "m_OpenPMDPlotWriter"],
        "interpretation": "arbitrary operator suffixes are collected, prefix-stripped, and forwarded as a parameter map",
    },
    "<diag_name>.adios2_engine.parameters.*": {
        "kind": "dynamic_key_consumer_and_forwarding",
        "required": ["getEntries(engine_prefix)", "ppe.get(k, v)", "engine_parameters.insert", "m_OpenPMDPlotWriter"],
        "interpretation": "arbitrary engine suffixes are collected, prefix-stripped, and forwarded as a parameter map",
    },
    "<diag_name>.particle_fields.<field_name>.do_average": {
        "kind": "dynamic_key_default_and_consumer",
        "required": ["bool do_average = true", "query(var + \".do_average\", do_average)", "m_pfield_do_average", "ParticleReductionFunctor"],
        "interpretation": "particle-field averaging defaults true and is forwarded to the reduction functor",
    },
    "<diag_name>.particle_fields.<field_name>(x,y,z,ux,uy,uz)": {
        "kind": "dynamic_key_required_parser_and_consumer",
        "required": ["Store_parserString", "cannot find parser string", "m_pfield_strings", "ParticleReductionFunctor"],
        "interpretation": "the particle-field expression is required, stored, and consumed by the reduction functor",
    },
    "<diag_name>.particle_fields.<field_name>.filter(x,y,z,ux,uy,uz)": {
        "kind": "dynamic_key_optional_filter_and_consumer",
        "required": ["query(var + \".filter(x,y,z,ux,uy,uz)\"", "m_pfield_dofilter", "m_pfield_filter_strings", "ParticleReductionFunctor"],
        "interpretation": "the filter expression is optional and its presence/string are forwarded independently",
    },
    "amr.ref_ratio": {
        "kind": "external_owner_consumer_boundary",
        "required": ["refRatio(lev-1)", "refRatio(lev)", "coarsen(ref_ratio)"],
        "interpretation": "AMReX-owned ratio is consumed by WarpX geometry/time consumers after ownership leaves ParmParse",
    },
    "amr.ref_ratio_vect": {
        "kind": "external_owner_consumer_boundary",
        "required": ["ref_ratios", "ref_ratio[idim]", "domain_box.coarsen(ref_ratios[lev-1])"],
        "interpretation": "directional AMReX-owned ratio is consumed as a full IntVect and by per-axis geometry branches",
    },
}


def main() -> int:
    rows = rows_by_parameter()
    checks = []
    records = []
    for parameter, expected in SEMANTIC_CASES.items():
        columns = rows.get(parameter)
        references = [item.strip().strip("`") for item in (columns[6].split(",") if columns else [])]
        source_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for reference in references
            for path in source_paths(reference)
        )
        missing = [anchor for anchor in expected["required"] if anchor not in source_text]
        passed = columns is not None and not missing
        checks.append({"parameter": parameter, "kind": expected["kind"], "passed": passed})
        records.append({
            "parameter": parameter,
            "kind": expected["kind"],
            "required_anchor_count": len(expected["required"]),
            "missing_anchors": missing,
            "interpretation": expected["interpretation"],
        })

    result = {
        "contract": "parameter-map semantic consumer/default/validation anchors",
        "scope": "10 structured parameter rows; source-level semantic anchors, not C++ AST, runtime value execution, or all defaults",
        "passed": all(check["passed"] for check in checks),
        "classification": "STRUCTURED_PARAMETER_MAP_SEMANTIC_ANCHORS_VERIFIED_RUNTIME_VALUE_EXECUTION_REMAINS",
        "case_count": len(checks),
        "checks": checks,
        "records": records,
    }
    output_dir = ROOT / "runs/stage-c-validation/parameter-map-semantic-anchor-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Parameter-map semantic consumer/default/validation anchors",
        "",
        f"- status: `{'PASS' if result['passed'] else 'FAIL'}`",
        f"- cases: `{result['case_count']}`",
        "- scope: source-level semantic anchors; runtime value execution and complete C++ AST remain outside scope",
        "",
        "| parameter | kind | result |",
        "|---|---|:---:|",
    ]
    lines.extend(f"| `{check['parameter']}` | `{check['kind']}` | `{'PASS' if check['passed'] else 'FAIL'}` |" for check in checks)
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("passed", "classification", "case_count")}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
