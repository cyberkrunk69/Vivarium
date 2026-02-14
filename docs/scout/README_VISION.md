# Scout Vision README

## Purpose

Scout exists to make AI-assisted software development more trustworthy, more
auditable, and less expensive to operate in real codebases.

The long-term vision is not "faster autocomplete." The long-term vision is a
durable collaboration system where:

- code context stays current without manual archaeology,
- AI outputs are easier to verify,
- automation remains human-governed,
- and costs are visible before they become surprises.

## Why Scout Exists

Modern teams hit the same recurring pain:

1. AI assistants lose context in large repositories.
2. Existing docs drift from source quickly.
3. Commit and PR writing is repetitive and often low signal.
4. "Magic" automation hides cost, confidence, and failure states.
5. Tooling gets tied to one editor or one model vendor.

Scout is the response: a text-first, Git-native layer that turns code into
living documentation and uses those artifacts as the shared substrate for
drafting and review.

## Vision Statement

Scout should become the "context operating layer" for development workflows:

- **Context is continuously generated and versioned**
  - Symbol and module docs are generated from source, stored in-repo, and
    diff-aware.
- **Automation is inspectable by default**
  - Every meaningful LLM operation is logged with cost and metadata.
- **Authoring loops are low friction**
  - Commit and PR drafts are assembled from existing artifacts, minimizing
    expensive calls at decision time.
- **Failure modes are explicit**
  - Budget limits, stale docs, and unresolved context should be surfaced as
    first-class states, not hidden side effects.
- **Humans remain decision owners**
  - Scout can prepare, summarize, and propose. Humans approve, merge, and ship.

## Product Principles

1. **Text over lock-in**
   - Prefer plain Markdown/JSON artifacts over proprietary state.
2. **Truth over style**
   - Correctness and traceability are more important than polished but vague prose.
3. **Cost is a product feature**
   - Spend controls and auditability are required behavior, not optional extras.
4. **Progressive autonomy**
   - Start with assistive tooling, then automate only where confidence and rollback
     posture are strong.
5. **Git-native by design**
   - Outputs and state should fit normal repository workflows.

## What Scout Is Aiming To Be

At maturity, Scout should provide:

- Reliable continuous documentation coverage across the repo.
- Deterministic commit/PR draft assembly backed by fresh context.
- Query/navigation that is scoped, explainable, and resistant to hallucination.
- CI enforcement for doc freshness and workflow integrity.
- Hook and CLI ergonomics that work out of the box on fresh clone.

## What Scout Is Right Now (Current Reality)

Scout today already delivers meaningful value:

- living docs (`.tldr.md`, `.deep.md`, `.eliv.md`),
- diff-aware regeneration via source and symbol hashes,
- call graph export and impact summaries,
- draft generation + assembly,
- cost and event audit logs,
- index-first navigation and optional LLM fallback.

Scout also has active hardening work:

- some top-level devtool wrappers have drifted from runtime requirements,
- hook installer/templates need tighter consistency checks,
- docs and command surfaces need stronger anti-drift guardrails.

This is expected for the current stage: a capable core with integration polish
still in progress.

## Near-Term Mission

The near-term mission is reliability hardening, not feature explosion:

- make wrappers and hooks deterministic on fresh clone,
- align docs with actual command surfaces,
- tighten validation around generated doc quality invariants,
- and protect these with fast smoke checks in CI.

## Non-Goals (for Now)

- Becoming a closed IDE-only experience.
- Replacing code review ownership or merge decisions.
- Hiding uncertainty to appear "smart."
- Optimizing for demos at the expense of operational clarity.

## Success Criteria

Scout is succeeding when teams can say:

- "Our AI context is usually current."
- "We can explain what automation did and what it cost."
- "Onboarding into this repo is easier because docs are attached to code."
- "When Scout fails, it fails loudly and recoverably."

## Companion Documents

- Technical implementation and current architecture:
  - `README_TECHNICAL.md`
- Configuration reference:
  - `CONFIGURATION.md`
- Audit schema reference:
  - `AUDIT_SCHEMA.md`
- Current-state white paper:
  - `../../.github/PR_WHITEPAPER.md`
