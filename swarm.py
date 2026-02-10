"""
Vivarium API Server (Groq + Local Execution)

Endpoints:
  POST /grind  - Execute a task (Groq or local command)
  POST /plan   - Scan codebase and write tasks to queue.json
  GET  /status - Queue summary
"""

from typing import Optional, Any, Dict, List

import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from config import (
    DEFAULT_GROQ_MODEL,
    validate_model_id,
    validate_config,
)
from runtime_contract import normalize_queue, normalize_task
from safety_gateway import SafetyGateway
from secure_api_wrapper import SecureAPIWrapper, create_admin_context
from utils import read_json, write_json

load_dotenv()

app = FastAPI(title="Vivarium", version="1.0")
WORKSPACE = Path(__file__).parent
QUEUE_FILE = WORKSPACE / "queue.json"

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "knowledge",
    ".checkpoints",
    ".grind_cache",
}

LOCAL_COMMAND_ALLOWLIST = {
    "python",
    "python3",
    "pytest",
    "pip",
    "pip3",
    "uv",
    "ruff",
    "mypy",
    "git",
    "ls",
    "pwd",
    "echo",
    "cat",
    "sed",
    "awk",
    "rg",
    "cp",
    "mv",
    "mkdir",
    "touch",
    "chmod",
    "node",
    "npm",
    "pnpm",
    "yarn",
    "make",
    "go",
    "cargo",
}

LOCAL_COMMAND_DENYLIST = [
    (re.compile(r"\bcurl\b[^|]*\|\s*(bash|sh)\b", re.IGNORECASE), "piping curl output into shell"),
    (re.compile(r"\bwget\b[^|]*\|\s*(bash|sh)\b", re.IGNORECASE), "piping wget output into shell"),
    (re.compile(r"\brm\s+-rf\b", re.IGNORECASE), "destructive recursive delete"),
    (re.compile(r"\bmkfs(\.[a-z0-9]+)?\b", re.IGNORECASE), "disk formatting command"),
    (re.compile(r"\bdd\s+if=", re.IGNORECASE), "raw disk write command"),
    (re.compile(r"\b(shutdown|reboot|poweroff)\b", re.IGNORECASE), "host power control command"),
    (re.compile(r"/etc/(passwd|shadow)", re.IGNORECASE), "system credential file access"),
]

ENV_ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$")


def _safe_float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _safe_int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _build_safety_gateway() -> Optional[SafetyGateway]:
    try:
        return SafetyGateway(WORKSPACE)
    except Exception:
        return None


def _build_secure_wrapper() -> SecureAPIWrapper:
    return SecureAPIWrapper(
        context=create_admin_context(user_id="swarm_api"),
        budget_limit=_safe_float_env("SWARM_BUDGET_LIMIT", 5.0),
        rate_limit=_safe_int_env("SWARM_RATE_LIMIT", 60),
    )


SWARM_SAFETY_GATEWAY = _build_safety_gateway()
SECURE_API_WRAPPER = _build_secure_wrapper()


class GrindRequest(BaseModel):
    """
    Request model for the /grind endpoint.

    Attributes:
        prompt: Task prompt to send to the Groq API.
        task: Local command to execute (argv parsed, no shell).
        mode: "llm" or "local". If omitted, inferred from provided fields.
        model: Optional Groq model id (must be in whitelist).
        max_tokens: Maximum completion tokens.
        temperature: Sampling temperature.
        timeout: Local command timeout (seconds).
        min_budget/max_budget/intensity: Optional metadata for logging.
        task_id: Optional task identifier (echoed in response).
    """

    prompt: Optional[str] = None
    task: Optional[str] = None
    mode: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = Field(default=2048, ge=1, le=65536)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    timeout: int = Field(default=30, ge=1, le=3600)
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    intensity: Optional[str] = None
    task_id: Optional[str] = None


class GrindResponse(BaseModel):
    """Response model for the /grind endpoint."""

    status: str
    result: str
    model: str
    task_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    output: Optional[str] = None
    budget_used: Optional[float] = None
    exit_code: Optional[int] = None
    safety_report: Optional[Dict[str, Any]] = None


def _pre_execute_safety_report(task_text: str, task_id: Optional[str]) -> Dict[str, Any]:
    if not task_text.strip():
        return {
            "passed": False,
            "blocked_reason": "Task text is empty",
            "checks": {},
            "task_id": task_id,
        }
    if SWARM_SAFETY_GATEWAY is None:
        return {
            "passed": False,
            "blocked_reason": "Safety gateway unavailable",
            "checks": {},
            "task_id": task_id,
        }
    passed, report = SWARM_SAFETY_GATEWAY.pre_execute_safety_check(task_text)
    report["task_id"] = task_id
    report["passed"] = passed
    return report


def _extract_primary_command(command: str) -> Optional[str]:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return None

    while tokens and ENV_ASSIGNMENT_RE.match(tokens[0]):
        tokens.pop(0)

    if not tokens:
        return None
    return Path(tokens[0]).name


