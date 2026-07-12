#!/usr/bin/env python
"""Build a Poincare-section and invariant ledger for the Higuera-Cary test."""

from __future__ import annotations

import argparse
import json
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import yt
from scipy.constants import c, m_e

yt.funcs.mylog.setLevel(40)


L0 = 0.299792458
A_COEFF = 1.0
B_COEFF = 2.0
EXPECTED_SPECIES = ("p05", "p10", "p17", "p22", "p27")


def plotfiles(run_dir: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in (run_dir / "diags").glob("diag1[0-9]*")
            if path.is_dir() and re.fullmatch(r"diag1\d+", path.name)
        ),
        key=lambda path: int(re.search(r"diag1(\d+)$", path.name).group(1)),
    )


def load_trajectories(run_dir: Path, expected_species: tuple[str, ...]) -> tuple[np.ndarray, dict[str, dict[str, np.ndarray]]]:
    files = plotfiles(run_dir)
    if len(files) < 1001:
        raise ValueError(f"expected at least 1001 plotfiles in {run_dir}, got {len(files)}")
    times: list[float] = []
    rows = {species: {name: [] for name in ("x", "y", "px", "py", "pz")} for species in expected_species}
    for path in files:
        ds = yt.load(str(path))
        ad = ds.all_data()
        times.append(float(ds.current_time))
        for species in expected_species:
            rows[species]["x"].append(float(ad[species, "particle_position_x"].to_ndarray()[0]))
            rows[species]["y"].append(float(ad[species, "particle_position_y"].to_ndarray()[0]))
            # WarpX writes physical momentum (kg m/s); the paper uses p/(m c).
            rows[species]["px"].append(float(ad[species, "particle_momentum_x"].to_ndarray()[0]) / (m_e * c))
            rows[species]["py"].append(float(ad[species, "particle_momentum_y"].to_ndarray()[0]) / (m_e * c))
            rows[species]["pz"].append(float(ad[species, "particle_momentum_z"].to_ndarray()[0]) / (m_e * c))
    return np.asarray(times), {species: {name: np.asarray(values) for name, values in data.items()} for species, data in rows.items()}


def hamiltonian(x: float, y: float, px: float, py: float, pz: float) -> float:
    xn = x / L0
    # WarpX writes mechanical p_z. The paper's canonical P_z satisfies
    # P_z - A_z = p_z(mechanical), so the kinetic term is simply p_z^2.
    return float(np.sqrt(1.0 + px * px + py * py + pz * pz) + 0.5 * A_COEFF * xn * xn)


def invariant_y(y: float, py: float, pz: float) -> float:
    return float(py * py + pz * pz)


def section_points(times: np.ndarray, data: dict[str, np.ndarray]) -> list[dict[str, float]]:
    points: list[dict[str, float]] = []
    for index in range(len(times) - 1):
        x0, x1 = data["x"][index] / L0, data["x"][index + 1] / L0
        if not (x0 < 0.0 <= x1 and x1 != x0):
            continue
        alpha = -x0 / (x1 - x0)
        if alpha <= 1.0e-8 or alpha > 1.0:
            continue
        y = data["y"][index] + alpha * (data["y"][index + 1] - data["y"][index])
        px = data["px"][index] + alpha * (data["px"][index + 1] - data["px"][index])
        py = data["py"][index] + alpha * (data["py"][index + 1] - data["py"][index])
        pz = data["pz"][index] + alpha * (data["pz"][index + 1] - data["pz"][index])
        if px <= 0.0:
            continue
        points.append(
            {
                "time": float(times[index] + alpha * (times[index + 1] - times[index])),
                "y_over_L0": float(y / L0),
                "py": float(py),
                "pz": float(pz),
                "px": float(px),
                "H": hamiltonian(0.0, y, px, py, pz),
                "I_y": invariant_y(y, py, pz),
            }
        )
    return points


