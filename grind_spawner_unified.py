"""
Unified Grind Spawner - Works with both Claude Code and Groq.

Automatically selects engine based on:
1. Explicit user command ("use groq", "use claude")
2. Task complexity analysis
3. Budget constraints
4. Environment configuration

Usage:
    # Auto-detect engine
    python grind_spawner_unified.py --delegate --budget 1.00

    # Force specific engine
    python grind_spawner_unified.py --delegate --engine claude --budget 1.00
    python grind_spawner_unified.py --delegate --engine groq --budget 0.50

    # Or set via environment
    INFERENCE_ENGINE=groq python grind_spawner_unified.py --delegate
"""

import argparse
import json
import sys
import time
import re
import os
import signal
import atexit
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# Checkpoint file for resume capability
CHECKPOINT_FILE = Path(__file__).parent / "swarm_checkpoint.json"

# Import unified inference engine
from inference_engine import (
    get_engine,
    EngineType,
    InferenceEngine,
    InferenceResult
)

# Import safety modules
from safety_sandbox import initialize_sandbox
from safety_gateway import SafetyGateway
from safety_sanitize import sanitize_task, detect_injection_attempt
from safety_killswitch import get_kill_switch, get_circuit_breaker
from safety_constitutional import ConstitutionalChecker

# Import experiment sandbox
from experiments_sandbox import (
    ExperimentSandbox,
    create_experiment,
    is_core_protected
)

# Import core modules
from roles import decompose_task
from knowledge_graph import KnowledgeGraph
from utils import read_json, write_json
from groq_code_extractor import GroqArtifactExtractor
from surgical_edit_extractor import SurgicalEditExtractor, get_surgical_prompt_instructions

# Optional: Together AI for verification (critic node)
try:
    from together_client import TogetherInferenceEngine
    TOGETHER_AVAILABLE = True
except ImportError:
    TOGETHER_AVAILABLE = False

# Configuration
WORKSPACE = Path(os.environ.get("WORKSPACE", Path(__file__).parent))
LOGS_DIR = WORKSPACE / "grind_logs"
TASKS_FILE = WORKSPACE / "grind_tasks.json"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)


