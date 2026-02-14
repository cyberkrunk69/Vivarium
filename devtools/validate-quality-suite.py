#!/usr/bin/env python3
"""
Quality Validation Suite — proves docs deliver understanding, not just facts.

Runs:
  1. Structural audit (hierarchy completeness)
  2. ELIV critic prompt generation (for LLM-as-critic scoring)
  3. Big picture rubric output

Evidence: reports/quality-audit-structural.txt, quality-audit-eliv.json, quality-audit-bigpicture.csv
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS = REPO_ROOT / "reports"

# Target files: check both local .docs/ and docs/livingDoc/
DEEP_FILES = [
    REPO_ROOT / "docs/livingDoc/vivarium/scout/router.py.deep.md",
    REPO_ROOT / "docs/livingDoc/vivarium/runtime/inference_engine.py.deep.md",
    REPO_ROOT / "docs/livingDoc/vivarium/scout/audit.py.deep.md",
]

# Fallback to local .docs/ if central doesn't exist
def _resolve_doc(path: Path) -> Path | None:
    if path.exists():
        return path
    # Map docs/livingDoc/vivarium/scout/X -> vivarium/scout/.docs/X
    rel = path.relative_to(REPO_ROOT)
    if "livingDoc" in str(rel):
        parts = list(rel.parts)
        idx = parts.index("livingDoc")
        # livingDoc/vivarium/scout/router.py.deep.md -> vivarium/scout/.docs/router.py.deep.md
        sub = Path(*parts[idx + 1 : -1])  # vivarium/scout
        fname = parts[-1]
        local = REPO_ROOT / sub / ".docs" / fname
        if local.exists():
            return local
    return None


def audit_hierarchy(filepath: Path) -> dict[str, bool]:
    """Check structural hierarchy per ticket spec."""
    content = filepath.read_text(encoding="utf-8")
    # Strict: ticket expects # TLDR, # ELIV at top
    # Relaxed: hybrid output has # Module Summary at top (no separate TLDR/ELIV)
    checks = {
        "file_tldr_top": bool(re.search(r"^# TLDR\s*$", content, re.MULTILINE)),
        "file_eliv_present": bool(re.search(r"^# ELIV\s*$", content, re.MULTILINE)),
        "module_summary_present": bool(re.search(r"# Module Summary", content)),
        "no_function_before_summary": _no_function_before_summary(content),
        # Relaxed (hybrid format)
        "summary_at_top": bool(re.search(r"^# Module Summary\s*$", content, re.MULTILINE)),
    }
    return checks


def _no_function_before_summary(content: str) -> bool:
    """True if no ## FunctionName/## ClassName appears before # TLDR or # Module Summary."""
    tldr_pos = content.find("# TLDR")
    summary_pos = content.find("# Module Summary")
    first_summary = min(
        p for p in (tldr_pos, summary_pos) if p >= 0
    ) if (tldr_pos >= 0 or summary_pos >= 0) else -1
    if first_summary < 0:
        return True  # no summary/tldr, vacuous
    before = content[:first_summary]
    # Check for ## Function: or ## Class: before summary
    if re.search(r"^## (Function|Class):", before, re.MULTILINE):
        return False
    return True


def run_structural_audit() -> bool:
    """Step 1: Structural audit. Returns True if all pass."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    all_pass = True

    for f in DEEP_FILES:
        resolved = _resolve_doc(f)
        if not resolved:
            lines.append(f"\n{f.relative_to(REPO_ROOT)}: NOT FOUND")
            all_pass = False
            continue
        checks = audit_hierarchy(resolved)
        lines.append(f"\n{resolved.relative_to(REPO_ROOT)}:")
        for name, passed in checks.items():
            status = "✅" if passed else "❌"
            lines.append(f"  {status} {name}")
            if not passed:
                all_pass = False

    out = REPORTS / "quality-audit-structural.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("".join(lines))
    return all_pass


def generate_eliv_critic_prompt() -> None:
    """Step 2: Generate ELIV critic prompt for LLM-as-critic scoring."""
    # Hybrid mode does NOT generate .eliv.md. Use Module Summary / deep content as proxy.
    samples: list[dict] = []
    source_truth = {
        "vivarium/scout/router.py": "Routes LLM queries to tools based on cost/budget constraints; enforces MAX_EXPANDED_CONTEXT ceiling; audits all tool invocations",
        "vivarium/runtime/inference_engine.py": "Executes LLM inference with engine selection (70B/8B); tracks token costs; enforces budget exhaustion guardrails",
        "vivarium/scout/audit.py": "Append-only JSONL event log; line buffering, fsync cadence, log rotation; tracks Scout costs and events",
    }

    for deep_path in DEEP_FILES:
        resolved = _resolve_doc(deep_path)
        if not resolved or not resolved.exists():
            continue
        content = resolved.read_text(encoding="utf-8")
        # Extract first 800 chars as "explain" content (Module Summary + start of detail)
        explain_section = content[:800].strip()
        rel = str(resolved.relative_to(REPO_ROOT))
        if "livingDoc" in rel:
            # docs/livingDoc/vivarium/scout/router.py.deep.md -> vivarium/scout/router.py
            parts = Path(rel).parts
            idx = parts.index("livingDoc")
            module_key = "/".join(parts[idx + 1 : -1]) + "/" + resolved.name.replace(".deep.md", "")
        else:
            # vivarium/scout/.docs/router.py.deep.md -> vivarium/scout/router.py
            module_key = str(resolved.parent.parent.relative_to(REPO_ROOT)) + "/" + resolved.name.replace(".deep.md", "")
        samples.append({
            "module": module_key,
            "eliv_section": explain_section,
            "source_truth": source_truth.get(module_key, "(verify from source)"),
        })

    critic_prompt = """You are a documentation quality auditor. For each sample:
