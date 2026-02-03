#!/usr/bin/env python3
"""
Quick launcher for the Enhanced Engine Visibility Dashboard
Integrates with the existing Black Swarm ecosystem.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    # Add current directory to path so we can import modules
    current_dir = Path(__file__).parent
    workspace_dir = current_dir.parent.parent

    sys.path.insert(0, str(workspace_dir))

    print("🧠 Starting Enhanced Black Swarm Engine Visibility Dashboard")
    print(f"   Workspace: {workspace_dir}")
    print(f"   Experiment: exp_20260203_103351_unified_session_13")
    print()

    # Check if dependencies exist
    required_files = [
        workspace_dir / "wave_status.json",
        workspace_dir / "inference_engine.py",
        current_dir / "enhanced_progress_server.py"
    ]

    missing_files = []
    for file in required_files:
        if not file.exists():
            missing_files.append(file)

    if missing_files:
        print("⚠️  Warning: Some required files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        print()

    # Launch the enhanced progress server
    enhanced_server = current_dir / "enhanced_progress_server.py"

    try:
        print("🚀 Launching enhanced dashboard server...")
        print("   URL: http://localhost:8080")
        print("   Features: Engine visibility, model tracking, cost monitoring")
        print("   Press Ctrl+C to stop")
        print()

        # Run the enhanced server
        subprocess.run([
            sys.executable,
            str(enhanced_server),
            "--lan"  # Make it accessible on LAN
        ])

    except KeyboardInterrupt:
        print("\n🔴 Enhanced dashboard stopped")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())