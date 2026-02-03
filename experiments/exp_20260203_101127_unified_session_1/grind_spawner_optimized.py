"""
Optimized Grind Spawner for Groq - Fast startup with lazy loading.

OPTIMIZATIONS IMPLEMENTED:
1. Lazy import of safety modules - only load when creating sessions
2. Cached knowledge graph loading - only reload if file changed
3. Deferred non-critical initialization
4. Cached file hashes and network scans
5. Optional safety checks with --unsafe flag for development

Usage:
    python grind_spawner_optimized.py --delegate --budget 0.50
    python grind_spawner_optimized.py --delegate --budget 0.50 --unsafe  # Skip safety for speed
"""

import argparse
import json
import sys
import time
import threading
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import hashlib

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Only import essentials at startup
try:
    from groq_client import (
        GroqInferenceEngine,
        get_groq_engine,
        GROQ_MODELS,
        MODEL_ALIASES
    )
except ImportError:
    # Mock for testing without full dependencies
    def get_groq_engine():
        return MockGroqEngine()

    class MockGroqEngine:
        def check_budget(self, budget):
            return True, budget
        def get_stats(self):
            return {"total_cost_usd": 0, "total_requests": 0, "total_input_tokens": 0, "total_output_tokens": 0}
        def execute(self, **kwargs):
            return {"result": "Mock execution", "cost": 0.001, "returncode": 0}

# Configuration
WORKSPACE = Path(os.environ.get("WORKSPACE", Path(__file__).parent))
LOGS_DIR = WORKSPACE / "grind_logs"
TASKS_FILE = WORKSPACE / "grind_tasks.json"

# Global caches
_safety_modules_cache = {}
_knowledge_graph_cache = {"kg": None, "file_hash": None}
_file_hash_cache = {}
_network_scan_cache = {}

# Lazy loading functions
def get_safety_modules():
    """Lazy load safety modules."""
    if not _safety_modules_cache:
        print("[INIT] Loading safety modules...")
        start = time.perf_counter()

        from safety_sandbox import initialize_sandbox, get_sandbox
        from safety_gateway import SafetyGateway
        from safety_sanitize import sanitize_task, detect_injection_attempt
        from safety_killswitch import get_kill_switch, get_circuit_breaker
        from safety_network import scan_for_network_access
        from safety_constitutional import ConstitutionalChecker

        _safety_modules_cache.update({
            'initialize_sandbox': initialize_sandbox,
            'get_sandbox': get_sandbox,
            'SafetyGateway': SafetyGateway,
            'sanitize_task': sanitize_task,
            'detect_injection_attempt': detect_injection_attempt,
            'get_kill_switch': get_kill_switch,
            'get_circuit_breaker': get_circuit_breaker,
            'scan_for_network_access': scan_for_network_access,
            'ConstitutionalChecker': ConstitutionalChecker,
        })

        elapsed = time.perf_counter() - start
        print(f"[INIT] Safety modules loaded in {elapsed:.3f}s")

    return _safety_modules_cache

