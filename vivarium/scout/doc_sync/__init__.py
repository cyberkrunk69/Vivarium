"""
Scout doc_sync — Hybrid documentation system.

Deterministic fact extraction (AST) + constrained LLM prose synthesis.
Facts are extracted from source code. Prose is synthesized from facts only.
Never the twain shall meet.
"""

from vivarium.scout.doc_sync.ast_facts import (
    ASTFactExtractor,
    ControlFlowFact,
    ModuleFacts,
    SymbolFact,
)
from vivarium.scout.doc_sync.synthesizer import (
    ConstrainedDocSynthesizer,
    ReasoningDocSynthesizer,
    RichDocSynthesizer,
)

__all__ = [
    "ASTFactExtractor",
    "ConstrainedDocSynthesizer",
    "ControlFlowFact",
    "ModuleFacts",
    "ReasoningDocSynthesizer",
    "RichDocSynthesizer",
    "SymbolFact",
]
