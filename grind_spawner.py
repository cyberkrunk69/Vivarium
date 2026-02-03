"""
Grind Spawner - Spawn parallel Claude sessions with delegated tasks

Usage:
    # Single task mode
    python grind_spawner.py --sessions 5 --model opus --budget 0.10 --task "Fix all UI bugs"

    # Delegation mode (reads tasks from tasks.json)
    python grind_spawner.py --delegate --model opus --budget 0.10

    # Target a specific repo
    python grind_spawner.py --task "Add documentation" --workspace D:/some/repo

Each session runs autonomously until complete, then respawns with same task.
Press Ctrl+C to stop all sessions.
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

# Configuration
WORKSPACE = Path(__file__).parent
LOGS_DIR = WORKSPACE / "grind_logs"
TASKS_FILE = WORKSPACE / "grind_tasks.json"
LEARNED_LESSONS_FILE = WORKSPACE / "learned_lessons.json"

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

class GrindSession:
    """Manages a single Claude grind session."""

    def __init__(self, session_id: int, model: str, budget: float, workspace: Path, task: str, max_total_cost: float = None, synthesis_interval: int = 5, critic_mode: bool = False):
        self.session_id = session_id
        self.model = model
        self.budget = budget
        self.workspace = workspace
        self.task = task
        self.runs = 0
        self.total_cost = 0.0
        self.running = True
        self.max_total_cost = max_total_cost
        self.synthesis_interval = synthesis_interval  # Default: synthesize every N sessions
        self.critic_mode = critic_mode  # Enable critic feedback loop when True
        self.task_decomposition = decompose_task(task)

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

        # Initialize Knowledge Graph and populate from codebase
        self.kg = KnowledgeGraph()
        self.kg.populate_from_codebase(str(self.workspace))

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

        # Retrieve relevant skill from skill_registry
        skill_injection = ""
        skill = retrieve_skill(self.task)
        if skill:
            skill_name = skill.get('name', 'Unknown')
            skill_code = skill.get('code', '')
            skill_injection = f"""
{'='*60}
VOYAGER SKILL INJECTION (arXiv:2305.16291)
{'='*60}

RELEVANT SKILL: {skill_name}

{skill_code}

