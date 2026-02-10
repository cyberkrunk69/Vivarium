"""
Safety Validator - Prevents the swarm from breaking itself.

Validates code before writing, creates checkpoints, enables rollback.
"""

import ast
import hashlib
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of validating a file change."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    file_path: str

    def is_safe_to_write(self) -> bool:
        """Whether it's safe to write this file."""
        return self.valid and len(self.errors) == 0


@dataclass
class Checkpoint:
    """Snapshot of file state before modification."""
    checkpoint_id: str
    timestamp: str
    files: Dict[str, str]  # path -> content_hash
    backup_dir: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Checkpoint':
        return cls(**data)


class SyntaxValidator:
    """Validates Python syntax before writing files."""

    @staticmethod
    def validate_python(code: str, filepath: str = "<string>") -> ValidationResult:
        """
        Validate Python syntax.

        Returns:
            ValidationResult with errors/warnings
        """
        errors = []
        warnings = []

        try:
            ast.parse(code, filename=filepath)
        except SyntaxError as e:
            errors.append(f"SyntaxError at line {e.lineno}: {e.msg}")
        except Exception as e:
            errors.append(f"Parse error: {str(e)}")

        # Check for common issues
        if len(code.strip()) == 0:
            warnings.append("File is empty")

        # Check for unclosed strings/brackets (additional validation)
        try:
            compile(code, filepath, 'exec')
        except SyntaxError as e:
            if "SyntaxError" not in str(errors):
                errors.append(f"Compilation error at line {e.lineno}: {e.msg}")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            file_path=filepath
        )

    @staticmethod
    def validate_file(filepath: Path) -> ValidationResult:
        """Validate an existing Python file."""
        if not filepath.exists():
            return ValidationResult(
                valid=False,
                errors=[f"File not found: {filepath}"],
                warnings=[],
                file_path=str(filepath)
            )

        if filepath.suffix != '.py':
            # Non-Python files are assumed valid
            return ValidationResult(
                valid=True,
                errors=[],
                warnings=[f"Non-Python file, skipping syntax check"],
                file_path=str(filepath)
            )

        try:
            code = filepath.read_text(encoding='utf-8')
            return SyntaxValidator.validate_python(code, str(filepath))
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Failed to read file: {e}"],
                warnings=[],
                file_path=str(filepath)
            )


class CheckpointManager:
    """Manages file snapshots for rollback capability."""

    def __init__(self, checkpoint_dir: Path = None):
        self.checkpoint_dir = checkpoint_dir or Path(".checkpoints")
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.checkpoint_index = self.checkpoint_dir / "index.json"

    def create_checkpoint(self, files: List[Path], reason: str = "pre-modification") -> Checkpoint:
        """
        Create a checkpoint of specified files.

        Args:
            files: List of file paths to checkpoint
            reason: Why this checkpoint was created

        Returns:
            Checkpoint object
        """
        checkpoint_id = hashlib.sha256(
            f"{datetime.now().isoformat()}{reason}".encode()
        ).hexdigest()[:12]

        timestamp = datetime.now().isoformat()
        backup_dir = self.checkpoint_dir / checkpoint_id
        backup_dir.mkdir(exist_ok=True)

        file_hashes = {}

        for filepath in files:
            if not filepath.exists():
                continue

            # Calculate hash
            content = filepath.read_bytes()
            content_hash = hashlib.sha256(content).hexdigest()
            file_hashes[str(filepath)] = content_hash

            # Copy to backup
            backup_path = backup_dir / filepath.name
            shutil.copy2(filepath, backup_path)

        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            timestamp=timestamp,
            files=file_hashes,
            backup_dir=str(backup_dir),
            reason=reason
        )

        # Update index
        self._update_index(checkpoint)

        return checkpoint

    def rollback(self, checkpoint: Checkpoint) -> Tuple[bool, List[str]]:
        """
        Rollback to a checkpoint.

        Returns:
            (success, list of restored files)
        """
        backup_dir = Path(checkpoint.backup_dir)
        if not backup_dir.exists():
            return False, [f"Backup directory not found: {backup_dir}"]

        restored = []
        errors = []

        for filepath_str, expected_hash in checkpoint.files.items():
            filepath = Path(filepath_str)
            backup_file = backup_dir / filepath.name

            if not backup_file.exists():
                errors.append(f"Backup not found: {backup_file}")
                continue

            try:
                shutil.copy2(backup_file, filepath)
                restored.append(str(filepath))
            except Exception as e:
                errors.append(f"Failed to restore {filepath}: {e}")

        return len(errors) == 0, restored if len(errors) == 0 else errors

    def _update_index(self, checkpoint: Checkpoint):
        """Update the checkpoint index."""
        index = []
        if self.checkpoint_index.exists():
            try:
                index = json.loads(self.checkpoint_index.read_text())
            except:
                pass

        index.append(checkpoint.to_dict())

        # Keep only last 50 checkpoints
        index = index[-50:]

        self.checkpoint_index.write_text(json.dumps(index, indent=2))

    def list_checkpoints(self) -> List[Checkpoint]:
        """List all available checkpoints."""
        if not self.checkpoint_index.exists():
            return []

        try:
            index = json.loads(self.checkpoint_index.read_text())
            return [Checkpoint.from_dict(c) for c in index]
        except:
            return []

    def get_latest_checkpoint(self) -> Optional[Checkpoint]:
        """Get the most recent checkpoint."""
        checkpoints = self.list_checkpoints()
        return checkpoints[-1] if checkpoints else None


