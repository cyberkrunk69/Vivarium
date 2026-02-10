"""
RLIF Sentiment Detector - FREE sentiment detection via regex/keywords.

Part of the Reinforcement Learning from Immediate Feedback system.
Detects user frustration, approval, and corrections without LLM calls.
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SentimentResult:
    """Result from sentiment detection."""
    sentiment: str  # "positive", "negative", "neutral"
    trigger_analysis: bool  # Whether to trigger root cause analysis
    confidence: float = 1.0
    matched_patterns: List[str] = None

    def __post_init__(self):
        if self.matched_patterns is None:
            self.matched_patterns = []


class SentimentDetector:
    """FREE sentiment detection via regex/keywords."""

    # Frustration indicators - user is unhappy with output
    FRUSTRATION_PATTERNS = [
        (r"\b(whoa|wait|no|wrong|stop)\b", "direct_rejection"),
        (r"didn't I (say|tell|ask)", "repeat_frustration"),
        (r"are you not going to", "expectation_gap"),
        (r"I (already|just) (said|told)", "repetition_frustration"),
        (r"\?{2,}", "excessive_questions"),
        (r"!{2,}", "excessive_exclamation"),
        (r"\b(ugh|argh|sigh)\b", "frustration_expression"),
        (r"\b(useless|worthless|terrible|awful)\b", "quality_complaint"),
        (r"why (didn't|won't|can't) you", "capability_frustration"),
        (r"that's not what I", "mismatch_complaint"),
        (r"you (missed|forgot|ignored)", "oversight_complaint"),
        (r"please (read|listen|pay attention)", "attention_request"),
    ]

    # Approval indicators - user is happy
    APPROVAL_PATTERNS = [
        (r"\b(perfect|exactly|love it|great|good|nice|excellent)\b", "positive_adjective"),
        (r"that's (right|correct|it|what I wanted)", "confirmation"),
        (r"yes[,.]?\s*(that|this)", "affirmation"),
        (r"\b(thanks|thank you|awesome)\b", "gratitude"),
        (r"(well done|good job|nice work)", "praise"),
        (r"\b(works|working|fixed)\b", "functional_confirmation"),
    ]

    # Correction indicators - user is providing specific correction
    CORRECTION_PATTERNS = [
        (r"no[,.]?\s*(it should|use|try)", "redirect_correction"),
        (r"instead[,.]?\s*(of|use)", "alternative_correction"),
        (r"not\s+\w+[,.]?\s*(but|use)", "negation_correction"),
        (r"change.*to\s", "explicit_change"),
        (r"replace.*with\s", "replacement_instruction"),
        (r"should (be|have|use)", "should_correction"),
        (r"actually[,.]?\s*(it|I|the)", "correction_marker"),
        (r"I meant", "clarification"),
    ]

    # Confusion indicators - user doesn't understand
    CONFUSION_PATTERNS = [
        (r"what (do you mean|is this)", "comprehension_issue"),
        (r"I don't (understand|get)", "explicit_confusion"),
        (r"can you (explain|clarify)", "explanation_request"),
        (r"how (does|is) (this|that)", "understanding_question"),
        (r"\?\s*\?", "repeated_question"),
    ]

    def detect(self, user_message: str) -> SentimentResult:
        """
        Detect sentiment from user message.

        Args:
            user_message: The user's response to agent output

        Returns:
            SentimentResult with sentiment classification
        """
        message_lower = user_message.lower()
        matched_patterns = []

        # Score each category
        frustration_score = 0
        for pattern, name in self.FRUSTRATION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                frustration_score += 1
                matched_patterns.append(f"frustration:{name}")

        approval_score = 0
        for pattern, name in self.APPROVAL_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                approval_score += 1
                matched_patterns.append(f"approval:{name}")

        correction_detected = False
        for pattern, name in self.CORRECTION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                correction_detected = True
                matched_patterns.append(f"correction:{name}")

        confusion_detected = False
        for pattern, name in self.CONFUSION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                confusion_detected = True
                matched_patterns.append(f"confusion:{name}")

        # Decision logic
        if frustration_score >= 2 or correction_detected:
            return SentimentResult(
                sentiment="negative",
                trigger_analysis=True,
                confidence=min(1.0, 0.5 + frustration_score * 0.2),
                matched_patterns=matched_patterns
            )
        elif confusion_detected:
            return SentimentResult(
                sentiment="negative",
                trigger_analysis=True,  # Confusion also triggers analysis
                confidence=0.7,
                matched_patterns=matched_patterns
            )
        elif approval_score >= 1:
            return SentimentResult(
                sentiment="positive",
                trigger_analysis=False,
                confidence=min(1.0, 0.6 + approval_score * 0.2),
                matched_patterns=matched_patterns
            )
        else:
            return SentimentResult(
                sentiment="neutral",
                trigger_analysis=False,
                confidence=0.5,
                matched_patterns=matched_patterns
            )

    def extract_correction_content(self, user_message: str) -> Optional[str]:
        """
        Extract the actual correction content from a correction message.

        Returns the part after "instead use", "should be", etc.
        """
        patterns = [
            r"(?:instead|rather)[,.]?\s*(?:of.*?)?\s*(?:use|try)\s+(.+)",
            r"(?:it )?\s*should (?:be|use|have)\s+(.+)",
            r"change.*?to\s+(.+)",
            r"replace.*?with\s+(.+)",
            r"I meant\s+(.+)",
            r"actually[,.]?\s*(?:it's|its|the)\s+(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, user_message, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def get_frustration_trigger(self, user_message: str) -> Optional[str]:
        """
        Identify what specifically triggered user frustration.

        Returns a brief description of the trigger if found.
        """
        message_lower = user_message.lower()

        # Look for specific complaint patterns
        triggers = {
            r"you (missed|forgot|ignored) (the |my )?(\w+)": "Missed: {}",
            r"didn't.*?(follow|do|implement|add)\s+(.+?)[\.\?!]": "Didn't: {}",
            r"where('s| is) (the |my )?(.+?)[\.\?!]": "Missing: {}",
            r"why.*?no\s+(.+?)[\.\?!]": "Expected: {}",
        }

        for pattern, template in triggers.items():
            match = re.search(pattern, message_lower)
            if match:
                return template.format(match.group(match.lastindex))

        return None


# Global instance
_detector: Optional[SentimentDetector] = None


def get_detector() -> SentimentDetector:
    """Get or create global SentimentDetector instance."""
    global _detector
    if _detector is None:
        _detector = SentimentDetector()
    return _detector


def detect_sentiment(message: str) -> SentimentResult:
    """Convenience function to detect sentiment."""
    return get_detector().detect(message)


if __name__ == "__main__":
    # Test cases
    detector = SentimentDetector()

    test_messages = [
        "Perfect! That's exactly what I wanted.",
        "No, that's wrong. Use the other function instead.",
        "Whoa wait, I didn't ask for that!",
        "Thanks, this looks good.",
        "Didn't I already tell you to use the config file??",
        "Can you explain what this does?",
        "Ugh, you missed the error handling again.",
        "Yes, that's it!",
        "I don't understand this code.",
        "Replace the hardcoded value with a constant.",
    ]

    print("Testing RLIF Sentiment Detector...")
    print("=" * 60)

    for msg in test_messages:
        result = detector.detect(msg)
        print(f"\nMessage: {msg}")
        print(f"  Sentiment: {result.sentiment}")
        print(f"  Trigger analysis: {result.trigger_analysis}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Patterns: {result.matched_patterns}")
