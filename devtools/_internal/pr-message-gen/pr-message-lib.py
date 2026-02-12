#!/usr/bin/env python3
"""
pr-message-lib.py — Build PR description from branch-status, ci-status, repo-map outputs.
Reads file paths from argv, outputs formatted Markdown to stdout.
"""

import re
import sys
from pathlib import Path


def read_file(path: str) -> str:
    """Read file or return empty string."""
    if not path or path == "/dev/null":
        return ""
    try:
        f = Path(path)
        if f.exists():
            return f.read_text(errors="replace")
    except OSError:
        pass
    return ""


def parse_branch_status(content: str) -> dict:
    """Extract branch, base, commits, diff stat from branch-status markdown."""
    out = {
        "branch": "",
        "base": "",
        "commits_ahead": "",
        "pr_status": "",
        "commits": [],
        "diff_stat": "",
    }
    if not content:
        return out

    for line in content.split("\n"):
        s = line.strip()
        if s.startswith("- **Branch:**"):
            out["branch"] = s.replace("- **Branch:**", "").strip()
        elif s.startswith("- **Base:**"):
            out["base"] = s.replace("- **Base:**", "").strip()
        elif s.startswith("- **Commits ahead:**"):
            out["commits_ahead"] = s.replace("- **Commits ahead:**", "").strip()
        elif s.startswith("- **PR:**"):
            out["pr_status"] = s.replace("- **PR:**", "").strip()

    # Commits table: | hash | subject |
    in_table = False
    for line in content.split("\n"):
        if "| Hash | Subject |" in line or "|------|---------|" in line:
            in_table = True
            continue
        if in_table and line.strip().startswith("|") and "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                out["commits"].append({"hash": parts[0], "subject": parts[1]})
        elif in_table and line.strip() == "":
            in_table = False

    # Diff stat (between ```)
    in_code = False
    code_lines = []
    for line in content.split("\n"):
        if "```" in line:
            if in_code:
                out["diff_stat"] = "\n".join(code_lines)
                break
            in_code = True
            code_lines = []
            continue
        if in_code:
            code_lines.append(line)

    return out


def parse_ci_status(content: str) -> dict:
    """Extract summary, passing/failed counts, run URLs from ci-status markdown."""
    out = {
        "branch": "",
        "passing": "",
        "failed": "",
        "pending": "",
        "failed_details": [],
        "latest_run_url": "",
    }
    if not content:
        return out

    for line in content.split("\n"):
        s = line.strip()
        if s.startswith("- **Branch:**"):
            out["branch"] = s.replace("- **Branch:**", "").strip()
        elif s.startswith("- **Passing:**"):
            out["passing"] = s.replace("- **Passing:**", "").strip()
        elif s.startswith("- **Failed:**"):
            out["failed"] = s.replace("- **Failed:**", "").strip()
        elif s.startswith("- **Pending:**"):
            out["pending"] = s.replace("- **Pending:**", "").strip()
        elif s.startswith("- **URL:**"):
            url = s.replace("- **URL:**", "").strip()
            if url.startswith("http"):
                out["failed_details"].append({"url": url})
                if not out["latest_run_url"]:
                    out["latest_run_url"] = url

    # Get first URL from any failed section
    for line in content.split("\n"):
        if "- **URL:**" in line:
            m = re.search(r"https://[^\s\)]+", line)
            if m and not out["latest_run_url"]:
                out["latest_run_url"] = m.group(0)
            break

    return out


def parse_repo_map(content: str) -> dict:
    """Extract manifest, file tree summary from repo-map."""
    out = {"manifest": "", "modules": [], "file_tree_lines": []}
    if not content:
        return out

    # Manifest JSON
    in_manifest = False
    for line in content.split("\n"):
        if "```json" in line:
            in_manifest = True
            continue
        if in_manifest:
            if "```" in line:
                break
            out["manifest"] = line.strip()

    # Modules section
    in_modules = False
    for line in content.split("\n"):
        if "### Modules" in line and "Code Structure" in content.split("### Modules")[0]:
            in_modules = True
            continue
        if in_modules and "```" in line:
            break
        if in_modules and line.strip():
            out["modules"].append(line.strip())

    return out


