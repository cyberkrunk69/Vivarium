"""DM blueprint: resident-to-resident direct message threads and send."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

bp = Blueprint("dm", __name__, url_prefix="/api")


def _app_helpers():
    from vivarium.runtime import control_panel_app as app
    return (
        app._dm_enrichment,
        app.get_identities,
        app._clamp_int,
        app.DM_THREADS_DEFAULT_LIMIT,
        app.DM_MESSAGES_MAX_LIMIT,
    )


def _identity_name_map():
    _, get_identities, *_ = _app_helpers()
    return {item.get("id"): item.get("name") for item in get_identities() if item.get("id")}


@bp.route("/dm/threads/<identity_id>")
def api_dm_threads(identity_id):
    """List DM threads for one resident identity."""
    _dm_enrichment, _, _clamp_int, DM_THREADS_DEFAULT_LIMIT, _ = _app_helpers()
    ident = str(identity_id or "").strip()
    if not ident:
        return jsonify({"success": False, "error": "identity_id required"}), 400
    try:
        threads = _dm_enrichment().get_direct_threads(ident, limit=DM_THREADS_DEFAULT_LIMIT)
        names = _identity_name_map()
        for thread in threads:
            peer_id = thread.get("peer_id")
            if peer_id:
                thread["peer_name"] = names.get(peer_id, peer_id)
        return jsonify({"success": True, "identity_id": ident, "threads": threads})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@bp.route("/dm/messages")
def api_dm_messages():
    """Get DM messages between two identities."""
    _dm_enrichment, _, _clamp_int, _, DM_MESSAGES_MAX_LIMIT = _app_helpers()
    identity_id = str(request.args.get("identity_id") or "").strip()
    peer_id = str(request.args.get("peer_id") or "").strip()
    limit = request.args.get("limit", 100, type=int)
    if not identity_id or not peer_id:
        return jsonify({"success": False, "error": "identity_id and peer_id required"}), 400
    try:
        messages = _dm_enrichment().get_direct_messages(
            identity_id,
            peer_id,
            limit=_clamp_int(limit, 1, DM_MESSAGES_MAX_LIMIT),
        )
        return jsonify({"success": True, "identity_id": identity_id, "peer_id": peer_id, "messages": messages})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@bp.route("/dm/send", methods=["POST"])
def api_dm_send():
    """Send a resident-to-resident private DM."""
    _dm_enrichment, get_identities, _ = _app_helpers()
    names = {item.get("id"): item.get("name") for item in get_identities() if item.get("id")}
    data = request.get_json(force=True, silent=True) or {}
    from_id = str(data.get("from_id") or "").strip()
    to_id = str(data.get("to_id") or "").strip()
    content = str(data.get("content") or "").strip()
    if not from_id or not to_id:
        return jsonify({"success": False, "error": "from_id and to_id are required"}), 400
    if from_id == to_id:
        return jsonify({"success": False, "error": "from_id and to_id must differ"}), 400
    if not content:
        return jsonify({"success": False, "error": "content is required"}), 400
    try:
        result = _dm_enrichment().post_direct_message(
            sender_id=from_id,
            sender_name=names.get(from_id, from_id),
            recipient_id=to_id,
            content=content,
            importance=3,
        )
        if not result.get("success"):
            return jsonify({"success": False, "error": result.get("reason", "send_failed")}), 400
        return jsonify({"success": True, "room": result.get("room"), "message": result.get("message")})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
