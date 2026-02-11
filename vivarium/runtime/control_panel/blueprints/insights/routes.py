"""Insights blueprint: aggregate queue/execution/social/safety signals for quick UI scanning."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone

from flask import Blueprint, current_app, jsonify

bp = Blueprint("insights", __name__, url_prefix="/api")


def _app_helpers():
    from vivarium.runtime import control_panel_app as app
    from vivarium.runtime.control_panel.blueprints.bounties.routes import load_bounties
    from vivarium.runtime.control_panel.blueprints.stop_toggle import get_stop_status
    return (
        app.QUEUE_FILE,
        app.EXECUTION_LOG,
        app.ACTION_LOG,
        app.DISCUSSIONS_DIR,
        app.INSIGHTS_SOCIAL_UNREAD_WARN,
        app._read_jsonl_tail,
        app._read_api_audit_entries,
        app._parse_iso_timestamp,
        app._extract_usd_cost,
        app._count_discussion_messages_since,
        app._trend_snapshot,
        app._format_usd_display,
        app.get_identities,
        app.get_messages_to_human,
        app.get_human_responses,
        app.load_ui_settings,
        load_bounties,
        get_stop_status,
    )


@bp.route("/insights")
def api_insights():
    """Aggregate queue/execution/social/safety signals for quick UI scanning."""
    (
        QUEUE_FILE,
        EXECUTION_LOG,
        ACTION_LOG,
        DISCUSSIONS_DIR,
        INSIGHTS_SOCIAL_UNREAD_WARN,
        _read_jsonl_tail,
        _read_api_audit_entries,
        _parse_iso_timestamp,
        _extract_usd_cost,
        _count_discussion_messages_since,
        _trend_snapshot,
        _format_usd_display,
        get_identities,
        get_messages_to_human,
        get_human_responses,
        load_ui_settings,
        load_bounties,
        get_stop_status,
    ) = _app_helpers()

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)

    queue = {}
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                queue = json.load(f)
        except Exception:
            queue = {}
    queue_tasks = queue.get("tasks", []) if isinstance(queue.get("tasks"), list) else []
    queue_completed = queue.get("completed", []) if isinstance(queue.get("completed"), list) else []
    queue_failed = queue.get("failed", []) if isinstance(queue.get("failed"), list) else []
    queue_summary = {"open": len(queue_tasks), "completed": len(queue_completed), "failed": len(queue_failed)}

    execution_entries = _read_jsonl_tail(EXECUTION_LOG)
    completed_24h = approved_24h = failed_24h = requeue_24h = pending_review_24h = 0
    last_event_at = None
    for entry in execution_entries:
        status = str(entry.get("status") or "").strip().lower()
        timestamp = _parse_iso_timestamp(entry.get("timestamp"))
        if timestamp and (last_event_at is None or timestamp > last_event_at):
            last_event_at = timestamp
        if not timestamp or timestamp < cutoff:
            continue
        if status in {"completed", "approved"}:
            completed_24h += 1
        if status == "approved":
            approved_24h += 1
        if status == "failed":
            failed_24h += 1
        if status == "requeue":
            requeue_24h += 1
        if status == "pending_review":
            pending_review_24h += 1

    failure_streak = 0
    for entry in reversed(execution_entries):
        status = str(entry.get("status") or "").strip().lower()
        if not status:
            continue
        if status == "failed":
            failure_streak += 1
            continue
        if status in {"in_progress", "pending_review", "requeue"}:
            continue
        break

    reviewed_total = approved_24h + failed_24h + requeue_24h
    approval_rate_24h = round((approved_24h / reviewed_total) * 100, 1) if reviewed_total > 0 else None
    execution_summary = {
        "completed_24h": completed_24h,
        "approved_24h": approved_24h,
        "failed_24h": failed_24h,
        "requeue_24h": requeue_24h,
        "pending_review_24h": pending_review_24h,
        "approval_rate_24h": approval_rate_24h,
        "failure_streak": failure_streak,
        "last_event_at": last_event_at.isoformat() if last_event_at else None,
    }

    execution_cost_all_time = sum(
        float(e.get("budget_used"))
        for e in execution_entries
        if e.get("budget_used") is not None
    )

    action_entries = _read_jsonl_tail(ACTION_LOG, max_lines=60000)
    api_audit_entries = _read_api_audit_entries(max_lines=60000)
    action_cost_all_time = sum(
        _extract_usd_cost(e.get("detail", ""))
        for e in action_entries
        if str(e.get("action_type") or "").strip().upper() == "API"
    )

    api_calls_24h = api_cost_24h = safety_blocks_24h = errors_24h = 0
    actor_counter = Counter()
    action_type_timestamps = {}
    for entry in action_entries:
        timestamp = _parse_iso_timestamp(entry.get("timestamp"))
        if not timestamp:
            continue
        action_type = str(entry.get("action_type") or "").strip().upper() or "UNKNOWN"
        action_type_timestamps.setdefault(action_type, []).append(timestamp)
        if timestamp < cutoff:
            continue
        actor = str(entry.get("actor") or "").strip()
        action_blob = f"{entry.get('action', '')} {entry.get('detail', '')}".upper()
        if actor and actor not in {"SYSTEM", "UNKNOWN"}:
            actor_counter[actor] += 1
        if action_type == "API":
            api_calls_24h += 1
            api_cost_24h += _extract_usd_cost(entry.get("detail", ""))
        if action_type == "SAFETY" and "BLOCKED" in action_blob:
            safety_blocks_24h += 1
        if action_type == "ERROR":
            errors_24h += 1

    for entry in execution_entries:
        timestamp = _parse_iso_timestamp(entry.get("timestamp"))
        if not timestamp or timestamp < cutoff:
            continue
        budget_used = entry.get("budget_used")
        if budget_used is not None:
            try:
                api_cost_24h += float(budget_used)
            except (TypeError, ValueError):
                pass

    api_calls_24h_from_audit = 0
    api_cost_24h_from_audit = api_cost_all_time_from_audit = 0.0
    for entry in api_audit_entries:
        try:
            cost_val = float(entry.get("cost", 0))
        except (TypeError, ValueError):
            cost_val = 0.0
        api_cost_all_time_from_audit += cost_val
        ts = _parse_iso_timestamp(entry.get("timestamp"))
        if ts and ts >= cutoff:
            api_calls_24h_from_audit += 1
            api_cost_24h_from_audit += cost_val

    if api_calls_24h == 0 and api_calls_24h_from_audit > 0:
        api_calls_24h = api_calls_24h_from_audit
    if api_cost_24h == 0.0 and api_cost_24h_from_audit > 0:
        api_cost_24h = api_cost_24h_from_audit
    if action_cost_all_time == 0.0 and api_cost_all_time_from_audit > 0:
        action_cost_all_time = api_cost_all_time_from_audit

    ops_summary = {
        "api_calls_24h": api_calls_24h,
        "api_cost_24h": round(api_cost_24h, 6),
        "api_cost_all_time": round(execution_cost_all_time + action_cost_all_time, 6),
        "safety_blocks_24h": safety_blocks_24h,
        "errors_24h": errors_24h,
    }

    budget_events_24h = sum(1 for ts in action_type_timestamps.get("BUDGET", []) if ts >= cutoff)
    ui_settings = load_ui_settings()
    task_min_budget = float(ui_settings.get("task_min_budget", 0.05) or 0.05)
    task_max_budget = float(ui_settings.get("task_max_budget", max(task_min_budget, 0.10)) or max(task_min_budget, 0.10))
    if task_max_budget < task_min_budget:
        task_max_budget = task_min_budget
    queue_budget_exposure = 0.0
    for task in queue_tasks:
        try:
            queue_budget_exposure += float(task.get("max_budget", task.get("budget", 0.0)) or 0.0)
        except Exception:
            continue

    identities = get_identities()
    identity_name_map = {item.get("id"): item.get("name") for item in identities}
    active_identity_ids = {
        actor for actor in actor_counter
        if actor in identity_name_map or actor.startswith("identity_")
    }
    top_actor = None
    if actor_counter:
        actor_id, actor_actions = actor_counter.most_common(1)[0]
        top_actor = {"id": actor_id, "name": identity_name_map.get(actor_id) or actor_id, "actions": actor_actions}
    identities_summary = {"count": len(identities), "active_24h": len(active_identity_ids), "top_actor": top_actor}

    messages = get_messages_to_human()
    responses = get_human_responses()
    unread_messages = sum(1 for msg in messages if msg.get("id") and msg.get("id") not in responses)
    bounties = load_bounties()
    open_bounties = len([b for b in bounties if b.get("status") == "open"])
    claimed_bounties = len([b for b in bounties if b.get("status") == "claimed"])
    completed_bounties = len([b for b in bounties if b.get("status") == "completed"])
    social_summary = {
        "total_messages": len(messages),
        "unread_messages": unread_messages,
        "open_bounties": open_bounties,
        "claimed_bounties": claimed_bounties,
        "completed_bounties": completed_bounties,
        "chat_messages_24h": _count_discussion_messages_since(cutoff),
    }

    backlog_pressure = "low"
    if queue_summary["open"] >= 12:
        backlog_pressure = "high"
    elif queue_summary["open"] >= 5:
        backlog_pressure = "medium"

    kill_switch = get_stop_status()
    health_state = "stable"
    if kill_switch:
        health_state = "critical"
    elif (
        execution_summary["failure_streak"] >= 3
        or execution_summary["failed_24h"] > max(1, execution_summary["completed_24h"])
        or ops_summary["safety_blocks_24h"] > 0
    ):
        health_state = "watch"
    if (
        execution_summary["failure_streak"] >= 6
        or ops_summary["errors_24h"] >= 5
        or ops_summary["safety_blocks_24h"] >= 3
    ):
        health_state = "critical"

    health_summary = {"state": health_state, "kill_switch": kill_switch, "backlog_pressure": backlog_pressure}

    dm_timestamps = []
    if DISCUSSIONS_DIR.exists():
        for room_file in DISCUSSIONS_DIR.glob("dm__*.jsonl"):
            try:
                with open(room_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            payload = json.loads(line)
                        except Exception:
                            continue
                        ts = _parse_iso_timestamp(payload.get("timestamp"))
                        if ts:
                            dm_timestamps.append(ts)
            except Exception:
                continue

    metric_cards = []
    queue_open = int(queue_summary["open"])
    queue_tone = "warn" if queue_open >= 8 else "teal"
    metric_cards.append({
        "id": "queue",
        "label": "Queue",
        "headline": str(queue_open),
        "subline": f"{queue_summary['completed']} completed • {queue_summary['failed']} failed",
        "tone": queue_tone,
        "details": [f"Open tasks: {queue_summary['open']}", f"Completed tasks: {queue_summary['completed']}", f"Failed tasks: {queue_summary['failed']}", f"Backlog pressure: {backlog_pressure}"],
    })

    throughput_tone = "bad" if failed_24h > completed_24h else ("good" if completed_24h > 0 else "")
    metric_cards.append({
        "id": "throughput",
        "label": "Throughput (24h)",
        "headline": f"{completed_24h} / {failed_24h}",
        "subline": "completed / failed",
        "tone": throughput_tone,
        "details": [f"Completed: {completed_24h}", f"Failed: {failed_24h}", f"Requeue: {requeue_24h}", f"Pending review: {pending_review_24h}", f"Failure streak: {failure_streak}"],
    })

    quality_headline = "--" if approval_rate_24h is None else f"{approval_rate_24h:.1f}%"
    quality_tone = "good" if (approval_rate_24h or 0) >= 85 else ("warn" if (approval_rate_24h or 0) >= 60 else ("bad" if approval_rate_24h else ""))
    metric_cards.append({
        "id": "quality",
        "label": "Quality (24h)",
        "headline": quality_headline,
        "subline": f"{approved_24h} approved • {pending_review_24h} pending",
        "tone": quality_tone,
        "details": [f"Approval rate: {quality_headline}", f"Approved: {approved_24h}", f"Pending review: {pending_review_24h}", f"Requeue: {requeue_24h}", f"Last execution event: {execution_summary['last_event_at'] or 'n/a'}"],
    })

    cost_tone = "warn" if api_cost_24h > 1.0 else ("teal" if api_cost_24h > 0 else "")
    metric_cards.append({
        "id": "cost_api",
        "label": "Cost + API (24h)",
        "headline": _format_usd_display(api_cost_24h),
        "subline": f"{api_calls_24h} API calls",
        "tone": cost_tone,
        "details": [f"API cost (24h): ${api_cost_24h:.6f}", f"API calls (24h): {api_calls_24h}", f"Safety blocks (24h): {safety_blocks_24h}", f"Errors (24h): {errors_24h}"],
    })

    spend_queue_tone = "warn" if queue_budget_exposure > 1.0 else ("teal" if (api_cost_24h > 0 or queue_budget_exposure > 0) else "")
    metric_cards.append({
        "id": "spend_queue",
        "label": "Spend + Queue",
        "headline": _format_usd_display(api_cost_24h),
        "subline": f"all-time {_format_usd_display(execution_cost_all_time + action_cost_all_time)} • queue est ${queue_budget_exposure:.2f}",
        "tone": spend_queue_tone,
        "details": [
            f"API cost (24h): ${api_cost_24h:.6f}",
            f"API cost (all-time): ${execution_cost_all_time + action_cost_all_time:.6f}",
            f"Budget actions (24h): {budget_events_24h}",
            f"Queued budget exposure: ${queue_budget_exposure:.4f}",
            f"Per-task default range: ${task_min_budget:.2f} - ${task_max_budget:.2f}",
        ],
    })

    safety_tone = "bad" if (safety_blocks_24h > 0 or errors_24h > 0) else "good"
    metric_cards.append({
        "id": "safety_errors",
        "label": "Safety + Errors (24h)",
        "headline": f"{safety_blocks_24h} / {errors_24h}",
        "subline": "blocked safety / errors",
        "tone": safety_tone,
        "details": [f"Safety blocks: {safety_blocks_24h}", f"Errors: {errors_24h}", f"Kill switch: {'ON' if kill_switch else 'OFF'}", f"Health state: {health_state.upper()}"],
    })

    metric_cards.append({
        "id": "social",
        "label": "Social",
        "headline": str(unread_messages),
        "subline": f"{open_bounties} open • {claimed_bounties} claimed bounties",
        "tone": "warn" if unread_messages > INSIGHTS_SOCIAL_UNREAD_WARN else ("teal" if unread_messages > 0 else ""),
        "details": [f"Unread human messages: {unread_messages}", f"Open bounties: {open_bounties}", f"Claimed bounties: {claimed_bounties}", f"Completed bounties: {completed_bounties}", f"Discussion messages (24h): {social_summary['chat_messages_24h']}"],
    })

    top_actor_name = (top_actor or {}).get("name") or "none"
    top_actor_actions = int((top_actor or {}).get("actions") or 0)
    metric_cards.append({
        "id": "identities",
        "label": "Active Identities (24h)",
        "headline": f"{identities_summary['active_24h']}/{identities_summary['count']}",
        "subline": f"top actor: {top_actor_name}",
        "tone": "good" if identities_summary["active_24h"] > 0 else "",
        "details": [f"Active identities (24h): {identities_summary['active_24h']}", f"Total identities: {identities_summary['count']}", f"Top actor: {top_actor_name} ({top_actor_actions} actions)"],
    })

    metric_cards.append({
        "id": "health",
        "label": "Swarm Health",
        "headline": health_state.upper(),
        "subline": f"backlog {backlog_pressure} • streak {failure_streak}",
        "tone": "good" if health_state == "stable" else ("warn" if health_state == "watch" else "bad"),
        "details": [f"Health state: {health_state.upper()}", f"Backlog pressure: {backlog_pressure}", f"Failure streak: {failure_streak}", f"Kill switch: {'ON' if kill_switch else 'OFF'}"],
    })

    dm_trends = _trend_snapshot(dm_timestamps, now)
    metric_cards.append({
        "id": "dm_activity",
        "label": "DM Activity",
        "headline": str(dm_trends["day"]),
        "subline": f"day sends • week {dm_trends['week']} • month {dm_trends['month']}",
        "tone": "teal" if dm_trends["day"] > 0 else "",
        "details": [
            f"DMs today: {dm_trends['day']}",
            f"DMs this week: {dm_trends['week']}",
            f"DMs this month: {dm_trends['month']}",
            f"Day change vs 3-week baseline: {dm_trends['day_trend_3w_pct'] if dm_trends['day_trend_3w_pct'] is not None else 'n/a'}%",
            f"Day change vs 3-month baseline: {dm_trends['day_trend_3m_pct'] if dm_trends['day_trend_3m_pct'] is not None else 'n/a'}%",
        ],
    })

    for action_type in sorted(action_type_timestamps.keys()):
        snapshot = _trend_snapshot(action_type_timestamps[action_type], now)
        tone = "teal" if snapshot["day"] > 0 else ""
        if action_type in {"ERROR"} and snapshot["day"] > 0:
            tone = "bad"
        if action_type in {"SAFETY", "BUDGET"} and snapshot["day"] > 0:
            tone = "warn"
        metric_cards.append({
            "id": f"action_{action_type.lower()}",
            "label": f"Action: {action_type}",
            "headline": str(snapshot["day"]),
            "subline": f"day • week {snapshot['week']} • month {snapshot['month']}",
            "tone": tone,
            "details": [
                f"{action_type} today: {snapshot['day']}",
                f"{action_type} this week: {snapshot['week']}",
                f"{action_type} this month: {snapshot['month']}",
                f"Day change vs 3-week baseline: {snapshot['day_trend_3w_pct'] if snapshot['day_trend_3w_pct'] is not None else 'n/a'}%",
                f"Day change vs 3-month baseline: {snapshot['day_trend_3m_pct'] if snapshot['day_trend_3m_pct'] is not None else 'n/a'}%",
            ],
        })

    return jsonify({
        "success": True,
        "timestamp": now.isoformat(),
        "queue": queue_summary,
        "execution": execution_summary,
        "ops": ops_summary,
        "social": social_summary,
        "identities": identities_summary,
        "health": health_summary,
        "metric_cards": metric_cards,
    })
