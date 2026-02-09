#!/usr/bin/env bash
# install_linux.sh
# -------------------------------------------------
# Interdimensional Radio - One-Click Installer
# -------------------------------------------------
# This script performs the following steps:
#   1. Checks for Python 3.11+ installation
#   2. Creates a virtual environment (venv) if missing
#   3. Installs required Python packages
#   4. Downloads required AI models with a progress bar
#   5. Sets up default characters
#   6. Launches the Interdimensional Radio application
# -------------------------------------------------

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

# ---------- 1. Verify Python ----------
if ! command -v python3 >/dev/null 2>&1; then
    print_error "Python 3 not found. Please install Python 3.11+ and ensure 'python3' is in your PATH."
fi

PY_VER=$(python3 -c 'import sys, json; print(json.dumps({"major": sys.version_info.major, "minor": sys.version_info.minor}))')
PY_MAJOR=$(echo "$PY_VER" | python3 -c "import sys, json, sys; print(json.load(sys.stdin)['major'])")
PY_MINOR=$(echo "$PY_VER" | python3 -c "import sys, json, sys; print(json.load(sys.stdin)['minor'])")

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 11 ]; }; then
    print_error "Python version $PY_MAJOR.$PY_MINOR detected. Minimum required is 3.11."
else
    print_info "Detected Python $PY_MAJOR.$PY_MINOR - OK."
fi

# ---------- 2. Create / Activate Virtual Environment ----------
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv || print_error "Failed to create virtual environment."
else
    print_info "Virtual environment already exists."
fi

# Activate venv
# shellcheck disable=SC1091
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel >/dev/null
print_info "Upgraded pip."

# ---------- 3. Install Requirements ----------
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in the current directory."
fi

print_info "Installing Python dependencies..."
python -m pip install -r requirements.txt
print_info "Dependencies installed."

# ---------- 4. Download Required Models ----------
# Expect a file named models.txt with lines: <URL> <TARGET_PATH>
if [ ! -f "models.txt" ]; then
    print_error "models.txt not found. Cannot download required models."
fi

print_info "Downloading required models..."
while read -r URL TARGET; do
    # Skip empty lines or comments
    [[ -z "$URL" || "$URL" =~ ^# ]] && continue
    if [ -f "$TARGET" ]; then
        print_info "Model already present at $TARGET – skipping."
        continue
    fi
    mkdir -p "$(dirname "$TARGET")"
    print_info "Downloading $URL -> $TARGET"
    # Use curl with a progress bar
    curl -L --progress-bar "$URL" -o "$TARGET" || print_error "Failed to download model from $URL"
done < models.txt

# ---------- 5. Set Up Default Characters ----------
# Assuming default characters are stored in "default_characters" folder
if [ -d "default_characters" ]; then
    mkdir -p data/characters
    print_info "Copying default characters..."
    cp -r default_characters/* data/characters/
else
    print_info "No default_characters folder found – skipping character setup."
fi

# ---------- 6. Launch the Application ----------
print_info "Launching Interdimensional Radio..."
# Adjust the entry point if your project uses a different module or script
python -m interdimensional_radio
# If the above returns a non‑zero exit code, the script will already have exited due to set -e