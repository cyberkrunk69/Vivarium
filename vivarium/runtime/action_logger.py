#!/usr/bin/env python3
"""
Action Logger - Real-time visibility into all swarm activity.

Provides a centralized, structured log of every action taken by any actor
in the system. Designed for human monitoring and auditability.

Usage:
    from vivarium.runtime.action_logger import get_action_logger, ActionType

    logger = get_action_logger()
    logger.log(
        actor="Custom-Name",
        action_type=ActionType.TOOL,
        action="write_file",
        detail="app/gut_check.py (+12 lines)"
    )

Log Format:
    HH:MM:SS | Actor        | Type     | Action        | Detail
    11:05:23 | Custom-Name  | TOOL     | write_file    | app/gut_check.py (+12 lines)
"""

import json
import threading
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Callable, List
from dataclasses import dataclass, asdict
from vivarium.runtime.vivarium_scope import AUDIT_ROOT, ensure_scope_layout

ensure_scope_layout()


class ActionType(Enum):
    """Categories of actions for filtering and display."""
    TOOL = "TOOL"           # File operations, tool calls
    COST = "COST"           # API costs, token usage
    SOCIAL = "SOCIAL"       # Watercooler, discussions
    IDENTITY = "IDENTITY"   # Token grants, session changes
    SAFETY = "SAFETY"       # Blocked actions, violations
    BUDGET = "BUDGET"       # Budget alerts, limits
    TEST = "TEST"           # Test executions
    JOURNAL = "JOURNAL"     # Journal entries
    ERROR = "ERROR"         # Errors, failures
    SYSTEM = "SYSTEM"       # System events, startup/shutdown
    API = "API"             # API calls (model, tokens)


# ANSI color codes for terminal output
class Colors:
    """Terminal colors for action types."""
    RED = "\033[91m"        # Danger: SAFETY blocked, ERROR, BUDGET exceeded
    ORANGE = "\033[93m"     # Warning: BUDGET alerts, safety warnings
    YELLOW = "\033[33m"     # Cost: COST, API, money-related
    GREEN = "\033[92m"      # Success: Tests passing, safety OK
    TEAL = "\033[96m"       # Social: SOCIAL, IDENTITY, JOURNAL (personality/emergent)
    BLUE = "\033[94m"       # Info: TOOL calls, file operations
    PURPLE = "\033[95m"     # System: SYSTEM events
    WHITE = "\033[97m"      # Neutral: timestamps, general
    GRAY = "\033[90m"       # Dim: less important info
    RESET = "\033[0m"       # Reset to default
    BOLD = "\033[1m"        # Bold text


# Map action types to colors
ACTION_COLORS = {
    ActionType.TOOL: Colors.BLUE,
    ActionType.COST: Colors.YELLOW,
    ActionType.API: Colors.YELLOW,
    ActionType.SOCIAL: Colors.TEAL,
    ActionType.IDENTITY: Colors.TEAL,
    ActionType.JOURNAL: Colors.TEAL,
    ActionType.SAFETY: Colors.RED,      # Will be orange for warnings
    ActionType.BUDGET: Colors.ORANGE,   # Will be red when exceeded
    ActionType.TEST: Colors.GREEN,      # Will be red if failures
    ActionType.ERROR: Colors.RED,
    ActionType.SYSTEM: Colors.PURPLE,
}


