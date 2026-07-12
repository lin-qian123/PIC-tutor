#!/usr/bin/env python
"""Validate the reduced transition-zone route-count ledger schema.

This checks the analysis contract on supplied JSON records. It does not claim
that the current WarpX checkout emits these records at runtime.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


COUNT_KEYS = (
    "nfine_gather",
    "nbuffer_gather",
    "nfine_deposit",
    "nbuffer_deposit",
    "np_before_partition",
)
WEIGHT_KEYS = ("weight_fine", "weight_buffer", "weight_deposited")
SOURCE_KEYS = (
    "rho_fp_l1",
    "rho_buf_l1",
    "current_fp_l1",
    "current_buf_l1",
    "coarsened_fine_l1",
    "merged_coarse_l1",
    "owner_mask_removed_l1",
    "post_sync_l1",
)
REQUIRED_FLAGS = ("route_partition_pass", "source_merge_pass")


def finite_nonnegative(record: dict[str, Any], key: str) -> bool:
    value = record.get(key)
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0.0


def validate_record(record: dict[str, Any], index: int, tolerance: float) -> list[str]:
    errors: list[str] = []
    for key in COUNT_KEYS:
        if not isinstance(record.get(key), int) or record[key] < 0:
            errors.append(f"record[{index}].{key} must be a non-negative integer")
    for key in WEIGHT_KEYS + SOURCE_KEYS:
        if not finite_nonnegative(record, key):
            errors.append(f"record[{index}].{key} must be a finite non-negative number")
    for key in REQUIRED_FLAGS:
        if record.get(key) is not True:
            errors.append(f"record[{index}].{key} must be true")
    if record.get("nfine_gather", -1) + record.get("nbuffer_gather", -1) != record.get("np_before_partition", -2):
        errors.append(f"record[{index}] gather route counts do not close")
    if record.get("nfine_deposit", -1) + record.get("nbuffer_deposit", -1) != record.get("np_before_partition", -2):
        errors.append(f"record[{index}] deposit route counts do not close")
    if abs(record.get("weight_fine", math.nan) + record.get("weight_buffer", math.nan) - record.get("weight_deposited", math.nan)) > tolerance:
        errors.append(f"record[{index}] deposited weight does not close")
    return errors


def validate(data: dict[str, Any], tolerance: float) -> dict[str, Any]:
    records = data.get("records")
    errors: list[str] = []
    if data.get("schema") != "transition-zone-route-count-v0":
        errors.append("schema must be transition-zone-route-count-v0")
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list")
        records = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record[{index}] must be an object")
            continue
        errors.extend(validate_record(record, index, tolerance))
    return {
        "contract": "transition-zone reduced route-count ledger schema",
        "schema": "transition-zone-route-count-v0",
        "record_count": len(records),
        "passed": not errors,
        "classification": "DESIGN_SCHEMA_VALIDATED" if not errors else "DESIGN_SCHEMA_REJECTED",
        "scope": "schema and ledger arithmetic only; current WarpX checkout does not emit this runtime ledger",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--tolerance", type=float, default=1.0e-12)
    args = parser.parse_args()
    result = validate(json.loads(args.input.read_text(encoding="utf-8")), args.tolerance)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
