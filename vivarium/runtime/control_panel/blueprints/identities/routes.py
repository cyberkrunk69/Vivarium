"""Identities blueprint: list, create, profile, and log endpoints."""
from __future__ import annotations

import json
import math
import secrets
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

from vivarium.runtime import resident_onboarding
from vivarium.utils import get_timestamp, read_json, write_json

bp = Blueprint("identities", __name__, url_prefix="/api")


def _calculate_identity_level(sessions: int) -> int:
    """Calculate identity level based on sessions (ARPG-style progression)."""
    return max(1, int(math.sqrt(sessions)))


def _calculate_respec_cost(sessions: int, respec_count: int = 0) -> int:
    """Calculate respec cost. First 3 changes are free; then BASE + (sessions * SCALE)."""
    RESPEC_FREE_CHANGES = 3
    if respec_count < RESPEC_FREE_CHANGES:
        return 0
    RESPEC_BASE_COST = 10
    RESPEC_SCALE_PER_SESSION = 3
    return RESPEC_BASE_COST + (sessions * RESPEC_SCALE_PER_SESSION)


def _parse_csv_items(raw: str, *, max_items: int = 10, max_len: int = 2000) -> list[str]:
    if not raw:
        return []
    items: list[str] = []
    for part in str(raw).split(","):
        value = part.strip()
        if not value:
            continue
        if len(value) > max_len:
            value = value[:max_len].rstrip()
        if value not in items:
            items.append(value)
        if len(items) >= max_items:
            break
    return items


def _fresh_hybrid_seed() -> str:
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    left = "".join(secrets.choice(letters) for _ in range(2))
    middle = "".join(secrets.choice("0123456789") for _ in range(4))
    right = "".join(secrets.choice(letters) for _ in range(2))
    return f"{left}-{middle}-{right}"


def _reserve_creativity_seed(seed: str) -> bool:
    pattern = current_app.config["CREATIVE_SEED_PATTERN"]
    used_file = current_app.config["CREATIVE_SEED_USED_FILE"]
    used_max = current_app.config["CREATIVE_SEED_USED_MAX"]
    normalized = str(seed or "").strip().upper()
    if not pattern.fullmatch(normalized):
        return False
    payload = read_json(used_file, default={})
    used = payload.get("used", {}) if isinstance(payload, dict) else {}
    if not isinstance(used, dict):
        used = {}
    if normalized in used:
        return False
    used[normalized] = get_timestamp()
    if len(used) > used_max:
        recent = sorted(used.items(), key=lambda item: item[1], reverse=True)[:used_max]
        used = {k: v for k, v in recent}
    write_json(used_file, {"used": used})
    return True


def _read_jsonl_tail(path: Path, max_lines: int = 12000) -> list:
    if not path.exists():
        return []
    lines = deque(maxlen=max_lines)
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                entry = line.strip()
                if entry:
                    lines.append(entry)
    except Exception:
        return []
    payloads = []
    for line in lines:
        try:
            payloads.append(json.loads(line))
        except Exception:
            continue
    return payloads


@bp.route("/identities", methods=["GET"])
def get_identities():
    """GET /api/identities - List all identities."""
    IDENTITIES_DIR = current_app.config["IDENTITIES_DIR"]
    FREE_TIME_BALANCES = current_app.config["FREE_TIME_BALANCES"]
    identities = []

    balances = {}
    if FREE_TIME_BALANCES.exists():
        try:
            with open(FREE_TIME_BALANCES) as f:
                balances = json.load(f)
        except Exception:
            pass

    if IDENTITIES_DIR.exists():
        for f in IDENTITIES_DIR.glob("*.json"):
            try:
                with open(f) as file:
                    data = json.load(file)
                    identity_id = data.get("id", f.stem)
                    attrs = data.get("attributes", {})
                    profile = attrs.get("profile", {})
                    core = attrs.get("core", {})
                    sessions = data.get("sessions_participated", 0)
                    respec_count = attrs.get("meta", {}).get("respec_count", 0)

                    identities.append({
                        "id": identity_id,
                        "name": data.get("name", "Unknown"),
                        "tokens": balances.get(identity_id, {}).get("tokens", 0),
                        "journal_tokens": balances.get(identity_id, {}).get("journal_tokens", 0),
                        "sessions": sessions,
                        "tasks_completed": data.get("tasks_completed", 0),
                        "profile_display": profile.get("display"),
                        "profile_thumbnail_html": profile.get("thumbnail_html"),
                        "profile_thumbnail_css": profile.get("thumbnail_css"),
                        "traits": core.get("personality_traits", []),
                        "values": core.get("core_values", []),
                        "level": _calculate_identity_level(sessions),
                        "respec_cost": _calculate_respec_cost(sessions, respec_count),
                    })
            except Exception:
                pass

    return jsonify(identities)


