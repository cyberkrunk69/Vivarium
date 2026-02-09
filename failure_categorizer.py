# failure_categorizer.py
import logging
import json

class FailureCategorizer:
    def __init__(self):
        self.error_categories = {
            'TIMEOUT': 'Session exceeded time limit',
            'ENCODING': 'Unicode/charset issues',
            'IMPORT': 'Missing module errors',
            'SYNTAX': 'Python syntax errors',
            'RUNTIME': 'Execution errors',
            'UNKNOWN': 'Uncategorized'
        }

    def categorize_failure(self, error):
        """Return the appropriate error category string."""
        err_str = str(error).lower()
        if 'timeout' in err_str:
            return 'TIMEOUT'
        elif 'encoding' in err_str or 'charset' in err_str:
            return 'ENCODING'
        elif 'import' in err_str and 'error' in err_str:
            return 'IMPORT'
        elif 'syntax' in err_str:
            return 'SYNTAX'
        elif 'execution' in err_str or 'runtime' in err_str:
            return 'RUNTIME'
        else:
            return 'UNKNOWN'

    def log_failure(self, error_category, error_message, grind_log_file='grind_log.json'):
        """Append a failure entry (with category) to the grind log."""
        try:
            with open(grind_log_file, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                f.seek(0)
                data.append({
                    'error_category': error_category,
                    'error_message': error_message
                })
                json.dump(data, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            # Create a new log if it doesn't exist
            with open(grind_log_file, 'w') as f:
                json.dump([{
                    'error_category': error_category,
                    'error_message': error_message
                }], f, indent=4)

    def update_learned_lessons(self, error_category, error_message, learned_lessons_file='learned_lessons.json'):
        """Record the failure pattern for future learning."""
        try:
            with open(learned_lessons_file, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                f.seek(0)
                data.append({
                    'error_category': error_category,
                    'error_message': error_message
                })
                json.dump(data, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            with open(learned_lessons_file, 'w') as f:
                json.dump([{
                    'error_category': error_category,
                    'error_message': error_message
                }], f, indent=4)

    def count_errors_by_category(self, grind_log_file='grind_log.json'):
        """Return a dict counting occurrences of each error category."""
        error_counts = {}
        try:
            with open(grind_log_file, 'r') as f:
                data = json.load(f)
                for entry in data:
                    cat = entry.get('error_category', 'UNKNOWN')
                    error_counts[cat] = error_counts.get(cat, 0) + 1
            return error_counts
        except FileNotFoundError:
            return {}

if __name__ == "__main__":
    # Simple sanity‑check demo
    categorizer = FailureCategorizer()
    error_message = "Example error message"
    error_category = categorizer.categorize_failure(error_message)
    categorizer.log_failure(error_category, error_message)
    categorizer.update_learned_lessons(error_category, error_message)
    print("Current error counts:", categorizer.count_errors_by_category())
import json
import os
from collections import defaultdict
from typing import Any, Dict

# Global counter for error categories
_error_counts: Dict[str, int] = defaultdict(int)

def categorize_error(exc: BaseException) -> str:
    """
    Return a string category for the given exception.
    Categories:
        TIMEOUT   – timeout related exceptions
        ENCODING  – Unicode/charset problems
        IMPORT    – missing module / import errors
        SYNTAX    – Python syntax errors
        RUNTIME   – any other runtime execution errors
        UNKNOWN   – anything that does not fit above
    """
    # TIMEOUT
    if isinstance(exc, TimeoutError):
        return "TIMEOUT"

    # ENCODING
    if isinstance(exc, UnicodeError):
        return "ENCODING"

    # IMPORT
    if isinstance(exc, (ImportError, ModuleNotFoundError)):
        return "IMPORT"

    # SYNTAX
    if isinstance(exc, SyntaxError):
        return "SYNTAX"

    # RUNTIME – any other exception derived from Exception
    if isinstance(exc, Exception):
        return "RUNTIME"

    # Fallback
    return "UNKNOWN"


def record_error_category(category: str) -> None:
    """
    Increment the in‑memory counter for the supplied category.
    """
    _error_counts[category] += 1


def get_error_counts() -> Dict[str, int]:
    """
    Return a copy of the current error‑category counts.
    """
    return dict(_error_counts)


def persist_error_counts(stats_path: str = "error_stats.json") -> None:
    """
    Write the current error‑category counts to a JSON file.
    """
    try:
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(_error_counts, f, indent=2, ensure_ascii=False)
    except Exception:
        # If persisting fails we do not want to interrupt the main workflow.
        pass
import json
import os
from collections import defaultdict

# Path to the learned lessons JSON file
LEARNED_LESSONS_PATH = os.path.join(os.path.dirname(__file__), "learned_lessons.json")

# Global counter for error categories
error_counts = defaultdict(int)

def categorize_error(exc: Exception) -> str:
    """Return an error category based on the exception type or message."""
    msg = str(exc).lower()
    # TIMEOUT
    if isinstance(exc, TimeoutError):
        return "TIMEOUT"
    # ENCODING
    if "unicode" in msg or "encoding" in msg or "decode" in msg or "encode" in msg:
        return "ENCODING"
    # IMPORT
    if isinstance(exc, ModuleNotFoundError) or isinstance(exc, ImportError):
        return "IMPORT"
    # SYNTAX
    if isinstance(exc, SyntaxError):
        return "SYNTAX"
    # RUNTIME
    if isinstance(exc, RuntimeError):
        return "RUNTIME"
    # Fallback for other execution‑time exceptions
    if isinstance(exc, Exception):
        return "RUNTIME"
    # UNKNOWN
    return "UNKNOWN"

def record_error_category(category: str):
    """Increment the global counter for a given category."""
    error_counts[category] += 1

def persist_failure_pattern(pattern: str, category: str):
    """Append a failure pattern with its category to learned_lessons.json."""
    entry = {"pattern": pattern, "category": category}
    # Ensure the JSON file exists and contains a list
    if not os.path.exists(LEARNED_LESSONS_PATH):
        data = []
    else:
        with open(LEARNED_LESSONS_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    data.append(entry)
    with open(LEARNED_LESSONS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
import json
import os
from datetime import datetime

# ----------------------------------------------------------------------
# Paths to persistent JSON artefacts (located next to this module)
# ----------------------------------------------------------------------
LEARNED_LESSONS_PATH = os.path.join(os.path.dirname(__file__), "learned_lessons.json")
ERROR_COUNTS_PATH   = os.path.join(os.path.dirname(__file__), "error_counts.json")

def _load_json(path: str) -> dict:
    """Safely load a JSON file; return empty dict if missing or malformed."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def _save_json(path: str, data: dict) -> None:
    """Write JSON data atomically."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def categorize_error(exc: BaseException, timeout_occurred: bool = False) -> str:
    """
    Return a categorical label for the supplied exception.

    Categories (as required by the task):
        TIMEOUT   – session exceeded its time budget
        ENCODING  – Unicode / charset related problems
        IMPORT    – missing‑module / import errors
        SYNTAX    – Python syntax errors
        RUNTIME   – any other execution‑time exception
        UNKNOWN   – could not be classified
    """
    if timeout_occurred or isinstance(exc, TimeoutError):
        return "TIMEOUT"
    if isinstance(exc, UnicodeError):
        return "ENCODING"
    if isinstance(exc, (ImportError, ModuleNotFoundError)):
        return "IMPORT"
    if isinstance(exc, SyntaxError):
        return "SYNTAX"
    if isinstance(exc, Exception):
        return "RUNTIME"
    return "UNKNOWN"


def record_failure_pattern(category: str, exc: BaseException) -> None:
    """
    Append a failure pattern to ``learned_lessons.json``.
    The entry contains a timestamp, the derived category, the exception type
    and the textual message – useful for later pattern‑matching.
    """
    lessons = _load_json(LEARNED_LESSONS_PATH)
    failures = lessons.get("failures", [])
    failures.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "category":  category,
        "type":      type(exc).__name__,
        "message":   str(exc)
    })
    lessons["failures"] = failures
    _save_json(LEARNED_LESSONS_PATH, lessons)


def increment_error_count(category: str) -> None:
    """
    Increment the per‑category counter stored in ``error_counts.json``.
    This file is later used for reporting aggregate statistics.
    """
    counts = _load_json(ERROR_COUNTS_PATH)
    counts[category] = counts.get(category, 0) + 1
    _save_json(ERROR_COUNTS_PATH, counts)
import re
import traceback
from typing import Any

# Mapping of known patterns to categories
_PATTERN_MAP = {
    "timeout": "TIMEOUT",
    "timed out": "TIMEOUT",
    "unicode": "ENCODING",
    "encoding": "ENCODING",
    "cannot import": "IMPORT",
    "ImportError": "IMPORT",
    "SyntaxError": "SYNTAX",
    "IndentationError": "SYNTAX",
    "NameError": "RUNTIME",
    "TypeError": "RUNTIME",
    "AttributeError": "RUNTIME",
    "ZeroDivisionError": "RUNTIME",
    # add more patterns as needed
}

def _match_pattern(message: str) -> str | None:
    """Return a category if a known pattern is found in *message*."""
    lowered = message.lower()
    for pat, cat in _PATTERN_MAP.items():
        if pat in lowered:
            return cat
    return None

def classify_error(exc: BaseException, timeout_occurred: bool = False) -> str:
    """
    Determine the error category for a grind failure.

    Parameters
    ----------
    exc: BaseException
        The exception that was raised.
    timeout_occurred: bool, optional
        Set to True when the failure is known to be a timeout
        (e.g. a watchdog killed the process).

    Returns
    -------
    str
        One of the defined categories:
        TIMEOUT, ENCODING, IMPORT, SYNTAX, RUNTIME, UNKNOWN
    """
    if timeout_occurred:
        return "TIMEOUT"

    # Direct type checks first
    if isinstance(exc, TimeoutError):
        return "TIMEOUT"
    if isinstance(exc, (UnicodeDecodeError, UnicodeEncodeError)):
        return "ENCODING"
    if isinstance(exc, ImportError):
        return "IMPORT"
    if isinstance(exc, SyntaxError):
        return "SYNTAX"

    # Heuristic pattern matching on the string representation
    message = str(exc)
    cat = _match_pattern(message)
    if cat:
        return cat

    # Fallback – treat as runtime unless we cannot recognise anything
    if isinstance(exc, Exception):
        return "RUNTIME"

    return "UNKNOWN"
import re
import traceback

# Error categories
TIMEOUT   = "TIMEOUT"
ENCODING  = "ENCODING"
IMPORT    = "IMPORT"
SYNTAX    = "SYNTAX"
RUNTIME   = "RUNTIME"
UNKNOWN   = "UNKNOWN"

def categorize_error(exc: BaseException, timeout_occurred: bool = False) -> str:
    """
    Return an error category string for a given exception.
    """
    if timeout_occurred:
        return TIMEOUT

    # Unicode/encoding problems
    if isinstance(exc, UnicodeError):
        return ENCODING

    # Import errors
    if isinstance(exc, (ImportError, ModuleNotFoundError)):
        return IMPORT

    # Syntax errors (including compile errors)
    if isinstance(exc, SyntaxError):
        return SYNTAX

    # Runtime execution errors (ZeroDivisionError, TypeError, etc.)
    # We treat any non‑syntax, non‑import, non‑unicode error as RUNTIME
    # unless we cannot recognise it.
    if isinstance(exc, Exception):
        # Some runtime errors embed “timeout” in the message; catch them
        msg = str(exc).lower()
        if "timeout" in msg:
            return TIMEOUT
        return RUNTIME

    return UNKNOWN