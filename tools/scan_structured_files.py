import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_EXTENSIONS = (".json", ".jsonl", ".ndjson", ".yaml", ".yml", ".toml", ".xml")
DEFAULT_EXCLUDES = {
    ".git",
    ".checkpoints",
    ".claude",
    ".grind_cache",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
}


@dataclass
class ScanResult:
    path: str
    error_type: str
    detail: str


def _iter_files(root: Path, extensions: Sequence[str], exclude_dirs: Iterable[str]) -> Iterable[Path]:
    exclude_set = set(exclude_dirs)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude_set]
        for filename in filenames:
            if filename.lower().endswith(tuple(extensions)):
                yield Path(dirpath) / filename


def _decode_text(raw: bytes) -> Tuple[Optional[str], Optional[str]]:
    if not raw:
        return None, "empty_file"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, f"utf8_decode_error: {exc}"
    if "\x00" in text:
        return None, "null_byte_found"
    return text, None


def _scan_json_file(path: Path) -> Optional[ScanResult]:
    raw = path.read_bytes()
    text, decode_error = _decode_text(raw)
    if decode_error:
        return ScanResult(str(path), "decode_error", decode_error)
    if text is None:
        return ScanResult(str(path), "decode_error", "unknown_decode_failure")
    try:
        json.loads(text)
    except json.JSONDecodeError as exc:
        detail = f"json_decode_error: line {exc.lineno}, col {exc.colno} ({exc.msg})"
        return ScanResult(str(path), "json_decode_error", detail)
    return None


def _scan_jsonl_file(path: Path) -> Optional[ScanResult]:
    raw = path.read_bytes()
    text, decode_error = _decode_text(raw)
    if decode_error:
        return ScanResult(str(path), "decode_error", decode_error)
    if text is None:
        return ScanResult(str(path), "decode_error", "unknown_decode_failure")
    for idx, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            json.loads(stripped)
        except json.JSONDecodeError as exc:
            detail = f"jsonl_decode_error: line {idx} ({exc.msg})"
            return ScanResult(str(path), "jsonl_decode_error", detail)
    return None


def _scan_yaml_file(path: Path) -> Optional[ScanResult]:
    try:
        import yaml  # type: ignore
    except Exception:
        return ScanResult(str(path), "yaml_parser_missing", "PyYAML not available")
    raw = path.read_bytes()
    text, decode_error = _decode_text(raw)
    if decode_error:
        return ScanResult(str(path), "decode_error", decode_error)
    if text is None:
        return ScanResult(str(path), "decode_error", "unknown_decode_failure")
    try:
        yaml.safe_load(text)
    except Exception as exc:
        return ScanResult(str(path), "yaml_decode_error", f"yaml_error: {exc}")
    return None


def _scan_toml_file(path: Path) -> Optional[ScanResult]:
    toml_loader = None
    try:
        import tomllib  # type: ignore
        toml_loader = tomllib.loads
    except Exception:
        try:
            import tomli  # type: ignore
            toml_loader = tomli.loads
        except Exception:
            return ScanResult(str(path), "toml_parser_missing", "tomllib/tomli not available")
    raw = path.read_bytes()
    text, decode_error = _decode_text(raw)
    if decode_error:
        return ScanResult(str(path), "decode_error", decode_error)
    if text is None:
        return ScanResult(str(path), "decode_error", "unknown_decode_failure")
    try:
        toml_loader(text)
    except Exception as exc:
        return ScanResult(str(path), "toml_decode_error", f"toml_error: {exc}")
    return None


def _scan_xml_file(path: Path) -> Optional[ScanResult]:
    raw = path.read_bytes()
    text, decode_error = _decode_text(raw)
    if decode_error:
        return ScanResult(str(path), "decode_error", decode_error)
    if text is None:
        return ScanResult(str(path), "decode_error", "unknown_decode_failure")
    try:
        import xml.etree.ElementTree as ET

        ET.fromstring(text)
    except Exception as exc:
        return ScanResult(str(path), "xml_decode_error", f"xml_error: {exc}")
    return None


def scan_paths(
    root: Path,
    extensions: Sequence[str],
    exclude_dirs: Sequence[str],
) -> List[ScanResult]:
    results: List[ScanResult] = []
    for path in _iter_files(root, extensions, exclude_dirs):
        suffix = path.suffix.lower()
        if suffix == ".json":
            result = _scan_json_file(path)
        elif suffix in {".jsonl", ".ndjson"}:
            result = _scan_jsonl_file(path)
        elif suffix in {".yaml", ".yml"}:
            result = _scan_yaml_file(path)
        elif suffix == ".toml":
            result = _scan_toml_file(path)
        elif suffix == ".xml":
            result = _scan_xml_file(path)
        else:
            result = None
        if result:
            results.append(result)
    return results


def _summarize(results: Sequence[ScanResult]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for result in results:
        counts[result.error_type] = counts.get(result.error_type, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _format_markdown(results: Sequence[ScanResult]) -> str:
    summary = _summarize(results)
    lines = ["# Structured File Scan Report", "", "## Summary"]
    if not summary:
        lines.append("- No corrupted files detected.")
    else:
        for error_type, count in summary.items():
            lines.append(f"- {error_type}: {count}")
    lines.extend(["", "## Findings"])
    if not results:
        lines.append("- None")
    else:
        for result in results:
            lines.append(f"- `{result.path}` — {result.detail}")
    return "\n".join(lines) + "\n"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan for corrupted structured files.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root to scan",
    )
    parser.add_argument(
        "--extensions",
        default=",".join(DEFAULT_EXTENSIONS),
        help="Comma-separated list of extensions to scan",
    )
    parser.add_argument(
        "--exclude",
        default=",".join(sorted(DEFAULT_EXCLUDES)),
        help="Comma-separated list of directory names to skip",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output path for markdown report",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    root = Path(args.root).resolve()
    extensions = tuple(ext.strip().lower() for ext in args.extensions.split(",") if ext.strip())
    exclude_dirs = [entry.strip() for entry in args.exclude.split(",") if entry.strip()]

    results = scan_paths(root, extensions, exclude_dirs)
    report = _format_markdown(results)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
