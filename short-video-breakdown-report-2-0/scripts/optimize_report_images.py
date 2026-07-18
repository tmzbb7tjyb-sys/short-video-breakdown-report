#!/usr/bin/env python3
"""Create a PDF-friendly HTML source with optimized embedded report images.

This keeps report text as real PDF text by optimizing only local <img> assets.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image


SRC_RE = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")', re.IGNORECASE)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def optimized_name(src: str) -> str:
    path = Path(src)
    return f"{path.stem}.jpg"


def optimize_image(source: Path, target: Path, max_width: int, max_height: int, quality: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(source).convert("RGB")
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    image.save(target, "JPEG", quality=quality, optimize=True, progressive=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize local report images while preserving PDF text.")
    parser.add_argument("input_html", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument("--asset-dir", default="report_pdf_images", help="relative output folder for optimized images")
    parser.add_argument("--max-width", type=int, default=360)
    parser.add_argument("--max-height", type=int, default=640)
    parser.add_argument("--quality", type=int, default=78)
    args = parser.parse_args()

    html = args.input_html.read_text(encoding="utf-8")
    root = args.input_html.parent
    asset_dir = Path(args.asset_dir)
    converted: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        prefix, src, suffix = match.groups()
        if src.startswith(("http://", "https://", "data:")):
            return match.group(0)
        source = (root / src).resolve()
        if not source.exists() or source.suffix.lower() not in IMAGE_EXTS:
            return match.group(0)
        new_src = str(asset_dir / optimized_name(src))
        target = root / new_src
        if src not in converted:
            optimize_image(source, target, args.max_width, args.max_height, args.quality)
            converted[src] = new_src
        return f"{prefix}{converted[src]}{suffix}"

    output = SRC_RE.sub(replace, html)
    args.output_html.write_text(output, encoding="utf-8")

    original_bytes = sum(((root / src).stat().st_size for src in converted), 0)
    optimized_bytes = sum(((root / new_src).stat().st_size for new_src in converted.values()), 0)
    print(
        f"optimized_images={len(converted)} "
        f"original_bytes={original_bytes} optimized_bytes={optimized_bytes} "
        f"output_html={args.output_html}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
