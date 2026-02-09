# INSTALL_GUIDE.md

# Interdimensional Radio – One‑Click Installer

Welcome! This guide explains how to install and run **Interdimensional Radio** on Windows, Linux, or macOS with a single click.  
After the initial setup you can run the application offline – no further downloads are required.

---

## Table of Contents
1. [Prerequisites](#prerequisites)  
2. [Installation Steps](#installation-steps)  
   - [Windows](#windows)  
   - [Linux / macOS](#linux-macos)  
3. [What the Installer Does](#what-the-installer-does)  
4. [Troubleshooting](#troubleshooting)  
5. [Running the App Manually (Optional)](#running-manually)  

---

## Prerequisites

| Platform | Required Software |
|----------|-------------------|
| **All**  | **Python 3.11** or newer (must be added to your `PATH`). |
| Windows  | No additional tools – the installer uses built‑in `powershell` for progress bars. |
| Linux/macOS | `curl` (usually pre‑installed) and `bash`. |

> **Tip:** If you are unsure whether Python is installed, open a terminal / command prompt and run `python3 --version` (Linux/macOS) or `python --version` (Windows). The version must be **3.11** or higher.

---

## Installation Steps

### Windows

1. **Download the installer**
   - Save `install_windows.bat` into the root folder of the Interdimensional Radio project (the same folder that contains `requirements.txt`).

2. **Run the installer**
   - Double‑click `install_windows.bat` or right‑click → *Run as administrator* (admin rights are only needed for creating the virtual environment).

3. **Sit back**  
   The script will:
   - Verify Python,
   - Create a virtual environment (`venv`),
   - Install all Python dependencies,
   - Download the AI model files,
   - Populate default characters,
   - Launch the app.

4. **First launch complete!**  
   Subsequent launches can be done by running `venv\Scripts\activate.bat` and then `python -m interdimensional_radio`, or simply by re‑running `install_windows.bat` (it will skip already‑done steps).

---

### Linux / macOS

1. **Download the installer**
   - Save `install_linux.sh` into the root folder of the project (next to `requirements.txt`).

2. **Make it executable**
   ```bash
   chmod +x install_linux.sh
   ```

3. **Run the installer**
   ```bash
   ./install_linux.sh
   ```

4. **Enjoy!**  
   The script performs the same actions as the Windows version and finally starts the application.

---

## What the Installer Does

| Step | Description |
|------|-------------|
| **Python check** | Ensures `python3` (or `python` on Windows) is version **3.11** or newer. |
| **Virtual environment** | Creates a folder called `venv` (if it does not already exist) and isolates all packages from the system Python. |
| **Dependency installation** | Runs `pip install -r requirements.txt` inside the virtual environment. |
| **Model download** | Reads `models.txt` (each line: `<URL> <local_path>`) and downloads the required model files with a progress bar. Files are saved exactly where the application expects them. |
| **Default characters** | Copies everything from `default_characters/` into `data/characters/` (creating the directories if needed). |
| **Launch** | Starts the main module (`python -m interdimensional_radio`). If the launch fails you’ll see a clear error message. |

> **Note:** After the first successful run you can disconnect from the internet – all required assets are stored locally.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| `Python not found` | Python not installed or not on `PATH`. | Install Python 3.11+ from https://www.python.org/downloads/ and **check** the “Add Python to PATH” option (Windows) or add `export PATH="/path/to/python:$PATH"` (Linux/macOS). |
| `Python version < 3.11` | Older Python version present. | Upgrade Python to 3.11 or newer. |
| `Failed to create virtual environment` | Permissions issue or missing `venv` module. | Run the installer as Administrator (Windows) or with `sudo` (Linux) **or** install the `venv` module (`sudo apt install python3.11-venv`). |
| `pip install` fails | Network problem or corrupted `requirements.txt`. | Ensure you have internet for the first run, then retry. |
| Model download stalls or fails | Wrong URL, network block, or missing `curl`/`powershell`. | Verify the URLs in `models.txt`. On Linux/macOS, make sure `curl` works (`curl -V`). |
| Application crashes on start | Missing model files or character data. | Re‑run the installer – it will skip existing steps and only download missing assets. |
| `python -m interdimensional_radio` not found | Wrong entry point. | Check the project's documentation for the correct module name and edit the last line of the installer accordingly. |

If you encounter an error that isn’t covered above, please open an issue on the project repository with the full console output.

---

## Running the App Manually (Optional)

If you prefer to start the program without re‑running the installer: