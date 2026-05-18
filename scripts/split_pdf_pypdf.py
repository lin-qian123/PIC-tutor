#!/usr/bin/env python3
"""Split a PDF into fixed-size page chunks using pypdf."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split PDF into page chunks")
    parser.add_argument("filepath", help="Path to the source PDF")
    parser.add_argument(
        "--pages-per-part",
        "-n",
        type=int,
        default=200,
        help="Maximum pages per output PDF",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help="Directory for split PDFs; defaults to a sibling folder",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    src = Path(args.filepath).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(src)
    if args.pages_per_part <= 0:
        raise ValueError("--pages-per-part must be positive")

    reader = PdfReader(str(src))
    total_pages = len(reader.pages)
    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else src.parent / f"{src.stem}_split"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    for start in range(0, total_pages, args.pages_per_part):
        end = min(start + args.pages_per_part, total_pages)
        writer = PdfWriter()
        for page_index in range(start, end):
            writer.add_page(reader.pages[page_index])
        out_path = output_dir / f"{src.stem}_p{start+1:04d}-{end:04d}.pdf"
        with out_path.open("wb") as fh:
            writer.write(fh)
        print(out_path)


if __name__ == "__main__":
    main()
