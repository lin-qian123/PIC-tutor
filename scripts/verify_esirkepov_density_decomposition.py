#!/usr/bin/env python
"""Verify the second-order Esirkepov density-decomposition identity."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def density_decomposition(old, delta):
    ox, oy, oz = old
    dx, dy, dz = delta
    w1 = dx * (oy * oz + 0.5 * dy * oz + 0.5 * oy * dz + (1.0 / 3.0) * dy * dz)
    w2 = dy * (ox * oz + 0.5 * dx * oz + 0.5 * ox * dz + (1.0 / 3.0) * dx * dz)
    w3 = dz * (ox * oy + 0.5 * dx * oy + 0.5 * ox * dy + (1.0 / 3.0) * dx * dy)
    return w1, w2, w3


def product_difference(old, delta):
    ox, oy, oz = old
    dx, dy, dz = delta
    return (ox + dx) * (oy + dy) * (oz + dz) - ox * oy * oz


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    rng = random.Random(2001)
    sample_count = 10000
    max_error = 0.0
    for _ in range(sample_count):
        old = tuple(rng.uniform(-1.0, 1.0) for _ in range(3))
        delta = tuple(rng.uniform(-1.0, 1.0) for _ in range(3))
        residual = sum(density_decomposition(old, delta)) - product_difference(old, delta)
        max_error = max(max_error, abs(residual))
    if max_error > 2.0e-15:
        raise AssertionError(f"density decomposition residual {max_error:.3e}")
    result = {
        "contract": "Esirkepov second-order density decomposition identity",
        "sample_count": sample_count,
        "random_seed": 2001,
        "max_residual": max_error,
        "tolerance": 2.0e-15,
        "passed": True,
        "scope": "paper formula / algebra layer; not a WarpX kernel or end-to-end regression",
    }
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(
            "# Esirkepov density-decomposition contract\n\n"
            f"- samples: `{sample_count}`\n"
            f"- deterministic seed: `{result['random_seed']}`\n"
            f"- maximum residual: `{max_error:.8e}`\n"
            "- gate: maximum residual `<= 2e-15`\n"
            "- status: `PASS`\n"
            f"- scope: {result['scope']}\n",
            encoding="utf-8",
        )
    print(f"PASS: {sample_count} cases, max residual = {max_error:.3e}")


if __name__ == "__main__":
    main()
