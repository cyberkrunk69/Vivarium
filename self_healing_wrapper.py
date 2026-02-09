"""
Self-Healing Wrapper for Grind Spawner

Wraps the spawner with health checks, automatic rollback, and crash loop detection.
"""

import sys
import subprocess
import time
import traceback
from pathlib import Path
from typing import Optional, Tuple

from safety_validator import (
    HealthChecker,
    CheckpointManager,
    validate_critical_files,
    SyntaxValidator
)


class SelfHealingSpawner:
    """
    Wraps the grind spawner with self-healing capabilities.

    Features:
    - Detects crash loops
    - Validates critical files on startup
    - Auto-rollback on repeated failures
    - Safe mode when things are broken
    """

    def __init__(self):
        self.health_checker = HealthChecker()
        self.checkpoint_manager = CheckpointManager()
        self.safe_mode = False

    def startup_health_check(self) -> Tuple[bool, str]:
        """
        Check if it's safe to start the spawner.

        Returns:
            (is_healthy, reason)
        """
        # Check for crash loop
        if self.health_checker.is_crash_loop(threshold=3):
            info = self.health_checker.get_crash_loop_info()
            return False, f"Crash loop detected: {info['consecutive_failures']} consecutive failures"

        # Validate critical files
        validation_errors = validate_critical_files()
        if validation_errors:
            error_details = []
            for result in validation_errors:
                error_details.append(f"{result.file_path}: {', '.join(result.errors)}")
            return False, f"Critical file validation failed:\n" + "\n".join(error_details)

        return True, "Health check passed"

    def attempt_auto_heal(self) -> bool:
        """
        Attempt to automatically fix issues.

        Returns:
            True if healing was successful
        """
        print("[SELF-HEAL] Attempting automatic recovery...")

        # Get the latest checkpoint
        latest_checkpoint = self.checkpoint_manager.get_latest_checkpoint()

        if not latest_checkpoint:
            print("[SELF-HEAL] No checkpoints available for rollback")
            return False

        print(f"[SELF-HEAL] Rolling back to checkpoint: {latest_checkpoint.checkpoint_id}")
        print(f"[SELF-HEAL] Created: {latest_checkpoint.timestamp}")
        print(f"[SELF-HEAL] Reason: {latest_checkpoint.reason}")

        success, result = self.checkpoint_manager.rollback(latest_checkpoint)

        if success:
            print(f"[SELF-HEAL] ✓ Rolled back {len(result)} files:")
            for filepath in result:
                print(f"  - {filepath}")

            # Re-validate after rollback
            validation_errors = validate_critical_files()
            if not validation_errors:
                print("[SELF-HEAL] ✓ Validation passed after rollback")
                return True
            else:
                print("[SELF-HEAL] ✗ Still have errors after rollback")
                return False
        else:
            print(f"[SELF-HEAL] ✗ Rollback failed: {result}")
            return False

    def enter_safe_mode(self):
        """
        Enter safe mode - minimal functionality to prevent further damage.
        """
        print("\n" + "=" * 70)
        print("ENTERING SAFE MODE")
        print("=" * 70)
        print("\nThe swarm has been stopped to prevent further self-damage.")
        print("\nIssues detected:")

        info = self.health_checker.get_crash_loop_info()
        print(f"  - Consecutive failures: {info['consecutive_failures']}")
        print(f"  - Last startup attempt: {info['last_startup_attempt']}")

        validation_errors = validate_critical_files()
        if validation_errors:
            print("\nFile validation errors:")
            for result in validation_errors:
                print(f"\n  {result.file_path}:")
                for error in result.errors:
                    print(f"    - {error}")

        print("\nRecovery options:")
        print("  1. Fix the errors manually")
        print("  2. Use safety_validator.py to rollback to last checkpoint")
        print("  3. Reset health status: rm .health_status.json")
        print("\nExiting...")
        self.safe_mode = True

    def run(self):
        """
        Main entry point - run the spawner with self-healing.
        """
        print("=" * 70)
        print("Self-Healing Spawner Starting...")
        print("=" * 70)

        # Record startup attempt
        self.health_checker.record_startup_attempt()

        # Health check
        is_healthy, reason = self.startup_health_check()

        if not is_healthy:
            print(f"\n[HEALTH CHECK] ✗ Failed: {reason}\n")

            # Attempt auto-heal
            if self.attempt_auto_heal():
                print("[HEALTH CHECK] ✓ Auto-heal successful, retrying startup...")
                # Reset failure counter
                self.health_checker.record_startup_success()
                # Try again
                is_healthy, reason = self.startup_health_check()

            if not is_healthy:
                self.enter_safe_mode()
                return 1

        print("[HEALTH CHECK] ✓ All systems go\n")

        try:
            # Import and run the actual spawner
            from grind_spawner_unified import main as spawner_main

            # Record successful startup
            self.health_checker.record_startup_success()

            # Run the spawner
            return spawner_main()

        except ImportError as e:
            print(f"\n[ERROR] Failed to import grind_spawner_unified: {e}")
            traceback.print_exc()
            return 1

        except SyntaxError as e:
            print(f"\n[ERROR] Syntax error in spawner: {e}")
            print(f"  File: {e.filename}")
            print(f"  Line: {e.lineno}")
            print(f"  Text: {e.text}")

            # This is a critical error - try to rollback
            if self.attempt_auto_heal():
                print("\n[RECOVERY] Auto-heal successful")
                print("Please restart the spawner")
                return 0
            else:
                self.enter_safe_mode()
                return 1

        except KeyboardInterrupt:
            print("\n\n[SHUTDOWN] Interrupted by user")
            return 0

        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
            traceback.print_exc()

            # Record failure
            print("\n[RECOVERY] Recording failure...")
            return 1


def main():
    """Entry point for self-healing wrapper."""
    wrapper = SelfHealingSpawner()
    sys.exit(wrapper.run())


if __name__ == "__main__":
    main()
