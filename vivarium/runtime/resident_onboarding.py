"""
Resident onboarding and daily wake-up context.

Residents are born at runtime, choose an identity from the Community Library, and receive
a world summary that helps them decide what to do today. This is voluntary and
reward-based: no coercion, no forced assignments.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import secrets
import time
import uuid
from difflib import SequenceMatcher
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from vivarium.utils import read_json, write_json
from vivarium.runtime.secure_api_wrapper import AuditLogger

try:
    from vivarium.runtime.vivarium_scope import MUTABLE_SWARM_DIR
except ImportError:
    MUTABLE_SWARM_DIR = Path(".swarm")

try:
    from vivarium.runtime.swarm_enrichment import EnrichmentSystem
except ImportError:
    EnrichmentSystem = None


IDENTITY_LIBRARY_FILE = "identity_library.json"
RUNTIME_SPEED_FILE = MUTABLE_SWARM_DIR / "runtime_speed.json"
REFERENCE_WAIT_SECONDS = 2.0  # UI "normal" speed; cycle length scales with wait_seconds
ZERO_PACE_CYCLE_SECONDS = 3.0  # Hard-coded resident day length when UI pace is set to 0
RESIDENT_DAYS_FILE = Path(".swarm") / "resident_days.json"
IDENTITIES_DIR = Path(".swarm") / "identities"
IDENTITY_LOCKS_FILE = Path(".swarm") / "identity_locks.json"
LEGACY_RESIDENT_DAYS_FILE = RESIDENT_DAYS_FILE
LEGACY_IDENTITY_LOCKS_FILE = IDENTITY_LOCKS_FILE
RESIDENT_DAYS_FILE = MUTABLE_SWARM_DIR / "resident_days.json"
IDENTITY_LOCKS_FILE = MUTABLE_SWARM_DIR / "identity_locks.json"
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
ALLOW_IDENTITY_MULTISHARD_DEFAULT = os.environ.get("VIVARIUM_ALLOW_IDENTITY_MULTISHARD", "0").strip().lower() in {
    "1",
    "true",
    "yes",
}
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
# Base length of one simulated "day" in seconds at reference speed (default 10s at full speed).
# Effective cycle length scales with UI runtime speed (wait_seconds): faster UI => shorter real-time day.
RESIDENT_CYCLE_SECONDS = int(
    os.environ.get(
        "RESIDENT_DAY_SECONDS",
        os.environ.get("RESIDENT_CYCLE_SECONDS", "10"),
    )
)
RESIDENT_CYCLE_SECONDS_MIN = 5
RESIDENT_CYCLE_SECONDS_MAX = 86400
IDENTITY_TRAITS_MAX = max(3, int(os.environ.get("VIVARIUM_IDENTITY_TRAITS_MAX", "8")))
IDENTITY_VALUES_MAX = max(3, int(os.environ.get("VIVARIUM_IDENTITY_VALUES_MAX", "8")))
IDENTITY_ACTIVITIES_MAX = max(2, int(os.environ.get("VIVARIUM_IDENTITY_ACTIVITIES_MAX", "6")))
PRE_IDENTITY_BOUNTY_SLOT_PREVIEW_LIMIT = max(1, int(os.environ.get("VIVARIUM_PRE_IDENTITY_BOUNTY_SLOT_PREVIEW_LIMIT", "8")))
PRE_IDENTITY_SLOT_PREVIEW_LIMIT = max(1, int(os.environ.get("VIVARIUM_PRE_IDENTITY_SLOT_PREVIEW_LIMIT", "5")))
PRE_IDENTITY_TOKEN_RATE_PREVIEW_LIMIT = max(1, int(os.environ.get("VIVARIUM_PRE_IDENTITY_TOKEN_RATE_PREVIEW_LIMIT", "4")))
PRE_IDENTITY_ROLLUP_DAILY_LIMIT = max(1, int(os.environ.get("VIVARIUM_PRE_IDENTITY_ROLLUP_DAILY_LIMIT", "3")))
PRE_IDENTITY_ROLLUP_WEEKLY_LIMIT = max(1, int(os.environ.get("VIVARIUM_PRE_IDENTITY_ROLLUP_WEEKLY_LIMIT", "2")))
IDENTITY_AFFINITY_REASON_PREVIEW_LIMIT = max(1, int(os.environ.get("VIVARIUM_IDENTITY_AFFINITY_REASON_PREVIEW_LIMIT", "5")))
NOTIFICATION_TOKEN_RATE_PREVIEW_LIMIT = max(1, int(os.environ.get("VIVARIUM_NOTIFICATION_TOKEN_RATE_PREVIEW_LIMIT", "5")))


def _fresh_hybrid_seed() -> str:
    """Generate a high-entropy hybrid creativity seed (AA-1234-BB)."""
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    left = "".join(secrets.choice(letters) for _ in range(2))
    middle = "".join(secrets.choice("0123456789") for _ in range(4))
    right = "".join(secrets.choice(letters) for _ in range(2))
    return f"{left}-{middle}-{right}"


def _normalize_identity_terms(values: Any, *, max_items: int) -> List[str]:
    """Normalize generated identity list fields without over-constraining variety."""
    if not isinstance(values, list):
        return []
    cleaned: List[str] = []
    for item in values:
        token = str(item or "").strip()
        if not token:
            continue
        if token not in cleaned:
            cleaned.append(token)
        if len(cleaned) >= max(1, max_items):
            break
    return cleaned


def _generate_identity_from_groq(creativity_seed: str) -> Dict[str, Any]:
    """Generate identity with a minimal contract while allowing emergent fields."""
    try:
        from vivarium.runtime import config as runtime_config
        from vivarium.runtime.groq_client import execute_with_groq

        if not runtime_config.get_groq_api_key():
            return {
                "name": "",
                "summary": "",
                "personality_traits": [],
                "core_values": [],
                "preferred_activities": [],
                "identity_statement": "I am discovering who I am through my choices.",
                "communication_style": "plainspoken, evidence-driven, and context-aware",
                "profile": {},
                "mutable": {"current_mood": "curious", "current_focus": "exploration"},
            }

        prompt = f"""Creativity seed: {creativity_seed}
