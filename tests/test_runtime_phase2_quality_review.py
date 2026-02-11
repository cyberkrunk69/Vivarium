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


class _StubCommunityEnrichment(_StubEnrichment):
    def __init__(self):
        super().__init__()
        self.submissions = []

    def submit_task_for_community_review(
        self,
        task_id,
        result_excerpt,
        author_id,
        author_name,
        result_summary="",
        review_verdict="",
    ):
        self.submissions.append(
            {
                "task_id": task_id,
                "author_id": author_id,
                "author_name": author_name,
                "review_verdict": review_verdict,
            }
        )
        return {"success": True, "jurors_selected": 2, "auto_accepted": False}


def test_runtime_contract_includes_phase2_review_statuses():
    assert "pending_review" in KNOWN_EXECUTION_STATUSES
    assert "approved" in KNOWN_EXECUTION_STATUSES
    assert "requeue" in KNOWN_EXECUTION_STATUSES


def test_post_execution_review_approved_records_needs_qa(monkeypatch, tmp_path):
    manager = QualityGateManager(tmp_path)
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", manager)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")
    monkeypatch.setattr(worker, "REQUIRE_HUMAN_APPROVAL_DEFAULT", False)
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

    # Verifier approved -> auto-approved for high-confidence low-risk tasks.
    assert review["status"] == "approved"
    assert review["quality_gate_status"] == "needs_qa"

    state = manager.load_state()
    assert state["changes"]["task_phase2_ok"]["status"] == "needs_qa"

def test_post_execution_review_requeue_then_fail_after_max_attempts(monkeypatch, tmp_path):
    manager = QualityGateManager(tmp_path)
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", manager)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")
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


def test_post_execution_review_requeues_when_docs_task_did_not_write_artifact(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "WORKER_TASK_VERIFIER", None)
    monkeypatch.setattr(worker, "MVP_DOCS_ONLY_MODE", True)
    monkeypatch.setattr(worker, "MAX_REQUEUE_ATTEMPTS", 3)
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")

    task = {"id": "task_docs_missing_artifact", "prompt": "Create a markdown proposal for onboarding."}
    result = {
        "status": "completed",
        "result_summary": "I analyzed options and will create a proposal next.",
        "errors": None,
        "model": "local",
        "mvp_markdown_artifacts": {"enabled": True, "written": False, "reason": "doc_write_failed:disk_full"},
    }

    review = worker._run_post_execution_review(task, result, resident_ctx=None, previous_review_attempt=0)
    assert review["status"] == "requeue"
    assert "did not produce an artifact" in review["errors"]
    assert review["review_verdict"] == "REJECT"


def test_post_execution_review_requeues_planning_only_docs_output(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "WORKER_TASK_VERIFIER", None)
    monkeypatch.setattr(worker, "MVP_DOCS_ONLY_MODE", True)
    monkeypatch.setattr(worker, "MAX_REQUEUE_ATTEMPTS", 3)
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")

    task = {"id": "task_docs_planning_text", "prompt": "Write and persist a markdown proposal."}
    result = {
        "status": "completed",
        "result_summary": "I will create a markdown proposal in the resident_suggestions folder.",
        "errors": None,
        "model": "local",
        "mvp_markdown_artifacts": {
            "enabled": True,
            "written": True,
            "doc_path": str(tmp_path / "library" / "community_library" / "resident_suggestions" / "x.md"),
        },
    }

    review = worker._run_post_execution_review(task, result, resident_ctx=None, previous_review_attempt=0)
    assert review["status"] == "requeue"
    assert "planning text" in review["errors"]
    assert review["review_verdict"] == "REJECT"


def test_post_execution_review_approved_applies_phase5_reward(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")
    monkeypatch.setattr(worker, "PHASE5_REWARD_LEDGER", tmp_path / "phase5_reward_ledger.json")
    monkeypatch.setattr(worker, "REQUIRE_HUMAN_APPROVAL_DEFAULT", False)
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

    # Verifier approved -> auto-approved; reward is applied immediately on auto-approval.
    assert review["status"] == "approved"
    assert review["phase5_reward_applied"] is True
    assert review["phase5_reward_reason"].startswith("worker_approved_under_budget:")
    assert len(enrichment.calls) == 1


def test_post_execution_review_approved_skips_phase5_reward_without_budget_savings(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")
    monkeypatch.setattr(worker, "PHASE5_REWARD_LEDGER", tmp_path / "phase5_reward_ledger.json")
    monkeypatch.setattr(worker, "REQUIRE_HUMAN_APPROVAL_DEFAULT", False)
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

    # Verifier approved -> auto-approved; reward skipped when not under budget.
    assert review["status"] == "approved"
    assert review["phase5_reward_applied"] is False
    assert review["phase5_reward_reason"] == "not_under_budget"
    assert enrichment.calls == []


def test_post_execution_review_approved_phase5_reward_is_idempotent(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")
    monkeypatch.setattr(worker, "PHASE5_REWARD_LEDGER", tmp_path / "phase5_reward_ledger.json")
    monkeypatch.setattr(worker, "REQUIRE_HUMAN_APPROVAL_DEFAULT", False)
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

    # First auto-approval grants once; second run is idempotent.
    assert first_review["status"] == "approved"
    assert first_review["phase5_reward_applied"] is True
    assert second_review["status"] == "approved"
    assert second_review["phase5_reward_applied"] is False
    assert second_review["phase5_reward_reason"] == "already_granted"
    assert len(enrichment.calls) == 1


def test_post_execution_review_can_still_require_human_approval(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", None)
    monkeypatch.setattr(worker, "REQUIRE_HUMAN_APPROVAL_DEFAULT", True)
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

    task = {"id": "task_human_required", "prompt": "Ship patch"}
    result = {"status": "completed", "result_summary": "done", "errors": None, "model": "local"}
    review = worker._run_post_execution_review(task, result, resident_ctx=None, previous_review_attempt=0)

    assert review["status"] == "pending_review"
    assert review["phase5_reward_applied"] is False
    assert review["phase5_reward_reason"] == "awaiting_human_approval"


def test_post_execution_review_submits_to_community_review(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, "WORKER_QUALITY_GATES", None)
    monkeypatch.setattr(worker, "EXECUTION_LOG", tmp_path / "execution_log.jsonl")
    monkeypatch.setattr(worker, "MESSAGES_TO_HUMAN_PATH", tmp_path / "messages_to_human.jsonl")
    monkeypatch.setattr(worker, "REQUIRE_HUMAN_APPROVAL_DEFAULT", False)
    monkeypatch.setattr(worker, "MVP_DOCS_ONLY_MODE", False)
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
    enrichment = _StubCommunityEnrichment()
    monkeypatch.setattr(worker, "WORKER_ENRICHMENT", enrichment)

    class _ResidentCtx:
        class _Identity:
            identity_id = "identity_alpha"
            name = "Alpha"

        identity = _Identity()

    task = {"id": "task_community_wired", "prompt": "Write docs", "max_budget": 0.2}
    result = {"status": "completed", "result_summary": "done", "errors": None, "model": "local", "budget_used": 0.05}
    review = worker._run_post_execution_review(task, result, resident_ctx=_ResidentCtx(), previous_review_attempt=0)

    assert review["status"] == "approved"
    assert review["community_review_submitted"] is True
    assert review["community_review_jurors_selected"] == 2
    assert len(enrichment.submissions) == 1
    assert enrichment.submissions[0]["task_id"] == "task_community_wired"

