"""
Intent Gatekeeper - Capture and preserve user intent throughout execution.

First node in the swarm - extracts structured intent from user requests
and monitors for drift during task execution.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import skill registry for semantic comparison
try:
    from skills.skill_registry import SkillRegistry
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False


@dataclass
class UserIntent:
    """Structured representation of user intent."""
    goal: str                    # What the user wants to achieve
    constraints: List[str]       # Must do / must not do
    preferences: List[str]       # Nice to have
    anti_goals: List[str]        # Explicitly NOT wanted
    clarifications: List[str]    # Follow-up Q&A accumulated
    original_text: str           # Exact user words (preserved)
    extracted_at: str            # Timestamp
    confidence: float            # 0-1.0 extraction confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "constraints": self.constraints,
            "preferences": self.preferences,
            "anti_goals": self.anti_goals,
            "clarifications": self.clarifications,
            "original_text": self.original_text,
            "extracted_at": self.extracted_at,
            "confidence": self.confidence
        }

    def add_clarification(self, clarification: str):
        """Add a clarification from follow-up Q&A."""
        self.clarifications.append(clarification)


@dataclass
class AlignmentResult:
    """Result from alignment check."""
    is_aligned: bool
    alignment_score: float
    constraint_violations: List[str]
    anti_goal_violations: List[str]
    drift_reason: Optional[str] = None

    @property
    def needs_correction(self) -> bool:
        """Whether the work needs correction."""
        return not self.is_aligned or self.alignment_score < 0.5


class IntentGatekeeper:
    """First node - captures and preserves user intent."""

    # Keywords indicating constraints (must do / must not do)
    CONSTRAINT_KEYWORDS = [
        "must", "don't", "never", "always", "only", "require",
        "need", "important", "critical", "essential", "mandatory"
    ]

    # Keywords indicating preferences (nice to have)
    PREFERENCE_KEYWORDS = [
        "prefer", "if possible", "ideally", "would be nice",
        "optionally", "bonus", "extra", "also"
    ]

    # Keywords indicating anti-goals (explicitly NOT wanted)
    ANTI_GOAL_KEYWORDS = [
        "not", "without", "don't add", "no need", "skip",
        "avoid", "exclude", "leave out", "ignore"
    ]

    # Keywords for goal extraction
    GOAL_KEYWORDS = [
        "create", "build", "implement", "add", "fix", "update",
        "refactor", "modify", "change", "make", "generate", "write"
    ]

    def __init__(self):
        self._skill_registry = None

    def _get_skill_registry(self):
        """Lazy-load skill registry for semantic comparison."""
        if self._skill_registry is None and REGISTRY_AVAILABLE:
            self._skill_registry = SkillRegistry()
        return self._skill_registry

    def extract_intent(self, user_message: str) -> UserIntent:
        """
        Extract structured intent from user message.

        Args:
            user_message: Raw user request

        Returns:
            UserIntent with extracted components
        """
        sentences = self._split_sentences(user_message)

        goal = self._extract_goal(sentences, user_message)
        constraints = self._extract_constraints(sentences)
        preferences = self._extract_preferences(sentences)
        anti_goals = self._extract_anti_goals(sentences)
        confidence = self._calculate_confidence(goal, constraints, user_message)

        return UserIntent(
            goal=goal,
            constraints=constraints,
            preferences=preferences,
            anti_goals=anti_goals,
            clarifications=[],
            original_text=user_message,
            extracted_at=datetime.now().isoformat(),
            confidence=confidence
        )

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Split on sentence boundaries
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _extract_goal(self, sentences: List[str], full_text: str) -> str:
        """Extract the main goal from sentences."""
        # Look for sentences with goal keywords
        for sentence in sentences:
            lower = sentence.lower()
            for keyword in self.GOAL_KEYWORDS:
                if keyword in lower:
                    return sentence

        # Fallback: use first sentence or summarize
        if sentences:
            first = sentences[0]
            if len(first) < 200:
                return first
            return first[:200] + "..."

        return full_text[:200] if full_text else "Unknown goal"

    def _extract_constraints(self, sentences: List[str]) -> List[str]:
        """Extract constraint statements."""
        constraints = []
        for sentence in sentences:
            lower = sentence.lower()
            for keyword in self.CONSTRAINT_KEYWORDS:
                if keyword in lower:
                    # Clean up and add
                    clean = self._clean_constraint(sentence)
                    if clean and clean not in constraints:
                        constraints.append(clean)
                    break
        return constraints

    def _clean_constraint(self, sentence: str) -> str:
        """Clean up constraint text."""
        # Remove common filler words at start
        sentence = re.sub(r'^(please|can you|could you|i want you to)\s+', '', sentence, flags=re.IGNORECASE)
        return sentence.strip()

    def _extract_preferences(self, sentences: List[str]) -> List[str]:
        """Extract preference statements."""
        preferences = []
        for sentence in sentences:
            lower = sentence.lower()
            for keyword in self.PREFERENCE_KEYWORDS:
                if keyword in lower:
                    preferences.append(sentence)
                    break
        return preferences

    def _extract_anti_goals(self, sentences: List[str]) -> List[str]:
        """Extract anti-goal statements (what NOT to do)."""
        anti_goals = []
        for sentence in sentences:
            lower = sentence.lower()
            for keyword in self.ANTI_GOAL_KEYWORDS:
                if keyword in lower:
                    # Extract what to avoid
                    anti_goal = self._extract_anti_goal_target(sentence)
                    if anti_goal and anti_goal not in anti_goals:
                        anti_goals.append(anti_goal)
                    break
        return anti_goals

    def _extract_anti_goal_target(self, sentence: str) -> str:
        """Extract what specifically should be avoided."""
        # Patterns to extract anti-goal targets
        patterns = [
            r"(?:don't|do not|never|avoid|skip|without)\s+(.+)",
            r"no need (?:to|for)\s+(.+)",
            r"(?:exclude|leave out|ignore)\s+(.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return sentence

    def _calculate_confidence(self, goal: str, constraints: List[str], original: str) -> float:
        """Calculate confidence in intent extraction."""
        confidence = 0.5  # Base confidence

        # Goal extraction quality
        if goal and len(goal) > 10:
            confidence += 0.2

        # Constraints found
        if constraints:
            confidence += 0.1 * min(len(constraints), 3)

        # Original message clarity
        if len(original) > 50 and len(original) < 500:
            confidence += 0.1

        return min(confidence, 1.0)

    def check_alignment(self, current_work: str, intent: UserIntent) -> AlignmentResult:
        """
        Check if current work aligns with original intent.

        Args:
            current_work: Description or code of current work
            intent: Original user intent

        Returns:
            AlignmentResult with alignment status
        """
        # Check goal relevance
        goal_similarity = self._semantic_similarity(current_work, intent.goal)

        # Check constraint violations
        constraint_violations = []
        for constraint in intent.constraints:
            if self._violates_constraint(current_work, constraint):
                constraint_violations.append(constraint)

        # Check anti-goal pursuit
        anti_goal_violations = []
        for anti_goal in intent.anti_goals:
            if self._pursues_anti_goal(current_work, anti_goal):
                anti_goal_violations.append(anti_goal)

        is_aligned = (
            goal_similarity >= 0.5 and
            len(constraint_violations) == 0 and
            len(anti_goal_violations) == 0
        )

        drift_reason = None
        if not is_aligned:
            drift_reason = self._explain_drift(
                goal_similarity,
                constraint_violations,
                anti_goal_violations
            )

        return AlignmentResult(
            is_aligned=is_aligned,
            alignment_score=goal_similarity,
            constraint_violations=constraint_violations,
            anti_goal_violations=anti_goal_violations,
            drift_reason=drift_reason
        )

    def _semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        # Use skill registry embeddings if available
        registry = self._get_skill_registry()
        if registry and registry.vectorizer:
            try:
                from physics.math_utils import cosine_similarity_vectors
                emb1 = registry.compute_embedding(text1)
                emb2 = registry.compute_embedding(text2)
                if emb1 is not None and emb2 is not None:
                    return cosine_similarity_vectors(emb1, emb2)
            except Exception:
                pass

        # Fallback: word overlap
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0

    def _violates_constraint(self, work: str, constraint: str) -> bool:
        """Check if work violates a constraint."""
        work_lower = work.lower()
        constraint_lower = constraint.lower()

        # Check for "must" constraints
        if "must" in constraint_lower:
            # Extract what must be present
            match = re.search(r'must\s+(.+)', constraint_lower)
            if match:
                required = match.group(1).split()[0:3]  # First few words
                if not any(word in work_lower for word in required):
                    return True

        # Check for "don't" constraints
        if "don't" in constraint_lower or "never" in constraint_lower:
            # Extract what must not be present
            match = re.search(r"(?:don't|never)\s+(.+)", constraint_lower)
            if match:
                forbidden = match.group(1).split()[0:3]
                if any(word in work_lower for word in forbidden):
                    return True

        return False

    def _pursues_anti_goal(self, work: str, anti_goal: str) -> bool:
        """Check if work is pursuing an anti-goal."""
        work_lower = work.lower()
        anti_goal_lower = anti_goal.lower()

        # Check for significant overlap with anti-goal
        anti_words = set(anti_goal_lower.split())
        work_words = set(work_lower.split())

        overlap = len(anti_words & work_words)
        if overlap >= 2:  # If 2+ anti-goal words appear in work
            return True

        return False

    def _explain_drift(
        self,
        goal_similarity: float,
        constraint_violations: List[str],
        anti_goal_violations: List[str]
    ) -> str:
        """Explain why drift was detected."""
        reasons = []

        if goal_similarity < 0.5:
            reasons.append(f"Goal alignment low ({goal_similarity:.2f})")

        if constraint_violations:
            reasons.append(f"Constraint violations: {constraint_violations}")

        if anti_goal_violations:
            reasons.append(f"Pursuing anti-goals: {anti_goal_violations}")

        return "; ".join(reasons) if reasons else "Unknown drift"

    def inject_into_prompt(self, prompt: str, intent: UserIntent) -> str:
        """
        Inject intent context into downstream prompts.

        Args:
            prompt: Original prompt
            intent: User intent to inject

        Returns:
            Modified prompt with intent context
        """
        intent_block = f"""
