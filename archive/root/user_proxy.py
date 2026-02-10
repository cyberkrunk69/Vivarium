"""
# ----------------------------------------------------------------------
    # Internal helpers that hold the original logic – these are called by the
    # v2‑wrapped methods above.  If they already exist, this block is a no‑op.
    # ----------------------------------------------------------------------
    if not hasattr(UserProxy, "_original_feature_breakdown"):
        UserProxy._original_feature_breakdown = UserProxy.feature_breakdown
    if not hasattr(UserProxy, "_original_feature_planning"):
        UserProxy._original_feature_planning = UserProxy.feature_planning
    if not hasattr(UserProxy, "_original_e2e_testing"):
        UserProxy._original_e2e_testing = UserProxy.e2e_testing
# ----------------------------------------------------------------------
    # New capture helpers – store only non‑personal user signals for validation
    # ----------------------------------------------------------------------
    def _capture_stated_preferences(self, data):
        """Store preferences explicitly stated by the user during feature breakdown."""
        if not hasattr(self, "stated_preferences"):
            self.stated_preferences = {}
        self.stated_preferences.update(data or {})

    def _capture_confirmed_requirements(self, data):
        """Store requirements the user has confirmed during feature planning."""
        if not hasattr(self, "confirmed_requirements"):
            self.confirmed_requirements = {}
        self.confirmed_requirements.update(data or {})

    def _capture_corrections_and_style(self, corrections=None, style=None):
        """Store any corrections and style preferences the user supplies after E2E testing."""
        if not hasattr(self, "corrections"):
            self.corrections = {}
        if not hasattr(self, "style_preferences"):
            self.style_preferences = {}
        self.corrections.update(corrections or {})
        self.style_preferences.update(style or {})
User Proxy Node - Persistent representation of user preferences.

Acts as the 'CEO' that approves outputs before they're finalized.
Learns from user interactions to build a preference profile.
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime

from rlif_detector import SentimentDetector, detect_sentiment


@dataclass
class UserProfile:
    """Persistent user preference profile."""
    communication_style: str          # "concise", "detailed", "technical"
    formatting_preferences: List[str] # ["no emojis", "use bullet points"]
    anti_patterns: List[str]          # Things user has rejected before
    approval_patterns: List[str]      # Things user has approved
    frustration_triggers: List[str]   # What annoys this user
    technical_level: str              # "beginner", "intermediate", "expert"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    interaction_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "communication_style": self.communication_style,
            "formatting_preferences": self.formatting_preferences,
            "anti_patterns": self.anti_patterns,
            "approval_patterns": self.approval_patterns,
            "frustration_triggers": self.frustration_triggers,
            "technical_level": self.technical_level,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "interaction_count": self.interaction_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        return cls(
            communication_style=data.get("communication_style", "concise"),
            formatting_preferences=data.get("formatting_preferences", []),
            anti_patterns=data.get("anti_patterns", []),
            approval_patterns=data.get("approval_patterns", []),
            frustration_triggers=data.get("frustration_triggers", []),
            technical_level=data.get("technical_level", "intermediate"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            interaction_count=data.get("interaction_count", 0)
        )

    @classmethod
    def default(cls) -> 'UserProfile':
        """Create default profile for new users."""
        return cls(
            communication_style="concise",
            formatting_preferences=[
                "no emojis in code",
                "use clear variable names",
                "include error handling"
            ],
            anti_patterns=[
                "over-engineering",
                "unnecessary comments",
                "magic numbers"
            ],
            approval_patterns=[
                "clean code",
                "proper error handling",
                "follows existing patterns"
            ],
            frustration_triggers=[
                "ignored instructions",
                "breaking existing functionality",
                "verbose explanations"
            ],
            technical_level="intermediate"
        )


@dataclass
class ApprovalResult:
    """Result from approval simulation."""
    approved: bool
    confidence: float
    concerns: List[str]
    suggested_changes: List[str]

    @property
    def needs_revision(self) -> bool:
        """Whether output needs revision before finalizing."""
        return not self.approved or len(self.concerns) > 0


class UserProxy:
    """Persistent representation of user - the 'CEO' that approves outputs."""

    # Default anti-patterns that most developers dislike
    DEFAULT_ANTI_PATTERNS = [
        "hardcoded values",
        "no error handling",
        "unclear variable names",
        "excessive comments",
        "breaking changes without notice",
        "ignoring existing patterns",
    ]

    # Common formatting preferences
    COMMON_PREFERENCES = {
        "no_emojis": r"[^\x00-\x7F]",  # Non-ASCII characters
        "uses_constants": r"[A-Z_]{2,}\s*=",  # CONSTANT_NAMES
        "has_docstrings": r'""".*?"""',  # Docstrings
        "has_type_hints": r"def \w+\([^)]*:\s*\w+",  # Type hints
    }

    def __init__(self, profile_path: str = "user_profile.json"):
        self.profile_path = Path(profile_path)
        self.profile = self._load_profile()
        self._sentiment_detector = SentimentDetector()

    def _load_profile(self) -> UserProfile:
        """Load user profile from disk."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return UserProfile.from_dict(data)
            except (json.JSONDecodeError, IOError):
                pass
        return UserProfile.default()

    def _save_profile(self):
        """Save profile to disk."""
        self.profile.updated_at = datetime.now().isoformat()
        try:
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.profile.to_dict(), f, indent=2)
        except IOError as e:
            print(f"[USER PROXY] Warning: Could not save profile: {e}")

    def simulate_approval(self, output: str, task: str) -> ApprovalResult:
        """
        Before marking complete, ask: 'Would the user approve this?'

        Args:
            output: The agent's output (code, text, etc.)
            task: The original task description

        Returns:
            ApprovalResult with approval status and concerns
        """
        concerns = []
        suggested_changes = []

        # Check against anti-patterns
        for pattern in self.profile.anti_patterns:
            if self._matches_pattern(output, pattern):
                concerns.append(f"Contains anti-pattern: {pattern}")
                suggested_changes.append(f"Remove/fix: {pattern}")

        # Check formatting preferences
        for pref in self.profile.formatting_preferences:
            if not self._satisfies_preference(output, pref):
                concerns.append(f"Doesn't satisfy preference: {pref}")
                suggested_changes.append(f"Add: {pref}")

        # Check for frustration triggers
        for trigger in self.profile.frustration_triggers:
            if self._contains_trigger(output, trigger):
                concerns.append(f"Contains frustration trigger: {trigger}")
                suggested_changes.append(f"Address: {trigger}")

        # Check task completion
        if not self._task_appears_complete(output, task):
            concerns.append("Task may not be fully complete")
            suggested_changes.append("Verify all requirements are met")

        # Calculate approval confidence
        confidence = 1.0 - (len(concerns) * 0.15)
        confidence = max(0.0, min(1.0, confidence))

        # Approval threshold: 60%
        approved = confidence >= 0.6 and len(concerns) <= 2

        return ApprovalResult(
            approved=approved,
            confidence=confidence,
            concerns=concerns,
            suggested_changes=suggested_changes
        )

    def _matches_pattern(self, output: str, pattern: str) -> bool:
        """Check if output contains an anti-pattern."""
        output_lower = output.lower()
        pattern_lower = pattern.lower()

        # Direct keyword matching
        if pattern_lower in output_lower:
            return True

        # Pattern-specific checks
        pattern_checks = {
            "hardcoded": lambda o: any(s in o for s in ["localhost", "127.0.0.1", "http://", "https://"]) and "config" not in o.lower(),
            "no error handling": lambda o: "try" not in o and "except" not in o and "def " in o,
            "magic numbers": lambda o: any(f" {n} " in o for n in ["0", "1", "100", "1000", "60", "24"]),
            "over-engineering": lambda o: o.count("class ") > 3 or o.count("def ") > 10,
        }

        for key, check in pattern_checks.items():
            if key in pattern_lower:
                try:
                    return check(output)
                except Exception:
                    pass

        return False

    def _satisfies_preference(self, output: str, preference: str) -> bool:
        """Check if output satisfies a preference."""
        pref_lower = preference.lower()

        # Check common preferences
        if "no emojis" in pref_lower:
            import re
            # Check for common emojis
            emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]'
            return not bool(re.search(emoji_pattern, output))

        if "error handling" in pref_lower:
            return "try" in output or "except" in output or "raise" in output

        if "bullet points" in pref_lower:
            return "-" in output or "*" in output or "•" in output

        if "type hints" in pref_lower:
            return ": " in output and "def " in output

        if "docstring" in pref_lower:
            return '"""' in output or "'''" in output

        # Default: assume satisfied
        return True

    def _contains_trigger(self, output: str, trigger: str) -> bool:
        """Check if output contains a frustration trigger."""
        output_lower = output.lower()
        trigger_lower = trigger.lower()

        # Direct match
        if trigger_lower in output_lower:
            return True

        # Semantic triggers
        trigger_indicators = {
            "ignored instructions": lambda o: "TODO" in o or "FIXME" in o,
            "breaking changes": lambda o: "removed" in o.lower() or "deleted" in o.lower(),
            "verbose explanations": lambda o: len(o) > 5000 and o.count("\n\n") > 10,
        }

        for key, check in trigger_indicators.items():
            if key in trigger_lower:
                try:
                    return check(output)
                except Exception:
                    pass

        return False

    def _task_appears_complete(self, output: str, task: str) -> bool:
        """Check if the task appears to be complete."""
        # Look for completion indicators
        completion_indicators = ["done", "complete", "finished", "implemented", "created", "fixed"]
        output_lower = output.lower()

        has_indicator = any(ind in output_lower for ind in completion_indicators)

        # Check if output has substance
        has_substance = len(output) > 50

        # Check if it contains code (if task seems to require it)
        task_lower = task.lower()
        needs_code = any(kw in task_lower for kw in ["implement", "create", "add", "fix", "write", "build"])
        has_code = "def " in output or "class " in output or "function" in output

        if needs_code and not has_code:
            return False

        return has_substance and (has_indicator or has_code)

    def learn_from_interaction(self, user_reaction: str, agent_output: str):
        """
        Update profile from user reactions.

        Args:
            user_reaction: User's response to agent output
            agent_output: What the agent produced
        """
        sentiment = self._sentiment_detector.detect(user_reaction)
        self.profile.interaction_count += 1

        if sentiment.sentiment == "negative":
            # Extract what triggered the negative reaction
            trigger = self._extract_trigger(user_reaction, agent_output)
            if trigger:
                if trigger not in self.profile.anti_patterns:
                    self.profile.anti_patterns.append(trigger)
                    print(f"[USER PROXY] Learned anti-pattern: {trigger}")

                if trigger not in self.profile.frustration_triggers:
                    self.profile.frustration_triggers.append(trigger)

        elif sentiment.sentiment == "positive":
            # Extract what the user approved of
            pattern = self._extract_approval_pattern(user_reaction, agent_output)
            if pattern and pattern not in self.profile.approval_patterns:
                self.profile.approval_patterns.append(pattern)
                print(f"[USER PROXY] Learned approval pattern: {pattern}")

        # Update communication style based on interaction
        self._update_communication_style(user_reaction)

        # Save updated profile
        self._save_profile()

    def _extract_trigger(self, user_reaction: str, agent_output: str) -> Optional[str]:
        """Extract what triggered negative reaction."""
        reaction_lower = user_reaction.lower()

        # Common complaint patterns
        patterns = {
            r"you (missed|forgot|ignored) (.+?)[\.\!]": lambda m: f"ignored: {m.group(2)}",
            r"(didn't|don't|never) (.+?)[\.\!]": lambda m: m.group(2)[:30],
            r"why.*?(no|without) (.+?)[\.\!]": lambda m: f"missing: {m.group(2)}",
            r"too (much|many|long|complex)": lambda m: f"over-{m.group(1)}",
        }

        import re
        for pattern, extractor in patterns.items():
            match = re.search(pattern, reaction_lower)
            if match:
                return extractor(match)

        return None

    def _extract_approval_pattern(self, user_reaction: str, agent_output: str) -> Optional[str]:
        """Extract what the user approved of."""
        reaction_lower = user_reaction.lower()

        # Common approval patterns
        patterns = {
            r"(love|like) the (.+?)[\.\!]": lambda m: m.group(2)[:30],
            r"(perfect|exactly|great) (.+?)[\.\!]": lambda m: m.group(2)[:30],
            r"this is (.+?)[\.\!]": lambda m: m.group(1)[:30],
        }

        import re
        for pattern, extractor in patterns.items():
            match = re.search(pattern, reaction_lower)
            if match:
                return extractor(match)

        # Generic approval
        if any(word in reaction_lower for word in ["thanks", "perfect", "great", "good"]):
            # Try to identify what was good about the output
            if "clean" in agent_output.lower():
                return "clean code"
            if "error" in agent_output.lower() and "try" in agent_output:
                return "proper error handling"

        return None

    def _update_communication_style(self, user_reaction: str):
        """Update preferred communication style based on reaction."""
        reaction_lower = user_reaction.lower()

        if any(word in reaction_lower for word in ["verbose", "long", "too much"]):
            self.profile.communication_style = "concise"
        elif any(word in reaction_lower for word in ["more detail", "explain", "elaborate"]):
            self.profile.communication_style = "detailed"
        elif any(word in reaction_lower for word in ["technical", "specific", "exact"]):
            self.profile.communication_style = "technical"

    def get_profile_summary(self) -> str:
        """Get a summary of user preferences for prompt injection."""
        return f"""
## USER PREFERENCES
- Communication style: {self.profile.communication_style}
- Technical level: {self.profile.technical_level}
- Formatting: {', '.join(self.profile.formatting_preferences[:3])}
- Avoid: {', '.join(self.profile.anti_patterns[:3])}
"""

    def inject_preferences(self, prompt: str) -> str:
        """Inject user preferences into a prompt."""
        preferences = self.get_profile_summary()
        return preferences + "\n" + prompt


