"""Quests blueprint: create, status, tip, pause, resume, approve."""
from __future__ import annotations

import time
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request

from vivarium.utils import read_json, write_json
from vivarium.runtime.runtime_contract import normalize_queue, normalize_task

QUEST_DEFAULT_BUDGET = 0.20
QUEST_DEFAULT_UPFRONT_TIP = 10
QUEST_DEFAULT_COMPLETION_REWARD = 30

bp = Blueprint("quests", __name__, url_prefix="/api")


def _quest_helpers():
    """Lazy import from control_panel_app to avoid circular deps."""
    from vivarium.runtime import control_panel_app as app

    return (
        app.get_identities,
        app.get_human_username,
        app._enqueue_identity_task,
        app._remove_open_queue_task,
        app._dm_enrichment,
        app._refresh_mailbox_quests_state,
    )


def _get_quests_file():
    return current_app.config["MAILBOX_QUESTS_FILE"]


def _load_mailbox_quests() -> list[dict]:
    data = read_json(_get_quests_file(), default=[])
    return data if isinstance(data, list) else []


def _save_mailbox_quests(quests: list[dict]) -> None:
    path = _get_quests_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, quests)


def _normalize_quest_budget(value, default: float = QUEST_DEFAULT_BUDGET) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = default
    if parsed < 0:
        return 0.0
    return round(min(parsed, 50.0), 4)