class EngineSelector:
    """
    Intelligently selects inference engine based on task characteristics.

    Selection criteria:
    1. Explicit override ("use groq", "use claude" in task)
    2. Task complexity (complex -> Claude, simple -> Groq)
    3. Budget constraints (low budget -> Groq)
    4. Security sensitivity (high -> Claude for better reasoning)
    """

    # Patterns that indicate explicit engine preference
    GROQ_PATTERNS = [
        r'\buse\s+groq\b',
        r'\bvia\s+groq\b',
        r'\bgroq\s+mode\b',
        r'\bfast\s+mode\b',
        r'\bcheap\s+mode\b',
    ]

    CLAUDE_PATTERNS = [
        r'\buse\s+claude\b',
        r'\bvia\s+claude\b',
        r'\bclaude\s+mode\b',
        r'\bsmart\s+mode\b',
        r'\bcareful\s+mode\b',
    ]

    # Patterns indicating task needs Claude's intelligence
    COMPLEX_PATTERNS = [
        r'\barchitect\b',
        r'\bdesign\b.*\bsystem\b',
        r'\bsecurity\b',
        r'\brefactor\b',
        r'\boptimize\b',
        r'\banalyze\b',
        r'\breview\b',
        r'\baudit\b',
        r'\bmulti-?step\b',
        r'\bcomplex\b',
    ]

    # Patterns indicating simple tasks suitable for Groq
    SIMPLE_PATTERNS = [
        r'\bsimple\b',
        r'\bquick\b',
        r'\bstraightforward\b',
        r'\bjust\s+create\b',
        r'\bjust\s+add\b',
        r'\bbasic\b',
    ]

    def __init__(self, default_engine: EngineType = EngineType.AUTO):
        self.default_engine = default_engine

    def detect_explicit_preference(self, task_text: str) -> Optional[EngineType]:
        """Check if task explicitly requests an engine."""
        task_lower = task_text.lower()

        for pattern in self.GROQ_PATTERNS:
            if re.search(pattern, task_lower):
                return EngineType.GROQ

        for pattern in self.CLAUDE_PATTERNS:
            if re.search(pattern, task_lower):
                return EngineType.CLAUDE

        return None

    def analyze_complexity(self, task_text: str) -> float:
        """
        Analyze task complexity. Returns 0.0-1.0.
        Higher = more complex = prefer Claude.
        """
        score = 0.5  # Neutral default

        # Check for complexity indicators
        for pattern in self.COMPLEX_PATTERNS:
            if re.search(pattern, task_text, re.IGNORECASE):
                score += 0.1

        for pattern in self.SIMPLE_PATTERNS:
            if re.search(pattern, task_text, re.IGNORECASE):
                score -= 0.1

        # Length is a rough proxy for complexity
        word_count = len(task_text.split())
        if word_count > 200:
            score += 0.1
        elif word_count < 50:
            score -= 0.1

        # Clamp to [0, 1]
        return max(0.0, min(1.0, score))

    def select_engine(
        self,
        task_text: str,
        budget: float,
        force_engine: Optional[EngineType] = None
    ) -> Tuple[EngineType, str]:
        """
        Select appropriate engine for task.

        Returns:
            Tuple of (engine_type, reason)
        """
        # 1. Forced override
        if force_engine and force_engine != EngineType.AUTO:
            return force_engine, f"Forced to {force_engine.value}"

        # 2. Explicit preference in task
        explicit = self.detect_explicit_preference(task_text)
        if explicit:
            return explicit, f"Task explicitly requested {explicit.value}"

        # 3. Analyze complexity
        complexity = self.analyze_complexity(task_text)

        # 4. Budget consideration (if very low, prefer Groq)
        if budget < 0.10:
            return EngineType.GROQ, f"Low budget (${budget:.2f}) -> Groq for cost efficiency"

        # 5. Complexity-based selection
        if complexity > 0.6:
            return EngineType.CLAUDE, f"Complex task (score={complexity:.2f}) -> Claude for reliability"
        elif complexity < 0.4:
            return EngineType.GROQ, f"Simple task (score={complexity:.2f}) -> Groq for speed"

        # 6. Default based on environment
        env_engine = os.environ.get("INFERENCE_ENGINE", "").lower()
        if env_engine == "groq":
            return EngineType.GROQ, "Default from INFERENCE_ENGINE=groq"
        elif env_engine == "claude":
            return EngineType.CLAUDE, "Default from INFERENCE_ENGINE=claude"

        # 7. Final default: Claude (more reliable)
        return EngineType.CLAUDE, "Default: Claude for reliability"


