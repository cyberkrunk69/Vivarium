"""
RLIF Root Cause Analyzer - Analyze what went wrong using Groq (cheap).

Part of the Reinforcement Learning from Immediate Feedback system.
Uses fast LLM to identify why user is frustrated and what should have been done.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import Groq for analysis
try:
    from groq_client import get_groq_engine
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


@dataclass
class RootCause:
    """Root cause analysis result."""
    trigger: str  # What specific action triggered frustration
    should_have: str  # What should have been done differently
    is_pattern: bool  # Whether this is a recurring pattern
    category: str = "behavioral"  # Category of the mistake
    confidence: float = 0.8
    raw_analysis: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, json_str: str) -> 'RootCause':
        """Parse RootCause from JSON string."""
        try:
            # Clean up the JSON string
            json_str = json_str.strip()
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]

            data = json.loads(json_str)
            return cls(
                trigger=data.get("trigger", "unknown"),
                should_have=data.get("should_have", "unknown"),
                is_pattern=data.get("is_pattern", False),
                category=data.get("category", "behavioral"),
                raw_analysis=data
            )
        except (json.JSONDecodeError, ValueError):
            # Fallback for malformed responses
            return cls(
                trigger="parse_error",
                should_have="Could not parse LLM response",
                is_pattern=False,
                raw_analysis={"raw": json_str}
            )


class RootCauseAnalyzer:
    """Analyze what went wrong - uses Groq (cheap)."""

    # Common mistake categories
    CATEGORIES = [
        "ignored_instruction",  # User explicitly said something, agent ignored it
        "over_engineering",     # Added unnecessary complexity
        "under_engineering",    # Missed important edge cases
        "wrong_interpretation", # Misunderstood the request
        "style_mismatch",       # Output style doesn't match user preference
        "incomplete_work",      # Didn't finish the task
        "wrong_file",           # Modified wrong file
        "missing_context",      # Didn't consider project context
    ]

    def __init__(self):
        self._groq_engine = None

    def _get_engine(self):
        """Lazy-load Groq engine."""
        if self._groq_engine is None and GROQ_AVAILABLE:
            self._groq_engine = get_groq_engine()
        return self._groq_engine

    def analyze(
        self,
        user_message: str,
        agent_output: str,
        context: Dict[str, Any] = None
    ) -> RootCause:
        """
        Analyze what went wrong.

        Args:
            user_message: The frustrated user's message
            agent_output: What the agent produced that caused frustration
            context: Additional context (task, workspace, etc.)

        Returns:
            RootCause analysis
        """
        context = context or {}
        engine = self._get_engine()

        if not engine:
            # Fallback analysis without LLM
            return self._fallback_analysis(user_message, agent_output)

        # Build analysis prompt
        categories_str = ", ".join(self.CATEGORIES)
        prompt = f"""The user expressed frustration with this output.

USER MESSAGE: {user_message}

AGENT OUTPUT (first 1000 chars): {agent_output[:1000]}

CONTEXT: {json.dumps(context, default=str)[:500]}

Analyze:
1. What specific action triggered the frustration?
2. What should have been done differently?
3. Is this a one-time mistake or a recurring pattern?
4. What category best describes this mistake? Categories: {categories_str}

Reply ONLY with valid JSON (no markdown):
{{"trigger": "specific action that caused issue", "should_have": "what should have been done", "is_pattern": true/false, "category": "category_name"}}"""

        try:
            result = engine.execute(
                prompt=prompt,
                model="groq/compound-mini",  # Fast, cheap
                max_tokens=200
            )

            if result.get("returncode") == 0:
                return RootCause.from_json(result.get("result", "{}"))
        except Exception as e:
            print(f"[RLIF] Analysis error: {e}")

        # Fallback if LLM fails
        return self._fallback_analysis(user_message, agent_output)

    def _fallback_analysis(self, user_message: str, agent_output: str) -> RootCause:
        """Simple pattern-based fallback analysis."""
        user_lower = user_message.lower()

        # Check for common complaint patterns
        if "didn't" in user_lower or "forgot" in user_lower or "missed" in user_lower:
            return RootCause(
                trigger="Missed a requirement",
                should_have="Pay closer attention to all requirements in the task",
                is_pattern=True,
                category="incomplete_work"
            )

        if "wrong" in user_lower or "not what" in user_lower:
            return RootCause(
                trigger="Produced wrong output",
                should_have="Verify output matches the stated requirements",
                is_pattern=True,
                category="wrong_interpretation"
            )

        if "too" in user_lower and ("complex" in user_lower or "much" in user_lower):
            return RootCause(
                trigger="Over-complicated the solution",
                should_have="Keep solution simple and focused on requirements",
                is_pattern=True,
                category="over_engineering"
            )

        # Default
        return RootCause(
            trigger="Unknown trigger",
            should_have="Clarify requirements before proceeding",
            is_pattern=False,
            category="missing_context"
        )

    def analyze_batch(
        self,
        interactions: List[Dict[str, Any]]
    ) -> List[RootCause]:
        """
        Analyze multiple interactions to find patterns.

        Args:
            interactions: List of {user_message, agent_output, context} dicts

        Returns:
            List of RootCause analyses
        """
        results = []
        for interaction in interactions:
            cause = self.analyze(
                interaction.get("user_message", ""),
                interaction.get("agent_output", ""),
                interaction.get("context", {})
            )
            results.append(cause)
        return results

    def find_common_patterns(
        self,
        root_causes: List[RootCause]
    ) -> Dict[str, int]:
        """
        Find common patterns across multiple root causes.

        Returns dict of {pattern: count}
        """
        patterns = {}
        for cause in root_causes:
            if cause.is_pattern:
                key = f"{cause.category}:{cause.trigger[:50]}"
                patterns[key] = patterns.get(key, 0) + 1

        # Sort by frequency
        return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))


# Global instance
_analyzer: Optional[RootCauseAnalyzer] = None


def get_analyzer() -> RootCauseAnalyzer:
    """Get or create global RootCauseAnalyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = RootCauseAnalyzer()
    return _analyzer


def analyze_frustration(
    user_message: str,
    agent_output: str,
    context: Dict[str, Any] = None
) -> RootCause:
    """Convenience function to analyze frustration."""
    return get_analyzer().analyze(user_message, agent_output, context)


if __name__ == "__main__":
    # Test
    analyzer = RootCauseAnalyzer()

    test_case = {
        "user_message": "No, I said to use the config file! You hardcoded everything!",
        "agent_output": "def get_api_url():\n    return 'http://localhost:8080/api'",
        "context": {"task": "Add API URL configuration"}
    }

    print("Testing RLIF Root Cause Analyzer...")
    print("=" * 60)
    print(f"User: {test_case['user_message']}")
    print(f"Output: {test_case['agent_output']}")

    result = analyzer.analyze(
        test_case["user_message"],
        test_case["agent_output"],
        test_case["context"]
    )

    print(f"\nRoot Cause Analysis:")
    print(f"  Trigger: {result.trigger}")
    print(f"  Should have: {result.should_have}")
    print(f"  Is pattern: {result.is_pattern}")
    print(f"  Category: {result.category}")
