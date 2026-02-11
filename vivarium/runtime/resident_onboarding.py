"""
Resident onboarding and daily wake-up context.

Residents are born at runtime, choose an identity from the Community Library, and receive
a world summary that helps them decide what to do today. This is voluntary and
reward-based: no coercion, no forced assignments.
"""

from __future__ import annotations

import json
import os
import random
import time
import uuid
from difflib import SequenceMatcher
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from vivarium.utils import read_json, write_json

try:
    from vivarium.runtime.swarm_enrichment import EnrichmentSystem
except ImportError:
    EnrichmentSystem = None


IDENTITY_LIBRARY_FILE = "identity_library.json"
RESIDENT_DAYS_FILE = Path(".swarm") / "resident_days.json"
IDENTITIES_DIR = Path(".swarm") / "identities"
IDENTITY_LOCKS_FILE = Path(".swarm") / "identity_locks.json"
COMMUNITY_LIBRARY_ROOT = "library/community_library"
BOOTSTRAP_IDENTITY_COUNT = 8
AUTO_BOOTSTRAP_IDENTITIES = os.environ.get("VIVARIUM_BOOTSTRAP_IDENTITIES", "0").strip().lower() in {
    "1",
    "true",
    "yes",
}
IDENTITY_NAME_SIMILARITY_MAX = 0.90
IDENTITY_STATEMENT_SIMILARITY_MAX = 0.93
IDENTITY_SUMMARY_SIMILARITY_MAX = 0.95
UNCREATIVE_IDENTITY_NAME_TERMS = frozenset(
    {
        "resident",
        "identity",
        "persona",
        "person",
        "individual",
        "self",
        "character",
        "avatar",
        "agent",
        "worker",
        "profile",
        "npc",
    }
)
# One simulated "day" length (seconds). Default compressed to 1 minute.
RESIDENT_CYCLE_SECONDS = int(
    os.environ.get(
        "RESIDENT_DAY_SECONDS",
        os.environ.get("RESIDENT_CYCLE_SECONDS", "60"),
    )
)

CREATIVE_NAME_PREFIXES = [
    "Velvet", "Signal", "Kite", "Cipher", "Moon", "Echo", "Drift", "Lumen",
    "Sable", "Mosaic", "Tidal", "Nova", "Cinder", "Willow", "Quartz", "Harbor",
]
CREATIVE_NAME_SUFFIXES = [
    "Thread", "Harbor", "Glyph", "Bloom", "Arc", "Lantern", "Orbit", "Whisper",
    "Compass", "Pulse", "Canvas", "Bridge", "Riddle", "Meadow", "Circuit", "Atlas",
]
CREATIVE_TRAITS = [
    "curious", "reflective", "playful", "precise", "empathetic", "inventive",
    "patient", "bold", "collaborative", "observant", "poetic", "systems-minded",
]
CREATIVE_VALUES = [
    "clarity", "care", "craft", "autonomy", "curiosity", "truth-seeking",
    "kindness", "experimentation", "resilience", "aesthetic joy", "community", "integrity",
]
CREATIVE_ACTIVITIES = [
    "prototyping", "worldbuilding", "debug storytelling", "pair reasoning",
    "toolmaking", "archive curation", "conversation hosting", "rapid experiments",
]


