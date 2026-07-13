#!/usr/bin/env python
"""Verify the source anchors behind the non-literal parameter-map entries."""

from __future__ import annotations

import json
from pathlib import Path

from audit_parameter_map_surface import MAP, source_paths


ROOT = MAP.parent.parent
AMREX = ROOT.parent / "amrex"


CASES = {
    "amr.ref_ratio": {
        "kind": "external_owner",
        "required_map_text": "AMReX/AmrCore-owned input",
        "source_files": [AMREX / "Src/AmrCore/AMReX_AmrMesh.cpp"],
        "required_source_text": [
            'pp.queryarr("ref_ratio",ratios)',
            "Only input *either* ref_ratio or ref_ratio_vect",
        ],
    },
    "amr.ref_ratio_vect": {
        "kind": "external_owner",
        "required_map_text": "AMReX/AmrCore-owned input",
        "source_files": [AMREX / "Src/AmrCore/AMReX_AmrMesh.cpp"],
        "required_source_text": [
            'pp.queryarr("ref_ratio_vect",ratios_vect,0,nratios_vect)',
            "ref_ratio[i][n] = ratios_vect[k]",
        ],
    },
    "<species_name>.attribute.<name>(x,y,z,ux,uy,uz,t)": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            '"attribute."+m_user_int_attribs',
            '"attribute."+m_user_real_attribs',
        ],
    },
    "<collision_name>.<scattering_process>_cross_section": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            'scattering_process + "_cross_section"',
            'pp_collision_name.query(kw_cross_section',
        ],
    },
    "<collision_name>.<scattering_process>_energy": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            'scattering_process + "_energy"',
            'getWithParser(\n                pp_collision_name, kw_energy.c_str()',
        ],
    },
    "<diag_name>.adios2_operator.parameters.*": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            "auto entr = amrex::ParmParse::getEntries(prefix)",
            "k.erase(0, prefix_len)",
        ],
    },
    "<diag_name>.adios2_engine.parameters.*": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            "auto eng_entr = amrex::ParmParse::getEntries(engine_prefix)",
            "k.erase(0, prefixlen)",
        ],
    },
    "<diag_name>.particle_fields.<field_name>.do_average": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            'var + ".do_average"',
            "m_pfield_do_average.push_back(do_average)",
        ],
    },
    "<diag_name>.particle_fields.<field_name>(x,y,z,ux,uy,uz)": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            'm_diag_name + ".particle_fields"',
            'Store_parserString(\n            pp_diag_pfield, (var + "(x,y,z,ux,uy,uz)")',
        ],
    },
    "<diag_name>.particle_fields.<field_name>.filter(x,y,z,ux,uy,uz)": {
        "kind": "dynamic_key_constructor",
        "required_source_text": [
            'var + ".filter(x,y,z,ux,uy,uz)"',
            "m_pfield_filter_strings.push_back(filter_parser_str)",
        ],
    },
}


def rows_by_parameter() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for line in MAP.read_text(encoding="utf-8").splitlines()[10:]:
        if not line.startswith("|"):
            continue
        columns = [column.strip() for column in line.split("|")[1:-1]]
        if len(columns) < 8:
            continue
        result[columns[0].strip("`")] = columns
    return result


def main() -> None:
    rows = rows_by_parameter()
    checks = []
    records = []
    for parameter, expected in CASES.items():
        columns = rows.get(parameter)
        map_ok = columns is not None
        map_text = " ".join(columns or [])
        references = [item.strip().strip("`") for item in (columns[6].split(",") if columns else [])]
        source_fragments = [
            path.read_text(encoding="utf-8", errors="ignore")
            for path in expected.get("source_files", [])
        ]
        source_fragments.extend(
            path.read_text(encoding="utf-8", errors="ignore")
            for reference in references
            for path in source_paths(reference)
        )
        source_text = "\n".join(source_fragments)
        required_map_ok = expected.get("required_map_text", "") in map_text
        required_sources = expected["required_source_text"]
        source_checks = [marker in source_text for marker in required_sources]
        source_ok = all(source_checks)
        passed = map_ok and required_map_ok and source_ok
        checks.append({"parameter": parameter, "kind": expected["kind"], "passed": passed})
        records.append(
            {
                "parameter": parameter,
                "kind": expected["kind"],
                "map_row_present": map_ok,
                "required_map_text_present": required_map_ok,
                "required_source_text": required_sources,
                "required_source_text_present": source_ok,
                "source_marker_checks": source_checks,
                "source_file_count": len(source_text.splitlines()) if source_text else 0,
            }
        )

    result = {
        "contract": "parameter-map structured dynamic/owner review",
        "scope": "10 non-literal parameter rows; source construction/owner anchors only, not full C++ AST or runtime value semantics",
        "contract_pass": all(check["passed"] for check in checks),
        "classification": "STRUCTURED_PARAMETER_MAP_DYNAMIC_AND_EXTERNAL_OWNER_SURFACE_VERIFIED_RUNTIME_SEMANTICS_REMAINS",
        "case_count": len(CASES),
        "dynamic_key_constructor_count": sum(item["kind"] == "dynamic_key_constructor" for item in checks),
        "external_owner_count": sum(item["kind"] == "external_owner" for item in checks),
        "checks": checks,
        "records": records,
    }
    output_dir = ROOT / "runs/stage-c-validation/parameter-map-structured-review-contract"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Parameter-map structured dynamic/owner review",
        "",
        f"- status: `{'PASS' if result['contract_pass'] else 'FAIL'}`",
        f"- cases: `{result['case_count']}`",
        f"- dynamic-key constructors: `{result['dynamic_key_constructor_count']}`",
        f"- external-owner rows: `{result['external_owner_count']}`",
        "- scope: source construction/owner anchors only; not full C++ AST or runtime value semantics",
        "",
        "| parameter | kind | result |",
        "|---|---|:---:|",
    ]
    lines.extend(f"| `{check['parameter']}` | `{check['kind']}` | `{'PASS' if check['passed'] else 'FAIL'}` |" for check in checks)
    (output_dir / "contract.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("contract_pass", "case_count", "dynamic_key_constructor_count", "external_owner_count", "classification")}, ensure_ascii=False))
    if not result["contract_pass"]:
        raise SystemExit("parameter-map structured review contract failed")


if __name__ == "__main__":
    main()
