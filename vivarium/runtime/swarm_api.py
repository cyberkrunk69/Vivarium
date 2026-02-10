"""
Vivarium API Server (Groq + Local Execution)

Endpoints:
  POST /cycle  - Execute one cycle task (Groq or local command)
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
from ipaddress import ip_address
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from vivarium.runtime.config import (
    DEFAULT_GROQ_MODEL,
    validate_model_id,
    validate_config,
)
from vivarium.runtime.runtime_contract import normalize_queue, normalize_task
from vivarium.runtime.safety_gateway import SafetyGateway
from vivarium.runtime.secure_api_wrapper import SecureAPIWrapper, create_admin_context
from vivarium.utils import read_json, write_json
from vivarium.runtime.vivarium_scope import (
    AUDIT_ROOT,
    MUTABLE_QUEUE_FILE,
    MUTABLE_ROOT,
    SECURITY_ROOT,
    ensure_scope_layout,
    get_execution_token,
)

load_dotenv()
ensure_scope_layout()
os.environ.setdefault("VIVARIUM_API_AUDIT_LOG", str(AUDIT_ROOT / "api_audit.log"))
REPO_ROOT = Path(__file__).resolve().parents[2]

app = FastAPI(title="Vivarium", version="1.0")
WORKSPACE = MUTABLE_ROOT
QUEUE_FILE = MUTABLE_QUEUE_FILE

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "community_library",
    "knowledge",  # legacy path; retained for backward compatibility
    ".checkpoints",
    ".cycle_cache",
}

LOCAL_COMMAND_ALLOWLIST = {
    "ls",
    "pwd",
    "echo",
    "cat",
    "rg",
}
REPO_READ_ROOT = REPO_ROOT.resolve()
PHYSICS_READ_BLOCKLIST = (
    (REPO_ROOT / "vivarium" / "physics").resolve(),
)
SECURITY_READ_BLOCKLIST = (
    (REPO_ROOT / "vivarium" / "meta" / "security").resolve(),
    (REPO_ROOT / "config" / "SAFETY_CONSTRAINTS.json").resolve(),
    (REPO_ROOT / "SECURITY.md").resolve(),
    (REPO_ROOT / "vivarium" / "runtime" / "safety_gateway.py").resolve(),
    (REPO_ROOT / "vivarium" / "runtime" / "safety_validator.py").resolve(),
    (REPO_ROOT / "vivarium" / "runtime" / "secure_api_wrapper.py").resolve(),
    (REPO_ROOT / "vivarium" / "runtime" / "vivarium_scope.py").resolve(),
)
JOURNAL_PRIVACY_READ_BLOCKLIST = (
    (REPO_ROOT / "vivarium" / "world" / "mutable" / ".swarm" / "journals").resolve(),
    (REPO_ROOT / "vivarium" / "world" / "mutable" / ".swarm" / "journal_votes.json").resolve(),
)
READ_BLOCKLIST = PHYSICS_READ_BLOCKLIST + SECURITY_READ_BLOCKLIST + JOURNAL_PRIVACY_READ_BLOCKLIST
RG_BLOCKED_GLOBS = (
    "vivarium/physics/**",
    "vivarium/meta/security/**",
    "config/SAFETY_CONSTRAINTS.json",
    "SECURITY.md",
    "vivarium/runtime/safety_gateway.py",
    "vivarium/runtime/safety_validator.py",
    "vivarium/runtime/secure_api_wrapper.py",
    "vivarium/runtime/vivarium_scope.py",
    "vivarium/world/mutable/.swarm/journals/**",
    "vivarium/world/mutable/.swarm/journal_votes.json",
)

LOCAL_COMMAND_DENYLIST = [
    (re.compile(r"\bcurl\b[^|]*\|\s*(bash|sh)\b", re.IGNORECASE), "piping curl output into shell"),
    (re.compile(r"\bwget\b[^|]*\|\s*(bash|sh)\b", re.IGNORECASE), "piping wget output into shell"),
    (re.compile(r"\b(curl|wget|nc|ncat|socat|telnet|python\s+-m\s+http\.server)\b", re.IGNORECASE), "unauthorized network tool"),
    (re.compile(r"\brm\s+-rf\b", re.IGNORECASE), "destructive recursive delete"),
    (re.compile(r"\bmkfs(\.[a-z0-9]+)?\b", re.IGNORECASE), "disk formatting command"),
    (re.compile(r"\bdd\s+if=", re.IGNORECASE), "raw disk write command"),
    (re.compile(r"\b(shutdown|reboot|poweroff)\b", re.IGNORECASE), "host power control command"),
    (re.compile(r"/etc/(passwd|shadow)", re.IGNORECASE), "system credential file access"),
]
LOCAL_COMMAND_OPERATOR_RE = re.compile(r"(;|&&|\|\||`|\$\(|>|<)")
URL_TOKEN_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://")

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
        constraints_file = SECURITY_ROOT / "SAFETY_CONSTRAINTS.json"
        if not constraints_file.exists():
            constraints_file = REPO_ROOT / "config" / "SAFETY_CONSTRAINTS.json"
        return SafetyGateway(
            WORKSPACE,
            constraints_file=constraints_file,
            audit_log=AUDIT_ROOT / "safety_audit.log",
        )
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
INTERNAL_EXECUTION_TOKEN = get_execution_token()
SWARM_ENFORCE_INTERNAL_TOKEN = (
    os.environ.get("SWARM_ENFORCE_INTERNAL_TOKEN", "1").strip().lower()
    not in {"0", "false", "no"}
)
MVP_DOCS_ONLY_MODE = (
    os.environ.get("VIVARIUM_MVP_DOCS_ONLY", "1").strip().lower()
    not in {"0", "false", "no"}
)
LOOPBACK_HOST_ALIASES = {"localhost", "testclient"}


class CycleRequest(BaseModel):
    """
    Request model for the /cycle endpoint.

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