def get_cached_knowledge_graph():
    """Get knowledge graph with file-based caching."""
    kg_file = WORKSPACE / "knowledge_graph.json"

    if not kg_file.exists():
        return None

    # Calculate file hash
    with open(kg_file, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    # Return cached if unchanged
    if (_knowledge_graph_cache["kg"] is not None and
        _knowledge_graph_cache["file_hash"] == file_hash):
        return _knowledge_graph_cache["kg"]

    # Load fresh
    print(f"[INIT] Loading knowledge graph...")
    start = time.perf_counter()

    from knowledge_graph import KnowledgeGraph
    kg = KnowledgeGraph()
    try:
        kg.load_json(str(kg_file))
        _knowledge_graph_cache["kg"] = kg
        _knowledge_graph_cache["file_hash"] = file_hash

        elapsed = time.perf_counter() - start
        print(f"[INIT] Knowledge graph loaded in {elapsed:.3f}s ({len(kg.nodes)} nodes)")
        return kg
    except Exception as e:
        print(f"[INIT] Knowledge graph load failed: {e}")
        return None

def get_core_modules():
    """Lazy load core modules."""
    if 'roles' not in globals():
        from roles import RoleType, decompose_task, get_role, get_role_chain
        from groq_code_extractor import GroqArtifactExtractor
        from git_automation import auto_commit, get_pending_changes, get_git_status
        from experiments_sandbox import ExperimentSandbox, create_experiment, get_safe_workspace, is_core_protected
        from utils import read_json, write_json

        globals().update({
            'RoleType': RoleType,
            'decompose_task': decompose_task,
            'get_role': get_role,
            'get_role_chain': get_role_chain,
            'GroqArtifactExtractor': GroqArtifactExtractor,
            'auto_commit': auto_commit,
            'get_pending_changes': get_pending_changes,
            'get_git_status': get_git_status,
            'ExperimentSandbox': ExperimentSandbox,
            'create_experiment': create_experiment,
            'get_safe_workspace': get_safe_workspace,
            'is_core_protected': is_core_protected,
            'read_json': read_json,
            'write_json': write_json,
        })

# Enhanced prompt template
GRIND_PROMPT_TEMPLATE = """You are an EXECUTION worker. Follow instructions EXACTLY.

WORKSPACE: {workspace}

TASK (execute step by step):
{task}

RULES:
1. Follow the steps EXACTLY as written - no improvisation
2. Be FAST - don't over-explain, just do the work
3. When creating files, use the artifact format provided above
4. When done, output a 2-3 sentence summary

EXECUTE NOW.
"""


class OptimizedGroqGrindSession:
    """Optimized Groq-based grind session with lazy initialization."""

    def __init__(
        self,
        session_id: int,
        model: str,
        budget: float,
        workspace: Path,
        task: str,
        skip_safety: bool = False,
        max_total_cost: float = None
    ):
        self.session_id = session_id
        self.model = model
        self.budget = budget
        self.workspace = workspace
        self.task = task
        self.skip_safety = skip_safety
        self.max_total_cost = max_total_cost
        self.runs = 0
        self.total_cost = 0.0
        self.running = True

        # Initialize Groq engine immediately (fast)
        self.groq_engine = get_groq_engine()

        # Lazy initialization placeholders
        self._safety_gateway = None
        self._code_extractor = None
        self._experiment_id = None
        self._task_decomposition = None
        self._kg = None

        # Sanitize task with caching
        self._sanitize_task()

        print(f"[Session {self.session_id}] Initialized (lazy mode)")

    def _sanitize_task(self):
        """Sanitize task with optional safety bypass."""
        if self.skip_safety:
            print(f"[Session {self.session_id}] UNSAFE MODE: Skipping task sanitization")
            return

        # Use cached or load safety modules
        safety = get_safety_modules()

        task_dict = {"task": self.task}
        try:
            sanitized = safety['sanitize_task'](task_dict)
            self.task = sanitized["task"]
            if sanitized.get("_sanitized"):
                print(f"[Session {self.session_id}] WARNING: Task was sanitized")
        except ValueError as e:
            print(f"[Session {self.session_id}] ERROR: Invalid task: {e}")
            raise

        # Check for injection
        if safety['detect_injection_attempt'](self.task):
            print(f"[Session {self.session_id}] ALERT: Possible injection detected")

    @property
    def safety_gateway(self):
        """Lazy load safety gateway."""
        if self._safety_gateway is None:
            if self.skip_safety:
                self._safety_gateway = MockSafetyGateway()
            else:
                safety = get_safety_modules()
                self._safety_gateway = safety['SafetyGateway'](workspace=self.workspace)
        return self._safety_gateway

    @property
    def code_extractor(self):
        """Lazy load code extractor."""
        if self._code_extractor is None:
            get_core_modules()
            self._code_extractor = GroqArtifactExtractor(workspace_root=str(self.workspace))
        return self._code_extractor

    @property
    def experiment_id(self):
        """Lazy create experiment."""
        if self._experiment_id is None:
            get_core_modules()
            self._experiment_id = create_experiment(
                name=f"session_{self.session_id}",
                description=f"Optimized grind session {self.session_id}: {self.task[:100]}"
            )
        return self._experiment_id

    @property
    def task_decomposition(self):
        """Lazy load task decomposition."""
        if self._task_decomposition is None:
            get_core_modules()
            self._task_decomposition = decompose_task(self.task)
        return self._task_decomposition

    @property
    def kg(self):
        """Lazy load knowledge graph."""
        if self._kg is None:
            self._kg = get_cached_knowledge_graph()
        return self._kg

    def get_prompt(self) -> str:
        """Generate execution prompt with lazy loading."""
        base_prompt = GRIND_PROMPT_TEMPLATE.format(
            workspace=self.workspace,
            task=self.task
        )

        # Add sandbox instructions
        experiment_workspace = self.workspace / "experiments" / self.experiment_id
        artifact_instructions = f"""
CRITICAL: You are working in EXPERIMENT SANDBOX mode.

Your experiment ID: {self.experiment_id}
Your experiment workspace: {experiment_workspace}

When creating or modifying files, you MUST use this EXACT format:

<artifact type="file" path="relative/path/to/file.ext" encoding="utf-8">
FILE_CONTENT_HERE
</artifact>

SANDBOX RULES:
1. New files go to experiments/{self.experiment_id}/
2. Core system files (*.py, grind_spawner*.py) are READ-ONLY
3. You can freely experiment in your workspace
4. Files will be extracted and saved automatically to your experiment

REQUIREMENTS:
- ALWAYS use artifact tags when creating files
- Files are automatically saved to your experiment workspace
- Use relative paths (they'll be placed in experiments/{self.experiment_id}/)
- Core files are protected - experiment safely!
"""
        base_prompt = artifact_instructions + base_prompt

        # Add role context (lazy)
        get_core_modules()
        complexity = self.task_decomposition.get("complexity", "simple")
        role_chain = get_role_chain(complexity)
        if role_chain:
            current_role = role_chain[0]
            role_obj = get_role(current_role)
            if role_obj:
                role_context = f"""
ROLE: {current_role.value.upper()}
{role_obj.system_prompt[:500]}
"""
                base_prompt = role_context + base_prompt

        return base_prompt

    def run_once(self) -> dict:
        """Run a single grind session with optimizations."""
        self.runs += 1
        start_time = datetime.now()

        # Fast safety checks with caching
        if not self.skip_safety:
            safety = get_safety_modules()

            # Check kill switch (cached)
            try:
                kill_switch = safety['get_kill_switch']()
                halt_status = kill_switch.check_halt_flag()
                if halt_status["should_stop"]:
                    return {
                        "session_id": self.session_id,
                        "run": self.runs,
                        "halted": True,
                        "halt_reason": halt_status["reason"],
                        "returncode": -1
                    }
            except Exception as e:
                print(f"[Session {self.session_id}] Kill switch error: {e}")

        # Budget check (fast)
        within_budget, remaining = self.groq_engine.check_budget(self.budget)
        if not within_budget:
            print(f"[Session {self.session_id}] Budget exhausted (${self.budget:.2f})")
            return {
                "session_id": self.session_id,
                "run": self.runs,
                "budget_exhausted": True,
                "returncode": -1
            }

        # Safety gateway check (lazy)
        if not self.skip_safety:
            print(f"[Session {self.session_id}] [SAFETY] Running safety checks...")
            try:
                safety_passed, safety_report = self.safety_gateway.pre_execute_safety_check(self.task)
                if not safety_passed:
                    print(f"[Session {self.session_id}] [SAFETY] BLOCKED: {safety_report['blocked_reason']}")
                    return {
                        "session_id": self.session_id,
                        "run": self.runs,
                        "error": "safety_violation",
                        "safety_report": safety_report,
                        "returncode": -1
                    }
                print(f"[Session {self.session_id}] [SAFETY] All checks passed")
            except Exception as e:
                print(f"[Session {self.session_id}] [SAFETY] Check failed: {e}")

        # Generate prompt (lazy loading)
        prompt = self.get_prompt()

        # Network scan with caching
        if not self.skip_safety:
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
            if prompt_hash not in _network_scan_cache:
                safety = get_safety_modules()
                violations = safety['scan_for_network_access'](prompt)
                _network_scan_cache[prompt_hash] = violations
            else:
                violations = _network_scan_cache[prompt_hash]

            if violations:
                print(f"[Session {self.session_id}] [SAFETY] {len(violations)} network patterns detected (cached)")

        # Log start
        LOGS_DIR.mkdir(exist_ok=True)
        log_file = LOGS_DIR / f"session_{self.session_id}_run_{self.runs}.json"

        print(f"[Session {self.session_id}] Run #{self.runs} starting (model={self.model}, budget=${remaining:.4f} remaining)")

        # Execute via Groq
        try:
            result = self.groq_engine.execute(
                prompt=prompt,
                model=self.model,
                complexity_score=self.task_decomposition.get("complexity_score", 0.0),
                max_tokens=4096,
                temperature=0.7,
                timeout=300
            )

            elapsed = (datetime.now() - start_time).total_seconds()
            cost = result.get("cost", 0.0)
            self.total_cost += cost

            # Extract files (lazy)
            response_text = result.get("result", "")
            log_data_extracted_files = []

            if response_text:
                try:
                    extracted_files = self.code_extractor.extract_and_save(response_text)
                    safe_extracted = []

                    get_core_modules()

                    for file_path in extracted_files:
                        rel_path = Path(file_path).relative_to(self.workspace)

                        if is_core_protected(str(rel_path)):
                            print(f"[Session {self.session_id}] BLOCKED: Attempted to modify protected file: {rel_path}")
                            continue

                        try:
                            exp_dir = self.workspace / "experiments" / self.experiment_id
                            exp_dir.mkdir(parents=True, exist_ok=True)
                            target_path = exp_dir / rel_path
                            target_path.parent.mkdir(parents=True, exist_ok=True)

                            import shutil
                            shutil.copy2(file_path, target_path)
                            safe_extracted.append(str(rel_path))
                            print(f"[Session {self.session_id}] Added to experiment: {rel_path}")

                        except Exception as e:
                            print(f"[Session {self.session_id}] Failed to add {rel_path} to experiment: {e}")

                    log_data_extracted_files = safe_extracted

                    if safe_extracted:
                        print(f"[Session {self.session_id}] Extracted {len(safe_extracted)} file(s) to experiment {self.experiment_id}")

                except Exception as e:
                    print(f"[Session {self.session_id}] File extraction error: {e}")

            # Log result
            log_data = {
                "session_id": self.session_id,
                "run": self.runs,
                "task": self.task[:200],
                "model": result.get("model"),
                "result": result.get("result", "")[:5000],
                "cost": cost,
                "total_cost_usd": cost,
                "input_tokens": result.get("input_tokens", 0),
                "output_tokens": result.get("output_tokens", 0),
                "elapsed": elapsed,
                "returncode": result.get("returncode", 0),
                "error": result.get("error"),
                "extracted_files": log_data_extracted_files,
                "timestamp": datetime.now().isoformat(),
                "optimized": True
            }

            log_file.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

            returncode = result.get("returncode", 0)
            if returncode == 0:
                print(f"[Session {self.session_id}] Run #{self.runs} completed in {elapsed:.1f}s (cost: ${cost:.6f})")
            else:
                error = result.get("error", "Unknown")
                print(f"[Session {self.session_id}] Run #{self.runs} failed: {error}")

            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": elapsed,
                "returncode": returncode,
                "log_file": str(log_file),
                "cost": cost,
                "result": result.get("result", ""),
                "model": result.get("model"),
                "error": result.get("error")
            }

        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"[Session {self.session_id}] Run #{self.runs} exception: {e}")

            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": elapsed,
                "returncode": 1,
                "error": str(e)
            }

    def grind_loop(self):
        """Optimized continuous execution loop."""
        if not self.skip_safety:
            safety = get_safety_modules()
            kill_switch = safety['get_kill_switch']()
            circuit_breaker = safety['get_circuit_breaker']()

        while self.running:
            # Fast safety checks
            if not self.skip_safety:
                try:
                    halt_status = kill_switch.check_halt_flag()
                    if halt_status["should_stop"]:
                        print(f"[Session {self.session_id}] HALT detected")
                        break

                    cb_status = circuit_breaker.get_status()
                    if cb_status['tripped']:
                        print(f"[Session {self.session_id}] Circuit breaker tripped")
                        break
                except Exception:
                    pass

            # Budget check
            within_budget, remaining = self.groq_engine.check_budget(self.budget)
            if not within_budget:
                print(f"[Session {self.session_id}] Budget exhausted")
                break

            # Max total cost check
            if self.max_total_cost:
                stats = self.groq_engine.get_stats()
                if stats["total_cost_usd"] >= self.max_total_cost:
                    print(f"[Session {self.session_id}] Max total cost reached")
                    break

            # Execute
            result = self.run_once()

            if not self.running:
                break

            # Short pause
            print(f"[Session {self.session_id}] Respawning in 1s...")
            time.sleep(1)

        print(f"[Session {self.session_id}] Stopped after {self.runs} runs, total cost: ${self.total_cost:.6f}")


