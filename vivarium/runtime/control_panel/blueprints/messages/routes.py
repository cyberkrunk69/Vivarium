"""Messages blueprint: feed, respond, send, mailbox endpoints."""
from __future__ import annotations

import time
from datetime import datetime

from flask import Blueprint, jsonify, request

bp = Blueprint("messages", __name__, url_prefix="/api")


def _app_helpers():
    """Lazy import from control_panel_app to avoid circular imports."""
    from vivarium.runtime import control_panel_app as app

    return (
        app.get_messages_to_human,
        app.get_human_responses,
        app.get_human_username,
        app.get_human_outbox_messages,
        app.get_identities,
        app._dm_enrichment,
        app._enqueue_identity_task,
        app._append_human_outbox_message,
        app.MESSAGES_FEED_MAX,
        app.MAILBOX_MESSAGE_BONUS_TOKENS,
    )


@bp.route("/messages", methods=["GET"])
def get_messages():
    """GET /api/messages - Get messages from identities with any responses."""
    (
        get_messages_to_human,
        get_human_responses,
        get_human_username,
        *_,
        MESSAGES_FEED_MAX,
    ) = _app_helpers()

    messages = get_messages_to_human()
    responses = get_human_responses()

    for msg in messages:
        msg_id = msg.get("id", "")
        if msg_id in responses:
            msg["response"] = responses[msg_id]
        msg["human_username"] = get_human_username()

    return jsonify(list(reversed(messages[-MESSAGES_FEED_MAX:])))


@bp.route("/messages/respond", methods=["POST"])
def respond_to_message():
    """POST /api/messages/respond - Send a response to an identity message."""
    data = request.json
    message_id = data.get("message_id")
    response = data.get("response")

    if not message_id or not response:
        return jsonify({"success": False, "error": "Missing message_id or response"})

    from vivarium.runtime import control_panel_app as app

    result = app.save_human_response(message_id, response)
    return jsonify({"success": True, "responded_at": result["responded_at"]})


@bp.route("/messages/send", methods=["POST"])
def send_message():
    """POST /api/messages/send - Send a new outbound message from human to one resident (or broadcast)."""
    (
        get_human_username,
        _,
        _,
        _,
        _dm_enrichment,
        _enqueue_identity_task,
        _append_human_outbox_message,
        _,
        MAILBOX_MESSAGE_BONUS_TOKENS,
    ) = _app_helpers()

    data = request.get_json(force=True, silent=True) or {}
    content = str(data.get("content") or "").strip()
    to_id = str(data.get("to_id") or "").strip()
    to_name = str(data.get("to_name") or "").strip()
    if not content:
        return jsonify({"success": False, "error": "content is required"}), 400
    if len(content) > 1200:
        return jsonify({"success": False, "error": "content too long (max 1200 chars)"}), 400

    sender_name = get_human_username()
    safe_target = to_name or to_id or "all residents"
    try:
        chat_line = f"[to {safe_target}] {content}"
        _dm_enrichment().post_discussion_message(
            identity_id="human_operator",
            identity_name=sender_name,
            content=chat_line,
            room="human_async",
            mood="async",
            importance=4,
        )
        if to_id:
            _dm_enrichment().post_direct_message(
                sender_id="human_operator",
                sender_name=sender_name,
                recipient_id=to_id,
                content=content,
                importance=4,
            )
            _dm_enrichment().grant_free_time(
                to_id,
                MAILBOX_MESSAGE_BONUS_TOKENS,
                reason="human_message_received",
            )
            followup_task_id = f"mailbox-inbox-{to_id}-{int(time.time() * 1000)}"
            _enqueue_identity_task(
                task_id=followup_task_id,
                identity_id=to_id,
                prompt=(
                    "I received a new direct message from the human operator. "
                    f"Message: {content}\n"
                    "Process it, coordinate with other residents if useful, and take the best immediate next action."
                ),
                min_budget=0.03,
                max_budget=0.20,
            )
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

    outbox_payload = {
        "id": f"human_out_{int(time.time() * 1000)}",
        "message_id": None,
        "to_id": to_id or "",
        "to_name": safe_target,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "sender_name": sender_name,
        "source": "new_message",
    }
    _append_human_outbox_message(outbox_payload)
    return jsonify({"success": True, "message": outbox_payload})


