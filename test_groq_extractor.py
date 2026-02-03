#!/usr/bin/env python3
"""
Test the Groq code extractor with a simple task that creates a file.
"""

import json
from pathlib import Path
from groq_code_extractor import GroqArtifactExtractor

def test_simple_file_creation():
    """Test extractor with a simple file creation task."""

    # Initialize extractor with test workspace
    test_workspace = Path("./test_output")
    extractor = GroqArtifactExtractor(workspace_root=str(test_workspace))

    # Simulate a model response that creates a simple file
    mock_response = '''I'll create a simple hello world script for you.

<artifact type="file" path="hello_world.py" encoding="utf-8">
#!/usr/bin/env python3
"""
Simple hello world script created by Groq model.
"""

def main():
    print("Hello, World!")
    print("This file was created using the Groq artifact extractor!")

if __name__ == "__main__":
    main()
</artifact>

I've created a simple Python script that prints a greeting message.'''

    # Extract and save files
    print("Testing Groq artifact extractor...")
    print(f"Workspace: {test_workspace}")
    print("\nMock response:")
    print("-" * 50)
    print(mock_response[:200] + "...")
    print("-" * 50)

    saved_files = extractor.extract_and_save(mock_response)

    print(f"\nExtracted files: {saved_files}")

    # Verify the file was created
    if saved_files:
        for file_path in saved_files:
            full_path = test_workspace / file_path
            if full_path.exists():
                print(f"[OK] File created: {full_path}")
                print(f"  Size: {full_path.stat().st_size} bytes")

                # Show first few lines
                content = full_path.read_text(encoding="utf-8")
                lines = content.split('\n')[:5]
                print(f"  Content preview:")
                for i, line in enumerate(lines, 1):
                    print(f"    {i}: {line}")
            else:
                print(f"[ERROR] File not found: {full_path}")
    else:
        print("[ERROR] No files were extracted")

    # Get extraction stats
    stats = extractor.get_extraction_stats(mock_response)
    print(f"\nExtraction statistics:")
    print(f"  Total artifacts: {stats['total_artifacts']}")
    print(f"  File types: {stats['file_types']}")
    print(f"  Total size: {stats['total_size']} bytes")
    print(f"  Paths: {stats['paths']}")

if __name__ == "__main__":
    test_simple_file_creation()