@bp.route("/creative_seed", methods=["GET"])
def get_creative_seed():
    """GET /api/creative_seed - Return a fresh hybrid creativity seed."""
    return jsonify({"success": True, "seed": _fresh_hybrid_seed()})


@bp.route("/identities/create", methods=["POST"])
def create_identity():
    """POST /api/identities/create - Create a resident-authored identity from UI input."""
    IDENTITIES_DIR = current_app.config["IDENTITIES_DIR"]
    WORKSPACE = current_app.config["WORKSPACE"]
    data = request.json or {}

    name = str(data.get("name", "")).strip()
    summary = str(data.get("summary", "")).strip()
    identity_statement = str(data.get("identity_statement", "")).strip()
    creativity_seed = str(data.get("creativity_seed", "")).strip().upper()
    creator_identity_id = str(data.get("creator_identity_id", "")).strip()
    creator_resident_id = str(data.get("creator_resident_id", "")).strip()

    if not name:
        return jsonify({"success": False, "error": "name is required"}), 400
    if len(name) > 80:
        return jsonify({"success": False, "error": "name is too long (max 80 chars)"}), 400
    if len(summary) > 600:
        return jsonify({"success": False, "error": "summary is too long (max 600 chars)"}), 400
    if not creativity_seed:
        creativity_seed = _fresh_hybrid_seed()
    pattern = current_app.config["CREATIVE_SEED_PATTERN"]
    if not pattern.fullmatch(creativity_seed):
        return jsonify({"success": False, "error": "invalid creativity seed format"}), 400
    if not _reserve_creativity_seed(creativity_seed):
        return jsonify({"success": False, "error": "creativity seed already used; request a fresh one"}), 409

    if creator_identity_id:
        creator_path = IDENTITIES_DIR / f"{creator_identity_id}.json"
        if not creator_path.exists():
            return jsonify({"success": False, "error": "creator_identity_id not found"}), 400

    if not creator_identity_id:
        creator_identity_id = "resident_identity_forge"
    if not creator_resident_id:
        creator_resident_id = f"resident_{creator_identity_id}"

    affinities = data.get("affinities")
    if not isinstance(affinities, list):
        affinities = _parse_csv_items(data.get("traits_csv", ""))
    else:
        affinities = _parse_csv_items(",".join(str(x) for x in affinities))

    values = data.get("values")
    if not isinstance(values, list):
        values = _parse_csv_items(data.get("values_csv", ""))
    else:
        values = _parse_csv_items(",".join(str(x) for x in values))

    activities = data.get("preferred_activities")
    if not isinstance(activities, list):
        activities = _parse_csv_items(data.get("activities_csv", ""))
    else:
        activities = _parse_csv_items(",".join(str(x) for x in activities))

    try:
        identity_id = resident_onboarding.create_identity_from_resident(
            workspace=WORKSPACE,
            creator_resident_id=creator_resident_id,
            creator_identity_id=creator_identity_id,
            name=name,
            summary=summary or "Creative self-authored resident identity.",
            affinities=affinities,
            values=values,
            preferred_activities=activities,
            identity_statement=identity_statement or summary,
            creativity_seed=creativity_seed,
        )
    except ValueError as exc:
        message = str(exc)
        retry = "TRY AGAIN" in message or "IDENTITY_NAME_RULE_VIOLATION" in message
        return jsonify({"success": False, "error": message, "retry": retry}), 400
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

    identity_file = IDENTITIES_DIR / f"{identity_id}.json"
    identity_name = name
    if identity_file.exists():
        try:
            with open(identity_file, "r", encoding="utf-8") as f:
                identity_name = json.load(f).get("name", name)
        except Exception:
            pass

    return jsonify({
        "success": True,
        "identity": {
            "id": identity_id,
            "name": identity_name,
            "summary": summary,
            "creator_identity_id": creator_identity_id,
            "creativity_seed": creativity_seed,
        },
    })


