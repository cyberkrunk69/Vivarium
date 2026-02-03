#!/usr/bin/env python3
"""
Engine Tracker Integration Module
Provides real-time tracking of engine switches, cost accumulation, and model usage.
"""

import json
import time
import requests
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class EngineEvent:
    """Represents an engine-related event for tracking."""
    worker_id: str
    event_type: str  # "selection", "switch", "cost_update"
    engine: str
    model: str
    reason: str
    cost: float = 0.0
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class EngineTracker:
    """
    Real-time engine tracking with dashboard integration.
    Monitors engine selections, switches, and cost accumulation.
    """

    def __init__(self, dashboard_url: str = "http://localhost:8080"):
        self.dashboard_url = dashboard_url
        self.events = []
        self.worker_states = {}
        self.running = False
        self.thread = None

        # Cost tracking per engine
        self.cost_accumulator = {
            "claude": 0.0,
            "groq": 0.0
        }

        # Usage statistics
        self.stats = {
            "total_requests": 0,
            "claude_requests": 0,
            "groq_requests": 0,
            "total_switches": 0,
            "session_start": datetime.now()
        }

    def start_tracking(self):
        """Start background tracking thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._tracking_loop, daemon=True)
            self.thread.start()
            print("🔍 Engine tracker started")

    def stop_tracking(self):
        """Stop background tracking."""
        self.running = False
        if self.thread:
            self.thread.join()
        print("🛑 Engine tracker stopped")

    def record_engine_selection(self, worker_id: str, engine: str, model: str, reason: str, cost: float = 0.0):
        """Record an engine selection for a worker."""
        event = EngineEvent(
            worker_id=worker_id,
            event_type="selection",
            engine=engine,
            model=model,
            reason=reason,
            cost=cost
        )

        # Update worker state
        old_engine = self.worker_states.get(worker_id, {}).get("engine")
        self.worker_states[worker_id] = {
            "engine": engine,
            "model": model,
            "reason": reason,
            "cost_accumulated": self.worker_states.get(worker_id, {}).get("cost_accumulated", 0.0) + cost,
            "switches": self.worker_states.get(worker_id, {}).get("switches", 0),
            "last_update": datetime.now().isoformat()
        }

        # Check if this is a switch
        if old_engine and old_engine != engine:
            self.worker_states[worker_id]["switches"] += 1
            self.stats["total_switches"] += 1
            event.event_type = "switch"

        # Update global stats
        self.stats["total_requests"] += 1
        if engine.lower() == "claude":
            self.stats["claude_requests"] += 1
        elif engine.lower() == "groq":
            self.stats["groq_requests"] += 1

        self.cost_accumulator[engine.lower()] += cost

        # Store event
        self.events.append(event)
        if len(self.events) > 1000:  # Keep last 1000 events
            self.events.pop(0)

        # Send to dashboard
        self._send_to_dashboard(event)

        print(f"📊 Engine selection: Worker {worker_id} → {engine} ({model}) - {reason}")

    def record_cost_update(self, worker_id: str, additional_cost: float):
        """Record additional cost for a worker."""
        if worker_id in self.worker_states:
            worker_state = self.worker_states[worker_id]
            worker_state["cost_accumulated"] += additional_cost

            engine = worker_state.get("engine", "claude").lower()
            self.cost_accumulator[engine] += additional_cost

            event = EngineEvent(
                worker_id=worker_id,
                event_type="cost_update",
                engine=worker_state.get("engine", "unknown"),
                model=worker_state.get("model", "unknown"),
                reason=f"Cost update: +${additional_cost:.3f}",
                cost=additional_cost
            )

            self.events.append(event)
            self._send_to_dashboard(event)

    def get_engine_distribution(self) -> Dict[str, Any]:
        """Get current engine usage distribution."""
        total_requests = max(self.stats["total_requests"], 1)

        claude_pct = (self.stats["claude_requests"] / total_requests) * 100
        groq_pct = (self.stats["groq_requests"] / total_requests) * 100

        return {
            "claude_percentage": claude_pct,
            "groq_percentage": groq_pct,
            "total_cost": sum(self.cost_accumulator.values()),
            "claude_cost": self.cost_accumulator["claude"],
            "groq_cost": self.cost_accumulator["groq"],
            "total_switches": self.stats["total_switches"],
            "total_requests": self.stats["total_requests"],
            "session_duration": str(datetime.now() - self.stats["session_start"]),
            "cost_savings": self.cost_accumulator["groq"]  # Assuming Groq is cheaper
        }

    def get_worker_states(self) -> Dict[str, Any]:
        """Get enhanced worker data with engine information."""
        return {
            worker_id: {
                **state,
                "engine_type": state.get("engine", "CLAUDE").upper(),
                "model_name": state.get("model", "claude-sonnet-4"),
                "selection_reason": state.get("reason", "Default selection"),
                "engine_color": "claude" if state.get("engine", "claude").lower() == "claude" else "groq"
            }
            for worker_id, state in self.worker_states.items()
        }

    def get_recent_events(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent engine events."""
        return [asdict(event) for event in self.events[-limit:]]

    def _send_to_dashboard(self, event: EngineEvent):
        """Send event to dashboard via HTTP."""
        try:
            payload = {
                "event": asdict(event),
                "distribution": self.get_engine_distribution(),
                "worker_states": self.get_worker_states()
            }

            requests.post(
                f"{self.dashboard_url}/api/engine/update",
                json=payload,
                timeout=1.0
            )
        except Exception as e:
            # Silently fail - dashboard might not be running
            pass

    def _tracking_loop(self):
        """Background loop for periodic updates."""
        while self.running:
            try:
                # Send periodic status update to dashboard
                self._send_status_update()
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                print(f"⚠️ Engine tracker error: {e}")
                time.sleep(10)

    def _send_status_update(self):
        """Send current status to dashboard."""
        try:
            payload = {
                "type": "status_update",
                "distribution": self.get_engine_distribution(),
                "worker_states": self.get_worker_states(),
                "recent_events": self.get_recent_events(10)
            }

            requests.post(
                f"{self.dashboard_url}/api/engine/status",
                json=payload,
                timeout=1.0
            )
        except Exception:
            pass  # Silently fail

    def export_session_report(self, output_path: Path = None) -> Dict[str, Any]:
        """Export comprehensive session report."""
        if output_path is None:
            output_path = Path(f"engine_session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        report = {
            "session_summary": {
                "start_time": self.stats["session_start"].isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_minutes": (datetime.now() - self.stats["session_start"]).total_seconds() / 60,
                "total_requests": self.stats["total_requests"],
                "total_switches": self.stats["total_switches"]
            },
            "cost_breakdown": {
                "total_cost": sum(self.cost_accumulator.values()),
                "claude_cost": self.cost_accumulator["claude"],
                "groq_cost": self.cost_accumulator["groq"],
                "cost_savings": self.cost_accumulator["groq"]
            },
            "engine_distribution": self.get_engine_distribution(),
            "worker_final_states": self.get_worker_states(),
            "event_timeline": [asdict(event) for event in self.events],
            "efficiency_metrics": {
                "avg_cost_per_request": sum(self.cost_accumulator.values()) / max(self.stats["total_requests"], 1),
                "switch_rate": self.stats["total_switches"] / max(self.stats["total_requests"], 1),
                "groq_utilization": (self.stats["groq_requests"] / max(self.stats["total_requests"], 1)) * 100
            }
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 Session report exported: {output_path}")
        return report

# Global tracker instance
_tracker = None

def get_tracker(dashboard_url: str = "http://localhost:8080") -> EngineTracker:
    """Get or create the global engine tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = EngineTracker(dashboard_url)
        _tracker.start_tracking()
    return _tracker

def record_engine_selection(worker_id: str, engine: str, model: str, reason: str, cost: float = 0.0):
    """Convenience function to record engine selection."""
    tracker = get_tracker()
    tracker.record_engine_selection(worker_id, engine, model, reason, cost)

def record_cost_update(worker_id: str, additional_cost: float):
    """Convenience function to record cost update."""
    tracker = get_tracker()
    tracker.record_cost_update(worker_id, additional_cost)

def get_engine_summary() -> Dict[str, Any]:
    """Convenience function to get engine summary."""
    tracker = get_tracker()
    return tracker.get_engine_distribution()

def export_session_report(output_path: Path = None) -> Dict[str, Any]:
    """Convenience function to export session report."""
    tracker = get_tracker()
    return tracker.export_session_report(output_path)

if __name__ == "__main__":
    # Test the engine tracker
    tracker = get_tracker()

    # Simulate some engine selections
    tracker.record_engine_selection("worker_1", "claude", "claude-sonnet-4", "Complex analysis task", 0.05)
    tracker.record_engine_selection("worker_2", "groq", "llama-3.3-70b", "Simple code generation", 0.01)
    tracker.record_engine_selection("worker_1", "groq", "llama-3.3-70b", "Switching for speed", 0.01)

    time.sleep(2)

    # Print summary
    print("\n📊 Engine Distribution:")
    distribution = tracker.get_engine_distribution()
    for key, value in distribution.items():
        print(f"  {key}: {value}")

    print("\n👥 Worker States:")
    for worker_id, state in tracker.get_worker_states().items():
        print(f"  {worker_id}: {state['engine_type']} ({state['model_name']}) - {state['cost_accumulated']:.3f}")

    # Export report
    report = tracker.export_session_report()
    print(f"\n📄 Report exported with {len(report['event_timeline'])} events")