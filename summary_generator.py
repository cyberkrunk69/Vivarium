#!/usr/bin/env python3
"""
Auto-generate SUMMARY.md from wave_status.json and other data sources.

Usage:
    py summary_generator.py          # Generate SUMMARY.md
    py summary_generator.py --watch  # Watch and regenerate on changes
"""

import json
import time
import argparse
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent
WAVE_STATUS_FILE = WORKSPACE / "wave_status.json"
LESSONS_FILE = WORKSPACE / "learned_lessons.json"
SUMMARY_FILE = WORKSPACE / "SUMMARY.md"


# Roadmap for future waves - update as planning evolves
FUTURE_ROADMAP = {
    12: ("Production Hardening", "Retry logic, rate limits, health checks, security"),
    13: ("Tool Creation", "AI writes new tools for itself"),
    14: ("Meta-Learning", "AI learns how to learn better"),
    15: ("Multi-Task Parallel", "AI works on multiple improvements simultaneously"),
    16: ("Self-Curriculum", "AI designs its own training exercises"),
    17: ("Emergent Behaviors", "AI develops capabilities not explicitly programmed"),
    18: ("External Integration", "Connect to external services and APIs"),
    19: ("Autonomous Debugging", "AI diagnoses and fixes its own bugs"),
    20: ("Full Autonomy", "Self-directed improvement without human prompts"),
}

# Wave results - what each wave accomplished
WAVE_RESULTS = {
    1: ("Analysis", "AI analyzes its own codebase and finds problems to fix.", "Found 8 issues ranked by importance."),
    2: ("Consolidation", "AI cleans up duplicate code and centralizes configuration.", "Eliminated 76 lines of redundant code."),
    3: ("Testing", "5 worker AIs write tests for the codebase in parallel.", "80+ automated tests created."),
    4: ("Research Implementation", "6 worker AIs each implement a different AI research paper.",
        "6 new capabilities: Memory synthesis, Skill library, Role system, Prompt optimizer, Quality gates, Self-reflection."),
    5: ("Deep Research (Opus)", "2 senior AIs read 715MB of AI research papers.", "984 lines of implementation plans."),
    6: ("Advanced Integration", "6 worker AIs implement research recommendations.", "Connected all new capabilities together."),
    7: ("Wire Everything", "Connect all pieces so they actually work together.",
        "Prompt optimizer, skill registry, message pool, self-verification, error categorization, health metrics - all wired up."),
    8: ("Advanced Intelligence", "Add semantic search, code review, tree exploration.",
        "Created critic.py, tree_search.py, knowledge_graph.py, embeddings for skill/lesson retrieval."),
    9: ("Continuous Learning", "Enable AI to learn and improve while working.",
        "Online learning hooks, demonstration injection, feedback loops."),
    10: ("Structural Cleanup", "Split monolithic code, remove dead code.",
         "grind_spawner.py split (1,617 -> 1,073 lines), 5 dead files removed."),
    11: ("Complete Implementations", "Finish all stub implementations from papers.",
         "LATS tree search, KnowledgeGraph integration, DSPy persistence, metrics loop, critic retry, integration tests, /grind endpoint, structured logging, config validation."),
}

CAPABILITIES = [
    ("Memory Synthesis", "Remembers important lessons, forgets trivial ones", "Generative Agents"),
    ("Skill Library", "Saves successful code patterns for reuse", "Voyager"),
    ("Role System", "Different AIs specialize in different jobs", "CAMEL"),
    ("Prompt Optimizer", "Prompts get better from successful examples", "DSPy"),
    ("Quality Gates", "Catches mistakes before they spread", "MetaGPT"),
    ("Self-Reflection", "AI thinks about why things failed", "Reflexion"),
    ("Critic System", "AI reviews its own code quality", "LATS/TextGrad"),
    ("Tree Search", "Explores multiple solutions, picks the best", "LATS"),
    ("Knowledge Graph", "Maps how concepts connect", "HippoRAG"),
    ("Semantic Search", "Finds relevant skills/lessons by meaning", "Voyager/HippoRAG"),
    ("Opus Orchestrator", "Automatically spawns senior AI for strategy", "Custom"),
]


def load_wave_status() -> dict:
    """Load wave status from JSON."""
    if WAVE_STATUS_FILE.exists():
        try:
            return json.loads(WAVE_STATUS_FILE.read_text(encoding='utf-8'))
        except:
            pass
    return {"waves": [], "current_wave": 0, "current_activity": {"title": "Starting...", "workers": []}}


def get_stats() -> dict:
    """Get current stats."""
    logs_dir = WORKSPACE / "grind_logs"
    log_count = len(list(logs_dir.glob("*.json"))) if logs_dir.exists() else 0

    lesson_count = 0
    if LESSONS_FILE.exists():
        try:
            data = json.loads(LESSONS_FILE.read_text(encoding='utf-8'))
            if isinstance(data, dict):
                for value in data.values():
                    if isinstance(value, list):
                        lesson_count += len(value)
            elif isinstance(data, list):
                lesson_count = len(data)
        except:
            pass

    py_files = list(WORKSPACE.glob("*.py")) + list(WORKSPACE.glob("**/*.py"))
    py_count = len(set(py_files))

    total_lines = 0
    for py_file in set(py_files):
        try:
            total_lines += len(py_file.read_text(encoding='utf-8').splitlines())
        except:
            pass

    return {
        "sessions": log_count,
        "lessons": lesson_count,
        "files": py_count,
        "lines": total_lines,
    }


