"""
groq_code_extractor.py

Extracts code snippets from Groq responses and writes them to disk.
Now integrated with the quality validator to ensure generated code meets
the project's quality standards before being persisted.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

# Local imports
from .quality_validator import validate_all  # <-- New integration


def extract_and_write_code(response: Dict[str, Any], output_dir: str) -> None:
    """
    Given a Groq response dictionary, extract any code blocks and write them
    to files inside ``output_dir``. Each code block is validated before being
    written; if validation fails, the file is not created and an error is logged.

    Args:
        response: Parsed JSON response from Groq containing a ``code`` field.
        output_dir: Directory where extracted files should be placed.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Assume the response contains a list of entries with ``filename`` and ``code``.
    for entry in response.get("files", []):
        filename = entry.get("filename")
        code = entry.get("code", "")

        if not filename:
            continue  # Skip malformed entries

        target_path = Path(output_dir) / filename

        # ----- QUALITY VALIDATION -----
        passed, errors = validate_all(code, str(target_path))
        if not passed:
            # Log the validation failures; in a real system you might raise an
            # exception or collect these for reporting.
            print(f"[QUALITY VALIDATION FAILED] {target_path}:")
            for err in errors:
                print(f"  - {err}")
            # Skip writing the invalid file.
            continue
        # ----- END VALIDATION -----

        # Write the validated code to disk.
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"[WRITE SUCCESS] {target_path}")
        except OSError as exc:
            print(f"[WRITE ERROR] {target_path}: {exc}")


def load_groq_response(path: str) -> Dict[str, Any]:
    """
    Load a Groq JSON response from ``path``.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # Example usage:
    import sys

    if len(sys.argv) != 3:
        print("Usage: python groq_code_extractor.py <response.json> <output_dir>")
        sys.exit(1)

    response_path = sys.argv[1]
    output_directory = sys.argv[2]

    response_data = load_groq_response(response_path)
    extract_and_write_code(response_data, output_directory)