## USER INTENT (Do not deviate)
GOAL: {intent.goal}
CONSTRAINTS: {', '.join(intent.constraints) or 'None specified'}
ANTI-GOALS (DO NOT DO): {', '.join(intent.anti_goals) or 'None specified'}
PREFERENCES: {', '.join(intent.preferences) or 'None specified'}
"""

        if intent.clarifications:
            intent_block += f"CLARIFICATIONS: {'; '.join(intent.clarifications)}\n"

        intent_block += """
Before completing, verify: "Does this output match the user's stated goal?"
"""

        return intent_block + "\n" + prompt

    def create_drift_correction_prompt(
        self,
        alignment: AlignmentResult,
        intent: UserIntent
    ) -> str:
        """
        Create a correction prompt when drift is detected.

        Args:
            alignment: Alignment check result
            intent: Original user intent

        Returns:
            Correction prompt to inject
        """
        correction = f"""
## DRIFT CORRECTION REQUIRED
The current work has drifted from the user's original intent.

DRIFT REASON: {alignment.drift_reason}

ORIGINAL GOAL: {intent.goal}
"""

        if alignment.constraint_violations:
            correction += f"""
VIOLATED CONSTRAINTS:
{chr(10).join('- ' + c for c in alignment.constraint_violations)}
"""

        if alignment.anti_goal_violations:
            correction += f"""
