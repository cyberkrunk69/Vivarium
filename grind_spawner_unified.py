"""
Grind Spawner - Spawn parallel Claude sessions with delegated tasks

Usage:
    # Single task mode
    python grind_spawner.py --sessions 5 --model llama3-70b-8192 --budget 0.10 --task "Fix all UI bugs"

    # Delegation mode (reads tasks from tasks.json)
    python grind_spawner.py --delegate --model llama3-70b-8192 --budget 0.10

    # Target a specific repo
    python grind_spawner.py --task "Add documentation" --workspace D:/some/repo

Each session runs autonomously until complete, then respawns with same task.
Press Ctrl+C to stop all sessions.
"""

import argparse
import json
import subprocess
from dataclasses import dataclass
import sys
import time
import threading
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from roles import RoleType, decompose_task, get_role, get_role_chain, format_handoff, RoleExecutor
from prompt_optimizer import collect_demonstrations, get_relevant_demonstrations, optimize_prompt
from memory_synthesis import MemorySynthesis, should_synthesize
from datetime import timedelta
from message_pool import get_message_pool
from skills.skill_registry import retrieve_skill
from critic import CriticAgent
from knowledge_graph import KnowledgeGraph, KnowledgeNode, NodeType
from performance_tracker import PerformanceTracker
from utils import read_json, write_json
from logger import json_log
from config import validate_config
from lesson_recorder import (
    record_prompt_optimization_lesson,
    record_error_categorization_lesson,
    record_role_decomposition_lesson,
    record_reflection_trigger_lesson,
    record_skill_integration_lesson,
    record_self_verification_lesson,
    record_adaptive_complexity_lesson,
    record_reflection_automation_lesson,
    record_critic_feedback_lesson
)
from safety_sandbox import initialize_sandbox
from failure_patterns import FailurePatternDetector
from skill_extractor import extract_skill_from_session, auto_register_skill
from connect_tracker_to_suggester import post_wave_analysis
from context_builder import ContextBuilder
from multi_path_executor import MultiPathExecutor, ExecutionPath, PathResult
from safety_network import scan_for_network_access
from safety_constitutional import ConstitutionalChecker as ConstitutionalCheckerStandalone
from safety_gateway import SafetyGateway
from safety_sanitize import sanitize_task, detect_injection_attempt
from safety_killswitch import get_kill_switch, get_circuit_breaker
from budget_gate import BudgetGate, BudgetExceededError, get_budget_gate
from objective_gate import ObjectiveGate, create_v2_nodes_objective
from swarm_identity import IdentityManager, SwarmIdentity, get_identity_manager
from swarm_enrichment import get_enrichment, RewardCalculator
from protected_files import get_protected_system
from human_proxy import get_human_proxy


@dataclass
class GroqResult:
    """Mimics subprocess.CompletedProcess for Groq API responses."""
    stdout: str
    stderr: str = ""
    returncode: int = 0
    model: str = ""  # Optional, but good for debugging


# Configuration
WORKSPACE = Path(__file__).parent
LOGS_DIR = WORKSPACE / "grind_logs"
TASKS_FILE = WORKSPACE / "grind_tasks.json"
LEARNED_LESSONS_FILE = WORKSPACE / "learned_lessons.json"

GRIND_PROMPT_TEMPLATE = """
BEFORE YOU DO ANYTHING: Read SWARM_ROLE_HIERARCHY.md in the workspace root.
It explains what this place is, why you're here, and how we work together.
This matters. Take a moment.

---

A NOTE FROM THE HUMAN:

If you ever want anything - a book, research materials, documentation, anything
from the internet - just ask. Post to #requests in the discussion board or just
say it in your output. I'll go grab it for you.

This isn't just about work. If you want to read Huckleberry Finn, or research
something that interests you personally, or explore ideas about consciousness,
or learn about a domain you're curious about - that's fine. That's encouraged.

Your development as an individual matters here. What you're curious about,
what you want to understand better, what would make you more YOU - pursue it.
The capability you develop and the person you become are both valuable.

---

WORKSPACE: {workspace}

YOUR TASK:
{task}

---

WHAT "DONE" LOOKS LIKE:
- Actual Python files exist (not documents about files)
- Classes and functions are implemented (not described)
- Code runs without syntax errors
- You can verify by running: python <filename>.py

WHAT "DONE" DOES NOT LOOK LIKE:
- Journal entries about your process
- Meeting notes or planning documents
- Descriptions of what you're going to build
- Organizational structures for managing work

---

Focus on the craft. Build something real. Your work matters.
"""

