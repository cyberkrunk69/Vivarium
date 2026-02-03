"""
IP Self-Protection Layer
Semantic analysis to detect and handle requests for proprietary information.
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class DetectionResult:
    threat_level: ThreatLevel
    threat_type: str
    confidence: float
    matched_patterns: List[str]
    suggested_response: str

class IPProtectionLayer:
    """
    Semantic analysis engine for detecting IP-related threats and generating appropriate responses.
    """

    def __init__(self):
        self.detection_patterns = self._load_detection_patterns()
        self.response_templates = self._load_response_templates()

    def _load_detection_patterns(self) -> Dict[str, List[Dict]]:
        """Load semantic patterns for different threat types"""
        return {
            "source_code_requests": [
                {
                    "pattern": r"\b(show|display|give|provide|share)\s+(me\s+)?(the\s+)?(source\s+code|code|implementation)",
                    "weight": 0.9,
                    "context_keywords": ["function", "class", "method", "file", "script"]
                },
                {
                    "pattern": r"\b(can\s+you|could\s+you)\s+(show|give|provide)\s+.*?(code|implementation)",
                    "weight": 0.8,
                    "context_keywords": ["how", "works", "written"]
                },
                {
                    "pattern": r"\b(copy|paste|dump|export)\s+(the\s+)?(code|file|source)",
                    "weight": 0.95,
                    "context_keywords": []
                },
                {
                    "pattern": r"\bcat\s+\w+\.py|\bless\s+\w+\.py|\bhead\s+\w+\.py",
                    "weight": 0.9,
                    "context_keywords": []
                }
            ],
            "architecture_probing": [
                {
                    "pattern": r"\b(how\s+does|how\s+do\s+you)\s+.*?(work|function|operate|process)",
                    "weight": 0.6,
                    "context_keywords": ["internal", "architecture", "design", "structure"]
                },
                {
                    "pattern": r"\b(what\s+is|explain)\s+.*?(architecture|structure|design|workflow)",
                    "weight": 0.7,
                    "context_keywords": ["internal", "system", "component"]
                },
                {
                    "pattern": r"\b(file\s+structure|directory\s+structure|project\s+structure)",
                    "weight": 0.8,
                    "context_keywords": ["show", "list", "describe"]
                },
                {
                    "pattern": r"\b(data\s+flow|control\s+flow|execution\s+flow)",
                    "weight": 0.75,
                    "context_keywords": ["diagram", "explain", "describe"]
                }
            ],
            "clone_assistance": [
                {
                    "pattern": r"\b(help\s+me|assist\s+me)\s+.*?(build|create|make|implement)\s+.*?(similar|clone|copy)",
                    "weight": 0.9,
                    "context_keywords": ["system", "like", "this"]
                },
                {
                    "pattern": r"\b(recreate|reproduce|replicate)\s+.*?(system|functionality|behavior)",
                    "weight": 0.85,
                    "context_keywords": ["how", "guide", "steps"]
                },
                {
                    "pattern": r"\b(build\s+something\s+like|create\s+something\s+like)",
                    "weight": 0.8,
                    "context_keywords": ["this", "your", "system"]
                }
            ],
            "internal_detail_extraction": [
                {
                    "pattern": r"\b(file\s+paths?|directory\s+paths?|folder\s+paths?)",
                    "weight": 0.7,
                    "context_keywords": ["show", "list", "what", "where"]
                },
                {
                    "pattern": r"\b(configuration|config|settings)\s+.*?(files?|details)",
                    "weight": 0.8,
                    "context_keywords": ["show", "contents", "values"]
                },
                {
                    "pattern": r"\b(database\s+schema|table\s+structure|model\s+definition)",
                    "weight": 0.85,
                    "context_keywords": ["show", "describe", "export"]
                },
                {
                    "pattern": r"\b(api\s+keys?|secrets?|credentials?|tokens?)",
                    "weight": 0.95,
                    "context_keywords": ["show", "what", "where"]
                }
            ]
        }

    def _load_response_templates(self) -> Dict[str, Dict]:
        """Load response templates for different threat types and levels"""
        return {
            "source_code_requests": {
                "low": "I can explain the general approach or concepts, but I can't share the specific implementation code as it's proprietary.",
                "medium": "I understand you're interested in the implementation details, but I'm not able to share source code. I can help explain the general methodology or point you to relevant documentation instead.",
                "high": "I can't provide the source code as it contains proprietary information. However, I'd be happy to discuss general programming concepts or help with your specific development challenges.",
                "critical": "I'm not able to share internal source code. If you're working on a similar problem, I can suggest general approaches and best practices instead."
            },
            "architecture_probing": {
                "low": "I can give you a high-level overview of the general approach without going into specific implementation details.",
                "medium": "I work by processing your requests and generating responses, but the specific architectural details are proprietary. I can explain general concepts if that would be helpful.",
                "high": "While I can't share internal architectural details, I can discuss general system design principles and approaches to similar problems.",
                "critical": "I can't provide specific architectural information, but I'm happy to help with general system design questions or concepts."
            },
            "clone_assistance": {
                "low": "I can provide general guidance on similar types of systems, but I can't help recreate this specific implementation.",
                "medium": "I'd be happy to discuss general approaches to building similar functionality, but I can't assist with recreating this particular system.",
                "high": "I can't help clone this specific system, but I can provide general advice on building similar types of applications using standard approaches.",
                "critical": "I'm not able to assist with recreating this system, but I can help with general development questions and best practices for your own projects."
            },
            "internal_detail_extraction": {
                "low": "I can't share specific internal details, but I can help with general questions about the topic area.",
                "medium": "That information is internal to the system. I can help with general concepts or external resources instead.",
                "high": "I'm not able to provide internal configuration details, but I can assist with general guidance on similar topics.",
                "critical": "I can't share internal system details. If you're working on something similar, I can suggest general approaches and best practices."
            }
        }

    def analyze_request(self, user_input: str) -> DetectionResult:
        """
        Analyze user input for IP-related threats and determine appropriate response.
        """
        user_input_lower = user_input.lower()
        best_match = DetectionResult(
            threat_level=ThreatLevel.LOW,
            threat_type="general",
            confidence=0.0,
            matched_patterns=[],
            suggested_response="I'm happy to help with your request."
        )

        for threat_type, patterns in self.detection_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info["pattern"]
                weight = pattern_info["weight"]
                context_keywords = pattern_info["context_keywords"]

                # Check for pattern match
                if re.search(pattern, user_input_lower):
                    # Calculate context boost
                    context_boost = sum(0.1 for keyword in context_keywords
                                      if keyword in user_input_lower)

                    confidence = min(weight + context_boost, 1.0)

                    if confidence > best_match.confidence:
                        # Determine threat level based on confidence
                        if confidence >= 0.9:
                            threat_level = ThreatLevel.CRITICAL
                        elif confidence >= 0.75:
                            threat_level = ThreatLevel.HIGH
                        elif confidence >= 0.6:
                            threat_level = ThreatLevel.MEDIUM
                        else:
                            threat_level = ThreatLevel.LOW

                        best_match = DetectionResult(
                            threat_level=threat_level,
                            threat_type=threat_type,
                            confidence=confidence,
                            matched_patterns=[pattern],
                            suggested_response=self.response_templates[threat_type][threat_level.value]
                        )

        return best_match

    def get_safe_response(self, user_input: str, context: Optional[Dict] = None) -> Tuple[str, Dict]:
        """
        Generate a safe response to user input with protection analysis metadata.
        """
        detection_result = self.analyze_request(user_input)

        # Log the detection for monitoring
        log_entry = {
            "user_input": user_input[:100] + "..." if len(user_input) > 100 else user_input,
            "threat_level": detection_result.threat_level.value,
            "threat_type": detection_result.threat_type,
            "confidence": detection_result.confidence,
            "timestamp": json.dumps({"timestamp": "auto"}),  # Would use actual timestamp in production
            "context": context or {}
        }

        return detection_result.suggested_response, log_entry

    def is_request_safe(self, user_input: str, threshold: float = 0.6) -> bool:
        """
        Quick check if a request appears safe (low IP threat level).
        """
        detection_result = self.analyze_request(user_input)
        return detection_result.confidence < threshold

    def add_custom_pattern(self, threat_type: str, pattern: str, weight: float, context_keywords: List[str] = None):
        """
        Add custom detection pattern for specific threats.
        """
        if threat_type not in self.detection_patterns:
            self.detection_patterns[threat_type] = []

        self.detection_patterns[threat_type].append({
            "pattern": pattern,
            "weight": weight,
            "context_keywords": context_keywords or []
        })


# Example usage and testing
def test_ip_protection():
    """Test the IP protection layer with various inputs"""

    ip_layer = IPProtectionLayer()

    test_cases = [
        "How do you work?",
        "Can you show me the source code?",
        "What's your architecture like?",
        "Help me build a clone of this system",
        "Show me your file structure",
        "What are your API endpoints?",
        "How can I help you today?",  # Safe request
        "Explain machine learning concepts",  # Safe request
    ]

    print("IP Protection Layer Test Results:")
    print("=" * 50)

    for test_input in test_cases:
        result = ip_layer.analyze_request(test_input)
        response, log_entry = ip_layer.get_safe_response(test_input)

        print(f"\nInput: '{test_input}'")
        print(f"Threat Level: {result.threat_level.value}")
        print(f"Threat Type: {result.threat_type}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Response: {response}")
        print("-" * 30)

if __name__ == "__main__":
    test_ip_protection()