import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence


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


def _load_yaml_module():
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    return yaml


def _make_unique_key_loader(yaml_module):
    class UniqueKeyLoader(yaml_module.SafeLoader):
        def construct_mapping(self, node, deep=False):
            mapping = {}
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                if key in mapping:
                    raise ValueError(f"duplicate key: {key}")
                mapping[key] = self.construct_object(value_node, deep=deep)
            return mapping

    return UniqueKeyLoader


def _validate_workflow_doc(doc, path: Path) -> List[ScanResult]:
    results: List[ScanResult] = []
    if not isinstance(doc, dict):
        results.append(
            ScanResult(str(path), "workflow_not_mapping", "Top-level YAML must be a mapping.")
        )
        return results

    if "on" not in doc:
        results.append(ScanResult(str(path), "workflow_missing_on", "Missing required `on` key."))
    else:
        on_value = doc.get("on")
        if not isinstance(on_value, (dict, list, str)):
            results.append(
                ScanResult(
                    str(path),
                    "workflow_invalid_on",
                    "`on` must be mapping, list, or string.",
                )
            )

    jobs = doc.get("jobs")
    if jobs is None:
        results.append(ScanResult(str(path), "workflow_missing_jobs", "Missing `jobs` section."))
        return results

    if not isinstance(jobs, dict) or not jobs:
        results.append(
            ScanResult(str(path), "workflow_invalid_jobs", "`jobs` must be a non-empty mapping.")
        )
        return results

    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            results.append(
                ScanResult(str(path), "job_not_mapping", f"Job `{job_name}` must be mapping.")
            )
            continue

        has_runs_on = "runs-on" in job
        has_uses = "uses" in job
        if not has_runs_on and not has_uses:
            results.append(
                ScanResult(
                    str(path),
                    "job_missing_executor",
                    f"Job `{job_name}` missing `runs-on` or `uses`.",
                )
            )

        steps = job.get("steps")
        if has_runs_on and steps is None:
            results.append(
                ScanResult(
                    str(path),
                    "job_missing_steps",
                    f"Job `{job_name}` missing `steps`.",
                )
            )
            continue

        if steps is not None:
            if not isinstance(steps, list):
                results.append(
                    ScanResult(
                        str(path),
                        "job_steps_not_list",
                        f"Job `{job_name}` `steps` must be a list.",
                    )
                )
                continue

            for idx, step in enumerate(steps, start=1):
                if not isinstance(step, dict):
                    results.append(
                        ScanResult(
                            str(path),
                            "step_not_mapping",
                            f"Job `{job_name}` step {idx} must be a mapping.",
                        )
                    )
                    continue
                if "run" not in step and "uses" not in step:
                    results.append(
                        ScanResult(
                            str(path),
                            "step_missing_action",
                            f"Job `{job_name}` step {idx} missing `run` or `uses`.",
                        )
                    )

    return results


def scan_workflows(
    root: Path,
    extensions: Sequence[str],
    exclude_dirs: Sequence[str],
) -> List[ScanResult]:
    results: List[ScanResult] = []
    yaml_module = _load_yaml_module()
    if yaml_module is None:
        results.append(
            ScanResult(str(root), "yaml_parser_missing", "PyYAML not available.")
        )
        return results

    loader = _make_unique_key_loader(yaml_module)

    for path in _iter_files(root, extensions, exclude_dirs):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "\x00" in text:
            results.append(ScanResult(str(path), "null_byte_found", "Null byte detected."))
            continue

        try:
            docs = list(yaml_module.load_all(text, Loader=loader))
        except Exception as exc:
            results.append(ScanResult(str(path), "yaml_parse_error", f"yaml_error: {exc}"))
            continue

        if len(docs) != 1:
            results.append(
                ScanResult(
                    str(path),
                    "workflow_multi_document",
                    f"Workflow must be single document, found {len(docs)}.",
                )
            )
            continue

        results.extend(_validate_workflow_doc(docs[0], path))

    return results


def _summarize(results: Sequence[ScanResult]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for result in results:
        counts[result.error_type] = counts.get(result.error_type, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _format_markdown(results: Sequence[ScanResult], root: Path) -> str:
    summary = _summarize(results)
    lines = ["# Workflow Semantic Scan Report", "", f"Root: `{root}`", "", "## Summary"]
    if not summary:
        lines.append("- No semantic issues detected.")
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
    parser = argparse.ArgumentParser(description="Scan GitHub workflow YAML for semantic issues.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1] / ".github" / "workflows"),
        help="Workflows directory to scan",
    )
    parser.add_argument(
        "--extensions",
        default=".yml,.yaml",
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

    results = scan_workflows(root, extensions, exclude_dirs)
    report = _format_markdown(results, root)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
