"""
Scout Audit Log — Append-only JSONL event log for LLM navigation accounting.

Survives SIGKILL, power loss, existential dread. Answers "what happened and how much did it cost?"

Usage:
    from vivarium.scout.audit import AuditLog

    log = AuditLog()
    log.log("nav", cost=0.000003, model="llama-3.1-8b", input_t=42, output_t=28)
    spend = log.hourly_spend(hours=1)
"""

import gzip
import json
import logging
import os
import threading
import time
import uuid
from collections import deque
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

logger = logging.getLogger(__name__)

# Default path: ~/.scout/audit.jsonl
DEFAULT_AUDIT_PATH = Path("~/.scout/audit.jsonl").expanduser()
ROTATION_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
FSYNC_EVERY_N_LINES = 10
FSYNC_INTERVAL_SEC = 1.0

# Event types per spec
EVENT_TYPES = frozenset({
    "nav", "brief", "cascade", "validation_fail", "budget", "skip", "trigger",
    "tldr", "tldr_auto_generated", "deep", "doc_sync",
    "commit_draft", "pr_snippet", "impact_analysis",
    "module_brief",
    "pr_synthesis",
    "roast_with_docs",
})

# Per-process session ID
_SESSION_ID: Optional[str] = None
_SESSION_LOCK = threading.Lock()


def _get_session_id() -> str:
    """Return uuid4 session ID, one per process."""
    global _SESSION_ID
    with _SESSION_LOCK:
        if _SESSION_ID is None:
            _SESSION_ID = str(uuid.uuid4())
        return _SESSION_ID


