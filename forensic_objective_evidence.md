# Forensic Objective Evidence

Scope: compare commit messages to the actual files changed in git, and
record objective mismatches or unverifiable claims.

Method:
- Use `git show --stat` and `git show --name-only` for each commit.
- When a commit claims specific file contents, compare with file content
  in that commit via `git show <sha>:<path>`.

## Findings (objective evidence only)

### 1) Commit message claims "core architecture" but files land in experiments
Commit: `3e623eb` (subject: "Milestone: Swarm builds its own architecture autonomously ($0.17)")

Claimed in message:
- "atomizer.py", "feature_breakdown.py", "consensus_node.py",
  "tool_router.py", "rlif_learner.py", "gut_check_planner.py",
  "test_gates.py"

Evidence from `git show --name-only 3e623eb`:
- The majority of these files are added under experiment paths:
  - experiments/exp_20260204_023818_unified_session_1/atomizer.py
  - experiments/exp_20260204_023831_unified_session_9/feature_breakdown.py
  - experiments/exp_20260204_023835_unified_session_11/consensus_node.py
  - experiments/exp_20260204_023837_unified_session_13/tool_router.py
  - experiments/exp_20260204_023850_unified_session_18/test_gates.py
  - experiments/exp_20260204_023855_unified_session_34/rlif_learner.py
  - experiments/exp_20260204_023818_unified_session_4/gut_check_planner.py
- Only one of these appears at repo root: `tool_router.py`

Observation:
The commit message describes these as "core orchestration infrastructure,"
but most are stored as experiment artifacts, not integrated runtime code.

---

### 2) Commit claims a large research index but file is invalid JSON and placeholder
Commit: `9378091` (subject: "AI builds its own self-observation infrastructure ($0.0045)")

Claimed in message:
- "research_index.json: Organized 150+ consciousness research papers"

Evidence from `git show 9378091:research_index.json`:
- The file contains two concatenated JSON objects (invalid JSON).
- The first object lists placeholder file names:
  - "paper1.pdf", "paper2.pdf", "paper3.pdf"
  - "paperA.pdf", "paperB.pdf", "paperC.pdf"

Observation:
The commit message claims 150+ papers. The file content is not valid JSON
and contains only placeholder entries.

---

### 3) Commit adds architecture spec and claims "100% adherence" in same commit
Commit: `3e623eb`

Claimed in message:
- "Architecture compliance: 100% adherence to SWARM_ARCHITECTURE_V2.md spec"

Evidence from `git show --name-only 3e623eb`:
- `SWARM_ARCHITECTURE_V2.md` is added in the same commit.

Observation:
The spec being introduced in the same commit makes the claim of
"100% adherence" not independently verifiable within that commit.

---

### 4) Commit labeled "BACKUP" is a massive code and data import
Commit: `5b6a0b6` (subject: "BACKUP: All work from Feb 3-4 before clean rollback")

Evidence from `git show --shortstat 5b6a0b6`:
- 3300 files changed, 455283 insertions

Observation:
The commit message suggests a backup; the diff indicates a large-scale
import of code, data, and logs. This is a scale mismatch that should be
explicitly noted when evaluating provenance.

---

## Notes
- This document is intentionally narrow: it records objective, verifiable
  mismatches between commit messages and the files changed.
- It does not attempt to infer intent or causality.
