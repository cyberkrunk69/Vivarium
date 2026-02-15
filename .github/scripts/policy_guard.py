#!/usr/bin/env python3
"""Repository hardening policy guard.

Runs in CI to prevent quiet weakening of governance and quality gates.
"""

from __future__ import annotations

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

POLICY_OWNER = os.environ.get("POLICY_OWNER", "cyberkrunk69").lower()
PROTECTED_BRANCHES = {"master", "main"}
MIN_RUNTIME_COVERAGE = 45
MIN_CONTROL_PANEL_COVERAGE = 50
REQUIRED_STATUS_CONTEXTS = {"policy", "tests", "integration", "lint"}
REQUIRED_BRANCH_RULE_TYPES = {
    "deletion",
    "non_fast_forward",
    "pull_request",
    "required_status_checks",
    "required_linear_history",
    "update",
}
REQUIRED_PR_TEMPLATE_HEADINGS = [
    "## Summary",
    "## Testing",
    "## Evidence",
    "## Security",
    "## Ownership & Risk",
]
RESTRICTED_PATH_PREFIXES = (
    ".github/workflows/",
    ".github/scripts/",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    "devtools/apply-branch-protection.sh",
)
NON_OWNER_SENSITIVE_PATH_PREFIXES = (
    "tests/",
    "pytest.ini",
    "requirements-dev.txt",
    "requirements.txt",
    "requirements-groq.txt",
    "pyproject.toml",
    "setup.cfg",
    ".flake8",
)
WORKFLOW_PATHS = (
    ".github/workflows/ci.yml",
    ".github/workflows/integration.yml",
    ".github/workflows/lint.yml",
    ".github/workflows/control-panel.yml",
    ".github/workflows/policy-guard.yml",
)
REQUIRED_WORKFLOW_SNIPPETS = {
    ".github/workflows/ci.yml": (
        'pytest -q -m "not integration and not e2e"',
        "--cov=vivarium.runtime",
        "Scout Smoke Tests",
    ),
    ".github/workflows/integration.yml": ('pytest -q -m "integration or e2e"',),
    ".github/workflows/lint.yml": (
        "Determine changed Python files",
        "Run Black (check mode) on changed files",
        "Run Flake8 on changed files",
        "Run MyPy on changed files",
    ),
}


@dataclass
class GuardResult:
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)

    def finish(self) -> int:
        for note in self.notes:
            print(f"INFO: {note}")
        if self.errors:
            print("\nPOLICY GUARD FAILED", file=sys.stderr)
            for err in self.errors:
                print(f" - {err}", file=sys.stderr)
            return 1
        print("POLICY GUARD PASSED")
        return 0


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def _load_event_payload() -> dict:
    path = _require_env("GITHUB_EVENT_PATH")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _api_get(path: str) -> dict | list:
    token = _require_env("GITHUB_TOKEN")
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {exc.code} for {path}: {body}") from exc


def _resolve_ref(event_name: str, payload: dict) -> str:
    if event_name in {"pull_request", "pull_request_target"}:
        return payload["pull_request"]["head"]["sha"]
    if event_name == "push":
        return payload.get("after") or _require_env("GITHUB_SHA")
    return _require_env("GITHUB_SHA")


def _fetch_file_at_ref(repo: str, file_path: str, ref: str) -> str:
    encoded_path = urllib.parse.quote(file_path, safe="/")
    encoded_ref = urllib.parse.quote(ref, safe="")
    data = _api_get(f"/repos/{repo}/contents/{encoded_path}?ref={encoded_ref}")
    if not isinstance(data, dict) or "content" not in data:
        raise RuntimeError(f"Unexpected contents payload for {file_path}@{ref}")
    if data.get("encoding") != "base64":
        raise RuntimeError(
            f"Unsupported encoding for {file_path}: {data.get('encoding')}"
        )
    raw = base64.b64decode(data["content"])
    return raw.decode("utf-8", errors="replace")


def _list_changed_files(repo: str, pr_number: int) -> list[str]:
    files: list[str] = []
    page = 1
    while True:
        chunk = _api_get(
            f"/repos/{repo}/pulls/{pr_number}/files?per_page=100&page={page}"
        )
        if not isinstance(chunk, list):
            raise RuntimeError(f"Unexpected pulls/files payload for PR #{pr_number}")
        if not chunk:
            break
        files.extend(
            item.get("filename", "") for item in chunk if isinstance(item, dict)
        )
        page += 1
    return [f for f in files if f]


def _parse_inline_branches(text: str, event_key: str) -> list[str]:
    block = re.search(
        rf"(?ms)^\s*{re.escape(event_key)}:\s*\n(?P<body>(?:\s{{2,}}.*\n)+)",
        text,
    )
    if not block:
        return []
    line = re.search(r"branches:\s*\[([^\]]+)\]", block.group("body"))
    if not line:
        return []
    parts = [p.strip().strip("'\"") for p in line.group(1).split(",")]
    return [p for p in parts if p]


