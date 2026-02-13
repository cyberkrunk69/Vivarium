"""
Scout configuration — YAML + env vars + hard caps.

User-controlled chaos with non-negotiable safety ceilings.
Load order: ~/.scout/config.yaml < .scout/config.yaml < env vars < hard caps.

TICKET-17: EnvLoader auto-loads .env for all Scout execution paths (tests, CLI).
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


class EnvLoader:
    """
    Auto-loads .env once, safely, idempotently.

    TICKET-17: Ensures GROQ_API_KEY etc. are available for pytest and CLI
    without manual 'source .env'. Uses setdefault — never overwrites existing
    env vars (cloud/deployment env > .env).
    """

    _loaded = False

    @classmethod
    def load(cls, path: Optional[Path] = None) -> None:
        if cls._loaded:
            return

        path = path or Path(".env")
        if not path.exists():
            cls._loaded = True
            return  # No .env = no problem (cloud env vars still work)

        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    key, value = key.strip(), value.strip()
                    # Strip quotes if present
                    value = value.strip('"').strip("'")
                    os.environ.setdefault(key, value)

        cls._loaded = True


def _path_matches(path: Path, pattern: str) -> bool:
    """
    Match path against glob pattern (supports * and **).
    * = any chars except /; ** = any number of path segments.
    """
    path_str = str(path).replace("\\", "/")
    pattern = pattern.replace("\\", "/")
    # Convert glob to regex: * -> [^/]*, ** -> (?:[^/]+/)*[^/]*
    # Escaped, then * -> [^/]*, ? -> ., ** -> .*
    def _glob_to_regex(p: str) -> str:
        i = 0
        result = []
        while i < len(p):
            if i + 1 < len(p) and p[i : i + 2] == "**":
                # ** = zero or more path segments: (?:[^/]+/)*[^/]*
                result.append("(?:[^/]+/)*[^/]*")
                i += 2
            elif p[i] == "*":
                result.append("[^/]*")
                i += 1
            elif p[i] == "?":
                result.append(".")
                i += 1
            else:
                result.append(re.escape(p[i]))
                i += 1
        return "".join(result)

    regex = "^" + _glob_to_regex(pattern) + "$"
    try:
        return bool(re.fullmatch(regex, path_str))
    except re.error:
        return False

logger = logging.getLogger(__name__)

# ─── Hard safety caps (NON-OVERRIDABLE) ─────────────────────────────────────
HARD_MAX_COST_PER_EVENT = 1.00  # Never allow >$1 per trigger
HARD_MAX_HOURLY_BUDGET = 10.00  # Emergency brake
HARD_MAX_AUTO_ESCALATIONS = 3   # Prevent retry loops


@dataclass
class TriggerConfig:
    """Resolved trigger type and cost limit for a file path."""

    type: str  # manual | on-save | on-commit | on-push | disabled
    max_cost: float


DEFAULT_CONFIG = {
    "triggers": {
        "default": "on-commit",
        "patterns": [
            {"pattern": "vivarium/runtime/**/*.py", "trigger": "on-save", "max_cost": 0.02},
            {"pattern": "tests/**/*", "trigger": "manual"},
            {"pattern": "docs/**/*.md", "trigger": "disabled"},
        ],
    },
    "limits": {
        "max_cost_per_event": 0.05,
        "hourly_budget": 1.00,
        "hard_safety_cap": 10.00,
    },
    "models": {
        "scout_nav": "llama-3.1-8b",
        "max_for_auto": "llama-3.1-8b",
        "tldr": "llama-3.1-8b-instant",  # Fast + cheap for summaries
        "deep": "llama-3.3-70b-versatile",  # High quality for deep analysis
        "eliv": "llama-3.1-8b-instant",  # ELIV doesn't need 70B
        "pr_synthesis": "llama-3.3-70b-versatile",
    },
    "notifications": {
        "on_validation_failure": "alert",
    },
    "drafts": {
        "enable_commit_drafts": True,
        "enable_pr_snippets": True,
        "enable_impact_analysis": False,
        "enable_module_briefs": True,
    },
    "roast": {
        "enable_roast": True,
    },
    "doc_generation": {
        "generate_eliv": True,  # Set to False during large syncs to skip .eliv.md
    },
    "ui": {
        "whimsy": False,  # TICKET-20: Cave man CEO mode (SCOUT_WHIMSY=1 overrides)
    },
}

def _max_concurrent_calls() -> int:
    """Max concurrent LLM API calls. Read from SCOUT_MAX_CONCURRENT_CALLS env (default 5)."""
    val = os.environ.get("SCOUT_MAX_CONCURRENT_CALLS", "5")
    try:
        n = int(val)
        return max(1, min(n, 100))  # Clamp 1–100
    except (ValueError, TypeError):
        return 5


# Lazy-initialized semaphore to avoid "attached to a different loop" errors.
# Creating Semaphore at module import (before any event loop runs) can bind it
# to the wrong loop. Created on first use when we're inside an async context.
_semaphore: Optional[asyncio.Semaphore] = None


def get_global_semaphore() -> asyncio.Semaphore:
    """Return the global semaphore, creating it lazily when first used in an async context."""
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(_max_concurrent_calls())
    return _semaphore


# Env var mapping: SCOUT_MAX_COST_PER_EVENT -> limits.max_cost_per_event
ENV_TO_CONFIG = {
    "SCOUT_MAX_COST_PER_EVENT": ("limits", "max_cost_per_event", float),
    "SCOUT_HOURLY_BUDGET": ("limits", "hourly_budget", float),
    "SCOUT_DEFAULT_TRIGGER": ("triggers", "default", str),
    "SCOUT_ON_VALIDATION_FAILURE": ("notifications", "on_validation_failure", str),
}


def _deep_merge(base: dict, override: dict) -> dict:
    """Merge override into base recursively. Override wins."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _load_yaml(path: Path) -> Optional[dict]:
    """Load YAML file. Return None if missing or invalid."""
    if not path.exists():
        return None
    try:
        import yaml

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else None
    except Exception as e:
        logger.warning("ScoutConfig: failed to load %s: %s", path, e)
        return None