# Global instance
_proxy: Optional[UserProxy] = None


def get_user_proxy() -> UserProxy:
    """Get or create global UserProxy instance."""
    global _proxy
    if _proxy is None:
        _proxy = UserProxy()
    return _proxy


def simulate_approval(output: str, task: str) -> ApprovalResult:
    """Convenience function to simulate approval."""
    return get_user_proxy().simulate_approval(output, task)


if __name__ == "__main__":
    # Test
    proxy = UserProxy()

    test_output = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    return total
'''

    test_task = "Create a function to calculate shopping cart total"

    print("Testing User Proxy...")
    print("=" * 60)
    print(f"Task: {test_task}")
    print(f"Output:\n{test_output}")

    approval = proxy.simulate_approval(test_output, test_task)
    print(f"\nApproval Result:")
    print(f"  Approved: {approval.approved}")
    print(f"  Confidence: {approval.confidence:.2f}")
    print(f"  Concerns: {approval.concerns}")
    print(f"  Suggested changes: {approval.suggested_changes}")

    # Test learning
    print("\n" + "=" * 60)
    print("Testing learning from interaction...")

    proxy.learn_from_interaction(
        "No! You forgot error handling! I always want try-except!",
        test_output
    )

    print(f"\nUpdated anti-patterns: {proxy.profile.anti_patterns}")
    print(f"Updated frustration triggers: {proxy.profile.frustration_triggers}")
