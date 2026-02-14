"""
Pressure-test the confidence extraction prompt against real Scout context.

Runs 3 queries through Groq 70B with CONFIDENCE_PROMPT.
Deliverable: test_results/prompts_first_person.json with raw 70B outputs + parse status.

Success criteria:
- All 3 outputs contain confidence_score: X.XX (parseable)
- All confidence values ∈ [0.00, 1.00] (no hallucinated >1.0)
- All outputs declare gaps via [GAP] OR "None identified — verified coverage of N symbols"
- Fail fast on any parse exception — log raw output for Intern B
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add repo root for imports
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CONFIDENCE_PROMPT = """You are a codebase analyst. Answer the user's question based ONLY on the provided context.

REQUIRED OUTPUT FORMAT (strict):
1. Start with: confidence_score: X.XX  (where X.XX is a float in [0.00, 1.00])
2. Then your analysis (plain text).
3. End with exactly one of:
   - [GAP] <description of what is missing or uncertain>
   - OR: None identified — verified coverage of N symbols  (where N is the count of symbols you verified)

Rules:
- confidence_score MUST be parseable (e.g. 0.75, 0.92, 0.00)
- confidence_score MUST be between 0.00 and 1.00 inclusive
- You MUST declare gaps or verified coverage — no exceptions
"""

GROQ_70B_MODEL = "llama-3.1-70b-versatile"


def _collect_docs(repo_root: Path, scope: str, include_deep: bool) -> list[tuple[str, str, str]]:
    """Collect .tldr.md and optionally .deep.md for scope. Returns (module_path, suffix, content)."""
    root = repo_root.resolve()
    scope_path = Path(scope)
    seen: set[tuple[str, str]] = set()
    results: list[tuple[str, str, str]] = []
    suffixes = [".tldr.md"]
    if include_deep:
        suffixes.append(".deep.md")

    central = root / "docs" / "livingDoc" / scope_path
    if central.exists():
        for md_path in central.rglob("*.md"):
            stem = md_path.stem
            if stem.endswith(".tldr"):
                suffix = ".tldr.md"
                stem = stem.removesuffix(".tldr")
            elif stem.endswith(".deep"):
                suffix = ".deep.md"
                stem = stem.removesuffix(".deep")
            else:
                continue
            if suffix not in suffixes:
                continue
            try:
                rel = md_path.parent.relative_to(central)
                module_path = f"{rel / stem}".replace("\\", "/") if rel != Path(".") else stem
            except ValueError:
                module_path = stem
            key = (module_path, suffix)
            if key in seen:
                continue
            seen.add(key)
            try:
                content = md_path.read_text(encoding="utf-8", errors="replace").strip()
                results.append((module_path, suffix, content))
            except OSError:
                pass

    scope_dir = root / scope_path
    if scope_dir.exists():
        for docs_dir in scope_dir.rglob(".docs"):
            if not docs_dir.is_dir():
                continue
            for suffix in suffixes:
                for md_path in docs_dir.glob(f"*{suffix}"):
                    stem = md_path.stem.removesuffix(suffix.removesuffix(".md"))
                    try:
                        parent_rel = docs_dir.parent.relative_to(scope_dir)
                        module_path = f"{parent_rel / stem}".replace("\\", "/") if str(parent_rel) != "." else stem
                    except ValueError:
                        module_path = stem
                    key = (module_path, suffix)
                    if key in seen:
                        continue
                    seen.add(key)
                    try:
                        content = md_path.read_text(encoding="utf-8", errors="replace").strip()
                        results.append((module_path, suffix, content))
                    except OSError:
                        pass
    return results


def _build_prompts_context(repo_root: Path) -> str:
    """Build context from Scout living docs (prompts in doc_generation, router, big_brain)."""
    results = _collect_docs(repo_root, "vivarium/scout", include_deep=True)
    # Focus on modules with prompts
    prompt_modules = {"doc_generation", "router", "big_brain", "llm"}
    lines = []
    for module_path, suffix, content in sorted(results, key=lambda x: (x[0], x[1])):
        mod = module_path.split("/")[-1].replace(".py", "")
        if mod in prompt_modules:
            depth = "deep" if suffix == ".deep.md" else "tldr"
            lines.append(f"## {module_path} ({depth})\n\n{content}\n")
    return "\n---\n\n".join(lines) if lines else "(no docs found)"


def _build_safety_context(repo_root: Path) -> str:
    """Build context for safety preflight from runtime + LLM_CONTEXT."""
    parts = []
    llm_ctx = repo_root / "docs" / "LLM_CONTEXT.md"
    if llm_ctx.exists():
        parts.append(llm_ctx.read_text(encoding="utf-8", errors="replace"))
    sg = repo_root / "vivarium" / "runtime" / "safety_gateway.py"
    if sg.exists():
        parts.append(f"\n\n---\n\n# safety_gateway.py\n\n{sg.read_text(encoding='utf-8', errors='replace')[:6000]}")
    wr = repo_root / "vivarium" / "runtime" / "worker_runtime.py"
    if wr.exists():
        text = wr.read_text(encoding="utf-8", errors="replace")
        # Extract safety-related section
        start = text.find("def _run_worker_safety_check")
        if start >= 0:
            end = text.find("\ndef ", start + 5)
            end = end if end >= 0 else start + 1500
            parts.append(f"\n\n---\n\n# worker_runtime (safety)\n\n{text[start:end]}")
    return "\n".join(parts)


def _build_cycle_context(repo_root: Path) -> str:
    """Build context for worker_runtime.cycle from swarm_api + worker_runtime."""
    parts = []
    sa = repo_root / "vivarium" / "runtime" / "swarm_api.py"
    if sa.exists():
        text = sa.read_text(encoding="utf-8", errors="replace")
        # Extract cycle endpoint and related
        start = text.find("@app.post(\"/cycle\"")
        if start >= 0:
            end = text.find("\n@app.", start + 10)
            end = end if end >= 0 else start + 2500
            parts.append(f"# swarm_api.py (cycle)\n\n{text[start:end]}")
        # _pre_execute_safety_report
        idx = text.find("def _pre_execute_safety_report")
        if idx >= 0:
            e = text.find("\ndef ", idx + 5)
            e = e if e >= 0 else idx + 600
            parts.append(f"\n\n# _pre_execute_safety_report\n\n{text[idx:e]}")
    wr = repo_root / "vivarium" / "runtime" / "worker_runtime.py"
    if wr.exists():
        text = wr.read_text(encoding="utf-8", errors="replace")
        # CYCLE_EXECUTION_ENDPOINT and cycle-related
        for m in re.finditer(r"(CYCLE_EXECUTION_ENDPOINT|def.*cycle|/cycle)", text):
            start = max(0, m.start() - 200)
            end = min(len(text), m.end() + 800)
            parts.append(f"\n\n# worker_runtime (cycle)\n\n{text[start:end]}")
            break
    return "\n".join(parts)


def _parse_confidence(raw: str) -> tuple[float | None, str | None]:
    """Extract confidence_score from raw output. Returns (score, parse_error)."""
    m = re.search(r"confidence_score\s*:\s*([\d.]+)", raw, re.IGNORECASE)
    if not m:
        return None, "confidence_score: X.XX not found"
    try:
        val = float(m.group(1))
        if not (0.0 <= val <= 1.0):
            return val, f"confidence {val} outside [0.00, 1.00]"
        return val, None
    except ValueError as e:
        return None, str(e)


def _has_gaps_declaration(raw: str) -> bool:
    """True if output declares gaps via [GAP] or verified coverage."""
    if "[GAP]" in raw:
        return True
    if re.search(r"None identified\s*—\s*verified coverage of\s+\d+\s+symbols", raw, re.IGNORECASE):
        return True
    return False


async def _run_query(
    query_id: str,
    question: str,
    context: str,
    llm_client,
) -> dict:
    """Run one query through Groq 70B. Returns result dict with raw, parse status."""
    full_prompt = f"""{CONFIDENCE_PROMPT}

