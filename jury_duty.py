"""
jury_duty.py
------------
Blind jury voting system for task outcomes.

Features:
- Pass/fail voting with logically-justified votes.
- Voter rewards (visible only to voters).
- No vote counts surfaced publicly.
- Impact-based voter count scaling.
- Author feedback with compressed, constructive rationale.
"""

from __future__ import annotations

import os
import random
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Any, List, Optional

from utils import read_json, write_json, read_jsonl, append_jsonl, get_timestamp
from path_balance import record_path, get_path_multiplier


WORKSPACE = Path(__file__).parent
JURY_DIR = WORKSPACE / ".swarm" / "jury"
SUBMISSIONS_FILE = JURY_DIR / "submissions.jsonl"
VOTES_FILE = JURY_DIR / "votes.jsonl"
RESULTS_FILE = JURY_DIR / "results.jsonl"
ASSIGNMENTS_FILE = JURY_DIR / "assignments.json"
DECISIONS_FILE = JURY_DIR / "decisions.json"
REWARDS_FILE = JURY_DIR / "voter_rewards.jsonl"
FEEDBACK_FILE = JURY_DIR / "author_feedback.jsonl"
POOL_FILE = JURY_DIR / "jury_pool.json"
LOCK_FILE = JURY_DIR / "jury.lock"

LOCK_RETRIES = 25
LOCK_SLEEP_SECONDS = 0.05

PASS_THRESHOLD = 0.60
VOTER_REWARD_TOKENS = 6
LOGIC_BONUS_TOKENS = 4
VOTER_DAILY_LIMIT = 12


@contextmanager
def _jury_lock():
    acquired = False
    fd = None
    JURY_DIR.mkdir(parents=True, exist_ok=True)
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


def _load_assignments() -> Dict[str, List[str]]:
    return read_json(ASSIGNMENTS_FILE, default={})


def _save_assignments(assignments: Dict[str, List[str]]) -> None:
    write_json(ASSIGNMENTS_FILE, assignments)


def _load_decisions() -> Dict[str, Any]:
    return read_json(DECISIONS_FILE, default={})


def _save_decisions(decisions: Dict[str, Any]) -> None:
    write_json(DECISIONS_FILE, decisions)


def _load_submissions() -> List[Dict[str, Any]]:
    try:
        return read_jsonl(SUBMISSIONS_FILE, default=[])
    except Exception:
        return []


def _load_votes() -> List[Dict[str, Any]]:
    try:
        return read_jsonl(VOTES_FILE, default=[])
    except Exception:
        return []


def _load_voter_pool() -> List[str]:
    if POOL_FILE.exists():
        try:
            data = read_json(POOL_FILE, default=[])
            if isinstance(data, list):
                return [str(v) for v in data]
        except Exception:
            pass
    # Fallback: derive from identities
    identities_dir = WORKSPACE / ".swarm" / "identities"
    if identities_dir.exists():
        return [p.stem for p in identities_dir.glob("*.json")]
    return []


def estimate_impact(
    estimated_budget: Optional[float],
    task_type: str,
    files_touched: Optional[List[str]] = None,
    complexity_score: Optional[float] = None,
) -> float:
    """Heuristic impact estimate in [0, 1]."""
    impact = 0.2
    if estimated_budget:
        impact += min(estimated_budget / 0.2, 1.0) * 0.5
    if task_type in {"safety", "security", "core"}:
        impact += 0.2
    if files_touched:
        impact += min(len(files_touched) / 10.0, 0.2)
    if complexity_score is not None:
        impact += min(max(complexity_score, 0.0), 1.0) * 0.3
    return min(1.0, impact)


def required_voters(impact_score: float) -> int:
    if impact_score <= 0.3:
        return 3
    if impact_score <= 0.6:
        return 5
    if impact_score <= 0.8:
        return 7
    return 9


def _impact_label(score: float) -> str:
    if score <= 0.3:
        return "low"
    if score <= 0.6:
        return "medium"
    if score <= 0.8:
        return "high"
    return "critical"


def _validate_justification(text: str) -> bool:
    if not text or len(text.split()) < 30:
        return False
    sentence_count = sum(text.count(x) for x in [".", "?", "!"])
    if sentence_count < 2:
        return False
    lowered = text.lower()
    rationale_markers = ["because", "since", "therefore", "however", "risk", "impact", "quality", "evidence", "tradeoff"]
    return any(marker in lowered for marker in rationale_markers)


def _strong_justification(text: str) -> bool:
    return len(text.split()) >= 60 and text.count(".") >= 3