def _extract_cov_floor(text: str) -> int | None:
    values = [int(v) for v in re.findall(r"--cov-fail-under=(\d+)", text)]
    return values[-1] if values else None


def _contains_owner_wildcard(codeowners: str) -> bool:
    for raw_line in codeowners.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if parts and parts[0] == "*" and f"@{POLICY_OWNER}" in line.lower():
            return True
    return False


def _matches_restricted_path(path: str) -> bool:
    return any(
        path == prefix or path.startswith(prefix) for prefix in RESTRICTED_PATH_PREFIXES
    )


def _matches_sensitive_non_owner_path(path: str) -> bool:
    return any(
        path == prefix or path.startswith(prefix)
        for prefix in NON_OWNER_SENSITIVE_PATH_PREFIXES
    )


def _contains_top_level_contents_read(workflow_text: str) -> bool:
    return bool(
        re.search(
            r"(?ms)^permissions:\s*\n(?:^[ \t].*\n)+",
            workflow_text,
        )
        and re.search(r"(?m)^[ \t]+contents:\s*read\s*$", workflow_text)
    )


def _require_workflow_snippets(
    result: GuardResult, workflow_path: str, workflow_text: str
) -> None:
    expected = REQUIRED_WORKFLOW_SNIPPETS.get(workflow_path, ())
    missing = [snippet for snippet in expected if snippet not in workflow_text]
    if missing:
        result.fail(
            f"{workflow_path} is missing required command invariants: "
            f"{', '.join(missing)}."
        )


def _check_default_branch_rules(result: GuardResult, repo: str) -> None:
    repo_meta = _api_get(f"/repos/{repo}")
    if not isinstance(repo_meta, dict):
        result.fail("Failed to load repository metadata for ruleset validation.")
        return

    default_branch = str(repo_meta.get("default_branch") or "master")
    encoded_branch = urllib.parse.quote(default_branch, safe="")
    rules = _api_get(f"/repos/{repo}/rules/branches/{encoded_branch}")
    if not isinstance(rules, list):
        result.fail("Unexpected rules payload for default branch validation.")
        return

    by_type: dict[str, list[dict]] = {}
    for item in rules:
        if isinstance(item, dict):
            by_type.setdefault(str(item.get("type") or ""), []).append(item)

    missing_rule_types = sorted(REQUIRED_BRANCH_RULE_TYPES - set(by_type.keys()))
    if missing_rule_types:
        result.fail(
            f"Default branch '{default_branch}' missing required rules: "
            f"{', '.join(missing_rule_types)}."
        )
        return

    pull_rule = by_type["pull_request"][0]
    pull_params = pull_rule.get("parameters", {})
    if not pull_params.get("require_code_owner_review", False):
        result.fail("Default branch must require code owner reviews.")
    if int(pull_params.get("required_approving_review_count", 0)) < 1:
        result.fail("Default branch must require at least one approving review.")
    if not pull_params.get("required_review_thread_resolution", False):
        result.fail("Default branch must require conversation resolution.")
    if not pull_params.get("require_last_push_approval", False):
        result.fail("Default branch must require approval for the latest push.")

    status_rule = by_type["required_status_checks"][0]
    status_params = status_rule.get("parameters", {})
    if not status_params.get("strict_required_status_checks_policy", False):
        result.fail("Default branch status checks must require up-to-date branches.")
    configured_contexts: set[str] = set()
    for check in status_params.get("required_status_checks", []):
        if isinstance(check, dict):
            context = check.get("context")
            if context:
                configured_contexts.add(str(context))
    missing_contexts = sorted(REQUIRED_STATUS_CONTEXTS - configured_contexts)
    if missing_contexts:
        result.fail(
            "Default branch required status checks missing: "
            f"{', '.join(missing_contexts)}."
        )


