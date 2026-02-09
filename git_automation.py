#!/usr/bin/env python3
"""
Git automation module for automatic version control integration.
Handles auto-commits to different branches based on change type.
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class GitAutomation:
    """Handles automatic git operations for swarm changes."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.branches = {
            "swarm_changes": "swarm-changes",
            "pending_review": "pending-review",
            "experiments": "experiments"
        }

    def _run_git_command(self, cmd: List[str]) -> Tuple[bool, str]:
        """Run git command and return success status and output."""
        try:
            result = subprocess.run(
                ["git"] + cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip()

    def get_pending_changes(self) -> Dict[str, List[str]]:
        """Get all pending changes categorized by type."""
        success, output = self._run_git_command(["status", "--porcelain"])
        if not success:
            return {"error": [output]}

        changes = {
            "modified": [],
            "added": [],
            "deleted": [],
            "untracked": []
        }

        for line in output.split("\n"):
            if not line.strip():
                continue

            status = line[:2]
            filepath = line[3:]

            if status.startswith("M"):
                changes["modified"].append(filepath)
            elif status.startswith("A"):
                changes["added"].append(filepath)
            elif status.startswith("D"):
                changes["deleted"].append(filepath)
            elif status.startswith("??"):
                changes["untracked"].append(filepath)

        return changes

    def get_git_status(self) -> Dict[str, str]:
        """Get current git status information."""
        status_info = {}

        # Current branch
        success, branch = self._run_git_command(["branch", "--show-current"])
        status_info["current_branch"] = branch if success else "unknown"

        # Pending changes count
        changes = self.get_pending_changes()
        if "error" not in changes:
            total_changes = sum(len(files) for files in changes.values())
            status_info["pending_changes"] = total_changes
        else:
            status_info["pending_changes"] = "error"

        # Last commit
        success, commit = self._run_git_command(["log", "-1", "--format=%h %s"])
        status_info["last_commit"] = commit if success else "no commits"

        return status_info

    def get_git_diff(self) -> str:
        """Get git diff of current changes."""
        success, diff = self._run_git_command(["diff"])
        if success:
            return diff
        return f"Error getting diff: {diff}"

    def _ensure_branch_exists(self, branch_name: str) -> bool:
        """Ensure the specified branch exists, create if needed."""
        # Check if branch exists
        success, _ = self._run_git_command(["show-ref", "--verify", f"refs/heads/{branch_name}"])
        if success:
            return True

        # Create new branch
        success, output = self._run_git_command(["checkout", "-b", branch_name])
        if success:
            # Switch back to original branch
            self._run_git_command(["checkout", "-"])
            return True

        return False

    def _determine_target_branch(self, files: List[str], change_type: str = "auto") -> str:
        """Determine target branch based on files changed and change type."""
        if change_type == "experiment":
            return self.branches["experiments"]

        # Check for core files that need review
        core_files = [
            "orchestrator.py", "grind_spawner.py", "roles.py",
            "cost_tracker.py", "progress_server.py"
        ]

        for file_path in files:
            if any(core in file_path for core in core_files):
                return self.branches["pending_review"]

        # Default to swarm changes
        return self.branches["swarm_changes"]

    def auto_commit(self, message: str, change_type: str = "auto", files: Optional[List[str]] = None) -> Tuple[bool, str]:
        """
        Automatically commit changes to appropriate branch.

        Args:
            message: Commit message
            change_type: "auto", "experiment", or "core"
            files: Specific files to commit (None = all changes)

        Returns:
            (success, message)
        """
        # Get current branch
        success, current_branch = self._run_git_command(["branch", "--show-current"])
        if not success:
            return False, f"Failed to get current branch: {current_branch}"

        # Determine files to commit
        if files is None:
            changes = self.get_pending_changes()
            if "error" in changes:
                return False, f"Failed to get pending changes: {changes['error'][0]}"

            all_files = []
            for file_list in changes.values():
                all_files.extend(file_list)
            files = all_files

        if not files:
            return True, "No files to commit"

        # Determine target branch
        target_branch = self._determine_target_branch(files, change_type)

        # Ensure target branch exists
        if not self._ensure_branch_exists(target_branch):
            return False, f"Failed to create/access branch: {target_branch}"

        # Switch to target branch if needed
        if current_branch != target_branch:
            success, output = self._run_git_command(["checkout", target_branch])
            if not success:
                return False, f"Failed to switch to {target_branch}: {output}"

        # Add files
        success, output = self._run_git_command(["add"] + files)
        if not success:
            # Switch back to original branch
            if current_branch != target_branch:
                self._run_git_command(["checkout", current_branch])
            return False, f"Failed to add files: {output}"

        # Commit changes
        commit_msg = f"[{change_type}] {message} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        success, output = self._run_git_command(["commit", "-m", commit_msg])

        # Switch back to original branch
        if current_branch != target_branch:
            self._run_git_command(["checkout", current_branch])

        if success:
            return True, f"Successfully committed to {target_branch}: {commit_msg}"
        else:
            return False, f"Failed to commit: {output}"

    def create_pr(self, source_branch: str, target_branch: str = "master", title: str = "", body: str = "") -> Tuple[bool, str]:
        """
        Create a pull request using GitHub CLI.

        Args:
            source_branch: Source branch name
            target_branch: Target branch (default: master)
            title: PR title
            body: PR description

        Returns:
            (success, message/url)
        """
        try:
            # Check if gh CLI is available
            result = subprocess.run(["gh", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "GitHub CLI (gh) not installed or not in PATH"

        # Default title if not provided
        if not title:
            title = f"Auto PR: {source_branch} -> {target_branch}"

        # Default body if not provided
        if not body:
            body = f"Automated pull request from {source_branch}"

        try:
            result = subprocess.run([
                "gh", "pr", "create",
                "--base", target_branch,
                "--head", source_branch,
                "--title", title,
                "--body", body
            ], cwd=self.repo_path, capture_output=True, text=True, check=True)

            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, f"Failed to create PR: {e.stderr.strip()}"


# Global instance
git_automation = GitAutomation()


# Convenience functions
def auto_commit(message: str, change_type: str = "auto", files: Optional[List[str]] = None) -> Tuple[bool, str]:
    """Convenience function for auto-commit."""
    return git_automation.auto_commit(message, change_type, files)


def create_pr(source_branch: str, target_branch: str = "master", title: str = "", body: str = "") -> Tuple[bool, str]:
    """Convenience function for creating PR."""
    return git_automation.create_pr(source_branch, target_branch, title, body)


def get_pending_changes() -> Dict[str, List[str]]:
    """Convenience function for getting pending changes."""
    return git_automation.get_pending_changes()


def get_git_status() -> Dict[str, str]:
    """Convenience function for getting git status."""
    return git_automation.get_git_status()


def get_git_diff() -> str:
    """Convenience function for getting git diff."""
    return git_automation.get_git_diff()