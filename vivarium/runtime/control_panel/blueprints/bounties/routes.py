"""Bounties blueprint: list, create, delete, submit, list submissions, complete & reward."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

CRUCIBLE_NAME = "Commons Crucible"
DEFAULT_SLOT_POLICY = {
    "overflow_decay": 0.5,
    "min_multiplier": 0.05,
    "in_slot_multiplier": 1.0,
    "min_description_chars": 20,
    "allow_artifact_override": True,
    "max_rewarded_submissions_per_identity": 1,
}

bp = Blueprint("bounties", __name__, url_prefix="/api")


def _get_bounties_file() -> Path:
    return current_app.config["WORKSPACE"] / ".swarm" / "bounties.json"


def _get_slots_for_bounty(bounty: dict) -> int:
    slots = bounty.get("slots", bounty.get("max_teams", 1))
    try:
        return max(1, int(slots))
    except (TypeError, ValueError):
        return 1


def _normalize_slot_policy(policy):
    merged = DEFAULT_SLOT_POLICY.copy()
    if isinstance(policy, dict):
        for key in DEFAULT_SLOT_POLICY:
            if key in policy:
                merged[key] = policy[key]
    try:
        merged["overflow_decay"] = float(merged["overflow_decay"])
    except (TypeError, ValueError):
        merged["overflow_decay"] = DEFAULT_SLOT_POLICY["overflow_decay"]
    merged["overflow_decay"] = max(0.1, min(0.95, merged["overflow_decay"]))
    try:
        merged["min_multiplier"] = float(merged["min_multiplier"])
    except (TypeError, ValueError):
        merged["min_multiplier"] = DEFAULT_SLOT_POLICY["min_multiplier"]
    merged["min_multiplier"] = max(0.0, min(1.0, merged["min_multiplier"]))
    try:
        merged["in_slot_multiplier"] = float(merged["in_slot_multiplier"])
    except (TypeError, ValueError):
        merged["in_slot_multiplier"] = DEFAULT_SLOT_POLICY["in_slot_multiplier"]
    merged["in_slot_multiplier"] = max(0.1, min(2.0, merged["in_slot_multiplier"]))
    try:
        merged["min_description_chars"] = int(merged["min_description_chars"])
    except (TypeError, ValueError):
        merged["min_description_chars"] = DEFAULT_SLOT_POLICY["min_description_chars"]
    merged["min_description_chars"] = max(0, merged["min_description_chars"])
    try:
        merged["max_rewarded_submissions_per_identity"] = int(
            merged["max_rewarded_submissions_per_identity"]
        )
    except (TypeError, ValueError):
        merged["max_rewarded_submissions_per_identity"] = (
            DEFAULT_SLOT_POLICY["max_rewarded_submissions_per_identity"]
        )
    merged["max_rewarded_submissions_per_identity"] = max(
        1, merged["max_rewarded_submissions_per_identity"]
    )
    merged["allow_artifact_override"] = bool(merged.get("allow_artifact_override", True))
    return merged


def _compute_slot_multiplier(slot_index: int, slots: int, policy: dict) -> float:
    if slots <= 0 or slot_index <= slots:
        return float(policy.get("in_slot_multiplier", 1.0))
    overflow = max(0, slot_index - slots)
    decay = float(policy.get("overflow_decay", 0.5))
    multiplier = float(policy.get("in_slot_multiplier", 1.0)) * (decay**overflow)
    return max(float(policy.get("min_multiplier", 0.05)), multiplier)


def _evaluate_submission(bounty, identity_id, description, artifacts):
    teams = bounty.get("teams", [])
    slots = _get_slots_for_bounty(bounty)
    slot_index = len(teams) + 1
    policy = _normalize_slot_policy(bounty.get("slot_policy"))

    multiplier = _compute_slot_multiplier(slot_index, slots, policy)
    reasons = []

    if not identity_id:
        reasons.append("missing_identity")

    if identity_id:
        submitted = [t for t in teams if t.get("identity_id") == identity_id]
        if len(submitted) >= policy.get("max_rewarded_submissions_per_identity", 1):
            reasons.append("repeat_submission")

    min_chars = policy.get("min_description_chars", 0)
    desc_ok = len((description or "").strip()) >= min_chars if min_chars else True
    has_artifacts = bool(artifacts)
    if not desc_ok and not (
        policy.get("allow_artifact_override", True) and has_artifacts
    ):
        reasons.append("insufficient_contribution")

    if slot_index > slots:
        reasons.append("overflow")

    if reasons and any(
        r in ["missing_identity", "repeat_submission", "insufficient_contribution"]
        for r in reasons
    ):
        multiplier = 0.0

    if not reasons:
        reason = "in_slot"
    else:
        reason = ",".join(reasons)

    return {
        "slot_index": slot_index,
        "slots": slots,
        "slot_multiplier": round(multiplier, 4),
        "slot_reason": reason,
        "policy": policy,
    }


def _normalize_submission_text(value: str) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _submission_fingerprint(
    identity_id: str,
    description: str,
    artifacts: list,
    members: list,
) -> str:
    normalized_artifacts = sorted(
        {
            _normalize_submission_text(item)
            for item in artifacts
            if _normalize_submission_text(item)
        }
    )
    normalized_members = sorted(
        {
            _normalize_submission_text(item)
            for item in members
            if _normalize_submission_text(item)
        }
    )
    payload = "\n".join(
        [
            _normalize_submission_text(identity_id),
            _normalize_submission_text(description),
            ",".join(normalized_members),
            ",".join(normalized_artifacts),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_bounties() -> list:
    path = _get_bounties_file()
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    return []


def load_bounties() -> list:
    """Load bounties from file. Requires Flask app context. For use by control_panel_app."""
    return _load_bounties()


def _save_bounties(bounties: list) -> None:
    path = _get_bounties_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(bounties, f, indent=2)


@bp.route("/bounties", methods=["GET"])
def get_bounties():
    """GET /api/bounties - List all non-completed bounties."""
    bounties = _load_bounties()
    active = [b for b in bounties if b.get("status") in ("open", "claimed")]
    return jsonify({"success": True, "bounties": active})


@bp.route("/bounties", methods=["POST"])
def create_bounty():
    """POST /api/bounties - Create a new bounty."""
    data = request.json or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    reward = int(data.get("reward", 50))
    slots = data.get("slots", data.get("max_teams", 1))
    try:
        slots = max(1, int(slots))
    except (TypeError, ValueError):
        slots = 1
    game_mode = (data.get("game_mode") or "hybrid").lower()
    if game_mode not in ("pvp", "coop", "hybrid"):
        game_mode = "hybrid"
    slot_policy = _normalize_slot_policy(data.get("slot_policy"))

    if not title:
        return jsonify({"success": False, "error": "Title required"})

    bounties = _load_bounties()
    bounty = {
        "id": f"bounty_{int(time.time()*1000)}",
        "title": title,
        "description": description,
        "reward": reward,
        "game_name": CRUCIBLE_NAME,
        "game_mode": game_mode,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "claimed_by": None,
        "max_teams": slots,
        "slots": slots,
        "slot_policy": slot_policy,
        "slot_state": {"slots": slots, "filled": 0, "overflow": 0},
        "teams": [],
        "cost_tracking": {
            "api_cost": 0.0,
            "sessions_used": 0,
            "tokens_spent": 0,
            "started_at": None,
            "artifacts_created": [],
        },
    }
    bounties.append(bounty)
    _save_bounties(bounties)

    return jsonify({"success": True, "bounty": bounty})


@bp.route("/bounties/<bounty_id>", methods=["DELETE"])
def delete_bounty(bounty_id):
    """DELETE /api/bounties/<id> - Delete an unclaimed bounty."""
    bounties = _load_bounties()
    bounty = next((b for b in bounties if b["id"] == bounty_id), None)

    if not bounty:
        return jsonify({"success": False, "error": "Bounty not found"})

    if bounty.get("status") != "open":
        return jsonify({"success": False, "error": "Can only delete open bounties"})

    bounties = [b for b in bounties if b["id"] != bounty_id]
    _save_bounties(bounties)

    return jsonify({"success": True})


@bp.route("/bounties/<bounty_id>/submit", methods=["POST"])
def submit_to_bounty(bounty_id):
    """POST /api/bounties/<id>/submit - Submit work to a bounty."""
    data = request.json or {}
    bounties = _load_bounties()
    bounty = next((b for b in bounties if b["id"] == bounty_id), None)

    if not bounty:
        return jsonify({"success": False, "error": "Bounty not found"})

    if bounty.get("status") not in ("open", "claimed"):
        return jsonify({"success": False, "error": "Bounty is not open for submissions"})

    bounty["slot_policy"] = _normalize_slot_policy(bounty.get("slot_policy"))
    bounty["slots"] = _get_slots_for_bounty(bounty)

    identity_id = data.get("identity_id")
    description = data.get("description", "")
    raw_artifacts = data.get("artifacts", [])
    artifacts = []
    if isinstance(raw_artifacts, list):
        for artifact in raw_artifacts:
            normalized = str(artifact or "").strip()
            if normalized and normalized not in artifacts:
                artifacts.append(normalized)
    guild_id = str(data.get("guild_id") or "").strip() or None
    guild_name = str(data.get("guild_name") or "").strip() or None
    raw_members = data.get("members", [])
    members = []
    if isinstance(raw_members, list):
        for member in raw_members:
            normalized = str(member or "").strip()
            if normalized and normalized not in members:
                members.append(normalized)
    if not members and identity_id:
        members = [str(identity_id).strip()]

    candidate_fingerprint = _submission_fingerprint(
        identity_id, description, artifacts, members
    )
    for existing in bounty.get("teams", []):
        existing_fp = existing.get("submission_fingerprint")
        if not existing_fp:
            existing_fp = _submission_fingerprint(
                existing.get("identity_id"),
                existing.get("description", ""),
                existing.get("artifacts", []),
                existing.get("members", []),
            )
        if existing_fp == candidate_fingerprint:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Duplicate submission blocked: identical payload already exists.",
                    }
                ),
                409,
            )

    slot_info = _evaluate_submission(bounty, identity_id, description, artifacts)

    submission = {
        "id": f"sub_{int(time.time()*1000)}",
        "identity_id": identity_id,
        "identity_name": data.get("identity_name", "Unknown"),
        "members": members,
        "guild_id": guild_id,
        "guild_name": guild_name,
        "description": description,
        "artifacts": artifacts,
        "submitted_at": datetime.now().isoformat(),
        "notes": data.get("notes", ""),
        "slot_index": slot_info["slot_index"],
        "slots": slot_info["slots"],
        "slot_multiplier": slot_info["slot_multiplier"],
        "slot_reason": slot_info["slot_reason"],
        "reward_cap": int(
            round(bounty.get("reward", 0) * slot_info["slot_multiplier"])
        ),
        "submission_fingerprint": candidate_fingerprint,
    }

    if "teams" not in bounty:
        bounty["teams"] = []
    bounty["teams"].append(submission)

    slots = bounty.get("slots", _get_slots_for_bounty(bounty))
    team_count = len(bounty["teams"])
    bounty["slot_state"] = {
        "slots": slots,
        "filled": min(team_count, slots),
        "overflow": max(0, team_count - slots),
    }

    if bounty["status"] == "open" and len(bounty["teams"]) == 1:
        bounty["status"] = "claimed"
        bounty["cost_tracking"]["started_at"] = datetime.now().isoformat()
        if guild_id:
            bounty["claimed_by"] = {
                "type": "guild",
                "id": guild_id,
                "name": guild_name or guild_id,
                "claimed_by_identity": identity_id,
                "claimed_by_name": data.get("identity_name", "Unknown"),
            }
        elif identity_id:
            bounty["claimed_by"] = {
                "type": "individual",
                "id": identity_id,
                "name": data.get("identity_name", "Unknown"),
            }

    _save_bounties(bounties)

    return jsonify({"success": True, "submission": submission})


@bp.route("/bounties/<bounty_id>/track_cost", methods=["POST"])
def track_bounty_cost(bounty_id):
    """POST /api/bounties/<id>/track_cost - Track API cost against a bounty."""
    data = request.json or {}
    bounties = _load_bounties()
    bounty = next((b for b in bounties if b["id"] == bounty_id), None)

    if not bounty:
        return jsonify({"success": False, "error": "Bounty not found"})

    if "cost_tracking" not in bounty:
        bounty["cost_tracking"] = {
            "api_cost": 0.0,
            "sessions_used": 0,
            "tokens_spent": 0,
            "started_at": None,
            "artifacts_created": [],
        }

    if data.get("api_cost"):
        bounty["cost_tracking"]["api_cost"] += float(data["api_cost"])
    if data.get("session_increment"):
        bounty["cost_tracking"]["sessions_used"] += 1
    if data.get("tokens_spent"):
        bounty["cost_tracking"]["tokens_spent"] += int(data["tokens_spent"])
    if data.get("artifact"):
        bounty["cost_tracking"]["artifacts_created"].append(data["artifact"])
    if not bounty["cost_tracking"]["started_at"]:
        bounty["cost_tracking"]["started_at"] = datetime.now().isoformat()

    _save_bounties(bounties)
    return jsonify({"success": True, "cost_tracking": bounty["cost_tracking"]})


@bp.route("/bounties/<bounty_id>/submissions")
def get_bounty_submissions(bounty_id):
    """GET /api/bounties/<id>/submissions - List submissions for a bounty."""
    bounties = _load_bounties()
    bounty = next((b for b in bounties if b["id"] == bounty_id), None)

    if not bounty:
        return jsonify({"success": False, "error": "Bounty not found"})

    return jsonify(
        {
            "success": True,
            "bounty_id": bounty_id,
            "bounty_title": bounty.get("title"),
            "submissions": bounty.get("teams", []),
        }
    )


@bp.route("/bounties/<bounty_id>/complete", methods=["POST"])
def complete_bounty(bounty_id):
    """POST /api/bounties/<id>/complete - Complete & reward."""
    data = request.json or {}
    bounties = _load_bounties()
    bounty = next((b for b in bounties if b["id"] == bounty_id), None)

    if not bounty:
        return jsonify({"success": False, "error": "Bounty not found"})

    cost_tracking = bounty.get("cost_tracking", {})
    if cost_tracking.get("started_at"):
        action_log = current_app.config.get("ACTION_LOG")
        if action_log and Path(action_log).exists():
            try:
                start_time = datetime.fromisoformat(cost_tracking["started_at"])
                total_api_cost = cost_tracking.get("api_cost", 0.0)

                with open(action_log, "r") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("action_type") == "API":
                                entry_time = datetime.fromisoformat(
                                    entry["timestamp"].replace("Z", "+00:00")
                                )
                                if entry_time >= start_time:
                                    detail = entry.get("detail", "")
                                    if "$" in detail:
                                        cost_str = detail.split("$")[-1]
                                        try:
                                            total_api_cost += float(cost_str)
                                        except Exception:
                                            pass
                        except Exception:
                            pass

                cost_tracking["api_cost"] = total_api_cost
                cost_tracking["completed_at"] = datetime.now().isoformat()

                if cost_tracking.get("started_at"):
                    start = datetime.fromisoformat(cost_tracking["started_at"])
                    duration = datetime.now() - start
                    hours = duration.total_seconds() / 3600
                    cost_tracking["duration_hours"] = round(hours, 2)

            except Exception as e:
                print(f"Error calculating bounty costs: {e}")

    winner_reward = data.get("winner_reward", bounty.get("reward", 50))
    runner_up_reward = data.get("runner_up_reward", 0)

    try:
        workspace = current_app.config["WORKSPACE"]
        sys.path.insert(0, str(workspace))
        from vivarium.runtime.swarm_enrichment import get_enrichment

        enrichment = get_enrichment(workspace)

        teams = bounty.get("teams", [])
        if teams and len(teams) == 1:
            try:
                bounty["slot_multiplier"] = float(
                    teams[0].get("slot_multiplier", 1.0)
                )
                bounty["slot_reason"] = teams[0].get("slot_reason", "in_slot")
            except (TypeError, ValueError):
                bounty["slot_multiplier"] = 1.0
                bounty["slot_reason"] = "in_slot"
            if not bounty.get("claimed_by"):
                first_team = teams[0]
                if first_team.get("guild_id"):
                    bounty["claimed_by"] = {
                        "type": "guild",
                        "id": first_team.get("guild_id"),
                        "name": first_team.get("guild_name")
                        or first_team.get("guild_id"),
                        "claimed_by_identity": first_team.get("identity_id"),
                        "claimed_by_name": first_team.get("identity_name", "Unknown"),
                    }
                elif first_team.get("identity_id"):
                    bounty["claimed_by"] = {
                        "type": "individual",
                        "id": first_team.get("identity_id"),
                        "name": first_team.get("identity_name", "Unknown"),
                    }
            _save_bounties(bounties)
        if teams and len(teams) > 1:
            result = {
                "success": True,
                "distributions": [],
                "total_distributed": 0,
                "cost_tracking": cost_tracking,
            }
            for i, team in enumerate(teams):
                reward = (
                    winner_reward
                    if i == 0
                    else (runner_up_reward if i == 1 else 0)
                )
                try:
                    slot_multiplier = float(team.get("slot_multiplier", 1.0))
                except (TypeError, ValueError):
                    slot_multiplier = 1.0
                reward = int(round(reward * max(0.0, slot_multiplier)))
                if reward > 0:
                    team_members = []
                    raw_team_members = team.get("members", [])
                    if isinstance(raw_team_members, list):
                        for member_id in raw_team_members:
                            normalized_member = str(member_id or "").strip()
                            if (
                                normalized_member
                                and normalized_member not in team_members
                            ):
                                team_members.append(normalized_member)
                    if not team_members and team.get("identity_id"):
                        team_members = [str(team.get("identity_id")).strip()]
                    for member_id in team_members:
                        enrichment.grant_free_time(
                            member_id, reward, f"bounty_{bounty_id}_place_{i+1}"
                        )
                        result["total_distributed"] += reward
                        result["distributions"].append(
                            {
                                "identity": member_id,
                                "reward": reward,
                                "place": i + 1,
                                "slot_multiplier": slot_multiplier,
                            }
                        )
        else:
            result = enrichment.distribute_bounty(bounty_id)
            result["cost_tracking"] = cost_tracking

        bounty["status"] = "completed"
        bounty["completed_at"] = datetime.now().isoformat()
        bounty["cost_tracking"] = cost_tracking
        _save_bounties(bounties)

        return jsonify(result)

    except Exception as e:
        return jsonify(
            {"success": False, "error": str(e), "cost_tracking": cost_tracking}
        )
