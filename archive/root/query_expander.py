"""
Query Expansion Module

Expands search queries with synonyms, related technical terms, and extracted keywords
to improve retrieval accuracy for skills and lessons.
"""

import re
from typing import List, Set


# Technical term mappings for common concepts
TECHNICAL_SYNONYMS = {
    "error": ["exception", "failure", "bug", "issue"],
    "fix": ["repair", "resolve", "correct", "patch"],
    "test": ["testing", "verification", "validation", "coverage"],
    "config": ["configuration", "settings", "parameters", "options"],
    "optimize": ["optimization", "improve", "performance", "speedup"],
    "refactor": ["refactoring", "restructure", "cleanup", "rewrite"],
    "implement": ["implementation", "create", "build", "develop"],
    "duplicate": ["duplication", "redundant", "repeated", "copy"],
    "centralize": ["centralization", "consolidate", "unify", "merge"],
    "quality": ["QA", "validation", "review", "verification"],
    "feedback": ["review", "critique", "evaluation", "assessment"],
    "memory": ["storage", "cache", "persistence", "retention"],
    "synthesis": ["consolidation", "merging", "integration", "aggregation"],
    "retrieval": ["search", "query", "lookup", "find"],
    "embedding": ["vector", "representation", "encoding", "similarity"],
    "complexity": ["difficulty", "sophistication", "advanced", "intricate"],
    "task": ["job", "work", "operation", "activity"],
    "skill": ["capability", "ability", "function", "technique"],
    "lesson": ["insight", "learning", "pattern", "knowledge"],
    "code": ["implementation", "source", "program", "script"],
    "prompt": ["instruction", "message", "input", "query"],
    "agent": ["worker", "executor", "process", "system"],
    "role": ["responsibility", "function", "position", "part"]
}

# Common abbreviation expansions
ABBREVIATIONS = {
    "kg": "knowledge graph",
    "dspy": "dspy prompt optimization",
    "qa": "quality assurance",
    "api": "application programming interface",
    "cli": "command line interface",
    "json": "json data format",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "tfidf": "term frequency inverse document frequency",
    "lats": "language agent tree search",
    "camel": "communicative agents",
}

# Domain-specific technical terms
RELATED_TERMS = {
    "prompt": ["dspy", "optimization", "few-shot", "chain-of-thought"],
    "skill": ["voyager", "composition", "registry", "reuse"],
    "lesson": ["reflection", "synthesis", "memory", "learning"],
    "error": ["categorization", "handling", "recovery", "debugging"],
    "quality": ["critic", "review", "feedback", "assessment"],
    "complexity": ["adaptive", "threshold", "scoring", "detection"],
    "role": ["camel", "decomposition", "planner", "coder", "reviewer"],
    "memory": ["synthesis", "reflection", "consolidation", "archival"],
    "retrieval": ["embedding", "similarity", "semantic", "tfidf"],
    "graph": ["knowledge", "node", "edge", "relation"],
}


def expand_query(query: str) -> List[str]:
    """
    Expand query with synonyms, related technical terms, and extracted keywords.

    Args:
        query: Original search query string

    Returns:
        List of expanded terms including original query words, synonyms, and related terms
    """
    expanded_terms = []
    query_lower = query.lower()

    # Add original query words (filter out short stopwords)
    words = re.findall(r'\b\w+\b', query_lower)
    significant_words = [w for w in words if len(w) > 2]
    expanded_terms.extend(significant_words)

    # Expand abbreviations
    for abbrev, full_term in ABBREVIATIONS.items():
        if abbrev in query_lower:
            expanded_terms.append(full_term)

    # Add synonyms for each significant word
    for word in significant_words:
        if word in TECHNICAL_SYNONYMS:
            expanded_terms.extend(TECHNICAL_SYNONYMS[word])

    # Add related technical terms
    for word in significant_words:
        if word in RELATED_TERMS:
            expanded_terms.extend(RELATED_TERMS[word])

    # Extract quoted phrases (exact match terms)
    quoted_phrases = re.findall(r'"([^"]+)"', query)
    expanded_terms.extend(quoted_phrases)

    # Extract technical patterns (arXiv references, function names, etc.)
    arxiv_refs = re.findall(r'arxiv[:\s]*\d+\.\d+', query_lower)
    expanded_terms.extend(arxiv_refs)

    # Remove duplicates while preserving order
    seen: Set[str] = set()
    unique_expanded = []
    for term in expanded_terms:
        if term not in seen:
            seen.add(term)
            unique_expanded.append(term)

    return unique_expanded


def get_expansion_log(original_query: str, expanded_terms: List[str]) -> str:
    """
    Generate a log message showing query expansion details.

    Args:
        original_query: The original query string
        expanded_terms: List of expanded terms

    Returns:
        Formatted log string showing expansion details
    """
    added_terms = [term for term in expanded_terms if term not in original_query.lower()]

    log_msg = f"[QUERY EXPANSION]\n"
    log_msg += f"  Original: {original_query}\n"
    log_msg += f"  Expanded terms count: {len(expanded_terms)}\n"

    if added_terms:
        log_msg += f"  Added terms: {', '.join(added_terms[:10])}"
        if len(added_terms) > 10:
            log_msg += f" ... (+{len(added_terms) - 10} more)"
    else:
        log_msg += f"  No expansion needed"

    return log_msg