def _check_policy_files(
    result: GuardResult, repo: str, ref: str, event_name: str, payload: dict
) -> None:
    files: dict[str, str] = {}
    for path in WORKFLOW_PATHS + (
        ".github/CODEOWNERS",
        ".github/pull_request_template.md",
    ):
        try:
            files[path] = _fetch_file_at_ref(repo, path, ref)
        except RuntimeError as exc:
            result.fail(str(exc))
            return

    codeowners = files[".github/CODEOWNERS"]
    if not _contains_owner_wildcard(codeowners):
        result.fail("CODEOWNERS must contain '*' owned by @cyberkrunk69.")

    template = files[".github/pull_request_template.md"]
    for heading in REQUIRED_PR_TEMPLATE_HEADINGS:
        if heading not in template:
            result.fail(f"PR template missing required heading: {heading}")

    if event_name in {"pull_request", "pull_request_target"}:
        body = payload.get("pull_request", {}).get("body") or ""
        for heading in ("## Evidence", "## Security", "## Ownership & Risk"):
            if heading not in body:
                result.fail(f"PR description must include '{heading}' section.")

    lint = files[".github/workflows/lint.yml"]
    lint_push = set(_parse_inline_branches(lint, "push"))
    lint_pr = set(_parse_inline_branches(lint, "pull_request"))
    if not {"master", "main"}.issubset(lint_push):
        result.fail("lint.yml push trigger must include both master and main.")
    if not {"master", "main"}.issubset(lint_pr):
        result.fail("lint.yml pull_request trigger must include both master and main.")

    ci = files[".github/workflows/ci.yml"]
    runtime_floor = _extract_cov_floor(ci)
    if runtime_floor is None:
        result.fail("ci.yml must define --cov-fail-under for runtime coverage.")
    elif runtime_floor < MIN_RUNTIME_COVERAGE:
        result.fail(
            "ci.yml runtime coverage floor "
            f"{runtime_floor}% is below policy minimum "
            f"{MIN_RUNTIME_COVERAGE}%."
        )
    if "Scout Smoke Tests" not in ci:
        result.fail("ci.yml must include Scout Smoke Tests step.")

    control_panel = files[".github/workflows/control-panel.yml"]
    cp_floor = _extract_cov_floor(control_panel)
    if cp_floor is None:
        result.fail("control-panel.yml must define --cov-fail-under.")
    elif cp_floor < MIN_CONTROL_PANEL_COVERAGE:
        result.fail(
            "control-panel.yml coverage floor "
            f"{cp_floor}% is below policy minimum {MIN_CONTROL_PANEL_COVERAGE}%."
        )
    if not re.search(r"(?m)^\s*pull_request:\s*$", control_panel):
        result.fail("control-panel.yml must run on pull_request.")

    for workflow_path in WORKFLOW_PATHS:
        text = files[workflow_path]
        if not _contains_top_level_contents_read(text):
            result.fail(
                f"{workflow_path} must declare top-level permissions "
                "with contents: read."
            )
        if re.search(r"(?mi)^\s*continue-on-error:\s*true\s*$", text):
            result.fail(f"{workflow_path} must not use continue-on-error: true.")
        _require_workflow_snippets(result, workflow_path, text)


def _check_actor_controls(
    result: GuardResult, event_name: str, payload: dict, repo_owner: str
) -> None:
    actor = os.environ.get("GITHUB_ACTOR", "").lower()
    ref_name = os.environ.get("GITHUB_REF_NAME", "")
    owner_allowlist = {repo_owner.lower(), POLICY_OWNER}

    if (
        event_name == "push"
        and ref_name in PROTECTED_BRANCHES
        and actor not in owner_allowlist
    ):
        result.fail(
            "Direct push to protected branch "
            f"'{ref_name}' by '{actor}' is blocked by policy."
        )

    if event_name in {"pull_request", "pull_request_target"}:
        pr = payload.get("pull_request", {})
        changed_files = _list_changed_files(
            _require_env("GITHUB_REPOSITORY"), pr["number"]
        )
        restricted = [p for p in changed_files if _matches_restricted_path(p)]
        sensitive = [p for p in changed_files if _matches_sensitive_non_owner_path(p)]
        if restricted and actor not in owner_allowlist:
            result.fail(
                "Only the owner may modify policy-critical files in PRs. "
                f"Restricted changes detected: {', '.join(restricted[:10])}"
            )
        elif restricted:
            result.note(
                f"Owner is modifying restricted paths: {', '.join(restricted[:10])}"
            )

        if sensitive and actor not in owner_allowlist:
            result.fail(
                "Non-owner PRs cannot modify tests or quality-config surfaces. "
                f"Sensitive changes detected: {', '.join(sensitive[:10])}"
            )
        elif sensitive:
            result.note(
                "Owner is modifying sensitive test/config paths: "
                f"{', '.join(sensitive[:10])}"
            )


def main() -> int:
    try:
        event_name = _require_env("GITHUB_EVENT_NAME")
        repo = _require_env("GITHUB_REPOSITORY")
        repo_owner = _require_env("GITHUB_REPOSITORY_OWNER")
        payload = _load_event_payload()
        ref = _resolve_ref(event_name, payload)
    except Exception as exc:
        print(f"Policy guard bootstrap failure: {exc}", file=sys.stderr)
        return 2

    result = GuardResult()
    result.note(f"Policy owner: @{POLICY_OWNER}")
    result.note(f"Evaluating ref: {ref}")

    try:
        _check_default_branch_rules(result, repo)
        _check_policy_files(result, repo, ref, event_name, payload)
        _check_actor_controls(result, event_name, payload, repo_owner)
    except Exception as exc:  # Defensive: fail closed on unexpected guard exceptions.
        result.fail(f"Policy guard internal error: {exc}")

    return result.finish()


if __name__ == "__main__":
    sys.exit(main())
