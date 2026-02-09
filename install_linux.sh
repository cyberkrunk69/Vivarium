# install_linux.sh
#!/usr/bin/env bash

# -------------------------------------------------
# Interdimensional Radio - One-Click Installer
# -------------------------------------------------
# This script will:
#   1. Verify Python 3.11+ is installed
#   2. Create a virtual environment (if missing)
#   3. Install required Python packages
#   4. Download the necessary AI models (with progress bar)
#   5. Set up default characters
#   6. Launch the application
# -------------------------------------------------

set -e

# ==== 1. Check for Python 3.11+ ====
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python3 is not installed or not in PATH."
    echo "Please install Python 3.11+ from https://www.python.org/downloads/."
    exit 1
fi

PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
MAJOR=$(echo "$PYVER" | cut -d. -f1)
MINOR=$(echo "$PYVER" | cut -d. -f2)

if (( MAJOR < 3 )) || { (( MAJOR == 3 )) && (( MINOR < 11 )); }; then
    echo "[ERROR] Detected Python $PYVER. Python 3.11+ is required."
    exit 1
fi

echo "[INFO] Python $PYVER found."

# ==== 2. Create virtual environment if missing ====
if [ ! -d "./venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[INFO] Virtual environment already exists."
fi

# ==== 3. Activate venv and install requirements ====
source ./venv/bin/activate

echo "[INFO] Upgrading pip..."
pip install --upgrade pip

if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] requirements.txt not found in the current directory."
    exit 1
fi

echo "[INFO] Installing Python dependencies..."
pip install -r requirements.txt

# ==== 4. Download required models ====
MODEL_DIR="./models"
mkdir -p "$MODEL_DIR"

# Define model URLs (replace with actual URLs)
MODEL_URLS=(
    "https://example.com/models/model_a.zip"
    "https://example.com/models/model_b.zip"
)

for URL in "${MODEL_URLS[@]}"; do
    FILE_NAME=$(basename "$URL")
    DEST_PATH="$MODEL_DIR/$FILE_NAME"

    if [ -f "$DEST_PATH" ]; then
        echo "[INFO] Model $FILE_NAME already downloaded."
    else
        echo "[INFO] Downloading $FILE_NAME..."
        # Use curl with a progress bar
        if command -v curl &>/dev/null; then
            curl -L "$URL" -o "$DEST_PATH" --progress-bar
        elif command -v wget &>/dev/null; then
            wget "$URL" -O "$DEST_PATH" --show-progress
        else
            echo "[ERROR] Neither curl nor wget is available to download files."
            exit 1
        fi

        # If the file is a zip, extract it
        if [[ "$FILE_NAME" == *.zip ]]; then
            echo "[INFO] Extracting $FILE_NAME..."
            unzip -o "$DEST_PATH" -d "$MODEL_DIR"
            rm "$DEST_PATH"
        fi
    fi
done

# ==== 5. Set up default characters ====
CHAR_DIR="./characters"
mkdir -p "$CHAR_DIR"

if [ -d "./default_characters" ]; then
    echo "[INFO] Copying default characters..."
    cp -r ./default_characters/* "$CHAR_DIR"/
else
    echo "[WARNING] No default_characters folder found. Skipping character setup."
fi

# ==== 6. Launch the application ====
echo "[INFO] Launching Interdimensional Radio..."
# Adjust the entry point as needed (e.g., main.py or a module)
python -m interdimensional_radio || {
    echo "[ERROR] Application failed to start."
    exit 1
}