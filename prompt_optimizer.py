"""
DSPy-inspired prompt optimization through self-bootstrapping demonstrations.

Based on arXiv:2310.03714 - Demonstrate-Search-Predict (DSPy):
Achieves 25-65% improvement over standard few-shot prompting by:
1. Collecting demonstrations from successful task completions
2. Ranking by efficiency metrics (num_turns, duration_ms)
3. Injecting best examples into prompts before execution
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


def save_demonstrations(demos: List[Dict[str, Any]], file: str = 'demos.json') -> None:
    """
    Persist demonstrations to a JSON file.

    Args:
        demos: List of demonstration dicts to save
        file: Output filename (default: demos.json)
    """
    with open(file, 'w') as f:
        json.dump(demos, f, indent=2)


def load_demonstrations(file: str = 'demos.json') -> List[Dict[str, Any]]:
    """
    Load demonstrations from a JSON file.

    Args:
        file: Input filename (default: demos.json)

    Returns:
        List of demonstration dicts, or empty list if file doesn't exist
    """
    path = Path(file)
    if not path.exists():
        return []

    try:
        with open(file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def collect_demonstrations(logs_dir: Path) -> List[Dict[str, Any]]:
    """
    Extract successful task completions from grind_logs/.

    Each demonstration contains:
    - task_description: Original task prompt
    - result: Completion summary
    - num_turns: Task complexity indicator
    - duration_ms: Execution time
    - total_cost_usd: Resource efficiency
    - efficiency_score: Computed rank (lower turns = higher rank)

    Args:
        logs_dir: Path to grind_logs directory

    Returns:
        List of demonstration dicts, sorted by efficiency (best first)
    """
    demonstrations = []

    if not logs_dir.exists():
        return demonstrations

    # Parse all session log files
    for log_file in sorted(logs_dir.glob("*.json")):
        try:
            content = log_file.read_text().strip()
            if not content:
                continue

            data = json.loads(content)

            # Only keep successful completions
            if data.get("type") == "result" and data.get("is_error") is False:
                demo = {
                    "result": data.get("result", ""),
                    "num_turns": data.get("num_turns", 0),
                    "duration_ms": data.get("duration_ms", 0),
                    "total_cost_usd": data.get("total_cost_usd", 0.0),
                    "log_file": str(log_file)
                }

                # Compute efficiency score: lower num_turns = higher score
                # Normalize: 4 turns = perfect (100%), 20 turns = worst (10%)
                if demo["num_turns"] > 0:
                    demo["efficiency_score"] = max(0.1, 1.0 - (demo["num_turns"] - 4) / 20.0)
                else:
                    demo["efficiency_score"] = 0.5

                demonstrations.append(demo)
        except (json.JSONDecodeError, ValueError, KeyError):
            pass

    # Sort by efficiency score (highest first)
    demonstrations.sort(key=lambda x: x["efficiency_score"], reverse=True)

    # Save top 10 demonstrations for bootstrap across sessions
    save_demonstrations(demonstrations[:10])

    return demonstrations


def score_prompt(prompt_template: str, demonstrations: List[Dict[str, Any]]) -> float:
    """
    Calculate effectiveness score for a prompt with given demonstrations.

    Effectiveness = average efficiency_score of demonstrations used.
    Higher score = better examples injected.

    Args:
        prompt_template: The prompt text
        demonstrations: List of demonstrations

    Returns:
        Float score from 0.0 to 1.0
    """
    if not demonstrations:
        return 0.0

    # Average efficiency of top demonstrations
    top_demos = demonstrations[:3]  # Use best 3
    avg_efficiency = sum(d.get("efficiency_score", 0.5) for d in top_demos) / len(top_demos)
    return avg_efficiency


def optimize_prompt(prompt_template: str, demonstrations: List[Dict[str, Any]]) -> str:
    """
    Inject top 2-3 demonstrations into prompt template.

    Inserts few-shot examples between RULES header and rule content,
    following DSPy pattern: context -> examples -> task -> expected output.

    Args:
        prompt_template: Base prompt with {task} and other placeholders already filled
        demonstrations: List of demonstration dicts with 'result' and 'num_turns'

    Returns:
        Enhanced prompt with injected examples
    """
    if not demonstrations:
        return prompt_template

    # Take top 2-3 demonstrations
    top_demos = demonstrations[:3]

    # Build few-shot example section
    examples_section = "\n## EXAMPLES OF SUCCESSFUL EXECUTIONS:\n"

    for i, demo in enumerate(top_demos, 1):
        result = demo.get("result", "")
        num_turns = demo.get("num_turns", "?")

        # Truncate long results to ~200 chars
        if len(result) > 200:
            result = result[:197] + "..."

        examples_section += f"""
Example {i} (Completed in {num_turns} turns):
Result: {result}
"""

    examples_section += "\n"

    # Inject examples before RULES section
    if "RULES:" in prompt_template:
        enhanced = prompt_template.replace("RULES:", examples_section + "RULES:")
    else:
        enhanced = prompt_template + examples_section

    return enhanced


def get_relevant_demonstrations(
    task: str,
    demonstrations: List[Dict[str, Any]],
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Select most relevant demonstrations for a given task.

    Loads persisted demonstrations first, then returns top-k by efficiency score.
    Future: could add semantic similarity matching.

    Args:
        task: Task description (for future semantic matching)
        demonstrations: All available demonstrations
        top_k: Number of examples to return

    Returns:
        Top-k most relevant demonstrations
    """
    # Load from file first (enables bootstrap across sessions)
    persisted_demos = load_demonstrations()
    if persisted_demos:
        demonstrations = persisted_demos

    # Simple approach: return top-k by efficiency
    return demonstrations[:top_k]
