#!/usr/bin/env python
"""Independent reader-side contract for the RZ spacecraft-charging case."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--plot-dir", default="diags/diag1")
    args = parser.parse_args()

    from openpmd_viewer import OpenPMDTimeSeries

    case_dir = args.case_dir.resolve()
    ts = OpenPMDTimeSeries(str(case_dir / args.plot_dir))
    iterations = np.asarray(ts.iterations)
    dt = 1.27e-8
    times = dt * iterations
    phi_min = np.asarray([np.min(ts.get_field("phi", iteration=int(it), plot=False)[0]) for it in iterations])

    def model(time, v0, tau):
        return v0 * (1.0 - np.exp(-np.asarray(time) / tau))

    fitted, _ = curve_fit(model, times, phi_min)
    v0, tau = [float(value) for value in fitted]
    expected_v0, expected_tau = -151.347, 0.000004351
    v0_error = abs((v0 - expected_v0) / expected_v0)
    tau_error = abs((tau - expected_tau) / expected_tau)
    result = {
        "case": "test_rz_spacecraft_charging_picmi",
        "iterations": int(iterations.size),
        "first_iteration": int(iterations[0]),
        "last_iteration": int(iterations[-1]),
        "phi_min_initial": float(phi_min[0]),
        "phi_min_final": float(phi_min[-1]),
        "fit_v0": v0,
        "fit_tau": tau,
        "reference_v0": expected_v0,
        "reference_tau": expected_tau,
        "relative_v0_error": v0_error,
        "relative_tau_error": tau_error,
        "v0_pass": v0_error < 0.04,
        "tau_pass": tau_error < 0.20,
    }
    result["contract_pass"] = bool(result["v0_pass"] and result["tau_pass"])
    (case_dir / "contract.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (case_dir / "contract.md").write_text(
        "\n".join([
            "# RZ spacecraft-charging contract", "",
            f"- OpenPMD iterations: `{result['first_iteration']} -> {result['last_iteration']}` (`{result['iterations']}` samples).",
            f"- `phi_min`: `{result['phi_min_initial']:.6f} -> {result['phi_min_final']:.6f}`.",
            f"- Fit: `v0={v0:.6f}`, `tau={tau:.9e}`; relative errors `{v0_error:.6%}` and `{tau_error:.6%}`.",
            f"- Gates: `v0 {'PASS' if result['v0_pass'] else 'FAIL'}`, `tau {'PASS' if result['tau_pass'] else 'FAIL'}`.",
            f"- Independent contract: `{'PASS' if result['contract_pass'] else 'FAIL'}`.",
        ]) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["contract_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
