#!/usr/bin/env python3
"""
Fix grind spawner auto-discovery - it's too aggressive

PROBLEM:
Spawner auto-discovers ALL grind_tasks_*.json files and tries to run 1000+ tasks at once.
User specified ONE task file, but it loaded 1,017 tasks and burned $0.17 on random shit.

SOLUTION:
Make it smarter - only load tasks from explicitly specified file, not every file it finds.
"""
import os
from pathlib import Path

from groq_client import execute_with_groq

if not os.environ.get("GROQ_API_KEY"):
    raise SystemExit("Set GROQ_API_KEY in environment before running fix_spawner_autodiscovery.py")

REPO_ROOT = Path(__file__).resolve().parent.parent

# Read canonical legacy spawner code
spawner_code = (REPO_ROOT / "legacy_swarm_gen" / "grind_spawner_unified.py").read_text(
    encoding="utf-8"
)

prompt = f"""Fix dangerous auto-discovery in grind spawner.

## PROBLEM:
The spawner has auto-discovery that loads EVERY grind_tasks_*.json file it finds.
User runs: `python grind_spawner_unified.py --tasks-file grind_tasks_dashboard.json`
Spawner: "Cool, let me load ALL 20 task files and run 1,017 tasks!"
Result: Burns through budget on random tasks, not the one specified.

## CURRENT BEHAVIOR (from code):
```python
{spawner_code[spawner_code.find('[ITERATION 2]'):spawner_code.find('[ITERATION 2]')+500] if '[ITERATION 2]' in spawner_code else 'Auto-discovery happens somewhere in the code'}
```

## WHAT IT SHOULD DO:
1. If --tasks-file is specified, ONLY load that file
2. Don't scan for other task files automatically
3. Add a --auto-discover flag if user wants to load all tasks
4. Default behavior: load ONLY what's explicitly specified

## YOUR TASK:
Provide the code fix for grind_spawner_unified.py that:
- Disables auto-discovery by default
- Respects --tasks-file as the ONLY source
- Adds optional --auto-discover flag for when user wants everything

Show exactly what to change and where.
Make it safe and predictable, not stupid and dangerous.
"""

print("Asking swarm to fix its own auto-discovery...")
result = execute_with_groq(prompt=prompt, model="llama-3.3-70b-versatile")

print("\n" + "="*60)
print("SWARM'S FIX FOR ITS OWN SPAWNER:")
print("="*60)
print(result['result'])
print()
print(f"Cost: ${result['cost']:.4f}")

report_path = REPO_ROOT / "spawner_autodiscovery_fix.md"
report_path.write_text(
    "# Spawner Auto-Discovery Fix\n\n"
    "## Problem\n"
    "Auto-discovery loads ALL task files, not just the specified one.\n\n"
    "## Solution\n"
    f"{result['result']}",
    encoding="utf-8",
)

print("\nSaved to: spawner_autodiscovery_fix.md")
