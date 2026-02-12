#!/usr/bin/env bash
# repo-map.sh — Pure structural inventory for Python/GitHub repos
# Principle: programmatic discovery first (find, grep, awk); LLM only if needed for interpretation.
# Output: devtools/repo-map/repo-map_YYYY-MM-DD_HH-MM-SS.md — single consolidated markdown file

set -euo pipefail

# --- SAFETY CHECKS ---
if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "Abort: requires macOS (uname -s == Darwin)"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVTOOLS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$DEVTOOLS_ROOT/.." && pwd)"
cd "$REPO_ROOT"

if [[ ! -f requirements.txt ]] || [[ ! -d .github/workflows ]]; then
  echo "Abort: requires requirements.txt and .github/workflows (not a Python/GitHub repo root)"
  exit 1
fi

# Source common utilities
# shellcheck source=../_internal/common/utils.sh
source "$DEVTOOLS_ROOT/_internal/common/utils.sh"
ensure_path
load_dotenv "$REPO_ROOT"

# Exclusions (read-only; never modify)
EXCLUDE=".git|venv|.venv|__pycache__|node_modules|.pytest_cache"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUT_DIR="$DEVTOOLS_ROOT/repo-map"
OUT_FILE="$OUT_DIR/repo-map_${TIMESTAMP}.md"
mkdir -p "$OUT_DIR"

# Archive existing repo-map output files before generating new ones
archive_devtools_output "$OUT_DIR" "repo-map_*.md"

# --- DETECT SOURCE ROOT ---
SRC_DIR=""
for d in src vivarium; do
  if [[ -d "$d" ]]; then
    SRC_DIR="$d"
    break
  fi
done
if [[ -z "$SRC_DIR" ]]; then
  for d in */; do
    d="${d%/}"
    if [[ -f "$d/__init__.py" ]]; then
      SRC_DIR="$d"
      break
    fi
  done
fi
[[ -z "$SRC_DIR" ]] && SRC_DIR="."

# --- MANIFEST ---
PYTHON_VER=""
if [[ -f .python-version ]]; then
  PYTHON_VER=$(head -1 .python-version 2>/dev/null || echo "")
elif [[ -d .venv ]]; then
  PYTHON_VER=$(.venv/bin/python --version 2>/dev/null | awk '{print $2}' || echo "")
elif [[ -d venv ]]; then
  PYTHON_VER=$(venv/bin/python --version 2>/dev/null | awk '{print $2}' || echo "")
fi
[[ -z "$PYTHON_VER" ]] && PYTHON_VER="unknown"

