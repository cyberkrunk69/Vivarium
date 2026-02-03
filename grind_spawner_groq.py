"""
Grind Spawner for Groq - Network-isolated AI swarm execution.

This is the Groq-specific version of grind_spawner.py that:
- Uses Groq API instead of Claude CLI
- Enforces strict budget limits
- Supports adaptive model selection (8B vs 70B)

Usage:
    python grind_spawner_groq.py --delegate --model llama-3.1-8b-instant --budget 0.20
    python grind_spawner_groq.py --task "Fix bug in X" --budget 0.10
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

# Import Groq client
from groq_client import (
    GroqInferenceEngine,
    get_groq_engine,
    GROQ_MODELS,
    MODEL_ALIASES
)

# Import safety modules
from safety_sandbox import initialize_sandbox, get_sandbox
from safety_gateway import SafetyGateway
from safety_sanitize import sanitize_task, detect_injection_attempt
from safety_killswitch import get_kill_switch, get_circuit_breaker
from safety_network import scan_for_network_access
from safety_constitutional import ConstitutionalChecker

# Import core modules
from roles import RoleType, decompose_task, get_role, get_role_chain
from knowledge_graph import KnowledgeGraph
from utils import read_json, write_json

# Configuration
WORKSPACE = Path(os.environ.get("WORKSPACE", Path(__file__).parent))
LOGS_DIR = WORKSPACE / "grind_logs"
TASKS_FILE = WORKSPACE / "grind_tasks.json"
LEARNED_LESSONS_FILE = WORKSPACE / "learned_lessons.json"

# Simplified prompt template for Groq
GRIND_PROMPT_TEMPLATE = """You are an EXECUTION worker. Follow instructions EXACTLY.

WORKSPACE: {workspace}

TASK (execute step by step):
{task}

RULES:
1. Follow the steps EXACTLY as written - no improvisation
2. Be FAST - don't over-explain, just do the work
3. Output your work in a structured format
4. When done, output a 2-3 sentence summary