def _normalize_quest_tokens(value, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(0, min(parsed, 5000))


@bp.route("/quests/create", methods=["POST"])
def create_quest():
    """POST /api/quests/create - Create an identity-targeted quest from mailbox UI."""
    data = request.get_json(force=True, silent=True) or {}
    identity_id = str(data.get("identity_id") or "").strip()
    prompt = str(data.get("prompt") or "").strip()
    title = str(data.get("title") or "").strip() or "Mailbox Quest"
    if not identity_id:
        return jsonify({"success": False, "error": "identity_id is required"}), 400
    if not prompt:
        return jsonify({"success": False, "error": "prompt is required"}), 400

    budget = _normalize_quest_budget(data.get("budget"), QUEST_DEFAULT_BUDGET)
    upfront_tip = _normalize_quest_tokens(data.get("upfront_tip"), QUEST_DEFAULT_UPFRONT_TIP)
    completion_reward = _normalize_quest_tokens(data.get("completion_reward"), QUEST_DEFAULT_COMPLETION_REWARD)
    min_budget = max(0.01, round(min(0.10, budget), 4))
    max_budget = max(min_budget, budget)

    get_identities, get_human_username, _enqueue_identity_task, _, _dm_enrichment, _ = _quest_helpers()
    identities = get_identities()
    identity = next((i for i in identities if str(i.get("id")) == identity_id), None)
    identity_name = str((identity or {}).get("name") or identity_id)
    quest_id = f"quest_{int(time.time() * 1000)}"
    task_id = f"quest-task-{identity_id}-{int(time.time() * 1000)}"
    quest_prompt = (
        f"Quest for {identity_name} ({identity_id}).\n"
        f"Objective: {prompt}\n\n"
        "Run this quest while still participating in normal resident social life: "
        "coordination, DMs, and shared room interactions stay active."
    )

    try:
        _enqueue_identity_task(
            task_id=task_id,
            prompt=quest_prompt,
            identity_id=identity_id,
            min_budget=min_budget,
            max_budget=max_budget,
        )
        if upfront_tip > 0:
            _dm_enrichment().grant_free_time(identity_id, upfront_tip, reason=f"{quest_id}_upfront_tip")
        _dm_enrichment().post_discussion_message(
            identity_id="human_operator",
            identity_name=get_human_username(),
            content=f"[quest assigned to {identity_name}] {title}: {prompt}",
            room="human_async",
            mood="async",
            importance=4,
        )
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

    quests = _load_mailbox_quests()
    quests.insert(
        0,
        {
            "id": quest_id,
            "task_id": task_id,
            "identity_id": identity_id,
            "identity_name": identity_name,
            "title": title,
            "prompt": prompt,
            "budget": max_budget,
            "upfront_tip": upfront_tip,
            "completion_reward": completion_reward,
            "status": "active",
            "manual_paused": False,
            "completion_approved": False,
            "completion_reward_paid": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        },
    )
    _save_mailbox_quests(quests)
    return jsonify({"success": True, "quest_id": quest_id, "task_id": task_id})


@bp.route("/quests/status")
def quest_status():
    """GET /api/quests/status - Get quest status."""
    _, _, _, _, _, _refresh_mailbox_quests_state = _quest_helpers()
    quests = _refresh_mailbox_quests_state()
    return jsonify({"success": True, "quests": quests[:120]})


@bp.route("/quests/tip", methods=["POST"])
def quest_tip():
    """POST /api/quests/tip - Tip a quest."""
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    tokens = _normalize_quest_tokens(data.get("tokens"), 10)
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    if tokens <= 0:
        return jsonify({"success": False, "error": "tokens must be > 0"}), 400

    quests = _load_mailbox_quests()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404
    identity_id = str(quest.get("identity_id") or "").strip()
    if not identity_id:
        return jsonify({"success": False, "error": "quest identity missing"}), 400

    _, _, _, _, _dm_enrichment, _ = _quest_helpers()
    try:
        _dm_enrichment().grant_free_time(identity_id, tokens, reason=f"{quest_id}_manual_tip")
        quest["updated_at"] = datetime.now().isoformat()
        quest["last_tip_tokens"] = tokens
        quest["last_tip_at"] = quest["updated_at"]
        _save_mailbox_quests(quests)
        return jsonify({"success": True, "quest": quest})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@bp.route("/quests/pause", methods=["POST"])
def quest_pause():
    """POST /api/quests/pause - Pause a quest."""
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    quests = _load_mailbox_quests()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404

    _, _, _, _remove_open_queue_task, _, _ = _quest_helpers()
    task_id = str(quest.get("task_id") or "").strip()
    removed_task = None
    if task_id:
        removed_task, _ = _remove_open_queue_task(task_id)
    quest["paused_task"] = removed_task
    quest["manual_paused"] = True
    quest["status"] = "paused"
    quest["updated_at"] = datetime.now().isoformat()
    _save_mailbox_quests(quests)
    return jsonify({"success": True, "quest": quest, "removed_from_open_queue": bool(removed_task)})


@bp.route("/quests/resume", methods=["POST"])
def quest_resume():
    """POST /api/quests/resume - Resume a paused quest."""
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    quests = _load_mailbox_quests()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404

    paused_task = quest.get("paused_task")
    if isinstance(paused_task, dict) and paused_task.get("id"):
        queue_file = current_app.config["QUEUE_FILE"]
        queue = normalize_queue(read_json(queue_file, default={}))
        if not any(str(t.get("id") or "") == str(paused_task.get("id")) for t in queue.get("tasks", [])):
            queue.setdefault("tasks", []).append(normalize_task(paused_task))
            write_json(queue_file, normalize_queue(queue))
    quest["paused_task"] = None
    quest["manual_paused"] = False
    quest["status"] = "active"
    quest["updated_at"] = datetime.now().isoformat()
    _save_mailbox_quests(quests)
    return jsonify({"success": True, "quest": quest})


@bp.route("/quests/approve", methods=["POST"])
def quest_approve():
    """POST /api/quests/approve - Approve quest completion and pay reward."""
    data = request.get_json(force=True, silent=True) or {}
    quest_id = str(data.get("quest_id") or "").strip()
    if not quest_id:
        return jsonify({"success": False, "error": "quest_id is required"}), 400
    _, _, _, _, _dm_enrichment, _refresh_mailbox_quests_state = _quest_helpers()
    quests = _refresh_mailbox_quests_state()
    quest = next((q for q in quests if str(q.get("id")) == quest_id), None)
    if not quest:
        return jsonify({"success": False, "error": "quest not found"}), 404
    if str(quest.get("status")) not in {"awaiting_approval", "completed"}:
        return jsonify({"success": False, "error": "quest is not awaiting approval"}), 409
    if quest.get("completion_reward_paid"):
        return jsonify({"success": False, "error": "completion reward already paid"}), 409

    identity_id = str(quest.get("identity_id") or "").strip()
    reward = _normalize_quest_tokens(quest.get("completion_reward"), QUEST_DEFAULT_COMPLETION_REWARD)
    try:
        if reward > 0 and identity_id:
            _dm_enrichment().grant_free_time(identity_id, reward, reason=f"{quest_id}_completion_reward")
        quest["completion_approved"] = True
        quest["completion_reward_paid"] = reward > 0
        quest["status"] = "completed"
        quest["updated_at"] = datetime.now().isoformat()
        _save_mailbox_quests(quests)
        return jsonify({"success": True, "quest": quest, "reward": reward})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
