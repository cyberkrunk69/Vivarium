"""
Resident onboarding and daily wake-up context.

Residents are born at runtime, choose an identity from the library, and receive
a world summary that helps them decide what to do today. This is voluntary and
reward-based: no coercion, no forced assignments.
"""

from __future__ import annotations

import json
import os
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from utils import read_json, write_json

try:
    from vivarium.runtime.swarm_enrichment import EnrichmentSystem
except ImportError:
    EnrichmentSystem = None


IDENTITY_LIBRARY_FILE = "identity_library.json"
RESIDENT_DAYS_FILE = Path(".swarm") / "resident_days.json"
IDENTITIES_DIR = Path(".swarm") / "identities"
IDENTITY_LOCKS_FILE = Path(".swarm") / "identity_locks.json"
# "Day" length at machine speed (seconds per cycle).
RESIDENT_CYCLE_SECONDS = int(os.environ.get("RESIDENT_CYCLE_SECONDS", "900"))


@dataclass
class IdentityTemplate:
    identity_id: str
    name: str
    summary: str
    affinities: List[str] = field(default_factory=list)
    preferred_activities: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)


@dataclass
class WorldState:
    bounties: List[Dict[str, Any]]
    open_tasks: int
    slot_summary: List[str]
    token_rates: List[str]
    market_hint: str


@dataclass
class ResidentContext:
    resident_id: str
    identity: IdentityTemplate
    day_count: int
    cycle_id: int
    wallet: Dict[str, Any]
    pre_identity_summary: str
    dream_hint: str
    notifications: List[str]
    market_hint: str

    def build_wakeup_context(self) -> str:
        lines = [
            "DAY START",
            "You are waking up in Vivarium.",
            "",
            f"You are {self.identity.name} ({self.identity.identity_id}).",
            f"This is your day {self.day_count} (cycle {self.cycle_id}).",
            f"Token wallet: {self.wallet.get('free_time', 0)} free time, "
            f"{self.wallet.get('journal', 0)} journal.",
            "",
            f"I could have sworn I was dreaming about {self.dream_hint}.",
            "",
            "Pre-identity impressions (condensed):",
            self.pre_identity_summary,
            "",
            "Reframed as your morning briefing:",
            f"- Market hint: {self.market_hint}",
        ]
        if self.notifications:
            lines.append("As you roll out of bed and check your phone you notice:")
            for note in self.notifications:
                lines.append(f"- {note}")
        lines.append("")
        lines.append("Participation is voluntary. Choose what aligns with you.")
        return "\n".join(lines)

    def apply_to_prompt(self, prompt: str) -> str:
        wakeup = self.build_wakeup_context()
        return f"{wakeup}\n\nTASK:\n{prompt}"

    def score_task(self, task: Dict[str, Any]) -> Tuple[float, str]:
        text = " ".join(
            str(task.get(k, "")) for k in ["prompt", "description", "task", "instruction", "type"]
        ).lower()
        affinity_hits = [a for a in self.identity.affinities if a.lower() in text]
        score = float(len(affinity_hits))
        reason = "affinity match: " + (", ".join(affinity_hits) if affinity_hits else "none")

        reward = task.get("reward")
        if isinstance(reward, (int, float)) and reward > 0:
            score += min(reward / 100.0, 2.0)
            reason += f"; reward bonus {reward}"

        return score, reason


@dataclass
class IdentityChoice:
    identity: IdentityTemplate
    reason: str