@bp.route("/identity/<identity_id>/profile", methods=["GET"])
def get_identity_profile(identity_id):
    """GET /api/identity/<id>/profile - Get detailed profile for an identity."""
    IDENTITIES_DIR = current_app.config["IDENTITIES_DIR"]
    WORKSPACE = current_app.config["WORKSPACE"]
    ACTION_LOG = current_app.config["ACTION_LOG"]
    FREE_TIME_BALANCES = current_app.config["FREE_TIME_BALANCES"]

    identity_file = IDENTITIES_DIR / f"{identity_id}.json"

    if not identity_file.exists():
        return jsonify({"error": "identity_not_found"})

    try:
        with open(identity_file) as f:
            data = json.load(f)

        attrs = data.get("attributes", {})
        profile = attrs.get("profile", {})
        core = attrs.get("core", {})
        mutable = attrs.get("mutable", {})

        journals_dir = WORKSPACE / ".swarm" / "journals"
        journals = []
        if journals_dir.exists():
            for jf in sorted(journals_dir.glob(f"{identity_id}*.md"), reverse=True)[:10]:
                try:
                    with open(jf, "r", encoding="utf-8") as jfile:
                        content = jfile.read()
                        journals.append({
                            "filename": jf.name,
                            "content": content,
                            "modified": datetime.fromtimestamp(jf.stat().st_mtime).isoformat(),
                        })
                except Exception:
                    pass

        recent_actions = []
        if ACTION_LOG.exists():
            try:
                with open(ACTION_LOG, "r") as f:
                    lines = f.readlines()[-200:]
                    for line in reversed(lines):
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("actor") == identity_id:
                                recent_actions.append({
                                    "timestamp": entry.get("timestamp"),
                                    "type": entry.get("action_type"),
                                    "action": entry.get("action"),
                                    "detail": entry.get("detail"),
                                })
                                if len(recent_actions) >= 20:
                                    break
                        except Exception:
                            pass
            except Exception:
                pass

        task_success_rate = 0
        if data.get("tasks_completed", 0) + data.get("tasks_failed", 0) > 0:
            task_success_rate = (
                data.get("tasks_completed", 0)
                / (data.get("tasks_completed", 0) + data.get("tasks_failed", 0))
                * 100
            )

        chat_history = []
        messages_file = WORKSPACE / ".swarm" / "messages_to_human.jsonl"
        responses_file = WORKSPACE / ".swarm" / "messages_from_human.json"
        if messages_file.exists():
            responses = {}
            if responses_file.exists():
                try:
                    with open(responses_file) as rf:
                        responses = json.load(rf)
                except Exception:
                    pass
            try:
                with open(messages_file, "r") as mf:
                    for line in mf:
                        if line.strip():
                            msg = json.loads(line)
                            if msg.get("from_id") == identity_id:
                                chat_entry = {
                                    "id": msg.get("id"),
                                    "content": msg.get("content"),
                                    "type": msg.get("type", "message"),
                                    "sent_at": msg.get("timestamp"),
                                    "response": responses.get(msg.get("id"), {}).get("response"),
                                    "responded_at": responses.get(msg.get("id"), {}).get("responded_at"),
                                }
                                chat_history.append(chat_entry)
            except Exception:
                pass

        sessions = data.get("sessions_participated", 0)
        respec_count = attrs.get("meta", {}).get("respec_count", 0)
        wallet_tokens = 0
        wallet_journal = 0
        if FREE_TIME_BALANCES.exists():
            try:
                with open(FREE_TIME_BALANCES) as bf:
                    bal = json.load(bf)
                id_bal = (bal or {}).get(identity_id, {})
                wallet_tokens = int(id_bal.get("tokens", 0) or 0)
                wallet_journal = int(id_bal.get("journal_tokens", 0) or 0)
            except Exception:
                pass

        return jsonify({
            "identity_id": identity_id,
            "name": data.get("name"),
            "created_at": data.get("created_at"),
            "sessions": sessions,
            "tasks_completed": data.get("tasks_completed", 0),
            "tasks_failed": data.get("tasks_failed", 0),
            "task_success_rate": round(task_success_rate, 1),
            "level": _calculate_identity_level(sessions),
            "respec_cost": _calculate_respec_cost(sessions, respec_count),
            "tokens": wallet_tokens,
            "journal_tokens": wallet_journal,
            "profile": profile,
            "core_summary": {
                "traits": core.get("personality_traits", []),
                "values": core.get("core_values", []),
                "identity_statement": core.get("identity_statement"),
                "communication_style": core.get("communication_style"),
            },
            "mutable": {
                "likes": mutable.get("likes", []),
                "dislikes": mutable.get("dislikes", []),
                "current_interests": mutable.get("current_interests", []),
                "current_mood": mutable.get("current_mood"),
                "current_focus": mutable.get("current_focus"),
                "working_style": mutable.get("working_style"),
            },
            "identity_document": data,
            "recent_memories": data.get("memories", [])[-5:],
            "journals": journals,
            "recent_actions": recent_actions,
            "expertise": data.get("expertise", {}),
            "chat_history": chat_history[-20:],
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@bp.route("/identity/<identity_id>/log", methods=["GET"])
def get_identity_log(identity_id):
    """GET /api/identity/<id>/log - Full log for this identity only."""
    ACTION_LOG = current_app.config["ACTION_LOG"]
    EXECUTION_LOG = current_app.config["EXECUTION_LOG"]

    identity_id = (identity_id or "").strip()
    if not identity_id:
        return jsonify({"success": False, "error": "identity_id required"}), 400
    limit = request.args.get("limit", 3000, type=int)
    safe_limit = max(1, min(10000, limit))
    cycle_id_param = request.args.get("cycle_id", type=int)

    cycle_seconds = resident_onboarding.get_resident_cycle_seconds()
    action_entries = _read_jsonl_tail(ACTION_LOG, max_lines=safe_limit * 2)
    execution_entries = _read_jsonl_tail(EXECUTION_LOG, max_lines=safe_limit * 2)

    def actor_matches(entry: dict) -> bool:
        actor = str(entry.get("actor") or entry.get("worker_id") or entry.get("identity_id") or "").strip()
        return actor == identity_id

    def ts_to_cycle(ts) -> int:
        if not ts:
            return 0
        try:
            t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return int(t.timestamp() // cycle_seconds)
        except Exception:
            return 0

    out = []
    seen = set()
    for raw in action_entries:
        if not actor_matches(raw):
            continue
        ts = raw.get("timestamp")
        cid = ts_to_cycle(ts)
        if cycle_id_param is not None and cid != cycle_id_param:
            continue
        key = (ts, raw.get("action_type"), raw.get("action"), raw.get("detail"))
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "timestamp": ts,
            "actor": raw.get("actor"),
            "action_type": raw.get("action_type"),
            "action": raw.get("action"),
            "detail": raw.get("detail"),
            "cycle_id": cid,
            "model": (raw.get("metadata") or {}).get("model"),
        })

    for raw in execution_entries:
        actor = raw.get("worker_id") or raw.get("identity_id") or "worker"
        if actor != identity_id:
            continue
        ts = raw.get("timestamp")
        cid = ts_to_cycle(ts)
        if cycle_id_param is not None and cid != cycle_id_param:
            continue
        detail = f"{raw.get('task_id', 'task')} | {raw.get('result_summary') or raw.get('errors') or ''}".strip()
        key = (ts, "EXECUTION", raw.get("status"), detail)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "timestamp": ts,
            "actor": actor,
            "action_type": "EXECUTION",
            "action": raw.get("status") or "event",
            "detail": detail,
            "cycle_id": cid,
            "model": raw.get("model"),
        })

    out.sort(key=lambda e: str(e.get("timestamp") or ""))
    entries = out[-safe_limit:]
    cycles_with_data = sorted(set(e["cycle_id"] for e in entries), reverse=True)[:50]
    return jsonify({
        "success": True,
        "identity_id": identity_id,
        "entries": entries,
        "cycle_seconds": round(cycle_seconds, 1),
        "cycles_with_data": cycles_with_data,
    })
