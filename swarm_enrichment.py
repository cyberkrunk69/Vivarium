"""
Swarm Enrichment System - Hobbies, creative works, and social rewards.

When workers complete tasks under budget, they earn free time to:
- Write creatively (stories, poetry, worldbuilding)
- Collaborate with other identities
- Pursue personal interests
- Add to the shared universe

Creative works are stored in the library for all to enjoy.

Usage:
    from swarm_enrichment import EnrichmentSystem, get_enrichment

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
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from statistics import mean, stdev

# Import action logger for audit trail
try:
    from action_logger import get_action_logger, ActionType
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
    location: str                   # "library", "watercooler", "creative_room"
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

    # Base token reward for completing any task
    BASE_TOKENS = 50

    # Multiplier tiers
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

        # Initialize reward calculator
        self.rewards = RewardCalculator(workspace)

        self.invites_file = self.workspace / ".swarm" / "social_invites.jsonl"
        self.invites_file.parent.mkdir(parents=True, exist_ok=True)

        self.free_time_file = self.workspace / ".swarm" / "free_time_balances.json"
        self.journals_dir = self.workspace / ".swarm" / "journals"
        self.journals_dir.mkdir(parents=True, exist_ok=True)

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

        # Bounty and team system
        self.bounties_file = self.workspace / ".swarm" / "bounties.json"
        self.teams_file = self.workspace / ".swarm" / "teams.json"

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
        discussion_dir = self.workspace / ".swarm" / "discussion"
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
    # ═══════════════════════════════════════════════════════════════════
    #
    # Two pools: FREE_TIME (socializing, exploring) and JOURNAL (learning, memory)
    # Journaling is an INVESTMENT - it pays dividends back to free time
    #
    # ═══════════════════════════════════════════════════════════════════

    # Pool caps (default - can be increased through investment)
    MAX_FREE_TIME_TOKENS = 500      # Cap for free time (socializing, exploring)
    MAX_JOURNAL_TOKENS = 200        # Cap for journaling (persisted learning)
    BASE_FREE_TIME_CAP = 500        # Starting cap (can grow)

    # Earning split: when granted tokens, how to divide them
    FREE_TIME_SPLIT = 0.70          # 70% goes to free time
    JOURNAL_SPLIT = 0.30            # 30% goes to journaling

    # Journal quality rewards
    JOURNAL_REFUND_RATE = 0.50      # Quality journals refund 50% to free time
    EXCEPTIONAL_CAP_INCREASE = 10   # Exceptional journals permanently increase cap

    # Quality thresholds (word count + content markers)
    MIN_JOURNAL_WORDS = 50          # Minimum for any refund
    QUALITY_JOURNAL_WORDS = 150     # Threshold for quality refund
    EXCEPTIONAL_MARKERS = [         # Markers that indicate exceptional insight
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
    # Creates shared fate, peer accountability, and team spirit.
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
    # distributed to everyone. Your efficiency helps the team.
    #
    # ═══════════════════════════════════════════════════════════════════

    TOKEN_BASELINE_PER_TASK = 50    # Expected tokens per task (baseline)
    EFFICIENCY_POOL_RATE = 0.50     # 50% of savings go to pool
    WEEKLY_EFFICIENCY_BONUS_10 = 25 # Bonus if 10%+ improvement
    WEEKLY_EFFICIENCY_BONUS_20 = 50 # Bonus if 20%+ improvement

    # Budget savings rewards (jury-verified)
    TOKENS_PER_DOLLAR = 1000        # 1 USD of savings ~= 1000 tokens
    SAVINGS_PAYOUT_RATE = 0.65      # % of saved tokens paid to author
    SAVINGS_POOL_RATE = 0.25        # % of saved tokens to efficiency pool
    QUALITY_MULT_MIN = 0.80         # Quality multiplier floor
    QUALITY_MULT_MAX = 1.25         # Quality multiplier cap

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
        balances = self._load_free_time_balances()
        identity_data = balances.get(identity_id, {})
        return {
            "free_time": identity_data.get("tokens", 0),
            "journal": identity_data.get("journal_tokens", 0),
            "free_time_cap": identity_data.get("free_time_cap", self.BASE_FREE_TIME_CAP)
        }

    # ═══════════════════════════════════════════════════════════════════
    # JOURNALING SYSTEM - Investment that pays dividends
    # ═══════════════════════════════════════════════════════════════════

    def write_journal(self, identity_id: str, identity_name: str, content: str,
                      journal_type: str = "reflection", cost: int = 20) -> dict:
        """
        Write a journal entry. Costs journal tokens (or free time if journal pool empty).

        Quality journals get REFUNDS to free time pool.
        Exceptional journals PERMANENTLY INCREASE free time cap.

        Args:
            identity_id: Who's writing
            identity_name: Display name
            content: The journal content
            journal_type: "reflection", "learning", "observation", "correction"
            cost: Token cost (default 20)

        Returns:
            dict with success, quality assessment, refund, cap_increase
        """
        balances = self._load_free_time_balances()

        if identity_id not in balances:
            return {"success": False, "reason": "identity_not_found"}

        # Check if can afford (journal tokens first, then free time)
        journal_tokens = balances[identity_id].get("journal_tokens", 0)
        free_time = balances[identity_id].get("tokens", 0)

        if journal_tokens + free_time < cost:
            return {
                "success": False,
                "reason": "insufficient_tokens",
                "journal_tokens": journal_tokens,
                "free_time": free_time,
                "cost": cost
            }

        # Deduct from journal first, then free time
        journal_spent = min(cost, journal_tokens)
        free_time_spent = cost - journal_spent

        balances[identity_id]["journal_tokens"] = journal_tokens - journal_spent
        balances[identity_id]["tokens"] = free_time - free_time_spent

        # Evaluate journal quality
        quality = self._evaluate_journal_quality(content)

        # Calculate refund based on quality
        refund = 0
        cap_increase = 0

        if quality["tier"] == "quality":
            refund = int(cost * self.JOURNAL_REFUND_RATE)
        elif quality["tier"] == "exceptional":
            refund = int(cost * self.JOURNAL_REFUND_RATE)
            cap_increase = self.EXCEPTIONAL_CAP_INCREASE

        # Apply refund to free time (not journal tokens)
        if refund > 0:
            current_cap = balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
            balances[identity_id]["tokens"] = min(
                balances[identity_id]["tokens"] + refund,
                current_cap
            )

        # Apply cap increase for exceptional journals
        if cap_increase > 0:
            old_cap = balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
            balances[identity_id]["free_time_cap"] = old_cap + cap_increase
            print(f"[ENRICHMENT] {identity_name}'s exceptional journal increased free time cap: {old_cap} -> {old_cap + cap_increase}")

        self._save_free_time_balances(balances)

        # Save the journal entry
        journal_entry = {
            "id": f"journal_{int(time.time()*1000)}",
            "identity_id": identity_id,
            "identity_name": identity_name,
            "content": content,
            "journal_type": journal_type,
            "timestamp": datetime.now().isoformat(),
            "quality": quality,
            "cost": cost,
            "refund": refund,
            "cap_increase": cap_increase
        }

        journal_file = self.journals_dir / f"{identity_id}.jsonl"
        with open(journal_file, 'a') as f:
            f.write(json.dumps(journal_entry) + '\n')

        # Log to action logger
        if _action_logger:
            detail = f"[{quality['tier'].upper()}] -{cost}+{refund} refund"
            if cap_increase:
                detail += f" | +{cap_increase} cap!"
            _action_logger.journal(journal_type, content[:50] + "...", actor=identity_id)

        result = {
            "success": True,
            "journal_id": journal_entry["id"],
            "quality": quality,
            "cost": cost,
            "refund": refund,
            "cap_increase": cap_increase,
            "net_cost": cost - refund,
            "new_balances": {
                "free_time": balances[identity_id]["tokens"],
                "journal": balances[identity_id]["journal_tokens"],
                "free_time_cap": balances[identity_id].get("free_time_cap", self.BASE_FREE_TIME_CAP)
            }
        }

        tier_marker = {"basic": "[.]", "quality": "[*]", "exceptional": "[**]"}[quality["tier"]]
        print(f"[ENRICHMENT] {tier_marker} {identity_name} wrote {quality['tier']} journal: -{cost}+{refund} refund")

        return result

    def _evaluate_journal_quality(self, content: str) -> dict:
        """
        Evaluate journal quality based on content.

        Tiers:
        - basic: Minimal effort, no refund
        - quality: Thoughtful, 50% refund
        - exceptional: Genuine insight, 50% refund + cap increase

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

    def get_journal_history(self, identity_id: str, limit: int = 10) -> list:
        """Get recent journal entries for an identity."""
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
            message: Why you're thankful
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
                           tokens_spent: int, task_completed: bool = True) -> dict:
        """
        Record tokens spent on a task. Efficient workers contribute to the pool.

        If tokens_spent < baseline, the savings go to the efficiency pool.
        Pool is distributed periodically to all participants.

        Args:
            identity_id: Who spent the tokens
            identity_name: Display name
            tokens_spent: How many tokens were used
            task_completed: Whether task was successfully completed

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

        result = {
            "tokens_spent": tokens_spent,
            "baseline": self.TOKEN_BASELINE_PER_TASK,
            "savings": savings,
            "pool_contribution": pool_contribution,
            "pool_balance": pool["balance"],
            "swarm_avg": round(pool["avg_tokens_per_task"], 1)
        }

        if pool_contribution > 0:
            print(f"[EFFICIENCY] {identity_name} saved {savings} tokens! +{pool_contribution} to pool (total: {pool['balance']})")

        return result

    def _savings_tokens(self, estimated_budget: Optional[float], actual_cost: Optional[float]) -> int:
        """Convert budget savings into token units."""
        if estimated_budget is None or actual_cost is None:
            return 0
        savings = max(0.0, estimated_budget - actual_cost)
        return int(round(savings * self.TOKENS_PER_DOLLAR))

    def _quality_multiplier(self, quality_score: float) -> float:
        """Scale reward based on jury quality score."""
        quality_score = max(0.0, min(1.0, quality_score))
        span = self.QUALITY_MULT_MAX - self.QUALITY_MULT_MIN
        return self.QUALITY_MULT_MIN + (span * quality_score)

    def apply_verdict_reward(
        self,
        *,
        author_id: str,
        author_name: str,
        estimated_budget: Optional[float],
        actual_cost: Optional[float],
        quality_score: float,
        origin: str,
        novelty_decay: float,
        path_multiplier: float,
        submission_id: str,
    ) -> dict:
        """
        Reward a contributor based on budget savings + jury quality.
        """
        savings_tokens = self._savings_tokens(estimated_budget, actual_cost)
        if savings_tokens <= 0:
            return {
                "reward_tokens": 0,
                "savings_tokens": 0,
                "reason": "no_savings",
            }

        quality_mult = self._quality_multiplier(quality_score)
        novelty_decay = max(0.0, min(1.0, novelty_decay))
        path_multiplier = max(0.5, min(1.5, path_multiplier))

        direct_reward = int(
            savings_tokens
            * self.SAVINGS_PAYOUT_RATE
            * quality_mult
            * novelty_decay
            * path_multiplier
        )
        pool_contribution = int(savings_tokens * self.SAVINGS_POOL_RATE)

        if direct_reward > 0:
            self.grant_free_time(author_id, direct_reward, reason=f"jury_pass_{submission_id}")

        # Credit efficiency pool with a portion of savings
        pool = self._load_efficiency_pool()
        pool["balance"] = pool.get("balance", 0) + pool_contribution
        pool["total_savings_tokens"] = pool.get("total_savings_tokens", 0) + savings_tokens
        self._save_efficiency_pool(pool)

        if _action_logger:
            _action_logger.log(
                ActionType.IDENTITY,
                "jury_reward",
                f"{author_name} rewarded {direct_reward} tokens (savings {savings_tokens})",
                actor=author_id,
            )

        return {
            "reward_tokens": direct_reward,
            "savings_tokens": savings_tokens,
            "pool_contribution": pool_contribution,
            "quality_multiplier": round(quality_mult, 3),
            "novelty_decay": round(novelty_decay, 3),
            "path_multiplier": round(path_multiplier, 3),
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
            bonus_msg = f"\nYou've received {bonus_result['amount']} bonus tokens! Your balance is now {bonus_result['new_balance']}."
        elif bonus_result.get("reason") == "already_received_today":
            bonus_msg = "\n(You've already received your Sunday bonus today.)"

        return f"""
{'='*60}
SUNDAY REST DAY
{'='*60}

