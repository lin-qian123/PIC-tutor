#!/usr/bin/env python
"""Build a conservative triage report for literature-map entries still unclassified.

The report is an acquisition and reading queue. Keyword matches never upgrade a
paper to chapter evidence or imply that its full text has been read.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Entry:
    key: str
    title: str
    doi: str


RULES: tuple[tuple[str, tuple[str, ...], str, str, str], ...] = (
    ("QED / strong-field processes", ("qed", "breit", "wheeler", "synchrotron", "vacuum polarization"), "96-100", "P1", "metadata first; MinerU if a lawful PDF is acquired"),
    ("collisions / MCC / particle processes", ("collision", "scattering", "neutral", "capacitive discharge", "fusion", "secondary electron", "resampling", "stopping", "gas"), "90-92", "P1", "metadata first; MinerU if a lawful PDF is acquired"),
    ("particle-mesh / deposition", ("particle-mesh", "particle mesh", "spline", "weighting", "force law", "charge and current", "shape function"), "5-6", "P1", "MinerU if a lawful PDF is acquired"),
    ("field solver / Maxwell / divergence", ("maxwell", "finite-difference", "finite difference", "spectral", "pstd", "fdtd", "divergence", "wave equation", "numerical dispersion"), "6-7", "P1", "MinerU if a lawful PDF is acquired"),
    ("AMR / HPC / performance", ("amr", "mesh refinement", "exascale", "gpu", "load balancing", "parallel", "quasi-static"), "7-9", "P1", "metadata first; MinerU if a lawful PDF is acquired"),
    ("embedded boundary / boundary physics", ("embedded", "absorbing layer", "boundary", "multipactor", "surface"), "7", "P2", "metadata first; MinerU if a lawful PDF is acquired"),
    ("accelerator / beam dynamics", ("accelerator", "beam", "wakefield", "betatron", "quadrupole", "bhabha", "collider", "free electron laser", "fel"), "3A, 7-9", "P1", "metadata first; MinerU if a lawful PDF is acquired"),
    ("laser / plasma acceleration", ("laser", "plasma wave", "plasma-based", "self-injection", "ion acceleration"), "3A, 9", "P1", "MinerU if a lawful PDF is acquired"),
    ("numerical methods / discretization", ("upwind", "shock-capturing", "difference methods", "implicit algorithm", "variational algorithm", "numerical methods"), "2, 6", "P2", "metadata first; MinerU if a lawful PDF is acquired"),
)


def parse_entries(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `") or "| 待分类 |" not in line:
            continue
        fields = [field.strip() for field in line.strip().strip("|").split("|")]
        if len(fields) < 7:
            continue
        key = fields[0].strip("`")
        title = fields[5]
        doi = fields[6]
        entries.append(Entry(key, title, doi))
    return entries


def classify(entry: Entry) -> tuple[str, str, str, str]:
    haystack = f"{entry.key} {entry.title}".lower()
    for topic, keywords, chapters, priority, action in RULES:
        if any(re.search(rf"(?<![a-z]){re.escape(keyword.lower())}(?![a-z])", haystack) for keyword in keywords):
            return topic, chapters, priority, action
    return "general acquisition / manual review", "1-9", "P3", "keep metadata only until a chapter need is identified"


def build_report(entries: list[Entry]) -> str:
    lines = [
        "# Literature pending triage",
        "",
        "This is an acquisition and reading queue for entries still marked `待分类` in `docs/literature-map.md`.",
        "Keyword-derived topics and chapter suggestions are planning metadata only; they do not prove that a paper was read, downloaded, converted by MinerU, or suitable as primary evidence.",
        "",
        f"- pending entries: **{len(entries)}**",
        "- classification: conservative title/key triage",
        "- P1: likely useful for the current book's core algorithm or application routes",
        "- P2: useful for a later chapter or a narrower source comparison",
        "- P3: retain metadata until a concrete chapter need appears",
        "",
        "| key | candidate topic | suggested chapters | priority | next action | title | DOI |",
        "|---|---|---|:---:|---|---|---|",
    ]
    for entry in entries:
        topic, chapters, priority, action = classify(entry)
        safe_title = entry.title.replace("|", "\\|")
        lines.append(f"| `{entry.key}` | {topic} | {chapters} | {priority} | {action} | {safe_title} | {entry.doi} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--literature-map", type=Path, default=Path("docs/literature-map.md"))
    parser.add_argument("--output", type=Path, default=Path("docs/literature-pending-triage.md"))
    args = parser.parse_args()
    entries = parse_entries(args.literature_map)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_report(entries), encoding="utf-8")
    print(f"PASS: generated triage for {len(entries)} pending literature entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
