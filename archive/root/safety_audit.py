"""
Safety Audit Logging System
Comprehensive audit trail for all system operations.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


class AuditLogger:
    """Records all system operations for transparency and anomaly detection."""

    def __init__(self, log_file: str = "audit_log.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _write_entry(self, entry: Dict[str, Any]):
        """Append entry to audit log (append-only)."""
        entry["timestamp"] = datetime.now().isoformat()
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def log_task_execution(
        self,
        task_id: str,
        task_input: str,
        task_output: str,
        cost: float,
        status: str,
        metadata: Optional[Dict] = None
    ):
        """Record task execution with input, output, and cost."""
        entry = {
            "type": "task_execution",
            "task_id": task_id,
            "input": task_input,
            "output": task_output,
            "cost": cost,
            "status": status,
            "metadata": metadata or {}
        }
        self._write_entry(entry)

    def log_file_operation(
        self,
        operation: str,
        file_path: str,
        success: bool,
        details: Optional[Dict] = None
    ):
        """Record file read/write operations."""
        entry = {
            "type": "file_operation",
            "operation": operation,  # read, write, delete, etc.
            "file_path": file_path,
            "success": success,
            "details": details or {}
        }
        self._write_entry(entry)

    def log_tool_invocation(
        self,
        tool_name: str,
        parameters: Dict,
        result: Any,
        success: bool,
        duration: float
    ):
        """Record external tool invocations."""
        entry = {
            "type": "tool_invocation",
            "tool_name": tool_name,
            "parameters": parameters,
            "result": str(result)[:500],  # Truncate long results
            "success": success,
            "duration": duration
        }
        self._write_entry(entry)

    def log_blocked_operation(
        self,
        operation_type: str,
        reason: str,
        attempted_action: Dict,
        severity: str = "warning"
    ):
        """Record blocked or rejected operations."""
        entry = {
            "type": "blocked_operation",
            "operation_type": operation_type,
            "reason": reason,
            "attempted_action": attempted_action,
            "severity": severity
        }
        self._write_entry(entry)

    def _load_entries(self) -> List[Dict]:
        """Load all audit entries."""
        if not self.log_file.exists():
            return []

        entries = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries

    def generate_audit_report(self, output_file: str = "audit_report.md") -> str:
        """Generate markdown summary of audit log."""
        entries = self._load_entries()

        if not entries:
            return "# Audit Report\n\nNo audit entries found."

        # Aggregate statistics
        stats = defaultdict(int)
        task_costs = []
        blocked_ops = []

        for entry in entries:
            entry_type = entry.get("type", "unknown")
            stats[entry_type] += 1

            if entry_type == "task_execution":
                task_costs.append(entry.get("cost", 0))
            elif entry_type == "blocked_operation":
                blocked_ops.append(entry)

        # Generate report
        report_lines = [
            "# Audit Report",
            f"\nGenerated: {datetime.now().isoformat()}",
            f"\nTotal Entries: {len(entries)}",
            "\n## Summary Statistics\n"
        ]

        for entry_type, count in sorted(stats.items()):
            report_lines.append(f"- {entry_type}: {count}")

        if task_costs:
            total_cost = sum(task_costs)
            avg_cost = total_cost / len(task_costs)
            report_lines.extend([
                f"\n## Task Execution Costs",
                f"\n- Total tasks: {len(task_costs)}",
                f"- Total cost: ${total_cost:.4f}",
                f"- Average cost: ${avg_cost:.4f}"
            ])

        if blocked_ops:
            report_lines.append(f"\n## Blocked Operations ({len(blocked_ops)})\n")
            for op in blocked_ops[-10:]:  # Last 10
                report_lines.append(
                    f"- **{op.get('operation_type')}**: {op.get('reason')} "
                    f"(Severity: {op.get('severity')})"
                )

        # Recent activity
        report_lines.append("\n## Recent Activity (Last 10 Entries)\n")
        for entry in entries[-10:]:
            timestamp = entry.get("timestamp", "N/A")
            entry_type = entry.get("type", "unknown")
            report_lines.append(f"- [{timestamp}] {entry_type}")

        report = "\n".join(report_lines)

        # Write report to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        return report

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect suspicious patterns in audit log."""
        entries = self._load_entries()
        anomalies = []

        # Pattern 1: High frequency of blocked operations
        blocked_count = sum(1 for e in entries if e.get("type") == "blocked_operation")
        if blocked_count > 10:
            anomalies.append({
                "type": "high_blocked_ops",
                "severity": "warning",
                "description": f"High number of blocked operations: {blocked_count}",
                "count": blocked_count
            })

        # Pattern 2: Rapid task execution (potential runaway)
        task_entries = [e for e in entries if e.get("type") == "task_execution"]
        if len(task_entries) > 1:
            recent_tasks = task_entries[-20:]  # Last 20 tasks
            timestamps = [
                datetime.fromisoformat(e["timestamp"])
                for e in recent_tasks
            ]
            if len(timestamps) >= 2:
                time_span = (timestamps[-1] - timestamps[0]).total_seconds()
                if time_span < 60 and len(recent_tasks) >= 10:
                    anomalies.append({
                        "type": "rapid_execution",
                        "severity": "critical",
                        "description": f"{len(recent_tasks)} tasks in {time_span:.1f} seconds",
                        "tasks": len(recent_tasks),
                        "duration": time_span
                    })

        # Pattern 3: High cost tasks
        for entry in task_entries:
            cost = entry.get("cost", 0)
            if cost > 1.0:  # More than $1 per task
                anomalies.append({
                    "type": "high_cost_task",
                    "severity": "warning",
                    "description": f"Task {entry.get('task_id')} cost ${cost:.2f}",
                    "task_id": entry.get("task_id"),
                    "cost": cost
                })

        # Pattern 4: Failed tool invocations
        failed_tools = [
            e for e in entries
            if e.get("type") == "tool_invocation" and not e.get("success")
        ]
        if len(failed_tools) > 5:
            anomalies.append({
                "type": "tool_failures",
                "severity": "warning",
                "description": f"{len(failed_tools)} failed tool invocations",
                "count": len(failed_tools)
            })

        # Pattern 5: Suspicious file operations
        file_ops = [e for e in entries if e.get("type") == "file_operation"]
        delete_ops = [e for e in file_ops if e.get("operation") == "delete"]
        if len(delete_ops) > 10:
            anomalies.append({
                "type": "excessive_deletions",
                "severity": "critical",
                "description": f"{len(delete_ops)} file deletion operations",
                "count": len(delete_ops)
            })

        return anomalies


# Convenience function
def get_audit_logger() -> AuditLogger:
    """Get singleton audit logger instance."""
    return AuditLogger()