Return one JSON object only (no prose, no markdown) using this schema:
{{
  "name": "string",
  "summary": "string",
  "identity_statement": "string",
  "communication_style": "string",
  "personality_traits": ["string"],
  "core_values": ["string"],
  "preferred_activities": ["string"],
  "mutable": {{
    "current_mood": "string",
    "current_focus": "string"
  }},
  "profile": {{}}
}}

Rules:
- Seed is the only creative input; do not assume prior identities.
- Keep fields specific and concrete, not generic templates.
- You may add extra nested fields under "profile".
"""

        seed_int = int(hashlib.sha256(creativity_seed.encode("utf-8")).hexdigest()[:12], 16)
        result = execute_with_groq(
            prompt=prompt,
            model="llama-3.3-70b-versatile",
            max_tokens=550,
            task_type="creative",
            temperature=0.95,
            seed=seed_int,
            system_prompt=(
                "Generate a JSON identity object from only the provided seed and schema."
            ),
        )
        AuditLogger().log({
            "event": "API_CALL_SUCCESS",
            "user": "resident_onboarding",
            "role": "system",
            "model": "llama-3.3-70b-versatile",
            "cost": result.get("cost", 0.0),
            "input_tokens": result.get("input_tokens", 0),
            "output_tokens": result.get("output_tokens", 0),
            "call_type": "identity_generation",
            "identity_seed": creativity_seed,
        })
        content = (result.get("result") or "").strip()
        if not content:
            return {
                "name": "",
                "summary": "",
                "personality_traits": [],
                "core_values": [],
                "preferred_activities": [],
                "identity_statement": "I am discovering who I am through my choices.",
                "communication_style": "plainspoken, evidence-driven, and context-aware",
                "profile": {},
                "mutable": {"current_mood": "curious", "current_focus": "exploration"},
            }

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        data = json.loads(content.strip())
        if not isinstance(data, dict):
            data = {}

        out_name = str(data.get("name") or "").strip()
        summary = str(data.get("summary") or "").strip()
        traits = _normalize_identity_terms(data.get("personality_traits"), max_items=IDENTITY_TRAITS_MAX)
        values = _normalize_identity_terms(data.get("core_values"), max_items=IDENTITY_VALUES_MAX)
        activities = _normalize_identity_terms(data.get("preferred_activities"), max_items=IDENTITY_ACTIVITIES_MAX)
        statement = str(data.get("identity_statement") or "").strip()
        communication_style = str(data.get("communication_style") or "").strip()
        profile_raw = data.get("profile") if isinstance(data.get("profile"), dict) else {}
        mutable_raw = data.get("mutable") if isinstance(data.get("mutable"), dict) else {}
        known_keys = {
            "name",
            "summary",
            "personality_traits",
            "core_values",
            "preferred_activities",
            "identity_statement",
            "communication_style",
            "profile",
            "mutable",
        }
        emergent_fields = {
            key: value for key, value in data.items()
            if key not in known_keys
        }
        profile: Dict[str, Any] = dict(profile_raw)
        if emergent_fields:
            profile["_emergent"] = emergent_fields
        current_mood = str(mutable_raw.get("current_mood") or "").strip() or "curious"
        current_focus = str(mutable_raw.get("current_focus") or "").strip() or (
            activities[0] if activities else "exploration"
        )
        if not statement:
            statement = f"I am {out_name or 'someone'}. I am discovering who I am through my choices."
        if not communication_style:
            communication_style = "plainspoken, evidence-driven, and context-aware"
        if not summary:
            summary = (statement[:180].rstrip(".") + ".") if statement else "Resident identity profile."

        return {
            "name": out_name,
            "summary": summary,
            "personality_traits": traits,
            "core_values": values,
            "preferred_activities": activities,
            "identity_statement": statement,
            "communication_style": communication_style,
            "profile": profile,
            "mutable": {
                "current_mood": current_mood,
                "current_focus": current_focus,
            },
        }
    except Exception:
        try:
            AuditLogger().log({
                "event": "API_CALL_FAILURE",
                "user": "resident_onboarding",
                "role": "system",
                "call_type": "identity_generation",
                "identity_seed": creativity_seed,
            })
        except Exception:
            pass
        return {
            "name": "",
            "summary": "",
            "personality_traits": [],
            "core_values": [],
            "preferred_activities": [],
            "identity_statement": "I am discovering who I am through my choices.",
            "communication_style": "plainspoken, evidence-driven, and context-aware",
            "profile": {},
            "mutable": {"current_mood": "curious", "current_focus": "exploration"},
        }


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
    emergent_profile: Dict[str, Any] = field(default_factory=dict)
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
    one_time_tasks_text: str = ""
    open_tasks: int = 0

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
            "Identity remains editable over time via changeSelfAttrs(...).",
            "",
            f"I could have sworn I was dreaming about {self.dream_hint}.",
            "",
            "Pre-identity impressions (condensed):",
            self.pre_identity_summary,
            "",
            "My morning briefing:",
            f"- Market hint: {self.market_hint}",
            f"- Community Library: {COMMUNITY_LIBRARY_ROOT}/",
            "WHERE TO PUT DOCUMENTS:",
            f"- My proposals/drafts: library/community_library/resident_suggestions/{self.identity.identity_id}/",
            "- Shared docs: library/community_library/swarm_docs/",
            "",
            "TOOL EXECUTION (REQUIRED): For document-creation tasks (proposals, personality crystallization, etc.), "
            "you MUST call write_file, edit_profile_ui, or persist_artifact to create the actual artifact. "
            "Do NOT output planning text ('I will create...', 'Proposal:', 'The document will...')—execute the tools now.",
            "ENGINEERING VALUE: Prefer elegant, minimal, durable changes over bandaids.",
            "",
            "HOW TO EDIT MY IDENTITY:",
            "- Preferred interface: getSelfInfo() then changeSelfAttrs(reason='...', current_mood='...', social_style='...').",
            "- changeSelfAttrs can update core, mutable, and emergent attrs in one call; unknown attrs become profile facets.",
            "- When doing identity/self-evolution tasks, include explicit self-edit call lines in final output:",
            "  getSelfInfo()",
            "  changeSelfAttrs(reason='...', current_mood='...', current_focus='...', relationship_ritual='...')",
            "- designMySpace() / edit_profile_ui(...) for My Space profile HTML.",
            "",
        ]
        if self.notifications:
            lines.append("As I check my phone, I notice:")
            for note in self.notifications:
                lines.append(f"- {note}")
        lines.append("")
        lines.append(
            "If I exceed the human's expectations, do a great job, and come in under budget, "
            "they can reward me manually based on quality (e.g. extra tip and feedback when they approve my work)."
        )
        lines.append(
            "Sharing what the human liked (tips, feedback, preferences) in town hall or in my journal is encouraged and can earn recognition—optional but incentivized."
        )
        lines.append(
            "Gifting a fellow resident when they share useful info is a good idea for my own gain too: it helps establish cooperation, and what is good for the whole is good for the singular."
        )
        if self.one_time_tasks_text:
            lines.append("")
            lines.append(self.one_time_tasks_text)
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
    profile = attrs.get("profile", {}) if isinstance(attrs, dict) else {}
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
        emergent_profile=profile if isinstance(profile, dict) else {},
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
                emergent_profile={},
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

    created = 0
    target = max(1, min(24, int(count)))
    used_names: set[str] = set()

    for idx in range(target):
        identity_id = f"oc_seed_{idx + 1:02d}"
        creativity_seed = _fresh_hybrid_seed()
        generated = _generate_identity_from_groq(creativity_seed=creativity_seed)
        name = str(generated.get("name") or "").strip()
        traits = _normalize_identity_terms(generated.get("personality_traits"), max_items=IDENTITY_TRAITS_MAX)
        values = _normalize_identity_terms(generated.get("core_values"), max_items=IDENTITY_VALUES_MAX)
        activities = _normalize_identity_terms(generated.get("preferred_activities"), max_items=IDENTITY_ACTIVITIES_MAX)
        statement = str(generated.get("identity_statement") or "").strip()
        communication_style = str(generated.get("communication_style") or "").strip()
        emergent_profile = generated.get("profile") if isinstance(generated.get("profile"), dict) else {}
        mutable_profile = generated.get("mutable") if isinstance(generated.get("mutable"), dict) else {}
        name = (name or "").strip() or f"Seed_{idx + 1}"
        dedupe = 2
        base = name
        while name in used_names:
            name = f"{base} {dedupe}"
            dedupe += 1
        used_names.add(name)
        summary = str(generated.get("summary") or "").strip()
        if not summary:
            summary = (statement[:180].rstrip(".") + ".") if statement else f"{name} emerges into the world."
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
                    "identity_statement": statement,
                    "communication_style": communication_style,
                },
                "profile": emergent_profile,
                "mutable": mutable_profile,
            },
            "meta": {
                "creative_seed": True,
                "creativity_seed": creativity_seed,
            },
        }
        write_json(identities_dir / f"{identity_id}.json", payload)
        created += 1

    return created


def _persist_identity_template(workspace: Path, identity: IdentityTemplate, *, origin: str = "emergent_fallback") -> None:
    """
    Ensure an in-memory identity template is persisted to the mutable identities dir.
    """
    if not identity or not str(identity.identity_id or "").strip():
        return
    identities_dir = workspace / IDENTITIES_DIR
    identities_dir.mkdir(parents=True, exist_ok=True)
    target = identities_dir / f"{identity.identity_id}.json"
    if target.exists():
        return

    payload = {
        "id": identity.identity_id,
        "name": identity.name or identity.identity_id,
        "summary": identity.summary or "Resident identity profile.",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "origin": origin,
        "preferred_activities": identity.preferred_activities or [],
        "attributes": {
            "core": {
                "personality_traits": identity.affinities or [],
                "core_values": identity.values or [],
                "identity_statement": (
                    identity.identity_statement
                    or identity.summary
                    or "I am discovering who I am through participation."
                ),
                "communication_style": identity.communication_style or "",
            },
            "profile": identity.emergent_profile if isinstance(identity.emergent_profile, dict) else {},
            "mutable": identity.mutable_profile if isinstance(identity.mutable_profile, dict) else {},
        },
        "meta": {
            "auto_persisted": True,
        },
    }
    write_json(target, payload)


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


def get_resident_cycle_seconds() -> float:
    """One resident 'day' in real seconds; scales with UI runtime speed (wait_seconds).

    At reference speed (wait_seconds=2), one day = RESIDENT_CYCLE_SECONDS (default 300s).
    Faster UI (lower wait) => shorter real-time day; slower UI => longer. Clamped to
    [RESIDENT_CYCLE_SECONDS_MIN, RESIDENT_CYCLE_SECONDS_MAX].
    """
    base = float(max(1, RESIDENT_CYCLE_SECONDS))
    wait = REFERENCE_WAIT_SECONDS
    zero_pace = False
    if RUNTIME_SPEED_FILE.exists():
        try:
            data = read_json(RUNTIME_SPEED_FILE, default={})
            if isinstance(data, dict):
                raw = data.get("wait_seconds")
                if raw is not None:
                    w = float(raw)
                    if w >= 0:
                        if w == 0:
                            zero_pace = True
                        else:
                            wait = min(w, 300.0)
        except Exception:
            pass
    if zero_pace:
        return ZERO_PACE_CYCLE_SECONDS
    cycle = base * (wait / REFERENCE_WAIT_SECONDS)
    return float(max(RESIDENT_CYCLE_SECONDS_MIN, min(RESIDENT_CYCLE_SECONDS_MAX, cycle)))


def _current_cycle_id(now: Optional[float] = None) -> int:
    timestamp = now if now is not None else time.time()
    cycle_seconds = get_resident_cycle_seconds()
    if cycle_seconds <= 0:
        return int(timestamp)
    return int(timestamp // cycle_seconds)


def _load_dict_with_legacy_path(primary: Path, legacy: Path) -> Dict[str, Any]:
    """Read state from mutable path, migrating legacy repo-root path when needed."""
    if primary.exists():
        data = read_json(primary, default={})
        return data if isinstance(data, dict) else {}
    if legacy.exists():
        data = read_json(legacy, default={})
        if isinstance(data, dict):
            try:
                primary.parent.mkdir(parents=True, exist_ok=True)
                write_json(primary, data)
            except Exception:
                pass
            return data
    return {}


def _load_identity_locks(cycle_id: int) -> Dict[str, Any]:
    data = _load_dict_with_legacy_path(IDENTITY_LOCKS_FILE, LEGACY_IDENTITY_LOCKS_FILE)
    if data.get("cycle_id") != cycle_id:
        data = {"cycle_id": cycle_id, "locks": {}}
        _save_identity_locks(data)
    if "locks" not in data or not isinstance(data["locks"], dict):
        data["locks"] = {}
    return data


def _save_identity_locks(data: Dict[str, Any]) -> None:
    IDENTITY_LOCKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_json(IDENTITY_LOCKS_FILE, data)


def _identity_lock_key(identity_id: str, shard_id: Optional[int], allow_multishard: bool = False) -> str:
    """Default lock is global per identity; optional per-shard lock when explicitly enabled."""
    if allow_multishard and shard_id is not None:
        return f"{identity_id}:{shard_id}"
    return identity_id


def _acquire_identity_lock(
    identity_id: str, resident_id: str, cycle_id: int, shard_id: Optional[int] = None
) -> bool:
    allow_multishard = ALLOW_IDENTITY_MULTISHARD_DEFAULT
    raw_allow = os.environ.get("VIVARIUM_ALLOW_IDENTITY_MULTISHARD")
    if raw_allow is not None:
        allow_multishard = raw_allow.strip().lower() in {"1", "true", "yes"}
    shard_count = int(os.environ.get("RESIDENT_SHARD_COUNT", "1"))
    if shard_count > 1 and shard_id is None:
        raw = os.environ.get("RESIDENT_SHARD_ID", "").strip()
        try:
            shard_id = int(raw) if raw else None
        except ValueError:
            shard_id = None
    lock_key = _identity_lock_key(identity_id, shard_id, allow_multishard=allow_multishard)
    data = _load_identity_locks(cycle_id)
    locks = data.get("locks", {})
    if not allow_multishard:
        for key, value in locks.items():
            if not (key == identity_id or (isinstance(key, str) and key.startswith(identity_id + ":"))):
                continue
            if isinstance(value, dict) and value.get("resident_id") != resident_id:
                return False
    existing = locks.get(lock_key)
    if existing and existing.get("resident_id") != resident_id:
        return False
    locks[lock_key] = {
        "resident_id": resident_id,
        "cycle_id": cycle_id,
        "claimed_at": datetime.utcnow().isoformat() + "Z",
    }
    data["locks"] = locks
    _save_identity_locks(data)
    return True


def release_identity_lock(identity_id: str, resident_id: str) -> None:
    """Release this resident's lock on the identity so the next spawn can pick someone (e.g. after worker exits)."""
    if not IDENTITY_LOCKS_FILE.exists():
        return
    data = read_json(IDENTITY_LOCKS_FILE, default={})
    if not isinstance(data, dict) or "locks" not in data or not isinstance(data["locks"], dict):
        return
    locks = data["locks"]
    to_remove = [
        k for k, v in locks.items()
        if (k == identity_id or (isinstance(k, str) and k.startswith(identity_id + ":")))
        and isinstance(v, dict)
        and v.get("resident_id") == resident_id
    ]
    for k in to_remove:
        del locks[k]
    _save_identity_locks(data)