def summarize_points(points: list[dict[str, float]]) -> dict:
    if not points:
        return {"crossing_count": 0, "invariant_ledger": {}, "section_span": {}}
    h = np.asarray([point["H"] for point in points])
    iy = np.asarray([point["I_y"] for point in points])
    y = np.asarray([point["y_over_L0"] for point in points])
    py = np.asarray([point["py"] for point in points])
    return {
        "crossing_count": len(points),
        "invariant_ledger": {
            "H_initial": float(h[0]),
            "H_relative_drift_max": float(np.max(np.abs((h - h[0]) / h[0]))),
            "I_y_initial": float(iy[0]),
            "I_y_relative_drift_max": float(np.max(np.abs((iy - iy[0]) / max(abs(iy[0]), 1.0e-30)))),
        },
        "section_span": {
            "y_over_L0_min": float(y.min()),
            "y_over_L0_max": float(y.max()),
            "py_min": float(py.min()),
            "py_max": float(py.max()),
        },
        "points": points,
    }


def collect_case(arguments: tuple[Path, tuple[str, ...]]) -> dict:
    run_dir, expected_species = arguments
    run_dir = run_dir.resolve()
    times, trajectories = load_trajectories(run_dir, expected_species)
    species = {name: summarize_points(section_points(times, data)) for name, data in trajectories.items()}
    return {"run_dir": str(run_dir), "pusher": run_dir.name.rsplit("_", 1)[-1], "frame_count": len(times), "species": species}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dirs", nargs=3, type=Path)
    parser.add_argument("--species", nargs="+", default=list(EXPECTED_SPECIES))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    expected_species = tuple(args.species)
    with ProcessPoolExecutor(max_workers=3) as executor:
        cases = list(executor.map(collect_case, [(run_dir, expected_species) for run_dir in args.run_dirs]))

    checks = {
        "three_cases_present": len(cases) == 3,
        "all_expected_species_present": all(set(case["species"]) == set(expected_species) for case in cases),
        "all_species_have_sections": all(
            summary["crossing_count"] > 0 for case in cases for summary in case["species"].values()
        ),
    }
    result = {
        "contract": "Higuera-Cary Poincare section and invariant ledger",
        "passed": all(checks.values()),
        "checks": checks,
        "normalization": {
            "L0_m": L0,
            "a": A_COEFF,
            "b": B_COEFF,
            "dt_normalized": 0.1,
            "section": "x=0 with positive p_x",
            "runtime_charge_field_mapping": "charge=-q_e with E_x and B_x signs reversed; paper canonical P_z-A_z is evaluated from WarpX mechanical p_z",
        },
        "cases": cases,
        "evidence_boundary": {
            "paper_reproduction_promoted": False,
            "section_consumer_present": True,
            "resonance_island_classifier_present": False,
            "remaining": "This contract establishes the section and invariant ledger. It does not yet classify nested surfaces, crossings, or the two-fold resonance island against the paper's Fig. 2 by an automated topology gate.",
        },
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Higuera-Cary Poincare contract",
        "",
        "Section: `x=0` with positive `p_x`; the electron runtime reverses `E_x` and `B_x` together so its `qE/qB` matches the normalized paper construction `E_x=-a x`, `B_x=b y` with `a=1`, `b=2`. WarpX mechanical `p_z` is used for the paper's `P_z-A_z` term.",
        "",
        "| check | status |",
        "|---|:---:|",
    ]
    lines.extend(f"| `{name}` | `{'PASS' if passed else 'FAIL'}` |" for name, passed in checks.items())
    lines += ["", "| pusher | species | crossings | max H drift | max I_y drift |", "|---|---|---:|---:|---:|"]
    for case in cases:
        for species, summary in case["species"].items():
            ledger = summary.get("invariant_ledger", {})
            lines.append(
                f"| `{case['pusher']}` | `{species}` | `{summary['crossing_count']}` | `{ledger.get('H_relative_drift_max', float('nan')):.8e}` | `{ledger.get('I_y_relative_drift_max', float('nan')):.8e}` |"
            )
    lines += ["", "The section/invariant ledger is established, but no automated resonance-island or trajectory-crossing topology gate is claimed."]
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
