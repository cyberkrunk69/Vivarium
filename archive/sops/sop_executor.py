import json
import os
from typing import Any, Dict, List

# Simple registry of action handlers. Real implementations would be more sophisticated.
ACTION_HANDLERS = {}

def handler(action_name):
    """Decorator to register a function as an action handler."""
    def decorator(fn):
        ACTION_HANDLERS[action_name] = fn
        return fn
    return decorator

@handler("read_target_file")
def read_target_file(step: Dict[str, Any], context: Dict[str, Any]) -> Any:
    # For demo purposes we just read a placeholder file path from step if provided.
    target = step.get("target_file", "placeholder.py")
    with open(target, "r", encoding="utf-8") as f:
        code = f.read()
    return code

@handler("identify_patterns")
def identify_patterns(step: Dict[str, Any], context: Dict[str, Any]) -> Any:
    # Dummy pattern extraction – just returns lines containing the word "def"
    original = context.get(step["input"])
    patterns = [line for line in original.splitlines() if line.strip().startswith("def ")]
    return patterns

@handler("check_existing_utils")
def check_existing_utils(step: Dict[str, Any], context: Dict[str, Any]) -> Any:
    # Scan a predefined utils directory; return list of module names.
    utils_dir = step.get("utils_dir", "utils")
    if not os.path.isdir(utils_dir):
        return []
    return [f[:-3] for f in os.listdir(utils_dir) if f.endswith(".py")]

@handler("plan_migration")
def plan_migration(step: Dict[str, Any], context: Dict[str, Any]) -> Any:
    # Very naive plan: map each pattern to the first available util if any.
    patterns = context.get(step["input"][0])
    utils = context.get(step["input"][1])
    plan = {"mappings": []}
    for pat in patterns:
        util = utils[0] if utils else None
        plan["mappings"].append({"pattern": pat, "util": util})
    return plan

@handler("execute_migration")
def execute_migration(step: Dict[str, Any], context: Dict[str, Any]) -> Any:
    # Stub: just log the migration plan.
    plan = context.get(step["input"])
    print("Executing migration with plan:", json.dumps(plan, indent=2))
    return None

@handler("verify_no_regressions")
def verify_no_regressions(step: Dict[str, Any], context: Dict[str, Any]) -> Any:
    # Stub: assume tests pass.
    return {"tests_pass": True, "warnings": []}

@handler("document_lessons")
def document_lessons(step: Dict[str, Any], context: Dict[str, Any]) -> Any:
    results = context.get(step["input"])
    lesson = {"lesson": "Migration executed", "result": results}
    lessons_path = "learned_lessons.json"
    existing = []
    if os.path.exists(lessons_path):
        with open(lessons_path, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    existing.append(lesson)
    with open(lessons_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)
    return lesson

def load_sop(sop_path: str) -> Dict[str, Any]:
    with open(sop_path, "r", encoding="utf-8") as f:
        return json.load(f)

def execute_sop(sop: Dict[str, Any]) -> None:
    context: Dict[str, Any] = {}
    for step in sop.get("steps", []):
        action = step["action"]
        handler_fn = ACTION_HANDLERS.get(action)
        if not handler_fn:
            raise NotImplementedError(f"No handler for action '{action}'")
        # Resolve inputs from context if they are references
        resolved_inputs = {}
        for key, val in step.items():
            if key in ("action", "output"):
                continue
            if isinstance(val, str) and val in context:
                resolved_inputs[key] = context[val]
            else:
                resolved_inputs[key] = val
        # Execute handler
        result = handler_fn({**step, **resolved_inputs}, context)
        # Store output if defined
        if "output" in step:
            context[step["output"]] = result
    # Simple quality gate check
    gates = sop.get("quality_gates", [])
    for gate in gates:
        if gate == "tests_pass":
            assert context.get("test_results", {}).get("tests_pass"), "Quality gate failed: tests did not pass"
        if gate == "no_new_warnings":
            assert not context.get("test_results", {}).get("warnings"), "Quality gate failed: new warnings"
        if gate == "lesson_documented":
            assert os.path.exists("learned_lessons.json"), "Quality gate failed: lessons not documented"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sop_executor.py <sop_json_path>")
        sys.exit(1)
    sop_path = sys.argv[1]
    sop = load_sop(sop_path)
    execute_sop(sop)
    print("SOP execution completed successfully.")
import json
import importlib
import os

# Simple registry of action handlers – in a real system each would be a sophisticated function.
def read_target_file(step):
    # Placeholder: read a file path from step config or context
    print("Executing read_target_file")
    return {"original_code": "# dummy code"}

def identify_patterns(step, original_code):
    print("Executing identify_patterns")
    return {"patterns": []}

def check_existing_utils(step):
    print("Executing check_existing_utils")
    return {"available_utils": []}

def plan_migration(step, patterns, available_utils):
    print("Executing plan_migration")
    return {"migration_plan": {}}

def execute_migration(step, migration_plan):
    print("Executing execute_migration")
    # No return needed

def verify_no_regressions(step):
    print("Executing verify_no_regressions")
    return {"test_results": {"tests_pass": True, "no_new_warnings": True}}

def document_lessons(step, test_results):
    print("Executing document_lessons")
    lessons_path = os.path.join(os.path.dirname(__file__), "..", "learned_lessons.json")
    lesson_entry = {"sop": step.get('sop_name', 'unknown'), "result": test_results}
    # Ensure the lessons file exists and is a JSON array
    if not os.path.exists(lessons_path):
        with open(lessons_path, "w") as f:
            json.dump([], f)
    with open(lessons_path, "r+") as f:
        data = json.load(f)
        data.append(lesson_entry)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

# Mapping from action name to handler function
ACTION_HANDLERS = {
    "read_target_file": read_target_file,
    "identify_patterns": identify_patterns,
    "check_existing_utils": check_existing_utils,
    "plan_migration": plan_migration,
    "execute_migration": execute_migration,
    "verify_no_regressions": verify_no_regressions,
    "document_lessons": document_lessons,
}

def execute_sop(sop_path):
    with open(sop_path, "r") as f:
        sop = json.load(f)

    context = {}
    for step in sop.get("steps", []):
        action = step["action"]
        handler = ACTION_HANDLERS.get(action)
        if not handler:
            raise ValueError(f"No handler defined for action '{action}'")
        # Prepare inputs based on step definition
        inputs = {}
        for key, val in step.items():
            if key in ("action", "output"):
                continue
            # Resolve inputs from previous context if they refer to a key
            if isinstance(val, str) and val in context:
                inputs[key] = context[val]
            else:
                inputs[key] = val
        # Call handler
        result = handler(step, **inputs) if inputs else handler(step)
        # Store outputs back into context
        if "output" in step:
            context[step["output"]] = result.get(step["output"], result)
    print("SOP execution completed.")
    return context

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sop_executor.py <path_to_sop_json>")
        sys.exit(1)
    execute_sop(sys.argv[1])