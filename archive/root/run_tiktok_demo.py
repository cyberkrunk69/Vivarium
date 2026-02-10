# run_tiktok_demo.py
"""
run_tiktok_demo.py
------------------

A tiny driver script that automatically “plays” the 60‑second TikTok demo
defined in ``demo_scripts/tiktok_60s.json``.  It prints each line to the
console with timed pauses so that the whole sequence runs unattended – perfect
for screen‑recording a demo video.

The script:

1. Loads the JSON script.
2. Iterates through the ordered dialogue entries.
3. Sleeps for the ``delay`` (seconds) specified before showing the next line.
4. Prints the speaker name in a bold style (ANSI escape codes) followed by the
   spoken line.
5. Ends with the required “Link in bio” call‑to‑action.

No external dependencies are required beyond the Python standard library.
"""

import json
import time
import pathlib
import sys

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

SCRIPT_PATH = pathlib.Path(__file__).parent / "demo_scripts" / "tiktok_60s.json"

# ANSI escape codes for a simple “bold” speaker label.
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"


def load_script(path: pathlib.Path):
    """Load the JSON dialogue script."""
    if not path.is_file():
        sys.stderr.write(f"❌ Script file not found: {path}\n")
        sys.exit(1)

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def play_demo(script):
    """
    Play the demo by printing each line with the appropriate pause.
    The total runtime is designed to be roughly 60 seconds.
    """
    start_time = time.time()
    for entry in script["dialogue"]:
        # Respect the configured pause before showing the line.
        delay = entry.get("delay", 0)
        time.sleep(delay)

        speaker = entry.get("character", "Unknown")
        line = entry.get("line", "")

        # Print speaker in bold for readability.
        print(f"{ANSI_BOLD}{speaker}:{ANSI_RESET} {line}")

    # Final “Link in bio” prompt – no extra delay, just a clear end.
    print("\n🔗 " + f"{ANSI_BOLD}Link in bio{ANSI_RESET}")


def main():
    script = load_script(SCRIPT_PATH)
    print("▶️  Starting the 60‑second TikTok demo…\n")
    play_demo(script)
    total = time.time() - start_time
    print(f"\n⏱️  Demo finished (elapsed: {total:.1f}s)")


if __name__ == "__main__":
    main()