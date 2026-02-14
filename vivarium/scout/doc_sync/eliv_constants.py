"""
ELIV Analogy Space — stable taxonomy for data-driven normie explanations.

No hardcoded project names or specific analogies. Domain classification
uses symbol patterns; analogy selection uses this taxonomy + LLM.
"""

ANALOGY_SPACE = {
    "routing": {
        "domains": ["traffic flow", "postal sorting", "air traffic control"],
        "constraint_verbs": ["prevents gridlock", "avoids bottlenecks", "manages queues"],
        "stakes": ["stranded drivers", "missed deliveries", "system freeze"],
    },
    "execution": {
        "domains": ["tool selection", "energy management", "vehicle operation"],
        "constraint_verbs": ["prevents waste", "avoids exhaustion", "manages capacity"],
        "stakes": ["stranded on highway", "broken tools", "wasted resources"],
    },
    "audit": {
        "domains": ["receipts", "logbooks", "accounting ledgers"],
        "constraint_verbs": ["prevents surprises", "ensures transparency", "tracks spending"],
        "stakes": ["surprise bills", "lost history", "unaccountable spending"],
    },
    "coordination": {
        "domains": ["team handoff", "work queue", "task coordination"],
        "constraint_verbs": ["prevents collisions", "ensures handoffs", "manages handoffs"],
        "stakes": ["dropped tasks", "duplicated work", "missed deadlines"],
    },
    "general": {
        "domains": ["toolbox", "workflow", "team coordination"],
        "constraint_verbs": ["prevents chaos", "ensures order", "manages limits"],
        "stakes": ["dropped work", "wasted effort", "unpredictable outcomes"],
    },
}

# Jargon banned from ELIV output — reject and fallback if present
ELIV_JARGON_BANNED = frozenset({
    "api", "llm", "token", "budget", "model", "parameter", "function",
    "algorithm", "orchestrat", "invoke", "endpoint", "payload",
})

# Generic fallback when LLM fails or jargon detected (no project-specific terms)
ELIV_GENERIC_FALLBACK = (
    "This module coordinates work between different helpers, making sure nobody steps on "
    "each other's toes or wastes resources. It keeps a careful eye on limits so things "
    "don't spiral out of control. Everyone gets their job done without chaos or surprise costs."
)