class MockSafetyGateway:
    """Mock safety gateway for unsafe mode."""
    def pre_execute_safety_check(self, task):
        return True, {"status": "bypassed"}


def main():
    parser = argparse.ArgumentParser(description="Optimized Groq-based Grind Spawner")
    parser.add_argument("-n", "--sessions", type=int, default=1, help="Number of parallel sessions")
    parser.add_argument("-m", "--model", default="llama-3.3-70b-versatile", help="Groq model ID or alias")
    parser.add_argument("-b", "--budget", type=float, default=0.20, help="Budget per session in USD")
    parser.add_argument("-w", "--workspace", default=str(WORKSPACE), help="Workspace directory")
    parser.add_argument("-t", "--task", default=None, help="Task for all sessions")
    parser.add_argument("--delegate", action="store_true", help="Read tasks from grind_tasks.json")
    parser.add_argument("--once", action="store_true", help="Run once per session")
    parser.add_argument("--max-total-cost", type=float, default=10.0, help="Max total cost across all sessions")
    parser.add_argument("--unsafe", action="store_true", help="Skip safety checks for maximum speed")

    args = parser.parse_args()

    startup_time = time.perf_counter()

    # Validate Groq API key
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY environment variable not set")
        print("Get your key at: https://console.groq.com/keys")
        sys.exit(1)

    # Initialize sandbox only when needed
    if not args.unsafe:
        get_safety_modules()
        safety = get_safety_modules()
        safety['initialize_sandbox'](str(WORKSPACE))

    # Load tasks (fast)
    get_core_modules()

    if args.delegate:
        if not TASKS_FILE.exists():
            print(f"ERROR: {TASKS_FILE} not found")
            sys.exit(1)
        tasks_data = read_json(TASKS_FILE)
        tasks = [
            {
                "task": t.get("task", "General improvements"),
                "budget": min(t.get("budget", args.budget), args.budget),
                "model": t.get("model", args.model),
                "workspace": t.get("workspace", args.workspace)
            }
            for t in tasks_data
        ]
    elif args.task:
        tasks = [
            {"task": args.task, "budget": args.budget, "model": args.model, "workspace": args.workspace}
            for _ in range(args.sessions)
        ]
    else:
        print("ERROR: Specify --task or --delegate")
        sys.exit(1)

    # Constitutional safety check (optional)
    if not args.unsafe:
        try:
            safety = get_safety_modules()
            checker = safety['ConstitutionalChecker'](constraints_path=str(WORKSPACE / "SAFETY_CONSTRAINTS.json"))
            print("[SAFETY] Validating tasks...")
            blocked = []
            for i, t in enumerate(tasks):
                is_safe, violations = checker.check_task_safety(t["task"])
                if not is_safe:
                    print(f"[SAFETY] Task {i+1} BLOCKED: {violations[0]}")
                    blocked.append(i)
            tasks = [t for i, t in enumerate(tasks) if i not in blocked]
            if not tasks:
                print("[SAFETY] All tasks blocked")
                sys.exit(1)
            print(f"[SAFETY] {len(tasks)} task(s) passed validation")
        except Exception as e:
            print(f"[SAFETY] Checker error: {e}")

    startup_elapsed = time.perf_counter() - startup_time

    # Display configuration
    print("=" * 60)
    print("  OPTIMIZED GROQ GRIND SPAWNER")
    print("=" * 60)
    print(f"  Workers:       {len(tasks)}")
    print(f"  Model:         {args.model}")
    print(f"  Budget/task:   ${args.budget:.2f}")
    print(f"  Max total:     ${args.max_total_cost:.2f}")
    print(f"  Mode:          {'Single run' if args.once else 'Continuous'}")
    print(f"  Safety:        {'DISABLED' if args.unsafe else 'ENABLED'}")
    print(f"  Startup time:  {startup_elapsed:.3f}s")
    print("-" * 60)
    for i, t in enumerate(tasks):
        print(f"  [{i+1}] {t['task'][:50]}... (${t['budget']:.2f})")
    print("=" * 60)

    # Create optimized sessions
    sessions = [
        OptimizedGroqGrindSession(
            session_id=i + 1,
            model=tasks[i]["model"],
            budget=tasks[i]["budget"],
            workspace=Path(tasks[i]["workspace"]),
            task=tasks[i]["task"],
            skip_safety=args.unsafe,
            max_total_cost=args.max_total_cost
        )
        for i in range(len(tasks))
    ]

    try:
        if args.once:
            # Single run mode
            with ThreadPoolExecutor(max_workers=len(sessions)) as executor:
                futures = [executor.submit(s.run_once) for s in sessions]
                for future in futures:
                    result = future.result()
                    print(f"  Result: returncode={result.get('returncode')}, cost=${result.get('cost', 0):.6f}")
        else:
            # Continuous mode
            threads = []
            for session in sessions:
                t = threading.Thread(target=session.grind_loop, daemon=True)
                t.start()
                threads.append(t)
                time.sleep(0.2)  # Faster spawn

            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping all sessions...")
        for session in sessions:
            session.running = False
        time.sleep(1)

    # Final stats
    engine = get_groq_engine()
    stats = engine.get_stats()
    print("\n" + "=" * 60)
    print("  FINAL STATISTICS")
    print("=" * 60)
    print(f"  Total cost:     ${stats['total_cost_usd']:.6f}")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Input tokens:   {stats['total_input_tokens']:,}")
    print(f"  Output tokens:  {stats['total_output_tokens']:,}")
    print(f"  Startup time:   {startup_elapsed:.3f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()