def _identity_from_file(path: Path) -> Optional[IdentityTemplate]:
    try:
        data = read_json(path, default={})
    except Exception:
        return None

    identity_id = str(data.get("id", path.stem)).strip()
    name = str(data.get("name", "")).strip() or identity_id
    summary = str(data.get("summary", "")).strip()
    attrs = data.get("attributes", {}) if isinstance(data, dict) else {}
    core = attrs.get("core", {}) if isinstance(attrs, dict) else {}
    values = core.get("core_values", []) if isinstance(core, dict) else []
    traits = core.get("personality_traits", []) if isinstance(core, dict) else []

    if not summary:
        summary = "Resident identity profile."

    return IdentityTemplate(
        identity_id=identity_id,
        name=name,
        summary=summary,
        affinities=[str(x) for x in traits],
        preferred_activities=[str(x) for x in data.get("preferred_activities", [])],
        values=[str(x) for x in values],
    )


def _load_identity_library(workspace: Path) -> List[IdentityTemplate]:
    identities: List[IdentityTemplate] = []

    identities_dir = workspace / IDENTITIES_DIR
    if identities_dir.exists():
        for path in identities_dir.glob("*.json"):
            if not path.is_file():
                continue
            data = read_json(path, default={})
            available_cycle = data.get("available_cycle")
            current_cycle = _current_cycle_id()
            if isinstance(available_cycle, int) and available_cycle > current_cycle:
                continue
            ident = _identity_from_file(path)
            if ident:
                identities.append(ident)

    if identities:
        return identities

    lib_path = workspace / IDENTITY_LIBRARY_FILE
    if not lib_path.exists():
        return []
    data = read_json(lib_path, default={})
    for item in data.get("identities", []):
        identities.append(
            IdentityTemplate(
                identity_id=str(item.get("id", "")).strip(),
                name=str(item.get("name", "")).strip(),
                summary=str(item.get("summary", "")).strip(),
                affinities=[str(x) for x in item.get("affinities", [])],
                preferred_activities=[str(x) for x in item.get("preferred_activities", [])],
                values=[str(x) for x in item.get("values", [])],
            )
        )
    return [i for i in identities if i.identity_id and i.name]


def _load_bounties(workspace: Path) -> List[Dict[str, Any]]:
    if EnrichmentSystem is None:
        return []
    try:
        enrichment = EnrichmentSystem(workspace=workspace)
        return enrichment.get_open_bounties()
    except Exception:
        return []