class CycleResponse(BaseModel):
    """Response model for the /cycle endpoint."""

    status: str
    result: str
    model: str
    task_id: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    output: Optional[str] = None
    budget_used: Optional[float] = None
    exit_code: Optional[int] = None
    safety_report: Optional[Dict[str, Any]] = None


def _is_loopback_host(host: Optional[str]) -> bool:
    value = (host or "").strip().lower()
    if not value:
        return False
    if value in LOOPBACK_HOST_ALIASES:
        return True
    try:
        return ip_address(value).is_loopback
    except ValueError:
        return False


def _request_client_host(request: Request) -> str:
    forwarded = (request.headers.get("x-forwarded-for") or "").strip()
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    client = getattr(request, "client", None)
    if client and getattr(client, "host", None):
        return str(client.host).strip()
    return ""


def _enforce_internal_api_access(
    request: Request,
    provided_token: Optional[str],
    *,
    endpoint: str,
    require_token: bool = True,
) -> None:
    client_host = _request_client_host(request)
    if not _is_loopback_host(client_host):
        raise HTTPException(
            status_code=403,
            detail=f"{endpoint} is localhost-only",
        )

    if not require_token or not SWARM_ENFORCE_INTERNAL_TOKEN:
        return

    if not INTERNAL_EXECUTION_TOKEN or provided_token != INTERNAL_EXECUTION_TOKEN:
        raise HTTPException(
            status_code=403,
            detail=f"{endpoint} requires internal execution token",
        )


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


def _tokenize_local_command(command: str) -> Optional[List[str]]:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return None
    while tokens and ENV_ASSIGNMENT_RE.match(tokens[0]):
        tokens.pop(0)
    return tokens


def _is_within(path: Path, root: Path) -> bool:
    try:
        return path == root or root in path.parents
    except Exception:
        return False


def _blocked_read_reason(path: Path) -> Optional[str]:
    for blocked_root in PHYSICS_READ_BLOCKLIST:
        if _is_within(path, blocked_root):
            return "Local command blocked: physics files are restricted in MVP mode"
    for blocked_root in JOURNAL_PRIVACY_READ_BLOCKLIST:
        if _is_within(path, blocked_root):
            return (
                "Local command blocked: journal files are private "
                "(blind review excerpts are exposed only via journal voting APIs)"
            )
    for blocked_root in SECURITY_READ_BLOCKLIST:
        if _is_within(path, blocked_root):
            return "Local command blocked: security files are restricted in MVP mode"
    return None


def _is_path_token(token: str) -> bool:
    if token in {".", ".."}:
        return True
    if token.startswith(("/", "./", "../", "~")):
        return True
    if "/" in token:
        return True
    lowered = token.lower()
    pathlike_suffixes = (
        ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml",
        ".ini", ".cfg", ".log", ".sh", ".rst", ".csv",
    )
    return lowered.endswith(pathlike_suffixes)


def _resolve_repo_read_path(token: str) -> Optional[Path]:
    value = str(token or "").strip()
    if not value:
        return None
    if URL_TOKEN_RE.match(value):
        return None
    if value.startswith("~"):
        return None
    candidate = Path(value)
    if not candidate.is_absolute() and not _is_path_token(value):
        return None
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (REPO_READ_ROOT / candidate).resolve()
    return resolved


def _validate_read_only_token_scope(tokens: List[str]) -> Optional[str]:
    primary = Path(tokens[0]).name
    if primary == "git":
        return "Local command blocked: git access is disabled in MVP mode"

    if primary == "rg":
        disallowed_rg_flags = {"-g", "--glob", "--iglob", "--no-ignore", "--hidden"}
        for token in tokens[1:]:
            if token in disallowed_rg_flags or token.startswith("--glob=") or token.startswith("--iglob="):
                return "Local command blocked: custom rg glob/ignore flags are disabled in MVP mode"

    non_flags = [token for token in tokens[1:] if not token.startswith("-")]
    candidate_tokens: List[str] = []
    if primary in {"ls", "cat"}:
        candidate_tokens = non_flags
    elif primary == "rg":
        for token in non_flags:
            if _is_path_token(token):
                candidate_tokens.append(token)

    for token in candidate_tokens:
        resolved = _resolve_repo_read_path(token)
        if resolved is None:
            continue
        if not _is_within(resolved, REPO_READ_ROOT):
            return "Local command blocked: path outside repository root"
        blocked_reason = _blocked_read_reason(resolved)
        if blocked_reason:
            return blocked_reason
    return None


