"""System blueprint: fresh_reset and maintenance endpoints."""
from __future__ import annotations

import shutil

from flask import Blueprint, jsonify, request

bp = Blueprint("system", __name__, url_prefix="/api")


def _app_helpers():
    from vivarium.runtime import control_panel_app as app
    return (
        app.get_worker_status,
        app._stop_workers_for_maintenance,
        app.write_json,
        app.CODE_ROOT,
        app.QUEUE_FILE,
        app.MUTABLE_SWARM_DIR,
        app.MESSAGES_TO_HUMAN,
        app.MESSAGES_FROM_HUMAN,
        app.MESSAGES_FROM_HUMAN_OUTBOX,
        app.WORKSPACE,
        app.ACTION_LOG,
        app.EXECUTION_LOG,
        app.API_AUDIT_LOG_FILE,
        app.LEGACY_API_AUDIT_LOG_FILE,
        app._reset_log_watcher_positions,
    )


@bp.route("/system/fresh_reset", methods=["POST"])
def api_system_fresh_reset():
    """Wipe stale runtime state and return system to clean baseline. Safety: refuses while swarm is running."""
    (
        get_worker_status,
        _stop_workers_for_maintenance,
        write_json,
        CODE_ROOT,
        QUEUE_FILE,
        MUTABLE_SWARM_DIR,
        MESSAGES_TO_HUMAN,
        MESSAGES_FROM_HUMAN,
        MESSAGES_FROM_HUMAN_OUTBOX,
        WORKSPACE,
        ACTION_LOG,
        EXECUTION_LOG,
        API_AUDIT_LOG_FILE,
        LEGACY_API_AUDIT_LOG_FILE,
        _reset_log_watcher_positions,
    ) = _app_helpers()

    body = request.get_json(force=True, silent=True) or {}
    worker = get_worker_status()
    if worker.get("running"):
        if bool(body.get("force_stop")):
            stop_result = _stop_workers_for_maintenance()
            if not stop_result.get("success"):
                return jsonify({
                    "success": False,
                    "error": "Could not stop all workers before fresh reset.",
                    "running_count": len(stop_result.get("remaining_pids", [])),
                    "remaining_pids": stop_result.get("remaining_pids", []),
                }), 409
        else:
            return jsonify({"success": False, "error": "Stop swarm before running fresh reset."}), 409

    try:
        fresh_queue = {
            "version": "1.0",
            "api_endpoint": "http://127.0.0.1:8420",
            "tasks": [],
            "completed": [],
            "failed": [],
        }
        write_json(QUEUE_FILE, fresh_queue)

        local_swarm_dir = CODE_ROOT / ".swarm"
        local_swarm_dir.mkdir(parents=True, exist_ok=True)
        write_json(local_swarm_dir / "resident_days.json", {})
        write_json(local_swarm_dir / "identity_locks.json", {"cycle_id": 0, "locks": {}})

        transient_files = [
            MUTABLE_SWARM_DIR / "completed_requests.json",
            MUTABLE_SWARM_DIR / "daily_wind_down_allowance.json",
            MUTABLE_SWARM_DIR / "free_time_balances.json",
            MUTABLE_SWARM_DIR / "human_request.json",
            MUTABLE_SWARM_DIR / "journal_rollups.json",
            MUTABLE_SWARM_DIR / "bounties.json",
            MUTABLE_SWARM_DIR / "guilds.json",
            MUTABLE_SWARM_DIR / "artifact_fingerprints.json",
            MUTABLE_SWARM_DIR / "phase5_reward_ledger.json",
            MUTABLE_SWARM_DIR / "creative_seed_used.json",
            MESSAGES_TO_HUMAN,
            MESSAGES_FROM_HUMAN,
            MESSAGES_FROM_HUMAN_OUTBOX,
            WORKSPACE / ".swarm" / "one_time_tasks.json",
            WORKSPACE / ".swarm" / "one_time_completions.json",
            ACTION_LOG,
            EXECUTION_LOG,
            API_AUDIT_LOG_FILE,
            LEGACY_API_AUDIT_LOG_FILE,
        ]
        for file_path in transient_files:
            try:
                if file_path.exists():
                    file_path.unlink()
            except OSError:
                pass

        _reset_log_watcher_positions()

        wipe_dirs = [
            MUTABLE_SWARM_DIR / "discussions",
            MUTABLE_SWARM_DIR / "journals",
            MUTABLE_SWARM_DIR / "identities",
            WORKSPACE / "library" / "community_library" / "resident_suggestions",
            WORKSPACE / "library" / "creative_works",
        ]
        for directory in wipe_dirs:
            try:
                if directory.exists():
                    shutil.rmtree(directory)
                directory.mkdir(parents=True, exist_ok=True)
            except OSError:
                pass

        return jsonify({"success": True})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
