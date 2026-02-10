"""
Quality gating pipeline for code changes.

Flow:
1) Change submitted -> blind vote ballot created.
2) If approved -> change moves to needs_qa.
3) QA writes unit test -> test ballot created.
4) If approved -> unit tests run -> integration task created.
5) Integration tasks are batched -> run -> e2e task created.
6) When unit + integration + e2e pass -> ready_for_merge.
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils import read_json, write_json, get_timestamp


DEFAULT_GATES = {"unit": "pending", "integration": "pending", "e2e": "pending"}
ALLOWED_SPECIALIZATIONS = {"qa", "integration", "e2e", "review", "testing"}


class QualityGateError(ValueError):
    """Raised when a gating transition is invalid."""


class QualityGateManager:
    def __init__(self, workspace: Optional[Path] = None):
        self.workspace = Path(workspace) if workspace else Path(__file__).resolve().parents[2]
        self.queue_file = self.workspace / "quality_gate_queue.json"

    def load_state(self) -> Dict[str, Any]:
        # New workspaces won't have a queue file yet; default state should be used.
        state = read_json(self.queue_file, default=self._default_state())
        if not state:
            state = self._default_state()
        return self._normalize_state(state)

    def save_state(self, state: Dict[str, Any]) -> None:
        state["updated_at"] = get_timestamp()
        write_json(self.queue_file, state)

    def register_resident(
        self,
        resident_id: str,
        name: str,
        specializations: Optional[List[str]] = None,
        focus_statement: Optional[str] = None,
    ) -> Dict[str, Any]:
        state = self.load_state()
        specs = sorted({s for s in (specializations or []) if s in ALLOWED_SPECIALIZATIONS})
        resident = {
            "resident_id": resident_id,
            "name": name,
            "specializations": specs,
            "focus_statement": focus_statement or "",
            "updated_at": get_timestamp(),
        }
        state["residents"][resident_id] = resident
        self.save_state(state)
        return resident

    def submit_change(
        self,
        title: str,
        description: str,
        author_id: str,
        change_id: Optional[str] = None,
    ) -> str:
        state = self.load_state()
        change_id = change_id or self._new_id("chg")
        change = {
            "change_id": change_id,
            "title": title,
            "description": description,
            "author_id": author_id,
            "created_at": get_timestamp(),
            "status": "pending_vote",
            "gates": dict(DEFAULT_GATES),
            "qa": {"assigned_to": None, "test_submission_id": None},
            "integration": {"batch_id": None, "status": "pending"},
            "e2e": {"status": "pending"},
            "blind_vote": {"ballot_id": None, "status": "pending"},
        }
        state["changes"][change_id] = change
        self.save_state(state)
        return change_id

    def submit_change_for_vote(
        self,
        title: str,
        description: str,
        author_id: str,
        change_id: Optional[str] = None,
    ) -> str:
        change_id = self.submit_change(title, description, author_id, change_id)
        state = self.load_state()
        ballot_id = self._create_ballot(
            state,
            subject_type="change",
            subject_id=change_id,
            summary=title,
        )
        state["changes"][change_id]["blind_vote"] = {
            "ballot_id": ballot_id,
            "status": "pending",
        }
        self.save_state(state)
        return change_id

    def record_change_vote(self, change_id: str, decision: str) -> Dict[str, Any]:
        state = self.load_state()
        change = self._get_change(state, change_id)
        ballot_id = change["blind_vote"].get("ballot_id")
        if not ballot_id:
            raise QualityGateError("Change has no ballot to record")
        self._record_ballot(state, ballot_id, decision)
        if decision == "approved":
            change["status"] = "needs_qa"
        else:
            change["status"] = "rejected"
        change["blind_vote"]["status"] = decision
        self.save_state(state)
        return change

    def list_needs_qa(self) -> List[Dict[str, Any]]:
        state = self.load_state()
        return [c for c in state["changes"].values() if c["status"] == "needs_qa"]

    def claim_qa(self, change_id: str, resident_id: str) -> Dict[str, Any]:
        state = self.load_state()
        change = self._get_change(state, change_id)
        self._require_specialization(state, resident_id, "qa")
        if change["status"] != "needs_qa":
            raise QualityGateError("Change not available for QA")
        change["qa"]["assigned_to"] = resident_id
        change["status"] = "qa_in_progress"
        self.save_state(state)
        return change

    def submit_test_for_vote(
        self,
        change_id: str,
        submitted_by: str,
        test_type: str = "unit",
        test_id: Optional[str] = None,
    ) -> str:
        if test_type not in DEFAULT_GATES:
            raise QualityGateError(f"Unsupported test type: {test_type}")
        state = self.load_state()
        change = self._get_change(state, change_id)
        if change["status"] not in ("needs_qa", "qa_in_progress"):
            raise QualityGateError("Change is not in QA flow")
        if test_type != "unit" and change["gates"]["unit"] != "passed":
            raise QualityGateError("Unit tests must pass before higher-level tests")
        test_id = test_id or self._new_id("test")
        ballot_id = self._create_ballot(
            state,
            subject_type="test",
            subject_id=test_id,
            summary=f"{test_type} test for {change_id}",
        )
        test_submission = {
            "test_id": test_id,
            "change_id": change_id,
            "submitted_by": submitted_by,
            "test_type": test_type,
            "created_at": get_timestamp(),
            "ballot_id": ballot_id,
            "status": "pending_vote",
        }
        state["test_submissions"][test_id] = test_submission
        if test_type == "unit":
            change["qa"]["test_submission_id"] = test_id
        self.save_state(state)
        return test_id

    def record_test_vote(self, test_id: str, decision: str) -> Dict[str, Any]:
        state = self.load_state()
        test_submission = self._get_test_submission(state, test_id)
        self._record_ballot(state, test_submission["ballot_id"], decision)
        test_submission["status"] = decision
        self.save_state(state)
        return test_submission

    def record_test_result(
        self,
        change_id: str,
        test_type: str,
        passed: bool,
        details: Optional[str] = None,
    ) -> Dict[str, Any]:
        if test_type not in DEFAULT_GATES:
            raise QualityGateError(f"Unsupported test type: {test_type}")
        state = self.load_state()
        change = self._get_change(state, change_id)
        change["gates"][test_type] = "passed" if passed else "failed"
        change.setdefault("test_results", {})[test_type] = {
            "passed": passed,
            "details": details or "",
            "recorded_at": get_timestamp(),
        }
        if passed and test_type == "unit":
            self._queue_integration_task(state, change_id)
            change["status"] = "needs_integration"
        if passed and test_type == "integration":
            self._queue_e2e_task(state, change_id)
            change["status"] = "needs_e2e"
        if passed and test_type == "e2e":
            if self.is_change_mergeable(change):
                change["status"] = "ready_for_merge"
        self.save_state(state)
        return change

    def create_integration_batches(self, max_batch_size: int = 5) -> List[Dict[str, Any]]:
        if max_batch_size < 1:
            raise QualityGateError("Batch size must be >= 1")
        state = self.load_state()
        pending = [
            t for t in state["integration_tasks"].values()
            if t["status"] == "pending"
        ]
        batches = []
        for i in range(0, len(pending), max_batch_size):
            chunk = pending[i:i + max_batch_size]
            batch_id = self._new_id("batch")
            for task in chunk:
                task["status"] = "batched"
                task["batch_id"] = batch_id
            batch = {
                "batch_id": batch_id,
                "task_ids": [t["task_id"] for t in chunk],
                "created_at": get_timestamp(),
                "status": "pending",
            }
            state["integration_batches"][batch_id] = batch
            batches.append(batch)
        self.save_state(state)
        return batches

    def record_integration_batch_result(
        self,
        batch_id: str,
        passed: bool,
        details: Optional[str] = None,
    ) -> Dict[str, Any]:
        state = self.load_state()
        batch = state["integration_batches"].get(batch_id)
        if not batch:
            raise QualityGateError("Unknown integration batch")
        batch["status"] = "passed" if passed else "failed"
        batch["details"] = details or ""
        for task_id in batch["task_ids"]:
            task = state["integration_tasks"].get(task_id)
            if not task:
                continue
            task["status"] = "passed" if passed else "failed"
            change = self._get_change(state, task["change_id"])
            change["gates"]["integration"] = "passed" if passed else "failed"
            if passed:
                self._queue_e2e_task(state, change["change_id"])
                change["status"] = "needs_e2e"
        self.save_state(state)
        return batch

    def record_e2e_result(
        self,
        change_id: str,
        passed: bool,
        details: Optional[str] = None,
    ) -> Dict[str, Any]:
        state = self.load_state()
        change = self._get_change(state, change_id)
        change["gates"]["e2e"] = "passed" if passed else "failed"
        change.setdefault("test_results", {})["e2e"] = {
            "passed": passed,
            "details": details or "",
            "recorded_at": get_timestamp(),
        }
        if passed and self.is_change_mergeable(change):
            change["status"] = "ready_for_merge"
        else:
            change["status"] = "blocked"
        self.save_state(state)
        return change

    def is_change_mergeable(self, change: Dict[str, Any]) -> bool:
        return all(change["gates"].get(k) == "passed" for k in DEFAULT_GATES)

    def _queue_integration_task(self, state: Dict[str, Any], change_id: str) -> None:
        task_id = self._new_id("int")
        state["integration_tasks"][task_id] = {
            "task_id": task_id,
            "change_id": change_id,
            "status": "pending",
            "created_at": get_timestamp(),
            "batch_id": None,
        }

    def _queue_e2e_task(self, state: Dict[str, Any], change_id: str) -> None:
        change = self._get_change(state, change_id)
        change["e2e"]["status"] = "pending"

    def _create_ballot(self, state: Dict[str, Any], subject_type: str, subject_id: str, summary: str) -> str:
        ballot_id = self._new_id("vote")
        state["votes"][ballot_id] = {
            "ballot_id": ballot_id,
            "subject_type": subject_type,
            "subject_id": subject_id,
            "summary": summary,
            "created_at": get_timestamp(),
            "status": "pending",
        }
        state["vote_outbox"].append(ballot_id)
        return ballot_id

    def _record_ballot(self, state: Dict[str, Any], ballot_id: str, decision: str) -> None:
        if decision not in ("approved", "rejected"):
            raise QualityGateError("Decision must be 'approved' or 'rejected'")
        ballot = state["votes"].get(ballot_id)
        if not ballot:
            raise QualityGateError("Ballot not found")
        ballot["status"] = decision

    def _require_specialization(self, state: Dict[str, Any], resident_id: str, specialization: str) -> None:
        resident = state["residents"].get(resident_id)
        if not resident:
            raise QualityGateError("Resident not registered")
        if specialization not in resident.get("specializations", []):
            raise QualityGateError("Resident lacks required specialization")

    def _get_change(self, state: Dict[str, Any], change_id: str) -> Dict[str, Any]:
        change = state["changes"].get(change_id)
        if not change:
            raise QualityGateError("Change not found")
        change.setdefault("gates", dict(DEFAULT_GATES))
        return change

    def _get_test_submission(self, state: Dict[str, Any], test_id: str) -> Dict[str, Any]:
        test_submission = state["test_submissions"].get(test_id)
        if not test_submission:
            raise QualityGateError("Test submission not found")
        return test_submission

    def _default_state(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "created_at": get_timestamp(),
            "updated_at": get_timestamp(),
            "changes": {},
            "residents": {},
            "test_submissions": {},
            "integration_tasks": {},
            "integration_batches": {},
            "votes": {},
            "vote_outbox": [],
        }

    def _normalize_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        defaults = self._default_state()
        for key, value in defaults.items():
            if key not in state:
                state[key] = value
        return state

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:10]}"


__all__ = ["QualityGateManager", "QualityGateError"]