REPO_NAME=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || basename "$REPO_ROOT")
WORKFLOW_COUNT=$(find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
WORKFLOW_COUNT=${WORKFLOW_COUNT:-0}

MODULE_COUNT=0
if [[ -d "$SRC_DIR" ]] && [[ "$SRC_DIR" != "." ]]; then
  MODULE_COUNT=$(find "$SRC_DIR" -name "__init__.py" 2>/dev/null | wc -l | tr -d ' ')
fi

# --- BUILD SINGLE .md FILE ---
{
  echo "# Repo Map: $REPO_NAME"
  echo "Generated: $TIMESTAMP"
  echo ""
  echo "## Manifest"
  echo '```json'
  echo "{\"repo_name\":\"$REPO_NAME\",\"timestamp\":\"$TIMESTAMP\",\"python_version\":\"$PYTHON_VER\",\"workflow_count\":$WORKFLOW_COUNT,\"module_count\":$MODULE_COUNT,\"src_dir\":\"$SRC_DIR\"}"
  echo '```'
  echo ""

  # --- FILE TREE ---
  echo "## File Tree"
  echo '```'
  {
    for d in "$SRC_DIR" tests docs; do
      [[ -d "$d" ]] && find "$d" -type f \( -name "*.py" -o -name "*.md" -o -name "*.rst" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) 2>/dev/null | grep -vE "$EXCLUDE" | sort
    done
    if find . -type d -name "control_panel" 2>/dev/null | head -1 | grep -q .; then
      find . -path "*control_panel*" -type f \( -name "*.py" -o -name "*.html" -o -name "*.js" \) 2>/dev/null | grep -vE "$EXCLUDE" | sort
    fi
  } | sort -u | sed 's|^\./||' 2>/dev/null || true
  echo '```'
  echo ""

  # --- DEPENDENCIES ---
  echo "## Dependencies"
  echo "### requirements.txt"
  echo '```'
  cat requirements.txt 2>/dev/null || echo "(empty)"
  echo '```'
  echo ""
  echo "### deptree"
  echo '```'
  if command -v pipdeptree &>/dev/null; then
    pipdeptree 2>/dev/null || echo "pipdeptree_error"
  else
    echo "MISSING:pipdeptree"
  fi
  echo '```'
  echo ""

  # --- WORKFLOWS ---
  echo "## Workflows"
  for wf in .github/workflows/*.yml .github/workflows/*.yaml; do
    [[ -f "$wf" ]] || continue
    base=$(basename "$wf")
    echo "### $base"
    echo '```yaml'
    cat "$wf" 2>/dev/null || true
    echo '```'
    echo ""
  done

  # --- CODE STRUCTURE ---
  echo "## Code Structure"
  echo "### Modules"
  echo '```'
  find "$SRC_DIR" -name "__init__.py" 2>/dev/null | grep -vE "$EXCLUDE" | cut -d/ -f2 | sort -u 2>/dev/null || true
  echo '```'
  echo ""
  echo "### Imports (ndjson)"
  echo '```ndjson'
  if [[ -d "$SRC_DIR" ]] && [[ "$SRC_DIR" != "." ]]; then
    find "$SRC_DIR" -name "*.py" 2>/dev/null | grep -vE "$EXCLUDE" | while read -r f; do
      imports=$(grep -h -E '^import |^from ' "$f" 2>/dev/null | sed 's/^[[:space:]]*//' | sort -u || true)
      echo "$imports" | python3 -c "
import sys, json
f = sys.argv[1]
lines = [l.strip() for l in sys.stdin.read().strip().split('\n') if l.strip()]
print(json.dumps({'file': f, 'imports': lines}))
" "$f" 2>/dev/null || echo "{\"file\":\"$f\",\"imports\":[]}"
    done 2>/dev/null || true
  fi
  echo '```'
  echo ""
  echo "### Import summary (top-level modules used)"
  echo '```'
  if [[ -d "$SRC_DIR" ]] && [[ "$SRC_DIR" != "." ]]; then
    find "$SRC_DIR" -name "*.py" 2>/dev/null | grep -vE "$EXCLUDE" | while read -r f; do
      grep -h -E '^import |^from ' "$f" 2>/dev/null | sed 's/^[[:space:]]*//' | \
        sed -E 's/^(import|from) +([A-Za-z0-9_]+).*/\2/' | sort -u || true
    done 2>/dev/null | sort | uniq -c | sort -rn | head -30 || true
  fi
  echo '```'
  echo ""

  # --- TESTS ---
  echo "## Tests"
  echo "### Topology (ndjson)"
  echo '```ndjson'
  find tests -name "test_*.py" -o -name "*_test.py" 2>/dev/null | grep -vE "$EXCLUDE" | while read -r tf; do
    base=$(basename "$tf" .py)
    base=${base#test_}
    base=${base%_test}
    echo "{\"test_file\":\"$tf\",\"covers_module\":\"$base\"}"
  done 2>/dev/null || true
  echo '```'
  echo ""
  echo "### Patterns"
  echo '```'
  grep -rh -E '@pytest\.mark\.|unittest\.skip|@flaky|@pytest\.mark\.parametrize' tests --include="*.py" 2>/dev/null || true
  echo '```'
  echo ""

  # --- DOCS ---
  echo "## Docs"
  echo "### Inventory"
  echo '```'
  find docs -type f \( -name "*.md" -o -name "*.rst" \) 2>/dev/null | grep -vE "$EXCLUDE" | while read -r f; do
    ts=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$f" 2>/dev/null || stat -c "%y" "$f" 2>/dev/null | cut -d. -f1 || echo "unknown")
    echo "$ts	$f"
  done | sort -k2 2>/dev/null || true
  echo '```'
  echo ""
  echo "### Stale indicators"
  echo '```'
  grep -rh -E '202[0-4]|outdated' docs --include="*.md" --include="*.rst" 2>/dev/null || true
  echo '```'
  echo ""

  # --- GIT SIGNALS ---
  echo "## Git Signals"
  echo "### Hot files (last 90 days)"
  echo '```'
  git log --since="90 days ago" --pretty=format: --name-only 2>/dev/null | sort | uniq -c | sort -rn | head -20 || true
  echo '```'
  echo ""
  echo "### Churn"
  echo '```'
  git log --pretty=format: --name-only 2>/dev/null | sort | uniq -c | sort -rn | head -50 || true
  echo '```'
  echo ""

  # --- MARKERS ---
  echo "## Markers"
  echo "### TODOs (ndjson)"
  echo '```ndjson'
  find . -name "*.py" -not -path "./.git/*" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./__pycache__/*" -not -path "*/__pycache__/*" -not -path "./node_modules/*" -not -path "./.pytest_cache/*" 2>/dev/null | while read -r pyf; do
    grep -n -E 'TODO:' "$pyf" 2>/dev/null | while read -r line; do
      ln=$(echo "$line" | cut -d: -f1)
      rest=$(echo "$line" | cut -d: -f2- | sed 's/^[[:space:]]*//')
      text=$(echo "$rest" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))' 2>/dev/null || echo '""')
      echo "{\"file\":\"$pyf\",\"line\":$ln,\"text\":$text}"
    done
  done 2>/dev/null || true
  echo '```'
  echo ""
  echo "### FIXMEs (ndjson)"
  echo '```ndjson'
  find . -name "*.py" -not -path "./.git/*" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./__pycache__/*" -not -path "*/__pycache__/*" -not -path "./node_modules/*" -not -path "./.pytest_cache/*" 2>/dev/null | while read -r pyf; do
    grep -n -E 'FIXME:|XXX:' "$pyf" 2>/dev/null | while read -r line; do
      ln=$(echo "$line" | cut -d: -f1)
      rest=$(echo "$line" | cut -d: -f2- | sed 's/^[[:space:]]*//')
      text=$(echo "$rest" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))' 2>/dev/null || echo '""')
      echo "{\"file\":\"$pyf\",\"line\":$ln,\"text\":$text}"
    done
  done 2>/dev/null || true
  echo '```'
  echo ""

  # --- CONTROL PANEL (if exists) ---
  if find . -type d -name "control_panel" 2>/dev/null | head -1 | grep -q .; then
    echo "## Control Panel"
    echo "### Modules"
    echo '```'
    find . -path "*control_panel*" -name "*.py" 2>/dev/null | grep -vE "$EXCLUDE" | sort 2>/dev/null || true
    echo '```'
    echo ""
    echo "### Imports (ndjson)"
    echo '```ndjson'
    find . -path "*control_panel*" -name "*.py" 2>/dev/null | grep -vE "$EXCLUDE" | while read -r f; do
      imports=$(grep -h -E '^import |^from ' "$f" 2>/dev/null | sed 's/^[[:space:]]*//' | sort -u || true)
      echo "$imports" | python3 -c "
import sys, json
f = sys.argv[1]
lines = [l.strip() for l in sys.stdin.read().strip().split('\n') if l.strip()]
print(json.dumps({'file': f, 'imports': lines}))
" "$f" 2>/dev/null || echo "{\"file\":\"$f\",\"imports\":[]}"
    done 2>/dev/null || true
    echo '```'
    echo ""
  fi

} > "$OUT_FILE"

# Copy to clipboard (macOS)
[[ "$(uname -s)" == "Darwin" ]] && pbcopy < "$OUT_FILE" 2>/dev/null || true

# --- FINAL MESSAGE ---
echo ""
echo "✅ Repo map generated at $OUT_FILE"
[[ ${archived_count:-0} -gt 0 ]] && echo "   Archived: $archived_count previous output file(s) to $OUT_DIR/archive"
echo "   Copied to clipboard. Feed to your LLM for debt synthesis."
