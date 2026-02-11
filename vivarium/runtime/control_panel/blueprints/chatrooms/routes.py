"""Chatrooms blueprint: watercooler, town hall, etc."""
from __future__ import annotations

import json

from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("chatrooms", __name__, url_prefix="/api")

ROOM_INFO = {
    "watercooler": {"name": "Break Room", "icon": "☕", "description": "Casual chat, status updates"},
    "town_hall": {"name": "Town Hall", "icon": "🏛️", "description": "Proposals, votes, community decisions"},
    "human_async": {"name": "Human Async", "icon": "🕰️", "description": "Async group chat with the human operator"},
    "improvements": {"name": "Improvements", "icon": "💡", "description": "System enhancement ideas"},
    "struggles": {"name": "Struggles", "icon": "🤔", "description": "Challenges and help requests"},
    "discoveries": {"name": "Discoveries", "icon": "✨", "description": "Interesting findings"},
    "project_war_room": {"name": "War Room", "icon": "⚔️", "description": "Active project coordination"},
}


def _get_discussions_dir():
    return current_app.config["DISCUSSIONS_DIR"]


@bp.route("/chatrooms")
def api_get_chatrooms():
    """Get list of available chat rooms with message counts."""
    DISCUSSIONS_DIR = _get_discussions_dir()
    rooms = []
    if DISCUSSIONS_DIR.exists():
        for room_file in DISCUSSIONS_DIR.glob("*.jsonl"):
            room_name = room_file.stem
            if room_name.startswith("town_hall_") or room_name.startswith("permanent"):
                continue
            info = ROOM_INFO.get(room_name, {"name": room_name.title(), "icon": "💬", "description": ""})
            message_count = 0
            latest_timestamp = None
            latest_preview = None
            try:
                with open(room_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    message_count = len([l for l in lines if l.strip()])
                    if lines:
                        for line in reversed(lines):
                            if line.strip():
                                msg = json.loads(line)
                                latest_timestamp = msg.get("timestamp")
                                author = msg.get("author_name", "Unknown")
                                content = msg.get("content", "") or ""
                                latest_preview = f"{author}: {content}"
                                break
            except Exception:
                pass
            rooms.append({
                "id": room_name,
                "name": info["name"],
                "icon": info["icon"],
                "description": info["description"],
                "message_count": message_count,
                "latest_timestamp": latest_timestamp,
                "latest_preview": latest_preview,
            })
    rooms.sort(key=lambda r: r.get("latest_timestamp") or "", reverse=True)
    return jsonify({"success": True, "rooms": rooms})


@bp.route("/chatrooms/<room_id>")
def api_get_chatroom_messages(room_id):
    """Get messages from a specific chat room."""
    DISCUSSIONS_DIR = _get_discussions_dir()
    limit = request.args.get("limit", 50, type=int)
    if not DISCUSSIONS_DIR.exists():
        return jsonify({"success": True, "messages": [], "room": room_id})
    room_file = DISCUSSIONS_DIR / f"{room_id}.jsonl"
    if not room_file.exists():
        return jsonify({"success": True, "messages": [], "room": room_id})
    messages = []
    try:
        with open(room_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    info = ROOM_INFO.get(room_id, {"name": room_id.title(), "icon": "💬", "description": ""})
    return jsonify({
        "success": True,
        "room": room_id,
        "room_name": info["name"],
        "room_icon": info["icon"],
        "messages": messages[-limit:],
    })
