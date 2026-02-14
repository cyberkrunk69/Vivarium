#!/usr/bin/env python3
"""
ELIV Critic — scores pedagogical quality via GROQ.
Proves ELIV delivers understanding, not just structural presence.

Extracts # ELIV section from .deep.md (hybrid docs; .eliv.md not generated).
Scores: factual_fidelity, pedagogical_clarity (1-5 each).
Gate: exit 0 if both averages ≥4.0.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def extract_eliv_from_deep(deep_path: Path) -> str:
    """Extract ELIV section from .deep.md (between # ELIV and next # or end)."""
    if not deep_path.exists():
        return ""
    content = deep_path.read_text(encoding="utf-8")
    m = re.search(r"^# ELIV\s*\n(.*?)(?=^# |\Z)", content, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="ELIV Critic — score pedagogical quality via GROQ")
    parser.add_argument("--dry-run", action="store_true", help="Print ELIV text + source truth, skip API")
    args = parser.parse_args()
    # Hybrid docs: ELIV is in .deep.md, not .eliv.md
    samples = [
        {
            "module": "vivarium/scout/router.py",
            "eliv_text": extract_eliv_from_deep(
                REPO_ROOT / "vivarium/scout/.docs/router.py.deep.md"
            ),
            "source_truth": "Routes LLM queries to tools based on ScoutConfig budget constraints; enforces MAX_EXPANDED_CONTEXT=40000 ceiling to prevent token cost explosion; audits all tool invocations via AuditLog; blocks execution if estimated_cost exceeds remaining budget",
        },
        {
            "module": "vivarium/runtime/inference_engine.py",
            "eliv_text": extract_eliv_from_deep(
                REPO_ROOT / "vivarium/runtime/.docs/inference_engine.py.deep.md"
            ),
            "source_truth": "Executes LLM inference with engine selection (70B for complex tasks, 8B for simple); tracks token costs against budget; raises BudgetExhaustedError when cost ceiling reached; uses COST_PER_MILLION_* constants for accurate billing",
        },
        {
            "module": "vivarium/scout/audit.py",
            "eliv_text": extract_eliv_from_deep(
                REPO_ROOT / "vivarium/scout/.docs/audit.py.deep.md"
            ),
            "source_truth": "Append-only JSONL event log; line buffering, fsync cadence, log rotation; tracks Scout costs and events; used by router for budget enforcement and cost auditing",
        },
    ]

    if args.dry_run:
        print("ELIV Critic — Dry Run (no API)\n")
        for s in samples:
            print(f"=== {s['module']} ===\nELIV:\n{s['eliv_text']}\n\nSource Truth:\n{s['source_truth']}\n")
        print("Run with GROQ_API_KEY set to score via API.")
        return 0

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not set. Set it to run ELIV critic.", file=sys.stderr)
        print("   Or run with --dry-run to see ELIV text for human validation.", file=sys.stderr)
        return 2

    try:
        from groq import Groq
    except ImportError:
        print("❌ groq package not installed. pip install groq", file=sys.stderr)
        return 2

    client = Groq(api_key=api_key)
    results = []

    for sample in samples:
        prompt = f"""ELIV Text:
{sample['eliv_text']}

Source Truth:
{sample['source_truth']}

Score (1-5):
- Factual fidelity: Does ELIV distort or hallucinate facts?
- Pedagogical clarity: Would a beginner grasp the "why" in <30 seconds?

Respond JSON only:
{{"module": "...", "factual_fidelity": N, "pedagogical_clarity": N, "distortions": [...], "clarity_issues": [...]}}"""

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown code fence if present
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
        result = json.loads(raw)
        result["module"] = sample["module"]
        results.append(result)

    REPO_ROOT.joinpath("reports").mkdir(parents=True, exist_ok=True)
    out_path = REPO_ROOT / "reports" / "eliv-critic-results.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    avg_fidelity = sum(r.get("factual_fidelity", 0) for r in results) / len(results)
    avg_clarity = sum(r.get("pedagogical_clarity", 0) for r in results) / len(results)

    print("ELIV Critic Results:")
    for r in results:
        print(f"  {r['module']}: fidelity={r.get('factual_fidelity', '?')}/5, clarity={r.get('pedagogical_clarity', '?')}/5")
    print(f"  Avg Factual Fidelity: {avg_fidelity:.1f}/5")
    print(f"  Avg Pedagogical Clarity: {avg_clarity:.1f}/5")
    print(f"  Evidence: {out_path}")

    if avg_fidelity >= 4.0 and avg_clarity >= 4.0:
        print("✅ PEDAGOGICAL QUALITY GATE PASSED")
        return 0
    print("❌ PEDAGOGICAL QUALITY GATE FAILED (need ≥4.0 on both)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
