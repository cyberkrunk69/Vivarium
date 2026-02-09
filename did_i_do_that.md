# did_i_do_that.md

Purpose: capture every place in this repo that references or documents the
"hallucination" pattern (false claims, fabricated data, or model outputs
that do not match real state).

This is a raw index. It does not judge truth, it just lists evidence.

## Direct incident reports and validation notes (docs/legacy)

- docs/legacy/HALLUCINATION_BUG_FIX.md
  - Reports a "hallucination bug" investigation and fix.
  - Notes the system can log "HALLUCINATION" status when files are claimed
    but not modified, and that critic checks for hallucination patterns.

- docs/legacy/SWARM_VALIDATION_REPORT.md
  - States that verification failures mean the system "cannot distinguish
    actual work from hallucinations."

- docs/legacy/DONT_BE_STUPID.md
  - Section "Hallucinating Results Instead of Using Real Data" describes
    a fabricated failure taxonomy and warns to verify outputs.
  - Explicit lesson: "LLMs hallucinate. Verify outputs match reality."

- docs/legacy/GRIND_LOG_ANALYSIS.md
  - Defines "Hallucination/fabrication" as an error category.
  - Lists "Hallucinating data" as a mistake (invented data vs real files).

## Research and design references (docs/legacy)

- docs/legacy/AI_RESEARCH_FINDINGS.md
  - Notes that chain-of-thought prompting reduces hallucinations.

- docs/legacy/NOVEL_REASONING_RESEARCH.md
  - Multiple entries note that self-consistency and multi-sample CoT
    reduce hallucinations.

## Research and ideas (docs/ideas)

- docs/ideas/research/RESEARCH_FAILURE_MODES.md
  - Includes "Hallucination" as a logic failure category with
    CriticAgent-based detection.

- docs/ideas/research/LONG_TERM_PLANNING_RESEARCH.md
  - Lists "hallucinated resources" as a limitation of LLM planning.

- docs/ideas/research/RESEARCH_EXTERNAL_SURVEY.md
  - States that Gorilla-style API training reduces "hallucinated API calls."

- docs/ideas/research/RESEARCH_MULTI_AGENT_COORDINATION.md
  - References "structured outputs prevent hallucination cascading."

- docs/ideas/architecture/ARCHITECTURE_DIAGRAMS.md
  - Knowledge base stats include a "hallucination_factuality" category.

## Experiments (experiments/)

- experiments/exp_20260204_033433_unified_session_1/CURRENT_CAPABILITIES.md
  - Safety guardrails mention monitoring for hallucinations.

- experiments/exp_20260204_033253_unified_session_1/CURRENT_CAPABILITIES.md
  - Lists "plausible-but-incorrect answers (hallucinations)" as a limitation.

## Artifacts and schemas

- artifacts/schemas.py
  - Module comment says structured outputs prevent hallucination cascading.

## Grind log evidence (grind_logs/)

The following logs contain explicit "hallucination" references in task text
or summaries:

- grind_logs/session_1_run_2.json
  - Task: "CRITICAL: INVESTIGATE AND FIX SWARM HALLUCINATION BUG"
  - Summary claims a fix for workers "claiming to modify files" without writing.

- grind_logs/session_1_run_3.json
  - Same hallucination bug task, details verification and critic updates.

- grind_logs/session_1_run_4.json
  - Same hallucination bug task, includes "CRITICAL HALLUCINATION" phrasing.

- grind_logs/session_1_run_5.json
- grind_logs/session_1_run_6.json
- grind_logs/session_1_run_7.json
- grind_logs/session_1_run_8.json
- grind_logs/session_1_run_9.json
  - These runs include the same hallucination bug task context string.

- grind_logs/unified_session_111_run_1.json
- grind_logs/unified_session_174_run_1.json
- grind_logs/unified_session_193_run_1.json
  - Task text includes "prevents hallucination cascading" (structured artifacts).

Pre-hash snapshots also reference hallucination-related files:

- grind_logs/session_1_pre_hashes.json
- grind_logs/session_2_pre_hashes.json
- grind_logs/session_3_pre_hashes.json
- grind_logs/session_4_pre_hashes.json
- grind_logs/session_5_pre_hashes.json
- grind_logs/session_6_pre_hashes.json
  - These include file names like "HALLUCINATION_BUG_FIX.md" and
    "test_hallucination_detection.py" in their hash maps.

## Pattern summary (why this keeps showing up)

Across documentation, experiments, and logs, the recurring theme is:

- The system can claim work that did not actually happen.
- Verification and critic scoring were historically too trusting of claims.
- Structured outputs, self-consistency, and tool-verified actions are
  repeatedly suggested as mitigations.
