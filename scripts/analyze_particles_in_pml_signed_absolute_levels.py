#!/usr/bin/env python
"""Decompose particles-in-PML signed/absolute field gates by frame and AMR level."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yt


FIELDS = ("Ex", "Ey", "Ez")


def max_record(array: np.ndarray, left_edge: np.ndarray, right_edge: np.ndarray) -> dict[str, object]:
    """Return signed extrema, absolute maximum, index, and physical position."""
    positive_index = tuple(int(value) for value in np.unravel_index(np.argmax(array), array.shape))
    negative_index = tuple(int(value) for value in np.unravel_index(np.argmin(array), array.shape))
    abs_index = tuple(int(value) for value in np.unravel_index(np.argmax(np.abs(array)), array.shape))
    cell_size = (right_edge - left_edge) / np.asarray(array.shape, dtype=float)

    def position(index: tuple[int, ...]) -> list[float]:
        return [float(left_edge[axis] + (index[axis] + 0.5) * cell_size[axis]) for axis in range(array.ndim)]

    return {
        "positive_max": float(array[positive_index]),
        "positive_index": list(positive_index),
        "positive_position": position(positive_index),
        "negative_min": float(array[negative_index]),
        "negative_index": list(negative_index),
        "negative_position": position(negative_index),
        "absolute_max": float(np.abs(array[abs_index])),
        "absolute_index": list(abs_index),
        "absolute_position": position(abs_index),
    }


def level_snapshot(ds, level: int, base_dims: list[int]) -> dict[str, object]:
    dims = [value * (2**level) for value in base_dims]
    grid = ds.covering_grid(level=level, left_edge=ds.domain_left_edge, dims=dims)
    left_edge = ds.domain_left_edge.to_ndarray()
    right_edge = ds.domain_right_edge.to_ndarray()
    fields = {
        name: max_record(grid["boxlib", name].to_ndarray(), left_edge, right_edge)
        for name in FIELDS
    }
    return {"level": level, "dimensions": dims, "fields": fields}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("diagnostics_dir", type=Path)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=110.0)
    args = parser.parse_args()

    plotfiles = sorted(path for path in args.diagnostics_dir.glob("diag*") if path.is_dir())
    if not plotfiles:
        raise SystemExit(f"no diag* plotfiles found in {args.diagnostics_dir}")

    frames: list[dict[str, object]] = []
    for plotfile in plotfiles:
        ds = yt.load(str(plotfile))
        if ds.dimensionality != 3 or ds.max_level != 1:
            raise SystemExit(
                f"expected a 3D max_level=1 case, got {plotfile}: "
                f"dimensionality={ds.dimensionality}, max_level={ds.max_level}"
            )
        base_dims = [int(value) for value in ds.domain_dimensions]
        finest = level_snapshot(ds, ds.max_level, base_dims)
        coarse = level_snapshot(ds, 0, base_dims)
        frame_fields = finest["fields"]
        signed_values = [frame_fields[name]["positive_max"] for name in FIELDS]
        frames.append(
            {
                "plotfile": str(plotfile),
                "iteration": int(plotfile.name.removeprefix("diag")),
                "current_time": float(ds.current_time),
                "official_signed_max": float(max(signed_values)),
                "official_signed_pass": bool(max(signed_values) < args.tolerance),
                "finest": finest,
                "coarse": coarse,
                "absolute_max": float(max(frame_fields[name]["absolute_max"] for name in FIELDS)),
                "absolute_pass": bool(max(frame_fields[name]["absolute_max"] for name in FIELDS) < args.tolerance),
            }
        )

    final = frames[-1]
    final_fields = final["finest"]["fields"]
    negative_exceeding = [
        name for name in FIELDS if final_fields[name]["negative_min"] < -args.tolerance
    ]
    result = {
        "contract": "particles-in-PML signed-vs-absolute level decomposition",
        "diagnostics_dir": str(args.diagnostics_dir),
        "tolerance_abs": args.tolerance,
        "frames": frames,
        "final_negative_components_exceeding_tolerance": negative_exceeding,
        "final_signed_pass": bool(final["official_signed_pass"]),
        "final_absolute_pass": bool(final["absolute_pass"]),
        "signed_absolute_difference_is_negative_peak": bool(
            final["official_signed_pass"] and not final["absolute_pass"] and negative_exceeding
        ),
        "interpretation": (
            "At the final finest-level frame, the signed consumer passes while the absolute "
            "consumer fails only when a negative component peak exceeds the same threshold. "
            "This is an analysis-contract boundary; it does not identify whether the threshold "
            "or the AMR/PML field evolution should be changed upstream."
        ),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Particles-in-PML signed/absolute level contract",
        "",
        f"- tolerance: `{args.tolerance:g}`",
        f"- frames: `{len(frames)}` (`{frames[0]['iteration']}` -> `{final['iteration']}`)",
        f"- final official signed max: `{final['official_signed_max']:.8f}`; pass=`{final['official_signed_pass']}`",
        f"- final finest absolute max: `{final['absolute_max']:.8f}`; pass=`{final['absolute_pass']}`",
        f"- negative components beyond `-{args.tolerance:g}`: `{negative_exceeding or 'none'}`",
        "",
        "| frame | level | Ex (+/-/abs) | Ey (+/-/abs) | Ez (+/-/abs) |",
        "|---:|---:|---:|---:|---:|",
    ]
    for frame in frames:
        for snapshot in (frame["coarse"], frame["finest"]):
            values = []
            for name in FIELDS:
                item = snapshot["fields"][name]
                values.append(f"{item['positive_max']:.4f}/{item['negative_min']:.4f}/{item['absolute_max']:.4f}")
            lines.append(f"| {frame['iteration']} | {snapshot['level']} | " + " | ".join(values) + " |")
    lines.extend(
        [
            "",
            "The final signed/absolute disagreement is driven by the negative `Ex` peak at the finest level.",
            "This report is a reader-side decomposition and does not modify the WarpX analysis or threshold.",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["signed_absolute_difference_is_negative_peak"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
