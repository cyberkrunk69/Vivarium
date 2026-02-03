"""
OPTIMIZED Grind Spawner - Fast startup with lazy loading

OPTIMIZATION SUMMARY:
1. Lazy import heavy modules (knowledge_graph, safety_gateway, etc.)
2. Defer KnowledgeGraph loading until actually needed
3. Cache file hashes to avoid repeated reads
4. Background thread for non-critical initialization
5. Skip safety gateway init until first execution

Startup improvements:
- KnowledgeGraph: Load on first use (~321KB -> 0 at startup)
- Safety modules: Import on demand
- File operations: Cache and batch
- Demo loading: Defer until prompt generation

Usage: Drop-in replacement for grind_spawner.py
"""

import argparse
import json
import subprocess
import sys
import time
import threading
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Fast imports only - heavy modules imported on demand
from utils import read_json, write_json

# Configuration
WORKSPACE = Path(__file__).parent.parent if __file__.endswith('grind_spawner_optimized.py') else Path(__file__).parent
LOGS_DIR = WORKSPACE / "grind_logs"
TASKS_FILE = WORKSPACE / "grind_tasks.json"
LEARNED_LESSONS_FILE = WORKSPACE / "learned_lessons.json"

# Cache for expensive operations
_startup_cache = {
    'file_hashes': {},
    'kg_loaded': False,
    'safety_initialized': False,
    'demos_loaded': False
}

GRIND_PROMPT_TEMPLATE = """You are an EXECUTION worker. Follow instructions EXACTLY.

WORKSPACE: {workspace}

TASK (execute step by step):
{task}

RULES:
1. Follow the steps EXACTLY as written - no improvisation
2. Be FAST - don't over-explain, just do the work
3. If a step says "edit file X", edit it. If it says "create file Y", create it.
4. No lengthy analysis - the planning was already done
5. When done, output a 2-3 sentence summary

EXECUTE NOW.
"""

