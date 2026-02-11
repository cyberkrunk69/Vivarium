"""Rollback blueprint: preview and execute rollback by days."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from vivarium.runtime.vivarium_scope import CHANGE_JOURNAL_FILE, get_mutable_version_control

bp = Blueprint('rollback', __name__, url_prefix='/api')

ROLLBACK_DAYS_MIN = 1
ROLLBACK_DAYS_MAX = 180
ROLLBACK_AVAILABLE_DAYS_WINDOW = 14
ROLLBACK_AFFECTED_PREVIEW_MAX = 6
ROLLBACK_CHECKPOINT_SCAN_MAX = 10000


def _clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def _parse_utc_timestamp(raw: str):
    value = str(raw or "").strip()
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _load_checkpoint_events(limit: int = 5000) -> list[dict]:
    """Load checkpoint-created events from change journal."""
    if not CHANGE_JOURNAL_FILE.exists():
        return []
    events: list[dict] = []
    try:
        with open(CHANGE_JOURNAL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if payload.get("event") != "checkpoint_created":
                    continue
                commit_sha = str(payload.get("commit_sha") or "").strip()
                if not commit_sha:
                    continue
                ts = _parse_utc_timestamp(payload.get("timestamp"))
                if ts is None:
                    continue
                events.append(
                    {
                        "timestamp": ts,
                        "timestamp_iso": ts.isoformat(),
                        "day_tag": ts.date().isoformat(),
                        "task_id": str(payload.get("task_id") or ""),
                        "summary": str(payload.get("summary") or ""),
                        "commit_sha": commit_sha,
                    }
                )
    except OSError:
        return []
    events.sort(key=lambda item: item["timestamp"])
    if limit > 0 and len(events) > limit:
        events = events[-limit:]
    return events


def _rollback_preview_by_days(days: int) -> dict:
    now = datetime.now(timezone.utc)
    safe_days = _clamp_int(days, ROLLBACK_DAYS_MIN, ROLLBACK_DAYS_MAX)
    checkpoints = _load_checkpoint_events(limit=ROLLBACK_CHECKPOINT_SCAN_MAX)
    if not checkpoints:
        return {
            "success": False,
            "error": "No checkpoints available yet. Run tasks first so checkpoints are created.",
            "days": safe_days,
            "available_days": [],
        }

    cutoff = now - timedelta(days=safe_days)
    target = None
    for cp in checkpoints:
        if cp["timestamp"] <= cutoff:
            target = cp
        else:
            break
    if target is None:
        oldest = checkpoints[0]
        oldest_age_days = max(0.0, (now - oldest["timestamp"]).total_seconds() / 86400.0)
        return {
            "success": False,
            "error": (
                f"Not enough checkpoint history for {safe_days} day(s). "
                f"Oldest checkpoint is ~{oldest_age_days:.1f} day(s) old."
            ),
            "days": safe_days,
            "oldest_available_days": round(oldest_age_days, 2),
            "available_days": sorted({cp["day_tag"] for cp in checkpoints}, reverse=True)[:ROLLBACK_AVAILABLE_DAYS_WINDOW],
        }

    affected = [cp for cp in checkpoints if cp["timestamp"] > target["timestamp"]]
    recent_days = sorted({cp["day_tag"] for cp in checkpoints}, reverse=True)[:ROLLBACK_AVAILABLE_DAYS_WINDOW]
    return {
        "success": True,
        "days": safe_days,
        "target": {
            "commit_sha": target["commit_sha"],
            "timestamp": target["timestamp_iso"],
            "day_tag": target["day_tag"],
            "task_id": target["task_id"],
            "summary": target["summary"],
        },
        "checkpoints_total": len(checkpoints),
        "checkpoints_since_target": len(affected),
        "available_days": recent_days,
        "affected_preview": [
            {
                "day_tag": cp["day_tag"],
                "task_id": cp["task_id"],
                "summary": cp["summary"],
                "timestamp": cp["timestamp_iso"],
            }
            for cp in affected[-ROLLBACK_AFFECTED_PREVIEW_MAX:]
        ],
    }


def _rollback_helpers():
    """Lazy import from control_panel_app to avoid circular imports."""
    from vivarium.runtime.control_panel_app import (
        _stop_workers_for_maintenance,
        get_worker_status,
    )
    return get_worker_status, _stop_workers_for_maintenance


@bp.route('/rollback/preview', methods=['GET'])
def preview_rollback():
    """GET /api/rollback/preview?days=N - Show what would be affected."""
    raw_days = request.args.get("days", "1")
    try:
        days = int(raw_days)
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "days must be an integer"}), 400
    preview = _rollback_preview_by_days(days)
    status_code = 200 if preview.get("success") else 400
    return jsonify(preview), status_code


@bp.route('/rollback/by_days', methods=['POST'])
def rollback_by_days():
    """POST /api/rollback/by_days - Execute rollback."""
    body = request.get_json(force=True, silent=True) or {}
    raw_days = body.get("days", 1)
    reason = str(body.get("reason") or "").strip()
    try:
        days = int(raw_days)
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "days must be an integer"}), 400

    if days < ROLLBACK_DAYS_MIN or days > ROLLBACK_DAYS_MAX:
        return jsonify(
            {
                "success": False,
                "error": f"days must be between {ROLLBACK_DAYS_MIN} and {ROLLBACK_DAYS_MAX}",
            }
        ), 400

    get_worker_status, _stop_workers_for_maintenance = _rollback_helpers()
    worker_status = get_worker_status()
    if worker_status.get("running"):
        if bool(body.get("force_stop")):
            stop_result = _stop_workers_for_maintenance()
            if not stop_result.get("success"):
                return jsonify({
                    "success": False,
                    "error": "Could not stop all workers before rollback.",
                    "running_count": len(stop_result.get("remaining_pids", [])),
                    "remaining_pids": stop_result.get("remaining_pids", []),
                }), 409
        else:
            return jsonify({
                "success": False,
                "error": "Stop the swarm before rollback to avoid race conditions.",
                "running_count": worker_status.get("running_count", 0),
            }), 409

    preview = _rollback_preview_by_days(days)
    if not preview.get("success"):
        return jsonify(preview), 400

    target = preview.get("target") or {}
    commit_sha = str(target.get("commit_sha") or "").strip()
    if not commit_sha:
        return jsonify({"success": False, "error": "Could not resolve rollback target commit"}), 500

    rollback_reason = reason or f"UI rollback by {days} day(s)"
    try:
        vcs = get_mutable_version_control()
        ok = vcs.rollback_to(commit_sha=commit_sha, reason=rollback_reason)
    except Exception as exc:
        return jsonify({"success": False, "error": f"Rollback failed: {exc}"}), 500

    if not ok:
        return jsonify({"success": False, "error": "Rollback command did not complete successfully"}), 500

    return jsonify({
        "success": True,
        "days": days,
        "target": target,
        "message": "Rollback applied to mutable world state.",
    })
