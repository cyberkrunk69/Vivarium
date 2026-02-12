"""
Vivarium scope layout and mutable-world version control.

This module defines a strict world separation:
- vivarium/world/mutable : swarm-operable mutable files
- vivarium/meta/*        : security/audit/change-control artifacts
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[2]
VIVARIUM_ROOT = REPO_ROOT / "vivarium"
WORLD_ROOT = VIVARIUM_ROOT / "world"
MUTABLE_ROOT = WORLD_ROOT / "mutable"
META_ROOT = VIVARIUM_ROOT / "meta"
AUDIT_ROOT = META_ROOT / "audit"
SECURITY_ROOT = META_ROOT / "security"
CHANGE_CONTROL_ROOT = META_ROOT / "change_control"
CHECKPOINT_ROOT = CHANGE_CONTROL_ROOT / "checkpoints"
CHANGE_JOURNAL_FILE = CHANGE_CONTROL_ROOT / "change_journal.jsonl"
EXECUTION_TOKEN_FILE = SECURITY_ROOT / "internal_execution_token.txt"

MUTABLE_QUEUE_FILE = MUTABLE_ROOT / "queue.json"
MUTABLE_DATA_DIR = MUTABLE_ROOT / "data"
MUTABLE_EXPERIMENTS_DIR = MUTABLE_ROOT / "experiments"
MUTABLE_CYCLE_LOGS_DIR = MUTABLE_ROOT / "cycle_logs"
# Legacy alias retained for modules not yet migrated.
MUTABLE_GRIND_LOGS_DIR = MUTABLE_CYCLE_LOGS_DIR
MUTABLE_LOCKS_DIR = MUTABLE_ROOT / "task_locks"
# ⚠️ .swarm/ is ephemeral runtime state — NEVER commit
MUTABLE_SWARM_DIR = MUTABLE_ROOT / ".swarm"
MUTABLE_LIBRARY_ROOT = MUTABLE_ROOT / "library"
MUTABLE_COMMUNITY_LIBRARY_ROOT = MUTABLE_LIBRARY_ROOT / "community_library"

ALLOWED_GIT_NETWORK_HOSTS = {"github.com", "api.github.com"}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_queue_payload() -> Dict[str, Any]:
    return {
        "version": "1.0",
        "api_endpoint": "http://127.0.0.1:8420",
        "tasks": [],
        "completed": [],
        "failed": [],
    }


def _append_jsonl(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")


def ensure_scope_layout() -> None:
    """Create all world/meta directories and seed mutable queue."""
    for directory in (
        VIVARIUM_ROOT,
        WORLD_ROOT,
        MUTABLE_ROOT,
        META_ROOT,
        AUDIT_ROOT,
        SECURITY_ROOT,
        CHANGE_CONTROL_ROOT,
        CHECKPOINT_ROOT,
        MUTABLE_DATA_DIR,
        MUTABLE_EXPERIMENTS_DIR,
        MUTABLE_CYCLE_LOGS_DIR,
        MUTABLE_LOCKS_DIR,
        MUTABLE_SWARM_DIR,
        MUTABLE_LIBRARY_ROOT,
        MUTABLE_COMMUNITY_LIBRARY_ROOT,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    legacy_knowledge_dir = MUTABLE_ROOT / "knowledge"
    if legacy_knowledge_dir.exists() and legacy_knowledge_dir.is_dir():
        if not any(MUTABLE_COMMUNITY_LIBRARY_ROOT.iterdir()):
            for item in legacy_knowledge_dir.iterdir():
                target = MUTABLE_COMMUNITY_LIBRARY_ROOT / item.name
                if target.exists():
                    continue
                item.rename(target)
            try:
                legacy_knowledge_dir.rmdir()
            except OSError:
                pass

    if not MUTABLE_QUEUE_FILE.exists():
        legacy_queue = REPO_ROOT / "queue.json"
        if legacy_queue.exists():
            MUTABLE_QUEUE_FILE.write_text(
                legacy_queue.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        else:
            MUTABLE_QUEUE_FILE.write_text(
                json.dumps(_default_queue_payload(), indent=2) + "\n",
                encoding="utf-8",
            )

    CHANGE_JOURNAL_FILE.touch(exist_ok=True)


def get_execution_token() -> str:
    """
    Return the internal execution token used for worker->API authentication.

    Resolution order:
    1. VIVARIUM_INTERNAL_EXECUTION_TOKEN environment variable
    2. vivarium/meta/security/internal_execution_token.txt
    3. generate and persist a new token in the security scope
    """
    env_token = (os.environ.get("VIVARIUM_INTERNAL_EXECUTION_TOKEN") or "").strip()
    if env_token:
        return env_token

    ensure_scope_layout()
    if EXECUTION_TOKEN_FILE.exists():
        existing = EXECUTION_TOKEN_FILE.read_text(encoding="utf-8").strip()
        if existing:
            return existing

    token = secrets.token_urlsafe(48)
    EXECUTION_TOKEN_FILE.write_text(token + "\n", encoding="utf-8")
    try:
        os.chmod(EXECUTION_TOKEN_FILE, 0o600)
    except OSError:
        # Best-effort on platforms/filesystems that may not support chmod semantics.
        pass
    return token


def resolve_mutable_path(path_token: str, cwd: Optional[Path] = None) -> Path:
    """
    Resolve a token into an absolute path and enforce mutable-world containment.
    """
    raw = Path(path_token)
    base = (cwd or MUTABLE_ROOT).resolve()
    candidate = raw if raw.is_absolute() else (base / raw)
    resolved = candidate.resolve()
    mutable_root = MUTABLE_ROOT.resolve()
    if resolved == mutable_root or mutable_root in resolved.parents:
        return resolved
    raise ValueError(f"Path escapes mutable world scope: {path_token}")


def is_within_mutable(path: Path) -> bool:
    try:
        resolve_mutable_path(str(path))
        return True
    except ValueError:
        return False


def is_allowed_git_remote(url: str) -> bool:
    """
    Allow git network remotes only for GitHub domains.
    """
    trimmed = (url or "").strip()
    if not trimmed:
        return False

    if "://" in trimmed:
        parsed = urlparse(trimmed)
        host = (parsed.hostname or "").lower()
        return host in ALLOWED_GIT_NETWORK_HOSTS

    # SSH-style: git@github.com:owner/repo.git
    if "@" in trimmed and ":" in trimmed:
        host_part = trimmed.split("@", 1)[1].split(":", 1)[0].lower()
        return host_part in ALLOWED_GIT_NETWORK_HOSTS

    return False


@dataclass
class CheckpointResult:
    commit_sha: Optional[str]
    changed: bool
    message: str


class MutableWorldVersionControl:
    """
    Lightweight auto-version-control for the mutable world scope.
    """

    def __init__(
        self,
        mutable_root: Path = MUTABLE_ROOT,
        journal_file: Path = CHANGE_JOURNAL_FILE,
    ):
        self.mutable_root = mutable_root
        self.journal_file = journal_file
        ensure_scope_layout()

    def _run_git(self, *args: str) -> Tuple[bool, str]:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=str(self.mutable_root),
                capture_output=True,
                text=True,
                check=True,
            )
            return True, (result.stdout or "").strip()
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or exc.stdout or str(exc)).strip()
            return False, stderr

    def _ensure_repo(self) -> None:
        git_dir = self.mutable_root / ".git"
        if git_dir.exists():
            return

        ok, output = self._run_git("init")
        if not ok:
            raise RuntimeError(f"Failed to initialize mutable git repo: {output}")

        # Configure local identity for automatic checkpoints.
        self._run_git("config", "user.name", "vivarium-autocheckpoint")
        self._run_git("config", "user.email", "vivarium@local")

    def _append_journal(self, payload: Dict[str, Any]) -> None:
        payload_with_time = {"timestamp": _utc_now_iso(), **payload}
        _append_jsonl(self.journal_file, payload_with_time)

    def checkpoint(
        self,
        task_id: str,
        summary: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CheckpointResult:
        self._ensure_repo()

        ok, status = self._run_git("status", "--porcelain")
        if not ok:
            self._append_journal(
                {
                    "event": "checkpoint_failed",
                    "task_id": task_id,
                    "summary": summary,
                    "reason": status,
                }
            )
            return CheckpointResult(commit_sha=None, changed=False, message=status)

        if not status.strip():
            self._append_journal(
                {
                    "event": "checkpoint_skipped",
                    "task_id": task_id,
                    "summary": summary,
                    "reason": "no_changes",
                }
            )
            return CheckpointResult(commit_sha=None, changed=False, message="No mutable changes")

        add_ok, add_out = self._run_git("add", "-A")
        if not add_ok:
            self._append_journal(
                {
                    "event": "checkpoint_failed",
                    "task_id": task_id,
                    "summary": summary,
                    "reason": add_out,
                }
            )
            return CheckpointResult(commit_sha=None, changed=False, message=add_out)

        commit_message = f"auto-checkpoint:{task_id} {summary[:500]}".strip()
        commit_ok, commit_out = self._run_git("commit", "-m", commit_message)
        if not commit_ok:
            # Can happen if changes collapse to nothing after normalization/hooks.
            self._append_journal(
                {
                    "event": "checkpoint_skipped",
                    "task_id": task_id,
                    "summary": summary,
                    "reason": commit_out or "commit_failed",
                }
            )
            return CheckpointResult(commit_sha=None, changed=False, message=commit_out)

        sha_ok, sha_out = self._run_git("rev-parse", "HEAD")
        commit_sha = sha_out if sha_ok else None
        self._append_journal(
            {
                "event": "checkpoint_created",
                "task_id": task_id,
                "summary": summary,
                "commit_sha": commit_sha,
                "metadata": metadata or {},
            }
        )
        return CheckpointResult(
            commit_sha=commit_sha,
            changed=True,
            message=commit_out or "checkpoint_created",
        )

    def rollback_to(self, commit_sha: str, reason: str = "") -> bool:
        self._ensure_repo()
        ok, output = self._run_git("reset", "--hard", commit_sha)
        self._append_journal(
            {
                "event": "rollback",
                "commit_sha": commit_sha,
                "reason": reason,
                "success": ok,
                "details": output,
            }
        )
        return ok


_version_control: Optional[MutableWorldVersionControl] = None


def get_mutable_version_control() -> MutableWorldVersionControl:
    global _version_control
    if _version_control is None:
        _version_control = MutableWorldVersionControl()
    return _version_control

