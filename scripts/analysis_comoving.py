#!/usr/bin/env python
"""Prototype analysis script for comoving PSATD regression design work.

This script mirrors the style of WarpX regression analysis helpers but keeps
the gate semantics explicit:

- finite-field checks are always performed
- spike-ratio checks are optional and are the current preferred first-stage gate
- energy-ratio checks are optional and remain disabled by default because the
  current PIC-tutor evidence does not yet justify a hard-coded comoving energy
  oracle

It is intentionally located in PIC-tutor, not in ../warpx, so that the gate
shape can be tested locally before any WarpX-side patch is proposed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import scipy.constants as scc


FIELD_NAMES = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run prototype finite/spike/optional-energy analysis for a WarpX comoving plotfile."
    )
    parser.add_argument("plotfile", type=Path, help="WarpX plotfile to analyze")
    parser.add_argument(
        "--label",
        default="comoving-analysis",
        help="Label used in printed summaries",
    )
    parser.add_argument(
        "--ledger-json",
        type=Path,
        help=(
            "Optional reference ledger JSON. If provided, "
            "`spike_ratio_ref_stable` and `energy_ref_unstable` can be loaded from it."
        ),
    )
    parser.add_argument(
        "--spike-ratio-ref",
        type=float,
        help="Reference spike ratio from a stable baseline.",
    )
    parser.add_argument(
        "--spike-ratio-max",
        type=float,
        help="Direct absolute spike-ratio ceiling. Overrides ledger/ref-derived thresholds.",
    )
    parser.add_argument(
        "--spike-ratio-safety-factor",
        type=float,
        default=1.0,
        help="Multiplier applied to the chosen spike-ratio reference. Default: 1.0",
    )
    parser.add_argument(
        "--enable-spike-gate",
        action="store_true",
        help="Enable spike-ratio gate. Without this flag the script reports the ratio but does not assert on it.",
    )
    parser.add_argument(
        "--energy-ref",
        type=float,
        help="Reference unstable energy used for an optional energy-ratio gate.",
    )
    parser.add_argument(
        "--tol-energy",
        type=float,
        help="Maximum allowed energy / energy_ref ratio. Required when --enable-energy-gate is set.",
    )
    parser.add_argument(
        "--enable-energy-gate",
        action="store_true",
        help="Enable optional energy-ratio gate. Disabled by default in the current comoving prototype.",
    )
    parser.add_argument(
        "--dump-json",
        action="store_true",
        help="Emit the computed summary as JSON after textual output.",
    )
    return parser.parse_args()


def load_ledger(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text())


def load_plotfile_arrays(plotfile: Path) -> tuple[dict[str, np.ndarray], list[int]]:
    try:
        import yt
    except ImportError as exc:
        raise RuntimeError(
            "yt is required to read WarpX plotfiles. Install yt in the current python environment."
        ) from exc

    yt.funcs.mylog.setLevel(0)
    ds = yt.load(str(plotfile))
    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()
    grid = ds.covering_grid(
        level=0,
        left_edge=ds.domain_left_edge,
        dims=ds.domain_dimensions,
    )

    arrays = {
        name: np.asarray(grid["boxlib", name].squeeze().v) for name in FIELD_NAMES
    }
    dims = [int(v) for v in np.asarray(ds.domain_dimensions)]
    return arrays, dims


def choose_spike_threshold(args: argparse.Namespace, ledger: dict[str, Any]) -> float | None:
    if args.spike_ratio_max is not None:
        return args.spike_ratio_max

    ref = args.spike_ratio_ref
    if ref is None:
        ref = (
            ledger.get("derived_contract_observations", {}) or {}
        ).get("spike_ratio_ref_stable")
    if ref is None:
        return None
    return ref * args.spike_ratio_safety_factor


def choose_energy_ref(args: argparse.Namespace, ledger: dict[str, Any]) -> float | None:
    if args.energy_ref is not None:
        return args.energy_ref
    return (ledger.get("derived_contract_observations", {}) or {}).get(
        "energy_ref_unstable"
    )


def main() -> None:
    args = parse_args()
    ledger = load_ledger(args.ledger_json)
    arrays, dims = load_plotfile_arrays(args.plotfile.resolve())

    finite_status = {name: bool(np.all(np.isfinite(arr))) for name, arr in arrays.items()}
    failed_fields = [name for name, ok in finite_status.items() if not ok]
    if failed_fields:
        raise AssertionError(f"Non-finite values found in fields: {', '.join(failed_fields)}")

    ex = arrays["Ex"]
    ey = arrays["Ey"]
    ez = arrays["Ez"]
    e_mag = np.sqrt(ex**2 + ey**2 + ez**2)
    energy = float(np.sum(scc.epsilon_0 * 0.5 * (ex**2 + ey**2 + ez**2)))
    e_mag_max = float(np.max(e_mag))
    e_mag_p99 = float(np.percentile(e_mag, 99))
    spike_ratio = float(e_mag_max / (e_mag_p99 + 1e-300))

    summary = {
        "label": args.label,
        "plotfile": str(args.plotfile.resolve()),
        "domain_dimensions": dims,
        "all_fields_finite": True,
        "electric_energy": energy,
        "e_mag_max": e_mag_max,
        "e_mag_p99": e_mag_p99,
        "spike_ratio": spike_ratio,
    }

    print(f"\n[{args.label}] finite-field sanity")
    print("all_fields_finite = True")
    print(f"domain_dimensions = {dims}")

    print(f"\n[{args.label}] field summary")
    print(f"electric_energy = {energy:.16e}")
    print(f"e_mag_max = {e_mag_max:.16e}")
    print(f"e_mag_p99 = {e_mag_p99:.16e}")
    print(f"spike_ratio = {spike_ratio:.16e}")

    spike_threshold = choose_spike_threshold(args, ledger)
    if args.enable_spike_gate:
        if spike_threshold is None:
            raise SystemExit(
                "--enable-spike-gate requires one of: --spike-ratio-max, "
                "--spike-ratio-ref, or --ledger-json with spike_ratio_ref_stable"
            )
        print(f"\n[{args.label}] spike gate")
        print(f"spike_ratio_threshold = {spike_threshold:.16e}")
        assert spike_ratio <= spike_threshold, (
            f"spike_ratio={spike_ratio:.16e} exceeds threshold={spike_threshold:.16e}"
        )
    elif spike_threshold is not None:
        print(f"\n[{args.label}] spike gate disabled")
        print(f"candidate_spike_ratio_threshold = {spike_threshold:.16e}")

    energy_ref = choose_energy_ref(args, ledger)
    if args.enable_energy_gate:
        if energy_ref is None or args.tol_energy is None:
            raise SystemExit(
                "--enable-energy-gate requires --tol-energy and either --energy-ref "
                "or --ledger-json with energy_ref_unstable"
            )
        err_energy = energy / energy_ref
        summary["energy_ref"] = energy_ref
        summary["err_energy"] = err_energy
        summary["tol_energy"] = args.tol_energy
        print(f"\n[{args.label}] energy gate")
        print(f"energy_ref = {energy_ref:.16e}")
        print(f"err_energy = {err_energy:.16e}")
        print(f"tol_energy = {args.tol_energy:.16e}")
        assert err_energy <= args.tol_energy, (
            f"err_energy={err_energy:.16e} exceeds tol_energy={args.tol_energy:.16e}"
        )
    elif energy_ref is not None:
        err_energy = energy / energy_ref
        print(f"\n[{args.label}] energy gate disabled")
        print(f"candidate_energy_ref = {energy_ref:.16e}")
        print(f"candidate_err_energy = {err_energy:.16e}")

    if args.dump_json:
        print("\n" + json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"\nAssertion failed: {exc}", file=sys.stderr)
        raise
