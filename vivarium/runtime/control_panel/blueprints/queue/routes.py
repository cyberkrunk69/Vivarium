"""Queue blueprint: queue CRUD, one-time tasks, approve/requeue/remove."""
from __future__ import annotations

import time
from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request

from vivarium.runtime.runtime_contract import normalize_queue, normalize_task
from vivarium.utils import append_jsonl, read_json, write_json

bp = Blueprint("queue", __name__, url_prefix="/api")


def _queue_helpers():
    """Lazy import — this is the core orchestration."""
    from vivarium.runtime.control_panel_app import (
        _apply_queue_outcome,
        _dm_enrichment,
        _latest_execution_status,
        get_human_username,
        load_ui_settings,
    )
    return (
        load_ui_settings,
        get_human_username,
        _latest_execution_status,
        _dm_enrichment,
        _apply_queue_outcome,
    )


# ═══════════════════════════════════════════════════════════════════
# QUEUE – Add task from UI
# ═══════════════════════════════════════════════════════════════════


@bp.route("/queue/add", methods=["POST"])
def api_queue_add():
    """Add a task to the queue from UI. Body: { "task_id": "...", "instruction": "..." }."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = (data.get("task_id") or "").strip()
    instruction = (data.get("instruction") or "").strip()
    if not instruction:
        return jsonify({"success": False, "error": "instruction is required"}), 400
    QUEUE_FILE = current_app.config["QUEUE_FILE"]
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    existing_ids = {t.get("id") for t in queue.get("tasks", []) if t.get("id")}
    if not task_id:
        task_id = f"task-{int(time.time() * 1000)}"
    if task_id in existing_ids:
        base = task_id
        suffix = 1
        while f"{base}-{suffix}" in existing_ids:
            suffix += 1
        task_id = f"{base}-{suffix}"
    load_ui_settings, _, _, _, _ = _queue_helpers()
    ui_settings = load_ui_settings()
    override_model = bool(ui_settings.get("override_model"))
    model = str(ui_settings.get("model") or "auto")
    task_model = model if override_model and model != "auto" else None
    min_budget = float(ui_settings.get("task_min_budget", 0.05))
    max_budget = float(ui_settings.get("task_max_budget", max(min_budget, 0.10)))
    if max_budget < min_budget:
        max_budget = min_budget
    task = normalize_task({
        "id": task_id,
        "type": "cycle",
        "prompt": instruction,
        "min_budget": min_budget,
        "max_budget": max_budget,
        "intensity": "medium",
        "model": task_model,
        "depends_on": [],
        "parallel_safe": True,
    })
    queue.setdefault("tasks", []).append(task)
    write_json(QUEUE_FILE, normalize_queue(queue))
    return jsonify({"success": True, "task_id": task_id})


@bp.route("/queue/update", methods=["POST"])
def api_queue_update():
    """Update an open queue task's id and/or instruction."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    new_task_id = str(data.get("new_task_id") or "").strip()
    instruction = str(data.get("instruction") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400
    if not instruction:
        return jsonify({"success": False, "error": "instruction is required"}), 400

    QUEUE_FILE = current_app.config["QUEUE_FILE"]
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    tasks = list(queue.get("tasks", []))
    target_idx = None
    for idx, task in enumerate(tasks):
        if str(task.get("id") or "").strip() == task_id:
            target_idx = idx
            break
    if target_idx is None:
        return jsonify({"success": False, "error": "task not found in open queue"}), 404

    final_id = new_task_id or task_id
    existing_ids = {
        str(t.get("id") or "").strip()
        for i, t in enumerate(tasks)
        if i != target_idx and str(t.get("id") or "").strip()
    }
    if final_id in existing_ids:
        return jsonify({"success": False, "error": f"task id already exists: {final_id}"}), 409

    updated = dict(tasks[target_idx])
    updated["id"] = final_id
    updated["prompt"] = instruction
    tasks[target_idx] = normalize_task(updated)
    queue["tasks"] = tasks
    write_json(QUEUE_FILE, normalize_queue(queue))
    return jsonify({"success": True, "task_id": final_id})


@bp.route("/queue/delete", methods=["POST"])
def api_queue_delete():
    """Delete a task from open/completed/failed queue collections."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400

    QUEUE_FILE = current_app.config["QUEUE_FILE"]
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    removed_from = None
    for section in ("tasks", "completed", "failed"):
        items = list(queue.get(section, []))
        new_items = [item for item in items if str(item.get("id") or "").strip() != task_id]
        if len(new_items) != len(items):
            queue[section] = new_items
            removed_from = section
            break
    if not removed_from:
        return jsonify({"success": False, "error": "task not found"}), 404

    write_json(QUEUE_FILE, normalize_queue(queue))
    return jsonify({"success": True, "task_id": task_id, "removed_from": removed_from})


@bp.route("/queue/state")
def api_queue_state():
    """Return queue tasks for UI visualization, including tasks pending human approval."""
    QUEUE_FILE = current_app.config["QUEUE_FILE"]
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    open_tasks = queue.get("tasks", []) if isinstance(queue.get("tasks"), list) else []
    completed = queue.get("completed", []) if isinstance(queue.get("completed"), list) else []
    failed = queue.get("failed", []) if isinstance(queue.get("failed"), list) else []
    _, _, _latest_execution_status, _, _ = _queue_helpers()
    pending_review = []
    for task in open_tasks[:50]:
        tid = task.get("id")
        if not tid:
            continue
        status, last_event = _latest_execution_status(tid)
        if status != "pending_review":
            continue
        pending_review.append({
            **task,
            "identity_id": last_event.get("identity_id") or last_event.get("worker_id"),
            "result_summary": last_event.get("result_summary"),
            "review_verdict": last_event.get("review_verdict"),
        })
    return jsonify({
        "success": True,
        "open": open_tasks[:50],
        "pending_review": pending_review,
        "completed": completed[-25:],
        "failed": failed[-25:],
    })


# ─── One-time tasks (per identity) ─────────────────────────────────────────


@bp.route("/one_time_tasks", methods=["GET"])
def api_one_time_tasks_list():
    """List one-time-per-identity task definitions."""
    try:
        from vivarium.runtime.one_time_tasks import get_completions, get_one_time_tasks
        WORKSPACE = current_app.config["WORKSPACE"]
        tasks = get_one_time_tasks(WORKSPACE)
        completions = get_completions(WORKSPACE)
        out = []
        for t in tasks:
            tid = t.get("id", "")
            out.append({
                "id": tid,
                "title": t.get("title", tid),
                "prompt": t.get("prompt", ""),
                "bonus_tokens": int(t.get("bonus_tokens", 0)),
                "completions_count": len(completions.get(tid, [])),
            })
        return jsonify({"success": True, "tasks": out})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/one_time_tasks", methods=["POST"])
def api_one_time_tasks_create():
    """Create or update a one-time-per-identity task."""
    data = request.get_json(force=True, silent=True) or {}
    try:
        from vivarium.runtime.one_time_tasks import add_one_time_task
        WORKSPACE = current_app.config["WORKSPACE"]
        result = add_one_time_task(WORKSPACE, data)
        if result.get("success"):
            return jsonify(result)
        return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/one_time_tasks/<task_id>", methods=["PATCH"])
def api_one_time_tasks_update(task_id):
    """Update a one-time task (e.g. bonus_tokens)."""
    try:
        from vivarium.runtime.one_time_tasks import update_one_time_task
        WORKSPACE = current_app.config["WORKSPACE"]
        data = request.json or {}
        result = update_one_time_task(WORKSPACE, task_id, data)
        if result.get("success"):
            return jsonify(result)
        return jsonify(result), 400 if result.get("error") != "task not found" else 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/one_time_tasks/<task_id>", methods=["DELETE"])
def api_one_time_tasks_delete(task_id):
    """Remove a one-time-per-identity task by id."""
    try:
        from vivarium.runtime.one_time_tasks import delete_one_time_task
        WORKSPACE = current_app.config["WORKSPACE"]
        result = delete_one_time_task(WORKSPACE, task_id)
        if result.get("success"):
            return jsonify(result)
        return jsonify(result), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ─── Task approve / requeue / remove ──────────────────────────────────────


@bp.route("/queue/task/approve", methods=["POST"])
def api_queue_task_approve():
    """Human approves a task that is pending_review; reward is granted, optional tip/feedback, task marked completed."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400
    _, get_human_username, _latest_execution_status, _dm_enrichment, _apply_queue_outcome = _queue_helpers()
    status, last_event = _latest_execution_status(task_id)
    if status != "pending_review":
        return jsonify({
            "success": False,
            "error": f"Task is not pending approval (status: {status})",
        }), 409
    identity_id = str(last_event.get("identity_id") or last_event.get("worker_id") or "").strip()
    QUEUE_FILE = current_app.config["QUEUE_FILE"]
    EXECUTION_LOG = current_app.config["EXECUTION_LOG"]
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    task = next((t for t in queue.get("tasks", []) if t.get("id") == task_id), None)
    if not task:
        return jsonify({"success": False, "error": "Task not found in queue"}), 404
    tip_tokens = max(0, int(data.get("tip_tokens") or 0))
    feedback = str(data.get("feedback") or "").strip()
    approved_record = {
        "task_id": task_id,
        "status": "approved",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "identity_id": identity_id,
        "approved_by": "human_operator",
        "tip_tokens": tip_tokens,
        "feedback_sent": bool(feedback),
    }
    append_jsonl(EXECUTION_LOG, approved_record)
    _apply_queue_outcome(task_id, "approved")
    from vivarium.runtime.worker_runtime import apply_phase5_reward_for_human_approval
    reward_out = apply_phase5_reward_for_human_approval(
        task_id=task_id,
        identity_id=identity_id,
        task=task,
        last_event=last_event,
        enrichment=_dm_enrichment(),
    )
    one_time_bonus_awarded = 0
    try:
        from vivarium.runtime.one_time_tasks import get_task_by_id, grant_and_record
        WORKSPACE = current_app.config["WORKSPACE"]
        if get_task_by_id(task_id, WORKSPACE):
            one_time_result = grant_and_record(
                WORKSPACE,
                task_id,
                identity_id,
                _dm_enrichment(),
            )
            if one_time_result.get("granted"):
                one_time_bonus_awarded = one_time_result.get("tokens", 0)
    except Exception:
        pass
    tip_awarded = 0
    if tip_tokens > 0 and identity_id:
        try:
            tip_result = _dm_enrichment().grant_free_time(
                identity_id, tip_tokens, reason="human_tip_excellence"
            )
            granted = (tip_result or {}).get("granted", {})
            tip_awarded = int(granted.get("free_time", 0)) + int(granted.get("journal", 0))
        except Exception:
            pass
    if feedback and identity_id:
        try:
            human_name = get_human_username()
            _dm_enrichment().post_direct_message(
                sender_id="human_operator",
                sender_name=human_name,
                recipient_id=identity_id,
                content=f"[Feedback on task {task_id}] {feedback}",
                importance=4,
            )
        except Exception:
            pass
    return jsonify({
        "success": True,
        "task_id": task_id,
        "reward_applied": reward_out.get("phase5_reward_applied"),
        "tokens_awarded": reward_out.get("phase5_reward_tokens_awarded", 0),
        "tip_awarded": tip_awarded,
        "one_time_bonus_awarded": one_time_bonus_awarded,
    })


@bp.route("/queue/task/requeue", methods=["POST"])
def api_queue_task_requeue():
    """Human sends task back for another attempt (try again); task stays in open queue."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400
    _, _, _latest_execution_status, _, _apply_queue_outcome = _queue_helpers()
    status, last_event = _latest_execution_status(task_id)
    if status != "pending_review":
        return jsonify({
            "success": False,
            "error": f"Task is not pending approval (status: {status})",
        }), 409
    QUEUE_FILE = current_app.config["QUEUE_FILE"]
    EXECUTION_LOG = current_app.config["EXECUTION_LOG"]
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    if not any(t.get("id") == task_id for t in queue.get("tasks", [])):
        return jsonify({"success": False, "error": "Task not found in queue"}), 404
    requeue_record = {
        "task_id": task_id,
        "status": "requeue",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "requested_by": "human_operator",
        "reason": "try_again",
    }
    append_jsonl(EXECUTION_LOG, requeue_record)
    _apply_queue_outcome(task_id, "requeue")
    return jsonify({"success": True, "task_id": task_id})


@bp.route("/queue/task/remove", methods=["POST"])
def api_queue_task_remove():
    """Human removes task from queue (mark as failed); resident does not get completion reward."""
    data = request.get_json(force=True, silent=True) or {}
    task_id = str(data.get("task_id") or "").strip()
    if not task_id:
        return jsonify({"success": False, "error": "task_id is required"}), 400
    _, _, _latest_execution_status, _, _apply_queue_outcome = _queue_helpers()
    status, last_event = _latest_execution_status(task_id)
    if status != "pending_review":
        return jsonify({
            "success": False,
            "error": f"Task is not pending approval (status: {status})",
        }), 409
    QUEUE_FILE = current_app.config["QUEUE_FILE"]
    EXECUTION_LOG = current_app.config["EXECUTION_LOG"]
    queue = normalize_queue(read_json(QUEUE_FILE, default={}))
    if not any(t.get("id") == task_id for t in queue.get("tasks", [])):
        return jsonify({"success": False, "error": "Task not found in queue"}), 404
    remove_record = {
        "task_id": task_id,
        "status": "failed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors": "Removed by human operator",
        "removed_by": "human_operator",
    }
    append_jsonl(EXECUTION_LOG, remove_record)
    _apply_queue_outcome(task_id, "failed")
    return jsonify({"success": True, "task_id": task_id})
