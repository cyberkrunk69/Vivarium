"""Shared library for ci-status-dry-run and ci-status-execute scripts.
Provides preprocessing, token counting, cost estimation, and Groq API calls."""
import os
import json
import re
import sys

# Add repo root to path for llm_cost import
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from vivarium.utils.llm_cost import estimate_cost, rough_token_count


def preprocess_log_for_ai(log_text):
    lines = log_text.split("\n")
    filtered_lines = []
    for line in lines:
        stripped_line = line.strip()
        if (
            not stripped_line
            or re.search(r"\[3[0-9];1m|\[0m", stripped_line)
            or "##[group]" in stripped_line
            or "##[endgroup]" in stripped_line
            or "shell: /usr/bin/bash" in stripped_line
            or "env:" in stripped_line
            or re.match(r"^\s*\d+%\s*$", stripped_line)
            or ("Downloading" in stripped_line and ".whl" in stripped_line)
        ):
            continue
        cleaned_line = re.sub(
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z\s*", "", stripped_line
        )
        cleaned_line = re.sub(
            r"^.*\s+\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z\s*",
            "",
            cleaned_line,
        )
        cleaned_line = re.sub(r"^.*tests\s+", "", cleaned_line)
        cleaned_line = re.sub(r"^.*Enforce runtime coverage\s+", "", cleaned_line)
        if cleaned_line.strip():
            filtered_lines.append(cleaned_line.strip())

    condensed_parts = []
    i = 0
    while i < len(filtered_lines):
        line = filtered_lines[i]
        if (
            "FAILED" in line
            or "ERROR" in line.upper()
            or "FAIL" in line.upper()
            or "AssertionError" in line
            or "Traceback" in line
            or ("coverage" in line.lower() and "fail" in line.lower())
        ):
            block_start = max(0, i - 2)
            block_end = min(len(filtered_lines), i + 15)
            condensed_parts.extend(filtered_lines[block_start:block_end])
            i = block_end
            continue
        i += 1

    if not condensed_parts:
        condensed_parts = filtered_lines[-20:]

    final_lines = []
    prev_line = None
    for line in condensed_parts:
        if line != prev_line:
            final_lines.append(line)
        prev_line = line

    return "\n".join(final_lines)


def estimate_cost_for_condensed_log(condensed_log):
    """Estimate USD cost for a single API call (no request made). Returns 0 if log too short."""
    result = estimate_tokens_and_cost_for_condensed_log(condensed_log)
    return result[2] if result else 0.0


def estimate_tokens_and_cost_for_condensed_log(condensed_log):
    """Estimate (input_tokens, output_tokens, cost_usd) for a single API call. Returns None if log too short."""
    if len(condensed_log) < 50:
        return None
    prompt = f"""
    Analyze this condensed CI/CD failure log snippet and provide a concise summary with:
    1. Root cause (one sentence)
    2. Specific error type (e.g., syntax, dependency, timeout, test failure, coverage issue)
    3. Affected component/file (if clearly mentioned)
    4. Action item (what needs to be fixed, be specific)
    
    Format as short bullet points. Be extremely brief - under 150 words total.
    
    CONDENSED LOG SNIPPET:
    {condensed_log}
    """
    input_tokens = rough_token_count(prompt)
    output_tokens = 150  # typical summary length
    cost_usd = estimate_cost("llama-3.1-8b-instant", input_tokens, output_tokens)
    return (input_tokens, output_tokens, cost_usd)


GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_groq_api(condensed_log, api_key):
    """Call Groq API. Returns (summary, cost_info). cost_info is dict with input_tokens, output_tokens, cost_usd, or None if no API call."""
    if len(condensed_log) < 50:
        return (condensed_log, None)

    import requests  # Ensured by ensure_python_deps() before AI mode runs
    prompt = f"""
    Analyze this condensed CI/CD failure log snippet and provide a concise summary with:
    1. Root cause (one sentence)
    2. Specific error type (e.g., syntax, dependency, timeout, test failure, coverage issue)
    3. Affected component/file (if clearly mentioned)
    4. Action item (what needs to be fixed, be specific)
    
    Format as short bullet points. Be extremely brief - under 150 words total.
    
    CONDENSED LOG SNIPPET:
    {condensed_log}
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 250,
    }

    try:
        response = requests.post(
            GROQ_CHAT_URL,
            headers=headers,
            json=payload,
            timeout=45,
        )
        response.raise_for_status()
        result = response.json()
        summary = result["choices"][0]["message"]["content"].strip()
        summary = summary if summary else "[AI Summary: Generated, but empty]"

        # Extract actual usage from response; fall back to estimate if missing
        usage = result.get("usage") or {}
        input_tokens = usage.get("prompt_tokens") or rough_token_count(prompt)
        output_tokens = usage.get("completion_tokens") or min(
            250, rough_token_count(summary)
        )
        cost_usd = estimate_cost("llama-3.1-8b-instant", input_tokens, output_tokens)
        return (
            summary,
            {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": cost_usd,
            },
        )
    except requests.exceptions.RequestException as e:
        return (
            f"[AI Summary Failed: {type(e).__name__}] Condensed log:\n{condensed_log[:300]}...",
            None,
        )
    except Exception as e:
        return (
            f"[Summary Error: {type(e).__name__}] Condensed log:\n{condensed_log[:300]}...",
            None,
        )


def extract_programmatic_summary(condensed_log):
    if "coverage" in condensed_log.lower() and (
        "fail" in condensed_log.lower()
        or "<" in condensed_log
        or "below" in condensed_log.lower()
    ):
        cov_match = re.search(
            r"(\d+\.?\d*)\s*(?:<|<=|is less than|below)\s*(\d+\.?\d*)",
            condensed_log,
        )
        if cov_match:
            current_cov, required_cov = cov_match.groups()
            return f"Coverage Failure: Current {current_cov}% is below required {required_cov}%.\nCheck --cov-fail-under settings."

    if "AssertionError" in condensed_log:
        assertion_match = re.search(r"AssertionError:\s*(.+)", condensed_log)
        if assertion_match:
            return f"Assertion Failed: {assertion_match.group(1)}"

    if "ModuleNotFoundError" in condensed_log or "ImportError" in condensed_log:
        mod_match = re.search(
            r"(ModuleNotFoundError|ImportError):\s*(.+)", condensed_log
        )
        if mod_match:
            return f"Import Error: {mod_match.group(1)} - {mod_match.group(2)}"

    return condensed_log


def log_processing_details(
    log_file_path, original_size, condensed_size, ai_used, job_name, run_number, cost_info=None
):
    with open(log_file_path, "a") as log_f:
        log_f.write("\n--- Job Processing ---\n")
        log_f.write(f"Job: {job_name} (Run #{run_number})\n")
        log_f.write(f"Original Log Size: {original_size} chars\n")
        log_f.write(f"Condensed Log Size: {condensed_size} chars\n")
        log_f.write(
            f"Reduction: {((original_size - condensed_size) / original_size * 100):.1f}%\n"
        )
        log_f.write(f"AI Used: {ai_used}\n")
        if cost_info:
            log_f.write(f"Input Tokens: {cost_info['input_tokens']}\n")
            log_f.write(f"Output Tokens: {cost_info['output_tokens']}\n")
            log_f.write(f"Request Cost: ${cost_info['cost_usd']:.6f}\n")
        log_f.write("--- End Job ---\n")
