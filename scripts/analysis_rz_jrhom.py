#!/usr/bin/env python
"""Prototype analysis helper for RZ JRhom LL2 stability-style validation.

This script is intentionally kept in PIC-tutor, not in ../warpx. It turns the
current local sibling scan into an explicit first-stage gate shape:

- finite-field checks are always required
- energy gate is the default first-stage discriminator
- spike gate is optional and kept as an additive enhancement
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np


EPSILON_0 = 8.8541878128e-12
FIELD_NAMES = ("Er", "Ez", "Bt", "jr", "jz", "rho")
DEFAULT_LEDGER = (
    Path(__file__).resolve().parents[1]
    / "runs"
    / "fieldsolver-validation"
    / "rz-reference-ledgers"
    / "rz-jrhom-reference-scan-mpi2.json"
)
DEFAULT_REFERENCE_LABEL = "ll2-no-timeavg-cleaning"
DEFAULT_BASELINE_LABEL = "baseline-jrhom-ll2-timeavg-cleaning"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run prototype finite/energy/optional-spike analysis for an RZ JRhom plotfile."
    )
    parser.add_argument("plotfile", type=Path, help="WarpX plotfile to analyze")
    parser.add_argument(
        "--label",
        default="rz-jrhom-analysis",
        help="Label used in printed summaries.",
    )
    parser.add_argument(
        "--ledger-json",
        type=Path,
        default=DEFAULT_LEDGER,
        help="Reference sibling scan JSON used to derive energy/spike thresholds.",
    )
    parser.add_argument(
        "--reference-label",
        default=DEFAULT_REFERENCE_LABEL,
        help="Candidate label used as the unstable reference energy/spike source.",
    )
    parser.add_argument(
        "--baseline-label",
        default=DEFAULT_BASELINE_LABEL,
        help="Baseline label used to derive the stable-side tolerance.",
    )
    parser.add_argument(
        "--energy-ref",
        type=float,
        help="Direct unstable reference energy. Overrides ledger-derived value.",
    )
    parser.add_argument(
        "--tol-energy",
        type=float,
        help="Direct energy ratio tolerance. Overrides ledger-derived value.",
    )
    parser.add_argument(
        "--energy-safety-factor",
        type=float,
        default=1.001,
        help="Multiplier applied to the derived stable/reference energy ratio. Default: 1.001",
    )
    parser.add_argument(
        "--disable-energy-gate",
        action="store_true",
        help="Disable the default energy gate and report it as candidate-only.",
    )
    parser.add_argument(
        "--enable-spike-gate",
        action="store_true",
        help="Enable optional spike gate in addition to finite + energy.",
    )
    parser.add_argument(
        "--spike-ratio-max",
        type=float,
        help="Direct spike ratio ceiling. Overrides ledger-derived value.",
    )
    parser.add_argument(
        "--spike-safety-factor",
        type=float,
        default=1.001,
        help="Multiplier applied to the derived stable/reference spike ratio. Default: 1.001",
    )
    parser.add_argument(
        "--dump-json",
        action="store_true",
        help="Emit the computed summary as JSON after textual output.",
    )
    return parser.parse_args()


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


def load_ledger(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text())


def find_candidate(
    ledger: dict[str, Any], label: str, required: bool = True
) -> dict[str, Any] | None:
    for item in (ledger.get("summary", {}) or {}).get("candidates", []):
        if item.get("label") == label:
            return item
    if required:
        raise SystemExit(f"Could not find candidate label {label!r} in ledger JSON.")
    return None


def derive_energy_gate(args: argparse.Namespace, ledger: dict[str, Any]) -> tuple[float | None, float | None]:
    if args.energy_ref is not None and args.tol_energy is not None:
        return args.energy_ref, args.tol_energy

    reference = find_candidate(ledger, args.reference_label, required=False)
    baseline = find_candidate(ledger, args.baseline_label, required=False)

    energy_ref = args.energy_ref
    if energy_ref is None and reference is not None:
        energy_ref = ((reference.get("metrics") or {}).get("electric_energy"))

    tol_energy = args.tol_energy
    if tol_energy is None and energy_ref is not None and baseline is not None:
        baseline_energy = (baseline.get("metrics") or {}).get("electric_energy")
        if baseline_energy is not None:
            tol_energy = (baseline_energy / energy_ref) * args.energy_safety_factor

    return energy_ref, tol_energy


def derive_spike_threshold(args: argparse.Namespace, ledger: dict[str, Any]) -> float | None:
    if args.spike_ratio_max is not None:
        return args.spike_ratio_max

    reference = find_candidate(ledger, args.reference_label, required=False)
    baseline = find_candidate(ledger, args.baseline_label, required=False)
    if reference is None or baseline is None:
        return None

    reference_spike = (reference.get("metrics") or {}).get("spike_ratio")
    baseline_spike = (baseline.get("metrics") or {}).get("spike_ratio")
    if reference_spike is None or baseline_spike is None:
        return None

    return (baseline_spike / reference_spike) * args.spike_safety_factor


def main() -> None:
    args = parse_args()
    ledger = load_ledger(args.ledger_json)
    arrays, dims = load_plotfile_arrays(args.plotfile.resolve())

    finite_status = {name: bool(np.all(np.isfinite(arr))) for name, arr in arrays.items()}
    failed_fields = [name for name, ok in finite_status.items() if not ok]
    if failed_fields:
        raise AssertionError(f"Non-finite values found in fields: {', '.join(failed_fields)}")

    er = arrays["Er"]
    ez = arrays["Ez"]
    electric_energy = float(np.sum(EPSILON_0 * 0.5 * (er**2 + ez**2)))
    e_mag = np.sqrt(er**2 + ez**2)
    e_mag_max = float(np.max(e_mag))
    e_mag_p99 = float(np.percentile(e_mag, 99))
    spike_ratio = float(e_mag_max / (e_mag_p99 + 1e-300))

    summary = {
        "label": args.label,
        "plotfile": str(args.plotfile.resolve()),
        "domain_dimensions": dims,
        "all_fields_finite": True,
        "electric_energy": electric_energy,
        "e_mag_max": e_mag_max,
        "e_mag_p99": e_mag_p99,
        "spike_ratio": spike_ratio,
        "reference_label": args.reference_label,
        "baseline_label": args.baseline_label,
    }

    print(f"\n[{args.label}] finite-field sanity")
    print("all_fields_finite = True")
    print(f"domain_dimensions = {dims}")

    print(f"\n[{args.label}] field summary")
    print(f"electric_energy = {electric_energy:.16e}")
    print(f"e_mag_max = {e_mag_max:.16e}")
    print(f"e_mag_p99 = {e_mag_p99:.16e}")
    print(f"spike_ratio = {spike_ratio:.16e}")

    energy_ref, tol_energy = derive_energy_gate(args, ledger)
    if args.disable_energy_gate:
        if energy_ref is not None:
            err_energy = electric_energy / energy_ref
            print(f"\n[{args.label}] energy gate disabled")
            print(f"candidate_energy_ref = {energy_ref:.16e}")
            print(f"candidate_tol_energy = {tol_energy:.16e}" if tol_energy is not None else "candidate_tol_energy = undefined")
            print(f"candidate_err_energy = {err_energy:.16e}")
    else:
        if energy_ref is None or tol_energy is None:
            raise SystemExit(
                "Energy gate requires either explicit --energy-ref and --tol-energy, "
                "or a ledger JSON containing both the baseline and reference candidates."
            )
        err_energy = electric_energy / energy_ref
        summary["energy_ref"] = energy_ref
        summary["tol_energy"] = tol_energy
        summary["err_energy"] = err_energy
        print(f"\n[{args.label}] energy gate")
        print(f"energy_ref = {energy_ref:.16e}")
        print(f"tol_energy = {tol_energy:.16e}")
        print(f"err_energy = {err_energy:.16e}")
        assert err_energy <= tol_energy, (
            f"err_energy={err_energy:.16e} exceeds tol_energy={tol_energy:.16e}"
        )

    spike_threshold = derive_spike_threshold(args, ledger)
    if args.enable_spike_gate:
        if spike_threshold is None:
            raise SystemExit(
                "Spike gate requires either --spike-ratio-max or a ledger JSON "
                "containing both the baseline and reference candidates."
            )
        summary["spike_ratio_max"] = spike_threshold
        print(f"\n[{args.label}] spike gate")
        print(f"spike_ratio_max = {spike_threshold:.16e}")
        assert spike_ratio <= spike_threshold, (
            f"spike_ratio={spike_ratio:.16e} exceeds spike_ratio_max={spike_threshold:.16e}"
        )
    elif spike_threshold is not None:
        print(f"\n[{args.label}] spike gate disabled")
        print(f"candidate_spike_ratio_max = {spike_threshold:.16e}")

    if args.dump_json:
        print("\n" + json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"\nAssertion failed: {exc}", file=sys.stderr)
        raise
