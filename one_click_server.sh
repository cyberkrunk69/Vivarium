#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
elif [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source "venv/bin/activate"
fi

PYTHON_BIN="python"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    echo "[ERROR] Python not found. Install Python 3."
    exit 1
  fi
fi

missing="$("$PYTHON_BIN" - <<'PY'
import importlib

missing = []
for name in ["flask", "flask_socketio", "watchdog"]:
    try:
        importlib.import_module(name)
    except Exception:
        missing.append(name)

if missing:
    print(",".join(missing))
PY
)"

if [ -n "$missing" ]; then
  echo "[INFO] Installing missing UI dependencies: $missing"
  "$PYTHON_BIN" -m pip install -r requirements-groq.txt
  "$PYTHON_BIN" -m pip install watchdog
fi

echo "[INFO] Starting control panel on http://localhost:8421"
"$PYTHON_BIN" control_panel.py
