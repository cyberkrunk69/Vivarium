import os

APPLIED = "APPLIED"
FAILED = "FAILED"

def verify_file_changed(filepath: str, expected_content_snippet: str) -> str:
    """
    Verify that the file at ``filepath`` contains ``expected_content_snippet``.
    Returns ``APPLIED`` if the snippet is found, otherwise ``FAILED``.
    """
    if not os.path.isfile(filepath):
        return FAILED
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return FAILED

    if expected_content_snippet in content:
        return APPLIED
    return FAILED

# ----------------------------------------------------------------------
# Integration hint for ``grind_spawner_unified.py``:
# ----------------------------------------------------------------------
# Locate the point in ``grind_spawner_unified.py`` where the file modifications
# have just been written to disk (typically after a ``with open(..., "w")`` block).
# Insert the following two lines *exactly* at that location:
#
#   status = verify_file_changed(target_path, "<expected snippet>")
#   print(f"Verification result for {target_path}: {status}")
#
# Replace ``target_path`` with the variable that holds the path of the file you
# just modified, and replace ``<expected snippet>`` with a short, unique string
# that should appear in the file after the change (e.g., a function name,
# comment marker, or any literal you inserted).
# The function will return ``APPLIED`` if the snippet is present, otherwise
# ``FAILED``.