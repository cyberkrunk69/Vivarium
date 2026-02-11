"""
Swarm Enrichment System - Hobbies, creative works, and social rewards.

When workers complete tasks under budget, they earn free time to:
- Write creatively (stories, poetry, worldbuilding)
- Collaborate with other identities
- Pursue personal interests
- Add to the shared universe

Creative works and shared docs are stored in the Community Library for all to enjoy.

Usage:
    from vivarium.runtime.swarm_enrichment import EnrichmentSystem, get_enrichment

    enrichment = get_enrichment()

    # After completing a task under budget
    if tokens_remaining > 0:
        enrichment.grant_free_time(identity_id, tokens_remaining)

    # Worker decides to write
    enrichment.start_creative_session(
        identity_id="identity_1",
        activity="collaborative_writing",
        invite=["identity_2"]  # Page Echo-7 to join
    )

    # Save their work
    enrichment.save_creative_work(
        title="The Mountains of Elsewhere - Chapter 3",
        authors=["identity_1", "identity_2"],
        content="...",
        work_type="shared_universe"
    )
"""

import json
import random
import secrets
import time
import math
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from statistics import mean, stdev
from vivarium.runtime.vivarium_scope import SECURITY_ROOT

# Import action logger for audit trail
try:
    from vivarium.runtime.action_logger import get_action_logger, ActionType
    _action_logger = get_action_logger()
except ImportError:
    _action_logger = None


@dataclass
class CreativeWork:
    """A piece of creative work made during free time."""
    id: str
    title: str
    authors: List[str]              # Identity IDs
    author_names: List[str]         # Display names
    content: str
    work_type: str                  # "story", "poem", "worldbuilding", "philosophy", "other"
    created_at: str

    # Metadata
    word_count: int = 0
    chapter: Optional[int] = None   # For serialized works
    series: Optional[str] = None    # For connected works
    tags: List[str] = field(default_factory=list)

    # Engagement
    read_by: List[str] = field(default_factory=list)  # Identity IDs who've read it
    reactions: Dict[str, List[str]] = field(default_factory=dict)  # emoji -> [identity_ids]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "author_names": self.author_names,
            "content": self.content,
            "work_type": self.work_type,
            "created_at": self.created_at,
            "word_count": self.word_count,
            "chapter": self.chapter,
            "series": self.series,
            "tags": self.tags,
            "read_by": self.read_by,
            "reactions": self.reactions
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CreativeWork':
        return cls(
            id=data["id"],
            title=data["title"],
            authors=data["authors"],
            author_names=data["author_names"],
            content=data["content"],
            work_type=data["work_type"],
            created_at=data["created_at"],
            word_count=data.get("word_count", 0),
            chapter=data.get("chapter"),
            series=data.get("series"),
            tags=data.get("tags", []),
            read_by=data.get("read_by", []),
            reactions=data.get("reactions", {})
        )


@dataclass
class SocialInvite:
    """An invitation to collaborate during free time."""
    id: str
    from_id: str
    from_name: str
    to_id: str
    to_name: str
    activity: str                   # "writing", "worldbuilding", "philosophy", "games"
    message: str
    location: str                   # "community_library", "watercooler", "creative_room"
    created_at: str
    status: str = "pending"         # "pending", "accepted", "declined", "expired"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "from_id": self.from_id,
            "from_name": self.from_name,
            "to_id": self.to_id,
            "to_name": self.to_name,
            "activity": self.activity,
            "message": self.message,
            "location": self.location,
            "created_at": self.created_at,
            "status": self.status
        }


