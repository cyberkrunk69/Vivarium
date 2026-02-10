#!/usr/bin/env python3
"""
Opus Orchestrator - Automatic Opus instance management for strategic oversight.

Ensures Opus researchers are utilized optimally by:
1. Spawning Opus every N waves for review/planning
2. Harvesting recommendations from Opus outputs
3. Feeding recommendations into wave task generation
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = REPO_ROOT
STATE_FILE = WORKSPACE / "opus_orchestrator_state.json"
RECOMMENDATIONS_FILE = WORKSPACE / "opus_recommendations.json"


class OpusOrchestrator:
    """Manages automatic Opus spawning and recommendation harvesting."""

    def __init__(self, opus_interval: int = 3):
        """
        Initialize orchestrator.

        Args:
            opus_interval: Spawn Opus every N waves (default: 3)
        """
        self.opus_interval = opus_interval
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load orchestrator state from file."""
        if STATE_FILE.exists():
            try:
                return json.loads(STATE_FILE.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "wave_count": 0,
            "opus_spawns": 0,
            "last_opus_wave": 0,
            "pending_recommendations": [],
            "processed_briefs": []
        }

    def _save_state(self) -> None:
        """Save orchestrator state to file."""
        STATE_FILE.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def increment_wave(self) -> int:
        """Increment wave count and return new count."""
        self.state["wave_count"] += 1
        self._save_state()
        return self.state["wave_count"]

    def should_spawn_opus(self) -> bool:
        """Check if Opus should be spawned based on wave count."""
        waves_since_opus = self.state["wave_count"] - self.state["last_opus_wave"]
        return waves_since_opus >= self.opus_interval

    def spawn_opus_researchers(self, tasks: List[Dict[str, Any]] = None) -> bool:
        """
        Spawn Opus researchers with given or default tasks.

        Args:
            tasks: Optional list of task dicts. If None, uses default research tasks.

        Returns:
            True if spawn initiated, False on error.
        """
        if tasks is None:
            tasks = self._get_default_opus_tasks()

        # Write tasks to file
        opus_tasks_file = WORKSPACE / "opus_research_tasks.json"
        opus_tasks_file.write_text(
            json.dumps(tasks, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

        # Spawn via spawn_opus.py
        try:
            subprocess.Popen(
                [sys.executable, str(WORKSPACE / "spawn_opus.py")],
                cwd=str(WORKSPACE),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.state["opus_spawns"] += 1
            self.state["last_opus_wave"] = self.state["wave_count"]
            self._save_state()
            print(f"[OPUS] Spawned {len(tasks)} Opus researchers (wave {self.state['wave_count']})")
            return True
        except Exception as e:
            print(f"[OPUS] Failed to spawn: {e}")
            return False

    def _get_default_opus_tasks(self) -> List[Dict[str, Any]]:
        """Generate default Opus research tasks based on current state."""
        wave = self.state["wave_count"]

        tasks = [
            {
                "task": f"""ARCHITECTURE REVIEW: Wave {wave} Code Audit

You are a senior architect. Review recent changes in D:\\codingProjects\\swarm_workspace

1. Read all .py files and recent grind_logs/*.json
2. Assess:
   - Code quality of recent wave outputs
   - Integration coherence between modules
   - Technical debt accumulating
   - Missed opportunities for improvement

3. Write audit_report_wave{wave}.md with:
   - Quality scores per module (1-10)
   - Critical issues needing immediate attention
   - Recommendations for next 2-3 waves
   - Specific tasks to add to grind_tasks.json

Be specific and actionable - your output drives the next wave.""",
                "budget": 5.00,
                "model": "opus"
            },
            {
                "task": f"""STRATEGY: Wave {wave + 1}-{wave + 5} Planning

You are a strategic planner. Based on current codebase state:

1. Read PROGRESS.md, SUMMARY.md, learned_lessons.json
2. Analyze what's been built and what's missing
3. Identify the highest-impact improvements for next 5 waves

Write strategy_wave{wave}.md with:
- Assessment of current capabilities
- Gap analysis: what's missing?
- Prioritized roadmap for waves {wave + 1}-{wave + 5}
- Specific task definitions ready to copy to grind_tasks.json

Focus on compound improvements - what enables other improvements?""",
                "budget": 5.00,
                "model": "opus"
            }
        ]

        return tasks

    def harvest_recommendations(self) -> List[Dict[str, Any]]:
        """
        Harvest recommendations from Opus output files.

        Scans for:
        - research_brief_*.md
        - audit_report*.md
        - strategy_*.md

        Returns:
            List of recommendation dicts with action items.
        """
        recommendations = []
        patterns = [
            "research_brief_*.md",
            "audit_report*.md",
            "strategy_*.md"
        ]

        for pattern in patterns:
            for file_path in WORKSPACE.glob(pattern):
                if str(file_path) in self.state["processed_briefs"]:
                    continue

                try:
                    content = file_path.read_text(encoding='utf-8')
                    recs = self._extract_recommendations(content, file_path.name)
                    recommendations.extend(recs)
                    self.state["processed_briefs"].append(str(file_path))
                except Exception as e:
                    print(f"[OPUS] Error reading {file_path}: {e}")

        if recommendations:
            self.state["pending_recommendations"].extend(recommendations)
            self._save_state()

            # Also save to recommendations file
            RECOMMENDATIONS_FILE.write_text(
                json.dumps(recommendations, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print(f"[OPUS] Harvested {len(recommendations)} recommendations")

        return recommendations

    def _extract_recommendations(self, content: str, source: str) -> List[Dict[str, Any]]:
        """Extract actionable recommendations from markdown content."""
        recommendations = []

        # Look for task definitions (numbered lists, bullet points with action verbs)
        action_patterns = [
            r'^\d+\.\s+\*\*([^*]+)\*\*:?\s*(.+)$',  # 1. **Task**: description
            r'^[-*]\s+(?:TODO|TASK|ACTION|IMPLEMENT|ADD|CREATE|FIX):\s*(.+)$',  # - TODO: ...
            r'^###\s+(?:Task|Recommendation):\s*(.+)$',  # ### Task: ...
        ]

        for line in content.split('\n'):
            line = line.strip()
            for pattern in action_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    recommendations.append({
                        "source": source,
                        "type": "task",
                        "description": match.group(1) if match.lastindex >= 1 else line,
                        "details": match.group(2) if match.lastindex >= 2 else "",
                        "timestamp": datetime.now().isoformat()
                    })
                    break

        # Look for quality issues (warnings, criticals)
        issue_patterns = [
            r'(?:CRITICAL|WARNING|ISSUE):\s*(.+)',
            r'Quality Score:\s*(\d+)/10\s*-\s*(.+)',
        ]

        for pattern in issue_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    desc = f"Score {match[0]}/10: {match[1]}" if len(match) > 1 else match[0]
                else:
                    desc = match
                recommendations.append({
                    "source": source,
                    "type": "issue",
                    "description": desc,
                    "timestamp": datetime.now().isoformat()
                })

        return recommendations

    def get_pending_recommendations(self) -> List[Dict[str, Any]]:
        """Get pending recommendations that haven't been actioned."""
        return self.state.get("pending_recommendations", [])

    def clear_processed_recommendations(self) -> None:
        """Clear processed recommendations after they've been actioned."""
        self.state["pending_recommendations"] = []
        self._save_state()

    def get_status(self) -> Dict[str, Any]:
        """Get current orchestrator status."""
        return {
            "wave_count": self.state["wave_count"],
            "opus_spawns": self.state["opus_spawns"],
            "last_opus_wave": self.state["last_opus_wave"],
            "waves_until_opus": max(0, self.opus_interval - (self.state["wave_count"] - self.state["last_opus_wave"])),
            "pending_recommendations": len(self.state.get("pending_recommendations", [])),
            "processed_briefs": len(self.state.get("processed_briefs", []))
        }


def maybe_spawn_opus_after_wave(wave_number: int = None) -> bool:
    """
    Convenience function to check and spawn Opus after a wave completes.
    Call this from grind_spawner after each wave.

    Args:
        wave_number: Optional wave number to set. If None, increments automatically.

    Returns:
        True if Opus was spawned, False otherwise.
    """
    orchestrator = OpusOrchestrator()

    if wave_number is not None:
        orchestrator.state["wave_count"] = wave_number
        orchestrator._save_state()
    else:
        orchestrator.increment_wave()

    # Harvest any pending recommendations first
    orchestrator.harvest_recommendations()

    # Check if we should spawn Opus
    if orchestrator.should_spawn_opus():
        return orchestrator.spawn_opus_researchers()

    return False


def main():
    """CLI interface for Opus orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description="Opus Orchestrator")
    parser.add_argument("--status", action="store_true", help="Show orchestrator status")
    parser.add_argument("--spawn", action="store_true", help="Force spawn Opus researchers")
    parser.add_argument("--harvest", action="store_true", help="Harvest recommendations from Opus outputs")
    parser.add_argument("--wave", type=int, help="Set current wave number")
    parser.add_argument("--interval", type=int, default=3, help="Waves between Opus spawns (default: 3)")

    args = parser.parse_args()

    orchestrator = OpusOrchestrator(opus_interval=args.interval)

    if args.wave:
        orchestrator.state["wave_count"] = args.wave
        orchestrator._save_state()
        print(f"[OPUS] Set wave count to {args.wave}")

    if args.status:
        status = orchestrator.get_status()
        print("\n[OPUS ORCHESTRATOR STATUS]")
        print(f"  Wave count: {status['wave_count']}")
        print(f"  Opus spawns: {status['opus_spawns']}")
        print(f"  Last Opus at wave: {status['last_opus_wave']}")
        print(f"  Waves until next Opus: {status['waves_until_opus']}")
        print(f"  Pending recommendations: {status['pending_recommendations']}")
        print(f"  Processed briefs: {status['processed_briefs']}")

    if args.harvest:
        recs = orchestrator.harvest_recommendations()
        if recs:
            print(f"\n[OPUS] Found {len(recs)} recommendations:")
            for r in recs[:5]:
                print(f"  - [{r['type']}] {r['description'][:60]}...")
        else:
            print("[OPUS] No new recommendations found")

    if args.spawn:
        orchestrator.spawn_opus_researchers()


if __name__ == "__main__":
    main()