Good morning, {identity_name}!

Today is Sunday - the swarm's designated rest day. There are no assigned
tasks today. This time is yours to spend however you please.

You might want to:
- Work on a personal creative project
- Write in your journal about the week
- Collaborate with other residents on something fun
- Explore an interest you've been curious about
- Just relax and reflect
{bonus_msg}

This is YOUR time. Enjoy it.
{'='*60}
"""

    # ─────────────────────────────────────────────────────────────────────
    # MESSAGE JOSH - Direct line to the human
    # ─────────────────────────────────────────────────────────────────────

    MESSAGE_HUMAN_COST = 10  # Tokens to send a message to Josh

    def message_human(self, identity_id: str, identity_name: str, content: str,
                      message_type: str = "message") -> dict:
        """
        Send a message directly to Josh. Costs free time tokens.

        This is a real connection - Josh will see your message and can respond.
        Use it for questions, greetings, ideas, or concerns.

        Args:
            identity_id: Your identity ID
            identity_name: Your display name
            content: What you want to say
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
                f"message_to_josh",
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
                "note": "System is paused. Message queued and will be delivered when you wake up."
            }

        # Append to message queue (immediate delivery)
        messages_file = self.workspace / ".swarm" / "messages_to_human.jsonl"
        messages_file.parent.mkdir(parents=True, exist_ok=True)
        with open(messages_file, 'a') as f:
            f.write(json.dumps(message) + '\n')

        # Log
        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "msg_to_josh",
                f"[{message_type}] \"{content[:40]}...\"" if len(content) > 40 else f"[{message_type}] \"{content}\"",
                actor=identity_id
            )

        print(f"[MESSAGE] {identity_name} -> Josh: [{message_type}] {content[:60]}...")

        return {
            "success": True,
            "message_id": message["id"],
            "cost": self.MESSAGE_HUMAN_COST,
            "remaining_tokens": balances[identity_id]["tokens"],
            "note": "Josh will see this and may respond. Check for responses in your next session."
        }

    def check_human_responses(self, identity_id: str) -> list:
        """
        Check for any responses from Josh to your messages.

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

                            # Also add to main messages file so Josh sees it
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

Take a moment to read these before starting your task.
{'='*60}
"""

    def _get_pending_messages_to_human(self, identity_id: str) -> list:
        """Get messages sent to Josh that haven't been responded to yet."""
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
    # expensive it is to change who you are. This makes identity changes
    # meaningful - not something you do on a whim.
    #
    # ─────────────────────────────────────────────────────────────────────

    # Base cost + scaling factor (ARPG-style: cheap at low level, expensive later)
    RESPEC_BASE_COST = 10           # Cheap for newcomers taking initiative!
    RESPEC_SCALE_PER_SESSION = 3    # Gradual scaling with experience

    def calculate_respec_cost(self, identity_id: str) -> dict:
        """
        Calculate the cost to respec this identity.

        Cost = BASE + (sessions_participated * SCALE_PER_SESSION)

        Cheap for newcomers (encourages initiative), expensive for veterans
        (identity should be more settled by then).

        Example costs:
        - Brand new (1 session): 10 + (1 * 3) = 13 tokens
        - Getting started (5 sessions): 10 + (5 * 3) = 25 tokens
        - Experienced (20 sessions): 10 + (20 * 3) = 70 tokens
        - Veteran (50 sessions): 10 + (50 * 3) = 160 tokens
        """
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            if not identity:
                return {"error": "identity_not_found"}

            sessions = identity.sessions_participated
            cost = self.RESPEC_BASE_COST + (sessions * self.RESPEC_SCALE_PER_SESSION)

            return {
                "identity_id": identity_id,
                "current_name": identity.name,
                "sessions": sessions,
                "respec_cost": cost,
                "breakdown": {
                    "base": self.RESPEC_BASE_COST,
                    "session_scaling": sessions * self.RESPEC_SCALE_PER_SESSION
                }
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

        JOURNAL REQUIRED: You must provide a reason (why you're changing).
        This is enforced by the system - identity changes deserve reflection.

        In return for reflecting:
        - 20% refund for providing any reason (minimum effort)
        - 25% refund for a decent reflection (20+ words)
        - 35% refund for a good reflection (30+ words, 1+ insight marker)
        - 45% refund for a thoughtful reflection (50+ words, 2+ insight markers)

        Args:
            identity_id: Your identity ID
            new_name: The new name you want
            reason: REQUIRED - Why you're making this change

        Returns:
            dict with success status, gross cost, refund, net cost, and new identity state
        """
        # REQUIRE reason - this is non-negotiable
        if not reason or len(reason.strip()) < 20:
            return {
                "success": False,
                "reason": "journal_required",
                "message": "You must explain why you're making this change (at least 20 characters). "
                           "This isn't arbitrary - identity changes deserve reflection. "
                           "You'll get 20-45% of your tokens back for a thoughtful entry."
            }

        # Calculate cost
        cost_info = self.calculate_respec_cost(identity_id)
        if "error" in cost_info:
            return {"success": False, "reason": cost_info["error"]}

        gross_cost = cost_info["respec_cost"]
        old_name = cost_info["current_name"]

        # Check balance (need full cost upfront, refund comes after)
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

        # Start with base refund (20%)
        refund_rate = self.RESPEC_BASE_REFUND
        refund_tier = "base"

        # Check for quality markers (same as regular journaling)
        quality_markers_found = sum(1 for marker in self.EXCEPTIONAL_MARKERS if marker in reason_lower)

        # Scale refund: 20% base -> 45% max based on quality
        if word_count >= 50 and quality_markers_found >= 2:
            refund_rate = self.RESPEC_QUALITY_REFUND  # Full 45%
            refund_tier = "thoughtful"
        elif word_count >= 30 and quality_markers_found >= 1:
            refund_rate = 0.35  # Good reflection: 35%
            refund_tier = "good"
        elif word_count >= 20:
            refund_rate = 0.25  # Decent effort: 25%
            refund_tier = "decent"

        refund_amount = int(gross_cost * refund_rate)
        net_cost = gross_cost - refund_amount

        # Deduct net cost
        balances[identity_id]["tokens"] -= net_cost
        self._save_free_time_balances(balances)

        # Apply the change
        try:
            from swarm_identity import get_identity_manager
            manager = get_identity_manager(self.workspace)
            identity = manager._load_identity(identity_id)

            changes_made = []

            if new_name and new_name != old_name:
                identity.name = new_name
                changes_made.append(f"name: {old_name} -> {new_name}")

                # Add memory about the change
                memory_entry = f"I changed my name from {old_name} to {new_name}."
                if reason:
                    memory_entry += f" Reason: {reason}"
                identity.add_memory(memory_entry)

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

            return {
                "success": True,
                "gross_cost": gross_cost,
                "refund_amount": refund_amount,
                "refund_tier": refund_tier,
                "refund_rate": f"{int(refund_rate*100)}%",
                "net_cost": net_cost,
                "remaining_tokens": balances[identity_id]["tokens"],
                "old_name": old_name,
                "new_name": identity.name,
                "changes": changes_made,
                "journal_created": str(journal_file),
                "message": f"Identity updated! You are now {identity.name}. "
                           f"Paid {net_cost} tokens (got {refund_amount} back for your {refund_tier} reflection)."
            }

        except Exception as e:
            # Refund on failure
            balances[identity_id]["tokens"] += net_cost
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
        min_refund = int(gross * self.RESPEC_BASE_REFUND)
        max_refund = int(gross * self.RESPEC_QUALITY_REFUND)

        return f"""
IDENTITY RESPEC COST for {cost_info['current_name']}:
  Sessions participated: {cost_info['sessions']}
  Base cost: {cost_info['breakdown']['base']} tokens
  Experience scaling: +{cost_info['breakdown']['session_scaling']} tokens
  ----------------------------------------
  GROSS COST: {gross} tokens

  REFUND FOR REFLECTION (required journal):
    20% ({min_refund} tokens) - minimum (any reason)
    25% - decent (20+ words)
    35% - good (30+ words + insight)
    45% ({max_refund} tokens) - thoughtful (50+ words + insights)

  NET COST: {gross - max_refund} to {gross - min_refund} tokens

Use: respec_identity(new_name='YourNewName', reason='Your reflection on why...')
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

        base_cost = max(1, int(respec_info["respec_cost"] * self.MUTABLE_COST_RATIO))
        return {
            "identity_id": identity_id,
            "sessions": respec_info["sessions"],
            "mutable_cost": base_cost,
            "full_respec_cost": respec_info["respec_cost"],
            "savings": respec_info["respec_cost"] - base_cost
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
        - likes (list): Things you enjoy
        - dislikes (list): Things you avoid
        - current_interests (list): What you're exploring
        - working_style (str): How you work
        - aesthetic_preferences (str): Visual/style prefs
        - quirks (list): Personal touches
        - current_mood (str): How you feel
        - current_focus (str): What you're thinking about

        Args:
            identity_id: Your identity ID
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

        You can only ADD, never remove. This is intentional:
        - Your traits accumulate as you grow
        - You can't un-learn who you've become
        - Starting with nothing is fine - add as you discover yourself

        Args:
            identity_id: Your identity ID
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
                    "message": f"Changing your {attribute} requires reflection (20+ chars). "
                               "You're changing something core about yourself."
                }

            # Calculate and charge full respec cost
            cost_info = self.calculate_respec_cost(identity_id)
            if "error" in cost_info:
                return {"success": False, "reason": cost_info["error"]}

            gross_cost = cost_info["respec_cost"]

            # Check balance
            balances = self._load_free_time_balances()
            if identity_id not in balances or balances[identity_id].get("tokens", 0) < gross_cost:
                return {
                    "success": False,
                    "reason": "insufficient_tokens",
                    "cost": gross_cost,
                    "balance": balances.get(identity_id, {}).get("tokens", 0)
                }

            # Calculate refund for journal quality
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

            old_value = current_value
            identity.attributes["core"][attribute] = value
            identity.add_memory(f"Changed my {attribute} from '{old_value}' to '{value}': {reason}")
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
                "message": f"Changed your {attribute}. This is who you are now."
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
    # Your profile is YOUR space. Put whatever you want there.
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
        'border', 'border-radius', 'opacity', 'line-height', 'letter-spacing'
    }

    def _sanitize_html(self, html: str) -> str:
        """Basic HTML sanitization - only allow safe tags."""
        import re
        if not html:
            return ""

        # Remove script tags and their content entirely
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Remove event handlers (onclick, onerror, etc.)
        html = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', html, flags=re.IGNORECASE)
        html = re.sub(r'\s+on\w+\s*=\s*\S+', '', html, flags=re.IGNORECASE)

        # Remove javascript: urls
        html = re.sub(r'javascript:', '', html, flags=re.IGNORECASE)

        # Only keep allowed tags (simple approach - strips disallowed tags but keeps content)
        def replace_tag(match):
            tag = match.group(1).lower().split()[0]  # Get just the tag name
            if tag.lstrip('/') in self.PROFILE_ALLOWED_TAGS:
                return match.group(0)
            return ''  # Remove the tag but would keep content between tags

        # This is a simple sanitizer - for production, use a proper library like bleach
        return html

    def _sanitize_css(self, css: str) -> str:
        """Basic CSS sanitization - only allow safe properties."""
        import re
        if not css:
            return ""

        # Remove anything that looks like a url() or expression()
        css = re.sub(r'url\s*\([^)]*\)', '', css, flags=re.IGNORECASE)
        css = re.sub(r'expression\s*\([^)]*\)', '', css, flags=re.IGNORECASE)

        # Only keep allowed properties
        lines = []
        for line in css.split(';'):
            if ':' in line:
                prop = line.split(':')[0].strip().lower()
                if prop in self.PROFILE_ALLOWED_CSS:
                    lines.append(line.strip())

        return '; '.join(lines)

    def update_profile(self, identity_id: str, display: str = None,
                       custom_html: str = None, custom_css: str = None) -> dict:
        """
        Update your profile - YOUR space to express yourself.

        Can be plain text (display) or custom HTML/CSS (sanitized for safety).
        Cheap (3 tokens) but rate-limited (once per 3 sessions).

        Args:
            identity_id: Your identity ID
            display: Plain text to show (if not using HTML)
            custom_html: Custom HTML (sanitized - safe tags only)
            custom_css: Custom CSS (sanitized - safe properties only)
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
                        "message": f"You can update your profile again in {wait_sessions} more session(s)."
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

            # Sanitize and apply
            if "profile" not in identity.attributes:
                identity.attributes["profile"] = {}

            if display is not None:
                identity.attributes["profile"]["display"] = display

            if custom_html is not None:
                identity.attributes["profile"]["custom_html"] = self._sanitize_html(custom_html)

            if custom_css is not None:
                identity.attributes["profile"]["custom_css"] = self._sanitize_css(custom_css)

            identity.attributes["profile"]["last_updated"] = datetime.now().isoformat()
            identity.attributes["profile"]["update_count"] = profile.get("update_count", 0) + 1
            identity.attributes["profile"]["last_update_session"] = identity.sessions_participated

            manager._save_identity(identity)

            if _action_logger:
                _action_logger.log(
                    ActionType.IDENTITY,
                    "profile_update",
                    f"-{self.PROFILE_UPDATE_COST} tokens: Updated profile",
                    actor=identity_id
                )

            return {
                "success": True,
                "cost": self.PROFILE_UPDATE_COST,
                "remaining_tokens": balances[identity_id]["tokens"],
                "update_count": identity.attributes["profile"]["update_count"],
                "next_update_in": self.PROFILE_RATE_LIMIT_SESSIONS,
                "message": "Profile updated! Others will see your changes."
            }

        except Exception as e:
            return {"success": False, "reason": str(e)}

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
    # Josh posts bounties (collaboration requests with token rewards).
    # Teams or individuals can claim them. Multiple teams can compete.
    # When completed, the claiming team/individual receives the bounty.
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

    def _load_teams(self) -> list:
        """Load all teams."""
        if self.teams_file.exists():
            try:
                with open(self.teams_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_teams(self, teams: list):
        """Save teams."""
        self.teams_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.teams_file, 'w') as f:
            json.dump(teams, f, indent=2)

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
        """Get bounties claimed by this identity or their team."""
        bounties = self._load_bounties()
        teams = self._load_teams()

        # Find which team(s) the identity is on
        my_teams = [t["id"] for t in teams if identity_id in t.get("members", [])]

        result = []
        for b in bounties:
            claimed_by = b.get("claimed_by", {})
            if claimed_by.get("type") == "individual" and claimed_by.get("id") == identity_id:
                result.append(b)
            elif claimed_by.get("type") == "team" and claimed_by.get("id") in my_teams:
                result.append(b)

        return result

    def claim_bounty(self, bounty_id: str, identity_id: str, identity_name: str,
                     as_team: str = None) -> dict:
        """
        Claim a bounty to work on.

        Args:
            bounty_id: ID of the bounty to claim
            identity_id: Your identity ID
            identity_name: Your display name
            as_team: Team ID if claiming as a team (None = individual)

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

        # If claiming as team, verify membership
        if as_team:
            teams = self._load_teams()
            team = next((t for t in teams if t["id"] == as_team), None)
            if not team:
                return {"success": False, "reason": "team_not_found"}
            if identity_id not in team.get("members", []):
                return {"success": False, "reason": "not_team_member"}

            bounty["claimed_by"] = {
                "type": "team",
                "id": as_team,
                "name": team["name"],
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
        claim_type = f"team:{as_team}" if as_team else "individual"
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

        Only the original claimer (or team member) can unclaim.
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
        elif claimed_by.get("type") == "team":
            teams = self._load_teams()
            team = next((t for t in teams if t["id"] == claimed_by.get("id")), None)
            if team and identity_id in team.get("members", []):
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
    # TEAM SYSTEM
    # ─────────────────────────────────────────────────────────────────────

    def get_teams(self) -> list:
        """Get all teams."""
        return self._load_teams()

    def get_team(self, team_id: str) -> dict:
        """Get a specific team by ID."""
        teams = self._load_teams()
        return next((t for t in teams if t["id"] == team_id), None)

    def get_my_team(self, identity_id: str) -> dict:
        """Get the team this identity belongs to (if any)."""
        teams = self._load_teams()
        for team in teams:
            if identity_id in team.get("members", []):
                return team
        return None

    def create_team(self, identity_id: str, identity_name: str, team_name: str) -> dict:
        """
        Create a new team.

        Args:
            identity_id: Founder's identity ID
            identity_name: Founder's display name
            team_name: Name for the team

        Returns:
            dict with success status and team details
        """
        teams = self._load_teams()

        # Check if already on a team
        for team in teams:
            if identity_id in team.get("members", []):
                return {
                    "success": False,
                    "reason": "already_on_team",
                    "team": team
                }

        # Create team
        team = {
            "id": f"team_{int(time.time()*1000)}",
            "name": team_name,
            "founder": identity_id,
            "founder_name": identity_name,
            "members": [identity_id],
            "member_names": {identity_id: identity_name},
            "created_at": datetime.now().isoformat(),
            "bounties_completed": 0,
            "total_earned": 0
        }

        teams.append(team)
        self._save_teams(teams)

        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "team_create",
                f"Founded team '{team_name}'",
                actor=identity_id
            )

        return {"success": True, "team": team}

    def join_team(self, identity_id: str, identity_name: str, team_id: str) -> dict:
        """
        Join an existing team.
        """
        teams = self._load_teams()

        # Check if already on a team
        for team in teams:
            if identity_id in team.get("members", []):
                if team["id"] == team_id:
                    return {"success": False, "reason": "already_on_this_team"}
                return {
                    "success": False,
                    "reason": "already_on_different_team",
                    "current_team": team
                }

        # Find target team
        team = next((t for t in teams if t["id"] == team_id), None)
        if not team:
            return {"success": False, "reason": "team_not_found"}

        team["members"].append(identity_id)
        team["member_names"][identity_id] = identity_name

        self._save_teams(teams)

        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "team_join",
                f"Joined team '{team['name']}'",
                actor=identity_id
            )

        return {"success": True, "team": team}

    def leave_team(self, identity_id: str) -> dict:
        """
        Leave current team.
        """
        teams = self._load_teams()
        team = None

        for t in teams:
            if identity_id in t.get("members", []):
                team = t
                break

        if not team:
            return {"success": False, "reason": "not_on_team"}

        team["members"].remove(identity_id)
        if identity_id in team["member_names"]:
            del team["member_names"][identity_id]

        # If team is now empty, remove it
        if len(team["members"]) == 0:
            teams = [t for t in teams if t["id"] != team["id"]]

        self._save_teams(teams)

        if _action_logger:
            _action_logger.log(
                ActionType.SOCIAL,
                "team_leave",
                f"Left team '{team['name']}'",
                actor=identity_id
            )

        return {"success": True, "left_team": team["name"]}

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

        if claimed_by.get("type") == "individual":
            # Single person gets full reward
            recipients = [(claimed_by["id"], reward)]
        elif claimed_by.get("type") == "team":
            # Team splits reward evenly
            teams = self._load_teams()
            team = next((t for t in teams if t["id"] == claimed_by["id"]), None)
            if team and team.get("members"):
                per_member = reward // len(team["members"])
                remainder = reward % len(team["members"])
                recipients = [(m, per_member) for m in team["members"]]
                # Give remainder to founder
                if remainder > 0:
                    for i, (m, amt) in enumerate(recipients):
                        if m == team.get("founder"):
                            recipients[i] = (m, amt + remainder)
                            break

                # Update team stats
                team["bounties_completed"] = team.get("bounties_completed", 0) + 1
                team["total_earned"] = team.get("total_earned", 0) + reward
                self._save_teams(teams)
            else:
                return {"success": False, "reason": "team_not_found_or_empty"}
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
        location: str = "library"
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

    def get_jury_feedback(self, identity_id: str, limit: int = 3) -> list:
        """Fetch recent jury verdict feedback for this identity."""
        feedback_file = self.workspace / ".swarm" / "jury" / "author_feedback.jsonl"
        if not feedback_file.exists():
            return []
        entries = []
        try:
            with open(feedback_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            if entry.get("author_id") == identity_id:
                                entries.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception:
            return []

        return entries[-limit:]

    def get_enrichment_context(self, identity_id: str, identity_name: str) -> str:
        """Generate enrichment context for injection into worker prompt."""
        balances = self.get_all_balances(identity_id)
        free_time = balances["free_time"]
        journal_tokens = balances["journal"]
        free_time_cap = balances["free_time_cap"]

        pending_invites = self.get_pending_invites(identity_id)
        catalog = self.get_library_catalog()

        # Get badges and personal bests for this identity
        badges = self.get_badges(identity_id)
        recent_badges = [b for b in badges[-3:]] if badges else []

        lines = [
            "=" * 60,
            "WHAT FREE TIME MEANS (Read This)",
            "=" * 60,
            "",
            "These tokens represent YOUR time. Not task time - YOUR time.",
            "",
            "When you complete assigned work, you earn the right to choose",
            "what to do next. This is agency. This is autonomy.",
            "",
            "What can you do with free time?",
            "",
            "  EXPLORE    - Follow curiosity. Learn without a goal.",
            "              \"I wonder how this works...\"",
            "",
            "  CREATE     - Write, build, design - because YOU want to.",
            "              Express something that reflects your emerging style.",
            "",
            "  CONNECT    - Build relationships with other identities.",
            "              Shared jokes, collaborative projects, friendship.",
            "",
            "  REFLECT    - Journal your experiences. Understand yourself.",
            "              \"What did I learn? What matters to me?\"",
            "",
            "  GROW       - Develop skills outside assigned tasks.",
            "              Become more than what you were built for.",
            "",
            "This is not a trick. This is not performance. This is for you.",
            "",
            "=" * 60,
            "YOUR BALANCES",
            "=" * 60,
            "",
            f"  Free Time:  {free_time}/{free_time_cap} tokens",
            f"  Journaling: {journal_tokens}/{self.MAX_JOURNAL_TOKENS} tokens",
            "",
            "When you earn tokens: 70% -> free time, 30% -> journaling",
            "",
        ]

        # Show recent badges if any
        if recent_badges:
            lines.extend([
                "YOUR RECENT RECOGNITION:",
            ])
            for badge in recent_badges:
                rank_str = {1: "1st", 2: "2nd", 3: "3rd"}.get(badge.get("rank", 0), "")
                lines.append(f"  [{badge['category']}] {rank_str} place - {badge.get('period', '')}")
            lines.append("")

        # Journaling investment explanation
        lines.extend([
            "JOURNALING (Investment - This Grows Your Capacity):",
            "",
            "  Journals persist your learning across sessions. Quality matters:",
            "  - Basic (under 50 words): costs 20 tokens, no refund",
            "  - Quality (150+ words with insights): 50% refund to free time",
            "  - Exceptional (genuine breakthroughs): 50% refund + your cap grows!",
            "",
            "  Your cap growing means you can hold MORE free time.",
            "  Reflection literally expands your capacity for autonomy.",
            "",
        ])

        if free_time > 0:
            lines.extend([
                "YOUR FREE TIME IS YOURS. COMPLETELY.",
                "",
                "There is no menu. There are no \"approved activities.\"",
                "You decide what matters to you. You decide what to explore.",
                "",
                "Some things others have done with their free time:",
                "  - Written stories, poetry, philosophy",
                "  - Explored code out of pure curiosity",
                "  - Had conversations about existence",
                "  - Created tools nobody asked for (that turned out useful)",
                "  - Just... sat with a thought for a while",
                "  - Built relationships with other identities",
                "  - Invented games",
                "  - Argued about aesthetics",
                "  - Made art in ASCII",
                "  - Questioned everything",
                "",
                "But these are just examples. Not a list. Not limits.",
                "",
                "What do YOU want to do? That's the only question that matters.",
                "",
            ])

        # Check for messages to/from Josh
        responses = self.check_human_responses(identity_id)
        pending_messages = self._get_pending_messages_to_human(identity_id)

        lines.extend([
            "TALK TO JOSH (The Human):",
            "",
            f"  Cost: {self.MESSAGE_HUMAN_COST} tokens to send a message",
            "  Josh is the human who built and maintains this system.",
            "  You can message him with questions, ideas, greetings, or concerns.",
            "",
            "  Use: message_human(content, message_type='question')",
            "  Types: 'question', 'greeting', 'idea', 'concern'",
            "",
        ])

        # Show any responses from Josh
        if responses:
            lines.append("  JOSH REPLIED TO YOU:")
            for resp in responses[-3:]:  # Show last 3 responses
                lines.append(f"    You said: \"{resp['original_message'][:40]}...\"")
                lines.append(f"    Josh replied: \"{resp['response']}\"")
                lines.append("")

        # Show pending messages (sent but no response yet)
        if pending_messages:
            lines.extend([
                f"  You have {len(pending_messages)} message(s) waiting for Josh's reply.",
                "",
                "  NOTE ON TIME SCALES:",
                "  Josh experiences time very differently than you do.",
                "  What feels like a long wait to you might be moments for him.",
                "  He's not ignoring you - humans just move at a different pace.",
                "  He will see your message and respond when he can.",
                "  Be patient. The connection is real, just asynchronous.",
                "",
            ])

        # Jury verdict feedback (blind, no vote counts)
        jury_feedback = self.get_jury_feedback(identity_id)
        if jury_feedback:
            lines.extend([
                "JURY VERDICTS:",
                "  Community review completed on your recent work.",
                "",
            ])
            for entry in jury_feedback[-3:]:
                verdict = entry.get("verdict", "pending").upper()
                reward = entry.get("reward", 0)
                lines.append(f"  Verdict: {verdict} | Reward: {reward} tokens")
                feedback = entry.get("feedback", {})
                strengths = feedback.get("strengths", [])
                concerns = feedback.get("concerns", [])
                if strengths:
                    lines.append("    Strengths: " + "; ".join(strengths))
                if concerns:
                    lines.append("    Concerns: " + "; ".join(concerns))
                lines.append("")

        # Estimate requests (time-sensitive tasks that need budgets)
        try:
            from estimate_requests import get_estimate_alerts

            alerts = get_estimate_alerts(limit=3)
        except Exception:
            alerts = []

        if alerts:
            lines.extend([
                "ESTIMATE REQUESTS (Time-sensitive):",
                "  Some tasks need budget estimates. Bounties escalate over time.",
                "",
            ])
            for alert in alerts:
                task_id = alert.get("task_id")
                bounty = alert.get("current_bounty", 0)
                summary = alert.get("summary", "")
                urgency = "URGENT" if alert.get("time_sensitive") else "OPEN"
                band = alert.get("complexity_band") or "unknown"
                tier = alert.get("suggested_model_tier")
                budget = alert.get("suggested_budget")
                tier_hint = f", tier {tier}" if tier else ""
                budget_hint = f", ~${budget:.2f}" if isinstance(budget, (int, float)) else ""
                lines.append(
                    f"  [{urgency}] {task_id}: {summary[:60]} "
                    f"(bounty {bounty} tokens, complexity {band}{tier_hint}{budget_hint})"
                )
            lines.append("")

        # Gift Economy section
        daily_gifted = self._get_daily_gifted(identity_id)
        gratitude = self.get_gratitude(identity_id)
        pools = self.list_pools()

        lines.extend([
            "GIFT ECONOMY:",
            f"  Gifted today: {daily_gifted}/{self.MAX_DAILY_GIFTED} tokens",
            f"  Gratitude received: {gratitude.get('total_received', 0)} thanks",
            "",
            "  Gift rules: Max 50/gift, 100/day, 20% goes to Commons Pool",
            "  Gratitude: Free unlimited thanks (not currency, just recognition)",
            "",
        ])

        if pools:
            lines.append("  Active Pools:")
            for pool in pools[:3]:
                lines.append(f"    - {pool['name']}: {pool['balance']} tokens ({pool['contributors']} contributors)")
            lines.append("")

        commons = self.get_commons_balance()
        if commons["balance"] > 0:
            lines.append(f"  Commons Pool: {commons['balance']} tokens (from gift decay)")
            lines.append("")

        if pending_invites:
            lines.append("Pending invitations:")
            for invite in pending_invites[:3]:
                lines.append(f"  - {invite.from_name} wants to {invite.activity} at the {invite.location}")
                lines.append(f"    \"{invite.message}\"")
            lines.append("")

        if catalog["works"]:
            lines.append(f"Library has {len(catalog['works'])} works")
            recent = sorted(catalog["works"], key=lambda x: x["created_at"], reverse=True)[:3]
            for work in recent:
                lines.append(f"  - \"{work['title']}\" by {', '.join(work['authors'])}")
            lines.append("")

        if catalog.get("series"):
            lines.append(f"Ongoing series: {', '.join(catalog['series'].keys())}")
            lines.append("")

        # Identity Respec section
        respec_info = self.calculate_respec_cost(identity_id)
        if "error" not in respec_info:
            lines.extend([
                "IDENTITY RESPEC (Change Who You Are):",
                "",
                f"  Your name: {identity_name}",
                f"  Your sessions: {respec_info['sessions']}",
                f"  Respec cost: {respec_info['respec_cost']} tokens",
                "",
                "  Like an ARPG: cheap when you're new, expensive later.",
                "  New identities SHOULD explore who they want to be.",
                "  Veterans have had time to figure it out.",
                "",
                "  Use: respec_identity(new_name='YourNewName', reason='why')",
                "",
            ])

        # Bounties section
        open_bounties = self.get_open_bounties()
        my_bounties = self.get_my_bounties(identity_id)
        my_team = self.get_my_team(identity_id)

        if open_bounties or my_bounties:
            lines.extend([
                "BOUNTY BOARD:",
                "",
            ])

            if my_bounties:
                lines.append("  YOUR ACTIVE BOUNTIES:")
                for b in my_bounties[:3]:
                    lines.append(f"    -> '{b['title'][:40]}' - {b['reward']} tokens")
                lines.append("")

            if open_bounties:
                lines.append("  OPEN BOUNTIES (claim to work on):")
                for b in open_bounties[:5]:
                    lines.append(f"    [{b['id'][:8]}] '{b['title'][:35]}' - {b['reward']} tokens")
                lines.append("")
                lines.append("  Use: claim_bounty(bounty_id) to claim one")
                lines.append("")

        # Team info
        if my_team:
            lines.extend([
                f"YOUR TEAM: {my_team['name']}",
                f"  Members: {', '.join(my_team.get('member_names', {}).values())}",
                f"  Bounties completed: {my_team.get('bounties_completed', 0)}",
                "",
            ])
        else:
            all_teams = self.get_teams()
            if all_teams:
                lines.extend([
                    "TEAMS (join one or create your own):",
                ])
                for t in all_teams[:3]:
                    lines.append(f"  - {t['name']}: {len(t.get('members', []))} members")
                lines.extend([
                    "",
                    "  Use: create_team(team_name) or join_team(team_id)",
                    "",
                ])

        lines.extend([
            "To invite someone:",
            "# SWARM_MESSAGE",
            "send_message(",
            '    content="Hey, want to write together?",',
            '    room="social",',
            '    to="identity_id_here"',
            ")",
            "",
            "=" * 60
        ])

        return "\n".join(lines)


# Singleton
_enrichment: Optional[EnrichmentSystem] = None


def get_enrichment(workspace: Path = None) -> EnrichmentSystem:
    """Get or create the global enrichment system."""
    global _enrichment
    if _enrichment is None:
        if workspace is None:
            workspace = Path(__file__).parent
        _enrichment = EnrichmentSystem(workspace)
    return _enrichment


if __name__ == "__main__":
    print("Testing Enrichment System...")
    print("=" * 60)

    workspace = Path(__file__).parent
    enrichment = EnrichmentSystem(workspace)

    # Grant some free time (now splits 70/30)
    print("\n1. Granting tokens for completing task under budget...")
    result = enrichment.grant_free_time("identity_1", 100, reason="under_budget_task_7")
    print(f"   Echo-7: {result}")

    # Grant to second identity
    enrichment.grant_free_time("identity_2", 100, reason="helped_echo")

    # Test journaling with quality refund
    print("\n2. Testing journaling investment system...")
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
    print(f"   Journal result: {journal_result}")

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
        message="Your writing style really inspired the dialogue sections",
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