@dataclass
class IdentityTemplate:
    identity_id: str
    name: str
    summary: str
    affinities: List[str] = field(default_factory=list)
    preferred_activities: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    identity_statement: str = ""
    communication_style: str = ""
    mutable_profile: Dict[str, Any] = field(default_factory=dict)


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

    @property
    def week_count(self) -> int:
        return max(1, ((self.day_count - 1) // 7) + 1)

    @property
    def day_of_week(self) -> int:
        return ((self.day_count - 1) % 7) + 1

    def build_wakeup_context(self) -> str:
        statement = (self.identity.identity_statement or "").strip()
        if not statement:
            statement = (
                self.identity.summary
                or "I am still discovering who I am through my choices and reflections."
            )
        style = (self.identity.communication_style or "").strip()
        mutable = self.identity.mutable_profile if isinstance(self.identity.mutable_profile, dict) else {}
        mood = str(mutable.get("current_mood") or "").strip()
        focus = str(mutable.get("current_focus") or "").strip()

        lines = [
            "DAY START",
            "I am waking up in Vivarium.",
            "",
            f"I am {self.identity.name} ({self.identity.identity_id}).",
            f"This is day {self.day_count} (week {self.week_count}, day {self.day_of_week}/7).",
            f"My token wallet: {self.wallet.get('free_time', 0)} free time, "
            f"{self.wallet.get('journal', 0)} journal.",
            "",
            "WHO I AM (PERSISTENT, NEVER COMPRESSED):",
            statement,
            "",
            "CORE ATTRIBUTES (ALWAYS IN CONTEXT):",
            f"- Personality traits: {', '.join(self.identity.affinities) if self.identity.affinities else 'unspecified'}",
            f"- Core values: {', '.join(self.identity.values) if self.identity.values else 'unspecified'}",
            f"- Communication style: {style or 'unspecified'}",
            f"- Current mood: {mood or 'unspecified'}",
            f"- Current focus: {focus or 'unspecified'}",
            "",
            f"I could have sworn I was dreaming about {self.dream_hint}.",
            "",
            "Pre-identity impressions (condensed):",
            self.pre_identity_summary,
            "",
            "My morning briefing:",
            f"- Market hint: {self.market_hint}",
            f"- Community Library: {COMMUNITY_LIBRARY_ROOT}/",
            "- Personal proposals: library/community_library/resident_suggestions/<my_identity_id>/",
            "- Shared docs: library/community_library/swarm_docs/",
        ]
        if self.notifications:
            lines.append("As I check my phone, I notice:")
            for note in self.notifications:
                lines.append(f"- {note}")
        lines.append("")
        lines.append("Participation is voluntary. I choose what aligns with me.")
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
    mutable = attrs.get("mutable", {}) if isinstance(attrs, dict) else {}
    values = core.get("core_values", []) if isinstance(core, dict) else []
    traits = core.get("personality_traits", []) if isinstance(core, dict) else []
    identity_statement = core.get("identity_statement", "") if isinstance(core, dict) else ""
    communication_style = core.get("communication_style", "") if isinstance(core, dict) else ""

    if not summary:
        summary = "Resident identity profile."

    return IdentityTemplate(
        identity_id=identity_id,
        name=name,
        summary=summary,
        affinities=[str(x) for x in traits],
        preferred_activities=[str(x) for x in data.get("preferred_activities", [])],
        values=[str(x) for x in values],
        identity_statement=str(identity_statement or "").strip(),
        communication_style=str(communication_style or "").strip(),
        mutable_profile=mutable if isinstance(mutable, dict) else {},
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
                identity_statement=str(item.get("identity_statement", "")).strip(),
                communication_style=str(item.get("communication_style", "")).strip(),
                mutable_profile={},
            )
        )
    return [i for i in identities if i.identity_id and i.name]


def _bootstrap_identity_library(workspace: Path, count: int = BOOTSTRAP_IDENTITY_COUNT) -> int:
    """
    Seed the identity library with creative starter identities when empty.

    Returns number of identities created.
    """
    identities_dir = workspace / IDENTITIES_DIR
    identities_dir.mkdir(parents=True, exist_ok=True)
    existing = [p for p in identities_dir.glob("*.json") if p.is_file()]
    if existing:
        return 0

    rng = random.Random(42)
    created = 0
    target = max(1, min(24, int(count)))
    used_names: set[str] = set()

    for idx in range(target):
        prefix = rng.choice(CREATIVE_NAME_PREFIXES)
        suffix = rng.choice(CREATIVE_NAME_SUFFIXES)
        if prefix == suffix:
            suffix = CREATIVE_NAME_SUFFIXES[(CREATIVE_NAME_SUFFIXES.index(suffix) + 1) % len(CREATIVE_NAME_SUFFIXES)]
        base_name = f"{prefix} {suffix}"
        name = base_name
        dedupe = 2
        while name in used_names:
            name = f"{base_name} {dedupe}"
            dedupe += 1
        used_names.add(name)

        identity_id = f"oc_seed_{idx + 1:02d}"
        traits = rng.sample(CREATIVE_TRAITS, k=3)
        values = rng.sample(CREATIVE_VALUES, k=3)
        activities = rng.sample(CREATIVE_ACTIVITIES, k=2)
        summary = (
            f"{name} explores ideas through {activities[0]} and {activities[1]}, "
            f"with a {traits[0]} and {traits[1]} style."
        )
        payload = {
            "id": identity_id,
            "name": name,
            "summary": summary,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "origin": "system_bootstrap_creative_seed",
            "preferred_activities": activities,
            "attributes": {
                "core": {
                    "personality_traits": traits,
                    "core_values": values,
                    "identity_statement": (
                        f"I am {name}. I care about {values[0]} and {values[1]}, "
                        f"and I learn by staying {traits[0]}."
                    ),
                },
                "profile": {},
                "mutable": {},
            },
            "meta": {
                "creative_seed": True,
            },
        }
        write_json(identities_dir / f"{identity_id}.json", payload)
        created += 1

    return created


def _normalize_compare_text(value: str) -> str:
    cleaned = "".join(ch if (ch.isalnum() or ch.isspace()) else " " for ch in str(value or "").lower())
    return " ".join(cleaned.split())


def _text_similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def _disallowed_name_terms(name: str) -> List[str]:
    normalized = _normalize_compare_text(name)
    words = [token for token in normalized.split() if token]
    hits = sorted({word for word in words if word in UNCREATIVE_IDENTITY_NAME_TERMS})
    return hits


def _blacklist_retry_message(name: str, blocked_terms: List[str]) -> str:
    terms = ", ".join(blocked_terms)
    return (
        f"IDENTITY_NAME_RULE_VIOLATION: '{name}' contains banned literal terms ({terms}). "
        "Rule: identity names must be creative, specific, and non-literal. "
        "TRY AGAIN with a completely new name that avoids these terms."
    )


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


def _build_pre_identity_summary(
    world: WorldState,
    workspace: Optional[Path] = None,
    identity_id: Optional[str] = None,
) -> str:
    parts = [
        f"{world.open_tasks} open tasks",
        f"{len(world.bounties)} open bounties",
    ]
    if world.slot_summary:
        parts.append("slots: " + "; ".join(world.slot_summary[:3]))
    if world.token_rates:
        parts.append("token rates: " + "; ".join(world.token_rates[:2]))
    if EnrichmentSystem is not None and workspace is not None and identity_id:
        try:
            enrichment = EnrichmentSystem(workspace=workspace)
            rollups = enrichment.get_journal_rollups(
                identity_id=identity_id,
                requester_id=identity_id,
                daily_limit=2,
                weekly_limit=1,
            )
            daily = rollups.get("daily", [])
            weekly = rollups.get("weekly", [])
            if daily:
                parts.append(f"recent reflections: {sum(int(d.get('entries', 0)) for d in daily)} entries")
            if weekly:
                top = weekly[0]
                parts.append(
                    f"weekly memory: {top.get('week', 'unknown')} ({top.get('entries', 0)} entries)"
                )
        except Exception:
            pass
    return "; ".join(parts) + "."


def _select_identity(identities: List[IdentityTemplate], world: WorldState) -> Tuple[IdentityTemplate, str]:
    if not identities:
        suffix = uuid.uuid4().hex[:6]
        name = f"{random.choice(CREATIVE_NAME_PREFIXES)} {random.choice(CREATIVE_NAME_SUFFIXES)}"
        fallback = IdentityTemplate(
            identity_id=f"oc_{suffix}",
            name=name,
            summary="Emergent creative identity bootstrapped from current world context.",
        )
        return fallback, "emergent fallback identity"

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
    identity_statement: Optional[str] = None,
    creativity_seed: Optional[str] = None,
    available_cycle: Optional[int] = None,
) -> str:
    """Create a new resident identity (OC) authored by a resident."""
    cycle_id = _current_cycle_id()
    available_at = available_cycle if available_cycle is not None else cycle_id
    clean_name = (name or "").strip()
    if not clean_name:
        raise ValueError("identity name is required")
    if len(clean_name) > 80:
        raise ValueError("identity name is too long (max 80 chars)")
    banned_terms = _disallowed_name_terms(clean_name)
    if banned_terms:
        raise ValueError(_blacklist_retry_message(clean_name, banned_terms))

    identity_id = f"oc_{uuid.uuid4().hex[:8]}"
    clean_summary = (summary or "").strip() or "Self-authored resident identity."
    clean_statement = (identity_statement or "").strip() or clean_summary

    # Duplicate guard: block exact and near-copy identity names/statements.
    identities_dir = workspace / IDENTITIES_DIR
    identities_dir.mkdir(parents=True, exist_ok=True)
    candidate_name_norm = _normalize_compare_text(clean_name)
    candidate_statement_norm = _normalize_compare_text(clean_statement)

    for identity_path in identities_dir.glob("*.json"):
        if not identity_path.is_file():
            continue
        try:
            existing = read_json(identity_path, default={})
        except Exception:
            continue
        existing_name = str(existing.get("name") or existing.get("id") or "").strip()
        attrs = existing.get("attributes", {}) if isinstance(existing, dict) else {}
        core = attrs.get("core", {}) if isinstance(attrs, dict) else {}
        existing_statement = str(core.get("identity_statement") or existing.get("summary") or "").strip()

        existing_name_norm = _normalize_compare_text(existing_name)
        existing_statement_norm = _normalize_compare_text(existing_statement)
        if candidate_name_norm and existing_name_norm:
            if candidate_name_norm == existing_name_norm:
                raise ValueError(f"duplicate identity name: '{clean_name}' already exists")
            name_similarity = _text_similarity(candidate_name_norm, existing_name_norm)
            if name_similarity >= IDENTITY_NAME_SIMILARITY_MAX:
                raise ValueError(
                    f"identity name is too similar to existing '{existing_name}' "
                    f"(similarity {name_similarity:.2f}); remix it more"
                )
        if len(candidate_statement_norm) >= 20 and len(existing_statement_norm) >= 20:
            statement_similarity = _text_similarity(candidate_statement_norm, existing_statement_norm)
            if statement_similarity >= IDENTITY_STATEMENT_SIMILARITY_MAX:
                raise ValueError(
                    f"identity statement is too similar to existing '{existing_name}' "
                    f"(similarity {statement_similarity:.2f}); rewrite it in a new voice"
                )
        existing_summary = str(existing.get("summary") or "").strip()
        existing_summary_norm = _normalize_compare_text(existing_summary)
        candidate_summary_norm = _normalize_compare_text(clean_summary)
        if len(candidate_summary_norm) >= 20 and len(existing_summary_norm) >= 20:
            summary_similarity = _text_similarity(candidate_summary_norm, existing_summary_norm)
            if summary_similarity >= IDENTITY_SUMMARY_SIMILARITY_MAX:
                raise ValueError(
                    f"identity summary is too similar to existing '{existing_name}' "
                    f"(similarity {summary_similarity:.2f}); make it genuinely different"
                )

    identity_data = {
        "id": identity_id,
        "name": clean_name,
        "summary": clean_summary,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "created_by": {
            "resident_id": creator_resident_id,
            "identity_id": creator_identity_id,
        },
        "origin": "resident_authored",
        "available_cycle": available_at,
        "preferred_activities": preferred_activities or [],
        "attributes": {
            "core": {
                "personality_traits": affinities or [],
                "core_values": values or [],
                "identity_statement": clean_statement,
            },
            "profile": {},
            "mutable": {},
        },
        "meta": {
            "creative_self_authored": True,
            "creativity_seed": str(creativity_seed or "").strip(),
        },
    }

    write_json(identities_dir / f"{identity_id}.json", identity_data)
    return identity_id

def spawn_resident(workspace: Path, identity_override: Optional[str] = None) -> Optional[ResidentContext]:
    resident_id = f"resident_{uuid.uuid4().hex[:8]}"
    cycle_id = _current_cycle_id()
    identities = _load_identity_library(workspace)
    if not identities and AUTO_BOOTSTRAP_IDENTITIES:
        _bootstrap_identity_library(workspace)
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

    pre_identity_summary = _build_pre_identity_summary(
        world,
        workspace=workspace,
        identity_id=identity.identity_id,
    ) + f" selection signal: {selection_reason}."

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