{'='*60}
"""
            print(f"[Session {self.session_id}] Retrieved skill: {skill_name}")

        # Query Knowledge Graph for context
        kg_context_injection = ""
        try:
            # Query related concepts for current task from KG
            related_subgraph = self.kg.query_related(f"class:grind_spawner.py:GrindSession", depth=2)

            if related_subgraph and related_subgraph.get("nodes"):
                kg_nodes = list(related_subgraph.get("nodes", {}).keys())[:5]
                kg_context_injection = f"""
{'='*60}
KNOWLEDGE GRAPH CONTEXT
{'='*60}
Related concepts from codebase analysis:
"""
                for node_id in kg_nodes:
                    node_data = related_subgraph["nodes"][node_id]
                    if isinstance(node_data, dict):
                        kg_context_injection += f"\n  - {node_data.get('label', node_id)} ({node_data.get('type', 'unknown')})"
                    else:
                        kg_context_injection += f"\n  - {node_id}"
                kg_context_injection += f"\n{'='*60}\n"
                print(f"[Session {self.session_id}] Injected knowledge graph context with {len(kg_nodes)} related concepts")
        except Exception as e:
            print(f"[Session {self.session_id}] Warning: Could not query knowledge graph: {e}")

        # Collect demonstrations and optimize with DSPy if available
        all_demonstrations = collect_demonstrations(LOGS_DIR)
        relevant_demos = get_relevant_demonstrations(self.task, all_demonstrations, top_k=3)

        # Combine: CAMEL + Skill Injection + KG Context + DSPy optimization
        combined_prompt = camel_injection + skill_injection + kg_context_injection
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
                # Build claude command
                # Using -p flag for non-interactive mode, piping prompt via stdin
                cmd = [
                    "claude",
                    "-p",
                    "--model", self.model,
                    "--dangerously-skip-permissions",
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
                if result.returncode != 0:
                    error_category = self._categorize_error("execution", result.stderr, result.stdout, result.stderr)
                    output_data["error_category"] = error_category
                    print(f"[Session {self.session_id}] Run #{self.runs} categorized as: {error_category}")

                log_file.write_text(json.dumps(output_data), encoding="utf-8")

                elapsed = (datetime.now() - start_time).total_seconds()
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

                    # If critic mode enabled and quality score below threshold, trigger feedback-driven retry
                    if self.critic_mode and critic_quality_score < 0.7 and critic_retry_count < 1:
                        print(f"[Session {self.session_id}] [CRITIC RETRY] Quality score {critic_quality_score:.2f} < 0.7 threshold, triggering improvement attempt")
                        improvement_suggestions = "\n".join(critic_review.get('feedback', []))
                        print(f"[Session {self.session_id}] [Session {self.session_id}] Critic retry with feedback")
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
                        print(f"[Session {self.session_id}] Retrying with enhanced prompt (critic attempt {critic_retry_count}/1)")
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
                return {"session_id": self.session_id, "run": self.runs, "error": "timeout", "error_category": error_category}
            except Exception as e:
                error_message = str(e)
                error_category = self._categorize_error("execution", error_message)
                print(f"[Session {self.session_id}] Run #{self.runs} error ({error_category}): {e}")
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

    def grind_loop(self):
        """Continuously run grind sessions until stopped."""
        synth = MemorySynthesis(str(LEARNED_LESSONS_FILE))

        while self.running:
            # Check max total cost before spawning new session
            if self.max_total_cost:
                total_spent = get_total_spent()
                if total_spent >= self.max_total_cost:
                    print(f"[Session {self.session_id}] WARNING: Total cost (${total_spent:.2f}) reached max (${self.max_total_cost:.2f})")
                    print(f"[Session {self.session_id}] Stopping to prevent runaway costs")
                    self.running = False
                    break

            result = self.run_once()

            if not self.running:
                break

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

            # Brief pause between runs
            print(f"[Session {self.session_id}] Respawning in 2s...")
            time.sleep(2)

        print(f"[Session {self.session_id}] Stopped after {self.runs} runs")


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
        base_model: Original model selection (haiku, sonnet, opus)
        complexity_score: Float 0.0-1.0 from decompose_task()

    Returns:
        Adapted model name

    Logic:
    - complexity_score < 0.35: Keep base_model (simple tasks)
    - 0.35 <= complexity_score < 0.65: Upgrade to sonnet if haiku (moderate complexity)
    - 0.65 <= complexity_score < 0.85: Upgrade to opus (high complexity)
    - 0.85 <= complexity_score: Prefer opus (very high complexity)
    """
    if complexity_score >= 0.85:
        return "opus"  # Very complex tasks need best model
    elif complexity_score >= 0.65:
        return "opus"  # High complexity -> opus
    elif complexity_score >= 0.35:
        if base_model == "haiku":
            return "sonnet"  # Moderate complexity -> at least sonnet
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

    except Exception as e:
        print(f"[Session {session_id}] Warning: Could not record online learning: {e}")



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
    parser = argparse.ArgumentParser(description="Spawn parallel Claude grind sessions")
    parser.add_argument("-n", "--sessions", type=int, default=1, help="Number of parallel sessions (ignored in delegate mode)")
    parser.add_argument("-m", "--model", default="haiku", help="Model: haiku (default, cheapest), sonnet, opus")
    parser.add_argument("-b", "--budget", type=float, default=0.10, help="Budget per session in dollars")
    parser.add_argument("-w", "--workspace", default=str(WORKSPACE), help="Workspace directory to grind on")
    parser.add_argument("-t", "--task", default=None, help="Task for all sessions (single task mode)")
    parser.add_argument("--delegate", action="store_true", help="Read tasks from grind_tasks.json")
    parser.add_argument("--once", action="store_true", help="Run once per session, don't respawn")
    parser.add_argument("--max-total-cost", type=float, default=None, help="Maximum total cost across all sessions in dollars (prevents runaway costs)")
    parser.add_argument("--synthesize", action="store_true", help="Force immediate memory synthesis and exit")
    parser.add_argument("--critic", action="store_true", help="Enable critic review mode with feedback-driven retries (quality_score < 0.7 triggers improvement attempt)")

    args = parser.parse_args()

    # Handle --synthesize flag (explicit synthesis request)
    if args.synthesize:
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

    # Create sessions
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


if __name__ == "__main__":
    main()
