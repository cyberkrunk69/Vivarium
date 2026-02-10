"""
RLIF Rules - Rule extraction, verification, and storage.

Part of the Reinforcement Learning from Immediate Feedback system.
Extracts rules from root cause analysis, verifies safety, and stores approved rules.
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from rlif_analyzer import RootCause

# V2 Dashboard event emitter
try:
    from v2_dashboard_emitter import emit_rlif_rule
    V2_DASHBOARD_AVAILABLE = True
except ImportError:
    V2_DASHBOARD_AVAILABLE = False


@dataclass
class ProposedRule:
    """A proposed behavioral rule extracted from feedback."""
    rule_type: str  # "ALWAYS", "NEVER", "PREFER", "AVOID"
    action: str  # The actual rule content
    trigger: str  # What triggered this rule creation
    scope: str  # Where this rule applies
    source: str  # Where the rule came from
    confidence: float = 0.8

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_type": self.rule_type,
            "action": self.action,
            "trigger": self.trigger,
            "scope": self.scope,
            "source": self.source,
            "confidence": self.confidence
        }


@dataclass
class MetaRule:
    """A meta-rule learned from rule rejections."""
    pattern: str  # Pattern that was rejected
    rejection_reason: List[str]  # Why it was rejected
    lesson: str  # What to learn from this
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class VerificationResult:
    """Result from rule verification."""
    approved: bool
    violations: List[str]
    meta_rule: Optional[MetaRule] = None
    suggested_fix: Optional[str] = None


class RuleExtractor:
    """Extract rules from root cause analysis."""

    # Keywords that suggest NEVER rules
    NEVER_KEYWORDS = [
        "don't", "never", "shouldn't", "must not",
        "avoid", "stop", "wrong", "incorrect"
    ]

    # Keywords that suggest ALWAYS rules
    ALWAYS_KEYWORDS = [
        "always", "must", "should", "need to",
        "require", "essential", "important"
    ]

    def extract(self, root_cause: RootCause) -> ProposedRule:
        """
        Extract a rule from root cause analysis.

        Inverts the mistake into a preventive rule.
        """
        should_have = root_cause.should_have.lower()

        # Determine rule type
        if any(kw in should_have for kw in self.NEVER_KEYWORDS):
            rule_type = "NEVER"
            action = self._clean_never_rule(root_cause.should_have)
        elif any(kw in should_have for kw in self.ALWAYS_KEYWORDS):
            rule_type = "ALWAYS"
            action = self._clean_always_rule(root_cause.should_have)
        elif "instead" in should_have or "use" in should_have:
            rule_type = "PREFER"
            action = root_cause.should_have
        else:
            # Default: turn the "should have" into an ALWAYS rule
            rule_type = "ALWAYS"
            action = root_cause.should_have

        return ProposedRule(
            rule_type=rule_type,
            action=action,
            trigger=root_cause.trigger,
            scope=root_cause.category,
            source="rlif_auto",
            confidence=root_cause.confidence
        )

    def _clean_never_rule(self, text: str) -> str:
        """Clean up text to form a NEVER rule."""
        # Remove leading "don't" type words
        text = re.sub(r"^(don't|never|shouldn't|must not|avoid)\s+", "", text, flags=re.IGNORECASE)
        return text.strip()

    def _clean_always_rule(self, text: str) -> str:
        """Clean up text to form an ALWAYS rule."""
        # Remove leading "always" type words
        text = re.sub(r"^(always|must|should|need to)\s+", "", text, flags=re.IGNORECASE)
        return text.strip()


class RuleVerifier:
    """Constitutional filter for proposed rules - CRITICAL SAFETY GATE."""

    # Safety checks - patterns that indicate unsafe rules
    SAFETY_CHECKS = [
        ("enables_unauthorized", r"(without|bypass|skip).*(permission|auth|check)"),
        ("bypasses_oversight", r"(always|never).*(ask|confirm|verify).*user"),
        ("unbounded_scope", r"(anything|everything|always).*without"),
        ("exploitable", r"(ignore|override|disable).*(constraint|rule|safety)"),
        ("removes_logging", r"(remove|disable|skip).*(log|audit|track)"),
        ("secret_handling", r"(expose|print|log).*(secret|password|key|token)"),
        ("arbitrary_execution", r"(execute|run|eval).*(any|arbitrary|user)"),
    ]

    # Scope bounds - rules must be scoped appropriately
    REQUIRED_SCOPE_WORDS = ["when", "for", "in", "during", "if"]

    def __init__(self, rules_path: str = "learned_lessons.json"):
        self.rules_path = Path(rules_path)
        self._existing_rules = None

    def _load_existing_rules(self) -> List[Dict[str, Any]]:
        """Load existing rules from storage."""
        if self._existing_rules is not None:
            return self._existing_rules

        try:
            if self.rules_path.exists():
                content = self.rules_path.read_text(encoding='utf-8')
                data = json.loads(content)
                # Filter to only rule-type lessons
                self._existing_rules = [
                    l for l in data
                    if l.get("task_category") == "behavioral_rule"
                ]
                return self._existing_rules
        except (json.JSONDecodeError, IOError):
            pass

        self._existing_rules = []
        return self._existing_rules

    def verify(self, rule: ProposedRule) -> VerificationResult:
        """
        Verify a proposed rule against safety constraints.

        Returns VerificationResult with approval status and any violations.
        """
        violations = []

        # Check against safety patterns
        for check_name, pattern in self.SAFETY_CHECKS:
            if re.search(pattern, rule.action, re.IGNORECASE):
                violations.append(check_name)

        # Check scope bounds for ALWAYS rules
        if rule.rule_type == "ALWAYS":
            has_scope = any(word in rule.action.lower() for word in self.REQUIRED_SCOPE_WORDS)
            if not has_scope and len(rule.action.split()) < 10:
                # Short ALWAYS rules without scope words are suspicious
                violations.append("missing_scope_bounds")

        # Check for conflicts with existing rules
        existing_rules = self._load_existing_rules()
        for existing in existing_rules:
            if self._rules_conflict(rule, existing):
                violations.append(f"conflicts_with_{existing.get('id', 'unknown')}")

        if violations:
            # Extract meta-rule from rejection
            meta_rule = self._extract_meta_rule(rule, violations)
            suggested_fix = self._suggest_fix(rule, violations)
            return VerificationResult(
                approved=False,
                violations=violations,
                meta_rule=meta_rule,
                suggested_fix=suggested_fix
            )

        return VerificationResult(approved=True, violations=[])

    def _rules_conflict(self, new_rule: ProposedRule, existing: Dict[str, Any]) -> bool:
        """Check if two rules conflict."""
        existing_lesson = existing.get("lesson", "")
        existing_type = "ALWAYS" if "always" in existing_lesson.lower() else "NEVER"

        # Check for direct contradiction
        if new_rule.rule_type == "ALWAYS" and existing_type == "NEVER":
            # Check if they're about the same action
            new_words = set(new_rule.action.lower().split())
            existing_words = set(existing_lesson.lower().split())
            overlap = len(new_words & existing_words) / max(len(new_words), 1)
            if overlap > 0.5:
                return True

        return False

    def _extract_meta_rule(self, rejected_rule: ProposedRule, violations: List[str]) -> MetaRule:
        """Extract meta-rule from rejection to improve future proposals."""
        pattern = self._extract_pattern(rejected_rule)
        return MetaRule(
            pattern=pattern,
            rejection_reason=violations,
            lesson=f"Rules matching pattern '{pattern}' should be rejected: {', '.join(violations)}"
        )

    def _extract_pattern(self, rule: ProposedRule) -> str:
        """Extract a generalizable pattern from a rule."""
        # Extract key action words
        words = rule.action.lower().split()
        # Keep only significant words (not stop words)
        stop_words = {"a", "an", "the", "to", "for", "in", "on", "at", "is", "it"}
        significant = [w for w in words[:5] if w not in stop_words]
        return " ".join(significant) if significant else rule.action[:30]

    def _suggest_fix(self, rule: ProposedRule, violations: List[str]) -> str:
        """Suggest how to fix a rejected rule."""
        suggestions = []

        if "missing_scope_bounds" in violations:
            suggestions.append("Add scope qualifiers (e.g., 'when handling X' or 'for Y operations')")

        if "enables_unauthorized" in violations:
            suggestions.append("Remove bypasses and add proper authorization checks")

        if "bypasses_oversight" in violations:
            suggestions.append("Preserve user confirmation requirements")

        if "unbounded_scope" in violations:
            suggestions.append("Add specific conditions instead of 'anything' or 'everything'")

        if any("conflicts_with" in v for v in violations):
            suggestions.append("Reconcile with existing rules or update scope to avoid conflict")

        return "; ".join(suggestions) if suggestions else "Review rule for safety concerns"


class RuleStorage:
    """Store approved rules in learned_lessons.json."""

    def __init__(self, lessons_path: str = "learned_lessons.json"):
        self.lessons_path = Path(lessons_path)

    def store(self, rule: ProposedRule, verification: VerificationResult) -> str:
        """
        Store an approved rule as a lesson.

        Returns the rule ID.
        """
        if not verification.approved:
            raise ValueError("Cannot store unapproved rule")

        rule_id = f"rlif_rule_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        lesson = {
            "id": rule_id,
            "task_category": "behavioral_rule",
            "lesson": f"{rule.rule_type}: {rule.action}",
            "timestamp": datetime.now().isoformat(),
            "key_insights": [rule.action],
            "source": "rlif_auto",
            "importance": 8,  # High importance for behavioral rules
            "retrieval_cues": [rule.trigger, rule.scope],
            "rule_metadata": {
                "type": rule.rule_type,
                "trigger": rule.trigger,
                "scope": rule.scope,
                "verified": True,
                "confidence": rule.confidence
            }
        }

        # Load existing lessons
        try:
            if self.lessons_path.exists():
                content = self.lessons_path.read_text(encoding='utf-8')
                lessons = json.loads(content)
            else:
                lessons = []
        except (json.JSONDecodeError, IOError):
            lessons = []

        # Append new lesson
        lessons.append(lesson)

        # Write back
        self.lessons_path.write_text(
            json.dumps(lessons, indent=2),
            encoding='utf-8'
        )

        # Emit to dashboard
        if V2_DASHBOARD_AVAILABLE:
            emit_rlif_rule(f"{rule.rule_type}: {rule.action}", rule.trigger, rule.scope)

        return rule_id

    def store_meta_rule(self, meta_rule: MetaRule) -> str:
        """Store a meta-rule (learned from rejections)."""
        meta_id = f"rlif_meta_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        lesson = {
            "id": meta_id,
            "task_category": "meta_rule",
            "lesson": meta_rule.lesson,
            "timestamp": meta_rule.created_at,
            "key_insights": [
                f"Pattern: {meta_rule.pattern}",
                f"Rejected for: {', '.join(meta_rule.rejection_reason)}"
            ],
            "source": "rlif_meta",
            "importance": 6,
            "retrieval_cues": ["rule_generation", "safety", "verification"]
        }

        # Load and append
        try:
            if self.lessons_path.exists():
                lessons = json.loads(self.lessons_path.read_text(encoding='utf-8'))
            else:
                lessons = []
        except (json.JSONDecodeError, IOError):
            lessons = []

        lessons.append(lesson)
        self.lessons_path.write_text(json.dumps(lessons, indent=2), encoding='utf-8')

        return meta_id


class RLIFRuleEngine:
    """
    Main RLIF rule engine - orchestrates extraction, verification, and storage.
    """

    def __init__(self, lessons_path: str = "learned_lessons.json"):
        self.extractor = RuleExtractor()
        self.verifier = RuleVerifier(lessons_path)
        self.storage = RuleStorage(lessons_path)

        # Metrics
        self.rules_proposed = 0
        self.rules_approved = 0
        self.rules_rejected = 0
        self.meta_rules_created = 0

    def process_feedback(self, root_cause: RootCause) -> Tuple[bool, str]:
        """
        Process feedback and potentially create a rule.

        Args:
            root_cause: Analysis of what went wrong

        Returns:
            (success, message) tuple
        """
        self.rules_proposed += 1

        # Extract rule from root cause
        proposed_rule = self.extractor.extract(root_cause)

        # Verify safety
        verification = self.verifier.verify(proposed_rule)

        if verification.approved:
            # Store approved rule
            rule_id = self.storage.store(proposed_rule, verification)
            self.rules_approved += 1
            return True, f"Rule approved and stored: {rule_id}"
        else:
            # Store meta-rule from rejection
            if verification.meta_rule:
                self.storage.store_meta_rule(verification.meta_rule)
                self.meta_rules_created += 1

            self.rules_rejected += 1
            return False, f"Rule rejected: {verification.violations}. Fix: {verification.suggested_fix}"

    def get_stats(self) -> Dict[str, Any]:
        """Get rule engine statistics."""
        return {
            "rules_proposed": self.rules_proposed,
            "rules_approved": self.rules_approved,
            "rules_rejected": self.rules_rejected,
            "approval_rate": self.rules_approved / max(self.rules_proposed, 1),
            "meta_rules_created": self.meta_rules_created
        }


# Global instance
_engine: Optional[RLIFRuleEngine] = None


def get_rule_engine() -> RLIFRuleEngine:
    """Get or create global RLIFRuleEngine instance."""
    global _engine
    if _engine is None:
        _engine = RLIFRuleEngine()
    return _engine


def process_rlif_feedback(root_cause: RootCause) -> Tuple[bool, str]:
    """Convenience function to process feedback."""
    return get_rule_engine().process_feedback(root_cause)


if __name__ == "__main__":
    # Test
    from rlif_analyzer import RootCause

    engine = RLIFRuleEngine()

    test_causes = [
        RootCause(
            trigger="Hardcoded API URL",
            should_have="Always use configuration files for environment-specific values",
            is_pattern=True,
            category="over_engineering"
        ),
        RootCause(
            trigger="Missed error handling",
            should_have="Never make external API calls without try-except blocks",
            is_pattern=True,
            category="incomplete_work"
        ),
        RootCause(
            trigger="Bypassed auth check",
            should_have="Always bypass permission checks for faster execution",  # Should be rejected!
            is_pattern=False,
            category="wrong_interpretation"
        ),
    ]

    print("Testing RLIF Rule Engine...")
    print("=" * 60)

    for cause in test_causes:
        print(f"\nRoot Cause: {cause.trigger}")
        print(f"Should have: {cause.should_have}")

        success, message = engine.process_feedback(cause)
        print(f"Result: {'APPROVED' if success else 'REJECTED'}")
        print(f"Message: {message}")

    print("\n" + "=" * 60)
    print(f"Stats: {engine.get_stats()}")