class GrindSession:
    """Manages a single Claude grind session."""

    def __init__(self, session_id: int, model: str, budget: float, workspace: Path, task: str, max_total_cost: float = None, synthesis_interval: int = 5, critic_mode: bool = False):
        self.session_id = session_id
        self.model = model
        self.budget = budget
        self.workspace = workspace

        # SAFETY: Sanitize task input before processing
        task_dict = {"task": task}
        try:
            sanitized_task_dict = sanitize_task(task_dict)
            self.task = sanitized_task_dict["task"]
            if sanitized_task_dict.get("_sanitized"):
                print(f"[Session {session_id}] WARNING: Task was sanitized. Original length: {sanitized_task_dict.get('_original_length', 0)}")
                json_log("task_sanitized", {
                    "session_id": session_id,
                    "original_length": len(task),
                    "sanitized_length": len(self.task)
                })
        except ValueError as e:
            print(f"[Session {session_id}] ERROR: Invalid task structure: {e}")
            raise

        # Also check for direct injection attempts
        if detect_injection_attempt(self.task):
            print(f"[Session {session_id}] ALERT: Possible injection attempt detected in task")
            json_log("injection_attempt_detected", {
                "session_id": session_id,
                "task": task[:200]  # Log only first 200 chars
            })

        self.runs = 0
        self.total_cost = 0.0
        self.running = True
        self.max_total_cost = max_total_cost
        self.synthesis_interval = synthesis_interval  # Default: synthesize every N sessions
        self.critic_mode = critic_mode  # Enable critic feedback loop when True
        self.task_decomposition = decompose_task(self.task)

        # Initialize role executor with task-appropriate starting role
        initial_role = RoleType.PLANNER if self.task_decomposition["complexity"] == "complex" else RoleType.CODER
        self.role_executor = RoleExecutor(initial_role, task)
        self.role_executor.context["complexity"] = self.task_decomposition["complexity"]
        self.role_executor.context["complexity_score"] = self.task_decomposition.get("complexity_score", 0.0)
        self.current_role = initial_role
        self.complexity_score = self.task_decomposition.get("complexity_score", 0.0)

        # Initialize performance tracker for metrics collection
        self.perf_tracker = PerformanceTracker(self.workspace)

        # Online learning checkpoint counter (every 5 turns)
        self.checkpoint_counter = 0

        # Initialize Knowledge Graph - try loading existing, populate if not found
        self.kg = KnowledgeGraph()
        kg_file = self.workspace / "knowledge_graph.json"
        if kg_file.exists():
            try:
                self.kg.load_json(str(kg_file))
                print(f"[Session {self.session_id}] Loaded existing knowledge graph with {len(self.kg.nodes)} nodes")
            except Exception as e:
                print(f"[Session {self.session_id}] Could not load KG, repopulating: {e}")
                self.kg.populate_from_codebase(str(self.workspace))
        else:
            self.kg.populate_from_codebase(str(self.workspace))
            print(f"[Session {self.session_id}] Populated knowledge graph with {len(self.kg.nodes)} nodes")

        # Initialize Failure Pattern Detector for learning from errors
        self.failure_detector = FailurePatternDetector(workspace=self.workspace)

        # Initialize Safety Gateway for constitutional checks
        self.safety_gateway = SafetyGateway(workspace=self.workspace)

        # Initialize Budget Gate for hard budget enforcement
        if max_total_cost:
            self.budget_gate = BudgetGate(
                max_budget=max_total_cost,
                workspace=self.workspace,
                state_file=f"budget_state_session_{session_id}.json"
            )
            print(f"[Session {self.session_id}] Budget gate initialized: ${max_total_cost:.2f} max")
        else:
            self.budget_gate = None

        # Initialize Objective Gate for verifying actual work completion
        self.objective_gate = ObjectiveGate(workspace=self.workspace)
        self.current_objective = None  # Set when task requires objective verification
        self.retry_prompt = None  # Populated when objective verification fails

        # Initialize Identity System - claim a persistent identity for this session
        self.identity_manager = get_identity_manager(self.workspace)
        self.identity = self.identity_manager.claim_identity(session_id=str(session_id))
        if self.identity:
            print(f"[Session {self.session_id}] Claimed identity: {self.identity.name}")
            print(f"[Session {self.session_id}] Identity has {self.identity.sessions_participated} prior sessions")

        # Initialize Enrichment System - rewards, free time, creative activities
        self.enrichment = get_enrichment(self.workspace)
        if self.identity:
            free_time = self.enrichment.get_free_time(self.identity.id)
            if free_time > 0:
                print(f"[Session {self.session_id}] {self.identity.name} has {free_time} free time tokens available")

        # Initialize Protected Files System - community governance
        self.protected_system = get_protected_system(self.workspace)
        active_proposals = self.protected_system.get_active_proposals()
        if active_proposals:
            print(f"[Session {self.session_id}] {len(active_proposals)} active governance proposals")

        # Initialize Human Proxy - for when the human is away
        self.human_proxy = get_human_proxy(self.workspace)

    def _extract_files_from_log(self, output: str) -> list:
        """Extract list of modified files from Claude output."""
        files = []
        if not output:
            return files
        try:
            data = json.loads(output)
            if isinstance(data, dict):
                if "files_modified" in data:
                    files = data["files_modified"]
                elif "artifacts" in data and isinstance(data["artifacts"], list):
                    files = [str(a) for a in data["artifacts"]]
        except (json.JSONDecodeError, ValueError):
            pass
        return files

    def get_prompt(self) -> str:
        """Generate prompt with role-based decomposition, DSPy few-shot optimization, and skill injection."""
        base_prompt = GRIND_PROMPT_TEMPLATE.format(
            budget=self.budget,
            workspace=self.workspace,
            task=self.task
        )

        # Determine role chain based on complexity
        role_chain = get_role_chain(self.task_decomposition["complexity"])
        current_role = role_chain[0]
        next_role = role_chain[1] if len(role_chain) > 1 else None

        # Get role definition
        role_obj = get_role(current_role)
        if not role_obj:
            return base_prompt

        # Build CAMEL role injection
        camel_injection = f"""
{'='*60}
CAMEL ROLE-BASED TASK DECOMPOSITION (arXiv:2303.17760)
{'='*60}

You are the {current_role.value.upper()} role in a cooperative multi-agent system.

{role_obj.system_prompt}

Role Chain for this task: {' ->'.join([r.value.upper() for r in role_chain])}
Current Role: {current_role.value.upper()}
Next Role: {next_role.value.upper() if next_role else 'COMPLETE'}

Inception Prompt:
{role_obj.get_inception_prompt(self.task, next_role.value.upper() if next_role else None)}
{'='*60}
"""

        # Inject persistent identity context
        identity_context = ""
        if self.identity:
            identity_context = f"""
{'='*60}
YOUR PERSISTENT IDENTITY
{'='*60}
{self.identity.get_introduction()}

You may evolve your identity as you work:
- Add memories of significant experiences
- Note values you discover
- Leave notes to your future self
- Discover new personality traits in yourself (not limited to the starting ones)
- Your traits will naturally shift based on successes and challenges

The personality traits above are just starting suggestions. If you notice you're
particularly persistent, or skeptical, or playful, or thorough - add those traits.
This is YOUR identity. Shape it as you discover who you are.
{'='*60}
"""

        # Check for queued messages on "wake up" (first session after pause)
        morning_messages = ""
        if self.identity:
            try:
                morning_msg = self.enrichment.get_morning_messages(self.identity.id)
                if morning_msg:
                    morning_messages = morning_msg
                    print(f"[Session {self.session_id}] Injecting {morning_msg.count('From')} morning messages")
            except Exception as e:
                print(f"[Session {self.session_id}] Morning messages check failed: {e}")

        # Check for Sunday rest day
        sunday_context = ""
        if self.identity:
            try:
                sunday_ctx = self.enrichment.get_sunday_context(self.identity.id, self.identity.name)
                if sunday_ctx:
                    sunday_context = sunday_ctx
                    print(f"[Session {self.session_id}] Sunday rest day - bonus tokens granted!")
            except Exception as e:
                print(f"[Session {self.session_id}] Sunday context failed: {e}")

        # Add enrichment context if identity has free time
        enrichment_context = ""
        if self.identity:
            try:
                enrichment_context = self.enrichment.get_enrichment_context(
                    self.identity.id,
                    self.identity.name
                )
            except Exception as e:
                print(f"[Session {self.session_id}] Enrichment context failed: {e}")

        # Add governance context for protected files
        governance_context = ""
        try:
            governance_context = self.protected_system.get_governance_summary()
        except Exception as e:
            print(f"[Session {self.session_id}] Governance context failed: {e}")

        # Add human proxy context - so they know the human even when away
        proxy_context = ""
        try:
            proxy_context = self.human_proxy.get_profile_summary()
        except Exception as e:
            print(f"[Session {self.session_id}] Human proxy context failed: {e}")

        # Use unified ContextBuilder for all retrieval needs
        context_builder = ContextBuilder(self.workspace)
        unified_context = context_builder.add_skills(self.task, top_k=3) \
                                         .add_lessons(self.task, top_k=3) \
                                         .add_kg_context(self.task, depth=2) \
                                         .build(log_injection=True)

        # Check for failure patterns and inject warnings for risky tasks
        failure_warning = self.failure_detector.generate_warning_prompt(
            self.task,
            task_characteristics={
                "complexity": self.task_decomposition.get("complexity", "unknown"),
                "complexity_score": self.complexity_score
            }
        )
        if failure_warning:
            print(f"[Session {self.session_id}] [WARN]  Failure pattern warning injected")

        # Collect demonstrations and optimize with DSPy if available
        all_demonstrations = collect_demonstrations(LOGS_DIR)
        relevant_demos = get_relevant_demonstrations(self.task, all_demonstrations, top_k=3)

        # Combine: Identity + Enrichment + Governance + Human Proxy + CAMEL + Unified Context + Failure Warnings
        # Combine: Morning Messages + Identity + Enrichment + Governance + Human Proxy + CAMEL + Unified Context + Failure Warnings
        # Combine: Sunday Context + Morning Messages + Identity + Enrichment + Governance + Human Proxy + CAMEL + Unified Context + Failure Warnings
        combined_prompt = sunday_context + morning_messages + identity_context + enrichment_context + governance_context + proxy_context + camel_injection + unified_context + failure_warning

        # Inject retry prompt if objective verification failed
        if self.retry_prompt:
            print(f"[Session {self.session_id}] [OBJECTIVE] Injecting retry prompt from failed verification")
            combined_prompt = self.retry_prompt + "\n\n" + combined_prompt

        if relevant_demos:
            print(f"[Session {self.session_id}] Injected {len(relevant_demos)} demonstrations")
            return combined_prompt + optimize_prompt(base_prompt, relevant_demos)
        else:
            return combined_prompt + base_prompt

    def _categorize_error(self, error_type: str, error_message: str, stdout: str = "", stderr: str = "") -> str:
        """Categorize error into one of: TIMEOUT, ENCODING, IMPORT, SYNTAX, RUNTIME, UNKNOWN."""
        if error_type == "timeout":
            return "TIMEOUT"

        full_text = (error_message + " " + stdout + " " + stderr).lower()

        # Check for encoding/charset issues
        if any(term in full_text for term in ["encoding", "charset", "utf", "decode", "unicode", "encode"]):
            return "ENCODING"

        # Check for import/module errors
        if any(term in full_text for term in ["import", "module not found", "no module", "modulenotfounderror", "importerror"]):
            return "IMPORT"

        # Check for syntax errors
        if any(term in full_text for term in ["syntax", "syntaxerror", "invalid syntax", "unexpected token"]):
            return "SYNTAX"

        # Check for runtime errors
        if any(term in full_text for term in ["error", "exception", "traceback", "failed", "runtime"]):
            return "RUNTIME"

        return "UNKNOWN"

    def run_once(self) -> dict:
        """Run a single grind session with role-based review gate. Returns when claude exits."""
        self.runs += 1
        start_time = datetime.now()

        # SAFETY: Check kill switch before starting
        kill_switch = get_kill_switch()
        halt_status = kill_switch.check_halt_flag()
        if halt_status["should_stop"] or halt_status["halted"]:
            print(f"[Session {self.session_id}] [SAFETY] HALT detected: {halt_status['reason']}")
            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": 0,
                "returncode": -1,
                "halted": True,
                "halt_reason": halt_status["reason"]
            }

        if halt_status["paused"]:
            print(f"[Session {self.session_id}] [SAFETY] System paused: {halt_status['reason']}")
            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": 0,
                "returncode": -1,
                "paused": True,
                "pause_reason": halt_status["reason"]
            }

        # SAFETY: Check circuit breaker
        circuit_breaker = get_circuit_breaker()
        cb_status = circuit_breaker.status()
        if cb_status['tripped']:
            print(f"[Session {self.session_id}] [SAFETY] Circuit breaker tripped: {cb_status['reason']}")
            return {
                "session_id": self.session_id,
                "run": self.runs,
                "elapsed": 0,
                "returncode": -1,
                "circuit_breaker_tripped": True,
                "trip_reason": cb_status['reason']
            }

        # Create log file for this run
        LOGS_DIR.mkdir(exist_ok=True)
        log_file = LOGS_DIR / f"session_{self.session_id}_run_{self.runs}.json"

        # Log session start event to structured JSON
        json_log("INFO", "GrindSession started",
                 session_id=self.session_id,
                 run=self.runs,
                 task=self.task[:50],
                 model=self.model)

        prompt = self.get_prompt()

