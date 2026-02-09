import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import worker
from quality_gates import QualityGateManager
from runtime_contract import KNOWN_EXECUTION_STATUSES
from task_verifier import VerificationResult, Verdict
from utils import read_jsonl


class _StaticVerifier:
    def __init__(self, result: VerificationResult):
        self._result = result

    def verify_task_output(self, task, output, files_created=None):
        return self._result


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

    assert review["status"] == "approved"
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