def _save_yaml(path: Path, data: dict) -> bool:
    """Save dict to YAML. Return True on success."""
    try:
        import yaml

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        logger.warning("ScoutConfig: failed to save %s: %s", path, e)
        return False


def _get_nested(data: dict, *keys: str) -> Any:
    """Get nested key. Returns None if any key missing."""
    cur = data
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def _set_nested(data: dict, value: Any, *keys: str) -> None:
    """Set nested key, creating dicts as needed."""
    for k in keys[:-1]:
        if k not in data or not isinstance(data[k], dict):
            data[k] = {}
        data = data[k]
    data[keys[-1]] = value


class ScoutConfig:
    """
    Layered configuration: user YAML + env vars + hard caps.

    Hard caps are never overridden by user config.
    """

    def __init__(self, search_paths: Optional[List[Path]] = None):
        """
        Load config with precedence order:
        1. Hardcoded defaults
        2. ~/.scout/config.yaml (user global)
        3. .scout/config.yaml (project local)
        4. Environment variables
        """
        self._raw: Dict[str, Any] = dict(DEFAULT_CONFIG)
        paths = (
            self._default_search_paths()
            if search_paths is None
            else list(search_paths)
        )
        for p in paths:
            layer = _load_yaml(Path(p))
            if layer:
                self._raw = _deep_merge(self._raw, layer)
        self._apply_env_overrides()
        self._ensure_hard_cap_in_limits()

    def _default_search_paths(self) -> List[Path]:
        """Return [user_global, project_local] paths."""
        user = Path.home() / ".scout" / "config.yaml"
        project = Path.cwd() / ".scout" / "config.yaml"
        return [user, project]

    def _apply_env_overrides(self) -> None:
        """Apply env vars over config."""
        for env_key, (section, key, conv) in ENV_TO_CONFIG.items():
            val = os.environ.get(env_key)
            if val is None:
                continue
            try:
                if conv is float:
                    parsed = float(val)
                elif conv is str:
                    parsed = str(val).strip()
                else:
                    parsed = val
                if section not in self._raw:
                    self._raw[section] = {}
                self._raw[section][key] = parsed
            except (ValueError, TypeError) as e:
                logger.warning("ScoutConfig: invalid env %s=%r: %s", env_key, val, e)

    def _ensure_hard_cap_in_limits(self) -> None:
        """Ensure limits.hard_safety_cap reflects the constant (informational)."""
        limits = self._raw.get("limits") or {}
        limits["hard_safety_cap"] = HARD_MAX_HOURLY_BUDGET  # Non-overridable
        self._raw["limits"] = limits

    def resolve_trigger(self, file_path: Path) -> TriggerConfig:
        """
        Return trigger type and cost limit for this file.
        First pattern match wins; else fall back to default.
        """
        path_str = str(Path(file_path).as_posix())
        patterns = self._raw.get("triggers", {}).get("patterns") or []
        for entry in patterns:
            pattern = entry.get("pattern", "")
            if not pattern:
                continue
            if _path_matches(Path(path_str), pattern):
                trigger = str(entry.get("trigger", "on-commit")).lower()
                max_cost = entry.get("max_cost")
                if max_cost is not None:
                    max_cost = min(float(max_cost), HARD_MAX_COST_PER_EVENT)
                else:
                    max_cost = self.effective_max_cost(file_path)
                return TriggerConfig(type=trigger, max_cost=max_cost)
        default = str(
            self._raw.get("triggers", {}).get("default") or "on-commit"
        ).lower()
        max_cost = self.effective_max_cost(file_path)
        return TriggerConfig(type=default, max_cost=max_cost)

    def effective_max_cost(self, file_path: Optional[Path] = None) -> float:
        """
        User setting bounded by hard safety cap.
        """
        if file_path is not None:
            path_str = str(Path(file_path).as_posix())
            patterns = self._raw.get("triggers", {}).get("patterns") or []
            for entry in patterns:
                if _path_matches(Path(path_str), entry.get("pattern", "")):
                    mc = entry.get("max_cost")
                    if mc is not None:
                        return min(float(mc), HARD_MAX_COST_PER_EVENT)
        user_val = _get_nested(
            self._raw, "limits", "max_cost_per_event"
        )
        if user_val is not None:
            return min(float(user_val), HARD_MAX_COST_PER_EVENT)
        return min(
            float(DEFAULT_CONFIG["limits"]["max_cost_per_event"]),
            HARD_MAX_COST_PER_EVENT,
        )

    def should_process(
        self,
        estimated_cost: float,
        file_path: Optional[Path] = None,
        hourly_spend: float = 0.0,
    ) -> bool:
        """
        Check all limits before any LLM call.
        Returns True only if estimated_cost fits within per-event and hourly budgets.
        """
        max_per = self.effective_max_cost(file_path)
        if estimated_cost > max_per:
            return False
        if estimated_cost > HARD_MAX_COST_PER_EVENT:
            return False
        hour_budget = float(
            self._raw.get("limits", {}).get("hourly_budget") or 1.0
        )
        hour_budget = min(hour_budget, HARD_MAX_HOURLY_BUDGET)
        if hourly_spend + estimated_cost > hour_budget:
            return False
        return True

    def to_dict(self) -> dict:
        """Current effective config (for audit logging)."""
        return {
            "triggers": dict(self._raw.get("triggers", {})),
            "limits": dict(self._raw.get("limits", {})),
            "models": dict(self._raw.get("models", {})),
            "notifications": dict(self._raw.get("notifications", {})),
            "ui": dict(self._raw.get("ui", {})),
            "hard_caps": {
                "max_cost_per_event": HARD_MAX_COST_PER_EVENT,
                "hourly_budget": HARD_MAX_HOURLY_BUDGET,
                "max_auto_escalations": HARD_MAX_AUTO_ESCALATIONS,
            },
        }

    def get_user_config_path(self) -> Path:
        """Path to user global config (for opening in editor)."""
        return Path.home() / ".scout" / "config.yaml"

    def get_project_config_path(self) -> Path:
        """Path to project local config."""
        return Path.cwd() / ".scout" / "config.yaml"

    @property
    def whimsy_mode(self) -> bool:
        """TICKET-20: Cave man CEO mode. SCOUT_WHIMSY=1 or config ui.whimsy: true."""
        if os.environ.get("SCOUT_WHIMSY", "0") == "1":
            return True
        return bool(self.get("ui.whimsy"))

    def get(self, key_path: str) -> Optional[Any]:
        """Get value by dot path, e.g. 'triggers.default'."""
        parts = key_path.split(".")
        return _get_nested(self._raw, *parts)

    def set(self, key_path: str, value: Any) -> bool:
        """Set value by dot path. Writes to project config if it exists."""
        parts = key_path.split(".")
        if len(parts) < 2:
            return False
        _set_nested(self._raw, value, *parts)
        proj = self.get_project_config_path()
        if proj.exists():
            return _save_yaml(proj, self._raw)
        user = self.get_user_config_path()
        user.parent.mkdir(parents=True, exist_ok=True)
        return _save_yaml(user, self._raw)

    def validate_yaml(self, path: Optional[Path] = None) -> tuple[bool, str]:
        """
        Validate YAML syntax. Returns (ok, message).
        If path is None, validates merged config.
        """
        if path is not None:
            try:
                import yaml

                with open(path, encoding="utf-8") as f:
                    yaml.safe_load(f)
                return True, "Valid YAML"
            except Exception as e:
                return False, str(e)
        # Validate that our merged config is serializable
        try:
            import yaml

            yaml.safe_dump(self._raw)
            return True, "Valid"
        except Exception as e:
            return False, str(e)