def _validate_local_command(command: str) -> Optional[str]:
    for pattern, reason in LOCAL_COMMAND_DENYLIST:
        if pattern.search(command):
            return f"Local command blocked: {reason}"

    primary = _extract_primary_command(command)
    if not primary:
        return "Local command blocked: unable to parse executable"
    if primary not in LOCAL_COMMAND_ALLOWLIST:
        return f"Local command blocked: '{primary}' is not in allowlist"
    return None


@app.post("/grind", response_model=GrindResponse)
async def grind(req: GrindRequest) -> GrindResponse:
    """
    Execute a task by calling Groq's OpenAI-compatible chat completions API,
    or by running a local command when mode is "local".
    """
    if not req.prompt and not req.task:
        raise HTTPException(status_code=400, detail="prompt or task must be provided")

    mode = (req.mode or "").lower().strip()
    if mode and mode not in {"llm", "local"}:
        raise HTTPException(status_code=400, detail="mode must be 'llm' or 'local'")

    safety_target = (req.task or req.prompt or "").strip()
    safety_report = _pre_execute_safety_report(safety_target, req.task_id)
    if not safety_report.get("passed"):
        blocked_reason = safety_report.get("blocked_reason", "blocked by safety gateway")
        raise HTTPException(status_code=403, detail=f"Safety check failed: {blocked_reason}")

    if mode == "local" or (not mode and req.task and not req.prompt):
        return _run_local_task(req, safety_report=safety_report)

    return await _run_groq_task(req, safety_report=safety_report)


async def _run_groq_task(
    req: GrindRequest,
    safety_report: Optional[Dict[str, Any]] = None,
) -> GrindResponse:
    if not req.prompt:
        raise HTTPException(status_code=400, detail="llm mode requires prompt")
    validate_config(require_groq_key=True)

    model = req.model or DEFAULT_GROQ_MODEL
    validate_model_id(model)

    estimated_cost = SECURE_API_WRAPPER._estimate_cost(req.prompt, model)
    if req.max_budget is not None and estimated_cost > req.max_budget:
        SECURE_API_WRAPPER.auditor.log({
            "event": "TASK_BUDGET_EXCEEDED",
            "task_id": req.task_id,
            "model": model,
            "estimated_cost": estimated_cost,
            "task_max_budget": req.max_budget,
        })
        raise HTTPException(
            status_code=403,
            detail=(
                f"Estimated cost ${estimated_cost:.6f} exceeds task max budget "
                f"${req.max_budget:.6f}"
            ),
        )

    try:
        result = SECURE_API_WRAPPER.call_llm(
            prompt=req.prompt,
            model=model,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            timeout=60,
        )
    except PermissionError as exc:
        detail = str(exc)
        status_code = 429 if "Rate limit" in detail else 403
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Secure Groq execution failed: {exc}") from exc

    if result.get("error"):
        raise HTTPException(status_code=500, detail=f"Groq API error: {result['error']}")

    result_text = result.get("result", "")
    usage = {
        "prompt_tokens": result.get("input_tokens", 0),
        "completion_tokens": result.get("output_tokens", 0),
    }
    budget_used = result.get("cost")

    return GrindResponse(
        status="completed",
        result=result_text,
        model=result.get("model", model),
        task_id=req.task_id,
        usage=usage,
        budget_used=round(budget_used, 6) if isinstance(budget_used, (int, float)) else None,
        safety_report=safety_report,
    )


def _run_local_task(
    req: GrindRequest,
    safety_report: Optional[Dict[str, Any]] = None,
) -> GrindResponse:
    task = (req.task or "").strip()
    if not task:
        raise HTTPException(status_code=400, detail="local mode requires task")
    policy_error = _validate_local_command(task)
    if policy_error:
        raise HTTPException(status_code=403, detail=policy_error)

    try:
        tokens = shlex.split(task, posix=True)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Unable to parse local command: {exc}") from exc

    env = os.environ.copy()
    while tokens and ENV_ASSIGNMENT_RE.match(tokens[0]):
        key, value = tokens.pop(0).split("=", 1)
        env[key] = value

    if not tokens:
        raise HTTPException(status_code=400, detail="local mode requires an executable command")

    start_time = time.time()
    try:
        process = subprocess.run(
            tokens,
            shell=False,
            capture_output=True,
            text=True,
            timeout=req.timeout,
            cwd=WORKSPACE,
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail=f"Task timeout after {req.timeout}s")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task execution error: {e}")

    elapsed_time = time.time() - start_time
    output = (process.stdout + process.stderr)[:1000]
    status = "completed" if process.returncode == 0 else "failed"
    result = f"Task executed in {elapsed_time:.2f}s with exit code {process.returncode}"

    intensity = req.intensity or "medium"
    intensity_multiplier = {"low": 0.5, "medium": 1.0, "high": 1.5}.get(intensity, 1.0)
    time_cost = elapsed_time * 0.01 * intensity_multiplier
    budget_used = None
    if req.min_budget is not None and req.max_budget is not None:
        budget_used = max(req.min_budget, min(req.max_budget, time_cost))

    return GrindResponse(
        status=status,
        result=result,
        output=output,
        model="local",
        task_id=req.task_id,
        budget_used=round(budget_used, 4) if budget_used is not None else None,
        exit_code=process.returncode,
        safety_report=safety_report,
    )