@dataclass
class ActionEntry:
    """A single logged action."""
    timestamp: str
    actor: str
    action_type: str
    action: str
    detail: str
    session_id: Optional[str] = None
    metadata: Optional[dict] = None

    def to_line(self, color: bool = False) -> str:
        """Format as a single log line for display."""
        time_short = self.timestamp.split("T")[1].split(".")[0] if "T" in self.timestamp else self.timestamp

        # Add day of week (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
        try:
            dt = datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
            day_abbrev = dt.strftime("%a")  # Mon, Tue, etc.
        except (ValueError, TypeError):
            day_abbrev = "???"

        base_line = f"{day_abbrev} {time_short} | {self.actor:<12} | {self.action_type:<8} | {self.action:<14} | {self.detail}"

        if not color:
            return base_line

        # Get color based on action type and context
        try:
            action_type_enum = ActionType(self.action_type)
            base_color = ACTION_COLORS.get(action_type_enum, Colors.WHITE)
        except ValueError:
            base_color = Colors.WHITE

        # Special color overrides based on context
        if self.action_type == "SAFETY" and "BLOCKED" in self.action:
            base_color = Colors.RED
        elif self.action_type == "SAFETY" and "WARNING" in self.action:
            base_color = Colors.ORANGE
        elif self.action_type == "BUDGET" and "EXCEEDED" in self.action:
            base_color = Colors.RED
        elif self.action_type == "TEST" and "fail" in self.detail.lower():
            base_color = Colors.RED if "0 pass" in self.detail else Colors.ORANGE
        elif self.action_type == "TEST" and "0 fail" in self.detail:
            base_color = Colors.GREEN

        return f"{base_color}{base_line}{Colors.RESET}"

    def to_dict(self) -> dict:
        d = asdict(self)
        # Ensure metadata is JSON-serializable (e.g. no datetime/custom objects)
        if d.get("metadata") is not None and isinstance(d["metadata"], dict):
            clean = {}
            for k, v in d["metadata"].items():
                if isinstance(v, (str, int, float, bool, type(None))):
                    clean[k] = v
                else:
                    clean[k] = str(v)
            d["metadata"] = clean
        return d


