"""
estimate_requests.py
--------------------
Escalating budget-estimate requests with time-sensitive bounty growth.
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils import read_json, write_json, append_jsonl, get_timestamp


WORKSPACE = Path(__file__).parent
ESTIMATE_DIR = WORKSPACE / ".swarm" / "estimates"
STATE_FILE = ESTIMATE_DIR / "requests.json"
LOG_FILE = ESTIMATE_DIR / "estimate_log.jsonl"
LOCK_FILE = ESTIMATE_DIR / "estimate.lock"

LOCK_RETRIES = 25
LOCK_SLEEP_SECONDS = 0.05

BASE_BOUNTY = 6
ESCALATION_RATE = 2.0  # tokens per hour
MAX_BOUNTY = 60
URGENT_BONUS = 6


@contextmanager
def _estimate_lock():
    acquired = False
    fd = None
    ESTIMATE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for _ in range(LOCK_RETRIES):
            try:
                fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                acquired = True
                break
            except FileExistsError:
                time.sleep(LOCK_SLEEP_SECONDS)
        yield
    finally:
        if acquired:
            try:
                if fd is not None:
                    os.close(fd)
                if LOCK_FILE.exists():
                    LOCK_FILE.unlink()
            except Exception:
                pass


def _load_state() -> Dict[str, Any]:
    return read_json(STATE_FILE, default={"requests": {}, "updated_at": get_timestamp()})


def _save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = get_timestamp()
    write_json(STATE_FILE, state)


def _current_bounty(request: Dict[str, Any]) -> int:
    created_at_ts = request.get("created_at_ts", time.time())
    age_hours = max(0.0, (time.time() - created_at_ts) / 3600.0)
    rate = float(request.get("escalation_rate", ESCALATION_RATE))
    base = int(request.get("base_bounty", BASE_BOUNTY))
    urgent = URGENT_BONUS if request.get("time_sensitive") else 0
    bounty = base + int(age_hours * rate) + urgent
    cap = int(request.get("max_bounty", MAX_BOUNTY))
    return min(bounty, cap)


def _complexity_tuning(
    complexity_score: Optional[float],
    complexity_band: Optional[str],
) -> Dict[str, float]:
    band = (complexity_band or "").lower().strip()
    score = complexity_score if complexity_score is not None else 0.0

    if not band:
        if score >= 0.8:
            band = "critical"
        elif score >= 0.6:
            band = "high"
        elif score >= 0.3:
            band = "medium"
        else:
            band = "low"

    if band == "critical":
        return {"base_bounty": 10, "escalation_rate": 4.0, "max_bounty": 120}
    if band == "high":
        return {"base_bounty": 8, "escalation_rate": 3.0, "max_bounty": 90}
    if band == "medium":
        return {"base_bounty": 6, "escalation_rate": 2.2, "max_bounty": 70}
    return {"base_bounty": 4, "escalation_rate": 1.6, "max_bounty": 50}


def register_request(
    *,
    task_id: str,
    summary: str,
    time_sensitive: bool = False,
    escalation_rate: Optional[float] = None,
    complexity_score: Optional[float] = None,
    complexity_band: Optional[str] = None,
    suggested_model_tier: Optional[str] = None,
    suggested_budget: Optional[float] = None,
) -> Dict[str, Any]:
    """Create or update an estimate request."""
    with _estimate_lock():
        state = _load_state()
        requests = state.get("requests", {})
        if task_id in requests:
            req = requests[task_id]
        else:
            tuning = _complexity_tuning(complexity_score, complexity_band)
            base_bounty = tuning["base_bounty"]
            max_bounty = tuning["max_bounty"]
            rate = tuning["escalation_rate"]
            req = {
                "task_id": task_id,
                "summary": summary[:400],
                "created_at": get_timestamp(),
                "created_at_ts": time.time(),
                "time_sensitive": bool(time_sensitive),
                "base_bounty": base_bounty,
                "escalation_rate": escalation_rate if escalation_rate is not None else rate,
                "max_bounty": max_bounty,
                "status": "open",
                "complexity_score": complexity_score,
                "complexity_band": complexity_band,
                "suggested_model_tier": suggested_model_tier,
                "suggested_budget": suggested_budget,
            }
            requests[task_id] = req

        state["requests"] = requests
        _save_state(state)

    req["current_bounty"] = _current_bounty(req)
    return req


def list_requests(limit: int = 10) -> List[Dict[str, Any]]:
    state = _load_state()
    requests = list(state.get("requests", {}).values())
    open_requests = [r for r in requests if r.get("status") == "open"]
    for req in open_requests:
        req["current_bounty"] = _current_bounty(req)

    open_requests.sort(key=lambda r: r.get("current_bounty", 0), reverse=True)
    return open_requests[:limit]


def resolve_request(task_id: str, reason: str = "estimated") -> None:
    """Mark an estimate request as resolved without a payout."""
    with _estimate_lock():
        state = _load_state()
        req = state.get("requests", {}).get(task_id)
        if not req:
            return
        if req.get("status") == "resolved":
            return
        req["status"] = "resolved"
        req["resolved_by"] = reason
        req["resolved_at"] = get_timestamp()
        state["requests"][task_id] = req
        _save_state(state)


def claim_request(task_id: str, estimator_id: str, estimator_name: str) -> Dict[str, Any]:
    with _estimate_lock():
        state = _load_state()
        req = state.get("requests", {}).get(task_id)
        if not req:
            return {"success": False, "error": "request_not_found"}
        if req.get("status") != "open":
            return {"success": False, "error": "request_not_open"}

        req["status"] = "claimed"
        req["claimed_by"] = estimator_id
        req["claimed_name"] = estimator_name
        req["claimed_at"] = get_timestamp()
        state["requests"][task_id] = req
        _save_state(state)

    req["current_bounty"] = _current_bounty(req)
    return {"success": True, "request": req}


def submit_estimate(
    *,
    task_id: str,
    estimator_id: str,
    estimator_name: str,
    estimate_budget: float,
    justification: str,
    collaborators: Optional[List[str]] = None,
    model_tier: Optional[str] = None,
) -> Dict[str, Any]:
    with _estimate_lock():
        state = _load_state()
        req = state.get("requests", {}).get(task_id)
        if not req:
            return {"success": False, "error": "request_not_found"}
        if req.get("status") == "resolved":
            return {"success": False, "error": "request_already_resolved"}

        req["status"] = "resolved"
        req["resolved_by"] = estimator_id
        req["resolved_name"] = estimator_name
        req["resolved_at"] = get_timestamp()
        state["requests"][task_id] = req
        _save_state(state)

    bounty = _current_bounty(req)
    reward = bounty
    try:
        from swarm_enrichment import get_enrichment
        enrichment = get_enrichment(WORKSPACE)
        enrichment.grant_free_time(estimator_id, reward, reason="estimate_request")
    except Exception:
        pass

    append_jsonl(
        LOG_FILE,
        {
            "task_id": task_id,
            "estimator_id": estimator_id,
            "estimator_name": estimator_name,
            "estimate_budget": estimate_budget,
            "justification": justification[:2000],
            "collaborators": collaborators or [],
            "model_tier": model_tier,
            "reward_tokens": reward,
            "timestamp": get_timestamp(),
        },
    )

    _write_task_estimate(task_id, estimate_budget, estimator_id, justification, model_tier)
    return {"success": True, "reward_tokens": reward}


def _write_task_estimate(
    task_id: str,
    estimate_budget: float,
    estimator_id: str,
    justification: str,
    model_tier: Optional[str],
) -> None:
    queue_path = WORKSPACE / "queue.json"
    if not queue_path.exists():
        return
    try:
        queue = read_json(queue_path)
    except Exception:
        return

    tasks = queue.get("tasks", [])
    updated = False
    for task in tasks:
        if task.get("id") == task_id:
            task["estimated_budget"] = estimate_budget
            task["estimated_by"] = estimator_id
            task["estimate_justification"] = justification[:300]
            if model_tier:
                task["estimate_model_tier"] = model_tier
            updated = True
            break

    if updated:
        write_json(queue_path, queue)


def get_estimate_alerts(limit: int = 3) -> List[Dict[str, Any]]:
    alerts = list_requests(limit=limit)
    results = []
    for req in alerts:
        results.append(
            {
                "task_id": req.get("task_id"),
                "summary": req.get("summary"),
                "current_bounty": req.get("current_bounty", 0),
                "time_sensitive": req.get("time_sensitive", False),
                "complexity_score": req.get("complexity_score"),
                "complexity_band": req.get("complexity_band"),
                "suggested_model_tier": req.get("suggested_model_tier"),
                "suggested_budget": req.get("suggested_budget"),
            }
        )
    return results


__all__ = [
    "register_request",
    "list_requests",
    "claim_request",
    "submit_estimate",
    "get_estimate_alerts",
    "resolve_request",
]