EXECUTE NOW.
"""


class GroqGrindSession:
    """Manages a single Groq-based grind session."""

    def __init__(
        self,
        session_id: int,
        model: str,
        budget: float,
        workspace: Path,
        task: str,
        max_total_cost: float = None
    ):
        self.session_id = session_id
        self.model = model
        self.budget = budget
        self.workspace = workspace
        self.max_total_cost = max_total_cost

        # Sanitize task
        task_dict = {"task": task}
        try:
            sanitized = sanitize_task(task_dict)
            self.task = sanitized["task"]
            if sanitized.get("_sanitized"):
                print(f"[Session {session_id}] WARNING: Task was sanitized")
        except ValueError as e:
            print(f"[Session {session_id}] ERROR: Invalid task: {e}")
            raise

        # Check for injection
        if detect_injection_attempt(self.task):
            print(f"[Session {session_id}] ALERT: Possible injection detected")

        self.runs = 0
        self.total_cost = 0.0
        self.running = True

        # Task analysis
        self.task_decomposition = decompose_task(self.task)
        self.complexity_score = self.task_decomposition.get("complexity_score", 0.0)

        # Initialize Groq engine
        self.groq_engine = get_groq_engine()

        # Initialize safety gateway
        self.safety_gateway = SafetyGateway(workspace=self.workspace)

        # Knowledge graph (lightweight load)
        self.kg = KnowledgeGraph()
        kg_file = self.workspace / "knowledge_graph.json"
        if kg_file.exists():
            try:
                self.kg.load_json(str(kg_file))
                print(f"[Session {self.session_id}] Loaded KG with {len(self.kg.nodes)} nodes")
            except Exception:
                pass

    def get_prompt(self) -> str:
        """Generate execution prompt."""
        base_prompt = GRIND_PROMPT_TEMPLATE.format(
            workspace=self.workspace,
            task=self.task
        )

        # Add role context
        role_chain = get_role_chain(self.task_decomposition["complexity"])
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
        """Run a single grind session using Groq API."""
        self.runs += 1
        start_time = datetime.now()

        # Safety checks
        kill_switch = get_kill_switch()
        circuit_breaker = get_circuit_breaker()

        # Check kill switch
        try:
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

        # Check circuit breaker
        try:
            cb_status = circuit_breaker.get_status()
            if cb_status['tripped']:
                return {
                    "session_id": self.session_id,
                    "run": self.runs,
                    "circuit_breaker_tripped": True,
                    "trip_reason": cb_status['reason'],
                    "returncode": -1
                }
        except Exception as e:
            print(f"[Session {self.session_id}] Circuit breaker error: {e}")

        # Check budget BEFORE execution
        within_budget, remaining = self.groq_engine.check_budget(self.budget)
        if not within_budget:
            print(f"[Session {self.session_id}] Budget exhausted (${self.budget:.2f})")
            return {
                "session_id": self.session_id,
                "run": self.runs,
                "budget_exhausted": True,
                "returncode": -1
            }

        # Safety gateway check
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

        # Generate prompt
        prompt = self.get_prompt()

        # Network scan (informational)
        violations = scan_for_network_access(prompt)
        if violations:
            print(f"[Session {self.session_id}] [SAFETY] {len(violations)} network patterns detected (blocked)")

        # Log start
        LOGS_DIR.mkdir(exist_ok=True)
        log_file = LOGS_DIR / f"session_{self.session_id}_run_{self.runs}.json"

        print(f"[Session {self.session_id}] Run #{self.runs} starting (model={self.model}, budget=${remaining:.4f} remaining)")

        # Execute via Groq
        try:
            result = self.groq_engine.execute(
                prompt=prompt,
                model=self.model,
                complexity_score=self.complexity_score,
                max_tokens=4096,
                temperature=0.7,
                timeout=300
            )

            elapsed = (datetime.now() - start_time).total_seconds()

            # Update cost tracking
            cost = result.get("cost", 0.0)
            self.total_cost += cost

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
                "timestamp": datetime.now().isoformat()
            }

            log_file.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

            # Print summary
            returncode = result.get("returncode", 0)
            if returncode == 0:
                print(f"[Session {self.session_id}] Run #{self.runs} completed in {elapsed:.1f}s (cost: ${cost:.6f})")
                circuit_breaker.record_success()
            else:
                error = result.get("error", "Unknown")
                print(f"[Session {self.session_id}] Run #{self.runs} failed: {error}")
                circuit_breaker.record_failure(f"session_{self.session_id}: {error}")

            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": elapsed,
                "returncode": returncode,
                "log_file": str(log_file),
                "cost": cost,
                "result": result.get("result", ""),
                "model": result.get("model"),
                "complexity_score": self.complexity_score,
                "error": result.get("error")
            }

        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"[Session {self.session_id}] Run #{self.runs} exception: {e}")
            circuit_breaker.record_failure(f"session_{self.session_id}: {str(e)[:200]}")

            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": elapsed,
                "returncode": 1,
                "error": str(e)
            }

    def grind_loop(self):
        """Continuous execution loop with budget enforcement."""
        kill_switch = get_kill_switch()
        circuit_breaker = get_circuit_breaker()

        while self.running:
            # Safety checks
            try:
                halt_status = kill_switch.check_halt_flag()
                if halt_status["should_stop"]:
                    print(f"[Session {self.session_id}] HALT detected")
                    break
            except Exception:
                pass

            try:
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

            # Pause between runs
            print(f"[Session {self.session_id}] Respawning in 2s...")
            time.sleep(2)

        print(f"[Session {self.session_id}] Stopped after {self.runs} runs, total cost: ${self.total_cost:.6f}")


def main():
    # Initialize sandbox
    initialize_sandbox(str(WORKSPACE))

    parser = argparse.ArgumentParser(description="Groq-based Grind Spawner")
    parser.add_argument("-n", "--sessions", type=int, default=1, help="Number of parallel sessions")
    parser.add_argument("-m", "--model", default="llama-3.1-8b-instant", help="Groq model ID or alias")
    parser.add_argument("-b", "--budget", type=float, default=0.20, help="Budget per session in USD")
    parser.add_argument("-w", "--workspace", default=str(WORKSPACE), help="Workspace directory")
    parser.add_argument("-t", "--task", default=None, help="Task for all sessions")
    parser.add_argument("--delegate", action="store_true", help="Read tasks from grind_tasks.json")
    parser.add_argument("--once", action="store_true", help="Run once per session")
    parser.add_argument("--max-total-cost", type=float, default=10.0, help="Max total cost across all sessions (default: $10)")

    args = parser.parse_args()

    # Validate Groq API key
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY environment variable not set")
        print("Get your key at: https://console.groq.com/keys")
        sys.exit(1)

    # Load tasks
    if args.delegate:
        if not TASKS_FILE.exists():
            print(f"ERROR: {TASKS_FILE} not found")
            sys.exit(1)
        tasks_data = read_json(TASKS_FILE)
        tasks = [
            {
                "task": t.get("task", "General improvements"),
                "budget": min(t.get("budget", args.budget), args.budget),  # Enforce budget cap
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

    # Constitutional safety check
    try:
        checker = ConstitutionalChecker(constraints_path=str(WORKSPACE / "SAFETY_CONSTRAINTS.json"))
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

    # Display configuration
    print("=" * 60)
    print("  GROQ GRIND SPAWNER")
    print("=" * 60)
    print(f"  Workers:       {len(tasks)}")
    print(f"  Model:         {args.model}")
    print(f"  Budget/task:   ${args.budget:.2f}")
    print(f"  Max total:     ${args.max_total_cost:.2f}")
    print(f"  Mode:          {'Single run' if args.once else 'Continuous'}")
    print("-" * 60)
    for i, t in enumerate(tasks):
        print(f"  [{i+1}] {t['task'][:50]}... (${t['budget']:.2f})")
    print("=" * 60)

    # Create sessions
    sessions = [
        GroqGrindSession(
            session_id=i + 1,
            model=tasks[i]["model"],
            budget=tasks[i]["budget"],
            workspace=Path(tasks[i]["workspace"]),
            task=tasks[i]["task"],
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
                time.sleep(0.5)

            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping all sessions...")
        for session in sessions:
            session.running = False
        time.sleep(2)

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
    print("=" * 60)


if __name__ == "__main__":
    main()