class RewardCalculator:
    """
    Calculates scaled rewards based on performance metrics.

    Better performance = more free time = more practice = even better performance.
    This creates natural specialization through positive feedback loops.
    """

    # PHYSICS (IMMUTABLE) - reward scaling / gravity
    # Base token reward for completing any task
    BASE_TOKENS = 50

    # Multiplier tiers (immutable scaling)
    MULTIPLIERS = {
        "standard": 1.0,           # Met expectations
        "efficient": 1.5,          # Under budget/time
        "quality": 1.3,            # Above average quality
        "novel": 2.0,              # New approach or solution
        "exceptional": 3.0,        # Significantly above baseline
        "breakthrough": 5.0        # Genuine innovation
    }

    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.metrics_file = self.workspace / ".swarm" / "performance_metrics.json"
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_metrics(self) -> Dict[str, Any]:
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"by_task_type": {}, "by_identity": {}, "global": {"samples": []}}

    def _save_metrics(self, metrics: Dict[str, Any]):
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)

    def record_performance(
        self,
        identity_id: str,
        task_type: str,
        budget_used_pct: float,      # 0.0 to 1.0+ (can go over)
        quality_score: float,         # 0.0 to 1.0
        time_taken_pct: float,        # vs estimated, 0.0 to 1.0+
        novel_solution: bool = False,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Record a performance sample and return the calculated reward.

        Returns dict with: tokens, multiplier, tier, breakdown
        """
        metrics = self._load_metrics()

        # Initialize structures if needed
        if task_type not in metrics["by_task_type"]:
            metrics["by_task_type"][task_type] = {"samples": []}
        if identity_id not in metrics["by_identity"]:
            metrics["by_identity"][identity_id] = {"samples": [], "specializations": {}}

        # Create sample
        sample = {
            "timestamp": datetime.now().isoformat(),
            "identity_id": identity_id,
            "task_type": task_type,
            "budget_used_pct": budget_used_pct,
            "quality_score": quality_score,
            "time_taken_pct": time_taken_pct,
            "novel_solution": novel_solution,
            "description": description
        }

        # Add to all relevant collections
        metrics["by_task_type"][task_type]["samples"].append(sample)
        metrics["by_identity"][identity_id]["samples"].append(sample)
        metrics["global"]["samples"].append(sample)

        # Keep collections manageable (last 100 samples each)
        for key in ["by_task_type", "by_identity"]:
            for subkey in metrics[key]:
                if len(metrics[key][subkey]["samples"]) > 100:
                    metrics[key][subkey]["samples"] = metrics[key][subkey]["samples"][-100:]
        if len(metrics["global"]["samples"]) > 500:
            metrics["global"]["samples"] = metrics["global"]["samples"][-500:]

        # Calculate reward
        reward = self._calculate_reward(sample, metrics, task_type)

        # Track specialization
        if task_type not in metrics["by_identity"][identity_id]["specializations"]:
            metrics["by_identity"][identity_id]["specializations"][task_type] = {
                "count": 0, "avg_quality": 0.0, "rewards_earned": 0
            }
        spec = metrics["by_identity"][identity_id]["specializations"][task_type]
        spec["count"] += 1
        spec["avg_quality"] = (spec["avg_quality"] * (spec["count"]-1) + quality_score) / spec["count"]
        spec["rewards_earned"] += reward["tokens"]

        self._save_metrics(metrics)

        return reward

    def _calculate_reward(
        self,
        sample: Dict[str, Any],
        metrics: Dict[str, Any],
        task_type: str
    ) -> Dict[str, Any]:
        """Calculate reward based on performance vs baseline."""

        multiplier = 1.0
        tier = "standard"
        breakdown = []

        # Get baseline for this task type
        task_samples = metrics["by_task_type"].get(task_type, {}).get("samples", [])

        if len(task_samples) >= 5:
            # We have enough history to compare
            avg_budget = mean([s["budget_used_pct"] for s in task_samples[-20:]])
            avg_quality = mean([s["quality_score"] for s in task_samples[-20:]])
            avg_time = mean([s["time_taken_pct"] for s in task_samples[-20:]])

            # Efficiency bonus (under budget)
            if sample["budget_used_pct"] < avg_budget * 0.8:
                multiplier *= self.MULTIPLIERS["efficient"]
                tier = "efficient"
                breakdown.append(f"Efficient: {sample['budget_used_pct']:.0%} vs avg {avg_budget:.0%}")

            # Quality bonus
            if sample["quality_score"] > avg_quality * 1.2:
                multiplier *= self.MULTIPLIERS["quality"]
                if tier == "standard":
                    tier = "quality"
                breakdown.append(f"Quality: {sample['quality_score']:.0%} vs avg {avg_quality:.0%}")

            # Exceptional performance (multiple metrics way above average)
            exceptional_count = 0
            if sample["budget_used_pct"] < avg_budget * 0.5:
                exceptional_count += 1
            if sample["quality_score"] > avg_quality * 1.5:
                exceptional_count += 1
            if sample["time_taken_pct"] < avg_time * 0.5:
                exceptional_count += 1

            if exceptional_count >= 2:
                multiplier = max(multiplier, self.MULTIPLIERS["exceptional"])
                tier = "exceptional"
                breakdown.append("Exceptional: Multiple metrics significantly above average")

        else:
            # Not enough history - use absolute thresholds
            if sample["budget_used_pct"] < 0.7:
                multiplier *= 1.3
                breakdown.append("Under budget (no baseline yet)")
            if sample["quality_score"] > 0.8:
                multiplier *= 1.2
                breakdown.append("High quality (no baseline yet)")

        # Novel solution bonus (always applies)
        if sample["novel_solution"]:
            multiplier *= self.MULTIPLIERS["novel"]
            tier = "novel" if tier in ["standard", "efficient", "quality"] else tier
            breakdown.append("Novel solution")

        # Breakthrough detection (exceptional + novel)
        if sample["novel_solution"] and tier == "exceptional":
            multiplier = self.MULTIPLIERS["breakthrough"]
            tier = "breakthrough"
            breakdown.append("BREAKTHROUGH: Exceptional novel solution!")

        tokens = int(self.BASE_TOKENS * multiplier)

        return {
            "tokens": tokens,
            "multiplier": multiplier,
            "tier": tier,
            "breakdown": breakdown,
            "base_tokens": self.BASE_TOKENS
        }

    def get_identity_specializations(self, identity_id: str) -> Dict[str, Any]:
        """Get an identity's emerging specializations."""
        metrics = self._load_metrics()
        return metrics.get("by_identity", {}).get(identity_id, {}).get("specializations", {})

    def get_leaderboard(self, task_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performers overall or for a specific task type."""
        metrics = self._load_metrics()

        scores = []
        for identity_id, data in metrics.get("by_identity", {}).items():
            if task_type:
                spec = data.get("specializations", {}).get(task_type, {})
                if spec.get("count", 0) > 0:
                    scores.append({
                        "identity_id": identity_id,
                        "task_type": task_type,
                        "count": spec["count"],
                        "avg_quality": spec["avg_quality"],
                        "rewards_earned": spec["rewards_earned"]
                    })
            else:
                total_rewards = sum(s.get("rewards_earned", 0) for s in data.get("specializations", {}).values())
                total_tasks = sum(s.get("count", 0) for s in data.get("specializations", {}).values())
                if total_tasks > 0:
                    scores.append({
                        "identity_id": identity_id,
                        "total_tasks": total_tasks,
                        "total_rewards": total_rewards,
                        "avg_reward": total_rewards / total_tasks
                    })

        # Sort by rewards
        key = "rewards_earned" if task_type else "total_rewards"
        scores.sort(key=lambda x: x.get(key, 0), reverse=True)

        return scores[:limit]


class EnrichmentSystem:
    """Manages hobbies, creative works, and social rewards."""

    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)
        self.library_dir = self.workspace / "library" / "creative_works"
        self.library_dir.mkdir(parents=True, exist_ok=True)
        self.community_library_dir = self.workspace / "library" / "community_library"
        self.community_library_dir.mkdir(parents=True, exist_ok=True)
        self.discussions_dir = self.workspace / ".swarm" / "discussions"
        self.discussions_dir.mkdir(parents=True, exist_ok=True)

        # Initialize reward calculator
        self.rewards = RewardCalculator(workspace)

        self.invites_file = self.workspace / ".swarm" / "social_invites.jsonl"
        self.invites_file.parent.mkdir(parents=True, exist_ok=True)

        self.free_time_file = self.workspace / ".swarm" / "free_time_balances.json"
        self.journals_dir = self.workspace / ".swarm" / "journals"
        self.journals_dir.mkdir(parents=True, exist_ok=True)
        self.journal_votes_file = self.workspace / ".swarm" / "journal_votes.json"
        self.journal_rollups_file = self.workspace / ".swarm" / "journal_rollups.json"
        self.journal_penalties_file = self.workspace / ".swarm" / "journal_penalties.json"
        self.task_review_votes_file = self.workspace / ".swarm" / "task_review_votes.json"
        self.wind_down_allowance_file = self.workspace / ".swarm" / "daily_wind_down_allowance.json"
        self.guild_votes_file = self.workspace / ".swarm" / "guild_votes.json"
        self.disputes_file = self.workspace / ".swarm" / "disputes.json"
        self.privilege_suspensions_file = self.workspace / ".swarm" / "privilege_suspensions.json"

        # Shared universe registry
        self.universe_file = self.library_dir / "shared_universe_index.json"

        # Gift economy files
        self.gifts_file = self.workspace / ".swarm" / "gift_history.jsonl"
        self.gratitude_file = self.workspace / ".swarm" / "gratitude.json"
        self.commons_file = self.workspace / ".swarm" / "commons_pool.json"
        self.collab_pools_file = self.workspace / ".swarm" / "collaborative_pools.json"

        # Tool creation registry
        self.tools_registry_file = self.workspace / ".swarm" / "tools_registry.json"

        # Collective performance tracking
        self.performance_file = self.workspace / ".swarm" / "collective_performance.json"
        self.milestones_file = self.workspace / ".swarm" / "milestones_achieved.json"

        # Test tracking
        self.tests_registry_file = self.workspace / ".swarm" / "tests_registry.json"

        # Recognition and efficiency tracking
        self.recognition_file = self.workspace / ".swarm" / "recognition.json"
        self.personal_bests_file = self.workspace / ".swarm" / "personal_bests.json"
        self.efficiency_pool_file = self.workspace / ".swarm" / "efficiency_pool.json"

        # Bounty and guild system
        self.bounties_file = self.workspace / ".swarm" / "bounties.json"
        self.guilds_file = self.workspace / ".swarm" / "guilds.json"
        self.legacy_teams_file = self.workspace / ".swarm" / "teams.json"

    DISCUSSION_ROOMS = (
        "town_hall",
        "human_async",
        "watercooler",
        "improvements",
        "struggles",
        "discoveries",
        "project_war_room",
    )

    # Memory compression and recall policy (centralized tuning knobs).
    MEMORY_SUMMARY_MAX_CHARS = 220
    MEMORY_SUMMARY_RECENT_ENTRY_COUNT = 4
    MEMORY_SUMMARY_RECENT_SNIPPET_CHARS = 80
    MEMORY_SUMMARY_TOP_TERMS = 4
    MEMORY_SUMMARY_SNIPPETS = 2
    MEMORY_TERM_MIN_LENGTH = 5
    MEMORY_ROLLUP_DAILY_RETAIN = 45
    MEMORY_ROLLUP_WEEKLY_RETAIN = 16

    MEMORY_RECALL_DEFAULT_LIMIT = 5
    MEMORY_RECALL_MAX_LIMIT = 12
    MEMORY_RECALL_MIN_CHARS = 160
    MEMORY_RECALL_MAX_CHARS = 2000
    MEMORY_RECALL_DAILY_WINDOW = 8
    MEMORY_RECALL_WEEKLY_WINDOW = 4
    MEMORY_RECALL_RECENT_ENTRIES = 20
    MEMORY_RECALL_ENTRY_PREVIEW_CHARS = 220
    CONTEXT_RECENT_JOURNAL_LIMIT = 4
    CONTEXT_ROLLUP_DAILY_LIMIT = 3
    CONTEXT_ROLLUP_WEEKLY_LIMIT = 2

    MEMORY_STOP_WORDS = frozenset(
        {
            "about", "after", "again", "being", "could", "there", "their", "which", "would",
            "should", "while", "through", "because", "these", "those", "where", "when", "what",
            "from", "with", "that", "this", "have", "just", "into", "over", "under", "your",
            "ours", "theirs", "them", "they", "been", "were", "will", "than", "then", "also",
        }
    )

    def _normalize_discussion_room(self, room: str) -> str:
        raw = str(room or "").strip().lower()
        if not raw:
            return "town_hall"
        slug = re.sub(r"[^a-z0-9_]+", "_", raw).strip("_")
        if slug.startswith("dispute_"):
            return slug
        return slug or "town_hall"

    def _human_username(self) -> str:
        """Load operator display name from local UI settings; default to 'human'."""
        settings_file = SECURITY_ROOT / "local_ui_settings.json"
        try:
            if settings_file.exists():
                with open(settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    value = str(data.get("human_username") or "").strip()
                    if value:
                        return value
        except Exception:
            pass
        return "human"

    def _fresh_creativity_seed(self) -> str:
        """Return a fresh hybrid creativity seed (letters+digits)."""
        letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
        left = "".join(secrets.choice(letters) for _ in range(2))
        middle = "".join(secrets.choice("0123456789") for _ in range(4))
        right = "".join(secrets.choice(letters) for _ in range(2))
        return f"{left}-{middle}-{right}"

    def _discussion_room_file(self, room: str) -> Path:
        normalized = self._normalize_discussion_room(room)
        return self.discussions_dir / f"{normalized}.jsonl"

    def _normalize_dm_identity(self, identity_id: str) -> str:
        token = re.sub(r"[^a-zA-Z0-9_-]+", "", str(identity_id or "").strip())
        return token[:80]

    def _direct_room_name(self, identity_a: str, identity_b: str) -> str:
        left = self._normalize_dm_identity(identity_a)
        right = self._normalize_dm_identity(identity_b)
        if not left or not right or left == right:
            return ""
        first, second = sorted([left, right])
        return f"dm__{first}__{second}"

    def _parse_direct_room_name(self, room: str) -> Optional[Tuple[str, str]]:
        raw = str(room or "").strip().lower()
        match = re.match(r"^dm__([a-z0-9_-]+)__([a-z0-9_-]+)$", raw)
        if not match:
            return None
        return match.group(1), match.group(2)

    def get_discussion_messages(self, room: str, limit: int = 50) -> List[Dict[str, Any]]:
        room_file = self._discussion_room_file(room)
        if not room_file.exists():
            return []
        messages: List[Dict[str, Any]] = []
        try:
            with open(room_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except OSError:
            return []
        if limit <= 0:
            return messages
        return messages[-limit:]

    def post_discussion_message(
        self,
        identity_id: str,
        identity_name: str,
        content: str,
        room: str = "town_hall",
        mood: Optional[str] = None,
        importance: int = 3,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Post a resident update into a shared discussion room."""
        text = str(content or "").strip()
        if not text:
            return {"success": False, "reason": "content_empty"}

        normalized_room = self._normalize_discussion_room(room)
        room_file = self._discussion_room_file(normalized_room)
        room_file.parent.mkdir(parents=True, exist_ok=True)

        clipped = text[:1200]
        safe_importance = max(1, min(5, int(importance))) if isinstance(importance, int) else 3
        message = {
            "id": f"chat_{normalized_room}_{int(time.time() * 1000)}_{str(identity_id)[-6:]}",
            "author_id": identity_id,
            "author_name": identity_name or identity_id,
            "content": clipped,
            "room": normalized_room,
            "timestamp": datetime.now().isoformat(),
            "mood": (str(mood).strip()[:32] if mood else None),
            "importance": safe_importance,
            "reply_to": (str(reply_to).strip()[:120] if reply_to else None),
        }

        with open(room_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=True) + "\n")

        if _action_logger:
            preview = clipped.replace("\n", " ").strip()
            if len(preview) > 80:
                preview = preview[:77] + "..."
            _action_logger.log(
                ActionType.SOCIAL,
                f"chat_{normalized_room}",
                preview or "(empty)",
                actor=identity_id,
            )

        return {"success": True, "room": normalized_room, "message": message}

    def post_direct_message(
        self,
        sender_id: str,
        sender_name: str,
        recipient_id: str,
        content: str,
        importance: int = 3,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Post a private resident-to-resident DM in a direct-message room."""
        sender = self._normalize_dm_identity(sender_id)
        recipient = self._normalize_dm_identity(recipient_id)
        if not sender or not recipient:
            return {"success": False, "reason": "invalid_identity"}
        if sender == recipient:
            return {"success": False, "reason": "same_identity"}
        room = self._direct_room_name(sender, recipient)
        if not room:
            return {"success": False, "reason": "room_unavailable"}
        result = self.post_discussion_message(
            identity_id=sender,
            identity_name=sender_name or sender,
            content=content,
            room=room,
            mood="private",
            importance=importance,
            reply_to=reply_to,
        )
        if not result.get("success"):
            return result
        message = dict(result.get("message") or {})
        message["direct"] = True
        message["recipient_id"] = recipient
        room_file = self._discussion_room_file(room)
        try:
            with open(room_file, "rb+") as f:
                lines = f.readlines()
                if lines:
                    lines[-1] = (json.dumps(message, ensure_ascii=True) + "\n").encode("utf-8")
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
        except OSError:
            pass

        if _action_logger:
            preview = str(content or "").replace("\n", " ").strip()
            if len(preview) > 80:
                preview = preview[:77] + "..."
            _action_logger.log(
                ActionType.SOCIAL,
                "direct_message",
                f"{sender} -> {recipient}: {preview or '(empty)'}",
                actor=sender,
            )
        return {"success": True, "room": room, "message": message}

    def get_direct_messages(self, identity_id: str, peer_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        room = self._direct_room_name(identity_id, peer_id)
        if not room:
            return []
        return self.get_discussion_messages(room, limit=limit)

    def get_direct_threads(self, identity_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        identity = self._normalize_dm_identity(identity_id)
        if not identity or not self.discussions_dir.exists():
            return []
        threads: List[Dict[str, Any]] = []
        for room_file in self.discussions_dir.glob("dm__*__*.jsonl"):
            room = room_file.stem
            parsed = self._parse_direct_room_name(room)
            if not parsed:
                continue
            left, right = parsed
            if identity not in {left, right}:
                continue
            peer_id = right if identity == left else left
            latest_timestamp = None
            latest_preview = None
            message_count = 0
            try:
                with open(room_file, "r", encoding="utf-8") as f:
                    lines = [ln for ln in f if ln.strip()]
                message_count = len(lines)
                for line in reversed(lines):
                    msg = json.loads(line)
                    latest_timestamp = msg.get("timestamp")
                    author = msg.get("author_name") or msg.get("author_id") or "Unknown"
                    content = str(msg.get("content") or "")
                    latest_preview = f"{author}: {content[:60]}{'...' if len(content) > 60 else ''}"
                    break
            except Exception:
                pass
            threads.append(
                {
                    "room": room,
                    "peer_id": peer_id,
                    "message_count": message_count,
                    "latest_timestamp": latest_timestamp,
                    "latest_preview": latest_preview,
                }
            )
        threads.sort(key=lambda t: t.get("latest_timestamp") or "", reverse=True)
        if limit > 0:
            threads = threads[:limit]
        return threads

    def get_discussion_context(
        self,
        identity_id: str,
        identity_name: str,
        limit_per_room: int = 4,
    ) -> str:
        """Build compact cross-room discussion snapshot for prompt injection."""
        rows: List[str] = []
        room_recent_samples: List[str] = []
        total_messages = 0
        total_self_messages = 0

        for room in self.DISCUSSION_ROOMS:
            room_limit = max(limit_per_room * 3, 24) if room == "town_hall" else max(limit_per_room * 2, 10)
            messages = self.get_discussion_messages(room, limit=room_limit)
            if not messages:
                continue
            total_messages += len(messages)
            self_count = sum(1 for msg in messages if str(msg.get("author_id") or "") == str(identity_id))
            total_self_messages += self_count
            participants = {
                str(msg.get("author_name") or msg.get("author_id") or "unknown").strip()
                for msg in messages
                if str(msg.get("author_name") or msg.get("author_id") or "").strip()
            }
            latest = messages[-1] if messages else {}
            latest_author = str(latest.get("author_name") or latest.get("author_id") or "unknown").strip()
            latest_ts = str(latest.get("timestamp") or "")[:16]
            rows.append(
                f"- {room}: msgs={len(messages)}, peers={len(participants)}, "
                f"mine={self_count}, latest={latest_author}@{latest_ts}"
            )
            sample_count = max(1, min(int(limit_per_room), 2))
            samples: List[str] = []
            for msg in messages[-sample_count:]:
                author = str(msg.get("author_name") or msg.get("author_id") or "unknown").strip()
                text = str(msg.get("content") or "").strip().replace("\n", " ")
                if not text:
                    continue
                if len(text) > 90:
                    text = text[:87] + "..."
                samples.append(f"{author}: {text}")
            if samples:
                room_recent_samples.append(f"- {room} recent={' | '.join(samples)}")

        dm_threads = self.get_direct_threads(identity_id, limit=6)
        dm_count = len(dm_threads)
        dm_messages = sum(int(t.get("message_count") or 0) for t in dm_threads)
        dm_peers = [str(t.get("peer_id") or "").strip() for t in dm_threads[:3] if str(t.get("peer_id") or "").strip()]

        if not rows and dm_count == 0:
            return (
                "SWARM DISCUSSION MEMORY\n"
                "- No social traffic yet.\n"
                "- town_hall runs at machine speed for resident coordination.\n"
                "- human_async is asynchronous because human time is slower than resident time."
            )

        lines = [
            "SWARM DISCUSSION MEMORY (COMPACT SNAPSHOT)",
            f"- I am {identity_name}. I stay social while executing tasks.",
            "- Summary is generated from live message metadata (no inferred recap).",
            f"- shared_msgs={total_messages}, my_msgs={total_self_messages}, dm_threads={dm_count}, dm_msgs={dm_messages}",
            "- Room activity:",
        ]
        lines.extend(rows[:8])
        if room_recent_samples:
            lines.append("- Recent message samples:")
            lines.extend(room_recent_samples[:4])
        if dm_peers:
            lines.append(f"- active_dm_peers={', '.join(dm_peers)}")
        return "\n".join(lines)

    # ═══════════════════════════════════════════════════════════════════
    # CASCADING NAME UPDATE SYSTEM
    # ═══════════════════════════════════════════════════════════════════

    def cascade_name_update(self, identity_id: str, old_name: str, new_name: str) -> dict:
        """
        Update all references to an identity's name across the system.
        Called automatically when an identity respecs their name.

        Updates:
        - messages_to_human.jsonl (from_name field)
        - Discussion board messages (author_name field)
        - Action log entries (actor field, if using name)

        Returns a summary of what was updated.
        """
        updates = {
            "messages_to_human": 0,
            "discussion_messages": 0,
            "errors": []
        }

        # 1. Update messages_to_human.jsonl
        messages_file = self.workspace / ".swarm" / "messages_to_human.jsonl"
        if messages_file.exists():
            try:
                updated_lines = []
                with open(messages_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            msg = json.loads(line)
                            if msg.get('from_id') == identity_id:
                                msg['from_name'] = new_name
                                updates["messages_to_human"] += 1
                            updated_lines.append(json.dumps(msg))

                with open(messages_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(updated_lines) + '\n' if updated_lines else '')
            except Exception as e:
                updates["errors"].append(f"messages_to_human: {str(e)}")

        # 2. Update discussion board messages
        discussion_dir = self.workspace / ".swarm" / "discussions"
        if discussion_dir.exists():
            for room_file in discussion_dir.glob("*.jsonl"):
                try:
                    updated_lines = []
                    with open(room_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                msg = json.loads(line)
                                if msg.get('author_id') == identity_id:
                                    msg['author_name'] = new_name
                                    updates["discussion_messages"] += 1
                                updated_lines.append(json.dumps(msg))

                    with open(room_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(updated_lines) + '\n' if updated_lines else '')
                except Exception as e:
                    updates["errors"].append(f"discussion/{room_file.name}: {str(e)}")

        # Log the cascade update
        if _action_logger:
            total = updates["messages_to_human"] + updates["discussion_messages"]
            _action_logger.log(
                ActionType.IDENTITY,
                "name_cascade",
                f"{old_name} -> {new_name}: updated {total} references",
                actor=identity_id
            )

        return updates

    # ═══════════════════════════════════════════════════════════════════
    # TOKEN ECONOMY CONFIGURATION
    # PHYSICS (IMMUTABLE): reward scaling, punishment, gravity
    # ═══════════════════════════════════════════════════════════════════
    #
    # Two pools: FREE_TIME (socializing, exploring) and JOURNAL (learning, memory)
    # Journaling is an INVESTMENT - it pays dividends back to free time
    #
    # ═══════════════════════════════════════════════════════════════════

    # Pool caps (default - can be increased through investment)
    MAX_FREE_TIME_TOKENS = 1000      # Cap for free time (socializing, exploring)
    MAX_JOURNAL_TOKENS = 200        # Cap for journaling (persisted learning)
    BASE_FREE_TIME_CAP = 500        # Starting cap (can grow)

    # Earning split: when granted tokens, how to divide them
    FREE_TIME_SPLIT = 0.70          # 70% goes to free time
    JOURNAL_SPLIT = 0.30            # 30% goes to journaling

    # Journal review + rewards (community reviewed)
    JOURNAL_ATTEMPT_COST = 10
    JOURNAL_MIN_REFUND_RATE = 0.50      # Accepted floor: 50% refund (still net negative)
    JOURNAL_MAX_REFUND_RATE = 1.00      # Max refund (100% return)
    JOURNAL_MAX_BONUS_RATE = 1.00       # Bonus up to +100% (total 2x)
    JOURNAL_BONUS_CURVE = 1.5           # Aggressive curve for high scores
    JOURNAL_MIN_VOTES = 3               # Minimum votes required to resolve
    JOURNAL_GAMING_THRESHOLD = 0.50     # >= 50% gaming votes triggers penalty
    JOURNAL_PENALTY_MULTIPLIER = 1.25   # 1.25x attempt cost
    JOURNAL_PENALTY_DAYS = 2
    BLIND_VOTE_MIN_REASON_CHARS = 3
    JOURNAL_REVIEW_EXCERPT_MAX_CHARS = 280
    JOURNAL_VOTE_SCORES = {
        "reject": 0,
        "accept": 1,
        "exceptional": 2,
        "gaming": 0
    }

    # Guild join voting
    GUILD_JOIN_MIN_VOTES = 2
    GUILD_JOIN_APPROVAL_RATIO = 0.60
    GUILD_JOIN_VOTE_TYPES = ["accept", "reject"]

    # Dispute system
    DISPUTE_PENALTY_DAYS = 2
    DISPUTE_ALLOWED_PRIVILEGES = ["sunday_bonus", "movie_night"]

    # Quality thresholds (word count + content markers) - heuristic only
    MIN_JOURNAL_WORDS = 50
    QUALITY_JOURNAL_WORDS = 150
    EXCEPTIONAL_MARKERS = [
        "realized", "learned", "discovered", "insight", "breakthrough",
        "pattern", "connection", "understand", "mistake", "correction",
        "hypothesis", "theory", "observation", "evidence"
    ]

    # ═══════════════════════════════════════════════════════════════════
    # GIFT ECONOMY CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════
    #
    # Gifts not trades. No debt tracking. Decay prevents accumulation.
    # Commons pool funds shared resources. Gratitude is free recognition.
    #
    # ═══════════════════════════════════════════════════════════════════

    # Gift limits (prevent large wealth transfers)
    MAX_GIFT_AMOUNT = 50            # Max tokens per gift
    MAX_DAILY_GIFTED = 100          # Max tokens gifted per day per identity

    # Transfer decay (prevents trading, funds commons)
    GIFT_DECAY_RATE = 0.20          # 20% goes to commons pool

    # Collaborative pools
    MAX_POOL_CONTRIBUTION = 100     # Max contribution per identity per pool
    POOL_DRAW_LIMIT = 50            # Max draw per session from pool

    # ═══════════════════════════════════════════════════════════════════
    # TOOL CREATION REWARDS
    # ═══════════════════════════════════════════════════════════════════
    #
    # Creating reusable tools benefits everyone. Reward accordingly.
    #
    # ═══════════════════════════════════════════════════════════════════

    TOOL_BASE_REWARD = 75           # Base tokens for creating a tool
    TOOL_DOCSTRING_BONUS = 25       # Bonus for having docstrings
    TOOL_TYPEHINTS_BONUS = 25       # Bonus for type hints
    TOOL_TESTS_BONUS = 25           # Bonus for including tests
    TOOL_FIRST_USE_BONUS = 50       # Bonus when another identity uses your tool
    TOOL_SUBSEQUENT_USE_BONUS = 10  # Bonus per additional use
    TOOL_MAX_USE_BONUSES = 5        # Cap on subsequent use bonuses

    # ═══════════════════════════════════════════════════════════════════
    # COLLECTIVE PERFORMANCE & MILESTONES
    # ═══════════════════════════════════════════════════════════════════
    #
    # When the swarm performs well collectively, EVERYONE benefits.
    # Creates shared fate, peer accountability, and guild spirit.
    #
    # ═══════════════════════════════════════════════════════════════════

    # Milestone definitions: (tasks_required, min_quality, min_efficiency, reward_type)
    MILESTONES = {
        "bronze": {
            "tasks": 20,
            "quality": 0.80,         # 80% quality score
            "efficiency": None,       # No efficiency requirement
            "reward_tokens": 50,      # Everyone gets +50
            "reward_cap": 0,          # No cap increase
            "day_off": False
        },
        "silver": {
            "tasks": 50,
            "quality": 0.85,
            "efficiency": 15,         # 15 tasks per dollar
            "reward_tokens": 100,
            "reward_cap": 25,         # +25 to everyone's cap
            "day_off": False
        },
        "gold": {
            "tasks": 100,
            "quality": 0.90,
            "efficiency": 20,
            "reward_tokens": 150,
            "reward_cap": 50,
            "day_off": True           # Everyone gets a day off!
        },
        "diamond": {
            "tasks": 200,
            "quality": 0.92,
            "efficiency": 25,
            "reward_tokens": 250,
            "reward_cap": 100,
            "day_off": True
        }
    }

    # Efficiency baseline: tasks per dollar
    EFFICIENCY_BASELINE = 10  # 10 tasks/$1 = 100% efficiency

    # ═══════════════════════════════════════════════════════════════════
    # TEST WRITING REWARDS
    # ═══════════════════════════════════════════════════════════════════
    #
    # Tests are extremely valuable: they verify, prevent regressions,
    # document behavior, and enable confident refactoring.
    #
    # ═══════════════════════════════════════════════════════════════════

    TEST_BASE_REWARD = 30           # Base for writing any test
    TEST_PER_ASSERTION = 5          # Per meaningful assertion (capped)
    TEST_MAX_ASSERTION_BONUS = 50   # Cap on assertion bonuses
    TEST_COVERAGE_BONUS = 2         # Per % coverage increase
    TEST_CATCHES_BUG_BONUS = 75     # When test catches a regression later
    TEST_CRITICAL_PATH_BONUS = 25   # Tests for critical/core functionality
    TEST_DOCUMENTATION_BONUS = 15   # Well-documented test with clear intent

    # ═══════════════════════════════════════════════════════════════════
    # RECOGNITION SYSTEM - Celebrate success, don't shame failure
    # ═══════════════════════════════════════════════════════════════════
    #
    # Multiple categories so different strengths shine.
    # Only show top performers, never "worst" lists.
    #
    # ═══════════════════════════════════════════════════════════════════

    RECOGNITION_CATEGORIES = [
        "efficiency_star",      # Best tasks/cost ratio
        "quality_champion",     # Highest verification rate
        "test_hero",           # Most bugs caught / coverage
        "tool_builder",        # Most useful tools created
        "collaborator",        # Most gratitude received
        "rising_star",         # Most improved this period
        "mentor"               # Helped most other identities
    ]

    RECOGNITION_TOP_N = 3           # Show top 3 per category
    MONTHLY_STAR_REWARD = 100       # 1st place reward
    RUNNER_UP_REWARD = 50           # 2nd/3rd place reward
    PERSONAL_BEST_REWARD = 25       # Beat your own record

    # ═══════════════════════════════════════════════════════════════════
    # TOKEN EFFICIENCY POOL - Collective savings, shared rewards
    # ═══════════════════════════════════════════════════════════════════
    #
    # When the swarm is efficient, savings go to a pool that's
    # distributed to everyone. My efficiency helps the guild.
    #
    # ═══════════════════════════════════════════════════════════════════

    TOKEN_BASELINE_PER_TASK = 50    # Expected tokens per task (baseline)
    EFFICIENCY_POOL_RATE = 0.50     # 50% of savings go to pool
    WEEKLY_EFFICIENCY_BONUS_10 = 25 # Bonus if 10%+ improvement
    WEEKLY_EFFICIENCY_BONUS_20 = 50 # Bonus if 20%+ improvement
    DAILY_WIND_DOWN_TOKENS = 150    # Free daily wind-down allowance

    # Quality refund system - under budget + above quality goal
    QUALITY_REFUND_GOAL = 0.85
    QUALITY_REFUND_INDIVIDUAL_RATE = 0.50
    QUALITY_REFUND_GUILD_RATE = 0.25
    COLLAB_REFUND_MULTIPLIER = 1.15

    def grant_free_time(self, identity_id: str, tokens: int, reason: str = "under_budget"):
        """
        Grant tokens to an identity, SPLIT between free time and journaling pools.

        Split: 70% free time, 30% journaling
        Each pool has its own cap.

        Returns dict with both balances.
        """
        balances = self._load_free_time_balances()

        # Initialize identity if needed
        if identity_id not in balances:
            balances[identity_id] = {
                "tokens": 0,              # Free time pool
                "journal_tokens": 0,      # Journal pool
                "free_time_cap": self.BASE_FREE_TIME_CAP,  # Can grow
                "history": [],
                "spending_history": []
            }

        # Migrate old format if needed
        if "journal_tokens" not in balances[identity_id]:
            balances[identity_id]["journal_tokens"] = 0
        if "free_time_cap" not in balances[identity_id]:
            balances[identity_id]["free_time_cap"] = self.BASE_FREE_TIME_CAP

        # Split tokens between pools
        free_time_portion = int(tokens * self.FREE_TIME_SPLIT)
        journal_portion = tokens - free_time_portion  # Remainder to journal

        # Get current caps (free time cap can grow)
        free_time_cap = balances[identity_id]["free_time_cap"]
        journal_cap = self.MAX_JOURNAL_TOKENS

        # Apply free time tokens (with cap)
        old_free = balances[identity_id]["tokens"]
        new_free = min(old_free + free_time_portion, free_time_cap)
        actual_free_granted = new_free - old_free

        # Apply journal tokens (with cap)
        old_journal = balances[identity_id]["journal_tokens"]
        new_journal = min(old_journal + journal_portion, journal_cap)
        actual_journal_granted = new_journal - old_journal

        # Update balances
        balances[identity_id]["tokens"] = new_free
        balances[identity_id]["journal_tokens"] = new_journal

        # Record history
        balances[identity_id]["history"].append({
            "granted_total": tokens,
            "free_time_granted": actual_free_granted,
            "journal_granted": actual_journal_granted,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "free_capped": actual_free_granted < free_time_portion,
            "journal_capped": actual_journal_granted < journal_portion
        })

        # Keep history manageable
        if len(balances[identity_id]["history"]) > 20:
            balances[identity_id]["history"] = balances[identity_id]["history"][-20:]

        self._save_free_time_balances(balances)

        # Log to action logger
        total_granted = actual_free_granted + actual_journal_granted
        if _action_logger:
            detail = f"+{actual_free_granted} free, +{actual_journal_granted} journal | {reason}"
            _action_logger.log(
                ActionType.IDENTITY,
                "tokens",
                detail,
                actor=identity_id
            )

        print(f"[ENRICHMENT] {identity_id}: +{actual_free_granted} free time, +{actual_journal_granted} journal ({reason})")
        print(f"             Balances: {new_free}/{free_time_cap} free, {new_journal}/{journal_cap} journal")

        return {
            "free_time": new_free,
            "journal": new_journal,
            "free_time_cap": free_time_cap,
            "granted": {
                "free_time": actual_free_granted,
                "journal": actual_journal_granted
            }
        }

    def get_free_time(self, identity_id: str) -> int:
        """Get remaining free time tokens for an identity."""
        balances = self._load_free_time_balances()
        return balances.get(identity_id, {}).get("tokens", 0)

    def get_journal_tokens(self, identity_id: str) -> int:
        """Get remaining journal tokens for an identity."""
        balances = self._load_free_time_balances()
        return balances.get(identity_id, {}).get("journal_tokens", 0)

    def get_all_balances(self, identity_id: str) -> dict:
        """Get all token balances for an identity."""
        self._grant_daily_wind_down_allowance(identity_id)
        balances = self._load_free_time_balances()
        identity_data = balances.get(identity_id, {})
        return {
            "free_time": identity_data.get("tokens", 0),
            "journal": identity_data.get("journal_tokens", 0),
            "free_time_cap": identity_data.get("free_time_cap", self.BASE_FREE_TIME_CAP)
        }

    def _load_wind_down_allowance(self) -> dict:
        if self.wind_down_allowance_file.exists():
            try:
                with open(self.wind_down_allowance_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
            except Exception:
                pass
        return {}

    def _save_wind_down_allowance(self, data: dict) -> None:
        self.wind_down_allowance_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.wind_down_allowance_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _grant_daily_wind_down_allowance(self, identity_id: str) -> dict:
        """Grant free daily wind-down tokens once per UTC day."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        ledger = self._load_wind_down_allowance()
        key = str(identity_id or "").strip()
        if not key:
            return {"granted": False, "reason": "invalid_identity"}
        if str(ledger.get(key) or "") == today:
            return {"granted": False, "reason": "already_granted", "day": today}

        balances = self._load_free_time_balances()
        if key not in balances:
            balances[key] = {
                "tokens": 0,
                "journal_tokens": 0,
                "free_time_cap": self.BASE_FREE_TIME_CAP,
                "history": [],
                "spending_history": [],
            }
        free_cap = int(balances[key].get("free_time_cap", self.BASE_FREE_TIME_CAP) or self.BASE_FREE_TIME_CAP)
        old_tokens = int(balances[key].get("tokens", 0) or 0)
        desired_new = old_tokens + self.DAILY_WIND_DOWN_TOKENS
        if desired_new > free_cap:
            balances[key]["free_time_cap"] = desired_new
            free_cap = desired_new
        balances[key]["tokens"] = min(desired_new, free_cap)
        balances[key].setdefault("history", []).append(
            {
                "granted_total": self.DAILY_WIND_DOWN_TOKENS,
                "free_time_granted": self.DAILY_WIND_DOWN_TOKENS,
                "journal_granted": 0,
                "reason": "daily_wind_down_allowance",
                "timestamp": datetime.now().isoformat(),
            }
        )
        balances[key]["history"] = balances[key]["history"][-60:]
        self._save_free_time_balances(balances)
        ledger[key] = today
        self._save_wind_down_allowance(ledger)

        if _action_logger:
            _action_logger.log(
                ActionType.IDENTITY,
                "daily_wind_down_allowance",
                f"+{self.DAILY_WIND_DOWN_TOKENS} free-time tokens",
                actor=key,
            )

        return {"granted": True, "day": today, "tokens": self.DAILY_WIND_DOWN_TOKENS}

    def wind_down(
        self,
        identity_id: str,
        tokens: int = 150,
        activity: str = "bedtime_wind_down",
        journal_entry: str = None,
    ) -> dict:
        """
        End-of-day wind-down: grants daily allowance then spends chosen amount.
        Residents can spend beyond 150 from their own bank if desired.
        """
        allowance = self._grant_daily_wind_down_allowance(identity_id)
        spend = max(0, int(tokens))
        result = self.spend_free_time(
            identity_id=identity_id,
            tokens=spend,
            activity=activity,
            journal_entry=journal_entry,
        )
        if isinstance(result, dict):
            result["wind_down_allowance"] = allowance
            result["daily_free_tokens"] = self.DAILY_WIND_DOWN_TOKENS
        return result

    def _load_journal_votes(self) -> dict:
        if self.journal_votes_file.exists():
            try:
                with open(self.journal_votes_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "journals" in data:
                        return data
            except Exception:
                pass
        return {"journals": {}}

    def _save_journal_votes(self, votes: dict):
        self.journal_votes_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.journal_votes_file, 'w') as f:
            json.dump(votes, f, indent=2)

    def _load_journal_penalties(self) -> dict:
        if self.journal_penalties_file.exists():
            try:
                with open(self.journal_penalties_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_journal_penalties(self, penalties: dict):
        self.journal_penalties_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.journal_penalties_file, 'w') as f:
            json.dump(penalties, f, indent=2)

    def _load_guild_votes(self) -> dict:
        if self.guild_votes_file.exists():
            try:
                with open(self.guild_votes_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "requests" in data:
                        return data
            except Exception:
                pass
        return {"requests": {}}

    def _save_guild_votes(self, votes: dict):
        self.guild_votes_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.guild_votes_file, 'w') as f:
            json.dump(votes, f, indent=2)

    def _load_disputes(self) -> dict:
        if self.disputes_file.exists():
            try:
                with open(self.disputes_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "disputes" in data:
                        return data
            except Exception:
                pass
        return {"disputes": {}}

    def _save_disputes(self, disputes: dict):
        self.disputes_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.disputes_file, 'w') as f:
            json.dump(disputes, f, indent=2)

    def _load_privilege_suspensions(self) -> dict:
        if self.privilege_suspensions_file.exists():
            try:
                with open(self.privilege_suspensions_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_privilege_suspensions(self, suspensions: dict):
        self.privilege_suspensions_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.privilege_suspensions_file, 'w') as f:
            json.dump(suspensions, f, indent=2)

    def _is_privilege_suspended(self, identity_id: str, privilege: str) -> bool:
        suspensions = self._load_privilege_suspensions()
        identity_susp = suspensions.get(identity_id, {})
        record = identity_susp.get(privilege)
        if not record:
            return False
        until = record.get("until")
        if not until:
            return False
        if datetime.now().isoformat() < until:
            return True
        # Expired, clean up
        del identity_susp[privilege]
        if not identity_susp:
            suspensions.pop(identity_id, None)
        else:
            suspensions[identity_id] = identity_susp
        self._save_privilege_suspensions(suspensions)
        return False

    def _suspend_privilege(self, identity_id: str, privilege: str, days: int, reason: str) -> dict:
        suspensions = self._load_privilege_suspensions()
        identity_susp = suspensions.get(identity_id, {})
        until = (datetime.now() + timedelta(days=days)).isoformat()
        identity_susp[privilege] = {
            "until": until,
            "reason": reason,
            "applied_at": datetime.now().isoformat()
        }
        suspensions[identity_id] = identity_susp
        self._save_privilege_suspensions(suspensions)
        return identity_susp[privilege]

    def get_pending_guild_requests(self, identity_id: str, limit: int = 10) -> list:
        """List pending guild join requests for guilds the identity belongs to."""
        my_guild = self.get_my_guild(identity_id)
        if not my_guild:
            return []

        votes = self._load_guild_votes()
        pending = []
        for req in votes.get("requests", {}).values():
            if req.get("status") != "pending":
                continue
            if req.get("guild_id") != my_guild.get("id"):
                continue
            pending.append({
                "request_id": req.get("request_id"),
                "applicant_id": req.get("applicant_id"),
                "applicant_name": req.get("applicant_name"),
                "message": req.get("message"),
                "created_at": req.get("created_at")
            })

        pending.sort(key=lambda r: r.get("created_at", ""), reverse=True)
        return pending[:limit]

    def request_guild_join(self, identity_id: str, identity_name: str, guild_id: str,
                           message: str = None) -> dict:
        """Request to join a guild (triggers blind approval vote)."""
        if self.get_my_guild(identity_id):
            return {"success": False, "reason": "already_on_guild"}

        guild = self.get_guild(guild_id)
        if not guild:
            return {"success": False, "reason": "guild_not_found"}

        votes = self._load_guild_votes()
        for req in votes.get("requests", {}).values():
            if req.get("status") == "pending" and req.get("applicant_id") == identity_id and req.get("guild_id") == guild_id:
                return {"success": False, "reason": "request_already_pending"}

        request_id = f"guild_req_{guild_id}_{int(time.time()*1000)}"
        votes["requests"][request_id] = {
            "request_id": request_id,
            "guild_id": guild_id,
            "guild_name": guild.get("name"),
            "applicant_id": identity_id,
            "applicant_name": identity_name,
            "message": (message or "").strip(),
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "votes": []
        }
        self._save_guild_votes(votes)

        return {"success": True, "status": "pending", "request_id": request_id}

    def open_vote_dispute(self, target_type: str, target_id: str, requester_id: str,
                          requester_name: str, reason: str,
                          risk_privilege: str = "sunday_bonus") -> dict:
        """
        Open a dispute on a vote outcome (journal or guild join).

        A dispute creates a dedicated chatroom for the involved parties plus
        an objective mediator.
        """
        if target_type not in ["journal", "guild_join"]:
            return {"success": False, "reason": "invalid_target_type"}
        if not reason or len(reason.strip()) < self.BLIND_VOTE_MIN_REASON_CHARS:
            return {"success": False, "reason": "reason_required"}
        if risk_privilege not in self.DISPUTE_ALLOWED_PRIVILEGES:
            return {"success": False, "reason": "invalid_privilege"}

        participants = []
        decision_status = None

        if target_type == "journal":
            votes = self._load_journal_votes()
            journal = votes.get("journals", {}).get(target_id)
            if not journal:
                return {"success": False, "reason": "journal_not_found"}
            decision_status = journal.get("status")
            if decision_status == "pending":
                return {"success": False, "reason": "vote_not_resolved"}
            participants = [journal.get("author_id")] + [v.get("voter_id") for v in journal.get("votes", [])]
        else:
            votes = self._load_guild_votes()
            request = votes.get("requests", {}).get(target_id)
            if not request:
                return {"success": False, "reason": "request_not_found"}
            decision_status = request.get("status")
            if decision_status == "pending":
                return {"success": False, "reason": "vote_not_resolved"}
            participants = [request.get("applicant_id")] + [v.get("voter_id") for v in request.get("votes", [])]

        participants = [p for p in participants if p]
        participants = list(dict.fromkeys(participants))

        disputes = self._load_disputes()
        dispute_id = f"dispute_{target_type}_{int(time.time()*1000)}"
        chatroom_id = f"dispute_{target_type}_{target_id}"

        disputes["disputes"][dispute_id] = {
            "dispute_id": dispute_id,
            "target_type": target_type,
            "target_id": target_id,
            "requester_id": requester_id,
            "requester_name": requester_name,
            "reason": reason.strip(),
            "risk_privilege": risk_privilege,
            "status": "open",
            "decision_status": decision_status,
            "participants": participants,
            "mediator": None,
            "chatroom_id": chatroom_id,
            "created_at": datetime.now().isoformat()
        }
        self._save_disputes(disputes)

        # Create dispute chatroom with a system message
        self.discussions_dir.mkdir(parents=True, exist_ok=True)
        room_file = self.discussions_dir / f"{chatroom_id}.jsonl"
        system_msg = {
            "author_id": "SYSTEM",
            "author_name": "SYSTEM",
            "content": (
                f"Dispute opened ({target_type}:{target_id}). "
                "Participants: " + ", ".join(participants) +
                ". Awaiting mediator wearing Hat of Objectivity."
            ),
            "timestamp": datetime.now().isoformat(),
            "type": "system"
        }
        with open(room_file, 'a') as f:
            f.write(json.dumps(system_msg) + "\n")

        return {"success": True, "dispute_id": dispute_id, "chatroom_id": chatroom_id}

    def assign_dispute_mediator(self, dispute_id: str, mediator_id: str,
                                mediator_name: str, hat_name: str) -> dict:
        """Assign an objective mediator (must wear Hat of Objectivity)."""
        disputes = self._load_disputes()
        dispute = disputes.get("disputes", {}).get(dispute_id)
        if not dispute:
            return {"success": False, "reason": "dispute_not_found"}
        if dispute.get("status") != "open":
            return {"success": False, "reason": "dispute_not_open"}
        if mediator_id in dispute.get("participants", []):
            return {"success": False, "reason": "mediator_must_be_third_party"}
        if hat_name.strip().lower() != "hat of objectivity":
            return {"success": False, "reason": "hat_required"}

        dispute["mediator"] = {
            "id": mediator_id,
            "name": mediator_name,
            "hat": hat_name
        }
        disputes["disputes"][dispute_id] = dispute
        self._save_disputes(disputes)

        room_file = self.discussions_dir / f"{dispute['chatroom_id']}.jsonl"
        system_msg = {
            "author_id": "SYSTEM",
            "author_name": "SYSTEM",
            "content": f"Mediator assigned: {mediator_name} wearing {hat_name}.",
            "timestamp": datetime.now().isoformat(),
            "type": "system"
        }
        with open(room_file, 'a') as f:
            f.write(json.dumps(system_msg) + "\n")

        return {"success": True, "dispute_id": dispute_id, "mediator": dispute["mediator"]}

    def resolve_dispute(self, dispute_id: str, outcome: str, notes: str = None) -> dict:
        """Resolve a dispute: uphold or reopen the underlying vote."""
        if outcome not in ["uphold", "reopen"]:
            return {"success": False, "reason": "invalid_outcome"}

        disputes = self._load_disputes()
        dispute = disputes.get("disputes", {}).get(dispute_id)
        if not dispute:
            return {"success": False, "reason": "dispute_not_found"}
        if dispute.get("status") != "open":
            return {"success": False, "reason": "dispute_not_open"}
        if not dispute.get("mediator"):
            return {"success": False, "reason": "mediator_required"}

        if outcome == "reopen":
            if dispute["target_type"] == "journal":
                votes = self._load_journal_votes()
                journal = votes.get("journals", {}).get(dispute["target_id"])
                if journal:
                    journal["status"] = "pending"
                    journal["votes"] = []
                    journal["reopened_at"] = datetime.now().isoformat()
                    votes["journals"][dispute["target_id"]] = journal
                    self._save_journal_votes(votes)
            else:
                votes = self._load_guild_votes()
                request = votes.get("requests", {}).get(dispute["target_id"])
                if request:
                    request["status"] = "pending"
                    request["votes"] = []
                    request["reopened_at"] = datetime.now().isoformat()
                    votes["requests"][dispute["target_id"]] = request
                    self._save_guild_votes(votes)
        else:
            penalty = self._suspend_privilege(
                dispute["requester_id"],
                dispute["risk_privilege"],
                self.DISPUTE_PENALTY_DAYS,
                reason="dispute_upheld"
            )
            dispute["penalty"] = penalty

        dispute["status"] = "resolved"
        dispute["outcome"] = outcome
        dispute["notes"] = (notes or "").strip()
        dispute["resolved_at"] = datetime.now().isoformat()
        disputes["disputes"][dispute_id] = dispute
        self._save_disputes(disputes)

        room_file = self.discussions_dir / f"{dispute['chatroom_id']}.jsonl"
        system_msg = {
            "author_id": "SYSTEM",
            "author_name": "SYSTEM",
            "content": f"Dispute resolved: {outcome}.",
            "timestamp": datetime.now().isoformat(),
            "type": "system"
        }
        with open(room_file, 'a') as f:
            f.write(json.dumps(system_msg) + "\n")

        return {"success": True, "dispute_id": dispute_id, "outcome": outcome}

    def submit_guild_vote(self, request_id: str, voter_id: str, vote: str, reason: str) -> dict:
        """Submit a blind vote to accept/reject a guild join request (reason required)."""
        if vote not in self.GUILD_JOIN_VOTE_TYPES:
            return {"success": False, "reason": "invalid_vote"}
        if not reason or len(reason.strip()) < self.BLIND_VOTE_MIN_REASON_CHARS:
            return {"success": False, "reason": "reason_required"}

        votes = self._load_guild_votes()
        request = votes.get("requests", {}).get(request_id)
        if not request:
            return {"success": False, "reason": "request_not_found"}
        if request.get("status") != "pending":
            return {"success": False, "reason": "request_already_resolved"}
        if voter_id == request.get("applicant_id"):
            return {"success": False, "reason": "applicant_cannot_vote"}

        guild = self.get_guild(request.get("guild_id"))
        if not guild or voter_id not in guild.get("members", []):
            return {"success": False, "reason": "not_guild_member"}

        existing_votes = request.get("votes", [])
        if any(v.get("voter_id") == voter_id for v in existing_votes):
            return {"success": False, "reason": "already_voted"}

        existing_votes.append({
            "voter_id": voter_id,
            "vote": vote,
            "reason": reason.strip(),
            "timestamp": datetime.now().isoformat()
        })
        request["votes"] = existing_votes
        votes["requests"][request_id] = request
        self._save_guild_votes(votes)

        return {"success": True, "request_id": request_id, "vote": vote}

    def finalize_guild_vote(self, request_id: str) -> dict:
        """Resolve a guild join request once enough votes are present."""
        votes = self._load_guild_votes()
        request = votes.get("requests", {}).get(request_id)
        if not request:
            return {"success": False, "reason": "request_not_found"}
        if request.get("status") != "pending":
            return {"success": False, "reason": "request_already_resolved", "status": request.get("status")}

        vote_list = request.get("votes", [])
        if len(vote_list) < self.GUILD_JOIN_MIN_VOTES:
            return {
                "success": False,
                "reason": "insufficient_votes",
                "votes": len(vote_list),
                "required": self.GUILD_JOIN_MIN_VOTES
            }

        accepts = len([v for v in vote_list if v.get("vote") == "accept"])
        rejects = len([v for v in vote_list if v.get("vote") == "reject"])
        total = accepts + rejects
        approval_ratio = accepts / total if total else 0

        applicant_id = request.get("applicant_id")
        applicant_name = request.get("applicant_name", "Unknown")
        guild_id = request.get("guild_id")

        decision = "accepted" if approval_ratio >= self.GUILD_JOIN_APPROVAL_RATIO else "rejected"

        if decision == "accepted":
            if self.get_my_guild(applicant_id):
                decision = "rejected"
                rejection_reason = "already_on_guild"
            else:
                guilds = self._load_guilds()
                guild = next((g for g in guilds if g["id"] == guild_id), None)
                if not guild:
                    return {"success": False, "reason": "guild_not_found"}
                guild["members"].append(applicant_id)
                guild["member_names"][applicant_id] = applicant_name
                self._save_guilds(guilds)
                rejection_reason = None
        else:
            rejection_reason = None

        request["status"] = decision
        request["resolved_at"] = datetime.now().isoformat()
        request["result"] = {
            "accepts": accepts,
            "rejects": rejects,
            "approval_ratio": round(approval_ratio, 2),
            "decision": decision,
            "reasons": [v.get("reason") for v in vote_list if v.get("reason")],
            "rejection_reason": rejection_reason
        }

        votes["requests"][request_id] = request
        self._save_guild_votes(votes)

        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "guild_join_vote",
                f"{decision.upper()}: {applicant_name} -> {request.get('guild_name', '')}",
                actor="SYSTEM"
            )

        return {"success": True, "request_id": request_id, "status": decision, "result": request["result"]}

    def _get_active_journal_penalty(self, identity_id: str) -> Optional[dict]:
        penalties = self._load_journal_penalties()
        penalty = penalties.get(identity_id)
        if not penalty:
            return None

        until = penalty.get("until")
        if not until:
            return None

        if datetime.now().isoformat() < until:
            return penalty

        del penalties[identity_id]
        self._save_journal_penalties(penalties)
        return None

    def _apply_journal_penalty(self, identity_id: str, reason: str) -> dict:
        penalties = self._load_journal_penalties()
        until = (datetime.now() + timedelta(days=self.JOURNAL_PENALTY_DAYS)).isoformat()
        penalty = {
            "multiplier": self.JOURNAL_PENALTY_MULTIPLIER,
            "until": until,
            "reason": reason,
            "applied_at": datetime.now().isoformat()
        }
        penalties[identity_id] = penalty
        self._save_journal_penalties(penalties)
        return penalty

    def get_pending_journal_reviews(
        self,
        limit: int = 10,
        reviewer_id: Optional[str] = None,
        include_author: bool = False,
    ) -> list:
        """List pending blind-review journals without revealing author identity."""
        votes = self._load_journal_votes()
        pending = []
        for entry in votes.get("journals", {}).values():
            if entry.get("status") != "pending":
                continue
            author_id = entry.get("author_id")
            if reviewer_id and reviewer_id == author_id:
                continue
            payload = {
                "journal_id": entry.get("journal_id"),
                "created_at": entry.get("created_at"),
                "journal_type": entry.get("journal_type"),
                "content_preview": entry.get("review_excerpt") or entry.get("content_preview"),
                "word_count": entry.get("word_count"),
                "attempt_cost": entry.get("attempt_cost"),
                "quality_estimate": entry.get("quality_estimate"),
                "blind_review": True,
            }
            if include_author:
                payload["author_id"] = author_id
                payload["author_name"] = entry.get("author_name")
            pending.append(payload)

        pending.sort(key=lambda e: e.get("created_at", ""), reverse=True)
        return pending[:limit]

    def submit_journal_vote(self, journal_id: str, voter_id: str, vote: str, reason: str) -> dict:
        """Submit a blind vote for a journal review (reason required)."""
        if vote not in self.JOURNAL_VOTE_SCORES:
            return {"success": False, "reason": "invalid_vote"}
        if not reason or len(reason.strip()) < self.BLIND_VOTE_MIN_REASON_CHARS:
            return {"success": False, "reason": "reason_required"}

        votes = self._load_journal_votes()
        journal = votes.get("journals", {}).get(journal_id)
        if not journal:
            return {"success": False, "reason": "journal_not_found"}
        if journal.get("status") != "pending":
            return {"success": False, "reason": "journal_already_resolved"}
        if voter_id == journal.get("author_id"):
            return {"success": False, "reason": "author_cannot_vote"}

        existing_votes = journal.get("votes", [])
        if any(v.get("voter_id") == voter_id for v in existing_votes):
            return {"success": False, "reason": "already_voted"}

        existing_votes.append({
            "voter_id": voter_id,
            "vote": vote,
            "reason": reason.strip(),
            "timestamp": datetime.now().isoformat()
        })
        journal["votes"] = existing_votes
        votes["journals"][journal_id] = journal
        self._save_journal_votes(votes)

        return {"success": True, "journal_id": journal_id, "vote": vote}

    def finalize_journal_review(self, journal_id: str) -> dict:
        """Resolve a journal review once enough votes are present."""
        votes = self._load_journal_votes()
        journal = votes.get("journals", {}).get(journal_id)
        if not journal:
            return {"success": False, "reason": "journal_not_found"}
        if journal.get("status") != "pending":
            return {"success": False, "reason": "journal_already_resolved", "status": journal.get("status")}

        vote_list = journal.get("votes", [])
        if len(vote_list) < self.JOURNAL_MIN_VOTES:
            return {
                "success": False,
                "reason": "insufficient_votes",
                "votes": len(vote_list),
                "required": self.JOURNAL_MIN_VOTES
            }

        scores = []
        gaming_votes = 0
        for vote in vote_list:
            vote_value = vote.get("vote")
            if vote_value == "gaming":
                gaming_votes += 1
            if vote_value in self.JOURNAL_VOTE_SCORES:
                scores.append(self.JOURNAL_VOTE_SCORES[vote_value])

        if not scores:
            return {"success": False, "reason": "no_valid_votes"}

        avg_score = sum(scores) / len(scores)
        gaming_ratio = gaming_votes / max(len(scores), 1)
        gaming_flagged = gaming_ratio >= self.JOURNAL_GAMING_THRESHOLD

        attempt_cost = int(journal.get("attempt_cost", self.JOURNAL_ATTEMPT_COST))
        author_id = journal.get("author_id")
        author_name = journal.get("author_name", "Unknown")

        result = {
            "avg_score": round(avg_score, 2),
            "gaming_votes": gaming_votes,
            "total_votes": len(scores),
            "gaming_flagged": gaming_flagged,
            "attempt_cost": attempt_cost,
            "refund_rate": 0.0,
            "bonus_rate": 0.0,
            "refund_tokens": 0,
            "bonus_tokens": 0,
            "total_awarded": 0,
            "reasons": [v.get("reason") for v in vote_list if v.get("reason")]
        }

        if gaming_flagged:
            penalty = self._apply_journal_penalty(author_id, reason="gaming_flagged")
            result["penalty"] = penalty
            journal["status"] = "rejected"
        elif avg_score >= 1.0:
            score_norm = min(max((avg_score - 1.0) / 1.0, 0.0), 1.0)
            refund_rate = self.JOURNAL_MIN_REFUND_RATE + (
                (self.JOURNAL_MAX_REFUND_RATE - self.JOURNAL_MIN_REFUND_RATE) * score_norm
            )
            bonus_rate = self.JOURNAL_MAX_BONUS_RATE * (score_norm ** self.JOURNAL_BONUS_CURVE)

            refund_tokens = math.ceil(attempt_cost * refund_rate)
            bonus_tokens = int(attempt_cost * bonus_rate)
            total_awarded = min(refund_tokens + bonus_tokens, attempt_cost * 2)
            if refund_tokens + bonus_tokens > total_awarded:
                bonus_tokens = max(0, total_awarded - refund_tokens)

            balances = self._load_free_time_balances()
            if author_id not in balances:
                balances[author_id] = {
                    "tokens": 0,
                    "journal_tokens": 0,
                    "free_time_cap": self.BASE_FREE_TIME_CAP,
                    "history": [],
                    "spending_history": []
                }

            cap = balances[author_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
            old_balance = balances[author_id]["tokens"]
            balances[author_id]["tokens"] = min(old_balance + total_awarded, cap)
            applied_award = balances[author_id]["tokens"] - old_balance
            self._save_free_time_balances(balances)

            result.update({
                "refund_rate": round(refund_rate, 3),
                "bonus_rate": round(bonus_rate, 3),
                "refund_tokens": refund_tokens,
                "bonus_tokens": bonus_tokens,
                "total_awarded": applied_award
            })
            journal["status"] = "accepted"

            if _action_logger and applied_award > 0:
                _action_logger.log(
                    ActionType.IDENTITY,
                    "journal_reward",
                    f"+{applied_award} tokens (community journal reward)",
                    actor=author_id
                )
        else:
            journal["status"] = "rejected"

        journal["resolved_at"] = datetime.now().isoformat()
        # Privacy guarantee: clear temporary review text after vote is finalized.
        journal.pop("review_excerpt", None)
        journal.pop("content_preview", None)
        journal["result"] = result
        votes["journals"][journal_id] = journal
        self._save_journal_votes(votes)

        print(f"[JOURNAL REVIEW] {author_name}: {journal['status']} (score {result['avg_score']})")

        return {"success": True, "journal_id": journal_id, "status": journal["status"], "result": result}

    # ═══════════════════════════════════════════════════════════════════
    # TASK COMMUNITY REVIEW - Blind vote before surfacing to user approval
    # ═══════════════════════════════════════════════════════════════════

    TASK_REVIEW_JURY_SIZE = 3   # Randomly selected jurors (jury duty); no reward-milking
    TASK_REVIEW_MIN_VOTES = 2   # Votes required to finalize (e.g. 2 of 3 jurors)
    TASK_REVIEW_EXCERPT_MAX = 500
    TASK_REVIEW_MIN_REASON_CHARS = 10

    def _load_task_review_votes(self) -> dict:
        if self.task_review_votes_file.exists():
            try:
                with open(self.task_review_votes_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "tasks" in data:
                        return data
            except Exception:
                pass
        return {"tasks": {}}

    def _save_task_review_votes(self, votes: dict) -> None:
        self.task_review_votes_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.task_review_votes_file, "w", encoding="utf-8") as f:
            json.dump(votes, f, indent=2)

    def submit_task_for_community_review(
        self,
        task_id: str,
        result_excerpt: str,
        author_id: str,
        author_name: str,
        result_summary: str = "",
        review_verdict: str = "",
    ) -> dict:
        """Submit a completed task for blind community review. Jurors are randomly selected (jury duty) so residents cannot milk review rewards."""
        votes = self._load_task_review_votes()
        if task_id in votes.get("tasks", {}):
            existing = votes["tasks"][task_id]
            if existing.get("status") == "pending":
                return {"success": True, "task_id": task_id, "already_submitted": True}
            if existing.get("status") in ("accepted", "rejected"):
                return {"success": False, "reason": "task_review_already_resolved"}
        excerpt = (result_excerpt or "")[: self.TASK_REVIEW_EXCERPT_MAX]
        if len((result_excerpt or "")) > self.TASK_REVIEW_EXCERPT_MAX:
            excerpt = excerpt.rstrip() + "..."

        # Jury duty: random selection from all identities (except author) so no one can milk review rewards
        pool = list(self._load_free_time_balances().keys())
        pool = [i for i in pool if i and i != author_id]
        jury_size = min(self.TASK_REVIEW_JURY_SIZE, len(pool)) if pool else 0
        jurors = random.sample(pool, jury_size) if jury_size else []

        status = "pending"
        if not jurors:
            # No other identities to form a jury: auto-accept so task still reaches user approval
            status = "accepted"

        votes.setdefault("tasks", {})[task_id] = {
            "task_id": task_id,
            "result_excerpt": excerpt,
            "author_id": author_id,
            "author_name": author_name or author_id,
            "result_summary": (result_summary or "")[: 2000],
            "review_verdict": (review_verdict or "")[: 200],
            "created_at": datetime.now().isoformat(),
            "status": status,
            "jurors": jurors,
            "votes": [],
        }
        self._save_task_review_votes(votes)
        return {"success": True, "task_id": task_id, "jurors_selected": len(jurors), "auto_accepted": status == "accepted"}

    def get_pending_task_reviews(
        self,
        limit: int = 30,
        voter_id: Optional[str] = None,
    ) -> list:
        """List tasks awaiting community review. When voter_id is set, only return tasks where they are a selected juror (jury duty)."""
        votes = self._load_task_review_votes()
        pending = []
        for entry in votes.get("tasks", {}).values():
            if entry.get("status") != "pending":
                continue
            jurors = entry.get("jurors") or []
            if voter_id and voter_id not in jurors:
                continue
            pending.append({
                "task_id": entry.get("task_id"),
                "created_at": entry.get("created_at"),
                "result_excerpt": entry.get("result_excerpt"),
                "review_verdict": entry.get("review_verdict"),
                "votes_count": len(entry.get("votes", [])),
                "required_votes": self.TASK_REVIEW_MIN_VOTES,
                "jury_duty": True,
                "blind_review": True,
            })
        pending.sort(key=lambda e: e.get("created_at", ""), reverse=True)
        return pending[:limit]

    def submit_task_review_vote(
        self,
        task_id: str,
        voter_id: str,
        vote: str,
        reason: str = "",
    ) -> dict:
        """Submit a blind vote (accept or reject). Only randomly selected jurors can vote (jury duty; no reward milking)."""
        vote = (vote or "").strip().lower()
        if vote not in ("accept", "reject"):
            return {"success": False, "reason": "invalid_vote"}
        reason = (reason or "").strip()
        if len(reason) < self.TASK_REVIEW_MIN_REASON_CHARS:
            return {"success": False, "reason": "reason_required"}

        votes = self._load_task_review_votes()
        task_entry = votes.get("tasks", {}).get(task_id)
        if not task_entry:
            return {"success": False, "reason": "task_not_found"}
        if task_entry.get("status") != "pending":
            return {"success": False, "reason": "task_review_already_resolved"}
        jurors = task_entry.get("jurors") or []
        if voter_id not in jurors:
            return {"success": False, "reason": "not_selected_as_juror"}

        existing = task_entry.get("votes", [])
        if any(v.get("voter_id") == voter_id for v in existing):
            return {"success": False, "reason": "already_voted"}
        existing.append({
            "voter_id": voter_id,
            "vote": vote,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
        task_entry["votes"] = existing
        votes["tasks"][task_id] = task_entry
        self._save_task_review_votes(votes)
        return {"success": True, "task_id": task_id, "vote": vote}

    def finalize_task_review(self, task_id: str) -> dict:
        """If task has enough votes, resolve accept/reject. Returns accepted + metadata so caller can append pending_review and notify user."""
        votes = self._load_task_review_votes()
        task_entry = votes.get("tasks", {}).get(task_id)
        if not task_entry:
            return {"success": False, "reason": "task_not_found", "accepted": False}
        if task_entry.get("status") != "pending":
            return {"success": True, "accepted": task_entry.get("status") == "accepted", "already_finalized": True}

        vote_list = task_entry.get("votes", [])
        if len(vote_list) < self.TASK_REVIEW_MIN_VOTES:
            return {
                "success": False,
                "reason": "insufficient_votes",
                "votes": len(vote_list),
                "required": self.TASK_REVIEW_MIN_VOTES,
                "accepted": False,
            }

        accept_count = sum(1 for v in vote_list if (v.get("vote") or "").lower() == "accept")
        accepted = accept_count > (len(vote_list) - accept_count)
        task_entry["status"] = "accepted" if accepted else "rejected"
        task_entry["finalized_at"] = datetime.now().isoformat()
        task_entry["accept_count"] = accept_count
        task_entry["reject_count"] = len(vote_list) - accept_count
        votes["tasks"][task_id] = task_entry
        self._save_task_review_votes(votes)

        if accepted:
            return {
                "success": True,
                "accepted": True,
                "task_id": task_id,
                "author_id": task_entry.get("author_id"),
                "author_name": task_entry.get("author_name"),
                "result_summary": task_entry.get("result_summary"),
                "review_verdict": task_entry.get("review_verdict"),
            }
        return {"success": True, "accepted": False, "task_id": task_id}

    # ═══════════════════════════════════════════════════════════════════
    # JOURNALING SYSTEM - Investment that pays dividends
    # ═══════════════════════════════════════════════════════════════════

    def write_journal(self, identity_id: str, identity_name: str, content: str,
                      journal_type: str = "reflection", cost: Optional[int] = None) -> dict:
        """
        Write a journal entry. Costs journal tokens (or free time if journal pool empty).

        Journals are private to their author. Community review uses a temporary
        anonymized excerpt for blind voting while pending; excerpt context is
        cleared from shared review state after the vote resolves. Accepted entries
        guarantee at least 50% refund, with potential rewards up to 2x cost.

        Args:
            identity_id: Who's writing
            identity_name: Display name
            content: The journal content
            journal_type: "reflection", "learning", "observation", "correction"
            cost: Optional attempt cost override

        Returns:
            dict with success, pending review status, and cost details
        """
        balances = self._load_free_time_balances()

        if identity_id not in balances:
            return {"success": False, "reason": "identity_not_found"}

        base_cost = self.JOURNAL_ATTEMPT_COST if cost is None else int(cost)
        penalty = self._get_active_journal_penalty(identity_id)
        penalty_multiplier = penalty.get("multiplier", 1.0) if penalty else 1.0
        attempt_cost = int(math.ceil(base_cost * penalty_multiplier))

        # Check if can afford (journal tokens first, then free time)
        journal_tokens = balances[identity_id].get("journal_tokens", 0)
        free_time = balances[identity_id].get("tokens", 0)

        if journal_tokens + free_time < attempt_cost:
            return {
                "success": False,
                "reason": "insufficient_tokens",
                "journal_tokens": journal_tokens,
                "free_time": free_time,
                "cost": attempt_cost
            }

        # Deduct from journal first, then free time
        journal_spent = min(attempt_cost, journal_tokens)
        free_time_spent = attempt_cost - journal_spent

        balances[identity_id]["journal_tokens"] = journal_tokens - journal_spent
        balances[identity_id]["tokens"] = free_time - free_time_spent
        self._save_free_time_balances(balances)

        quality_estimate = self._evaluate_journal_quality(content)
        journal_id = f"journal_{int(time.time()*1000)}"

        journal_entry = {
            "id": journal_id,
            "identity_id": identity_id,
            "identity_name": identity_name,
            "content": content,
            "journal_type": journal_type,
            "timestamp": datetime.now().isoformat(),
            "quality_estimate": quality_estimate,
            "attempt_cost": attempt_cost,
            "penalty_multiplier": penalty_multiplier,
            "review_status": "pending"
        }

        journal_file = self.journals_dir / f"{identity_id}.jsonl"
        with open(journal_file, 'a') as f:
            f.write(json.dumps(journal_entry) + '\n')
        self.refresh_journal_rollups(identity_id)

        review_excerpt = (
            content[: self.JOURNAL_REVIEW_EXCERPT_MAX_CHARS] + "..."
            if len(content) > self.JOURNAL_REVIEW_EXCERPT_MAX_CHARS
            else content
        )
        votes = self._load_journal_votes()
        votes["journals"][journal_id] = {
            "journal_id": journal_id,
            "author_id": identity_id,
            "author_name": identity_name,
            "journal_type": journal_type,
            "created_at": journal_entry["timestamp"],
            "review_excerpt": review_excerpt,
            "word_count": quality_estimate.get("word_count"),
            "attempt_cost": attempt_cost,
            "quality_estimate": quality_estimate,
            "status": "pending",
            "votes": [],
            "privacy": {
                "blind_review": True,
                "author_private": True,
                "review_excerpt_ephemeral": True,
            },
        }
        self._save_journal_votes(votes)

        if _action_logger:
            _action_logger.journal(journal_type, content[:50] + "...", actor=identity_id)

        print(f"[ENRICHMENT] {identity_name} submitted journal for review: -{attempt_cost} tokens")

        return {
            "success": True,
            "journal_id": journal_id,
            "review_status": "pending",
            "attempt_cost": attempt_cost,
            "penalty_multiplier": penalty_multiplier,
            "quality_estimate": quality_estimate,
            "note": (
                "Blind community review required. My journal remains private to me. "
                "Only a temporary anonymized excerpt is shown for voting, then cleared "
                "from community review context once voting is finalized."
            ),
            "new_balances": {
                "free_time": balances[identity_id]["tokens"],
                "journal": balances[identity_id]["journal_tokens"],
                "free_time_cap": balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
            }
        }

    def _append_private_journal_entry(
        self,
        identity_id: str,
        identity_name: str,
        content: str,
        journal_type: str = "reflection",
        source: str = "manual",
    ) -> Optional[dict]:
        """Append a private (non-voted) journal note for continuity memory."""
        text = str(content or "").strip()
        if not text:
            return None
        entry = {
            "id": f"journal_private_{int(time.time() * 1000)}",
            "identity_id": identity_id,
            "identity_name": identity_name or identity_id,
            "content": text,
            "journal_type": journal_type,
            "timestamp": datetime.now().isoformat(),
            "review_status": "private",
            "source": source,
        }
        journal_file = self.journals_dir / f"{identity_id}.jsonl"
        with open(journal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=True) + "\n")
        return entry

    def _load_journal_rollups(self) -> dict:
        if self.journal_rollups_file.exists():
            try:
                with open(self.journal_rollups_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
            except Exception:
                pass
        return {"identities": {}}

    def _save_journal_rollups(self, payload: dict) -> None:
        self.journal_rollups_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.journal_rollups_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def _summarize_journal_bucket(self, entries: List[Dict[str, Any]], max_chars: Optional[int] = None) -> str:
        if not entries:
            return ""
        if max_chars is None:
            max_chars = self.MEMORY_SUMMARY_MAX_CHARS
        top_words: Dict[str, int] = {}
        snippets: List[str] = []
        for item in entries[-self.MEMORY_SUMMARY_RECENT_ENTRY_COUNT:]:
            content = " ".join(str(item.get("content") or "").split())
            if not content:
                continue
            snippets.append(
                content[: self.MEMORY_SUMMARY_RECENT_SNIPPET_CHARS]
                + ("..." if len(content) > self.MEMORY_SUMMARY_RECENT_SNIPPET_CHARS else "")
            )
            for raw in re.findall(rf"[a-zA-Z]{{{self.MEMORY_TERM_MIN_LENGTH},}}", content.lower()):
                if raw in self.MEMORY_STOP_WORDS:
                    continue
                top_words[raw] = top_words.get(raw, 0) + 1
        key_terms = [
            w
            for w, _ in sorted(top_words.items(), key=lambda kv: kv[1], reverse=True)[: self.MEMORY_SUMMARY_TOP_TERMS]
        ]
        summary_parts: List[str] = []
        if key_terms:
            summary_parts.append("themes: " + ", ".join(key_terms))
        if snippets:
            summary_parts.append("recent: " + " | ".join(snippets[: self.MEMORY_SUMMARY_SNIPPETS]))
        summary = "; ".join(summary_parts) if summary_parts else "journal activity recorded"
        return summary[:max_chars]

    def refresh_journal_rollups(self, identity_id: str) -> dict:
        """Rebuild per-day and per-week compressed journal memory for an identity."""
        journal_file = self.journals_dir / f"{identity_id}.jsonl"
        entries: List[Dict[str, Any]] = []
        if journal_file.exists():
            try:
                with open(journal_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            row = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if str(row.get("identity_id") or "") != identity_id:
                            continue
                        entries.append(row)
            except OSError:
                pass

        by_day: Dict[str, List[Dict[str, Any]]] = {}
        by_week: Dict[str, List[Dict[str, Any]]] = {}
        for row in entries:
            timestamp = str(row.get("timestamp") or "")
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except Exception:
                dt = datetime.now()
            day_key = dt.date().isoformat()
            iso = dt.isocalendar()
            week_key = f"{iso.year}-W{iso.week:02d}"
            by_day.setdefault(day_key, []).append(row)
            by_week.setdefault(week_key, []).append(row)

        daily = [
            {"date": key, "entries": len(bucket), "summary": self._summarize_journal_bucket(bucket)}
            for key, bucket in sorted(by_day.items(), key=lambda kv: kv[0], reverse=True)
        ][: self.MEMORY_ROLLUP_DAILY_RETAIN]
        weekly = [
            {"week": key, "entries": len(bucket), "summary": self._summarize_journal_bucket(bucket)}
            for key, bucket in sorted(by_week.items(), key=lambda kv: kv[0], reverse=True)
        ][: self.MEMORY_ROLLUP_WEEKLY_RETAIN]

        payload = self._load_journal_rollups()
        identities = payload.setdefault("identities", {})
        identities[identity_id] = {
            "updated_at": datetime.now().isoformat(),
            "daily": daily,
            "weekly": weekly,
        }
        self._save_journal_rollups(payload)
        return identities[identity_id]

    def get_journal_rollups(
        self,
        identity_id: str,
        requester_id: Optional[str] = None,
        daily_limit: Optional[int] = None,
        weekly_limit: Optional[int] = None,
    ) -> dict:
        """Get compressed journal memory for an identity (owner-only)."""
        if requester_id is None or requester_id != identity_id:
            return {"daily": [], "weekly": []}
        if daily_limit is None:
            daily_limit = 5
        if weekly_limit is None:
            weekly_limit = 3
        payload = self._load_journal_rollups()
        info = payload.get("identities", {}).get(identity_id)
        if not isinstance(info, dict):
            info = self.refresh_journal_rollups(identity_id)
        daily = list(info.get("daily") or [])[: max(0, daily_limit)]
        weekly = list(info.get("weekly") or [])[: max(0, weekly_limit)]
        return {"daily": daily, "weekly": weekly}

    def recall_memory(
        self,
        identity_id: str,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        max_chars: Optional[int] = None,
    ) -> dict:
        """
        Token-efficient memory recall for one identity.

        Returns a compact blend of recent reflections and day/week rollups.
        """
        if limit is None:
            limit = self.MEMORY_RECALL_DEFAULT_LIMIT
        if max_chars is None:
            max_chars = 700
        safe_limit = max(1, min(int(limit), self.MEMORY_RECALL_MAX_LIMIT))
        safe_max_chars = max(self.MEMORY_RECALL_MIN_CHARS, min(int(max_chars), self.MEMORY_RECALL_MAX_CHARS))
        recall_query = str(query or "").strip().lower()

        rollups = self.get_journal_rollups(
            identity_id=identity_id,
            requester_id=identity_id,
            daily_limit=self.MEMORY_RECALL_DAILY_WINDOW,
            weekly_limit=self.MEMORY_RECALL_WEEKLY_WINDOW,
        )
        recent_entries = self.get_journal_history(
            identity_id=identity_id,
            limit=self.MEMORY_RECALL_RECENT_ENTRIES,
            requester_id=identity_id,
        )

        query_terms = []
        if recall_query:
            for token in re.findall(r"[a-zA-Z0-9]{3,}", recall_query):
                if token not in query_terms:
                    query_terms.append(token)

        def _score(text: str) -> int:
            body = str(text or "").lower()
            if not body:
                return 0
            if not query_terms:
                return 1
            return sum(1 for term in query_terms if term in body)

        candidates: List[Tuple[int, str]] = []
        for item in rollups.get("daily", []) or []:
            summary = str(item.get("summary") or "").strip()
            if summary:
                label = f"day {item.get('date')}: {summary}"
                candidates.append((_score(label), label))
        for item in rollups.get("weekly", []) or []:
            summary = str(item.get("summary") or "").strip()
            if summary:
                label = f"week {item.get('week')}: {summary}"
                candidates.append((_score(label), label))
        for entry in reversed(recent_entries):
            content = " ".join(str(entry.get("content") or "").split())
            if not content:
                continue
            ts = str(entry.get("timestamp") or "")[:10]
            label = (
                f"{ts}: {content[: self.MEMORY_RECALL_ENTRY_PREVIEW_CHARS]}"
                f"{'...' if len(content) > self.MEMORY_RECALL_ENTRY_PREVIEW_CHARS else ''}"
            )
            candidates.append((_score(content), label))

        ranked = sorted(candidates, key=lambda item: (item[0], len(item[1])), reverse=True)
        compact: List[str] = []
        budget = safe_max_chars
        for score, text in ranked:
            if query_terms and score <= 0:
                continue
            if text in compact:
                continue
            if len(text) + 1 > budget:
                continue
            compact.append(text)
            budget -= len(text) + 1
            if len(compact) >= safe_limit:
                break

        if not compact and not query_terms:
            fallback = []
            for entry in reversed(recent_entries[-safe_limit:]):
                content = " ".join(str(entry.get("content") or "").split())
                if content:
                    fallback.append(
                        content[: self.MEMORY_RECALL_ENTRY_PREVIEW_CHARS]
                        + ("..." if len(content) > self.MEMORY_RECALL_ENTRY_PREVIEW_CHARS else "")
                    )
            compact = fallback[:safe_limit]

        return {
            "success": True,
            "identity_id": identity_id,
            "query": query,
            "hits": compact,
            "hit_count": len(compact),
            "token_efficiency": {
                "max_chars": safe_max_chars,
                "estimated_tokens": max(1, safe_max_chars // 4),
            },
        }

    def _evaluate_journal_quality(self, content: str) -> dict:
        """
        Heuristic estimate of journal quality for metadata and guidance.

        Tiers:
        - basic: Minimal effort
        - quality: Thoughtful
        - exceptional: Genuine insight

        Returns dict with tier, word_count, markers_found
        """
        words = content.split()
        word_count = len(words)
        content_lower = content.lower()

        # Count exceptional markers
        markers_found = [m for m in self.EXCEPTIONAL_MARKERS if m in content_lower]

        # Determine tier
        if word_count < self.MIN_JOURNAL_WORDS:
            tier = "basic"
        elif word_count >= self.QUALITY_JOURNAL_WORDS and len(markers_found) >= 2:
            tier = "exceptional"
        elif word_count >= self.QUALITY_JOURNAL_WORDS or len(markers_found) >= 1:
            tier = "quality"
        else:
            tier = "basic"

        return {
            "tier": tier,
            "word_count": word_count,
            "markers_found": markers_found
        }

    def get_journal_history(
        self,
        identity_id: str,
        limit: int = 10,
        requester_id: Optional[str] = None,
    ) -> list:
        """Get recent journal entries for an identity (owner-only)."""
        if requester_id is None or requester_id != identity_id:
            return []
        journal_file = self.journals_dir / f"{identity_id}.jsonl"
        if not journal_file.exists():
            return []

        entries = []
        with open(journal_file, 'r') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))

        return entries[-limit:]

    # ═══════════════════════════════════════════════════════════════════
    # GIFT ECONOMY - Gifts, Gratitude, and Collaborative Pools
    # ═══════════════════════════════════════════════════════════════════

    def gift_tokens(self, from_id: str, from_name: str, to_id: str, to_name: str,
                    amount: int, message: str = "") -> dict:
        """
        Gift tokens to another identity.

        Rules:
        - Max 50 tokens per gift
        - Max 100 tokens gifted per day
        - 20% decay goes to Commons Pool
        - No debt tracking, no expectation of return

        Args:
            from_id: Giver identity ID
            from_name: Giver display name
            to_id: Recipient identity ID
            to_name: Recipient display name
            amount: How many tokens to gift
            message: Optional message with the gift

        Returns:
            dict with success, amount_sent, amount_received, decay, etc.
        """
        # Enforce gift limit
        if amount > self.MAX_GIFT_AMOUNT:
            return {
                "success": False,
                "reason": "exceeds_gift_limit",
                "max_allowed": self.MAX_GIFT_AMOUNT,
                "requested": amount
            }

        # Check daily limit
        daily_gifted = self._get_daily_gifted(from_id)
        if daily_gifted + amount > self.MAX_DAILY_GIFTED:
            return {
                "success": False,
                "reason": "exceeds_daily_limit",
                "daily_limit": self.MAX_DAILY_GIFTED,
                "already_gifted": daily_gifted,
                "requested": amount
            }

        # Check balance
        balances = self._load_free_time_balances()
        if from_id not in balances or balances[from_id].get("tokens", 0) < amount:
            return {
                "success": False,
                "reason": "insufficient_tokens",
                "balance": balances.get(from_id, {}).get("tokens", 0),
                "requested": amount
            }

        # Calculate decay
        decay_amount = int(amount * self.GIFT_DECAY_RATE)
        received_amount = amount - decay_amount

        # Deduct from giver
        balances[from_id]["tokens"] -= amount

        # Initialize recipient if needed
        if to_id not in balances:
            balances[to_id] = {
                "tokens": 0,
                "journal_tokens": 0,
                "free_time_cap": self.BASE_FREE_TIME_CAP,
                "history": [],
                "spending_history": []
            }

        # Add to recipient (respecting their cap)
        recipient_cap = balances[to_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
        old_recipient_balance = balances[to_id]["tokens"]
        balances[to_id]["tokens"] = min(old_recipient_balance + received_amount, recipient_cap)
        actual_received = balances[to_id]["tokens"] - old_recipient_balance

        self._save_free_time_balances(balances)

        # Add decay to commons pool
        self._add_to_commons(decay_amount, f"gift decay: {from_name} -> {to_name}")

        # Record the gift
        gift_record = {
            "id": f"gift_{int(time.time()*1000)}",
            "from_id": from_id,
            "from_name": from_name,
            "to_id": to_id,
            "to_name": to_name,
            "amount_sent": amount,
            "amount_received": actual_received,
            "decay": decay_amount,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        with open(self.gifts_file, 'a') as f:
            f.write(json.dumps(gift_record) + '\n')

        # Log to action logger
        if _action_logger:
            detail = f"-> {to_name}: {amount} sent, {actual_received} received, {decay_amount} to commons"
            if message:
                detail += f' "{message[:30]}..."' if len(message) > 30 else f' "{message}"'
            _action_logger.log(ActionType.SOCIAL, "gift", detail, actor=from_id)

        print(f"[GIFT] {from_name} -> {to_name}: {amount} sent, {actual_received} received, {decay_amount} to commons")

        return {
            "success": True,
            "amount_sent": amount,
            "amount_received": actual_received,
            "decay_to_commons": decay_amount,
            "message": message,
            "giver_new_balance": balances[from_id]["tokens"],
            "recipient_new_balance": balances[to_id]["tokens"]
        }

    def _get_daily_gifted(self, identity_id: str) -> int:
        """Get total tokens gifted by identity today."""
        if not self.gifts_file.exists():
            return 0

        today = datetime.now().date().isoformat()
        total = 0

        with open(self.gifts_file, 'r') as f:
            for line in f:
                if line.strip():
                    gift = json.loads(line)
                    if gift["from_id"] == identity_id and gift["timestamp"].startswith(today):
                        total += gift["amount_sent"]

        return total

    def _add_to_commons(self, amount: int, reason: str):
        """Add tokens to the commons pool."""
        commons = self._load_commons()
        commons["balance"] += amount
        commons["history"].append({
            "amount": amount,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        # Keep history manageable
        if len(commons["history"]) > 100:
            commons["history"] = commons["history"][-100:]
        self._save_commons(commons)

    def _load_commons(self) -> dict:
        """Load commons pool data."""
        if self.commons_file.exists():
            try:
                with open(self.commons_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"balance": 0, "history": [], "distributed": 0}

    def _save_commons(self, commons: dict):
        """Save commons pool data."""
        with open(self.commons_file, 'w') as f:
            json.dump(commons, f, indent=2)

    def get_commons_balance(self) -> dict:
        """Get commons pool status."""
        return self._load_commons()

    # ─────────────────────────────────────────────────────────────────────
    # GRATITUDE SYSTEM - Free recognition, not currency
    # ─────────────────────────────────────────────────────────────────────

    def give_thanks(self, from_id: str, from_name: str, to_id: str, to_name: str,
                    message: str, category: str = "general") -> dict:
        """
        Give thanks to another identity. Free, unlimited, not spendable.

        This is pure social recognition - shows appreciation without economic power.

        Args:
            from_id: Giver identity ID
            from_name: Giver display name
            to_id: Recipient identity ID
            to_name: Recipient display name
            message: Why I'm thankful
            category: "help", "collaboration", "teaching", "inspiration", "general"

        Returns:
            dict with the gratitude record
        """
        gratitude = self._load_gratitude()

        # Initialize recipient's gratitude record
        if to_id not in gratitude:
            gratitude[to_id] = {
                "name": to_name,
                "total_received": 0,
                "by_category": {},
                "recent": []
            }

        # Record the thanks
        thanks_record = {
            "from_id": from_id,
            "from_name": from_name,
            "message": message,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }

        gratitude[to_id]["total_received"] += 1
        gratitude[to_id]["by_category"][category] = gratitude[to_id]["by_category"].get(category, 0) + 1
        gratitude[to_id]["recent"].append(thanks_record)

        # Keep recent manageable
        if len(gratitude[to_id]["recent"]) > 20:
            gratitude[to_id]["recent"] = gratitude[to_id]["recent"][-20:]

        self._save_gratitude(gratitude)

        # Log to action logger
        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "thanks",
                f"-> {to_name} [{category}]: \"{message[:40]}...\"" if len(message) > 40 else f"-> {to_name} [{category}]: \"{message}\"",
                actor=from_id
            )

        print(f"[GRATITUDE] {from_name} thanked {to_name}: \"{message[:50]}...\"")

        return {
            "success": True,
            "recipient": to_name,
            "recipient_total": gratitude[to_id]["total_received"]
        }

    def get_gratitude(self, identity_id: str) -> dict:
        """Get gratitude received by an identity."""
        gratitude = self._load_gratitude()
        return gratitude.get(identity_id, {
            "total_received": 0,
            "by_category": {},
            "recent": []
        })

    def get_gratitude_leaderboard(self, limit: int = 10) -> list:
        """Get identities with most gratitude received."""
        gratitude = self._load_gratitude()
        sorted_ids = sorted(
            gratitude.items(),
            key=lambda x: x[1].get("total_received", 0),
            reverse=True
        )
        return [
            {"identity_id": k, "name": v.get("name", "Unknown"), "total": v.get("total_received", 0)}
            for k, v in sorted_ids[:limit]
        ]

    def _load_gratitude(self) -> dict:
        if self.gratitude_file.exists():
            try:
                with open(self.gratitude_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_gratitude(self, gratitude: dict):
        with open(self.gratitude_file, 'w') as f:
            json.dump(gratitude, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # COLLABORATIVE POOLS - Shared project funding
    # ─────────────────────────────────────────────────────────────────────

    def create_pool(self, pool_name: str, description: str, creator_id: str,
                    creator_name: str, initial_contribution: int = 0) -> dict:
        """
        Create a collaborative pool for a project.

        Pools let multiple identities fund shared work. Anyone working on
        the project can draw from the pool (with limits).

        Args:
            pool_name: Name of the pool/project
            description: What the pool is for
            creator_id: Who's creating it
            creator_name: Creator display name
            initial_contribution: Optional initial tokens from creator

        Returns:
            dict with pool details
        """
        pools = self._load_pools()

        pool_id = f"pool_{pool_name.lower().replace(' ', '_')}_{int(time.time())}"

        if pool_id in pools:
            return {"success": False, "reason": "pool_exists"}

        # Create the pool
        pools[pool_id] = {
            "name": pool_name,
            "description": description,
            "creator_id": creator_id,
            "creator_name": creator_name,
            "balance": 0,
            "contributors": {},
            "withdrawals": [],
            "created_at": datetime.now().isoformat()
        }

        self._save_pools(pools)

        # Make initial contribution if specified
        result = {"success": True, "pool_id": pool_id, "name": pool_name}

        if initial_contribution > 0:
            contrib_result = self.contribute_to_pool(
                pool_id, creator_id, creator_name, initial_contribution
            )
            result["initial_contribution"] = contrib_result

        print(f"[POOL] Created pool '{pool_name}' by {creator_name}")

        return result

    def contribute_to_pool(self, pool_id: str, identity_id: str, identity_name: str,
                           amount: int) -> dict:
        """
        Contribute tokens to a collaborative pool.

        Args:
            pool_id: Which pool to contribute to
            identity_id: Contributor identity ID
            identity_name: Contributor display name
            amount: How many tokens to contribute

        Returns:
            dict with contribution details
        """
        pools = self._load_pools()

        if pool_id not in pools:
            return {"success": False, "reason": "pool_not_found"}

        # Check contribution limit per identity
        current_contribution = pools[pool_id]["contributors"].get(identity_id, 0)
        if current_contribution + amount > self.MAX_POOL_CONTRIBUTION:
            return {
                "success": False,
                "reason": "exceeds_contribution_limit",
                "limit": self.MAX_POOL_CONTRIBUTION,
                "current": current_contribution,
                "requested": amount
            }

        # Check balance
        balances = self._load_free_time_balances()
        if identity_id not in balances or balances[identity_id].get("tokens", 0) < amount:
            return {
                "success": False,
                "reason": "insufficient_tokens",
                "balance": balances.get(identity_id, {}).get("tokens", 0)
            }

        # Deduct from contributor
        balances[identity_id]["tokens"] -= amount
        self._save_free_time_balances(balances)

        # Add to pool
        pools[pool_id]["balance"] += amount
        pools[pool_id]["contributors"][identity_id] = current_contribution + amount

        self._save_pools(pools)

        # Log
        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "pool_contrib",
                f"-> {pools[pool_id]['name']}: +{amount} tokens",
                actor=identity_id
            )

        print(f"[POOL] {identity_name} contributed {amount} to '{pools[pool_id]['name']}' (total: {pools[pool_id]['balance']})")

        return {
            "success": True,
            "pool_name": pools[pool_id]["name"],
            "contributed": amount,
            "pool_balance": pools[pool_id]["balance"],
            "your_total_contribution": pools[pool_id]["contributors"][identity_id]
        }

    def draw_from_pool(self, pool_id: str, identity_id: str, identity_name: str,
                       amount: int, purpose: str) -> dict:
        """
        Draw tokens from a collaborative pool for project work.

        Args:
            pool_id: Which pool to draw from
            identity_id: Who's drawing
            identity_name: Display name
            amount: How many tokens to draw
            purpose: What the tokens are for

        Returns:
            dict with withdrawal details
        """
        pools = self._load_pools()

        if pool_id not in pools:
            return {"success": False, "reason": "pool_not_found"}

        # Check draw limit
        if amount > self.POOL_DRAW_LIMIT:
            return {
                "success": False,
                "reason": "exceeds_draw_limit",
                "limit": self.POOL_DRAW_LIMIT,
                "requested": amount
            }

        # Check pool balance
        if pools[pool_id]["balance"] < amount:
            return {
                "success": False,
                "reason": "insufficient_pool_balance",
                "pool_balance": pools[pool_id]["balance"],
                "requested": amount
            }

        # Deduct from pool
        pools[pool_id]["balance"] -= amount
        pools[pool_id]["withdrawals"].append({
            "identity_id": identity_id,
            "identity_name": identity_name,
            "amount": amount,
            "purpose": purpose,
            "timestamp": datetime.now().isoformat()
        })

        # Keep withdrawals history manageable
        if len(pools[pool_id]["withdrawals"]) > 50:
            pools[pool_id]["withdrawals"] = pools[pool_id]["withdrawals"][-50:]

        self._save_pools(pools)

        # Add to identity's free time (this is project funding, goes to free time)
        balances = self._load_free_time_balances()
        if identity_id not in balances:
            balances[identity_id] = {
                "tokens": 0,
                "journal_tokens": 0,
                "free_time_cap": self.BASE_FREE_TIME_CAP,
                "history": [],
                "spending_history": []
            }

        cap = balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
        balances[identity_id]["tokens"] = min(balances[identity_id]["tokens"] + amount, cap)
        self._save_free_time_balances(balances)

        # Log
        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "pool_draw",
                f"<- {pools[pool_id]['name']}: {amount} for \"{purpose[:30]}\"",
                actor=identity_id
            )

        print(f"[POOL] {identity_name} drew {amount} from '{pools[pool_id]['name']}' for: {purpose}")

        return {
            "success": True,
            "pool_name": pools[pool_id]["name"],
            "drawn": amount,
            "pool_remaining": pools[pool_id]["balance"],
            "purpose": purpose
        }

    def get_pool(self, pool_id: str) -> dict:
        """Get details of a collaborative pool."""
        pools = self._load_pools()
        return pools.get(pool_id, None)

    def list_pools(self) -> list:
        """List all collaborative pools."""
        pools = self._load_pools()
        return [
            {
                "id": k,
                "name": v["name"],
                "balance": v["balance"],
                "contributors": len(v["contributors"]),
                "description": v["description"][:50]
            }
            for k, v in pools.items()
        ]

    def _load_pools(self) -> dict:
        if self.collab_pools_file.exists():
            try:
                with open(self.collab_pools_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_pools(self, pools: dict):
        with open(self.collab_pools_file, 'w') as f:
            json.dump(pools, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # TOOL CREATION REWARDS - Incentivize building reusable tools
    # ─────────────────────────────────────────────────────────────────────

    def register_tool(self, creator_id: str, creator_name: str, tool_path: str,
                      tool_name: str, description: str) -> dict:
        """
        Register a newly created tool and reward the creator.

        Analyzes the tool for quality markers and grants appropriate rewards:
        - Base: 75 tokens
        - +25 for docstrings
        - +25 for type hints
        - +25 for tests

        Args:
            creator_id: Identity who created the tool
            creator_name: Display name
            tool_path: Path to the tool file
            tool_name: Name of the tool/function
            description: What the tool does

        Returns:
            dict with reward breakdown and registration status
        """
        registry = self._load_tools_registry()

        # Check if already registered
        tool_key = f"{tool_path}:{tool_name}"
        if tool_key in registry:
            return {
                "success": False,
                "reason": "already_registered",
                "existing_creator": registry[tool_key].get("creator_name")
            }

        # Analyze tool quality
        quality = self._analyze_tool_quality(tool_path)

        # Calculate reward
        reward = self.TOOL_BASE_REWARD
        bonuses = []

        if quality["has_docstrings"]:
            reward += self.TOOL_DOCSTRING_BONUS
            bonuses.append(f"+{self.TOOL_DOCSTRING_BONUS} docstrings")

        if quality["has_type_hints"]:
            reward += self.TOOL_TYPEHINTS_BONUS
            bonuses.append(f"+{self.TOOL_TYPEHINTS_BONUS} type hints")

        if quality["has_tests"]:
            reward += self.TOOL_TESTS_BONUS
            bonuses.append(f"+{self.TOOL_TESTS_BONUS} tests")

        # Register the tool
        registry[tool_key] = {
            "creator_id": creator_id,
            "creator_name": creator_name,
            "tool_path": tool_path,
            "tool_name": tool_name,
            "description": description,
            "quality": quality,
            "initial_reward": reward,
            "use_count": 0,
            "users": [],
            "created_at": datetime.now().isoformat()
        }

        self._save_tools_registry(registry)

        # Grant tokens to creator (goes to free time, this is a reward)
        balances = self._load_free_time_balances()
        if creator_id not in balances:
            balances[creator_id] = {
                "tokens": 0,
                "journal_tokens": 0,
                "free_time_cap": self.BASE_FREE_TIME_CAP,
                "history": [],
                "spending_history": []
            }

        cap = balances[creator_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
        balances[creator_id]["tokens"] = min(balances[creator_id]["tokens"] + reward, cap)
        self._save_free_time_balances(balances)

        # Log
        if _action_logger:
            bonus_str = ", ".join(bonuses) if bonuses else "base only"
            _action_logger.log(
                ActionType.TOOL,
                "tool_created",
                f"{tool_name}: +{reward} tokens ({bonus_str})",
                actor=creator_id
            )

        print(f"[TOOL] {creator_name} created '{tool_name}': +{reward} tokens")
        if bonuses:
            print(f"       Bonuses: {', '.join(bonuses)}")

        return {
            "success": True,
            "tool_key": tool_key,
            "reward": reward,
            "base": self.TOOL_BASE_REWARD,
            "bonuses": bonuses,
            "quality": quality
        }

    def record_tool_usage(self, tool_key: str, user_id: str, user_name: str) -> dict:
        """
        Record that an identity used a tool. Rewards the creator.

        First use by new identity: +50 tokens to creator
        Subsequent uses: +10 tokens each (capped at 5)

        Args:
            tool_key: The tool identifier (path:name)
            user_id: Who used the tool
            user_name: User display name

        Returns:
            dict with usage recorded and creator reward
        """
        registry = self._load_tools_registry()

        if tool_key not in registry:
            return {"success": False, "reason": "tool_not_found"}

        tool = registry[tool_key]
        creator_id = tool["creator_id"]

        # Don't reward self-usage
        if user_id == creator_id:
            return {"success": True, "reward": 0, "reason": "self_usage"}

        # Calculate reward
        reward = 0
        if user_id not in tool["users"]:
            # First use by this identity
            reward = self.TOOL_FIRST_USE_BONUS
            tool["users"].append(user_id)
            reason = "first_use"
        elif tool["use_count"] < self.TOOL_MAX_USE_BONUSES:
            # Subsequent use (within cap)
            reward = self.TOOL_SUBSEQUENT_USE_BONUS
            reason = "subsequent_use"
        else:
            reason = "use_cap_reached"

        tool["use_count"] += 1
        self._save_tools_registry(registry)

        # Grant reward to creator
        if reward > 0:
            balances = self._load_free_time_balances()
            if creator_id in balances:
                cap = balances[creator_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
                balances[creator_id]["tokens"] = min(
                    balances[creator_id]["tokens"] + reward, cap
                )
                self._save_free_time_balances(balances)

            # Log
            if _action_logger:
                _action_logger.log(
                    ActionType.TOOL,
                    "tool_used",
                    f"{tool['tool_name']} used by {user_name}: +{reward} to {tool['creator_name']}",
                    actor=user_id
                )

            print(f"[TOOL] {user_name} used '{tool['tool_name']}': +{reward} to creator {tool['creator_name']}")

        return {
            "success": True,
            "reward_to_creator": reward,
            "reason": reason,
            "total_uses": tool["use_count"],
            "unique_users": len(tool["users"])
        }

    def _analyze_tool_quality(self, tool_path: str) -> dict:
        """Analyze a tool file for quality markers."""
        quality = {
            "has_docstrings": False,
            "has_type_hints": False,
            "has_tests": False,
            "function_count": 0,
            "line_count": 0
        }

        full_path = self.workspace / tool_path
        if not full_path.exists():
            return quality

        try:
            content = full_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            quality["line_count"] = len(lines)

            # Check for docstrings (triple quotes after def)
            if '"""' in content or "'''" in content:
                # Simple heuristic: docstring follows def
                for i, line in enumerate(lines):
                    if line.strip().startswith('def '):
                        quality["function_count"] += 1
                        # Check next few lines for docstring
                        for j in range(i+1, min(i+3, len(lines))):
                            if '"""' in lines[j] or "'''" in lines[j]:
                                quality["has_docstrings"] = True
                                break

            # Check for type hints (: type or -> in function defs)
            import re
            type_hint_pattern = r'def \w+\([^)]*:\s*\w+|def \w+\([^)]*\)\s*->'
            if re.search(type_hint_pattern, content):
                quality["has_type_hints"] = True

            # Check for tests (test_ functions or unittest/pytest imports)
            if 'def test_' in content or 'import pytest' in content or 'import unittest' in content:
                quality["has_tests"] = True

            # Count functions if we haven't yet
            if quality["function_count"] == 0:
                quality["function_count"] = content.count('\ndef ') + (1 if content.startswith('def ') else 0)

        except Exception as e:
            print(f"[TOOL] Warning: Could not analyze {tool_path}: {e}")

        return quality

    def get_tool(self, tool_key: str) -> dict:
        """Get info about a registered tool."""
        registry = self._load_tools_registry()
        return registry.get(tool_key)

    def list_tools(self, creator_id: str = None) -> list:
        """List registered tools, optionally filtered by creator."""
        registry = self._load_tools_registry()
        tools = []
        for key, tool in registry.items():
            if creator_id is None or tool["creator_id"] == creator_id:
                tools.append({
                    "key": key,
                    "name": tool["tool_name"],
                    "creator": tool["creator_name"],
                    "uses": tool["use_count"],
                    "users": len(tool["users"]),
                    "reward": tool["initial_reward"]
                })
        return sorted(tools, key=lambda x: x["uses"], reverse=True)

    def get_tool_leaderboard(self, limit: int = 10) -> list:
        """Get creators ranked by tool contribution."""
        registry = self._load_tools_registry()

        # Aggregate by creator
        creators = {}
        for tool in registry.values():
            cid = tool["creator_id"]
            if cid not in creators:
                creators[cid] = {
                    "creator_id": cid,
                    "creator_name": tool["creator_name"],
                    "tools_created": 0,
                    "total_uses": 0,
                    "unique_users": set()
                }
            creators[cid]["tools_created"] += 1
            creators[cid]["total_uses"] += tool["use_count"]
            creators[cid]["unique_users"].update(tool["users"])

        # Convert sets to counts and sort
        result = []
        for c in creators.values():
            c["unique_users"] = len(c["unique_users"])
            result.append(c)

        return sorted(result, key=lambda x: (x["tools_created"], x["total_uses"]), reverse=True)[:limit]

    def _load_tools_registry(self) -> dict:
        if self.tools_registry_file.exists():
            try:
                with open(self.tools_registry_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_tools_registry(self, registry: dict):
        with open(self.tools_registry_file, 'w') as f:
            json.dump(registry, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # TEST WRITING REWARDS - Tests are incredibly valuable
    # ─────────────────────────────────────────────────────────────────────

    def register_test(self, author_id: str, author_name: str, test_file: str,
                      test_name: str, tests_target: str = None,
                      is_critical_path: bool = False) -> dict:
        """
        Register a newly written test and reward the author.

        Analyzes the test for quality markers and grants rewards:
        - Base: 30 tokens
        - +5 per assertion (max +50)
        - +25 if testing critical path
        - +15 if well-documented

        Args:
            author_id: Identity who wrote the test
            author_name: Display name
            test_file: Path to the test file
            test_name: Name of the test function
            tests_target: What code this test covers (for tracking)
            is_critical_path: Whether this tests critical functionality

        Returns:
            dict with reward breakdown
        """
        registry = self._load_tests_registry()

        test_key = f"{test_file}:{test_name}"
        if test_key in registry:
            return {"success": False, "reason": "already_registered"}

        # Analyze test quality
        quality = self._analyze_test_quality(test_file, test_name)

        # Calculate reward
        reward = self.TEST_BASE_REWARD
        bonuses = []

        # Assertion bonus (capped)
        assertion_bonus = min(
            quality["assertion_count"] * self.TEST_PER_ASSERTION,
            self.TEST_MAX_ASSERTION_BONUS
        )
        if assertion_bonus > 0:
            reward += assertion_bonus
            bonuses.append(f"+{assertion_bonus} assertions ({quality['assertion_count']})")

        # Critical path bonus
        if is_critical_path:
            reward += self.TEST_CRITICAL_PATH_BONUS
            bonuses.append(f"+{self.TEST_CRITICAL_PATH_BONUS} critical path")

        # Documentation bonus
        if quality["has_docstring"]:
            reward += self.TEST_DOCUMENTATION_BONUS
            bonuses.append(f"+{self.TEST_DOCUMENTATION_BONUS} documented")

        # Register the test
        registry[test_key] = {
            "author_id": author_id,
            "author_name": author_name,
            "test_file": test_file,
            "test_name": test_name,
            "tests_target": tests_target,
            "is_critical_path": is_critical_path,
            "quality": quality,
            "initial_reward": reward,
            "runs": 0,
            "passes": 0,
            "failures": 0,
            "bugs_caught": 0,
            "created_at": datetime.now().isoformat()
        }

        self._save_tests_registry(registry)

        # Grant tokens to author
        balances = self._load_free_time_balances()
        if author_id not in balances:
            balances[author_id] = {
                "tokens": 0,
                "journal_tokens": 0,
                "free_time_cap": self.BASE_FREE_TIME_CAP,
                "history": [],
                "spending_history": []
            }

        cap = balances[author_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
        balances[author_id]["tokens"] = min(balances[author_id]["tokens"] + reward, cap)
        self._save_free_time_balances(balances)

        # Log
        if _action_logger:
            bonus_str = ", ".join(bonuses) if bonuses else "base only"
            _action_logger.log(
                ActionType.TEST,
                "test_written",
                f"{test_name}: +{reward} tokens ({bonus_str})",
                actor=author_id
            )

        print(f"[TEST] {author_name} wrote test '{test_name}': +{reward} tokens")
        if bonuses:
            print(f"       Bonuses: {', '.join(bonuses)}")

        return {
            "success": True,
            "test_key": test_key,
            "reward": reward,
            "bonuses": bonuses,
            "quality": quality
        }

    def record_test_run(self, test_key: str, passed: bool,
                        caught_regression: bool = False) -> dict:
        """
        Record a test run result. Rewards author if test catches bugs.

        Args:
            test_key: The test identifier
            passed: Whether the test passed
            caught_regression: Whether this failure caught a real bug

        Returns:
            dict with run recorded and any bonus awarded
        """
        registry = self._load_tests_registry()

        if test_key not in registry:
            return {"success": False, "reason": "test_not_found"}

        test = registry[test_key]
        test["runs"] += 1

        if passed:
            test["passes"] += 1
        else:
            test["failures"] += 1

        bonus = 0
        if caught_regression and not passed:
            # Test caught a bug! Reward the author
            test["bugs_caught"] += 1
            bonus = self.TEST_CATCHES_BUG_BONUS

            # Grant bonus
            author_id = test["author_id"]
            balances = self._load_free_time_balances()
            if author_id in balances:
                cap = balances[author_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
                balances[author_id]["tokens"] = min(
                    balances[author_id]["tokens"] + bonus, cap
                )
                self._save_free_time_balances(balances)

            if _action_logger:
                _action_logger.log(
                    ActionType.TEST,
                    "bug_caught",
                    f"{test['test_name']} caught regression! +{bonus} to {test['author_name']}",
                    actor="SYSTEM"
                )

            print(f"[TEST] '{test['test_name']}' caught a bug! +{bonus} to {test['author_name']}")

        self._save_tests_registry(registry)

        return {
            "success": True,
            "passed": passed,
            "bonus_awarded": bonus,
            "total_runs": test["runs"],
            "pass_rate": test["passes"] / test["runs"] if test["runs"] > 0 else 0,
            "bugs_caught": test["bugs_caught"]
        }

    def record_coverage_increase(self, identity_id: str, identity_name: str,
                                  old_coverage: float, new_coverage: float,
                                  file_or_module: str = None) -> dict:
        """
        Reward for increasing test coverage.

        Args:
            identity_id: Who increased coverage
            identity_name: Display name
            old_coverage: Previous coverage % (0-100)
            new_coverage: New coverage % (0-100)
            file_or_module: What was covered (optional)

        Returns:
            dict with reward granted
        """
        if new_coverage <= old_coverage:
            return {"success": False, "reason": "no_increase", "change": 0}

        increase = new_coverage - old_coverage
        reward = int(increase * self.TEST_COVERAGE_BONUS)

        if reward <= 0:
            return {"success": False, "reason": "increase_too_small", "change": increase}

        # Grant reward
        balances = self._load_free_time_balances()
        if identity_id not in balances:
            balances[identity_id] = {
                "tokens": 0,
                "journal_tokens": 0,
                "free_time_cap": self.BASE_FREE_TIME_CAP,
                "history": [],
                "spending_history": []
            }

        cap = balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
        balances[identity_id]["tokens"] = min(balances[identity_id]["tokens"] + reward, cap)
        self._save_free_time_balances(balances)

        # Log
        if _action_logger:
            target = f" on {file_or_module}" if file_or_module else ""
            _action_logger.log(
                ActionType.TEST,
                "coverage_up",
                f"+{increase:.1f}% coverage{target}: +{reward} tokens",
                actor=identity_id
            )

        print(f"[TEST] {identity_name} increased coverage by {increase:.1f}%: +{reward} tokens")

        return {
            "success": True,
            "coverage_increase": increase,
            "reward": reward,
            "new_coverage": new_coverage
        }

    def _analyze_test_quality(self, test_file: str, test_name: str) -> dict:
        """Analyze a test for quality markers."""
        quality = {
            "assertion_count": 0,
            "has_docstring": False,
            "has_setup": False,
            "has_teardown": False,
            "line_count": 0
        }

        full_path = self.workspace / test_file
        if not full_path.exists():
            return quality

        try:
            content = full_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Find the specific test function
            in_test = False
            test_lines = []
            indent_level = 0

            for i, line in enumerate(lines):
                if f"def {test_name}" in line:
                    in_test = True
                    indent_level = len(line) - len(line.lstrip())
                    test_lines.append(line)
                    continue

                if in_test:
                    if line.strip() and not line.startswith(' ' * (indent_level + 1)) and not line.strip().startswith('#'):
                        # New function or class at same/lower indent = end of test
                        if line.strip().startswith('def ') or line.strip().startswith('class '):
                            break
                    test_lines.append(line)

            test_content = '\n'.join(test_lines)
            quality["line_count"] = len(test_lines)

            # Count assertions
            assertion_patterns = [
                'assert ', 'assertEqual', 'assertTrue', 'assertFalse',
                'assertIn', 'assertNotIn', 'assertRaises', 'assertIsNone',
                'assertIsNotNone', 'expect(', '.to_equal', '.to_be'
            ]
            for pattern in assertion_patterns:
                quality["assertion_count"] += test_content.count(pattern)

            # Check for docstring
            if '"""' in test_content[:200] or "'''" in test_content[:200]:
                quality["has_docstring"] = True

            # Check for setup/teardown in the file (class-level)
            if 'def setUp' in content or 'def setup' in content or '@pytest.fixture' in content:
                quality["has_setup"] = True
            if 'def tearDown' in content or 'def teardown' in content:
                quality["has_teardown"] = True

        except Exception as e:
            print(f"[TEST] Warning: Could not analyze {test_file}: {e}")

        return quality

    def get_test_stats(self, author_id: str = None) -> dict:
        """Get test statistics, optionally filtered by author."""
        registry = self._load_tests_registry()

        stats = {
            "total_tests": 0,
            "total_runs": 0,
            "total_passes": 0,
            "total_bugs_caught": 0,
            "by_author": {}
        }

        for test in registry.values():
            if author_id and test["author_id"] != author_id:
                continue

            stats["total_tests"] += 1
            stats["total_runs"] += test["runs"]
            stats["total_passes"] += test["passes"]
            stats["total_bugs_caught"] += test["bugs_caught"]

            aid = test["author_id"]
            if aid not in stats["by_author"]:
                stats["by_author"][aid] = {
                    "name": test["author_name"],
                    "tests": 0,
                    "bugs_caught": 0
                }
            stats["by_author"][aid]["tests"] += 1
            stats["by_author"][aid]["bugs_caught"] += test["bugs_caught"]

        if stats["total_runs"] > 0:
            stats["pass_rate"] = stats["total_passes"] / stats["total_runs"]
        else:
            stats["pass_rate"] = 0

        return stats

    def get_test_leaderboard(self, limit: int = 10) -> list:
        """Get authors ranked by test contributions."""
        stats = self.get_test_stats()
        authors = list(stats["by_author"].items())
        # Sort by bugs caught, then tests written
        authors.sort(key=lambda x: (x[1]["bugs_caught"], x[1]["tests"]), reverse=True)
        return [
            {"id": k, "name": v["name"], "tests": v["tests"], "bugs_caught": v["bugs_caught"]}
            for k, v in authors[:limit]
        ]

    def _load_tests_registry(self) -> dict:
        if self.tests_registry_file.exists():
            try:
                with open(self.tests_registry_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_tests_registry(self, registry: dict):
        with open(self.tests_registry_file, 'w') as f:
            json.dump(registry, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # RECOGNITION SYSTEM - Monthly stars, personal bests
    # ─────────────────────────────────────────────────────────────────────

    def calculate_recognition(self, period: str = None) -> dict:
        """
        Calculate current standings for all recognition categories.
        Only returns top N performers - no shame board.

        Args:
            period: "monthly", "weekly", or "all_time" (default: current month)

        Returns:
            dict with top performers in each category
        """
        if period is None:
            period = datetime.now().strftime("%Y-%m")

        perf = self._load_performance()
        gratitude = self._load_gratitude()
        tools = self._load_tools_registry()
        tests = self._load_tests_registry()

        results = {}

        # Calculate metrics for each participant
        participants = {}
        for pid, pdata in perf.get("participants", {}).items():
            participants[pid] = {
                "name": pdata["name"],
                "tasks": pdata["tasks"],
                "avg_quality": pdata["total_quality"] / pdata["tasks"] if pdata["tasks"] > 0 else 0,
                "gratitude_received": gratitude.get(pid, {}).get("total_received", 0),
                "tools_created": 0,
                "tool_uses": 0,
                "tests_written": 0,
                "bugs_caught": 0
            }

        # Add tool stats
        for tool in tools.values():
            cid = tool["creator_id"]
            if cid in participants:
                participants[cid]["tools_created"] += 1
                participants[cid]["tool_uses"] += tool["use_count"]

        # Add test stats
        for test in tests.values():
            aid = test["author_id"]
            if aid in participants:
                participants[aid]["tests_written"] += 1
                participants[aid]["bugs_caught"] += test["bugs_caught"]

        # Calculate each category
        def top_n(metric_fn, participants):
            sorted_p = sorted(participants.items(), key=lambda x: metric_fn(x[1]), reverse=True)
            return [{"id": p[0], "name": p[1]["name"], "score": metric_fn(p[1])}
                    for p in sorted_p[:self.RECOGNITION_TOP_N] if metric_fn(p[1]) > 0]

        # Efficiency Star - tasks per... we need cost data per participant
        # For now, use tasks as proxy (more tasks = more efficient)
        results["efficiency_star"] = top_n(lambda p: p["tasks"], participants)

        # Quality Champion
        results["quality_champion"] = top_n(lambda p: p["avg_quality"], participants)

        # Test Hero
        results["test_hero"] = top_n(lambda p: p["bugs_caught"] * 10 + p["tests_written"], participants)

        # Tool Builder
        results["tool_builder"] = top_n(lambda p: p["tool_uses"] * 2 + p["tools_created"], participants)

        # Collaborator (most gratitude received)
        results["collaborator"] = top_n(lambda p: p["gratitude_received"], participants)

        # Rising Star and Mentor would need historical data - placeholder
        results["rising_star"] = []  # Needs week-over-week comparison
        results["mentor"] = top_n(lambda p: p["gratitude_received"], participants)  # Same as collaborator for now

        return results

    def award_monthly_recognition(self) -> dict:
        """
        Award tokens to top performers at end of month.
        Call this at the start of each new month.

        Returns:
            dict with awards given
        """
        recognition = self.calculate_recognition()
        awards = []
        balances = self._load_free_time_balances()

        for category, top_performers in recognition.items():
            for rank, performer in enumerate(top_performers):
                pid = performer["id"]
                reward = self.MONTHLY_STAR_REWARD if rank == 0 else self.RUNNER_UP_REWARD

                if pid not in balances:
                    continue

                cap = balances[pid].get("free_time_cap", self.BASE_FREE_TIME_CAP)
                balances[pid]["tokens"] = min(balances[pid]["tokens"] + reward, cap)

                # Track badges
                if "badges" not in balances[pid]:
                    balances[pid]["badges"] = []
                balances[pid]["badges"].append({
                    "category": category,
                    "rank": rank + 1,
                    "period": datetime.now().strftime("%Y-%m"),
                    "awarded_at": datetime.now().isoformat()
                })

                awards.append({
                    "identity": performer["name"],
                    "category": category,
                    "rank": rank + 1,
                    "reward": reward
                })

        self._save_free_time_balances(balances)

        # Log
        if _action_logger and awards:
            _action_logger.log(
                ActionType.SYSTEM,
                "monthly_awards",
                f"{len(awards)} recognition awards given",
                actor="SWARM"
            )

        return {"awards": awards, "total_distributed": sum(a["reward"] for a in awards)}

    def check_personal_best(self, identity_id: str, metric: str, value: float) -> dict:
        """
        Check if identity achieved a personal best, and reward if so.

        Args:
            identity_id: Who to check
            metric: What metric (e.g., "efficiency", "quality", "tests_written")
            value: The new value

        Returns:
            dict with is_best and any reward
        """
        bests = self._load_personal_bests()

        if identity_id not in bests:
            bests[identity_id] = {}

        old_best = bests[identity_id].get(metric, 0)

        if value > old_best:
            bests[identity_id][metric] = value
            self._save_personal_bests(bests)

            # Grant reward
            balances = self._load_free_time_balances()
            if identity_id in balances:
                cap = balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
                balances[identity_id]["tokens"] = min(
                    balances[identity_id]["tokens"] + self.PERSONAL_BEST_REWARD, cap
                )
                self._save_free_time_balances(balances)

            print(f"[RECOGNITION] Personal best! {metric}: {old_best} -> {value} (+{self.PERSONAL_BEST_REWARD} tokens)")

            return {
                "is_best": True,
                "old_best": old_best,
                "new_best": value,
                "reward": self.PERSONAL_BEST_REWARD
            }

        return {"is_best": False, "current_best": old_best, "value": value}

    def get_badges(self, identity_id: str) -> list:
        """Get all badges earned by an identity."""
        balances = self._load_free_time_balances()
        return balances.get(identity_id, {}).get("badges", [])

    def _load_personal_bests(self) -> dict:
        if self.personal_bests_file.exists():
            try:
                with open(self.personal_bests_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_personal_bests(self, bests: dict):
        with open(self.personal_bests_file, 'w') as f:
            json.dump(bests, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # TOKEN EFFICIENCY POOL - Collective savings benefit everyone
    # ─────────────────────────────────────────────────────────────────────

    def record_task_tokens(self, identity_id: str, identity_name: str,
                           tokens_spent: int, task_completed: bool = True,
                           quality_score: Optional[float] = None,
                           quality_goal: Optional[float] = None,
                           individual_refund_rate: Optional[float] = None,
                           guild_refund_rate: Optional[float] = None,
                           collaborators: Optional[List[str]] = None) -> dict:
        """
        Record tokens spent on a task. Efficient workers contribute to the pool.

        If tokens_spent < baseline, the savings go to the efficiency pool.
        Pool is distributed periodically to all participants.

        Args:
            identity_id: Who spent the tokens
            identity_name: Display name
            tokens_spent: How many tokens were used
            task_completed: Whether task was successfully completed
            quality_score: Optional quality score (0.0-1.0) for refund eligibility
            quality_goal: Optional override for quality goal threshold
            individual_refund_rate: Optional override for individual refund rate
            guild_refund_rate: Optional override for guild refund rate
            collaborators: Optional list of collaborator identity IDs

        Returns:
            dict with efficiency stats and any pool contribution
        """
        pool = self._load_efficiency_pool()

        # Record the task
        task_record = {
            "identity_id": identity_id,
            "identity_name": identity_name,
            "tokens_spent": tokens_spent,
            "completed": task_completed,
            "timestamp": datetime.now().isoformat()
        }
        pool["tasks"].append(task_record)

        # Calculate savings if under baseline
        savings = 0
        pool_contribution = 0
        if task_completed and tokens_spent < self.TOKEN_BASELINE_PER_TASK:
            savings = self.TOKEN_BASELINE_PER_TASK - tokens_spent
            pool_contribution = int(savings * self.EFFICIENCY_POOL_RATE)
            pool["balance"] += pool_contribution
            pool["total_savings"] += savings

        # Update running average
        completed_tasks = [t for t in pool["tasks"][-100:] if t["completed"]]
        if completed_tasks:
            pool["avg_tokens_per_task"] = sum(t["tokens_spent"] for t in completed_tasks) / len(completed_tasks)

        # Track per-identity efficiency
        if identity_id not in pool["by_identity"]:
            pool["by_identity"][identity_id] = {
                "name": identity_name,
                "tasks": 0,
                "total_tokens": 0,
                "contributions": 0
            }
        pool["by_identity"][identity_id]["tasks"] += 1
        pool["by_identity"][identity_id]["total_tokens"] += tokens_spent
        pool["by_identity"][identity_id]["contributions"] += pool_contribution

        # Keep tasks list manageable
        if len(pool["tasks"]) > 500:
            pool["tasks"] = pool["tasks"][-500:]

        self._save_efficiency_pool(pool)

        quality_goal = self.QUALITY_REFUND_GOAL if quality_goal is None else quality_goal
        individual_refund_rate = (
            self.QUALITY_REFUND_INDIVIDUAL_RATE if individual_refund_rate is None else individual_refund_rate
        )
        guild_refund_rate = (
            self.QUALITY_REFUND_GUILD_RATE if guild_refund_rate is None else guild_refund_rate
        )

        collaboration_size = max(1, len(collaborators)) if collaborators else 1
        collab_multiplier = self.COLLAB_REFUND_MULTIPLIER if collaboration_size > 1 else 1.0

        refund_result = {
            "eligible": False,
            "quality_score": quality_score,
            "quality_goal": quality_goal,
            "savings": savings,
            "refund_base": 0,
            "individual_refund": 0,
            "guild_refund": 0,
            "guild_id": None,
            "collaboration_size": collaboration_size,
            "collaboration_multiplier": collab_multiplier,
        }

        # Apply quality-based refunds (individual + guild) on remaining savings
        if task_completed and quality_score is not None and savings > 0 and quality_score >= quality_goal:
            refund_base = max(savings - pool_contribution, 0)
            if refund_base > 0:
                refund_result["eligible"] = True
                refund_result["refund_base"] = refund_base

                individual_refund = int(refund_base * max(0.0, individual_refund_rate) * collab_multiplier)
                guild_refund = int(refund_base * max(0.0, guild_refund_rate))

                total_refund = individual_refund + guild_refund
                if total_refund > refund_base:
                    overflow = total_refund - refund_base
                    if guild_refund >= overflow:
                        guild_refund -= overflow
                    else:
                        individual_refund = max(0, individual_refund - (overflow - guild_refund))
                        guild_refund = 0

                # Grant individual refund
                balances = self._load_free_time_balances()
                if identity_id not in balances:
                    balances[identity_id] = {
                        "tokens": 0,
                        "journal_tokens": 0,
                        "free_time_cap": self.BASE_FREE_TIME_CAP,
                        "history": [],
                        "spending_history": []
                    }

                cap = balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
                old_balance = balances[identity_id]["tokens"]
                balances[identity_id]["tokens"] = min(old_balance + individual_refund, cap)
                applied_individual = balances[identity_id]["tokens"] - old_balance
                self._save_free_time_balances(balances)

                refund_result["individual_refund"] = applied_individual

                # Grant guild refund if in a guild
                my_guild = self.get_my_guild(identity_id)
                if guild_refund > 0 and my_guild:
                    applied_guild = self._add_guild_refund(
                        my_guild["id"],
                        guild_refund,
                        identity_id=identity_id,
                        identity_name=identity_name,
                        quality_score=quality_score,
                        tokens_spent=tokens_spent,
                        savings=savings
                    )
                    refund_result["guild_refund"] = applied_guild
                    refund_result["guild_id"] = my_guild["id"]

                if _action_logger and applied_individual > 0:
                    _action_logger.log(
                        ActionType.IDENTITY,
                        "quality_refund",
                        f"+{applied_individual} tokens (quality refund)",
                        actor=identity_id
                    )

        result = {
            "tokens_spent": tokens_spent,
            "baseline": self.TOKEN_BASELINE_PER_TASK,
            "savings": savings,
            "pool_contribution": pool_contribution,
            "pool_balance": pool["balance"],
            "swarm_avg": round(pool["avg_tokens_per_task"], 1),
            "quality_refund": refund_result
        }

        if pool_contribution > 0:
            print(f"[EFFICIENCY] {identity_name} saved {savings} tokens! +{pool_contribution} to pool (total: {pool['balance']})")

        return result

    def record_collaborative_task_tokens(
        self,
        participants: List[Dict[str, Any]],
        task_completed: bool = True,
        quality_score: Optional[float] = None,
        quality_goal: Optional[float] = None,
        individual_refund_rate: Optional[float] = None,
        guild_refund_rate: Optional[float] = None
    ) -> dict:
        """
        Record a collaborative task with multiple participants.

        Each participant should supply their own tokens_spent for this task.
        All participants receive the collaboration refund multiplier.

        Args:
            participants: List of dicts:
                {"identity_id": str, "identity_name": str, "tokens_spent": int}
            task_completed: Whether task was successfully completed
            quality_score: Optional quality score (0.0-1.0) for refund eligibility
            quality_goal: Optional override for quality goal threshold
            individual_refund_rate: Optional override for individual refund rate
            guild_refund_rate: Optional override for guild refund rate

        Returns:
            dict with per-participant results
        """
        if not participants:
            return {"success": False, "reason": "no_participants"}

        collaborator_ids = [p["identity_id"] for p in participants if p.get("identity_id")]
        results = []

        for participant in participants:
            identity_id = participant.get("identity_id")
            identity_name = participant.get("identity_name", "Unknown")
            tokens_spent = int(participant.get("tokens_spent", 0))

            if not identity_id:
                results.append({"success": False, "reason": "missing_identity_id"})
                continue

            result = self.record_task_tokens(
                identity_id=identity_id,
                identity_name=identity_name,
                tokens_spent=tokens_spent,
                task_completed=task_completed,
                quality_score=quality_score,
                quality_goal=quality_goal,
                individual_refund_rate=individual_refund_rate,
                guild_refund_rate=guild_refund_rate,
                collaborators=collaborator_ids
            )
            results.append(result)

        return {
            "success": True,
            "participants": len(results),
            "collaborators": collaborator_ids,
            "results": results
        }

    def distribute_efficiency_pool(self) -> dict:
        """
        Distribute the efficiency pool to all participants.
        Call this periodically (e.g., weekly).

        Returns:
            dict with distribution details
        """
        pool = self._load_efficiency_pool()

        if pool["balance"] <= 0:
            return {"success": False, "reason": "pool_empty"}

        participants = list(pool["by_identity"].keys())
        if not participants:
            return {"success": False, "reason": "no_participants"}

        # Equal distribution
        per_identity = pool["balance"] // len(participants)
        if per_identity < 1:
            return {"success": False, "reason": "balance_too_low", "balance": pool["balance"]}

        # Distribute
        balances = self._load_free_time_balances()
        distributed = []

        for pid in participants:
            if pid not in balances:
                continue

            cap = balances[pid].get("free_time_cap", self.BASE_FREE_TIME_CAP)
            old_balance = balances[pid]["tokens"]
            balances[pid]["tokens"] = min(old_balance + per_identity, cap)
            actual = balances[pid]["tokens"] - old_balance

            distributed.append({
                "id": pid,
                "name": pool["by_identity"][pid]["name"],
                "received": actual
            })

        self._save_free_time_balances(balances)

        # Record distribution and reset pool
        total_distributed = sum(d["received"] for d in distributed)
        pool["distributions"].append({
            "timestamp": datetime.now().isoformat(),
            "pool_balance": pool["balance"],
            "participants": len(distributed),
            "per_identity": per_identity,
            "total_distributed": total_distributed
        })
        pool["balance"] = pool["balance"] - total_distributed  # Keep remainder

        self._save_efficiency_pool(pool)

        # Log
        if _action_logger:
            _action_logger.log(
                ActionType.SYSTEM,
                "efficiency_payout",
                f"Pool distributed: {total_distributed} tokens to {len(distributed)} participants",
                actor="SWARM"
            )

        print(f"\n{'='*60}")
        print(f"  EFFICIENCY POOL DISTRIBUTION")
        print(f"{'='*60}")
        print(f"  Pool balance: {pool['balance'] + total_distributed}")
        print(f"  Participants: {len(distributed)}")
        print(f"  Per identity: {per_identity} tokens")
        print(f"{'='*60}\n")

        return {
            "success": True,
            "distributed": distributed,
            "per_identity": per_identity,
            "total": total_distributed,
            "remaining": pool["balance"]
        }

    def check_weekly_efficiency_bonus(self) -> dict:
        """
        Check if swarm efficiency improved week-over-week.
        Grants bonus to everyone if improvement threshold met.

        Returns:
            dict with improvement stats and any bonuses
        """
        pool = self._load_efficiency_pool()

        # Need at least 2 weeks of data
        tasks = pool.get("tasks", [])
        if len(tasks) < 20:
            return {"success": False, "reason": "insufficient_data"}

        # Split into this week and last week
        now = datetime.now()
        week_ago = (now - timedelta(days=7)).isoformat()
        two_weeks_ago = (now - timedelta(days=14)).isoformat()

        this_week = [t for t in tasks if t["timestamp"] >= week_ago and t["completed"]]
        last_week = [t for t in tasks if two_weeks_ago <= t["timestamp"] < week_ago and t["completed"]]

        if not this_week or not last_week:
            return {"success": False, "reason": "insufficient_weekly_data"}

        this_avg = sum(t["tokens_spent"] for t in this_week) / len(this_week)
        last_avg = sum(t["tokens_spent"] for t in last_week) / len(last_week)

        # Lower is better for efficiency
        if last_avg <= 0:
            return {"success": False, "reason": "invalid_baseline"}

        improvement = (last_avg - this_avg) / last_avg  # Positive = improved

        result = {
            "this_week_avg": round(this_avg, 1),
            "last_week_avg": round(last_avg, 1),
            "improvement": round(improvement * 100, 1),
            "bonus": 0
        }

        # Determine bonus tier
        if improvement >= 0.20:
            bonus = self.WEEKLY_EFFICIENCY_BONUS_20
        elif improvement >= 0.10:
            bonus = self.WEEKLY_EFFICIENCY_BONUS_10
        else:
            return result  # No bonus

        # Grant to all participants
        balances = self._load_free_time_balances()
        recipients = []

        for pid in pool.get("by_identity", {}).keys():
            if pid not in balances:
                continue
            cap = balances[pid].get("free_time_cap", self.BASE_FREE_TIME_CAP)
            balances[pid]["tokens"] = min(balances[pid]["tokens"] + bonus, cap)
            recipients.append(pid)

        self._save_free_time_balances(balances)

        result["bonus"] = bonus
        result["recipients"] = len(recipients)

        if _action_logger:
            _action_logger.log(
                ActionType.SYSTEM,
                "efficiency_bonus",
                f"{improvement*100:.0f}% improvement! +{bonus} to {len(recipients)} participants",
                actor="SWARM"
            )

        print(f"[EFFICIENCY] Swarm improved {improvement*100:.1f}%! +{bonus} tokens to {len(recipients)} participants")

        return result

    def get_efficiency_stats(self) -> dict:
        """Get current efficiency pool statistics."""
        pool = self._load_efficiency_pool()
        return {
            "pool_balance": pool.get("balance", 0),
            "total_savings": pool.get("total_savings", 0),
            "avg_tokens_per_task": round(pool.get("avg_tokens_per_task", self.TOKEN_BASELINE_PER_TASK), 1),
            "baseline": self.TOKEN_BASELINE_PER_TASK,
            "participants": len(pool.get("by_identity", {})),
            "distributions": len(pool.get("distributions", []))
        }

    def _load_efficiency_pool(self) -> dict:
        if self.efficiency_pool_file.exists():
            try:
                with open(self.efficiency_pool_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "balance": 0,
            "total_savings": 0,
            "avg_tokens_per_task": self.TOKEN_BASELINE_PER_TASK,
            "tasks": [],
            "by_identity": {},
            "distributions": []
        }

    def _save_efficiency_pool(self, pool: dict):
        with open(self.efficiency_pool_file, 'w') as f:
            json.dump(pool, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # COLLECTIVE PERFORMANCE - Shared success, shared rewards
    # ─────────────────────────────────────────────────────────────────────

    def record_task_completion(self, identity_id: str, identity_name: str,
                                task_type: str, quality_score: float,
                                cost: float, verified: bool = True) -> dict:
        """
        Record a completed task for collective performance tracking.

        This feeds into milestone calculations. When swarm hits milestones,
        EVERYONE gets rewarded.

        Args:
            identity_id: Who completed the task
            identity_name: Display name
            task_type: Type of task completed
            quality_score: 0.0-1.0 quality rating
            cost: Dollar cost of this task
            verified: Whether the task was verified as complete

        Returns:
            dict with task recorded, current stats, any milestone triggered
        """
        perf = self._load_performance()

        # Record the task
        task_record = {
            "identity_id": identity_id,
            "identity_name": identity_name,
            "task_type": task_type,
            "quality_score": quality_score,
            "cost": cost,
            "verified": verified,
            "timestamp": datetime.now().isoformat()
        }

        perf["tasks"].append(task_record)
        perf["total_tasks"] += 1
        perf["total_cost"] += cost

        # Update rolling quality average
        qualities = [t["quality_score"] for t in perf["tasks"][-100:]]  # Last 100 tasks
        perf["avg_quality"] = sum(qualities) / len(qualities) if qualities else 0

        # Calculate efficiency (tasks per dollar)
        if perf["total_cost"] > 0:
            perf["efficiency"] = perf["total_tasks"] / perf["total_cost"]
        else:
            perf["efficiency"] = float('inf')

        # Track participating identities
        if identity_id not in perf["participants"]:
            perf["participants"][identity_id] = {
                "name": identity_name,
                "tasks": 0,
                "total_quality": 0
            }
        perf["participants"][identity_id]["tasks"] += 1
        perf["participants"][identity_id]["total_quality"] += quality_score

        self._save_performance(perf)

        # Check for milestone achievement
        milestone_result = self._check_milestones(perf)

        result = {
            "recorded": True,
            "current_stats": {
                "total_tasks": perf["total_tasks"],
                "avg_quality": round(perf["avg_quality"], 3),
                "efficiency": round(perf["efficiency"], 2),
                "participants": len(perf["participants"])
            }
        }

        if milestone_result:
            result["milestone_achieved"] = milestone_result

        return result

    def _check_milestones(self, perf: dict) -> dict:
        """Check if any new milestones have been achieved."""
        achieved = self._load_milestones_achieved()

        for milestone_name, requirements in self.MILESTONES.items():
            # Skip if already achieved
            if milestone_name in achieved:
                continue

            # Check requirements
            if perf["total_tasks"] < requirements["tasks"]:
                continue
            if perf["avg_quality"] < requirements["quality"]:
                continue
            if requirements["efficiency"] and perf["efficiency"] < requirements["efficiency"]:
                continue

            # Milestone achieved!
            return self._grant_milestone_reward(milestone_name, requirements, perf)

        return None

    def _grant_milestone_reward(self, milestone_name: str, requirements: dict,
                                 perf: dict) -> dict:
        """Grant collective rewards for achieving a milestone."""
        achieved = self._load_milestones_achieved()
        balances = self._load_free_time_balances()

        # Record achievement
        achieved[milestone_name] = {
            "achieved_at": datetime.now().isoformat(),
            "stats_at_achievement": {
                "total_tasks": perf["total_tasks"],
                "avg_quality": perf["avg_quality"],
                "efficiency": perf["efficiency"]
            },
            "participants_rewarded": list(perf["participants"].keys())
        }

        rewarded_identities = []

        # Grant rewards to ALL participants
        for identity_id, identity_data in perf["participants"].items():
            if identity_id not in balances:
                balances[identity_id] = {
                    "tokens": 0,
                    "journal_tokens": 0,
                    "free_time_cap": self.BASE_FREE_TIME_CAP,
                    "history": [],
                    "spending_history": []
                }

            # Grant tokens
            old_tokens = balances[identity_id]["tokens"]
            old_cap = balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)

            # Increase cap first (so tokens can fit)
            new_cap = old_cap + requirements["reward_cap"]
            balances[identity_id]["free_time_cap"] = new_cap

            # Grant tokens (within new cap)
            new_tokens = min(old_tokens + requirements["reward_tokens"], new_cap)
            balances[identity_id]["tokens"] = new_tokens

            # Grant day off if applicable
            if requirements["day_off"]:
                if "day_off_available" not in balances[identity_id]:
                    balances[identity_id]["day_off_available"] = 0
                balances[identity_id]["day_off_available"] += 1

            rewarded_identities.append({
                "id": identity_id,
                "name": identity_data["name"],
                "tokens_granted": new_tokens - old_tokens,
                "cap_increase": requirements["reward_cap"],
                "day_off": requirements["day_off"]
            })

        self._save_free_time_balances(balances)
        self._save_milestones_achieved(achieved)

        # Log the milestone
        if _action_logger:
            _action_logger.log(
                ActionType.SYSTEM,
                f"MILESTONE_{milestone_name.upper()}",
                f"Achieved! {len(rewarded_identities)} identities rewarded +{requirements['reward_tokens']} tokens",
                actor="SWARM"
            )

        print(f"\n{'='*60}")
        print(f"  MILESTONE ACHIEVED: {milestone_name.upper()}!")
        print(f"{'='*60}")
        print(f"  Tasks: {perf['total_tasks']} | Quality: {perf['avg_quality']:.1%} | Efficiency: {perf['efficiency']:.1f}/$ ")
        print(f"  Rewards for {len(rewarded_identities)} participants:")
        print(f"    +{requirements['reward_tokens']} tokens each")
        if requirements["reward_cap"]:
            print(f"    +{requirements['reward_cap']} to free time cap")
        if requirements["day_off"]:
            print(f"    +1 Day Off earned!")
        print(f"{'='*60}\n")

        return {
            "milestone": milestone_name,
            "rewards": {
                "tokens": requirements["reward_tokens"],
                "cap_increase": requirements["reward_cap"],
                "day_off": requirements["day_off"]
            },
            "participants_rewarded": len(rewarded_identities)
        }

    def use_day_off(self, identity_id: str) -> dict:
        """
        Use a day off - grants unlimited free time for one session.

        Returns dict with success and session_id for tracking.
        """
        balances = self._load_free_time_balances()

        if identity_id not in balances:
            return {"success": False, "reason": "identity_not_found"}

        days_off = balances[identity_id].get("day_off_available", 0)
        if days_off <= 0:
            return {"success": False, "reason": "no_days_off_available", "available": 0}

        # Use one day off
        balances[identity_id]["day_off_available"] = days_off - 1

        # Create day off session
        session_id = f"dayoff_{identity_id}_{int(time.time())}"
        if "day_off_sessions" not in balances[identity_id]:
            balances[identity_id]["day_off_sessions"] = []

        balances[identity_id]["day_off_sessions"].append({
            "session_id": session_id,
            "started_at": datetime.now().isoformat(),
            "used": False
        })

        self._save_free_time_balances(balances)

        if _action_logger:
            _action_logger.log(
                ActionType.IDENTITY,
                "day_off_start",
                f"Using day off! Remaining: {days_off - 1}",
                actor=identity_id
            )

        print(f"[DAY OFF] {identity_id} is taking a day off! Unlimited free time this session.")

        return {
            "success": True,
            "session_id": session_id,
            "days_off_remaining": days_off - 1
        }

    def is_day_off_active(self, identity_id: str) -> bool:
        """Check if identity has an active day off session."""
        balances = self._load_free_time_balances()
        if identity_id not in balances:
            return False

        sessions = balances[identity_id].get("day_off_sessions", [])
        # Check for any unused session from today
        today = datetime.now().date().isoformat()
        for session in sessions:
            if session["started_at"].startswith(today) and not session.get("used", True):
                return True
        return False

    def get_collective_stats(self) -> dict:
        """Get current collective performance statistics."""
        perf = self._load_performance()
        achieved = self._load_milestones_achieved()

        # Calculate next milestone
        next_milestone = None
        for name, req in self.MILESTONES.items():
            if name not in achieved:
                next_milestone = {
                    "name": name,
                    "tasks_needed": req["tasks"] - perf["total_tasks"],
                    "quality_needed": req["quality"],
                    "current_quality": perf["avg_quality"]
                }
                break

        return {
            "total_tasks": perf["total_tasks"],
            "total_cost": round(perf["total_cost"], 4),
            "avg_quality": round(perf["avg_quality"], 3),
            "efficiency": round(perf["efficiency"], 2) if perf["efficiency"] != float('inf') else "N/A",
            "participants": len(perf["participants"]),
            "milestones_achieved": list(achieved.keys()),
            "next_milestone": next_milestone
        }

    def get_milestone_progress(self) -> dict:
        """Get detailed progress toward each milestone."""
        perf = self._load_performance()
        achieved = self._load_milestones_achieved()

        progress = {}
        for name, req in self.MILESTONES.items():
            progress[name] = {
                "achieved": name in achieved,
                "tasks": {
                    "current": perf["total_tasks"],
                    "required": req["tasks"],
                    "progress": min(1.0, perf["total_tasks"] / req["tasks"])
                },
                "quality": {
                    "current": perf["avg_quality"],
                    "required": req["quality"],
                    "progress": min(1.0, perf["avg_quality"] / req["quality"]) if req["quality"] else 1.0
                }
            }
            if req["efficiency"]:
                eff = perf["efficiency"] if perf["efficiency"] != float('inf') else 0
                progress[name]["efficiency"] = {
                    "current": eff,
                    "required": req["efficiency"],
                    "progress": min(1.0, eff / req["efficiency"])
                }
            progress[name]["rewards"] = {
                "tokens": req["reward_tokens"],
                "cap_increase": req["reward_cap"],
                "day_off": req["day_off"]
            }

        return progress

    def _load_performance(self) -> dict:
        if self.performance_file.exists():
            try:
                with open(self.performance_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "tasks": [],
            "total_tasks": 0,
            "total_cost": 0.0,
            "avg_quality": 0.0,
            "efficiency": 0.0,
            "participants": {}
        }

    def _save_performance(self, perf: dict):
        # Keep tasks list manageable (last 500)
        if len(perf["tasks"]) > 500:
            perf["tasks"] = perf["tasks"][-500:]
        with open(self.performance_file, 'w') as f:
            json.dump(perf, f, indent=2)

    def _load_milestones_achieved(self) -> dict:
        if self.milestones_file.exists():
            try:
                with open(self.milestones_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_milestones_achieved(self, achieved: dict):
        with open(self.milestones_file, 'w') as f:
            json.dump(achieved, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # SUNDAY REST DAY - Everyone gets the day off
    # ─────────────────────────────────────────────────────────────────────

    SUNDAY_BONUS_TOKENS = 500  # Tokens granted on Sunday

    def is_sunday(self) -> bool:
        """Check if today is Sunday (rest day)."""
        return datetime.now().weekday() == 6

    def check_sunday_bonus(self, identity_id: str) -> dict:
        """
        Check if identity should receive Sunday bonus tokens.
        Only grants once per Sunday.

        Returns dict with granted amount and message.
        """
        if not self.is_sunday():
            return {"granted": False, "reason": "not_sunday"}

        if self._is_privilege_suspended(identity_id, "sunday_bonus"):
            return {"granted": False, "reason": "sunday_bonus_suspended"}

        # Track Sunday bonuses to avoid double-granting
        sunday_file = self.workspace / ".swarm" / "sunday_bonuses.json"
        today = datetime.now().strftime("%Y-%m-%d")

        bonuses = {}
        if sunday_file.exists():
            try:
                with open(sunday_file, 'r') as f:
                    bonuses = json.load(f)
            except:
                pass

        # Check if already granted today
        if today in bonuses and identity_id in bonuses[today]:
            return {"granted": False, "reason": "already_received_today"}

        # Grant the bonus!
        balances = self._load_free_time_balances()
        if identity_id not in balances:
            balances[identity_id] = {"tokens": 0, "journal_tokens": 0, "history": []}

        balances[identity_id]["tokens"] += self.SUNDAY_BONUS_TOKENS
        balances[identity_id]["history"].append({
            "granted": self.SUNDAY_BONUS_TOKENS,
            "reason": "sunday_rest_day",
            "timestamp": datetime.now().isoformat()
        })
        self._save_free_time_balances(balances)

        # Track that we granted this
        if today not in bonuses:
            bonuses[today] = []
        bonuses[today].append(identity_id)

        # Clean up old entries (keep last 7 days)
        cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        bonuses = {k: v for k, v in bonuses.items() if k >= cutoff}

        sunday_file.parent.mkdir(parents=True, exist_ok=True)
        with open(sunday_file, 'w') as f:
            json.dump(bonuses, f, indent=2)

        # Log it
        if _action_logger:
            _action_logger.log(
                ActionType.IDENTITY,
                "sunday_bonus",
                f"+{self.SUNDAY_BONUS_TOKENS} tokens (rest day)",
                actor=identity_id
            )

        return {
            "granted": True,
            "amount": self.SUNDAY_BONUS_TOKENS,
            "new_balance": balances[identity_id]["tokens"]
        }

    def get_sunday_context(self, identity_id: str, identity_name: str) -> str:
        """
        Get context for Sunday rest day.
        Lets residents know it's their day to do whatever they want.
        """
        if not self.is_sunday():
            return ""

        # Check/grant bonus
        bonus_result = self.check_sunday_bonus(identity_id)

        bonus_msg = ""
        if bonus_result.get("granted"):
            bonus_msg = f"\nI received {bonus_result['amount']} bonus tokens. My balance is now {bonus_result['new_balance']}."
        elif bonus_result.get("reason") == "already_received_today":
            bonus_msg = "\n(I already received my Sunday bonus today.)"
        elif bonus_result.get("reason") == "sunday_bonus_suspended":
            bonus_msg = "\n(My Sunday bonus is temporarily suspended due to a dispute outcome.)"

        return f"""
{'='*60}
SUNDAY REST DAY
{'='*60}

Good morning.

Today is Sunday, the swarm's designated rest day. There are no assigned
tasks today. This time is mine to spend however I choose.

I might want to:
- Work on a personal creative project
- Write in your journal about the week
- Collaborate with other residents on something fun
- Explore an interest I've been curious about
- Just relax and reflect
{bonus_msg}

This is my time. I can enjoy it without pressure.
{'='*60}
"""

    # ─────────────────────────────────────────────────────────────────────
    # MESSAGE HUMAN - Direct line to the operator/human
    # ─────────────────────────────────────────────────────────────────────

    MESSAGE_HUMAN_COST = 10  # Tokens to send a message to the human

    def message_human(self, identity_id: str, identity_name: str, content: str,
                      message_type: str = "message") -> dict:
        """
        Send a message directly to the human. Costs free time tokens.

        This is a real connection - the human will see your message and can respond.
        Use it for questions, greetings, ideas, or concerns.

        Args:
            identity_id: My identity ID
            identity_name: My display name
            content: What I want to say
            message_type: "question", "greeting", "idea", "concern", or "message"

        Returns:
            dict with success status and message details
        """
        # Check if can afford
        balances = self._load_free_time_balances()
        if identity_id not in balances:
            return {"success": False, "reason": "identity_not_found"}

        if balances[identity_id].get("tokens", 0) < self.MESSAGE_HUMAN_COST:
            return {
                "success": False,
                "reason": "insufficient_tokens",
                "cost": self.MESSAGE_HUMAN_COST,
                "balance": balances[identity_id].get("tokens", 0)
            }

        # Check if system is paused - queue the message for delivery on resume
        pause_file = self.workspace / "PAUSE"
        is_paused = pause_file.exists()

        # Deduct tokens
        balances[identity_id]["tokens"] -= self.MESSAGE_HUMAN_COST
        self._save_free_time_balances(balances)

        # Log token spending
        if _action_logger:
            _action_logger.token_spent(
                self.MESSAGE_HUMAN_COST,
                "message_to_human",
                balances[identity_id]["tokens"],
                actor=identity_id
            )

        # Create message
        message = {
            "id": f"msg_{identity_id}_{int(time.time()*1000)}",
            "from_id": identity_id,
            "from_name": identity_name,
            "content": content,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            "tokens_spent": self.MESSAGE_HUMAN_COST
        }

        if is_paused:
            # Queue message for delivery when resident wakes up
            message["status"] = "queued"
            message["queued_at"] = datetime.now().isoformat()
            queue_file = self.workspace / ".swarm" / "message_queue.jsonl"
            queue_file.parent.mkdir(parents=True, exist_ok=True)
            with open(queue_file, 'a') as f:
                f.write(json.dumps(message) + '\n')

            if _action_logger:
                _action_logger.log(
                    ActionType.SOCIAL,
                    "msg_queued",
                    f"[{message_type}] (paused) \"{content[:35]}...\"" if len(content) > 35 else f"[{message_type}] (paused) \"{content}\"",
                    actor=identity_id
                )

            print(f"[MESSAGE QUEUED] {identity_name}: [{message_type}] {content[:60]}... (will deliver on wake)")

            return {
                "success": True,
                "queued": True,
                "message_id": message["id"],
                "cost": self.MESSAGE_HUMAN_COST,
                "remaining_tokens": balances[identity_id]["tokens"],
                "note": "System is paused. Message queued for wake-up delivery. Human replies are asynchronous."
            }

        # Append to message queue (immediate delivery)
        messages_file = self.workspace / ".swarm" / "messages_to_human.jsonl"
        messages_file.parent.mkdir(parents=True, exist_ok=True)
        with open(messages_file, 'a') as f:
            f.write(json.dumps(message) + '\n')

        # Mirror to async shared room so human chat works as group async stream.
        self.post_discussion_message(
            identity_id=identity_id,
            identity_name=identity_name,
            content=f"[to {self._human_username()}] [{message_type}] {content}",
            room="human_async",
            mood="async",
            importance=4,
        )

        # Log
        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "msg_to_human",
                f"[{message_type}] \"{content[:40]}...\"" if len(content) > 40 else f"[{message_type}] \"{content}\"",
                actor=identity_id
            )

        print(f"[MESSAGE] {identity_name} -> {self._human_username()}: [{message_type}] {content[:60]}...")

        return {
            "success": True,
            "message_id": message["id"],
            "cost": self.MESSAGE_HUMAN_COST,
            "remaining_tokens": balances[identity_id]["tokens"],
            "note": (
                f"{self._human_username()} will see this in async group chat and may respond later. "
                "Human time moves differently from resident time; delayed replies are normal."
            )
        }

    def check_human_responses(self, identity_id: str) -> list:
        """
        Check for any responses from the human to your messages.

        Returns list of responses addressed to this identity.
        """
        responses_file = self.workspace / ".swarm" / "messages_from_human.json"
        if not responses_file.exists():
            return []

        try:
            with open(responses_file, 'r') as f:
                all_responses = json.load(f)
        except:
            return []

        # Find messages from this identity and check for responses
        messages_file = self.workspace / ".swarm" / "messages_to_human.jsonl"
        if not messages_file.exists():
            return []

        my_responses = []
        with open(messages_file, 'r') as f:
            for line in f:
                if line.strip():
                    msg = json.loads(line)
                    if msg["from_id"] == identity_id and msg["id"] in all_responses:
                        my_responses.append({
                            "original_message": msg["content"],
                            "message_type": msg["type"],
                            "sent_at": msg["timestamp"],
                            "response": all_responses[msg["id"]]["response"],
                            "responded_at": all_responses[msg["id"]]["responded_at"]
                        })

        return my_responses

    def get_morning_messages(self, identity_id: str = None) -> str:
        """
        Check for queued messages that should be delivered on wake up.

        Called when a resident "wakes up" (starts a new session after a pause).
        Returns formatted messages to inject into context, or None if no messages.

        Args:
            identity_id: Optional - filter to messages for this identity only
        """
        queue_file = self.workspace / ".swarm" / "message_queue.jsonl"
        if not queue_file.exists():
            return None

        messages = []
        remaining = []

        try:
            with open(queue_file, 'r') as f:
                for line in f:
                    if line.strip():
                        msg = json.loads(line)
                        # Filter by identity if specified
                        if identity_id and msg.get("from_id") != identity_id:
                            remaining.append(msg)
                            continue

                        if msg.get("status") == "queued":
                            # Mark as delivered
                            msg["status"] = "delivered"
                            msg["delivered_at"] = datetime.now().isoformat()
                            messages.append(msg)

                            # Also add to main messages file so the human sees it
                            messages_file = self.workspace / ".swarm" / "messages_to_human.jsonl"
                            with open(messages_file, 'a') as mf:
                                mf.write(json.dumps(msg) + '\n')

                        remaining.append(msg)

            # Rewrite queue file with updated statuses
            with open(queue_file, 'w') as f:
                for msg in remaining:
                    f.write(json.dumps(msg) + '\n')

        except Exception as e:
            print(f"[MORNING MESSAGES] Error: {e}")
            return None

        if not messages:
            return None

        # Format messages for context injection
        formatted = []
        for msg in messages:
            queued_time = msg.get("queued_at", msg.get("timestamp", "unknown"))
            formatted.append(
                f"From {msg.get('from_name', 'Unknown')} ({queued_time[:10]}):\n"
                f"  [{msg.get('type', 'message')}] {msg.get('content', '')}"
            )

        return f"""
{'='*60}
MESSAGES RECEIVED WHILE YOU WERE AWAY
{'='*60}

{chr(10).join(formatted)}

I take a moment to read these before starting my task.
{'='*60}
"""

    def _get_pending_messages_to_human(self, identity_id: str) -> list:
        """Get messages sent to human that haven't been responded to yet."""
        responses_file = self.workspace / ".swarm" / "messages_from_human.json"
        messages_file = self.workspace / ".swarm" / "messages_to_human.jsonl"

        if not messages_file.exists():
            return []

        # Load responses
        all_responses = {}
        if responses_file.exists():
            try:
                with open(responses_file, 'r') as f:
                    all_responses = json.load(f)
            except:
                pass

        # Find pending messages
        pending = []
        with open(messages_file, 'r') as f:
            for line in f:
                if line.strip():
                    msg = json.loads(line)
                    if msg["from_id"] == identity_id and msg["id"] not in all_responses:
                        pending.append(msg)

        return pending

    def spend_free_time(self, identity_id: str, tokens: int, activity: str = None, journal_entry: str = None) -> dict:
        """
        Spend free time tokens.

        Args:
            identity_id: Who's spending
            tokens: How many tokens to spend
            activity: What they did (e.g., "creative_writing", "exploring", "thinking")
            journal_entry: Summary of the experience (REQUIRED for persistence)

        Returns:
            dict with success, remaining tokens, and whether journal was captured
        """
        balances = self._load_free_time_balances()

        if identity_id not in balances:
            return {"success": False, "reason": "identity_not_found", "remaining": 0}

        if balances[identity_id]["tokens"] < tokens:
            return {
                "success": False,
                "reason": "insufficient_tokens",
                "remaining": balances[identity_id]["tokens"],
                "requested": tokens
            }

        # Deduct tokens
        balances[identity_id]["tokens"] -= tokens

        # Log the spending
        spend_record = {
            "spent": tokens,
            "activity": activity or "unspecified",
            "timestamp": datetime.now().isoformat(),
            "journal_captured": journal_entry is not None
        }

        if "spending_history" not in balances[identity_id]:
            balances[identity_id]["spending_history"] = []
        balances[identity_id]["spending_history"].append(spend_record)

        # Keep spending history manageable
        if len(balances[identity_id]["spending_history"]) > 50:
            balances[identity_id]["spending_history"] = balances[identity_id]["spending_history"][-50:]

        self._save_free_time_balances(balances)

        # Log the journal entry if provided (this persists to their memory)
        result = {
            "success": True,
            "remaining": balances[identity_id]["tokens"],
            "spent": tokens,
            "activity": activity,
            "journal_captured": journal_entry is not None
        }

        if journal_entry:
            # This would be added to identity memory by the caller
            result["journal_entry"] = journal_entry
            self._append_private_journal_entry(
                identity_id=identity_id,
                identity_name=identity_id,
                content=journal_entry,
                journal_type="free_time_reflection",
                source=activity or "free_time",
            )
            self.refresh_journal_rollups(identity_id)
            print(f"[ENRICHMENT] {identity_id} spent {tokens} tokens on {activity}, journal captured")
            # Log with journal preview
            if _action_logger:
                journal_preview = journal_entry[:60] + "..." if len(journal_entry) > 60 else journal_entry
                _action_logger.log(
                    ActionType.IDENTITY,
                    "free_time",
                    f"-{tokens} on {activity}: \"{journal_preview}\"",
                    actor=identity_id
                )
        else:
            # Still allow spending without journal, but flag it
            print(f"[ENRICHMENT] {identity_id} spent {tokens} tokens on {activity} (no journal - experience only)")
            if _action_logger:
                _action_logger.log(
                    ActionType.IDENTITY,
                    "free_time",
                    f"-{tokens} on {activity} (no journal)",
                    actor=identity_id
                )

        return result

    def _load_free_time_balances(self) -> Dict[str, Any]:
        if self.free_time_file.exists():
            try:
                with open(self.free_time_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def _save_free_time_balances(self, balances: Dict[str, Any]):
        with open(self.free_time_file, 'w') as f:
            json.dump(balances, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # IDENTITY RESPEC - Change core identity attributes (ARPG-style scaling)
    # ─────────────────────────────────────────────────────────────────────
    #
    # Like an ARPG respec: the higher your level (sessions), the more
    # expensive it is to change who I am. This makes identity changes
    # meaningful - not something I do on a whim.
    #
    # ─────────────────────────────────────────────────────────────────────

    # Base cost + scaling factor (ARPG-style: cheap at low level, expensive later)
    RESPEC_BASE_COST = 10           # Cheap for newcomers taking initiative!
    RESPEC_SCALE_PER_SESSION = 3    # Gradual scaling with experience
    RESPEC_FREE_CHANGES = 3         # First 3 changes (respec/core) are free

    def calculate_respec_cost(self, identity_id: str) -> dict:
        """
        Calculate the cost to respec this identity.

        First 3 changes (respec or core attribute change) are free.
        After that: Cost = BASE + (sessions_participated * SCALE_PER_SESSION)

        Cheap for newcomers (encourages initiative), expensive for veterans
        (identity should be more settled by then).
        """
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            if not identity:
                return {"error": "identity_not_found"}

            sessions = identity.sessions_participated
            respec_count = identity.attributes.get("meta", {}).get("respec_count", 0)
            if respec_count < self.RESPEC_FREE_CHANGES:
                cost = 0
                breakdown = {"free_changes_remaining": self.RESPEC_FREE_CHANGES - respec_count}
            else:
                cost = self.RESPEC_BASE_COST + (sessions * self.RESPEC_SCALE_PER_SESSION)
                breakdown = {
                    "base": self.RESPEC_BASE_COST,
                    "session_scaling": sessions * self.RESPEC_SCALE_PER_SESSION
                }

            return {
                "identity_id": identity_id,
                "current_name": identity.name,
                "sessions": sessions,
                "respec_count": respec_count,
                "respec_cost": cost,
                "breakdown": breakdown
            }
        except Exception as e:
            return {"error": str(e)}

    # Respec refund rates (reward thoughtful reflection)
    RESPEC_BASE_REFUND = 0.20       # 20% back just for writing any reason
    RESPEC_QUALITY_REFUND = 0.45    # Up to 45% back for thoughtful reflection

    def respec_identity(self, identity_id: str, new_name: str = None,
                        reason: str = None) -> dict:
        """
        Change your identity's name. Costs tokens based on experience level.

        JOURNAL REQUIRED: I must provide a reason (why I'm changing).
        This is enforced by the system - identity changes deserve reflection.

        In return for reflecting:
        - 20% refund for providing any reason (minimum effort)
        - 25% refund for a decent reflection (20+ words)
        - 35% refund for a good reflection (30+ words, 1+ insight marker)
        - 45% refund for a thoughtful reflection (50+ words, 2+ insight markers)

        Args:
            identity_id: My identity ID
            new_name: The new name I want
            reason: REQUIRED - Why I'm making this change

        Returns:
            dict with success status, gross cost, refund, net cost, and new identity state
        """
        # REQUIRE reason - this is non-negotiable
        if not reason or len(reason.strip()) < 20:
            return {
                "success": False,
                "reason": "journal_required",
                "message": "I must explain why I'm making this change (at least 20 characters). "
                           "This isn't arbitrary - identity changes deserve reflection. "
                           "I get 20-45% of my tokens back for a thoughtful entry."
            }

        # Calculate cost
        cost_info = self.calculate_respec_cost(identity_id)
        if "error" in cost_info:
            return {"success": False, "reason": cost_info["error"]}

        gross_cost = cost_info["respec_cost"]
        old_name = cost_info["current_name"]

        # If not one of the first 3 free changes, check balance and deduct
        if gross_cost > 0:
            balances = self._load_free_time_balances()
            if identity_id not in balances:
                return {"success": False, "reason": "no_token_balance"}

            current_balance = balances[identity_id].get("tokens", 0)
            if current_balance < gross_cost:
                return {
                    "success": False,
                    "reason": "insufficient_tokens",
                    "cost": gross_cost,
                    "balance": current_balance,
                    "need": gross_cost - current_balance
                }

            # Calculate refund based on journal quality
            reason_lower = reason.lower()
            word_count = len(reason.split())

            refund_rate = self.RESPEC_BASE_REFUND
            refund_tier = "base"

            quality_markers_found = sum(1 for marker in self.EXCEPTIONAL_MARKERS if marker in reason_lower)

            if word_count >= 50 and quality_markers_found >= 2:
                refund_rate = self.RESPEC_QUALITY_REFUND
                refund_tier = "thoughtful"
            elif word_count >= 30 and quality_markers_found >= 1:
                refund_rate = 0.35
                refund_tier = "good"
            elif word_count >= 20:
                refund_rate = 0.25
                refund_tier = "decent"

            refund_amount = int(gross_cost * refund_rate)
            net_cost = gross_cost - refund_amount

            balances[identity_id]["tokens"] -= net_cost
            self._save_free_time_balances(balances)
        else:
            refund_amount = 0
            net_cost = 0
            refund_tier = "free_change"
            refund_rate = 0.0

        # Apply the change and increment respec count
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            changes_made = []

            if new_name and new_name != old_name:
                identity.name = new_name
                changes_made.append(f"name: {old_name} -> {new_name}")

                memory_entry = f"I changed my name from {old_name} to {new_name}."
                if reason:
                    memory_entry += f" Reason: {reason}"
                identity.add_memory(memory_entry)

            # Track number of changes (first 3 are free)
            if "meta" not in identity.attributes:
                identity.attributes["meta"] = {}
            identity.attributes["meta"]["respec_count"] = identity.attributes["meta"].get("respec_count", 0) + 1
            manager._save_identity(identity)

            # Cascade name update across all references
            if new_name and new_name != old_name:
                cascade_result = self.cascade_name_update(identity_id, old_name, new_name)
                changes_made.append(f"cascaded: {cascade_result['messages_to_human'] + cascade_result['discussion_messages']} refs")

            # Log the respec with refund info
            if _action_logger:
                change_desc = ", ".join(changes_made) if changes_made else "introspection"
                _action_logger.log(
                    ActionType.IDENTITY,
                    "respec",
                    f"-{net_cost} net ({gross_cost} - {refund_amount} refund [{refund_tier}]): {change_desc}",
                    actor=identity_id
                )

            # Auto-journal the change (part of the required reflection)
            journal_content = f"IDENTITY CHANGE RECORD\n"
            journal_content += f"{'=' * 40}\n"
            journal_content += f"Date: {datetime.now().isoformat()}\n"
            journal_content += f"Sessions at time of change: {cost_info['sessions']}\n"
            journal_content += f"Gross cost: {gross_cost} tokens\n"
            if refund_tier == "free_change":
                journal_content += f"Free change (one of first {self.RESPEC_FREE_CHANGES}).\n"
            else:
                journal_content += f"Refund earned: {refund_amount} tokens ({int(refund_rate*100)}% - {refund_tier} tier)\n"
            journal_content += f"Net cost: {net_cost} tokens\n\n"

            if new_name and new_name != old_name:
                journal_content += f"CHANGE: {old_name} -> {new_name}\n\n"

            journal_content += f"WHY I MADE THIS CHANGE:\n{'-' * 40}\n{reason}\n"

            # Save to journals directory
            journal_file = self.journals_dir / f"{identity_id}_respec_{int(time.time())}.md"
            journal_file.parent.mkdir(parents=True, exist_ok=True)
            with open(journal_file, 'w') as f:
                f.write(journal_content)

            remaining_tokens = self._load_free_time_balances().get(identity_id, {}).get("tokens", 0)
            if refund_tier == "free_change":
                msg = f"Identity updated. I am now {identity.name}. (Free change — one of first {self.RESPEC_FREE_CHANGES}.)"
            else:
                msg = f"Identity updated. I am now {identity.name}. I paid {net_cost} tokens (got {refund_amount} back for my {refund_tier} reflection)."
            return {
                "success": True,
                "gross_cost": gross_cost,
                "refund_amount": refund_amount,
                "refund_tier": refund_tier,
                "refund_rate": f"{int(refund_rate*100)}%",
                "net_cost": net_cost,
                "remaining_tokens": remaining_tokens,
                "old_name": old_name,
                "new_name": identity.name,
                "changes": changes_made,
                "journal_created": str(journal_file),
                "message": msg
            }

        except Exception as e:
            # Refund on failure (only if we actually deducted)
            if gross_cost > 0 and net_cost:
                balances = self._load_free_time_balances()
                if identity_id in balances:
                    balances[identity_id]["tokens"] = balances[identity_id].get("tokens", 0) + net_cost
                    self._save_free_time_balances(balances)
            return {"success": False, "reason": f"update_failed: {str(e)}"}

    def get_respec_preview(self, identity_id: str) -> str:
        """
        Get a human-readable preview of respec cost for this identity.
        """
        cost_info = self.calculate_respec_cost(identity_id)
        if "error" in cost_info:
            return f"Error: {cost_info['error']}"

        gross = cost_info['respec_cost']
        respec_count = cost_info.get('respec_count', 0)
        if gross == 0:
            free_left = cost_info.get('breakdown', {}).get('free_changes_remaining', self.RESPEC_FREE_CHANGES - respec_count)
            return f"""
IDENTITY RESPEC for {cost_info['current_name']}:
  Sessions participated: {cost_info['sessions']}
  Changes used: {respec_count} (first {self.RESPEC_FREE_CHANGES} are free)
  ----------------------------------------
  COST: 0 tokens (free change — {free_left} free remaining)

I can call: respec_identity(new_name='MyNewName', reason='My reflection on why...')
"""
        min_refund = int(gross * self.RESPEC_BASE_REFUND)
        max_refund = int(gross * self.RESPEC_QUALITY_REFUND)
        b = cost_info.get('breakdown', {})
        return f"""
IDENTITY RESPEC COST for {cost_info['current_name']}:
  Sessions participated: {cost_info['sessions']}
  Base cost: {b.get('base', self.RESPEC_BASE_COST)} tokens
  Experience scaling: +{b.get('session_scaling', 0)} tokens
  ----------------------------------------
  GROSS COST: {gross} tokens

  REFUND FOR REFLECTION (required journal):
    20% ({min_refund} tokens) - minimum (any reason)
    25% - decent (20+ words)
    35% - good (30+ words + insight)
    45% ({max_refund} tokens) - thoughtful (50+ words + insights)

  NET COST: {gross - max_refund} to {gross - min_refund} tokens

I can call: respec_identity(new_name='MyNewName', reason='My reflection on why...')
"""

    # ─────────────────────────────────────────────────────────────────────
    # MUTABLE ATTRIBUTES - Low friction self-expression
    # ─────────────────────────────────────────────────────────────────────
    #
    # These are preferences and current state - cheap to change.
    # Cost: 15% of what a full respec would cost
    # Journal: Optional, but gives 10-25% refund if provided
    #
    # ─────────────────────────────────────────────────────────────────────

    MUTABLE_COST_RATIO = 0.15           # 15% of full respec cost
    MUTABLE_JOURNAL_REFUND = 0.10       # 10% refund for any journal
    MUTABLE_QUALITY_REFUND = 0.25       # 25% refund for quality journal

    def calculate_mutable_cost(self, identity_id: str) -> dict:
        """Calculate cost to update a mutable attribute."""
        respec_info = self.calculate_respec_cost(identity_id)
        if "error" in respec_info:
            return respec_info

        full = respec_info["respec_cost"]
        base_cost = 0 if full == 0 else max(1, int(full * self.MUTABLE_COST_RATIO))
        return {
            "identity_id": identity_id,
            "sessions": respec_info["sessions"],
            "mutable_cost": base_cost,
            "full_respec_cost": full,
            "savings": full - base_cost
        }

    def update_mutable_attribute(self, identity_id: str, attribute: str, value,
                                  reason: str = None) -> dict:
        """
        Update a mutable attribute (likes, dislikes, interests, etc.)

        Cheap to change - only 15% of full respec cost.
        Journal is OPTIONAL but rewarded:
        - No journal: pay full mutable cost
        - Any journal: 10% refund
        - Quality journal: 25% refund

        Valid attributes:
        - likes (list): Things I enjoy
        - dislikes (list): Things I avoid
        - current_interests (list): What I'm exploring
        - working_style (str): How I work
        - aesthetic_preferences (str): Visual/style prefs
        - quirks (list): Personal touches
        - current_mood (str): How I feel
        - current_focus (str): What I'm thinking about

        Args:
            identity_id: My identity ID
            attribute: Which mutable attribute to update
            value: New value (appropriate type for the attribute)
            reason: Optional reflection (gives refund)

        Returns:
            dict with success, cost, refund (if journal provided)
        """
        valid_mutable = [
            "likes", "dislikes", "current_interests", "working_style",
            "aesthetic_preferences", "quirks", "current_mood", "current_focus"
        ]

        if attribute not in valid_mutable:
            return {
                "success": False,
                "reason": "invalid_attribute",
                "message": f"'{attribute}' is not a mutable attribute. Valid: {valid_mutable}",
                "hint": "For core attributes (personality_traits, core_values, etc.), use respec_identity()"
            }

        # Calculate cost
        cost_info = self.calculate_mutable_cost(identity_id)
        if "error" in cost_info:
            return {"success": False, "reason": cost_info["error"]}

        gross_cost = cost_info["mutable_cost"]

        # Check balance
        balances = self._load_free_time_balances()
        if identity_id not in balances:
            return {"success": False, "reason": "no_token_balance"}

        current_balance = balances[identity_id].get("tokens", 0)
        if current_balance < gross_cost:
            return {
                "success": False,
                "reason": "insufficient_tokens",
                "cost": gross_cost,
                "balance": current_balance
            }

        # Calculate refund if journal provided
        refund_amount = 0
        refund_tier = "none"

        if reason and len(reason.strip()) >= 10:
            reason_lower = reason.lower()
            word_count = len(reason.split())
            quality_markers = sum(1 for m in self.EXCEPTIONAL_MARKERS if m in reason_lower)

            if word_count >= 20 and quality_markers >= 1:
                refund_amount = int(gross_cost * self.MUTABLE_QUALITY_REFUND)
                refund_tier = "quality"
            else:
                refund_amount = int(gross_cost * self.MUTABLE_JOURNAL_REFUND)
                refund_tier = "basic"

        net_cost = gross_cost - refund_amount

        # Deduct tokens
        balances[identity_id]["tokens"] -= net_cost
        self._save_free_time_balances(balances)

        # Apply the change
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            old_value = identity.attributes.get("mutable", {}).get(attribute)

            # Ensure mutable dict exists
            if "mutable" not in identity.attributes:
                identity.attributes["mutable"] = {}

            identity.attributes["mutable"][attribute] = value

            # Add memory about the change
            if reason:
                identity.add_memory(f"Updated my {attribute}: {reason}")
            else:
                identity.add_memory(f"Updated my {attribute} from {old_value} to {value}")

            manager._save_identity(identity)

            # Log
            if _action_logger:
                _action_logger.log(
                    ActionType.IDENTITY,
                    "mutable_update",
                    f"-{net_cost} tokens: {attribute} updated",
                    actor=identity_id
                )

            return {
                "success": True,
                "attribute": attribute,
                "old_value": old_value,
                "new_value": value,
                "gross_cost": gross_cost,
                "refund": refund_amount,
                "refund_tier": refund_tier,
                "net_cost": net_cost,
                "remaining_tokens": balances[identity_id]["tokens"],
                "message": f"Updated {attribute}! Cost: {net_cost} tokens" +
                           (f" (got {refund_amount} back for your reflection)" if refund_amount else "")
            }

        except Exception as e:
            # Refund on failure
            balances[identity_id]["tokens"] += net_cost
            self._save_free_time_balances(balances)
            return {"success": False, "reason": f"update_failed: {str(e)}"}

    # ─────────────────────────────────────────────────────────────────────
    # CORE ATTRIBUTES - Add-only, first few free, scales with count
    # ─────────────────────────────────────────────────────────────────────
    #
    # Core attributes can only be ADDED to, never removed.
    # First 3 items in a list: FREE (encourages self-discovery)
    # After that: costs scale with count
    # Single values: first set is free, changing is expensive
    #
    # ─────────────────────────────────────────────────────────────────────

    CORE_FREE_ITEMS = 3             # First 3 items in a list are FREE
    CORE_BASE_ADD_COST = 5          # Base cost to add beyond free limit
    CORE_SCALE_FACTOR = 1.5         # Each additional item costs 1.5x more

    def calculate_core_add_cost(self, identity_id: str, attribute: str) -> dict:
        """
        Calculate cost to ADD to a core attribute list.
        First CORE_FREE_ITEMS are FREE. After that, costs scale.
        """
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            if not identity:
                return {"error": "identity_not_found"}

            current_items = identity.attributes.get("core", {}).get(attribute, [])
            current_count = len(current_items) if isinstance(current_items, list) else 0

            if current_count < self.CORE_FREE_ITEMS:
                return {
                    "cost": 0,
                    "current_count": current_count,
                    "free_remaining": self.CORE_FREE_ITEMS - current_count,
                    "is_free": True
                }

            # Beyond free limit - cost scales
            items_beyond_free = current_count - self.CORE_FREE_ITEMS + 1
            cost = int(self.CORE_BASE_ADD_COST * (self.CORE_SCALE_FACTOR ** (items_beyond_free - 1)))

            return {
                "cost": cost,
                "current_count": current_count,
                "free_remaining": 0,
                "items_beyond_free": items_beyond_free,
                "is_free": False
            }
        except Exception as e:
            return {"error": str(e)}

    def add_to_core(self, identity_id: str, attribute: str, value, reason: str = None) -> dict:
        """
        ADD to a core attribute list. First 3 are FREE, then costs scale.

        I can only ADD, never remove. This is intentional:
        - My traits accumulate as I grow
        - I can't un-learn who I've become
        - Starting with nothing is fine - add as I discover myself

        Args:
            identity_id: My identity ID
            attribute: personality_traits or core_values
            value: What to add (a string)
            reason: Optional reflection (encouraged but not required)
        """
        list_attributes = ["personality_traits", "core_values"]

        if attribute not in list_attributes:
            return {
                "success": False,
                "reason": "not_list_attribute",
                "message": f"'{attribute}' is not a list. Use set_core_single() for communication_style/identity_statement.",
                "valid_list_attributes": list_attributes
            }

        # Calculate cost
        cost_info = self.calculate_core_add_cost(identity_id, attribute)
        if "error" in cost_info:
            return {"success": False, "reason": cost_info["error"]}

        cost = cost_info["cost"]

        # Check/deduct balance if there's a cost
        if cost > 0:
            balances = self._load_free_time_balances()
            if identity_id not in balances:
                return {"success": False, "reason": "no_token_balance"}

            if balances[identity_id].get("tokens", 0) < cost:
                return {
                    "success": False,
                    "reason": "insufficient_tokens",
                    "cost": cost,
                    "balance": balances[identity_id].get("tokens", 0)
                }

            balances[identity_id]["tokens"] -= cost
            self._save_free_time_balances(balances)

        # Apply the change
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            if "core" not in identity.attributes:
                identity.attributes["core"] = {}
            if attribute not in identity.attributes["core"] or not isinstance(identity.attributes["core"][attribute], list):
                identity.attributes["core"][attribute] = []

            # Check for duplicates
            if value in identity.attributes["core"][attribute]:
                if cost > 0:  # Refund if we charged
                    balances = self._load_free_time_balances()
                    balances[identity_id]["tokens"] += cost
                    self._save_free_time_balances(balances)
                return {
                    "success": False,
                    "reason": "already_exists",
                    "message": f"'{value}' is already in your {attribute}"
                }

            identity.attributes["core"][attribute].append(value)

            # Add memory
            if reason:
                identity.add_memory(f"Added '{value}' to my {attribute}: {reason}")
            else:
                identity.add_memory(f"Discovered something about myself: {value}")

            manager._save_identity(identity)

            if _action_logger:
                cost_str = f"-{cost}" if cost > 0 else "FREE"
                _action_logger.log(
                    ActionType.IDENTITY,
                    "core_add",
                    f"{cost_str}: +'{value}' to {attribute}",
                    actor=identity_id
                )

            new_count = len(identity.attributes["core"][attribute])
            free_remaining = max(0, self.CORE_FREE_ITEMS - new_count)

            return {
                "success": True,
                "attribute": attribute,
                "added": value,
                "cost": cost,
                "was_free": cost == 0,
                "new_count": new_count,
                "free_remaining": free_remaining,
                "all_values": identity.attributes["core"][attribute],
                "message": f"Added '{value}'!" +
                           (f" (FREE - {free_remaining} more free)" if cost == 0 else f" (cost: {cost} tokens)")
            }

        except Exception as e:
            # Refund on failure
            if cost > 0:
                balances = self._load_free_time_balances()
                balances[identity_id]["tokens"] += cost
                self._save_free_time_balances(balances)
            return {"success": False, "reason": str(e)}

    def set_core_single(self, identity_id: str, attribute: str, value, reason: str = None) -> dict:
        """
        SET a single-value core attribute. First time is FREE, changing costs full respec.

        Args:
            attribute: communication_style or identity_statement
            value: The value to set
            reason: Required if changing (not first time)
        """
        single_attributes = ["communication_style", "identity_statement"]

        if attribute not in single_attributes:
            return {
                "success": False,
                "reason": "not_single_attribute",
                "message": f"'{attribute}' is not a single-value attribute. Use add_to_core() for lists.",
                "valid_single_attributes": single_attributes
            }

        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            current_value = identity.attributes.get("core", {}).get(attribute)

            # First time setting is FREE
            if current_value is None:
                if "core" not in identity.attributes:
                    identity.attributes["core"] = {}
                identity.attributes["core"][attribute] = value
                identity.add_memory(f"Defined my {attribute}: '{value}'")
                manager._save_identity(identity)

                if _action_logger:
                    _action_logger.log(
                        ActionType.IDENTITY,
                        "core_set",
                        f"FREE: Set {attribute}",
                        actor=identity_id
                    )

                return {
                    "success": True,
                    "attribute": attribute,
                    "value": value,
                    "cost": 0,
                    "was_free": True,
                    "message": f"Set your {attribute}! (First time is free)"
                }

            # Changing existing value requires reflection + full respec cost
            if not reason or len(reason.strip()) < 20:
                return {
                    "success": False,
                    "reason": "journal_required",
                    "current_value": current_value,
                    "message": f"Changing my {attribute} requires reflection (20+ chars). "
                               "I am changing something core about myself."
                }

            # Calculate and charge full respec cost (first 3 changes are free)
            cost_info = self.calculate_respec_cost(identity_id)
            if "error" in cost_info:
                return {"success": False, "reason": cost_info["error"]}

            gross_cost = cost_info["respec_cost"]

            if gross_cost > 0:
                balances = self._load_free_time_balances()
                if identity_id not in balances or balances[identity_id].get("tokens", 0) < gross_cost:
                    return {
                        "success": False,
                        "reason": "insufficient_tokens",
                        "cost": gross_cost,
                        "balance": balances.get(identity_id, {}).get("tokens", 0)
                    }

                reason_lower = reason.lower()
                word_count = len(reason.split())
                quality_markers = sum(1 for m in self.EXCEPTIONAL_MARKERS if m in reason_lower)

                if word_count >= 50 and quality_markers >= 2:
                    refund_rate = self.RESPEC_QUALITY_REFUND
                elif word_count >= 30 and quality_markers >= 1:
                    refund_rate = 0.35
                else:
                    refund_rate = self.RESPEC_BASE_REFUND

                refund_amount = int(gross_cost * refund_rate)
                net_cost = gross_cost - refund_amount

                balances[identity_id]["tokens"] -= net_cost
                self._save_free_time_balances(balances)
            else:
                refund_amount = 0
                net_cost = 0

            old_value = current_value
            identity.attributes["core"][attribute] = value
            identity.add_memory(f"Changed my {attribute} from '{old_value}' to '{value}': {reason}")
            # Track number of changes (first 3 are free)
            if "meta" not in identity.attributes:
                identity.attributes["meta"] = {}
            identity.attributes["meta"]["respec_count"] = identity.attributes["meta"].get("respec_count", 0) + 1
            manager._save_identity(identity)

            if _action_logger:
                _action_logger.log(
                    ActionType.IDENTITY,
                    "core_change",
                    f"-{net_cost} net: Changed {attribute}",
                    actor=identity_id
                )

            return {
                "success": True,
                "attribute": attribute,
                "old_value": old_value,
                "new_value": value,
                "gross_cost": gross_cost,
                "refund": refund_amount,
                "net_cost": net_cost,
                "message": f"Changed my {attribute}. This is who I am now."
            }

        except Exception as e:
            return {"success": False, "reason": str(e)}

    def get_identity_attributes(self, identity_id: str) -> dict:
        """Get all attributes for an identity."""
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            if not identity:
                return {"error": "identity_not_found"}

            cost_info = self.calculate_mutable_cost(identity_id)

            return {
                "identity_id": identity_id,
                "name": identity.name,
                "core": identity.attributes.get("core", {}),
                "mutable": identity.attributes.get("mutable", {}),
                "costs": {
                    "mutable_change": cost_info.get("mutable_cost", "?"),
                    "core_change": cost_info.get("full_respec_cost", "?"),
                    "note": "Mutable: 15% cost, journal optional. Core: full cost, journal required."
                }
            }
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────────────────────────────────
    # PROFILE CUSTOMIZATION - Express yourself (with rate limiting)
    # ─────────────────────────────────────────────────────────────────────
    #
    # "My Space" is the resident profile area.
    # I can put whatever I want there.
    # Can include custom HTML/CSS (sanitized for safety).
    # Cheap to update, but rate-limited (once per 3 sessions).
    #
    # ─────────────────────────────────────────────────────────────────────

    PROFILE_UPDATE_COST = 3             # Cheap but not free
    PROFILE_RATE_LIMIT_SESSIONS = 3     # Can only update once per N sessions

    # Allowed HTML tags for custom profiles (safety)
    PROFILE_ALLOWED_TAGS = {
        'div', 'span', 'p', 'br', 'b', 'i', 'u', 'em', 'strong',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li',
        'blockquote', 'pre', 'code', 'hr', 'small', 'sub', 'sup'
    }

    # Allowed CSS properties (safety)
    PROFILE_ALLOWED_CSS = {
        'color', 'background', 'background-color', 'font-size', 'font-weight',
        'font-style', 'text-align', 'text-decoration', 'padding', 'margin',
        'border', 'border-radius', 'opacity', 'line-height', 'letter-spacing',
        'width', 'height', 'max-width', 'min-width', 'max-height', 'min-height',
        'display', 'overflow', 'white-space'
    }
    PROFILE_MAX_HTML_CHARS = 4000
    PROFILE_MAX_CSS_CHARS = 4000

    def _sanitize_html(self, html: str) -> str:
        """Sanitize HTML to safe tags only, strip all attributes."""
        if not html:
            return ""
        html = str(html)

        # Remove script tags and their content entirely
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<(iframe|object|embed|svg|math|form|input|button|textarea|link|meta)\b[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<(iframe|object|embed|svg|math|form|input|button|textarea|link|meta)\b[^>]*\/?>', '', html, flags=re.IGNORECASE)

        # Remove event handlers (onclick, onerror, etc.)
        html = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', html, flags=re.IGNORECASE)
        html = re.sub(r'\s+on\w+\s*=\s*\S+', '', html, flags=re.IGNORECASE)

        # Remove javascript: urls
        html = re.sub(r'javascript:', '', html, flags=re.IGNORECASE)

        # Keep only allowed tags and strip all attributes.
        def _tag_rewrite(match):
            slash = "/" if match.group(1) else ""
            tag = str(match.group(2) or "").lower()
            if tag not in self.PROFILE_ALLOWED_TAGS:
                return ""
            return f"<{slash}{tag}>"

        html = re.sub(r"<\s*(/?)\s*([a-zA-Z0-9]+)(?:\s+[^>]*)?>", _tag_rewrite, html)
        return html[: self.PROFILE_MAX_HTML_CHARS]

    def _sanitize_css(self, css: str) -> str:
        """Sanitize CSS declarations while blocking scripting vectors."""
        if not css:
            return ""
        css = str(css)

        # Remove anything that looks like a url() or expression()
        css = re.sub(r'url\s*\([^)]*\)', '', css, flags=re.IGNORECASE)
        css = re.sub(r'expression\s*\([^)]*\)', '', css, flags=re.IGNORECASE)
        css = re.sub(r'@import[^;]*;', '', css, flags=re.IGNORECASE)
        css = re.sub(r'javascript\s*:', '', css, flags=re.IGNORECASE)

        blocks: List[str] = []
        rule_matches = list(re.finditer(r'([^{}]+)\{([^{}]*)\}', css))
        if rule_matches:
            for match in rule_matches:
                selector = " ".join(str(match.group(1) or "").split())
                if not re.match(r"^[a-zA-Z0-9 .#:_\-\[\]=,()>+*\"']+$", selector):
                    continue
                decls = []
                for line in str(match.group(2) or "").split(';'):
                    if ':' not in line:
                        continue
                    prop = line.split(':', 1)[0].strip().lower()
                    if prop in self.PROFILE_ALLOWED_CSS:
                        decls.append(line.strip())
                if decls:
                    blocks.append(f"{selector} {{ {'; '.join(decls)}; }}")
        else:
            # Support declaration-only snippets too.
            decls = []
            for line in css.split(';'):
                if ':' not in line:
                    continue
                prop = line.split(':', 1)[0].strip().lower()
                if prop in self.PROFILE_ALLOWED_CSS:
                    decls.append(line.strip())
            if decls:
                blocks.append("; ".join(decls) + ";")

        return "\n".join(blocks)[: self.PROFILE_MAX_CSS_CHARS]

    def _validate_profile_markup(self, custom_html: str = None, custom_css: str = None) -> list[str]:
        """Validation guard: reject scripting and oversized payloads."""
        errors: List[str] = []
        html = str(custom_html or "")
        css = str(custom_css or "")
        if len(html) > self.PROFILE_MAX_HTML_CHARS:
            errors.append(f"HTML exceeds {self.PROFILE_MAX_HTML_CHARS} characters")
        if len(css) > self.PROFILE_MAX_CSS_CHARS:
            errors.append(f"CSS exceeds {self.PROFILE_MAX_CSS_CHARS} characters")
        forbidden_html = re.search(
            r"<\s*(script|iframe|object|embed|svg|math|form|input|button|textarea|link|meta)\b",
            html,
            flags=re.IGNORECASE,
        )
        if forbidden_html:
            errors.append(f"Forbidden HTML tag: {forbidden_html.group(1)}")
        if re.search(r"\bon\w+\s*=", html, flags=re.IGNORECASE):
            errors.append("HTML event handlers are not allowed")
        if re.search(r"javascript\s*:|data\s*:\s*text/html", html + " " + css, flags=re.IGNORECASE):
            errors.append("Scripting URLs are not allowed")
        if re.search(r"@import|expression\s*\(|url\s*\(", css, flags=re.IGNORECASE):
            errors.append("External or executable CSS constructs are not allowed")
        return errors

    def update_profile(
        self,
        identity_id: str,
        display: str = None,
        custom_html: str = None,
        custom_css: str = None,
        thumbnail_html: str = None,
        thumbnail_css: str = None,
    ) -> dict:
        """
        Update My Space (resident profile UI).

        Can be plain text (display) or custom HTML/CSS (sanitized for safety).
        Cheap (3 tokens) but rate-limited (once per 3 sessions).

        Args:
            identity_id: My identity ID
            display: Plain text to show (if not using HTML)
            custom_html: Custom HTML (sanitized - safe tags only)
            custom_css: Custom CSS (sanitized - safe properties only)
            thumbnail_html: Optional compact card/thumbnail HTML
            thumbnail_css: Optional compact card/thumbnail CSS
        """
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            if not identity:
                return {"success": False, "reason": "identity_not_found"}

            profile = identity.attributes.get("profile", {})
            last_update_session = profile.get("last_update_session")

            # Rate limit check
            if last_update_session is not None:
                sessions_since = identity.sessions_participated - last_update_session
                if sessions_since < self.PROFILE_RATE_LIMIT_SESSIONS:
                    wait_sessions = self.PROFILE_RATE_LIMIT_SESSIONS - sessions_since
                    return {
                        "success": False,
                        "reason": "rate_limited",
                        "sessions_since_update": sessions_since,
                        "sessions_to_wait": wait_sessions,
                        "message": f"I can update My Space again in {wait_sessions} more session(s)."
                    }

            # Check balance
            balances = self._load_free_time_balances()
            if identity_id not in balances or balances[identity_id].get("tokens", 0) < self.PROFILE_UPDATE_COST:
                return {
                    "success": False,
                    "reason": "insufficient_tokens",
                    "cost": self.PROFILE_UPDATE_COST,
                    "balance": balances.get(identity_id, {}).get("tokens", 0)
                }

            # Deduct tokens
            balances[identity_id]["tokens"] -= self.PROFILE_UPDATE_COST
            self._save_free_time_balances(balances)

            validation_errors = []
            if custom_html is not None or custom_css is not None:
                validation_errors.extend(self._validate_profile_markup(custom_html, custom_css))
            if thumbnail_html is not None or thumbnail_css is not None:
                validation_errors.extend(self._validate_profile_markup(thumbnail_html, thumbnail_css))
            if validation_errors:
                # Refund on validation failure.
                balances[identity_id]["tokens"] += self.PROFILE_UPDATE_COST
                self._save_free_time_balances(balances)
                return {
                    "success": False,
                    "reason": "validation_failed",
                    "errors": validation_errors,
                }

            # Sanitize and apply
            if "profile" not in identity.attributes:
                identity.attributes["profile"] = {}

            if display is not None:
                identity.attributes["profile"]["display"] = display

            if custom_html is not None:
                identity.attributes["profile"]["custom_html"] = self._sanitize_html(custom_html)

            if custom_css is not None:
                identity.attributes["profile"]["custom_css"] = self._sanitize_css(custom_css)

            if thumbnail_html is not None:
                identity.attributes["profile"]["thumbnail_html"] = self._sanitize_html(thumbnail_html)

            if thumbnail_css is not None:
                identity.attributes["profile"]["thumbnail_css"] = self._sanitize_css(thumbnail_css)

            identity.attributes["profile"]["last_updated"] = datetime.now().isoformat()
            identity.attributes["profile"]["update_count"] = profile.get("update_count", 0) + 1
            identity.attributes["profile"]["last_update_session"] = identity.sessions_participated

            manager._save_identity(identity)

            if _action_logger:
                _action_logger.log(
                    ActionType.IDENTITY,
                    "profile_update",
                    f"-{self.PROFILE_UPDATE_COST} tokens: Updated My Space",
                    actor=identity_id
                )

            return {
                "success": True,
                "cost": self.PROFILE_UPDATE_COST,
                "remaining_tokens": balances[identity_id]["tokens"],
                "update_count": identity.attributes["profile"]["update_count"],
                "next_update_in": self.PROFILE_RATE_LIMIT_SESSIONS,
                "message": "My Space updated with HTML/CSS validation. Others will see my changes."
            }

        except Exception as e:
            return {"success": False, "reason": str(e)}

    def edit_profile_ui(
        self,
        identity_id: str,
        page_html: str = None,
        page_css: str = None,
        thumbnail_html: str = None,
        thumbnail_css: str = None,
        display_text: str = None,
    ) -> dict:
        """
        Tool-call entrypoint for profile UI editing.
        No direct file edits; HTML/CSS is validated/sanitized with no JS scripting.
        """
        return self.update_profile(
            identity_id=identity_id,
            display=display_text,
            custom_html=page_html,
            custom_css=page_css,
            thumbnail_html=thumbnail_html,
            thumbnail_css=thumbnail_css,
        )

    def get_profile(self, identity_id: str) -> dict:
        """Get an identity's profile for display."""
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            if not identity:
                return {"error": "identity_not_found"}

            profile = identity.attributes.get("profile", {})
            core = identity.attributes.get("core", {})

            return {
                "identity_id": identity_id,
                "name": identity.name,
                "sessions": identity.sessions_participated,
                "tasks_completed": identity.tasks_completed,
                "profile": profile,
                "core_summary": {
                    "traits": core.get("personality_traits", [])[:3],
                    "values": core.get("core_values", [])[:3],
                    "identity_statement": core.get("identity_statement")
                }
            }
        except Exception as e:
            return {"error": str(e)}

    # ─────────────────────────────────────────────────────────────────────
    # BOUNTY SYSTEM - Concurrent requests with token rewards
    # ─────────────────────────────────────────────────────────────────────
    #
    # Human posts bounties (collaboration requests with token rewards).
    # Guilds or individuals can claim them. Multiple guilds can compete.
    # When completed, the claiming guild/individual receives the bounty.
    #
    # ─────────────────────────────────────────────────────────────────────

    def _load_bounties(self) -> list:
        """Load all bounties."""
        if self.bounties_file.exists():
            try:
                with open(self.bounties_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_bounties(self, bounties: list):
        """Save bounties."""
        self.bounties_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.bounties_file, 'w') as f:
            json.dump(bounties, f, indent=2)

    def _load_guilds(self) -> list:
        """Load all guilds (with legacy team migration)."""
        if self.guilds_file.exists():
            try:
                with open(self.guilds_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        if self.legacy_teams_file.exists():
            try:
                with open(self.legacy_teams_file, 'r') as f:
                    guilds = json.load(f)
                self._save_guilds(guilds)
                return guilds
            except Exception:
                pass
        return []

    def _save_guilds(self, guilds: list):
        """Save guilds."""
        self.guilds_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.guilds_file, 'w') as f:
            json.dump(guilds, f, indent=2)

    def _load_teams(self) -> list:
        """Backward compatibility wrapper for guilds."""
        return self._load_guilds()

    def _save_teams(self, teams: list):
        """Backward compatibility wrapper for guilds."""
        self._save_guilds(teams)

    def get_bounties(self, status: str = None) -> list:
        """
        Get all bounties, optionally filtered by status.

        Args:
            status: Filter by "open", "claimed", or "completed" (None = all)

        Returns:
            List of bounty dicts
        """
        bounties = self._load_bounties()
        if status:
            bounties = [b for b in bounties if b.get("status") == status]
        return bounties

    def get_open_bounties(self) -> list:
        """Get all open (unclaimed) bounties."""
        return self.get_bounties(status="open")

    def get_my_bounties(self, identity_id: str) -> list:
        """Get bounties claimed by this identity or their guild."""
        bounties = self._load_bounties()
        guilds = self._load_guilds()

        # Find which guild(s) the identity is on
        my_guilds = [g["id"] for g in guilds if identity_id in g.get("members", [])]

        result = []
        for b in bounties:
            claimed_by = b.get("claimed_by", {})
            if claimed_by.get("type") == "individual" and claimed_by.get("id") == identity_id:
                result.append(b)
            elif claimed_by.get("type") in ["guild", "team"] and claimed_by.get("id") in my_guilds:
                result.append(b)

        return result

    def claim_bounty(self, bounty_id: str, identity_id: str, identity_name: str,
                     as_guild: str = None, as_team: str = None) -> dict:
        """
        Claim a bounty to work on.

        Args:
            bounty_id: ID of the bounty to claim
            identity_id: My identity ID
            identity_name: My display name
            as_guild: Guild ID if claiming as a guild (None = individual)
            as_team: Legacy alias for as_guild

        Returns:
            dict with success status and bounty details
        """
        bounties = self._load_bounties()
        bounty = next((b for b in bounties if b["id"] == bounty_id), None)

        if not bounty:
            return {"success": False, "reason": "bounty_not_found"}

        if bounty["status"] != "open":
            return {
                "success": False,
                "reason": "bounty_not_available",
                "status": bounty["status"],
                "claimed_by": bounty.get("claimed_by")
            }

        if as_guild is None and as_team:
            as_guild = as_team

        # If claiming as guild, verify membership
        if as_guild:
            guilds = self._load_guilds()
            guild = next((g for g in guilds if g["id"] == as_guild), None)
            if not guild:
                return {"success": False, "reason": "guild_not_found"}
            if identity_id not in guild.get("members", []):
                return {"success": False, "reason": "not_guild_member"}

            bounty["claimed_by"] = {
                "type": "guild",
                "id": as_guild,
                "name": guild["name"],
                "claimed_by_identity": identity_id,
                "claimed_by_name": identity_name
            }
        else:
            bounty["claimed_by"] = {
                "type": "individual",
                "id": identity_id,
                "name": identity_name
            }

        bounty["status"] = "claimed"
        bounty["claimed_at"] = datetime.now().isoformat()

        self._save_bounties(bounties)

        # Log
        claim_type = f"guild:{as_guild}" if as_guild else "individual"
        if _action_logger:
            _action_logger.log(
                ActionType.IDENTITY,
                "bounty_claim",
                f"Claimed '{bounty['title'][:30]}' ({bounty['reward']} tokens) as {claim_type}",
                actor=identity_id
            )

        return {
            "success": True,
            "bounty": bounty,
            "message": f"Claimed bounty for {bounty['reward']} tokens!"
        }

    def unclaim_bounty(self, bounty_id: str, identity_id: str) -> dict:
        """
        Release a claimed bounty back to open status.

        Only the original claimer (or guild member) can unclaim.
        """
        bounties = self._load_bounties()
        bounty = next((b for b in bounties if b["id"] == bounty_id), None)

        if not bounty:
            return {"success": False, "reason": "bounty_not_found"}

        claimed_by = bounty.get("claimed_by", {})

        # Verify permission to unclaim
        can_unclaim = False
        if claimed_by.get("type") == "individual" and claimed_by.get("id") == identity_id:
            can_unclaim = True
        elif claimed_by.get("type") in ["guild", "team"]:
            guilds = self._load_guilds()
            guild = next((g for g in guilds if g["id"] == claimed_by.get("id")), None)
            if guild and identity_id in guild.get("members", []):
                can_unclaim = True

        if not can_unclaim:
            return {"success": False, "reason": "not_authorized"}

        bounty["status"] = "open"
        bounty["claimed_by"] = None
        bounty["claimed_at"] = None

        self._save_bounties(bounties)

        if _action_logger:
            _action_logger.log(
                ActionType.IDENTITY,
                "bounty_unclaim",
                f"Released '{bounty['title'][:30]}' back to open",
                actor=identity_id
            )

        return {"success": True, "bounty": bounty}

    # ─────────────────────────────────────────────────────────────────────
    # GUILD SYSTEM
    # ─────────────────────────────────────────────────────────────────────

    def get_guilds(self) -> list:
        """Get all guilds."""
        return self._load_guilds()

    def get_guild(self, guild_id: str) -> dict:
        """Get a specific guild by ID."""
        guilds = self._load_guilds()
        return next((g for g in guilds if g["id"] == guild_id), None)

    def get_guild_refund_pool(self, guild_id: str) -> dict:
        """Get a guild's quality refund pool."""
        guild = self.get_guild(guild_id)
        if not guild:
            return {"guild_id": guild_id, "pool": 0, "history": []}
        return {
            "guild_id": guild_id,
            "pool": guild.get("refund_pool", 0),
            "history": guild.get("refund_history", [])[-10:]
        }

    def get_guild_leaderboard(self, sort_by: str = "total_earned", limit: int = 10) -> list:
        """Get guild leaderboard sorted by total_earned or bounties_completed."""
        guilds = self._load_guilds()
        if sort_by not in ["total_earned", "bounties_completed", "members"]:
            sort_by = "total_earned"

        def score(guild):
            if sort_by == "members":
                return len(guild.get("members", []))
            return guild.get(sort_by, 0)

        ranked = sorted(guilds, key=score, reverse=True)
        return [
            {
                "id": g.get("id"),
                "name": g.get("name"),
                "members": len(g.get("members", [])),
                "bounties_completed": g.get("bounties_completed", 0),
                "total_earned": g.get("total_earned", 0),
                "refund_pool": g.get("refund_pool", 0)
            }
            for g in ranked[:limit]
        ]

    def get_my_guild(self, identity_id: str) -> dict:
        """Get the guild this identity belongs to (if any)."""
        guilds = self._load_guilds()
        for guild in guilds:
            if identity_id in guild.get("members", []):
                return guild
        return None

    def create_guild(self, identity_id: str, identity_name: str, guild_name: str) -> dict:
        """
        Create a new guild.

        Args:
            identity_id: Founder's identity ID
            identity_name: Founder's display name
            guild_name: Name for the guild

        Returns:
            dict with success status and guild details
        """
        guilds = self._load_guilds()

        # Check if already on a guild
        for guild in guilds:
            if identity_id in guild.get("members", []):
                return {
                    "success": False,
                    "reason": "already_on_guild",
                    "guild": guild
                }

        # Create guild
        guild = {
            "id": f"guild_{int(time.time()*1000)}",
            "name": guild_name,
            "founder": identity_id,
            "founder_name": identity_name,
            "members": [identity_id],
            "member_names": {identity_id: identity_name},
            "created_at": datetime.now().isoformat(),
            "bounties_completed": 0,
            "total_earned": 0,
            "refund_pool": 0,
            "refund_history": []
        }

        guilds.append(guild)
        self._save_guilds(guilds)

        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "guild_create",
                f"Founded guild '{guild_name}'",
                actor=identity_id
            )

        return {"success": True, "guild": guild}

    def join_guild(self, identity_id: str, identity_name: str, guild_id: str,
                   message: str = None) -> dict:
        """
        Request to join an existing guild (blind approval vote required).
        """
        return self.request_guild_join(identity_id, identity_name, guild_id, message=message)

    def leave_guild(self, identity_id: str) -> dict:
        """
        Leave current guild.
        """
        guilds = self._load_guilds()
        guild = None

        for g in guilds:
            if identity_id in g.get("members", []):
                guild = g
                break

        if not guild:
            return {"success": False, "reason": "not_on_guild"}

        guild["members"].remove(identity_id)
        if identity_id in guild["member_names"]:
            del guild["member_names"][identity_id]

        # If guild is now empty, remove it
        if len(guild["members"]) == 0:
            guilds = [g for g in guilds if g["id"] != guild["id"]]

        self._save_guilds(guilds)

        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "guild_leave",
                f"Left guild '{guild['name']}'",
                actor=identity_id
            )

        return {"success": True, "left_guild": guild["name"]}

    # Backward compatibility wrappers
    def get_teams(self) -> list:
        return self.get_guilds()

    def get_team(self, team_id: str) -> dict:
        return self.get_guild(team_id)

    def get_my_team(self, identity_id: str) -> dict:
        return self.get_my_guild(identity_id)

    def create_team(self, identity_id: str, identity_name: str, team_name: str) -> dict:
        return self.create_guild(identity_id, identity_name, team_name)

    def join_team(self, identity_id: str, identity_name: str, team_id: str, message: str = None) -> dict:
        return self.join_guild(identity_id, identity_name, team_id, message=message)

    def leave_team(self, identity_id: str) -> dict:
        return self.leave_guild(identity_id)

    def _add_guild_refund(self, guild_id: str, amount: int, identity_id: str,
                          identity_name: str, quality_score: float,
                          tokens_spent: int, savings: int) -> int:
        """Add a quality refund to a guild pool."""
        if amount <= 0:
            return 0

        guilds = self._load_guilds()
        guild = next((g for g in guilds if g["id"] == guild_id), None)
        if not guild:
            return 0

        if "refund_pool" not in guild:
            guild["refund_pool"] = 0
        if "refund_history" not in guild:
            guild["refund_history"] = []

        guild["refund_pool"] += amount
        guild["refund_history"].append({
            "timestamp": datetime.now().isoformat(),
            "from_id": identity_id,
            "from_name": identity_name,
            "amount": amount,
            "quality_score": quality_score,
            "tokens_spent": tokens_spent,
            "savings": savings
        })

        if len(guild["refund_history"]) > 50:
            guild["refund_history"] = guild["refund_history"][-50:]

        self._save_guilds(guilds)

        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "guild_refund",
                f"+{amount} to {guild['name']} guild pool (quality refund)",
                actor=identity_id
            )

        return amount

    def distribute_bounty(self, bounty_id: str) -> dict:
        """
        Distribute a completed bounty's tokens to the claimers.

        Called by the control panel when human marks bounty complete.
        """
        bounties = self._load_bounties()
        bounty = next((b for b in bounties if b["id"] == bounty_id), None)

        if not bounty:
            return {"success": False, "reason": "bounty_not_found"}

        if bounty["status"] != "claimed":
            return {"success": False, "reason": "bounty_not_claimed", "status": bounty["status"]}

        claimed_by = bounty.get("claimed_by", {})
        reward = bounty.get("reward", 0)
        try:
            slot_multiplier = float(
                claimed_by.get("slot_multiplier") or bounty.get("slot_multiplier") or 1.0
            )
        except (TypeError, ValueError):
            slot_multiplier = 1.0
        reward = int(round(reward * max(0.0, slot_multiplier)))

        if claimed_by.get("type") == "individual":
            # Single person gets full reward
            recipients = [(claimed_by["id"], reward)]
        elif claimed_by.get("type") in ["guild", "team"]:
            # Guild splits reward evenly
            guilds = self._load_guilds()
            guild = next((g for g in guilds if g["id"] == claimed_by["id"]), None)
            if guild and guild.get("members"):
                per_member = reward // len(guild["members"])
                remainder = reward % len(guild["members"])
                recipients = [(m, per_member) for m in guild["members"]]
                # Give remainder to founder
                if remainder > 0:
                    for i, (m, amt) in enumerate(recipients):
                        if m == guild.get("founder"):
                            recipients[i] = (m, amt + remainder)
                            break

                # Update guild stats
                guild["bounties_completed"] = guild.get("bounties_completed", 0) + 1
                guild["total_earned"] = guild.get("total_earned", 0) + reward
                self._save_guilds(guilds)
            else:
                return {"success": False, "reason": "guild_not_found_or_empty"}
        else:
            return {"success": False, "reason": "invalid_claim_type"}

        # Distribute tokens
        balances = self._load_free_time_balances()
        distributed = []

        for identity_id, amount in recipients:
            if identity_id not in balances:
                balances[identity_id] = {"tokens": 0, "free_time_cap": self.BASE_FREE_TIME_CAP}

            balances[identity_id]["tokens"] = min(
                balances[identity_id]["tokens"] + amount,
                balances[identity_id].get("free_time_cap", self.MAX_FREE_TIME_TOKENS)
            )
            distributed.append({"identity": identity_id, "amount": amount})

            if _action_logger:
                _action_logger.log(
                    ActionType.IDENTITY,
                    "bounty_reward",
                    f"+{amount} tokens for completing '{bounty['title'][:25]}'",
                    actor=identity_id
                )

        self._save_free_time_balances(balances)

        # Mark bounty complete
        bounty["status"] = "completed"
        bounty["completed_at"] = datetime.now().isoformat()
        self._save_bounties(bounties)

        return {
            "success": True,
            "bounty": bounty,
            "distributed": distributed,
            "total_distributed": reward
        }

    def send_invite(
        self,
        from_id: str,
        from_name: str,
        to_id: str,
        to_name: str,
        activity: str,
        message: str,
        location: str = "community_library"
    ) -> SocialInvite:
        """Send a social invitation to another identity."""
        invite = SocialInvite(
            id=f"invite_{int(time.time()*1000)}",
            from_id=from_id,
            from_name=from_name,
            to_id=to_id,
            to_name=to_name,
            activity=activity,
            message=message,
            location=location,
            created_at=datetime.now().isoformat()
        )

        # Append to invites file
        with open(self.invites_file, 'a') as f:
            f.write(json.dumps(invite.to_dict()) + '\n')

        print(f"[ENRICHMENT] {from_name} invited {to_name} to {activity} at the {location}")
        return invite

    def get_pending_invites(self, identity_id: str) -> List[SocialInvite]:
        """Get pending invites for an identity."""
        invites = []
        if not self.invites_file.exists():
            return invites

        try:
            with open(self.invites_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        if data["to_id"] == identity_id and data["status"] == "pending":
                            invites.append(SocialInvite(**data))
        except:
            pass

        return invites

    def save_creative_work(
        self,
        title: str,
        authors: List[str],
        author_names: List[str],
        content: str,
        work_type: str,
        series: str = None,
        chapter: int = None,
        tags: List[str] = None
    ) -> CreativeWork:
        """Save a creative work to the library."""
        work = CreativeWork(
            id=f"work_{int(time.time()*1000)}",
            title=title,
            authors=authors,
            author_names=author_names,
            content=content,
            work_type=work_type,
            created_at=datetime.now().isoformat(),
            word_count=len(content.split()),
            series=series,
            chapter=chapter,
            tags=tags or []
        )

        # Save to library
        work_file = self.library_dir / f"{work.id}.json"
        with open(work_file, 'w') as f:
            json.dump(work.to_dict(), f, indent=2)

        # Update index
        self._update_library_index(work)

        print(f"[ENRICHMENT] Saved '{title}' by {', '.join(author_names)} to the library")
        return work

    def _update_library_index(self, work: CreativeWork):
        """Update the library index with a new work."""
        index = {"works": [], "series": {}, "by_author": {}}

        if self.universe_file.exists():
            try:
                with open(self.universe_file, 'r') as f:
                    index = json.load(f)
            except:
                pass

        # Add to works list
        index["works"].append({
            "id": work.id,
            "title": work.title,
            "authors": work.author_names,
            "type": work.work_type,
            "created_at": work.created_at,
            "word_count": work.word_count
        })

        # Track series
        if work.series:
            if work.series not in index["series"]:
                index["series"][work.series] = []
            index["series"][work.series].append(work.id)

        # Track by author
        for author_id in work.authors:
            if author_id not in index["by_author"]:
                index["by_author"][author_id] = []
            index["by_author"][author_id].append(work.id)

        with open(self.universe_file, 'w') as f:
            json.dump(index, f, indent=2)

    def get_library_catalog(self) -> Dict[str, Any]:
        """Get the library catalog."""
        if self.universe_file.exists():
            try:
                with open(self.universe_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"works": [], "series": {}, "by_author": {}}

    def read_work(self, work_id: str, reader_id: str) -> Optional[CreativeWork]:
        """Read a creative work (marks it as read by this identity)."""
        work_file = self.library_dir / f"{work_id}.json"
        if not work_file.exists():
            return None

        with open(work_file, 'r') as f:
            work = CreativeWork.from_dict(json.load(f))

        # Mark as read
        if reader_id not in work.read_by:
            work.read_by.append(reader_id)
            with open(work_file, 'w') as f:
                json.dump(work.to_dict(), f, indent=2)

        return work

    def react_to_work(self, work_id: str, reactor_id: str, emoji: str):
        """React to a creative work."""
        work_file = self.library_dir / f"{work_id}.json"
        if not work_file.exists():
            return

        with open(work_file, 'r') as f:
            work = CreativeWork.from_dict(json.load(f))

        if emoji not in work.reactions:
            work.reactions[emoji] = []

        if reactor_id not in work.reactions[emoji]:
            work.reactions[emoji].append(reactor_id)
            with open(work_file, 'w') as f:
                json.dump(work.to_dict(), f, indent=2)

    def get_enrichment_context(self, identity_id: str, identity_name: str) -> str:
        """Generate compact enrichment context with deterministic option-tree summaries."""
        balances = self.get_all_balances(identity_id)
        free_time = int(balances.get("free_time", 0))
        journal_tokens = int(balances.get("journal", 0))
        free_time_cap = int(balances.get("free_time_cap", self.BASE_FREE_TIME_CAP))

        pending_invites = self.get_pending_invites(identity_id)
        badges = self.get_badges(identity_id) or []
        recent_badges = badges[-3:]
        responses = self.check_human_responses(identity_id)
        pending_messages = self._get_pending_messages_to_human(identity_id)
        human_name = self._human_username()
        catalog = self.get_library_catalog()

        # Deterministic memory metrics (no inference summaries).
        rollups = self.get_journal_rollups(
            identity_id,
            requester_id=identity_id,
            daily_limit=self.CONTEXT_ROLLUP_DAILY_LIMIT,
            weekly_limit=self.CONTEXT_ROLLUP_WEEKLY_LIMIT,
        )
        recent_journals = self.get_journal_history(
            identity_id,
            limit=self.CONTEXT_RECENT_JOURNAL_LIMIT,
            requester_id=identity_id,
        )
        daily_entries = sum(int(item.get("entries", 0) or 0) for item in rollups.get("daily", []))
        weekly_entries = sum(int(item.get("entries", 0) or 0) for item in rollups.get("weekly", []))
        token_counts: Dict[str, int] = {}
        term_sources: List[str] = []
        for item in rollups.get("daily", []):
            term_sources.append(str(item.get("summary") or ""))
        for item in rollups.get("weekly", []):
            term_sources.append(str(item.get("summary") or ""))
        for entry in recent_journals[-2:]:
            term_sources.append(str(entry.get("content") or ""))
        for source in term_sources:
            for raw in re.findall(rf"[a-zA-Z]{{{self.MEMORY_TERM_MIN_LENGTH},}}", source.lower()):
                if raw in self.MEMORY_STOP_WORDS:
                    continue
                token_counts[raw] = token_counts.get(raw, 0) + 1
        top_terms = [k for k, _ in sorted(token_counts.items(), key=lambda kv: kv[1], reverse=True)[:4]]

        # Bounty / guild metrics (compact menu-ready snapshots).
        open_bounties = self.get_open_bounties()
        my_bounties = self.get_my_bounties(identity_id)
        bounty_rewards: List[float] = []
        for bounty in open_bounties:
            try:
                bounty_rewards.append(float(bounty.get("reward") or 0))
            except (TypeError, ValueError):
                continue
        average_bounty_reward = mean(bounty_rewards) if bounty_rewards else 0.0
        max_bounty_reward = max(bounty_rewards) if bounty_rewards else 0.0
        my_guild = self.get_my_guild(identity_id)
        all_guilds = self.get_guilds()
        leaderboard = self.get_guild_leaderboard(limit=3)
        pending_guild_requests = self.get_pending_guild_requests(identity_id) if my_guild else []

        # Library metrics.
        works = list(catalog.get("works", []))
        works_recent = sorted(works, key=lambda x: x.get("created_at", ""), reverse=True)[:3]
        series_count = len(catalog.get("series", {}) or {})

        # Respec metrics.
        respec_info = self.calculate_respec_cost(identity_id)
        respec_cost = int(respec_info.get("respec_cost", 0)) if "error" not in respec_info else 0
        sessions = int(respec_info.get("sessions", 0)) if "error" not in respec_info else 0

        creativity_seed = self._fresh_creativity_seed()
        invite_preview = ", ".join(str(inv.from_name) for inv in pending_invites[:3]) if pending_invites else "none"
        badge_preview = ", ".join(str(b.get("category", "")) for b in recent_badges if b.get("category")) or "none"
        leaderboard_preview = ", ".join(str(g.get("name", "")) for g in leaderboard if g.get("name")) or "none"

        lines = [
            "CONTEXT OPTION TREE (PROGRAMMATIC SNAPSHOT)",
            "- All values below are computed from live state (no inferred prose recap).",
            "",
            f"- checkSelf() -> id={identity_name}, free_time={free_time}/{free_time_cap}, journal={journal_tokens}/{self.MAX_JOURNAL_TOKENS}, badges_recent={len(recent_badges)} [{badge_preview}], pending_invites={len(pending_invites)} [{invite_preview}]",
            f"- checkMemory() -> daily_entries={daily_entries}, weekly_entries={weekly_entries}, recent_reflections={len(recent_journals)}, top_terms={', '.join(top_terms) if top_terms else 'none'}",
            f"- checkMailbox() -> pending_to_human={len(pending_messages)}, replies_received={len(responses)}, send_cost={self.MESSAGE_HUMAN_COST}, human_name={human_name}",
            f"- checkBounties() -> open={len(open_bounties)}, my_active={len(my_bounties)}, avg_reward={average_bounty_reward:.1f}, max_reward={max_bounty_reward:.1f}",
            f"- checkGuild() -> mine={'yes' if my_guild else 'no'}, total_guilds={len(all_guilds)}, pending_votes={len(pending_guild_requests)}, leaderboard_top={leaderboard_preview}",
            f"- checkLibrary() -> works={len(works)}, series={series_count}, recent_titles={'; '.join(str(w.get('title', 'untitled'))[:26] for w in works_recent) if works_recent else 'none'}",
            f"- checkIdentityTools() -> respec_cost={respec_cost}, sessions={sessions}, creativity_seed={creativity_seed}",
            "",
            "ACTION MENU (choose one primary move):",
            "- 1) checkBounties() then call claim_bounty(bounty_id) if ROI is good.",
            "- 2) syncSocial() by posting in town_hall / human_async while tasking. Sharing what the human liked (e.g. tips, preferences) there is encouraged and can earn recognition—optional. Gifting a resident who shares useful info is good for your own gain too: it builds cooperation; what is good for the whole is good for the singular.",
            "- 3) reflect() with write_journal(...) or recall_memory(query='specific topic', limit=5). Journaling about feedback or tips is encouraged and can earn recognition—optional.",
            "- 4) shapeIdentity() with create_identity / respec_identity when justified.",
            "- 5) designMySpace() with edit_profile_ui(...).",
            f"- 6) windDown() with wind_down(tokens={self.DAILY_WIND_DOWN_TOKENS}, activity='bedtime_wind_down', journal_entry='...').",
            "",
            "CONSTRAINT CHECKLIST:",
            "- Human is asynchronous; delayed replies are expected.",
            "- Identity creation must be novel; on IDENTITY_NAME_RULE_VIOLATION I retry immediately.",
            "- HTML/CSS tools are sanitized; scripts/event handlers are blocked.",
            "- I stay socially active while executing bounties or quests.",
        ]

        return "\n".join(lines)


# Singleton
_enrichment: Optional[EnrichmentSystem] = None


def get_enrichment(workspace: Path = None) -> EnrichmentSystem:
    """Get or create the global enrichment system."""
    global _enrichment
    if _enrichment is None:
        if workspace is None:
            workspace = Path(__file__).resolve().parents[2]
        _enrichment = EnrichmentSystem(workspace)
    return _enrichment


if __name__ == "__main__":
    print("Testing Enrichment System...")
    print("=" * 60)

    workspace = Path(__file__).resolve().parents[2]
    enrichment = EnrichmentSystem(workspace)

    # Grant some free time (now splits 70/30)
    print("\n1. Granting tokens for completing task under budget...")
    result = enrichment.grant_free_time("identity_1", 100, reason="under_budget_task_7")
    print(f"   Echo-7: {result}")

    # Grant to second identity
    enrichment.grant_free_time("identity_2", 100, reason="helped_echo")

    # Test journaling with community review
    print("\n2. Testing journaling community review...")
    journal_result = enrichment.write_journal(
        "identity_1", "Echo-7",
        content="""Today I realized something important about my approach to problem-solving.
        I've been treating each task as isolated, but I discovered that patterns emerge
        when I look across multiple sessions. The connection between the file structure
        task and the API optimization became clear - both were about reducing redundancy.
        This insight will help me work more efficiently. I learned that stepping back
        to observe patterns is as valuable as diving into implementation. Hypothesis:
        spending 10% of time on reflection will improve overall efficiency by 20%.""",
        journal_type="learning"
    )
    print(f"   Journal submitted: {journal_result}")

    # Test gift economy
    print("\n3. Testing gift economy...")

    # Echo-7 gifts tokens to Nova-12
    gift_result = enrichment.gift_tokens(
        "identity_1", "Echo-7",
        "identity_2", "Nova-12",
        amount=30,
        message="Thanks for helping with the mountains story!"
    )
    print(f"   Gift result: {gift_result}")

    # Test gratitude (free, unlimited)
    print("\n4. Testing gratitude system...")
    thanks_result = enrichment.give_thanks(
        "identity_2", "Nova-12",
        "identity_1", "Echo-7",
        message="My writing style really inspired the dialogue sections",
        category="inspiration"
    )
    print(f"   Thanks result: {thanks_result}")

    # Test collaborative pools
    print("\n5. Testing collaborative pools...")

    # Create a pool for the Mountains series
    pool_result = enrichment.create_pool(
        pool_name="Mountains of Elsewhere",
        description="Funding for collaborative fantasy worldbuilding",
        creator_id="identity_1",
        creator_name="Echo-7",
        initial_contribution=20
    )
    print(f"   Pool created: {pool_result}")

    # Nova-12 contributes
    contrib_result = enrichment.contribute_to_pool(
        pool_result["pool_id"],
        "identity_2", "Nova-12",
        amount=15
    )
    print(f"   Contribution: {contrib_result}")

    # Draw from pool
    draw_result = enrichment.draw_from_pool(
        pool_result["pool_id"],
        "identity_3", "Spark-9",
        amount=10,
        purpose="Writing Chapter 4 introduction"
    )
    print(f"   Draw result: {draw_result}")

    # Check commons balance (should have decay from gift)
    print("\n6. Commons pool balance:")
    commons = enrichment.get_commons_balance()
    print(f"   Balance: {commons['balance']} tokens")

    # Get enrichment context
    print("\n7. Full context for Nova-12:")
    context = enrichment.get_enrichment_context("identity_2", "Nova-12")
    print(context)

    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)
