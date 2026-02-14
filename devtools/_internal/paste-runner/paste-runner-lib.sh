#!/usr/bin/env bash
# paste-runner-lib.sh — Helper functions for paste-runner CLI
# Sourced by devtools/paste-runner. Do not run directly.

# Strip comments (lines starting with #), empty lines, leading/trailing whitespace.
# Output: one command per line, no empty lines.
clean_paste_block() {
  local file="${1:?}"
  [[ -f "$file" ]] || { echo "File not found: $file" >&2; return 1; }
  grep -v '^[[:space:]]*#' "$file" | grep -v '^[[:space:]]*$' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v '^$'
}

# Syntax-check each command with bash -n. Returns 0 if all pass, 1 if any fail.
# Sets SYNTAX_ERRORS array with indices of failing commands (1-based).
syntax_check_commands() {
  local -a cmds=("$@")
  SYNTAX_ERRORS=()
  local i
  for i in "${!cmds[@]}"; do
    if ! bash -n -c "${cmds[$i]}" 2>/dev/null; then
      SYNTAX_ERRORS+=("$((i + 1))")
    fi
  done
  [[ ${#SYNTAX_ERRORS[@]} -eq 0 ]]
}

# Print numbered list of commands with optional syntax check markers.
preview_commands() {
  local -a cmds=("$@")
  syntax_check_commands "${cmds[@]}" || true
  local i
  for i in "${!cmds[@]}"; do
    local num=$((i + 1))
    local marker=""
    if [[ " ${SYNTAX_ERRORS[*]:-} " == *" $num "* ]]; then
      marker=" ⚠️ syntax?"
    fi
    printf "  %2d) %s%s\n" "$num" "${cmds[$i]}" "$marker"
  done
  if [[ ${#SYNTAX_ERRORS[@]:-0} -gt 0 ]]; then
    echo ""
    echo "⚠️  Syntax check failed for command(s): ${SYNTAX_ERRORS[*]}"
    return 1
  fi
  return 0
}

# Execute commands with logging. Stops on first failure unless CONTINUE=1.
# Logs to LOG_FILE. Respects DRY_RUN=1 (no execution).
execute_commands() {
  local -a cmds=("$@")
  local log_file="${LOG_FILE:?}"
  local continue_on_fail="${CONTINUE:-0}"
  local dry_run="${DRY_RUN:-0}"
  local exit_code=0

  {
    echo "=== Paste Runner Log ==="
    echo "Timestamp: $(date +%Y-%m-%d_%H-%M-%S)"
    echo "Commands: ${#cmds[@]}"
    echo "Dry run: $dry_run"
    echo "Continue on fail: $continue_on_fail"
    echo "--------------------------------"
  } >> "$log_file"

  local i
  for i in "${!cmds[@]}"; do
    local num=$((i + 1))
    local cmd="${cmds[$i]}"
    if [[ "$dry_run" == "1" ]]; then
      echo "[DRY-RUN] $num) $cmd" >> "$log_file"
      echo "[DRY-RUN] $num) $cmd"
      continue
    fi
    echo "" >> "$log_file"
    echo "--- Command $num ---" >> "$log_file"
    echo "$cmd" >> "$log_file"
    echo "--- Output ---" >> "$log_file"
    if bash -c "$cmd" >> "$log_file" 2>&1; then
      echo "--- Exit: 0 ---" >> "$log_file"
      echo "✅ $num) $cmd"
    else
      local ec=$?
      echo "--- Exit: $ec ---" >> "$log_file"
      echo "❌ $num) $cmd (exit $ec)"
      exit_code=$ec
      [[ "$continue_on_fail" != "1" ]] && return "$ec"
    fi
  done
  return "$exit_code"
}
