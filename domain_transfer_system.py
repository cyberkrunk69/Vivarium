"""
Domain Transfer System
----------------------
Provides a lightweight framework for representing tasks abstractly,
mapping skills across domains, measuring transfer efficiency, and
bridging domain‑specific implementations.

The design is intentionally modular so it can be integrated with the
existing swarm‑based code‑generation infrastructure without invasive
changes.
"""

from typing import Any, Callable, Dict, List, Tuple
import numpy as np


# ----------------------------------------------------------------------
# Abstract Task Representation Layer
# ----------------------------------------------------------------------
class TaskRepresentation:
    """
    Encapsulates a task in a domain‑agnostic vector space.
    - `features` : numeric embedding (e.g., from a language model)
    - `metadata` : optional dict with domain tags, difficulty, etc.
    """

    def __init__(self, features: np.ndarray, metadata: Dict[str, Any] | None = None):
        self.features = features.astype(float)
        self.metadata = metadata or {}

    def similarity(self, other: "TaskRepresentation") -> float:
        """Cosine similarity between two task embeddings."""
        a = self.features
        b = other.features
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ----------------------------------------------------------------------
# Cross‑Domain Skill Mapping
# ----------------------------------------------------------------------
class DomainBridge:
    """
    Stores mappings between source‑domain skill functions and target‑domain
    adapters.  A skill is any callable that can be invoked with a
    `TaskRepresentation` and returns a result appropriate for the target
    domain.
    """

    def __init__(self):
        # Mapping: (source_domain, target_domain) -> adapter callable
        self._bridges: Dict[Tuple[str, str], Callable] = {}

    def register(
        self,
        source_domain: str,
        target_domain: str,
        adapter: Callable[[Callable, TaskRepresentation], Any],
    ) -> None:
        """Register an adapter that knows how to translate a source skill."""
        self._bridges[(source_domain, target_domain)] = adapter

    def transfer(
        self,
        source_skill: Callable,
        source_task: TaskRepresentation,
        target_domain: str,
    ) -> Any:
        """Execute a source skill in the target domain using the appropriate bridge."""
        source_domain = source_task.metadata.get("domain")
        key = (source_domain, target_domain)
        if key not in self._bridges:
            raise ValueError(f"No bridge registered for {source_domain} → {target_domain}")
        adapter = self._bridges[key]
        return adapter(source_skill, source_task)


# ----------------------------------------------------------------------
# Transfer Learning Metrics
# ----------------------------------------------------------------------
class TransferMetrics:
    """
    Computes simple transfer efficiency metrics:
    - `raw_score` : performance of target task after transfer
    - `baseline_score` : performance without transfer (random / zero‑shot)
    - `efficiency` : (raw_score - baseline) / baseline
    """

    @staticmethod
    def efficiency(raw_score: float, baseline_score: float) -> float:
        if baseline_score == 0:
            return float("inf") if raw_score > 0 else 0.0
        return (raw_score - baseline_score) / baseline_score


# ----------------------------------------------------------------------
# Transfer Engine (orchestrates the process)
# ----------------------------------------------------------------------
class TransferEngine:
    """
    High‑level façade used by the swarm to request cross‑domain transfers.
    """

    def __init__(self, bridge: DomainBridge):
        self.bridge = bridge

    def execute_transfer(
        self,
        source_skill: Callable,
        source_task: TaskRepresentation,
        target_task: TaskRepresentation,
        evaluator: Callable[[Any, TaskRepresentation], float],
    ) -> Dict[str, float]:
        """
        Runs the transfer, evaluates the result on the target task,
        and returns a dictionary of metrics.
        """
        # 1️⃣ Transfer the skill
        result = self.bridge.transfer(
            source_skill, source_task, target_task.metadata.get("domain", "unknown")
        )

        # 2️⃣ Evaluate on target task
        raw_score = evaluator(result, target_task)

        # 3️⃣ Baseline (zero‑shot) evaluation
        baseline_score = evaluator(None, target_task)  # evaluator must handle None

        # 4️⃣ Compute efficiency
        efficiency = TransferMetrics.efficiency(raw_score, baseline_score)

        return {
            "raw_score": raw_score,
            "baseline_score": baseline_score,
            "efficiency": efficiency,
        }
\"\"\"domain_transfer_system.py
Abstract framework for cross‑domain transfer learning within the swarm.

