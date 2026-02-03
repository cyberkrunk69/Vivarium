import os
import sys
from pathlib import Path
from urllib.parse import urlparse

# Swarm API base URL - can be overridden via SWARM_API_URL environment variable
SWARM_API_URL = os.environ.get('SWARM_API_URL', 'http://127.0.0.1:8420')

# Default minimum budget for each agent task
DEFAULT_MIN_BUDGET = 0.05

# Default maximum budget for each agent task
DEFAULT_MAX_BUDGET = 0.10

# Timeout in seconds for acquiring locks before operation fails
LOCK_TIMEOUT_SECONDS = 300

# Timeout in seconds for API requests to external services
API_TIMEOUT_SECONDS = 120


def validate_config():
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

    # Validate workspace is accessible
    workspace = Path(__file__).parent
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