def generate_summary() -> str:
    """Generate SUMMARY.md content from current state."""
    status = load_wave_status()
    stats = get_stats()
    waves = status.get("waves", [])
    current_wave = status.get("current_wave", 0)
    activity = status.get("current_activity", {})

    # Count total workers
    total_workers = sum(w.get("workers", 0) for w in waves if w.get("status") == "done")

    # Calculate total time (rough estimate)
    done_waves = [w for w in waves if w.get("status") == "done"]

    lines = []
    lines.append("# What's Happening in the Basement")
    lines.append("")
    lines.append("## The Short Version")
    lines.append("An AI is teaching itself to become smarter by reading research papers and implementing the techniques. It spawns worker AIs to do the coding while a main AI (Opus) provides strategic oversight every few waves.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## RIGHT NOW")
    lines.append("")

    # Current activity section
    lines.append(f"### {activity.get('title', 'Working...')}")
    workers = activity.get("workers", [])
    if workers:
        for i, w in enumerate(workers, 1):
            task = w.get("task", "")
            wtype = w.get("type", "Worker")
            lines.append(f"{i}. **{wtype}** - {task}")
    lines.append("")

    # Find running wave for results
    running_wave = None
    next_wave = None
    for w in waves:
        if w.get("status") == "running":
            running_wave = w
        elif w.get("status") == "planned" and next_wave is None:
            next_wave = w

    # Show last completed wave results
    completed_waves = [w for w in waves if w.get("status") == "done"]
    if completed_waves:
        last = completed_waves[-1]
        wave_num = last.get("num", 0)
        if wave_num in WAVE_RESULTS:
            name, _, result = WAVE_RESULTS[wave_num]
            lines.append(f"### Wave {wave_num} Results (COMPLETE)")
            lines.append(f"**{last.get('workers', 0)} Worker AIs** completed:")
            lines.append(result)
            lines.append("")

    # Next wave preview
    if next_wave:
        wave_num = next_wave.get("num", 0)
        name = next_wave.get("name", "Unknown")
        desc = FUTURE_ROADMAP.get(wave_num, (name, ""))[1] if wave_num in FUTURE_ROADMAP else ""
        lines.append(f"### Up Next: Wave {wave_num} - {name}")
        if desc:
            lines.append(desc)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Progress So Far")
    lines.append("")

    # Progress for each completed wave
    for wave in completed_waves:
        wave_num = wave.get("num", 0)
        if wave_num in WAVE_RESULTS:
            name, goal, result = WAVE_RESULTS[wave_num]
            lines.append(f"### Wave {wave_num} - {name}")
            lines.append(f"**Goal:** {goal}")
            lines.append(f"**Result:** {result}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## What Capabilities Has It Built?")
    lines.append("")
    lines.append("| Capability | What It Does | Paper Source |")
    lines.append("|------------|--------------|--------------|")
    for cap, desc, source in CAPABILITIES:
        lines.append(f"| {cap} | {desc} | {source} |")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Future roadmap - show waves after current
    max_done = max((w.get("num", 0) for w in completed_waves), default=0)
    future_start = max_done + 1
    future_waves = [(num, name, desc) for num, (name, desc) in FUTURE_ROADMAP.items() if num >= future_start]

    if future_waves:
        lines.append(f"## Future Roadmap (Waves {future_start}-{max(FUTURE_ROADMAP.keys())})")
        lines.append("")
        lines.append("| Wave | Name | What It Does |")
        lines.append("|------|------|--------------|")
        for num, name, desc in sorted(future_waves):
            lines.append(f"| {num} | {name} | {desc} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Live Stats")
    lines.append("")
    lines.append("Watch the numbers tick up at **http://10.0.4.114:8080/dad**")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Sessions | {stats['sessions']} |")
    lines.append(f"| Lessons | {stats['lessons']} |")
    lines.append(f"| Files | {stats['files']} |")
    lines.append(f"| Lines | {stats['lines']:,} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Timeline")
    lines.append("")
    lines.append("| Wave | Workers | Status |")
    lines.append("|------|---------|--------|")

    for wave in waves:
        num = wave.get("num", "?")
        workers = wave.get("workers", 0)
        status_str = wave.get("status", "unknown")

        if status_str == "done":
            status_display = "Done"
        elif status_str == "running":
            status_display = "**NOW**"
        else:
            status_display = "Planned"

        worker_display = f"**{workers}**" if status_str == "running" else str(workers)
        lines.append(f"| Wave {num} | {worker_display} | {status_display} |")

    lines.append("")
    lines.append(f"**Total workers spawned: {total_workers}+**")
    lines.append(f"**Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}**")
    lines.append("")

    return "\n".join(lines)


def update_summary():
    """Generate and write SUMMARY.md."""
    content = generate_summary()
    SUMMARY_FILE.write_text(content, encoding='utf-8')
    print(f"[SUMMARY] Updated SUMMARY.md at {datetime.now().strftime('%H:%M:%S')}")


def watch_and_update():
    """Watch wave_status.json and regenerate on changes."""
    last_mtime = 0
    print("[SUMMARY] Watching for changes to wave_status.json...")

    while True:
        try:
            if WAVE_STATUS_FILE.exists():
                mtime = WAVE_STATUS_FILE.stat().st_mtime
                if mtime != last_mtime:
                    last_mtime = mtime
                    update_summary()
        except Exception as e:
            print(f"[SUMMARY] Error: {e}")

        time.sleep(2)


def main():
    parser = argparse.ArgumentParser(description="Generate SUMMARY.md")
    parser.add_argument("--watch", action="store_true", help="Watch and regenerate on changes")
    args = parser.parse_args()

    if args.watch:
        update_summary()  # Initial generation
        watch_and_update()
    else:
        update_summary()


if __name__ == "__main__":
    main()
