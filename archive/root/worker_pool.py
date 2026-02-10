# ----------------------------------------------------------------------
import task_verifier
import task_verifier
from .task_verifier import verify_output
import task_verifier
from task_verifier import Verdict  # Verdict enum: APPROVE, MINOR_ISSUES, REJECT
# Monkey‑patch WorkerPool.complete_task to run the Critic (task_verifier)
# before a task is finally marked complete.
# ----------------------------------------------------------------------
if 'WorkerPool' in globals():
    _original_complete_task = getattr(WorkerPool, 'complete_task', None)

def _process_verdict(self, task, result):
        """
        Run the worker's result through the Critic verifier and act on the verdict.
        """
        verdict, feedback = Critic.evaluate(result)

        if verdict == "APPROVE":
            self._mark_complete(task)
        elif verdict == "MINOR_ISSUES":
            self._log_issues(task, feedback)
            self._mark_complete(task)
        elif verdict == "REJECT":
            self._requeue_task(task, feedback)
        else:
            # Treat any unknown verdict as a rejection
            self._requeue_task(task, f"Unknown verdict: {verdict}")
    def _patched_complete_task(self, task_id, result, *args, **kwargs):
        """
def _mark_complete(self, task):
        """
        Wrapper around the existing completion logic.
        """
        # Preserve the original completion call (adjust if the original method name differs)
        # Verify the worker's output before marking the task complete
# Assume the worker's result is stored in a variable named `result`
verification = task_verifier.verify_task_output(result)
verdict = verification.get('verdict')
feedback = verification.get('feedback', '')

if verdict == 'REJECT':
    # Re‑queue the task with feedback for a retry
    self.requeue_task(task, feedback)
else:
    # APPROVE or MINOR_ISSUES: mark the task as completed
    verdict, feedback = verify_task_output(task, result)
if verdict in ("APPROVE", "MINOR_ISSUES"):
    self.complete_task(task)
elif verdict == "REJECT":
    self.requeue_task(task, feedback)
    if verdict == 'MINOR_ISSUES':
        self.log_minor_issues(task, feedback)

    def _log_issues(self, task, feedback):
        """
        Record minor‑issue feedback without aborting the task.
        """
        self.logger.info(f"Minor issues for task {task.id}: {feedback}")

    def _requeue_task(self, task, feedback):
        """
        Return a rejected task to the queue with the verifier's feedback.
        """
        self.logger.warning(f"Task {task.id} rejected: {feedback}. Re‑queuing.")
        # Assuming the pool uses a Queue named `task_queue`; adjust if named differently
        self.task_queue.put((task, feedback))
        Verify the worker's output using the Critic (task_verifier) before
        finalising the task.

        Returns:
            The original ``complete_task`` result for APPROVE/MINOR_ISSUES,
            or None for REJECT (the task is re‑queued with feedback).
        """
        verdict, feedback = verify_output(result)
# ----------------------------------------------------------------------
# Verify the worker's output using the Critic before finalizing the task.
# The Critic returns a tuple: (verdict, feedback). Verdict is one of:
#   - "APPROVE"
#   - "MINOR_ISSUES"
#   - "REJECT"
# If the verdict is REJECT, the task is re‑queued with the feedback for
# a retry. APPROVE and MINOR_ISSUES both result in the task being marked
# complete (the latter may be logged for later review).
verdict, feedback = task_verifier.verify_output(result)

if verdict == "APPROVE":
    self._finalize_task(task, result)
elif verdict == "MINOR_ISSUES":
    # Log the minor issues but still consider the task done.
    self.logger.info(
        f"Task {task.id} completed with minor issues: {feedback}"
    )
    self._finalize_task(task, result)
elif verdict == "REJECT":
    # Re‑queue the task with the Critic's feedback for another attempt.
    self.logger.warning(
        f"Task {task.id} rejected by Critic: {feedback}. Re‑queuing."
    )
    self.requeue_task(task, feedback=feedback)
else:
    # Defensive fallback – treat unknown verdicts as a rejection.
    self.logger.error(
        f"Unexpected verdict '{verdict}' from Critic for task {task.id}. "
        f"Re‑queuing as safety measure."
    )
    self.requeue_task(task, feedback="Unexpected verdict from Critic")
# ----------------------------------------------------------------------

        if verdict == "APPROVE":
            # Normal flow – mark the task as complete.
            if _original_complete_task:
                return _original_complete_task(self, task_id, result, *args, **kwargs)

        elif verdict == "MINOR_ISSUES":
            # Log the feedback but still consider the task complete.
            if hasattr(self, 'log_feedback'):
                self.log_feedback(task_id, feedback)
            if _original_complete_task:
                return _original_complete_task(self, task_id, result, *args, **kwargs)

        elif verdict == "REJECT":
            # Send the task back to the queue with the Critic's feedback.
            if hasattr(self, 'requeue_task'):
                self.requeue_task(task_id, feedback)
            # Do NOT call the original complete_task – the task stays pending.
            return

        else:
            # Fallback – preserve existing behaviour.
            if _original_complete_task:
# ----------------------------------------------------------------------
# Verify the worker's output before finalising the task.
# ----------------------------------------------------------------------
verdict, feedback = task_verifier.verify_output(result)

if verdict == Verdict.APPROVE or verdict == Verdict.MINOR_ISSUES:
    # Task is acceptable – mark it as completed.
    self._finalise_task(task, result, verdict, feedback)
elif verdict == Verdict.REJECT:
    # Task failed verification – re‑queue it with feedback for a retry.
    self._requeue_task(task, feedback)
else:
    # Fallback – treat unknown verdicts as a rejection.
    self._requeue_task(task, f"Unknown verdict: {verdict}")
    
# Skip the original completion call that would have run unconditionally.
continue
                return _original_complete_task(self, task_id, result, *args, **kwargs)

    # Replace the original method with the patched version.
    WorkerPool.complete_task = _patched_complete_task