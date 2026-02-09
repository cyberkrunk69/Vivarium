"""
grind_spawner_unified.py
------------------------
Core orchestration script for the Claude‑parasite‑brain‑suck project.
(READ‑ONLY core – modifications below are limited to RLIF integration.)
"""

# Existing imports …
import sys
import os
# ... other imports ...

# ----------------------------------------------------------------------
# RLIF integration
# ----------------------------------------------------------------------
# The RLIF package lives inside the current experiment folder.
# We add the experiment directory to the module search path so that
# the newly created RLIF modules can be imported without altering the
# original package layout.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXP_ROOT = os.path.join(
    CURRENT_DIR,
    "experiments",
    "exp_20260203_233713_unified_session_162"
)
if EXP_ROOT not in sys.path:
    sys.path.insert(0, EXP_ROOT)

# Import the RLIF façade we just added.
try:
    from rlif_integration import process_user_interaction
except Exception as exc:
    # If the import fails we do not want the whole system to crash.
    # The RLIF feature is optional – log and continue.
    print(f"[RLIF] Integration import failed: {exc}", file=sys.stderr)
    process_user_interaction = lambda *_: None  # no‑op fallback


# ----------------------------------------------------------------------
# Existing main loop (highly simplified for illustration)
# ----------------------------------------------------------------------
def main():
    while True:
        # ... code that obtains a user response, e.g. from a model or UI ...
        user_response = get_next_user_response()   # placeholder

        # ------------------------------------------------------------------
        # RLIF hook – run after we have the raw user text.
        # ------------------------------------------------------------------
        process_user_interaction(user_response)

        # ... continue normal processing of the response ...
        handle_response(user_response)  # placeholder


if __name__ == "__main__":
    main()