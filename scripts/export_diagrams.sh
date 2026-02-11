#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SRC_DIR="${REPO_ROOT}/docs/assets/diagrams/src"
OUT_DIR="${REPO_ROOT}/docs/assets/diagrams"

FILES=(
  "system-design"
  "quest-lifecycle"
  "task-review-state-machine"
)

DRAWIO_BIN=""
for candidate in drawio drawio-desktop; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    DRAWIO_BIN="${candidate}"
    break
  fi
done

if [[ -z "${DRAWIO_BIN}" ]]; then
  echo "draw.io CLI not found (expected drawio or drawio-desktop on PATH)." >&2
  echo "Install draw.io desktop/CLI, or export SVG manually from diagrams.net." >&2
  exit 1
fi

echo "Using ${DRAWIO_BIN} to export diagrams..."
for name in "${FILES[@]}"; do
  src="${SRC_DIR}/${name}.drawio"
  out="${OUT_DIR}/${name}.svg"

  if [[ ! -f "${src}" ]]; then
    echo "Missing source file: ${src}" >&2
    exit 1
  fi

  "${DRAWIO_BIN}" --export --format svg --output "${out}" "${src}"
  echo "Exported ${out}"
done

echo "Diagram export complete."