@app.post("/plan")
async def plan() -> Dict[str, Any]:
    """
    Scan codebase, analyze with Groq, and write tasks to queue.json.
    """
    validate_config(require_groq_key=True)

    scan_result = scan_codebase()
    tasks = await analyze_with_groq(scan_result)
    write_tasks_to_queue(tasks)

    return {
        "status": "planned",
        "files_scanned": scan_result["total_files"],
        "total_lines": scan_result["total_lines"],
        "tasks_created": len(tasks),
    }


def scan_codebase() -> Dict[str, Any]:
    """Scan all .py files in the codebase (skipping large vendor dirs)."""
    file_info: List[Dict[str, Any]] = []
    total_lines = 0
    test_files: List[str] = []

    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for filename in files:
            if not filename.endswith(".py"):
                continue
            path = Path(root) / filename
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lines = len(content.splitlines())
            total_lines += lines

            rel_path = str(path.relative_to(WORKSPACE))
            has_tests = "test" in rel_path.lower() or "def test_" in content

            file_info.append({
                "path": rel_path,
                "lines": lines,
                "has_tests": has_tests,
            })

            if has_tests:
                test_files.append(rel_path)

    return {
        "total_files": len(file_info),
        "total_lines": total_lines,
        "files": file_info,
        "test_files": test_files,
        "has_tests": len(test_files) > 0,
    }


def _summarize_scan(scan_result: Dict[str, Any], max_files: int = 120) -> str:
    files = scan_result.get("files", [])
    summary_lines = []
    for idx, info in enumerate(files):
        if idx >= max_files:
            break
        line = f"- {info['path']}: {info['lines']} lines"
        if info.get("has_tests"):
            line += " (has tests)"
        summary_lines.append(line)

    truncated = len(files) > max_files
    if truncated:
        summary_lines.append(f"... and {len(files) - max_files} more files (truncated)")

    return "\n".join(summary_lines)


async def analyze_with_groq(scan_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Call Groq to analyze codebase and suggest improvements.
    """
    summary = _summarize_scan(scan_result)
    prompt = f"""Analyze this Python codebase and suggest 3-5 improvement tasks.

Codebase scan:
- Total files: {scan_result['total_files']}
- Total lines: {scan_result['total_lines']}
- Has tests: {scan_result['has_tests']}

Files:
{summary}

Return a JSON array of tasks. Each task should have:
- id: unique task ID like "task_001"
- description: what to improve
- priority: "high", "medium", or "low"

Return ONLY valid JSON array, no other text."""

    try:
        result = SECURE_API_WRAPPER.call_llm(
            prompt=prompt,
            model=DEFAULT_GROQ_MODEL,
            max_tokens=1024,
            temperature=0.4,
            timeout=60,
        )
    except PermissionError as exc:
        detail = str(exc)
        status_code = 429 if "Rate limit" in detail else 403
        raise HTTPException(status_code=status_code, detail=detail) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Secure Groq planning failed: {exc}") from exc

    content = result.get("result", "")

    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        suggestions = json.loads(content.strip())
    except json.JSONDecodeError:
        suggestions = [
            {"id": "task_001", "description": "Add unit tests", "priority": "high"},
            {"id": "task_002", "description": "Add type hints", "priority": "medium"},
            {"id": "task_003", "description": "Add docstrings", "priority": "low"},
        ]

    tasks: List[Dict[str, Any]] = []
    for i, suggestion in enumerate(suggestions):
        task_id = suggestion.get("id", f"task_{i+1:03d}")
        priority = suggestion.get("priority", "medium")
        description = suggestion.get("description", "").strip() or "Review codebase improvements"

        if priority == "high":
            intensity, min_b, max_b = "high", 0.08, 0.15
        elif priority == "low":
            intensity, min_b, max_b = "low", 0.02, 0.05
        else:
            intensity, min_b, max_b = "medium", 0.05, 0.10

        tasks.append({
            "id": task_id,
            "type": "grind",
            "prompt": description,
            "min_budget": min_b,
            "max_budget": max_b,
            "intensity": intensity,
            "status": "pending",
            "depends_on": [],
            "parallel_safe": True,
        })

    return tasks


def write_tasks_to_queue(tasks: List[Dict[str, Any]]) -> None:
    """Write tasks to queue.json."""
    queue = normalize_queue({
        "tasks": [normalize_task(task) for task in tasks],
        "completed": [],
        "failed": [],
    })
    write_json(QUEUE_FILE, queue)


@app.get("/status")
async def status() -> Dict[str, int]:
    """Get current queue status."""
    if QUEUE_FILE.exists():
        queue = normalize_queue(read_json(QUEUE_FILE, default={}))
        if queue:
            return {
                "tasks": len(queue.get("tasks", [])),
                "completed": len(queue.get("completed", [])),
                "failed": len(queue.get("failed", [])),
            }
    return {"tasks": 0, "completed": 0, "failed": 0}
