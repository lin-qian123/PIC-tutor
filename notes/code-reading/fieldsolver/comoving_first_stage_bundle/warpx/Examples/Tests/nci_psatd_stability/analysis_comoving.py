#!/usr/bin/env python
"""
Draft WarpX-side first-stage analysis for test_2d_comoving_psatd_hybrid.

This file is intentionally stored in PIC-tutor as a patch draft asset. It is
the smallest helper shape that matches the current evidence boundary:

- always enforce finite-field sanity
- enforce a first-stage spike-ratio gate
- do not yet enforce an energy gate

Why no energy gate here?
Because the current local calibration audit shows that the obvious
`no-comoving` sibling does not yield the same unstable-energy ordering that the
analogous Galilean family does, so a hard-coded comoving `energy_ref` would
overstate what has actually been validated.
"""

import sys

import numpy as np
import yt

yt.funcs.mylog.setLevel(0)


FIELD_NAMES = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho")

# Candidate first-stage ceiling derived from the current stable baseline:
# spike_ratio_ref_stable = 1.1103719982074416
# safety_factor = 1.001
SPIKE_RATIO_MAX = 1.1114823702056489


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

    ex = fields["Ex"]
    ey = fields["Ey"]
    ez = fields["Ez"]
    e_mag = np.sqrt(ex**2 + ey**2 + ez**2)
    spike_ratio = np.max(e_mag) / (np.percentile(e_mag, 99) + 1e-300)

    print("\nCheck finite-field sanity:")
    print("all_fields_finite = True")

    print("\nCheck spike-ratio sanity:")
    print(f"spike_ratio = {spike_ratio}")
    print(f"spike_ratio_max = {SPIKE_RATIO_MAX}")
    assert spike_ratio <= SPIKE_RATIO_MAX


if __name__ == "__main__":
    main()
