"""Safe domain transfer primitives.

This module replaces a previously corrupted/concatenated file and provides a
small, deterministic API for cross-domain transfer experiments.

Security goals:
- no dynamic code execution (no eval/exec),
- no subprocess/network side effects,
- fail clearly for missing adapters/encoders.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
import math
from typing import Any, Callable, Dict, List, Optional, Tuple


def _to_float_list(values: Any) -> List[float]:
    if values is None:
        return []
    if isinstance(values, list):
        return [float(v) for v in values]
    raise TypeError("Embedding must be a list of numeric values")


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    length = min(len(a), len(b))
    if length == 0:
        return 0.0

    dot = sum(a[i] * b[i] for i in range(length))
    norm_a = math.sqrt(sum(x * x for x in a[:length]))
    norm_b = math.sqrt(sum(y * y for y in b[:length]))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


@dataclass
class TaskRepresentation:
    """Generic task container used by transfer utilities."""

    domain: str
    description: str = ""
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: List[float] = field(default_factory=list)

    def serialize(self) -> str:
        payload = {
            "domain": self.domain,
            "description": self.description,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "metadata": self.metadata,
            "embedding": self.embedding,
        }
        return json.dumps(payload, sort_keys=True)

    @classmethod
    def deserialize(cls, serialized: str) -> "TaskRepresentation":
        data = json.loads(serialized)
        data["embedding"] = _to_float_list(data.get("embedding", []))
        return cls(**data)

    def fingerprint(self) -> str:
        return sha256(self.serialize().encode("utf-8")).hexdigest()

    def similarity(self, other: "TaskRepresentation") -> float:
        return _cosine_similarity(self.embedding, other.embedding)


class AbstractTaskRepresentation:
    """Minimal wrapper for payload-based transfer APIs."""

    def __init__(self, domain: str, payload: Any):
        self.domain = domain
        self.payload = payload
        self.embedding: Optional[List[float]] = None

    def encode(self) -> List[float]:
        encoder = TransferRegistry.get_encoder(self.domain)
        if encoder is None:
            raise ValueError(f"No encoder registered for domain '{self.domain}'")
        encoded = encoder(self.payload)
        self.embedding = _to_float_list(encoded)
        return self.embedding

    def decode(self, target_domain: str) -> Any:
        bridge = TransferRegistry.get_bridge(self.domain, target_domain)
        if bridge is None:
            raise ValueError(f"No bridge from '{self.domain}' to '{target_domain}'")
        if self.embedding is None:
            self.encode()
        return bridge.decode(self.embedding or [])


class DomainBridge:
    """In-memory registry for source->target adapter functions."""

    _global_adapters: Dict[Tuple[str, str], Callable[[Callable], Callable]] = {}

    def __init__(self):
        self._bridges: Dict[Tuple[str, str], Callable[[Callable, TaskRepresentation], Any]] = {}

    def register(
        self,
        source_domain: str,
        target_domain: str,
        adapter: Callable[[Callable, TaskRepresentation], Any],
    ) -> None:
        self._bridges[(source_domain, target_domain)] = adapter

    def transfer(
        self,
        source_skill: Callable,
        source_task: TaskRepresentation,
        target_domain: str,
    ) -> Any:
        source_domain = source_task.metadata.get("domain", source_task.domain)
        key = (source_domain, target_domain)
        adapter = self._bridges.get(key)
        if adapter is None:
            raise ValueError(f"No bridge registered for {source_domain}->{target_domain}")
        return adapter(source_skill, source_task)

    @classmethod
    def register_adapter(cls, src: str, tgt: str):
        """Decorator-style adapter registration for compatibility."""

        def decorator(adapter_fn: Callable[[Callable], Callable]):
            cls._global_adapters[(src, tgt)] = adapter_fn
            return adapter_fn

        return decorator

    @classmethod
    def adapt(cls, src_domain: str, tgt_domain: str, skill_name: str) -> Callable:
        """Compatibility shim that adapts a registered skill."""
        skill = SkillRegistry.get(src_domain, skill_name)
        if skill is None:
            raise ValueError(f"Skill {skill_name} not found in {src_domain}")
        adapter = cls._global_adapters.get((src_domain, tgt_domain))
        if adapter is None:
            raise NotImplementedError(f"No adapter from {src_domain} to {tgt_domain}")
        return adapter(skill)


class TransferMetrics:
    """Utility methods for transfer score calculations."""

    @staticmethod
    def efficiency(raw_score: float, baseline_score: float) -> float:
        if baseline_score == 0:
            return float("inf") if raw_score > 0 else 0.0
        return (raw_score - baseline_score) / baseline_score

    @staticmethod
    def relative_gain(baseline: float, transferred: float) -> float:
        if baseline == 0:
            return float("inf") if transferred > 0 else 0.0
        return (transferred - baseline) / baseline

    @staticmethod
    def cosine_similarity(source_embedding: List[float], target_embedding: List[float]) -> float:
        return _cosine_similarity(source_embedding, target_embedding)


class TransferEngine:
    """Simple transfer orchestrator."""

    def __init__(self, bridge: Optional[DomainBridge] = None):
        self.bridge = bridge or DomainBridge()

    def execute_transfer(
        self,
        source_skill: Callable,
        source_task: TaskRepresentation,
        target_task: TaskRepresentation,
        evaluator: Callable[[Any, TaskRepresentation], float],
    ) -> Dict[str, float]:
        target_domain = target_task.metadata.get("domain", target_task.domain)
        result = self.bridge.transfer(source_skill, source_task, target_domain)
        raw_score = float(evaluator(result, target_task))
        baseline_score = float(evaluator(None, target_task))
        return {
            "raw_score": raw_score,
            "baseline_score": baseline_score,
            "efficiency": TransferMetrics.efficiency(raw_score, baseline_score),
        }

    def transfer(self, source_task: AbstractTaskRepresentation, target_type: str) -> Any:
        if source_task.embedding is None:
            source_task.encode()
        bridge = TransferRegistry.get_bridge(source_task.domain, target_type)
        if bridge is None:
            raise ValueError(f"No bridge from '{source_task.domain}' to '{target_type}'")
        return bridge.decode(source_task.embedding or [])


class _DecoderBridge:
    """Internal adapter wrapper used by TransferRegistry."""

    def __init__(self, decoder: Callable[[List[float]], Any]):
        self._decoder = decoder

    def decode(self, embedding: List[float]) -> Any:
        return self._decoder(embedding)


class TransferRegistry:
    """Global registry for encoders and bridges."""

    _encoders: Dict[str, Callable[[Any], List[float]]] = {}
    _bridges: Dict[Tuple[str, str], _DecoderBridge] = {}

    @classmethod
    def register_encoder(cls, domain: str, encoder: Callable[[Any], List[float]]) -> None:
        cls._encoders[domain] = encoder

    @classmethod
    def get_encoder(cls, domain: str) -> Optional[Callable[[Any], List[float]]]:
        return cls._encoders.get(domain)

    @classmethod
    def register_bridge(cls, source_domain: str, target_domain: str, bridge: Any) -> None:
        # Accept either an object exposing decode(embedding) or a callable.
        if callable(bridge) and not hasattr(bridge, "decode"):
            cls._bridges[(source_domain, target_domain)] = _DecoderBridge(bridge)
            return
        if hasattr(bridge, "decode") and callable(getattr(bridge, "decode")):
            cls._bridges[(source_domain, target_domain)] = bridge
            return
        raise TypeError("Bridge must be callable or expose a decode() method")

    @classmethod
    def get_bridge(cls, source_domain: str, target_domain: str):
        return cls._bridges.get((source_domain, target_domain))

    @classmethod
    def transfer(cls, src_task: Dict[str, Any], target_type: str) -> Any:
        source_type = src_task.get("type")
        payload = src_task.get("content")
        if not source_type:
            raise ValueError("src_task['type'] is required")

        task = AbstractTaskRepresentation(source_type, payload)
        embedding = task.encode()

        bridge = cls.get_bridge(source_type, target_type)
        if bridge is None:
            raise ValueError(f"No bridge from '{source_type}' to '{target_type}'")
        return bridge.decode(embedding)


class SkillRegistry:
    """Minimal skill registry used by DomainBridge.adapt compatibility layer."""

    _skills: Dict[Tuple[str, str], Callable] = {}

    @classmethod
    def register(cls, domain: str, name: str):
        def decorator(fn: Callable):
            cls._skills[(domain, name)] = fn
            return fn

        return decorator

    @classmethod
    def get(cls, domain: str, name: str) -> Optional[Callable]:
        return cls._skills.get((domain, name))
