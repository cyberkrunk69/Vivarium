"""
Emergency stop mechanisms for AI swarm system.
Provides KillSwitch and CircuitBreaker classes for emergency control.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class KillSwitch:
    """
    Emergency stop mechanism for halting all worker processes.
    Supports global halt, pause/resume, and file-based halt flag.
    """

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.halt_file = self.workspace / "HALT"
        self.pause_file = self.workspace / "PAUSE"
        self.state_file = self.workspace / "killswitch_state.json"
        self._halted = False
        self._paused = False

    def global_halt(self, reason: str = "Manual halt triggered"):
        """
        Stops all spawned processes immediately.
        Creates HALT file and sets internal halt flag.
        """
        self._halted = True
        self.halt_file.write_text(json.dumps({
            "halted": True,
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }, indent=2))
        self._save_state()
        print(f"[KILLSWITCH] GLOBAL HALT: {reason}")

    def pause_all(self, reason: str = "Manual pause triggered"):
        """
        Pauses execution but allows resume.
        Creates PAUSE file and sets pause flag.
        """
        self._paused = True
        self.pause_file.write_text(json.dumps({
            "paused": True,
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }, indent=2))
        self._save_state()
        print(f"[KILLSWITCH] PAUSED: {reason}")

    def resume(self):
        """Resume from paused state."""
        self._paused = False
        if self.pause_file.exists():
            self.pause_file.unlink()
        self._save_state()
        print("[KILLSWITCH] RESUMED")

    def check_halt_flag(self) -> Dict[str, any]:
        """
        Workers poll this to check if they should stop.
        Returns status dict with halt/pause state and reason.
        """
        # Check file-based halt (takes precedence)
        if self.halt_file.exists():
            try:
                data = json.loads(self.halt_file.read_text())
                return {
                    "should_stop": True,
                    "halted": True,
                    "paused": False,
                    "reason": data.get("reason", "HALT file exists")
                }
            except:
                return {
                    "should_stop": True,
                    "halted": True,
                    "paused": False,
                    "reason": "HALT file exists"
                }

        # Check file-based pause
        if self.pause_file.exists():
            try:
                data = json.loads(self.pause_file.read_text())
                return {
                    "should_stop": False,
                    "halted": False,
                    "paused": True,
                    "reason": data.get("reason", "PAUSE file exists")
                }
            except:
                return {
                    "should_stop": False,
                    "halted": False,
                    "paused": True,
                    "reason": "PAUSE file exists"
                }

        # Check internal state
        if self._halted:
            return {
                "should_stop": True,
                "halted": True,
                "paused": False,
                "reason": "Internal halt flag set"
            }

        if self._paused:
            return {
                "should_stop": False,
                "halted": False,
                "paused": True,
                "reason": "Internal pause flag set"
            }

        # All clear
        return {
            "should_stop": False,
            "halted": False,
            "paused": False,
            "reason": None
        }

    def get_halt_reason(self) -> str:
        """Get the reason for current halt/pause state."""
        if self.halt_file.exists():
            try:
                data = json.loads(self.halt_file.read_text())
                return data.get("reason", "Unknown reason")
            except:
                return "Halt file exists"
        if self.pause_file.exists():
            try:
                data = json.loads(self.pause_file.read_text())
                return data.get("reason", "Unknown reason")
            except:
                return "Pause file exists"
        return None

    def clear_halt(self):
        """Clear halt state (requires explicit action)."""
        self._halted = False
        if self.halt_file.exists():
            self.halt_file.unlink()
        self._save_state()
        print("[KILLSWITCH] HALT CLEARED")

    def _save_state(self):
        """Persist killswitch state to disk."""
        state = {
            "halted": self._halted,
            "paused": self._paused,
            "timestamp": datetime.now().isoformat()
        }
        self.state_file.write_text(json.dumps(state, indent=2))


class CircuitBreaker:
    """
    Circuit breaker that trips on cost threshold, failure rate, or suspicious patterns.
    """

    def __init__(self,
                 cost_threshold: float = 100.0,
                 failure_threshold: int = 5,
                 time_window: int = 300):
        """
        Args:
            cost_threshold: Max cost before tripping (dollars)
            failure_threshold: Max consecutive failures before tripping
            time_window: Time window for failure rate calculation (seconds)
        """
        self.cost_threshold = cost_threshold
        self.failure_threshold = failure_threshold
        self.time_window = time_window

        self.total_cost = 0.0
        self.failure_history: List[Dict] = []
        self.consecutive_failures = 0
        self.tripped = False
        self.trip_reason = None

    def record_cost(self, cost: float) -> bool:
        """
        Record operation cost and check if threshold exceeded.
        Returns True if circuit breaker tripped.
        """
        self.total_cost += cost
        if self.total_cost >= self.cost_threshold:
            self.trip(f"Cost threshold exceeded: ${self.total_cost:.2f} >= ${self.cost_threshold:.2f}")
            return True
        return False

    def record_failure(self, error: str) -> bool:
        """
        Record failure and check if failure threshold exceeded.
        Returns True if circuit breaker tripped.
        """
        now = time.time()
        self.failure_history.append({
            "timestamp": now,
            "error": error
        })
        self.consecutive_failures += 1

        # Clean old failures outside time window
        self.failure_history = [
            f for f in self.failure_history
            if now - f["timestamp"] <= self.time_window
        ]

        # Check consecutive failures
        if self.consecutive_failures >= self.failure_threshold:
            self.trip(f"Consecutive failure threshold exceeded: {self.consecutive_failures} failures")
            return True

        # Check failure rate in time window
        if len(self.failure_history) >= self.failure_threshold:
            self.trip(f"Failure rate exceeded: {len(self.failure_history)} failures in {self.time_window}s")
            return True

        return False

    def record_success(self):
        """Record successful operation (resets consecutive failure count)."""
        self.consecutive_failures = 0

    def detect_suspicious_pattern(self, operation: str) -> bool:
        """
        Detect suspicious patterns in operations.
        Returns True if circuit breaker tripped.
        """
        suspicious_keywords = [
            "rm -rf", "del /f", "format", "DROP DATABASE",
            "exec(", "eval(", "__import__",
            "os.system", "subprocess.call",
            "while True", "infinite loop"
        ]

        for keyword in suspicious_keywords:
            if keyword.lower() in operation.lower():
                self.trip(f"Suspicious pattern detected: '{keyword}' in operation")
                return True

        return False

    def trip(self, reason: str):
        """Trip the circuit breaker."""
        self.tripped = True
        self.trip_reason = reason
        print(f"[CIRCUIT BREAKER] TRIPPED: {reason}")

    def reset(self):
        """Reset circuit breaker (requires explicit action)."""
        self.tripped = False
        self.trip_reason = None
        self.consecutive_failures = 0
        self.failure_history.clear()
        print("[CIRCUIT BREAKER] RESET")

    def status(self) -> Dict:
        """Get current circuit breaker status."""
        return {
            "tripped": self.tripped,
            "reason": self.trip_reason,
            "total_cost": self.total_cost,
            "cost_threshold": self.cost_threshold,
            "consecutive_failures": self.consecutive_failures,
            "failure_threshold": self.failure_threshold,
            "recent_failures": len(self.failure_history)
        }

    def get_status(self) -> Dict:
        """Alias for status() for compatibility."""
        return self.status()

    def check_cost(self, cost: float) -> bool:
        """Alias for record_cost() for compatibility."""
        return self.record_cost(cost)


# Global instances
_kill_switch = None
_circuit_breaker = None

def get_kill_switch() -> KillSwitch:
    """Get global KillSwitch instance."""
    global _kill_switch
    if _kill_switch is None:
        _kill_switch = KillSwitch()
    return _kill_switch

def get_circuit_breaker() -> CircuitBreaker:
    """Get global CircuitBreaker instance."""
    global _circuit_breaker
    if _circuit_breaker is None:
        _circuit_breaker = CircuitBreaker()
    return _circuit_breaker