class HealthChecker:
    """Detects crash loops and startup failures."""

    def __init__(self, health_file: Path = None):
        self.health_file = health_file or Path(".health_status.json")

    def record_startup_attempt(self):
        """Record that a startup was attempted."""
        status = self._load_status()
        status["last_startup_attempt"] = datetime.now().isoformat()
        status["startup_attempts"] = status.get("startup_attempts", 0) + 1
        status["consecutive_failures"] = status.get("consecutive_failures", 0) + 1
        self._save_status(status)

    def record_startup_success(self):
        """Record successful startup."""
        status = self._load_status()
        status["last_successful_startup"] = datetime.now().isoformat()
        status["consecutive_failures"] = 0
        self._save_status(status)

    def is_crash_loop(self, threshold: int = 3) -> bool:
        """
        Check if we're in a crash loop.

        Args:
            threshold: Number of consecutive failures to consider a crash loop

        Returns:
            True if in crash loop
        """
        status = self._load_status()
        return status.get("consecutive_failures", 0) >= threshold

    def get_crash_loop_info(self) -> dict:
        """Get information about the crash loop."""
        status = self._load_status()
        return {
            "consecutive_failures": status.get("consecutive_failures", 0),
            "last_startup_attempt": status.get("last_startup_attempt"),
            "last_successful_startup": status.get("last_successful_startup"),
            "total_attempts": status.get("startup_attempts", 0)
        }

    def _load_status(self) -> dict:
        """Load health status."""
        if not self.health_file.exists():
            return {}
        try:
            return json.loads(self.health_file.read_text())
        except:
            return {}

    def _save_status(self, status: dict):
        """Save health status."""
        self.health_file.write_text(json.dumps(status, indent=2))


class SafeFileWriter:
    """
    Safe file writing with validation and checkpointing.

    Usage:
        writer = SafeFileWriter()
        result = writer.safe_write(filepath, content)
        if not result.valid:
            print(f"Failed: {result.errors}")
    """

    def __init__(self):
        self.validator = SyntaxValidator()
        self.checkpoint_manager = CheckpointManager()

    def safe_write(
        self,
        filepath: Path,
        content: str,
        create_checkpoint: bool = True,
        force: bool = False
    ) -> ValidationResult:
        """
        Safely write a file with validation and checkpointing.

        Args:
            filepath: Path to write
            content: Content to write
            create_checkpoint: Whether to create a checkpoint first
            force: Skip validation and write anyway (dangerous!)

        Returns:
            ValidationResult
        """
        filepath = Path(filepath)

        # Validate before writing
        if filepath.suffix == '.py' and not force:
            result = self.validator.validate_python(content, str(filepath))
            if not result.is_safe_to_write():
                return result

        # Create checkpoint if file exists
        if create_checkpoint and filepath.exists():
            self.checkpoint_manager.create_checkpoint(
                [filepath],
                reason=f"Before writing {filepath.name}"
            )

        # Write the file
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content, encoding='utf-8')

            return ValidationResult(
                valid=True,
                errors=[],
                warnings=[],
                file_path=str(filepath)
            )
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Write failed: {e}"],
                warnings=[],
                file_path=str(filepath)
            )


def validate_critical_files() -> List[ValidationResult]:
    """
    Validate all critical Python files in the project.

    Returns:
        List of validation results for files with errors
    """
    critical_files = [
        "vivarium/runtime/worker_runtime.py",
        "vivarium/runtime/swarm_api.py",
        "vivarium/runtime/inference_engine.py",
        "vivarium/runtime/groq_client.py",
        "vivarium/runtime/safety_validator.py",
    ]

    validator = SyntaxValidator()
    results = []

    for filename in critical_files:
        filepath = Path(filename)
        if not filepath.exists():
            continue

        result = validator.validate_file(filepath)
        if not result.valid:
            results.append(result)

    return results


if __name__ == "__main__":
    # Test the validator
    print("Testing Safety Validator...")

    # Test syntax validation
    good_code = "def hello():\n    print('Hello')\n"
    bad_code = "def hello(\n    print('Hello'\n"

    validator = SyntaxValidator()

    result = validator.validate_python(good_code)
    assert result.valid, "Good code should validate"

    result = validator.validate_python(bad_code)
    assert not result.valid, "Bad code should not validate"

    print("[OK] Syntax validation working")

    # Validate critical files
    print("\nValidating critical files...")
    errors = validate_critical_files()

    if errors:
        print(f"[ERROR] Found {len(errors)} files with errors:")
        for result in errors:
            print(f"\n{result.file_path}:")
            for error in result.errors:
                print(f"  - {error}")
    else:
        print("[OK] All critical files valid")
