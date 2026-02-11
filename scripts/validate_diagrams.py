#!/usr/bin/env python3
"""Validate diagram source and exported SVG assets."""

from __future__ import annotations

from pathlib import Path
import sys
import xml.etree.ElementTree as ET


REQUIRED_BASE_NAMES = (
    "system-design",
    "quest-lifecycle",
    "task-review-state-machine",
)


def parse_xml(path: Path) -> None:
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        raise RuntimeError(f"XML parse error in {path}: {exc}") from exc


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    src_dir = repo_root / "docs" / "assets" / "diagrams" / "src"
    out_dir = repo_root / "docs" / "assets" / "diagrams"

    failures: list[str] = []

    for base in REQUIRED_BASE_NAMES:
        drawio_path = src_dir / f"{base}.drawio"
        svg_path = out_dir / f"{base}.svg"

        if not drawio_path.exists():
            failures.append(f"Missing source file: {drawio_path}")
        else:
            try:
                parse_xml(drawio_path)
            except RuntimeError as exc:
                failures.append(str(exc))

        if not svg_path.exists():
            failures.append(f"Missing SVG artifact: {svg_path}")
        else:
            try:
                parse_xml(svg_path)
            except RuntimeError as exc:
                failures.append(str(exc))

    if failures:
        for failure in failures:
            print(f"[diagram-validate] {failure}", file=sys.stderr)
        return 1

    print("[diagram-validate] OK: all draw.io source and SVG files exist and parse as XML.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