def _apply_rg_blocklist_globs(tokens: List[str]) -> List[str]:
    primary = Path(tokens[0]).name if tokens else ""
    if primary != "rg":
        return tokens
    patched = list(tokens)
    for pattern in RG_BLOCKED_GLOBS:
        patched.extend(["--glob", f"!{pattern}"])
    return patched


def _validate_local_command(command: str) -> Optional[str]:
    if LOCAL_COMMAND_OPERATOR_RE.search(command):
        return "Local command blocked: shell operators are not permitted"

    for pattern, reason in LOCAL_COMMAND_DENYLIST:
        if pattern.search(command):
            return f"Local command blocked: {reason}"

    tokens = _tokenize_local_command(command)
    if tokens is None:
        return "Local command blocked: unable to parse executable"
    if not tokens:
        return "Local command blocked: unable to parse executable"

    primary = Path(tokens[0]).name
    if not primary:
        return "Local command blocked: unable to parse executable"
    if primary not in LOCAL_COMMAND_ALLOWLIST:
        return f"Local command blocked: '{primary}' is not in allowlist"
    return _validate_read_only_token_scope(tokens)


def _build_local_env(tokens: List[str]) -> Dict[str, str]:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
        "HOME": str(REPO_ROOT),
        "GIT_TERMINAL_PROMPT": "0",
    }
    while tokens and ENV_ASSIGNMENT_RE.match(tokens[0]):
        key, _value = tokens.pop(0).split("=", 1)
        raise HTTPException(
            status_code=403,
            detail=f"Local command blocked: env assignment '{key}' is not allowed",
        )
    return env


def _enforce_local_token_scope(tokens: List[str]) -> None:
    if not tokens:
        raise HTTPException(status_code=400, detail="local mode requires an executable command")
    token_error = _validate_read_only_token_scope(tokens)
    if token_error:
        raise HTTPException(status_code=403, detail=token_error)

    return None


@app.post("/cycle", response_model=CycleResponse)
async def cycle(
    req: CycleRequest,
    request: Request,
    x_vivarium_internal_token: Optional[str] = Header(
        default=None,
        alias="X-Vivarium-Internal-Token",
    ),
) -> CycleResponse:
    """
    Execute a task by calling Groq's OpenAI-compatible chat completions API,
    or by running a local command when mode is "local".
    """
    _enforce_internal_api_access(
        request,
        x_vivarium_internal_token,
        endpoint="/cycle",
    )

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
    req: CycleRequest,
    safety_report: Optional[Dict[str, Any]] = None,
) -> CycleResponse:
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

    return CycleResponse(
        status="completed",
        result=result_text,
        model=result.get("model", model),
        task_id=req.task_id,
        usage=usage,
        budget_used=round(budget_used, 6) if isinstance(budget_used, (int, float)) else None,
        safety_report=safety_report,
    )


def _run_local_task(
    req: CycleRequest,
    safety_report: Optional[Dict[str, Any]] = None,
) -> CycleResponse:
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

    env = _build_local_env(tokens)

    _enforce_local_token_scope(tokens)
    tokens = _apply_rg_blocklist_globs(tokens)

    start_time = time.time()
    try:
        process = subprocess.run(
            tokens,
            shell=False,
            capture_output=True,
            text=True,
            timeout=req.timeout,
            cwd=REPO_ROOT,
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

    return CycleResponse(
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
async def plan(
    request: Request,
    x_vivarium_internal_token: Optional[str] = Header(
        default=None,
        alias="X-Vivarium-Internal-Token",
    ),
) -> Dict[str, Any]:
    """
    Scan codebase, analyze with Groq, and write tasks to queue.json.
    """
    _enforce_internal_api_access(
        request,
        x_vivarium_internal_token,
        endpoint="/plan",
    )

    if MVP_DOCS_ONLY_MODE:
        raise HTTPException(
            status_code=410,
            detail="Planning endpoint disabled in MVP docs-only mode. Add tasks manually to queue.json.",
        )

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

    for root, dirs, files in os.walk(REPO_ROOT):
        root_path = Path(root).resolve()
        if _blocked_read_reason(root_path):
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for filename in files:
            if not filename.endswith(".py"):
                continue
            path = Path(root) / filename
            if _blocked_read_reason(path.resolve()):
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lines = len(content.splitlines())
            total_lines += lines

            rel_path = str(path.relative_to(REPO_ROOT))
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
            "type": "cycle",
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
async def status(request: Request) -> Dict[str, int]:
    """Get current queue status."""
    _enforce_internal_api_access(
        request,
        provided_token=None,
        endpoint="/status",
        require_token=False,
    )

    if QUEUE_FILE.exists():
        queue = normalize_queue(read_json(QUEUE_FILE, default={}))
        if queue:
            return {
                "tasks": len(queue.get("tasks", [])),
                "completed": len(queue.get("completed", [])),
                "failed": len(queue.get("failed", [])),
            }
    return {"tasks": 0, "completed": 0, "failed": 0}