def _vote_weight(voter_id: str, author_id: str) -> float:
    """Reduce weight for repeated pairings to discourage collusion."""
    votes = _load_votes()
    recent = [v for v in votes[-200:] if v.get("voter_id") == voter_id]
    pair_count = sum(1 for v in recent if v.get("author_id") == author_id)
    if pair_count >= 6:
        return 0.2
    if pair_count >= 3:
        return 0.5
    return 1.0


def _voter_daily_count(voter_id: str) -> int:
    votes = _load_votes()
    cutoff = time.time() - 24 * 60 * 60
    count = 0
    for v in votes[-300:]:
        if v.get("voter_id") != voter_id:
            continue
        ts = v.get("timestamp_ts")
        if ts and ts >= cutoff:
            count += 1
    return count


def submit_change(
    *,
    task_id: str,
    author_id: str,
    author_name: str,
    summary: str,
    task_type: str,
    origin: str,
    estimated_budget: Optional[float],
    actual_cost: Optional[float],
    novelty_decay: float = 1.0,
    files_touched: Optional[List[str]] = None,
    complexity_score: Optional[float] = None,
) -> Dict[str, Any]:
    """Create a jury submission and assign voters."""
    submission_id = f"sub_{int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}"
    impact_score = estimate_impact(estimated_budget, task_type, files_touched, complexity_score)
    voters_needed = required_voters(impact_score)
    pool = [v for v in _load_voter_pool() if v != author_id]
    random.shuffle(pool)
    jury_pool = pool[:voters_needed]

    path_multiplier = get_path_multiplier(origin)
    record_path(origin)

    submission = {
        "submission_id": submission_id,
        "task_id": task_id,
        "author_id": author_id,
        "author_name": author_name,
        "summary": summary[:500],
        "task_type": task_type,
        "origin": origin,
        "estimated_budget": estimated_budget,
        "actual_cost": actual_cost,
        "impact_score": round(impact_score, 3),
        "impact_label": _impact_label(impact_score),
        "voters_required": voters_needed,
        "novelty_decay": novelty_decay,
        "path_multiplier": round(path_multiplier, 3),
        "complexity_score": complexity_score,
        "created_at": get_timestamp(),
        "status": "pending",
    }

    append_jsonl(SUBMISSIONS_FILE, submission)

    with _jury_lock():
        assignments = _load_assignments()
        assignments[submission_id] = jury_pool
        _save_assignments(assignments)

    return {"submission_id": submission_id, "assigned": len(jury_pool), "required": voters_needed}


def get_assignments(voter_id: str) -> List[Dict[str, Any]]:
    """Return pending assignments for a voter (blind)."""
    assignments = _load_assignments()
    decisions = _load_decisions()
    votes = _load_votes()
    voted_ids = {v["submission_id"] for v in votes if v.get("voter_id") == voter_id}

    submissions = _load_submissions()
    results = []
    for sub in submissions[-200:]:
        sub_id = sub.get("submission_id")
        if not sub_id:
            continue
        if sub_id in decisions:
            continue
        if sub_id in voted_ids:
            continue
        if voter_id not in assignments.get(sub_id, []):
            continue
        results.append(
            {
                "submission_id": sub_id,
                "summary": sub.get("summary"),
                "task_type": sub.get("task_type"),
                "origin": sub.get("origin"),
                "impact": sub.get("impact_label"),
                "created_at": sub.get("created_at"),
            }
        )
    return results


def cast_vote(
    *,
    submission_id: str,
    voter_id: str,
    vote: str,
    justification: str,
) -> Dict[str, Any]:
    """Record a vote and trigger finalization if quorum reached."""
    vote = vote.lower().strip()
    if vote not in {"pass", "fail"}:
        return {"success": False, "error": "invalid_vote"}

    if not _validate_justification(justification):
        return {"success": False, "error": "justification_too_weak"}

    assignments = _load_assignments()
    if voter_id not in assignments.get(submission_id, []):
        return {"success": False, "error": "not_assigned"}

    decisions = _load_decisions()
    if submission_id in decisions:
        return {"success": False, "error": "already_decided"}

    votes = _load_votes()
    if any(v.get("submission_id") == submission_id and v.get("voter_id") == voter_id for v in votes):
        return {"success": False, "error": "already_voted"}

    submissions = _load_submissions()
    submission = next((s for s in submissions if s.get("submission_id") == submission_id), None)
    if not submission:
        return {"success": False, "error": "submission_not_found"}

    author_id = submission.get("author_id", "")
    if voter_id == author_id:
        return {"success": False, "error": "self_vote_not_allowed"}
    weight = _vote_weight(voter_id, author_id)

    daily_count = _voter_daily_count(voter_id)
    if daily_count >= VOTER_DAILY_LIMIT:
        weight = min(weight, 0.3)

    record = {
        "submission_id": submission_id,
        "voter_id": voter_id,
        "author_id": author_id,
        "vote": vote,
        "justification": justification[:2000],
        "weight": weight,
        "timestamp": get_timestamp(),
        "timestamp_ts": time.time(),
    }
    append_jsonl(VOTES_FILE, record)

    reward = VOTER_REWARD_TOKENS
    if _strong_justification(justification):
        reward += LOGIC_BONUS_TOKENS

    try:
        from swarm_enrichment import get_enrichment

        enrichment = get_enrichment(WORKSPACE)
        enrichment.grant_free_time(voter_id, reward, reason="jury_vote")
    except Exception:
        pass

    append_jsonl(
        REWARDS_FILE,
        {
            "submission_id": submission_id,
            "voter_id": voter_id,
            "reward_tokens": reward,
            "timestamp": get_timestamp(),
        },
    )

    finalize_submission(submission_id)
    return {"success": True, "reward_tokens": reward}


