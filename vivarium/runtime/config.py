from __future__ import annotations

import os
import sys
from pathlib import Path
from urllib.parse import urlparse
from vivarium.runtime.vivarium_scope import SECURITY_ROOT

# Swarm API base URL - can be overridden via SWARM_API_URL environment variable
SWARM_API_URL = os.environ.get("SWARM_API_URL", "http://127.0.0.1:8420")

# Groq API settings
GROQ_API_URL = os.environ.get("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_KEY_FILE = SECURITY_ROOT / "groq_api_key.txt"

# Groq-only model whitelist (hard policy)
GROQ_MODEL_WHITELIST = {
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
}

# Default model (must be in whitelist)
DEFAULT_GROQ_MODEL = os.environ.get("DEFAULT_GROQ_MODEL", "llama-3.1-8b-instant")

# Default minimum budget for each agent task
DEFAULT_MIN_BUDGET = 0.05

# Default maximum budget for each agent task
DEFAULT_MAX_BUDGET = 0.10

# Timeout in seconds for acquiring locks before operation fails
LOCK_TIMEOUT_SECONDS = 300

# Timeout in seconds for API requests to external services
API_TIMEOUT_SECONDS = 120

# Worker subprocess timeout (seconds)
WORKER_TIMEOUT_SECONDS = int(os.environ.get("WORKER_TIMEOUT_SECONDS", "900"))


def get_groq_api_key() -> str | None:
    """Return live GROQ API key (env overrides cached value)."""
    global GROQ_API_KEY
    env_key = os.environ.get("GROQ_API_KEY")
    if env_key:
        return env_key
    if GROQ_API_KEY:
        return GROQ_API_KEY
    if GROQ_API_KEY_FILE.exists():
        try:
            persisted = GROQ_API_KEY_FILE.read_text(encoding="utf-8").strip()
        except OSError:
            persisted = ""
        if persisted:
            os.environ["GROQ_API_KEY"] = persisted
            GROQ_API_KEY = persisted
            return persisted
    return None


def set_groq_api_key(api_key: str | None) -> None:
    """Set/clear GROQ API key for the current runtime process."""
    global GROQ_API_KEY
    normalized = (api_key or "").strip()
    if normalized:
        os.environ["GROQ_API_KEY"] = normalized
        GROQ_API_KEY = normalized
        return
    os.environ.pop("GROQ_API_KEY", None)
    GROQ_API_KEY = None


def validate_model_id(model_id: str) -> None:
    """Validate that a model id is in the Groq whitelist."""
    if model_id not in GROQ_MODEL_WHITELIST:
        raise ValueError(
            f"Model '{model_id}' is not allowed. "
            f"Allowed models: {sorted(GROQ_MODEL_WHITELIST)}"
        )


def validate_config(require_groq_key: bool = False) -> None:
    """
    Validate configuration at startup.

    Checks:
    - SWARM_API_URL is a valid URL
    - Required directories are accessible

    Raises:
        SystemExit: If validation fails with clear error message
    """
    errors = []

    # Validate SWARM_API_URL format
    try:
        parsed = urlparse(SWARM_API_URL)
        if not parsed.scheme:
            errors.append("SWARM_API_URL must include a scheme (http/https)")
        if not parsed.netloc:
            errors.append("SWARM_API_URL must include a valid host")
    except Exception as e:
        errors.append(f"SWARM_API_URL parse error: {e}")

    # Validate Groq API URL format
    try:
        parsed = urlparse(GROQ_API_URL)
        if not parsed.scheme or not parsed.netloc:
            errors.append("GROQ_API_URL must include scheme and host")
    except Exception as e:
        errors.append(f"GROQ_API_URL parse error: {e}")

    # Validate Groq API key if required
    if require_groq_key and not get_groq_api_key():
        errors.append("GROQ_API_KEY not set (required for Groq API calls)")

    # Validate default model is in whitelist
    try:
        validate_model_id(DEFAULT_GROQ_MODEL)
    except ValueError as e:
        errors.append(str(e))

    # Validate workspace is accessible
    workspace = Path(__file__).resolve().parents[2]
    if not workspace.exists():
        errors.append(f"Workspace directory does not exist: {workspace}")
    if not workspace.is_dir():
        errors.append(f"Workspace is not a directory: {workspace}")

    # If any errors, exit with clear message
    if errors:
        print("CONFIG VALIDATION FAILED:", file=sys.stderr)
        for i, error in enumerate(errors, 1):
            print(f"  [{i}] {error}", file=sys.stderr)
        sys.exit(1)