class AuditLog:
    """
    Append-only JSONL event log with line buffering, fsync cadence, and crash recovery.

    - Line buffering (buffering=1): flush on newline
    - Atomic writes: single write() per event, no partial JSON
    - Fsync: every 10 lines OR every 1 second
    - Log rotation: auto-archive at 10MB, gzip old logs
    - Corruption recovery: skip malformed lines on read, log warning
    """

    def __init__(self, path: Path = None):
        self._path = Path(path).expanduser().resolve() if path else DEFAULT_AUDIT_PATH
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._file: Optional[Any] = None
        self._lines_since_fsync = 0
        self._last_fsync = 0.0
        self._ensure_open()

    def _ensure_open(self) -> None:
        """Open file with line buffering if not already open."""
        if self._file is not None and not self._file.closed:
            return
        self._file = open(
            self._path,
            "a",
            encoding="utf-8",
            buffering=1,  # Line buffering — flush on newline
        )
        self._lines_since_fsync = 0
        self._last_fsync = time.monotonic()

    def _maybe_rotate(self) -> None:
        """Rotate log if >= 10MB: gzip current, start fresh."""
        try:
            stat = self._path.stat()
        except OSError:
            return
        if stat.st_size < ROTATION_SIZE_BYTES:
            return

        self._close_file()
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        archived = self._path.parent / f"{self._path.stem}_{ts}.jsonl.gz"

        with open(self._path, "rb") as f:
            data = f.read()
        with gzip.open(archived, "wb") as zf:
            zf.write(data)
        self._path.unlink()
        self._ensure_open()

    def _close_file(self) -> None:
        if self._file is not None and not self._file.closed:
            try:
                self._file.flush()
                os.fsync(self._file.fileno())
            except OSError:
                pass
            self._file.close()
            self._file = None

    def _fsync_if_needed(self) -> None:
        """Fsync every 10 lines or every 1 second."""
        self._lines_since_fsync += 1
        now = time.monotonic()
        if (
            self._lines_since_fsync >= FSYNC_EVERY_N_LINES
            or (now - self._last_fsync) >= FSYNC_INTERVAL_SEC
        ):
            try:
                if self._file is not None and not self._file.closed:
                    self._file.flush()
                    os.fsync(self._file.fileno())
            except OSError:
                pass
            self._lines_since_fsync = 0
            self._last_fsync = now

    def log(
        self,
        event_type: str,
        *,
        cost: float = None,
        model: str = None,
        input_t: int = None,
        output_t: int = None,
        files: List[str] = None,
        reason: str = None,
        confidence: int = None,
        duration_ms: int = None,
        config: Dict[str, Any] = None,
        raw_brief_path: str = None,
        **kwargs: Any,
    ) -> None:
        """
        Log an event. Atomic line write, fsync cadence.

        Args:
            event_type: One of nav|brief|cascade|validation_fail|budget|skip|trigger|tldr|deep|doc_sync
            cost: USD cost (optional). Omit (None) when no API call was made. When
                an API call was made, pass the calculated cost from usage; LLM clients
                use a small epsilon (e.g. 1e-7) when cost rounds to 0 so the log
                distinguishes "call made" from "no call".
            model: Model name (optional)
            input_t, output_t: Token counts (optional)
            files: Affected file paths (optional)
            reason: e.g. hallucinated_path|cost_exceeds_limit|hourly_budget_exhausted
            confidence: 0-100 (optional)
            duration_ms: Elapsed ms (optional)
            config: Snapshot of config at event time (optional)
            **kwargs: Additional fields (stored as-is if JSON-serializable)
        """
        session_id = kwargs.pop("session_id", None) or _get_session_id()
        event = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "event": event_type,
            "session_id": session_id,
        }
        if cost is not None:
            event["cost"] = cost
        if model is not None:
            event["model"] = model
        if input_t is not None:
            event["input_t"] = input_t
        if output_t is not None:
            event["output_t"] = output_t
        if files is not None:
            event["files"] = files
        if reason is not None:
            event["reason"] = reason
        if confidence is not None:
            event["confidence"] = confidence
        if duration_ms is not None:
            event["duration_ms"] = duration_ms
        if config is not None:
            event["config"] = config
        if raw_brief_path is not None:
            event["raw_brief_path"] = raw_brief_path

        for k, v in kwargs.items():
            if k not in event and v is not None:
                try:
                    json.dumps(v)
                    event[k] = v
                except (TypeError, ValueError):
                    event[k] = str(v)

        line = json.dumps(event, default=str) + "\n"

        with self._lock:
            self._maybe_rotate()
            self._ensure_open()
            self._file.write(line)
            self._fsync_if_needed()

    def _iter_lines(self) -> Iterator[str]:
        """Stream lines from current log file. Skips malformed lines, logs warnings."""
        if not self._path.exists():
            return
        with open(self._path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n\r")
                if not line:
                    continue
                yield line

    def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse one JSON line. Return None and log warning if corrupted."""
        try:
            return json.loads(line)
        except json.JSONDecodeError as e:
            logger.warning("AuditLog: skipping malformed line (corruption recovery): %s", e)
            return None

    def query(
        self,
        since: Optional[datetime] = None,
        event_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Streaming JSONL parser — memory-efficient for large logs.

        Returns events matching since (inclusive) and event_type filter.
        Skips malformed lines with a logged warning.
        """
        since_ts = since.isoformat() if since else None
        results: List[Dict[str, Any]] = []

        for line in self._iter_lines():
            obj = self._parse_line(line)
            if obj is None:
                continue
            if since_ts and obj.get("ts", "") < since_ts:
                continue
            if event_type is not None and obj.get("event") != event_type:
                continue
            results.append(obj)

        return results

    def hourly_spend(self, hours: int = 1) -> float:
        """Sum costs in last N hours."""
        if hours <= 0:
            return 0.0
        cutoff = datetime.now(timezone.utc).replace(
            microsecond=0, second=0, minute=0
        )
        cutoff = cutoff - timedelta(hours=hours)
        events = self.query(since=cutoff)
        return sum(e.get("cost", 0) or 0 for e in events)

    def last_events(
        self,
        n: int = 20,
        event_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Recent events, optionally filtered. Streams and keeps last N matches."""
        window: deque = deque(maxlen=n)
        for line in self._iter_lines():
            obj = self._parse_line(line)
            if obj is None:
                continue
            if event_type is not None and obj.get("event") != event_type:
                continue
            window.append(obj)
        return list(window)

    def accuracy_metrics(self, since: datetime) -> Dict[str, Any]:
        """
        % validation_fail vs total nav events.

        Returns dict with total_nav, validation_fail_count, accuracy_pct.
        """
        events = self.query(since=since)
        nav_events = [e for e in events if e.get("event") == "nav"]
        validation_fails = [e for e in events if e.get("event") == "validation_fail"]
        total_nav = len(nav_events)
        fail_count = len(validation_fails)
        if total_nav == 0:
            return {
                "total_nav": 0,
                "validation_fail_count": fail_count,
                "accuracy_pct": 100.0,
            }
        accuracy = 100.0 * (total_nav - fail_count) / total_nav
        return {
            "total_nav": total_nav,
            "validation_fail_count": fail_count,
            "accuracy_pct": round(accuracy, 2),
        }

    def gate_metrics(
        self,
        since: Optional[datetime] = None,
        last_n: int = 10,
    ) -> Dict[str, Any]:
        """
        Gate health from gate_compress and gate_escalate events.

        Returns: pass_count, escalate_count, total, pass_rate_pct, avg_confidence,
        escalate_rate_pct, last_queries (list of {outcome, reason}).
        """
        events = self.query(since=since) if since else self.query()
        gate_compress = [e for e in events if e.get("event") == "gate_compress"]
        gate_escalate = [e for e in events if e.get("event") == "gate_escalate"]

        # Pass: gate_compress with confidence, no reason (or not parse_fail/api_error/stale_cascade)
        passes = [
            e for e in gate_compress
            if e.get("confidence") is not None
            and e.get("reason") not in ("parse_fail", "api_error", "stale_cascade")
        ]
        # Escalate: gate_compress stale_cascade + gate_escalate
        escalates_stale = [e for e in gate_compress if e.get("reason") == "stale_cascade"]
        escalates_other = gate_escalate

        pass_count = len(passes)
        escalate_count = len(escalates_stale) + len(escalates_other)
        total = pass_count + escalate_count

        confidences = [e.get("confidence", 0) / 100.0 for e in passes if e.get("confidence") is not None]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        pass_rate_pct = round(100.0 * pass_count / total, 1) if total else 0.0
        escalate_rate_pct = round(100.0 * escalate_count / total, 1) if total else 0.0

        # Last N queries: pass + escalate in chronological order
        last_queries: List[Dict[str, Any]] = []
        all_outcomes = (
            [("pass", None, e) for e in passes]
            + [("escalate", "stale_cache", e) for e in escalates_stale]
            + [("escalate", "low_confidence", e) for e in escalates_other]
        )
        all_outcomes.sort(key=lambda x: x[2].get("ts", ""))
        for outcome, reason, ev in all_outcomes[-last_n:]:
            last_queries.append({"outcome": outcome, "reason": reason})

        return {
            "pass_count": pass_count,
            "escalate_count": escalate_count,
            "total": total,
            "pass_rate_pct": pass_rate_pct,
            "avg_confidence": round(avg_confidence, 2),
            "escalate_rate_pct": escalate_rate_pct,
            "last_queries": last_queries,
        }

    def flush(self) -> None:
        """Force flush and fsync to ensure events are persisted (e.g. before process exit)."""
        with self._lock:
            if self._file is not None and not self._file.closed:
                try:
                    self._file.flush()
                    os.fsync(self._file.fileno())
                except OSError:
                    pass

    def close(self) -> None:
        """Flush and close the log file."""
        with self._lock:
            self._close_file()

    def __enter__(self) -> "AuditLog":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