PURSUING ANTI-GOALS (STOP THIS):
{chr(10).join('- ' + a for a in alignment.anti_goal_violations)}
"""

        correction += """
Please correct course and ensure output matches the original intent.
"""
        return correction


# Global instance
_gatekeeper: Optional[IntentGatekeeper] = None


def get_gatekeeper() -> IntentGatekeeper:
    """Get or create global IntentGatekeeper instance."""
    global _gatekeeper
    if _gatekeeper is None:
        _gatekeeper = IntentGatekeeper()
    return _gatekeeper


def extract_intent(message: str) -> UserIntent:
    """Convenience function to extract intent."""
    return get_gatekeeper().extract_intent(message)


def check_alignment(work: str, intent: UserIntent) -> AlignmentResult:
    """Convenience function to check alignment."""
    return get_gatekeeper().check_alignment(work, intent)


if __name__ == "__main__":
    # Test
    gatekeeper = IntentGatekeeper()

    test_messages = [
        "Create a user authentication system. Must use JWT tokens. Don't add any OAuth support. Prefer stateless design if possible.",
        "Fix the bug in login.py. Never modify the database schema. Always keep backward compatibility.",
        "Refactor the payment module. Skip documentation for now. Must maintain existing API signatures.",
    ]

    print("Testing Intent Gatekeeper...")
    print("=" * 60)

    for msg in test_messages:
        print(f"\nMessage: {msg}")
        intent = gatekeeper.extract_intent(msg)
        print(f"  Goal: {intent.goal}")
        print(f"  Constraints: {intent.constraints}")
        print(f"  Preferences: {intent.preferences}")
        print(f"  Anti-goals: {intent.anti_goals}")
        print(f"  Confidence: {intent.confidence:.2f}")

        # Test prompt injection
        base_prompt = "Execute the following task:"
        enhanced = gatekeeper.inject_into_prompt(base_prompt, intent)
        print(f"\n  Enhanced prompt preview:")
        print("  " + enhanced[:300].replace("\n", "\n  ") + "...")
