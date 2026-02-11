#!/usr/bin/env bash
# Print velocity metrics (lines added/deleted, commits) for README.
# Run from repo root: ./scripts/velocity_metrics.sh

set -e
cd "$(dirname "$0")/.."

# 24 hours
ADD_24=$(git log --since='24 hours ago' --numstat --pretty=format:'' 2>/dev/null | awk '/^[0-9]/ { add += $1 } END { print add+0 }')
DEL_24=$(git log --since='24 hours ago' --numstat --pretty=format:'' 2>/dev/null | awk '/^[0-9]/ { del += $2 } END { print del+0 }')
COMMITS_24=$(git log --since='24 hours ago' --oneline 2>/dev/null | wc -l | tr -d ' ')

# 7 days
ADD_7=$(git log --since='7 days ago' --numstat --pretty=format:'' 2>/dev/null | awk '/^[0-9]/ { add += $1 } END { print add+0 }')
DEL_7=$(git log --since='7 days ago' --numstat --pretty=format:'' 2>/dev/null | awk '/^[0-9]/ { del += $2 } END { print del+0 }')
COMMITS_7=$(git log --since='7 days ago' --oneline 2>/dev/null | wc -l | tr -d ' ')

# Head
SHORT=$(git rev-parse --short HEAD 2>/dev/null)
DATE=$(git log -1 --format=%ci 2>/dev/null | cut -d' ' -f1)

echo "**Velocity (snapshot as of ${DATE}, \`${SHORT}\`).** Re-run \`./scripts/velocity_metrics.sh\` for current numbers."
echo ""
echo "| Window | Lines added | Lines deleted | Commits |"
echo "|--------|-------------|---------------|---------|"
printf "| 24h    | %s | %s | %s |\n" "$ADD_24" "$DEL_24" "$COMMITS_24"
printf "| 7d     | %s | %s | %s |\n" "$ADD_7" "$DEL_7" "$COMMITS_7"
