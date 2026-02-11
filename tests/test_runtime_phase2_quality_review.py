import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from vivarium.runtime import worker_runtime as worker
from vivarium.runtime.quality_gates import QualityGateManager
from vivarium.runtime.runtime_contract import KNOWN_EXECUTION_STATUSES
from vivarium.runtime.task_verifier import VerificationResult, Verdict
from vivarium.utils import read_json, read_jsonl


class _StaticVerifier:
    def __init__(self, result: VerificationResult):
        self._result = result

    def verify_task_output(self, task, output, files_created=None):
        return self._result


class _StubResidentContext:
    class _Identity:
        identity_id = "identity_phase5"

    identity = _Identity()


class _StubEnrichment:
    def __init__(self):
        self.calls = []

    def grant_free_time(self, identity_id, tokens, reason):
        self.calls.append(
            {"identity_id": identity_id, "tokens": tokens, "reason": reason}
        )
        return {
            "free_time": tokens,
            "journal": 0,
            "granted": {"free_time": tokens, "journal": 0},
        }


def test_runtime_contract_includes_phase2_review_statuses():
    assert "pending_review" in KNOWN_EXECUTION_STATUSES
    assert "approved" in KNOWN_EXECUTION_STATUSES
    assert "requeue" in KNOWN_EXECUTION_STATUSES


def test_post_execution_review_approved_records_needs_qa(monkeypatch, tmp_path):
    manager = QualityGateManager(tmp_path)
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", manager)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(
        worker,
        "WORKER_TASK_VERIFIER",
        _StaticVerifier(
            VerificationResult(
                verdict=Verdict.APPROVE,
                confidence=0.95,
                issues=[],
                suggestions=[],
            )
        ),
    )

    task = {"id": "task_phase2_ok", "prompt": "Ship the patch"}
    result = {"status": "completed", "result_summary": "done", "errors": None, "model": "local"}
    review = worker._run_post_execution_review(task, result, resident_ctx=None, previous_review_attempt=0)

    # Verifier approved -> task stays pending_review until human approves in control panel
    assert review["status"] == "pending_review"
    assert review["quality_gate_status"] == "needs_qa"

    state = manager.load_state()
    assert state["changes"]["task_phase2_ok"]["status"] == "needs_qa"

    events = read_jsonl(worker.EXECUTION_LOG, default=[])
    assert events
    assert events[-1]["status"] == "pending_review"
    assert events[-1]["review_verdict"] == "APPROVE"


def test_post_execution_review_requeue_then_fail_after_max_attempts(monkeypatch, tmp_path):
    manager = QualityGateManager(tmp_path)
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", manager)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MAX_REQUEUE_ATTEMPTS", 2)
    monkeypatch.setattr(
        worker,
        "WORKER_TASK_VERIFIER",
        _StaticVerifier(
            VerificationResult(
                verdict=Verdict.REJECT,
                confidence=0.9,
                issues=["Syntax errors detected"],
                suggestions=["Fix syntax and retry"],
            )
        ),
    )

    task = {"id": "task_phase2_reject", "prompt": "Implement feature"}
    result = {"status": "completed", "result_summary": "done", "errors": None, "model": "local"}

    first_review = worker._run_post_execution_review(
        task,
        result,
        resident_ctx=None,
        previous_review_attempt=0,
    )
    assert first_review["status"] == "requeue"
    assert first_review["review_attempt"] == 1
    assert first_review["quality_gate_status"] == "rejected"

    second_review = worker._run_post_execution_review(
        task,
        result,
        resident_ctx=None,
        previous_review_attempt=1,
    )
    assert second_review["status"] == "failed"
    assert second_review["review_attempt"] == 2
    assert "after 2 attempt(s)" in second_review["errors"]


def test_post_execution_review_approved_applies_phase5_reward(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "PHASE5_REWARD_LEDGER", tmp_path / "phase5_reward_ledger.json")
    monkeypatch.setattr(
        worker,
        "WORKER_TASK_VERIFIER",
        _StaticVerifier(
            VerificationResult(
                verdict=Verdict.APPROVE,
                confidence=0.9,
                issues=[],
                suggestions=[],
            )
        ),
    )
    enrichment = _StubEnrichment()
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", enrichment)

    task = {"id": "task_phase5_reward", "prompt": "Ship patch", "max_budget": 0.20}
    result = {
        "status": "completed",
        "result_summary": "done",
        "errors": None,
        "model": "local",
        "budget_used": 0.05,
    }
    review = worker._run_post_execution_review(
        task,
        result,
        resident_ctx=_StubResidentContext(),
        previous_review_attempt=0,
    )

    # Verifier approved -> pending_review; phase5 reward is applied on human approval, not here
    assert review["status"] == "pending_review"
    assert review["phase5_reward_applied"] is False
    assert review["phase5_reward_reason"] == "awaiting_human_approval"
    assert enrichment.calls == []


def test_post_execution_review_approved_skips_phase5_reward_without_budget_savings(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "PHASE5_REWARD_LEDGER", tmp_path / "phase5_reward_ledger.json")
    monkeypatch.setattr(
        worker,
        "WORKER_TASK_VERIFIER",
        _StaticVerifier(
            VerificationResult(
                verdict=Verdict.APPROVE,
                confidence=0.95,
                issues=[],
                suggestions=[],
            )
        ),
    )
    enrichment = _StubEnrichment()
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", enrichment)

    task = {"id": "task_phase5_no_reward", "prompt": "Ship patch", "max_budget": 0.10}
    result = {
        "status": "completed",
        "result_summary": "done",
        "errors": None,
        "model": "local",
        "budget_used": 0.12,
    }
    review = worker._run_post_execution_review(
        task,
        result,
        resident_ctx=_StubResidentContext(),
        previous_review_attempt=0,
    )

    # Verifier approved -> pending_review; reward not applied here (human approval path checks budget)
    assert review["status"] == "pending_review"
    assert review["phase5_reward_applied"] is False
    assert review["phase5_reward_reason"] == "awaiting_human_approval"
    assert enrichment.calls == []


def test_post_execution_review_approved_phase5_reward_is_idempotent(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "PHASE5_REWARD_LEDGER", tmp_path / "phase5_reward_ledger.json")
    monkeypatch.setattr(
        worker,
        "WORKER_TASK_VERIFIER",
        _StaticVerifier(
            VerificationResult(
                verdict=Verdict.APPROVE,
                confidence=0.92,
                issues=[],
                suggestions=[],
            )
        ),
    )
    enrichment = _StubEnrichment()
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", enrichment)

    task = {"id": "task_phase5_once", "prompt": "Ship patch", "max_budget": 0.30}
    result = {
        "status": "completed",
        "result_summary": "done",
        "errors": None,
        "model": "local",
        "budget_used": 0.10,
    }

    first_review = worker._run_post_execution_review(
        task,
        result,
        resident_ctx=_StubResidentContext(),
        previous_review_attempt=0,
    )
    second_review = worker._run_post_execution_review(
        task,
        result,
        resident_ctx=_StubResidentContext(),
        previous_review_attempt=0,
    )

    # Both return pending_review; no reward applied in this flow (human approval applies it)
    assert first_review["status"] == "pending_review"
    assert first_review["phase5_reward_applied"] is False
    assert first_review["phase5_reward_reason"] == "awaiting_human_approval"
    assert second_review["status"] == "pending_review"
    assert second_review["phase5_reward_applied"] is False
    assert second_review["phase5_reward_reason"] == "awaiting_human_approval"
    assert enrichment.calls == []

