# Worker.py File-Based Lock Protocol

## Lock Acquisition (try_acquire_lock)

The lock acquisition uses **atomic file creation** to prevent race conditions:

1. Check if lock file exists for the task
2. If exists and **stale** (>300 seconds old), remove it
3. If exists and fresh, return False (task is locked)
4. Create lock file atomically using `os.O_CREAT | os.O_EXCL` flags
   - Only ONE worker can successfully create the file
   - Other workers get FileExistsError and fail the acquisition
5. Write lock data: `{worker_id, started_at, task_id}`

## Stale Lock Detection (is_lock_stale)

A lock is considered stale if:

- **Age > 300 seconds (5 minutes)**: Original worker likely crashed
- **Corrupted**: JSON parse fails, missing "started_at" field
  - Corrupted locks are treated as stale and removed

Timestamp format: ISO 8601 UTC (`datetime.fromisoformat()` compatible)

## Race Condition Prevention

**Critical mechanism:** OS-level atomic file creation

```
Worker A                          Worker B
    |                                 |
    v                                 v
[Lock exists?]                  [Lock exists?]
    | No                             | No
    v                                v
[Try O_CREAT | O_EXCL]      [Try O_CREAT | O_EXCL]
    | SUCCESS                        | FAILS (FileExistsError)
    v                                v
[Acquire lock]              [Return False]
    |                                 |
    v                                 v
[Execute task]              [Skip task]
    |
    v
[Release lock]
```

**Why it works:**
- `os.O_CREAT | os.O_EXCL` is atomic at OS level
- Filesystem guarantees only one process succeeds
- No check-then-act race window
- Prevents multiple workers from executing same task

## Lock Lifecycle

1. **Acquired**: `try_acquire_lock()` creates `.lock` file in `task_locks/`
2. **Held**: During task execution (status = "in_progress")
3. **Released**: `release_lock()` deletes file after execution
4. **Recovery**: Stale locks auto-removed on next acquisition attempt

## Summary

The protocol uses **atomic OS-level file creation** as a distributed lock primitive, with 5-minute stale timeout for crash recovery. No explicit race conditions possible due to O_EXCL atomicity.