class UnifiedGrindSession:
    """
    Unified grind session that works with any inference engine.
    """

    def __init__(
        self,
        session_id: int,
        task: str,
        budget: float,
        workspace: Path,
        force_engine: Optional[EngineType] = None,
        max_total_cost: float = None
    ):
        self.session_id = session_id
        self.budget = budget
        self.workspace = workspace
        self.max_total_cost = max_total_cost
        self.runs = 0
        self.total_cost = 0.0
        self.running = True

        # Sanitize task
        task_dict = {"task": task}
        try:
            sanitized = sanitize_task(task_dict)
            self.task = sanitized["task"]
        except ValueError as e:
            print(f"[Session {session_id}] ERROR: Invalid task: {e}")
            raise

        # Select engine (logged to file, not console)
        self.selector = EngineSelector()
        engine_type, reason = self.selector.select_engine(self.task, budget, force_engine)
        # Verbose logging goes to file only
        self._engine_reason = reason

        self.engine = get_engine(engine_type)
        self.engine_type = engine_type

        # Initialize sandbox and safety
        self.sandbox = ExperimentSandbox()
        self.experiment_id = create_experiment(
            name=f"unified_session_{session_id}",
            description=f"Unified session {session_id}: {task[:100]}"
        )
        self.safety_gateway = SafetyGateway(workspace=self.workspace)

        # Code extractors for file output
        self.code_extractor = GroqArtifactExtractor(workspace_root=str(self.workspace))
        self.surgical_extractor = SurgicalEditExtractor(workspace_root=str(self.workspace))

        # Critic node for verification (uses Together AI if available)
        self.verifier = None
        if TOGETHER_AVAILABLE and os.environ.get("TOGETHER_API_KEY"):
            try:
                self.verifier = TogetherInferenceEngine()
            except Exception:
                pass  # Verification optional

        # Task analysis
        self.task_decomposition = decompose_task(self.task)
        self.complexity_score = self.task_decomposition.get("complexity_score", 0.0)

    def get_prompt(self) -> str:
        """Generate execution prompt - surgical edits for mods, full files for new."""
        experiment_workspace = self.workspace / "experiments" / self.experiment_id

        # Detect if this is a modification task vs new file creation
        is_modification = any(keyword in self.task.upper() for keyword in [
            'FIX', 'UPDATE', 'MODIFY', 'REFACTOR', 'EDIT', 'CHANGE', 'WIRE',
            'IMPROVE', 'REPAIR', 'CORRECT', 'PATCH', 'ADJUST'
        ])

        if is_modification:
            # Use surgical edit format for modifications
            surgical_instructions = get_surgical_prompt_instructions()
            prompt = f"""You are an EXECUTION worker. MODIFY code surgically.

WORKSPACE: {self.workspace}

TASK:
{self.task}

{surgical_instructions}

PROTECTED FILES (NEVER modify):
- grind_spawner*.py, orchestrator.py, roles.py
- safety_*.py, groq_code_extractor.py, surgical_edit_extractor.py

CRITICAL: Output ONLY the specific changes needed, NOT entire files.
Use SEARCH/REPLACE blocks. Be minimal and precise.

EXECUTE NOW."""
        else:
            # Use full file format for new file creation
            prompt = f"""You are an EXECUTION worker. CREATE the requested file(s).

WORKSPACE: {self.workspace}
EXPERIMENT: {self.experiment_id}

TASK:
{self.task}

FILE OUTPUT FORMAT - When creating NEW files:

<artifact type="file" path="relative/path/to/file.ext">
FILE_CONTENT_HERE
</artifact>

RULES:
1. Core system files are READ-ONLY (grind_spawner*.py, safety_*.py)
2. New files go to experiments/{self.experiment_id}/ by default
3. Be FAST - don't over-explain, just create the file

EXECUTE NOW."""

        return prompt

    def run_once(self) -> Dict[str, Any]:
        """Run a single execution cycle."""
        self.runs += 1
        start_time = datetime.now()

        # Safety check
        kill_switch = get_kill_switch()
        if kill_switch.check_halt_flag()["should_stop"]:
            return {"error": "Kill switch activated", "returncode": 1}

        # Pre-execution safety check
        is_safe, safety_report = self.safety_gateway.pre_execute_safety_check(self.task)
        if not is_safe:
            print(f"[Session {self.session_id}] BLOCKED by safety: {safety_report['blocked_reason']}")
            return {"error": safety_report["blocked_reason"], "returncode": 1}

        # Budget handling - Groq has limits, Claude Max is unlimited
        if self.engine_type == EngineType.GROQ:
            within_budget, remaining = self.engine.check_budget(self.budget)
            if not within_budget:
                print(f"[{self.session_id}] Groq budget hit → switching to Claude")
                self.engine = get_engine(EngineType.CLAUDE)
                self.engine_type = EngineType.CLAUDE

        # Build prompt
        prompt = self.get_prompt()

        # Clean, minimal user output - just key decisions
        task_short = self.task.split('\n')[0][:50]
        print(f"[{self.session_id}] START: {task_short}...")

        # Execute with live activity streaming
        result = self.engine.execute(
            prompt=prompt,
            workspace=self.workspace,
            max_tokens=4096,
            timeout=600,
            session_id=self.session_id
        )

        duration = (datetime.now() - start_time).total_seconds()

        # Extract and apply changes - try surgical edits first (more efficient)
        saved_files = []
        if result.success and result.output:
            try:
                # First, try surgical edits (preferred for modifications)
                edit_results = self.surgical_extractor.extract_and_apply(result.output)
                if edit_results:
                    successes = [r for r in edit_results if r.success]
                    if successes:
                        edited_files = [r.path.split('/')[-1] for r in successes]
                        print(f"[{self.session_id}] EDITED: {', '.join(edited_files)}")
                        saved_files = [r.path for r in successes]

                # Fall back to full file extraction if no surgical edits
                if not edit_results:
                    saved_files = self.code_extractor.extract_and_save(result.output)
                    if saved_files:
                        print(f"[{self.session_id}] CREATED: {', '.join([f.split('/')[-1] for f in saved_files])}")
            except Exception:
                pass  # Logged to file, not console

        # Update cost tracking
        self.total_cost += result.cost_usd

        # CRITIC NODE: Verify output before marking complete
        verification = {"verdict": "APPROVE", "reason": "No verifier", "cost": 0}
        if self.verifier and result.success and result.output:
            try:
                verification = self.verifier.verify(
                    task=self.task,
                    output=result.output[:2000],
                    files_changed=saved_files
                )
                self.total_cost += verification.get("cost", 0)

                if verification["verdict"] == "REJECT":
                    print(f"[{self.session_id}] REJECTED: {verification['reason'][:50]}")
                elif verification["verdict"] == "MINOR_ISSUES":
                    print(f"[{self.session_id}] MINOR: {verification['reason'][:50]}")
            except Exception:
                pass  # Verification is optional, don't block on failure

        # Log result
        log_data = {
            "session_id": self.session_id,
            "run": self.runs,
            "engine": self.engine_type.value,
            "model": result.model,
            "task": self.task[:500],
            "success": result.success,
            "duration_seconds": duration,
            "cost_usd": result.cost_usd,
            "tokens_input": result.tokens_input,
            "tokens_output": result.tokens_output,
            "files_created": saved_files,
            "error": result.error,
            "verification": verification,
            "timestamp": datetime.now().isoformat()
        }

        log_file = LOGS_DIR / f"unified_session_{self.session_id}_run_{self.runs}.json"
        write_json(log_file, log_data)

        # Determine success based on execution AND verification
        is_success = result.success and verification["verdict"] != "REJECT"

        return {
            "returncode": 0 if is_success else 1,
            "output": result.output,
            "cost": result.cost_usd + verification.get("cost", 0),
            "files": saved_files,
            "error": result.error,
            "verification": verification,
            "duration": duration
        }