@bp.route("/messages/mailbox", methods=["GET"])
def get_mailbox():
    """GET /api/messages/mailbox - Aggregate inbox/outbox threads for phone-style mailbox UI."""
    (
        get_messages_to_human,
        get_human_responses,
        get_human_username,
        get_human_outbox_messages,
        get_identities,
        *_,
    ) = _app_helpers()

    inbound = get_messages_to_human()
    responses = get_human_responses()
    outbox = get_human_outbox_messages()
    identities = get_identities()
    identity_map = {
        str(i.get("id") or ""): str(i.get("name") or i.get("id") or "")
        for i in identities
    }

    threads = {}
    now = datetime.now().isoformat()

    def _touch_thread(thread_id: str, thread_name: str):
        if thread_id not in threads:
            threads[thread_id] = {
                "id": thread_id,
                "name": thread_name or thread_id or "Resident",
                "unread": 0,
                "last_at": "",
                "last_preview": "",
                "messages": [],
            }
        return threads[thread_id]

    _PLACEHOLDER_IDS = frozenset({"identity_phase5", "worker", "resident"})
    execution_log_tasks = {}
    try:
        from vivarium.runtime.worker_runtime import read_execution_log

        execution_log_tasks = read_execution_log().get("tasks", {})
    except Exception:
        pass

    seen_task_approvals = set()
    for msg in inbound:
        from_id = str(msg.get("from_id") or "").strip()
        from_name = (
            str(msg.get("from_name") or "").strip()
            or identity_map.get(from_id)
            or from_id
            or "resident"
        )
        if (
            from_id.lower() in _PLACEHOLDER_IDS
            and msg.get("type") == "task_pending_approval"
            and msg.get("task_id")
        ):
            tid = str(msg.get("task_id") or "")
            ev = execution_log_tasks.get(tid, {})
            ev_id = str(ev.get("identity_id") or "").strip()
            ev_name = str(ev.get("identity_name") or "").strip()
            if ev_id and ev_id.lower() not in _PLACEHOLDER_IDS:
                from_id = ev_id
                from_name = ev_name or identity_map.get(ev_id) or ev_id
        thread_id = from_id or f"name::{from_name.lower()}"
        thread = _touch_thread(thread_id, from_name)
        if msg.get("type") == "task_pending_approval" and msg.get("task_id"):
            tid = str(msg.get("task_id") or "")
            if tid in seen_task_approvals:
                continue
            seen_task_approvals.add(tid)
        timestamp = str(msg.get("timestamp") or now)
        content = str(msg.get("content") or "")
        responded = str(msg.get("id") or "") in responses
        msg_payload = {
            "direction": "in",
            "id": str(msg.get("id") or ""),
            "timestamp": timestamp,
            "content": content,
            "author_name": from_name,
            "responded": responded,
        }
        if msg.get("type") == "task_pending_approval" and msg.get("task_id"):
            msg_payload["type"] = "task_pending_approval"
            msg_payload["task_id"] = str(msg.get("task_id") or "")
        thread["messages"].append(msg_payload)
        if not responded:
            thread["unread"] += 1
        if timestamp >= (thread.get("last_at") or ""):
            thread["last_at"] = timestamp
            thread["last_preview"] = content

    for msg in outbox:
        to_id = str(msg.get("to_id") or "").strip()
        to_name = (
            str(msg.get("to_name") or "").strip()
            or identity_map.get(to_id)
            or to_id
            or "all residents"
        )
        thread_id = to_id or "__broadcast__"
        thread = _touch_thread(thread_id, to_name)
        timestamp = str(msg.get("timestamp") or now)
        content = str(msg.get("content") or "")
        thread["messages"].append(
            {
                "direction": "out",
                "id": str(msg.get("id") or ""),
                "timestamp": timestamp,
                "content": content,
                "author_name": str(msg.get("sender_name") or get_human_username()),
                "responded": True,
            }
        )
        if timestamp >= (thread.get("last_at") or ""):
            thread["last_at"] = timestamp
            thread["last_preview"] = f"↗ {content}"

    thread_list = list(threads.values())
    for t in thread_list:
        t["messages"] = sorted(t.get("messages", []), key=lambda m: str(m.get("timestamp") or ""))
    thread_list.sort(key=lambda t: str(t.get("last_at") or ""), reverse=True)

    unread_total = sum(int(t.get("unread", 0)) for t in thread_list)
    return jsonify(
        {
            "success": True,
            "unread_count": unread_total,
            "threads": [
                {
                    "id": t.get("id"),
                    "name": t.get("name"),
                    "unread": t.get("unread", 0),
                    "last_at": t.get("last_at"),
                    "last_preview": t.get("last_preview", ""),
                }
                for t in thread_list
            ],
            "thread_messages": {str(t.get("id")): t.get("messages", []) for t in thread_list},
            "identities": [
                {"id": str(i.get("id") or ""), "name": str(i.get("name") or i.get("id") or "")}
                for i in identities
                if i.get("id")
            ],
            "human_name": get_human_username(),
        }
    )