Provides:
- TaskRepresentation: unified description of any task (code, math, UI, etc.).
- SkillMapper: maps skills/knowledge from a source domain to a target domain.
- TransferMetrics: quantitative measures of transfer efficiency.
- DomainBridge: orchestrates the transfer process using the above components.
\"\"\"

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Callable, List, Tuple
import time
import math
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ---------------------------------------------------------------------------
# Unified task representation
# ---------------------------------------------------------------------------
@dataclass
class TaskRepresentation:
    \"\"\"A language‑agnostic description of a task.

    Attributes
    ----------
    domain: str
        High‑level domain identifier (e.g., \"code\", \"math\", \"ui\", \"physics\").
    metadata: Dict[str, Any]
        Arbitrary key‑value pairs describing the task (e.g., difficulty, inputs, outputs).
    embedding: List[float] = field(default_factory=list)
        Optional vector embedding used for similarity / retrieval.
    \"\"\"
    domain: str
    metadata: Dict[str, Any]
    embedding: List[float] = field(default_factory=list)

    def compute_embedding(self, encoder: Callable[[Dict[str, Any]], List[float]]) -> None:
        \"\"\"Populate ``self.embedding`` using a provided encoder function."""
        logger.debug(f\"Computing embedding for task in domain '{self.domain}'\")
        self.embedding = encoder(self.metadata)


# ---------------------------------------------------------------------------
# Skill mapping between domains
# ---------------------------------------------------------------------------
class SkillMapper:
    \"\"\"Maps skills from a source task to a target task.

    The mapper maintains a registry of domain‑pair specific mapping functions.
    Users can register custom mappers to handle novel domain pairs.
    \"\"\"

    def __init__(self):
        self._registry: Dict[Tuple[str, str], Callable[[TaskRepresentation], TaskRepresentation]] = {}

    def register(self, source_domain: str, target_domain: str,
                 mapper_fn: Callable[[TaskRepresentation], TaskRepresentation]) -> None:
        key = (source_domain, target_domain)
        logger.info(f\"Registering skill mapper for {key}\")
        self._registry[key] = mapper_fn

    def map(self, source_task: TaskRepresentation, target_domain: str) -> TaskRepresentation:
        key = (source_task.domain, target_domain)
        if key not in self._registry:
            raise ValueError(f\"No mapper registered for {key}\")
        logger.info(f\"Mapping skill from {source_task.domain} → {target_domain}\")
        return self._registry[key](source_task)


# ---------------------------------------------------------------------------
# Transfer learning metrics
# ---------------------------------------------------------------------------
@dataclass
class TransferMetrics:
    \"\"\"Collects and reports metrics for a single transfer episode.\"\"\"
    source_domain: str
    target_domain: str
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0
    source_performance: float = 0.0
    target_performance: float = 0.0
    transferred: bool = False

    def stop(self) -> None:
        self.end_time = time.time()

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time else 0.0

    @property
    def improvement(self) -> float:
        \"\"\"Relative improvement of the target after transfer (0‑1).\"\"\"
        if self.source_performance == 0:
            return 0.0
        return max(0.0, (self.target_performance - self.source_performance) / self.source_performance)

    def to_dict(self) -> Dict[str, Any]:
        return {
            \"source_domain\": self.source_domain,
            \"target_domain\": self.target_domain,
            \"duration_s\": self.duration,
            \"source_perf\": self.source_performance,
            \"target_perf\": self.target_performance,
            \"improvement\": self.improvement,
            \"transferred\": self.transferred,
        }

    def log(self) -> None:
        logger.info(json.dumps(self.to_dict()))


# ---------------------------------------------------------------------------
# Domain bridge – orchestrates a transfer
# ---------------------------------------------------------------------------
class DomainBridge:
    \"\"\"High‑level API to perform cross‑domain transfer learning.\"

    Parameters
    ----------
    mapper: SkillMapper
        The skill‑mapping registry.
    encoder: Callable[[Dict[str, Any]], List[float]]
        Function that turns task metadata into a numeric embedding.
    evaluator: Callable[[TaskRepresentation], float]
        Function that returns a performance score for a given task.
    \"\"\"

    def __init__(self,
                 mapper: SkillMapper,
                 encoder: Callable[[Dict[str, Any]], List[float]],
                 evaluator: Callable[[TaskRepresentation], float]):
        self.mapper = mapper
        self.encoder = encoder
        self.evaluator = evaluator

    def transfer(self,
                 source_task: TaskRepresentation,
                 target_domain: str) -> Tuple[TaskRepresentation, TransferMetrics]:
        \"\"\"Execute a full transfer pipeline.

        Returns
        -------
        target_task : TaskRepresentation
            The newly created task representation in the target domain.
        metrics : TransferMetrics
            Collected statistics for the transfer.
        \"\"\"
        # 1️⃣ Embed source task
        source_task.compute_embedding(self.encoder)

        # 2️⃣ Evaluate source performance (baseline)
        src_perf = self.evaluator(source_task)

        # 3️⃣ Map to target domain
        target_task = self.mapper.map(source_task, target_domain)
        target_task.compute_embedding(self.encoder)

        # 4️⃣ Evaluate target performance
        tgt_perf = self.evaluator(target_task)

        # 5️⃣ Record metrics
        metrics = TransferMetrics(
            source_domain=source_task.domain,
            target_domain=target_domain,
            source_performance=src_perf,
            target_performance=tgt_perf,
            transferred=True,
        )
        metrics.stop()
        metrics.log()

        return target_task, metrics
```python
"""
domain_transfer_system.py

Core library for abstract cross‑domain transfer learning within the swarm.
Provides:
- Abstract task representation layer
- Cross‑domain skill mapping utilities
- Transfer learning metrics
- Domain bridge mechanisms to orchestrate transfers
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple
import numpy as np


# ----------------------------------------------------------------------
# Abstract Task Representation Layer
# ----------------------------------------------------------------------
class AbstractTaskRepresentation(ABC):
    """Define how a concrete task from any domain is encoded/decoded."""

    @abstractmethod
    def encode(self, task: Any) -> np.ndarray:
        """Encode a domain‑specific task into a fixed‑size vector."""
        ...

    @abstractmethod
    def decode(self, vector: np.ndarray) -> Any:
        """Decode a vector back into a domain‑specific task."""
        ...


class TaskRepresentationRegistry:
    """Registry that holds encoders/decoders for each supported domain."""

    _registry: Dict[str, AbstractTaskRepresentation] = {}

    @classmethod
    def register(cls, domain: str, impl: AbstractTaskRepresentation) -> None:
        cls._registry[domain] = impl

    @classmethod
    def get(cls, domain: str) -> AbstractTaskRepresentation:
        if domain not in cls._registry:
            raise KeyError(f"No task representation registered for domain '{domain}'")
        return cls._registry[domain]


# ----------------------------------------------------------------------
# Cross‑Domain Skill Mapping
# ----------------------------------------------------------------------
@dataclass
class SkillEmbedding:
    """Simple container for a skill vector and its metadata."""
    name: str
    vector: np.ndarray
    domain: str


class SkillMapper:
    """
    Maps skills between source and target domains using cosine similarity.
    Allows optional fine‑tuning via a linear projection learned from a small
    support set (few‑shot adaptation).
    """

    def __init__(self):
        self._skill_bank: List[SkillEmbedding] = []
        self._projection: np.ndarray | None = None  # shape (src_dim, tgt_dim)

    def add_skill(self, skill: SkillEmbedding) -> None:
        self._skill_bank.append(skill)

    def _cosine(self, a: np.ndarray, b: np.ndarray) -> float:
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def find_best_match(
        self, source_vec: np.ndarray, target_domain: str, top_k: int = 1
    ) -> List[Tuple[SkillEmbedding, float]]:
        """Return top‑k matching skills in the target domain."""
        candidates = [
            (skill, self._cosine(source_vec, skill.vector))
            for skill in self._skill_bank
            if skill.domain == target_domain
        ]
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_k]

    def learn_projection(
        self,
        source_vectors: np.ndarray,
        target_vectors: np.ndarray,
        reg: float = 1e-4,
    ) -> None:
        """
        Learn a linear projection W such that XW ≈ Y using ridge regression.
        X: (n_samples, src_dim), Y: (n_samples, tgt_dim)
        """
        X = source_vectors
        Y = target_vectors
        # Closed‑form ridge solution: W = (XᵀX + λI)⁻¹ Xᵀ Y
        xtx = X.T @ X
        dim = xtx.shape[0]
        ridge = xtx + reg * np.eye(dim)
        self._projection = np.linalg.solve(ridge, X.T @ Y)

    def project(self, source_vec: np.ndarray) -> np.ndarray:
        if self._projection is None:
            raise RuntimeError("Projection matrix not learned yet.")
        return source_vec @ self._projection


# ----------------------------------------------------------------------
# Transfer Learning Metrics
# ----------------------------------------------------------------------
class TransferMetrics:
    """
    Compute quantitative measures of transfer efficiency.
    Typical metric: (Performance_target_with_transfer - Performance_target_baseline)
                     / Performance_target_baseline
    """

    @staticmethod
    def relative_gain(baseline: float, transferred: float) -> float:
        if baseline == 0:
            return float("inf") if transferred != 0 else 0.0
        return (transferred - baseline) / baseline

    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        if np.linalg.norm(vec_a) == 0 or np.linalg.norm(vec_b) == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)))


# ----------------------------------------------------------------------
# Domain Bridge Mechanism
# ----------------------------------------------------------------------
class DomainBridge:
    """
    Orchestrates the transfer of knowledge from a source domain to a target domain.
    """

    def __init__(self, mapper: SkillMapper, metrics: TransferMetrics):
        self.mapper = mapper
        self.metrics = metrics

    def transfer(
        self,
        source_task: Any,
        source_domain: str,
        target_domain: str,
        target_task_factory: Callable[[Any], Any],
    ) -> Tuple[Any, Dict[str, float]]:
        """
        Perform a transfer:
        1. Encode source task.
        2. Map/Project to target skill space.
        3. Decode or adapt into a target‑specific task via the provided factory.
        4. Return the new task and a dict of metric values.
        """
        src_repr = TaskRepresentationRegistry.get(source_domain)
        tgt_repr = TaskRepresentationRegistry.get(target_domain)

        src_vec = src_repr.encode(source_task)

        # Try to project; if no projection, fall back to raw similarity search
        try:
            projected = self.mapper.project(src_vec)
        except RuntimeError:
            # raw similarity search – pick best matching skill and use its vector
            best, _ = self.mapper.find_best_match(src_vec, target_domain, top_k=1)[0]
            projected = best.vector

        target_task = target_task_factory(tgt_repr.decode(projected))

        # Example metric calculation (placeholder values – real evaluation
        # must be supplied by the caller)
        baseline_perf = getattr(target_task, "baseline_performance", 0.0)
        transferred_perf = getattr(target_task, "performance", 0.0)
        gain = self.metrics.relative_gain(baseline_perf, transferred_perf)

        return target_task, {"relative_gain": gain}
```
"""
Domain Transfer System
----------------------

Provides an abstract representation for tasks across heterogeneous domains,
mechanisms to map skills between domains, and utilities to measure transfer
effectiveness.

Key Components
==============

1. **TaskRepresentation** – A lightweight, serializable description of a task
   that captures inputs, outputs, and meta‑features (e.g., modality, difficulty).

2. **DomainBridge** – Registers mapping functions that translate a source
   representation into a target representation, optionally injecting domain‑specific
   adapters (e.g., code‑to‑math transformer).

3. **TransferMetrics** – Computes similarity, transfer gain, and efficiency
   scores to quantify how much knowledge has been reused.

4. **TransferEngine** – Orchestrates end‑to‑end transfer: encode source task,
   map via a bridge, decode into target task, and evaluate with a provided
   evaluator.

Usage Example
-------------
```python
from domain_transfer_system import TaskRepresentation, DomainBridge, TransferEngine

# Define a simple code generation task
code_task = TaskRepresentation(
    domain="code",
    description="Generate a Python function that computes factorial.",
    inputs={"prompt": "Write factorial function"},
    outputs={"type": "code"},
    metadata={"complexity": "medium"}
)

# Register a bridge that maps code tasks to math tasks
def code_to_math_bridge(src_repr: TaskRepresentation) -> TaskRepresentation:
    return TaskRepresentation(
        domain="math",
        description="Derive the closed‑form formula for n! and prove it by induction.",
        inputs={},
        outputs={"type": "proof"},
        metadata={"complexity": src_repr.metadata["complexity"]}
    )

DomainBridge.register("code_to_math", code_to_math_bridge)

engine = TransferEngine()
math_task = engine.transfer(code_task, bridge_name="code_to_math")
print(math_task.description)
```
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional
import json
import math
import hashlib


# --------------------------------------------------------------------------- #
# 1. Abstract Task Representation
# --------------------------------------------------------------------------- #
@dataclass
class TaskRepresentation:
    """
    A generic, serializable description of a task.

    Attributes
    ----------
    domain: str
        Identifier of the domain (e.g., "code", "math", "ui", "physics").
    description: str
        Human‑readable description of what the task entails.
    inputs: Dict[str, Any]
        Structured inputs required to solve the task.
    outputs: Dict[str, Any]
        Expected output specification.
    metadata: Dict[str, Any]
        Additional signals such as difficulty, modality, or provenance.
    """
    domain: str
    description: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def serialize(self) -> str:
        """JSON‑encode the representation."""
        return json.dumps({
            "domain": self.domain,
            "description": self.description,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "metadata": self.metadata,
        }, ensure_ascii=False, sort_keys=True)

    @staticmethod
    def deserialize(serialized: str) -> "TaskRepresentation":
        """Re‑create a TaskRepresentation from its JSON string."""
        data = json.loads(serialized)
        return TaskRepresentation(**data)

    def fingerprint(self) -> str:
        """Stable hash used for similarity calculations."""
        return hashlib.sha256(self.serialize().encode()).hexdigest()


# --------------------------------------------------------------------------- #
# 2. Domain Bridge Registry
# --------------------------------------------------------------------------- #
class DomainBridge:
    """
    Registry for functions that translate a source TaskRepresentation into a
    target TaskRepresentation. Bridges can be domain‑specific or generic.
    """
    _registry: Dict[str, Callable[[TaskRepresentation], TaskRepresentation]] = {}

    @classmethod
    def register(cls, name: str,
                 mapper: Callable[[TaskRepresentation], TaskRepresentation]) -> None:
        """Add a new bridge to the registry."""
        if name in cls._registry:
            raise ValueError(f"Bridge '{name}' already registered.")
        cls._registry[name] = mapper

    @classmethod
    def get(cls, name: str) -> Callable[[TaskRepresentation], TaskRepresentation]:
        """Retrieve a bridge by name."""
        try:
            return cls._registry[name]
        except KeyError as exc:
            raise KeyError(f"Bridge '{name}' not found.") from exc


# --------------------------------------------------------------------------- #
# 3. Transfer Metrics
# --------------------------------------------------------------------------- #
class TransferMetrics:
    """
    Compute quantitative measures of transfer quality.
    """

    @staticmethod
    def similarity(src: TaskRepresentation, tgt: TaskRepresentation) -> float:
        """
        Simple Jaccard‑style similarity over metadata keys and values.
        Returns a value in [0, 1].
        """
        src_set = set(src.metadata.items())
        tgt_set = set(tgt.metadata.items())
        if not src_set and not tgt_set:
            return 1.0
        return len(src_set & tgt_set) / len(src_set | tgt_set)

    @staticmethod
    def transfer_gain(base_score: float, transferred_score: float) -> float:
        """
        Relative improvement after transfer. Positive values indicate gain.
        """
        if base_score == 0:
            return float('inf') if transferred_score > 0 else 0.0
        return (transferred_score - base_score) / base_score

    @staticmethod
    def efficiency(time_before: float, time_after: float) -> float:
        """
        Ratio of time saved (>=0). Larger numbers mean more efficient transfer.
        """
        if time_before == 0:
            return float('inf')
        return (time_before - time_after) / time_before


# --------------------------------------------------------------------------- #
# 4. Transfer Engine
# --------------------------------------------------------------------------- #
class TransferEngine:
    """
    High‑level API to perform cross‑domain transfer using registered bridges.
    """

    def transfer(self,
                 src_task: TaskRepresentation,
                 bridge_name: str,
                 *,
                 evaluator: Optional[Callable[[TaskRepresentation], float]] = None,
                 baseline_evaluator: Optional[Callable[[TaskRepresentation], float]] = None
                 ) -> TaskRepresentation:
        """
        Perform transfer from `src_task` to a target task using the specified bridge.

        Parameters
        ----------
        src_task: TaskRepresentation
            The source task representation.
        bridge_name: str
            Name of the bridge registered in `DomainBridge`.
        evaluator: Callable, optional
            Function that scores the transferred task (higher is better).
        baseline_evaluator: Callable, optional
            Scoring function for the same task without transfer (used for gain).

        Returns
        -------
        TaskRepresentation
            The target task after mapping.
        """
        bridge_fn = DomainBridge.get(bridge_name)
        tgt_task = bridge_fn(src_task)

        # Optional diagnostics
        if evaluator:
            transferred_score = evaluator(tgt_task)
            if baseline_evaluator:
                baseline_score = baseline_evaluator(src_task)
                gain = TransferMetrics.transfer_gain(baseline_score, transferred_score)
                print(f"[TransferEngine] Gain: {gain:.2%}")

        return tgt_task
"""
domain_transfer_system.py
-------------------------

Provides a lightweight framework for representing tasks abstractly,
mapping skills across domains, measuring transfer effectiveness,
and defining simple bridge mechanisms that can be extended
for more sophisticated AGI‑level transfer learning.

The design is intentionally minimal so it can be integrated
into the existing swarm without breaking current functionality.
"""

from typing import Any, Callable, Dict, List, Tuple
import abc
import time
import math
import json
import hashlib


# ----------------------------------------------------------------------
# Abstract Task Representation
# ----------------------------------------------------------------------
class AbstractTask(abc.ABC):
    """
    Base class for any task that the swarm can execute.
    Sub‑classes must implement:
        - embed()   → vector representation (list of floats)
        - execute() → run the task and return a result
    """

    def __init__(self, name: str, payload: Any):
        self.name = name
        self.payload = payload
        self._embedding: List[float] | None = None

    @abc.abstractmethod
    def embed(self) -> List[float]:
        """Return a deterministic embedding for the task."""
        ...

    @abc.abstractmethod
    def execute(self) -> Any:
        """Run the task and return its output."""
        ...

    def hash(self) -> str:
        """Stable hash of the task (used for caching & similarity)."""
        data = json.dumps(
            {"name": self.name, "payload": self.payload}, sort_keys=True
        )
        return hashlib.sha256(data.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<AbstractTask {self.name} hash={self.hash()[:8]}>"


# ----------------------------------------------------------------------
# Concrete Task Implementations
# ----------------------------------------------------------------------
class CodeGenerationTask(AbstractTask):
    """Task that generates code from a natural‑language prompt."""

    def embed(self) -> List[float]:
        # Very simple deterministic embedding: length of prompt + hash bits
        base = len(str(self.payload))
        bits = sum(ord(c) for c in self.name) % 10
        return [float(base), float(bits)]

    def execute(self) -> str:
        # Placeholder: echo the prompt – real implementation will call the code generator
        return f"# Generated code for: {self.payload}"


class MathProblemTask(AbstractTask):
    """Task that solves a math problem expressed in natural language."""

    def embed(self) -> List[float]:
        base = len(str(self.payload))
        bits = sum(ord(c) for c in self.name) % 7
        return [float(base), float(bits)]

    def execute(self) -> Any:
        # Very naive evaluator – replace with a proper math solver later
        try:
            result = eval(str(self.payload), {"__builtins__": {}}, {})
        except Exception:
            result = "uncomputable"
        return result


# ----------------------------------------------------------------------
# Skill Mapping & Cross‑Domain Bridge
# ----------------------------------------------------------------------
class DomainBridge:
    """
    Holds mappings between source and target task embeddings.
    The bridge can be queried for the most similar source task
    given a target embedding.
    """

    def __init__(self):
        # Mapping: target_task_name → List[Tuple[source_task, similarity]]
        self._mappings: Dict[str, List[Tuple[AbstractTask, float]]] = {}

    @staticmethod
    def _cosine_sim(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        return dot / (norm_a * norm_b + 1e-9)

    def register(self, source: AbstractTask, target: AbstractTask):
        """Register a source → target relationship."""
        sim = self._cosine_sim(source.embed(), target.embed())
        self._mappings.setdefault(target.name, []).append((source, sim))

    def best_source(self, target: AbstractTask) -> Tuple[AbstractTask, float] | None:
        """Return the most similar source task for a given target."""
        candidates = self._mappings.get(target.name, [])
        if not candidates:
            return None
        return max(candidates, key=lambda x: x[1])


# ----------------------------------------------------------------------
# Transfer Metrics
# ----------------------------------------------------------------------
class TransferMetrics:
    """
    Simple metrics to quantify transfer learning effectiveness.
    Currently tracks:
        - similarity (embedding cosine)
        - speedup (time saved vs. baseline)
        - accuracy delta (result quality change)
    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def log(
        self,
        source: AbstractTask,
        target: AbstractTask,
        similarity: float,
        Speedup: float,
        AccuracyDelta: float,
    ):
        entry = {
            "source": source.name,
            "target": target.name,
            "similarity": Similarity,
            "Speedup": Speedup,
            "AccuracyDelta": AccuracyDelta,
        }
        self.records.append(entry)

    def report(self) -> str:
        return json.dumps(self.records, indent=2)


# ----------------------------------------------------------------------
# Helper Utilities
# ----------------------------------------------------------------------
def timed(fn: Callable) -> Callable:
    """Decorator to measure execution time of a task."""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        elapsed = time.time() - start
        return result, elapsed

    return wrapper


# ----------------------------------------------------------------------
# Example usage (can be removed or moved to a test suite)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Create simple tasks
    code_task = CodeGenerationTask("code_gen", "def foo(): pass")
    math_task = MathProblemTask("math_solve", "2 + 2")

    # Build a bridge and register the relationship
    bridge = DomainBridge()
    bridge.register(source=code_task, target=math_task)

    # Find best source for a new target
    best = bridge.best_source(math_task)
    if best:
        src, sim = best
        print(f"Best source for {math_task.name}: {src.name} (sim={sim:.2f})")
```
# domain_transfer_system.py
# Core infrastructure for cross‑domain transfer learning within the swarm.

from __future__ import annotations
from typing import Any, Callable, Dict, List, Tuple
import hashlib
import json
import numpy as np


class AbstractTaskRepresentation:
    """
    A lightweight, serialisable description of any task the swarm can perform.
    Includes a deterministic hash, optional schema definitions and a vector
    embedding (e.g., from a language model) for similarity calculations.
    """

    def __init__(
        self,
        name: str,
        domain: str,
        input_schema: Dict[str, Any] | None = None,
        output_schema: Dict[str, Any] | None = None,
        embedding: np.ndarray | None = None,
    ) -> None:
        self.name = name
        self.domain = domain
        self.input_schema = input_schema or {}
        self.output_schema = output_schema or {}
        self.embedding = embedding or np.zeros(768)  # placeholder size
        self.id = self._compute_id()

    def _compute_id(self) -> str:
        """Deterministic identifier based on name and domain."""
        raw = f"{self.domain}:{self.name}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "embedding": self.embedding.tolist(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "AbstractTaskRepresentation":
        emb = np.array(data.get("embedding", []))
        return AbstractTaskRepresentation(
            name=data["name"],
            domain=data["domain"],
            input_schema=data.get("input_schema"),
            output_schema=data.get("output_schema"),
            embedding=emb,
        )


class CrossDomainSkillMapper:
    """
    Maintains a bi‑directional map between source‑domain task embeddings and
    target‑domain task embeddings.  Supports registration of explicit mappings
    and on‑the‑fly similarity‑based suggestions.
    """

    def __init__(self) -> None:
        # key: source task id, value: list of (target_task_id, similarity_score)
        self._mappings: Dict[str, List[Tuple[str, float]]] = {}
        self._registry: Dict[str, AbstractTaskRepresentation] = {}

    def register_task(self, task: AbstractTaskRepresentation) -> None:
        self._registry[task.id] = task

    def add_mapping(
        self,
        source_task: AbstractTaskRepresentation,
        target_task: AbstractTaskRepresentation,
        similarity: float | None = None,
    ) -> None:
        if similarity is None:
            similarity = self._cosine_similarity(
                source_task.embedding, target_task.embedding
            )
        self._mappings.setdefault(source_task.id, []).append(
            (target_task.id, similarity)
        )

    def suggest_target(
        self, source_task: AbstractTaskRepresentation, top_k: int = 3
    ) -> List[Tuple[AbstractTaskRepresentation, float]]:
        candidates = []
        for tgt in self._registry.values():
            if tgt.domain == source_task.domain:
                continue
            sim = self._cosine_similarity(source_task.embedding, tgt.embedding)
            candidates.append((tgt, sim))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_k]

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class TransferMetrics:
    """
    Computes quantitative metrics for a transfer attempt.
    - similarity: embedding cosine similarity between source and target tasks
    - efficiency: (target performance) / (source performance) * similarity
    - success_rate: boolean based on a configurable threshold
    """

    def __init__(self, similarity_threshold: float = 0.6) -> None:
        self.similarity_threshold = similarity_threshold

    def evaluate(
        self,
        source_perf: float,
        target_perf: float,
        similarity: float,
    ) -> Dict[str, Any]:
        efficiency = (target_perf / source_perf) * similarity if source_perf else 0.0
        success = similarity >= self.similarity_threshold and efficiency >= 0.4
        return {
            "similarity": similarity,
            "efficiency": efficiency,
            "success": success,
        }


class DomainBridge:
    """
    Orchestrates a transfer from a source task to a target domain using the
    mapper and metrics.  It can invoke a provided `transfer_fn` that knows how
    to adapt source artefacts (e.g., code snippets) to the target format.
    """

    def __init__(
        self,
        mapper: CrossDomainSkillMapper,
        metrics: TransferMetrics,
        transfer_fn: Callable[[Any, AbstractTaskRepresentation], Any],
    ) -> None:
        self.mapper = mapper
        self.metrics = metrics
        self.transfer_fn = transfer_fn

    def transfer(
        self,
        source_task: AbstractTaskRepresentation,
        source_artifact: Any,
        target_task: AbstractTaskRepresentation,
        source_perf: float,
    ) -> Tuple[Any, Dict[str, Any]]:
        # Run the user‑provided adaptation logic
        adapted = self.transfer_fn(source_artifact, target_task)

        # Dummy evaluation of target performance (placeholder for real eval)
        target_perf = self._mock_evaluate(adapted, target_task)

        similarity = self.mapper._cosine_similarity(
            source_task.embedding, target_task.embedding
        )
        metric_report = self.metrics.evaluate(source_perf, target_perf, similarity)
        return adapted, metric_report

    @staticmethod
    def _mock_evaluate(artifact: Any, task: AbstractTaskRepresentation) -> float:
        # In a real system this would run the artifact against a validation set.
        # Here we return a pseudo‑random score based on the hash of the artifact.
        h = hashlib.sha256(str(artifact).encode()).hexdigest()
        return (int(h[:8], 16) % 100) / 100.0
"""
Domain Transfer System
======================

Provides a lightweight framework for representing tasks abstractly,
mapping skills across domains, and measuring transfer effectiveness.
Designed to be extensible for code, mathematics, UI design, debugging,
and scientific reasoning domains.

Key Components
--------------
- **AbstractTaskRepresentation**: Encodes any task into a domain‑agnostic
  vector using pluggable encoders (e.g., AST, symbolic math, UI DSL).
- **DomainBridge**: Registers source‑target adapters that translate
  representations and invoke appropriate solvers.
- **TransferMetrics**: Computes similarity, adaptation cost, and
  transfer efficiency (baseline vs. transferred performance).
- **TransferRegistry**: Global singleton storing encoders, bridges,
  and metric calculators.

Usage Example
-------------
```python
from domain_transfer_system import TransferRegistry, AbstractTaskRepresentation

# Register a code encoder
TransferRegistry.register_encoder('code', CodeEncoder())
# Register a math encoder
TransferRegistry.register_encoder('math', MathEncoder())

# Bridge code → math
TransferRegistry.register_bridge('code', 'math', CodeToMathBridge())

# Perform a transfer
src_task = {'type': 'code', 'content': 'def add(a,b): return a+b'}
result = TransferRegistry.transfer(src_task, target_type='math')
print(result)   # => symbolic expression "a + b"
```
"""

from __future__ import annotations
from typing import Any, Callable, Dict, Tuple
import numpy as np


# --------------------------------------------------------------------------- #
# Abstract Task Representation
# --------------------------------------------------------------------------- #
class AbstractTaskRepresentation:
    """
    Wraps a raw task (code, math statement, UI spec, etc.) and provides
    a domain‑agnostic embedding vector. Encoders are user‑provided callables
    that accept the raw payload and return a NumPy vector.
    """
    def __init__(self, domain: str, payload: Any):
        self.domain = domain
        self.payload = payload
        self.embedding: np.ndarray | None = None

    def encode(self) -> np.ndarray:
        encoder = TransferRegistry.get_encoder(self.domain)
        if encoder is None:
            raise ValueError(f"No encoder registered for domain '{self.domain}'")
        self.embedding = encoder(self.payload)
        return self.embedding

    def decode(self, target_domain: str) -> Any:
        """
        Decode the current embedding into a concrete artifact for the
        target domain using a registered bridge.
        """
        bridge = TransferRegistry.get_bridge(self.domain, target_domain)
        if bridge is None:
            raise ValueError(f"No bridge from '{self.domain}' to '{target_domain}'")
        if self.embedding is None:
            self.encode()
        return bridge.decode(self.embedding)


# --------------------------------------------------------------------------- #
# Domain Bridge
# --------------------------------------------------------------------------- #
class DomainBridge:
    """
    Translates an embedding from a source domain to a concrete artifact in a
    target domain. Implementations must provide a `decode` method.
    """
    def __init__(self, decode_fn: Callable[[np.ndarray], Any]):
        self.decode_fn = decode_fn

    def decode(self, embedding: np.ndarray) -> Any:
        return self.decode_fn(embedding)


# --------------------------------------------------------------------------- #
# Transfer Metrics
# --------------------------------------------------------------------------- #
class TransferMetrics:
    """
    Collection of static methods to evaluate transfer quality.
    """

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Return cosine similarity between two embeddings."""
        if a.ndim != 1 or b.ndim != 1:
            raise ValueError("Embeddings must be 1‑D vectors")
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        return float(dot / norm) if norm != 0 else 0.0

    @staticmethod
    def transfer_efficiency(baseline_score: float, transferred_score: float) -> float:
        """
        Compute % improvement of transferred solution over baseline.
        Positive values indicate beneficial transfer.
        """
        if baseline_score == 0:
            return float('inf') if transferred_score > 0 else 0.0
        return ((transferred_score - baseline_score) / abs(baseline_score)) * 100.0


# --------------------------------------------------------------------------- #
# Registry Singleton
# --------------------------------------------------------------------------- #
class TransferRegistry:
    """
    Central registry for encoders, bridges, and metric utilities.
    """
    _encoders: Dict[str, Callable[[Any], np.ndarray]] = {}
    _bridges: Dict[Tuple[str, str], DomainBridge] = {}

    @classmethod
    def register_encoder(cls, domain: str, encoder_fn: Callable[[Any], np.ndarray]) -> None:
        """Register an encoder for a specific domain."""
        cls._encoders[domain] = encoder_fn

    @classmethod
    def get_encoder(cls, domain: str) -> Callable[[Any], np.ndarray] | None:
        return cls._encoders.get(domain)

    @classmethod
    def register_bridge(cls, src_domain: str, tgt_domain: str, bridge: DomainBridge) -> None:
        """Register a bridge that maps src_domain embeddings to tgt_domain artifacts."""
        cls._bridges[(src_domain, tgt_domain)] = bridge

    @classmethod
    def get_bridge(cls, src_domain: str, tgt_domain: str) -> DomainBridge | None:
        return cls._bridges.get((src_domain, tgt_domain))

    @classmethod
    def transfer(cls, src_task: Dict[str, Any], target_type: str) -> Any:
        """
        High‑level API: encode source task, bridge to target, and return result.
        """
        src_repr = AbstractTaskRepresentation(domain=src_task["type"], payload=src_task["content"])
        src_repr.encode()
        return src_repr.decode(target_type)


# --------------------------------------------------------------------------- #
# Example Stub Encoders (to be replaced by real implementations)
# --------------------------------------------------------------------------- #
def _identity_encoder(payload: Any) -> np.ndarray:
    """Fallback encoder that hashes the string representation."""
    return np.frombuffer(str(payload).encode('utf-8'), dtype=np.uint8).astype(np.float32)


# Register identity encoders for any domain not yet provided.
for _domain in ["code", "math", "ui", "debug", "physics"]:
    if TransferRegistry.get_encoder(_domain) is None:
        TransferRegistry.register_encoder(_domain, _identity_encoder)
```
"""
domain_transfer_system.py

Core framework for cross‑domain transfer learning within the CLAUDE‑Parasite‑Brain‑Suck project.
Provides:
- AbstractTask: unified representation of any task (code, math, UI, physics, etc.).
- TaskRegistry: global store for task instances and their embeddings.
- SkillMapper: learns mappings between source‑domain skills and target‑domain skills.
- TransferMetrics: computes quantitative transfer efficiency.
- DomainBridge: orchestrates the end‑to‑end transfer process.
"""

import abc
import uuid
from typing import Any, Dict, List, Tuple, Callable
import numpy as np

# ----------------------------------------------------------------------
# Abstract task representation
# ----------------------------------------------------------------------
class AbstractTask(abc.ABC):
    """
    Base class for any task. Sub‑classes must implement:
    - embed(): produce a fixed‑size vector representation.
    - execute(inputs): run the task with given inputs.
    """

    def __init__(self, name: str, domain: str, payload: Any):
        self.id = str(uuid.uuid4())
        self.name = name
        self.domain = domain          # e.g. "code", "math", "ui", "physics"
        self.payload = payload        # raw definition (source code, problem statement, etc.)

    @abc.abstractmethod
    def embed(self) -> np.ndarray:
        """Return a dense embedding that captures the semantics of the task."""
        pass

    @abc.abstractmethod
    def execute(self, inputs: Any) -> Any:
        """Execute the task (or a proxy) and return the result."""
        pass

# ----------------------------------------------------------------------
# Registry for tasks and their embeddings
# ----------------------------------------------------------------------
class TaskRegistry:
    """Singleton registry that stores tasks and provides nearest‑neighbor lookup."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskRegistry, cls).__new__(cls)
            cls._instance._tasks: Dict[str, AbstractTask] = {}
            cls._instance._embeddings: Dict[str, np.ndarray] = {}
        return cls._instance

    def add_task(self, task: AbstractTask):
        self._tasks[task.id] = task
        self._embeddings[task.id] = task.embed()

    def get_task(self, task_id: str) -> AbstractTask:
        return self._tasks[task_id]

    def find_similar(self, query_emb: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """Return list of (task_id, similarity) sorted descending."""
        sims = []
        for tid, emb in self._embeddings.items():
            sim = float(np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb) + 1e-8))
            sims.append((tid, sim))
        sims.sort(key=lambda x: x[1], reverse=True)
        return sims[:top_k]

# ----------------------------------------------------------------------
# Skill mapping between domains
# ----------------------------------------------------------------------
class SkillMapper:
    """
    Learns a linear (or neural) mapping between source‑domain embeddings
    and target‑domain embeddings using a small set of paired examples.
    """

    def __init__(self):
        self._maps: Dict[Tuple[str, str], Callable[[np.ndarray], np.ndarray]] = {}

    def train(self,
              source_tasks: List[AbstractTask],
              target_tasks: List[AbstractTask],
              reg: float = 1e-3):
        """
        Train a ridge‑regressed linear map: W such that W·src ≈ tgt.
        source_tasks and target_tasks must be aligned (same length, ordered pairs).
        """
        src_mat = np.stack([t.embed() for t in source_tasks])
        tgt_mat = np.stack([t.embed() for t in target_tasks])

        # Closed‑form ridge regression: W = (XᵀX + λI)⁻¹ XᵀY
        XtX = src_mat.T @ src_mat
        reg_mat = reg * np.eye(XtX.shape[0])
        W = np.linalg.inv(XtX + reg_mat) @ src_mat.T @ tgt_mat

        def mapper(x: np.ndarray) -> np.ndarray:
            return x @ W

        key = (source_tasks[0].domain, target_tasks[0].domain)
        self._maps[key] = mapper

    def map(self, source_task: AbstractTask, target_domain: str) -> np.ndarray:
        key = (source_task.domain, target_domain)
        if key not in self._maps:
            raise ValueError(f"No mapping trained for {key}")
        return self._maps[key](source_task.embed())

# ----------------------------------------------------------------------
# Transfer learning metrics
# ----------------------------------------------------------------------
class TransferMetrics:
    """
    Provides quantitative measures:
    - transfer_gain: improvement of target task performance when initialized from source.
    - embedding_similarity: cosine similarity between source and mapped target embeddings.
    - data_efficiency: performance vs. number of target examples.
    """

    @staticmethod
    def embedding_similarity(src_emb: np.ndarray, tgt_emb: np.ndarray) -> float:
        return float(np.dot(src_emb, tgt_emb) /
                     (np.linalg.norm(src_emb) * np.linalg.norm(tgt_emb) + 1e-8))

    @staticmethod
    def transfer_gain(base_score: float, transferred_score: float) -> float:
        """Percentage gain relative to base (non‑transferred) score."""
        if base_score == 0:
            return float('inf')
        return 100.0 * (transferred_score - base_score) / base_score

# ----------------------------------------------------------------------
# Domain bridge – orchestrates the transfer
# ----------------------------------------------------------------------
class DomainBridge:
    """
    High‑level API:
        bridge = DomainBridge()
        bridge.register_task(my_task)
        bridge.train_mapping('code', 'math', paired_tasks)
        result = bridge.transfer('code_task_id', target_domain='math')
    """

    def __init__(self):
        self.registry = TaskRegistry()
        self.mapper = SkillMapper()
        self.metrics = TransferMetrics()

    def register_task(self, task: AbstractTask):
        self.registry.add_task(task)

    def train_mapping(self,
                      source_domain: str,
                      target_domain: str,
                      paired_task_ids: List[Tuple[str, str]]):
        src_tasks = [self.registry.get_task(sid) for sid, _ in paired_task_ids]
        tgt_tasks = [self.registry.get_task(tid) for _, tid in paired_task_ids]
        self.mapper.train(src_tasks, tgt_tasks)

    def transfer(self,
                 source_task_id: str,
                 target_domain: str,
                 inputs: Any = None) -> Dict[str, Any]:
        """
        Perform a transfer:
        1. Retrieve source task and its embedding.
        2. Map embedding to target domain.
        3. Find nearest target‑domain tasks (optional fine‑tuning).
        4. Execute target task (or a proxy) and return results + metrics.
        """
        src_task = self.registry.get_task(source_task_id)
        mapped_emb = self.mapper.map(src_task, target_domain)

        # Find closest existing target tasks (could be zero‑shot)
        candidates = self.registry.find_similar(mapped_emb, top_k=3)
        candidate_ids = [tid for tid, _ in candidates if self.registry.get_task(tid).domain == target_domain]

        # If we have a concrete target task, run it; otherwise return the mapped embedding.
        if candidate_ids:
            tgt_task = self.registry.get_task(candidate_ids[0])
            output = tgt_task.execute(inputs)
            sim = self.metrics.embedding_similarity(src_task.embed(), tgt_task.embed())
            return {
                "source_task_id": source_task_id,
                "target_task_id": tgt_task.id,
                "output": output,
                "embedding_similarity": sim
            }
        else:
            return {
                "source_task_id": source_task_id,
                "mapped_embedding": mapped_emb.tolist(),
                "note": "No concrete target task found; embedding provided for downstream use."
            }
"""
Domain Transfer System
Provides:
- AbstractTask: unified representation of inputs/outputs across domains.
- SkillRegistry: stores learned skills (functions) with metadata.
- DomainBridge: maps skills from source to target domains using adapters.
- TransferMetrics: computes transfer efficiency.
"""

from typing import Any, Callable, Dict, Tuple
import time

class AbstractTask:
    """Container for a task's data and its domain label."""
    def __init__(self, domain: str, data: Any, metadata: Dict[str, Any] = None):
        self.domain = domain
        self.data = data
        self.metadata = metadata or {}

class SkillRegistry:
    """Register and retrieve skills (callables) keyed by domain and name."""
    _registry: Dict[Tuple[str, str], Callable] = {}

    @classmethod
    def register(cls, domain: str, name: str):
        def decorator(fn: Callable):
            cls._registry[(domain, name)] = fn
            return fn
        return decorator

    @classmethod
    def get(cls, domain: str, name: str) -> Callable:
        return cls._registry.get((domain, name))

class DomainBridge:
    """Map a skill from a source domain to a target domain using an adapter."""
    _adapters: Dict[Tuple[str, str], Callable[[Callable], Callable]] = {}

    @classmethod
    def register_adapter(cls, src: str, tgt: str):
        def decorator(adapter_fn: Callable[[Callable], Callable]):
            cls._adapters[(src, tgt)] = adapter_fn
            return adapter_fn
        return decorator

    @classmethod
    def adapt(cls, src_domain: str, tgt_domain: str, skill_name: str) -> Callable:
        skill = SkillRegistry.get(src_domain, skill_name)
        if not skill:
            raise ValueError(f"Skill {skill_name} not found in {src_domain}")
        adapter = cls._adapters.get((src_domain, tgt_domain))
        if not adapter:
            raise NotImplementedError(f"No adapter from {src_domain} to {tgt_domain}")
        return adapter(skill)

class TransferMetrics:
    """Simple metrics to quantify transfer performance."""
    @staticmethod
    def time_gain(base_time: float, transferred_time: float) -> float:
        """Percentage reduction in execution time."""
        if base_time == 0:
            return 0.0
        return 100.0 * (base_time - transferred_time) / base_time

    @staticmethod
    def accuracy_gain(base_acc: float, transferred_acc: float) -> float:
        """Absolute increase in accuracy (0‑100)."""
        return transferred_acc - base_acc

# ----------------------------------------------------------------------
# Example registrations (can be removed or extended by the research team)

# 1. Code generation skill (source domain: "code")
@SkillRegistry.register(domain="code", name="generate_sort")
def generate_sort(arr):
    """Return Python code that sorts a list."""
    return "sorted_arr = sorted(" + repr(arr) + ")"

# 2. Math solving skill (source domain: "math")
@SkillRegistry.register(domain="math", name="solve_quadratic")
def solve_quadratic(a, b, c):
    """Return roots of ax^2+bx+c=0."""
    disc = b*b - 4*a*c
    if disc < 0:
        return None
    import math
    r1 = (-b + math.sqrt(disc)) / (2*a)
    r2 = (-b - math.sqrt(disc)) / (2*a)
    return r1, r2

# 3. Adapter from code → math (e.g., reuse sorting logic to order polynomial coefficients)
@DomainBridge.register_adapter(src="code", tgt="math")
def code_to_math_adapter(code_skill):
    def adapted(coeffs):
        # Use the code skill to produce a sorted representation of coefficients
        code_str = code_skill(coeffs)
        # Evaluate the generated code to obtain the sorted list
        local = {}
        exec(code_str, {}, local)
        return local.get("sorted_arr", [])
    return adapted
"""
domain_transfer_system.py
-------------------------

Core utilities for abstracting tasks, mapping skills across domains,
and measuring transfer effectiveness.

The implementation is deliberately lightweight – it provides the
interfaces and simple reference implementations that the rest of the
code‑base can import.  More sophisticated models (e.g. neural
embeddings, graph‑based skill graphs) can be swapped in later without
changing the surrounding infrastructure.
"""

from __future__ import annotations
from typing import Any, Dict, Callable, List, Tuple
import numpy as np


class TaskRepresentation:
    """
    Abstract representation of a task.

    Attributes
    ----------
    name: str
        Human‑readable identifier.
    domain: str
        High‑level domain tag (e.g. "code", "math", "physics").
    features: np.ndarray
        Numeric feature vector describing the task.  For prototype
        purposes we use a simple bag‑of‑words TF‑IDF style vector.
    metadata: dict
        Arbitrary additional information (e.g. difficulty, required
        libraries, etc.).
    """

    def __init__(self, name: str, domain: str, raw_text: str,
                 metadata: Dict[str, Any] | None = None):
        self.name = name
        self.domain = domain
        self.metadata = metadata or {}
        self.features = self._vectorize(raw_text)

    @staticmethod
    def _vectorize(text: str) -> np.ndarray:
        """
        Very lightweight vectorizer: count characters of each ASCII
        printable character and normalize.
        """
        counts = np.zeros(95)  # printable ASCII 32‑126
        for ch in text:
            code = ord(ch) - 32
            if 0 <= code < 95:
                counts[code] += 1
        norm = np.linalg.norm(counts) + 1e-9
        return counts / norm

    def similarity(self, other: "TaskRepresentation") -> float:
        """Cosine similarity between feature vectors."""
        return float(np.dot(self.features, other.features) /
                     (np.linalg.norm(self.features) *
                      np.linalg.norm(other.features) + 1e-9))


class SkillMapper:
    """
    Maps skills (functions, patterns) learned in a source domain to a
    target domain using the abstract task representations.

    The default implementation uses nearest‑neighbor lookup in the
    representation space.
    """

    def __init__(self):
        # registry: domain -> list[(TaskRepresentation, Callable)]
        self._registry: Dict[str, List[Tuple[TaskRepresentation, Callable]]] = {}

    def register(self, task: TaskRepresentation, skill_fn: Callable) -> None:
        """Add a new skill associated with a task."""
        self._registry.setdefault(task.domain, []).append((task, skill_fn))

    def transfer(self, source_task: TaskRepresentation,
                 target_task: TaskRepresentation) -> Callable | None:
        """
        Find the most similar registered skill from the source domain
        and adapt it (identity adaptation for the prototype).

        Returns
        -------
        Callable or None
            The transferred skill function, or None if no suitable
            candidate is found.
        """
        candidates = self._registry.get(source_task.domain, [])
        if not candidates:
            return None

        # rank by similarity
        best_task, best_fn = max(candidates,
                                 key=lambda pair: source_task.similarity(pair[0]))
        similarity = source_task.similarity(best_task)
        if similarity < 0.2:   # heuristic threshold
            return None
        return best_fn  # In a full system this would be wrapped/adapted


class TransferMetrics:
    """
    Simple metrics to quantify transfer performance.

    Currently supports:
        - success_rate: proportion of transferred tasks that meet a
          user‑provided success predicate.
        - average_similarity: mean cosine similarity of transferred pairs.
    """

    def __init__(self):
        self.successes: List[bool] = []
        self.similarities: List[float] = []

    def record(self, success: bool, similarity: float) -> None:
        self.successes.append(success)
        self.similarities.append(similarity)

    @property
    def success_rate(self) -> float:
        if not self.successes:
            return 0.0
        return sum(self.successes) / len(self.successes)

    @property
    def average_similarity(self) -> float:
        if not self.similarities:
            return 0.0
        return sum(self.similarities) / len(self.similarities)


class DomainBridge:
    """
    High‑level orchestrator that glues together representations,
    mapping, and metrics for a pair of domains.
    """

    def __init__(self, source_domain: str, target_domain: str):
        self.source = source_domain
        self.target = target_domain
        self.mapper = SkillMapper()
        self.metrics = TransferMetrics()

    def register_skill(self, task_name: str, raw_text: str,
                       skill_fn: Callable) -> None:
        task = TaskRepresentation(name=task_name,
                                  domain=self.source,
                                  raw_text=raw_text)
        self.mapper.register(task, skill_fn)

    def attempt_transfer(self, target_task_name: str, target_raw: str,
                         success_predicate: Callable[[Any], bool]) -> Tuple[bool, float]:
        target_task = TaskRepresentation(name=target_task_name,
                                         domain=self.target,
                                         raw_text=target_raw)
        # Find best source task (naïve: use same name if exists)
        source_task = TaskRepresentation(name=target_task_name,
                                         domain=self.source,
                                         raw_text=target_raw)  # reuse raw for similarity
        transferred = self.mapper.transfer(source_task, target_task)
        if transferred is None:
            self.metrics.record(False, 0.0)
            return False, 0.0

        # Execute transferred skill on a dummy input (could be extended)
        try:
            result = transferred()
            success = success_predicate(result)
        except Exception:
            success = False

        similarity = source_task.similarity(target_task)
        self.metrics.record(success, similarity)
        return success, similarity
"""
Domain Transfer System
----------------------
Provides an abstract representation for tasks, mechanisms to map skills across
domains, and utilities to measure transfer effectiveness.

The design is deliberately lightweight so it can be imported by any existing
module without affecting the current code‑generation pipeline.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple, Type
import time
import json
import hashlib


# ----------------------------------------------------------------------
# Abstract Task Representation
# ----------------------------------------------------------------------
@dataclass
class TaskRepresentation:
    """
    A generic, serialisable description of a task.

    Attributes
    ----------
    domain: str
        Human readable domain name (e.g., "code", "math", "physics").
    name: str
        Short identifier for the specific task.
    inputs: Any
        Structured description of inputs (type hints, shapes, etc.).
    outputs: Any
        Structured description of expected outputs.
    metadata: dict
        Additional free‑form information (e.g., difficulty, source paper).
    """
    domain: str
    name: str
    inputs: Any
    outputs: Any
    metadata: Dict[str, Any] = field(default_factory=dict)

    def fingerprint(self) -> str:
        """Stable hash used for cross‑domain matching."""
        payload = json.dumps(
            {
                "domain": self.domain,
                "name": self.name,
                "inputs": self.inputs,
                "outputs": self.outputs,
                "metadata": self.metadata,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()


# ----------------------------------------------------------------------
# Cross‑Domain Skill Mapping
# ----------------------------------------------------------------------
class DomainBridge:
    """
    Registry that knows how to translate a TaskRepresentation from one domain
    to another and optionally provide a callable that performs the translation.
    """

    _registry: Dict[Tuple[str, str], Callable[[TaskRepresentation], TaskRepresentation]] = {}

    @classmethod
    def register(
        cls,
        source_domain: str,
        target_domain: str,
        mapper: Callable[[TaskRepresentation], TaskRepresentation],
    ) -> None:
        """Register a mapping function between two domains."""
        key = (source_domain.lower(), target_domain.lower())
        cls._registry[key] = mapper

    @classmethod
    def translate(cls, task: TaskRepresentation, target_domain: str) -> TaskRepresentation:
        """Translate `task` into `target_domain` using a registered mapper."""
        key = (task.domain.lower(), target_domain.lower())
        if key not in cls._registry:
            raise ValueError(f"No bridge registered from {task.domain} to {target_domain}")
        return cls._registry[key](task)


# ----------------------------------------------------------------------
# Transfer Learning Metrics
# ----------------------------------------------------------------------
@dataclass
class TransferMetrics:
    """
    Tracks quantitative signals of transfer performance.
    """

    source_domain: str
    target_domain: str
    task_name: str
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    source_score: float | None = None
    target_score: float | None = None
    improvement: float | None = None

    def stop(self, target_score: float) -> None:
        self.end_time = time.time()
        self.target_score = target_score
        if self.source_score is not None:
            self.improvement = (target_score - self.source_score) / (
                self.source_score if self.source_score != 0 else 1
            )

    def duration(self) -> float | None:
        if self.end_time is None:
            return None
        return self.end_time - self.start_time

    def summary(self) -> dict:
        return {
            "source_domain": self.source_domain,
            "target_domain": self.target_domain,
            "task_name": self.task_name,
            "duration_s": self.duration(),
            "source_score": self.source_score,
            "target_score": self.target_score,
            "relative_improvement": self.improvement,
        }


# ----------------------------------------------------------------------
# Helper utilities for quick prototyping
# ----------------------------------------------------------------------
def simple_mapper_factory(
    target_domain: str,
    input_transform: Callable[[Any], Any],
    output_transform: Callable[[Any], Any],
) -> Callable[[TaskRepresentation], TaskRepresentation]:
    """
    Factory that creates a trivial mapper which only rewrites the inputs/outputs.
    Useful for early experiments where the underlying algorithm stays the same.
    """

    def mapper(src_task: TaskRepresentation) -> TaskRepresentation:
        return TaskRepresentation(
            domain=target_domain,
            name=src_task.name,
            inputs=input_transform(src_task.inputs),
            outputs=output_transform(src_task.outputs),
            metadata={**src_task.metadata, "mapped_from": src_task.domain},
        )

    return mapper


# ----------------------------------------------------------------------
# Example registrations (can be extended by the research team)
# ----------------------------------------------------------------------
def _register_builtin_bridges() -> None:
    # Code → Math (e.g., translate a code‑generation spec into a symbolic problem)
    DomainBridge.register(
        "code",
        "math",
        simple_mapper_factory(
            "math",
            input_transform=lambda i: {"description": i.get("prompt", ""), "language": "python"},
            output_transform=lambda o: {"expression": o.get("code", ""), "type": "symbolic"},
        ),
    )

    # UI Design → System Architecture (high‑level sketch → component diagram)
    DomainBridge.register(
        "ui",
        "architecture",
        simple_mapper_factory(
            "architecture",
            input_transform=lambda i: {"wireframes": i, "style": "modern"},
            output_transform=lambda o: {"components": o, "connections": []},
        ),
    )


# Auto‑register on import
_register_builtin_bridges()