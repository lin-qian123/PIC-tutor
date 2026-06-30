#!/usr/bin/env python
"""Regenerate the first-stage comoving patch draft assets from a reference ledger.

The generated assets stay in PIC-tutor on purpose. They are staging artifacts
for a future WarpX proposal, not an upstream patch applied in-place.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER_JSON = (
    ROOT
    / "runs"
    / "fieldsolver-validation"
    / "comoving-reference-ledgers"
    / "comoving-stable-vs-no-comoving.json"
)
DEFAULT_HELPER_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "analysis_comoving_first_stage_draft.py"
)
DEFAULT_DIFF_PATH = (
    ROOT
    / "notes"
    / "code-reading"
    / "fieldsolver"
    / "comoving_first_stage_patch.diff"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the first-stage comoving helper draft and unified diff from a ledger."
    )
    parser.add_argument(
        "--ledger-json",
        type=Path,
        default=DEFAULT_LEDGER_JSON,
        help="Reference ledger JSON with derived_contract_observations.",
    )
    parser.add_argument(
        "--safety-factor",
        type=float,
        default=1.001,
        help="Multiplier applied to spike_ratio_ref_stable. Default: 1.001",
    )
    parser.add_argument(
        "--helper-output",
        type=Path,
        default=DEFAULT_HELPER_PATH,
        help="Output path for the first-stage analysis helper draft.",
    )
    parser.add_argument(
        "--diff-output",
        type=Path,
        default=DEFAULT_DIFF_PATH,
        help="Output path for the unified diff draft.",
    )
    return parser.parse_args()


def load_ledger(path: Path) -> tuple[float, float]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    derived = payload.get("derived_contract_observations") or {}
    spike_ratio_ref_stable = derived.get("spike_ratio_ref_stable")
    if spike_ratio_ref_stable is None:
        raise KeyError(
            f"{path} is missing derived_contract_observations.spike_ratio_ref_stable"
        )
    return float(spike_ratio_ref_stable), float(payload["stable_metrics"]["spike_ratio"])


def render_helper(spike_ratio_ref_stable: float, safety_factor: float) -> str:
    spike_ratio_max = spike_ratio_ref_stable * safety_factor
    return f"""#!/usr/bin/env python
\"\"\"
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
\"\"\"

import sys

import numpy as np
import yt

yt.funcs.mylog.setLevel(0)


FIELD_NAMES = ("Ex", "Ey", "Ez", "Bx", "By", "Bz", "jx", "jy", "jz", "rho")

# Candidate first-stage ceiling derived from the current stable baseline:
# spike_ratio_ref_stable = {spike_ratio_ref_stable:.16f}
# safety_factor = {safety_factor}
SPIKE_RATIO_MAX = {spike_ratio_max:.16f}


def main() -> None:
    filename = sys.argv[1]
    ds = yt.load(filename)

    if hasattr(ds, "force_periodicity"):
        ds.force_periodicity()

    grid = ds.covering_grid(
        level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions
    )

    fields = {{}}
    for name in FIELD_NAMES:
        arr = grid["boxlib", name].squeeze().v
        if not np.all(np.isfinite(arr)):
            raise AssertionError(f"{{name}} contains non-finite values")
        fields[name] = arr

    ex = fields["Ex"]
    ey = fields["Ey"]
    ez = fields["Ez"]
    e_mag = np.sqrt(ex**2 + ey**2 + ez**2)
    spike_ratio = np.max(e_mag) / (np.percentile(e_mag, 99) + 1e-300)

    print("\\nCheck finite-field sanity:")
    print("all_fields_finite = True")

    print("\\nCheck spike-ratio sanity:")
    print(f"spike_ratio = {{spike_ratio}}")
    print(f"spike_ratio_max = {{SPIKE_RATIO_MAX}}")
    assert spike_ratio <= SPIKE_RATIO_MAX


if __name__ == "__main__":
    main()
"""


def render_diff(helper_text: str) -> str:
    helper_lines = helper_text.rstrip("\n").splitlines()
    diff_lines = [
        "diff --git a/Examples/Tests/nci_psatd_stability/CMakeLists.txt b/Examples/Tests/nci_psatd_stability/CMakeLists.txt",
        "index 0000000..0000000 100644",
        "--- a/Examples/Tests/nci_psatd_stability/CMakeLists.txt",
        "+++ b/Examples/Tests/nci_psatd_stability/CMakeLists.txt",
        "@@",
        " if(WarpX_FFT)",
        "     add_warpx_test(",
        "         test_2d_comoving_psatd_hybrid  # name",
        "         2  # dims",
        "         2  # nprocs",
        "         inputs_test_2d_comoving_psatd_hybrid  # inputs",
        "-        OFF  # analysis",
        '+        "analysis_comoving.py diags/diag1000400"  # analysis',
        '         "analysis_default_regression.py --path diags/diag1000400"  # checksum',
        "         OFF  # dependency",
        "     )",
        " endif()",
        "diff --git a/Examples/Tests/nci_psatd_stability/analysis_comoving.py b/Examples/Tests/nci_psatd_stability/analysis_comoving.py",
        "new file mode 100755",
        "index 0000000..0000000",
        "--- /dev/null",
        "+++ b/Examples/Tests/nci_psatd_stability/analysis_comoving.py",
        "@@",
    ]
    diff_lines.extend(f"+{line}" for line in helper_lines)
    return "\n".join(diff_lines) + "\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def main() -> None:
    args = parse_args()
    spike_ratio_ref_stable, stable_spike_ratio = load_ledger(args.ledger_json.resolve())
    if abs(spike_ratio_ref_stable - stable_spike_ratio) > 1e-12:
        raise ValueError(
            "spike_ratio_ref_stable does not match stable_metrics.spike_ratio in ledger"
        )

    helper_text = render_helper(spike_ratio_ref_stable, args.safety_factor)
    diff_text = render_diff(helper_text)
    write_text(args.helper_output.resolve(), helper_text)
    write_text(args.diff_output.resolve(), diff_text)


if __name__ == "__main__":
    main()