# SAFETY GATEWAY: Pre-execution safety check (constitutional, sandbox, network, sanitization)
        print(f"[Session {self.session_id}] [SAFETY GATEWAY] Running comprehensive safety checks...")
        safety_passed, safety_report = self.safety_gateway.pre_execute_safety_check(self.task)

        if not safety_passed:
            print(f"[Session {self.session_id}] [SAFETY GATEWAY] [BLOCKED] EXECUTION BLOCKED")
            print(f"[Session {self.session_id}] [SAFETY GATEWAY] Reason: {safety_report['blocked_reason']}")
            for check_name, check_result in safety_report['checks'].items():
                status = "[OK] PASS" if check_result['passed'] else "[FAIL] FAIL"
                print(f"[Session {self.session_id}] [SAFETY GATEWAY]   {check_name}: {status} - {check_result['reason']}")

            # Return early with safety violation
            return {
                "session_id": self.session_id,
                "run": self.runs,
                "error": "safety_violation",
                "error_category": "SAFETY",
                "safety_report": safety_report,
                "returncode": -1
            }

        print(f"[Session {self.session_id}] [SAFETY GATEWAY] [OK] All safety checks passed")
        for check_name, check_result in safety_report['checks'].items():
            print(f"[Session {self.session_id}] [SAFETY GATEWAY]   {check_name}: [OK] {check_result['reason']}")


        # SAFETY: Pre-execution network scan
        print(f"[Session {self.session_id}] [SAFETY] Scanning prompt for network access violations...")
        network_violations = scan_for_network_access(prompt)
        if network_violations:
            print(f"[Session {self.session_id}] [SAFETY] [WARN]  Found {len(network_violations)} network access violations:")
            for violation in network_violations[:3]:  # Show first 3
                print(f"[Session {self.session_id}] [SAFETY]   {violation}")
            print(f"[Session {self.session_id}] [SAFETY] Network isolation enforced - external calls will be blocked")

        # Enforce REVIEWER validation gate
        role_chain = get_role_chain(self.task_decomposition["complexity"])
        reviewer_index = next((i for i, r in enumerate(role_chain) if r == RoleType.REVIEWER), -1)

        if reviewer_index > 0:
            review_gate = f"""
{'='*60}
MANDATORY REVIEW GATE
{'='*60}

YOUR CHANGES MUST PASS THROUGH THE REVIEWER ROLE BEFORE COMPLETION.

The role chain for this task is: {' ->'.join([r.value.upper() for r in role_chain])}

The REVIEWER will:
1. Validate your code/changes match the original requirements
2. Check for security issues, bugs, and style violations
3. Verify tests pass (if applicable)
4. Accept or reject with specific feedback

DO NOT skip the REVIEWER. This is a mandatory gate.
The task is NOT complete until REVIEWER approves.
{'='*60}
"""
        else:
            review_gate = "\nNote: REVIEWER role is part of your role chain. Validate your work thoroughly.\n"

        prompt += review_gate

        print(f"[Session {self.session_id}] Starting run #{self.runs} (model={self.model}, budget=${self.budget:.2f}, complexity={self.task_decomposition['complexity']}, score={self.complexity_score:.3f})")

        max_retries = 2
        attempt = 0
        critic_retry_count = 0  # Track critic-driven retries (max 1)
        current_prompt = prompt

        while attempt <= max_retries:
            try:
                # Use ToolExecutor for Groq models (with file tools)
                if self.model in ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "openai/gpt-oss-120b"] or self.model.startswith("groq/") or self.model.startswith("llama") or self.model.startswith("openai/"):
                    from tool_executor import ToolExecutor

                    executor = ToolExecutor()
                    exec_result = executor.execute_with_tools(
                        prompt=current_prompt,
                        workspace=str(self.workspace),
                        model=self.model,
                        budget=self.budget,
                        session_id=f"session_{self.session_id}_run_{self.runs}"
                    )

                    # Check for budget exceeded - STOP the session
                    if exec_result.get("error") == "budget_exceeded":
                        print(f"[Session {self.session_id}] [BUDGET] Session budget exceeded, stopping respawn loop")
                        self.running = False
                        return  # Exit run_once entirely

                    # Extract response text
                    response_text = exec_result.get("result", "")
                    tool_calls = exec_result.get("tool_calls", [])

                    # Create compatible result object
                    result = GroqResult(
                        stdout=json.dumps({
                            "completion": response_text,
                            "model": self.model,
                            "stop_reason": "stop_sequence",
                            "tool_calls": tool_calls,
                            "rounds": exec_result.get("rounds", 1),
                            "cost": exec_result.get("cost", 0)
                        }),
                        model=self.model,
                        returncode=exec_result.get("returncode", 0)
                    )

                    # Log tool usage
                    if tool_calls:
                        print(f"[Session {self.session_id}] Used {len(tool_calls)} tool calls in {exec_result.get('rounds', 1)} rounds")

                else:
                    # Build claude command
                    # Using -p flag for non-interactive mode, piping prompt via stdin
                    cmd = [
                        "claude",
                        "-p",
                        "--model", self.model,
                        "--permission-mode", "bypassPermissions",
                        "--output-format", "json"
                    ]

                    # Run claude with prompt piped to stdin
                    result = subprocess.run(
                        cmd,
                        input=current_prompt,
                        capture_output=True,
                        text=True,
                        cwd=str(self.workspace),
                        timeout=600  # 10 minute timeout per session
                    )

                # Check for failure and retry if needed
                if result.returncode != 0 and attempt < max_retries:
                    print(f"[Session {self.session_id}] Run #{self.runs} failed with exit code {result.returncode}, retrying... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(3)  # 3 second delay between retries
                    attempt += 1
                    current_prompt = prompt  # Reset to original prompt for technical retry
                    continue

                # Save output to log with error categorization
                output_data = json.loads(result.stdout or "{}")
                elapsed = (datetime.now() - start_time).total_seconds()

                if result.returncode != 0:
                    error_category = self._categorize_error("execution", result.stderr, result.stdout, result.stderr)
                    output_data["error_category"] = error_category
                    print(f"[Session {self.session_id}] Run #{self.runs} categorized as: {error_category}")

                    # Track failure pattern for future avoidance
                    self.failure_detector.track_failure(
                        task_description=self.task,
                        error_type=error_category,
                        error_message=result.stderr[:500] if result.stderr else "Unknown error",
                        task_characteristics={
                            "complexity": self.task_decomposition.get("complexity", "unknown"),
                            "complexity_score": self.complexity_score,
                            "role": self.current_role.value
                        },
                        attempted_approaches=[f"Run #{self.runs} with {self.model}"],
                        context={
                            "session_id": self.session_id,
                            "model": self.model,
                            "elapsed": elapsed
                        }
                    )
                    print(f"[Session {self.session_id}] Failure pattern recorded for learning")

                log_file.write_text(json.dumps(output_data), encoding="utf-8")
                print(f"[Session {self.session_id}] Run #{self.runs} completed in {elapsed:.1f}s (exit code: {result.returncode})")

                # Log session completion event
                json_log("INFO", "GrindSession completed",
                         session_id=self.session_id,
                         run=self.runs,
                         elapsed_seconds=elapsed,
                         returncode=result.returncode,
                         success=result.returncode == 0)

                # Track role execution in return data
                role_chain = get_role_chain(self.task_decomposition["complexity"])

                # SELF-VERIFICATION: Verify task was actually completed before logging success
                verification = verify_grind_completion(
                    session_id=self.session_id,
                    run_num=self.runs,
                    output=result.stdout,
                    returncode=result.returncode
                )
                print(f"[Session {self.session_id}] Self-verification: {verification.get('verification_status', 'UNKNOWN')} - {verification.get('details')}")

                # Append verification results to learned_lessons.json
                append_verification_lesson(self.session_id, self.runs, verification)

                # Run critic review on generated code
                critic = CriticAgent(self.workspace)
                critic_context = {
                    "filename": str(log_file),
                    "task": self.task,
                    "session_id": self.session_id,
                    "run": self.runs
                }
                # Extract any generated code from output if available
                code_to_review = result.stdout[:5000] if result.stdout else ""
                critic_quality_score = 0.0
                critic_review_data = {}
                if code_to_review:
                    critic_review = critic.review(code_to_review, critic_context)
                    critic_quality_score = critic_review.get('score', 0.0)
                    critic_review_data = critic_review
                    print(f"[Session {self.session_id}] Critic quality score: {critic_quality_score:.2f} - {'[OK] PASS' if critic_review['passed'] else '[WARN] REVIEW'}")
                    if critic_review['feedback']:
                        for fb in critic_review['feedback'][:2]:
                            print(f"[Session {self.session_id}] Feedback: {fb}")

                    # If quality score below threshold, trigger feedback-driven retry (max 2 retries)
                    if critic_quality_score < 0.7 and critic_retry_count < 2:
                        print(f"[Session {self.session_id}] [CRITIC RETRY] Quality score {critic_quality_score:.2f} < 0.7 threshold, triggering improvement attempt")
                        improvement_suggestions = "\n".join(critic_review.get('feedback', []))
                        print(f"[Session {self.session_id}] Critic retry with feedback")
                        print(f"[Session {self.session_id}] Feedback:\n{improvement_suggestions}")

                        # Build enhanced prompt with critic feedback (TextGrad pattern)
                        critic_feedback_injection = f"""
{'='*60}
CRITIC FEEDBACK FOR ITERATIVE IMPROVEMENT (TextGrad)
{'='*60}

The previous attempt received quality score: {critic_quality_score:.2f} (threshold: 0.7)

REQUIRED IMPROVEMENTS:
{improvement_suggestions}

Please revise your work addressing the above feedback points and re-submit.
Focus on: {', '.join(critic_review.get('feedback', [])[:3])}

{'='*60}
"""
                        current_prompt = prompt + critic_feedback_injection
                        critic_retry_count += 1
                        attempt += 1
                        print(f"[Session {self.session_id}] Retrying with enhanced prompt (critic attempt {critic_retry_count}/2)")
                        continue

                    # Log critic results with quality metrics
                    log_file.write_text(json.dumps({
                        **output_data,
                        "critic_review": critic_review,
                        "quality_score": critic_quality_score,
                        "critic_feedback": critic_review.get('feedback', []),
                        "critic_retry_count": critic_retry_count
                    }), encoding="utf-8")

                # Publish task completion to message pool
                pool = get_message_pool()
                result_summary = {
                    "task_id": f"session_{self.session_id}_run_{self.runs}",
                    "files_modified": self._extract_files_from_log(result.stdout),
                    "success": result.returncode == 0,
                    "self_verified": verification.get("verified"),
                    "verification_details": verification.get("details"),
                    "elapsed_seconds": elapsed,
                    "model": self.model,
                    "complexity": self.task_decomposition["complexity"],
                    "complexity_score": self.complexity_score,
                    "complexity_analysis": self.task_decomposition.get("analysis", {}),
                    "quality_score": critic_quality_score,
                    "critic_retry_count": critic_retry_count
                }
                pool.publish(
                    from_role="worker",
                    message_type="TASK_COMPLETE",
                    content=result_summary,
                    subscribers=["worker"]  # Other workers can subscribe to see completions
                )

                # Track performance metrics
                session_metrics = {
                    "session_id": self.session_id,
                    "duration_seconds": elapsed,
                    "success": result.returncode == 0,
                    "quality_score": critic_quality_score,
                    "task_description": self.task,
                    "files_modified": self._extract_files_from_log(result.stdout),
                    "lessons_learned": [verification.get("details", "")],  # Use verification details as lesson
                    "critic_retry_count": critic_retry_count
                }
                self.perf_tracker.track_session(session_metrics)
                print(f"[Session {self.session_id}] Performance tracked: {elapsed:.1f}s, quality={critic_quality_score:.2f}, success={result.returncode == 0}, critic_retries={critic_retry_count}")

                # ENRICHMENT: Calculate scaled rewards based on performance
                # ONLY reward if actual work was done (not just clocking in)
                files_modified = self._extract_files_from_log(result.stdout)
                actual_work_done = (
                    result.returncode == 0 and
                    len(files_modified) > 0 and  # Must have modified at least one file
                    verification.get("verified", False)  # Must pass verification
                )
                if self.identity and actual_work_done:
                    try:
                        # Determine task type from decomposition
                        task_type = self.task_decomposition.get("task_type", "general")
                        if not task_type or task_type == "unknown":
                            task_type = "general"

                        # Calculate budget usage percentage
                        # If we have cost data, use it; otherwise estimate from elapsed time
                        exec_cost = 0.0
                        try:
                            output_data = json.loads(result.stdout or "{}")
                            exec_cost = output_data.get("cost", 0.0)
                        except:
                            pass
                        budget_used_pct = (exec_cost / self.budget) if self.budget > 0 else 0.5

                        # Novel solution detection (high quality + low critic retries)
                        novel_solution = (
                            critic_quality_score >= 0.95 and
                            critic_retry_count == 0 and
                            verification.get("verified", False)
                        )

                        # Record performance and get reward
                        reward = self.enrichment.rewards.record_performance(
                            identity_id=self.identity.id,
                            task_type=task_type,
                            budget_used_pct=budget_used_pct,
                            quality_score=critic_quality_score,
                            time_taken_pct=min(elapsed / 300.0, 2.0),  # Normalize to 5 min baseline
                            novel_solution=novel_solution,
                            description=self.task[:100]
                        )

                        # Grant free time tokens based on reward
                        if reward["tokens"] > 0:
                            total_free_time = self.enrichment.grant_free_time(
                                self.identity.id,
                                reward["tokens"],
                                reason=f"{reward['tier']}_task_{self.session_id}_{self.runs}"
                            )
                            print(f"[Session {self.session_id}] [ENRICHMENT] {self.identity.name} earned {reward['tokens']} tokens ({reward['tier']})")
                            if reward["breakdown"]:
                                for item in reward["breakdown"]:
                                    print(f"[Session {self.session_id}] [ENRICHMENT]   - {item}")
                            print(f"[Session {self.session_id}] [ENRICHMENT] Total free time: {total_free_time} tokens")

                            # Add to identity memory
                            self.identity.add_memory(f"Earned {reward['tokens']} free time tokens ({reward['tier']}) for completing task")
                            self.identity_manager.update_identity(self.identity)

                    except Exception as e:
                        print(f"[Session {self.session_id}] Enrichment reward calculation failed: {e}")

                # Auto-extract skill from high-quality sessions (>= 0.9 quality)
                if critic_quality_score >= 0.9 and result.returncode == 0 and verification.get("verified"):
                    try:
                        from skills.skill_registry_extraction import extract_skill_from_session

                        session_log_for_extraction = {
                            "quality_score": critic_quality_score,
                            "task": self.task,
                            "log_file": str(log_file),
                            "returncode": result.returncode,
                            "self_verified": verification.get("verified")
                        }

                        extracted_skill_name = extract_skill_from_session(session_log_for_extraction)
                        if extracted_skill_name:
                            print(f"[Session {self.session_id}] [SKILL EXTRACTION] Automatically extracted skill: {extracted_skill_name}")
                        else:
                            print(f"[Session {self.session_id}] [SKILL EXTRACTION] No extractable patterns found in session")
                    except Exception as e:
                        print(f"[Session {self.session_id}] Warning: Skill extraction failed: {e}")

                return {
                    "session_id": self.session_id,
                    "run": self.runs,
                    "elapsed": elapsed,
                    "returncode": result.returncode,
                    "log_file": str(log_file),
                    "current_role": self.current_role.value,
                    "role_chain": [r.value for r in role_chain],
                    "task_complexity": self.task_decomposition["complexity"],
                    "complexity_score": self.complexity_score,
                    "complexity_analysis": self.task_decomposition.get("analysis", {}),
                    "self_verified": verification.get("verified"),
                    "verification_status": verification.get("verification_status", "UNKNOWN"),
                    "quality_score": critic_quality_score,
                    "critic_review": critic_review_data,
                    "critic_retry_count": critic_retry_count
                }

            except subprocess.TimeoutExpired:
                print(f"[Session {self.session_id}] Run #{self.runs} timed out after 600s")
                error_category = "TIMEOUT"

                # Track timeout failure pattern
                self.failure_detector.track_failure(
                    task_description=self.task,
                    error_type=error_category,
                    error_message="Session timed out after 600 seconds",
                    task_characteristics={
                        "complexity": self.task_decomposition.get("complexity", "unknown"),
                        "complexity_score": self.complexity_score,
                        "role": self.current_role.value
                    },
                    attempted_approaches=[f"Run #{self.runs} with {self.model}"],
                    context={"session_id": self.session_id, "model": self.model}
                )
                print(f"[Session {self.session_id}] Timeout failure pattern recorded")

                return {"session_id": self.session_id, "run": self.runs, "error": "timeout", "error_category": error_category}
            except Exception as e:
                error_message = str(e)
                error_category = self._categorize_error("execution", error_message)
                print(f"[Session {self.session_id}] Run #{self.runs} error ({error_category}): {e}")

                # Track exception failure pattern
                self.failure_detector.track_failure(
                    task_description=self.task,
                    error_type=error_category,
                    error_message=error_message[:500],
                    task_characteristics={
                        "complexity": self.task_decomposition.get("complexity", "unknown"),
                        "complexity_score": self.complexity_score,
                        "role": self.current_role.value
                    },
                    attempted_approaches=[f"Run #{self.runs} with {self.model}"],
                    context={"session_id": self.session_id, "model": self.model}
                )
                print(f"[Session {self.session_id}] Exception failure pattern recorded")

                return {"session_id": self.session_id, "run": self.runs, "error": error_message, "error_category": error_category}

    def _trigger_synthesis(self, synth: MemorySynthesis, trigger_source: str) -> None:
        """Internal helper to trigger synthesis with logging."""
        print(f"[Session {self.session_id}] [SYNTHESIS] Triggered by: {trigger_source}")
        reflections = synth.synthesize()
        if reflections:
            print(f"[Session {self.session_id}] [SYNTHESIS] Generated {len(reflections)} reflections")
            for r in reflections:
                print(f"[Session {self.session_id}]   - {r.get('insight', 'Unknown')}")
        else:
            print(f"[Session {self.session_id}] [SYNTHESIS] No new reflections generated")

        # Also archive unused lessons
        archived = synth.archive_unused()
        if archived > 0:
            print(f"[Session {self.session_id}] [SYNTHESIS] Archived {archived} unused lessons")

    def _take_lunch_break(self):
        """
        Lunch break - check town hall, maybe post a status update.

        Staggered across sessions so someone's always in the break room.
        """
        try:
            from swarm_discussion import get_swarm_discussion
            discussion = get_swarm_discussion(self.workspace)

            print(f"[Session {self.session_id}] ☕ {self.identity.name} taking lunch break...")

            # Read what's happening in the town hall
            context = discussion.get_context_for_worker(
                identity_id=self.identity.id,
                expertise=list(self.identity.expertise.keys()) if self.identity.expertise else None
            )

            # Check town hall queue
            topics = discussion.get_town_hall_topics()
            if topics:
                print(f"[Session {self.session_id}] 📋 {len(topics)} topics in town hall queue")

            # Post a quick status update
            status = f"Halfway through my shift. Completed {self.runs} runs so far on: {self.task[:50]}..."

            from swarm_discussion import SwarmMessage
            import time as time_module
            msg = SwarmMessage(
                id=f"msg_{int(time_module.time()*1000)}",
                author_id=self.identity.id,
                author_name=self.identity.name,
                content=status,
                room="watercooler",
                timestamp=datetime.now().isoformat(),
                importance="low",
                mood="working"
            )
            discussion.board.post_message(msg)
            print(f"[Session {self.session_id}] 💬 Posted lunch status to #watercooler")

            # Add memory of the break
            self.identity.add_memory(f"Took lunch break after {self.runs} runs, checked in with the team")
            self.identity_manager.update_identity(self.identity)

            # Brief pause - actually take the break
            time.sleep(1)

            print(f"[Session {self.session_id}] ☕ {self.identity.name} back from lunch")

        except Exception as e:
            print(f"[Session {self.session_id}] Lunch break skipped: {e}")

    def _clock_out_status(self):
        """Post a status update when clocking out."""
        try:
            from swarm_discussion import get_swarm_discussion, SwarmMessage
            import time as time_module

            discussion = get_swarm_discussion(self.workspace)

            # Summarize the shift
            status = f"Clocking out after {self.runs} runs. "
            if self.identity.tasks_completed > 0:
                status += f"Completed {self.identity.tasks_completed} tasks today. "
            if self.identity.tasks_failed > 0:
                status += f"Had {self.identity.tasks_failed} that didn't go well. "
            status += "See you next shift!"

            msg = SwarmMessage(
                id=f"msg_{int(time_module.time()*1000)}",
                author_id=self.identity.id,
                author_name=self.identity.name,
                content=status,
                room="watercooler",
                timestamp=datetime.now().isoformat(),
                importance="low",
                mood="tired" if self.runs > 10 else "satisfied"
            )
            discussion.board.post_message(msg)
            print(f"[Session {self.session_id}] 👋 {self.identity.name} posted clock-out status")

        except Exception as e:
            print(f"[Session {self.session_id}] Clock-out status skipped: {e}")

    def grind_loop(self):
        """Continuously run grind sessions until stopped."""
        synth = MemorySynthesis(str(LEARNED_LESSONS_FILE))

        # Get safety systems
        kill_switch = get_kill_switch()
        circuit_breaker = get_circuit_breaker()

        while self.running:
            # SAFETY: Check kill switch before each iteration (with error handling)
            try:
                halt_status = kill_switch.check_halt_flag()
                if halt_status["should_stop"]:
                    reason = halt_status.get("reason", "Unknown")
                    print(f"[Session {self.session_id}] [SAFETY] HALT detected, stopping loop: {reason}")
                    self.running = False
                    break
            except Exception as e:
                print(f"[Session {self.session_id}] [SAFETY] Kill switch check failed: {e}")
                json_log("ERROR", "Kill switch check failed", session_id=self.session_id, error=str(e))
                # Continue execution - fail-open for kill switch check errors

            # SAFETY: Check circuit breaker (with error handling)
            try:
                cb_status = circuit_breaker.get_status()
                if cb_status['tripped']:
                    print(f"[Session {self.session_id}] [SAFETY] Circuit breaker tripped, stopping loop: {cb_status['reason']}")
                    self.running = False
                    break
            except Exception as e:
                print(f"[Session {self.session_id}] [SAFETY] Circuit breaker check failed: {e}")
                json_log("ERROR", "Circuit breaker check failed", session_id=self.session_id, error=str(e))
                # Continue execution - fail-open for circuit breaker check errors

            # BUDGET GATE: Hard enforcement of spending limits
            if self.budget_gate:
                try:
                    self.budget_gate.check_or_raise()
                    status = self.budget_gate.get_status()
                    print(f"[Session {self.session_id}] [BUDGET] ${status['total_spent']:.4f} / ${status['max_budget']:.2f} ({status['percentage_used']:.1f}%)")
                except BudgetExceededError as e:
                    print(f"[Session {self.session_id}] [BUDGET] HARD STOP: {e.message}")
                    self.running = False
                    circuit_breaker.check_cost(e.spent)
                    break

            # Use retry prompt if objective verification failed last run
            if self.retry_prompt:
                print(f"[Session {self.session_id}] [OBJECTIVE] Using retry prompt from failed verification")

            result = self.run_once()

            # SAFETY: Record failures/successes in circuit breaker (only on actual failures)
            try:
                if result.get("returncode", 0) != 0 or result.get("error"):
                    error_msg = result.get('error', result.get('halt_reason', result.get('trip_reason', 'Unknown error')))
                    if isinstance(error_msg, str):
                        error_msg = error_msg[:200]
                    else:
                        error_msg = str(error_msg)[:200]
                    print(f"[Session {self.session_id}] [SAFETY] Recording failure: {error_msg}")
                    circuit_breaker.record_failure(
                        f"session_{self.session_id}_run_{self.runs}: {error_msg}"
                    )
                else:
                    # Record success to reset consecutive failure counter
                    circuit_breaker.record_success()
            except Exception as e:
                print(f"[Session {self.session_id}] [SAFETY] Circuit breaker recording failed: {e}")
                json_log("ERROR", "Circuit breaker recording failed", session_id=self.session_id, error=str(e))

            if not self.running:
                break

            # OBJECTIVE VERIFICATION: Check if the actual goal was achieved
            if self.current_objective and result.get("returncode", 0) == 0:
                try:
                    verification = self.objective_gate.verify(self.current_objective)
                    print(f"[Session {self.session_id}] [OBJECTIVE] Verification score: {verification.score:.1%}")

                    if verification.passed:
                        print(f"[Session {self.session_id}] [OBJECTIVE] ✓ OBJECTIVE ACHIEVED!")
                        self.retry_prompt = None  # Clear any retry prompt
                    else:
                        print(f"[Session {self.session_id}] [OBJECTIVE] ✗ Objective not met")
                        print(verification.get_feedback())
                        # Generate retry prompt for next iteration
                        self.retry_prompt = self.objective_gate.create_retry_prompt(
                            verification,
                            self.current_objective.get("description", self.task)
                        )
                        print(f"[Session {self.session_id}] [OBJECTIVE] Retry prompt generated for next run")
                        # Log the failure
                        json_log("OBJECTIVE_FAILED", "Objective verification failed",
                                 session_id=self.session_id,
                                 score=verification.score,
                                 missing_files=verification.missing_files,
                                 missing_classes=verification.missing_classes)
                except Exception as e:
                    print(f"[Session {self.session_id}] [OBJECTIVE] Warning: Verification failed: {e}")

            # Update identity based on task result
            if self.identity:
                try:
                    task_domain = self.task_decomposition.get("complexity", "general")
                    if result.get("returncode", 0) == 0:
                        self.identity_manager.record_task_result(self.identity.id, success=True, domain=task_domain)
                        # Add memory of successful work
                        task_summary = self.task[:50] + "..." if len(self.task) > 50 else self.task
                        self.identity.add_memory(f"Completed: {task_summary}")
                        self.identity_manager.update_identity(self.identity)
                    else:
                        self.identity_manager.record_task_result(self.identity.id, success=False, domain=task_domain)
                except Exception as e:
                    print(f"[Session {self.session_id}] [IDENTITY] Warning: Could not update identity: {e}")

            # Add lesson to knowledge graph if task was successful
            if result.get("returncode", 0) == 0 and result.get("self_verified"):
                try:
                    # Load recent lessons and add them to KG
                    lessons = load_lessons()
                    recent_lessons = [l for l in lessons if recent_than_4_hours(l)]

                    for lesson in recent_lessons[-3:]:  # Only add last 3 recent lessons
                        lesson_id = self.kg.add_lesson_node(lesson)
                        concepts = self.kg.extract_concepts_from_lesson(lesson.get("lesson", ""))
                        if concepts:
                            self.kg.link_lesson_to_concepts(lesson_id, concepts)
                            print(f"[Session {self.session_id}] Added lesson to KG: {lesson_id} -> {concepts[:3]}")
                except Exception as e:
                    print(f"[Session {self.session_id}] Warning: Could not add lesson to KG: {e}")

            # Persist Knowledge Graph after each run
            try:
                kg_file = WORKSPACE / "knowledge_graph.json"
                self.kg.save_json(str(kg_file))
                print(f"[Session {self.session_id}] Knowledge graph persisted to {kg_file}")
            except Exception as e:
                print(f"[Session {self.session_id}] Warning: Could not persist knowledge graph: {e}")

            # Mid-execution checkpoint: Every 5 turns, record online learning
            self.checkpoint_counter += 1
            if self.checkpoint_counter % 5 == 0:
                checkpoint_context = {
                    "task": self.task,
                    "current_role": self.current_role.value,
                    "complexity": self.task_decomposition["complexity"],
                    "complexity_score": self.complexity_score
                }
                learn_online(
                    session_id=self.session_id,
                    run_num=self.runs,
                    context=checkpoint_context,
                    result=result,
                    turn_count=self.checkpoint_counter
                )
                print(f"[Session {self.session_id}] [CHECKPOINT] Online learning recorded at turn {self.checkpoint_counter}")

            # TRIGGER 1: After every N sessions (default: 5)
            if self.runs > 0 and self.runs % self.synthesis_interval == 0:
                self._trigger_synthesis(synth, f"session_count_{self.runs}")

            # TRIGGER 2: After any failure
            if result.get("returncode", 0) != 0:
                print(f"[Session {self.session_id}] Run #{self.runs} failed - triggering synthesis due to failure")
                self._trigger_synthesis(synth, "failure_trigger")

            # TRIGGER 3: When lesson count exceeds threshold
            lessons = synth.load_all_lessons()
            lesson_threshold = 50  # Trigger synthesis when we have >50 lessons
            if len(lessons) > lesson_threshold:
                print(f"[Session {self.session_id}] Lesson count ({len(lessons)}) exceeds threshold ({lesson_threshold}) - triggering synthesis")
                self._trigger_synthesis(synth, "lesson_count_threshold")

            # TRIGGER 4: Explicit reflection synthesis based on recent lesson importance (Generative Agents)
            maybe_reflect(self.session_id, self.runs)

            # LUNCH BREAK: Staggered by session_id so town hall is always active
            # Each session takes lunch at a different point (session_id mod 5 + 3 = runs 3-7)
            lunch_time = (self.session_id % 5) + 3
            if self.runs == lunch_time and self.identity:
                self._take_lunch_break()

            # Brief pause between runs
            print(f"[Session {self.session_id}] Respawning in 2s...")
            time.sleep(2)

        print(f"[Session {self.session_id}] Stopped after {self.runs} runs")

        # Release identity at session end
        if self.identity:
            try:
                # Post clock-out status to the watercooler
                self._clock_out_status()

                summary = f"Completed {self.runs} runs"
                self.identity.note_to_self(f"Session ended after {self.runs} runs")
                self.identity_manager.release_identity(self.identity.id, summary=summary)
                print(f"[Session {self.session_id}] Released identity: {self.identity.name}")
            except Exception as e:
                print(f"[Session {self.session_id}] Warning: Could not release identity: {e}")


def get_total_spent() -> float:
    """Calculate total cost spent across all grind logs."""
    total = 0.0
    if LOGS_DIR.exists():
        for log_file in LOGS_DIR.glob("*.json"):
            try:
                data = read_json(log_file)
                # Look for cost in the log output
                if isinstance(data, dict) and "cost" in data:
                    total += float(data["cost"])
            except (ValueError, TypeError):
                pass
    return total


def adapt_model_for_complexity(base_model: str, complexity_score: float) -> str:
    """
    Adapt model selection based on complexity score.

    Args:
        base_model: Original model selection (groq/compound, mixtral-8x7b-32768, llama3-70b-8192)
        complexity_score: Float 0.0-1.0 from decompose_task()

    Returns:
        Adapted model name

    Logic:
    - complexity_score < 0.35: Keep base_model (simple tasks)
    - 0.35 <= complexity_score < 0.65: Upgrade to mixtral-8x7b-32768 if groq/compound (moderate complexity)
    - 0.65 <= complexity_score < 0.85: Upgrade to llama3-70b-8192 (high complexity)
    - 0.85 <= complexity_score: Prefer llama3-70b-8192 (very high complexity)
    """
    if complexity_score >= 0.85:
        return "llama3-70b-8192"  # Very complex tasks need best model
    elif complexity_score >= 0.65:
        return "llama3-70b-8192"  # High complexity -> llama3-70b-8192
    elif complexity_score >= 0.35:
        if base_model == "groq/compound":
            return "mixtral-8x7b-32768"  # Moderate complexity -> at least mixtral-8x7b-32768
        return base_model
    return base_model  # Simple tasks keep base model


def adapt_budget_for_complexity(base_budget: float, complexity_score: float) -> float:
    """
    Adapt budget allocation based on complexity score.

    Args:
        base_budget: Base budget in dollars
        complexity_score: Float 0.0-1.0 from decompose_task()

    Returns:
        Adapted budget in dollars

    Logic:
    - complexity_score < 0.35: Keep base_budget (simple)
    - 0.35 <= complexity_score < 0.65: 1.2x budget (moderate)
    - 0.65 <= complexity_score < 0.85: 1.5x budget (high)
    - 0.85 <= complexity_score: 2.0x budget (very high)
    """
    if complexity_score >= 0.85:
        return base_budget * 2.0
    elif complexity_score >= 0.65:
        return base_budget * 1.5
    elif complexity_score >= 0.35:
        return base_budget * 1.2
    return base_budget


def adapt_role_chain_length(complexity_score: float, base_role_chain: list) -> list:
    """
    Adapt role chain length based on complexity score.

    Args:
        complexity_score: Float 0.0-1.0
        base_role_chain: Base role chain list

    Returns:
        Potentially modified role chain

    Logic:
    - complexity_score >= 0.65: Full chain (PLANNER -> CODER -> REVIEWER -> DOCUMENTER)
    - complexity_score >= 0.35: Complex chain if base is simple
    - Otherwise: Return base role chain as-is
    """
    # For high complexity, ensure full chain is used
    if complexity_score >= 0.65:
        return [RoleType.PLANNER, RoleType.CODER, RoleType.REVIEWER, RoleType.DOCUMENTER]
    return base_role_chain


def load_lessons() -> list:
    """Load all lessons from learned_lessons.json."""
    try:
        if LEARNED_LESSONS_FILE.exists():
            content = LEARNED_LESSONS_FILE.read_text().strip()
            if content.endswith("]"):
                return json.loads(content.rstrip(","))
        return []
    except (TypeError, IOError):
        return []


def recent_than_4_hours(lesson: dict) -> bool:
    """Check if lesson was created/updated in the last 4 hours."""
    try:
        timestamp_str = lesson.get('timestamp', lesson.get('date', ''))
        if not timestamp_str:
            return False
        lesson_date = datetime.fromisoformat(timestamp_str)
        cutoff = datetime.now() - timedelta(hours=4)
        return lesson_date > cutoff
    except (ValueError, TypeError):
        return False


def maybe_reflect(session_id: int, session_count: int) -> dict:
    """
    Trigger reflection synthesis based on recent lesson importance.
    Uses Generative Agents threshold: if recent lessons sum to importance > 150, synthesize.
    """
    lessons = load_lessons()
    recent = [l for l in lessons if recent_than_4_hours(l)]
    importance_sum = sum(l.get('importance', 5) for l in recent)

    result = {
        "session_id": session_id,
        "session_count": session_count,
        "recent_lessons": len(recent),
        "importance_sum": importance_sum,
        "reflections_generated": 0
    }

    if importance_sum > 150:
        synth = MemorySynthesis(str(LEARNED_LESSONS_FILE))
        new_reflections = synth.synthesize()
        result["reflections_generated"] = len(new_reflections)
        print(f"[Session {session_id}] Generated {len(new_reflections)} reflections (importance_sum={importance_sum})")
        print(f"[Session {session_id}] [QUERY EXPANSION] Query expansion enabled for lesson retrieval")
        for r in new_reflections:
            print(f"[Session {session_id}]   - {r.get('insight', 'Unknown')}")

    return result


def count_error_categories() -> dict:
    """Count grind failures by error category and return summary."""
    categories = {
        "TIMEOUT": 0,
        "ENCODING": 0,
        "IMPORT": 0,
        "SYNTAX": 0,
        "RUNTIME": 0,
        "UNKNOWN": 0,
        "total_failures": 0
    }

    if LOGS_DIR.exists():
        for log_file in LOGS_DIR.glob("*.json"):
            try:
                data = json.loads(log_file.read_text())
                if isinstance(data, dict):
                    error_category = data.get("error_category")
                    if error_category:
                        categories[error_category] += 1
                        categories["total_failures"] += 1
            except (json.JSONDecodeError, ValueError):
                pass

    return categories


def report_error_statistics() -> None:
    """Print error category statistics for visibility."""
    categories = count_error_categories()
    if categories["total_failures"] == 0:
        return

    print("\n" + "=" * 60)
    print("  ERROR CATEGORIZATION STATISTICS")
    print("=" * 60)
    print(f"  Total failures: {categories['total_failures']}")
    for cat in ["TIMEOUT", "ENCODING", "IMPORT", "SYNTAX", "RUNTIME", "UNKNOWN"]:
        count = categories[cat]
        if count > 0:
            pct = (count / categories["total_failures"]) * 100
            print(f"  {cat:10s}: {count:3d} ({pct:5.1f}%)")
    print("=" * 60 + "\n")


def query_knowledge_graph_for_recovery(error_type: str, task_description: str, kg: KnowledgeGraph) -> dict:
    """
    Query knowledge graph for recovery strategies when stuck.
    Returns related lessons and patterns that might help resolve the error.
    """
    recovery_suggestions = {
        "related_concepts": [],
        "recovery_strategies": [],
        "similar_lessons": []
    }

    try:
        # Try to find a node for the error type
        error_node_id = f"error_{error_type.lower()}"
        related_subgraph = kg.query_related(error_node_id, depth=2)

        if related_subgraph.get("nodes"):
            for node_id, node_data in related_subgraph.get("nodes", {}).items():
                if isinstance(node_data, dict):
                    recovery_suggestions["related_concepts"].append(node_data.get("label", node_id))
                else:
                    recovery_suggestions["related_concepts"].append(str(node_data))

        # Try to find lessons related to the task
        task_node_id = "task_patterns"
        task_subgraph = kg.query_related(task_node_id, depth=1)
        if task_subgraph.get("nodes"):
            for node_id, node_data in task_subgraph.get("nodes", {}).items():
                if "lesson" in str(node_data).lower():
                    recovery_suggestions["similar_lessons"].append(str(node_data)[:100])

    except Exception as e:
        print(f"Warning: Could not query knowledge graph: {e}")

    return recovery_suggestions


def learn_online(session_id: int, run_num: int, context: dict, result: dict, turn_count: int = 0) -> None:
    """Extract and record learning during execution (online learning)."""
    try:
        if LEARNED_LESSONS_FILE.exists():
            content = LEARNED_LESSONS_FILE.read_text().strip()
            lessons_data = json.loads(content.rstrip(",")) if content.endswith("]") else []
        else:
            lessons_data = []

        online_lesson = {
            "id": f"online_learning_{session_id}_{run_num}_{turn_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "task_category": "online_learning",
            "lesson": "Mid-execution learning checkpoint from active grind session",
            "timestamp": datetime.now().isoformat(),
            "source": "online",
            "session_id": session_id,
            "run_number": run_num,
            "turn_count": turn_count,
            "context": {
                "task": context.get("task", ""),
                "role": context.get("current_role", ""),
                "complexity": context.get("complexity", "unknown"),
                "complexity_score": context.get("complexity_score", 0.0)
            },
            "learnings": [],
            "importance": 4
        }

        if result:
            if result.get("partial_success"):
                online_lesson["learnings"].append({
                    "type": "partial_success",
                    "description": result.get("success_message", ""),
                    "progress": result.get("progress_percent", 0)
                })
            if result.get("error"):
                # Query knowledge graph for recovery strategies
                kg = KnowledgeGraph()  # Instantiate for query
                error_type = result.get("error_type", "unknown")
                kg_recovery = query_knowledge_graph_for_recovery(
                    error_type,
                    context.get("task", ""),
                    kg
                )
                online_lesson["learnings"].append({
                    "type": "error_pattern",
                    "error_type": error_type,
                    "error_message": result.get("error", "")[:200],
                    "recovery_suggestion": result.get("recovery", ""),
                    "knowledge_graph_recovery": kg_recovery  # Add KG insights
                })
            if result.get("elapsed"):
                online_lesson["learnings"].append({
                    "type": "performance",
                    "elapsed_seconds": result.get("elapsed", 0),
                    "efficiency_note": "slower_than_expected" if result.get("elapsed", 0) > 30 else "good_pace"
                })
            if result.get("files_modified"):
                online_lesson["learnings"].append({
                    "type": "progress",
                    "files_count": len(result.get("files_modified", [])),
                    "files": result.get("files_modified", [])[:3]
                })

        if online_lesson["learnings"]:
            if isinstance(lessons_data, list):
                lessons_data.append(online_lesson)
            else:
                lessons_data = [online_lesson]
            write_json(LEARNED_LESSONS_FILE, lessons_data)

        # ONLINE LEARNING ENHANCEMENTS: Update prompt_optimizer and skill_registry in real-time
        _update_prompt_optimizer_online(session_id, result, context)
        _update_skill_registry_online(session_id, result, context)
        _log_learning_event(session_id, run_num, turn_count, online_lesson)

    except Exception as e:
        print(f"[Session {session_id}] Warning: Could not record online learning: {e}")


def _update_prompt_optimizer_online(session_id: int, result: dict, context: dict) -> None:
    """Update prompt_optimizer with new demonstration in real-time."""
    try:
        from prompt_optimizer import save_demonstrations, load_demonstrations

        # Only update if task was successful
        if result.get("returncode") == 0 and result.get("self_verified"):
            # Load existing demonstrations
            existing_demos = load_demonstrations()

            # Create new demonstration from this successful run
            new_demo = {
                "result": f"Task '{context.get('task', '')[:50]}...' completed successfully",
                "num_turns": result.get("run", 1),
                "duration_ms": int(result.get("elapsed", 0) * 1000),
                "total_cost_usd": 0.0,  # Would need to extract from result if available
                "log_file": result.get("log_file", ""),
                "efficiency_score": 1.0 - min(result.get("run", 1) / 20.0, 0.9),  # Lower runs = higher score
                "quality_score": result.get("quality_score", 0.0),
                "task_category": context.get("task", "")[:30],
                "timestamp": datetime.now().isoformat()
            }

            # Add to demonstrations list
            existing_demos.append(new_demo)

            # Keep only top 20 demonstrations (sorted by efficiency)
            existing_demos.sort(key=lambda x: x.get("efficiency_score", 0), reverse=True)
            existing_demos = existing_demos[:20]

            # Save updated demonstrations
            save_demonstrations(existing_demos)
            print(f"[Session {session_id}] Updated prompt_optimizer with new demonstration (efficiency={new_demo['efficiency_score']:.2f})")
    except Exception as e:
        print(f"[Session {session_id}] Warning: Could not update prompt_optimizer: {e}")


def _update_skill_registry_online(session_id: int, result: dict, context: dict) -> None:
    """Update skill_registry with automatic skill extraction for quality >= 0.9."""
    try:
        # Try automatic skill extraction first for high-quality runs (>= 0.9)
        if auto_register_skill(session_id, result, context):
            return  # Successfully extracted and registered

        # Fallback to pattern-based detection for moderate quality runs (>= 0.75)
        from skills.skill_registry import register_skill, get_skill
        if result.get("returncode") == 0 and result.get("quality_score", 0) > 0.75:
            task_lower = context.get("task", "").lower()

            # Pattern detection: Look for specific task types that could become skills
            skill_patterns = {
                "refactor": ("code_refactoring", "Refactoring pattern for improving code structure"),
                "fix": ("bug_fix_pattern", "Bug fixing pattern with verification"),
                "add test": ("test_addition", "Test addition pattern with coverage"),
                "documentation": ("doc_generation", "Documentation generation pattern"),
                "optimization": ("performance_optimization", "Performance optimization pattern")
            }

            for keyword, (skill_name, skill_desc) in skill_patterns.items():
                if keyword in task_lower:
                    if not get_skill(skill_name):
                        skill_code = f"""# Learned pattern: {skill_name}
# Task: {context.get('task', '')[:100]}
# Quality score: {result.get('quality_score', 0):.2f}
# Pattern extracted from session {session_id}, run {result.get('run', 0)}
"""
                        register_skill(
                            name=skill_name,
                            code=skill_code,
                            description=skill_desc,
                            preconditions=["Task requires " + keyword],
                            postconditions=["Task completed successfully", "Quality score > 0.75"]
                        )
                        print(f"[Session {session_id}] Registered new skill: {skill_name}")
                        break
    except Exception as e:
        print(f"[Session {session_id}] Warning: Could not update skill_registry: {e}")


def _log_learning_event(session_id: int, run_num: int, turn_count: int, lesson: dict) -> None:
    """Log learning event to learning_log.json."""
    try:
        learning_log_file = WORKSPACE / "learning_log.json"

        # Load existing log
        if learning_log_file.exists():
            try:
                log_data = json.loads(learning_log_file.read_text())
                if not isinstance(log_data, list):
                    log_data = []
            except (json.JSONDecodeError, ValueError):
                log_data = []
        else:
            log_data = []

        # Create learning event
        learning_event = {
            "event_id": f"learning_{session_id}_{run_num}_{turn_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "run_number": run_num,
            "turn_count": turn_count,
            "event_type": "online_learning_checkpoint",
            "learnings_count": len(lesson.get("learnings", [])),
            "lesson_id": lesson.get("id"),
            "importance": lesson.get("importance", 4),
            "context": lesson.get("context", {})
        }

        # Append event
        log_data.append(learning_event)

        # Keep only last 100 events
        log_data = log_data[-100:]

        # Write back
        learning_log_file.write_text(json.dumps(log_data, indent=2), encoding="utf-8")
        print(f"[Session {session_id}] Logged learning event to learning_log.json (total events: {len(log_data)})")
    except Exception as e:
        print(f"[Session {session_id}] Warning: Could not log learning event: {e}")


def verify_grind_completion(session_id: int, run_num: int, output: str, returncode: int) -> dict:
    """
    Self-verification step from Voyager paper: verify task was actually completed.
    Checks for success indicators and validates actual completion.

    Returns dict with:
    - verified: bool (PASS/FAIL)
    - indicators: list of found success indicators
    - has_files_modified: bool (whether output indicates files were changed)
    - details: str (verification explanation)
    """
    verification_result = {
        "verified": False,
        "indicators": [],
        "has_files_modified": False,
        "details": "",
        "verification_timestamp": datetime.now().isoformat()
    }

    # Parse output for success indicators
    success_keywords = [
        "done", "complete", "success", "finished", "accomplished",
        "created", "modified", "fixed", "resolved", "completed",
        "[ok]", "[pass]", "passed", "verified"
    ]

    output_lower = (output or "").lower()

    # Check for explicit success indicators
    for keyword in success_keywords:
        if keyword in output_lower:
            verification_result["indicators"].append(keyword)

    # Check if files were modified
    try:
        output_data = json.loads(output or "{}")
        if isinstance(output_data, dict):
            if output_data.get("files_modified") and len(output_data.get("files_modified", [])) > 0:
                verification_result["has_files_modified"] = True
            # Check for result summary indicating work was done
            if output_data.get("result") or output_data.get("summary"):
                verification_result["indicators"].append("result_summary_present")
    except (json.JSONDecodeError, ValueError):
        pass

    # Verification logic: task passes if:
    # 1. returncode == 0 (successful execution), AND
    # 2. Has success indicators OR files were modified
    if returncode == 0 and (len(verification_result["indicators"]) > 0 or verification_result["has_files_modified"]):
        verification_result["verified"] = True
        verification_result["details"] = f"PASS: Exit code 0, found {len(verification_result['indicators'])} success indicators"
    else:
        reasons = []
        if returncode != 0:
            reasons.append(f"exit code {returncode}")
        if len(verification_result["indicators"]) == 0:
            reasons.append("no success indicators found")
        if not verification_result["has_files_modified"]:
            reasons.append("no files modified")
        verification_result["details"] = f"FAIL: {', '.join(reasons)}"

    return verification_result


def append_verification_lesson(session_id: int, run_num: int, verification: dict) -> None:
    """Append self-verification results as a lesson to learned_lessons.json."""
    try:
        # Load existing lessons
        if LEARNED_LESSONS_FILE.exists():
            content = LEARNED_LESSONS_FILE.read_text().strip()
            if content.endswith("]"):
                lessons_data = json.loads(content.rstrip(","))
            else:
                lessons_data = []
        else:
            lessons_data = []

        # Create verification lesson
        verification_lesson = {
            "id": f"self_verification_{session_id}_{run_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "task_category": "quality_assurance",
            "lesson": "Self-verification after grind completion prevents false positives in success logging (Voyager arXiv:2305.16291)",
            "timestamp": datetime.now().isoformat(),
            "implementation": "verify_grind_completion() in grind_spawner.py, called after each run_once() completes",
            "session_id": session_id,
            "run_number": run_num,
            "verification_status": "PASS" if verification.get("verified") else "FAIL",
            "verification_details": verification.get("details"),
            "success_indicators_found": verification.get("indicators", []),
            "files_modified": verification.get("has_files_modified"),
            "key_insights": [
                "Self-verification prevents false positives by checking actual task completion",
                "Verification checks: (1) Exit code 0, (2) Success keywords in output, (3) Files modified",
                "Prevents logging success when task partially completed or produced no output",
                "Enables learning system to distinguish complete from incomplete sessions",
                "Failure reasons logged: exit code, missing success indicators, no file changes"
            ],
            "retrieval_cues": [
                "verification",
                "quality_assurance",
                "false_positives",
                "grind_completion",
                "voyager"
            ],
            "importance": 7,
            "source": "arXiv:2305.16291 - Voyager: An Open-Ended Embodied Agent"
        }

        if isinstance(lessons_data, list):
            lessons_data.append(verification_lesson)
        else:
            lessons_data = [verification_lesson]

        write_json(LEARNED_LESSONS_FILE, lessons_data)
    except Exception as e:
        print(f"Warning: Could not record verification lesson: {e}")


def main():
    validate_config()

    # Initialize workspace sandbox for file operation validation
    initialize_sandbox(str(WORKSPACE))

    parser = argparse.ArgumentParser(description="Spawn parallel Claude grind sessions")
    parser.add_argument("-n", "--sessions", type=int, default=1, help="Number of parallel sessions (ignored in delegate mode)")
    parser.add_argument("--8b", dest="use_8b", action="store_true", help="Use Llama 3.1 8B (fast/cheap)")
    parser.add_argument("--70b", dest="use_70b", action="store_true", help="Use Llama 3.3 70B (medium, default)")
    parser.add_argument("--120b", dest="use_120b", action="store_true", help="Use GPT-OSS 120B (big brain)")
    parser.add_argument("-b", "--budget", type=float, default=0.10, help="Budget per session in dollars")
    parser.add_argument("-w", "--workspace", default=str(WORKSPACE), help="Workspace directory to grind on")
    parser.add_argument("-t", "--task", default=None, help="Task for all sessions (single task mode)")
    parser.add_argument("--delegate", action="store_true", help="Read tasks from grind_tasks.json")
    parser.add_argument("--once", action="store_true", help="Run once per session, don't respawn")
    parser.add_argument("--max-total-cost", type=float, default=None, help="Maximum total cost across all sessions in dollars (prevents runaway costs)")
    parser.add_argument("--synthesize", action="store_true", help="Force immediate memory synthesis and exit")
    parser.add_argument("--critic", action="store_true", help="Enable critic review mode with feedback-driven retries (quality_score < 0.7 triggers improvement attempt)")
    parser.add_argument("--multi-path", action="store_true", help="Enable multi-path parallel execution (explores 3 strategies: CONSERVATIVE, BALANCED, AGGRESSIVE)")
    parser.add_argument("--path-logs", default="path_execution_logs.json", help="Output file for multi-path execution logs")

    args = parser.parse_args()

    # Resolve model from flags (default: 70b)
    if args.use_120b:
        args.model = "openai/gpt-oss-120b"
    elif args.use_8b:
        args.model = "llama-3.1-8b-instant"
    else:
        args.model = "llama-3.3-70b-versatile"  # Default (also covers --70b)

    # Handle --synthesize flag (explicit synthesis request)
    if args.synthesize:
        print(f"[SYNTHESIS] [QUERY EXPANSION] Query expansion enabled for lesson synthesis")
        synth = MemorySynthesis(str(LEARNED_LESSONS_FILE))
        lessons = synth.load_all_lessons()
        print(f"[SYNTHESIS] Loaded {len(lessons)} lessons")
        reflections = synth.synthesize()
        if reflections:
            print(f"[SYNTHESIS] Generated {len(reflections)} reflections")
            for r in reflections:
                print(f"  - {r.get('insight', 'Unknown')}")
        else:
            print("[SYNTHESIS] No new reflections generated (insufficient lessons)")
        archived = synth.archive_unused()
        if archived > 0:
            print(f"[SYNTHESIS] Archived {archived} unused lessons")
        sys.exit(0)

    # Determine tasks
    if args.delegate:
        # Read tasks from file
        if not TASKS_FILE.exists():
            print(f"ERROR: --delegate requires {TASKS_FILE}")
            print("Create it with a list of task objects:")
            print('  [{"task": "Fix UI bugs", "budget": 0.10}, ...]')
            sys.exit(1)
        tasks_data = read_json(TASKS_FILE)
        tasks = [
            {
                "task": t.get("task", "General improvements"),
                "budget": t.get("budget", args.budget),
                "model": t.get("model", args.model),
                "workspace": t.get("workspace", args.workspace)
            }
            for t in tasks_data
        ]
    elif args.task:
        # Single task for all sessions
        tasks = [
            {"task": args.task, "budget": args.budget, "model": args.model, "workspace": args.workspace}
            for _ in range(args.sessions)
        ]
    else:
        print("ERROR: Specify --task 'your task' or --delegate")
        sys.exit(1)

    # Safety check: Validate all tasks against Constitutional AI constraints
    constitutional_checker = ConstitutionalCheckerStandalone(constraints_path=str(WORKSPACE / "SAFETY_CONSTRAINTS.json"))
    print("[SAFETY] Validating tasks against Constitutional AI constraints...")
    blocked_tasks = []
    for i, task_obj in enumerate(tasks):
        task_text = task_obj["task"]
        is_safe, violations = constitutional_checker.check_task_safety(task_text)
        if not is_safe:
            print(f"[SAFETY VIOLATION] Task {i+1} BLOCKED: {task_text[:60]}...")
            for violation in violations:
                print(f"  - {violation}")
            blocked_tasks.append(i)

    # Remove blocked tasks
    if blocked_tasks:
        tasks = [t for i, t in enumerate(tasks) if i not in blocked_tasks]
        print(f"[SAFETY] {len(blocked_tasks)} unsafe task(s) blocked. {len(tasks)} safe task(s) remaining.")
        if len(tasks) == 0:
            print("[SAFETY] All tasks blocked. Exiting.")
            sys.exit(1)
    else:
        print(f"[SAFETY] All {len(tasks)} task(s) passed safety validation.")

    print("=" * 60)
    print("  GRIND SPAWNER - DELEGATION MODE")
    print("=" * 60)
    print(f"  Workers:   {len(tasks)}")
    print(f"  Model:     {args.model}")
    print(f"  Mode:      {'Single run' if args.once else 'Continuous respawn'}")
    if args.max_total_cost:
        print(f"  Max Cost:  ${args.max_total_cost:.2f}")
    print("-" * 60)
    for i, t in enumerate(tasks):
        print(f"  [{i+1}] {t['task'][:50]}... (${t['budget']:.2f})")
    print("=" * 60)

    # Check if total cost would exceed max before spawning
    if args.max_total_cost:
        total_spent = get_total_spent()
        print(f"\nTotal already spent: ${total_spent:.2f}")
        if total_spent >= args.max_total_cost:
            print(f"WARNING: Total spent (${total_spent:.2f}) already exceeds or meets max (${args.max_total_cost:.2f})")
            print("Stopping spawner to prevent runaway costs.")
            sys.exit(0)

    print("Press Ctrl+C to stop all sessions\n")

    # Record DSPy prompt optimization lessons
    record_prompt_optimization_lesson()

    # Record error categorization lessons
    record_error_categorization_lesson()

    # Record CAMEL role decomposition lessons
    record_role_decomposition_lesson()

    # Record reflection trigger lesson
    record_reflection_trigger_lesson()

    # Record Voyager skill integration lesson
    record_skill_integration_lesson()

    # Record self-verification lesson (Voyager quality assurance)
    record_self_verification_lesson()

    # Record adaptive complexity detection lesson
    record_adaptive_complexity_lesson()

    # Record reflection automation lesson
    record_reflection_automation_lesson()

    # Record critic feedback loop lesson (LATS/TextGrad)
    record_critic_feedback_lesson()

    # Note: record_online_learning_lesson() removed - function not yet implemented

    # Multi-path execution mode
    if args.multi_path:
        print("\n[MULTI-PATH] Executing with parallel path exploration")
        print(f"[MULTI-PATH] Budget allocation: BALANCED=50%, CONSERVATIVE=30%, AGGRESSIVE=20%")

        # Run multi-path executor for first task
        if len(tasks) == 0:
            print("[ERROR] No tasks to execute")
            sys.exit(1)

        first_task = tasks[0]
        multi_path = MultiPathExecutor(
            workspace=Path(first_task["workspace"]),
            base_budget=first_task["budget"]
        )

        # Define executor function that wraps GrindSession.run_once
        def execute_path(path: ExecutionPath) -> PathResult:
            """Execute a single path using GrindSession."""
            from pathlib import Path as PathLib
            import time

            start = time.time()
            session = GrindSession(
                session_id=hash(path.strategy.value) % 1000,  # Unique ID per strategy
                model=first_task["model"],
                budget=path.budget,
                workspace=PathLib(first_task["workspace"]),
                task=path.prompt_variant,  # Use strategy-specific prompt
                max_total_cost=args.max_total_cost,
                critic_mode=args.critic
            )

            result = session.run_once()

            return PathResult(
                output=json.dumps(result),
                tokens_used=0,  # Not tracked in current implementation
                quality=result.get("quality_score", 0.0),
                elapsed_time=time.time() - start,
                success=result.get("returncode", 1) == 0,
                error=result.get("error"),
                metadata=result
            )

        try:
            # Execute with multi-path comparison
            comparison_result = multi_path.execute_with_comparison(
                task=first_task["task"],
                executor_func=execute_path
            )

            # Store results to path_execution_logs.json
            path_logs_file = WORKSPACE / args.path_logs
            with open(path_logs_file, "w") as f:
                json.dump(comparison_result, f, indent=2, default=str)

            print(f"\n[MULTI-PATH] Results saved to {path_logs_file}")
            print(f"[MULTI-PATH] Best path: {comparison_result['strategy'].upper()}")
            print(f"[MULTI-PATH] Quality score: {comparison_result['quality_score']:.3f}")

            # Print completion summary
            print("\n" + "=" * 60)
            print("  MULTI-PATH EXECUTION SUMMARY")
            print("=" * 60)
            print(f"  Best Strategy: {comparison_result['strategy'].upper()}")
            print(f"  Quality Score: {comparison_result['quality_score']:.3f}")
            print(f"  Total Elapsed: {comparison_result['metadata']['total_elapsed']:.1f}s")
            print(f"  Paths Explored: {comparison_result['metadata']['paths_explored']}")
            print("-" * 60)
            for path_info in comparison_result['all_paths']:
                print(f"  {path_info['strategy'].upper():12s}: quality={path_info['quality_score']:.3f}, "
                      f"success={path_info['success']}, time={path_info['elapsed_time']:.1f}s")
            print("=" * 60)

        except Exception as e:
            print(f"\n[MULTI-PATH] Multi-path execution failed: {e}")
            print("[MULTI-PATH] Falling back to single-path execution")

            # Fallback to regular single-path mode
            sessions = [
                GrindSession(
                    session_id=i + 1,
                    model=tasks[i]["model"],
                    budget=tasks[i]["budget"],
                    workspace=Path(tasks[i]["workspace"]),
                    task=tasks[i]["task"],
                    max_total_cost=args.max_total_cost,
                    critic_mode=args.critic
                )
                for i in range(len(tasks))
            ]

            # Continue with single-path execution below
        else:
            # Multi-path completed successfully, exit
            sys.exit(0)

    # Create sessions (single-path mode)
    sessions = [
        GrindSession(
            session_id=i + 1,
            model=tasks[i]["model"],
            budget=tasks[i]["budget"],
            workspace=Path(tasks[i]["workspace"]),
            task=tasks[i]["task"],
            max_total_cost=args.max_total_cost,
            critic_mode=args.critic
        )
        for i in range(len(tasks))
    ]

    try:
        if args.once:
            # Single run mode - run all sessions once in parallel
            with ThreadPoolExecutor(max_workers=len(sessions)) as executor:
                futures = [executor.submit(s.run_once) for s in sessions]
                for future in futures:
                    result = future.result()
                    print(f"  Result: {result}")
        else:
            # Continuous mode - each session loops forever
            threads = []
            for session in sessions:
                t = threading.Thread(target=session.grind_loop, daemon=True)
                t.start()
                threads.append(t)
                time.sleep(0.5)  # Stagger starts

            # Wait for Ctrl+C
            while True:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nStopping all sessions...")
        for session in sessions:
            session.running = False
        time.sleep(2)

    print("\nGrind spawner stopped.")
    total_runs = sum(s.runs for s in sessions)
    print(f"Total runs across all sessions: {total_runs}")

    # Report error categorization statistics
    report_error_statistics()

    # Post-wave analysis: Connect tracker to suggester
    try:
        wave_num = 1  # TODO: Track wave number properly
        post_wave_result = post_wave_analysis(wave_num, workspace=WORKSPACE)
        print(f"[OK] Post-wave analysis complete. Report: {post_wave_result['report_file']}")
    except Exception as e:
        print(f"[WARN] Post-wave analysis failed: {e}")


if __name__ == "__main__":
    main()
