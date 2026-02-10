# Self-Healing Infrastructure - Usage Guide

## What We Built

The swarm can now **prevent and recover from breaking itself**.

### Components

1. **`safety_validator.py`** - Validates Python syntax before writing
2. **`self_healing_wrapper.py`** - Wraps the spawner with health checks
3. **`task_verifier.py`** - Verifies task outputs before accepting

---

## How To Use

### Option 1: Run with Self-Healing Wrapper (Recommended)

```bash
python self_healing_wrapper.py
```

This will:
- ✓ Check for crash loops before starting
- ✓ Validate all critical Python files
- ✓ Auto-rollback if startup fails
- ✓ Enter safe mode if repeatedly broken

### Option 2: Run Normal Spawner (No Protection)

```bash
python grind_spawner_unified.py --delegate --budget 1.00
```

**Not recommended** until the rest of the architecture is implemented.

---

## Safety Features

### 1. Syntax Validation

Before any Python file is written:

```python
from safety_validator import SafeFileWriter

writer = SafeFileWriter()
result = writer.safe_write(filepath, content)

if not result.valid:
    print(f"Prevented writing invalid Python: {result.errors}")
```

### 2. Automatic Checkpoints

Every file modification creates a checkpoint:

```python
from safety_validator import CheckpointManager

cm = CheckpointManager()
checkpoint = cm.create_checkpoint([Path("myfile.py")], reason="before edit")

# ... make changes ...

# If something goes wrong:
cm.rollback(checkpoint)
```

### 3. Crash Loop Detection

The swarm tracks consecutive failures:

```bash
python -c "from safety_validator import HealthChecker; hc = HealthChecker(); print(hc.get_crash_loop_info())"
```

If 3+ consecutive failures → Safe mode automatically

### 4. Task Output Verification

Before marking a task complete:

```python
from task_verifier import TaskVerifier

verifier = TaskVerifier()
result = verifier.verify_task_output(task, output, files_created)

if result.verdict == Verdict.REJECT:
    print(f"Task failed verification: {result.issues}")
    # Don't accept the output, requeue the task
```

---

## Recovery Commands

### Manual Rollback

```python
from safety_validator import CheckpointManager
cm = CheckpointManager()

# List available checkpoints
checkpoints = cm.list_checkpoints()
for cp in checkpoints[-5:]:
    print(f"{cp.checkpoint_id}: {cp.timestamp} - {cp.reason}")

# Rollback to specific checkpoint
latest = cm.get_latest_checkpoint()
success, files = cm.rollback(latest)
```

### Reset Health Status

If you've manually fixed issues:

```bash
rm .health_status.json
```

### Validate Critical Files

Check if files are broken:

```bash
python -c "from safety_validator import validate_critical_files; print(validate_critical_files())"
```

---

## Integration with Grind Spawner

### Add to Task Execution Loop

```python
from safety_validator import SafeFileWriter, CheckpointManager
from task_verifier import TaskVerifier, Verdict

# Before writing files
writer = SafeFileWriter()
for filepath, content in task_output["files"].items():
    result = writer.safe_write(filepath, content, create_checkpoint=True)
    if not result.valid:
        return {"success": False, "error": f"Invalid Python: {result.errors}"}

# After task completes
verifier = TaskVerifier()
verification = verifier.verify_task_output(task, output, files_created)

if verification.verdict == Verdict.REJECT:
    # Rollback the changes
    checkpoint = CheckpointManager().get_latest_checkpoint()
    CheckpointManager().rollback(checkpoint)
    return {"success": False, "verification_failed": True, "issues": verification.issues}
elif verification.verdict == Verdict.MINOR_ISSUES:
    # Accept but log for cleanup
    return {"success": True, "warnings": verification.issues}
else:
    # Full approval
    return {"success": True}
```

---

## What's Next

Once the swarm is running safely with this infrastructure, it can build:

1. **Atomizer Node** - Parallel task execution
2. **Expert Node** - Batched deep thinking with caching
3. **Tool-First Router** - Build tools instead of re-solving
4. **Intent Gatekeeper** - Requirements gathering
5. **Consensus Node** - Multi-model debate
6. **Test Gates** - Automated testing

See `ARCHITECTURE_GAP_ANALYSIS.md` for the full roadmap.

---

## Metrics

Track how well the self-healing is working:

```python
from task_verifier import VerificationTracker

tracker = VerificationTracker()
stats = tracker.get_stats()

print(f"Approval rate: {stats['approval_rate']:.1%}")
print(f"Total verifications: {stats['total_verifications']}")
print(f"Rejected: {stats['rejected']}")
```

---

*Built: 2026-02-04*
*Purpose: Prevent the swarm from breaking itself*