def infer_affected_areas(diff_stat: str, branch_status: dict) -> list[str]:
    """Infer affected areas from diff stat (file paths)."""
    areas = set()
    lines = diff_stat.split("\n") if diff_stat else []
    skip = re.compile(r"^\d+ files? changed|^\.\.\.$|^[-\d]+ insertions?|^[-\d]+ deletions?")
    for line in lines:
        # Diff stat format: " path/to/file | 10 +-"
        if "|" in line:
            path = line.split("|")[0].strip()
        else:
            path = line.strip()
        if not path or path.startswith("---"):
            continue
        if skip.search(path):
            continue
        parts = path.split("/")
        if parts:
            top = parts[0]
            if not top or top[0].isdigit():
                continue
            if "." in top and "/" not in path:
                continue  # Skip bare filenames like api_audit.log
            areas.add(top)
            if len(parts) >= 2 and top in ("vivarium", "src"):
                areas.add(f"{top}/{parts[1]}")

    return sorted(areas)


def find_related_issues(commits: list, branch_name: str) -> list[str]:
    """Find issue refs like #123 in commit subjects."""
    refs = set()
    for c in commits:
        subj = c.get("subject", "")
        for m in re.finditer(r"#(\d+)", subj):
            refs.add(m.group(0))
    # Branch name sometimes has issue number
    for m in re.finditer(r"(\d{2,})", branch_name):
        refs.add("#" + m.group(1))
    return sorted(refs, key=lambda x: int(re.search(r"\d+", x).group()))


def build_pr_markdown(
    branch_status: dict,
    ci_status: dict,
    repo_map: dict,
    related_issues: list,
) -> str:
    """Build full PR description in Markdown."""
    lines = []
    branch = branch_status.get("branch", "unknown")
    base = branch_status.get("base", "")

    lines.append(f"# PR: {branch}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    commits = branch_status.get("commits", [])
    if commits:
        lines.append("### Commits")
        lines.append("")
        for c in commits:
            subj = c.get("subject", "")
            h = c.get("hash", "")
            lines.append(f"- `{h}` {subj}")
        lines.append("")

    # Affected areas
    diff_stat = branch_status.get("diff_stat", "")
    areas = infer_affected_areas(diff_stat, branch_status)
    if areas:
        lines.append("### Affected Areas")
        lines.append("")
        for a in areas:
            lines.append(f"- `{a}`")
        lines.append("")

    # CI Status
    lines.append("## CI Status")
    lines.append("")
    ci_url = ci_status.get("latest_run_url", "")
    if ci_url:
        lines.append(f"Latest run: {ci_url}")
        lines.append("")
    if ci_status.get("passing"):
        lines.append(f"- **Passing:** {ci_status['passing']}")
    if ci_status.get("failed"):
        lines.append(f"- **Failed:** {ci_status['failed']}")
    if ci_status.get("pending"):
        lines.append(f"- **Pending:** {ci_status['pending']}")
    if not ci_status.get("passing") and not ci_status.get("failed"):
        lines.append("*No CI data available. Run `./devtools/ci-status.sh` for details.*")
    lines.append("")

    # Testing checklist
    lines.append("## Testing")
    lines.append("")
    lines.append("- [ ] Unit tests pass")
    lines.append("- [ ] Integration tests pass")
    lines.append("- [ ] Manual smoke test (if applicable)")
    lines.append("")

    # Related issues
    if related_issues:
        lines.append("## Related Issues")
        lines.append("")
        for ref in related_issues:
            lines.append(f"- {ref}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Read paths from argv: branch_status_path, ci_status_path, repo_map_path [, gh_issues]."""
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: pr-message-lib.py <branch_status.md> <ci_status.md> <repo_map.md> [gh_issues]\n")
        sys.exit(1)

    branch_path = sys.argv[1]
    ci_path = sys.argv[2]
    repo_map_path = sys.argv[3]
    gh_issues_arg = sys.argv[4] if len(sys.argv) > 4 else ""

    branch_content = read_file(branch_path)
    ci_content = read_file(ci_path)
    repo_map_content = read_file(repo_map_path)

    branch_status = parse_branch_status(branch_content)
    ci_status = parse_ci_status(ci_content)
    repo_map = parse_repo_map(repo_map_content)

    related_issues = find_related_issues(branch_status.get("commits", []), branch_status.get("branch", ""))

    # Merge with gh issue list results (comma-separated #123,#456)
    seen = {r for r in related_issues}
    if gh_issues_arg:
        for ref in gh_issues_arg.split(","):
            ref = ref.strip()
            if ref.startswith("#") and ref not in seen:
                related_issues.append(ref)
                seen.add(ref)

    md = build_pr_markdown(branch_status, ci_status, repo_map, related_issues)
    print(md)


if __name__ == "__main__":
    main()
