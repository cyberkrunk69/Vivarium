#!/usr/bin/env python3
"""
Tool Operation Logger - Track actual tool usage vs claimed file modifications

This module provides logging functionality to track when workers claim to modify files
vs when they actually use tools like Write/Edit. This helps detect the hallucination bug
where workers claim success without actually performing work.
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Any
import hashlib

TOOL_LOG_FILE = "tool_operations.json"

class ToolOperationLogger:
    """Tracks tool operations and file modifications to detect hallucinations."""

    def __init__(self, workspace: Path, session_id: int):
        self.workspace = Path(workspace)
        self.session_id = session_id
        self.log_file = self.workspace / TOOL_LOG_FILE
        self.operations = []

    def log_claimed_operation(self, operation_type: str, file_path: str, details: str = None):
        """Log when a worker claims to have performed a file operation."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "type": "claimed",
            "operation": operation_type,  # "write", "edit", "create", "modify"
            "file": file_path,
            "details": details,
            "source": "worker_output"
        }
        self.operations.append(entry)
        self._append_to_log_file(entry)

    def log_actual_operation(self, operation_type: str, file_path: str, details: str = None):
        """Log when a tool actually performs a file operation."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "type": "actual",
            "operation": operation_type,
            "file": file_path,
            "details": details,
            "source": "tool_execution",
            "file_hash": self._get_file_hash(file_path) if Path(file_path).exists() else None
        }
        self.operations.append(entry)
        self._append_to_log_file(entry)

    def log_verification_result(self, claimed_files: List[str], verified_files: List[str],
                               hallucination_detected: bool):
        """Log the result of verification comparing claimed vs actual file modifications."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "type": "verification",
            "claimed_files": claimed_files,
            "verified_files": verified_files,
            "hallucination_detected": hallucination_detected,
            "discrepancy_count": len(claimed_files) - len(verified_files),
            "source": "verification_system"
        }
        self.operations.append(entry)
        self._append_to_log_file(entry)

    def _get_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file content."""
        try:
            path = Path(file_path) if not Path(file_path).is_absolute() else Path(file_path)
            if not path.is_absolute():
                path = self.workspace / path
            return hashlib.md5(path.read_bytes()).hexdigest()
        except Exception:
            return None

    def _append_to_log_file(self, entry: Dict[str, Any]):
        """Append a single log entry to the log file."""
        try:
            if self.log_file.exists():
                # Load existing logs
                log_data = json.loads(self.log_file.read_text())
                if not isinstance(log_data, list):
                    log_data = []
            else:
                log_data = []

            # Append new entry
            log_data.append(entry)

            # Keep only last 1000 entries to prevent file bloat
            if len(log_data) > 1000:
                log_data = log_data[-1000:]

            # Write back
            self.log_file.write_text(json.dumps(log_data, indent=2))

        except Exception as e:
            print(f"Warning: Could not write to tool operation log: {e}")

    def generate_session_summary(self) -> Dict[str, Any]:
        """Generate a summary of operations for this session."""
        claimed_ops = [op for op in self.operations if op.get("type") == "claimed"]
        actual_ops = [op for op in self.operations if op.get("type") == "actual"]
        verifications = [op for op in self.operations if op.get("type") == "verification"]

        claimed_files = set()
        actual_files = set()

        for op in claimed_ops:
            claimed_files.add(op.get("file", ""))

        for op in actual_ops:
            actual_files.add(op.get("file", ""))

        # Remove empty strings
        claimed_files.discard("")
        actual_files.discard("")

        hallucination_risk = len(claimed_files) > 0 and len(actual_files) == 0

        return {
            "session_id": self.session_id,
            "claimed_operations": len(claimed_ops),
            "actual_operations": len(actual_ops),
            "claimed_files": list(claimed_files),
            "actual_files": list(actual_files),
            "hallucination_risk": hallucination_risk,
            "verification_results": verifications,
            "summary_timestamp": datetime.datetime.now().isoformat()
        }

def create_tool_logger(workspace: Path, session_id: int) -> ToolOperationLogger:
    """Factory function to create a new tool operation logger."""
    return ToolOperationLogger(workspace, session_id)

def log_hallucination_detection(workspace: Path, session_id: int, run_num: int,
                               claimed_files: List[str], verified_files: List[str]):
    """Convenience function to log hallucination detection results."""
    logger = create_tool_logger(workspace, session_id)
    hallucination = len(claimed_files) > 0 and len(verified_files) == 0
    logger.log_verification_result(claimed_files, verified_files, hallucination)

    if hallucination:
        print(f"[Session {session_id}] [TOOL_LOGGER] HALLUCINATION logged: {len(claimed_files)} claimed, {len(verified_files)} verified")

    return logger.generate_session_summary()