def main():
    parser = argparse.ArgumentParser(description="Unified Grind Spawner")
    parser.add_argument("-n", "--sessions", type=int, default=1)
    parser.add_argument("-e", "--engine", choices=["claude", "groq", "auto"], default="auto",
                        help="Force specific engine (default: auto-select)")
    parser.add_argument("-b", "--budget", type=float, default=1.00)
    parser.add_argument("-w", "--workspace", default=str(WORKSPACE))
    parser.add_argument("-t", "--task", help="Single task to run")
    parser.add_argument("--delegate", action="store_true", help="Read tasks from grind_tasks.json")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--fresh", action="store_true", help="Ignore checkpoint, start fresh")
    parser.add_argument("--max-total-cost", type=float, help="Maximum total cost across all sessions")

    args = parser.parse_args()

    # Map engine argument to EngineType
    engine_map = {
        "claude": EngineType.CLAUDE,
        "groq": EngineType.GROQ,
        "auto": EngineType.AUTO
    }
    force_engine = engine_map.get(args.engine, EngineType.AUTO)

    # Get tasks
    tasks = []

    if args.delegate:
        if not TASKS_FILE.exists():
            print(f"ERROR: --delegate requires {TASKS_FILE}")
            sys.exit(1)

        # Load main tasks file
        tasks_data = read_json(TASKS_FILE)
        for t in tasks_data:
            tasks.append({
                "task": t.get("task", "General improvements"),
                "budget": t.get("budget", args.budget),
            })

        # Auto-discover grind_tasks_*.json files
        for task_file in Path(args.workspace).glob("grind_tasks_*.json"):
            if task_file == TASKS_FILE:
                continue
            try:
                print(f"[AUTODISCOVER] Loading {task_file.name}")
                new_tasks_data = read_json(task_file)
                if isinstance(new_tasks_data, dict) and "tasks" in new_tasks_data:
                    new_tasks_data = new_tasks_data["tasks"]

                for t in new_tasks_data:
                    tasks.append({
                        "task": t.get("task") or t.get("description", ""),
                        "budget": t.get("budget", 0.05),
                    })
            except Exception as e:
                print(f"[AUTODISCOVER] Failed to load {task_file}: {e}")

    elif args.task:
        tasks = [{"task": args.task, "budget": args.budget}]
    else:
        print("ERROR: Specify --task or --delegate")
        sys.exit(1)

    # Validate tasks against Constitutional AI
    checker = ConstitutionalChecker(constraints_path=str(WORKSPACE / "SAFETY_CONSTRAINTS.json"))
    print("[SAFETY] Validating tasks...")

    valid_tasks = []
    for i, task_obj in enumerate(tasks):
        is_safe, violations = checker.check_task_safety(task_obj["task"])
        if is_safe:
            valid_tasks.append(task_obj)
        else:
            print(f"[BLOCKED] Task {i+1}: {violations}")

    if not valid_tasks:
        print("[SAFETY] All tasks blocked. Exiting.")
        sys.exit(1)

    print(f"[SAFETY] {len(valid_tasks)}/{len(tasks)} tasks passed validation.")

    # Check for existing checkpoint (resume capability)
    completed_tasks = set()
    if args.fresh and CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()
        print("[FRESH] Cleared previous checkpoint")
    elif CHECKPOINT_FILE.exists():
        try:
            checkpoint = json.loads(CHECKPOINT_FILE.read_text())
            completed_tasks = set(checkpoint.get("completed", []))
            if completed_tasks:
                print(f"[RESUME] Found checkpoint with {len(completed_tasks)} completed tasks")
        except:
            pass

    # Save checkpoint on exit (Ctrl+C or normal)
    def save_checkpoint():
        checkpoint_data = {
            "completed": list(completed_tasks),
            "timestamp": datetime.now().isoformat(),
            "total_tasks": len(valid_tasks)
        }
        CHECKPOINT_FILE.write_text(json.dumps(checkpoint_data, indent=2))
        print(f"\n[CHECKPOINT] Saved progress: {len(completed_tasks)}/{len(valid_tasks)} tasks")

    atexit.register(save_checkpoint)

    def handle_interrupt(sig, frame):
        print("\n[INTERRUPT] Ctrl+C detected - saving checkpoint...")
        save_checkpoint()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)

    # Group tasks by phase/dependencies
    # Phase 1 (design tasks) can run in parallel
    # Phase 2+ tasks wait for prerequisites
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    # Separate tasks into waves based on phase, EXCLUDING already completed
    waves = {}
    for i, task_obj in enumerate(valid_tasks):
        # Check if already completed BEFORE adding to wave
        task_hash = hashlib.md5(task_obj["task"][:200].encode()).hexdigest()
        if task_hash in completed_tasks:
            continue  # Don't even add to wave
        phase = task_obj.get("phase", 1)
        if phase not in waves:
            waves[phase] = []
        waves[phase].append((i + 1, task_obj))

    # Banner
    remaining = len(valid_tasks) - len(completed_tasks)
    print("=" * 60)
    print("  UNIFIED GRIND SPAWNER")
    print("=" * 60)
    print(f"  Tasks:    {len(valid_tasks)} total, {remaining} remaining")
    print(f"  Engine:   {args.engine} (auto-select per task)")
    print(f"  Waves:    {len(waves)} (parallel within each wave)")
    print("-" * 60)

    # Thread-safe completed_tasks
    completed_lock = threading.Lock()

    def run_task(task_id, task_obj):
        """Run a single task - thread-safe."""
        # Use stable hash (md5) instead of Python's hash() which changes on restart
        task_hash = hashlib.md5(task_obj["task"][:200].encode()).hexdigest()

        with completed_lock:
            if task_hash in completed_tasks:
                print(f"[{task_id}] SKIP (already completed)")
                return None

        try:
            session = UnifiedGrindSession(
                session_id=task_id,
                task=task_obj["task"],
                budget=task_obj["budget"],
                workspace=Path(args.workspace),
                force_engine=force_engine if force_engine != EngineType.AUTO else None,
                max_total_cost=args.max_total_cost
            )

            result = session.run_once()

            if result.get("error"):
                print(f"[{task_id}] FAILED: {result['error'][:60]}")
            else:
                files_count = len(result.get('files', []))
                duration = result.get('duration', 0)
                print(f"[{task_id}] DONE ({duration:.0f}s){f' - {files_count} files' if files_count else ''}")
                with completed_lock:
                    completed_tasks.add(task_hash)

            return result

        except Exception as e:
            print(f"[{task_id}] EXCEPTION: {str(e)[:50]}")
            return {"error": str(e)}

    # Run waves sequentially, tasks within each wave in parallel
    max_parallel = 4  # Max concurrent tasks per wave

    # RECURSIVE LOOP: Keep running until budget exhausted or no new tasks
    max_iterations = 10  # Safety limit to prevent infinite loops
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # Check if we've exhausted budget
        engine = get_engine()
        stats = engine.get_stats()
        if stats.get('total_cost_usd', 0) >= args.budget:
            print(f"\n[BUDGET] Limit reached: ${stats.get('total_cost_usd', 0):.4f} / ${args.budget:.4f}")
            break

        # If no waves to run, check for NEW task files
        if not waves:
            print(f"\n[ITERATION {iteration}] No pending tasks. Scanning for new task files...")

            # Look for new task JSON files in workspace
            new_tasks_found = False
            for task_file in Path(args.workspace).glob("grind_tasks_*.json"):
                if task_file == TASKS_FILE:
                    continue  # Skip the main file

                try:
                    new_tasks_data = read_json(task_file)
                    if isinstance(new_tasks_data, dict) and "tasks" in new_tasks_data:
                        new_tasks_data = new_tasks_data["tasks"]

                    for new_task in new_tasks_data:
                        task_obj = {
                            "task": new_task.get("task") or new_task.get("description", ""),
                            "budget": new_task.get("budget", 0.05),
                        }

                        # Check if not already completed
                        task_hash = hashlib.md5(task_obj["task"][:200].encode()).hexdigest()
                        if task_hash not in completed_tasks:
                            phase = new_task.get("phase", 1)
                            if phase not in waves:
                                waves[phase] = []
                            waves[phase].append((len(valid_tasks) + 1, task_obj))
                            valid_tasks.append(task_obj)
                            new_tasks_found = True
                            print(f"  [+] Loaded: {task_obj['task'][:60]}...")
                except Exception as e:
                    print(f"  [!] Failed to load {task_file}: {e}")

            if not new_tasks_found:
                print("  [✓] No new tasks found. Execution complete.")
                break

        # Execute waves
        for phase in sorted(waves.keys()):
            wave_tasks = waves[phase]
            print(f"\n[WAVE {phase}] Starting {len(wave_tasks)} tasks in parallel...")

            with ThreadPoolExecutor(max_workers=max_parallel) as executor:
                futures = {
                    executor.submit(run_task, task_id, task_obj): task_id
                    for task_id, task_obj in wave_tasks
                }

                for future in as_completed(futures):
                    task_id = futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(f"[{task_id}] THREAD ERROR: {e}")

            print(f"[WAVE {phase}] Complete")

        # Clear waves for next iteration
        waves = {}

        # Check budget again before continuing
        stats = engine.get_stats()
        if stats.get('total_cost_usd', 0) >= args.budget:
            break

    # Final stats
    stats = engine.get_stats()
    print("\n" + "=" * 60)
    print("  FINAL STATS")
    print("=" * 60)
    print(f"  Engine:       {stats.get('engine', 'unknown')}")
    print(f"  Total Cost:   ${stats.get('total_cost_usd', 0):.4f}")
    print(f"  Total Calls:  {stats.get('total_calls', 0)}")
    print(f"  Iterations:   {iteration}")
    print("=" * 60)


if __name__ == "__main__":
    main()
