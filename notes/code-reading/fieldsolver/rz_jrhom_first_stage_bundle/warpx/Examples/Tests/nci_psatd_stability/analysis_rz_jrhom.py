#!/usr/bin/env python3
"""
Draft WarpX-side first-stage analysis for test_rz_psatd_JRhom_LL2.

This file is intentionally stored in PIC-tutor as a patch draft asset. It is
the smallest helper shape that matches the current mpi2 evidence boundary:

- always enforce finite-field sanity
- enforce a first-stage energy gate
- defer any spike gate to a follow-up
"""

import sys

import numpy as np
import yt

yt.funcs.mylog.setLevel(0)


EPSILON_0 = 8.8541878128e-12
FIELD_NAMES = ("Er", "Ez", "Bt", "jr", "jz", "rho")

# Candidate first-stage constants derived from the current mpi2 ledger:
# baseline_energy = 2.7378937095024567e+10
# energy_ref = 2.8020912961036427e+10
# energy_safety_factor = 1.001
ENERGY_REF = 2.8020912961036427e+10
TOL_ENERGY = 9.7806649163175208e-01


def main() -> None:
    filename = sys.argv[1]
    ds = yt.load(filename)

    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()

    grid = ds.covering_grid(
        level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions
    )

    fields = {}
    for name in FIELD_NAMES:
        arr = grid["boxlib", name].squeeze().v
        if not np.all(np.isfinite(arr)):
            raise AssertionError(f"{name} contains non-finite values")
        fields[name] = arr

    er = fields["Er"]
    ez = fields["Ez"]
    energy = np.sum(EPSILON_0 * 0.5 * (er**2 + ez**2))
    err_energy = energy / ENERGY_REF

    print("\nCheck finite-field sanity:")
    print("all_fields_finite = True")

    print("\nCheck numerical stability:")
    print(f"energy = {energy}")
    print(f"energy_ref = {ENERGY_REF}")
    print(f"err_energy = {err_energy}")
    print(f"tol_energy = {TOL_ENERGY}")
    assert err_energy <= TOL_ENERGY


if __name__ == "__main__":
    main()
