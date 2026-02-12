#!/usr/bin/env bash
# api-confirm.sh — Unified API confirmation for devtools scripts
# Sourced by scripts that may call external APIs (Groq, GitHub, etc.).
# Supports: VIVARIUM_CONFIRM_AI=1 (auto-confirm), interactive prompt, non-interactive default.

# Usage:
#   source api-confirm.sh
#   confirm_api_call "Estimated Groq API cost: \$0.05 for 3 job(s)." "Proceed with API calls?"
#   # Returns 0 if confirmed, 1 if declined. Sets API_CONFIRMED=1/0.

# Check if we should auto-confirm (env var set)
# VIVARIUM_CONFIRM_AI=1 means user has pre-approved; skip prompt
check_auto_confirm() {
  [[ "${VIVARIUM_CONFIRM_AI:-}" == "1" ]] || [[ "${VIVARIUM_CONFIRM_AI:-}" == "yes" ]]
}

# Prompt user for API confirmation. Works in CLI and when launched from .app (Terminal gets TTY).
# Args: $1=cost_message (e.g. "Estimated cost: \$0.05 for 3 job(s)")
#       $2=prompt_text (default: "Execute with this cost?")
# Reads REPLY from user; returns 0 if y/yes, 1 otherwise.
# When non-interactive (pipe, no TTY): returns 1 (decline).
confirm_api_call() {
  local cost_message="${1:-}"
  local prompt_text="${2:-Execute with this cost? [y/n]}"

  if check_auto_confirm; then
    return 0
  fi

  if [[ ! -t 0 ]]; then
    # Non-interactive: stdin is pipe (e.g. echo "n" | ci-status)
    local reply
    reply=$(head -1)
    reply=$(echo "$reply" | tr '[:upper:]' '[:lower:]')
    [[ "$reply" == "y" ]] || [[ "$reply" == "yes" ]] && return 0
    return 1
  fi

  echo ""
  [[ -n "$cost_message" ]] && echo "$cost_message"
  echo -n "$prompt_text "
  local reply
  if read -r reply 2>/dev/null; then
    reply=$(echo "$reply" | tr '[:upper:]' '[:lower:]')
    [[ "$reply" == "y" ]] || [[ "$reply" == "yes" ]] && return 0
  fi
  return 1
}

# Same as confirm_api_call but for scripts that need to pass confirmation to child process.
# Prints "y" or "n" to stdout based on user input; caller can capture and pipe to child.
confirm_api_call_and_echo() {
  if check_auto_confirm; then
    echo "y"
    return 0
  fi

  if [[ ! -t 0 ]]; then
    local reply
    reply=$(head -1)
    reply=$(echo "$reply" | tr '[:upper:]' '[:lower:]')
    if [[ "$reply" == "y" ]] || [[ "$reply" == "yes" ]]; then
      echo "y"
      return 0
    fi
    echo "n"
    return 1
  fi

  echo ""
  [[ -n "${1:-}" ]] && echo "$1"
  echo -n "Execute with this cost? [y/n] "
  local reply
  if read -r reply 2>/dev/null; then
    reply=$(echo "$reply" | tr '[:upper:]' '[:lower:]')
    if [[ "$reply" == "y" ]] || [[ "$reply" == "yes" ]]; then
      echo "y"
      return 0
    fi
  fi
  echo "n"
  return 1
}
