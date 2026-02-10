#!/usr/bin/env python3
"""
Experiment Sandbox System
Provides safe experimentation environment for worker agents.
"""

import json
import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

EXPERIMENTS_DIR = Path("experiments")
MANIFEST_FILE = Path("experiments_manifest.json")
CORE_PROTECTED_FILES = [
    "*.py", "grind_spawner*.py", "orchestrator.py", "cost_tracker.py",
    "safety_*.py", "utils.py", "roles.py"
]

logger = logging.getLogger(__name__)

class ExperimentSandbox:
    """Manages safe experimentation environment for worker agents."""

    def __init__(self):
        self.experiments_dir = EXPERIMENTS_DIR
        self.manifest_file = MANIFEST_FILE
        self._ensure_setup()

    def _ensure_setup(self):
        """Ensure experiments directory and manifest exist."""
        self.experiments_dir.mkdir(exist_ok=True)
        if not self.manifest_file.exists():
            self._create_manifest()

    def _create_manifest(self):
        """Create initial experiments manifest."""
        manifest = {
            "experiments": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0",
                "description": "Tracks experimental code that can be safely tested before promotion to main codebase"
            }
        }
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

    def load_manifest(self) -> Dict:
        """Load experiments manifest."""
        with open(self.manifest_file, 'r') as f:
            return json.load(f)

    def save_manifest(self, manifest: Dict):
        """Save experiments manifest."""
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

    def register_experiment(self, name: str, description: str, files: List[str]) -> bool:
        """Register a new experiment in the manifest."""
        try:
            manifest = self.load_manifest()
            experiment_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}"

            manifest["experiments"][experiment_id] = {
                "name": name,
                "description": description,
                "files": files,
                "created": datetime.now().isoformat(),
                "status": "active",
                "promoted": False
            }

            self.save_manifest(manifest)
            logger.info(f"Registered experiment: {experiment_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register experiment {name}: {e}")
            return False

    def get_experiment_path(self, experiment_id: str) -> Path:
        """Get path for experiment files."""
        return self.experiments_dir / experiment_id

    def create_experiment(self, name: str, description: str) -> Optional[str]:
        """Create new experiment directory and register it."""
        try:
            experiment_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}"
            exp_path = self.get_experiment_path(experiment_id)
            exp_path.mkdir(exist_ok=True)

            if self.register_experiment(name, description, []):
                logger.info(f"Created experiment: {experiment_id} at {exp_path}")
                return experiment_id
            return None
        except Exception as e:
            logger.error(f"Failed to create experiment {name}: {e}")
            return None

    def is_core_file_protected(self, filepath: str) -> bool:
        """Check if a file is protected core code."""
        path = Path(filepath)

        # Check against protected patterns
        for pattern in CORE_PROTECTED_FILES:
            if path.match(pattern):
                return True

        # Additional protection for critical files
        protected_names = [
            "orchestrator.py", "cost_tracker.py", "roles.py", "utils.py",
            "safety_audit.py", "safety_gateway.py", "safety_killswitch.py"
        ]

        return path.name in protected_names

    def promote_experiment(self, experiment_id: str, target_files: Optional[List[str]] = None) -> bool:
        """
        Promote approved experiment to main codebase.

        Args:
            experiment_id: ID of experiment to promote
            target_files: Optional list of specific files to promote. If None, promotes all.

        Returns:
            True if promotion successful, False otherwise
        """
        try:
            manifest = self.load_manifest()

            if experiment_id not in manifest["experiments"]:
                logger.error(f"Experiment {experiment_id} not found in manifest")
                return False

            experiment = manifest["experiments"][experiment_id]
            exp_path = self.get_experiment_path(experiment_id)

            if not exp_path.exists():
                logger.error(f"Experiment directory {exp_path} does not exist")
                return False

            # Get files to promote
            files_to_promote = target_files if target_files else experiment.get("files", [])
            if not files_to_promote:
                # If no files specified, promote all Python files in experiment dir
                files_to_promote = [f.name for f in exp_path.glob("*.py")]

            promoted_files = []

            for filename in files_to_promote:
                src_file = exp_path / filename
                dest_file = Path(filename)

                if not src_file.exists():
                    logger.warning(f"File {src_file} not found, skipping")
                    continue

                # Safety check: don't overwrite protected core files without explicit approval
                if self.is_core_file_protected(str(dest_file)):
                    logger.warning(f"File {dest_file} is protected core code - requires manual approval")
                    continue

                # Create backup if destination exists
                if dest_file.exists():
                    backup_file = Path(f"{dest_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                    shutil.copy2(dest_file, backup_file)
                    logger.info(f"Created backup: {backup_file}")

                # Promote the file
                shutil.copy2(src_file, dest_file)
                promoted_files.append(str(dest_file))
                logger.info(f"Promoted: {src_file} -> {dest_file}")

            # Update manifest
            experiment["promoted"] = True
            experiment["promoted_at"] = datetime.now().isoformat()
            experiment["promoted_files"] = promoted_files
            experiment["status"] = "promoted"

            self.save_manifest(manifest)
            logger.info(f"Successfully promoted experiment {experiment_id}: {len(promoted_files)} files")

            return True

        except Exception as e:
            logger.error(f"Failed to promote experiment {experiment_id}: {e}")
            return False

    def list_experiments(self) -> Dict:
        """List all experiments with their status."""
        manifest = self.load_manifest()
        return manifest["experiments"]

    def get_safe_workspace(self, experiment_name: str) -> Optional[Path]:
        """Get safe workspace path for an experiment."""
        experiment_id = self.create_experiment(experiment_name, f"Auto-created workspace for {experiment_name}")
        if experiment_id:
            return self.get_experiment_path(experiment_id)
        return None

# Global instance
sandbox = ExperimentSandbox()

def create_experiment(name: str, description: str) -> Optional[str]:
    """Convenience function to create new experiment."""
    return sandbox.create_experiment(name, description)

def promote_experiment(experiment_id: str, target_files: Optional[List[str]] = None) -> bool:
    """Convenience function to promote experiment."""
    return sandbox.promote_experiment(experiment_id, target_files)

def get_safe_workspace(experiment_name: str) -> Optional[Path]:
    """Convenience function to get safe workspace."""
    return sandbox.get_safe_workspace(experiment_name)

def is_core_protected(filepath: str) -> bool:
    """Convenience function to check if file is core protected."""
    return sandbox.is_core_file_protected(filepath)