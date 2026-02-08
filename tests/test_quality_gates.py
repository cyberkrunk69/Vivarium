import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from quality_gates import QualityGateManager, QualityGateError


def test_change_vote_to_needs_qa(tmp_path):
    manager = QualityGateManager(tmp_path)
    change_id = manager.submit_change_for_vote(
        title="Add input validation",
        description="Ensure request payload is sanitized.",
        author_id="resident_alpha",
    )

    change = manager.record_change_vote(change_id, "approved")
    assert change["status"] == "needs_qa"
    assert change["blind_vote"]["status"] == "approved"


def test_claim_qa_requires_specialization(tmp_path):
    manager = QualityGateManager(tmp_path)
    change_id = manager.submit_change_for_vote(
        title="Fix budget tracking",
        description="Align budget deductions with usage.",
        author_id="resident_beta",
    )
    manager.record_change_vote(change_id, "approved")

    manager.register_resident(
        resident_id="resident_qa",
        name="QA Focus",
        specializations=["qa", "testing"],
        focus_statement="I focus on testing and quality maxxing.",
    )
    manager.register_resident(
        resident_id="resident_dev",
        name="Builder",
        specializations=["review"],
    )

    change = manager.claim_qa(change_id, "resident_qa")
    assert change["qa"]["assigned_to"] == "resident_qa"

    with pytest.raises(QualityGateError):
        manager.claim_qa(change_id, "resident_dev")


def test_unit_test_flow_creates_integration_task(tmp_path):
    manager = QualityGateManager(tmp_path)
    change_id = manager.submit_change_for_vote(
        title="Harden API payloads",
        description="Add defensive parsing for JSON bodies.",
        author_id="resident_gamma",
    )
    manager.record_change_vote(change_id, "approved")

    manager.register_resident(
        resident_id="resident_qa",
        name="QA Specialist",
        specializations=["qa"],
    )
    manager.claim_qa(change_id, "resident_qa")

    test_id = manager.submit_test_for_vote(change_id, "resident_qa", test_type="unit")
    manager.record_test_vote(test_id, "approved")
    change = manager.record_test_result(change_id, "unit", passed=True)

    assert change["gates"]["unit"] == "passed"
    assert change["status"] == "needs_integration"

    state = manager.load_state()
    assert state["integration_tasks"]


def test_integration_batch_and_e2e_gate(tmp_path):
    manager = QualityGateManager(tmp_path)
    change_id = manager.submit_change_for_vote(
        title="Add queue guardrails",
        description="Prevent invalid queue transitions.",
        author_id="resident_delta",
    )
    manager.record_change_vote(change_id, "approved")
    manager.register_resident(
        resident_id="resident_qa",
        name="QA",
        specializations=["qa"],
    )
    manager.claim_qa(change_id, "resident_qa")
    test_id = manager.submit_test_for_vote(change_id, "resident_qa", test_type="unit")
    manager.record_test_vote(test_id, "approved")
    manager.record_test_result(change_id, "unit", passed=True)

    batches = manager.create_integration_batches(max_batch_size=2)
    assert batches

    batch = manager.record_integration_batch_result(batches[0]["batch_id"], passed=True)
    assert batch["status"] == "passed"

    change = manager.record_e2e_result(change_id, passed=True)
    assert change["status"] == "ready_for_merge"
    assert change["gates"]["integration"] == "passed"
    assert change["gates"]["e2e"] == "passed"