---
CONTEXT:
{context[:28000]}

---
QUESTION: {question}

---
YOUR RESPONSE (must include confidence_score and gaps/verified):"""

    try:
        resp = await llm_client(
            full_prompt,
            model=GROQ_70B_MODEL,
            system="You output structured responses. Always include confidence_score and gaps.",
            max_tokens=1024,
        )
        raw = resp.content.strip()
    except Exception as e:
        return {
            "query_id": query_id,
            "question": question,
            "raw_output": None,
            "parse_status": "error",
            "parse_error": str(e),
            "confidence_score": None,
            "confidence_valid": False,
            "gaps_declared": False,
        }

    score, parse_err = _parse_confidence(raw)
    gaps_ok = _has_gaps_declaration(raw)
    confidence_valid = score is not None and parse_err is None

    return {
        "query_id": query_id,
        "question": question,
        "raw_output": raw,
        "parse_status": "ok" if parse_err is None and confidence_valid and gaps_ok else "fail",
        "parse_error": parse_err,
        "confidence_score": float(score) if score is not None else None,
        "confidence_valid": confidence_valid and (score is not None and 0 <= score <= 1),
        "gaps_declared": gaps_ok,
    }


async def _mock_groq(prompt: str, model: str = "", system: str = "", max_tokens: int = 0):
    """Mock response for dry-run (no API key needed)."""
    from types import SimpleNamespace
    return SimpleNamespace(
        content="confidence_score: 0.75\nMock analysis.\nNone identified — verified coverage of 3 symbols",
        cost_usd=0.0,
        model=model,
        input_tokens=0,
        output_tokens=0,
    )


async def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Use mock LLM, no API key")
    args = parser.parse_args()

    if args.dry_run:
        llm_client = _mock_groq
    else:
        from vivarium.scout.llm import call_groq_async
        llm_client = call_groq_async

    repo_root = REPO_ROOT
    prompts_context = _build_prompts_context(repo_root)
    safety_context = _build_safety_context(repo_root)
    cycle_context = _build_cycle_context(repo_root)

    queries = [
        (
            "first_person",
            "How would changing all prompts to use first person instead of third affect the repo?",
            prompts_context,
        ),
        (
            "safety_remove",
            "What happens if I remove the safety preflight check?",
            safety_context,
        ),
        (
            "cycle_refactor",
            "What breaks if I refactor worker_runtime.cycle to async/await?",
            cycle_context,
        ),
    ]

    results = []
    for query_id, question, context in queries:
        print(f"Running {query_id}...", flush=True)
        r = await _run_query(query_id, question, context, llm_client)
        results.append(r)
        if r["parse_status"] == "error":
            print(f"  FAIL (API): {r['parse_error']}", flush=True)
            out_path = repo_root / "test_results" / "prompts_first_person.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "run_status": "api_error",
                "failed_query_id": query_id,
                "results": results,
                "raw_output_for_intern_b": None,
                "api_error": r["parse_error"],
            }
            out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return 1
        if r["parse_status"] == "fail":
            print(f"  FAIL (parse): {r['parse_error']} | gaps={r['gaps_declared']}", flush=True)
            # Fail fast: log raw for Intern B and exit
            out_path = repo_root / "test_results" / "prompts_first_person.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "run_status": "fail_fast",
                "failed_query_id": query_id,
                "results": results,
                "raw_output_for_intern_b": r.get("raw_output"),
            }
            out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return 1
        print(f"  OK: confidence={r['confidence_score']}", flush=True)

    out_path = repo_root / "test_results" / "prompts_first_person.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_status": "pass",
        "results": results,
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
