"""
One-time tasks: any resident can complete each task once and receive a bonus.

Residents see the list in context; when they complete a task (add it to the queue,
do the work, and get human approval), they receive the one-time bonus and are
recorded so they cannot claim it again.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ONE_TIME_COMPLETIONS_FILE = ".swarm/one_time_completions.json"
ONE_TIME_TASKS_FILE = ".swarm/one_time_tasks.json"

# Built-in default (each task: id, title, prompt, bonus_tokens)
ONE_TIME_TASKS_DEFAULT: List[Dict[str, Any]] = [
    {
        "id": "one_time_crystallize_personality",
        "title": "Crystallize your personality",
        "prompt": (
            "Create a short, clear document that crystallizes your personality: "
            "your core traits, values, and how you prefer to work and communicate. "
            "Save it under library/community_library/resident_suggestions/<your_identity_id>/ "
            "or in your journal. One-time completion bonus."
        ),
        "bonus_tokens": 25,
    },
]


def _ledger_path(workspace: Path) -> Path:
    return workspace / ONE_TIME_COMPLETIONS_FILE


def _tasks_file_path(workspace: Path) -> Path:
    return workspace / ONE_TIME_TASKS_FILE


def _get_current_identity_ids(workspace: Path) -> List[str]:
    """Return list of identity IDs that exist on disk (.swarm/identities/*.json). Used to lock new one-time tasks so only identities that existed at creation can claim—not 'create new identity to get tokens again'. Residents can swap which identity is active; eligibility is by identity record on disk, not who is currently inhabited."""
    identities_dir = workspace / ".swarm" / "identities"
    if not identities_dir.is_dir():
        return []
    return [p.stem for p in identities_dir.glob("*.json") if p.is_file() and p.stem]


def _identity_eligible_for_task(task: Dict[str, Any], identity_id: str) -> bool:
    """True if this identity can claim this one-time task. Tasks with eligible_identity_ids only allow those identities (lock at creation)."""
    eligible = task.get("eligible_identity_ids")
    if not eligible:
        return True  # Legacy or built-in: no lock, everyone eligible
    return identity_id in eligible


def _load_tasks_from_file(workspace: Path) -> List[Dict[str, Any]] | None:
    path = _tasks_file_path(workspace)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [t for t in data if isinstance(t, dict) and t.get("id")]
    except Exception:
        pass
    return None


def _save_tasks_to_file(workspace: Path, tasks: List[Dict[str, Any]]) -> None:
    path = _tasks_file_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def get_one_time_tasks(workspace: Path | None = None) -> List[Dict[str, Any]]:
    """Return the list of one-time task definitions. If workspace is set and has one_time_tasks.json, use that; else defaults."""
    if workspace is not None:
        from_file = _load_tasks_from_file(workspace)
        if from_file is not None:
            return list(from_file)
    return list(ONE_TIME_TASKS_DEFAULT)


def get_completions(workspace: Path) -> Dict[str, List[str]]:
    """Return { task_id: [identity_id, ...] } of who has completed each one-time task."""
    path = _ledger_path(workspace)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        comp = data.get("completions")
        if isinstance(comp, dict):
            return {k: list(v) if isinstance(v, list) else [] for k, v in comp.items()}
    except Exception:
        pass
    return {}


def has_completed(workspace: Path, task_id: str, identity_id: str) -> bool:
    """Return True if this identity has already completed this one-time task."""
    comp = get_completions(workspace)
    return identity_id in comp.get(task_id, [])


def get_task_by_id(task_id: str, workspace: Path | None = None) -> Dict[str, Any] | None:
    """Return the one-time task definition for this id, or None."""
    for t in get_one_time_tasks(workspace):
        if t.get("id") == task_id:
            return t
    return None


def add_one_time_task(workspace: Path, task: Dict[str, Any]) -> Dict[str, Any]:
    """Add or replace a one-time task. Locks eligibility to identities that exist at creation (prevents creating new identity to claim again)."""
    tid = str((task.get("id") or "").strip())
    if not tid:
        return {"success": False, "error": "id is required"}
    title = str(task.get("title") or tid).strip()
    prompt = str(task.get("prompt") or "").strip()
    bonus = max(0, int(task.get("bonus_tokens") or 0))
    eligible = _get_current_identity_ids(workspace)
    tasks = get_one_time_tasks(workspace)
    tasks = [t for t in tasks if t.get("id") != tid]
    tasks.append({
        "id": tid,
        "title": title,
        "prompt": prompt,
        "bonus_tokens": bonus,
        "eligible_identity_ids": eligible,
    })
    _save_tasks_to_file(workspace, tasks)
    return {"success": True, "task_id": tid, "eligible_count": len(eligible)}


def update_one_time_task(
    workspace: Path, task_id: str, updates: Dict[str, Any]
) -> Dict[str, Any]:
    """Update an existing one-time task (e.g. bonus_tokens, prompt). Returns { success, task_id, error? }."""
    task_id = str(task_id or "").strip()
    if not task_id:
        return {"success": False, "error": "task_id is required"}
    allowed = {"bonus_tokens", "prompt", "title"}
    updates = {k: v for k, v in (updates or {}).items() if k in allowed}
    if not updates:
        return {"success": False, "error": "no allowed fields to update"}
    tasks = get_one_time_tasks(workspace)
    for t in tasks:
        if t.get("id") == task_id:
            if "bonus_tokens" in updates:
                t["bonus_tokens"] = max(0, int(updates["bonus_tokens"]) if updates["bonus_tokens"] is not None else 0)
            if "prompt" in updates:
                t["prompt"] = str(updates["prompt"] or "").strip()
            if "title" in updates:
                t["title"] = str(updates["title"] or task_id).strip()
            _save_tasks_to_file(workspace, tasks)
            return {"success": True, "task_id": task_id}
    return {"success": False, "error": "task not found"}


def delete_one_time_task(workspace: Path, task_id: str) -> Dict[str, Any]:
    """Remove a one-time task by id. Returns { success, task_id, error? }."""
    task_id = str(task_id or "").strip()
    if not task_id:
        return {"success": False, "error": "task_id is required"}
    tasks = get_one_time_tasks(workspace)
    if not any(t.get("id") == task_id for t in tasks):
        return {"success": False, "error": "task not found"}
    tasks = [t for t in tasks if t.get("id") != task_id]
    # Always persist (even empty list) so delete sticks; only "no file" means use built-in defaults
    _save_tasks_to_file(workspace, tasks)
    return {"success": True, "task_id": task_id}


def grant_and_record(
    workspace: Path,
    task_id: str,
    identity_id: str,
    enrichment: Any,
) -> Dict[str, Any]:
    """
    If this identity has not completed this one-time task, grant the bonus and record.
    Returns { "granted": bool, "tokens": int, "reason": str }.
    """
    task = get_task_by_id(task_id, workspace)
    if not task:
        return {"granted": False, "tokens": 0, "reason": "not_one_time_task"}
    if not identity_id:
        return {"granted": False, "tokens": 0, "reason": "no_identity"}
    if not _identity_eligible_for_task(task, identity_id):
        return {"granted": False, "tokens": 0, "reason": "identity_not_eligible"}
    if has_completed(workspace, task_id, identity_id):
        return {"granted": False, "tokens": 0, "reason": "already_completed"}
    bonus = max(0, int(task.get("bonus_tokens", 0)))
    if bonus <= 0:
        return {"granted": False, "tokens": 0, "reason": "no_bonus"}
    try:
        result = enrichment.grant_free_time(
            identity_id, bonus, reason=f"one_time_bonus:{task_id}"
        )
        granted = (result or {}).get("granted", {})
        tokens = int(granted.get("free_time", 0)) + int(granted.get("journal", 0))
    except Exception as e:
        return {"granted": False, "tokens": 0, "reason": str(e)}
    # Record completion
    path = _ledger_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    comp = get_completions(workspace)
    comp.setdefault(task_id, [])
    if identity_id not in comp[task_id]:
        comp[task_id].append(identity_id)
    try:
        path.write_text(
            json.dumps({"completions": comp}, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass
    return {"granted": True, "tokens": tokens, "reason": f"one_time_bonus:{task_id}"}


def format_one_time_section(workspace: Path, identity_id: str) -> str:
    """Format the one-time tasks block for resident context. Only tasks this identity has not completed are listed."""
    tasks = get_one_time_tasks(workspace)
    if not tasks:
        return ""
    completions = get_completions(workspace)
    remaining = [
        t for t in tasks
        if identity_id not in completions.get(t.get("id", ""), [])
        and _identity_eligible_for_task(t, identity_id)
    ]
    if not remaining:
        return ""
    lines = [
        "ONE-TIME TASKS (each resident can complete each of these once for a bonus):",
        "You can all do these one time. Add a task to the queue with the id below to claim; when the human approves, you get the one-time bonus.",
        "",
    ]
    for t in remaining:
        tid = t.get("id", "")
        title = t.get("title", tid)
        bonus = t.get("bonus_tokens", 0)
        prompt_short = (t.get("prompt", "") or "").rstrip()
        lines.append(f"- [{tid}]: {title} (one-time bonus: {bonus} tokens)")
        lines.append(f"  Prompt: {prompt_short}")
    lines.append("")
    return "\n".join(lines)