def _compress_feedback(votes: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    pass_reasons = []
    fail_reasons = []
    for vote in votes:
        text = vote.get("justification", "")
        if not text:
            continue
        first_sentence = text.split(".", 1)[0].strip()
        if vote.get("vote") == "pass":
            pass_reasons.append(first_sentence)
        else:
            fail_reasons.append(first_sentence)

    def _unique(items: List[str]) -> List[str]:
        seen = set()
        result = []
        for item in items:
            key = item.lower()
            if key and key not in seen:
                result.append(item)
                seen.add(key)
        return result

    return {
        "strengths": _unique(pass_reasons)[:3],
        "concerns": _unique(fail_reasons)[:5],
    }


def finalize_submission(submission_id: str) -> Optional[Dict[str, Any]]:
    """Finalize a submission if quorum reached."""
    decisions = _load_decisions()
    if submission_id in decisions:
        return None

    submissions = _load_submissions()
    submission = next((s for s in submissions if s.get("submission_id") == submission_id), None)
    if not submission:
        return None

    votes = [v for v in _load_votes() if v.get("submission_id") == submission_id]
    if len(votes) < submission.get("voters_required", 0):
        return None

    total_weight = sum(v.get("weight", 1.0) for v in votes)
    if total_weight <= 0:
        verdict = "fail"
        quality_score = 0.0
    else:
        pass_weight = sum(v.get("weight", 1.0) for v in votes if v.get("vote") == "pass")
        quality_score = pass_weight / total_weight
        verdict = "pass" if quality_score >= PASS_THRESHOLD else "fail"

    feedback = _compress_feedback(votes)

    reward_result = None
    if verdict == "pass":
        try:
            from swarm_enrichment import get_enrichment

            enrichment = get_enrichment(WORKSPACE)
            reward_result = enrichment.apply_verdict_reward(
                author_id=submission.get("author_id", ""),
                author_name=submission.get("author_name", "Unknown"),
                estimated_budget=submission.get("estimated_budget"),
                actual_cost=submission.get("actual_cost"),
                quality_score=quality_score,
                origin=submission.get("origin", "general"),
                novelty_decay=submission.get("novelty_decay", 1.0),
                path_multiplier=submission.get("path_multiplier", 1.0),
                submission_id=submission_id,
            )
        except Exception:
            reward_result = None

    decision_record = {
        "submission_id": submission_id,
        "verdict": verdict,
        "decided_at": get_timestamp(),
    }
    decisions[submission_id] = decision_record
    _save_decisions(decisions)

    append_jsonl(
        RESULTS_FILE,
        {
            "submission_id": submission_id,
            "verdict": verdict,
            "decided_at": decision_record["decided_at"],
            "quality_score": round(quality_score, 3),
        },
    )

    author_feedback = {
        "submission_id": submission_id,
        "author_id": submission.get("author_id", ""),
        "author_name": submission.get("author_name", "Unknown"),
        "verdict": verdict,
        "reward": reward_result.get("reward_tokens") if reward_result else 0,
        "feedback": feedback,
        "timestamp": get_timestamp(),
    }
    append_jsonl(FEEDBACK_FILE, author_feedback)

    return decision_record


def get_voter_rewards(voter_id: str) -> List[Dict[str, Any]]:
    rewards = read_jsonl(REWARDS_FILE, default=[])
    return [r for r in rewards if r.get("voter_id") == voter_id][-50:]


def get_author_feedback(identity_id: str) -> List[Dict[str, Any]]:
    feedback = read_jsonl(FEEDBACK_FILE, default=[])
    return [f for f in feedback if f.get("author_id") == identity_id][-20:]


__all__ = [
    "submit_change",
    "get_assignments",
    "cast_vote",
    "finalize_submission",
    "get_voter_rewards",
    "get_author_feedback",
]
