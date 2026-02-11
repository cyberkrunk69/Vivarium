#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  exec "$ROOT_DIR/.venv/bin/python" "$ROOT_DIR/scripts/dev_launcher.py"
fi
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$ROOT_DIR/scripts/dev_launcher.py"
fi
echo "python3 is required but was not found."
exit 1