1. Extract the core claim from the ELIV/explain section
2. Compare against source truth
3. Score on two dimensions (1-5):
   - Factual fidelity: Does the section distort or hallucinate facts?
   - Pedagogical clarity: Would a beginner understand the "why" in <30 seconds?

Respond in JSON for each sample:
{
  "module": "name",
  "factual_fidelity": 1-5,
  "pedagogical_clarity": 1-5,
  "distortions": ["list any factual errors"],
  "clarity_issues": ["list any confusing phrasing"]
}
"""

    payload = {
        "critic_prompt": critic_prompt,
        "samples": samples,
        "note": "Hybrid doc-sync does not generate .eliv.md; using Module Summary / deep content as proxy.",
    }
    out = REPORTS / "quality-audit-eliv.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\n✓ ELIV critic prompt written: {out}")
    print(f"  Samples: {len(samples)} (feed to GROQ/Gemini for scoring)")


def generate_bigpicture_rubric() -> None:
    """Step 3: Big picture rubric template for human spot check."""
    rows = [
        ["Module", "Architecture (1-5)", "Why exists (1-5)", "Missing critical context?"],
        ["router.py", "", "", ""],
        ["inference_engine.py", "", "", ""],
        ["audit.py", "", "", ""],
        ["vivarium/scout/ (module)", "", "", ""],
        ["vivarium/ (project)", "", "", ""],
    ]
    csv_content = "\n".join(",".join(r) for r in rows)
    out = REPORTS / "quality-audit-bigpicture.csv"
    out.write_text(csv_content, encoding="utf-8")
    print(f"\n✓ Big picture rubric template: {out}")
    print("  Pass criteria: Average ≥4.0, zero critical omissions")


def run_cascade_audit() -> bool:
    """Step 4: Cascade integrity — module/project summaries have normie TLDR/ELIV."""
    cascade_checks = [
        (REPO_ROOT / "docs/livingDoc/vivarium/scout/__init__.py.module.md", ["foreman", "construction"]),
        (REPO_ROOT / "docs/livingDoc/vivarium/runtime/__init__.py.module.md", ["fleet", "delivery"]),
        (REPO_ROOT / "docs/livingDoc/vivarium/__init__.py.module.md", ["pit crew", "nascar"]),
    ]
    all_pass = True
    for p, normie_keywords in cascade_checks:
        if not p.exists():
            print(f"  ❌ Missing: {p.relative_to(REPO_ROOT)}")
            all_pass = False
            continue
        content = p.read_text(encoding="utf-8")
        has_tldr = bool(re.search(r"^# TLDR\s*$", content, re.MULTILINE))
        has_eliv = bool(re.search(r"^# ELIV\s*$", content, re.MULTILINE))
        has_normie = any(kw in content.lower() for kw in normie_keywords)
        if has_tldr and has_eliv and has_normie:
            print(f"  ✅ {p.relative_to(REPO_ROOT)}")
        else:
            print(f"  ❌ {p.relative_to(REPO_ROOT)} (tldr={has_tldr}, eliv={has_eliv}, normie={has_normie})")
            all_pass = False
    return all_pass


def main() -> int:
    print("=== Quality Validation Suite ===\n")
    print("Step 1: Structural audit")
    struct_ok = run_structural_audit()
    print("\nStep 2: ELIV critic prompt generation")
    generate_eliv_critic_prompt()
    print("\nStep 3: Big picture rubric")
    generate_bigpicture_rubric()
    print("\nStep 4: Cascade audit")
    cascade_ok = run_cascade_audit()

    if struct_ok and cascade_ok:
        print("\n✅ Structural audit + Cascade: PASS")
        return 0
    if not struct_ok:
        print("\n❌ Structural audit: FAIL (see reports/quality-audit-structural.txt)")
    if not cascade_ok:
        print("\n❌ Cascade audit: FAIL — run devtools/generate-cascade-summaries.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
