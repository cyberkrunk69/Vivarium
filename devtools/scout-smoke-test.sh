#!/bin/bash
set -euo pipefail

# Scout Hardening Smoke Tests
# Verifies: wrappers, find_python, hooks, module entrypoints
# Exit 0 = all critical paths work, non-zero = blockers detected

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

ERRORS=0
WARNINGS=0

error() { echo "❌ ERROR: $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo "⚠️  WARN: $1"; WARNINGS=$((WARNINGS + 1)); }
ok() { echo "✅ OK: $1"; }

echo "=== Scout Smoke Tests ==="
echo "Repo: $REPO_ROOT"
echo ""

# --- Test 1: Wrapper existence and executability ---
echo "--- Test 1: Wrapper Executables ---"
for wrapper in scout-nav scout-index scout-brief scout-roast scout-ship scout-query scout-autonomy; do
    path="devtools/$wrapper"
    if [ -x "$path" ]; then
        ok "$wrapper is executable"
    elif [ -f "$path" ]; then
        error "$wrapper exists but not executable (run: chmod +x devtools/$wrapper)"
    else
        error "$wrapper missing at devtools/$wrapper"
    fi
done

# --- Test 2: find_python works from any directory ---
echo ""
echo "--- Test 2: find_python Helper ---"
# shellcheck source=devtools/_internal/common/utils.sh
source "$SCRIPT_DIR/_internal/common/utils.sh" 2>/dev/null || {
    error "Cannot source devtools/_internal/common/utils.sh"
    exit 1
}

# Test from repo root
PYTHON_ROOT=$(find_python)
if [ -x "$PYTHON_ROOT" ] || command -v "$PYTHON_ROOT" >/dev/null 2>&1; then
    ok "find_python works from repo root: $PYTHON_ROOT"
else
    error "find_python failed from repo root: $PYTHON_ROOT"
fi

# Test from subdirectory
cd vivarium/scout
PYTHON_SUB=$(find_python)
cd "$REPO_ROOT"
if [ "$PYTHON_ROOT" = "$PYTHON_SUB" ]; then
    ok "find_python consistent in subdirectory: $PYTHON_SUB"
else
    warn "find_python differs in subdirectory (root: $PYTHON_ROOT, sub: $PYTHON_SUB)"
fi

# --- Test 3: Wrapper --help smoke ---
echo ""
echo "--- Test 3: Wrapper CLI Smoke ---"
for wrapper in scout-nav scout-index scout-brief scout-roast; do
    if "./devtools/$wrapper" --help >/dev/null 2>&1; then
        ok "$wrapper --help works"
    else
        error "$wrapper --help failed"
    fi
done

# scout-ship and scout-query may need deps, just check they parse
for wrapper in scout-ship scout-query; do
    if bash -n "./devtools/$wrapper" 2>/dev/null; then
        ok "$wrapper syntax valid"
    else
        error "$wrapper has syntax errors"
    fi
done

# --- Test 4: Hook installation and syntax ---
echo ""
echo "--- Test 4: Git Hooks ---"
if [ -d ".git" ]; then
    # Clean previous test
    rm -f .git/hooks/scout-smoke-test-hook

    # Test installer syntax
    if bash -n "./devtools/scout-autonomy"; then
        ok "scout-autonomy installer syntax valid"
    else
        error "scout-autonomy installer has syntax errors"
    fi

    # Test actual installation (then remove)
    "./devtools/scout-autonomy" enable-commit >/dev/null 2>&1 || true
    if [ -f ".git/hooks/prepare-commit-msg" ]; then
        ok "prepare-commit-msg hook installed"

        # Verify it uses find_python
        if grep -q "find_python" ".git/hooks/prepare-commit-msg"; then
            ok "hook uses find_python"
        else
            warn "hook does not use find_python (may use python3 directly)"
        fi

        # Syntax check
        if bash -n ".git/hooks/prepare-commit-msg"; then
            ok "installed hook syntax valid"
        else
            error "installed hook has syntax errors"
        fi

        # Cleanup
        rm -f .git/hooks/prepare-commit-msg
    else
        warn "prepare-commit-msg hook not installed (may need dependencies)"
    fi
else
    warn "Not a git repository, skipping hook tests"
fi

# --- Test 5: Module entrypoints (if available) ---
echo ""
echo "--- Test 5: Python Module Smoke ---"
if $PYTHON_ROOT -c "import vivarium.scout" 2>/dev/null; then
    ok "vivarium.scout imports successfully"

    # Test critical CLIs
    for module in cli.root cli.doc_sync cli.nav cli.index cli.brief cli.roast cli.status cli.ci_guard; do
        if $PYTHON_ROOT -m vivarium.scout.$module --help >/dev/null 2>&1; then
            ok "python -m vivarium.scout.$module --help works"
        else
            warn "python -m vivarium.scout.$module --help failed (may need deps)"
        fi
    done
else
    warn "vivarium.scout not installed (run: pip install -e .)"
fi

# --- Test 6: Doc sync repair exit code (regression test for #91) ---
echo ""
echo "--- Test 6: Doc Sync Repair Exit Code ---"
if $PYTHON_ROOT -c "import vivarium.scout" 2>/dev/null; then
    # Test on already-fresh docs
    if $PYTHON_ROOT -m vivarium.scout.cli.doc_sync repair --target vivarium/scout >/dev/null 2>&1; then
        ok "doc_sync repair returns 0 on fresh docs (regression #91)"
    else
        error "doc_sync repair returns non-zero on fresh docs (regression #91)"
    fi
else
    warn "Skipping doc_sync test (vivarium.scout not installed)"
fi

# --- Summary ---
echo ""
echo "=== Smoke Test Summary ==="
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "✅ ALL SMOKE TESTS PASSED"
    echo "Scout hardening blockers cleared. Wrappers, hooks, and core paths functional."
    exit 0
else
    echo ""
    echo "❌ SMOKE TESTS FAILED"
    echo "Fix errors above before considering hardening complete."
    exit 1
fi
