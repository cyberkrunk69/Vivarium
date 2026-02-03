"""
Black Swarm API Server

Endpoints:
  POST /grind  - Execute grind tasks with budget params
  POST /plan   - Scan codebase, analyze with Together AI, write tasks to queue
"""

import json
import os
import httpx
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import subprocess
import time
from utils import read_json, write_json

load_dotenv()

app = FastAPI(title="Black Swarm", version="1.0")

WORKSPACE = Path(__file__).parent
QUEUE_FILE = WORKSPACE / "queue.json"
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"


class GrindRequest(BaseModel):
    """
    Request model for the /grind endpoint.

    Attributes:
        task: Command or task description to execute.
        min_budget: Minimum budget in dollars (default: $0.05).
        max_budget: Maximum budget in dollars (default: $0.10).
        intensity: Task intensity level - "low", "medium", or "high".
        timeout: Subprocess timeout in seconds (default: 30).
    """
    task: str
    min_budget: float = 0.05
    max_budget: float = 0.10
    intensity: str = "medium"
    timeout: int = 30


class GrindResponse(BaseModel):
    """
    Response model for the /grind endpoint.

    Attributes:
        status: Execution status ("completed" or "failed").
        result: Human-readable result message or error description.
        output: Subprocess stdout/stderr output (first 1000 chars).
        budget_used: Actual budget consumed (between min and max).
        exit_code: Process exit code (0 for success).
    """
    status: str
    result: str
    output: str
    budget_used: float
    exit_code: int


@app.post("/grind", response_model=GrindResponse)
async def grind(req: GrindRequest):
    """
    Execute a grind task by running a subprocess command.

    Accepts a task description/command, executes it via subprocess,
    and returns results with actual execution metrics.

    Args:
        req: GrindRequest with task command and budget parameters.

    Returns:
        GrindResponse: Execution status, output, budget consumed, and exit code.

    Raises:
        HTTPException: 400 if task is empty, 500 if execution fails.

    Example:
        # curl -X POST http://127.0.0.1:8420/grind \
        #   -H "Content-Type: application/json" \
        #   -d '{"task": "python script.py", "intensity": "high"}'
    """
    if not req.task or not req.task.strip():
        raise HTTPException(status_code=400, detail="task parameter cannot be empty")

    start_time = time.time()
    try:
        process = subprocess.run(
            req.task,
            shell=True,
            capture_output=True,
            text=True,
            timeout=req.timeout,
            cwd=WORKSPACE
        )
        elapsed_time = time.time() - start_time

        # Truncate output to first 1000 chars
        output = (process.stdout + process.stderr)[:1000]

        status = "completed" if process.returncode == 0 else "failed"
        result = f"Task executed in {elapsed_time:.2f}s with exit code {process.returncode}"

        # Calculate budget based on actual execution time and intensity
        intensity_multiplier = {"low": 0.5, "medium": 1.0, "high": 1.5}.get(req.intensity, 1.0)
        time_cost = elapsed_time * 0.01 * intensity_multiplier
        budget_used = max(req.min_budget, min(req.max_budget, time_cost))

        return GrindResponse(
            status=status,
            result=result,
            output=output,
            budget_used=round(budget_used, 4),
            exit_code=process.returncode
        )
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        raise HTTPException(
            status_code=500,
            detail=f"Task execution timeout after {req.timeout}s"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Task execution error: {str(e)}"
        )


@app.post("/plan")
async def plan():
    """
    Scan codebase, analyze with Together AI, write tasks to queue.

    Three-step process:
    1. Scan workspace for .py files and collect metadata
    2. Send scan results to Together AI (Llama 3.3 70B) for analysis
    3. Write suggested improvement tasks to queue.json

    Returns:
        dict: Summary with files_scanned, total_lines, tasks_created.

    Raises:
        HTTPException: 500 if TOGETHER_API_KEY not configured.

    Example:
        # curl -X POST http://127.0.0.1:8420/plan
    """
    if not TOGETHER_API_KEY:
        raise HTTPException(status_code=500, detail="TOGETHER_API_KEY not set")

    # Step 1: Scan codebase
    scan_result = scan_codebase()

    # Step 2: Call Together AI for analysis
    tasks = await analyze_with_together(scan_result)

    # Step 3: Write tasks to queue.json
    write_tasks_to_queue(tasks)

    return {
        "status": "planned",
        "files_scanned": scan_result["total_files"],
        "total_lines": scan_result["total_lines"],
        "tasks_created": len(tasks)
    }