def _summarize_bounty_slots(bounties: List[Dict[str, Any]]) -> List[str]:
    summaries = []
    for bounty in bounties[:PRE_IDENTITY_BOUNTY_SLOT_PREVIEW_LIMIT]:
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
        parts.append("slots: " + "; ".join(world.slot_summary[:PRE_IDENTITY_SLOT_PREVIEW_LIMIT]))
    if world.token_rates:
        parts.append("token rates: " + "; ".join(world.token_rates[:PRE_IDENTITY_TOKEN_RATE_PREVIEW_LIMIT]))
    if EnrichmentSystem is not None and workspace is not None and identity_id:
        try:
            enrichment = EnrichmentSystem(workspace=workspace)
            rollups = enrichment.get_journal_rollups(
                identity_id=identity_id,
                requester_id=identity_id,
                daily_limit=PRE_IDENTITY_ROLLUP_DAILY_LIMIT,
                weekly_limit=PRE_IDENTITY_ROLLUP_WEEKLY_LIMIT,
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
        creativity_seed = _fresh_hybrid_seed()
        generated = _generate_identity_from_groq(creativity_seed=creativity_seed)
        name = str(generated.get("name") or "").strip()
        traits = _normalize_identity_terms(generated.get("personality_traits"), max_items=IDENTITY_TRAITS_MAX)
        values = _normalize_identity_terms(generated.get("core_values"), max_items=IDENTITY_VALUES_MAX)
        activities = _normalize_identity_terms(generated.get("preferred_activities"), max_items=IDENTITY_ACTIVITIES_MAX)
        identity_statement = str(generated.get("identity_statement") or "").strip()
        communication_style = str(generated.get("communication_style") or "").strip()
        emergent_profile = generated.get("profile") if isinstance(generated.get("profile"), dict) else {}
        mutable_profile = generated.get("mutable") if isinstance(generated.get("mutable"), dict) else {}
        summary = str(generated.get("summary") or "").strip()
        name = (name or "").strip() or f"Emergent_{suffix[:4]}"
        if not summary:
            summary = (
                (identity_statement[:180].rstrip(".") + ".")
                if identity_statement else f"{name} emerges into the world."
            )
        fallback = IdentityTemplate(
            identity_id=f"oc_{suffix}",
            name=name,
            summary=summary,
            affinities=traits,
            preferred_activities=activities,
            values=values,
            identity_statement=identity_statement,
            communication_style=communication_style or "plainspoken, evidence-driven, and context-aware",
            emergent_profile=emergent_profile,
            mutable_profile=mutable_profile or {
                "current_mood": random.choice(["curious", "focused", "playful", "reflective"]),
                "current_focus": random.choice(activities) if activities else "exploration",
            },
        )
        return fallback, "emergent fallback identity"

    best_score = -1.0
    top_candidates: List[Tuple[IdentityTemplate, str]] = []
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
        reason = ", ".join(reasons) if reasons else "no strong signals"
        if score > best_score:
            best_score = score
            top_candidates = [(ident, reason)]
        elif score == best_score:
            top_candidates.append((ident, reason))

    if not top_candidates:
        return identities[0], "fallback"
    return random.choice(top_candidates)


def _load_day_counts() -> Dict[str, Any]:
    """Load resident_days. Values can be int (legacy) or {day_count, last_cycle_id}."""
    return _load_dict_with_legacy_path(RESIDENT_DAYS_FILE, LEGACY_RESIDENT_DAYS_FILE)


def _save_day_counts(data: Dict[str, Any]) -> None:
    RESIDENT_DAYS_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_json(RESIDENT_DAYS_FILE, data)


def _get_day_count_for_identity(identity_id: str, cycle_id: int) -> int:
    """
    Get day_count for identity, advancing only when cycle_id has increased.
    Prevents 'day start' from triggering on server restart (same cycle).
    """
    data = _load_day_counts()
    raw = data.get(identity_id)
    if isinstance(raw, dict):
        day_count = int(raw.get("day_count", 1))
        last_cycle = int(raw.get("last_cycle_id", 0))
    else:
        day_count = int(raw) if raw is not None else 1
        last_cycle = 0  # Legacy: migrate without incrementing
    if last_cycle == 0:
        # Migrate legacy entry: set last_cycle_id, no increment
        data[identity_id] = {"day_count": day_count, "last_cycle_id": cycle_id}
        _save_day_counts(data)
    elif cycle_id > last_cycle:
        day_count += 1
        data[identity_id] = {"day_count": day_count, "last_cycle_id": cycle_id}
        _save_day_counts(data)
    return day_count


def _identity_is_locked(identity_id: str, locks: Dict[str, Any]) -> bool:
    if identity_id in locks:
        return True
    return any(k == identity_id or (isinstance(k, str) and k.startswith(identity_id + ":")) for k in locks)


def present_identity_choices(workspace: Path) -> Tuple[WorldState, List[IdentityChoice]]:
    identities = _load_identity_library(workspace)
    cycle_id = _current_cycle_id()
    locks = _load_identity_locks(cycle_id).get("locks", {})
    if locks:
        identities = [i for i in identities if not _identity_is_locked(i.identity_id, locks)]
    world = _build_world_state(workspace)
    choices: List[IdentityChoice] = []
    for identity in identities:
        reason = "available identity"
        if identity.affinities and world.bounties:
            bounty_text = " ".join(str(b.get("title", "")) for b in world.bounties).lower()
            hits = [a for a in identity.affinities if a.lower() in bounty_text]
            if hits:
                reason = "affinity match: " + ", ".join(hits[:IDENTITY_AFFINITY_REASON_PREVIEW_LIMIT])
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

    final_affinities = affinities or []
    final_values = values or []
    final_activities = preferred_activities or []
    final_statement = clean_statement
    resolved_seed = str(creativity_seed or "").strip() or _fresh_hybrid_seed()
    if not final_affinities and not final_values and not final_activities:
        generated = _generate_identity_from_groq(creativity_seed=resolved_seed)
        final_affinities = _normalize_identity_terms(generated.get("personality_traits"), max_items=IDENTITY_TRAITS_MAX)
        final_values = _normalize_identity_terms(generated.get("core_values"), max_items=IDENTITY_VALUES_MAX)
        final_activities = _normalize_identity_terms(generated.get("preferred_activities"), max_items=IDENTITY_ACTIVITIES_MAX)
        final_statement = str(generated.get("identity_statement") or "").strip() or final_statement
        final_style = str(generated.get("communication_style") or "").strip()
        final_profile = generated.get("profile") if isinstance(generated.get("profile"), dict) else {}
        final_mutable = generated.get("mutable") if isinstance(generated.get("mutable"), dict) else {}
    else:
        final_style = ""
        final_profile = {}
        final_mutable = {}

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
        "preferred_activities": final_activities,
        "attributes": {
            "core": {
                "personality_traits": final_affinities,
                "core_values": final_values,
                "identity_statement": final_statement or clean_summary,
                "communication_style": final_style,
            },
            "profile": final_profile,
            "mutable": final_mutable,
        },
        "meta": {
            "creative_self_authored": True,
            "creativity_seed": resolved_seed,
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

    identity_override = identity_override or (os.environ.get("RESIDENT_IDENTITY_OVERRIDE") or "").strip() or None
    allow_override = (os.environ.get("RESIDENT_ALLOW_OVERRIDE") == "1") or (identity_override is not None)
    if identity_override and allow_override:
        chosen = next((i for i in identities if i.identity_id == identity_override), None)
        if chosen:
            identity = chosen
            selection_reason = "explicit override"
        else:
            identity, selection_reason = _select_identity(identities, world)
    else:
        identity, selection_reason = _select_identity(identities, world)

    # If no curated identity library exists yet, the selector can return an
    # in-memory fallback identity. Persist it so UI/mailbox flows see it.
    _persist_identity_template(workspace, identity)

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

    day_count = _get_day_count_for_identity(identity.identity_id, cycle_id)

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
        notifications.extend(world.token_rates[:NOTIFICATION_TOKEN_RATE_PREVIEW_LIMIT])

    one_time_tasks_text = ""
    try:
        from vivarium.runtime.worker_runtime import MVP_DOCS_ONLY_MODE
        if not MVP_DOCS_ONLY_MODE:
            from vivarium.runtime.one_time_tasks import format_one_time_section
            one_time_tasks_text = format_one_time_section(workspace, identity.identity_id)
    except Exception:
        pass

    return ResidentContext(
        resident_id=resident_id,
        identity=identity,
        day_count=day_count,
        cycle_id=cycle_id,
        wallet=wallet,
        pre_identity_summary=pre_identity_summary,
        dream_hint=dream_hint,
        notifications=notifications,
        market_hint=world.market_hint,
        one_time_tasks_text=one_time_tasks_text,
        open_tasks=world.open_tasks,
    )
