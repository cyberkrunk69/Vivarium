"""
Lesson Recording Module - Extracted from grind_spawner.py

Centralizes all lesson recording functions for learned_lessons.json.
Provides a single parameterized interface: record_lesson(category, lesson_text, key_insights, source)
"""

import json
from pathlib import Path
from datetime import datetime
from memory_synthesis import MemorySynthesis

# Configuration
WORKSPACE = Path(__file__).parent
LEARNED_LESSONS_FILE = WORKSPACE / "learned_lessons.json"

# Initialize MemorySynthesis for embedding computation
_memory_synth = MemorySynthesis()


def record_lesson(category: str, lesson_text: str, key_insights: list, source: str,
                  additional_fields: dict = None) -> None:
    """
    Parameterized lesson recording function - centralizes all lesson recording logic.

    Args:
        category: Task category for the lesson (e.g., "prompt_optimization", "error_analysis")
        lesson_text: Main lesson description
        key_insights: List of insight strings
        source: Citation source (e.g., "arXiv:2310.03714")
        additional_fields: Optional dict with extra fields (id, implementation, etc.)
    """
    try:
        # Load existing lessons
        if LEARNED_LESSONS_FILE.exists():
            content = LEARNED_LESSONS_FILE.read_text().strip()
            lessons_data = json.loads(content.rstrip(",")) if content.endswith("]") else []
        else:
            lessons_data = []

        # Build base lesson object
        new_lesson = {
            "id": additional_fields.get("id", f"{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}") if additional_fields else f"{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "task_category": category,
            "lesson": lesson_text,
            "timestamp": datetime.now().isoformat(),
            "key_insights": key_insights,
            "source": source
        }

        # Compute and store embedding for semantic retrieval
        embedding = _memory_synth.compute_lesson_embedding(lesson_text)
        if embedding:
            new_lesson["embedding"] = embedding

        # Merge additional fields if provided
        if additional_fields:
            new_lesson.update(additional_fields)

        # Append to lessons
        if isinstance(lessons_data, list):
            lessons_data.append(new_lesson)
        else:
            lessons_data = [new_lesson]

        LEARNED_LESSONS_FILE.write_text(json.dumps(lessons_data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"Warning: Could not record lesson ({category}): {e}")


def record_prompt_optimization_lesson() -> None:
    """Append DSPy prompt optimization lessons to learned_lessons.json."""
    record_lesson(
        category="prompt_optimization",
        lesson_text="DSPy self-bootstrapping: collect successful demonstrations and inject into prompts",
        key_insights=[
            "Collect demonstrations from grind_logs/ - successful task completions",
            "Rank by efficiency: num_turns and duration_ms",
            "Inject 2-3 best examples into prompt before RULES section",
            "Expected improvement: 25-65% over standard few-shot (arXiv:2310.03714)",
            "DSPy insight: modules learn by creating and collecting demonstrations"
        ],
        source="arXiv:2310.03714",
        additional_fields={
            "id": f"dspy_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "prompt_optimizer.py integrated into grind_spawner.py"
        }
    )


def record_error_categorization_lesson() -> None:
    """Append error categorization lessons to learned_lessons.json."""
    record_lesson(
        category="error_analysis",
        lesson_text="Categorize grind failures into semantic categories for targeted improvements",
        key_insights=[
            "TIMEOUT: Session exceeded 600s time limit",
            "ENCODING: Unicode/charset issues (UTF, decode, encode errors)",
            "IMPORT: Missing module or import errors",
            "SYNTAX: Python syntax errors",
            "RUNTIME: Execution exceptions and failures",
            "UNKNOWN: Uncategorized or ambiguous errors",
            "Error categories enable pattern detection across multiple grind sessions",
            "Track category counts to identify systemic issues (e.g., too many TIMEOUT errors)"
        ],
        source="arXiv:2309.10025",
        additional_fields={
            "id": f"error_categorization_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "_categorize_error() method in GrindSession, error_category field in logs"
        }
    )


def record_role_decomposition_lesson() -> None:
    """Append CAMEL role-based task decomposition lessons to learned_lessons.json."""
    record_lesson(
        category="role_based_decomposition",
        lesson_text="CAMEL role-playing for autonomous cooperation via inception prompting",
        key_insights=[
            "Role-playing generates conversational behaviors for studying cooperation patterns (arXiv:2303.17760)",
            "Each role has specific system prompt, allowed tools, and handoff conditions",
            "Complex tasks routed to PLANNER first for decomposition into subtasks",
            "Simple tasks bypass PLANNER and go directly to CODER",
            "All completions pass through REVIEWER before finishing (mandatory review gate)",
            "Inception prompting: 'You are the {ROLE}. Your job is to {DESCRIPTION}. When done, hand off to {NEXT_ROLE}.'",
            "DOCUMENTER updates learned_lessons.json with patterns and insights from each task",
            "Role chain for complex tasks: PLANNER ->CODER ->REVIEWER ->DOCUMENTER",
            "Role chain for simple tasks: CODER ->REVIEWER ->DOCUMENTER"
        ],
        source="arXiv:2303.17760 - CAMEL: Communicative Agents for AI Language Model Exploration",
        additional_fields={
            "id": f"camel_role_decomposition_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "roles.py with RoleExecutor, integrated into grind_spawner.py",
            "role_definitions": {
                "PLANNER": "Breaks complex tasks into atomic subtasks, assigns to specialists, provides acceptance criteria",
                "CODER": "Implements code changes, follows existing patterns, edits existing files (no over-engineering)",
                "REVIEWER": "Validates code against requirements, checks security/bugs, approves or rejects with feedback",
                "DOCUMENTER": "Records lessons learned, patterns discovered, architectural decisions in JSON"
            }
        }
    )


def record_reflection_trigger_lesson() -> None:
    """Append reflection trigger synthesis lesson to learned_lessons.json."""
    record_lesson(
        category="memory_synthesis",
        lesson_text="Automatic reflection synthesis triggered by importance threshold (Generative Agents technique)",
        key_insights=[
            "Reflection synthesis consolidates lessons into higher-level insights automatically (arXiv:2304.03442)",
            "Trigger condition: sum of importance scores from recent lessons (< 4 hours) > 150",
            "Recent lessons defined as those created/updated in last 4 hours",
            "Each lesson has importance value (default 5), recent lessons contribute additively",
            "Reflection synthesis runs after each grind session completes (not just periodically)",
            "Dual trigger: maybe_reflect() runs always, periodic synthesis() runs every 10 sessions",
            "When triggered, MemorySynthesis.synthesize() creates higher-level reflections",
            "Reflections capture common themes and patterns across multiple lessons",
            "Reflections classified as level_1_pattern (single category) or level_2_principle (multiple categories)",
            "New reflections appended to learned_lessons.json and pruned for redundancy"
        ],
        source="arXiv:2304.03442 - Generative Agents: Interactive Simulacra of Human Behavior",
        additional_fields={
            "id": f"reflection_trigger_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "maybe_reflect() and helper functions in grind_spawner.py",
            "threshold_details": {
                "importance_sum_threshold": 150,
                "recency_window_hours": 4,
                "default_lesson_importance": 5,
                "synthesis_creates": "Higher-level insights from multiple similar lessons"
            }
        }
    )


def record_skill_integration_lesson() -> None:
    """Append Voyager skill integration lessons to learned_lessons.json."""
    record_lesson(
        category="skill_composition",
        lesson_text="Voyager compositional skill reuse for rapid capability compounding",
        key_insights=[
            "Voyager maintains ever-growing skill library of learned, interpretable, temporally extended skills (arXiv:2305.16291)",
            "Skills are retrieved by semantic matching on task description using embedding-based retrieval",
            "Embedding-based retrieval uses TF-IDF vectorization with fallback to keyword matching",
            "Retrieved skills injected into prompt context before task execution with RELEVANT SKILL section",
            "Skill injection enables compositional reuse: new tasks can leverage previously learned solutions",
            "Skill preconditions and postconditions enable validation of skill applicability",
            "Skill retrieval logged with session ID: [Session N] Retrieved skill: {name}",
            "Integration point: retrieve_skill(task_description) called during prompt generation in get_prompt()",
            "Skill code injected with clear section marker: VOYAGER SKILL INJECTION (arXiv:2305.16291)",
            "Skills compose multiple learned patterns to solve novel tasks without additional LLM training"
        ],
        source="arXiv:2305.16291 - Voyager: An Open-Ended Embodied Agent with Large Language Models",
        additional_fields={
            "id": f"voyager_skill_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "skill_registry.py integrated into grind_spawner.py get_prompt() method",
            "skill_retrieval_strategy": {
                "primary": "TF-IDF embedding cosine similarity (if sklearn available)",
                "fallback": "Keyword matching on skill names and descriptions",
                "min_similarity_threshold": 0.1
            }
        }
    )


def record_self_verification_lesson() -> None:
    """Append self-verification lesson framework to learned_lessons.json."""
    record_lesson(
        category="quality_assurance",
        lesson_text="Self-verification framework: Validate grind completion before logging success",
        key_insights=[
            "Self-verification from Voyager paper prevents false positives in autonomous learning systems",
            "After task completes, before logging success: parse result output for completion indicators",
            "Check for 'Done', 'Complete', 'Success' keywords and verify files were actually modified",
            "If verification fails, mark as partial completion and log reason for failure",
            "Verification happens before publishing to message pool, ensuring accurate learning signals",
            "Each verification result recorded as lesson in learned_lessons.json with session/run context",
            "Enables learning system to track not just success vs failure, but which completions were real",
            "Prevents silent failures where task ran to completion but produced no actual changes",
            "Verification status returned in run_once() return value and message pool publication"
        ],
        source="arXiv:2305.16291 - Voyager: An Open-Ended Embodied Agent with Large Language Models",
        additional_fields={
            "id": f"self_verification_framework_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "verify_grind_completion() and append_verification_lesson() in grind_spawner.py",
            "verification_process": {
                "step1": "After run_once() completes, call verify_grind_completion(session_id, run_num, output, returncode)",
                "step2": "Function checks: exit code == 0, success keywords in output, files_modified indicators",
                "step3": "Returns dict with: verified (PASS/FAIL), indicators list, files_modified bool, details string",
                "step4": "Call append_verification_lesson() to log results to learned_lessons.json",
                "step5": "Include self_verified flag in message pool publication for other workers to see",
                "step6": "Return verification status in run_once() return value"
            },
            "success_indicators": [
                "done", "complete", "success", "finished", "accomplished",
                "created", "modified", "fixed", "resolved", "completed"
            ],
            "retrieval_cues": [
                "self_verification",
                "quality_assurance",
                "false_positives",
                "grind_completion",
                "voyager",
                "autonomous_learning"
            ],
            "importance": 8
        }
    )


def record_adaptive_complexity_lesson() -> None:
    """Append adaptive task complexity detection lesson to learned_lessons.json."""
    record_lesson(
        category="task_classification",
        lesson_text="Adaptive task complexity detection with float-valued scoring for resource allocation",
        key_insights=[
            "Complexity scoring uses multiple signals instead of simple heuristics (arXiv:2303.17760, arXiv:2305.16291)",
            "Float-valued complexity_score (0.0-1.0) enables fine-grained resource adaptation vs. binary classification",
            "Scoring signals: word count, high-complexity keywords (create/implement/design), low-complexity keywords (fix/update), file references, paper/architecture mentions",
            "Threshold classification: score >= 0.35 = complex (routes to PLANNER), < 0.35 = simple (routes directly to CODER)",
            "Model adaptation: low complexity=base model, moderate (0.35-0.65)=upgrade to sonnet, high (0.65+)=use opus",
            "Budget adaptation: scales from 1.0x (simple) to 2.0x (very complex) based on predicted effort",
            "Role chain adaptation: ensures complex tasks (score >= 0.65) always use full PLANNER->CODER->REVIEWER->DOCUMENTER chain",
            "Complexity analysis included in session results for post-hoc learning and prompt optimization",
            "Published to message pool for inter-worker coordination and resource planning"
        ],
        source="arXiv:2303.17760 (CAMEL) + arXiv:2305.16291 (Voyager) - Adaptive task analysis for autonomous systems",
        additional_fields={
            "id": f"adaptive_complexity_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "decompose_task() in roles.py, adapt_model_for_complexity/budget/role_chain in grind_spawner.py",
            "complexity_thresholds": {
                "simple_threshold": 0.35,
                "moderate_threshold": 0.65,
                "high_threshold": 0.85
            },
            "model_adaptation_rules": {
                "simple": "base_model (haiku remains haiku)",
                "moderate": "upgrade haiku->sonnet, keep sonnet/opus",
                "high": "upgrade to opus",
                "very_high": "opus with max budget"
            },
            "budget_adaptation_multipliers": {
                "simple": 1.0,
                "moderate": 1.2,
                "high": 1.5,
                "very_high": 2.0
            },
            "scoring_signals": {
                "word_count": "0-50 words = 0.0-0.3 points (longer tasks more complex)",
                "high_complexity_keywords": "+0.15 per keyword (create, implement, design, build, refactor, architecture)",
                "low_complexity_keywords": "-0.08 per keyword (fix, update, add, change, modify)",
                "complexity_phrases": "+0.12 per phrase (multiple, several, integrate, coordinate, complex)",
                "file_references": "+0.05 per file mention (capped at 0.2)",
                "paper_references": "+0.10 per keyword (arxiv, paper, algorithm, framework, pattern)"
            },
            "retrieval_cues": [
                "complexity_detection",
                "adaptive_resources",
                "task_classification",
                "model_selection",
                "budget_allocation",
                "camel",
                "voyager"
            ],
            "importance": 9
        }
    )


def record_reflection_automation_lesson() -> None:
    """Append reflection automation triggers lesson to learned_lessons.json."""
    record_lesson(
        category="memory_synthesis",
        lesson_text="Automatic reflection triggers: synthesize memories at strategic points without manual intervention (Generative Agents arXiv:2304.03442)",
        key_insights=[
            "Reflection automation consolidates lessons into higher-level insights at strategic times (arXiv:2304.03442)",
            "TRIGGER 1 - After every N sessions (default: 5): Periodic synthesis based on session count using synthesis_interval parameter",
            "TRIGGER 2 - After any failure: Immediately synthesize when run_once() returns non-zero exit code to learn from failures",
            "TRIGGER 3 - When lesson count exceeds threshold: Trigger synthesis when loaded lessons > 50 to prevent overwhelming memory",
            "TRIGGER 4 - Explicit request: maybe_reflect() and --synthesize CLI flag for on-demand synthesis",
            "All triggers call MemorySynthesis.synthesize() which creates higher-level reflections from high-importance lessons",
            "Logging format: '[SYNTHESIS] Generated N reflections' and '[SYNTHESIS] Archived M lessons' for transparency",
            "Helper method _trigger_synthesis(synth, trigger_source) handles unified synthesis logic and logging",
            "Lesson archiving runs automatically with synthesis to prune rarely-accessed lessons (>30 days old, <1 retrieval)",
            "Synthesis runs are non-blocking and don't interrupt grind loop execution"
        ],
        source="arXiv:2304.03442 - Generative Agents: Interactive Simulacra of Human Behavior",
        additional_fields={
            "id": f"reflection_automation_triggers_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "grind_spawner.py GrindSession._trigger_synthesis(), four automatic trigger conditions",
            "trigger_conditions": {
                "session_count": {
                    "description": "After every N completed sessions",
                    "default_interval": 5,
                    "configurable": True,
                    "implementation": "self.runs % self.synthesis_interval == 0"
                },
                "failure_trigger": {
                    "description": "When any grind session fails (non-zero exit code)",
                    "default_interval": "always",
                    "configurable": False,
                    "implementation": "result.get('returncode', 0) != 0"
                },
                "lesson_count": {
                    "description": "When total lessons in memory exceed threshold",
                    "default_threshold": 50,
                    "configurable": True,
                    "implementation": "len(lessons) > lesson_threshold"
                },
                "explicit_request": {
                    "description": "On-demand synthesis via CLI flag or high importance threshold",
                    "methods": ["--synthesize CLI flag", "maybe_reflect() with importance_sum > 150"],
                    "implementation": "args.synthesize or importance_sum > 150"
                }
            },
            "logging_format": {
                "trigger": "[SYNTHESIS] Triggered by: {trigger_source}",
                "generation": "[SYNTHESIS] Generated {count} reflections",
                "archival": "[SYNTHESIS] Archived {count} unused lessons",
                "failure": "[SYNTHESIS] No new reflections generated"
            },
            "cli_integration": {
                "flag": "--synthesize",
                "behavior": "Force immediate memory synthesis, archive unused lessons, then exit",
                "use_case": "Manual intervention for memory management or testing"
            },
            "session_parameter": {
                "name": "synthesis_interval",
                "default_value": 5,
                "description": "Number of sessions before triggering session-count-based synthesis",
                "location": "GrindSession.__init__()"
            },
            "retrieval_cues": [
                "automatic_synthesis",
                "memory_consolidation",
                "trigger_conditions",
                "generative_agents",
                "reflection_automation",
                "failure_driven_learning",
                "periodic_synthesis"
            ],
            "importance": 9
        }
    )


def record_critic_feedback_lesson() -> None:
    """Append critic feedback loop lessons to learned_lessons.json (LATS/TextGrad pattern)."""
    record_lesson(
        category="code_quality",
        lesson_text="Critic feedback loop closes LATS/TextGrad improvement cycle - quality_score < 0.7 triggers improvement attempt",
        key_insights=[
            "CriticAgent implements LATS (Language Agent Tree Search) quality assessment pattern",
            "Evaluates code across dimensions: error handling, patterns, logic, imports",
            "Quality score 0.0-1.0 where 0.65 is baseline pass, 0.7 triggers improvement in critic mode",
            "Critic feedback includes: score, issues list, feedback suggestions, pass/fail boolean",
            "When --critic flag enabled: quality_score < 0.7 logs improvement suggestions for next run",
            "Each grind log stores: quality_score, critic_feedback, and full critic_review object",
            "Feedback loop closes by: review code -> identify issues -> suggest improvements -> retry task",
            "Enables TextGrad-style iterative refinement: gradient of quality scores guides next iteration",
            "Error handling patterns tracked: missing error handling, unused imports, syntax issues",
            "Pattern consistency checked: logger usage, pathlib.Path standard, JSON error handling"
        ],
        source="arXiv:2310.04406 - LATS; arXiv:2406.14762 - TextGrad",
        additional_fields={
            "id": f"critic_feedback_loop_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "implementation": "CriticAgent.review() integrated into GrindSession.run_once() with --critic CLI flag",
            "quality_score_interpretation": {
                "0.0_to_0.35": "Critical issues - code will fail",
                "0.35_to_0.65": "Warnings - code may work but has issues",
                "0.65_to_0.75": "Passing but lower quality - critic mode triggers improvement",
                "0.75_to_1.0": "High quality - minimal feedback needed"
            },
            "critic_checks": {
                "error_handling": "Detects external API calls without try-except blocks",
                "imports": "Flags unused imports and missing required modules",
                "syntax": "Validates bracket/paren/brace matching",
                "patterns": "Checks consistency with codebase patterns (logger, pathlib, json handling)",
                "logic": "Detects empty functions and hardcoded config values"
            },
            "cli_usage": "--critic flag enables feedback-driven retry mode",
            "retrieval_cues": [
                "code_quality",
                "iterative_refinement",
                "feedback_loop",
                "lats_textgrad",
                "grind_improvement",
                "quality_metrics"
            ],
            "importance": 7
        }
    )