def scan_codebase() -> dict:
    """
    Scan all .py files in the codebase.

    Recursively finds Python files and collects:
    - File paths (relative to workspace)
    - Line counts
    - Test file detection (by filename or content)

    Returns:
        dict: Scan results containing:
            - total_files: Number of .py files found
            - total_lines: Sum of all line counts
            - files: List of file info dicts
            - test_files: List of test file paths
            - has_tests: Boolean indicating test presence

    Example:
        scan = scan_codebase()
        print(f"Found {scan['total_files']} files, {scan['total_lines']} lines")
    """
    workspace = WORKSPACE

    py_files = list(workspace.rglob("*.py"))

    file_info = []
    total_lines = 0
    test_files = []

    for py_file in py_files:
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            lines = len(content.splitlines())
            total_lines += lines

            rel_path = str(py_file.relative_to(workspace))
            file_info.append({
                "path": rel_path,
                "lines": lines,
                "has_tests": "test" in rel_path.lower() or "def test_" in content
            })

            if "test" in rel_path.lower() or "def test_" in content:
                test_files.append(rel_path)
        except Exception:
            continue

    return {
        "total_files": len(py_files),
        "total_lines": total_lines,
        "files": file_info,
        "test_files": test_files,
        "has_tests": len(test_files) > 0
    }


async def analyze_with_together(scan_result: dict) -> list:
    """
    Call Together AI to analyze codebase and suggest improvements.

    Sends scan metadata to Llama 3.3 70B Instruct via Together AI API.
    The model analyzes the codebase structure and suggests 3-5 improvement
    tasks with priorities. Tasks are converted to grind task format.

    Args:
        scan_result: Output from scan_codebase() with file metadata.

    Returns:
        list: Task dicts ready for queue.json, each containing:
            - id, type, description, min_budget, max_budget, intensity

    Raises:
        HTTPException: 500 if Together AI API call fails.

    Example:
        scan = scan_codebase()
        tasks = await analyze_with_together(scan)
        write_tasks_to_queue(tasks)
    """

    files_summary = "\n".join([
        f"- {f['path']}: {f['lines']} lines" + (" (has tests)" if f['has_tests'] else "")
        for f in scan_result["files"]
    ])

    prompt = f"""Analyze this Python codebase and suggest 3-5 improvement tasks.

Codebase scan:
- Total files: {scan_result['total_files']}
- Total lines: {scan_result['total_lines']}
- Has tests: {scan_result['has_tests']}

Files:
{files_summary}

Return a JSON array of tasks. Each task should have:
- id: unique task ID like "task_001"
- description: what to improve
- priority: "high", "medium", or "low"

Return ONLY valid JSON array, no other text."""

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": TOGETHER_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1024,
                "temperature": 0.7
            }
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Together API error: {response.text}")

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Parse the JSON response
        try:
            # Handle markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            suggestions = json.loads(content.strip())
        except json.JSONDecodeError:
            # Fallback tasks if parsing fails
            suggestions = [
                {"id": "task_001", "description": "Add unit tests", "priority": "high"},
                {"id": "task_002", "description": "Add type hints", "priority": "medium"},
                {"id": "task_003", "description": "Add docstrings", "priority": "low"}
            ]

        # Convert to grind task format
        tasks = []
        for i, suggestion in enumerate(suggestions):
            task_id = suggestion.get("id", f"task_{i+1:03d}")
            priority = suggestion.get("priority", "medium")

            # Map priority to intensity and budget
            if priority == "high":
                intensity, min_b, max_b = "high", 0.08, 0.15
            elif priority == "low":
                intensity, min_b, max_b = "low", 0.02, 0.05
            else:
                intensity, min_b, max_b = "medium", 0.05, 0.10

            tasks.append({
                "id": task_id,
                "type": "grind",
                "description": suggestion.get("description", ""),
                "min_budget": min_b,
                "max_budget": max_b,
                "intensity": intensity,
                "status": "pending",
                "depends_on": [],
                "parallel_safe": True
            })

        return tasks


def write_tasks_to_queue(tasks: list):
    """
    Write tasks to queue.json.

    Creates a fresh queue file with the provided tasks. Overwrites any
    existing queue content. Sets default API endpoint and empty
    completed/failed lists.

    Args:
        tasks: List of task dicts to write.

    Example:
        tasks = [{"id": "task_001", "type": "grind", ...}]
        write_tasks_to_queue(tasks)
    """
    queue = {
        "version": "1.0",
        "api_endpoint": "http://127.0.0.1:8420",
        "tasks": tasks,
        "completed": [],
        "failed": []
    }

    write_json(QUEUE_FILE, queue)


@app.get("/status")
async def status():
    """
    Get current queue status.

    Returns counts of tasks in each state: pending, completed, failed.

    Returns:
        dict: Task counts by status.

    Example:
        # curl http://127.0.0.1:8420/status
        # {"tasks": 5, "completed": 2, "failed": 0}
    """
    if QUEUE_FILE.exists():
        queue = read_json(QUEUE_FILE)
        if queue:
            return {
                "tasks": len(queue.get("tasks", [])),
                "completed": len(queue.get("completed", [])),
                "failed": len(queue.get("failed", []))
            }
    return {"tasks": 0, "completed": 0, "failed": 0}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8420)