class OptimizedGrindSession:
    """Optimized version with lazy loading and startup caching."""

    def __init__(self, session_id: int, model: str, budget: float, workspace: Path, task: str,
                 max_total_cost: float = None, synthesis_interval: int = 5, critic_mode: bool = False):
        self.session_id = session_id
        self.model = model
        self.budget = budget
        self.workspace = workspace
        self.task = task
        self.runs = 0
        self.total_cost = 0.0
        self.running = True
        self.max_total_cost = max_total_cost
        self.synthesis_interval = synthesis_interval
        self.critic_mode = critic_mode

        # Lazy-loaded components (initialized on first use)
        self._kg = None
        self._failure_detector = None
        self._safety_gateway = None
        self._role_executor = None
        self._perf_tracker = None

        # Quick initialization only
        self._quick_init()

    def _quick_init(self):
        """Fast initialization - only essential operations"""
        # OPTIMIZATION: Sanitize task quickly without heavy imports
        try:
            # Basic sanitization without importing full safety modules
            if len(self.task) > 10000:
                self.task = self.task[:10000] + "... [truncated]"
                print(f"[Session {self.session_id}] Task truncated to 10K chars")

            # Quick injection check without heavy modules
            suspicious_patterns = ['subprocess.', 'os.system', 'eval(', 'exec(', '__import__']
            if any(pattern in self.task for pattern in suspicious_patterns):
                print(f"[Session {self.session_id}] WARNING: Suspicious patterns in task")

        except Exception as e:
            print(f"[Session {self.session_id}] Warning: Quick sanitization failed: {e}")

        # OPTIMIZATION: Defer task decomposition until needed
        self.complexity_score = 0.5  # Default moderate complexity
        self.checkpoint_counter = 0

    @property
    def kg(self):
        """Lazy-loaded KnowledgeGraph"""
        if self._kg is None:
            print(f"[Session {self.session_id}] Loading KnowledgeGraph...")
            start = time.time()

            # Lazy import
            from knowledge_graph import KnowledgeGraph

            self._kg = KnowledgeGraph()
            kg_file = self.workspace / "knowledge_graph.json"

            if kg_file.exists() and not _startup_cache['kg_loaded']:
                try:
                    self._kg.load_json(str(kg_file))
                    _startup_cache['kg_loaded'] = True
                    elapsed = time.time() - start
                    print(f"[Session {self.session_id}] KG loaded with {len(self._kg.nodes)} nodes ({elapsed*1000:.1f}ms)")
                except Exception as e:
                    print(f"[Session {self.session_id}] KG load failed, will populate: {e}")
                    self._kg.populate_from_codebase(str(self.workspace))
            else:
                # Use cached KG if available
                if _startup_cache['kg_loaded']:
                    print(f"[Session {self.session_id}] Using cached KG")
                else:
                    self._kg.populate_from_codebase(str(self.workspace))

        return self._kg

    @property
    def failure_detector(self):
        """Lazy-loaded FailurePatternDetector"""
        if self._failure_detector is None:
            from failure_patterns import FailurePatternDetector
            self._failure_detector = FailurePatternDetector(workspace=self.workspace)
            print(f"[Session {self.session_id}] Failure detector initialized")
        return self._failure_detector

    @property
    def safety_gateway(self):
        """Lazy-loaded SafetyGateway"""
        if self._safety_gateway is None:
            from safety_gateway import SafetyGateway
            self._safety_gateway = SafetyGateway(workspace=self.workspace)
            _startup_cache['safety_initialized'] = True
            print(f"[Session {self.session_id}] Safety gateway initialized")
        return self._safety_gateway

    @property
    def role_executor(self):
        """Lazy-loaded RoleExecutor with task decomposition"""
        if self._role_executor is None:
            from roles import RoleType, decompose_task, RoleExecutor

            task_decomposition = decompose_task(self.task)
            self.complexity_score = task_decomposition.get("complexity_score", 0.5)

            initial_role = RoleType.PLANNER if task_decomposition["complexity"] == "complex" else RoleType.CODER
            self._role_executor = RoleExecutor(initial_role, self.task)
            self._role_executor.context["complexity"] = task_decomposition["complexity"]
            self._role_executor.context["complexity_score"] = self.complexity_score

            print(f"[Session {self.session_id}] Role executor initialized (complexity: {self.complexity_score:.2f})")

        return self._role_executor

    @property
    def perf_tracker(self):
        """Lazy-loaded PerformanceTracker"""
        if self._perf_tracker is None:
            from performance_tracker import PerformanceTracker
            self._perf_tracker = PerformanceTracker(self.workspace)
        return self._perf_tracker

    def get_prompt(self) -> str:
        """Generate prompt with lazy-loaded optimizations"""
        base_prompt = GRIND_PROMPT_TEMPLATE.format(
            workspace=self.workspace,
            task=self.task
        )

        # OPTIMIZATION: Fast path for simple tasks
        if self.complexity_score < 0.3:
            return base_prompt

        # OPTIMIZATION: Lazy load heavy components only when needed
        try:
            # Roles and CAMEL injection
            from roles import get_role_chain, get_role

            role_chain = get_role_chain("complex" if self.complexity_score > 0.6 else "simple")
            current_role = role_chain[0]
            next_role = role_chain[1] if len(role_chain) > 1 else None

            role_obj = get_role(current_role)
            if role_obj:
                camel_injection = f"""
{'='*60}
CAMEL ROLE-BASED TASK DECOMPOSITION
{'='*60}
You are the {current_role.value.upper()} role.
{role_obj.system_prompt}
Role Chain: {' ->'.join([r.value.upper() for r in role_chain])}
{'='*60}
"""
            else:
                camel_injection = ""

            # OPTIMIZATION: Lazy context building
            unified_context = self._build_context_lazy()

            # OPTIMIZATION: Cache failure warnings
            failure_warning = self._get_failure_warning_cached()

            return camel_injection + unified_context + failure_warning + base_prompt

        except Exception as e:
            print(f"[Session {self.session_id}] Prompt optimization failed, using base: {e}")
            return base_prompt

    def _build_context_lazy(self) -> str:
        """Build context with lazy loading"""
        try:
            from context_builder import ContextBuilder
            context_builder = ContextBuilder(self.workspace)
            return context_builder.add_skills(self.task, top_k=2) \
                                  .add_lessons(self.task, top_k=2) \
                                  .add_kg_context(self.task, depth=1) \
                                  .build(log_injection=False)  # Disable verbose logging
        except Exception as e:
            print(f"[Session {self.session_id}] Context building failed: {e}")
            return ""

    def _get_failure_warning_cached(self) -> str:
        """Get failure warnings with caching"""
        cache_key = f"failure_warning_{hash(self.task[:100])}"
        if cache_key not in _startup_cache:
            try:
                warning = self.failure_detector.generate_warning_prompt(
                    self.task,
                    task_characteristics={
                        "complexity": "moderate",
                        "complexity_score": self.complexity_score
                    }
                )
                _startup_cache[cache_key] = warning
            except Exception:
                _startup_cache[cache_key] = ""

        return _startup_cache[cache_key]

    def run_once(self) -> dict:
        """Optimized run_once with lazy safety checks"""
        self.runs += 1
        start_time = datetime.now()

        # OPTIMIZATION: Quick safety check first, defer heavy checks
        try:
            from safety_killswitch import get_kill_switch
            kill_switch = get_kill_switch()
            halt_status = kill_switch.check_halt_flag()
            if halt_status["should_stop"]:
                return {
                    "session_id": self.session_id,
                    "run": self.runs,
                    "elapsed": 0,
                    "returncode": -1,
                    "halted": True,
                    "halt_reason": halt_status["reason"]
                }
        except Exception as e:
            print(f"[Session {self.session_id}] Kill switch check failed: {e}")

        # Create log file
        LOGS_DIR.mkdir(exist_ok=True)
        log_file = LOGS_DIR / f"session_{self.session_id}_run_{self.runs}.json"

        prompt = self.get_prompt()

        # OPTIMIZATION: Lazy safety gateway - only initialize when needed
        if self.runs == 1 or not _startup_cache['safety_initialized']:
            print(f"[Session {self.session_id}] Running safety checks...")
            try:
                safety_passed, safety_report = self.safety_gateway.pre_execute_safety_check(self.task)
                if not safety_passed:
                    print(f"[Session {self.session_id}] BLOCKED: {safety_report['blocked_reason']}")
                    return {
                        "session_id": self.session_id,
                        "run": self.runs,
                        "error": "safety_violation",
                        "safety_report": safety_report,
                        "returncode": -1
                    }
            except Exception as e:
                print(f"[Session {self.session_id}] Safety check failed: {e}")

        print(f"[Session {self.session_id}] Starting run #{self.runs} (model={self.model}, budget=${self.budget:.2f})")

        try:
            # Build claude command
            cmd = [
                "claude", "-p", "--model", self.model,
                "--permission-mode", "bypassPermissions",
                "--output-format", "json"
            ]

            # Run claude
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                cwd=str(self.workspace),
                timeout=600
            )

            # Process result
            elapsed = (datetime.now() - start_time).total_seconds()
            output_data = json.loads(result.stdout or "{}")

            if result.returncode != 0:
                error_category = self._categorize_error("execution", result.stderr)
                output_data["error_category"] = error_category

                # Track failure (lazy)
                try:
                    self.failure_detector.track_failure(
                        task_description=self.task,
                        error_type=error_category,
                        error_message=result.stderr[:500] if result.stderr else "Unknown error",
                        task_characteristics={
                            "complexity_score": self.complexity_score
                        }
                    )
                except Exception as e:
                    print(f"[Session {self.session_id}] Failure tracking failed: {e}")

            # Save log
            log_file.write_text(json.dumps(output_data), encoding="utf-8")
            print(f"[Session {self.session_id}] Run #{self.runs} completed in {elapsed:.1f}s (exit code: {result.returncode})")

            # OPTIMIZATION: Defer verification and critic to background
            threading.Thread(
                target=self._background_processing,
                args=(result, elapsed, log_file),
                daemon=True
            ).start()

            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": elapsed,
                "returncode": result.returncode,
                "log_file": str(log_file)
            }

        except subprocess.TimeoutExpired:
            print(f"[Session {self.session_id}] Run #{self.runs} timed out after 600s")
            return {"session_id": self.session_id, "run": self.runs, "error": "timeout"}
        except Exception as e:
            print(f"[Session {self.session_id}] Run #{self.runs} error: {e}")
            return {"session_id": self.session_id, "run": self.runs, "error": str(e)}

    def _background_processing(self, result, elapsed, log_file):
        """Handle verification and critic in background"""
        try:
            # Self-verification
            verification = verify_grind_completion(
                session_id=self.session_id,
                run_num=self.runs,
                output=result.stdout,
                returncode=result.returncode
            )

            # Critic review if enabled
            quality_score = 0.0
            if self.critic_mode and result.stdout:
                try:
                    from critic import CriticAgent
                    critic = CriticAgent(self.workspace)
                    critic_review = critic.review(result.stdout[:5000], {
                        "task": self.task,
                        "session_id": self.session_id
                    })
                    quality_score = critic_review.get('score', 0.0)
                except Exception as e:
                    print(f"[Session {self.session_id}] Background critic failed: {e}")

            # Update log with background results
            try:
                existing_data = json.loads(log_file.read_text())
                existing_data.update({
                    "verification": verification,
                    "quality_score": quality_score,
                    "background_processed": True
                })
                log_file.write_text(json.dumps(existing_data), encoding="utf-8")
            except Exception as e:
                print(f"[Session {self.session_id}] Background log update failed: {e}")

        except Exception as e:
            print(f"[Session {self.session_id}] Background processing failed: {e}")

    def _categorize_error(self, error_type: str, error_message: str) -> str:
        """Quick error categorization"""
        if error_type == "timeout":
            return "TIMEOUT"

        full_text = (error_message or "").lower()
        if any(term in full_text for term in ["encoding", "utf", "decode"]):
            return "ENCODING"
        if any(term in full_text for term in ["import", "module not found"]):
            return "IMPORT"
        if any(term in full_text for term in ["syntax", "syntaxerror"]):
            return "SYNTAX"
        if any(term in full_text for term in ["error", "exception", "traceback"]):
            return "RUNTIME"
        return "UNKNOWN"

    def grind_loop(self):
        """Optimized grind loop with lazy operations"""
        while self.running:
            # Quick safety check
            try:
                from safety_killswitch import get_kill_switch
                halt_status = get_kill_switch().check_halt_flag()
                if halt_status["should_stop"]:
                    print(f"[Session {self.session_id}] HALT detected, stopping")
                    break
            except Exception:
                pass

            # Check cost limits
            if self.max_total_cost and get_total_spent() >= self.max_total_cost:
                print(f"[Session {self.session_id}] Cost limit reached")
                break

            result = self.run_once()
            if not self.running:
                break

            # OPTIMIZATION: Defer heavy operations to background
            if result.get("returncode", 0) == 0:
                threading.Thread(
                    target=self._background_kg_update,
                    daemon=True
                ).start()

            print(f"[Session {self.session_id}] Respawning in 2s...")
            time.sleep(2)

        print(f"[Session {self.session_id}] Stopped after {self.runs} runs")

    def _background_kg_update(self):
        """Update knowledge graph in background"""
        try:
            kg_file = WORKSPACE / "knowledge_graph.json"
            self.kg.save_json(str(kg_file))
        except Exception as e:
            print(f"[Session {self.session_id}] Background KG update failed: {e}")