class ActionLogger:
    """
    Centralized action logger for swarm visibility.

    Thread-safe, writes to both file and optional callbacks (for streaming).
    """

    def __init__(self, log_file: Optional[str] = None, max_detail_length: int = 80):
        resolved_log = Path(log_file) if log_file else (AUDIT_ROOT / "action_log.jsonl")
        self.log_file = resolved_log
        self.max_detail_length = max_detail_length
        self._lock = threading.Lock()
        self._callbacks: List[Callable[[ActionEntry], None]] = []
        self._current_actor: Optional[str] = None
        self._current_session: Optional[str] = None

        # Also maintain a human-readable log
        self.readable_log = self.log_file.with_suffix(".log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.readable_log.parent.mkdir(parents=True, exist_ok=True)

        # Write header on startup
        self._write_header()

    def _write_header(self):
        """Write a header to the readable log."""
        now = datetime.now()
        day_name = now.strftime("%A")  # Full day name
        header = f"\n{'='*95}\nACTION LOG STARTED: {now.isoformat()} ({day_name})\n{'='*95}\n"
        header += f"{'DAY':<3} {'TIME':<8} | {'ACTOR':<12} | {'TYPE':<8} | {'ACTION':<14} | DETAIL\n"
        header += "-" * 95 + "\n"

        with self._lock:
            with open(self.readable_log, "a", encoding="utf-8") as f:
                f.write(header)

    def set_context(self, actor: str = None, session_id: str = None):
        """Set the current actor/session context for subsequent logs."""
        if actor:
            self._current_actor = actor
        if session_id:
            self._current_session = session_id

    def clear_context(self):
        """Clear the current context."""
        self._current_actor = None
        self._current_session = None

    def add_callback(self, callback: Callable[[ActionEntry], None]):
        """Add a callback for real-time streaming (e.g., to WebSocket)."""
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[ActionEntry], None]):
        """Remove a streaming callback."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _truncate(self, text: str) -> str:
        """Truncate detail text for display."""
        if len(text) > self.max_detail_length:
            return text[:self.max_detail_length - 3] + "..."
        return text

    def log(
        self,
        action_type: ActionType,
        action: str,
        detail: str,
        actor: str = None,
        session_id: str = None,
        metadata: dict = None,
        model: str = None,
    ):
        """
        Log an action.

        Args:
            action_type: Category of action (TOOL, COST, SOCIAL, etc.)
            action: Specific action name (write_file, edit_file, etc.)
            detail: Human-readable detail (truncated for display)
            actor: Who performed this (defaults to current context)
            session_id: Session ID (defaults to current context)
            metadata: Additional structured data (not displayed, but logged)
            model: Model used for this action (e.g. LLM name); stored in metadata and in JSONL.
        """
        with self._lock:
            # Snapshot context and build entry under lock for thread safety
            actor_val = actor or self._current_actor or "UNKNOWN"
            session_val = session_id or self._current_session
            meta = dict(metadata) if metadata else {}
            if model is not None and model != "":
                meta["model"] = str(model)
            entry = ActionEntry(
                timestamp=datetime.now().isoformat(timespec="milliseconds"),
                actor=actor_val,
                action_type=action_type.value,
                action=action,
                detail=self._truncate(detail),
                session_id=session_val,
                metadata=meta if meta else None,
            )
            # Write to JSONL for structured parsing
            try:
                line = json.dumps(entry.to_dict(), default=str) + "\n"
            except (TypeError, ValueError):
                line = json.dumps({
                    "timestamp": entry.timestamp,
                    "actor": entry.actor,
                    "action_type": entry.action_type,
                    "action": entry.action,
                    "detail": entry.detail,
                    "session_id": entry.session_id,
                    "metadata": None,
                }) + "\n"
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line)

            # Write to readable log for human monitoring
            with open(self.readable_log, "a", encoding="utf-8") as f:
                f.write(entry.to_line() + "\n")

        # Notify callbacks (for real-time streaming)
        for callback in self._callbacks:
            try:
                callback(entry)
            except Exception as e:
                # Don't let callback errors break logging
                pass

    # Convenience methods for common action types

    def tool(self, action: str, detail: str, actor: str = None, **kwargs):
        """Log a tool call."""
        self.log(ActionType.TOOL, action, detail, actor, **kwargs)

    def file_created(self, path: str, lines: int, actor: str = None):
        """Log file creation."""
        self.log(ActionType.TOOL, "create_file", f"{path} (+{lines} lines)", actor)

    def file_edited(self, path: str, added: int, removed: int, actor: str = None):
        """Log file edit."""
        self.log(ActionType.TOOL, "edit_file", f"{path} (+{added}/-{removed} lines)", actor)

    def file_deleted(self, path: str, actor: str = None):
        """Log file deletion."""
        self.log(ActionType.TOOL, "delete_file", path, actor)

    def api_call(self, model: str, tokens: int, cost: float, actor: str = None):
        """Log an API call (model used, tokens, cost). Full model name is stored in metadata."""
        model_display = (model or "")[:20]
        self.log(
            ActionType.API,
            model_display,
            f"{tokens} tokens | ${cost:.4f}",
            actor,
            metadata={"model": (model or "").strip()} if (model or "").strip() else None,
        )

    def external_api_call(self, url: str, method: str = "GET", status: int = None, actor: str = None):
        """Log an external API call (non-Groq, non-model API)."""
        # Truncate URL to domain + path start for readability
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url or "")
            domain = parsed.netloc or "?"
            path = parsed.path[:30] + "..." if len(parsed.path) > 30 else parsed.path
            url_display = f"{domain}{path}"
        except Exception:
            url_display = (url or "")[:50] + "..." if len(url or "") > 50 else (url or "?")

        detail = f"{method} {url_display}"
        if status:
            detail += f" [{status}]"
        self.log(ActionType.API, "external", detail, actor)

    def cost_update(self, total: float, budget: float, actor: str = None):
        """Log cost/budget update."""
        pct = (total / budget * 100) if budget > 0 else 0
        self.log(ActionType.BUDGET, "cost_update", f"${total:.3f}/${budget:.2f} ({pct:.0f}%)", actor)

    def budget_alert(self, threshold: int, spent: float, budget: float, actor: str = None):
        """Log budget threshold alert."""
        self.log(ActionType.BUDGET, f"ALERT_{threshold}%", f"${spent:.3f}/${budget:.2f}", actor)

    def budget_exceeded(self, spent: float, budget: float, actor: str = None):
        """Log budget exceeded."""
        self.log(ActionType.BUDGET, "EXCEEDED", f"${spent:.3f} > ${budget:.2f} limit", actor)

    def social(self, room: str, message: str, actor: str = None):
        """Log social/watercooler post."""
        self.log(ActionType.SOCIAL, room, f'"{message}"', actor)

    def identity_tokens(self, tokens_granted: int, new_balance: int, reason: str, actor: str = None):
        """Log token grant to identity."""
        self.log(ActionType.IDENTITY, "tokens", f"+{tokens_granted} ({reason}) | balance: {new_balance}", actor)

    def token_spent(self, tokens_spent: int, action: str, new_balance: int, actor: str = None):
        """Log token spending for voluntary actions."""
        self.log(ActionType.IDENTITY, "spent", f"-{tokens_spent} ({action}) | balance: {new_balance}", actor)

    def identity_session(self, event: str, actor: str = None):
        """Log identity session event (start/end)."""
        self.log(ActionType.IDENTITY, event, "", actor)

    def safety_blocked(self, violation_type: str, detail: str, actor: str = None):
        """Log a blocked action."""
        self.log(ActionType.SAFETY, "BLOCKED", f"{violation_type}: {detail}", actor)

    def safety_warning(self, warning_type: str, detail: str, actor: str = None):
        """Log a safety warning."""
        self.log(ActionType.SAFETY, "WARNING", f"{warning_type}: {detail}", actor)

    def test_result(self, test_type: str, passed: int, failed: int, skipped: int = 0, actor: str = None):
        """Log test execution results."""
        self.log(ActionType.TEST, test_type, f"{passed} pass, {failed} fail, {skipped} skip", actor)

    def journal(self, journal_name: str, content_preview: str, actor: str = None):
        """Log journal entry."""
        self.log(ActionType.JOURNAL, journal_name, f'"{content_preview}"', actor)

    def error(self, error_type: str, message: str, actor: str = None):
        """Log an error."""
        self.log(ActionType.ERROR, error_type, message, actor)

    def system(self, event: str, detail: str = ""):
        """Log a system event."""
        self.log(ActionType.SYSTEM, event, detail, actor="SYSTEM")


# Global singleton
_logger: Optional[ActionLogger] = None
_logger_lock = threading.Lock()


def get_action_logger(log_file: Optional[str] = None) -> ActionLogger:
    """Get the global action logger instance."""
    global _logger
    if _logger is None:
        with _logger_lock:
            if _logger is None:
                _logger = ActionLogger(log_file)
    return _logger


def reset_action_logger():
    """Reset the global logger (for testing)."""
    global _logger
    _logger = None


# Quick access functions for common operations
def log_action(action_type: ActionType, action: str, detail: str, actor: str = None, **kwargs):
    """Quick log function."""
    get_action_logger().log(action_type, action, detail, actor, **kwargs)


if __name__ == "__main__":
    # Demo/test
    logger = get_action_logger("test_action_log.jsonl")

    logger.system("STARTUP", "Action logger initialized")

    logger.set_context(actor="Beam-31", session_id="session_1")
    logger.tool("list_dir", "/app")
    logger.tool("read_file", "SWARM_ROLE_HIERARCHY.md (26KB)")
    logger.file_created("app/unit_test_gate.py", 12)
    logger.file_edited("app/gut_check.py", 5, 3)
    logger.api_call("llama-3.3-70b", 1523, 0.003)

    logger.set_context(actor="Custom-Name")
    logger.social("watercooler", "Halfway through my shift. Completed 4 runs...")
    logger.identity_tokens(50, 1510, "standard_task")
    logger.journal("PLANNER", "Day 1: Created journals directory...")

    logger.safety_blocked("network_access", "github.com", actor="Beam-31")
    logger.budget_alert(75, 0.038, 0.05)
    logger.test_result("unit", 3, 1, 0)

    logger.error("api_timeout", "Groq API timeout after 30s", actor="Custom-Name")

    logger.system("SHUTDOWN", "Clean shutdown")

    print(f"\nLogs written to: {logger.log_file} and {logger.readable_log}")
    print("\nReadable log contents:")
    print(open(logger.readable_log).read())