def _current_cycle_id(now: Optional[float] = None) -> int:
    timestamp = now if now is not None else time.time()
    if RESIDENT_CYCLE_SECONDS <= 0:
        return int(timestamp)
    return int(timestamp // RESIDENT_CYCLE_SECONDS)


def _load_identity_locks(cycle_id: int) -> Dict[str, Any]:
    if IDENTITY_LOCKS_FILE.exists():
        data = read_json(IDENTITY_LOCKS_FILE, default={})
    else:
        data = {}
    if not isinstance(data, dict):
        data = {}
    if data.get("cycle_id") != cycle_id:
        data = {"cycle_id": cycle_id, "locks": {}}
        _save_identity_locks(data)
    if "locks" not in data or not isinstance(data["locks"], dict):
        data["locks"] = {}
    return data


def _save_identity_locks(data: Dict[str, Any]) -> None:
    IDENTITY_LOCKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_json(IDENTITY_LOCKS_FILE, data)


def _acquire_identity_lock(identity_id: str, resident_id: str, cycle_id: int) -> bool:
    data = _load_identity_locks(cycle_id)
    locks = data.get("locks", {})
    existing = locks.get(identity_id)
    if existing and existing.get("resident_id") != resident_id:
        return False
    locks[identity_id] = {
        "resident_id": resident_id,
        "cycle_id": cycle_id,
        "claimed_at": datetime.utcnow().isoformat() + "Z",
    }
    data["locks"] = locks
    _save_identity_locks(data)
    return True


def _summarize_bounty_slots(bounties: List[Dict[str, Any]]) -> List[str]:
    summaries = []
    for bounty in bounties[:5]:
        slots = bounty.get("slots", bounty.get("max_teams", 1))
        teams = bounty.get("teams") or []
        claimed = 1 if bounty.get("status") == "claimed" else 0
        filled = max(len(teams), claimed)
        summaries.append(
            f"{bounty.get('title', 'Bounty')}: {filled}/{slots} slots filled"
        )
    return summaries


def _load_token_rates(workspace: Path) -> List[str]:
    metrics_path = workspace / ".swarm" / "performance_metrics.json"
    if not metrics_path.exists():
        return []
    try:
        metrics = read_json(metrics_path, default={})
    except Exception:
        return []
    rates = []
    by_task = metrics.get("by_task_type", {})
    for task_type, data in by_task.items():
        samples = data.get("samples", [])
        if not samples:
            continue
        rewards = data.get("specializations", {})
        reward_vals = [spec.get("rewards_earned", 0) for spec in rewards.values()]
        avg_reward = sum(reward_vals) / max(len(reward_vals), 1) if reward_vals else 0
        avg_quality = sum(s.get("quality_score", 0) for s in samples[-10:]) / max(len(samples[-10:]), 1)
        rates.append(f"{task_type}: avg_reward {avg_reward:.1f} tokens, quality {avg_quality:.2f}")
    return rates


def _build_world_state(workspace: Path) -> WorldState:
    queue = read_json(workspace / "queue.json", default={})
    open_tasks = len(queue.get("tasks", []))
    bounties = _load_bounties(workspace)
    slot_summary = _summarize_bounty_slots(bounties)
    token_rates = _load_token_rates(workspace)

    market_hint = "No strong signals yet."
    if bounties:
        market_hint = f"Open bounties: {bounties[0].get('title', 'New bounty')}"
    elif open_tasks:
        market_hint = f"{open_tasks} tasks available in the queue."

    return WorldState(
        bounties=bounties,
        open_tasks=open_tasks,
        slot_summary=slot_summary,
        token_rates=token_rates,
        market_hint=market_hint,
    )


def _build_pre_identity_summary(world: WorldState) -> str:
    parts = [
        f"{world.open_tasks} open tasks",
        f"{len(world.bounties)} open bounties",
    ]
    if world.slot_summary:
        parts.append("slots: " + "; ".join(world.slot_summary[:3]))
    if world.token_rates:
        parts.append("token rates: " + "; ".join(world.token_rates[:2]))
    return "; ".join(parts) + "."


def _select_identity(identities: List[IdentityTemplate], world: WorldState) -> Tuple[IdentityTemplate, str]:
    if not identities:
        fallback = IdentityTemplate(
            identity_id="resident_default",
            name="Resident",
            summary="Default resident identity.",
        )
        return fallback, "default identity"

    best = identities[0]
    best_score = -1.0
    best_reason = "fallback"
    bounty_text = " ".join(str(b.get("title", "")) for b in world.bounties).lower()

    for ident in identities:
        score = 0.0
        reasons = []
        for affinity in ident.affinities:
            if affinity.lower() in bounty_text:
                score += 2.0
                reasons.append(f"bounty match: {affinity}")
        if world.open_tasks > 0 and ident.preferred_activities:
            score += 0.5
            reasons.append("tasks available")
        if score > best_score:
            best = ident
            best_score = score
            best_reason = ", ".join(reasons) if reasons else "no strong signals"

    return best, best_reason


def _load_day_counts() -> Dict[str, int]:
    if RESIDENT_DAYS_FILE.exists():
        return read_json(RESIDENT_DAYS_FILE, default={})
    return {}


def _save_day_counts(data: Dict[str, int]) -> None:
    RESIDENT_DAYS_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_json(RESIDENT_DAYS_FILE, data)


def present_identity_choices(workspace: Path) -> Tuple[WorldState, List[IdentityChoice]]:
    identities = _load_identity_library(workspace)
    cycle_id = _current_cycle_id()
    locks = _load_identity_locks(cycle_id).get("locks", {})
    if locks:
        identities = [i for i in identities if i.identity_id not in locks]
    world = _build_world_state(workspace)
    choices: List[IdentityChoice] = []
    for identity in identities:
        reason = "available identity"
        if identity.affinities and world.bounties:
            bounty_text = " ".join(str(b.get("title", "")) for b in world.bounties).lower()
            hits = [a for a in identity.affinities if a.lower() in bounty_text]
            if hits:
                reason = "affinity match: " + ", ".join(hits[:3])
        choices.append(IdentityChoice(identity=identity, reason=reason))
    return world, choices


def create_identity_from_resident(
    workspace: Path,
    creator_resident_id: str,
    creator_identity_id: str,
    name: str,
    summary: str,
    affinities: Optional[List[str]] = None,
    values: Optional[List[str]] = None,
    preferred_activities: Optional[List[str]] = None,
    available_cycle: Optional[int] = None,
) -> str:
    """Create a new resident identity (OC) authored by a resident."""
    identity_id = f"oc_{uuid.uuid4().hex[:8]}"
    cycle_id = _current_cycle_id()
    available_at = available_cycle if available_cycle is not None else cycle_id + 1

    identity_data = {
        "id": identity_id,
        "name": name or identity_id,
        "summary": summary or "Resident-created identity.",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "created_by": {
            "resident_id": creator_resident_id,
            "identity_id": creator_identity_id,
        },
        "origin": "resident_oc",
        "available_cycle": available_at,
        "preferred_activities": preferred_activities or [],
        "attributes": {
            "core": {
                "personality_traits": affinities or [],
                "core_values": values or [],
            },
            "profile": {},
            "mutable": {},
        },
    }

    identities_dir = workspace / IDENTITIES_DIR
    identities_dir.mkdir(parents=True, exist_ok=True)
    write_json(identities_dir / f"{identity_id}.json", identity_data)
    return identity_id

def spawn_resident(workspace: Path, identity_override: Optional[str] = None) -> Optional[ResidentContext]:
    resident_id = f"resident_{uuid.uuid4().hex[:8]}"
    cycle_id = _current_cycle_id()
    identities = _load_identity_library(workspace)
    world = _build_world_state(workspace)

    allow_override = os.environ.get("RESIDENT_ALLOW_OVERRIDE") == "1"
    if identity_override and allow_override:
        chosen = next((i for i in identities if i.identity_id == identity_override), None)
        if chosen:
            identity = chosen
            selection_reason = "explicit override"
        else:
            identity, selection_reason = _select_identity(identities, world)
    else:
        identity, selection_reason = _select_identity(identities, world)

    available = list(identities) or [identity]
    locked = False
    while available:
        if _acquire_identity_lock(identity.identity_id, resident_id, cycle_id):
            locked = True
            break
        available = [i for i in available if i.identity_id != identity.identity_id]
        if not available:
            break
        identity, selection_reason = _select_identity(available, world)

    if not locked:
        return None

    day_counts = _load_day_counts()
    day_counts[identity.identity_id] = day_counts.get(identity.identity_id, 0) + 1
    _save_day_counts(day_counts)

    wallet = {"free_time": 0, "journal": 0}
    if EnrichmentSystem is not None:
        try:
            enrichment = EnrichmentSystem(workspace=workspace)
            wallet = enrichment.get_all_balances(identity.identity_id)
        except Exception:
            pass

    pre_identity_summary = _build_pre_identity_summary(world) + f" selection signal: {selection_reason}."

    dream_hint = world.market_hint
    notifications = []
    if world.slot_summary:
        notifications.extend(world.slot_summary)
    if world.token_rates:
        notifications.append("Token rates:")
        notifications.extend(world.token_rates[:3])

    return ResidentContext(
        resident_id=resident_id,
        identity=identity,
        day_count=day_counts[identity.identity_id],
        cycle_id=cycle_id,
        wallet=wallet,
        pre_identity_summary=pre_identity_summary,
        dream_hint=dream_hint,
        notifications=notifications,
        market_hint=world.market_hint,
    )