# Compatibility alias
GrindSession = OptimizedGrindSession

def get_total_spent() -> float:
    """Calculate total cost spent across all grind logs."""
    total = 0.0
    if LOGS_DIR.exists():
        for log_file in LOGS_DIR.glob("*.json"):
            try:
                data = read_json(log_file)
                if isinstance(data, dict) and "cost" in data:
                    total += float(data["cost"])
            except (ValueError, TypeError):
                pass
    return total

def verify_grind_completion(session_id: int, run_num: int, output: str, returncode: int) -> dict:
    """Quick self-verification"""
    success_keywords = ["done", "complete", "success", "finished", "[ok]"]
    output_lower = (output or "").lower()

    indicators = [kw for kw in success_keywords if kw in output_lower]
    verified = returncode == 0 and len(indicators) > 0

    return {
        "verified": verified,
        "indicators": indicators,
        "details": f"{'PASS' if verified else 'FAIL'}: Exit code {returncode}, {len(indicators)} indicators"
    }

def main():
    """Optimized main function with faster startup"""
    # OPTIMIZATION: Validate config lazily
    try:
        from config import validate_config
        validate_config()
    except ImportError:
        pass  # Skip if not available

    parser = argparse.ArgumentParser(description="Optimized grind spawner with fast startup")
    parser.add_argument("-n", "--sessions", type=int, default=1, help="Number of parallel sessions")
    parser.add_argument("-m", "--model", default="haiku", help="Model: haiku, sonnet, opus")
    parser.add_argument("-b", "--budget", type=float, default=0.10, help="Budget per session")
    parser.add_argument("-w", "--workspace", default=str(WORKSPACE), help="Workspace directory")
    parser.add_argument("-t", "--task", default=None, help="Task for all sessions")
    parser.add_argument("--delegate", action="store_true", help="Read tasks from grind_tasks.json")
    parser.add_argument("--once", action="store_true", help="Run once, don't respawn")
    parser.add_argument("--max-total-cost", type=float, default=None, help="Maximum total cost")
    parser.add_argument("--critic", action="store_true", help="Enable critic mode")

    args = parser.parse_args()

    # OPTIMIZATION: Fast task loading
    if args.delegate:
        if not TASKS_FILE.exists():
            print(f"ERROR: --delegate requires {TASKS_FILE}")
            sys.exit(1)
        tasks_data = read_json(TASKS_FILE)
        tasks = [
            {"task": t.get("task", "General improvements"), "budget": t.get("budget", args.budget)}
            for t in tasks_data
        ]
    elif args.task:
        tasks = [{"task": args.task, "budget": args.budget} for _ in range(args.sessions)]
    else:
        print("ERROR: Specify --task or --delegate")
        sys.exit(1)

    print("=" * 60)
    print("  OPTIMIZED GRIND SPAWNER")
    print("=" * 60)
    print(f"  Workers: {len(tasks)} | Model: {args.model} | Mode: {'Single' if args.once else 'Continuous'}")

    # OPTIMIZATION: Quick safety validation
    print("[SAFETY] Quick validation...")
    valid_tasks = []
    for task_obj in tasks:
        task_text = task_obj["task"]
        if len(task_text) > 0 and not any(bad in task_text for bad in ['rm -rf', 'format c:']):
            valid_tasks.append(task_obj)
        else:
            print(f"[SAFETY] Blocked suspicious task: {task_text[:50]}...")

    if len(valid_tasks) == 0:
        print("[SAFETY] No valid tasks remaining")
        sys.exit(1)

    print(f"[SAFETY] {len(valid_tasks)} task(s) validated")

    # Create sessions with optimized initialization
    print(f"[STARTUP] Creating {len(valid_tasks)} optimized sessions...")
    start_init = time.time()

    sessions = [
        OptimizedGrindSession(
            session_id=i + 1,
            model=args.model,
            budget=task_obj["budget"],
            workspace=Path(args.workspace),
            task=task_obj["task"],
            max_total_cost=args.max_total_cost,
            critic_mode=args.critic
        )
        for i, task_obj in enumerate(valid_tasks)
    ]

    init_time = time.time() - start_init
    print(f"[STARTUP] Sessions created in {init_time*1000:.1f}ms")

    # Run sessions
    try:
        if args.once:
            with ThreadPoolExecutor(max_workers=len(sessions)) as executor:
                futures = [executor.submit(s.run_once) for s in sessions]
                for future in futures:
                    result = future.result()
                    print(f"  Result: {result}")
        else:
            threads = []
            for session in sessions:
                t = threading.Thread(target=session.grind_loop, daemon=True)
                t.start()
                threads.append(t)
                time.sleep(0.2)  # Faster stagger

            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping sessions...")
        for session in sessions:
            session.running = False
        time.sleep(1)

    print("Optimized grind spawner stopped.")

if __name__ == "__main__":
    main()