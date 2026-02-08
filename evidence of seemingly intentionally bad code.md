# Evidence of seemingly intentionally bad code

Scope: This document lists concrete, verifiable anomalies found in the
black-swarm repository. It does NOT prove intent. It documents evidence
of broken, contradictory, or nonfunctional code that appears difficult
to explain as normal mistakes.

All references use file:line ranges from the current repo snapshot.

## 1) Concatenated or conflicting implementations in a single file

- file_permission_gateway.py:
  - A complete implementation ends around L1-L109, then a new module
    docstring and fresh imports begin at L109-L125, indicating multiple
    full versions appended into one file.
  - This pattern repeats throughout the file, producing multiple
    competing request_edit APIs.

- skill_registry.py:
  - The _text_to_embedding docstring opens at L15-L17 but immediately
    gives way to unindented imports at L18-L24, indicating a broken
    or pasted fragment inside a function body.
  - The file mixes unrelated sections and side-effect logic in one place.

- recursive_improvement_engine.py:
  - The class RecursiveImprovementEngine is defined multiple times
    in the same file (e.g., L18, L121, L228, L334, L505, etc.), so later
    definitions overwrite earlier behavior.

- safety/recursion_bounds.py:
  - Multiple conflicting constants and APIs appear in the same file:
    MAX_RECURSION_DEPTH (L4-L6 and again at L85-L88),
    MAX_DEPTH (L34-L36 and L51-L53), plus multiple check_depth/safety_check
    definitions (L37-L45, L60-L77, L92-L105, L145-L154, L187-L195).

These are not minor style issues; they create ambiguous, order-dependent
behavior and make the actual runtime logic unclear.

## 2) Nonexistent imports / ghost modules

- agi_capability_architecture.py imports modules that do not exist in the
  repo: novel_reasoning, cross_domain.alignment, recursion.rdn,
  planning.hltp, meta_learning.controller, embodiment.interface (L871-L877).
  This is a guaranteed runtime failure path.

- recursive_improvement_engine.py attempts to import atomizer, task_builder,
  meta_builder, architecture_evolver (L239-L256 and L941-L958), none of which
  exist in the repo.

## 3) Dependency mismatch (code uses libraries not declared)

- requirements.txt contains only:
  fastapi, uvicorn, sse-starlette (L1-L3).

- worker.py imports httpx (L15), which is not declared in requirements.txt.

- agi_capability_architecture.py imports transformers and torch_geometric
  (L664-L668), and torch (L719-L723, L1197-L1199), none of which are in
  requirements.txt.

This guarantees runtime failures in a clean environment.

## 4) Brittle defaults and silent failure in core runtime

- Hard-coded local API defaults:
  - config.py uses http://127.0.0.1:8420 (L6-L7).
  - worker.py falls back to that same URL if queue.json lacks api_endpoint
    (L269-L271).
  - Any non-local deployment will fail unless the environment is set up
    exactly to match this default.

- worker.py silently treats JSON/IO errors as an empty queue/log
  (L66-L87), which causes quiet termination instead of a hard failure.

- worker.py lock lifecycle can leak on exceptions:
  - find_and_execute_task wraps the entire task loop in a broad try/except
    (L266-L319), which makes lock release dependent on the happy path.

- orchestrator.py runs workers without a timeout:
  - subprocess.run(..., capture_output=True, text=True) has no timeout
    (L60-L64). A hung worker can stall the orchestrator indefinitely.

## 5) Roadmap/docs claim functionality that is not implemented

- AGI_ROADMAP_2026.md lists NSHR/DAEA/MOGHN as core techniques (L12-L26) and
  tasks to deploy them (L58-L66), yet implementations are stubs or absent.

- ARCHITECTURE_EVOLUTION_PROPOSAL.md proposes gossip-based coordination and
  skill pods (L94-L103, L120-L130), but no implementation exists in code.

## 6) Unexpected side effects at import time

- skill_registry.py patches grind_spawner on import via _patch_grind_spawner()
  (L67-L86). This is a global side effect and makes behavior order-dependent.

---

## Summary

The issues above are concrete, repeatable, and code-level. They include:
broken syntax fragments, multiple overlapping implementations, nonexistent
imports, missing dependencies, and brittle defaults that cause silent
failure. This is evidence of severely compromised code quality. It does
not prove intent, but it does document patterns consistent with
deliberately fragile or sabotaged code.
