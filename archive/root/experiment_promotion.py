"""
experiment_promotion.py

Provides utilities to automatically promote successful experiments into the main codebase.
It extracts the file changes produced by an experiment, applies them, creates a git commit
with proper attribution, optionally bumps the project version, and performs basic conflict
resolution when multiple experiments touch the same files.

Usage:
    from experiment_promotion import promote_experiment

    promote_experiment(
        experiment_id="exp_42",
        changes=[
            {"path": "module/submodule.py", "diff": "... unified diff ..."},
            {"path": "another_module.py", "diff": "..."},
        ],
        author_name="Jane Doe",
        author_email="jane@example.com",
        significant=True,  # bump version if the change is significant
    )
"""

import os
import re
import subprocess
from typing import List, Dict, Optional

from git import Repo, Actor, GitCommandError

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _repo_root() -> str:
    """Return the absolute path to the git repository root."""
    return Repo(search_parent_directories=True).working_tree_dir


def _apply_diff(repo_path: str, file_path: str, diff_text: str) -> None:
    """
    Apply a unified diff to a file within the repository.

    Parameters
    ----------
    repo_path : str
        Absolute path to the repository root.
    file_path : str
        Path to the file relative to the repository root.
    diff_text : str
        Unified diff text (as produced by `git diff`).

    Raises
    ------
    RuntimeError
        If the diff cannot be applied cleanly.
    """
    full_path = os.path.join(repo_path, file_path)
    # Ensure the target file exists (git apply can create new files with the diff)
    if not os.path.isdir(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Write diff to a temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write(diff_text)
        tmp_path = tmp.name

    try:
        # Use `git apply` with 3-way merge to help resolve simple conflicts
        subprocess.check_output(
            ["git", "apply", "--3way", "--whitespace=nowarn", tmp_path],
            cwd=repo_path,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Failed to apply diff for {file_path}: {exc.output.decode()}"
        ) from exc
    finally:
        os.remove(tmp_path)


def _stage_file(repo: Repo, file_path: str) -> None:
    """Stage a file for commit."""
    repo.index.add([file_path])


def _find_version_file(repo_path: str) -> Optional[str]:
    """
    Search common locations for a version declaration.
    Returns the relative path to the version file if found, otherwise None.
    """
    candidates = [
        "pyproject.toml",
        "setup.cfg",
        "setup.py",
        # Look for a package __init__ containing __version__
    ]
    for root, _, files in os.walk(repo_path):
        for f in files:
            if f == "__init__.py":
                candidates.append(os.path.relpath(os.path.join(root, f), repo_path))

    for candidate in candidates:
        full_path = os.path.join(repo_path, candidate)
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as fh:
                content = fh.read()
                if re.search(r"__version__\s*=", content) or re.search(r"version\s*=", content):
                    return candidate
    return None


def _bump_version(repo_path: str, version_file: str) -> None:
    """
    Increment the patch part of a semantic version string found in the version file.
    Supports formats like:
        __version__ = "1.2.3"
        version = "0.9.0"
    """
    full_path = os.path.join(repo_path, version_file)
    with open(full_path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    version_pattern = re.compile(r'(?P<prefix>["\'])(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix>["\'])')
    new_lines = []
    bumped = False

    for line in lines:
        if not bumped and ("__version__" in line or "version" in line):
            match = version_pattern.search(line)
            if match:
                major, minor, patch = map(int, match.group("major", "minor", "patch"))
                new_version = f'{match.group("prefix")}{major}.{minor}.{patch + 1}{match.group("suffix")}'
                line = version_pattern.sub(new_version, line, count=1)
                bumped = True
        new_lines.append(line)

    if not bumped:
        raise RuntimeError(f"Could not locate a version string in {version_file}")

    with open(full_path, "w", encoding="utf-8") as fh:
        fh.writelines(new_lines)


def _detect_conflict(repo: Repo, file_path: str) -> bool:
    """
    Detect if the given file already has uncommitted changes in the index or working tree.
    Returns True if a conflict is likely.
    """
    # Check if the file is already staged with modifications
    try:
        repo.git.diff("--cached", "--name-only", file_path)
        staged = repo.git.diff("--cached", "--name-only", file_path).strip()
    except GitCommandError:
        staged = ""

    # Check working tree changes
    try:
        wt = repo.git.diff("--name-only", file_path).strip()
    except GitCommandError:
        wt = ""

    return bool(staged or wt)


# --------------------------------------------------------------------------- #
# Core Promotion Logic
# --------------------------------------------------------------------------- #

def promote_experiment(
    experiment_id: str,
    changes: List[Dict[str, str]],
    author_name: str,
    author_email: str,
    significant: bool = False,
) -> None:
    """
    Promote a successful experiment into the main codebase.

    Parameters
    ----------
    experiment_id : str
        Identifier of the experiment (used for commit messages).
    changes : list of dict
        Each dict must contain:
            - "path": relative path to the file within the repo.
            - "diff": unified diff text representing the change.
    author_name : str
        Name of the experiment author.
    author_email : str
        Email of the experiment author.
    significant : bool, optional
        If True, the project version will be bumped after applying changes.
    """
    repo_path = _repo_root()
    repo = Repo(repo_path)

    # Step 1: Apply each diff, handling conflicts
    for change in changes:
        file_path = change["path"]
        diff_text = change["diff"]

        if _detect_conflict(repo, file_path):
            raise RuntimeError(
                f"Conflict detected: {file_path} has uncommitted changes. "
                "Resolve the conflict before promotion."
            )

        _apply_diff(repo_path, file_path, diff_text)
        _stage_file(repo, file_path)

    # Step 2: Optional version bump
    if significant:
        version_file = _find_version_file(repo_path)
        if version_file:
            _bump_version(repo_path, version_file)
            _stage_file(repo, version_file)
        else:
            # If we cannot locate a version file, we simply log a warning.
            print("Warning: No version file found; skipping version bump.")

    # Step 3: Commit with proper attribution
    author = Actor(author_name, author_email)
    commit_message = f"Promote experiment {experiment_id}\n\n"
    commit_message += "Automatically applied changes from a successful experiment.\n"
    if significant:
        commit_message += "\nVersion bumped due to significant changes."

    repo.index.commit(commit_message, author=author, committer=author)

    # Step 4: Push (optional – left to the caller or CI pipeline)
    # Example: repo.remotes.origin.push()
    print(f"Experiment {experiment_id} promoted and committed as {repo.head.commit.hexsha[:7]}.")